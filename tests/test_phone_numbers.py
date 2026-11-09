import copy
import tempfile
from pathlib import Path
import unittest

import game_core as core
import hidden_cast
import meet_cute
import phone_numbers as numbers
import town


class PhoneNumberTests(unittest.TestCase):
    def setUp(self):self.s=core.fresh('rei')

    def test_every_named_resident_has_a_unique_stable_number(self):
        residents=set(core.CONTACTS)|{n[0] for n in town.NPCS}|{n[0] for n in town.VENUE_STAFF.values()}|{town.RICHTER}
        self.assertEqual(residents,set(numbers.NUMBERS))
        self.assertEqual(len(set(numbers.NUMBERS.values())),len(residents))
        for who in residents-{'charles'}:
            self.assertEqual(numbers.number(self.s,who),numbers.number(core.fresh('minsu'),who))
            self.assertTrue(numbers.NUMBERS[who].startswith('120255501'))

    def test_accepts_formatted_and_plain_numbers_without_duplicate_contacts(self):
        number=numbers.number(self.s,'lena')
        self.assertEqual(numbers.add(self.s,number),'lena')
        count=len(numbers.ensure(self.s)['contacts'])
        history=copy.deepcopy(self.s['routes']['lena']['history'])
        self.assertEqual(numbers.add(self.s,numbers.NUMBERS['lena'][1:]),'lena')
        self.assertEqual(len(numbers.ensure(self.s)['contacts']),count)
        self.assertEqual(self.s['routes']['lena']['history'],history)
        self.assertTrue(hidden_cast.contact(self.s,'lena'))
        self.assertFalse(hidden_cast.ensure(self.s)['lena']['met'])
        self.assertFalse(hidden_cast.visible_place(self.s,'lena_home'))

    def test_invalid_unknown_and_self_numbers_leave_state_unchanged(self):
        numbers.ensure(self.s)
        before=copy.deepcopy(self.s)
        for value in ('abc','555','+44 202 555 0100','2025559999',numbers.number(self.s,'rei')):
            with self.assertRaises(ValueError):numbers.add(self.s,value)
            self.assertEqual(self.s,before)

    def test_existing_save_migration_does_not_reveal_hidden_numbers(self):
        d=numbers.ensure(self.s)
        self.assertIn('emily',d['contacts'])
        self.assertIn('rei',d['contacts'])
        self.assertNotIn('lena',d['contacts'])
        self.assertEqual(numbers.context(self.s,['lena']),{})

    def test_local_resident_number_creates_a_text_contact(self):
        numbers.add(self.s,numbers.number(self.s,'Maya'))
        self.assertIn('Maya',self.s['npc_chats'])
        self.assertEqual(self.s['groups']['npc:Maya']['channel'],'text')
        self.assertNotIn('Maya',self.s['world']['party'])

    def test_accepted_meet_cute_exchange_shares_and_saves_actual_number(self):
        self.s['world']['minute']=600
        meet_cute.publish(self.s,'Hi',['Drawing'],['A','B','C'],['portrait'],'Open to either','Evenings')
        m=meet_cute._match(self.s,'lena','Hello',meet_cute.ensure(self.s)['profile'])
        m['turns']=3
        meet_cute.request_numbers(self.s,'lena')
        self.assertIsNone(numbers.saved_number(self.s,'lena'))
        self.s['world']['minute']+=200
        meet_cute.tick(self.s)
        actual=numbers.number(self.s,'lena')
        self.assertEqual(numbers.saved_number(self.s,'lena'),actual)
        self.assertIn(actual,m['messages'][-1]['text'])
        self.assertEqual(m['phone_number'],actual)
        self.assertEqual(numbers.ensure(self.s)['contacts']['lena']['source'],'Meet-Cute')
        with tempfile.TemporaryDirectory(dir=core.ROOT/'.test-tmp') as folder:
            path=Path(folder)/'story.json';core.save(self.s,path);loaded=core.load(path)
        self.assertEqual(loaded['phone_numbers'],self.s['phone_numbers'])
        self.assertTrue(hidden_cast.contact(loaded,'lena'))
        self.assertFalse(hidden_cast.ensure(loaded)['lena']['met'])

    def test_adding_a_number_updates_existing_match(self):
        meet_cute.publish(self.s,'Hi',['Drawing'],['A','B','C'],['portrait'],'Open to either','Evenings')
        m=meet_cute._match(self.s,'lena','Hello',meet_cute.ensure(self.s)['profile'])
        numbers.add(self.s,numbers.number(self.s,'lena'))
        self.assertTrue(m['numbers'])
        self.assertEqual(m['phone_number'],numbers.saved_number(self.s,'lena'))


if __name__=='__main__':unittest.main()
