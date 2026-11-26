"""Exact-era, source-bound backgrounds, transparent portraits and core sequences."""
BACKGROUNDS={
 'syndicate_hq__executive_meeting_room':'locations/interiors/syndicate_hq/executive_meeting_room',
 'camila_meridian__receiving':'locations/campaign/camila/receiving',
 'camila_meridian__sitting':'locations/campaign/camila/sitting',
 'camila_meridian__loading':'locations/campaign/camila/loading'}
CURRENT={'camila':'camila-selection','crow':'crow-selection','camila-mara':'camila-mara-current','camila-inez':'camila-inez','camila-ansel':'camila-ansel',**{who:who+'-selection' for who in ('mavis','martos','elias')}}
HISTORICAL={
 'CA-F01':{'camila':'camila-child7','camila-elena':'camila-elena','camila-pilar':'camila-pilar','crow':'crow-mavis-history'},
 'CA-F02':{'camila':'camila-child7','camila-mara':'camila-mara-young','crow':'crow-mavis-history'},
 'CA-F03':{'camila':'camila-child11','camila-mara':'camila-mara-young','crow':'crow-mavis-history'},
 'CA-F04':{'camila':'camila-teen16','camila-mara':'camila-mara-young','crow':'crow-mavis-history'},
 'CA-F05':{'camila':'camila-young-adult','camila-mara':'camila-mara-current','crow':'crow-mavis-history'},
 'CA-F06':{'camila':'camila-young-adult','crow':'crow-mavis-history'},
 'CA-F07':{'camila':'camila-young-adult','crow':'crow-mavis-history'},
 'CA-F08':{'camila':'camila-young-adult','camila-inez':'camila-inez','crow':'crow-mavis-history'}}
CORE_SHOTS={key:dict(scene=scene,field=field,index=index,image='assets/campaigns/camila/core/'+key+'.png') for key,scene,field,index in (
 ('CS-CA01','CA-F01','text',4),('CS-CA02','CA-F02','text',8),('CS-CA03','CA-F04','text',5),('CS-CA04','CA-F07','text',0),('CS-CA05','CA-13','briefing',0))}

def bind(beats,scene,field,background,portraits,room=None,memory=False):
    active_room=room
    for index,beat in enumerate(beats):
        active_room=beat.get('room',active_room)
        if active_room:beat['room']=active_room
        beat.setdefault('background',BACKGROUNDS.get(active_room,background))
        if memory:beat['mode']='memory'
        cast=['camila']+[who for who,_ in beat.get('speeches',[]) if who!='camila'];style=portraits.copy()
        if active_room and (active_room.startswith('syndicate_hq__') or active_room=='camila_meridian__loading') and not memory:style.update({who:who+'-syndicate' for who in ('camila','mavis','martos','elias')})
        beat['portraits']={who:style[who] for who in dict.fromkeys(cast) if who in style}
        if beat.get('camila_costume'):beat['portraits']['camila']=beat['camila_costume']
        source=beat.setdefault('source_id',f'{scene}:{field}:{index:03}')
        core=next((key for key,row in CORE_SHOTS.items() if source==f"{row['scene']}:{row['field']}:{row['index']:03}"),None)
        parts=[dict(phase='dialogue',speaker=who,text=text) for who,text in beat.get('speeches',[])]
        if beat.get('narration'):parts.append(dict(phase='prose',text=beat['narration']))
        for part in parts:part.update(source_id=source,source_element=index,shot_id=source+(':'+core if core else ':stage'),core_id=core,background=beat['background'],portraits=beat['portraits'].copy())
        beat['stage_segments']=parts
    return beats

def apply(chapters,memories):
    for key,spec in memories.items():
        bind(spec['text'],key,'text','locations/campaign/camila/'+spec['background'],HISTORICAL[key],memory=True)
        for beat in spec['text']:beat['era']=spec['era']
        bind(spec['after_encounter'],key,'after_encounter',BACKGROUNDS['camila_meridian__receiving'],CURRENT,room='camila_meridian__receiving')
    for key,spec in chapters.items():
        for field in ('briefing','aftermath'):bind(spec[field],key,field,BACKGROUNDS[spec['room']],CURRENT,room=spec['room'])
