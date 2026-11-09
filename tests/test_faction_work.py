import copy
import tempfile
from pathlib import Path
import unittest
from unittest.mock import patch
import game_core as core
import crime_operations as ops
import faction_work as work
import world_loop as loop
import town
import four_aces
import phone_apps


def workplace(player='ivan',who='camila',minute=2*1440+12*60):
    s=core.fresh(player);s['world']['minute']=minute
    shift=work.appointment(who,minute);key=ops.site_of(shift[1])
    town.travel(s,key);ops.enter(s,key,'reception')
    if shift[1].endswith('_briefing'):ops.enter(s,key,'briefing')
    s['world']['cast'][who].update(location=shift[1],journey=None,activity=shift[2])
    return s,key


class WorkTests(unittest.TestCase):
    def test_shifts_rank_and_no_invented_memberships(self):
        for who in ('martos','camila'):
            self.assertEqual(work.appointment(who,2*1440+10*60)[1],'site_07_reception')
            self.assertIsNone(work.appointment(who,10*60))
        self.assertEqual(work.appointment('valentina',11*60)[1],'site_04_briefing')
        self.assertIsNone(work.appointment('neo',11*60))
        for who in four_aces.IDS:
            for day in range(4):
                shift=work.appointment(who,day*1440+18*60)
                if shift:self.assertTrue(ops.permitted(core.fresh('rei'),who,ops.site_of(shift[1])))
        self.assertFalse(ops.authority('camila','site_06'))

    def test_actual_clock_arrives_via_clearance_path(self):
        s=core.fresh('rei');s['world']['minute']=2*1440+12*60
        actor=s['world']['cast']['camila'];actor.update(location='downtown',journey=None)
        with patch('autonomy.control',return_value=False),patch('autonomy.tick'):
            for expected in ('site_07','site_07_reception','site_07_briefing'):
                loop.advance(s,1);self.assertEqual(actor['location'],expected)
        self.assertNotIn('camila',str(ops.read(s)).lower())
        self.assertNotIn('site_07_briefing',phone_apps.location_people(s))
        self.assertTrue(all('Site 07 · briefing' not in text for text in s['world']['log']))

    def test_denied_npc_path_and_party_not_teleported(self):
        s=core.fresh('rei')
        self.assertEqual(work.next_stop(s,'neo','site_01_briefing'),'site_01')
        s['world']['cast']['neo']['location']='site_01'
        self.assertEqual(work.next_stop(s,'neo','site_01_briefing'),'site_01_reception')
        s['world']['minute']=2*1440+12*60;s['world']['party']=['camila']
        s['world']['cast']['camila'].update(location=s['world']['location'],journey=None)
        with patch('autonomy.control',return_value=False),patch('autonomy.tick'):
            loop.advance(s,1)
        self.assertEqual(s['world']['cast']['camila']['location'],s['world']['location'])

    def test_joint_decision_records_both_and_pays_once(self):
        s,key=workplace();ops.begin(s,key,'briefing','camila')
        with tempfile.TemporaryDirectory(dir=core.ROOT/'.test-tmp') as folder:
            path=Path(folder)/'joint.json';core.save(s,path);s=core.load(path)
        self.assertEqual(ops.read(s)['active']['colleague'],'camila')
        before=s['world']['money'];ops.resolve(s,0)
        self.assertEqual(s['world']['money'],before+160)
        self.assertIn('Joint review',ops.read(s)['history'][-1]['text'])
        self.assertTrue(ops.context(s,'camila')['recent'])
        self.assertFalse(ops.context(s,'rei')['recent'])
        with self.assertRaises(ValueError):ops.resolve(s,0)

    def test_absent_offshift_and_new_listener_block_before_mutation(self):
        s,key=workplace();ops.begin(s,key,'command','camila')
        s['world']['cast']['rei'].update(location=s['world']['location'],journey=None)
        s['crime_operations']['people']['rei']=dict(permits={key:dict(until=s['world']['minute']+60)},sites={},history=[],active=None)
        before=copy.deepcopy(s)
        with self.assertRaises(ValueError):ops.resolve(s,0)
        self.assertEqual(s,before)
        s['world']['cast']['rei']['location']='square'
        s['world']['minute']=2*1440+17*60
        with self.assertRaises(ValueError):ops.resolve(s,0)
        ops.abandon(s)

    def test_cover_work_does_not_reveal_ace_or_oculus(self):
        s,key=workplace('rei','martos',2*1440+10*60)
        ops.begin(s,key,'reception','martos');ops.resolve(s,0)
        text=str(ops.context(s,'rei'))
        self.assertNotIn('Martos is the Ace',text)
        import crime_sites
        self.assertFalse(crime_sites.affiliation_known(s,key))


if __name__=='__main__':unittest.main()
