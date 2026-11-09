import tempfile
import unittest
from pathlib import Path

from PIL import Image
import character_types
import contact_profiles
import conversation_lore
import four_aces
import game_core as core
import hidden_cast
import phone_numbers
import social_world
import world_loop


class FourAcesTests(unittest.TestCase):
    def test_starting_contacts_and_main_cast(self):
        for player in core.playable_cast.ORIGINAL:
            state = core.fresh(player)
            for who in four_aces.IDS:
                self.assertTrue(character_types.is_major(who))
                self.assertIn(who, state['routes'])
                self.assertIn(who, state['world']['cast'])
                self.assertEqual(hidden_cast.contact(state, who), player == 'ivan')
                self.assertEqual(bool(phone_numbers.saved_number(state, who)), player == 'ivan')
                self.assertFalse(hidden_cast.ensure(state)[who]['home'])
                for colleague in ('ivan', 'sylvanis'):
                    self.assertIn(colleague, social_world.personal_ties(who))

    def test_old_save_migration_retains_existing_progress(self):
        for player in ('ivan', 'rei'):
            state = core.fresh(player)
            phone_numbers.ensure(state)
            for who in four_aces.IDS:
                for bucket in ('routes', 'friendships', 'discoveries'):
                    state[bucket].pop(who, None)
                state['world']['cast'].pop(who)
                state['contact_profiles']['people'].pop(who)
                state['phone_numbers']['contacts'].pop(who, None)
                state['phone_numbers']['directory'].pop(who)
            for key in world_loop.ACE_BONDS:
                state['bond_details'].pop(key)
            state['bond_details']['neo:tyler']['trust'] = 23
            with tempfile.TemporaryDirectory(dir=core.ROOT / '.test-tmp') as directory:
                path = Path(directory) / 'old.json'
                core.save(state, path)
                loaded = core.load(path)
            for who in four_aces.IDS:
                self.assertIn(who, loaded['routes'])
                self.assertIn(who, loaded['world']['cast'])
                self.assertEqual(hidden_cast.contact(loaded, who), player == 'ivan')
            self.assertEqual(loaded['bond_details']['neo:tyler']['trust'], 23)
            self.assertIn('ivan', loaded['autonomy']['people']['martos']['relationships'])
            loaded['friendships']['martos']['trust'] = 19
            hidden_cast.ensure(loaded)
            world_loop.ensure(loaded)
            self.assertEqual(loaded['friendships']['martos']['trust'], 19)

    def test_cover_and_private_audience(self):
        state = core.fresh('ivan')
        for who, person in four_aces.CAST.items():
            public = str(contact_profiles.public(state, who, 'rei')) + hidden_cast.profile(who)
            self.assertNotIn('Ace of', public)
            self.assertNotIn(person['trait'], public)
            for level in range(4):
                ref = conversation_lore.speaker_reference(who, ['rei'], level, 'are you an ace?')
                self.assertNotIn('Writer-only Ace identity', ref)
                self.assertNotIn('Shared Ace working history', ref['Vendetta AU'])
                self.assertIn('Do not reveal or confirm', ref['Vendetta AU']['Ace disclosure boundary'])
            private = conversation_lore.speaker_reference(who, ['ivan'], 0, 'work')
            self.assertIn('Shared Ace working history', private['Vendetta AU'])
            mixed = four_aces.private_context(who, ['ivan', 'rei'])
            self.assertNotIn('Shared Ace working history', mixed)
        self.assertEqual(four_aces.private_context('rei', ['ivan']), {})
        self.assertEqual(four_aces.CAST['mavis']['birthday'], 'Unknown')

    def test_occasional_headquarters_and_assets(self):
        numbers = []
        for who in four_aces.IDS:
            visits = [world_loop.appointment(who, day * 1440 + 21 * 60)[1] == hidden_cast.HQ for day in range(8)]
            self.assertEqual(sum(visits), 2)
            self.assertTrue(hidden_cast.hq_access({}, who))
            self.assertNotEqual(world_loop.appointment(who, 12 * 60)[1], hidden_cast.HQ)
            numbers.append(phone_numbers.NUMBERS[who])
            for folder, filename in [('portraits', who + '-selection.png'), ('profiles', who + '.png')]:
                with Image.open(core.ROOT / 'assets' / folder / filename) as im:
                    self.assertGreaterEqual(min(im.size), 1024)
                    if folder == 'portraits':
                        self.assertEqual(im.mode, 'RGBA')
                        self.assertEqual(im.getchannel('A').getextrema(), (0, 255))
            self.assertIn('Breakfast', conversation_lore.everyday_favourites(who))
        self.assertEqual(len(set(numbers)), 4)
        self.assertEqual(phone_numbers.NUMBERS['garrett'], '12025550100')


if __name__ == '__main__':
    unittest.main()
