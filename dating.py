"""Relationship invitations and persistent one-on-one dates."""
import json
import re

import character_memory
import emotions
import social_world
import town
import mysterious_hearts


# Minimum closeness, trust and attraction, respectively.
STATS = ('closeness', 'trust', 'attraction')
LIMITS = {
    'samantha': ((10, 30, 18), (75, 80, 70)),
    'april': ((45, 60, 38), (65, 75, 60)),
    'emily': ((48, 60, 42), (70, 78, 65)),
    'sophie': ((22, 38, 24), (55, 65, 52)),
    'amy': ((32, 50, 28), (60, 72, 55)),
    'yuriko': ((25, 42, 25), (55, 68, 52)),
    'lena': ((30, 45, 28), (58, 67, 55)),
    'naomi': ((38, 55, 32), (65, 72, 58)),
    'celeste': ((24, 42, 25), (55, 65, 55)),
    'valentina': ((28, 45, 28), (62, 72, 55)),
    'rei': ((35, 50, 30), (65, 75, 55)),
    'garrett': ((20, 38, 25), (65, 72, 60)),
    'minsu': ((25, 42, 25), (55, 65, 50)),
    'ivan': ((35, 52, 30), (65, 75, 60)),
    'tyler': ((30, 45, 30), (58, 68, 52)),
    'daniel': ((35, 48, 30), (62, 70, 55)),
    'dev': ((32, 45, 30), (60, 68, 52)),
    'elliot': ((38, 50, 30), (62, 72, 55)),
    'Theo': ((28, 42, 30), (55, 65, 50)),
    'Noah': ((25, 40, 30), (55, 65, 52)),
    'Leo': ((22, 38, 30), (58, 64, 52)),
}
ASK = {'date': 'Would you like to go on a date with me?',
       'official': 'I’d like to make this official. How do you feel about being exclusive?'}
KISS = 'Share your first kiss together'
GOALS = ('conversation', 'activity', 'kiss')
PRICE = 150
DECLARATIONS = {
    'sophie': 'She can flirt as a joke. When someone means it, let her drop the competitive banter long enough to answer them plainly.',
    'samantha': 'She can want a date immediately and still want to talk honestly about exclusivity. Let her own the distinction.',
    'april': 'She rarely flirts casually. Give her a precise, personal answer. With Garrett she can reach for one of their childhood memories.',
    'amy': 'She cares what the words mean to the person saying them. Let her offer her own answer, as well as ask a question.',
    'garrett': 'His first instinct may be a cocky comeback. When trust runs deep, he can risk a plain admission and let it stand.',
    'ivan': 'He values being chosen freely. An answer can be quiet and direct, followed by a specific time he wants to keep for them.',
    'valentina': 'Let her speak for herself. If she wants a date, she can take the lead and propose what to do together.',
}


def minimums(s, who, kind):
    levels = LIMITS[who]
    if who == 'april' and s['player'] == 'garrett':
        levels = ((28, 42, 20), (50, 65, 48))
    if who == 'emily' and s['player'] == 'rei' and mysterious_hearts.feeling(s, 'emily', 'rei') >= 60:
        levels = ((0, 0, 0), (45, 58, 42))
    return levels[0 if kind == 'date' else 1]


def decision(s, who, kind, *, face_to_face=False):
    if kind in ASK and who in town.sexuality.CANON and not town.sexuality.compatible(s['player'], who):
        return 'no', town.sexuality.reason(s['player'], who)
    if kind not in ASK or not town.romanceable(s, who) or who not in s['relationships'] or not town.hidden.known(s, who):
        raise ValueError('This relationship invitation is unavailable.')
    if not town.hidden.contact(s, who) and not (face_to_face and town.present(s, who)):
        raise ValueError('Exchange contact details first so you can send an invitation.')
    r = s['relationships'][who]
    if kind == 'date' and s.get('date_session'):
        raise ValueError('Finish or cancel the current date before arranging another.')
    if r['status'] == 'strained' or r.get('unresolved_harm'):
        return 'no', 'Trust needs repair.'
    if kind == 'date' and who == 'emily' and s['player'] == 'rei' and mysterious_hearts.feeling(s, 'emily', 'rei') >= 60:
        return 'yes', 'She has wanted him to ask. Her first reaction is unmistakable delight.'
    if kind == 'official' and r['status'] != 'dating':
        return 'no', 'They are already exclusive.' if r['status'] == 'official' else 'They need to date before becoming exclusive.'
    missing = [key for key, n in zip(STATS, minimums(s, who, kind)) if r.get(key, 0) < n]
    if missing:
        return 'no', 'They need more ' + ', '.join(missing) + '.'
    return 'yes', 'They feel ready to take this step.'


