"""Current feelings shared by private chats, group chats and town encounters."""
import json


FEELINGS = (
    'content', 'happy', 'ecstatic', 'sad', 'miserable', 'jealous', 'inspired',
    'focused', 'anxious', 'scared', 'angry', 'enraged', 'flirty', 'enamored',
    'grateful', 'playful', 'curious', 'hopeful', 'relieved', 'embarrassed',
    'disappointed', 'surprised', 'proud', 'irritated', 'lonely', 'flustered',
    'amused', 'guarded',
)

TONE_REACTIONS = {
    'Friendly': 'Acknowledge the actual offer or greeting. Familiar company can put someone at ease; a stranger may take an interest cautiously.',
    'Sincere': 'Answer what was honestly shared. An apology, a confession and painful news can land very differently.',
    'Funny': 'React to the specific joke or comic gesture. They might laugh, top the joke, miss it or call out its timing.',
    'Flirtatious': 'Let the intended recipient notice the specific flirt. They can be bashful, tease back, hold a boundary or turn it down.',
    'Supportive': 'Show how this particular offer of support lands between siblings.',
    'Inquisitive': 'Answer with one particular moment from their day. Their mood can colour which moment they pick.',
    'Connection': 'Share an interest, value or memory at a depth that fits their trust in the player.',
    'Open': 'Respond to the detail the player just volunteered, in a way that fits their relationship.',
    'Emotional': 'Let them choose how much to share and whether to ask the player how they feel too.',
}

NEXT_MORNING = {
    'flustered': 'content', 'amused': 'content', 'surprised': 'content',
    'playful': 'content', 'flirty': 'content', 'ecstatic': 'happy',
    'enraged': 'angry', 'miserable': 'sad',
}
INPUT_TONES = (*TONE_REACTIONS, 'Other')


def current(state, who):
    return state['emotions'].get(who, 'content')


def snapshot(state, members):
    return {who: current(state, who) for who in (state['player'], *members)}


def likely_reaction(state, who, tone):
    """A starting beat for an addressed character, given their mood and relationship."""
    if tone not in TONE_REACTIONS:
        return None
    import town
    feeling = current(state, who)
    bond = town.character_stats(state, who) or {}
    guarded = (bond.get('status') in ('strained', 'exes') or bond.get('unresolved_harm')
               or bond.get('trust', 50) < 25
               or feeling in ('angry', 'enraged', 'jealous', 'irritated', 'guarded', 'disappointed'))
    hurting = feeling in ('anxious', 'scared', 'sad', 'miserable', 'lonely')
    close = bond.get('closeness', 0) >= 45
    if tone == 'Flirtatious':
        if not town.romanceable(state,who):
            return 'guarded'
        if who in ('sylvanis', 'neo', 'alyssa', town.RICHTER) or town.sibling_route(state, who):
            return 'guarded'
        if guarded or hurting:
            return 'guarded' if guarded else feeling
        return {'emily': 'flustered', 'sophie': 'playful', 'samantha': 'flirty',
                'april': 'curious', 'amy': 'flustered'}.get(who, 'playful' if close else 'surprised')
    if tone == 'Funny':
        if guarded:
            return 'irritated'
        if hurting and close:
            return 'relieved'
        return 'playful' if close else 'amused'
    if tone == 'Friendly':
        if guarded:
            return 'guarded'
        if hurting:
            return 'relieved'
        return 'happy' if close else 'curious'
    if tone in ('Inquisitive', 'Connection', 'Open', 'Emotional'):
        if guarded:
            return 'guarded'
        if hurting:
            return 'relieved' if close else feeling
        return 'grateful' if tone == 'Emotional' and close else 'curious'
    # Sincerity and support can open a conversation while trust is being repaired.
    if guarded:
        return 'hopeful'
    return 'relieved' if hurting else 'grateful'


def expected_feelings(state, members, tone, result=None):
    """Emily's authored reaction applies to a flirt directed at her in a receptive moment."""
    if state['player'] != 'rei' or 'emily' not in members:
        return {}
    result = result or {}
    direct = len(members) == 1
    targeted_flirt = (result.get('social_event') in ('flirt', 'welcomed_flirt', 'returned_flirt')
                      and (direct or result.get('social_target') == 'emily'))
    if not ((direct and tone == 'Flirtatious') or targeted_flirt):
        return {}
    if likely_reaction(state, 'emily', 'Flirtatious') == 'flustered':
        return {'emily': 'flustered'}
    return {}


