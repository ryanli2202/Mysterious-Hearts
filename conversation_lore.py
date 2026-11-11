"""Select authored Winterfield references for the speaker and the people listening."""
from functools import lru_cache
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parent
GUIDE = ROOT / 'Mysterious Hearts - Character References.md'
WORLD = ROOT / 'Mysterious Hearts - Worldbuilding.md'
BIOGRAPHIES = ROOT / 'Mysterious Hearts - RPG Game.md'
LAYERS = ('Public life', 'Familiar', 'Personal', 'Confidence')
DELIVERY = (
    'Answer the subject directly. Keep the personal part brief and set a boundary if pressed.',
    'Give one ordinary fact in your own words. Let the listener follow up.',
    'Offer a firsthand detail and what it meant to you, if it answers the question.',
    'Speak freely about your own experience with this listener. Meet a personal question with a real memory or feeling.',
)


def table_rows(section):
    for line in section.splitlines():
        if line.startswith('|'):
            yield [field.strip() for field in line.strip('|').split('|')]


@lru_cache(maxsize=1)
def guide_sections():
    return dict(section.split('\n', 1) for section in GUIDE.read_text(encoding='utf-8').split('\n## ')[1:])


@lru_cache(maxsize=1)
def character_tables():
    guides = {}
    for name, body in guide_sections().items():
        if name in ('Relationship evidence', 'Canonical sexual orientations'):
            continue
        header, _, *rows = table_rows(body)
        if name == 'Everyday town residents · playable roster expansion':
            import town_residents
            for who, role, personality, connections in rows:
                guides[who] = {
                    'Public life': role,
                    'Familiar': personality,
                    'Personal': connections,
                    'Confidence': 'Let trust grow through actual exchanges. No additional private history is established.',
                    'World knowledge': 'Everyday public life and their own work; no private cases, criminal secrets or other residents’ undisclosed history.',
                    'With visitors': 'An adult local acquaintance. Remember actual conversations without inventing past meetings or romantic commitments.',
                    'Everyday favourites': town_residents.favourites(who),
                    'Appearance': town_residents.portrait_reference(who),
                    'Portrait style': 'Cel-shaded manhwa portrait; clothing and features follow the assigned transparent selection portrait. A portrait is not a live view during texting.',
                }
            continue
        if name == 'Winterfield locals':
            for who, *fields in rows:
                guides[who] = dict(zip(header[1:], fields, strict=True))
        else:
            key = name if name == 'Joseph Richter' else name.split()[0].lower()
            guides[key] = dict(rows)
    import outskirts
    import town_residents
    import street_recruits
    for who, person in {**outskirts.RESIDENTS, **street_recruits.RESIDENTS}.items():
        guides[who] = {
            'Public life': f"Age {person['age']}. {person['role']}. {person['life']}",
            'Familiar': person['voice'],
            'Personal': person['life'],
            'Confidence': 'No additional private history is established.',
            'World knowledge': 'Their own work and public town life; no private cases or undisclosed history.',
            'With visitors': 'An adult local acquaintance. Use actual conversation history; never invent meetings.',
            'Everyday favourites': town_residents.favourites(who),
            'Appearance': person['appearance'],
            'Portrait style': 'Cel-shaded manhwa portrait; clothing and features follow the assigned transparent selection portrait. A portrait is not a live view during texting or evidence of today’s outfit.',
        }
    import the_crow
    for who in street_recruits.NAMES:
        guides[who]['Portrait style'] = 'Cel-shaded manhwa portrait and matching contact photo. Use the authored appearance; neither image is a live view during texting or evidence of a current location.'
    guides['crow'] = {layer: the_crow.BOUNDARY for layer in LAYERS}
    guides['crow'].update({'Appearance': the_crow.APPEARANCE, 'Portrait style': 'Half-body cel-shaded portrait in concealed plague-doctor robes; a portrait is not a live view during texting.', 'World knowledge': the_crow.CANON, 'With visitors': the_crow.BOUNDARY, 'Everyday favourites': 'Unknown'})
    import thirteen
    guides['thirteen']={layer:thirteen.BOUNDARY for layer in LAYERS}
    guides['thirteen'].update({'Public life':thirteen.PROFILE,'World knowledge':thirteen.HISTORY,'Appearance':thirteen.APPEARANCE,'With visitors':thirteen.BOUNDARY,'Portrait style':'Cel-shaded manhwa transparent suit portrait; not a live view during texting.','Everyday favourites':'Unknown'})
    import keisuke
    import gang_leaders
    guides[keisuke.NAME] = keisuke.reference_table()
    guides.update(gang_leaders.reference_tables())
    import gang_members
    for name, person in gang_members.MEMBERS.items():
        guides[name] = {layer: gang_members.BOUNDARY for layer in LAYERS}
        guides[name].update({'Public life': person['role'], 'Familiar': person['personality'],
                            'Appearance': person['appearance'], 'World knowledge': person['work'] + ' ' + gang_members.BOUNDARY})
    import interpol_cast
    guides.update({who: interpol_cast.reference(who) for who in interpol_cast.IDS})
    import character_types
    for who, guide in guides.items():
        guide['Character type'] = character_types.kind(who)
    import custom_protagonist
    return custom_protagonist.Registry(guides, custom_protagonist.lore_record)


