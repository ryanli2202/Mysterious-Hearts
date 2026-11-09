"""What Winterfield residents know firsthand and what the player has actually heard."""
import json
import re
from functools import lru_cache

import hidden_cast
import conversation_lore as lore
import character_memory
import story_calendar
import world_loop


# Each entry is reciprocal. The last field is a memory for the people involved.
TIES = {
    ('garrett', 'ivan'): ('Garrett and Ivan have met through business.', 'They met during a criminal deal. Both recognise each other personally. The transaction is private.'),
    ('rei', 'ivan'): ('Ivan and Rei worked on a K-pop modelling campaign together.', ''),
    ('minsu', 'ivan'): ('Ivan has personally approached Minsu before.', 'Ivan tried to recruit Minsu. Minsu never agreed. The approach was private.'),
    ('ivan', 'valentina'): ('Ivan and Valentina are adoptive siblings.', 'Ivan helped pay for the first boat Valentina restored. They argue over the oak table: sail repairs on one side, two bowls of soup on the other. At karaoke she takes the second verse.'),
    ('rei', 'yuriko'): ('Rei and his younger sister Yuriko share a home.', 'Yuriko trusts Rei with her worst first drafts and saves him a seat backstage. She likes him to ask before fixing a model.'),
    ('rei', 'emily'): ('Rei and Emily have been best friends since high school.', 'Rei got the roof of her model greenhouse back from two bullies. Emily carried the roof to her presentation herself. One pane was painted white to shade the seedlings.'),
    ('garrett', 'april'): ('April and Garrett are childhood best friends from Hong Kong. They moved to Winterfield together when Garrett was eighteen.', 'April beat him at chess in front of the boys who followed him. When he wanted to resign gracefully, she made him tip his own king over.'),
    ('garrett', 'rei'): ('Rei and Garrett are best friends.', 'Rei took the split dumpling on his first visit after a shoot. His drawing of Garrett stealing one back is taped inside the till drawer. After closing Rei has kept Garrett company while he talks about his missing older brother Charles.'),
    ('sophie', 'minsu'): ('Sophie and Minsu are close friends from sports club.', 'He trusts her to time his last interval honestly, even when he starts negotiating with ten seconds left.'),
    ('amy', 'minsu'): ('Amy and Minsu are close friends and live one dorm apart.', 'Amy caught him reviewing a bun he had sat on. On hard study nights he brings two intact buns to her door.'),
    ('rei', 'sophie'): ('Rei and Sophie went to high school together and see one another at parties.', ''),
    ('garrett', 'sophie'): ('Garrett and Sophie know each other from parties.', ''),
    ('garrett', 'emily'): ('Garrett and Emily are already friends.', ''),
    ('rei', 'samantha'): ('Rei and Samantha fight in the same underground ring.', ''),
    ('rei', 'amy'): ('Amy arranged to interview Rei for her humanities assignment.', ''),
    ('garrett', 'amy'): ('Amy arranged to interview Garrett for her humanities assignment.', ''),
    ('garrett', 'minsu'): ('Sophie introduced Garrett and Minsu at a party.', ''),
    ('rei', 'minsu'): ('Sophie introduced Rei and Minsu at a party.', ''),
    ('emily', 'minsu'): ('Minsu met Emily at the café and got her number.', ''),
    ('samantha', 'minsu'): ('Minsu and Samantha ran into one another at the gym.', ''),
    ('april', 'minsu'): ('Minsu and April met at the library.', ''),
    ('sylvanis', 'ivan'): ('Ivan and Sylvanis recognise each other and have a hostile working relationship.', 'Their dealings are private.'),
    ('rei', 'Joseph Richter'): ('Joseph and Rei went to high school together in Winterfield and recognise each other.', ''),
}
for pair, (kind, _, _, memory) in world_loop.BONDS.items():
    left, right = pair.split(':')
    TIES[left, right] = (f'{left.title()} and {right.title()} know each other: {kind.lower()}.', memory)

