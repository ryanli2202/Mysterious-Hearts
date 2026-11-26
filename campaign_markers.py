"""Read-only campaign wayfinding, derived from existing mission authorities."""
import copy

MARK='◆'


def targets(state):
    # Existing guard readers initialise their bookkeeping. Keep that entirely
    # inside a disposable projection, never in the live save or access rules.
    s=copy.deepcopy(state)
    import interiors,interior_activities as rooms,campaign_flashbacks as memories
    import organisation_guards as guards
    result=[]
    def add(title,venue,room=None):
        base=interiors.building(venue) if interiors.enabled(s,venue) else venue
        result.append(dict(title=title,building=base,room=room if room in interiors.ROOMS else None))
    player=s.get('player')
    if player=='ivan':
        import ivan_campaigns as route
        if not route.read(s).get('complete'):add(route.chapter(s)['title'],route.destination(s),route.room_target(s))
        return result
    if player=='neo':
        import neo_campaigns as route
        if route.read(s).get('started') and not route.read(s).get('complete'):add(route.chapter(s)['title'],route.destination(s),route.room_target(s))
        return result
    if player=='sylvanis':
        import sylvanis_campaigns as route
        if not route.read(s).get('complete'):add(route.chapter(s)['title'],route.destination(s),route.room_target(s))
        return result
    if player=='takeo':
        import takeo_campaigns as route
        if not route.read(s).get('complete'):add(route.chapter(s)['title'],route.destination(s),route.room_target(s))
        return result
    if player=='camila':
        import camila_campaigns as route
        if not route.read(s).get('complete'):add(route.chapter(s)['title'],route.destination(s),route.room_target(s))
        return result
    if player=='elias':
        import elias_campaigns as route
        if not route.read(s).get('complete'):add(route.chapter(s)['title'],route.destination(s),route.room_target(s))
        return result
    if player=='martos':
        import martos_campaigns as route
        if not route.read(s).get('complete'):add(route.chapter(s)['title'],route.destination(s),route.room_target(s))
        return result
    if player=='mavis':
        import ace_campaigns
        if not ace_campaigns.read(s).get('complete'):
            venue=ace_campaigns.destination(s)
            add(ace_campaigns.chapter(s)['title'],venue,ace_campaigns.room_target(s))
        return result
    active=s.get('post_story',{}).get('active')
    if active:
        import post_story
        spec=post_story.MISSIONS.get(active.get('key'))
        owner='garrett' if active.get('key','').startswith('dragon_') else 'rei'
        if spec and player==owner:
            add(spec['title'],spec['venue'],rooms.POST_STORY.get(active['key']))
            return result
    memory=memories.pending(s)
    if memory:
        venue=memories.venue(s,memory)
        room={'rei_home':'rei_home__art_space','noodle_shop':'noodle_shop__dining_room',
              'glasshouse_lab':'glasshouse_lab__private_review_reunion_room'}.get(venue)
        add(memories.SCENES[memory]['title'],venue,room)
        return result
    if player=='rei':
        import rei_story
        d=s.get('rei_story',{});stage=d.get('stage',0)
        if d.get('complete'):return result
        if stage<len(rei_story.SCENES):
            title,venue,*_=rei_story.SCENES[stage];add(title,venue,rooms.REI.get(stage))
        else:
            if not d.get('hamayashi'):add('Decide the successor’s future','hamayashi_house','hamayashi_house__meeting_room')
            for venues,scope in ((guards.HAMAYASHI if d.get('hamayashi')=='destroy' else (), 'rei:hamayashi'),
                                 (guards.BLACKSTONE if not d.get('richter') else (), 'rei:blackstone')):
                seen=set();remaining=False
                for venue in venues:
                    rows=guards.remaining(s,venue,scope)
                    if rows:
                        remaining=True;base=interiors.building(venue) if interiors.enabled(s,venue) else venue
                        if base not in seen:add('Clear the next mission guard',venue,rows[0].get('room'));seen.add(base)
                if scope=='rei:blackstone' and venues and not remaining:
                    add('Confront Richter','blackstone_command','blackstone_hq__executive_command')
    elif player=='garrett':
        import charles_quest
        step=charles_quest.read(s)['step']
        if step<len(charles_quest.STEPS):
            title,venue,*_=charles_quest.STEPS[step];room=rooms.CHARLES.get(step)
            if step in (6,9):
                remaining=guards.remaining(s,venue,'charles:search')
                if remaining:room=remaining[0].get('room') or room
            add(title,venue,room)
    elif player in ('fox','gordon'):
        import interpol
        step=interpol.objective(s)
        if step:add(step['title'],step['venue'],rooms.interpol_room(step))
    return result


def visible_targets(s):
    import town
    return [t for t in targets(s) if town.hidden.visible_place(copy.deepcopy(s),t['building'])]


def for_building(s,building):
    return [t for t in visible_targets(s) if t['building']==building]


def room_guidance(s):
    """Target labels and adjacent next doors; this never grants door access."""
    import interiors
    current=interiors.room(s);building=interiors.building(s['world']['location'])
    goals=for_building(s,building);doors=set();labels=[];here=False
    for goal in goals:
        room=goal['room']
        if not room:continue
        if current==room:here=True
        else:
            try:
                route=interiors.route(s,room)
                if route:doors.add(route[0])
            except ValueError:continue
        labels.append(goal['title']+' · '+interiors.ROOMS[room].label)
    return tuple(labels),frozenset(doors),here
