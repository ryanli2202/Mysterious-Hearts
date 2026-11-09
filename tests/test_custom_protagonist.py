import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from PIL import Image
import custom_protagonist as custom
import game_core as core
import town
import phone_apps
import phone_numbers
import phone_personalization
import meet_cute

PROFILE = dict(name='Alex Rivers', gender='Woman', age=25, height=172, sexuality='Bisexual',
               hairstyle='Wavy', mbti='INFP', occupation='Illustrator', interests=['Art', 'Cooking'],
               appearance='Shoulder-length brown hair, green eyes, denim jacket and dark trousers.',
               home='vacant_beach_home')


class CustomTests(unittest.TestCase):
    def setUp(self):
        folder = core.ROOT / 'assets' / 'generated'
        folder.mkdir(exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=folder)
        self.addCleanup(self.temp.cleanup)
        self.image = Path(self.temp.name) / 'image.png'
        image = Image.new('RGBA', (8, 8), (0, 0, 0, 0))
        image.putpixel((4, 4), (80, 100, 120, 255))
        image.save(self.image)
        self.relative = self.image.relative_to(core.ROOT).as_posix()

    def create(self, **changes):
        return custom.create(PROFILE | changes, self.relative)

    def test_new_arrival_is_unknown_and_home_works(self):
        s = self.create()
        self.assertEqual(s['world']['location'], PROFILE['home'])

    def test_library_profile_starts_fresh_story(self):
        import custom_library
        with tempfile.TemporaryDirectory(dir=self.temp.name) as folder:
            root = Path(folder) / 'saves'
            old = self.create()
            old['world']['money'] = 12
            old['turn'] = 90
            custom_library.remember(old, root)
            profile = custom_library.profiles(root)[0]
            new = custom.create(profile, profile['portrait'])
            self.assertNotEqual(old['player'], new['player'])
            self.assertEqual(new['custom_protagonist'], old['custom_protagonist'])
            self.assertEqual(new['turn'], 0)
            self.assertEqual(new['world']['money'], 100000)

    def test_awakening_validation_and_legacy_defaults(self):
        legacy = custom.validate(PROFILE)
        self.assertFalse(legacy['awakened'])
        self.assertEqual(legacy['awakening_trait'], '')
        for change in ({'awakened': 'yes'}, {'awakened': True},
                       {'awakened': True, 'awakening_trait': 'Echo', 'awakening_description': ' '},
                       {'awakened': True, 'awakening_trait': 'x'*101, 'awakening_description': 'Sound.'}):
            with self.assertRaises(ValueError):
                custom.validate(PROFILE | change)
        inactive = custom.validate(PROFILE | {'awakening_trait': 'Unused'})
        self.assertEqual(inactive['awakening_trait'], '')

    def test_awakened_story_save_and_context(self):
        s = self.create(awakened=True, awakening_trait='Resonance',
                        awakening_description='Shapes nearby sound; requires concentration.')
        path = Path(self.temp.name) / 'awakened.json'
        core.save(s, path)
        custom._profiles.pop(s['player'])
        loaded = core.load(path)
        self.assertEqual(loaded['custom_protagonist'], s['custom_protagonist'])
        self.assertTrue(loaded['custom_protagonist']['awakened'])
        self.assertIn('Trait: Resonance', core.CONTACTS[s['player']][3])
        town.travel(loaded, loaded['world']['cast']['emily']['location'])
        town.meet(loaded, 'emily')
        self.assertIn('requires concentration', str(core.build_messages(loaded, 'Hello.')))
        self.assertNotIn('Resonance', custom.portrait_prompt(loaded['custom_protagonist']))

    def test_new_arrival_contacts_and_home_actions(self):
        s = self.create()
        self.assertEqual(phone_apps.contacts(s), [])
        self.assertEqual(set(phone_numbers.ensure(s)['contacts']), {s['player']})
        self.assertFalse(phone_personalization.ensure(s)['archived_messages'])
        self.assertTrue(all(r['closeness'] == 0 and r['status'] == 'strangers' for r in s['relationships'].values()))
        self.assertEqual(s['world']['npcs'], [])
        self.assertNotIn('rei_home', __import__('phone_map').places(s))
        town.home_action(s, 'Unpack a moving box')
        town.rest(s)
        town.travel(s, 'cafe')
        town.travel(s, 'home')
        self.assertEqual(s['world']['location'], PROFILE['home'])

    def test_profiles_do_not_leak_between_stories_and_reload(self):
        one = self.create()
        two = self.create(name='Jamie New', gender='Man', home='vacant_downtown_home')
        self.assertEqual(core.PLAYERS[one['player']], 'Alex Rivers')
        self.assertEqual(town.HOMES[one['player']], PROFILE['home'])
        self.assertNotIn(one['player'], two['world']['cast'])
        canon = core.fresh('rei')
        self.assertNotIn(one['player'], canon['world']['cast'])
        self.assertNotIn(one['player'], canon['routes'])
        path = Path(self.temp.name) / 'save.json'
        core.save(one, path)
        custom._profiles.pop(one['player'])  # Simulate reopening without an in-memory identity.
        loaded = core.load(path)
        self.assertEqual(loaded['custom_protagonist'], one['custom_protagonist'])
        self.assertEqual(phone_apps.contacts(loaded), [])
        import save_system, zipfile
        bundle = Path(self.temp.name) / 'story.zip'
        save_system.export_story(one, bundle, core.ROOT)
        with zipfile.ZipFile(bundle) as archive:
            self.assertIn(self.relative, archive.namelist())

    def test_meeting_unlocks_contact_and_persists(self):
        s = self.create()
        town.travel(s, s['world']['cast']['emily']['location'])
        town.meet(s, 'emily')
        self.assertIn('emily', phone_apps.contacts(s))
        self.assertNotIn('sophie', phone_apps.contacts(s))
        self.assertIsNotNone(phone_numbers.saved_number(s, 'emily'))
        town.wait(s, 15)

    def test_profile_identity_and_generator_contract(self):
        s = self.create()
        identity = meet_cute.identity(s['player'])
        self.assertEqual(identity['name'], PROFILE['name'])
        self.assertEqual(identity['age'], 25)
        self.assertEqual(identity['gender'], 'Women')
        self.assertEqual(meet_cute.interest_options(s), tuple(PROFILE['interests']))
        with patch('codex_images.generate', return_value={'path': str(self.image)}) as generate:
            self.assertEqual(custom.generate_portrait(PROFILE), self.relative)
        prompt = generate.call_args.args[0]
        self.assertIn('transparent_background true', prompt)
        self.assertIn(PROFILE['appearance'], prompt)
        self.assertNotIn('Bisexual', prompt)
        self.assertIn('STYLE REFERENCES ONLY', prompt)
        self.assertIn('do not copy', prompt)
        self.assertIn('head-to-upper-thigh', prompt)
        references = generate.call_args.kwargs['references']
        self.assertEqual([p.name for p in references], ['rei-selection.png', 'emily-selection.png'])
        for reference in references:
            self.assertTrue(reference.is_file())
            with Image.open(reference) as artwork:
                artwork.verify()

    def test_validation_rejects_bad_profile_and_opaque_portrait(self):
        for changes in ({'age': 17}, {'age': 101}, {'height': 0}, {'home': 'rei_home'}, {'interests': []}, {'gender': 'bogus'}):
            with self.assertRaises(ValueError): custom.validate(PROFILE | changes)
        Image.new('RGB', (8, 8)).save(self.image)
        with self.assertRaises(ValueError): self.create()
        with patch('codex_images.generate', side_effect=RuntimeError('Generation cancelled')):
            with self.assertRaisesRegex(RuntimeError, 'cancelled'):
                custom.generate_portrait(PROFILE)
        with self.assertRaises(ValueError): custom.portrait_path({'portrait': '../outside.png'})

    def test_meet_cute_exchange_unlocks_only_agreed_contact(self):
        s = self.create(gender='Man')
        meet_cute.publish(s, 'New to town and looking forward to meeting people.', PROFILE['interests'],
                          ['Cooking.', 'Coffee and a walk.', 'Art.'], ['portrait'], 'Open to either', 'Flexible')
        self.assertTrue(meet_cute.feed(s))
        m = meet_cute._match(s, 'emily', 'Hello!', meet_cute.ensure(s)['profile'])
        m['turns'] = 3
        self.assertFalse(town.hidden.contact(s, 'emily'))
        # Exercise an agreed exchange; compatibility otherwise varies with the
        # random custom UUID and can legitimately reject this unrelated fixture.
        with patch.object(meet_cute, 'compatibility', return_value=60):
            meet_cute.request_numbers(s, 'emily')
            s['world']['minute'] += 200
            meet_cute.tick(s)
        self.assertEqual(m['proposal']['status'], 'accepted')
        self.assertTrue(town.hidden.contact(s, 'emily'))
        self.assertFalse(town.hidden.ensure(s)['emily']['met'])
        self.assertNotIn('sophie', phone_apps.contacts(s))
        messages = core.build_messages(s, 'Hello, I just moved here.')
        self.assertIn(PROFILE['name'], str(messages))
        self.assertIn('Just moved into Winterfield', str(messages))

    def test_all_homes_orientations_and_time_progress(self):
        import vacant_homes, sexuality, social_world, camera
        for key in vacant_homes.HOMES:
            s = self.create(home=key)
            self.assertTrue(camera.scene(s)['at_home'])
            self.assertEqual(town.loop.place_name(s), town.loop.HOUSES[s['player']][1])
            self.assertEqual(social_world.demographics(s['player'])['MBTI'], 'INFP')
            town.wait(s, 120)
            self.assertEqual(phone_apps.contacts(s), [])
        s = self.create(gender='Woman', sexuality='Lesbian')
        self.assertTrue(sexuality.compatible(s['player'], 'naomi'))
        self.assertFalse(sexuality.compatible(s['player'], 'garrett'))
        s = self.create(gender='Nonbinary', sexuality='Pansexual')
        self.assertTrue(sexuality.compatible(s['player'], 'sophie'))
        self.assertFalse(sexuality.compatible(s['player'], 'emily'))
        s = self.create(sexuality='Asexual')
        self.assertFalse(sexuality.compatible(s['player'], 'sophie'))
