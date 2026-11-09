import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import game_core as core
import hidden_cast as hidden
import phone_numbers
import town
import world_loop
import conversation_lore
import social_world
import the_crow

class CrowTests(unittest.TestCase):
    def test_starting_contacts_and_existing_save(self):
        for player in core.PLAYERS:
            s = core.fresh(player)
            self.assertEqual(hidden.contact(s, 'crow'), player == 'ivan')
            self.assertEqual(bool(phone_numbers.saved_number(s, 'crow')), player == 'ivan')
            for bucket in ('routes', 'friendships', 'discoveries'):
                s[bucket].pop('crow', None)
            s['world']['cast'].pop('crow')
            with tempfile.TemporaryDirectory(dir=core.ROOT / '.test-tmp') as directory:
                path = Path(directory) / 'save.json'
                core.save(s, path)
                loaded = core.load(path)
            self.assertIn('crow', loaded['routes'])
            self.assertEqual(hidden.contact(loaded, 'crow'), player == 'ivan')
            self.assertEqual(loaded['world']['cast']['crow']['location'], hidden.HQ)

    def test_meeting_does_not_grant_private_number(self):
        s = core.fresh('rei')
        with self.assertRaises(ValueError): hidden.mark_met(s, 'crow')
        with self.assertRaises(ValueError): phone_numbers.add(s, phone_numbers.number(s, 'crow'))
        town.end_hangouts(s)
        # Exercise an authorised visitor without granting high official status.
        with patch.object(hidden, 'SYNDICATE_MEMBERS', hidden.SYNDICATE_MEMBERS | {'rei'}):
            town.travel(s, hidden.HQ)
            town.meet(s, 'crow')
            self.assertTrue(hidden.known(s, 'crow'))
            self.assertFalse(hidden.contact(s, 'crow'))
            self.assertIsNone(phone_numbers.saved_number(s, 'crow'))
            with self.assertRaises(ValueError): hidden.add_contact(s, 'crow')
            with self.assertRaises(ValueError): hidden.discover_home(s, 'crow')
        self.assertFalse(hidden.visible_place(s, hidden.HQ))

    def test_no_public_social_activity(self):
        import phone_apps, grove_photos, grove_reactions
        s = core.fresh('ivan')
        data = phone_apps.ensure(s)
        s['world']['minute'] += 10000
        phone_apps.sync(s)
        self.assertNotIn('crow', data['grove_next'])
        self.assertNotIn('crow', data['grove_photo_next'])
        with self.assertRaises(ValueError): phone_apps.queue_grove(s, 'crow')

    def test_headquarters_only_and_private_identity(self):
        s = core.fresh('ivan')
        for minute in range(0, 14 * 1440, 60):
            self.assertEqual(world_loop.appointment('crow', minute)[1], hidden.HQ)
        with self.assertRaises(ValueError): town.summon(s, 'crow')
        with self.assertRaises(ValueError): world_loop.start_trip(s, 'crow', 'park')
        world_loop.advance(s, 60)
        self.assertEqual(s['world']['cast']['crow']['location'], hidden.HQ)
        for level in range(4):
            ref = conversation_lore.speaker_reference('crow', ['ivan'], level, 'your birthday and childhood')
            self.assertEqual(ref['How much to share'], the_crow.BOUNDARY)
        for field in ('MBTI', 'Birthday', 'Height', 'Age'):
            self.assertEqual(social_world.demographics('crow')[field], 'Unknown')
        self.assertIn('sylvanis', social_world.personal_ties('crow'))
        self.assertNotIn('crow_home', town.LOCATIONS)

    def test_voice_reaches_solo_text_and_spoken_prompts(self):
        import json
        s = core.fresh('ivan')
        s['active'] = 'crow'
        # An old bland reply must not supply the current speaking style.
        s['routes']['crow']['history'].append(dict(role='assistant', content='Hey Ivan, how was your day?'))
        for channel in ('text', 'in_person'):
            s['routes']['crow']['channel'] = channel
            messages = core.build_messages(s, 'why was I summoned?')
            self.assertIn(the_crow.VOICE, messages[0]['content'])
            focus = json.loads(messages[-1]['content'])['reference_for_reply']
            self.assertIn(the_crow.TEMPERAMENT, focus)
            self.assertIn(the_crow.SUMMONS_DIRECTION, focus)
            self.assertIn(the_crow.BOUNDARY, focus)
            self.assertNotIn('Polymath', hidden.profile('crow'))

    def test_voice_reaches_group_generation_without_live_ai(self):
        import json
        import groups
        s = core.fresh('ivan')
        town.travel(s, hidden.HQ)
        s['world']['cast']['sylvanis'].update(location=hidden.HQ, journey=None)
        groups.open_group(s, ['crow', 'sylvanis'])
        for channel in ('in_person', 'text'):
            group = s['groups'][s['active_group']]
            group['channel'] = channel
            # Capture the actual provider boundary; never submit an AI request.
            with patch.object(core, 'request', side_effect=RuntimeError('captured')) as request:
                with self.assertRaisesRegex(RuntimeError, 'captured'):
                    groups.generate(s, s['active_group'], 'why was I summoned?')
            messages = request.call_args.args[1]['messages']
            self.assertIn(the_crow.VOICE, messages[0]['content'])
            context = json.loads(messages[-1]['content'])
            self.assertIn(the_crow.SUMMONS_DIRECTION, context['reference_for_reply']['crow'])
            self.assertIn(the_crow.TEMPERAMENT, context['reference_for_reply']['crow'])
            self.assertIn('professional Syndicate', messages[0]['content'])

if __name__ == '__main__': unittest.main()
