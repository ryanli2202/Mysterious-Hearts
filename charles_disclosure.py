"""An eyewitness report advances NPC Garrett's search in this save only."""
LAB = 'glasshouse_lab'

def read(s):
    return s.get('charles_disclosure', {})

def eligible(s):
    return s['player'] != 'garrett' and (bool(read(s)) or s.get('discoveries', {}).get('charles', {}).get('met_in_play', False))

def together(s, who):
    w=s['world']; a=w['cast'][who]; p=w['cast'][s['player']]
    if a['location']!=w['location'] or p['location']!=w['location'] or a.get('journey') or p.get('journey') or a.get('activity')=='Sleep':
        raise ValueError('Speak to '+who.title()+' in person while both of you are awake and present.')
    import groups
    if w.get('party') or w.get('npcs') or groups.hanging_out_with(s)-{who} or any(k not in (who,s['player']) and v['location']==w['location'] and not v.get('journey') for k,v in w['cast'].items()):
        raise ValueError('Find a private moment without other listeners first.')

def act(s):
    if not eligible(s): raise ValueError('Meet Charles at the laboratory before reporting a sighting.')
    d=read(s); stage=d.get('stage',0)
    together(s,'charles' if stage==1 else 'garrett')
    if stage==0:
        text='Garrett stops mid-sentence. “Charles? You saw him yourself?” You describe meeting him in the Glasshouse, without claiming to know why he is there. “Alive, then. Working there does not tell me whether he can leave. Please ask him what we used to measure Mum’s broth. Do not announce that I am looking.” His hope is cautious; he asks for a reply, not a raid.'
        d=s.setdefault('charles_disclosure',dict(stage=0,journal=[],reporter=s['player']))
    elif stage==1:
        if s['world']['location']!=LAB: raise ValueError('Charles receives this request only at the laboratory.')
        text='Charles holds the kettle still. “Dad’s chipped teacup. Garrett always overfilled it.” He seals a note for Garrett and authorises a private evening visit. “Tell him I chose to stay. The rest is a conversation I owe him.” He shares neither his assignment nor Syndicate plans with you.'
    elif stage==2:
        text='Garrett reads the note twice. “He remembers the cup. That sounds like him. It does not excuse the silence.” He accepts the personal invitation for tomorrow evening, alone. “Thank you for bringing this to me. Let me ask my brother the rest.” This grants Garrett visitor access only; it grants you no clearance.'
        d['due']=(s['world']['minute']//1440+1)*1440+20*60
    elif stage==3: raise ValueError('The brothers still need their private evening meeting. Leave the laboratory clear and let story time pass; check back with Garrett afterwards.')
    elif stage==4:
        text='“I saw him,” Garrett says. Relief comes before the anger. “He had reasons. They are his to tell. I told him that keeping me safe did not give him the right to disappear.” He thanks you for bringing evidence instead of rumours. “We have a way to stay in touch now. I am still deciding how much I can forgive.” He will not share Charles’s number or private explanation.'
    else: raise ValueError('Garrett has already thanked you. His brother’s confidence remains private.')
    d['stage']=stage+1;d['journal'].append(text)
    return text

def hold(s):
    d=read(s);w=s['world'];a=w['cast']['garrett'];now=w['minute']
    if d.get('stage')!=3 or now<d['due']:return False
    import scheduled_events,groups,town,world_loop
    if now%1440>=23*60:
        d['due']=(now//1440+1)*1440+20*60;d.pop('started',None);return False
    if now%1440<20*60:return False
    if scheduled_events.active(s,'garrett') or 'garrett' in w.get('party',[]) or 'garrett' in groups.hanging_out_with(s) or town.dating.in_hangout(s,'garrett') or a.get('activity')=='Sleep':return False
    if a.get('journey'):return False
    if a['location']!=LAB:
        world_loop.start_trip(s,'garrett',LAB);return True
    private=w['location']!=LAB and not any(k not in ('garrett','charles') and v['location']==LAB and not v.get('journey') for k,v in w['cast'].items())
    if not private:d.pop('started',None);a['activity']='Waiting for a private family meeting';return True
    d.setdefault('started',now);a['activity']='Private reunion with Charles'
    if now-d['started']>=20:
        d['stage']=4;d['journal'].append('The brothers have met privately. Ask Garrett how he is doing; their conversation is not yours to read.')
    return True

def knowledge(s,who,listeners=()):
    d=read(s)
    if not d or who not in ('garrett','charles'):return ''
    stage=d['stage']; audience=set(listeners)
    if audience and not audience<={d['reporter'],'garrett','charles'}:return 'Keep the private family enquiry confidential with these listeners.'
    if stage>=4:return 'Authoritative continuity: Garrett and Charles met privately in the Glasshouse. Garrett is relieved but hurt by the silence. Thank the eyewitness for helping. Do not disclose Charles’s private number, undercover motive or their private conversation to the reporter. Charles remains in the lab. The search is no longer an unresolved disappearance.'
    return 'Authoritative eyewitness enquiry: Garrett has a firsthand report that Charles is alive at the Glasshouse. '+('The family reply is authenticated and a private visit is pending. ' if stage>=3 else 'Garrett seeks the chipped-teacup family reply before arranging a visit. ')+'Do not claim a reunion, mission disclosure, rescue or death. Respond with cautious hope and concern, not ignorance of the report.'