@lru_cache(maxsize=1)
def relationship_tables():
    _, _, *rows = table_rows(guide_sections()['Relationship evidence'])
    return {tuple(pair.split(' / ')): (public, firsthand, inference) for pair, public, firsthand, inference in rows}


def everyday_favourites(who):
    """Structured tastes from the dedicated row, never private biography layers."""
    text = character_tables().get(who, {}).get('Everyday favourites', '')
    labels = r'Breakfast|Lunch|Dinner|Snack|Drink|TV show|Movie|Book|Author'
    matches = list(re.finditer(r'(?:^|;\s*)(' + labels + r'):\s*', text))
    result = {}
    for i, match in enumerate(matches):
        value = text[match.end():matches[i+1].start() if i+1 < len(matches) else len(text)].strip(' ;')
        if match[1] == 'Author':
            # Preserve initials (e.g. Ursula K. Le Guin), omit the reading-habit sentence.
            value = re.split(r'(?<!\b[A-Z])\.\s+(?=[A-Z][a-z]{2,}\b)', value, maxsplit=1)[0].rstrip('.')
        if value: result[match[1]] = value
    return result


def names_person(text, name):
    if name == 'Joseph Richter':
        return re.search(r"\b(?:Joseph|Richter|Blackstone(?:’s|'s)? CEO)\b", text, re.I)
    return re.search(r'\b' + re.escape(name) + r'\b', text, re.I)


@lru_cache(maxsize=1)
def topic_tables():
    section = WORLD.read_text(encoding='utf-8').split('\n## Conversation topics\n', 1)[1]
    _, _, *rows = table_rows(section)
    result = []
    for aliases, common, practitioners, working, insiders, inside in rows:
        names = aliases.split(', ')
        pattern = re.compile(r'\b(?:' + '|'.join(map(re.escape, names)) + r')\b', re.I)
        result.append((pattern, names[0], common, practitioners.lower().split(', '),
                       working, insiders.lower().split(', '), inside))
    return result


def topic_reference(who, cue):
    facts = {}
    for pattern, name, common, practitioners, working, insiders, inside in topic_tables():
        if pattern.search(cue):
            detail = [common]
            if who.lower() in practitioners or who.lower() in insiders:
                detail.append(working)
            if who.lower() in insiders:
                detail.append(inside)
            facts[name] = ' '.join(detail)
    return facts


def openness(stats):
    # Closeness makes personal subjects familiar; trust limits what feels safe.
    score = min(stats.get('trust', 0), stats.get('closeness', 0) + 18)
    return sum(score >= threshold for threshold in (40, 58, 78))


# Longer anecdotes stay in the original biography. Only fetch a passage the
# speaker remembers and can share here, even if the listener names it outright.
PASSAGES = {
    'garrett': (
        (2, 'Flaming Prince|Kit|Mrs Lau|pears|worst beating', "Seventeen, behind Mrs Lau's shop"),
        (3, 'teacup|electricity bill|mother.s noodles|chipped cup', 'Growing up with Charles'),
        (3, 'shrimp shells|last call|Sunday calls', 'The last call from Hong Kong')),
    'rei': (
        (1, 'backdrops?|first cheque|first shoot|paint on your hands', 'A face on the studio wall'),
        (2, 'bus driver|bus route|bus timetable|greenhouse', 'Starting over at fifteen')),
    'minsu': (
        (1, 'gold medal|national final|chemistry practical|why medicine', 'His own gold and the choice to study medicine'),
        (2, 'summers?|melon|kitchen radio', 'Summers with Jiwon'),
        (3, 'co-op|wheelchair|rice cooker|Jiwon.s accident', 'The first game after the accident')),
}


