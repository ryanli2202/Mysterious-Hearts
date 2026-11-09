import json
import unittest
from unittest.mock import patch
import game_core as core
import phone_apps as apps
import grove


class PhoneAppsTests(unittest.TestCase):
    def setUp(self):
        self.s = core.fresh('rei')
        from supafast_fixtures import seed
        seed(self.s)

    def test_daily_catalog_and_saved_ownership(self):
        first = apps.catalog(self.s)
        key = next(iter(first))
        money = self.s['world']['money']
        apps.order(self.s, 'Supafast', key)
        self.assertEqual(self.s['world']['money'], money-first[key]['price'])
        self.assertEqual(self.s['world']['inventory'][key], 1)
        self.s = json.loads(json.dumps(self.s))
        self.assertEqual(first, apps.catalog(self.s))
        self.s['world']['minute'] += 1440
        self.assertFalse(set(first) & set(apps.catalog(self.s)))
        self.assertIn(key, apps.gift_options(self.s))
        with self.assertRaises(ValueError): apps.order(self.s, 'Supafast', key)

    def test_menus_delivery_and_validation(self):
        for restaurant, menu in apps.MENUS.items():
            self.assertEqual(len(menu), 20)
            self.assertEqual(set(p['category'] for p in menu.values()), set(apps.CATEGORIES))
            key = next(iter(menu))
            apps.order(self.s, 'Doober Eats', key, 'emily', restaurant)
        self.assertEqual(len(apps.ensure(self.s)['orders']), 4)
        before = self.s['world']['money']
        with self.assertRaises(ValueError): apps.order(self.s, 'Supafast', next(iter(apps.catalog(self.s))), 'nobody')
        self.assertEqual(before, self.s['world']['money'])
        self.s['world']['money'] = 0
        with self.assertRaises(ValueError): apps.order(self.s, 'Supafast', next(iter(apps.catalog(self.s))))

    def test_feed_threads_frequencies_and_no_duplicate_refresh(self):
        apps.sync(self.s)
        apps.post(self.s, 'Hello Grove!')
        parent = apps.ensure(self.s)['posts'][-1]['id']
        apps.post(self.s, 'A reply', parent)
        reply = apps.ensure(self.s)['posts'][-1]['id']
        apps.post(self.s, 'A nested reply', reply)
        self.s['world']['minute'] += 1440
        posts = apps.sync(self.s)
        count = len(posts)
        self.assertEqual(len(apps.sync(self.s)), count)
        self.assertEqual(count, 3)  # Scheduling never publishes prewritten content.
        pending = apps.ensure(self.s)['grove_pending']
        self.assertEqual(len(pending), len({j['author'] for j in pending}))
        self.assertLess(apps.frequency('sophie'), apps.frequency('april'))
        self.assertEqual(len(set(apps.handle(who) for who in self.s['routes'])), len(self.s['routes']))
        with self.assertRaises(ValueError): apps.post(self.s, ' ')
        with self.assertRaises(ValueError): apps.post(self.s, 'x'*281)
        with self.assertRaises(ValueError): apps.post(self.s, 'bad parent', -1)

    def test_exact_post_boundary(self):
        self.s['world']['minute'] = 149
        apps.sync(self.s)
        self.s['world']['minute'] = 150
        self.assertEqual(apps.sync(self.s), [])
        self.assertTrue(any(j['author']=='sophie' for j in apps.ensure(self.s)['grove_pending']))

    def test_ai_uses_live_thread_and_relationships(self):
        data = apps.ensure(self.s)
        first = apps._append(data, 'emily', 'The blue flowers finally opened.', 1)
        second = apps._append(data, 'sophie', 'Can I see them after practice?', 2, first['id'])
        apps.queue_grove(self.s, 'emily', second['id'])
        job = data['grove_pending'][0]
        self.s['bond_details']['emily:sophie'] = {'trust': 11, 'closeness': 22, 'tension': 70, 'events': ['They argued.']}
        expected = {'text': 'You can stop by. I am still upset about earlier, though.', 'parent': second['id']}
        with patch.object(core, 'request', return_value={'message': {'content': json.dumps(expected)}}) as request:
            result = grove.generate(self.s, job)
        payload = json.loads(request.call_args.args[1]['messages'][1]['content'])
        self.assertEqual([p['id'] for p in payload['thread_ancestry']], [first['id'], second['id']])
        self.assertEqual(payload['relationships'][0]['current_state']['tension'], 70)
        self.assertEqual(len(data['posts']), 2)
        self.assertTrue(apps.commit_grove(self.s, job, result))
        self.assertFalse(apps.commit_grove(self.s, job, result))
        self.assertEqual(data['posts'][-1]['text'], expected['text'])
        self.assertEqual(data['grove_next']['emily'], self.s['world']['minute']+apps.frequency('emily'))

    def test_player_reply_queues_contextual_answer(self):
        data = apps.ensure(self.s)
        root = apps._append(data, 'emily', 'A new bouquet today.', 1)
        apps.post(self.s, 'Which flowers did you use?', root['id'])
        job = data['grove_pending'][0]
        self.assertEqual(job['author'], 'emily')
        self.assertEqual(job['parent'], data['posts'][-1]['id'])
        context = grove.context(self.s, job)
        state = context['relationships'][0]['current_state']
        self.assertEqual(state, self.s['relationships']['emily'])
        self.s = json.loads(json.dumps(self.s))
        self.assertEqual(apps.ensure(self.s)['grove_pending'][0], job)

    def test_ai_failure_keeps_job_without_fallback(self):
        apps.queue_grove(self.s, 'emily')
        data = apps.ensure(self.s)
        job = data['grove_pending'][0]
        with patch.object(core, 'request', side_effect=RuntimeError('offline')):
            with self.assertRaises(RuntimeError): grove.generate(self.s, job)
        for bad in ({'text': '', 'parent': None}, {'text': 'x'*281, 'parent': None},
                    {'text': 'Hello', 'parent': 999}, {'text': 'Hello', 'parent': False}):
            with patch.object(core, 'request', return_value={'message': {'content': json.dumps(bad)}}):
                with self.assertRaises(ValueError): grove.generate(self.s, job)
        self.assertEqual(data['posts'], [])
        self.assertEqual(data['grove_pending'], [job])

    def test_bios_unique_and_cover_cast(self):
        self.assertFalse(set(core.CONTACTS) - set(grove.BIOS))
        self.assertEqual(len(grove.BIOS), len(set(grove.BIOS.values())))

    def test_map_lists_people_and_distinguishes_travel(self):
        w = self.s['world']
        w['cast']['emily'].update(location='flowers', journey=None)
        w['cast']['garrett'].update(location='car:garrett', journey={
            'destination': 'flowers', 'arrives': w['minute'] + 12})
        people = apps.location_people(self.s)
        self.assertIn('Emily Fields', people['flowers'])
        self.assertIn('Garrett Han · On the way (12 min)', people['flowers'])
        self.assertNotIn('car:garrett', people)
        w['cast']['emily'].update(location='cafe')
        self.assertIn('Emily Fields', apps.location_people(self.s)['cafe'])

    def test_migration_does_not_rewrite_or_backfill_feed(self):
        self.s['phone_apps'] = dict(posts=[dict(id=1, author='emily', text='Existing post', minute=1, parent=None)],
                                    next_id=2, last_sync=1, catalogs={}, products={}, orders=[])
        apps.sync(self.s)
        data = apps.ensure(self.s)
        self.assertEqual(len(data['posts']), 1)
        self.assertEqual(data['grove_pending'], [])
