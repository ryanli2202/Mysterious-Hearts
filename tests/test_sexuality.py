import copy
import json
import unittest
from unittest.mock import patch

import dating
import game_core as core
import meet_cute as mc
import mysterious_hearts
import sexuality
import town


class SexualityTests(unittest.TestCase):
    def test_contact_profiles_use_read_only_canon_for_new_and_old_saves(self):
        import contact_profiles as profiles
        import social_world
        s=core.fresh('rei')
        for who in s['world']['cast']:
            if who in sexuality.CANON:
                self.assertEqual(profiles.public(s,who,'rei')['Sexuality'],sexuality.CANON[who][1])
                self.assertEqual(social_world.demographics(who)['Sexuality'],sexuality.CANON[who][1])
        row=profiles.ensure(s)['people']['ivan']
        row['fields']['Sexuality']='Straight';row['fields']['Music']='Keep this preference'
        row['visibility']['Sexuality']='private'
        profiles.ensure(s)
        self.assertEqual(profiles.public(s,'ivan','rei')['Sexuality'],'Bisexual')
        self.assertEqual(row['fields']['Music'],'Keep this preference')
        self.assertNotIn('Sexuality',profiles.EDITABLE_FIELDS)
        with self.assertRaisesRegex(ValueError,'canon'):profiles.edit(s,'rei','Sexuality','Bisexual')
        view=profiles.view(s,'ivan','rei')
        view['details']['Sexuality']=dict(value='Straight',minute=999999)
        self.assertEqual(profiles.field_value(view,'Sexuality'),'Bisexual')

    def test_suggestions_and_flirt_reactions_respect_orientation(self):
        import suggestions
        s=core.fresh('rei');s['active']='garrett'
        s['routes']['garrett']['dialogue']='How was your day?'
        result=dict(choices_speaker=core.PLAYERS['rei'],choices=['Hello.','Nice weather.','How are you?','Coffee later?'])
        with patch.object(core.chatgpt_provider,'settings',return_value={'provider':'ollama','model':''}), patch.object(core,'request',return_value={'message':{'content':json.dumps(result)}}) as request:
            suggestions.generate(s,('route','garrett'))
        prompt=request.call_args.args[1]['messages'][0]['content']
        self.assertIn('garrett: straight',prompt)
        self.assertIn('boundaries: []',prompt)
        self.assertEqual(core.emotions.likely_reaction(s,'garrett','Flirtatious'),'guarded')
        self.assertEqual(core.emotions.likely_reaction(s,'naomi','Flirtatious'),'guarded')
        self.assertEqual(core.emotions.likely_reaction(s,'emily','Flirtatious'),'flustered')

    def test_group_text_schema_and_delivery_reject_incompatible_reciprocation(self):
        import messaging
        for player,who,allowed in [('rei','garrett',False),('ivan','elliot',True)]:
            s=core.fresh(player)
            s['groups']['test']=dict(channel='text',name='Friends',members=[who,'sophie'],history=[])
            job=dict(who=who,group=True,key='test',text='Would you date me?',ids=[],reason=None)
            with patch.object(core.chatgpt_provider,'settings',return_value={'provider':'ollama','model':''}), patch.object(core,'request',side_effect=RuntimeError('capture')) as request:
                with self.assertRaisesRegex(RuntimeError,'capture'):messaging.generate(s,job)
            payload=request.call_args.args[1]
            self.assertIn(who+': '+sexuality.CANON[who][1].lower(),payload['messages'][0]['content'])
            self.assertEqual('returned_flirt' in payload['format']['properties']['social_event']['enum'],allowed)
            if not allowed:
                before=copy.deepcopy(s)
                self.assertFalse(messaging.apply(s,job,dict(social_event='returned_flirt',bubbles=['Yes.'])))
                self.assertEqual(s,before)

    def test_canonical_protagonists_and_pair_matrix(self):
        self.assertEqual([sexuality.CANON[p][1] for p in ('rei','garrett','ivan','minsu')],
                         ['Straight','Straight','Bisexual','Straight'])
        for a, (gender_a, orientation_a) in sexuality.CANON.items():
            for b, (gender_b, orientation_b) in sexuality.CANON.items():
                def allows(orientation, same):
                    return orientation == 'Bisexual' or (same if orientation in ('Gay','Lesbian') else not same)
                expected = a != b and allows(orientation_a,gender_a==gender_b) and allows(orientation_b,gender_a==gender_b)
                self.assertEqual(sexuality.compatible(a,b), expected, (a,b))
        self.assertTrue(sexuality.compatible('naomi','amy'))
        self.assertFalse(sexuality.compatible('naomi','emily'))
        self.assertTrue(sexuality.compatible('ivan','elliot'))
        self.assertFalse(sexuality.compatible('ivan','rei'))

    def test_discovery_and_incoming_likes_never_override_orientation(self):
        for player in ('rei','garrett','ivan','minsu'):
            s=core.fresh(player);s['world']['minute']=3*1440+600
            mc.publish(s,'Hello',list(mc.interest_options(s)),['A','B','C'],['portrait'],'Open to either','Flexible')
            for mode in ('Must have','Preferred'):
                for gender in ('Everyone','Men','Women'):
                    mc.preferences(s,18,100,gender,'Open to either',mode)
                    self.assertTrue(all(sexuality.compatible(player,p['who']) for p in mc.feed(s)))
                    if player!='ivan' and gender=='Men':self.assertEqual(mc.feed(s),[])
            mc.preferences(s,18,100,'Everyone','Open to either','Preferred')
            for _ in range(10):s['world']['minute']+=240;mc.tick(s)
            self.assertTrue(all(sexuality.compatible(player,p['who']) for p in mc.ensure(s)['likes']))
            with self.assertRaises(ValueError):mc._match(s,'naomi','Hello',mc.ensure(s)['profile'])

    def test_advances_cannot_unlock_incompatible_romance(self):
        s=core.fresh('rei')
        for who in ('garrett','ivan','naomi','elliot'):
            for _ in range(8):town.social_event(s,who,'returned_flirt')
            self.assertFalse(town.romanceable(s,who))
            self.assertEqual(dating.decision(s,who,'date')[0],'no')
            self.assertFalse(dating.can_confess(s,who))
            self.assertIn('decline clearly',dating.romantic_voice(s,who))
            with self.assertRaises(ValueError):dating.accept(s,who,'date',{})
        s['active']='garrett'
        self.assertEqual(core.choice_tones(s),core.PLATONIC_TONES)
        self.assertNotIn('flirty',' '.join(core.action_choices(s)))
        s=core.fresh('ivan')
        for _ in range(3):town.social_event(s,'elliot','returned_flirt')
        self.assertEqual(s['relationships']['elliot']['status'],'mutual interest')
        self.assertFalse(town.romanceable(s,'valentina'))
        self.assertFalse(town.romanceable(s,'neo'))

    def test_old_matches_close_without_erasing_history(self):
        s=core.fresh('rei');s['world']['minute']=5000
        d=mc.ensure(s)
        d['matches']['ivan']=dict(who='ivan',status='active',messages=[dict(author='them',text='Earlier conversation',minute=1)],
                                  pending=dict(id=1),proposal=dict(status='pending'),dates=[99])
        s['scheduled_events']=[dict(id=99,end=6000,cancelled=False)]
        d['likes']=[dict(who='ivan',status='incoming')]
        mc.ensure(s)
        self.assertEqual(d['matches']['ivan']['status'],'closed')
        self.assertEqual(d['matches']['ivan']['messages'][0]['text'],'Earlier conversation')
        self.assertEqual(d['likes'][0]['status'],'declined')
        self.assertTrue(s['scheduled_events'][0]['cancelled'])
        before=copy.deepcopy(d);mc.ensure(s);self.assertEqual(d,before)
        self.assertFalse(mc.commit_reply(s,'ivan',1,'A stale romantic reply'))

    def test_existing_romance_and_anonymous_feelings_reconcile(self):
        s=core.fresh('rei')
        s['relationships']['garrett']=dict(status='official',attraction=100,trust=95,closeness=90)
        s['date_session']=dict(partner='garrett',started=True)
        sexuality.reconcile(s)
        self.assertEqual(s['relationships']['garrett']['status'],'friends')
        self.assertEqual(s['relationships']['garrett']['trust'],95)
        self.assertNotIn('date_session',s)
        self.assertEqual(s['orientation_ended_dates'][0]['partner'],'garrett')
        mysterious_hearts.ensure(s)['feelings']['garrett']={'rei':90}
        self.assertEqual(mysterious_hearts.feeling(s,'garrett','rei'),0)
        self.assertFalse(mysterious_hearts.eligible(s,'garrett','rei'))
        self.assertTrue(mysterious_hearts.eligible(s,'emily','rei'))

    def test_old_unsent_flirts_are_retired_and_new_mutual_events_rejected(self):
        s=core.fresh('rei');s['active']='garrett'
        s.pop('sexuality_canon_version')
        s['routes']['garrett']['choices']=['A cached romantic suggestion']
        sexuality.reconcile(s)
        self.assertEqual(s['routes']['garrett']['choices'],[])
        data=dict(speaker='Garrett Han',addressee='Rei Takamura',choices_speaker='Rei Takamura',
                  narration='A message arrives.',dialogue='Hello.',memory='',
                  choices=['Hello.','How are you?','Nice weather.','See you later.'])
        for fields in ({'romance_event':'kiss'},{'social_event':'returned_flirt'}):
            with self.assertRaises(ValueError):core.validate_response(dict(data,**fields),s)


if __name__=='__main__':unittest.main()
