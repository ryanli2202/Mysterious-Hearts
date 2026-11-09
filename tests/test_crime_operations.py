import copy
import json
from pathlib import Path
import tempfile
import unittest
import game_core as core
import crime_operations as ops
import crime_sites as sites
import town
import world_loop
import artwork


def visit(s,key):
    if s['world']['location']!=key: town.travel(s,key)
    ops.enter(s,key,'reception')


def qualify(s,key):
    visit(s,key)
    for _ in range(2):
        ops.begin(s,key,'reception');ops.resolve(s,0)
        s['world']['minute']+=1440
    ops.request_pass(s,key)


class OperationsTests(unittest.TestCase):
    def test_all_receptions_enterable_with_art_and_no_free_restricted_entry(self):
        for key in sites.SITES:
            s=core.fresh('rei');visit(s,key)
            self.assertEqual(s['world']['location'],key+'_reception')
            self.assertEqual(artwork.scene_art(s['world']['location']),'locations/'+key+'_interior')
            from PIL import Image
            with Image.open(core.ROOT/'assets'/'ui'/'locations'/(key+'_interior.png')) as art:
                self.assertEqual(art.size,(1536,1024))
            import phone_map
            class MapState:
                state=s
            self.assertEqual(phone_map.MapView.player_position(MapState()),phone_map.POINTS[key])
            before=copy.deepcopy(s)
            with self.assertRaises(ValueError): ops.enter(s,key,'briefing')
            self.assertEqual(before,s)
            ops.exit_site(s,key);self.assertEqual(s['world']['location'],key)

    def test_direct_and_companion_bypasses_rejected(self):
        s=core.fresh('ivan')
        with self.assertRaises(ValueError): town.travel(s,'site_04_briefing')
        visit(s,'site_04')
        s['world']['cast']['rei'].update(location='site_04_reception',journey=None)
        s['world']['party']=['rei']
        with self.assertRaises(ValueError): ops.enter(s,'site_04','briefing')
        s['world']['party']=[];ops.enter(s,'site_04','briefing')
        self.assertTrue(ops.authority('valentina','site_04'))
        self.assertFalse(ops.authority('valentina','site_08'))
        self.assertFalse(ops.authority('neo','site_01'))

    def test_scoped_pass_expiry_and_no_membership(self):
        s=core.fresh('garrett');qualify(s,'site_01')
        self.assertTrue(ops.permitted(s,'garrett','site_01'))
        self.assertFalse(ops.permitted(s,'garrett','site_02'))
        ops.enter(s,'site_01','briefing');ops.begin(s,'site_01','briefing')
        s['world']['minute']+=1440;world_loop.ensure(s)
        self.assertEqual(s['world']['location'],'site_01_reception')
        with self.assertRaises(ValueError): ops.resolve(s,0)
        ops.abandon(s)
        self.assertFalse(ops.authority('garrett','site_01'))

    def test_oculus_stays_secret_and_public_work_cannot_unlock_it(self):
        s=core.fresh('rei');visit(s,'site_07')
        for _ in range(2):
            ops.begin(s,'site_07','reception');ops.resolve(s,0);s['world']['minute']+=1440
        with self.assertRaises(ValueError): ops.request_pass(s,'site_07')
        self.assertFalse(sites.affiliation_known(s,'site_07'))
        self.assertNotIn('Syndicate',ops.hierarchy(s,'site_07'))

    def test_saved_order_rewards_once_and_records_hierarchy_consequences(self):
        s=core.fresh('ivan');visit(s,'site_06');ops.enter(s,'site_06','briefing');ops.begin(s,'site_06','command')
        self.assertIn('Ace',ops.read(s)['active']['issuer'])
        with tempfile.TemporaryDirectory(dir=core.ROOT/'.test-tmp') as folder:
            path=Path(folder)/'interiors.json';core.save(s,path);s=core.load(path)
        balance=s['world']['money'];ops.resolve(s,1)
        self.assertEqual(s['world']['money'],balance+240)
        self.assertEqual(ops.progress(s,'site_06')['harm'],2)
        with self.assertRaises(ValueError): ops.resolve(s,1)
        with self.assertRaises(ValueError): ops.begin(s,'site_06','command')
        self.assertFalse(ops.context(s,'emily')['recent'])

    def test_expired_load_ejects_and_read_only_queries_preserve_old_save(self):
        s=core.fresh('rei');before=copy.deepcopy(s)
        ops.progress(s,'site_01');ops.hierarchy(s,'site_01');ops.access_text(s,'site_01')
        self.assertEqual(before,s)
        qualify(s,'site_02');ops.enter(s,'site_02','briefing');s['world']['minute']+=1440
        restored=json.loads(json.dumps(s));ops.reconcile(restored)
        self.assertEqual(restored['world']['location'],'site_02_reception')

    def test_pressure_suspends_clearance_and_reception_work_restores_it(self):
        s=core.fresh('rei');qualify(s,'site_02');ops.enter(s,'site_02','briefing')
        ops.data(s)['sites']['site_02']['pressure']=15
        ops.reconcile(s)
        self.assertEqual(s['world']['location'],'site_02_reception')
        self.assertFalse(ops.permitted(s,'rei','site_02'))
        with self.assertRaises(ValueError): ops.request_pass(s,'site_02')
        ops.begin(s,'site_02','reception');ops.resolve(s,0)
        self.assertEqual(ops.progress(s,'site_02')['pressure'],12)
        self.assertTrue(ops.permitted(s,'rei','site_02'))


if __name__=='__main__':unittest.main()
