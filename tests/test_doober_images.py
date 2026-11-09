import copy
import unittest
from unittest.mock import Mock, patch
from PIL import Image
import doober_images as food
import game_core as core
import phone_apps as apps

class FoodImageTests(unittest.TestCase):
    def test_complete_unique_decodable_assets(self):
        paths = set()
        for restaurant, authored in apps.MENUS.items():
            products = food.menu({}, restaurant)
            self.assertEqual(products.keys(), authored.keys())
            for ident, item in products.items():
                self.assertEqual({k: item[k] for k in authored[ident]}, authored[ident])
                path = food.image_path(item)
                self.assertIsNotNone(path, (restaurant, ident))
                with Image.open(path) as image:
                    image.verify()
                paths.add(path)
        self.assertEqual(len(paths), 80)

    def test_browsing_ignores_legacy_art_without_mutating_save(self):
        state = core.fresh('rei')
        restaurant = next(iter(apps.MENUS))
        apps.ensure(state)['food_photos'] = {restaurant: {'entrees-0': {'image': 'old.png'}}}
        before = copy.deepcopy(state)
        with patch('codex_images.generate', side_effect=AssertionError('No generation allowed')) as generate:
            manager = food.FoodImages(Mock())
            for retry in (False, True):
                manager.request(retry=retry)
            products = food.menu(state, restaurant)
            self.assertTrue(all(manager.status(p) == 'ready' for p in products.values()))
            generate.assert_not_called()
        self.assertEqual(state, before)
        state['world']['minute'] += 1440
        self.assertEqual(food.menu(state, restaurant), products)
        self.assertEqual(food.menu(core.fresh('garrett'), restaurant), products)

    def test_recipe_change_does_not_show_wrong_dish(self):
        changed = copy.deepcopy(apps.MENUS)
        restaurant = next(iter(changed))
        changed[restaurant]['entrees-0']['name'] = 'New recipe'
        with patch.object(apps, 'MENUS', changed):
            self.assertNotIn('image', food.menu({}, restaurant)['entrees-0'])

    def test_paths_confined_and_orders_unchanged(self):
        self.assertIsNone(food.image_path({'image': 'assets/../phone_ui.py'}))
        self.assertIsNone(food.image_path({'image': 'assets/doober/missing.png'}))
        state = core.fresh('rei')
        restaurant = next(iter(apps.MENUS))
        product = food.menu(state, restaurant)['entrees-0']
        money = state['world']['money']
        apps.order(state, 'Doober Eats', 'entrees-0', restaurant=restaurant)
        self.assertEqual(state['world']['money'], money - product['price'])

if __name__ == '__main__':
    unittest.main()
