import json
import unittest
from unittest.mock import patch

import conversation_lore as lore
import game_core as core
import groups
import social_world as social
import town


class ConversationLoreTests(unittest.TestCase):
    def test_crow_addresses_and_aces_restraint_reach_dialogue_guidance(self):
        import the_crow
        s = core.fresh('ivan')
        for who in the_crow.OFFICIALS:
            with self.subTest(who=who):
                reference = lore.speaker_reference(who, ['crow', 'sylvanis'], 0, 'Bro', s)
                self.assertEqual(reference['Private Crow address and deference canon'], the_crow.ADDRESS_CANON)
                focus = lore.turn_focus(s, who, ['crow', 'sylvanis'], 0, 'Bro')
                for phrase in ('"master"', '"Crow"', '"Mr. Crow"', '"Bird-man"', '"Bro"',
                               'reluctant', 'given his position', 'not approval', 'concealed Syndicate identities'):
                    self.assertIn(phrase, focus)
        self.assertNotIn('Private Crow address and deference canon',
                         lore.speaker_reference('emily', ['ivan'], 0, '', s))

    def test_charles_news_matters_at_low_trust_and_in_pronoun_followups(self):
        s = core.fresh('ivan')
        s['active'] = 'garrett'
        s['_text_only'] = True
        town.character_stats(s, 'garrett').update(trust=5, closeness=0)
        for cue in ("It's about your brother.", "You don't have to. I found him.",
                    "I did, he's working for the syndicate at the moment."):
            prompt = core.build_messages(s, cue)[0]['content']
            self.assertIn(json.dumps(lore.CHARLES_NEWS)[1:-1], prompt)
            self.assertNotIn('You can say Charles is your brother and leave it there.', prompt)
            self.assertNotIn('charles_disclosure', s)
        self.assertNotIn('Receiving news about Charles',
                         lore.speaker_reference('emily', ['ivan'], 0, '', s))

    def test_charles_news_preserves_confirmed_reunion(self):
        s = core.fresh('ivan')
        s['active'] = 'garrett'
        s['charles_disclosure'] = dict(stage=4, reporter='ivan', journal=[])
        focus = lore.turn_focus(s, 'garrett', ['ivan'], 3, 'Any news about Charles?')
        self.assertIn('met privately in the Glasshouse', focus)
        self.assertNotIn('you still have no word from him', focus)
        self.assertIn('preserve that continuity', focus)

    def test_faction_npc_tables_reuse_authored_identity(self):
        import gang_leaders
        import keisuke
        tables = lore.character_tables()
        self.assertEqual(tables[keisuke.NAME]['Appearance'], keisuke.APPEARANCE)
        self.assertIn(keisuke.BACKSTORY, tables[keisuke.NAME]['Confidence'])
        for name, person in gang_leaders.BY_NAME.items():
            self.assertEqual(tables[name]['Appearance'], person['appearance'])
            self.assertEqual(tables[name]['Personal'], person['detail'])
        for name in (keisuke.NAME, *gang_leaders.NAMES):
            self.assertEqual(tables[name]['Character type'], 'town NPC')
            self.assertEqual(lore.everyday_favourites(name), {})
            for level in range(4):
                ref = lore.speaker_reference(name, ['rei'], level, '')
                self.assertEqual(ref['How much to share'], tables[name]['Disclosure boundary'])
                self.assertIn('Do not supply favourites', ref['Using preferences'])

    def test_faction_npc_private_backstory_is_not_a_low_trust_disclosure(self):
        import keisuke
        public = lore.speaker_reference(keisuke.NAME, ['rei'], 0, '')
        private = lore.speaker_reference(keisuke.NAME, ['rei'], 3, '')
        self.assertNotIn(keisuke.BACKSTORY, str(public))
        self.assertIn(keisuke.BACKSTORY, private['Confidence'])
        self.assertIn('not automatically', private['How much to share'])
        daichi = lore.speaker_reference('Daichi Kurose', ['rei'], 0, '')
        self.assertNotIn('Rei destroyed', str(daichi))
        self.assertIn('private history', daichi['How much to share'])

    def test_portrait_appearance_is_available_for_every_speaker(self):
        for who, guide in lore.character_tables().items():
            self.assertTrue(guide.get('Appearance'), who)
            self.assertTrue(guide.get('Portrait style'), who)

    def test_named_appearance_question_uses_the_known_subjects_portrait(self):
        s = core.fresh('rei')
        s['active'] = 'garrett'
        prompt = core.build_messages(s, "Do you think Amy's cute?")[0]['content']
        self.assertIn('softly waved ginger bob', prompt)
        self.assertIn('conventionally attractive', prompt)
        appearance = social.appearance_reference(s, 'garrett', ['rei'], "Do you think Amy's cute?", texting=True)
        self.assertIn('amy', appearance['People'])
        self.assertNotIn('emily', appearance['People'])
        self.assertIn('without romantic interest', appearance['Guidance'])
        # Undiscovered people are not made recognisable merely by naming them.
        unknown = social.appearance_reference(s, 'garrett', ['rei'], 'What does Lena look like?', texting=True)
        self.assertNotIn('lena', unknown['People'])
        self.assertIn('lena', unknown['Not known by sight from this reference'])

    def test_today_compliment_respects_texting_and_the_selected_outfit(self):
        s = core.fresh('rei')
        s['active'] = 'emily'
        s['world']['player_outfit'] = 'Black leather moto jacket'
        phone = social.appearance_reference(s, 'emily', ['rei'], 'Do I look good today?', texting=True)
        self.assertIn('shaggy layered black hair', phone['People']['rei']['Recognisable features'])
        self.assertNotIn('Selected outfit in this in-person scene', phone['People']['rei'])
        self.assertIn('no live view', phone['Guidance'])
        face_to_face = social.appearance_reference(s, 'emily', ['rei'], 'Do I look good today?', texting=False)
        self.assertEqual(face_to_face['People']['rei']['Selected outfit in this in-person scene'],
                         'Black leather moto jacket')
        self.assertIn('automatic confession', face_to_face['Guidance'])

    def test_marcus_memories_have_personality_and_distinct_friendships(self):
        anchors = {'rei': 'temporary custody concluded',
                   'emily': 'management apologises',
                   'sophie': 'Commentary is not cardio'}
        for speaker, anchor in anchors.items():
            listeners = [name for name in anchors if name != speaker]
            reference = lore.speaker_reference(speaker, listeners, 0, 'What should we make?')
            memory = reference['Marcus as a person — shared school memories']
            self.assertIn(anchor, memory)
            self.assertIn('local weather', memory)
            self.assertIn('get defensive about criticism', memory)
            self.assertIn('Do not append Joseph, suicide or a grief lesson', memory)
            for other, other_anchor in anchors.items():
                if speaker != other:
                    self.assertNotIn(other_anchor, memory)
            mixed = lore.speaker_reference(speaker, [*listeners, 'ivan'], 0, '')
            self.assertNotIn('Marcus as a person — shared school memories', mixed)
        self.assertNotIn('marcus', lore.character_tables())
        # A new, low-trust conversation still receives the memories without
        # the player explaining Marcus or explicitly asking about the loss.
        s = core.fresh('rei')
        s['active'] = 'emily'
        town.character_stats(s, 'emily').update(trust=5, closeness=0)
        prompt = core.build_messages(s, 'Working on any models today?')[0]['content']
        self.assertIn('management apologises', prompt)
        self.assertIn('paper pigeon', prompt)

    def test_marcus_is_remembered_by_school_friends_without_explanation(self):
        for speaker in ('rei', 'emily', 'sophie'):
            listeners = [name for name in ('rei', 'emily', 'sophie') if name != speaker]
            reference = lore.speaker_reference(speaker, listeners, 0, 'Marcus')
            memory = reference['School history already known to this audience']
            self.assertIn('Marcus', memory)
            self.assertIn('died by suicide', memory)
            self.assertNotIn('School history already known to this audience',
                             lore.speaker_reference(speaker, [*listeners, 'ivan'], 0, ''))
        s = core.fresh('rei')
        for speaker in ('emily', 'sophie'):
            facts = social.relationship_reference(s, speaker, ['rei'], 'Joseph?')
            lore.check_observer(facts, speaker, 'Joseph?', 'I remember Marcus died by suicide.')
            lore.check_observer(facts, speaker, 'Joseph?', 'Joseph bullied Marcus.')
            with self.assertRaises(ValueError):
                lore.check_observer(facts, speaker, 'Joseph?', 'I saw them bullying Marcus behind the gym.')

    def test_school_friends_react_to_joseph_without_a_new_disclosure(self):
        s = core.fresh('rei')
        for speaker, reaction in [('emily', 'quiet anger'), ('sophie', 'anger and contempt')]:
            s['active'] = speaker
            town.character_stats(s, speaker).update(trust=5, closeness=0)
            prompt = core.build_messages(s, 'Joseph was at Blackstone today.')[0]['content']
            self.assertIn('already knows Joseph bullied Marcus', prompt)
            self.assertIn(reaction, prompt)
            self.assertIn('Rei', prompt)
            mixed = lore.speaker_reference(speaker, ['rei', 'ivan'], 0, 'Joseph?')
            self.assertIn('Reaction to Joseph', mixed)
            self.assertNotIn('School history already known to this audience', mixed)
            self.assertNotIn('bullied Marcus', str(mixed))
        facts = social.relationship_reference(s, 'minsu', ['rei'], 'Joseph?')
        self.assertNotIn('already knows Joseph bullied Marcus', str(facts))
        with self.assertRaises(ValueError):
            lore.check_observer(facts, 'minsu', 'Joseph?', 'Joseph bullied Marcus.')

    def test_garrett_knows_marcus_through_reis_disclosure_not_as_an_eyewitness(self):
        s = core.fresh('rei')
        s['active'] = 'garrett'
        town.character_stats(s, 'garrett').update(trust=5, closeness=0)
        prompt = core.build_messages(s, 'Joseph was at Blackstone today.')[0]['content']
        self.assertIn('paper-pigeon', prompt)
        self.assertIn('enduring anger and contempt', prompt)
        self.assertIn('Garrett never met Marcus', prompt)
        for who, other in [('garrett', 'rei'), ('rei', 'garrett')]:
            reference = lore.speaker_reference(who, [other], 0, '')
            self.assertIn('folded clean towels', reference['History both people already know'])
        facts = social.relationship_reference(s, 'garrett', ['rei'], 'Joseph?')
        lore.check_observer(facts, 'garrett', 'Joseph?', 'You told me Joseph bullied Marcus. I believe you.')
        with self.assertRaises(ValueError):
            lore.check_observer(facts, 'garrett', 'Joseph?', 'I saw them bullying Marcus behind the gym.')
        mixed = social.reference_for(s, 'garrett', ['rei', 'ivan'], 'Joseph?')
        self.assertIn('Reaction to Joseph', mixed)
        self.assertNotIn('folded clean towels', str(mixed))
        self.assertNotIn('already knows Joseph bullied Marcus', str(mixed))

    def test_hamayashi_history_is_shared_by_siblings_without_recovered_memories(self):
        for speaker, listener in [('rei', 'yuriko'), ('yuriko', 'rei')]:
            private = lore.speaker_reference(speaker, [listener], 0, 'Hamayashi-kai')
            history = private['History both people already know']
            for fact in ('Hamayashi-kai', 'training and torture', 'entire clan',
                         'misogynistic', 'Sheltered does not mean safe', 'memory gaps'):
                self.assertIn(fact, history)
            group = lore.speaker_reference(speaker, [listener, 'emily'], 0, '')
            self.assertNotIn('training and torture', str(group))
            self.assertNotIn('entire clan', str(group))
        s = core.fresh('rei')
        focus = lore.turn_focus(s, 'yuriko', ['rei'], 0, 'Do you remember Hamayashi-kai?')
        self.assertIn('human weapon', focus)
        self.assertIn('newly recovered memory', focus)
        self.assertIn('Yakuza', lore.topic_reference('yuriko', 'Hamayashi-kai'))

    def test_every_speaker_has_all_favourites_available_without_a_trust_gate(self):
        for speaker, guide in lore.character_tables().items():
            reference = lore.speaker_reference(speaker, ['minsu'], 0, '')
            preferences = reference['Everyday favourites']
            self.assertEqual(preferences, guide['Everyday favourites'])
            if speaker == 'takeo':
                self.assertIn('strength, domination', preferences)
                self.assertIn('Other tastes unknown', preferences)
                self.assertIn('Do not invent favourite', reference['Using preferences'])
                continue
            if preferences == 'Unknown':
                self.assertEqual(preferences, 'Unknown')
                self.assertIn('Do not supply favourites', reference['Using preferences'])
                continue
            for category in ('Breakfast', 'Lunch', 'Dinner', 'Snack', 'Drink',
                             'TV show', 'Movie', 'Book', 'Author'):
                self.assertIn(category + ': ', preferences, (speaker, category))
        # A non-reader has an explicit answer rather than a fabricated title.
        self.assertIn('Book: None', lore.character_tables()['sophie']['Everyday favourites'])
        # Knowing someone does not automatically expose their favourite order.
        emily = lore.speaker_reference('emily', ['garrett'], 0, '')
        self.assertNotIn('Kitchen Confidential', str(emily))

    def test_garrett_meeting_stories_are_reciprocal_and_disclosures_stay_private(self):
        for other, anchor in [('rei', 'broken seam'), ('emily', 'steam would spoil'),
                              ('sophie', 'conversation time counts')]:
            for speaker, listener in [('garrett', other), (other, 'garrett')]:
                private = lore.speaker_reference(speaker, [listener], 0, '')
                self.assertIn(anchor, private['History both people already know'])
                group = lore.speaker_reference(speaker, [listener, 'minsu'], 0, '')
                self.assertIn(anchor, str(group['Everyday shared memories with people present']))
                self.assertNotIn('Rei deliberately told Garrett', str(group))
        history = lore.speaker_reference('garrett', ['rei'], 0, '')['History both people already know']
        self.assertIn('Rei deliberately told Garrett', history)
        self.assertIn('does NOT know that Rei killed the clan', history)
        self.assertIn('not from being present during school', history)
        for listener in ('emily', 'sophie', 'ivan'):
            reference = lore.speaker_reference('garrett', [listener], 0, '')
            self.assertNotIn('Rei deliberately told Garrett', str(reference))

    def test_expanded_history_is_present_without_player_explanation_or_save_memory(self):
        for player, speaker, callback in [
            ('rei', 'sophie', 'expert walking assessment'),
            ('rei', 'emily', 'roof supervisor'),
            ('rei', 'yuriko', 'grocery lists'),
            ('garrett', 'april', 'Enough water'),
            ('ivan', 'valentina', 'repair concert'),
            ('minsu', 'amy', 'Independent texture review'),
        ]:
            s = core.fresh(player)
            s['active'] = speaker
            town.character_stats(s, speaker).update(trust=5, closeness=0)
            s['routes'][speaker]['memory'] = ''
            s['routes'][speaker]['history'] = []
            prompt = core.build_messages(s, 'Hey, how is your day?')[0]['content']
            self.assertIn(callback.casefold(), prompt.casefold(), (player, speaker))
            self.assertIn('without asking the player to explain', prompt)
            # The same memory is accessible to the other participant, too.
            reverse = social.reference_for(s, player, [speaker], '')
            self.assertIn('History both people already know', reverse)

    def test_group_callbacks_are_available_to_participants_not_uninvolved_speakers(self):
        s = core.fresh('rei')
        for speaker, other in [('emily', 'sophie'), ('sophie', 'emily')]:
            reference = social.reference_for(s, speaker, ['rei', other, 'ivan'], '')
            shared = reference['Everyday shared memories with people present']
            self.assertIn('slowest relay', str(shared))
            self.assertIn('rei', shared)
            self.assertIn(other, shared)
            self.assertNotIn('ivan', shared)
            self.assertNotIn('History both people already know', reference)
        outsider = social.reference_for(s, 'ivan', ['rei', 'emily', 'sophie'], '')
        self.assertNotIn('slowest relay', str(outsider))
        # Even when a sibling is present, the mixed audience gets everyday
        # family memories, never the pair's private history.
        for speaker, sibling, secret in [('yuriko', 'rei', 'killed'),
                                          ('valentina', 'ivan', 'signed order'),
                                          ('april', 'garrett', 'Kit')]:
            shared = lore.speaker_reference(speaker, [sibling, 'minsu'], 0, '')
            self.assertIn('Everyday shared memories with people present', shared)
            self.assertNotIn('History both people already know', shared)
            self.assertNotIn(secret, str(shared))

    def test_expanded_connections_are_recognised_without_disclosing_memories(self):
        s = core.fresh('minsu')
        for speaker, other in [('yuriko', 'sophie'), ('sophie', 'yuriko'),
                                ('yuriko', 'emily'), ('emily', 'yuriko')]:
            fact = social.recognition_question(s, speaker, f'Do you know {other}?')
            self.assertEqual(fact['person'], other)
            self.assertIn('school', fact['firsthand'])
            self.assertNotIn('clan', fact['firsthand'])
            with self.assertRaises(ValueError):
                social.check_recognition(fact, "I've never met them.")

    def test_group_generation_sends_school_history_on_an_ordinary_opening(self):
        s = core.fresh('rei')
        gid = groups.create_text(s, 'School friends', ['emily', 'sophie'])
        # Inspect the real provider boundary without making a network request.
        with patch.object(core, 'request', side_effect=RuntimeError('captured')) as request:
            with self.assertRaisesRegex(RuntimeError, 'captured'):
                groups.generate(s, gid, 'Any plans for today?')
        prompt = request.call_args.args[1]['messages'][0]['content']
        self.assertIn('slowest relay', prompt)
        self.assertIn('roof supervisor', prompt)
        self.assertIn('expert walking assessment', prompt)
        self.assertIn('do not force one into every reply', prompt)
        self.assertNotIn('killed his clan', prompt)
        self.assertNotIn('signed order', prompt)

    def test_every_speaker_has_an_authored_table_and_an_audience(self):
        locals_ = {name for name, *_ in [*town.NPCS, *town.VENUE_STAFF.values(), town.HQ_EXECUTIVE]}
        self.assertEqual(set(lore.character_tables()), set(core.CONTACTS) | locals_)
        for who, guide in lore.character_tables().items():
            for field in (*lore.LAYERS, 'World knowledge'):
                self.assertTrue(guide[field], (who, field))
            for player in core.PLAYERS.keys() - {who}:
                self.assertTrue(guide.get('With ' + player.title()) or guide.get('With visitors'), (who, player))

    def test_garrett_discloses_more_as_both_scores_grow(self):
        s = core.fresh('ivan')
        s['active'] = 'garrett'
        stats = town.character_stats(s, 'garrett')
        cue = 'What happened to Charles?'
        anchors = ('missing older brother', 'he is still looking for him', 'missed two calls', 'toasting shrimp shells')
        for trust, close, count in [(45,18,1), (55,32,2), (70,50,3), (92,88,4), (35,95,1), (90,0,1)]:
            stats.update(trust=trust, closeness=close, attraction=100)
            prompt = core.build_messages(s, cue)[0]['content']
            for index, anchor in enumerate(anchors):
                self.assertEqual(anchor in prompt, index < count, (trust, close, anchor))
            self.assertNotIn('undercover inside', prompt)
        s = core.fresh('rei')
        s['active'] = 'garrett'
        self.assertIn(anchors[-1], core.build_messages(s, cue)[0]['content'])
        self.assertNotIn(anchors[-1], social.knowledge_direction(s, ['garrett','ivan'], cue))

    def test_shared_escape_and_third_party_confidences(self):
        s = core.fresh('rei')
        s['active'] = 'yuriko'
        prompt = core.build_messages(s, 'Remember how we got out of the yakuza?')[0]['content']
        self.assertIn('other survivor', prompt)
        self.assertIn('Rei was fifteen when he rescued them both', prompt)
        self.assertIn('gaps in his recollection', prompt)
        s = core.fresh('minsu')
        detail = 'took her with him to the States'
        self.assertNotIn(detail, social.knowledge_direction(s, ['yuriko'], 'Tell me about Rei.'))
        town.character_stats(s, 'yuriko').update(trust=92, closeness=88)
        self.assertIn(detail, social.knowledge_direction(s, ['yuriko'], 'Tell me about Rei.'))
        for player, partner in [('garrett', 'april'), ('rei', 'yuriko')]:
            s = core.fresh(player)
            guide = social.reference_for(s, player, [partner], '')
            self.assertIn('fifteen' if partner == 'yuriko' else 'eighteen', guide['With this listener'])

    def test_speaker_occupation_controls_expertise_at_every_bond_level(self):
        cue = 'imagine i joined the syndicate. would interpol care?'
        for speaker in ('garrett', 'ivan', 'emily', 'Dana Lin'):
            topics = lore.topic_reference(speaker, cue)
            self.assertEqual(set(topics), {'Syndicate', 'Interpol'})
            self.assertIn('international criminal organisation', topics['Syndicate'])
            self.assertEqual('recruitment' in topics['Syndicate'].lower(), speaker in ('garrett','ivan'))
            self.assertEqual('Spades assassinations' in topics['Syndicate'], speaker == 'ivan')
            self.assertEqual('named subject' in topics['Interpol'], speaker == 'Dana Lin')
        s = core.fresh('rei')
        s['active'] = 'emily'
        town.character_stats(s, 'emily').update(trust=100, closeness=100)
        prompt = core.build_messages(s, cue)[0]['content']
        self.assertNotIn('Spades assassinations', prompt)
        s = core.fresh('ivan')
        s['active'] = 'emily'
        town.hidden.mark_met(s, 'emily')  # Ivan no longer starts with every resident.
        self.assertNotIn('Black and White Joker Card', core.build_messages(s, cue)[0]['content'])

    def test_find_charles_evidence_is_scoped_to_garrett_and_the_saved_stage(self):
        s = core.fresh('garrett')
        s['active'] = 'april'
        for stage, stamp, pier in [('unopened', False, False), ('slip', True, False), ('traced', True, True)]:
            s['charles_lead'] = stage
            own = social.reference_for(s, 'garrett', ['april'], 'Charles')
            self.assertEqual('handwriting' in own['Search continuity'], stamp)
            self.assertEqual('West Pier' in own['Search continuity'], pier)
            self.assertNotIn('West Pier', core.build_messages(s, 'Any word about Charles?')[0]['content'])
        s = core.fresh('rei')
        s['charles_lead'] = 'traced'
        s['active'] = 'garrett'
        self.assertNotIn('West Pier', core.build_messages(s, 'Any news about him?')[0]['content'])

    def test_private_and_group_generation_repair_a_syndicate_denial(self):
        s = core.fresh('rei')
        s['active'] = 'garrett'
        joke = 'imagine i joined the syndicate'
        replies = ['Okay.', 'Thanks.', 'Really?', 'Maybe.']
        good = "Their favours come with interest. I'll stick to buying you dinner."
        scene = dict(narration='A message arrives.', dialogue=good, memory='Rei joked about joining.',
                     speaker='Garrett Han', addressee='Rei Takamura', choices_speaker='Rei Takamura',
                     choices=replies, input_tone='Other', emotions={'rei':'playful', 'garrett':'playful'},
                     bond_moments={'garrett':'none'})
        options = dict(choices_speaker='Rei Takamura', choices=replies,
                       personal_choices=['What about you?', 'How much?', 'Just kidding.', 'You worry about me?'])
        sequence = [dict(scene, dialogue='Which syndicate?'), scene, options]
        with patch.object(core, 'request', side_effect=[{'message':{'content':json.dumps(r)}} for r in sequence]) as model:
            self.assertEqual(core.generate(s, joke)['dialogue'], good)
            self.assertEqual(model.call_count, 2)
        gid = groups.create_text(s, 'Dinner', ['garrett','emily'])
        batch = dict(narration='Two messages arrive.', lines=[dict(speaker='Emily Fields', text="i hope you're kidding"),
                     dict(speaker='Garrett Han', text=good)], choices=replies, personal_choices=options['personal_choices'],
                     emotions={'rei':'playful','garrett':'playful','emily':'curious'}, input_tone='Other',
                     bond_moments={'garrett':'none','emily':'none'})
        bad = dict(batch, lines=[batch['lines'][0], dict(speaker='Garrett Han', text='Which syndicate do you mean?')])
        with patch.object(core, 'request', side_effect=[{'message':{'content':json.dumps(r)}} for r in [bad, batch]]) as model:
            self.assertEqual(groups.generate(s, gid, joke)['lines'], batch['lines'])
            self.assertEqual(model.call_count, 2)

    def test_new_turn_uses_delivered_words_and_skips_nickname_echoes(self):
        s = core.fresh('rei')
        s['active'] = 'garrett'
        route = s['routes']['garrett']
        route['history'] = [dict(role='assistant', content=json.dumps(
            dict(dialogue='Their favours come at a price.', choices=['Bro, tell me the secret rank.'])))]
        messages = core.build_messages(s, "You mean the Syndicate?")
        self.assertNotIn('secret rank', str(messages))
        self.assertNotIn('Someone recently used', messages[0]['content'])
        messages = core.build_messages(s, 'thanks bro')
        self.assertEqual(json.loads(messages[-1]['content'])['text'], 'thanks bro')
        self.assertIn('Someone recently used', messages[0]['content'])
        with self.assertRaises(ValueError):
            core.check_nickname(0, ['Always, bro.'])
        with self.assertRaises(ValueError):
            core.check_nickname(1, ['Thanks bro.', 'How come, bro?'])
        core.check_nickname(0, ['My brother used to say that.'])

    def test_observers_distinguish_public_family_firsthand_history_and_inference(self):
        s = core.fresh('rei')
        public = social.relationship_reference(s, 'emily', ['rei'], "Who's Ivan's sister?")
        self.assertIn('adoptive sister', public['Valentina and Ivan']['public'])
        self.assertNotIn('mechanic', str(public))
        for subject, speaker, listener, secret in [('Joseph', 'Joseph Richter', 'rei', 'Joseph helped bully'),
                                                  ('Sylvanis', 'sylvanis', 'ivan', 'signed order')]:
            cue = f'Tell me about {subject} and {listener}.'
            insider = social.relationship_reference(s, speaker, [listener], cue)
            self.assertIn(secret, str(insider))
            outsider = social.relationship_reference(s, 'emily', ['rei'], cue)
            self.assertNotIn(secret, str(outsider))
            self.assertIn('if observed', str(outsider))
        gid = groups.create_text(s, 'School friends', ['emily','sophie'])
        s['groups'][gid]['history'] = [dict(speaker='Rei Takamura (You)', text='Richter used to block the corridor at school.')]
        for who, witnessed in [('emily', True), ('sophie', True), ('garrett', False)]:
            reference = social.relationship_reference(s, who, ['rei'], 'What do you think of Joseph?')
            self.assertEqual('block the corridor' in str(reference), witnessed)
        s['active'] = 'garrett'
        s['routes']['garrett']['history'] = [dict(role='assistant', content=json.dumps(
            dict(dialogue='Is that so?', choices=['Joseph hid a letter.'])))]
        self.assertNotIn('hid a letter', str(social.relationship_reference(s,'garrett',['rei'],'Richter?')))

    def test_richter_encounter_only_supplies_evidence_to_present_companions(self):
        s = core.fresh('rei')
        town.travel(s, 'blackstone_hq')
        town.finish_drive(s)
        town.summon(s, 'garrett')
        s['world']['party'] = ['garrett']
        opening = town.generate_npc(s, town.RICHTER, None)
        town.commit_npc(s, town.RICHTER, None, opening)
        for who, witnessed in [('garrett', True), ('emily', False)]:
            facts = social.relationship_reference(s, who, ['rei'], 'What did you make of Richter?')
            self.assertEqual(opening['lines'][0]['text'] in str(facts), witnessed)
            self.assertIn('already knows Joseph bullied Marcus', str(facts))
            self.assertNotIn('Joseph helped bully', str(facts))

    def test_specific_memories_from_long_biographies_respect_the_listener(self):
        for who, rows in lore.PASSAGES.items():
            for minimum, subjects, heading in rows:
                self.assertTrue(lore.source_paragraphs(heading), (who, heading))
        self.assertIn('Mrs Lau', lore.remembered_passage('garrett', 3, "What about Mrs Lau?"))
        self.assertIsNone(lore.remembered_passage('garrett', 0, "What about Mrs Lau?"))

    def test_generic_story_answer_is_repaired_with_consistent_scene_and_memory(self):
        s = core.fresh('rei')
        s['active'] = 'garrett'
        question = 'Have you heard anything from Charles?'
        choices = ['Want company?', 'I can listen.', 'Come over?', 'Tell me about him.']
        base = dict(narration='A text arrives.', speaker='Garrett Han', addressee='Rei Takamura',
                    choices_speaker='Rei Takamura', choices=choices, input_tone='Other',
                    emotions={'rei':'curious', 'garrett':'sad'}, bond_moments={'garrett':'none'})
        calls = []

        def generate(path, body):
            props = body['format']['properties']
            if 'dialogue' not in props:
                return {'message':{'content':json.dumps(dict(choices_speaker='Rei Takamura', choices=choices,
                    personal_choices=['What do you miss?', 'I can stay.', 'You can talk to me.', 'Should I bring dinner?']))}}
            line = props['dialogue'].get('enum', ['You know how these things are.'])[0]
            calls.append(line)
            return {'message':{'content':json.dumps(dict(base, dialogue=line, memory='Garrett said '+line))}}
        with patch.object(core, 'request', side_effect=generate):
            reply = core.generate(s, question)
        self.assertEqual(len(calls), 2)
        self.assertIn('supplier', reply['dialogue'])
        self.assertEqual(s['routes']['garrett']['history'], [])
        core.commit(s, 'Any word from Charles?', reply)
        import memory_store
        self.assertTrue(any(reply['dialogue'] in r['text'] for r in memory_store.retrieve(s,'garrett','Charles',20)))

    def test_observer_cannot_invent_a_secret_or_a_prior_witnessing(self):
        s = core.fresh('rei')
        cue = 'Ivan and Sylvanis were arguing. What do you think?'
        facts = social.relationship_reference(s,'garrett',['rei'],cue)
        for reply in ("They're always going at it.", "Sylvanis always gets loud.", "I've seen them arguing.", "Sylvanis is blackmailing him."):
            with self.assertRaises(ValueError):
                lore.check_observer(facts,'garrett',cue,reply)
        lore.check_observer(facts,'garrett',cue,"Sounds personal, but I don't know what their business is.")
        lore.check_reply(s,'garrett','Is Charles all right?', "I don't know whether he's dead or alive.")

    def test_hostility_and_loss_of_trust_preserve_the_history_of_those_involved(self):
        for player, speaker, fact in [('ivan','sylvanis','signed order'), ('rei','yuriko','fifteen')]:
            s = core.fresh(player)
            town.character_stats(s,speaker).update(trust=5, closeness=0)
            private = social.reference_for(s,speaker,[player],'Hello')
            self.assertIn(fact, private['History both people already know'])
            public = social.reference_for(s,speaker,[player,'emily'],'Hello')
            self.assertNotIn('History both people already know', public)
