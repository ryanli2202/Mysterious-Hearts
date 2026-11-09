import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import dating
import game_core as core
import groups
import social_world as social
import town


def scene(line, **fields):
    return dict(narration='A message arrives.', dialogue=line, memory=line,
                choices=['Okay.', 'Thank you.', 'Really?', 'I hear you.'], **fields)


class SocialWorldTests(unittest.TestCase):
    def test_friendship_and_romance_are_independent(self):
        for player, best in [('rei', ['garrett','emily']), ('garrett', ['rei','april'])]:
            s = core.fresh(player)
            for who in best: self.assertEqual(social.friendship(s, who), 'Best friends')
        s = core.fresh('rei')
        bond = s['relationships']['samantha']
        for scores, level in [((5,0),'Strangers'), ((40,10),'Acquaintances'), ((55,32),'Friends'),
                              ((77,60),'Close friends'), ((96,88),'Best friends')]:
            bond.update(trust=scores[0], closeness=scores[1], status='official')
            self.assertEqual(social.status_line(s,'samantha'), level+'  ·  Official')
        for player, sister in [('rei','yuriko'),('ivan','valentina')]:
            s = core.fresh(player)
            s['friendships'][sister].update(trust=0, closeness=0)
            self.assertEqual(social.status_line(s,sister), 'Siblings')
            self.assertFalse(dating.can_confess(s,sister))

    def test_affection_and_invitations_in_an_ordinary_chat(self):
        s = core.fresh('rei')
        self.assertFalse(dating.can_confess(s,'emily'))
        s['relationships']['emily']['trust'] = 100
        self.assertTrue(dating.can_confess(s,'emily'))
        core.commit(s, 'What did you want to tell me?', scene('I love you.', relationship_step='confession'))
        self.assertFalse(dating.can_confess(s,'emily'))
        self.assertEqual(social.romance(s,'emily'), '')
        core.commit(s, 'I love you too.', scene('I-I hoped you did.'))
        self.assertNotIn('date_session', s)
        core.commit(s, 'Will you go on a date with me?', scene('Yes! Saturday?', relationship_step='date',
                    date_topics=['Talk about the greenhouse', 'Sketch the view together']))
        self.assertEqual(social.status_line(s,'emily'), 'Best friends  ·  Date planned')
        self.assertEqual(s['emotions']['emily'], 'ecstatic')
        self.assertEqual(len(s['date_session']['goals']), 3)
        before = copy.deepcopy(s)
        with self.assertRaises(ValueError):
            core.commit(s, 'Again?', scene('Yes.', relationship_step='date', date_topics=[]))
        self.assertEqual(s, before)
        dating.cancel(s,'emily')
        s['relationships']['emily']['status'] = 'dating'
        core.commit(s, 'Can we be exclusive?', scene('Yes, I want that.', relationship_step='official'))
        self.assertEqual(social.status_line(s,'emily'), 'Best friends  ·  Official')
        self.assertEqual(s['turn'], 4)

    def test_recognition_and_confidences(self):
        s = core.fresh('rei')
        s['active'] = 'garrett'
        question = 'hey do you know Ivan Yeun?'
        move = json.loads(core.build_messages(s, question)[-1]['content'])
        fact = move['speaker_knows_person']
        self.assertEqual(fact['person'], 'ivan')
        with self.assertRaises(ValueError): social.check_recognition(fact, "I've never met him.")
        social.check_recognition(fact, "Yeah, we've done business. Why?")
        self.assertFalse(social.recognition_question(s,'garrett', 'How do you know if you won?'))
        for speaker, subject, topic in [('valentina','ivan','karaoke'), ('yuriko','rei','backstage'),
                                         ('april','garrett','king over')]:
            s = core.fresh('minsu')
            r = town.character_stats(s, speaker)
            r.update(trust=35, closeness=0)
            self.assertNotIn(topic, social.knowledge_direction(s,[speaker],subject))
            r.update(trust=85, closeness=75)
            self.assertIn(topic, social.knowledge_direction(s,[speaker],subject))

    def test_generation_repairs_a_denial_of_a_known_person(self):
        s = core.fresh('rei')
        s['active'] = 'garrett'
        question = 'Hey, do you know Ivan Yeun?'
        answer = scene("Yeah, we've done business, bro.", speaker='Garrett Han', addressee='Rei Takamura',
                       choices_speaker='Rei Takamura', input_tone='Other', emotions={'rei':'curious','garrett':'content'},
                       bond_moments={'garrett':'none'})
        choices = dict(choices_speaker='Rei Takamura', choices=answer['choices'],
                       personal_choices=['Tell me more.', 'How did you meet?', 'I know his work.', 'Still in touch?'])
        responses = [dict(answer, dialogue="Nope, never met him."), answer, choices]
        with patch.object(core, 'request', side_effect=[{'message':{'content':json.dumps(r)}} for r in responses]) as model:
            actual = core.generate(s, question)
        self.assertEqual(actual['dialogue'], answer['dialogue'])
        self.assertEqual(model.call_count, 2)
        self.assertIn('Acknowledge the established connection', model.call_args_list[1].args[1]['messages'][0]['content'])

    def test_profile_sources_survive_reload_without_unlocking_contacts(self):
        s = core.fresh('garrett')
        line = 'Ivan takes the second verse when we sing together.'
        s['active'] = 'valentina'
        core.hidden.mark_met(s,'valentina')
        note = dict(source='valentina', subject='ivan', quote=line)
        result = scene(line, profile_notes=[note, dict(note, quote='an unsent suggestion')])
        core.commit(s, 'Tell me about Ivan.', result)
        core.commit(s, 'Really?', result)
        self.assertEqual(len(s['profile_notes']['ivan']), 1)
        self.assertEqual(s['profile_notes']['ivan'][0]['source'], 'valentina')
        gid = groups.create_text(s, 'Friends', ['rei','emily'])
        groups.commit(s, gid, 'Who runs the boathouse?', dict(narration='A phone lights up.',
            choices=result['choices'], lines=[dict(speaker='Rei Takamura',text='I met Valentina at the boathouse.'),
            dict(speaker='Emily Fields',text='Oh!')], profile_notes=[dict(source='rei',subject='valentina',quote='I met Valentina at the boathouse.')]))
        self.assertTrue(core.hidden.contact(s,'valentina'))
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp)/'story.json'
            core.save(s,path)
            self.assertEqual(core.load(path)['profile_notes'], s['profile_notes'])
        self.assertEqual(social.demographics('emily'), dict(Sexuality='Straight', Birthday='November 4', MBTI='ISFP', Age='20', Height='154 cm'))
        self.assertTrue(social.initial_notes(core.fresh('rei'),'emily'))
        self.assertFalse(social.initial_notes(core.fresh('garrett'),'valentina'))