def can_confess(s, who):
    r = s['relationships'].get(who, {})
    if (not town.romanceable(s, who) or not r or r.get('confessed_at') is not None or r.get('breakups')
            or r.get('unresolved_harm') or r.get('status') in town.ROMANTIC_STATUSES or s.get('date_session')
            or any(b.get('status') in ('official','strained') for b in s['relationships'].values())):
        return False
    if (s['player'], who) == ('rei', 'emily') and mysterious_hearts.feeling(s, 'emily', 'rei') >= 60:
        return r['trust'] >= 100
    return who in ('sophie', 'samantha', 'amy', 'garrett', 'ivan', 'valentina') and (
        r['trust'] >= 90 and r['closeness'] >= 75 and r.get('attraction', 0) >= 70)


def romantic_voice(s, who):
    orientation = town.sexuality.direction(s['player'], [who])
    if not town.romanceable(s, who):
        return orientation+' Receive declarations according to this platonic or adversarial relationship. Keep sibling love familial.'
    guidance = ('Answer confessions, “I love you”, date invitations and requests for exclusivity as different moments. '
                'Use this speaker’s personality, their friendship, current romantic relationship and history. '
                'A surprised pause can lead to a clear answer. A partner might recall a specific shared moment; '
                'someone unsure can say what they do feel. A declaration alone never creates a date or exclusivity.')
    guidance += ' ' + DECLARATIONS.get(who, '')
    bond = s['relationships'].get(who, {})
    if bond.get('unresolved_harm') or bond.get('status') == 'strained':
        guidance += ' A loving statement can matter while trust still needs repair. Address the actual hurt.'
    elif bond.get('status') == 'official':
        guidance += ' They already chose each other. Answer as a partner who remembers that promise and their recent time together.'
    elif bond.get('status') == 'dating':
        guidance += ' Let the last date colour the answer. They have begun dating and can still want different things from commitment.'
    if bond.get('confessed_at') is not None:
        guidance += ' You have already told the player how you feel. Build on their response rather than treating it as a secret again.'
    if (s['player'], who) == ('rei', 'emily') and mysterious_hearts.feeling(s, 'emily', 'rei') >= 60:
        guidance += (' Emily currently has strong feelings for Rei. When he asks her out and trust is intact, let her joy lead: '
                     'say yes clearly and eagerly, then take some initiative about their date. Her stutter can carry '
                     'excitement. When he tells her he loves her, allow real relief and reciprocal tenderness. '
                     'Use her own fresh words and their shared history.')
    return orientation+' '+guidance


def conversation_direction(s, who, schema, played):
    direction = '\n' + romantic_voice(s, who)
    import relationship_dynamics
    pending_date = any(p['status'] == 'open' and p.get('proposal_type') == 'date'
                       for p in relationship_dynamics.peek(s, who)['proposals'])
    if pending_date:
        direction += (' You previously proposed a date. An explicit player acceptance of that pending date '
                      'counts as a request for the date step if eligible; generate date_topics and relationship_step=date. '
                      'A vague answer, refusal or acceptance of an introduction does not start a date.')
    moves = ['none']
    if played and who in s['relationships'] and town.romanceable(s, who):
        for kind in ASK:
            try:
                face_to_face = s['routes'].get(who, {}).get('channel') == 'in_person' or who in town.LOCAL_MEN
                answer, reason = decision(s, who, kind, face_to_face=face_to_face)
            except ValueError as exc:
                answer, reason = 'no', str(exc)
            direction += f' If the player currently asks for {kind}, the answer is {answer}: {reason} Respond in character.'
            if answer == 'yes': moves.append(kind)
    if can_confess(s, who):
        moves.append('confession')
        direction += (' On a fitting private beat you can initiate a first romantic confession in your own words. '
                      'Leave room for the player to respond. Set relationship_step to confession only if you actually tell them. '
                      'Respect any prior rejection or request for space.')
    else:
        direction += ' Leave initiation of a new confession to the player this turn. You can respond honestly to their feelings.'
    if len(moves) > 1:
        schema['properties']['relationship_step'] = {'type':'string','enum':moves}
        schema['required'].append('relationship_step')
        direction += (' Return relationship_step for an explicit new step in this exchange. Use date or official only if '
                      'the player explicitly asks for that step and the partner accepts in the delivered dialogue, '
                      'or the player explicitly accepts this speaker’s recorded pending date proposal. '
                      'Ordinary plans, past dates, I love you, jokes, hypotheticals and unsent choices are none.')
        if 'date' in moves:
            schema['properties']['date_topics'] = {'type':'array','maxItems':2,'items':{'type':'string'}}
            schema['required'].append('date_topics')
            direction += (' For an accepted date return date_topics with two short playable goals: a personal conversation topic '
                          'and a shared activity. Each under 90 characters. The game supplies the kiss goal. Otherwise return [].')
    return direction


