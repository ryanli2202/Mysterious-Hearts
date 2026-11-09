"""Additive, source-backed memory ledger. Original save fields remain untouched."""
import hashlib
import json
import re
import copy

STOP = set('about after again also been could does from have just like more that them then there these they this want what when where which with would your'.split())


def terms(text):
    return sorted({w for w in re.findall(r"[\w']+", text.casefold()) if len(w) > 2 and w not in STOP})


def identity(source):
    return hashlib.sha256(source.encode('utf-8')).hexdigest()[:24]


def ensure(s):
    return s.setdefault('memory_store', dict(version=1, records={}, cursors={}, owners={}, topics={}, revisions=0))


def add(s, *, source, text, owners, kind='experience', subjects=(), minute=None,
        location=None, status='recorded', certainty='observed', importance=1, supersedes=None, slot=None):
    db = ensure(s); rid = identity(source)
    if rid in db['records']: return rid
    if not isinstance(text, str) or not text.strip(): return None
    record = dict(id=rid, source=source, text=text, owners=sorted(set(owners)), kind=kind,
                  subjects=sorted(set(subjects)), minute=minute, location=location,
                  status=status, certainty=certainty, importance=importance,
                  supersedes=supersedes, slot=slot, tokens=terms(text))
    db['records'][rid] = record
    for who in record['owners']: db['owners'].setdefault(who, []).append(rid)
    for word in record['tokens']: db['topics'].setdefault(word, []).append(rid)
    db['revisions'] += 1
    return rid


def correct(s, rid, text, source, owners=None):
    """Explicit, auditable correction; never broaden the original audience implicitly."""
    old = ensure(s)['records'][rid]
    allowed = old['owners'] if owners is None else sorted(set(owners).intersection(old['owners']))
    return add(s, source=source, text=text, owners=allowed, kind=old['kind'], subjects=old['subjects'],
               minute=s['world']['minute'], certainty='corrected', importance=old['importance'], supersedes=rid)


def utterance(s, source, text, speaker, owners, minute, location=None, importance=1):
    if not text: return
    add(s, source=source, text=f'{speaker}: {text}', owners=owners, subjects=[speaker], minute=minute,
        location=location, certainty='quoted speech',importance=importance)
    import personal_details
    for field, value in personal_details.extract(text).items():
        slot = 'profile:'+field
        previous = next((r['id'] for r in reversed(list(ensure(s)['records'].values()))
                         if r.get('slot') == slot and r['subjects'] == [speaker]), None)
        rid = add(s, source=source+':detail:'+field, text=f'{speaker} said: {text}', owners=owners,
                  subjects=[speaker], kind='fact', minute=minute, certainty='self-reported',
                  importance=3, slot=slot, supersedes=previous)
        ensure(s)['records'][rid]['profile_field'] = field
        ensure(s)['records'][rid]['profile_value'] = value
    # Keep reported preferences and promises as claims, never silently turn speech into world facts.
    plain=text.replace('’',"'")
    hedged=bool(re.search(r'\b(?:i think|i suspect|i heard|apparently|maybe)\b',plain,re.I))
    if not hedged and re.search(r"\b(?:my favou?rite|i (?:love|hate|prefer|enjoy)|i am allergic|i'm allergic)\b", plain, re.I):
        preference=re.search(r'\bmy favou?rite ([\w ]{1,40}?) (?:is|are)\b',plain,re.I)
        slot='preference:'+preference[1].strip().casefold() if preference else None
        previous=None
        if slot:
            previous=next((r['id'] for r in reversed(list(ensure(s)['records'].values()))
                           if r.get('slot')==slot and r['subjects']==[speaker]),None)
        add(s, source=source+':preference', text=f'{speaker} said: {text}', owners=owners,
            kind='fact', subjects=[speaker], minute=minute, certainty='self-reported', importance=3,slot=slot,supersedes=previous)
    if re.search(r"\b(?:i promise|i will|i'll|we agreed|let['’]s|shall we)\b", plain, re.I):
        proposed = bool(re.search(r"let['’]s|shall we|\?",text,re.I))
        add(s, source=source+':commitment', text=f'{speaker} said: {text}', owners=owners,
            kind='commitment', subjects=[speaker], minute=minute,
            status='proposed' if proposed else 'unresolved statement', certainty='quoted; completion unconfirmed', importance=4)
    if hedged:
        add(s, source=source+':belief', text=f'{speaker} said: {text}', owners=owners,
            kind='belief', subjects=[speaker], minute=minute, certainty='unverified claim', importance=2)