FAMILIAR_DETAILS = {
    'emily':'She builds LEGO sets, collects plushies and works with flowers at Petal & Stem.',
    'rei':'He sketches on receipts and works as a model. Painting is one of the things he does for himself.',
    'garrett':'He runs the Golden Dragon. He cares enough about his dumplings to remember the one that split.',
    'april':'She loves science and chess. She takes a good game seriously, even with an old friend.',
    'yuriko':'She builds theatre sets in miniature and collects secondhand fabric for the models.',
    'ivan':'Offstage he likes taking a sticking piano key apart. He keeps time against his thumb.',
    'valentina':'She teaches sailing, mends old sails, and takes the second verse on karaoke nights.',
    'minsu':'He is studying medicine, trains in taekwondo and writes food reviews in his campus planner.',
    'amy':'She studies philosophy, paints, and lives one dorm away from Minsu.',
    'sophie':'She runs university track and takes the last interval as seriously as the first.',
}


def personal_ties(who):
    ties = {b if a == who else a: details for (a, b), details in TIES.items() if who in (a, b)}
    # The authored relationship table also defines recognition. Do not copy its
    # private memories here: this list is used when outsiders ask who we know.
    for pair, (public, _, _) in lore.relationship_tables().items():
        a, b = (name if name == 'Joseph Richter' else name.lower() for name in pair)
        if who in (a, b):
            ties.setdefault(b if a == who else a, (public, ''))
    return ties


def friendship(s, who):
    import town
    import custom_protagonist
    if custom_protagonist.is_custom(s['player']) and not hidden_cast.known(s, who):
        return 'Strangers'
    if town.sibling_route(s, who):
        return 'Siblings'
    if who == 'sylvanis' or (who == town.RICHTER and s['player'] == 'rei'):
        return 'Adversaries'
    r = s['relationships'].get(who) or s['friendships'].get(who) or s.get('npc_chats', {}).get(who, {}).get('connection', {})
    trust, close = r.get('trust', 0), r.get('closeness', 0)
    lifelong = {s['player'], who} in ({'rei','emily'}, {'rei','garrett'}, {'garrett','april'})
    if (trust >= 90 and close >= 85) or (lifelong and trust >= 85 and close >= 75):
        return 'Best friends'
    if trust >= 70 and close >= 55: return 'Close friends'
    if trust >= 50 and close >= 25: return 'Friends'
    if trust >= 35 and (close >= 5 or who in personal_ties(s['player']) or
                         (who in hidden_cast.CAST and hidden_cast.known(s, who)) or who in s.get('npc_chats', {})):
        return 'Acquaintances'
    return 'Strangers'


def romance(s, who):
    import town
    if not town.romanceable(s, who): return ''
    status = s['relationships'].get(who, {}).get('status')
    if status in ('official', 'strained', 'dating'): return status.title()
    if (s.get('date_session') or {}).get('partner') == who:
        return 'On a date' if s['date_session']['started'] else 'Date planned'
    if status == 'mutual interest': return 'Mutual interest'
    if s['relationships'].get(who, {}).get('breakups'): return 'Former partners'
    return ''


def status_line(s, who):
    return '  ·  '.join(filter(None, [friendship(s, who), romance(s, who)]))


def initial_notes(s, who):
    tie = personal_ties(s['player']).get(who, ())
    facts = [fact for fact in tie if fact]
    for pair, (_, firsthand, _) in lore.relationship_tables().items():
        if {s['player'].casefold(), who.casefold()} == {name.casefold() for name in pair}:
            facts.append(firsthand)
    return facts


def familiar_detail(s, who):
    tie = personal_ties(s['player']).get(who)
    if who == s['player'] or (tie and tie[1] and 'private' not in tie[1].lower()):
        return FAMILIAR_DETAILS.get(who)


def earlier_exchanges(s, who):
    """For older saves, surface the partner's delivered words from personal exchanges."""
    lines = []
    for turn in reversed(s['routes'].get(who, {}).get('history', [])):
        if turn['role'] != 'assistant': continue
        try: scene = json.loads(turn['content'])
        except (TypeError, ValueError): continue
        if not isinstance(scene, dict) or 'profile_notes' in scene: continue
        if (scene.get('bond_moments') or {}).get(who) in ('personal_detail','chemistry') and isinstance(scene.get('dialogue'), str):
            lines.append(scene['dialogue'])
            if len(lines) == 3: break
    return lines


