"""MH-013 stature must survive padding, different slots and cropped bodies."""
import json
from pathlib import Path
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from PIL import Image, ImageDraw
import character_stature as stature
import custom_protagonist
import game
import portrait_framing as framing

ROOT = Path(__file__).resolve().parents[1]
ROSTER = json.loads((ROOT/'roadmap/artwork-stage-02/roster.json').read_text())['assets']
SPECIFIED_HEIGHTS = {'gordon':183, 'fox':184, 'crow':180, 'keisuke-hachimura':183,
                     'joseph-richter':190, 'guard-oni':198, 'guard-custom_robotic':198}


def span(image):
    box = framing.visible_bounds(image)
    return box[3] - box[1]


class PortraitFramingTests(unittest.TestCase):
    def tearDown(self):
        framing._load.cache_clear()

    def test_complete_roster_known_heights_and_fallback_ranges(self):
        import hidden_cast
        import character_biographies
        self.assertEqual(set(stature.records()), {r['id'] for r in ROSTER})
        for who, row in stature.records().items():
            with self.subTest(who=who):
                if row['basis'] == 'authored':
                    known = character_biographies.ORIGINAL_FACTS.get(who, (None,))[0]
                    known = known or hidden_cast.CAST.get(who, {}).get('height')
                    self.assertEqual(row['height_cm'], known)
                elif row['basis'] == 'user specified':
                    self.assertEqual(row['height_cm'], SPECIFIED_HEIGHTS[who])
                else:
                    self.assertEqual(row['basis'], 'display fallback')
                    low, high = (160, 165) if row['profile'] == 'female' else (175, 180)
                    self.assertTrue(low <= row['height_cm'] <= high)
        self.assertEqual([stature.height_cm(w) for w in ('ivan','garrett','rei')], [193,188,184])
        self.assertEqual(stature.height_cm('takeo'), 211)
        self.assertEqual(stature.height_cm('april'), 150)

    def test_defaults_vary_stably_and_original_known_heights_are_unchanged(self):
        before=json.loads((ROOT/'roadmap/artwork-stage-02/height-variation/before-stature.json').read_text(encoding='utf-8'))['characters']
        for who,row in before.items():
            if row['basis']=='authored':
                self.assertEqual(stature.records()[who],row,who)
        self.assertEqual({k for k,r in stature.records().items() if r['basis']=='user specified'},set(SPECIFIED_HEIGHTS))
        for profile,low in (('male',175),('female',160)):
            values={r['height_cm'] for r in stature.records().values() if r['basis']=='display fallback' and r['profile']==profile}
            self.assertEqual(values,set(range(low,low+6)))
        first=stature.records()
        stature.records.cache_clear()
        self.assertEqual(first,stature.records())

    def test_names_guard_roles_custom_and_undisclosed_heights(self):
        self.assertEqual(stature.height_cm('Priya Shah'), 162)
        self.assertEqual(stature.height_cm('guard_art_team9'), 160)
        self.assertEqual(stature.height_cm('saved encounter', ROOT/'assets/portraits/guards/kai_guard.png'), 161)
        self.assertEqual(stature.height_cm('Joseph Richter', ROOT/'assets/portraits/guards/richter_cybernetic.png'), 190)
        self.assertEqual(stature.height_cm('guard_art_richter_cybernetic'), 190)
        for who in ('guard_art_oni','guard_art_custom_robotic'):
            self.assertEqual(stature.height_cm(who),198)
        with patch.dict(custom_protagonist._profiles, {'custom_test': {'height': 203}}):
            self.assertEqual(stature.height_cm('custom_test'), 203)
        import character_biographies
        self.assertEqual(character_biographies.facts('crow')['Height'], 'Unknown')

    def test_padding_does_not_reduce_stature_or_distort_the_body(self):
        art = Image.new('RGBA', (300,500))
        ImageDraw.Draw(art).rectangle((75,40,224,459), fill='#aabbcc')
        art = art.crop(framing.visible_bounds(art))
        scaled = framing.fit(art, (200,360), 184)
        box = framing.visible_bounds(scaled)
        self.assertAlmostEqual((box[2]-box[0])/(box[3]-box[1]), 150/420, delta=.006)
        self.assertEqual(box[3], 360)
        # 184 cm is full height; the visible cropped span is only 70%.
        scaled = framing.fit(art, (300,400), 184, scale=2)
        self.assertAlmostEqual(span(scaled), 184*.70*2, delta=1)

    def test_all_live_and_staged_characters_share_stature_despite_different_slots(self):
        real_open = Image.open
        staged = {(ROOT/r['path']).resolve(): ROOT/'roadmap/artwork-stage-02/candidates'/(r['id']+'.png') for r in ROSTER}
        for mode in ('live','staged'):
            framing._load.cache_clear()
            def open_art(path, *args, **kwargs):
                if mode == 'staged' and isinstance(path,(str,Path)):
                    path = staged.get(Path(path).resolve(), path)
                return real_open(path,*args,**kwargs)
            with patch.object(Image,'open',open_art), patch.object(game.ImageTk,'PhotoImage',side_effect=lambda im:im.copy()):
                app = SimpleNamespace(photos={},state_data={})
                for row in ROSTER:
                    who = 'guard_art_'+row['character'] if row['role'] else row['character']
                    with self.subTest(mode=mode,who=who):
                        images = game.Game.portrait_group(app, {'ivan':(368,352),who:(192,352)})
                        ratio = stature.height_cm(who)/193
                        self.assertAlmostEqual(span(images[who]), span(images['ivan'])*ratio, delta=2)
                        self.assertEqual(images[who].size,(192,352))

    def test_order_and_player_slot_cannot_make_a_person_taller(self):
        with patch.object(game.ImageTk,'PhotoImage',side_effect=lambda im:im.copy()):
            app = SimpleNamespace(photos={},state_data={})
            sizes = {'ivan':(368,352),'garrett':(192,352),'rei':(192,352),'emily':(192,352)}
            images = game.Game.portrait_group(app, sizes)
            self.assertGreater(span(images['ivan']),span(images['garrett']))
            self.assertGreater(span(images['garrett']),span(images['rei']))
            for who in sizes:
                self.assertAlmostEqual(span(images[who])/span(images['ivan']),stature.height_cm(who)/193,delta=.008)

    def test_individual_thumbnails_do_not_flatten_tall_characters(self):
        with patch.object(game.ImageTk,'PhotoImage',side_effect=lambda im:im.copy()):
            app=SimpleNamespace(photos={},state_data={})
            reference=span(game.Game.portrait(app,'ivan',(150,225)))
            for row in ROSTER:
                who='guard_art_'+row['character'] if row['role'] else row['character']
                with self.subTest(who=who):
                    rendered=game.Game.portrait(app,who,(150,225))
                    self.assertAlmostEqual(span(rendered),reference*stature.height_cm(who)/193,delta=2)

    def test_wardrobe_and_historical_resolution_still_wins(self):
        app=SimpleNamespace(photos={},state_data={})
        _, path=game.Game.portrait_path(app,'ivan',outfit='gym-tank')
        self.assertEqual(path.name,'ivan-gym-tank.png')
        historical=ROOT/'assets/portraits/rei-selection.png'
        with patch('campaign_flashbacks.portrait_path',return_value=historical):
            _, path=game.Game.portrait_path(app,'rei','cafe',480,outfit='home')
            self.assertEqual(path,historical)


if __name__ == '__main__':
    unittest.main()