@lru_cache(maxsize=None)
def source_paragraphs(heading):
    text = BIOGRAPHIES.read_text(encoding='utf-8').split(f'\n#### {heading}\n', 1)[1]
    section = re.split(r'\n#{1,4} ', text, maxsplit=1)[0]
    return section.strip().split('\n\n')


def remembered_passage(who, level, cue):
    for minimum, subjects, heading in PASSAGES.get(who, ()):
        match = re.search(r'\b(?:' + subjects + r')\b', cue, re.I)
        if level >= minimum and match:
            paragraphs = source_paragraphs(heading)
            return next((p for p in paragraphs if match[0].lower() in p.lower()), paragraphs[0])


def speaker_reference(who, listeners, level, cue, state=None):
    import vendetta_lore
    import the_crow
    guide = character_tables()[who]
    reference = {field: guide[field] for field in LAYERS[:level + 1]}
    if address := the_crow.address_direction(who):
        reference['Private Crow address and deference canon'] = address
    reference['Vendetta AU'] = vendetta_lore.speaker_context(who, listeners, state)
    import criminal_dynamics
    reference['Criminal dynamics'] = criminal_dynamics.context(who, listeners, state)
    import interpol
    reference['Interpol case knowledge'] = interpol.context(state, who, listeners)
    import charles_quest
    if search := charles_quest.knowledge(state,who,listeners):
        reference['Authoritative Charles search progression'] = search
    if narrative := __import__('campaign_prose').knowledge(state,who,listeners):
        reference['Shared campaign conversations'] = narrative
    import four_aces
    if who in four_aces.CAST:
        reference['Individual personality and voice'] = four_aces.CHARACTER_DIRECTION[who]
    if favourites := guide.get('Everyday favourites'):
        reference['Everyday favourites'] = favourites
        reference['Using preferences'] = (
            'These are your own established tastes, available for ordinary conversation at any trust level. '
            'Mention only what fits; do not list them or turn every invitation into a favourite. '
            'Another person does not automatically know your order or favourite title unless shared history '
            'or an actual conversation establishes it. Preferences are not dietary restrictions or consent.')
    reference['How much to share'] = DELIVERY[level]
    if who == 'garrett':
        reference['Receiving news about Charles'] = CHARLES_NEWS
    if boundary := guide.get('Disclosure boundary'):
        reference['How much to share'] = boundary
    if guide.get('Everyday favourites') == 'Unknown':
        reference['Using preferences'] = 'Do not supply favourites or invent tastes; none are established. Authored hobbies are not favourite meals, books or films.'
    if who == 'charles':
        import charles_han
        reference['How much to share'] = charles_han.BOUNDARY
    if who == 'thirteen':
        import thirteen
        reference['How much to share']=thirteen.BOUNDARY
        reference['Using preferences']='Do not supply favourites; his tastes are unestablished.'
    if who == 'takeo':
        import takeo
        reference['How much to share'] = takeo.BOUNDARY
        reference['Using preferences'] = 'Only strength and domination as likes, weakness and mercy as dislikes are established. Do not invent favourite meals, media or books.'
    if who == 'crow':
        import the_crow
        reference['How much to share'] = the_crow.BOUNDARY
        reference['Using preferences'] = 'His personal tastes are unknown. Do not supply favourites or invent a personal disclosure.'
    reference['Knowledge from experience (private vantage point)'] = guide['World knowledge']
    # These explicitly authored rows are safe to recall in company. Never use
    # the full private pair history as a substitute in a group conversation.
    everyday = {other: guide['In company with ' + other.title()]
                for other in listeners if 'In company with ' + other.title() in guide}
    if everyday:
        reference['Everyday shared memories with people present'] = everyday
    if memory := shared_school_history(who, listeners):
        reference['School history already known to this audience'] = memory
        if memories := guide.get('Memories of Marcus'):
            reference['Marcus as a person — shared school memories'] = memories
    if guide.get('Reaction to Joseph') and (
            names_person(cue, 'Joseph Richter') or 'Joseph Richter' in listeners):
        reference['Reaction to Joseph'] = guide['Reaction to Joseph']
    if passage := remembered_passage(who, level, cue):
        reference['Remembered detail'] = passage
    if len(listeners) == 1:
        other = listeners[0]
        response = guide.get('With ' + other.title(), guide.get('With visitors'))
        if response:
            reference['With this listener'] = response
        for pair, (_, firsthand, _) in relationship_tables().items():
            if {who.casefold(), other.casefold()} == {name.casefold() for name in pair}:
                reference['History both people already know'] = firsthand
    if topics := topic_reference(who, cue):
        reference['Subject raised'] = topics
    return reference


