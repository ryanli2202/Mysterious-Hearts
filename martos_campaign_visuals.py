"""Source-bound Martos staging. This module grants no gameplay result.

Room identifiers are travel gates in the present. Historical backgrounds belong
to isolated sessions. Every spoken/prose element retains its unabridged text.
"""

EXECUTIVE = 'syndicate_hq__executive_meeting_room'
OPERATIONS = 'syndicate_hq__cross_branch_operations_room'
LOUNGE = 'syndicate_hq__members_lounge'
SITTING = 'martos_transfer_house__sitting'
DEPARTURE = 'martos_transfer_house__departure'
RECEIVING = 'martos_transfer_house__receiving'
ROOMS = {'executive': EXECUTIVE, 'neutral': SITTING, 'safe_stop': SITTING,
         'kitchen': LOUNGE, 'receiving': RECEIVING}
BACKGROUNDS = {
 EXECUTIVE: 'locations/interiors/syndicate_hq/executive_meeting_room',
 OPERATIONS: 'locations/interiors/syndicate_hq/cross_branch_operations_room',
 LOUNGE: 'locations/interiors/syndicate_hq/members_lounge',
 SITTING: 'locations/campaign/martos/safe_stop',
 DEPARTURE: 'locations/campaign/martos/departure',
 RECEIVING: 'locations/campaign/martos/receipt',
}
CURRENT = {'martos':'martos-selection', 'mavis':'mavis-selection',
 'camila':'camila-selection', 'elias':'elias-selection',
 'sylvanis':'sylvanis-selection', 'crow':'crow-selection',
 'martos-lena':'lena-current', 'martos-sera':'sera-current', 'martos-voss':'voss-current'}
HQ_UNIFORMS = {who:who+'-syndicate' for who in ('martos','mavis','camila','elias','sylvanis')}
HISTORICAL = {
 'MT-F01': {'martos':'martos-service-early','martos-sera':'sera-service','martos-tomas':'tomas-service'},
 'MT-F02': {'martos':'martos-special-forces','martos-sera':'sera-service','martos-tomas':'tomas-service','martos-voss':'voss-service'},
 'MT-F03': {'martos':'martos-special-forces','martos-sera':'sera-service','martos-voss':'voss-service'},
 'MT-F04': {'martos':'martos-special-forces','martos-sera':'sera-service','martos-voss':'voss-service'},
 'MT-F05': {'martos':'martos-special-forces','martos-sera':'sera-refuge','martos-voss':'voss-service'},
 'MT-F06': {'martos':'martos-fugitive','martos-sera':'sera-refuge','crow':'crow-mavis-history'},
 'MT-F07': {'martos':'martos-early-service','martos-sera':'sera-early-service','crow':'crow-mavis-history'},
 'MT-F08': {'martos':'martos-early-service','crow':'crow-mavis-history'},
}
CORE_SHOTS = {
 'CS-MT01': {'scene':'MT-F01','field':'text','index':0,
             'image':'assets/campaigns/martos/core/CS-MT01.png', 'purpose':'Conventional-service evacuation before selection.'},
 'CS-MT02': {'scene':'MT-F03','field':'text','index':0,
             'image':'assets/campaigns/martos/core/CS-MT02.png', 'purpose':'Civilian-facing forced-removal cordon; fixed culpability.'},
 'CS-MT03': {'scene':'MT-F05','field':'text','index':8,
             'image':'assets/campaigns/martos/core/CS-MT03.png', 'purpose':'Limited escape supporting wounded Sera; no universal rescue.'},
 'CS-MT04': {'scene':'MT-F06','field':'text','index':4,
             'image':'assets/campaigns/martos/core/CS-MT04.png', 'purpose':'Recruitment in executive room with concealed Crow.'},
 'CS-MT05': {'scene':'MT-13','field':'briefing','index':0,
             'image':'assets/campaigns/martos/core/CS-MT05.png', 'purpose':'Holding departure line before resolution, receipt or custody.'},
}


def bind(beats, scene, background, portraits, *, room=None, field='text'):
    current_room = room
    for index, beat in enumerate(beats):
        if room:
            current_room = ROOMS.get(beat.get('room'), beat.get('room', current_room))
            beat['room'] = current_room
        beat['background'] = BACKGROUNDS.get(current_room, background)
        speakers = [who for who, _ in beat.get('speeches', [])]
        # No nonspeaking witness is inferred to have heard a separate disclosure.
        visible = ['martos'] + [who for who in speakers if who != 'martos']
        shot_portraits = portraits
        if current_room and current_room.startswith('syndicate_hq__') and beat.get('mode') != 'memory':
            # Present authorised headquarters service uses the accepted masked
            # uniform. Historical visitor/provisional-service art is independent.
            shot_portraits = portraits | HQ_UNIFORMS
        beat['portraits'] = {who:shot_portraits[who] for who in visible if who in shot_portraits}
        source = beat.setdefault('source_id', f'{scene}:{field}:{index:03}')
        source_index = int(source.rsplit(':', 1)[-1])
        selected = next((key for key, item in CORE_SHOTS.items()
                         if source == f"{item['scene']}:{item['field']}:{item['index']:03}"), None)
        shot = source + (':' + selected if selected else ':stage')
        segments = [dict(phase='dialogue', speaker=who, text=text,
                         source_element=source_index, source_id=source, shot_id=shot, core_id=selected)
                    for who,text in beat.get('speeches', [])]
        if beat.get('narration'):
            segments.append(dict(phase='prose', text=beat['narration'], source_element=source_index,
                                 source_id=source, shot_id=shot, core_id=selected))
        for segment in segments:
            segment['background'] = beat['background']
            segment['portraits'] = beat['portraits'].copy()
        beat['stage_segments'] = segments
    return beats


