import tempfile
import copy
import unittest
from pathlib import Path

import game_core as core
import protectiveness
import relationship_dynamics as dynamics
import social_world
import town
import groups
import dating


class RelationshipDynamicsTests(unittest.TestCase):
    def setUp(self):
        self.s = core.fresh('garrett')
        self.s['relationships']['emily'].update(trust=65, closeness=60)

    def event(self, kind, detail='Call tomorrow', ref=0, due=-1, speaker=None, quote=None, owners=None):
        speaker = speaker or ('emily' if kind in ('boundary', 'proposal', 'loyalty', 'forgive') else 'garrett')
        quote = quote or f'{kind}: {detail}'
        event = dict(kind=kind, who='emily', source=speaker, quote=quote, detail=detail, ref=ref, due_minutes=due)
        dynamics.commit(self.s, {'relationship_events': [event]},
                        {'emily': quote if speaker == 'emily' else 'I hear you.'},
                        quote if speaker == 'garrett' else '', owners=owners)
        return event

    def test_promise_kept_once_and_private_conduct_does_not_change_approval(self):
        protectiveness.observe(self.s, 'emily', 'flirt', ['rei'])
        self.event('promise')
        self.event('kept', ref=1)
        self.event('kept', ref=1, quote='Another claim about the same promise')
        self.assertEqual(self.s['relationships']['emily']['trust'], 70)
        self.assertEqual(self.s['protectiveness']['rei:emily']['approval'], 0)
        self.event('promise', detail='Attend the flower show')
        self.event('kept', detail='Attended the flower show', ref=2, owners=['garrett', 'emily', 'rei'])
        self.assertEqual(self.s['protectiveness']['rei:emily']['approval'], 5)

    def test_deadline_is_overdue_once_and_can_be_followed_up(self):
        self.event('promise', due=2)
        town.loop.advance(self.s, 3)
        self.assertEqual(dynamics.person(self.s, 'emily')['promises'][0]['status'], 'overdue')
        trust = self.s['relationships']['emily']['trust']
        dynamics.tick(self.s)
        self.assertEqual(self.s['relationships']['emily']['trust'], trust)
        self.event('kept', ref=1)
        self.assertEqual(dynamics.person(self.s, 'emily')['promises'][0]['status'], 'kept')
        self.assertIn('unresolved_harm', self.s['relationships']['emily'])

    def test_boundary_and_specific_repair_require_later_day_and_forgiveness(self):
        self.event('boundary', detail='Please do not tease me about my stutter')
        self.event('crossed', detail='Teased her stutter', ref=1)
        with self.assertRaises(ValueError):
            town.relationship(self.s, 'emily', 'repair')
        self.event('acknowledge', detail='I hurt you by mocking your stutter')
        self.event('changed', detail='Stopped the joke and listened')
        self.assertFalse(dynamics.repair_ready(self.s, 'emily'))
        self.event('forgive', quote='I forgive you now')
        self.assertIn('unresolved_harm', self.s['relationships']['emily'])
        self.s['world']['minute'] += 1440
        self.event('changed', detail='Respected her request during another conversation')
        self.assertTrue(dynamics.repair_ready(self.s, 'emily'))
        self.event('forgive', quote='I can forgive you after seeing you follow through')
        self.assertNotIn('unresolved_harm', self.s['relationships']['emily'])
        trust = self.s['relationships']['emily']['trust']
        self.event('forgive', quote='I forgive you again')
        self.assertEqual(self.s['relationships']['emily']['trust'], trust)

    def test_proposals_need_readiness_and_do_not_start_date(self):
        self.event('proposal', detail='Would you like to go to the flower show?')
        p = dynamics.person(self.s, 'emily')
        self.assertEqual(len(p['proposals']), 1)
        self.assertNotIn('date_session', self.s)
        self.event('proposal', detail='Would you like to meet my friends?')
        self.assertEqual(len(p['proposals']), 1)
        self.event('decline', ref=1)
        self.assertFalse(dynamics.proposal_allowed(self.s, 'emily'))
        self.s['world']['minute'] += 4320
        self.assertTrue(dynamics.proposal_allowed(self.s, 'emily'))
        self.event('proposal', detail='Would you like to meet my friends?')
        self.event('accept', ref=2)
        self.assertEqual(p['proposals'][1]['status'], 'accepted')
        self.assertNotIn('date_session', self.s)

    def test_private_records_are_not_given_to_group(self):
        self.event('promise')
        self.event('boundary', detail='Ask before kissing me in public')
        self.event('loyalty', detail='Rei cares about me, but I make my own choices')
        context = dynamics.context(self.s, 'emily', ['garrett', 'sophie'])
        self.assertEqual(context['promises'], [])
        self.assertEqual(context['boundaries'], [])
        self.assertEqual(context['loyalties'], [])
        self.assertIn('Call tomorrow', '\n'.join(dynamics.notebook(self.s, 'emily')))

    def test_unspoken_evidence_and_speaker_forgery_are_ignored(self):
        event = dict(kind='promise', who='emily', source='garrett', quote='I promise to call',
                     detail='Call', ref=0, due_minutes=-1)
        dynamics.commit(self.s, {'relationship_events': [event]}, {'emily': 'Hello'}, 'Hi')
        self.assertEqual(dynamics.person(self.s, 'emily')['promises'], [])
        self.event('boundary', speaker='garrett')
        self.assertEqual(dynamics.person(self.s, 'emily')['boundaries'], [])

    def test_save_load_and_schema(self):
        self.event('promise')
        schema = dict(properties={}, required=[])
        social_world.add_note_schema(schema, self.s, ['emily'])
        self.assertIn('relationship_events', schema['required'])
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'story.json'
            core.save(self.s, path)
            loaded = core.load(path)
        self.assertEqual(loaded['relationship_dynamics'], self.s['relationship_dynamics'])

    def test_context_is_read_only_for_new_local_and_existing_contacts(self):
        before = copy.deepcopy(self.s)
        for who in ('Maya', 'emily', 'rei'):
            dynamics.context(self.s, who, ['garrett'])
        self.assertEqual(self.s, before)

    def test_private_completion_is_not_shared_with_original_audience(self):
        self.event('promise', owners=['garrett', 'emily', 'sophie'])
        self.event('kept', ref=1)
        self.assertEqual(dynamics.context(self.s, 'emily', ['garrett', 'sophie'])['promises'], [])

    def test_group_promise_and_protector_disclosure(self):
        gid = groups.create_text(self.s, 'Friends', ['emily', 'rei'])
        text = 'Emily, I promise to call tomorrow.'
        data = dict(narration='A message arrives.', choices=['Okay.', 'Thanks.', 'Hello.', 'Good night.'],
                    lines=[dict(speaker=core.CONTACTS[m][0], text='I hear you.') for m in ('emily', 'rei')],
                    relationship_events=[dict(kind='promise', who='emily', source='garrett', quote=text,
                        detail='Call tomorrow', ref=0, due_minutes=-1)])
        groups.commit(self.s, gid, text, data)
        self.assertIn('rei', dynamics.peek(self.s, 'emily')['promises'][0]['owners'])
        text = 'Rei, Emily and I are dating.'
        dynamics.commit(self.s, {'relationship_events': [dict(kind='disclosure', who='rei', source='garrett',
            quote=text, detail='emily', ref=0, due_minutes=-1)]}, {'rei': 'Treat her well.'}, text)
        self.assertEqual(self.s['protectiveness']['rei:emily']['source'], 'player disclosure')

    def test_date_proposal_uses_existing_acceptance_flow(self):
        self.event('proposal', detail='Would you like a date?')
        proposal = dynamics.peek(self.s, 'emily')['proposals'][0]
        proposal['proposal_type'] = 'date'
        schema = dict(properties={}, required=[])
        self.assertIn('explicit player acceptance', dating.conversation_direction(self.s, 'emily', schema, True))
        dating.accept(self.s, 'emily', 'date', dict(conversation='Talk about flowers', activity='Take a walk', kiss=dating.KISS))
        self.assertEqual(proposal['status'], 'accepted')
        self.assertEqual(self.s['date_session']['partner'], 'emily')

    def test_single_chat_commit_records_actual_promise(self):
        self.s['active'] = 'emily'
        text = 'I promise to call you tomorrow.'
        scene = dict(narration='A message arrives.', dialogue='Thank you. I will look forward to it.',
                     memory='A promise to call.', choices=['Okay.', 'Thanks.', 'See you.', 'Good night.'],
                     relationship_events=[dict(kind='promise', who='emily', source='garrett', quote=text,
                                               detail='Call tomorrow', ref=0, due_minutes=-1)])
        core.commit(self.s, text, scene)
        self.assertEqual(dynamics.person(self.s, 'emily')['promises'][0]['detail'], 'Call tomorrow')


if __name__ == '__main__':
    unittest.main()
