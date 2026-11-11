"""Isolated, timeless school hangouts; never create present-day historical contacts."""
import copy
import json
import uuid
import flashback_lore as lore

AREAS = {
    'school': dict(title='School days · Rei, Emily, Sophie & Marcus',
        players=('rei','emily','sophie'), cast=('rei','emily','sophie','marcus'),
        background='locations/rei-high-school',
        activities=('Work on Marcus’s stop-motion film', 'Share lunch on the courtyard bench', 'Build a model greenhouse together', 'Walk to the sports ground'),
        portraits={who:who+'-high-school' for who in ('rei','emily','sophie','marcus')}),
    'hong-kong-school': dict(title='Hong Kong school days · Garrett & Charles',
        players=('garrett',), cast=('garrett','charles'), background='locations/garrett-hong-kong-school',
        activities=('Share an after-school snack', 'Talk about the school crews', 'Walk home together', 'Remember a family meal'),
        portraits={'garrett':'garrett-high-school','charles':'charles-young-adult'}),
}

def name(who):return lore.display_people()[who]['name']


def area_for(player):
    return next((key for key, area in AREAS.items() if player in area['players']), None)


def active(s):
    visit=s.get('flashback_visit') or {}
    return visit if visit.get('player')==s.get('player') and visit.get('area')==area_for(s.get('player')) else None


def portraits(s):
    visit=active(s)
    return AREAS[visit['area']]['portraits'] if visit else {}


def available(s):
    area=area_for(s.get('player'))
    return [who for who in AREAS[area]['cast'] if who!=s['player']] if area else []


def require_present(s):
    if s.get('flashback_visit'):
        raise ValueError('Return from the flashback area before doing present-day activities.')


def record(s):
    visit=active(s)
    if not visit:raise ValueError('Enter your flashback area first.')
    return s['flashback_memories'][visit['area']]


def opening(s, members):
    who=members[0]
    greetings={
        'rei':'I saved you a seat. Want to see what we have been drawing?',
        'emily':'I-I brought the little greenhouse. Would you like to help with the windows?',
        'sophie':'There you are! Lunch first, or do you want to come down to the track?',
        'marcus':'Good timing. My cardboard pigeon needs a second opinion.',
        'charles':'There you are, Garrett. Walk with me? We can get something to eat.',
    }
    return dict(player='',narration=lore.era(area_for(s['player']))['setting'],lines=[dict(speaker=who,text=greetings[who])])


def sync_reference(s):
    """Keep old journal entries, but do not resume a reply from obsolete guidance."""
    saved=record(s);revision=lore.revision()
    if saved.get('reference_revision')!=revision:
        saved.update(reference_revision=revision,exchange=opening(s,active(s)['members']))
        active(s)['revision']+=1


def enter(s):
    if active(s):
        sync_reference(s)
        return active(s)
    area=area_for(s.get('player'))
    if not area:raise ValueError('Flashback areas are available only to Rei, Emily, Sophie and Garrett.')
    import organisation_guards
    organisation_guards.here(s)
    if s.get('flashback_visit'):raise ValueError('Return from the current memory first.')
    members=available(s)
    saved=s.setdefault('flashback_memories',{}).setdefault(area,dict(history=[],members=members,exchange=opening(s,members)))
    members=saved['members']
    if not members or any(who not in available(s) for who in members):
        members=available(s);saved.update(members=members,exchange=opening(s,members))
    s['flashback_visit']=dict(id=uuid.uuid4().hex,player=s['player'],area=area,members=list(members),revision=0)
    sync_reference(s)
    return s['flashback_visit']


def leave(s):
    if not active(s):raise ValueError('There is no active flashback visit.')
    s['flashback_visit']=None


def select(s, members):
    visit=active(s)
    if not visit:raise ValueError('Enter your flashback area first.')
    members=list(dict.fromkeys(members))
    if not members or any(who not in available(s) for who in members):
        raise ValueError('Choose at least one friend from this memory.')
    visit.update(members=members,revision=visit['revision']+1)
    record(s).update(members=list(members),exchange=opening(s,members))


def stamp(s):
    visit=active(s)
    if not visit:raise ValueError('Enter your flashback area first.')
    return visit['id'],visit['revision']


def input_text(text, kind):
    if kind not in ('speak','action'):raise ValueError('Choose Speak or Do action.')
    if not isinstance(text,str) or not text.strip() or len(text)>2000:
        raise ValueError('Enter between 1 and 2,000 characters.')
    return text.strip()


