import copy
import json
from pathlib import Path
import sys
import tempfile
import time
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from PIL import Image
import camera
import codex_images
import game_core as core
import town


class CameraTests(unittest.TestCase):
    def setUp(self):
        self.state = core.fresh('rei')
        world = town.ensure(self.state)
        world['location'] = town.HOMES['rei']
        world['cast']['rei']['location'] = world['location']
        world['party'] = []
        for route in self.state['routes'].values(): route['channel'] = 'text'

    def companion(self, who, status='friends'):
        w = self.state['world']
        w['party'].append(who)
        w['cast'][who].update(location=w['location'], journey=None, activity='Hanging out')
        self.state['relationships'][who]['status'] = status

    def test_location_modes_and_activity_gating(self):
        context = camera.scene(self.state)
        self.assertEqual(camera.modes(context), ['Selfie', 'Mirror selfie', 'Photo of hobby'])
        self.state['world']['location'] = 'park'
        context = camera.scene(self.state)
        self.assertEqual(camera.modes(context), ['Selfie', 'Photo of environment'])
        self.assertIn('Photo of activity', camera.modes(context, 'A picnic lunch'))
        with self.assertRaises(ValueError): camera.request(self.state, {'mode': 'Photo of activity'})
        shot = camera.request(self.state, {'mode': 'Photo of activity', 'detail': 'A picnic lunch'})
        self.assertEqual(shot['snapshot']['subjects'], [])
        self.assertEqual(shot['references'], [])

    def test_group_only_with_present_hangout_members(self):
        self.companion('emily')
        self.companion('sophie')
        self.state['world']['cast']['sophie']['location'] = 'park'
        context = camera.scene(self.state)
        self.assertEqual(context['companions'], ['emily'])
        self.assertIn('Group selfie', camera.modes(context))
        shot = camera.request(self.state, {'mode': 'Group selfie'})
        self.assertEqual([s['id'] for s in shot['snapshot']['subjects']], ['rei', 'emily'])
        self.state['world']['cast']['emily']['location'] = 'park'
        with self.assertRaises(ValueError): camera.request(self.state, {'mode': 'Group selfie'})

    def test_romance_poses_only_for_present_partners(self):
        self.companion('emily', 'dating')
        self.companion('amy', 'friends')
        context = camera.scene(self.state)
        options = camera.group_poses(context)
        self.assertIn('Hold hands · Emily Fields', options)
        self.assertFalse(any('Amy' in p for p in options))
        shot = camera.request(self.state, {'mode': 'Group photo', 'group_pose': 'Hold hands · Emily Fields'})
        self.assertIn('ONLY to the player and the named partner', shot['prompt'])
        self.state['relationships']['emily']['status'] = 'strained'
        with self.assertRaises(ValueError):
            camera.request(self.state, {'mode': 'Group photo', 'group_pose': 'Hold hands · Emily Fields'})

    def test_custom_outfits_and_reference_identity(self):
        self.companion('emily', 'official')
        settings = {'mode': 'Group selfie', 'people': {
            'rei': {'outfit': 'Custom', 'custom': 'A navy cardigan', 'expression': 'Playful wink', 'pose': 'Peace sign'},
            'emily': {'outfit': 'Custom', 'custom': 'A floral summer dress', 'expression': 'Laughing', 'pose': 'Wave'}}}
        shot = camera.request(self.state, settings)
        self.assertEqual(len(shot['references']), 2)
        self.assertTrue(all(Path(p).is_file() for p in shot['references']))
        self.assertEqual(shot['snapshot']['subjects'][0]['outfit'], 'A navy cardigan')
        self.assertEqual(shot['snapshot']['subjects'][1]['expression'], 'Laughing')
        self.assertIn('replace clothes', shot['snapshot']['subjects'][0]['reference_role'])
        settings['people']['rei']['custom'] = ''
        with self.assertRaises(ValueError): camera.request(self.state, settings)

    def test_local_date_partner_can_join_photo(self):
        self.state['world']['npcs'] = ['Theo']
        self.state['date_session'] = {'partner': 'Theo', 'started': True}
        self.state['relationships']['Theo'] = {'status': 'dating'}
        context = camera.scene(self.state)
        self.assertIn('Theo', context['companions'])
        self.assertIn('Hold hands · Theo', camera.group_poses(context))
        self.assertTrue(camera.outfits(self.state, 'Theo'))

    def test_saved_outfits_and_bedroom_access(self):
        self.assertIn('Black leather moto jacket', camera.outfits(self.state, 'rei'))
        self.assertFalse(any('Bedroom' in k for k in camera.outfits(self.state, 'emily')))
        self.state['relationships']['emily']['status'] = 'official'
        self.assertTrue(any('Bedroom' in k for k in camera.outfits(self.state, 'emily')))

    def test_recent_activity_expires_and_does_not_follow_player(self):
        world = self.state['world']
        world['location'] = 'park'
        world['camera_activity'] = dict(location='park', minute=world['minute'], text='Sketching the trees')
        self.assertIn('Photo of activity', camera.modes(camera.scene(self.state)))
        world['minute'] += 61
        self.assertNotIn('Photo of activity', camera.modes(camera.scene(self.state)))
        world['minute'] -= 61
        world['location'] = 'square'
        self.assertEqual(camera.scene(self.state)['activity'], '')

    def test_delivered_food_enables_activity_photo(self):
        import phone_apps
        self.state['world']['location'] = 'park'
        self.state['world']['money'] = 1000
        restaurant = next(iter(phone_apps.MENUS))
        item = next(iter(phone_apps.MENUS[restaurant]))
        phone_apps.order(self.state, 'Doober Eats', item, restaurant=restaurant)
        self.assertIn('Photo of activity', camera.modes(camera.scene(self.state)))

    def test_album_is_save_scoped_dated_and_snapshot_is_stable(self):
        tmp_root = core.ROOT / '.test-tmp'
        tmp_root.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=tmp_root) as tmp:
            folder = Path(tmp)
            with patch.object(camera, 'ALBUMS', folder / 'albums'), patch.object(codex_images, 'STORE', folder):
                file = folder / 'image.png'
                Image.new('RGB', (20, 20), 'blue').save(file)
                shot = camera.request(self.state, {'mode': 'Selfie'})
                captured = self.state['world']['minute']
                self.state['world']['minute'] += 2880
                generated = dict(id='one', path=str(file), created=time.time())
                camera.commit(self.state, shot, generated)
                camera.commit(self.state, shot, generated)
                later = camera.request(self.state, {'mode': 'Selfie'})
                camera.commit(self.state, later, dict(generated, id='two'))
                restored = json.loads(json.dumps(self.state))
                save_path = folder / 'story.json'
                core.save(restored, save_path)
                restored = core.load(save_path)
                photos = camera.photos(restored)
                self.assertEqual(len(photos), 2)
                self.assertEqual(photos[0]['id'], 'two')
                self.assertEqual(photos[1]['minute'], captured)
                self.assertEqual(photos[1]['date'], camera.story_calendar.story_date(captured).isoformat())
                other = core.fresh('rei')
                self.assertEqual(camera.photos(other), [])

    def test_reference_args_keep_subscription_lock(self):
        args = codex_images.command('codex', Path('job'), [Path('portrait.png')])
        self.assertIn('forced_login_method="chatgpt"', args)
        self.assertEqual(args[args.index('--image') + 1], 'portrait.png')

    def test_custom_selections_persist_and_reach_photo_prompt(self):
        self.companion('emily')
        expression = camera.save_selection(self.state, 'expression', '  A faint smile with one eyebrow raised  ')
        pose = camera.save_selection(self.state, 'pose', 'Rest one hand on the windowsill')
        group = camera.save_selection(self.state, 'group_pose', 'Both lean toward the lens and wave')
        camera.save_selection(self.state, 'expression', 'A faint smile with one eyebrow raised')
        restored = json.loads(json.dumps(self.state))
        self.assertEqual(len(camera.saved_selections(restored, 'expression')), 1)
        self.assertIn(pose, camera.selection_options(restored, camera.scene(restored), 'pose'))
        shot = camera.request(restored, {'mode': 'Group photo', 'group_pose': group,
            'people': {'rei': {'expression': expression, 'pose': pose},
                       'emily': {'expression': expression}}})
        self.assertEqual(shot['snapshot']['group_pose'], 'Both lean toward the lens and wave')
        self.assertEqual(shot['snapshot']['subjects'][1]['expression'], 'A faint smile with one eyebrow raised')
        self.assertEqual(shot['snapshot']['subjects'][0]['pose'], 'Rest one hand on the windowsill')
        for invalid in (' ', 'x' * 501):
            with self.assertRaises(ValueError): camera.save_selection(restored, 'pose', invalid)

    def test_edit_delete_custom_presets_updates_active_choices(self):
        data = camera.ensure(self.state)
        for kind in ('expression', 'pose', 'group_pose'):
            old = camera.save_selection(self.state, kind, 'Original description')
            camera.save_selection(self.state, kind, 'Updated description')
            settings = {'group_pose': old, 'people': {
                'rei': {kind: old}, 'emily': {kind: old}}}
            data['preferences'] = copy.deepcopy(settings)
            camera.change_custom(self.state, kind, 'Original description', 'Updated description', preferences=settings)
            self.assertEqual(camera.saved_selections(self.state, kind), ['Updated description'])
            if kind == 'group_pose':
                self.assertEqual(settings[kind], 'Custom: Updated description')
            else:
                self.assertEqual(settings['people']['emily'][kind], 'Custom: Updated description')
            camera.change_custom(self.state, kind, 'Updated description', preferences=settings)
            self.assertEqual(camera.saved_selections(self.state, kind), [])
            self.assertEqual(data['preferences'], settings)
        data['custom_outfits'] = {'rei': ['Blue coat'], 'emily': ['Blue coat']}
        settings = {'people': {'rei': {'outfit': 'Custom', 'custom': 'Blue coat'},
                               'emily': {'outfit': 'Custom', 'custom': 'Blue coat'}}}
        data['preferences'] = copy.deepcopy(settings)
        camera.change_custom(self.state, 'outfit', 'Blue coat', 'Green coat', 'rei', settings)
        self.assertEqual(settings['people']['rei']['custom'], 'Green coat')
        self.assertEqual(settings['people']['emily']['custom'], 'Blue coat')
        with self.assertRaises(ValueError):
            camera.change_custom(self.state, 'outfit', 'Green coat', ' ', 'rei', settings)
        camera.change_custom(self.state, 'outfit', 'Green coat', who='rei', preferences=settings)
        self.assertNotEqual(settings['people']['rei']['outfit'], 'Custom')
        self.assertEqual(settings['people']['rei']['custom'], '')
        self.assertEqual(camera.custom_items(self.state, 'outfit', 'emily'), ['Blue coat'])

    def test_studio_portrait_options_are_location_gated(self):
        ordinary = camera.request(self.state, {'mode': 'Selfie', 'people': {
            'rei': {'expression': 'Smoulder', 'pose': 'Arms folded'}}})
        self.assertEqual(ordinary['snapshot']['subjects'][0]['expression'], 'Smoulder')
        settings = {'mode': 'Modelling portrait', 'people': {
            'rei': {'expression': 'Editorial gaze', 'pose': 'Runway walk'}}}
        with self.assertRaises(ValueError): camera.request(self.state, settings)
        self.state['world']['location'] = 'studio'
        shot = camera.request(self.state, settings)
        self.assertEqual([p['id'] for p in shot['snapshot']['subjects']], ['rei'])
        self.assertIn('Full-length frame', shot['snapshot']['subjects'][0]['pose_direction'])
        self.assertIn('studio lighting', shot['prompt'])
        self.assertTrue(shot['references'])
        self.state['world']['location'] = 'park'
        settings['mode'] = 'Selfie'
        with self.assertRaisesRegex(ValueError, 'require the studio'):
            camera.request(self.state, settings)


if __name__ == '__main__': unittest.main()
