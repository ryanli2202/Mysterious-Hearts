"""Production asset bindings and ordered illustrated shot sequences."""
BACKGROUNDS={
 'site_01__briefing_room':'locations/campaign/takeo/kestrel_command',
 'site_02__briefing_room':'locations/site_02_briefing',
 'site_01__operations_office':'locations/campaign/takeo/kestrel_reception',
 **{'takeo_meridian__'+room:'locations/campaign/takeo/meridian_'+room for room in ('entry','command','research','archive')}}
CURRENT={who:who+'-selection' for who in ('takeo','sylvanis','thirteen')}
CURRENT['Keisuke Hachimura']='keisuke-hachimura-selection'
CURRENT.update({'takeo-deputy':'takeo-deputy-current','takeo-opposition':'takeo-opposition'})
HISTORICAL={
 'TK-F01':{'takeo':'takeo-directive','takeo-deputy':'takeo-deputy-young','takeo-medic':'takeo-medic'},
 'TK-F02':{'takeo':'takeo-directive','takeo-deputy':'takeo-deputy-young'},
 'TK-F03':{'takeo':'takeo-onami','takeo-kazama':'takeo-kazama'},
 'TK-F04':{'takeo':'takeo-onami','takeo-researcher':'takeo-researcher'},
 'TK-F05':{'takeo':'takeo-onami','takeo-officer':'takeo-officer'},
 'TK-F06':{'takeo':'takeo-selection','takeo-researcher':'takeo-researcher','takeo-one-child':'takeo-one-child'},
 'TK-F07':{'takeo':'takeo-selection','thirteen':'takeo-thirteen-history'},
 'TK-F08':{'takeo':'takeo-selection','sylvanis':'sylvanis-selection'}}
CORE_SHOTS={key:dict(scene=scene,field=field,index=index,image='assets/campaigns/takeo/core/'+key+'.png') for key,scene,field,index in (
 ('CS-TK01A','TK-F01','text',0),('CS-TK01B','TK-F01','text',1),
 ('CS-TK02A','TK-F03','text',0),('CS-TK02B','TK-F03','text',1),
 ('CS-TK03A','TK-13','briefing',0),('CS-TK03B','TK-13','briefing',1),
 ('CS-TK04A','TK-14','briefing',7),('CS-TK04B','TK-14','briefing',8),
 ('CS-TK05A','TK-13','destroy',0),('CS-TK05B','TK-13','destroy',2))}

def bind(beats,scene,field,room,memory=False):
    import takeo_campaign_content as content
    portraits=HISTORICAL.get(scene,CURRENT) if memory else CURRENT
    for index,beat in enumerate(beats):
        target=beat.get('room',room);beat['room']=target
        beat['background']='locations/campaign/takeo/'+content.MEMORIES[scene]['background'] if memory else BACKGROUNDS.get(target,'locations/campaign/takeo/kestrel_command')
        if memory:beat.update(mode='memory',era=content.MEMORIES[scene]['era'])
        cast=['takeo']+[who for who,_ in beat.get('speeches',[])]
        if memory and scene=='TK-F06' and index in (0,3):cast.append('takeo-one-child')
        beat['portraits']={who:portraits[who] for who in dict.fromkeys(cast) if who in portraits}
        source=f'{scene}:{field}:{index:03}';beat['source_id']=source
        source_field='text' if memory else field
        shot=next((key for key,row in CORE_SHOTS.items() if (row['scene'],row['field'],row['index'])==(scene,source_field,index)),None)
        parts=[dict(phase='dialogue',speaker=who,text=text) for who,text in beat.get('speeches',[])]
        if beat.get('narration'):parts.append(dict(phase='prose',text=beat['narration']))
        for part in parts:part.update(source_id=source,source_element=index,shot_id=source+':shot',core_id=shot,background=beat['background'],portraits=beat['portraits'].copy())
        beat['stage_segments']=parts
    return beats