def direction(state, members, tone, texting):
    previous = snapshot(state, members)
    guide = (
        '\nCurrent private feelings by character ID: ' + json.dumps(previous) +
        '. Return emotions with these exact IDs and one lowercase feeling per person. '
        'Choose from ' + ', '.join(FEELINGS) + '. Start from each previous feeling and '
        'change it only when this exchange gives that person a reason. Let the feeling '
        'shape their delivery without naming it in every line. For the player (' + state['player'] +
        '), use only what their submitted words or actions express. Keep their feeling '
        'on openings, scene directions and ambiguous input. Unsent choices express no '
        'one’s feelings. Private feelings are not shared knowledge or proof of attraction.'
    )
    if tone:
        guide += '\nThe submitted choice has the tone ' + tone + '. ' + TONE_REACTIONS.get(tone, 'Respond to this move in character.')
        if tone in TONE_REACTIONS:
            beats = {who: likely_reaction(state, who, tone) for who in members}
            guide += (' Use this immediate feeling for the person addressed unless the scene gives a more specific reaction: '
                      + json.dumps(beats) + '.')
    else:
        guide += ('\nWhen the schema requests input_tone, classify the free-form words or gesture as '
                  + ', '.join(INPUT_TONES) + '. A quoted joke or an account of past flirting '
                  'can be a serious disclosure. Answer the move in character. On an opening, react to the situation itself.')
    guide += (' Write the reaction into the answer itself. Consider the topic, previous feeling, trust, '
              'recent events and boundaries. A painful disclosure or a badly timed joke can outweigh its tone. '
              'In a group, distinguish the recipient from people observing. Report the feeling the answer conveys.')
    guide += (' Convey the reaction in the message they type, through wording, timing or punctuation.'
              if texting else ' Show the response in their spoken words or an observable gesture in narration.')
    if ('emily' in members and state['player'] == 'rei'
            and likely_reaction(state, 'emily', 'Flirtatious') == 'flustered'):
        guide += (' When Rei flirts with Emily herself, her immediate feeling is flustered. '
                  'Let her lose her train of thought or try a shy comeback specific to what Rei just did. '
                  'If he asks her out, show how pleased she is. Keep undisclosed feelings private unless '
                  'this turn permits a confession or she is answering his declaration.')
    return guide


def schema(participants, expected=None):
    expected = expected or {}
    properties = {who: {'type': 'string', 'enum': [expected[who]] if who in expected else list(FEELINGS)}
                  for who in participants}
    return {'type': 'object', 'properties': properties,
            'required': list(participants), 'additionalProperties': False}


def request_input_tone(schema):
    schema['properties']['input_tone'] = {'type': 'string', 'enum': list(INPUT_TONES)}
    schema['required'].append('input_tone')


def validate(report, participants, expected=None):
    if (not isinstance(report, dict) or set(report) != set(participants)
            or any(value not in FEELINGS for value in report.values())):
        raise ValueError('Expected one supported feeling for each conversation participant.')
    for who, feeling in (expected or {}).items():
        if report[who] != feeling:
            raise ValueError(f'Show {who} reacting to this turn as {feeling} in the response and report that feeling.')


def turn_update(state, result, members, *, tone=None, player_acted=True, generated=False):
    """Keep specific scene reactions; resolve a flat neutral report from the move that landed."""
    if player_acted and tone is None:
        tone = result.get('input_tone')
        if (generated or 'input_tone' in result) and tone not in INPUT_TONES:
            raise ValueError('Classify the submitted words or action using one of the listed input tones.')
    expected = expected_feelings(state, members, tone, result) if player_acted else {}
    player = state['player']
    previous = snapshot(state, members)
    if generated or 'emotions' in result:
        validate(result.get('emotions'), previous, expected if generated else None)
        feelings = dict(result['emotions'])
    else:
        feelings = previous.copy()
    if not player_acted:
        feelings[player] = previous[player]
    else:
        if tone in (None, 'Other') and result.get('social_event') in ('flirt', 'welcomed_flirt', 'returned_flirt'):
            tone = 'Flirtatious'
        target = members[0] if len(members) == 1 else result.get('social_target')
        if target in members and (feelings[target] == 'content' or 'emotions' not in result):
            reaction = likely_reaction(state, target, tone)
            if reaction:
                feelings[target] = reaction
        expressed = {'Funny': 'playful', 'Flirtatious': 'flirty'}.get(tone)
        if expressed and feelings[player] == previous[player] == 'content':
            feelings[player] = expressed
        feelings.update(expected)
    if 'emotions' not in result and feelings == previous:
        return {}
    return feelings