def speaker_ties(s, who):
    ties = personal_ties(who)
    if who == 'ivan':
        for other in story_calendar.BIRTHDAYS:
            if other != who:
                ties.setdefault(other, ('They have already been introduced through Ivan’s circle.', ''))
    elif who in story_calendar.BIRTHDAYS:
        ties.setdefault('ivan', ('They have already been introduced through Ivan’s circle.', ''))
    for group in s.get('groups', {}).values():
        if who in group['members'] and any(line.get('speaker','').endswith(' (You)') for line in group['history']):
            for other in [s['player'], *group['members']]:
                if other != who:
                    ties.setdefault(other, ('They have taken part in the same group conversation.', ''))
    return ties


def recognition_question(s, speaker, line):
    if not re.search(r'\b(?:do you know|have you (?:ever )?met|have you heard of|know who)\s+', line, re.I):
        return None
    ties = speaker_ties(s, speaker)
    matches = [who for who in ties if re.search(r'\b'+re.escape(who)+r'\b', line, re.I)]
    if len(matches) == 1:
        who = matches[0]
        return {'person':who, 'firsthand':ties[who][0]}


def check_recognition(fact, reply):
    if not fact: return
    name = re.escape(fact['person'])
    denial = (rf"\b(?:(?:never|haven't|have not) (?:met|heard of)|(?:don't|do not|don't really) know) (?:him|her|them|{name})\b"
              r"(?! (?:well|very well|that well|anymore|like that))|\b(?:never crossed paths|doesn't ring a bell|only know (?:him|her) by (?:name|reputation))\b")
    if re.search(denial, reply.replace('’', "'"), re.I) or reply.strip(" .!?").casefold() in ('no', 'nope', 'nah', 'not personally'):
        raise ValueError('This speaker has met the named person. Acknowledge the established connection in their reply.')


def audience_openness(s, who, listeners):
    player = s['player']
    levels = []
    for other in listeners:
        if player in (who, other):
            contact = other if who == player else who
            stats = (s['relationships'].get(contact) or s['friendships'].get(contact)
                     or s.get('npc_chats', {}).get(contact, {}).get('connection') or {})
        else:
            stats = s['bond_details'].get(f'{who}:{other}') or s['bond_details'].get(f'{other}:{who}') or {}
            if not stats and frozenset((who, other)) in PRIVATE_FRIENDS:
                stats = {'trust': 90, 'closeness': 85}
        levels.append(lore.openness(stats))
    return min(levels)


PRIVATE_FRIENDS = {frozenset(pair) for pair in (
    ('garrett', 'rei'), ('garrett', 'april'), ('rei', 'emily'), ('rei', 'yuriko'),
    ('ivan', 'valentina'), ('minsu', 'amy'), ('minsu', 'sophie'))}


CONTINUITY_DIRECTION = (
    'ESTABLISHED FAMILIARITY: Use this speaker\'s known favourites and shared history as existing knowledge, '
    'including before the first saved conversation. Do not ask someone to introduce a favourite, hobby or '
    'shared event that this speaker already knows, and do not act surprised to learn it again. '
    'Build on it: suggest their usual food, recall the specific title, ask whether they want it today, '
    'what they thought of a rewatch, or whether their tastes have changed. A confirmation about today\'s '
    'choice is different from asking what their favourite is. Use a relevant detail naturally; do not '
    'recite a profile or force a callback into every reply. Later explicitly shared changes override older '
    'preferences. Reduced trust changes willingness to talk, not memory. Unknown information still needs '
    'to be learned. Knowledge belongs to the named speaker, not automatically to everyone listening; '
    'do not expose private disclosures to a group. Apply the same rules to unsent player suggestions. '
    'Never rewrite the player\'s actual words if they choose to ask a familiar question.'
)