def conversation_goals(data):
    topics = data.get('date_topics')
    if not isinstance(topics, list) or len(topics) != 2:
        raise ValueError('An accepted date needs a conversation topic and a shared activity.')
    goals = dict(conversation=topics[0], activity=topics[1], kiss=KISS)
    validate_goals(goals)
    return goals


def check_conversation_step(s, who, data, played):
    step = data.get('relationship_step', 'none')
    if step == 'none': return
    if step == 'confession' and can_confess(s, who): return
    face_to_face = s['routes'].get(who, {}).get('channel') == 'in_person' or who in town.LOCAL_MEN
    if step not in ASK or not played or decision(s, who, step, face_to_face=face_to_face)[0] != 'yes':
        raise ValueError('This relationship step is unavailable.')
    if step == 'date': conversation_goals(data)


def apply_conversation_step(s, who, data):
    step = data.get('relationship_step')
    if step == 'confession':
        s['relationships'][who]['confessed_at'] = s['world']['minute']
        town.relationship_notice(s, who, who.title() + ' told you about their feelings.')
    elif step in ASK:
        accept(s, who, step, conversation_goals(data) if step == 'date' else None)


def validate_answer(data, answer, kind):
    if (not isinstance(data, dict) or data.get('answer') != answer or not isinstance(data.get('reply'), str)
            or not data['reply'].strip() or len(data['reply']) > 1200):
        raise ValueError('Expected an in-character reply to this invitation.')
    if kind == 'date' and answer == 'yes':
        validate_goals(data.get('goals'))


def validate_goals(goals):
    if (not isinstance(goals, dict) or set(goals) != set(GOALS) or goals['kiss'] != KISS
            or any(not isinstance(g, str) or not g.strip() or len(g) > 90 or '\n' in g for g in goals.values())
            or len({g.strip().casefold() for g in goals.values()}) != 3
            or any(re.search(r'\bkiss\w*\b', goals[k], re.I) for k in GOALS[:2])):
        raise ValueError('Expected three distinct date goals including the first kiss.')


def validate_saved(s):
    if 'date_session' not in s:
        return
    date = s['date_session']
    if not isinstance(date, dict):
        raise ValueError('The saved date is damaged.')
    who, done = date.get('partner'), date.get('done')
    if (not isinstance(who, str) or who not in s['relationships'] or not town.romanceable(s, who)
            or type(date.get('started')) is not bool or not isinstance(done, list)
            or any(k not in GOALS for k in done) or len(set(done)) != len(done) or len(done) == 3
            or (who in town.LOCAL_MEN and date.get('meeting_place') not in town.LOCATIONS)):
        raise ValueError('The saved date is damaged.')
    validate_goals(date.get('goals'))