def open_commitments(s, owners):
    """Latest commitment versions known by every specified participant."""
    records=ensure(s)['records']; audience=set(owners)
    visible={rid:r for rid,r in records.items() if audience.issubset(r['owners'])}
    superseded=set()
    for r in visible.values():
        previous=r.get('supersedes')
        while previous in records and previous not in superseded:
            superseded.add(previous); previous=records[previous].get('supersedes')
    return [r for rid,r in visible.items() if rid not in superseded and r['kind']=='commitment'
            and r['status'] not in ('fulfilled','completed','cancelled','reported_fulfilled')]


def report_commitment(s, rid, status, evidence, speaker, listener, source):
    """Record an explicit report heard in this exchange, never infer physical completion."""
    if status not in ('agreed','reported_fulfilled','cancelled'): raise ValueError('Invalid commitment update.')
    old=next((r for r in open_commitments(s,[speaker,listener]) if r['id']==rid),None)
    if old is None: return None
    return add(s,source=source,text=old['text']+' Update from '+speaker+': '+evidence,
        owners=[speaker,listener],kind='commitment',subjects=old['subjects'],minute=s['world']['minute'],
        status=status,certainty='explicit reported update; physical completion not independently verified',
        importance=4,supersedes=rid)


def sync(s):
    """Incrementally index append-only histories; preserve every original and summary revision."""
    import game_core as core
    db=ensure(s); player=s['player']
    def new_rows(key, rows):
        start=db['cursors'].get(key,0)
        if start > len(rows): start=0
        db['cursors'][key]=len(rows)
        return enumerate(rows[start:],start)
    for who, route in s.get('routes',{}).items():
        owners=[player,who]
        for i,line in new_rows('route:'+who,route.get('history',[])):
            src=f'route:{who}:{i}'; text=line.get('content',''); minute=line.get('minute')
            if line.get('role')=='assistant':
                try: data=json.loads(text)
                except (ValueError,TypeError): data=None
                if not isinstance(data,dict):
                    add(s,source=src,text=text,owners=owners,subjects=[who,player],kind='legacy_summary',
                        minute=minute,certainty='unparsed historical text; verify before treating as fact')
                    continue
                moment=data.get('bond_moments',{}).get(who,'none') if isinstance(data.get('bond_moments',{}),dict) else 'none'
                utterance(s,src,data.get('dialogue',''),who,owners,minute,importance=4 if moment!='none' else 1)
                if data.get('memory') and not data.get('suggestions_deferred'):
                    add(s,source=src+':summary',text=data['memory'],owners=owners,subjects=[player,who],
                        kind='legacy_summary',minute=minute,certainty='historical model summary; verify against source')
            elif line.get('role')=='user':
                if line.get('message_id') is not None: continue  # Indexed individually when actually read.
                if text not in (*core.SCENE_DIRECTIONS,core.INCOMING_TEXT): utterance(s,src,text,player,owners,minute)
            elif line.get('role')=='status':
                add(s,source=src,text=text,owners=owners,subjects=[player,who],minute=minute,certainty='saved status')
        summary=route.get('memory','')
        if summary and summary != 'Source-backed memories are stored separately.':
            add(s,source='summary:'+who+':'+identity(summary),text=summary,owners=owners,
                subjects=[who,player],kind='legacy_summary',certainty='historical model summary; verify against source')
    for prefix, collection in [('group',s.get('groups',{})),('local',s.get('npc_chats',{}))]:
        for key,chat in collection.items():
            members=chat.get('members',[key]); owners=[player,*members]
            names={core.CONTACTS.get(w,(w,))[0]:w for w in members}
            for i,line in new_rows(prefix+':'+key,chat.get('history',[])):
                if line.get('message_id') is not None: continue
                speaker=line.get('speaker',''); text=line.get('text',''); src=f'{prefix}:{key}:{i}'
                if speaker in ('Narrator','Status update'):
                    add(s,source=src,text=text,owners=owners,subjects=members,minute=line.get('minute'),
                        certainty='narration' if speaker=='Narrator' else 'saved status')
                else:
                    speaker=player if speaker.endswith('(You)') else names.get(speaker,speaker)
                    utterance(s,src,text,speaker,owners,line.get('minute'))
    for i,e in new_rows('shared_events',s.get('shared_events',[])):
        add(s,source=f'shared_events:{i}',text=e['text'],owners=e.get('witnesses',[]),
            subjects=e.get('witnesses',[]),minute=e.get('minute'),importance=4)
    for i,episode in new_rows('hangout_journal',s.get('hangout_journal',[])):
        owners=[player,*episode.get('members',[])]
        for j,line in enumerate(episode.get('history',[])):
            add(s,source=f'hangout_journal:{i}:{j}',text=line.get('speaker','')+': '+line.get('text',''),
                owners=owners,subjects=owners,minute=line.get('minute',episode.get('started')),
                location=episode.get('location'),certainty='archived hangout')
    for who, notes in s.get('profile_notes',{}).items():
        for i,n in new_rows('notes:'+who,notes):
            add(s,source=f'profile_notes:{who}:{i}',text=f"{n['source']} said: {n['quote']}",
                owners=n.get('owners', [player,n['source']]),subjects=[who],kind='fact' if n['source']==who else 'belief',
                minute=n.get('minute'),certainty='self-reported' if n['source']==who else 'reported by another person',importance=3)
    for who,r in {**s.get('friendships',{}),**s.get('relationships',{})}.items():
        for kind,stamp in r.get('firsts',{}).items():
            add(s,source=f'first:{who}:{kind}:{stamp}',text=f'{kind}: {stamp}',owners=[player,who],
                subjects=[player,who],kind='fact',certainty='game milestone',importance=5)
        for text in r.get('milestones',[]):
            add(s,source=f'milestone:{who}:'+identity(text),text=text,owners=[player,who],subjects=[who,player],
                kind='experience',certainty='game milestone',importance=4)
    for trip in s.get('world',{}).get('journeys',[]):
        if trip.get('status')!='arrived': continue
        owners=[trip['driver'],*trip.get('passengers',[])]
        add(s,source='journey:'+identity(json.dumps(trip,sort_keys=True)),
            text='Shared a drive to '+core.town.LOCATIONS[trip['destination']]+' with '+', '.join(owners)+'.',
            owners=owners,subjects=owners,minute=trip.get('arrives'),location=trip['destination'],importance=2)
    for name in ('log','home_journal'):
        for text in s.get('world',{}).get(name,[]):
            add(s,source='world:'+name+':'+identity(text),text=text,owners=[player],certainty='player journal')
    for pair,bond in s.get('bond_details',{}).items():
        for text in bond.get('events',[]):
            add(s,source='bond:'+pair+':'+identity(text),text=text,owners=pair.split(':'),subjects=pair.split(':'),certainty='relationship event',importance=3)
    for who,plan in s.get('meeting_plans',{}).items():
        plan_record(s,who,plan,'agreed')
    for e in s.get('scheduled_events',[]):
        # Historical appointments without attendance evidence remain explicitly unknown.
        phase='cancelled' if e.get('cancelled') else e.get('memory_phase','planned' if e['start']>s['world']['minute'] else 'attendance unknown')
        event_record(s,e,phase)
    return db


