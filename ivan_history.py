"""Eight scoped historical periods; unresolved ages fail closed before entry."""
import copy
import uuid
AREA='ivan-network-history'
PERIODS=(
 ('IV-H04','Between the Counts','IV-M04','Conclave years','training',None),
 ('IV-H04B','What Excellence Earned','IV-M04','Conclave years','training',None),
 ('IV-H05','The Waiting Room · eighteen','IV-M05','Handover','handover',18),
 ('IV-H06','A Choice Shared','IV-M06','Network origins','founding',None),
 ('IV-H07','Before the First Burst','IV-M07','Network origins','athletics',None),
 ('IV-H08','Terms at the Ring','IV-M08','Network origins','kickboxing',None),
 ('IV-H09','A Safe Interval','IV-M09','Network origins','refuge',None),
 ('IV-H10','A Dangerous Agreement','IV-M10','Network origins','backroom',None),
)
PROTECTED=('player','world','combat','interiors','inventory','money','relationships','friendships','phone_numbers','discoveries','job_apps','crime_diplomacy','interpol','ivan_campaign','groups','routes','npc_chats','criminal_dynamics','scheduled_events','hangout_journal')
ROOM_TEXT={
 'H1':'The waiting-room chair faces a closed door. The trade is fixed history; the quiet interval does not offer a different destination.',
 'H2':'The supervised corridor leads only between the waiting room and permitted practice room. No office, file or future recruit is accessible.',
 'H3':'The designated practice room is clear. A wrist turn can be repeated harmlessly here; it teaches no new present-day move and changes no resource.',
}

def reason(s,period):
    row=next((row for row in PERIODS if row[0]==period),None)
    if not row:return 'Unknown historical period.'
    if s.get('player')!='ivan':return 'This history belongs to Ivan.'
    if row[2] not in s.get('ivan_campaign',{}).get('memories',[]):return 'Complete the corresponding chapter history first.'
    if row[5] is None:return 'Historical age/reference data is unassigned. Conversation and entry remain locked; no present-day fallback.'
    import flashback_lore
    try:
        record=flashback_lore.profile('ivan_handover18','ivan')
        if record['age']!=18:return 'The age-eighteen reference is invalid.'
    except ValueError:return 'The independent age-eighteen reference/voice pair is missing.'
    return None

def enter(s,period='IV-H05'):
    import combat,flashback_visits,flashback_lore
    if reason(s,period):raise ValueError(reason(s,period))
    if flashback_visits.active(s):return flashback_visits.active(s)
    if s.get('flashback_visit') or s.get('campaign_dialogue') or combat.active(s) or combat.recovering(s):raise ValueError('Finish the current scene, visit or combat and recover first.')
    if s.get('ivan_campaign',{}).get('pending_return'):raise ValueError('Read the return to the present before optional visits.')
    snapshot={key:copy.deepcopy(s[key]) for key in PROTECTED if key in s}
    visit=dict(id=uuid.uuid4().hex,player='ivan',area=AREA,members=[],revision=0,room='H1',period=period,suspended=snapshot,protected_absent=[key for key in PROTECTED if key not in s])
    s['flashback_visit']=visit
    root=s.setdefault('flashback_memories',{}).setdefault(AREA,dict(history=[],members=[],exchange={}))
    root.setdefault('period_records',{}).setdefault(period,dict(history=[],members=[],exchange={}))
    record=flashback_visits.record(s);record.update(reference_revision=flashback_lore.revision(),exchange=opening(s))
    return visit

def opening(s):
    return dict(player='',narration='Handover · Ivan, eighteen · '+ROOM_TEXT[(s.get('flashback_visit') or {}).get('room','H1')],lines=[])

def leave(s):
    visit=s.get('flashback_visit') or {}
    snapshot=visit.get('suspended')
    if visit.get('area')!=AREA or not isinstance(snapshot,dict) or 'world' not in snapshot:raise ValueError('The suspended present is invalid; preserve the save and use its last valid copy.')
    for key in PROTECTED:
        if key in snapshot:s[key]=copy.deepcopy(snapshot[key])
        elif key in visit.get('protected_absent',[]):s.pop(key,None)
    s['flashback_visit']=None

def inspect(s,text='Observe the room'):
    import flashback_visits
    visit=flashback_visits.active(s)
    if not visit or visit['area']!=AREA:raise ValueError('Enter this historical interval first.')
    narration=ROOM_TEXT[visit['room']]
    entry=dict(kind='action',text=text,narration=narration,lines=[],members=[],period=visit['period'],room=visit['room'],reference_revision=__import__('flashback_lore').revision())
    record=flashback_visits.record(s);record['history'].append(entry);record['exchange']=dict(player='',narration=narration,lines=[])
    visit['revision']+=1
    return narration