def conversation_knowledge(s, speaker, listeners):
    """Observer-owned tastes and audience-safe history, shared by every chat path."""
    import contact_profiles
    result = {}
    table = lore.character_tables().get(speaker, {})
    audience = list(dict.fromkeys(p for p in listeners if p != speaker))
    for other in audience:
        facts = contact_profiles.known_favourites(s, other, speaker)
        history = []
        if len(audience) == 1:
            tie = personal_ties(speaker).get(other, ())
            history.extend(fact for fact in tie if fact)
            if detail := table.get('With '+other.title()): history.append(detail)
            for pair, (_, firsthand, _) in lore.relationship_tables().items():
                if {speaker.casefold(), other.casefold()} == {name.casefold() for name in pair}:
                    history.append(firsthand)
        elif detail := table.get('In company with '+other.title()):
            history.append(detail)
        result[other] = dict(known_favourites=facts, shared_history=list(dict.fromkeys(history)),
                            learned_details=contact_profiles.learned_details(s, other, speaker),
                            personal_disclosures=[dict(text=r['text'], certainty=r.get('certainty'), source=r['source'])
                                                  for r in contact_profiles.disclosures(s, other, speaker)
                                                  if r['kind'] in ('fact', 'belief')][-12:])
    return result


PUBLIC_FAME = {
    'rei': 'Rei Takamura, a famous model known from public modelling work and campaigns.',
    'elias': 'Elias Braun, a famous actor known from his public acting career.',
    'ivan': 'Ivan Yeun, a famous K-pop idol known from music and public performances.',
}


def public_recognition(s, speaker, listeners, *, texting=None):
    """Public reputation is available to strangers, without granting private knowledge."""
    import game_core as core
    import four_aces
    if texting is None:
        texting = core.is_texting(s)
    ties = speaker_ties(s, speaker)
    people = {}
    for other in dict.fromkeys(listeners):
        if other == speaker or other not in PUBLIC_FAME:
            continue
        actor = s.get('world', {}).get('cast', {}).get(other, {})
        concealed = (not texting and four_aces.uniform_at(other, actor.get('location'))
                     and actor.get('location') == s.get('world', {}).get('location'))
        people[other] = {
            'public_reputation': PUBLIC_FAME[other],
            'established_personal_connection': other in ties,
            'face_concealed': concealed,
        }
    return {'people': people, 'direction': (
        'PUBLIC FAME: Being strangers does not mean being unaware of a public figure. '
        'On a first introduction to an identifiable famous person here, give the NPC a brief, '
        'natural recognition beat without waiting for the player to ask about fame. '
        'Vary it with the speaker’s personality: a double take, tentative name confirmation, '
        'warm enthusiasm, understated professional recognition, or a composed acknowledgement. '
        'Do not use a stock catchphrase or make everyone a fan. Refer only to the supplied public '
        'career; do not invent film titles, songs, campaigns, awards or past meetings. '
        'Established acquaintances and people who already recognised them in the supplied history '
        'must not repeat first-meeting surprise. Continue the actual conversation after the brief beat. '
        'Public recognition grants no trust, intimacy, phone number, private memories, criminal '
        'identity or knowledge of powers. A concealed face must not be identified through fame; '
        'do not connect a masked operational identity to a celebrity without established knowledge. '
        'Do not write the player’s reaction or actions for them; this guidance may inform unsent suggestions. '
        + ('This is text: recognition may follow an established name or introduction, never a live '
           'view, anonymous handle alone, or an invented photo. No physical double take or encounter.'
           if texting else 'This is in person: ground recognition in the visible, unconcealed person or their introduction.')
    )}