def shared_school_history(who, listeners):
    """A shared loss can be recalled among school friends without a trust gate."""
    school_friends = {'rei', 'emily', 'sophie'}
    if who in school_friends and listeners and set(listeners) <= school_friends:
        return character_tables()[who].get('Shared school bereavement', '')
    return ''


def charles_context(state, who, level):
    if who != 'garrett':
        return ''
    import charles_quest
    report=__import__('charles_disclosure').knowledge(state,who,[state['player']])
    if report: return report
    if state.get('player') == 'garrett' and 'charles_quest' in state:
        return charles_quest.knowledge(state,who)
    # The search controls belong to Garrett's playable route. As an NPC he
    # knows the opening disappearance, never evidence from another playthrough.
    stage = state.get('charles_lead', 'unopened') if state['player'] == who else 'unopened'
    evidence = {
        'unopened': 'The search has produced no new lead.',
        'slip': 'Mei sent a delivery slip dated eleven days after Charles left his job. The correction resembles his handwriting. The stamp is unreadable.',
        'traced': 'The receiving copy identifies West Pier Cold Storage in Hong Kong, eleven days after Charles left his job. The correction resembles his handwriting. Nobody signed as driver.',
    }
    return ('Charles Han is your missing older brother. You are still looking. His whereabouts, motive and allegiance are unknown. '
            'Only authored search actions establish evidence. ' + evidence[stage] + ' '
            + ('Keep private history private, but listen seriously to news about Charles regardless of trust.'
               if level == 0 else 'Answer at the level of personal detail available for this listener.'))


CHARLES_NEWS = (
    'When the conversation brings news of your missing brother Charles, including follow-ups such as '
    '"I found him" or "he is working for the Syndicate", treat it as personally momentous at every trust level. '
    'A guarded relationship limits what you reveal, not how much you care about finding him. '
    'At "it is about your brother", become attentive and concerned; do not dismiss it as family history. '
    'At a claimed sighting, let shock, urgent hope and fear for his safety interrupt your usual easy charm. '
    'Ask a focused practical question about where or when they saw him, whether he is safe, or how to reach him; '
    'use what they already told you instead of asking them to repeat it. News that he works for the Syndicate '
    'adds alarm and confusion given your opposition to them, not casual acceptance or a faction joke. '
    'Respond naturally in your own voice, without forced shouting or melodrama. '
    'Follow the actual conversation, including pronoun-only follow-ups, without inventing a report when none was made. '
    'Acknowledge what the speaker reports without treating it as verified allegiance, motive or a completed reunion. '
    'Only authored in-person actions advance the investigation; texts do not grant access, arrange a completed visit '
    'or reveal the undercover explanation. After an established reunion, preserve that continuity rather than '
    'reacting as if this were the first news that he is alive.'
)


CHARLES = re.compile(r"\b(?:charles|your (?:missing |older |big )?brother)\b", re.I)
ESCAPE = re.compile(r"\b(?:yakuza|clan|hamayashi(?:-kai)?|escap\w*|got (?:us |you )?out|rescue\w*|came to (?:america|the states))\b", re.I)


