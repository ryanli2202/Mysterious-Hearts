import copy
import json
import unittest
from unittest.mock import patch
import game_core as core
import phone_apps as apps
import supafast
from supafast_fixtures import items


class SupafastTests(unittest.TestCase):
    def setUp(self):
        self.s = core.fresh('rei')
        self.day = self.s['world']['minute']//1440

    def test_no_fixed_fallback_or_read_side_effect(self):
        with patch.object(core, 'request') as request:
            self.assertEqual(apps.catalog(self.s), {})
            request.assert_not_called()
        self.assertEqual(apps.ensure(self.s)['products'], {})

    def test_generation_uses_provider_and_recent_names(self):
        supafast.commit(self.s, self.day, items(self.day))
        self.s['world']['minute'] += 1440
        fresh = items(self.day+1)
        with patch.object(core, 'request', return_value={'message': {'content': json.dumps({'items': fresh})}}) as request:
            result = supafast.generate(self.s, self.day+1)
        self.assertEqual(result, fresh)
        body = request.call_args.args[1]
        context = json.loads(body['messages'][1]['content'])
        self.assertEqual(len(context['avoid_recent_products']), 12)
        self.assertEqual(context['story_day'], self.day+2)
        self.assertEqual(apps.catalog(self.s), {})

    def test_saved_daily_stock_ownership_and_stale_order(self):
        self.assertTrue(supafast.commit(self.s, self.day, items(self.day)))
        first = apps.catalog(self.s)
        key = next(iter(first))
        apps.order(self.s, 'Supafast', key)
        restored = json.loads(json.dumps(self.s))
        self.assertEqual(apps.catalog(restored), first)
        self.assertFalse(supafast.commit(restored, self.day, items(100)))
        restored['world']['minute'] = (self.day+1)*1440
        self.assertEqual(apps.catalog(restored), {})
        money = restored['world']['money']
        with self.assertRaises(ValueError): apps.order(restored, 'Supafast', key)
        self.assertEqual(restored['world']['money'], money)
        self.assertTrue(supafast.commit(restored, self.day+1, items(self.day+1)))
        self.assertFalse(set(first) & set(apps.catalog(restored)))
        self.assertEqual(restored['world']['inventory'][key], 1)
        self.assertIn(key, apps.gift_options(restored))
        self.assertEqual(apps.ensure(restored)['products'][key]['description'], first[key]['description'])

    def test_legacy_stock_retained_but_replaced_for_browsing(self):
        data = apps.ensure(self.s)
        data['catalogs'] = {str(self.day): ['old']}
        data['products']['old'] = dict(name='Old journal', category='Gifts', price=10)
        self.s['world']['inventory']['old'] = 1
        self.assertEqual(apps.catalog(self.s), {})
        supafast.commit(self.s, self.day, items(self.day))
        self.assertIn('old', apps.gift_options(self.s))
        self.assertEqual(self.s['world']['inventory']['old'], 1)

    def test_atomic_validation_and_late_day_result(self):
        before = copy.deepcopy(apps.ensure(self.s)['products'])
        for key, value in [('name', ''), ('description', ''), ('category', 4), ('price', True), ('price', -1), ('price', 501)]:
            bad = items(self.day)
            bad[5][key] = value
            with self.assertRaises(ValueError): supafast.commit(self.s, self.day, bad)
            self.assertEqual(apps.ensure(self.s)['products'], before)
        bad = items(self.day)
        bad[4] = bad[0]
        with self.assertRaises(ValueError): supafast.commit(self.s, self.day, bad)
        self.s['world']['minute'] += 1440
        self.assertFalse(supafast.commit(self.s, self.day, items(self.day)))
        self.assertEqual(apps.catalog(self.s), {})

    def test_repeat_previous_products_and_provider_errors(self):
        supafast.commit(self.s, self.day, items(self.day))
        self.s['world']['minute'] += 1440
        with self.assertRaises(ValueError): supafast.commit(self.s, self.day+1, items(self.day))
        with patch.object(core, 'request', side_effect=RuntimeError('offline')):
            with self.assertRaises(RuntimeError): supafast.generate(self.s, self.day+1)
        for response in ({}, {'message': {'content':'invalid'}}, {'message': {'content':'{"items":[]}'}}):
            with patch.object(core, 'request', return_value=response):
                with self.assertRaises(ValueError): supafast.generate(self.s, self.day+1)
        self.assertEqual(apps.catalog(self.s), {})

if __name__ == '__main__': unittest.main()