def generate_invitation(s, who, kind):
    import game_core as core
    answer, reason = decision(s, who, kind)
    player = core.PLAYERS[s['player']]
    name = core.CONTACTS[who][0] if who in core.CONTACTS else who
    question = ASK[kind]
    system = (f'Write the short phone text {name} sends in reply to {player}. The invitation is real. '
              f'The decision is {answer}: {reason} Make that answer clear in their own words. '
              'Keep game stats, objectives and undisclosed secrets out of the text. An invitation does not establish a kiss or teleport anyone. '
              + core.PHONE_DELIVERY + ' Voice: ' + core.TEXT_STYLES.get(who, 'Conversational, personal and direct.'))
    if who in core.CONTACTS:
        styles = json.loads((core.ROOT / 'dialogue_styles.json').read_text(encoding='utf-8'))
        system += '\nCharacter voice: ' + styles.get(who, styles.get(who + '_player', ''))
    else:
        _, role, hook = next(n for n in town.NPCS if n[0] == who)
        system += f' Their work: {role}. Something they know: {hook}'
    feelings = emotions.snapshot(s, [who])
    system += '\n' + romantic_voice(s, who) + social_world.knowledge_direction(s, [who])
    system += (' Report their feelings after reading this invitation, and the player’s feeling as they ask. '
               'Keep the player’s previous feeling if the message leaves it open. Current feelings: ' + json.dumps(feelings))
    delighted = kind == 'date' and answer == 'yes' and (s['player'], who) == ('rei','emily')
    props = {'answer': {'type':'string', 'enum':[answer]}, 'reply': {'type':'string'},
             'emotions':emotions.schema(feelings, {'emily':'ecstatic'} if delighted else {})}
    if kind == 'date' and answer == 'yes':
        system += (' Generate three date goals. conversation is one concrete topic these people could explore; '
                   'activity is one simple shared action achievable in any hangout through a custom gesture or dialogue. '
                   'Draw on their interests and recent exchanges. No required purchases, travel or invented props. '
                   'Use distinct short imperative labels, up to 90 characters. kiss is the specified mutual first kiss.')
        props['goals'] = {'type':'object', 'properties':{'conversation':{'type':'string'}, 'activity':{'type':'string'},
                          'kiss':{'type':'string', 'enum':[KISS]}}, 'required':list(GOALS), 'additionalProperties':False}
    chat = s['routes'].get(who) or s.get('npc_chats', {}).get(who, {})
    import memory_store
    context = dict(message=question, relationship=social_world.status_line(s, who),
                   history=chat.get('history', [])[-4:], memory=memory_store.summary(s,who,question),
                   previous_date=s['relationships'][who].get('last_date'))
    schema = {'type':'object', 'properties':props, 'required':list(props), 'additionalProperties':False}
    for attempt in range(2):
        response = core.request('/api/chat', dict(model=core.MODEL, stream=False, think=False, format=schema,
            messages=[{'role':'system','content':system}, {'role':'user','content':json.dumps(context, ensure_ascii=False)}],
            options={'temperature':0.7, 'num_ctx':8192, 'num_predict':900}))
        try:
            data = json.loads(response['message']['content'])
            validate_answer(data, answer, kind)
            emotions.validate(data.get('emotions'), feelings)
            return data
        except (ValueError, KeyError, TypeError) as exc:
            if attempt:
                raise ValueError('Could not generate the invitation reply. Please retry.') from exc
            system += '\nRepair the response: ' + str(exc)


def session(s, who):
    date = s.get('date_session')
    return date if date and date['partner'] == who else None


def in_hangout(s, who):
    date = session(s, who)
    return bool(date and date['started'] and town.present(s, who) and
                (who not in s['routes'] or s['routes'][who]['channel'] == 'in_person'))


def begin(s, who):
    if not town.romanceable(s, who): return False
    date = session(s, who)
    if not date or date['started'] or not town.present(s, who) or s['world']['money'] < PRICE:
        return False
    date['started'] = True
    s['world']['money'] -= PRICE
    town.betrayal(s, who, 'a date')
    town.relationship_notice(s, who, 'Your date has started ($150).\n' + describe(s, who))
    return True


def commit_invitation(s, who, kind, data):
    import game_core as core
    answer, _ = decision(s, who, kind)
    validate_answer(data, answer, kind)
    if 'emotions' in data:
        emotions.validate(data['emotions'], (s['player'], who))
        s['emotions'].update(data['emotions'])
    question, reply = ASK[kind], data['reply'].strip()
    route = s['routes'].get(who)
    if route is not None:
        scene = {'narration':'A reply arrives on your phone.', 'dialogue':reply, 'conversation_channel':'text', 'choices':[], 'suggestions_deferred':True}
        route['history'].extend([{'role':'user','channel':'text','content':question,'minute':s['world']['minute']},
                                 {'role':'assistant','channel':'text','content':json.dumps(scene, ensure_ascii=False),'minute':s['world']['minute']}])
        if route['channel'] == 'text':
            route.update(dialogue=reply, scene=scene['narration'], memory=route['memory'] or question + ' ' + reply,
                         choices=[], suggestions_deferred=True, suggestions_requested=[],
                         ordered_tones=False, personal_choices=[], unread=0, followup_sent=False,
                         awaiting_since=s['world']['minute'], idle_wait=0)
    else:
        chat = s.setdefault('npc_chats', {}).setdefault(who, {'history': []})
        chat.update(choices=[],personal_choices=[],suggestions_requested=[],suggestions_deferred=True)
        chat['history'].extend([{'speaker':core.PLAYERS[s['player']]+' (You)', 'text':question, 'channel':'text'},
                                {'speaker':who, 'text':reply, 'channel':'text'}])
    if answer == 'yes':
        accept(s, who, kind, data.get('goals'))
    s['turn'] += 1
    # Sending/receiving an invitation by phone never advances the story clock.
    return reply


