import copy
import tempfile
import unittest
from pathlib import Path
import game_core as core
import town
import job_apps as jobs
import gang_members as members
import phone_numbers
import character_types
import groups


class GangCoworkerTests(unittest.TestCase):
    def joined(self, key):
        s = core.fresh('minsu')
        jobs.ensure(s).update(reputation=60, completed=12)
        jobs.progression.join(s, key)
        return s

    def test_roster_presence_contacts_and_isolation(self):
        self.assertEqual(len(members.NAMES), 14)
        self.assertEqual({p['gang'] for p in members.MEMBERS.values()}, {*jobs.progression.GANGS, 'dragons'})
        for key in jobs.progression.GANGS:
            s = self.joined(key)
            names = members.coworkers(s)
            self.assertEqual(len(names), 2)
            town.travel(s, members.MEMBERS[names[0]]['base'])
            for name in names:
                self.assertIn(name, s['world']['npcs'])
                self.assertTrue(phone_numbers.saved_number(s, name))
                self.assertEqual(character_types.kind(name), character_types.TOWN)
                self.assertNotIn(name, s['routes'])
                groups.open_local(s, name)
                groups.close_active(s, 'Done')
            before = copy.deepcopy(s['npc_chats'])
            members.ensure(s)
            self.assertEqual(before, s['npc_chats'])
            town.travel(s, 'square')
            self.assertFalse(set(names) & set(s['world']['npcs']))

    def test_saved_shared_work_and_leaving(self):
        s = self.joined('rail')
        names = members.coworkers(s)
        jobs.accept(s, 'crew')
        a = jobs.ensure(s)['pending']
        self.assertEqual(a['coworkers'], names)
        self.assertEqual(a['venue'], 'saints_depot')
        with self.assertRaises(ValueError): jobs.resolve(s, 0)
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'save.json'
            core.save(s, path)
            s = core.load(path)
        town.travel(s, a['venue'])
        result = jobs.resolve(s, 0)
        for name in names:
            self.assertIn(name, result)
        self.assertEqual(jobs.ensure(s)['gang']['standing'], 1)
        jobs.progression.leave(s)
        self.assertEqual(members.coworkers(s), [])
        self.assertNotIn('coworkers', jobs.contract_spec(s, 'crew'))
        self.assertTrue(phone_numbers.saved_number(s, names[0]))

    def test_old_pending_and_excluded_factions(self):
        s = self.joined('lantern')
        d = jobs.ensure(s)
        d['pending'] = dict(kind='contract', key='crew', venue='downtown', started=0, deadline=s['world']['minute']+1440)
        before = copy.deepcopy(d['pending'])
        jobs.ensure(s)
        self.assertEqual(before, d['pending'])
        for name in ('Shinokami', 'Syndicate', 'My crew'):
            d['gang'] = dict(name=name, role='Founder', standing=0)
            self.assertEqual(members.coworkers(s), [])
        s = core.fresh('garrett')
        jobs.ensure(s)
        self.assertEqual(len(members.coworkers(s)), 2)
        self.assertEqual(jobs.contract_spec(s, 'crew')['venue'], 'syndicate')

    def test_unmet_number_is_not_a_membership_shortcut(self):
        s = core.fresh('minsu')
        with self.assertRaises(ValueError):
            phone_numbers.add(s, phone_numbers.NUMBERS[members.NAMES[0]])


if __name__ == '__main__':
    unittest.main()
