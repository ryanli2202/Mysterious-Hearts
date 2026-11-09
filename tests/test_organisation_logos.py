import hashlib
import unittest
from PIL import Image
import organisation_logos as logos
import crime_diplomacy
import bubblegram_progression


class OrganisationLogoTests(unittest.TestCase):
    def test_all_organisations_gangs_and_custom_crews_have_assets(self):
        for key in {*crime_diplomacy.ORGANISATIONS,*bubblegram_progression.GANGS,'custom-crew'}:
            self.assertIn(key,logos.KEYS)
            with Image.open(logos.ROOT/(key+'.png')) as art:
                self.assertEqual(art.format,'PNG')
                self.assertGreater(min(art.size),100)
            preview=logos.thumbnail(key)
            self.assertLessEqual(max(preview.size),96)

    def test_generated_marks_preserve_transparency_and_are_distinct(self):
        digests=set()
        for key in logos.KEYS:
            path=logos.ROOT/(key+'.png')
            digests.add(hashlib.sha256(path.read_bytes()).hexdigest())
            if key in ('syndicate','shinokami'): continue
            with Image.open(path) as art:
                self.assertIn('A',art.getbands())
                lo,hi=art.getchannel('A').getextrema()
                self.assertEqual(lo,0); self.assertEqual(hi,255)
        self.assertEqual(len(digests),len(logos.KEYS))

    def test_aliases_and_safe_custom_fallback(self):
        self.assertEqual(logos.key('Clubs'),'syndicate')
        self.assertEqual(logos.key('Shinokami'),'shinokami')
        self.assertEqual(logos.key(dict(name='Red Dragons')),'dragons')
        self.assertEqual(logos.key(dict(id='purple',name='Purple Skulls')),'purple')
        self.assertEqual(logos.key('crew:New Company'),'custom-crew')
        self.assertEqual(logos.key('../../portrait'),'custom-crew')

    def test_syndicate_display_copy_has_alpha_and_original_remains(self):
        with Image.open(logos.ROOT/'syndicate.png') as original:
            self.assertEqual(original.size,(1024,1024))
        with Image.open(logos.ROOT/'syndicate-display.png') as display:
            self.assertEqual(display.getchannel('A').getextrema(),(0,255))


if __name__=='__main__': unittest.main()