def apply(chapters, memories, disclosures, outcomes):
    hbg = {'MT-F01':'evacuation_hall','MT-F02':'yard','MT-F03':'field_court',
           'MT-F04':'field_court','MT-F05':'field_court','MT-F06':'refuge',
           'MT-F07':'service_sitting','MT-F08':'service_sitting'}
    for key, memory in memories.items():
        cast = HISTORICAL[key]
        background = 'locations/campaign/martos/' + hbg[key]
        bind(memory['text'], key, background, cast)
        bind(memory.get('after_encounter', []), key, background, cast, field='after_encounter')
        # Distinct scene changes remain explicit; later era references are never used.
        if key == 'MT-F01':
            bind(memory['after_encounter'], key, 'locations/campaign/martos/evacuation_hall', cast, field='after_encounter')
            bind(memory['after_encounter'][-1:], key + ':mess', 'locations/campaign/martos/mess', cast, field='after_encounter')
        if key == 'MT-F02':
            bind(memory['text'][5:], key + ':rescue', 'locations/campaign/martos/field_court', cast)
            bind(memory['after_encounter'], key, 'locations/campaign/martos/mess', cast, field='after_encounter')
        if key == 'MT-F04':
            bind(memory['after_encounter'], key, 'locations/campaign/martos/infirmary', cast, field='after_encounter')
        if key == 'MT-F05':
            bind(memory['after_encounter'], key, 'locations/campaign/martos/refuge',
                 cast | {'martos':'martos-fugitive'}, field='after_encounter')
        if key == 'MT-F06':
            # Narrative announces the actual historical authorised visit before Crow speaks.
            bind(memory['text'][4:], key + ':hq', BACKGROUNDS[EXECUTIVE], cast)
        if key == 'MT-F07':
            bind(memory['text'][0:2], key + ':care_authorisation', BACKGROUNDS[EXECUTIVE], cast)
            bind(memory['text'][6:7], key + ':recovery', 'locations/campaign/martos/field_court', cast)
            bind(memory['text'][7:9], key + ':recovery_debrief', BACKGROUNDS[EXECUTIVE], cast)
            bind(memory['text'][8:10], key + ':recovery_boarding', 'locations/campaign/martos/field_court', cast)
            bind(memory['text'][10:12], key + ':training_report', 'locations/campaign/martos/yard', cast)
            bind(memory['text'][12:13], key + ':restriction', BACKGROUNDS[EXECUTIVE], cast)
            bind(memory['text'][13:14], key + ':training', 'locations/campaign/martos/yard', cast)
            bind(memory['text'][14:], key + ':service', BACKGROUNDS[EXECUTIVE], cast)
        if key == 'MT-F08':
            bind(memory['text'][3:], key + ':appointment', BACKGROUNDS[EXECUTIVE], cast)
            memory['text'][-2]['portraits'] = {'martos':'martos-syndicate'}
            for segment in memory['text'][-2]['stage_segments']:
                segment['portraits'] = {'martos':'martos-syndicate'}
    for key, chapter in chapters.items():
        room = EXECUTIVE if key in ('MT-01','MT-07','MT-11') else OPERATIONS if key == 'MT-10' else DEPARTURE if key in ('MT-05','MT-13') else RECEIVING if key == 'MT-14' else SITTING
        for field in ('briefing','operation_intro','aftermath'):
            if field not in chapter:
                continue
            phase_room = room
            if key == 'MT-01' and field != 'briefing': phase_room = SITTING
            if key == 'MT-05' and field == 'aftermath': phase_room = SITTING
            bind(chapter[field], key, BACKGROUNDS[phase_room], CURRENT,
                 room=phase_room, field=field)
    for who, beats in disclosures.items():
        bind(beats, 'MT-disclosure:' + who, BACKGROUNDS[OPERATIONS], CURRENT, room=OPERATIONS)
    for key, beats in outcomes.items():
        room = SITTING if key == 'withdrawal_recovery' else RECEIVING
        bind(beats, 'MT-outcome:' + key, BACKGROUNDS[room], CURRENT, room=room)


def source_manifest(chapters, memories):
    """Text hashes bind shot scope; production/visual acceptance stays separate."""
    import hashlib
    result = []
    for core_id, spec in CORE_SHOTS.items():
        source = (memories if spec['scene'].startswith('MT-F') else chapters)[spec['scene']][spec['field']][spec['index']]
        text = '\n'.join(([source['narration']] if source.get('narration') else []) + [t for _,t in source.get('speeches',[])])
        result.append(dict(id=core_id, core_id=core_id, **spec,
                           scene_id=spec['scene'], beat=spec['index'], anchor_text=text,
                           resolution='pre-resolution', source_id=source['source_id'],
                           source_sha256=hashlib.sha256(text.encode('utf-8')).hexdigest(),
                           asset_acceptance='pending raw and in-app visual inspection'))
    return {'schema_version':1, 'scope':'Source bindings only; not artwork acceptance or release evidence.', 'core_shots':result}
