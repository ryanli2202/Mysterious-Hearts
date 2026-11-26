"""Reusable exact-era staging plus selected illustrated core paintings."""
from copy import deepcopy
CURRENT={'sylvanis':'sylvanis-syndicate','crow':'crow-selection','charles':'charles-selection-v2','takeo':'takeo-selection'}
BACKGROUNDS={
 'glasshouse_lab__private_review_reunion_room':'locations/interiors/glasshouse_lab/private_review_reunion_room',
 'glasshouse_lab__laboratory_workroom':'locations/glasshouse_lab',
 'syndicate_hq__executive_meeting_room':'locations/interiors/syndicate_hq/executive_meeting_room',
 'site_01__briefing_room':'locations/campaign/sylvanis/takeo_meeting',
 **{'sylvanis_arena__'+k:'locations/campaign/sylvanis/'+v for k,v in [('entry','arena_entry'),('control','arena_control'),('ring','arena')]} }
HISTORICAL={key:{'sylvanis':'sylvanis-early',**extra} for key,extra in {
 'SY-M01':{},'SY-M02':{},'SY-M03':{'kaden':'sylvanis-kaden','conspirator':'sylvanis-conspirator'},'SY-M04':{'kaden':'sylvanis-kaden','conspirator':'sylvanis-conspirator'},'SY-M05':{'kaden':'sylvanis-kaden','conspirator':'sylvanis-conspirator'},'SY-M06':{'crow':'crow-mavis-history'},'SY-M07':{},'SY-M08':{'parent-one':'sylvanis-parent-one','parent-two':'sylvanis-parent-two'},'SY-M09':{'charles':'sylvanis-charles-early'},'SY-M10':{'takeo':'takeo-selection'}}.items()}
for key in ('SY-M06','SY-M07','SY-M08','SY-M09','SY-M10'):HISTORICAL[key]['sylvanis']='sylvanis-research'
HISTORICAL['SY-M07']['martos']='martos-early-service'
# Populated from explicit manuscript anchors by apply(), including CS-SY08.
CORE_SHOTS={}
def background(room):return BACKGROUNDS.get(room,'locations/campaign/sylvanis/arena')
def bind(beats,scene,field,bg,portraits,room=None,memory=False):
    current=room
    for index,beat in enumerate(beats):
        current=beat.get('room',current)
        if current:beat['room']=current
        beat.setdefault('background',background(current) if current else bg)
        if memory:beat['mode']='memory'
        cast=list(dict.fromkeys(['sylvanis',*[who for who,_ in beat.get('speeches',[])]]))
        selected={who:portraits[who] for who in cast if who in portraits}
        if not memory and current and current.startswith('glasshouse_lab__'):selected['sylvanis']='sylvanis-selection'
        beat['portraits']=deepcopy(selected)
        source=beat.setdefault('source_id',f'{scene}:{field}:{index:03}')
        # Explicit authored tags survive expansion, inserted responses and rebinds.
        core=beat.get('core_id')
        parts=[dict(phase='dialogue',speaker=who,text=text) for who,text in beat.get('speeches',[])]
        if beat.get('narration'):parts.append(dict(phase='prose',text=beat['narration']))
        for part in parts:part.update(source_id=source,source_element=index,shot_id=source+(':'+core if core else ':stage'),core_id=core,background=beat['background'],portraits=deepcopy(selected))
        beat['stage_segments']=parts
    return beats
def apply(chapters,memories):
    CORE_SHOTS.clear()
    for collection in (chapters,memories):
        for scene,spec in collection.items():
            for field in ('text','briefing','aftermath'):
                for index,beat in enumerate(spec.get(field,[])):
                    if beat.get('core_id'):
                        key=beat['core_id']
                        if key in CORE_SHOTS:raise ValueError('Duplicate Sylvanis core shot: '+key)
                        CORE_SHOTS[key]=dict(scene=scene,field=field,index=index,image='assets/campaigns/sylvanis/core/'+key+'.png')
    for key,spec in memories.items():
        bind(spec['text'],key,'text','locations/campaign/sylvanis/'+spec['background'],HISTORICAL[key],memory=True)
        for beat in spec['text']:beat['era']=spec['era']
        bind(spec['after_encounter'],key,'after_encounter',BACKGROUNDS['glasshouse_lab__private_review_reunion_room'],CURRENT,room='glasshouse_lab__private_review_reunion_room')
    for key,spec in chapters.items():
        for field in ('briefing','aftermath'):bind(spec[field],key,field,background(spec['room']),CURRENT,room=spec['room'])
