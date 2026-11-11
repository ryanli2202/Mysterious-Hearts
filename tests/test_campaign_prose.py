"""MH-005 route, state, audience and manuscript integration checks."""
import copy
import itertools
import json
import re
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import game_core as core
import campaign_prose as prose
import campaign_dialogue as dialogue
import campaign_flashbacks as memories
import charles_quest as charles
import rei_story as rei
import interpol
import combat
import organisation_guards as guards
from test_major_campaigns import arrive,clear,win,investigate
from flashback_helpers import finish_scene,finish_memories


def script(s,action,args=()):
    dialogue.begin(s,action,args)
    text='\n'.join(b['narration'] for b in s['campaign_dialogue']['beats'])
    finish_scene(s)
    return text


def place_friend(s,who,venue):
    if who in s['world']['cast']:
        s['world']['cast'][who].update(location=venue,journey=None,activity='Available')
        s.get('friendships',{}).setdefault(who,{})['trust']=80
    else:s['world']['npcs'].append(who)


def ready_case(s,key):
    arrive(s,'interpol_hq');partner='fox' if s['player']=='gordon' else 'gordon'
    place_friend(s,partner,'interpol_hq');interpol.begin(s,key)


def case_step(s):
    step=interpol.objective(s);a=interpol.read(s)['active'];partner=a['partner']
    arrive(s,step['venue']);place_friend(s,partner,step['venue']);s['world']['party']=[partner]
    return script(s,'interpol.advance')


def finish_case(s,key):
    ready_case(s,key)
    while interpol.read(s)['active']:
        case_step(s)
        if combat.active(s):
            if combat.active(s).get('scripted_outcome')=='crow_defeat':combat.concede(s);combat.close(s);s['world']['minute']+=1440
            else:win(s)


