import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import game_core as core
import memory_store as memory
import suggestions
import scheduled_events
import story_calendar
import groups


def response(s,dialogue='hello there'):
    return dict(narration='A message arrives.',dialogue=dialogue,speaker=core.CONTACTS[s['active']][0],
                addressee=core.PLAYERS[s['player']],emotions={s['player']:'content',s['active']:'content'},
                conversation_channel='text',bond_moments={s['active']:'none'},social_event='none',input_tone='Other')


class MemoryStoreTests(unittest.TestCase):
    def test_migration_preserves_sources_and_is_idempotent(self):
        s=core.fresh('rei'); r=s['routes']['emily']
        r['memory']='We made a promise about the blue origami crane.'
        r['history']=[dict(role='user',content='I promise to bring the crane.',minute=840),
                      dict(role='assistant',content=json.dumps(dict(dialogue='My favourite flower is the iris.',memory='Older cumulative summary.')),minute=840)]
        s['shared_events']=[dict(text='An old shared birthday.',minute=800,witnesses=['emily'])]
        original=copy.deepcopy(s)
        memory.sync(s); count=len(s['memory_store']['records']); memory.sync(s)
        self.assertEqual(count,len(s['memory_store']['records']))
        for key,value in original.items(): self.assertEqual(s[key],value)
        texts=[r['text'] for r in s['memory_store']['records'].values()]
        self.assertIn(r['memory'],texts); self.assertIn('Older cumulative summary.',texts)
        self.assertIn('An old shared birthday.',texts)
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'story.json'; core.save(s,path); loaded=core.load(path)
            self.assertEqual(loaded['routes'],s['routes'])
            self.assertEqual(loaded['memory_store'],s['memory_store'])

    def test_private_claims_and_corrections_never_become_public_facts(self):
        s=core.fresh('rei')
        memory.utterance(s,'old','My favourite flower is the iris.','emily',['rei','emily'],1)
        memory.utterance(s,'new','My favourite flower is the rose.','emily',['rei','emily'],2)
        memory.utterance(s,'rumour','I heard Sophie won a million dollars.','emily',['rei','emily'],3)
        rows=memory.retrieve(s,'emily','favourite flower',20)
        self.assertTrue(any('rose' in r['text'] for r in rows))
        self.assertFalse(any('iris' in r['text'] for r in rows))
        self.assertTrue(any('iris' in r['text'] for r in s['memory_store']['records'].values()))
        self.assertTrue(any(r['kind']=='belief' for r in rows))
        self.assertEqual(memory.retrieve(s,'sophie','million flower'),[])
        self.assertEqual(memory.retrieve(s,'amy','million flower'),[])

    def test_correction_only_reaches_its_recorded_audience(self):
        s=core.fresh('rei')
        memory.utterance(s,'group-old','My favourite flower is the iris.','emily',['rei','emily','sophie'],1)
        memory.utterance(s,'private-new','My favourite flower is the rose.','emily',['rei','emily'],2)
        self.assertTrue(any('iris' in r['text'] for r in memory.retrieve(s,'sophie','flower')))
        self.assertFalse(any('rose' in r['text'] for r in memory.retrieve(s,'sophie','flower')))
        self.assertTrue(any('rose' in r['text'] for r in memory.retrieve(s,'emily','flower')))

    def test_retrieval_is_read_only_and_suggestions_never_become_memories(self):
        s=core.fresh('rei')
        s['routes']['emily']['history']=[dict(role='assistant',content=json.dumps(dict(dialogue='hi', choices=['We secretly married.'])))]
        before=copy.deepcopy(s)
        rows=memory.retrieve(s,'emily','married')
        self.assertEqual(s,before)
        self.assertFalse(any('secretly married' in r['text'] for r in rows))

    def test_agreed_plan_cancellation_keeps_evidence_but_resolves_recall(self):
        import encounter_context
        s=core.fresh('rei')
        encounter_context.record(s,dict(meeting_plans=[dict(who='emily',status='agreed',details='Tea at the cafe tomorrow')]),['emily'])
        encounter_context.record(s,dict(meeting_plans=[dict(who='emily',status='cancelled',details='Tea at the cafe tomorrow')]),['emily'])
        rows=memory.retrieve(s,'emily','Tea')
        self.assertTrue(any(r['status']=='cancelled' for r in rows))
        self.assertFalse(any(r['status']=='agreed' for r in rows))
        self.assertTrue(any(r['status']=='agreed' for r in s['memory_store']['records'].values()))

    def test_proposal_and_missed_event_are_not_shared_attendance(self):
        s=core.fresh('rei'); s['world']['minute']=480
        e=scheduled_events.create(s,'Tea','2050-01-01','10:00','cafe',['emily'],60)
        self.assertEqual(e['memory_phase'],'planned')
        core.town.loop.advance(s,180)
        self.assertEqual(e['memory_phase'],'missed')
        self.assertNotIn('rei',e['attendees']); self.assertIn('emily',e['attendees'])
        rows=memory.retrieve(s,'emily','Tea cafe',20)
        self.assertTrue(any(r['status']=='missed' for r in rows))
        self.assertFalse(any(r['status']=='planned' for r in rows))
        self.assertFalse(any('Tea' in r['text'] for r in memory.retrieve(s,'sophie','Tea')))

    def test_legacy_appointment_does_not_invent_attendance(self):
        s=core.fresh('rei'); s['scheduled_events']=[dict(id='old',title='Tea',venue='cafe',guests=['emily'],start=100,end=160,cancelled=False)]
        memory.sync(s)
        self.assertNotIn('attendees',s['scheduled_events'][0])
        self.assertTrue(any(r['status']=='attendance unknown' for r in memory.retrieve(s,'emily','Tea')))

    def test_relevant_old_memory_and_open_promise_survive_many_turns(self):
        s=core.fresh('rei')
        memory.utterance(s,'promise','I promise to bring the blue origami crane.','rei',['rei','emily'],1)
        for i in range(60): memory.utterance(s,str(i),'A routine chat about coffee.','emily',['rei','emily'],i+2)
        self.assertTrue(any('crane' in r['text'] for r in memory.retrieve(s,'emily','our promise')))


