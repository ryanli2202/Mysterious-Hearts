"""Small local conversations: authored identity, recent chat and familiarity only."""
import json
import character_types


def generate(state, names, context, *, texting=False, opening=False):
    import game_core as core
    import town
    import groups
    import emotions
    profiles = {}
    for name in names:
        detail = next(p for p in (*town.NPCS, *town.VENUE_STAFF.values(), town.HQ_EXECUTIVE) if p[0] == name)
        profiles[name] = dict(role=detail[1], background=detail[2],
            today=town.town_residents.context(name, state['world']['minute']),
            familiarity=state.get('npc_chats', {}).get(name, {}).get('connection', {}).get('status', 'strangers'))
        import criminal_dynamics
        profiles[name]['Criminal dynamics'] = criminal_dynamics.context(name, [state['player'], *[n for n in names if n != name]], state)
        import keisuke
        member = (state.get('job_apps', {}).get('gang') or {}).get('members', {}).get(name)
        if member:
            profiles[name]['Player crew'] = dict(name=state['job_apps']['gang']['name'], role=member['role'],
                boundary='Voluntarily recruited in this save. Ordinary life and routine retained. No secret past or automatic access to faction secrets. Dialogue cannot change membership or roles.')
        if name == keisuke.NAME:
            profiles[name]['Shinokami liaison context'] = keisuke.context(state)
        import gang_members
        if name in gang_members.MEMBERS:
            profiles[name]["Gang coworker"] = gang_members.context(state, name)
        import gang_leaders, criminal_reputation
        if name in gang_leaders.BY_NAME:
            profiles[name]['Gang leadership'] = gang_leaders.context(state, name)
            if texting: profiles[name]['Gang leadership']['meeting'] = {}
        if fear := criminal_reputation.context(state, name):
            profiles[name]['Underworld reputation'] = fear
        if name == town.RICHTER and state['player'] == 'rei':
            profiles[name]['established_history'] = town.RICHTER_HISTORY
    system = ('Write an ordinary conversation with town NPCs in Winterfield. Only listed participants speak. '
        'Keep their individual voices, jobs, interests and boundaries. Town NPCs are strictly nonromantic: '
        'decline romantic or sexual advances clearly, without implying they can be won over. '
        'They have no Grove accounts or Meet-Cute profiles. Do not invent posts, dates, gifts, quests, '
        'promises completed, private knowledge, player actions or shared history. '
        'Remember the supplied recent conversation. Respond briefly and naturally, not as a quest menu. '
        'No attraction, jealousy, dating goals, attachment analysis or relationship milestones. '
        'Return narration, spoken contributions and current emotions for all participants. '
        + (core.PHONE_DELIVERY if texting else core.SPOKEN_DELIVERY))
    if texting:
        system += ' Return exactly one message per participant.'
    else:
        system += '\n' + core.dialogue_craft.direction(
            context.get('recent_exchange', context.get('recent_group', [])), names, group=len(names) > 1)
    payload = dict(player=core.PLAYERS[state['player']], residents=profiles,
        player_reply=context.get('player_reply') or context.get('player_input') or context.get('player_action'),
        recent_exchange=context.get('recent_exchange', context.get('recent_group', []))[-24:],
        location=None if texting else town.loop.place_name(state), clock=town.loop.clock(state),
        channel='text' if texting else 'in_person')
    participants = [state['player'], *names]
    schema = {'type': 'object', 'properties': {
        'narration': {'type':'string'},
        'lines': {'type':'array', 'minItems':len(names) if texting else 1, 'maxItems':len(names) if texting else core.dialogue_craft.line_limit(names), 'items': {
            'type':'object', 'properties': {'speaker':{'type':'string','enum':names}, 'text':{'type':'string'}},
            'required':['speaker','text'], 'additionalProperties':False}},
        'emotions': emotions.schema(participants)},
        'required':['narration','lines','emotions'], 'additionalProperties':False}
    for _ in range(2):
        response = core.request('/api/chat', {'model':core.MODEL,
            'messages':[{'role':'system','content':system},{'role':'user','content':json.dumps(payload,ensure_ascii=False)}],
            'format':schema,'stream':False,'think':False,
            'options':{'temperature':0.7,'num_ctx':8192,'num_predict':1200}})
        try:
            data = json.loads(response['message']['content'])
            data.update(choices=[], suggestions_deferred=True)
            validate(state, names, data, texting=texting)
            if not texting: groups.validate_spoken_exchange(data)
            return data
        except (ValueError, KeyError, TypeError) as error:
            system += '\nRepair response format: '+str(error)
    raise ValueError('The local conversation could not be validated. Please retry.')


