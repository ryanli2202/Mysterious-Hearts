"""Authored criminal standing, gang networks and evidence-based discoveries."""
GANGS = {
    'lantern': dict(name='Lantern Crew', rep=20, jobs=4, kind='Small street crew', venue='downtown'),
    'rail': dict(name='Rail Yard Saints', rep=25, jobs=5, kind='Small neighbourhood gang', venue='market'),
    'purple': dict(name='Purple Skulls', rep=35, jobs=7, kind='Motorcycle gang', venue='downtown'),
    'hamayashi': dict(name='Hamayashi-kai', rep=40, jobs=8, kind='Successor yakuza organisation built from the ashes of the old clan', venue='market'),
    'rojos': dict(name='Los Rojos', rep=45, jobs=9, kind='Cartel', venue='market'),
    'waterfront': dict(name='Waterfront Consortium', rep=50, jobs=10, kind='Criminal consortium', venue='downtown'),
}
STAGES = ((0,'Unknown'),(10,'Small-time criminal'),(20,'Street regular'),(40,'Connected operator'),
          (60,'Underworld name'),(80,'Major criminal figure'),(95,'Underworld power'))
ESTABLISHED = {
    'takeo': (100, 'Takeo Mishima / Human Siege Engine', 'Shinokami'),
    'garrett': (95,'Flaming Prince','Red Dragons'),
    'ivan': (98,'Black and White Joker','Syndicate · Black and White Joker network'),
    'sylvanis': (100,'Crazed Demon / Coloured Joker · most dangerous man on Earth',None),
    'crow': (100,'The Crow / Cardmaster',None),
    'valentina': (90,'Queen of Wind',None),
    'martos': (96,'Ace of Clubs',None), 'elias': (96,'Ace of Hearts',None),
    'camila': (96,'Ace of Diamonds',None), 'mavis': (96,'Ace of Spades',None),
}
GANG_RANKS = ('Associate','Trusted member','Lieutenant','Captain')
GANG_REVIEWS = ((0,0),(3,30),(8,45),(16,65))
REVIEWS = ((0,0),(3,50),(7,60),(12,70),(18,80),(26,90),(38,95),(52,98))


def sync(s,d):
    """One-time additive migration; preserve earned losses after initial seeding."""
    if not d.get('criminal_origin_v2'):
        origin=ESTABLISHED.get(s['player'])
        if origin:
            d['reputation']=max(d['reputation'],origin[0])
            d['established_role']=origin[1]
            if origin[2]:
                d['leadership']=dict(name=origin[2],role='Leader',standing=40,rank=3,established=True)
                if not d['gang']: d['gang']=dict(d['leadership'])
        d['criminal_origin_v2']=True
    d.setdefault('invitations',{})
    import criminal_reputation
    if not d.get('criminal_reputation_v3'):
        if s['player'] in criminal_reputation.SCORES:
            d['reputation'] = max(d['reputation'], criminal_reputation.SCORES[s['player']])
        d['criminal_reputation_v3'] = True
    if s['player'] == 'ivan':
        d['affiliations'] = ['Syndicate', 'Black and White Joker network']
        d['syndicate_role'] = 'Black and White Joker'
        d['story_membership'] = dict(faction='Syndicate', role='Black and White Joker', authority='Senior command · cross-Suit authority')
        if d.get('leadership'): d['leadership']['name'] = 'Black and White Joker network'
        if (d.get('gang') or {}).get('established'): d['gang']['name'] = 'Black and White Joker network'
    d.setdefault('gang_archive',[])
    if s['player'] == 'garrett':
        d['affiliations'] = ['Red Dragons']
        d['story_membership'] = dict(faction='Red Dragons', role='Leader / Flaming Prince',
                                    authority='Established command of the Red Dragons')
    import bubblegram_roles
    bubblegram_roles.sync(s, d)
    if s['player'] in ('fox','gordon'):
        expelled='interpol' in s.get('combat',{}).get('expelled',[])
        d['legal_affiliations']=[] if expelled else ['Interpol']
        d['interpol_role']='Access revoked' if expelled else 'Team 9 commander' if s['player']=='gordon' else 'Licensed vigilante associate'
    d.setdefault('hamayashi_discovery',dict(return_known=False,affiliation_known=False))
    gang=d.get('gang')
    if gang: gang.setdefault('rank',0)
    # Membership already accepted in old saves is retained without retrospective gates.
    if (not d['membership'] and s['player']!='ivan' and s['player'] not in bubblegram_roles.ROLES and d['reputation']>=40 and d['heat']<30
            and (d['completed']>=8 or d.get('leadership')) and gang and gang['standing']>=3):
        for faction,alias in (('Syndicate','@suitrelay'),('Shinokami','@moonrelay')):
            if faction not in d['invitations']:
                d['invitations'][faction]=dict(status='invited',minute=s['world']['minute'],alias=alias)
                d['history'].append(dict(minute=s['world']['minute'],private=True,
                    text=alias+': Your reputation has reached us. Invitation to '+faction+' broker trials received. Three successful trials precede sponsorship.'))


def stage(d):
    return next(label for minimum,label in reversed(STAGES) if d['reputation']>=minimum)


