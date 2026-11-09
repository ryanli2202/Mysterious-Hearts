import unittest

import game_core as core
import phone_map as maps
import town


class MapTests(unittest.TestCase):
    def test_metropolitan_texture_covers_outskirts_in_both_layers(self):
        for satellite in (False, True):
            for center in ((-3000, -3000), (700, 500), (5000, 5000)):
                surface = maps.metropolitan_view(500, 400, *center, .25, satellite)
                self.assertEqual(surface.size, (500, 400))
                self.assertGreater(len(surface.getcolors(500*400)), 10)
                for box in ((0, 0, 50, 50), (450, 350, 500, 400)):
                    self.assertGreater(len(surface.crop(box).getcolors(2500)), 5)

    def setUp(self):
        self.state = core.fresh('rei')

    def test_every_destination_has_coordinates(self):
        import crime_operations
        expected = {k for k in town.LOCATIONS if k != 'home' and not k.startswith('car:') and k not in crime_operations.ROOMS}
        self.assertEqual(expected, set(maps.POINTS))
        self.assertEqual(len(maps.POINTS), len(set(maps.POINTS.values())))

    def test_search_ignores_case_accents_and_whitespace(self):
        self.assertIn('cafe', maps.places(self.state, '  CAMPUS CAFE  '))
        self.assertIn('flowers', maps.places(self.state, 'petal'))
        self.assertFalse(maps.places(self.state, 'no such place'))

    def test_private_locations_do_not_leak_into_search(self):
        self.assertNotIn('lena_home', maps.places(self.state))
        self.assertNotIn(town.hidden.HQ, maps.places(self.state, 'headquarters'))
        self.state['discoveries']['lena']['home'] = True
        self.assertIn('lena_home', maps.places(self.state, 'lena'))

    def test_categories(self):
        self.assertEqual(set(maps.places(self.state, category='Food')), maps.FOOD)
        self.assertEqual(set(maps.places(self.state, category='Outdoors')), maps.GREEN)
        self.assertTrue(all(k.endswith('_home') for k in maps.places(self.state, category='Homes')))


if __name__ == '__main__':
    unittest.main()