class CampaignProseTests(unittest.TestCase):
    def test_compiler_matches_shipping_content_and_has_no_directions(self):
        from tools.build_campaign_prose import compiled,CONDITIONS
        conditions=copy.deepcopy(CONDITIONS)
        self.assertEqual(compiled(),prose.library())
        self.assertEqual(CONDITIONS,conditions)
        self.assertEqual(len(prose.library()),120)
        forbidden=(r'\*Mapping:',r'\b(?:runtime|implementation|unimplemented|authoritative|game mechanics)\b',
                   r'(?:Use|Begin with) the complete',r'Apply only',r'\]\(CAMPAIGN',r'\bDo not (?:invent|replay|grant|appoint)')
        for key,scene in prose.library().items():
            self.assertTrue(scene['elements'],key)
            for e in scene['elements']:
                for pattern in forbidden:self.assertNotRegex(e['text'],pattern,key)

    def test_interview_and_operation_phases_never_borrow_the_outcome(self):
        s=core.fresh('fox')
        def text(key,**ctx):return '\n'.join(b['narration'] for b in prose.pages(key,prose.context(s,**ctx)))
        interview=text('FD10',phase='interview');after=text('FD10',phase='after')
        self.assertIn('contractor stopped at the date',interview)
        self.assertNotIn('exterior observations',interview)
        self.assertNotIn('contractor stopped at the date',after)
        self.assertIn('exterior observations',after)
        for key in ('syndicate_witness','syndicate_supply','syndicate_coercion'):
            before=text('FD38',operation=key);after=text('FD38',operation=key,phase='after')
            self.assertTrue(before);self.assertTrue(after)
            self.assertNotEqual(before,after)
            self.assertFalse(set(before.split('\n')) & set(after.split('\n'))- {''})

    def test_reading_choice_and_reload_do_not_commit_early(self):
        s=core.fresh('rei');arrive(s,'rei_home');dialogue.begin(s,'rei_story.advance',(1,))
        d=s['campaign_dialogue'];self.assertGreater(len(d['beats']),3)
        while not d['beats'][d['cursor']].get('reflection'):dialogue.next_line(s)
        with self.assertRaisesRegex(ValueError,'reflection'):dialogue.next_line(s)
        prose.choose_reflection(s,1)
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'story.json';core.save(s,path);s=core.load(path)
        self.assertEqual(s['rei_story']['stage'],0)
        self.assertEqual(s['campaign_dialogue']['narrative_flags']['RD01'],'present')
        finish_scene(s);self.assertEqual(s['rei_story']['stage'],1)
        self.assertEqual(prose.read(s)['flags']['RD01'],'present')
        before=copy.deepcopy(s)
        prose.recap(s)
        self.assertEqual(before,s)
        with self.assertRaises(ValueError):dialogue.next_line(s)

    def test_wrong_authentication_never_promises_invitation(self):
        s=core.fresh('garrett');s['charles_quest']=dict(charles.read(s),step=8,last_day=-1)
        arrive(s,'noodle_shop');s['world']['minute']=3*1440
        text=script(s,'charles_quest.advance',(1,))
        self.assertEqual(charles.read(s)['step'],8)
        self.assertNotIn('private evening invitation followed',text)
        self.assertNotIn('authenticated reply',text)
        self.assertIn('answered the enquiry incorrectly',text)
        with self.assertRaises(ValueError):dialogue.begin(s,'charles_quest.advance',(0,))
        s['world']['minute']+=1440
        text=script(s,'charles_quest.advance',(0,))
        self.assertEqual(charles.read(s)['step'],9)
        self.assertIn('private evening invitation followed',text)

    def test_direct_route_does_not_gain_documents(self):
        s=core.fresh('garrett');arrive(s,charles.LAB);s['world']['minute']=20*60
        for who,a in s['world']['cast'].items():
            if who not in ('garrett','charles'):a['location']='square'
        place_friend(s,'charles',charles.LAB)
        with patch('criminal_dynamics.lab_access',return_value=True):charles.recognise(s)
        self.assertEqual(charles.read(s)['step'],9)
        self.assertEqual([e['title'] for e in charles.read(s)['evidence']],['Direct encounter'])
        finish_memories(s);clear(s,(charles.LAB,),'charles:search');s['world']['minute']=20*60
        text=script(s,'charles_quest.security_action')
        self.assertIn('recognised Charles before the room',text)
        self.assertNotIn('invitation',text.casefold())
        self.assertNotIn('slip',text.casefold())
        self.assertTrue(combat.active(s))

    def test_garrett_entire_route_two_reconciliation_policies(self):
        for choice in (0,1):
            s=core.fresh('garrett')
            for step,spec in enumerate(charles.STEPS):
                finish_memories(s)
                arrive(s,spec[1]);s['world']['minute']=(step+1)*1440+20*60
                for who,a in s['world']['cast'].items():
                    if who not in ('garrett','charles') and a['location']==charles.LAB:a['location']='square'
                if spec[1]==charles.LAB:place_friend(s,'charles',charles.LAB)
                if step in (6,9):
                    clear(s,(spec[1],),'charles:search');s['world']['minute']=(step+1)*1440+20*60
                if step==9:
                    script(s,'charles_quest.security_action');win(s);s['campaign_epilogues']=[]
                if step in (14,16):
                    while charles.garrett_chapters.remaining(s,step):
                        script(s,'charles_quest.security_action');win(s)
                with patch('messaging.initiate'):
                    script(s,'charles_quest.advance',(0 if 5<=step<=8 else choice,))
                self.assertEqual(charles.read(s)['step'],step+1)
            self.assertTrue(charles.read(s)['complete'])
            self.assertEqual(len(charles.read(s)['evidence']),20)
            self.assertEqual(charles.read(s)['ending'],'quiet alliance' if choice==0 else 'guarded reconciliation')
            self.assertIn('GD40',prose.read(s)['read'])

    def test_rei_all_endings_both_resolution_orders(self):
        for ending,order in itertools.product(('leave','lead','destroy'),('successor','richter')):
            s=core.fresh('rei')
            for i,spec in enumerate(rei.SCENES):
                finish_memories(s);arrive(s,spec[1]);script(s,'rei_story.advance',(i%2,))
            for part in (order,'richter' if order=='successor' else 'successor'):
                if part=='successor':
                    arrive(s,'hamayashi_house');script(s,'rei_story.choose',(ending,))
                    if ending=='destroy':
                        self.assertFalse(rei.data(s)['complete'])
                        clear(s,guards.HAMAYASHI,'rei:hamayashi')
                        dialogue.activate_epilogue(s);finish_scene(s)
                else:
                    clear(s,guards.BLACKSTONE,'rei:blackstone');script(s,'rei_story.confront');win(s)
                    dialogue.activate_epilogue(s);finish_scene(s)
                self.assertEqual(rei.data(s)['complete'],rei.data(s)['richter'] and rei.data(s)['hamayashi'] in ('lead','leave','destroyed'))
            self.assertTrue(rei.data(s)['complete'])
            arrive(s,'rei_home');prose.begin_social(s,'RD33');finish_scene(s)
            text=' '.join(b['narration'] for b in s['campaign_dialogue_history'][-1]['beats'])
            markers={'lead':'agreed to help govern','leave':'without his oversight','destroy':'operations were closed'}
            self.assertIn(markers[ending],text)
            for other,marker in markers.items():
                if other!=ending:self.assertNotIn(marker,text)

    def test_boss_failure_has_no_apology_or_release(self):
        s=core.fresh('rei');investigate(s);clear(s,guards.BLACKSTONE,'rei:blackstone')
        script(s,'rei_story.confront');combat.concede(s);combat.close(s)
        s['world']['minute']+=1440;dialogue.activate_epilogue(s)
        text=str(s.get('campaign_dialogue'))
        self.assertNotIn('I am sorry',text);self.assertNotIn('participants could leave',text)
        self.assertFalse(rei.data(s)['richter']);finish_scene(s)

    def test_social_availability_privacy_disclosure_and_no_cross_progress(self):
        s=core.fresh('garrett');s['charles_quest']=dict(charles.read(s),step=12,ending='guarded reconciliation')
        arrive(s,'noodle_shop');place_friend(s,'rei','square')
        with self.assertRaises(ValueError):prose.begin_social(s,'GD27','share')
        place_friend(s,'rei','noodle_shop');before=copy.deepcopy(s['rei_story']) if 'rei_story' in s else None
        prose.begin_social(s,'GD27','private');text=str(s['campaign_dialogue'])
        self.assertNotIn('He’s alive',text);finish_scene(s)
        self.assertNotIn('rei',prose.read(s)['disclosures'])
        prose.begin_social(s,'GD27','share');finish_scene(s)
        self.assertIn('Charles is alive',prose.read(s)['disclosures']['rei'])
        self.assertEqual(s.get('rei_story'),before)
        self.assertNotIn('infiltrat',str(prose.read(s)['disclosures']))
        s['combat']['ruptures'].append('rei')
        with self.assertRaises(ValueError):prose.begin_social(s,'GD27')

    def test_every_optional_scene_has_an_executable_cast_variant(self):
        for key,spec in prose.SOCIAL.items():
            s=core.fresh(spec['player']);arrive(s,spec['venue']);s['world']['minute']=12*60
            if spec['player']=='garrett':s['charles_quest']=dict(charles.read(s),step=spec['minimum'],ending='quiet alliance')
            else:
                rei.data(s).update(stage=spec['minimum'])
                s['campaign_flashbacks']={'completed':list(memories.SCENES)[:3]}
                if key in ('RD32','RD33','RD34','RD35'):rei.data(s).update(richter=True,hamayashi='leave',complete=True)
            cast=spec['cast'] or (['emily','sophie'] if key in ('RD21','RD27') else ['yuriko','emily','sophie'] if key=='RD35' else ['april'] if key=='GD42' else [])
            for who in cast:place_friend(s,who,spec['venue'])
            self.assertEqual(prose.unavailable(s,key),'',key)
            prose.begin_social(s,key,'share','help');self.assertTrue(s['campaign_dialogue']['beats'],key)
            finish_scene(s);self.assertIn(key,prose.read(s)['read'])

    def test_single_friend_and_empty_gathering_do_not_summon_cast(self):
        for visitor in ('emily','sophie'):
            s=core.fresh('rei');rei.data(s)['stage']=6;arrive(s,'square')
            for who in ('emily','sophie'):place_friend(s,who,'square' if who==visitor else 'park')
            before=copy.deepcopy(s['world']);prose.begin_social(s,'RD27');text=str(s['campaign_dialogue']['beats'])
            self.assertIn(visitor.title(),text);self.assertNotIn(('Sophie' if visitor=='emily' else 'Emily'),text)
            finish_scene(s);self.assertEqual(s['world'],before)
        s=core.fresh('rei');rei.data(s).update(stage=6,richter=True,hamayashi='leave',complete=True)
        arrive(s,'rei_home')
        for who in ('yuriko','emily','sophie'):place_friend(s,who,'square')
        prose.begin_social(s,'RD35');self.assertIn('fresh page',str(s['campaign_dialogue']))

    def test_shared_first_meeting_dialogue_identical_and_drawings_distinct(self):
        def memory(key,player):
            return '\n'.join(b['narration'] for b in prose.pages(key,prose.context(core.fresh(player))) if b['mode']=='memory')
        g,r=memory('GD04','garrett'),memory('RD04','rei')
        self.assertEqual(re.findall('“([^”]+)”',g),re.findall('“([^”]+)”',r))
        self.assertNotEqual(g,r)
        self.assertIn('receipt',g);self.assertNotIn('till drawer',g)
        self.assertIn('Different drawing',str(prose.pages('GD41',prose.context(core.fresh('garrett')))))
        g,r=memory('GD15','garrett'),memory('RD08','rei')
        self.assertEqual([t.replace("'",'’').rstrip('.,') for t in re.findall('“([^”]+)”',g)],
                         [t.replace("'",'’').rstrip('.,') for t in re.findall('“([^”]+)”',r)])
        s=core.fresh('garrett');arrive(s,'noodle_shop');place_friend(s,'rei','noodle_shop')
        prose.begin_social(s,'GD03');finish_scene(s)
        self.assertEqual(prose.read(s)['shared_events']['GR-F01']['scene'],'GD04')
        self.assertNotIn('rei',s['campaign_prose']['players'])

    def test_disclosures_only_in_authorised_audience_and_pending_scene_preserved(self):
        s=core.fresh('garrett');s['charles_quest']=dict(charles.read(s),step=12)
        arrive(s,'noodle_shop');place_friend(s,'rei','noodle_shop')
        prose.begin_social(s,'GD27','share');pending=copy.deepcopy(s['campaign_dialogue'])
        with self.assertRaises(ValueError):prose.begin_social(s,'GD27','private')
        self.assertEqual(s['campaign_dialogue'],pending)
        self.assertEqual(prose.knowledge(s,'rei',['garrett','rei']),'')
        finish_scene(s)
        self.assertIn('Charles is alive',prose.knowledge(s,'rei',['garrett','rei']))
        self.assertEqual(prose.knowledge(s,'rei',['garrett','rei','april']),'')
        self.assertEqual(prose.knowledge(s,'april',['garrett','april']),'')
        s['world']['party']=['april']
        with self.assertRaises(ValueError):prose.begin_social(s,'GD27','share')

    def test_fight_reactions_require_resolved_events_and_do_not_repeat(self):
        s=core.fresh('fox')
        f=dict(kind='interpol',opponent='camila',player={'health':90},enemy={'health':90},ally_resources={'health':90},
               exchanges=[dict(records=[dict(side='player',move_id='punch',outcome='missed')]),
                          dict(records=[dict(side='player',move_id='punch',outcome='countered')])])
        prose.resolved_reaction(s,f);self.assertIn('twice',f['log'][0])
        prose.resolved_reaction(s,f);self.assertEqual(len(f['log']),1)
        f.pop('prose_reaction_exchange');f['enemy']['health']=0
        prose.resolved_reaction(s,f);self.assertEqual(len(f['log']),1)
        f['enemy']['health']=90;f['ally_resources']['health']=0
        prose.resolved_reaction(s,f);self.assertEqual(len(f['log']),1)
        prose.after_interpol(s,dict(result='Defeat'), 'ace_clubs',False)
        text=str(s['campaign_epilogues']);self.assertIn('objective’s still open',text);self.assertNotIn('secured the material',text)
        s['campaign_epilogues']=[]
        prose.after_interpol(s,dict(result='Victory'), 'syndicate_witness',True)
        text=str(s['campaign_epilogues']);self.assertIn('protected contact received the witness',text)

    def test_all_24_ace_orders_both_viewpoints_and_reveal_before_guard(self):
        for player in ('fox','gordon'):
            base=core.fresh(player)
            for key in ('blackhaven','rail','shinokami'):finish_case(base,key)
            for order in itertools.permutations(('clubs','hearts','diamonds','spades')):
                s=copy.deepcopy(base)
                for suit in order:
                    key='ace_'+suit;ready_case(s,key);case_step(s)
                    self.assertNotIn('hypotheses',s['interpol']['files'][key])
                    case_step(s)
                    identity=interpol.CASES[key]['reveal']
                    self.assertTrue(interpol.known_identity(s,player,identity))
                    self.assertEqual(len(s['interpol']['files'][key]['hypotheses']),1)
                    for _ in range(3):
                        case_step(s);self.assertEqual(combat.active(s)['kind'],'guard');win(s)
                        self.assertEqual(s['interpol']['files'][key]['step'],2)
                    text=case_step(s)
                    self.assertTrue(combat.active(s));self.assertEqual(combat.active(s)['opponent'],identity)
                    win(s);case_step(s)
                    self.assertTrue(s['interpol']['files'][key]['complete'])
                self.assertTrue(interpol.available(s,'crow_trail'))

    def test_current_crow_defeat_and_legacy_capture_remain_distinct(self):
        for player in ('fox','gordon'):
            s=core.fresh(player)
            for key in ('blackhaven','rail','shinokami','ace_clubs','ace_hearts','ace_diamonds','ace_spades','crow_trail','crow_operation'):finish_case(s,key)
            self.assertTrue(s['interpol']['files']['crow_operation']['crow_defeated_team'])
            self.assertNotIn('crow',s['interpol']['custody'])
            self.assertIn('FD32',prose.read(s)['read']);self.assertIn('FD36',prose.read(s)['read'])
            self.assertEqual(sum(len(f.get('hypotheses',{})) for f in s['interpol']['files'].values()),8)
            self.assertNotIn('FD37',prose.read(s)['read'])
        s=core.fresh('fox');d=interpol.ensure(s)
        d['files']['crow_operation']=dict(step=3,evidence=[dict(finding='The Crow is defeated in this operation; the team secures the command records.')],attempts=0,complete=False)
        d['active']=dict(key='crow_operation',repeatable=False,partner='gordon',participants=['fox','gordon'],party_added=False,started=0)
        text=case_step(s)
        self.assertNotIn('We lost',text);self.assertIn('custody record',text)
        self.assertIn('crow',d['custody']);self.assertTrue(d['files']['crow_operation']['complete'])

    def test_old_active_scene_completes_without_new_choices_or_gate(self):
        s=core.fresh('garrett');arrive(s,'noodle_shop')
        s['campaign_dialogue']=dict(player='garrett',venue='noodle_shop',action='charles_quest.advance',args=[0],cursor=0,beats=[dialogue.beat(narration='Older saved final page')])
        dialogue.next_line(s);self.assertEqual(charles.read(s)['step'],1)
        self.assertIsNone(memories.pending(s));self.assertNotIn('campaign_prose',s)

    def test_hypotheses_and_recaps_do_not_leak_future_findings(self):
        s=core.fresh('fox');ready_case(s,'blackhaven')
        self.assertNotIn('chemical',str(prose.recap(s)))
        case_step(s)
        self.assertNotIn('hypotheses',s['interpol']['files']['blackhaven'])
        case_step(s)
        h=s['interpol']['files']['blackhaven']['hypotheses']['FL01']
        self.assertIn('too common',h['conclusion'])
        self.assertEqual(s['interpol']['files']['blackhaven']['step'],2)
        self.assertFalse(interpol.known_identity(s,'fox','martos'))


if __name__=='__main__':unittest.main()
