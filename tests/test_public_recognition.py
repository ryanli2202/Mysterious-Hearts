import copy
import unittest

import game_core as core
import social_world as social


class PublicRecognitionTests(unittest.TestCase):
    def test_strangers_recognise_all_three_public_careers_without_state_changes(self):
        s = core.fresh('rei')
        before = copy.deepcopy(s)
        ref = social.public_recognition(s, 'rosa', ['rei', 'elias', 'ivan'], texting=False)
        for person, career in [('rei', 'model'), ('elias', 'actor'), ('ivan', 'K-pop idol')]:
            self.assertIn(career, ref['people'][person]['public_reputation'])
        self.assertFalse(ref['people']['elias']['established_personal_connection'])
        self.assertEqual(s, before)

    def test_old_friends_are_not_first_introductions(self):
        s = core.fresh('rei')
        ref = social.public_recognition(s, 'garrett', ['rei'], texting=False)
        self.assertTrue(ref['people']['rei']['established_personal_connection'])
        self.assertIn('must not repeat first-meeting surprise', ref['direction'])

    def test_masked_celebrity_and_text_boundaries(self):
        s = core.fresh('rei')
        s['world']['location'] = 'syndicate_hq'
        s['world']['cast'].setdefault('elias', {})['location'] = 'syndicate_hq'
        ref = social.public_recognition(s, 'rosa', ['elias'], texting=False)
        self.assertTrue(ref['people']['elias']['face_concealed'])
        self.assertIn('must not be identified through fame', ref['direction'])
        ref = social.public_recognition(s, 'rosa', ['elias'], texting=True)
        self.assertIn('anonymous handle alone', ref['direction'])
        self.assertIn('No physical double take', ref['direction'])

    def test_shared_reference_and_nonfamous_people(self):
        s = core.fresh('rei')
        ref = social.reference_for(s, 'rosa', ['rei', 'elias', 'emily'], '', texting=False)
        people = ref['Public recognition of listeners']['people']
        self.assertEqual(set(people), {'rei', 'elias'})
        self.assertIn('Public recognition of listeners', social.knowledge_direction(s, ['rosa'], texting=False))


if __name__ == '__main__':
    unittest.main()
