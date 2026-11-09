import copy
import tempfile
import unittest
from pathlib import Path

import game_core as core
import job_apps as jobs
import crime_diplomacy as dip
import gang_members as members
import phone_numbers


class GarrettStatusTests(unittest.TestCase):
    def test_leader_and_workers_start_established(self):
        s = core.fresh('garrett')
        d = jobs.ensure(s)
        self.assertEqual(d['story_membership']['faction'], 'Red Dragons')
        self.assertEqual(d['affiliations'], ['Red Dragons'])
        self.assertIsNone(d['membership'])
        self.assertEqual(dip.relation(dip.ensure(s), 'dragons'), 95)
        self.assertEqual(dip.relation(dip.ensure(s), 'syndicate'), 35)
        self.assertEqual(members.coworkers(s), ['Mina Cho', 'Anton Bellamy'])
        for name in members.coworkers(s):
            chat = s['npc_chats'][name]
            self.assertEqual(chat['connection'], dict(status='established colleagues', trust=80, closeness=35))
            self.assertTrue(phone_numbers.saved_number(s, name))
            self.assertIn('Boss', chat['history'][0]['text'])
            self.assertIn('established Red Dragons leader', members.context(s, name)['established_relationship'])
        before = copy.deepcopy(s['npc_chats'])
        jobs.ensure(s)
        self.assertEqual(s['npc_chats'], before)

    def test_legacy_deltas_save_load_and_no_repeated_boost(self):
        s = core.fresh('garrett'); jobs.ensure(s)
        b = dip.ensure(s)
        b.pop('dragons_standing_v1'); b['relations']['dragons'] = 25
        name = 'Mina Cho'; chat = s['npc_chats'][name]
        chat.pop('garrett_worker_origin_v1')
        chat['connection'].update(trust=25, closeness=10, status='familiar face')
        history = copy.deepcopy(chat['history'])
        jobs.ensure(s); dip.ensure(s)
        self.assertEqual(chat['connection'], dict(status='familiar face', trust=70, closeness=45))
        self.assertEqual(chat['history'], history)
        self.assertEqual(b['relations']['dragons'], 85)
        chat['connection'].update(trust=20, closeness=5)
        b['relations']['dragons'] = 40
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder)/'garrett.json'
            core.save(s, path); restored = core.load(path)
        jobs.ensure(restored)
        self.assertEqual(restored['npc_chats'][name]['connection']['trust'], 20)
        self.assertEqual(restored['npc_chats'][name]['connection']['closeness'], 5)
        self.assertEqual(dip.ensure(restored)['relations']['dragons'], 40)
        import town_npc_system
        town_npc_system.familiarity(restored, 'Anton Bellamy')
        self.assertEqual(restored['npc_chats']['Anton Bellamy']['connection']['status'], 'established colleagues')
        self.assertEqual(restored['npc_chats']['Anton Bellamy']['connection']['trust'], 80)

    def test_other_protagonists_keep_normal_coworker_baseline(self):
        s = core.fresh('minsu')
        jobs.ensure(s).update(reputation=60, completed=12)
        jobs.progression.join(s, 'lantern')
        for name in members.coworkers(s):
            self.assertEqual(s['npc_chats'][name]['connection']['trust'], 35)
            self.assertEqual(s['npc_chats'][name]['connection']['closeness'], 0)
            self.assertIsNone(members.context(s, name)['established_relationship'])


if __name__ == '__main__':
    unittest.main()
