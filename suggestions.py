"""On-demand player suggestions; generation never commits a story turn."""
import hashlib
import json
import game_core as core
import memory_store

FIELDS={'main':'choices','personal':'personal_choices','actions':'action_choices'}


def chat(s, target):
    scope,key=target
    return s[{'route':'routes','group':'groups','local':'npc_chats'}[scope]][key]


def members(s,target):
    return chat(s,target)['members'] if target[0]=='group' else [target[1]]


def texting(s,target):
    return target[0]!='local' and chat(s,target).get('channel','text' if target[0]=='route' else 'in_person')=='text'


def ready(s,target):
    c=chat(s,target)
    if target[0]=='route': return bool(c.get('dialogue'))
    if target[0]=='group' and not texting(s,target) and not c.get('open'): return False
    return any(m.get('speaker') not in ('Narrator','Status update') and not m.get('speaker','').endswith('(You)') for m in c.get('history',[]))


def stamp(s,target):
    c=chat(s,target)
    data=[s['player'],s['turn'],target,c.get('history',[])[-4:],len(c.get('history',[])),
          c.get('channel'),c.get('open'),c.get('members'),s['world']['minute'],s['world']['location']]
    return hashlib.sha256(json.dumps(data,sort_keys=True,ensure_ascii=False).encode()).hexdigest()


def visible(c,kind):
    # Older cached choices are retained, but become visible only after a manual request.
    return c.get(FIELDS[kind],[]) if kind in c.get('suggestions_requested',[]) else []


def apply(s,target,kind,expected,lines):
    if stamp(s,target)!=expected or not ready(s,target): return False
    validate(lines, not texting(s,target))
    c=chat(s,target); c[FIELDS[kind]]=lines
    requested=c.setdefault('suggestions_requested',[])
    if kind not in requested: requested.append(kind)
    c['ordered_tones']=True
    if kind=='actions': c['ordered_action_tones']=True
    return True


def validate(lines,spoken=False):
    core.validate_action_choices(lines)
    if len({x.strip().casefold() for x in lines})!=4: raise ValueError('Suggestions must be distinct.')
    if spoken: core.validate_spoken(lines)


def generate(s,target,kind='main'):
    if kind not in FIELDS: raise ValueError('Unknown suggestion type.')
    if not ready(s,target): raise ValueError('Wait for the character response before requesting suggestions.')
    is_text=texting(s,target)
    if kind=='actions' and is_text: raise ValueError('Physical actions are only available in person.')
    c=chat(s,target); people=members(s,target)
    if c.get('guard_session'):
        import guard_dialogue
        r,_=guard_dialogue.active(s,c['local'])
        if kind=='actions': return ['Nod to the guard.', 'Wait beside the visitor area.', 'Step back from the entrance.', 'Indicate the public desk.']
        if kind=='personal': return ['How has your shift been?', 'Is it usually busy here?', 'Thank you for your help.', 'I will let you get back to work.']
        return guard_dialogue.choices(s,r)

    styles=json.loads((core.ROOT/'dialogue_styles.json').read_text(encoding='utf-8'))
    player=core.PLAYERS[s['player']]
    custom_context=__import__('character_identity').audience(s,people)
    background=json.dumps(custom_context,ensure_ascii=False) if custom_context else core.lore.character_tables()[s['player']]['Public life']
    tones=core.choice_tones(s,c if target[0]=='group' else {'members':people})
    guide=(core.ACTION_GUIDE if kind=='actions' else core.PERSONAL_GUIDE if kind=='personal' else core.reply_tone_guide(tones))
    import four_aces
    guide += '\n' + four_aces.business_direction(s['player'], people)
    system=(f'Write exactly four UNSENT suggestions for {player}, addressing the current conversation participants. '
            'Only return choices_speaker and choices from the schema, regardless of the field names in the style guide. '
            'Do not answer as another character, continue the story, or change any game state. '
            'Suggestions are possibilities, never things the player did, felt, knew or promised. '
            'Respect character canon, privacy, family relationships and current boundaries. '
            'Memory records are evidence with explicit certainty and status: beliefs and proposals are not confirmed facts or completed events. '
            'Do not invent shared experiences or rewrite the character response. '
            f'Player voice: {core.playable_cast.voice(s["player"], styles)}\nPlayer public background: '
            +background+'\n'+guide)
    system+='\n'+core.playable_cast.direction(s, people)
    system+='\n'+(core.PHONE_DELIVERY+' Player texting voice: '+core.TEXT_STYLES.get(s['player'],'') if is_text else core.SPOKEN_DELIVERY)
    if not is_text and kind != 'actions':
        system += '\nLet the four optional replies differ in scope: a brief reaction, a plain answer or a longer thought as appropriate. Leave emotional subtext unspoken where it fits. No forced question or offer in each option.'
    system += '\n' + core.social_world.CONTINUITY_DIRECTION
    system += '\n' + core.town.sexuality.direction(s['player'],people)
    romantic_targets=[who for who in people if core.town.romanceable(s,who)]
    system += '\nRomantic suggestion targets permitted by canon and route boundaries: '+json.dumps(romantic_targets)+'. If empty, all four suggestions must be nonromantic, including physical actions.'
    memory_cue=' '.join(people)+' '+c.get('dialogue','')+' '+ ' '.join(
        m.get('text',m.get('content','')) for m in c.get('history',[])[-3:])
    context=dict(participants=people,channel='text' if is_text else 'in_person',
                 recent=c.get('history',[])[-10:],dialogue=c.get('dialogue',''),
                 player_memories=memory_store.packet(s,s['player'],memory_cue,6),
                 current_state=json.loads(core.town.context(s,people[0])))
    context['player_established_familiarity'] = core.social_world.conversation_knowledge(s, s['player'], people)
    date=s.get('date_session')
    if date and date['partner'] in people:
        context['unfinished_date_goals']=[v for k,v in date['goals'].items() if k not in date['done']]
    schema={'type':'object','properties':{'choices_speaker':{'type':'string','enum':[player]},
            'choices':{'type':'array','items':{'type':'string'},'minItems':4,'maxItems':4}},
            'required':['choices_speaker','choices'],'additionalProperties':False}
    for attempt in range(2):
        response=core.request('/api/chat',dict(model=core.MODEL, messages=[{'role':'system','content':system},
                {'role':'user','content':json.dumps(context,ensure_ascii=False)}], format=schema,stream=False,think=False,
                options=dict(temperature=.7 if not attempt else .3,num_ctx=16384,num_predict=700)))
        try:
            data=json.loads(response['message']['content'])
            if data['choices_speaker']!=player: raise ValueError('Wrong suggestion speaker.')
            validate(data['choices'],not is_text)
            recent=[line.get('text',line.get('content','')) for line in c.get('history',[])[-6:]]
            core.check_nickname(core.nickname_limit(s,recent),data['choices'])
            return data['choices']
        except (ValueError,KeyError,TypeError) as exc:
            if attempt: raise ValueError('Could not generate valid suggestions. Your conversation is already saved; try Suggest replies again.') from exc
            system+='\nRepair suggestions: '+str(exc)
