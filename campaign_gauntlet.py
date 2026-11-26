"""Explicit, saved next-wave handoff after the authoritative combat resolver.

Mission scope/slot receipts remain owned by organisation_guards. Ordinary patrols
never chain. Existing fresh per-fight resources are intentionally unchanged.
"""
import copy


def next_wave(s, encounter):
    import organisation_guards as guards, interiors
    scope=encounter['scope'];venue=encounter['venue']
    if scope in ('rei:blackstone','rei:hamayashi','charles:search'):
        venues=guards.BLACKSTONE if scope=='rei:blackstone' else guards.HAMAYASHI if scope=='rei:hamayashi' else (venue,)
        for place in venues:
            if not interiors.same_building(place,venue):continue
            rows=guards.remaining(s,place,scope)
            if rows:
                row=rows[0]
                return dict(scope=scope,venue=place,room=row.get('room'),slot=row['id'])
        if scope=='rei:blackstone' and not s.get('rei_story',{}).get('richter'):
            return dict(scope=scope,venue='blackstone_command',room='blackstone_hq__executive_command' if interiors.enabled(s,venue) else None,
                        handler='richter',kind='scene')
        if scope=='charles:search' and __import__('charles_quest').read(s)['step']==9 and 'charles' not in guards.data(s)['victories'].get('charles:finale',[]):
            return dict(scope=scope,venue=venue,room='glasshouse_lab__private_review_reunion_room' if interiors.enabled(s,venue) else None,
                        handler='charles_finale',kind='scene')
    elif scope.startswith('interpol:'):
        import interpol
        a=interpol.read(s).get('active');step=interpol.objective(s)
        current_scope=('interpol:'+a['key']+':'+str(interpol.read(s)['files'].get(a['key'],{}).get('step',0))+
                       (':'+str(a['started']) if a.get('repeatable') else '')) if a else None
        if a and scope==current_scope and step and step['kind']=='combat' and interiors.same_building(step['venue'],venue):
            return dict(scope=scope,venue=venue,room=encounter.get('room'),handler='interpol')
    elif scope.startswith('garrett:protection:'):
        import garrett_chapters, charles_quest
        index=charles_quest.read(s)['step']
        if index in garrett_chapters.BATTLES and scope==garrett_chapters.scope(index) and garrett_chapters.remaining(s,index):
            return dict(scope=scope,venue=venue,room=encounter.get('room'),handler='charles')
    elif scope.startswith('post-story:'):
        import post_story
        a=post_story.read(s).get('active')
        if a and a['scope']==scope:
            return dict(scope=scope,venue=venue,room=encounter.get('room'),handler='post' if post_story.remaining(s) else 'post_finish',
                        kind='fight' if post_story.remaining(s) else 'outcome')
    return None


def after_close(s, fight, encounter):
    if not encounter or not fight.get('result','').startswith('Victory'):return
    # The same mission can be resumed by its ordinary at-location controls.
    # Replace an older Continue receipt instead of stranding it ahead of the
    # final aftermath in the saved epilogue queue.
    queue=s.setdefault('campaign_epilogues',[])
    queue[:]=[e for e in queue if not (e.get('action')=='campaign_gauntlet.continue_wave'
              and e.get('args') and e['args'][0].get('scope')==encounter['scope'])]
    plan=next_wave(s,encounter)
    if not plan:return
    import town,interiors
    label=interiors.ROOMS[plan['room']].label if plan.get('room') in interiors.ROOMS else town.location_name(s,plan['venue'])
    text=('The detail is cleared. Continue to secure the civilian’s departure and record this mission’s outcome.' if plan.get('kind')=='outcome' else
          'This post is cleared. Continue to the authored confrontation at '+label+'. Read the scene before the next fight begins.' if plan.get('kind')=='scene' else
          'This post is cleared. The next required opponent is at '+label+'.\n\nContinue through the building when you are ready. The next fight uses the same recovery rules as a separately started encounter.')
    lines=[__import__('campaign_prose').page(text,title='Secure departure' if plan.get('kind')=='outcome' else 'Continue the building',gauntlet=True)]
    s.setdefault('campaign_epilogues',[]).append(dict(lines=lines,venue=s['world']['location'],
        action='campaign_gauntlet.continue_wave',args=[copy.deepcopy(encounter),plan]))


def continue_wave(s, encounter, expected):
    import combat,interiors,organisation_guards as guards
    combat.guard(s)
    if not interiors.same_building(s['world']['location'],encounter['venue']):
        raise ValueError('Return to this building to continue the gauntlet.')
    current=next_wave(s,encounter)
    if current!=expected:raise ValueError('This wave is no longer available. Return to the current objective.')
    # Preflight all doors on a copy before mutating real room or attendance state.
    def enter(state):
        target=current.get('room')
        if target and interiors.enabled(state,current['venue']):
            for door in interiors.route(state,target):interiors.move(state,door)
        handler=current.get('handler')
        if handler in ('interpol','richter','charles_finale'):
            import campaign_dialogue,campaign_flashbacks
            memory=campaign_flashbacks.pending(state)
            if memory:
                campaign_flashbacks.start(state,memory)
                state.setdefault('campaign_epilogues',[]).append(dict(lines=[__import__('campaign_prose').page('The required memory is complete. Continue the building when you are ready.',title='Continue the building',gauntlet=True)],
                    venue=state['world']['location'],action='campaign_gauntlet.continue_wave',args=[copy.deepcopy(encounter),copy.deepcopy(expected)]))
            else:campaign_dialogue.begin(state,{'interpol':'interpol.advance','richter':'rei_story.confront','charles_finale':'charles_quest.security_action'}[handler])
            return 'Read the next authored scene before the encounter begins.'
        if handler=='charles':return __import__('charles_quest').security_action(state)
        if handler=='post':return __import__('post_story').fight(state)
        if handler=='post_finish':return __import__('post_story').finish(state)
        if current['scope'].startswith('rei:'):
            __import__('rei_story').check(state,solo=True)
        elif current['scope']=='charles:search':
            __import__('charles_quest').guard(state,current['venue'])
        return guards.begin(state,current['venue'],current['scope'])
    enter(copy.deepcopy(s))
    return enter(s)


def withdraw(s):
    d=s.get('campaign_dialogue')
    if not d or d.get('action')!='campaign_gauntlet.continue_wave':
        raise ValueError('There is no pending building continuation.')
    # Completed posts stay in their authoritative mission scope. No action/reward
    # is replayed and the next ordinary objective can resume the remaining posts.
    s['campaign_dialogue']=None


def prune(s):
    queue=s.get('campaign_epilogues',[])
    queue[:]=[e for e in queue if e.get('action')!='campaign_gauntlet.continue_wave'
              or (e.get('args') and next_wave(s,e['args'][0])==e['args'][1])]