def turn_focus(state, who, listeners, level, cue):
    """Put just the relevant playable beat beside the actual line, after old history."""
    import four_aces
    import the_crow
    if who in four_aces.CAST:
        return (the_crow.address_direction(who) + ' ' + four_aces.CHARACTER_DIRECTION[who] +
                ' Show the disposition through the answer to the current subject; do not recite the profile. '
                'Respect audience clearance and actual history. With Ivan, retain this individual voice '
                'while keeping the conversation professional and deflecting personal questions.')
    if who == 'crow':
        import the_crow
        return the_crow.turn_direction()
    if who == 'charles':
        import charles_han
        return charles_han.direction(state,listeners)
    if who == 'thirteen':
        import thirteen
        return thirteen.direction()
    if who == 'takeo':
        import takeo
        return takeo.direction()
    beats = [the_crow.address_direction(who)] if the_crow.address_direction(who) else []
    if who == 'garrett' and CHARLES.search(cue):
        beats.append(charles_context(state, who, level))
        beats.append(CHARLES_NEWS)
        beats.append((
            'For questions about private family history, keep a personal boundary. For news about Charles, listen and respond with concern.',
            'Tell them plainly that your older brother is missing and you are looking. Let that fact land.',
            'Give one concrete detail of how you knew something was wrong: two missed Sunday calls, or the call to his old workplace.',
            'Take the question seriously and give a concrete, personal answer. Do not deny news already given in this conversation. '
            'You might miss the Sunday call during prep, the argument about shrimp shells that you wish you could finish, '
            'or making noodles together after your parents died. Choose the detail that fits what was actually asked.')[level])
    if who in ('yuriko', 'rei') and (ESCAPE.search(cue) or who == 'yuriko' and re.search(r'\b(?:rei|your (?:older |big )?brother)\b', cue, re.I)):
        sibling = 'rei' if who == 'yuriko' else 'yuriko'
        if list(listeners) == [sibling] and ESCAPE.search(cue):
            beats.append('This is a private exchange between the two people who survived it. Rei was fifteen when he '
                         'got Yuriko out of their yakuza clan, Hamayashi-kai, and brought them both to the States. '
                         'The clan subjected Rei to extreme training and torture from birth to forge a human weapon. '
                         'He had to kill the entire clan to take Yuriko and escape. Her more sheltered life still involved '
                         'misogynistic ideals and abuse; never dismiss it as a safe childhood. Speak directly to your sibling '
                         'about what one did for the other and what it means now. Yuriko can remember things Rei cannot. '
                         'Let care or relief come through without inventing the route, a chase or a newly recovered memory.')
        elif who == 'yuriko':
            beats.append(('Speak about your brother as someone you live with. His childhood is private.',
                          'Offer something you see at home, like the way he waits to be asked before helping with a set.',
                          'You can describe trusting Rei with a first draft or saving him a seat backstage.',
                          'If asked about growing up or how you got here, tell the listener something they can actually learn: '
                          'Rei got you both out when he was fifteen and brought you to America. If asked about everyday life, '
                          'choose a personal detail of your life together that fits instead. Speak for yourself about him.')[level])
    topics = topic_reference(who, cue)
    if topics:
        beats.extend(topics.values())
        if who == 'garrett' and 'Syndicate' in topics:
            beats.append('You run the Red Dragons. You know exactly which organisation they mean. If they joke about joining, '
                         'play off the obligations, the price of a favour, or what your friend would make of taking orders. '
                         'Make the joke work specifically about joining this organisation; they have not actually joined.')
    if who == 'sylvanis' and listeners == ['ivan'] and re.search(r'\b(?:leave|leaving|out|resign|release|order|press)\b', cue, re.I):
        beats.append('Ivan knows you are holding his signed order over him. You have threatened to send it to the press '
                     'if he walks away. Use that specific leverage in this private exchange. Their hostility and low trust '
                     'do not erase what both already know. Keep it in your own unsettling, precise voice.')
    return ' '.join(beats)


def check_reply(state, who, cue, reply):
    """Repair unambiguous continuity errors, leaving wording and tone to the model."""
    words = reply.casefold().replace('’', "'")
    if re.search(r'\bsyndicate\b', cue, re.I) and re.search(
            r"\b(?:which|what) syndicate\s*(?:\?|do you mean|are you talking about)|\bnever heard of (?:the |that )?syndicate", words):
        raise ValueError('The Syndicate is the known international organisation. Respond to what the player said about it.')
    if who == 'garrett' and CHARLES.search(cue):
        if re.search(r"\b(?:who(?:'s| is) charles|(?:i (?:don't|do not) have|i never had) (?:a |an older )?brother)\b", words):
            raise ValueError('Garrett recognises Charles as his missing older brother.')
        if not __import__('charles_quest').reunited(state) and re.search(r"(?:^|[.!]\s+|\bi (?:know|learned|found out) (?:that )?)(?:charles|my (?:older )?brother|he)"
                     r"(?: is|'s| was| went| works| worked) (?:dead[.!]|undercover\b|for the syndicate\b)", words):
            raise ValueError('Charles is missing. Garrett cannot establish his death, allegiance or whereabouts.')
        if __import__('charles_quest').reunited(state) and re.search(r"(?:charles|my brother|he) (?:is|was) dead[.!]",words):
            raise ValueError('Charles is alive after the authored reunion.')
        if 'west pier cold storage' in words and 'west pier' not in cue.lower() and (state['player'] != 'garrett' or state.get('charles_lead') != 'traced'):
            raise ValueError('Only the authored traced search lead reveals the receiving stamp.')