def join(s,key):
    if key in s.get('organisation_guards',{}).get('disabled',[]):
        raise ValueError('This organisation has been dismantled in this story.')
    import job_apps as j
    d=j.ensure(s)
    if key not in GANGS: raise ValueError('Choose a listed gang.')
    if d['gang']: raise ValueError('Leave your current gang before joining another.')
    if d['pending'] or d['membership']: raise ValueError('Finish your assignment; sponsored members cannot switch gangs.')
    spec=GANGS[key]
    if d['reputation']<spec['rep'] or d['completed']<spec['jobs']:
        raise ValueError(f'{spec["name"]} requires reputation {spec["rep"]} and {spec["jobs"]} completed contracts.')
    d['gang']=dict(id=key,name=spec['name'],role='Member',standing=0,rank=0)
    import gang_leaders
    gang_leaders.ensure(s)
    import gang_members
    gang_members.ensure(s)
    if key=='hamayashi': d['hamayashi_affiliated']=True
    if key=='hamayashi' and s['player']=='rei': reveal_hamayashi(s)
    return j.log(s,'Joined '+spec['name']+' as an associate. This affiliation remains private until disclosed.',True)


def leave(s):
    import job_apps as j
    d=j.ensure(s)
    import crime_diplomacy
    if crime_diplomacy.has_obligations(s): raise ValueError('Resolve your organisation’s meetings and deals before leaving.')
    if not d['gang']: raise ValueError('You do not belong to a gang.')
    if d.get('leadership'): raise ValueError('Your established large-gang leadership is a story role and cannot be discarded here.')
    if d['pending'] or d['membership']: raise ValueError('Finish your assignment; sponsorship binds your current gang affiliation.')
    d['gang_archive'].append(dict(d['gang'])); d['gang']=None
    return j.log(s,'Left the gang. Reputation retained; a new crew requires its own standing. Past affiliations remain in your history.',True)


def review_gang(s):
    import job_apps as j
    d=j.ensure(s); g=d['gang']
    if not g: raise ValueError('Join or create a gang first.')
    if g['rank']>=3: raise ValueError('Your gang has reached its current progression ceiling.')
    standing,rep=GANG_REVIEWS[g['rank']+1]
    if g['standing']<standing or d['reputation']<rep: raise ValueError(f'Gang review requires standing {standing} and reputation {rep}.')
    g['rank']+=1
    return j.log(s, g['name']+': '+gang_title(g)+'.',True)


def gang_title(g):
    if g.get('id')=='hamayashi' and g.get('role')=='Leader': return 'Leader · voluntary successor charter'
    if g.get('mission_desk'): return g['role'] + ' · Established mandate'
    if g.get('established'): return 'Established leader · large organisation'
    if g['role']=='Founder': return ('New crew','Established crew','District network','City network')[g.get('rank',0)]+' · Founder'
    return GANG_RANKS[g.get('rank',0)]


def directory(s):
    import four_aces
    import interpol
    # Display operational reputations without mapping them to civilian identities.
    cleared=four_aces.knows_identities(s,s['player'])
    rows=[]
    order = ['sylvanis', 'crow', *sorted((w for w in ESTABLISHED if w not in ('sylvanis','crow')), key=lambda w:-ESTABLISHED[w][0])]
    for who in order:
        rep,alias,gang = ESTABLISHED[who]
        label=alias
        if who in four_aces.CAST and (cleared or interpol.known_identity(s,s['player'],who)): label+=' · '+four_aces.CAST[who]['name']
        rows.append(f'{label} · reputation {rep}'+(' · '+gang if gang else ''))
    return rows


def reveal_hamayashi(s):
    """Explicit evidence shown in person, never omniscient discovery from app use."""
    import job_apps as j
    import town
    d=j.ensure(s); discovery=d['hamayashi_discovery']; player=s['player']
    if player!='rei':
        actors=s['world']['cast']; rei=actors['rei']; actor=actors[player]
        if actor.get('journey') or rei.get('journey') or rei['location']!=s['world']['location'] or actor['location']!=rei['location']:
            raise ValueError('Meet Rei in person before showing him this evidence.')
    affiliated=bool(d.get('hamayashi_affiliated') or (d.get('gang') or {}).get('id')=='hamayashi')
    if discovery['return_known'] and (not affiliated or discovery['affiliation_known']):
        raise ValueError('Rei already knows the evidence you can show him. This setback cannot be repeated.')
    discovery['return_known']=True
    s.setdefault('emotions',{})['rei']='enraged'
    text='Rei learns that a successor Hamayashi-kai has formed from the old clan’s ashes. He is furious that the organisation has returned.'
    if affiliated:
        discovery['affiliation_known']=True
        if player!='rei':
            stats=town.character_stats(s,'rei')
            stats['trust']=max(0,stats.get('trust',0)-40)
            stats['closeness']=max(0,stats.get('closeness',0)-30)
            text+=' He also sees proof of your affiliation. Trust −40; closeness −30. Leaving later does not erase what he learned.'
    discovery['minute']=s['world']['minute']
    import memory_store
    memory_store.add(s,source='hamayashi-discovery:'+str(affiliated),text=text,owners=list(dict.fromkeys([player,'rei'])),minute=s['world']['minute'],importance=5)
    return j.log(s,text,True)


def context(s,who):
    d=s.get('job_apps',{}); found=d.get('hamayashi_discovery',{})
    if who not in ('rei',s['player']): return {}
    if who=='rei' and not found.get('return_known'):
        return {'Hamayashi boundary':'You are unaware of the successor Hamayashi-kai. Private player app activity cannot reveal its return or their affiliation. Your old clan history remains unchanged.'}
    if who=='rei':
        return {'Hamayashi discovery':'You saw evidence of the successor clan and reacted with anger. '+
                ('You also discovered the protagonist’s affiliation, which seriously damaged your relationship. Do not treat a casual apology or their leaving as automatic forgiveness. ' if found.get('affiliation_known') else 'You have no evidence of the protagonist’s affiliation. ')+
                'This discovery is private; do not broadcast family history or invent surviving original members.'}
    return {}