def reference_for(s, who, listeners, cue, *, texting=None):
    level = audience_openness(s, who, listeners)
    reference = lore.speaker_reference(who, listeners, level, cue, s)
    import crime_sites
    if sites := crime_sites.context(s, who, cue):
        reference['City site knowledge (private vantage point)'] = sites
    import crime_operations
    reference['Recorded faction work'] = crime_operations.context(s,who)
    import bubblegram_progression
    reference['Criminal discovery continuity'] = bubblegram_progression.context(s,who)
    import crime_diplomacy
    reference['Private leadership journal'] = crime_diplomacy.context(s,who)
    reference['Current leadership meeting'] = {} if texting else crime_diplomacy.scene_context(s, who)
    import criminal_reputation
    if fear := criminal_reputation.context(s, who):
        reference['Underworld reputation'] = fear
    reference['Established familiarity with listeners'] = conversation_knowledge(s, who, listeners)
    reference['Use established familiarity'] = CONTINUITY_DIRECTION
    reference['Public recognition of listeners'] = public_recognition(s, who, listeners, texting=texting)
    if who in story_calendar.BIRTHDAYS or who in hidden_cast.CAST:
        reference['Profile'] = demographics(who)
    if search := lore.charles_context(s, who, level):
        reference['Search continuity'] = search
    bonds = relationship_reference(s, who, listeners, cue)
    if bonds:
        reference['Relationships raised'] = bonds
    reference['Appearance for this conversation'] = appearance_reference(s, who, listeners, cue, texting=texting)
    return reference


def appearance_reference(s, who, listeners, cue, *, texting=None):
    """Supply visible/recognisable features, not every resident's private profile."""
    import game_core as core
    if texting is None:
        texting = core.is_texting(s)
    guides = lore.character_tables()
    familiar = set(speaker_ties(s, who)) | {who, *listeners}
    # Public models/idols can be recognised without having met personally.
    public_faces = set(PUBLIC_FAME)
    subjects = {who, *listeners}
    unknown = []
    for person in guides:
        if lore.names_person(cue, person) or lore.names_person(cue, person.split()[0]):
            if person in familiar or person in public_faces:
                subjects.add(person)
            else:
                unknown.append(person)
    import character_appearance
    people = {}
    for person in sorted(subjects):
        guide = guides.get(person, {})
        if not guide.get('Appearance'):
            continue
        people[person] = character_appearance.reference(person) or {
            'Recognisable features': guide['Appearance'],
            'Usual portrait styling, not today’s outfit': guide['Portrait style'],
        }
        import four_aces
        actor = s.get('world', {}).get('cast', {}).get(person, {})
        if not texting and four_aces.uniform_at(person, actor.get('location')) and actor.get('location') == s['world']['location']:
            people[person] = {'Current visible uniform': four_aces.uniform_description(person),
                              'Concealment': 'The mask and hood conceal the civilian face. Do not describe visible eyes, hair, tattoos or facial expressions behind it.'}
        if person == s['player'] and not texting and 'Current visible uniform' not in people[person]:
            outfit = s.get('world', {}).get('player_outfit')
            if outfit and outfit != 'Automatic':
                people[person]['Selected outfit in this in-person scene'] = outfit
    return {
        'People': people,
        'Not known by sight from this reference': unknown,
        'Guidance': (
            'All portrayed adult characters are conventionally attractive, with distinct features. '
            'Answer appearance questions naturally with one or two specific details, not a clinical inventory. '
            'A speaker may find someone cute or handsome without romantic interest; respect individual tastes, '
            'existing relationships, familial boundaries and dislike based on conduct. Do not infer consent or '
            'mutual attraction, force jealousy, or turn a compliment into an automatic confession. '
            'Use the named subject’s features, not the listener’s. Usual clothing, smiles, props and poses are '
            'reference styling, not observations of today. Current established scene details and selected outfits '
            'override that styling. Never invent a new haircut, outfit, expression or a visible tattoo hidden by clothes. '
            + ('This is a text conversation: there is no live view of the recipient or their outfit. '
               'A familiar face can receive an affectionate general compliment; for “today”, ask what they are '
               'wearing or respond to what they actually described. Do not pretend a photo was sent.'
               if texting else
               'This is an in-person conversation: the people present can comment on each other’s established '
               'features and the selected outfit. Without a current outfit description, use features rather than '
               'claiming the reference outfit is being worn today.')
        ),
    }