def grounded_alternative(who, listener, level, cue, reply, recent=()):
    """For direct story questions only, repair a generic or misattributed answer.

    On repair the model writes the entire scene around the authored line so its
    narration, choices and remembered events agree with the actual disclosure.
    """
    words = reply.casefold()
    if who == 'garrett' and CHARLES.search(cue) and re.search(
            r'\b(?:heard (?:anything|from)|any (?:news|word)|what happened to)\b', cue, re.I):
        if level == 3 and not re.search(
                r'\b(?:sundays?|call\w*|shells?|broth|noodles?|teacup|phone\w*|messages?|restaurant|'
                r'kitchen|work\w*|job|shift|flat|clothes|supplier|hong kong|parents|dough|recipe|prep)\b',
                ' '.join([words, *recent]).casefold()):
            return ("Still no word. I cut our last call short for a supplier. He was halfway through telling me "
                    "I make Mum’s broth wrong. I’d give a lot to hear the rest of that argument.")
        if level == 0 and not re.search(r"\b(?:my|me|family|private|personal|rather|brother|missing|looking|word|news)\b", words):
            return "Charles is my brother. I’m handling it. I’d rather keep the rest in the family for now."
    if who == 'yuriko' and listener == 'rei' and ESCAPE.search(cue) and re.search(
            r'\b(?:remember|think about|how we|how did we|got out)\b', cue, re.I):
        if not re.search(r'\b(?:you|fifteen|15|states|america|remember|home|safe|together|thank\w*)\b', words):
            return ("I think about how young you were. Fifteen, and you got us both all the way to the States. "
                    "If there’s a part you want me to remember with you, I can do that.")
    if who == 'garrett' and re.search(r'\b(?:imagine|what if)\b.*\bjoin\w*\b.*\bsyndicate\b', cue, re.I):
        if ('red dragons' in words and 'syndicate' not in words) or not re.search(
                r'\b(?:syndicate|order\w*|owe\w*|debt|favo[u]?rs?|price|cost|boss|recruit\w*|pay\w*|money|obligation\w*)\b', words):
            return "You taking orders? I’d pay to see that. Trouble with the Syndicate is they’d make you pay too."


def check_observer(information, who, cue, reply):
    for pair, row in information.items():
        people = pair.casefold().split(' and ')
        if who.casefold() in people:
            continue
        heard = ' '.join([cue, *row.get('words this person actually heard', [])])
        words = reply.replace('’', "'")
        if not row.get('words this person actually heard'):
            if re.search(r"\b(?:i've (?:seen|heard) them|i (?:saw|heard) them)\b", words, re.I):
                raise ValueError('The listener reported this interaction. This speaker was not an eyewitness.')
            subjects = '|'.join(re.escape(part) for name in people for part in name.split())
            if re.search(r"\b(?:(?:they(?:'re| are)?|he|she|" + subjects + r") (?:always|usually|keeps)|as usual)\b", words, re.I) and not re.search(
                    r'\b(?:always|every|usually|again|keep)\b', cue, re.I):
                raise ValueError('One reported interaction does not establish a recurring pattern between these people.')
        secret = {'Joseph Richter and Rei': r'\b(?:suicide|bullied|bullying|killed (?:themself|himself|herself))\b',
                  'Sylvanis and Ivan': r'\b(?:signed order|blackmail\w*|joker cards?|cardmaster)\b'}.get(pair)
        if pair == 'Joseph Richter and Rei' and row.get('already knows Joseph bullied Marcus'):
            # Authored school knowledge permits acknowledging the bullying,
            # but the eyewitness checks above still prohibit invented scenes.
            secret = None
        if secret and re.search(secret, reply, re.I) and not re.search(secret, heard, re.I):
            raise ValueError('This observer can infer familiarity or tension only from what they heard. The private cause has not been disclosed to them.')