def plan_record(s,who,plan,status,previous=None,owners=None):
    source=f"plan:{who}:{plan.get('agreed_at',s['world']['minute'])}:{status}:"+identity(plan['details'])
    return add(s,source=source,text=f"Meeting with {who}: {plan['details']} ({status}; do not assume completion).",
               owners=owners or [s['player'],who],subjects=[who,s['player']],kind='commitment',status=status,
               minute=plan.get('agreed_at'),certainty='recorded agreement',importance=5,supersedes=previous)


def event_record(s,e,phase):
    import town
    import story_calendar
    owners=[s['player'],*e['guests']]
    attendees=e.get('attendees',[])
    start=e['start']; end=e['end']
    text=(f"{e['title']} at {town.LOCATIONS[e['venue']]} · {phase}. "
          f"Scheduled {story_calendar.story_date(start)} {start%1440//60:02}:{start%60:02}–{end%1440//60:02}:{end%60:02}. "
          f"Invited: {', '.join(e['guests'])}.")
    if phase in ('attended','completed','missed'):
        text+=' Recorded attendees: '+(', '.join(attendees) or 'none')+'.'
    if phase=='missed': text+=' The player did not attend; this does not mean the guests missed it.'
    if e.get('source') == 'syndicate_council':
        import syndicate_council
        text = 'Private Syndicate council. ' + syndicate_council.details(e)
    # Invited people know the plan; actual experiences are only owned by attendees.
    if phase=='attended': owners=attendees
    rid = add(s,source=f"event:{e['id']}:{phase}:"+identity(','.join(attendees)),text=text,
               owners=owners,subjects=owners,kind='commitment' if phase=='planned' else 'experience',
               minute=s['world']['minute'] if phase!='planned' else e.get('created_minute'),location=e['venue'],
               status=phase,certainty='game event' if phase!='attendance unknown' else 'legacy attendance unknown',importance=5,
               supersedes=e.get('memory_record'))
    e['memory_record']=rid
    return rid


