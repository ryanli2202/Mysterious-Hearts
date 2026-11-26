"""Versioned, offline reading phases over immutable campaign snapshots.

The action cursor still indexes the saved authoritative beats. Presentation
cursors never commit story actions, including when loading legacy snapshots.
"""
import copy
import re

VERSION=2


def bubble_prose(source):
    """Omit plain attribution already conveyed by a labelled bubble.

    Only touch prose paired with explicit speech in the same source element.
    Tone, timing, action and reported speech remain authored narration.
    Source snapshots themselves are never rewritten.
    """
    groups={}
    for index,part in enumerate(source):groups.setdefault(part.get('source_element'),[]).append((index,part))
    rendered={}
    for group in groups.values():
        speakers={p.get('speaker') for _,p in group if p['phase']=='dialogue' and p.get('speaker')}
        if not speakers:continue
        subjects={'he','she','they'}
        for speaker in speakers:
            subjects.add(speaker);subjects.add(speaker.split()[0])
            if not speaker.lower().startswith('the '):subjects.add('the '+speaker)
            subjects.update({'gordon':{'the officer'},'member':{'someone'}}.get(speaker.lower(),set()))
        subject='(?:'+'|'.join(re.escape(s) for s in sorted(subjects,key=len,reverse=True))+')'
        tag=re.compile(r'(^\s*|(?<=[.!?])\s+)(?:then\s+)?'+subject+r'\s+(?:said|asked|replied|answered)\s*[.,:]\s*',re.I)
        for index,part in group:
            if part['phase']!='prose':continue
            text=part['text'];cleaned=tag.sub(lambda m:m.group(1),text)
            if cleaned!=text:
                cleaned=cleaned.strip()
                if cleaned:cleaned=cleaned[0].upper()+cleaned[1:]
                rendered[index]=cleaned
    return rendered


def present_cast(s,beat):
    """Freeze physical attendance; a quoted letter never summons its author."""
    import interiors
    people=interiors.occupants(s,interiors.room(s)) if interiors.enabled(s) else [
        who for who,actor in s['world']['cast'].items()
        if actor.get('location')==s['world']['location'] and not actor.get('journey') and actor.get('activity')!='Sleep']
    people=set(people)|set(s['world'].get('npcs',[]))|{s['player']}
    speakers=[u.get('speaker') for u in units(beat,s['player'])]
    return list(dict.fromkeys([s['player']]+[who for who in speakers if who in people]))


def passages(text, limit=240):
    """Short logical lines; do not treat initials/abbreviations as full stops."""
    lines=re.split(r'\n\s*\n',text)
    result=[]
    for paragraph in lines:
        protected=re.sub(r'\b(?:Mr|Mrs|Ms|Dr|Prof|St|Jr|Sr|[A-Z])\.',
                         lambda m:m.group().replace('.','\ufff0'),paragraph.strip())
        protected=re.sub(r'\b(?:e\.g\.|i\.e\.)',lambda m:m.group().replace('.','\ufff0'),protected)
        sentences=[s.replace('\ufff0','.') for s in re.split(r'(?<=[!?])\s+|(?<=[.])\s+(?=[“"A-Z])',protected)]
        current=''
        for sentence in sentences:
            if current and len(current)+len(sentence)>limit:
                result.append(current);current=''
            # A long sentence can wrap and scroll; it is never truncated.
            current+=(('\n' if current else '')+sentence)
        if current:result.append(current)
    return result


