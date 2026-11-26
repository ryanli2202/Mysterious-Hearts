"""Authored Mavis shot bindings; no gameplay or historical knowledge effects.

The released MH-016 reader owns bubbles, prose pages and saved phase cursors.
These bindings are copied into each new immutable conversation snapshot.
"""

HQ = 'locations/interiors/syndicate_hq/cross_branch_operations_room'
EXCHANGE = 'locations/mavis-dispatch-exchange'
CURRENT = {'mavis': 'mavis-selection', 'crow': 'crow-selection',
           'sylvanis': 'sylvanis-selection', 'martos': 'martos-selection',
           'elias': 'elias-selection', 'camila': 'camila-selection',
           'mavis-broker': 'mavis-broker'}


def bind(beats, scene, background, portraits=None, core=None):
    """Bind complete authored exchanges, never infer speech from quotations."""
    for index, beat in enumerate(beats):
        beat['background'] = background
        if portraits is not None:
            # A speaking camera keeps small casts readable at compact sizes.
            speakers = [who for who, _ in beat.get('speeches', [])]
            visible = ['mavis'] + [who for who in speakers if who != 'mavis']
            beat['portraits'] = {who: portraits[who] for who in visible if who in portraits}
        shot = scene + ':' + ':'.join(beat.get('portraits', {}))
        selected = core if index == 0 else None
        if selected:
            shot = scene + ':' + selected
        segments = []
        for who, text in beat.get('speeches', []):
            segments.append(dict(phase='dialogue', speaker=who, text=text,
                                 source_element=index, shot_id=shot, core_id=selected))
        if beat.get('narration'):
            segments.append(dict(phase='prose', text=beat['narration'],
                                 source_element=index, shot_id=shot, core_id=selected))
        beat['stage_segments'] = segments
    return beats


def apply(chapters, memories, disclosures, outcomes):
    historical = {'mavis': 'mavis-age20', 'crow': 'crow-mavis-history',
                  'mavis-broker': 'mavis-broker',
                  'mavis-previous-spade': 'mavis-previous-spade',
                  'sylvanis': 'sylvanis-mavis-history'}
    for key, memory in memories.items():
        cast = historical.copy()
        if key == 'MV-F05':
            cast['mavis'] = 'mavis-early-service'
        background = {'MV-F01': 'locations/mavis-quiet-house-office',
                      'MV-F02': EXCHANGE, 'MV-F03': HQ,
                      'MV-F04': EXCHANGE,
                      'MV-F05': 'locations/glasshouse_lab',
                      'MV-F06': HQ}[key]
        bind(memory['text'], key, background, cast,
             {'MV-F01': 'CS-MV01', 'MV-F02': 'CS-MV02', 'MV-F03': 'CS-MV03'}.get(key))
        if key == 'MV-F04':
            bind(memory['text'][:4], key + ':orders', HQ, cast)
        if memory.get('after_encounter'):
            bind(memory['after_encounter'], key + ':resolved', HQ if key == 'MV-F04' else EXCHANGE, cast)
            if key == 'MV-F04':
                bind(memory['after_encounter'][-1:], key + ':quarters',
                     'locations/mavis-early-service-terrace', {'mavis': 'mavis-age20'})
        # Promotion begins in provisional clothes; the accepted final title is
        # the first shot with the sealed Spade uniform. No early rank is implied.
        if key == 'MV-F06':
            bind(memory['text'][-2:], key + ':accepted', HQ,
                 historical | {'mavis': 'mavis-early-service'})
    for key, chapter in chapters.items():
        destination = chapter['location']
        room = HQ if destination == 'syndicate_hq' else (
            'locations/glasshouse_lab' if destination == 'glasshouse_lab' else EXCHANGE)
        for phase in ('briefing', 'operation_intro', 'aftermath', 'confrontation'):
            if phase not in chapter:
                continue
            background = HQ if phase == 'aftermath' else room
            speakers = {who for beat in chapter[phase] for who, _ in beat.get('speeches', [])}
            if phase == 'briefing' and speakers.intersection({'crow', 'martos', 'elias', 'camila'}):
                background = HQ
            if phase == 'aftermath' and key == 'MV-05':
                background = 'locations/glasshouse_lab'
            if phase == 'confrontation':
                background = 'locations/mavis-dispatch-inner-room'
            # Named campaign-only Broker art has no ordinary-world cast entry.
            cast = None
            if key in ('MV-01', 'MV-04', 'MV-07', 'MV-08', 'MV-11') and phase != 'aftermath':
                cast = CURRENT | {'mavis': 'mavis-syndicate'}
            bind(chapter[phase], key + ':' + phase, background, cast,
                 'CS-MV04' if key == 'MV-11' and phase == 'confrontation' else None)
    for who, beats in disclosures.items():
        bind(beats, 'MV-09:disclosure:' + who, HQ)
    for key, beats in outcomes.items():
        bind(beats, 'MV-12:outcome:' + key, HQ)