def accept(s, who, kind, goals):
    if not town.romanceable(s, who):
        raise ValueError('This pairing is not romantically compatible.')
    if kind == 'date':
        import relationship_dynamics
        for proposal in relationship_dynamics.peek(s, who)['proposals']:
            if proposal['status'] == 'open' and proposal.get('proposal_type') == 'date':
                proposal['status'] = 'accepted'
    route = s['routes'].get(who)
    if kind == 'date':
        if (s['player'], who) == ('rei', 'emily') and mysterious_hearts.feeling(s, 'emily', 'rei') >= 60:
            s['emotions'][who] = 'ecstatic'
        kissed = 'kiss' in s['relationships'][who].get('firsts', {})
        date = dict(partner=who, started=False, goals=goals.copy(), done=['kiss'] if kissed else [])
        s['date_session'] = date
        if who in town.LOCAL_MEN:
            place = s['world']['location']
            date['meeting_place'] = place if town.present(s, who) else ('cafe' if place == 'square' else 'square')
        if town.present(s, who):
            if route is not None:
                town.meet(s, who)
            else:
                begin(s, who)
        if not date['started']:
            town.relationship_notice(s, who, describe(s, who))
    elif kind == 'official':
        town.become_official(s, who)


def describe(s, who):
    date = session(s, who)
    if not date:
        return ''
    if in_hangout(s, who):
        heading = 'Date goals'
    else:
        where = town.LOCATIONS[date['meeting_place']] if 'meeting_place' in date else town.loop.place_name(s, who)
        heading = ('Resume your date' if date['started'] else 'Meet with $150 to start your date') + ' · ' + where
    return heading + '\n' + '\n'.join(('✓ ' if k in date['done'] else '□ ') + date['goals'][k] for k in GOALS)


def configure_turn(s, who, schema, played):
    date = session(s, who)
    pending = [k for k in GOALS[:2] if k not in date['done']]
    if pending and played:
        schema['properties']['date_progress'] = {'type':'array', 'items':{'type':'string','enum':pending}, 'maxItems':len(pending)}
        schema['required'].append('date_progress')
    direction = ('\nThis is a private date. Let the next exchange help the player pursue these goals naturally: '
            + json.dumps(date['goals']) + '. Already achieved: ' + json.dumps(date['done'])
            + '. Only a newly completed mutual kiss counts as a kiss. Let either person decline.')
    if pending and played:
        direction += (' Return date_progress for pending conversation/activity IDs actually achieved with this partner this turn. '
                      'Return [] for an attempt, promise, mere request for credit or unsent suggestion.')
    if not played:
        direction += ' Set the scene. Leave every goal and physical decision for the player’s next turn.'
    return direction


def check_progress(s, who, data, played):
    date = session(s, who)
    pending = set(GOALS[:2]) - set(date['done']) if played and in_hangout(s, who) else set()
    ids = data.get('date_progress', None if pending else [])
    if (not isinstance(ids, list) or any(not isinstance(k, str) or k not in pending for k in ids)
            or len(set(ids)) != len(ids)):
        raise ValueError('Invalid date goal progress. Please retry this turn.')
    return ids


def advance(s, who, ids, kissed):
    if not town.romanceable(s, who): return
    date = session(s, who)
    if not date or not in_hangout(s, who):
        return
    if kissed:
        character_memory.record_first(s, who, 'kiss')
    reached = set(ids)
    if 'kiss' in s['relationships'][who].get('firsts', {}):
        reached.add('kiss')
    new = [k for k in GOALS if k in reached and k not in date['done']]
    date['done'].extend(new)
    if new:
        town.relationship_notice(s, who, 'Date progress · ' + ' · '.join(date['goals'][k] for k in new))
    if len(date['done']) == 3:
        del s['date_session']
        town.date_progress(s, who)
        character_memory.record_first(s, who, 'date')
        r = s['relationships'][who]
        r['last_date'] = dict(when=town.loop.clock(s), goals=date['goals'])
        note = 'Date complete with ' + who.title() + ' · all three goals achieved.'
        r.setdefault('milestones', []).append(town.loop.clock(s) + ': ' + note)
        town.relationship_notice(s, who, note)
        town.log(s, note)


def cancel(s, who):
    if session(s, who):
        del s['date_session']
        town.relationship_notice(s, who, 'Date cancelled.')