def units(beat, player='Player', *, omit_tags=True):
    """Explicit authored speech is never harvested from quotation marks."""
    result=[]
    source=beat.get('stage_segments')
    if source is not None and beat.get('gm_narration') and not beat.get('presentation_archive'):
        source=list(source)+[dict(phase='prose',text=beat['gm_narration'],source_element='optional-description')]
    if source is None:
        source=[]
        if not beat.get('prose'):
            if beat.get('player'):source.append(dict(phase='dialogue',speaker=player,text=beat['player']))
            source.extend(dict(phase='dialogue',speaker=who,text=text) for who,text in beat.get('speeches',[]))
        text=beat.get('gm_narration') or beat.get('narration','')
        if text:source.append(dict(phase='prose',text=text))
    # Within each authored source element, play the complete exchange before
    # its associated attribution/action prose. The immutable source spans stay
    # in manuscript order for fidelity validation and old snapshot compatibility.
    indexed=list(enumerate(source))
    if beat.get('stage_segments') is not None:
        ordered=[];group=[];previous=object()
        for entry in indexed:
            key=entry[1].get('source_element',entry[0])
            if group and key!=previous:
                ordered.extend(sorted(group,key=lambda e:e[1]['phase']!='dialogue'));group=[]
            group.append(entry);previous=key
        ordered.extend(sorted(group,key=lambda e:e[1]['phase']!='dialogue'))
        indexed=ordered
    cleaned=bubble_prose(source) if omit_tags else {}
    for index,segment in indexed:
        for page,text in enumerate(passages(cleaned.get(index,segment['text']))):
            result.append(dict(segment=index,page=page,text=text,phase=segment['phase'],
                               speaker=segment.get('speaker'),shot_id=segment.get('shot_id',beat.get('shot_id') or
                               str(beat.get('scene_id') or beat.get('title') or 'scene')+':'+beat.get('mode','present')),
                               core_id=segment.get('core_id'),**{k:copy.deepcopy(segment[k]) for k in ('background','portraits') if k in segment}))
    return result or [dict(segment=0,page=0,text='',phase='prose',speaker=None,
                           shot_id=beat.get('shot_id') or beat.get('scene_id') or 'scene',core_id=None)]


def position(d):
    beat=d['beats'][d['cursor']]
    pages=units(beat,d.get('player','Player'))
    state=d.setdefault('presentation',dict(version=VERSION,beat=d['cursor'],unit=0))
    if state.get('version',1)<VERSION and state.get('beat')==d['cursor']:
        # Preserve the old reading position by source segment/page. If its tag
        # vanished, resume at the next surviving unit, never skip an action.
        old=units(beat,d.get('player','Player'),omit_tags=False)
        old_index=max(0,min(state.get('unit',0),len(old)-1))
        order={(u['segment'],u['page']):i for i,u in enumerate(old)}
        state['unit']=next((i for i,u in enumerate(pages) if order.get((u['segment'],u['page']),-1)>=old_index),len(pages)-1)
    state['version']=VERSION
    if state.get('beat')!=d['cursor']:
        state.update(beat=d['cursor'],unit=0)
    state['unit']=max(0,min(state.get('unit',0),len(pages)-1))
    unit=pages[state['unit']]
    state.update(phase=unit['phase'],segment=unit['segment'],page=unit['page'],shot_id=unit['shot_id'],
                 visual_mode='core_image' if unit.get('core_id') else 'composed_scene',core_id=unit.get('core_id'))
    return unit,state['unit'],len(pages)


def advance(s, delta):
    import campaign_dialogue
    d=s.get('campaign_dialogue')
    if not d:raise ValueError('No scripted conversation.')
    _,index,total=position(d)
    if delta<0:
        if index:d['presentation']['unit']-=1
        elif d['cursor']:
            d['cursor']-=1
            d['presentation'].update(beat=d['cursor'],unit=len(units(d['beats'][d['cursor']],d['player']))-1)
    elif index<total-1:
        d['presentation']['unit']+=1
    else:
        campaign_dialogue.next_line(s)
    if s.get('campaign_dialogue') is d:position(d)


def archive(d):
    """Flatten copies only; history navigation cannot mutate action snapshots."""
    result=[]
    for b in d.get('beats',[]):
        for u in units(b,d.get('player','Player')):
            parts=b.get('stage_segments',[])
            source=parts[u['segment']] if 0<=u['segment']<len(parts) else {}
            segment={k:copy.deepcopy(source[k]) for k in
                     ('source_element','source_start','source_end','fox_voice_when','fixed_voice') if k in source}
            segment.update(voice_source_text=source.get('voice_source_text',source.get('text',u['text'])),
                           phase=u['phase'],text=u['text'],speaker=u['speaker'],shot_id=u['shot_id'],core_id=u.get('core_id'))
            segment.update({k:copy.deepcopy(u[k]) for k in ('background','portraits') if k in u})
            result.append(copy.deepcopy(b)|dict(presentation_archive=True,stage_segments=[segment]))
    return result
