"""Stable Elias source bindings and exact-era theatre/family staging."""
EXECUTIVE='syndicate_hq__executive_meeting_room'
OPERATIONS='syndicate_hq__cross_branch_operations_room'
LOUNGE='syndicate_hq__members_lounge'
STAGE='elias_theatre__stage'
DRESSING='elias_theatre__dressing'
RECEIVING='elias_theatre__receiving'
LOADING='elias_theatre__loading'
BACKGROUNDS={EXECUTIVE:'locations/interiors/syndicate_hq/executive_meeting_room',OPERATIONS:'locations/interiors/syndicate_hq/cross_branch_operations_room',LOUNGE:'locations/interiors/syndicate_hq/members_lounge',STAGE:'locations/campaign/elias/stage_current',DRESSING:'locations/campaign/elias/dressing_current',RECEIVING:'locations/campaign/elias/receiving',LOADING:'locations/campaign/elias/loading'}
CURRENT={'elias':'elias-selection','elias-johanna':'johanna-current','elias-konrad':'konrad-current','elias-lotte':'lotte-current','crow':'crow-selection',**{who:who+'-selection' for who in ('mavis','martos','camila','sylvanis')}}
HISTORICAL={
 'EL-F01':{'elias':'elias-childhood','elias-konrad':'konrad-childhood','elias-anja':'anja-childhood'},
 'EL-F02':{'elias':'elias-actor','elias-johanna':'johanna-young','elias-konrad':'konrad-history','elias-lotte':'lotte-history'},
 'EL-F03':{'elias':'elias-actor','elias-johanna':'johanna-young','elias-konrad':'konrad-history'},
 'EL-F04':{'elias':'elias-actor','elias-johanna':'johanna-young','elias-konrad':'konrad-history'},
 'EL-F05':{'elias':'elias-actor','crow':'crow-mavis-history'},
 'EL-F06':{'elias':'elias-actor','elias-johanna':'johanna-young','elias-konrad':'konrad-history','crow':'crow-mavis-history'},
 'EL-F07':{'elias':'elias-early-service','crow':'crow-mavis-history'},
 'EL-F08':{'elias':'elias-early-service','crow':'crow-mavis-history','elias-lotte':'lotte-history'},
}
CORE_SHOTS={key:dict(scene=scene,field=field,index=index,image='assets/campaigns/elias/core/'+key+'.png') for key,scene,field,index in (
 ('CS-EL01','EL-F01','text',0),('CS-EL02','EL-F04','after_encounter',0),('CS-EL03','EL-F05','text',4),('CS-EL04','EL-F05','after_encounter',0),('CS-EL05','EL-F06','text',2),('CS-EL06','EL-13','briefing',0))}

def bind(beats,scene,field,background,portraits,room=None,memory=False):
    active_room=room
    for index,beat in enumerate(beats):
        active_room=beat.get('room',active_room)
        if active_room:beat['room']=active_room
        beat.setdefault('background',BACKGROUNDS.get(active_room,background))
        if memory:beat['mode']='memory'
        cast=['elias']+[who for who,_ in beat.get('speeches',[]) if who!='elias']
        style=portraits.copy()
        if active_room and active_room.startswith('syndicate_hq__') and not memory:style.update({who:who+'-syndicate' for who in ('elias','mavis','martos','camila','sylvanis')})
        beat['portraits']={who:style[who] for who in dict.fromkeys(cast) if who in style}
        source=beat.setdefault('source_id',f'{scene}:{field}:{index:03}')
        core=next((key for key,record in CORE_SHOTS.items() if source==f"{record['scene']}:{record['field']}:{record['index']:03}"),None)
        parts=[dict(phase='dialogue',speaker=who,text=text) for who,text in beat.get('speeches',[])]
        if beat.get('narration'):parts.append(dict(phase='prose',text=beat['narration']))
        for part in parts:part.update(source_id=source,source_element=index,shot_id=source+(':'+core if core else ':stage'),core_id=core,background=beat['background'],portraits=beat['portraits'].copy())
        beat['stage_segments']=parts
    return beats

def apply(chapters,memories):
    backgrounds={'EL-F01':'music','EL-F02':'stage','EL-F03':'family_meeting','EL-F04':'courtyard','EL-F05':'family_meeting','EL-F06':'family_meeting','EL-F07':'family_meeting','EL-F08':'dressing'}
    for key,spec in memories.items():
        for field in ('text','after_encounter'):bind(spec.get(field,[]),key,field,'locations/campaign/elias/'+backgrounds[key],HISTORICAL[key],memory=True)
    # Historical site cuts and returns are explicit source-bound staging. A
    # historical background never pretends to move the live present actor.
    for key,start,background in (('EL-F02',4,'family_meeting'),('EL-F08',0,'family_meeting'),('EL-F08',4,'dressing')):
        end=4 if key=='EL-F08' and start==0 else len(memories[key]['text'])
        for beat in memories[key]['text'][start:end]:
            beat['background']='locations/campaign/elias/'+background
            for segment in beat['stage_segments']:segment['background']=beat['background']
    recovery=memories['EL-F04']['after_encounter'][3]
    recovery['background']='locations/campaign/elias/family_meeting'
    for segment in recovery['stage_segments']:segment['background']=recovery['background']
    returns={'EL-F01':(0,STAGE),'EL-F02':(0,RECEIVING),'EL-F03':(3,RECEIVING),'EL-F04':(4,LOADING),'EL-F05':(3,DRESSING),'EL-F06':(0,RECEIVING),'EL-F07':(0,RECEIVING),'EL-F08':(0,DRESSING)}
    for key,(index,room) in returns.items():
        for beat in memories[key]['after_encounter'][index:]:
            beat['mode']='present';beat['room']=room;beat['background']=BACKGROUNDS[room]
        bind(memories[key]['after_encounter'][index:],key,'after_encounter',BACKGROUNDS[room],CURRENT,room=room)
    for key,spec in chapters.items():
        for field in ('briefing','aftermath'):bind(spec.get(field,[]),key,field,BACKGROUNDS[spec['room']],CURRENT,room=spec['room'])
    if 'EL-09' in chapters:
        coda=chapters['EL-09']['aftermath'][0]
        coda.update(mode='memory',era='elias_appointment25',room=EXECUTIVE,background=BACKGROUNDS[EXECUTIVE])
        bind([coda],'EL-09','aftermath',BACKGROUNDS[EXECUTIVE],{'elias':'elias-syndicate','crow':'crow-mavis-history'},memory=True)
