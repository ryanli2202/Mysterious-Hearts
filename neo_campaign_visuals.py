"""Exact-age portraits, room paintings and two-shot illustrated sequences."""
from copy import deepcopy
CURRENT={who:who+'-selection' for who in ('neo','alyssa','tyler','daniel','april','garrett')}
CURRENT.update(neo='neo-scene',mariko='mariko-current',soren='neo-soren',**{'tyler-father':'neo-tyler-father','hachimura':'keisuke-hachimura-selection','thirteen':'thirteen-selection'})
HISTORICAL={
 'NE-M01':{'neo':'neo-home12','mariko':'mariko-home12'},
 'NE-M02':{'neo':'neo-school16','tyler':'tyler-school16','daniel':'daniel-school16'},
 'NE-M03':{'neo':'neo-school16','mariko':'mariko-home16'},
 'NE-M04':{'neo':'neo-child10','thirteen':'thirteen-child10','trainee':'neo-trainee10'},
 'NE-M05':{'neo':'neo-child10','mariko':'mariko-raid','takeo':'takeo-selection'},
 'NE-M06':{'neo':'neo-school16','mariko':'mariko-home16'}}
ROOM_ART={
 'neo_mariko__kitchen':'home_kitchen','neo_mariko__living':'home_living','neo_mariko__hall':'home_hall','neo_mariko__bedroom':'home_bedroom','neo_mariko__garden':'home_garden',
 'neo_club__back_room':'club','neo_alfheim__square':'alfheim','neo_alfheim__passage':'alfheim_damaged','neo_refuge__sitting':'refuge','neo_refuge__exit':'refuge_exit','neo_yard__loading':'yard','neo_yard__lane':'yard','neo_transport__boarding':'transport','neo_annex__entry':'annex_entry','neo_annex__records':'annex_records','neo_annex__command':'annex_command','neo_annex__medical':'annex_medical'}
SEQUENCES={'NE01:briefing':('opening',0),'NE-M01:text':('home_memory',0),'NE-M02:text':('school_memory',0),'NE04:briefing':('evacuation',2),'NE08:briefing':('transport',0),'NE-M05:text':('raid_memory',0),'NE12:briefing':('hachimura',0),'NE13:briefing':('formation',0),'NE14:briefing':('ending',0)}
CORE_SHOTS={}
for source,(sequence,start) in SEQUENCES.items():
    for shot in (0,1):
        key='CS-NE-'+sequence+'-'+str(shot+1)
        scene,field=source.split(':');CORE_SHOTS[key]=dict(scene=scene,field=field,index=start+shot,image='assets/campaigns/neo/core/'+key+'.png',sequence=sequence,shot=shot)
for _row in CORE_SHOTS.values():
    if _row['scene'] in ('NE04','NE08','NE12','NE13') and _row['shot']==1:_row.update(field='aftermath',index=0)

for _row in CORE_SHOTS.values():
    if _row['scene']=='NE08':_row.update(field='aftermath',index=_row['shot'])
    if _row['scene']=='NE01':_row['index']+=1

def background(room):
    if room=='neo_home__kitchen_dining':return 'locations/interiors/neo_home/kitchen_dining'
    return 'locations/campaign/neo/'+ROOM_ART.get(room,'refuge')
def bind(beats,scene,field,bg,portraits,room=None,memory=False):
    for index,beat in enumerate(beats):
        if room:beat['room']=room
        beat['background']=bg if bg.startswith('locations/') else 'locations/campaign/neo/'+bg
        if memory:
            beat['mode']='memory';beat['era']=__import__('neo_campaign_content').MEMORIES[scene]['era']
        # A portrait is a participant, never a roster of people mentioned in prose.
        cast=list(dict.fromkeys(['neo',*[who for who,_ in beat.get('speeches',[])]]))
        selected={who:portraits[who] for who in cast if who in portraits}
        beat['portraits']=deepcopy(selected);source=beat.setdefault('source_id',f'{scene}:{field}:{index:03}')
        core=next((key for key,row in CORE_SHOTS.items() if source==f"{row['scene']}:{row['field']}:{row['index']:03}"),None)
        parts=[dict(phase='dialogue',speaker=who,text=text) for who,text in beat.get('speeches',[])]
        if beat.get('narration'):parts.append(dict(phase='prose',text=beat['narration']))
        for part in parts:part.update(source_id=source,source_element=index,shot_id=source+(':'+core if core else ':stage'),core_id=core,background=beat['background'],portraits=deepcopy(selected))
        beat['stage_segments']=parts
    return beats