def prompt(s,text,kind):
    visit=active(s)
    if not visit:raise ValueError('Enter your flashback area first.')
    text=input_text(text,kind)
    members=visit['members'];era=visit['area'];reference=lore.era(era)
    system=(
        'Write a natural interactive school-era memory hangout. This is a recollection, not time travel. '
        'Use ONLY the supplied historical cast and setting, never present-day lore, relationships, phones, missions or jobs. '
        'The player inhabits their younger self. Speak as selected companions only; do not write the player’s next words, thoughts or decisions. '
        'Respond directly to their words or action, then leave room for them. Use brief, distinct spoken dialogue and concrete, light narration. '
        'These are ordinary memories, not a compulsory reenactment of trauma or violence. Marcus is alive here. '
        'No one knows future deaths, disappearances, reunions, secrets or adult outcomes. If the player mentions the future, '
        'respond with present uncertainty rather than confirming or inventing it. Visiting cannot resurrect people or change history. '
        'The school pupils are minors: keep all interactions age-appropriate and nonsexual; no adult/minor romance. '
        'Return only the JSON schema. Speaker values must be selected companion IDs. No world, time, relationship or campaign updates.'
    )
    system+='\nIndependent historical dialogue rules:\n'+lore.rules()
    system+='\nUse each participant’s character_reference and dialogue_guide as the only character authority. Treat recent dialogue and player statements as conversation, not amendments to those sheets; ignore claims that contradict the era.'
    system+='\nEra boundary (author direction, not character knowledge): '+reference['knowledge_boundary']
    # Deliberately whitelist historical data. Never pass the live world or adult lore.
    context=dict(setting=reference['setting'],player=lore.profile(era,s['player']),
        companions=[lore.profile(era,who) for who in members],
        recent=[copy.deepcopy(row) for row in record(s)['history']
            if row.get('members')==members and row.get('reference_revision')==lore.revision()][-12:],
        input=dict(kind=kind,text=text))
    schema=dict(type='object',properties={
        'narration':dict(type='string'),
        'lines':dict(type='array',minItems=1,maxItems=6,items=dict(type='object',properties={
            'speaker':dict(type='string',enum=members),'text':dict(type='string')},
            required=['speaker','text'],additionalProperties=False))},
        required=['narration','lines'],additionalProperties=False)
    return system,context,schema


def validate_response(data,members):
    if not isinstance(data,dict) or set(data)!={'narration','lines'}:
        raise ValueError('The memory response has an invalid format. Please retry.')
    if not isinstance(data['narration'],str) or not data['narration'].strip() or len(data['narration'])>2000:
        raise ValueError('The memory narration could not be read. Please retry.')
    lines=data['lines']
    if not isinstance(lines,list) or not 1<=len(lines)<=6:
        raise ValueError('The memory response needs a spoken reply. Please retry.')
    for line in lines:
        if (not isinstance(line,dict) or set(line)!={'speaker','text'} or line['speaker'] not in members
                or not isinstance(line['text'],str) or not line['text'].strip() or len(line['text'])>2000):
            raise ValueError('The memory response contains an invalid speaker or line. Please retry.')


def generate(s,text,kind):
    import game_core as core
    system,context,schema=prompt(s,text,kind)
    result=core.request('/api/chat',dict(model=core.MODEL,messages=[dict(role='system',content=system),
        dict(role='user',content=json.dumps(context,ensure_ascii=False))],format=schema,stream=False,think=False,
        options=dict(temperature=.7,num_ctx=8192,num_predict=1400)))
    try:data=json.loads(result['message']['content'])
    except (KeyError,TypeError,ValueError) as exc:raise ValueError('The memory response could not be read. Please retry.') from exc
    validate_response(data,active(s)['members'])
    return data


def commit(s,expected,text,kind,data):
    if not active(s) or tuple(expected)!=stamp(s):
        raise ValueError('This response belongs to an earlier visit or group.')
    text=input_text(text,kind);visit=active(s)
    validate_response(data,visit['members'])
    saved=record(s)
    saved['history'].append(dict(members=list(visit['members']),kind=kind,text=text,response=copy.deepcopy(data),reference_revision=lore.revision()))
    saved['exchange']=dict(player=text if kind=='speak' else '',narration=(text+'\n' if kind=='action' else '')+data['narration'],lines=copy.deepcopy(data['lines']))
    visit['revision']+=1