def relationship_reference(s, who, listeners, cue):
    facts = {}
    for (subject, partner), (public, firsthand, inference) in lore.relationship_tables().items():
        # Looking up the side character should work by surname too. Mentioning
        # Ivan alone must not introduce an undiscovered contact such as Sylvanis.
        side = subject if subject == 'Joseph Richter' else subject.lower()
        other = partner.lower()
        family_question = side == 'valentina' and re.search(r"\bIvan(?:'s|’s) (?:younger |adoptive )*sister\b", cue, re.I)
        if not (family_question or lore.names_person(cue, subject) or who == side and lore.names_person(cue, partner)):
            continue
        row = {'public': public}
        if subject == 'Joseph Richter' and lore.shared_school_history(who, listeners):
            row['already knows Joseph bullied Marcus'] = (
                'Joseph and classmates repeatedly bullied Marcus, Rei’s close school friend, '
                'who later died by suicide. Rei, Emily and Sophie already know this from their school years. '
                'No specific eyewitness incident, method of death or single cause is established.')
        elif subject == 'Joseph Richter' and who == 'garrett' and listeners == ['rei']:
            row['already knows Joseph bullied Marcus'] = lore.character_tables()['garrett']['Marcus told by Rei']
        if (who == side and listeners == [other]) or (who == other and listeners == [side]):
            row['shared firsthand'] = firsthand
        else:
            row['if observed'] = inference
        heard = character_memory.heard_about(s, who, subject, partner)
        if heard:
            row['words this person actually heard'] = heard
        facts[f'{subject} and {partner}'] = row
    return facts


def knowledge_direction(s, members, cue='', *, texting=None):
    import sexuality
    player = s['player']
    records = {}
    for who in members:
        ties = speaker_ties(s, who)
        depth = friendship(s, who)
        listeners = [player, *(m for m in members if m != who)]
        level = audience_openness(s, who, listeners)
        own = {}
        for other, (connection, memory) in ties.items():
            private_pair = len(listeners) == 1 and other == player
            if {who, other} == {'rei', 'samantha'} and not private_pair:
                connection = 'They recognise one another personally. How they met is private.'
            own[other] = connection
            # Personal history with the player is theirs already. For a third party,
            # earn a firsthand anecdote through the speaker's trust, never the subject's.
            if memory and (private_pair or level >= 2 and 'private' not in memory.lower()):
                own[other] += ' ' + memory
        previous = [n for notes in s.get('profile_notes', {}).values() for n in notes
                    if n['source'] == who and (n['subject'] in cue.casefold() or n['subject'] == who)]
        records[who] = dict(bond_with_player=depth, personally_knows=own,
                            reference=reference_for(s, who, listeners, cue, texting=texting))
        import mysterious_hearts, contact_profiles
        records[who]['private_app_knowledge'] = mysterious_hearts.context(s, who)
        import protectiveness
        records[who]['protectiveness'] = protectiveness.context(s, who, listeners)
        import relationship_dynamics
        records[who]['relationship_dynamics'] = relationship_dynamics.context(s, who, listeners)
        records[who]['visible_contact_profiles'] = contact_profiles.context(s, who)
        records[who]['profile_direction'] = 'Notice visible favourites and bio changes naturally. Private notebooks are unavailable. Anonymous-thread knowledge belongs only to this speaker; protect it from other listeners.'
        if len(listeners) == 1:
            records[who]['previously_told_player'] = previous[-4:]
    return ('\nSPEAKER KNOWLEDGE. Public fame and meeting someone personally are different; use each speaker’s public recognition reference. '
            'These firsthand connections apply in both directions. Acknowledge an established meeting even if asked by a stranger; '
            'a private meeting can be acknowledged without disclosing its business. Answer questions about other residents from the speaker’s '
            'own experience. Use the current disclosure level for personal anecdotes. A sibling with damaged trust still recognises shared history. '
            'Protect other people’s confidences. With shared history, start from what both already know and explore what it meant. '
            'Authored shared memories predate this save: an empty chat log or low trust never makes old friends strangers. '
            'Recognise their inside jokes without asking the player to explain them. You may initiate a relevant callback '
            'or ordinary recollection without a lore question; do not force one into every reply or retell its origin to a participant. '
            'Use at most one brief callback when it fits the immediate exchange, and avoid repeating a joke from recent turns. '
            'In groups use the everyday shared memories supplied for people present; private pair histories are not group knowledge. '
            'Each speaker uses only their own record. Public recognition and professional competence apply at every bond level. '
            'Use private professional knowledge to shape a reaction without announcing a secret identity. '
            'Answer jokes as jokes. Followups continue the same subject. Previously delivered words and shared experiences '
            'are already known to those present then. When asked how people know one another, distinguish a public tie, '
            'a line the speaker witnessed, a report someone gave them, and an inference. A hypothetical or a question proves nothing. '
            'An observer can name the behaviour that suggests tension or familiarity and leave the cause open. '
            'Other biography, suggestions and game mechanics are never evidence. '
            'The available reference layers set the depth ceiling. Within those layers, let the exact current trust and closeness '
            'gradually change ease, warmth, detail and willingness to volunteer more. A small gain earns a small change. '
            'Apply the disclosure guidance for everyone listening. ' + sexuality.direction(s['player'], members)
            + ' ' + json.dumps(records, ensure_ascii=False))


