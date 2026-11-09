import json
import unittest
from unittest.mock import patch
import game_core as core
import custom_gangs as cg
import crime_diplomacy as dip
import job_apps as jobs


class CustomGangTests(unittest.TestCase):
    def setUp(self):
        self.s=core.fresh('minsu'); self.d=jobs.ensure(self.s)
        self.d.update(reputation=40,completed=10)
        jobs.gang(self.s,'Evening Circle'); self.g=cg.crew(self.s)

    def ready(self,name='Gabe Turner'):
        self.s['world']['minute']=600
        self.s.setdefault('npc_chats',{})[name]=dict(history=[],connection=dict(trust=80,status='friends'))
        venue=cg.location(self.s,name)
        self.s['world']['location']=venue
        self.s['world']['cast']['minsu'].update(location=venue,journey=None)

    def test_recruitment_gates_and_saved_roles(self):
        with self.assertRaises(ValueError): cg.recruit(self.s,'Gabe Turner')
        self.ready(); self.s['world']['cast']['minsu']['journey']={'destination':'square'}
        with self.assertRaises(ValueError): cg.recruit(self.s,'Gabe Turner')
        self.s['world']['cast']['minsu']['journey']=None
        with patch.object(jobs.careers,'spend_time') as spend:
            cg.recruit(self.s,'Gabe Turner'); spend.assert_called_once_with(self.s,15,2)
        with self.assertRaises(ValueError): cg.recruit(self.s,'Gabe Turner')
        cg.assign(self.s,'Gabe Turner','Quartermaster')
        restored=json.loads(json.dumps(self.s))
        self.assertEqual(cg.crew(restored)['members'],self.g['members'])
        self.assertEqual(cg.operation(restored,'crew',True),50)
        self.assertEqual(cg.operation(restored,'parcel',True),0)
        cg.dismiss(restored,'Gabe Turner'); self.assertFalse(cg.crew(restored)['members'])

    def test_capacity_unique_roles_pending_and_charter(self):
        self.g['members']={n:dict(role='Member') for n in list(cg.RECRUITS)[:3]}
        self.ready('Tess Morgan'); self.assertIn('full',cg.reason(self.s,'Tess Morgan'))
        cg.assign(self.s,'Gabe Turner','Deputy')
        with self.assertRaises(ValueError): cg.assign(self.s,'Ben Okafor','Deputy')
        self.d['pending']={'kind':'contract'}
        with self.assertRaises(ValueError): cg.dismiss(self.s,'Gabe Turner')
        self.d['pending']=None; cg.charter(self.s,'Stay independent')
        self.assertEqual(self.g['charter'],'Stay independent')

    def test_offers_once_decline_and_accept(self):
        self.d['reputation']=60; jobs.ensure(self.s)
        self.assertEqual(set(self.g['assimilation']),{'Syndicate'})
        before=len(self.d['history']); jobs.ensure(self.s); self.assertEqual(before,len(self.d['history']))
        cg.respond(self.s,'Syndicate'); self.d['reputation']=70; jobs.ensure(self.s)
        self.assertEqual(self.g['assimilation']['Syndicate']['status'],'declined')
        with self.assertRaises(ValueError): cg.respond(self.s,'Shinokami',True)
        self.g['standing']=3; self.d['connections']['Shinokami']=3
        cg.respond(self.s,'Shinokami',True)
        self.assertEqual(self.d['membership']['rank'],0)
        self.assertEqual(self.g['parent_faction'],'Shinokami')
        self.assertEqual(self.g['name'],'Evening Circle')
        self.assertEqual(dip.mandate(self.s)[0],'crew:evening circle')

    def test_founder_relations_and_old_save_migration(self):
        self.assertIsNotNone(dip.mandate(self.s))
        b=dip.ensure(self.s); b['relations']['lantern']=40
        self.g['members']['Gabe Turner']=dict(role='Envoy')
        cg.operation(self.s,'network',True); self.assertEqual(b['relations']['lantern'],41)
        self.g.pop('assimilation'); self.g.pop('charter'); jobs.ensure(self.s)
        self.assertEqual(self.g['charter'],'Independent crew')
        self.assertIn('Gabe Turner',self.g['members'])


if __name__=='__main__': unittest.main()
