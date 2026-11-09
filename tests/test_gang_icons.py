import json
import unittest
import game_core as core
import job_apps
import gang_icons as icons
import organisation_logos as logos


class GangIconTests(unittest.TestCase):
    def state(self):
        s=core.fresh('minsu'); job_apps.ensure(s).update(reputation=20,completed=4)
        job_apps.gang(s,'Night Circle'); return s

    def test_design_saved_and_used_without_shared_asset_changes(self):
        s=self.state(); design=dict(icons.DEFAULT,symbol='Initials',initials=' nc ',accent='Rose')
        icons.apply(s,design); restored=json.loads(json.dumps(s)); g=restored['job_apps']['gang']
        self.assertEqual(g['icon']['initials'],'NC')
        self.assertEqual(logos.picture(g).tobytes(),icons.render(g['icon']).tobytes())
        other=self.state(); self.assertNotIn('icon',other['job_apps']['gang'])
        icons.reset(restored); self.assertNotIn('icon',g)
        self.assertEqual(logos.picture(g).tobytes(),logos.thumbnail('custom-crew').tobytes())

    def test_render_all_shapes_symbols_and_corrupt_fallback(self):
        digests=set()
        for shape in icons.SHAPES:
            for symbol in icons.SYMBOLS:
                art=icons.render(dict(icons.DEFAULT,shape=shape,symbol=symbol))
                self.assertEqual(art.size,(96,96)); self.assertEqual(art.getchannel('A').getextrema(),(0,255))
                digests.add(art.tobytes())
        self.assertEqual(len(digests),20)
        g=dict(name='Night Circle',role='Founder',icon={'shape':[]})
        self.assertEqual(logos.picture(g).tobytes(),logos.thumbnail('custom-crew').tobytes())
        art=icons.render(icons.DEFAULT); art.paste((0,0,0,0),(0,0,96,96))
        self.assertNotEqual(art.tobytes(),icons.render(icons.DEFAULT).tobytes())

    def test_validation_and_founder_only(self):
        s=self.state()
        for change in ({'accent':'white'},{'initials':'TOOLONG'},{'initials':'☠'},{'symbol':'unknown'}):
            with self.assertRaises(ValueError): icons.apply(s,dict(icons.DEFAULT,**change))
        self.assertNotIn('icon',s['job_apps']['gang'])
        with self.assertRaises(ValueError): icons.apply(core.fresh('garrett'),icons.DEFAULT)
        with self.assertRaises(ValueError): icons.reset(core.fresh('minsu'))


if __name__=='__main__': unittest.main()