def add_note_schema(schema, s, members):
    import relationship_dynamics
    dynamics_guide = relationship_dynamics.add_schema(schema, s, members)
    subjects = sorted(set(s['routes']) | set(members) | set(s.get('npc_chats', {})))
    schema['properties']['profile_notes'] = {'type':'array', 'maxItems':3, 'items':{
        'type':'object', 'properties':{'source':{'type':'string','enum':list(members)},
        'subject':{'type':'string','enum':subjects}, 'quote':{'type':'string'}},
        'required':['source','subject','quote'], 'additionalProperties':False}}
    schema['required'].append('profile_notes')
    return (' Return profile_notes for new, lasting personal facts actually disclosed to the player this turn. '
            'Use the speaker key, the subject key (they can differ), and a short exact quote from that speaker’s delivered line. '
            'Use [] for small talk, questions, guesses, secrets left unsaid, and unsent suggestions.' + dynamics_guide)


def record_notes(s, data, spoken, owners=None):
    notes = data.get('profile_notes', [])
    owners = sorted(set(owners or [s['player'], *spoken]))
    if not isinstance(notes, list): return
    for note in notes[:3]:
        if not isinstance(note, dict): continue
        source, subject, quote = (note.get(k) for k in ('source','subject','quote'))
        if not all(isinstance(v, str) for v in (source, subject, quote)): continue
        quote = quote.strip()
        if (source not in spoken or subject not in s['routes'] and subject not in spoken and subject not in s.get('npc_chats', {})
                or not 3 <= len(quote) <= 350 or quote not in spoken[source]): continue
        entries = s.setdefault('profile_notes', {}).setdefault(subject, [])
        if not any(n['source'] == source and n['quote'].casefold() == quote.casefold()
                   and set(owners).issubset(n.get('owners', [s['player'], source])) for n in entries):
            entries.append(dict(source=source, subject=subject, quote=quote, minute=s['world']['minute'], owners=owners))


@lru_cache(maxsize=None)
def demographics(who):
    import custom_protagonist
    if who in custom_protagonist._profiles:
        p = custom_protagonist._profiles[who]
        return {'Sexuality': p['sexuality'], 'Birthday': 'Not specified', 'MBTI': p['mbti'],
                'Age': str(p['age']), 'Height': str(p['height']) + ' cm'}
    import sexuality
    import game_core as core
    info = hidden_cast.CAST.get(who, {})
    if info:
        age, height, mbti = (info.get(k) for k in ('age', 'height', 'mbti'))
    elif who in ('ivan', 'yuriko'):
        age, height, mbti = (24, 193, 'ISTP') if who == 'ivan' else (18, 159, 'ENFP')
    else:
        canon = core.canon_section(core.CONTACTS[who][0]) if who in core.CONTACTS else ''
        fields = dict(re.findall(r'^\| (Age|Height|MBTI) \| (.*?) \|', canon, re.M))
        age, height, mbti = (fields.get(k) for k in ('Age','Height','MBTI'))
    return {'Sexuality':sexuality.CANON.get(who, ('', 'Not established'))[1],
            'Birthday':story_calendar.BIRTHDAYS.get(who, 'Unknown'), 'MBTI':mbti or 'Unknown',
            'Age':str(age or 'Unknown'), 'Height':f'{height} cm' if isinstance(height, int) else height or 'Unknown'}
