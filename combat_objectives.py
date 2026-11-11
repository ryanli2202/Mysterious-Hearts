"""Alternative encounter goals; campaign victory gates remain authoritative."""


def choices(f):
    if f.get('kind') in ('circle','spar') or f.get('opponent_profile',{}).get('boss') or f.get('campaign_objective'):
        return ['Duel']
    result=['Duel','Survive','Delay','Escape']
    if f.get('ally_resources'): result.append('Rescue ally')
    return result


def select(s,goal):
    import combat,interpol
    f=combat.active(s)
    if not f or f['status']!='active' or f['turn']:
        raise ValueError('Choose an objective before the first exchange.')
    if interpol.crow_story_fight(s,f) or goal not in choices(f):
        raise ValueError('This encounter has an authored objective.')
    f['objective']=goal
    f['log'].append(description(f))


def description(f):
    goal=f.get('objective','Duel')
    return {'Duel':'Objective: defeat the opponent or concede.',
        'Survive':'Objective: remain standing for six exchanges; survival is not a duel victory.',
        'Delay':'Objective: hold attention for four exchanges, causing damage or defending at close range.',
        'Escape':'Objective: reach an arena edge with at least three spaces of separation and no restraint.',
        'Rescue ally':'Objective: keep your ally standing through four exchanges, then both reach the same edge with three spaces of separation. Your ally follows one space each exchange unless restrained.'}[goal]


def success(f):
    if f['player']['health']<=0: return False
    goal=f.get('objective','Duel'); arena=f['arena']; pos=arena['positions']
    clear=pos['player'] in (0,6) and abs(pos['player']-pos['enemy'])>=3 and not f['player'].get('restrained')
    if goal=='Survive': return f['turn']>=6
    if goal=='Delay': return f.get('delay_progress',0)>=4
    if goal=='Escape': return clear
    if goal=='Rescue ally':
        ally=f.get('ally_resources',{})
        return clear and f['turn']>=4 and ally.get('health',0)>0 and not ally.get('restrained') and pos.get('ally',pos['player'])==pos['player']
    return False