def validate(state, names, data, *, texting=False):
    import groups
    import emotions
    groups.validate(data, names, flexible=not texting)
    emotions.validate(data.get('emotions'), [state['player'], *names])
    if data.get('kissed_contact', 'none') != 'none' or data.get('social_event', 'none') not in ('none', 'flirt'):
        raise ValueError('Town NPC conversations cannot create romantic progression.')


def familiarity(state, name):
    chat = state.setdefault('npc_chats', {}).setdefault(name, {'history': []})
    link = chat.setdefault('connection', dict(status='acquaintances', trust=35, closeness=0))
    day = state['world']['minute']//1440
    days = link.setdefault('visit_days', [])
    if day not in days: days.append(day)
    link['visit_days'] = days[-3:]
    if link.get('status') != 'established colleagues':
        link['status'] = 'familiar face' if len(days) >= 3 else 'acquaintances'
    return link


def commit(state, names, reply, data, *, group=None, texting=False, mark_read=True):
    import combat
    if combat.active(state) or combat.recovering(state) or any(combat.recovering(state,who) for who in names):
        raise ValueError('Finish combat or recover before conversation.')
    import game_core as core
    import town
    import groups
    validate(state, names, data, texting=texting)
    if not texting:
        for name in names: town.npc_details(state, name)
        groups.validate_spoken_exchange(data)
    minute = state['world']['minute']
    lines = []
    if reply is not None and reply not in (*core.SCENE_DIRECTIONS, core.INCOMING_TEXT):
        line = dict(speaker=core.PLAYERS[state['player']]+' (You)', text=reply, minute=minute)
        if not texting and reply.startswith(core.ACTION_PREFIX):
            line.update(kind='action', text=reply[len(core.ACTION_PREFIX):])
        lines.append(line)
        for name in names: familiarity(state, name)
    lines.append(dict(speaker='Narrator', text=data['narration'], minute=minute))
    lines.extend(dict(line, minute=minute) for line in data['lines'])
    if texting:
        for line in lines: line['channel'] = 'text'
    for name in names:
        chat = state.setdefault('npc_chats', {}).setdefault(name, {'history': []})
        chat['history'].extend(lines)
        chat.update(choices=data['choices'], personal_choices=[], suggestions_requested=[],
                    suggestions_deferred=data.get('suggestions_deferred', False), ordered_tones=name != town.RICHTER)
        town.acknowledge_arrival(state, name)
    if group is not None:
        # In-person local groups share the chat's history object already.
        if not any(group['history'] is state['npc_chats'][n]['history'] for n in names):
            group['history'].extend(lines)
        group.update(choices=data['choices'], suggestions_deferred=data.get('suggestions_deferred',False),
                     suggestions_requested=[], ordered_tones=True)
        if texting: group['unread'] = 0 if mark_read else group.get('unread',0)+1
    feelings = dict(data['emotions'])
    if reply is None or reply in (*core.SCENE_DIRECTIONS, core.INCOMING_TEXT):
        feelings.pop(state['player'], None)
    state['emotions'].update(feelings)
    if not texting and town.RICHTER in names and state['player'] == 'rei':
        witnesses = [who for who in state['world']['party'] if town.loop.together(state, who)]
        if witnesses:
            spoken = core.dialogue_craft.spoken_by(data['lines']).get(town.RICHTER)
            if spoken:
                exchange = ((f'Rei said “{reply}”. ' if reply else '') + f'Joseph Richter said to Rei, “{spoken}”')
                state.setdefault('shared_events', []).append(dict(minute=minute, text=exchange, witnesses=witnesses))
    state['turn'] += 1
    groups.sync_contacts(state)
    town.log(state, '; '.join(line['speaker']+': '+line['text'] for line in data['lines']))