def retrieve(s,who,cue='',limit=8):
    # Prompt construction is read-only, even when a legacy state has not been indexed yet.
    # Copy index containers, not every transcript or immutable memory record.
    view=dict(s)
    view['scheduled_events']=copy.deepcopy(s.get('scheduled_events',[]))
    if 'memory_store' in s:
        original=s['memory_store']
        view['memory_store']={**original,'records':dict(original['records']),'cursors':dict(original['cursors']),
                              'owners':{k:list(v) for k,v in original['owners'].items()},
                              'topics':{k:list(v) for k,v in original['topics'].items()}}
    db=sync(view); accessible=set(db['owners'].get(who,[]))
    superseded={db['records'][r]['supersedes'] for r in accessible if db['records'][r].get('supersedes')}
    for rid in list(superseded):
        seen=set()
        while rid in db['records'] and rid not in seen:
            seen.add(rid); superseded.add(rid)
            rid=db['records'][rid].get('supersedes')
    for rid in list(superseded):
        old=db['records'].get(rid,{})
        if old.get('slot') and old['source'].endswith(':preference'):
            superseded.add(identity(old['source'].removesuffix(':preference')))
    accessible-=superseded
    words=terms(cue); scores={}
    for word in words:
        for rid in db['topics'].get(word,[]):
            if rid in accessible: scores[rid]=scores.get(rid,0)+1
    def score(rid):
        r=db['records'][rid]
        return (scores.get(rid,0)*6+r['importance'],r.get('minute') if isinstance(r.get('minute'),int) else -1)
    mandatory=[rid for rid in accessible if (db['records'][rid]['kind']=='commitment' and db['records'][rid]['status'] in ('agreed','planned','proposed','unresolved statement'))
               or db['records'][rid]['certainty']=='game milestone']
    chosen=sorted(mandatory,key=score,reverse=True)[:max(2,limit//2)]
    ranked=sorted(accessible,key=score,reverse=True)
    # Include a recent exchange without sacrificing relevant older facts.
    recent=sorted((r for r in accessible if db['records'][r]['certainty']=='quoted speech'),
                  key=lambda r:db['records'][r].get('minute') or -1,reverse=True)[:1]
    for rid in [*recent,*ranked]:
        if rid not in chosen: chosen.append(rid)
        if len(chosen)>=limit: break
    return [db['records'][rid] for rid in chosen[:limit]]


def packet(s,who,cue='',limit=8):
    import story_calendar
    records=retrieve(s,who,cue,limit)
    def stamp(r):
        m=r.get('minute')
        return f'{story_calendar.story_date(m)} {m%1440//60:02}:{m%60:02}' if isinstance(m,int) and m>=0 else 'Earlier; date not recorded'
    return [f"[{r['id']} | {stamp(r)} | {r['kind']} | {r['certainty']} | {r['status']}] {r['text'][:1800]}" for r in records]


def summary(s,who,cue=''):
    """Disposable extractive view, never overwrites historical summaries or evidence."""
    rows=retrieve(s,who,cue,6)
    return dict(text='\n'.join(r['text'][:350] for r in rows),sources=[r['id'] for r in rows])
