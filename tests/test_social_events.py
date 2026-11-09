import consequences
import copy
import tempfile
import unittest
from pathlib import Path

import game_core as core
import groups
import town
from date_fixtures import finish_date, invite


class SocialEvents(unittest.TestCase):
    def test_group_flirt_is_witnessed_but_private_text_is_private(self):
        s = core.fresh('rei')
        for who in ('emily', 'amy'):
            s['relationships'][who]['status'] = 'dating'
        gid = groups.create_text(s, 'Practice', ['emily','sophie'])
        reply = dict(narration='A text arrives.', choices=['Hi.', 'Thanks.', 'Ha!', 'You look good.'],
                     lines=[dict(speaker=core.CONTACTS[m][0],text='Hey.') for m in ['emily','sophie']],
                     social_event='flirt', social_target='sophie')
        groups.commit(s,gid,'Sophie, looking good.',reply)
        self.assertEqual(s['relationships']['emily']['jealousy'],20)
        self.assertFalse(s['relationships']['amy'].get('jealousy'))
        self.assertEqual(core.emotions.current(s, 'emily'), 'jealous')
        self.assertEqual(core.emotions.current(s, 'amy'), 'content')
        s['active']='sophie'
        scene=dict(narration='Her phone lights up.',dialogue='Hey.',memory='A text.',choices=reply['choices'],
                   social_event='flirt')
        core.commit(s,'Another compliment.',scene)
        self.assertEqual(s['relationships']['emily']['jealousy'],20)
        s['active']='amy'
        core.commit(s,'I flirted with Sophie.',dict(scene,social_event='disclosed_flirt'))
        self.assertEqual(s['relationships']['amy']['jealousy'],20)

    def test_breakups_preserve_cause(self):
        for cause, kind in [('agreement','amicable'),('mistreatment','volatile'),('cheating','volatile')]:
            s=core.fresh()
            r=s['relationships']['emily']
            r['status']='official'
            if cause=='mistreatment':
                for _ in range(2): town.social_event(s,'emily','mistreatment')
            elif cause=='cheating':
                town.betrayal(s,'sophie','kiss')
                consequences.disclose(s, 0, 'emily')
                town.relationship(s,'emily','breakup')
            else: town.social_event(s,'emily','agreed_breakup')
            self.assertEqual(r['breakups'][-1]['kind'],kind)
            self.assertIn('breakup',r['firsts'])
            self.assertNotIn(r['status'],town.ROMANTIC_STATUSES)

    def test_male_romance_unlocks_only_on_reciprocation(self):
        s=core.fresh('ivan')
        town.social_event(s,'elliot','flirt')
        self.assertNotIn('elliot',s['relationships'])
        for _ in range(3): town.social_event(s,'elliot','returned_flirt')
        town.summon(s,'elliot')
        finish_date(s, 'elliot')
        invite(s, 'elliot', 'official')
        self.assertEqual(s['relationships']['elliot']['status'],'official')
        town.betrayal(s,'sophie','kiss')
        consequences.disclose(s, 0, 'elliot')
        self.assertEqual(s['relationships']['elliot']['status'],'strained')
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'story.json'
            core.save(s,path)
            self.assertEqual(core.load(path)['relationships']['elliot'],s['relationships']['elliot'])

    def test_local_conversation_declines_romance_without_progression(self):
        s = core.fresh('ivan')
        s['world']['npcs'] = ['Theo']
        response = dict(narration='Theo shakes his head gently.',
                        lines=[dict(speaker='Theo', text='No, thank you. I am happy to talk about books.')],
                        emotions={'ivan': 'content', 'Theo': 'content'},
                        choices=[], suggestions_deferred=True,
                        social_event='flirt', social_target='Theo')
        before = copy.deepcopy(s)
        with self.assertRaisesRegex(ValueError, 'cannot create romantic progression'):
            town.commit_npc(s, 'Theo', 'Dinner with me?', dict(response, social_event='returned_flirt'))
        self.assertEqual(s, before)
        town.commit_npc(s, 'Theo', 'Dinner with me?', response)
        self.assertEqual(s['npc_chats']['Theo']['history'][-1]['text'], response['lines'][0]['text'])
        self.assertFalse(town.romanceable(s, 'Theo'))
        self.assertNotIn('Theo', s['relationships'])
        self.assertNotIn('attraction', s['npc_chats']['Theo']['connection'])
        self.assertFalse(s.get('date_session'))
