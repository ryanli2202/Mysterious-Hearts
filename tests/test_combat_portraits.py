"""Roster coverage and safe fallbacks for the combat-only artwork."""
import unittest
from unittest.mock import Mock, patch
from PIL import Image
import combat_portraits as art
from combat_profiles import RATINGS


class CombatPortraitTests(unittest.TestCase):
    def test_entire_awakened_roster_has_transparent_art(self):
        self.assertEqual(set(art.CAST), set(RATINGS))
        for who in RATINGS:
            with self.subTest(who=who):
                path = art.resolve(who)
                self.assertIsNotNone(path)
                with Image.open(path) as image:
                    self.assertEqual(image.format, 'PNG')
                    self.assertIn('A', image.getbands())
                    low, high = image.getchannel('A').getextrema()
                    self.assertEqual(low, 0)
                    # Generated near-opaque 254 is valid; require real body coverage.
                    self.assertGreaterEqual(high, 250)
                    histogram = image.getchannel('A').histogram()
                    self.assertGreater(sum(histogram[220:]) / (image.width * image.height), .15)

    def test_unknown_and_custom_keep_existing_portrait(self):
        game = Mock()
        for who in ('custom_player', 'Joseph Richter', 'guard_art_oni', '../garrett'):
            self.assertIsNone(art.resolve(who))
            self.assertIs(art.portrait(game, who, (160, 190), 'park', 123), game.portrait.return_value)
            game.portrait.assert_called_with(who, (160, 190), 'park', 123)

    def test_damaged_art_falls_back(self):
        game = Mock()
        with patch.object(art, '_thumbnail', side_effect=OSError('broken image')):
            self.assertIs(art.portrait(game, 'garrett', (160, 190), 'park', 123), game.portrait.return_value)

    def test_shared_fighter_scale_includes_saved_female_guard(self):
        import game as client
        import portrait_framing as framing
        from types import SimpleNamespace
        app=SimpleNamespace(photos={},state_data={})
        app.portrait_path=lambda *a,**kw:client.Game.portrait_path(app,*a,**kw)
        app.portrait=lambda *a,**kw:client.Game.portrait(app,*a,**kw)
        with patch.object(art.ImageTk,'PhotoImage',side_effect=lambda im,**kw:im.copy()):
            photos=art.group(app,{'ivan':(250,320),'guard_art_team9':(180,320)},'park',123)
        boxes={who:framing.visible_bounds(im) for who,im in photos.items()}
        heights={who:b[3]-b[1] for who,b in boxes.items()}
        self.assertAlmostEqual(heights['guard_art_team9']/heights['ivan'],160/193,delta=.01)


if __name__ == '__main__':
    unittest.main()