class ManualSuggestionsTests(unittest.TestCase):
    def test_response_commits_without_second_call_or_choices(self):
        s=core.fresh('rei'); old=s['routes']['emily']['memory']='An old memory worth keeping.'
        with patch.object(core,'request',return_value={'message':{'content':json.dumps(response(s))}}) as request:
            result=core.generate(s,'hello'); self.assertEqual(request.call_count,1)
            schema=request.call_args.args[1]['format']
            self.assertNotIn('choices',schema['properties']); self.assertNotIn('memory',schema['properties'])
        core.commit(s,'hello',result)
        self.assertEqual(s['routes']['emily']['choices'],[])
        self.assertEqual(s['routes']['emily']['memory'],old)
        self.assertTrue(suggestions.ready(s,('route','emily')))

    def test_manual_generation_is_isolated_and_stale_results_rejected(self):
        s=core.fresh('rei'); s['routes']['emily']['dialogue']='What a day.'
        target=('route','emily'); before=copy.deepcopy(s)
        answer=dict(choices_speaker=core.PLAYERS['rei'],choices=['Long day?', 'Want to talk?', 'Coffee later?', 'You made mine better.'])
        with patch.object(core,'request',return_value={'message':{'content':json.dumps(answer)}}) as req:
            lines=suggestions.generate(copy.deepcopy(s),target,'main')
            self.assertEqual(req.call_count,1)
            self.assertEqual(set(req.call_args.args[1]['format']['properties']),{'choices','choices_speaker'})
        self.assertEqual(before,s)
        stamp=suggestions.stamp(s,target)
        self.assertTrue(suggestions.apply(s,target,'main',stamp,lines))
        self.assertEqual(s['turn'],before['turn']); self.assertEqual(s['world'],before['world'])
        self.assertNotIn('personal',s['routes']['emily']['suggestions_requested'])
        s['turn']+=1
        self.assertFalse(suggestions.apply(s,target,'personal',stamp,lines))

    def test_followup_does_not_require_generated_choices(self):
        import messaging
        s=core.fresh('rei'); messaging.initiate(s,'emily','An independent thought.')
        s['world']['minute']+=10
        job=messaging.next_job(s)
        self.assertIsNotNone(job)
        messaging.apply(s,job,dict(bubbles=['hi'],moment='none',pause_minutes=0))
        r=s['routes']['emily']
        self.assertEqual(r['choices'],[]); self.assertTrue(r['suggestions_deferred'])

    def test_group_response_has_no_automatic_suggestions(self):
        s=core.fresh('rei'); gid=groups.create_text(s,'Friends',['emily','sophie'])
        data=dict(narration='A message arrives.',lines=[dict(speaker='Emily Fields',text='hi'),dict(speaker='Sophie Parker',text='hey')],
                  emotions={'rei':'content','emily':'content','sophie':'content'},bond_moments={'emily':'none','sophie':'none'},input_tone='Other')
        with patch.object(core,'request',return_value={'message':{'content':json.dumps(data)}}) as req:
            result=groups.generate(s,gid,'hey')
            self.assertEqual(req.call_count,1)
            for field in ('choices','personal_choices','action_choices'): self.assertNotIn(field,req.call_args.args[1]['format']['properties'])
        groups.commit(s,gid,'hey',result)
        self.assertEqual(s['groups'][gid]['choices'],[])
        self.assertTrue(suggestions.ready(s,('group',gid)))
