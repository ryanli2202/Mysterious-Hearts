"""Part 2 combat states. All counters live in saves, never in UI callbacks."""
import copy


def trait(p,name):
    ability=p.get('trait') or {}
    return ability.get('effect')!='custom' and name.casefold() in ability.get('name','').casefold()


def ensure(r):
    for key,value in dict(protocol_ready=0,protocol_left=0,protocol_used=False,protocol_strain=0,
                          war_momentum=0,war_last='',observations={},last_exchange='',
                          soul_damage=0,misanthropy=False,misanthropy_used=False,endurance_left=0,endurance_debt=0,
                          tranquility=False,channel='',control_immunity=0).items():
        r.setdefault(key,copy.deepcopy(value))


def readiness_required(r):
    return 3 if r['health']<r['max_health']*.6 else 4


def protocol_choice(s,f,side,p):
    r=f[side]
    return protocol_available(s,f,side,p) and (r['stamina']>=55 or r['health']<r['max_health']*.6)


def protocol_available(s,f,side,p):
    r=f[side]; ensure(r)
    who=s['player'] if side=='player' else f['opponent']
    spent=s.get('combat',{}).get('protocol_spent',{}).get(who)
    recovered=(side=='enemy' and isinstance(spent,dict) and s['world']['minute']>=spent.get('recover_at',float('inf')))
    return (trait(p,'Shinigami Protocol') and r['protocol_ready']>=readiness_required(r) and not r['protocol_used']
            and (not spent or recovered)
            and r['stamina']>=20 and r['health']>0)


def activate_protocol(s,side='player'):
    import combat
    from combat_profiles import profile
    f=combat.active(s)
    if not f or f['status']!='active': raise ValueError('No active encounter.')
    p=profile(s,s['player']) if side=='player' else f['opponent_profile']
    if not protocol_available(s,f,side,p):
        raise ValueError('Shinigami Protocol requires three to four meaningful exchanges, 20 stamina and recovery since its last use.')
    r=f[side]; r['stamina']-=20; r['protocol_left']=4; r['protocol_used']=True
    who=s['player'] if side=='player' else f['opponent']
    s['combat'].setdefault('protocol_spent',{})[who]=dict(recover_at=s['world']['minute']+60)
    f['log'].append(p['name']+' activates Shinigami Protocol: four exchanges; 20 stamina spent.')


def rest(s):
    import combat,world_loop
    combat.guard(s)
    if combat.active(s): raise ValueError('Finish the encounter before genuine recovery.')
    world_loop.advance(s,60)
    s['combat'].setdefault('protocol_spent',{}).pop(s['player'],None)
    return 'One hour of recovery restores Shinigami readiness for future encounters.'


def set_channel(s,channel):
    import combat
    from combat_profiles import profile
    f=combat.active(s)
    if not f or f['status']!='active': raise ValueError('No active encounter.')
    p=profile(s,s['player'])
    choices=channels(p)
    if channel not in choices: raise ValueError('That channel is not part of this Trait.')
    r=f['player']; ensure(r)
    if r['channel']==channel: return
    if channel and r['energy']<8: raise ValueError('Switching channel requires 8 mana.')
    if channel: r['energy']-=8
    r['channel']=channel; r['tranquility']=channel=='Ice'
    f['log'].append(p['name']+' channels '+(channel or 'no element')+'.')


def channels(p):
    if trait(p,'Conduit'): return ['', 'Red lightning','Blue lightning','Wind','Fire','Ice']
    if trait(p,'Deathwind'): return ['', 'Wind']
    return []


def activate_endurance(s,side='player'):
    import combat
    from combat_profiles import profile
    f=combat.active(s)
    if not f or f['status']!='active': raise ValueError('No active encounter.')
    p=profile(s,s['player']) if side=='player' else f['opponent_profile']; r=f[side]; ensure(r)
    if not (trait(p,'Conduit') or trait(p,'Deathwind')) or r['misanthropy_used'] or r['energy']<18:
        raise ValueError('Misanthropy requires wind access, 18 mana and unused endurance this encounter.')
    r['energy']-=18; r['misanthropy']=True; r['misanthropy_used']=True; r['endurance_left']=4
    # A finite functional reserve, not healing: accumulated damage stays recorded.
    r['endurance_reserve']=round(r['max_health']*.18)
    f['log'].append(p['name']+' activates Misanthropy: four exchanges of finite continued-function endurance.')


def prepare_action(p,r,move):
    ensure(r); m=copy.deepcopy(move); tags=set(m['tags'])
    # True Sight improves mana application efficiency without making it free.
    if trait(p,'True Sight') and m['mana']:
        m['mana']=max(1,round(m['mana']*.65)); tags.update(('precision','speed'))
    if r['protocol_left']:
        tags.update(('precision','adapt','evade'))
        if p.get('combat_id')=='thirteen' and m['role'] in ('attack','combo','break','throw','control','counter'):
            m['stamina']+=2; tags.add('stagger')
    if trait(p,'War God') and r['war_momentum']:
        tags.add('stability')
        if m['role']=='combo': m['stamina']+=3
        if r['war_momentum']==3 and m['role'] in ('break','counter'):
            m['stamina']+=10; m['force']*=1.3; m['war_finisher']=True
    channel=r['channel']
    aspects=(m.get('aspects','')+' '+str((m.get('amplification') or {}).get('aspect',''))).lower()
    active={channel} if channel else set()
    if channel: m['mana']+=4
    if trait(p,'Conduit'):
        for element,words in {'Red lightning':('red lightning',),'Blue lightning':('blue lightning',),
                              'Wind':('wind',),'Fire':('fire',),'Ice':('ice',)}.items():
            if any(word in aspects for word in words): active.add(element)
    elif trait(p,'Deathwind') and 'wind' in aspects: active.add('Wind')
    if 'Red lightning' in active: m['force']*=1.22
    if 'Blue lightning' in active: tags.update(('speed','evade'))
    if 'Wind' in active: m['soul_fraction']=.22
    if 'Fire' in active: tags.add('breach'); m['force']*=1.12
    if 'Ice' in active: tags.update(('precision','stability')); m['instant_reaction']=True
    if trait(p,'Analysis') and r['observations']: tags.update(('precision','adapt'))
    m['tags']=list(sorted(tags)); return m


def end_exchange(f,profiles,selected,records,sides=('player','enemy')):
    for side in sides:
        other='enemy' if side=='player' else 'player'; r=f[side]; t=f[other]
        ensure(r); p=profiles[side]; action=selected[side]; own=records[side]; incoming=records[other]
        r['last_observed_role']=incoming['role']
        r['observed_pressure']=incoming['damage']
        roles=r.setdefault('observed_roles',{})
        roles[incoming['role']]=roles.get(incoming['role'],0)+1
        observed=incoming['move_id']; r['observations'][observed]=min(5,r['observations'].get(observed,0)+1)
        signature=own['move_id']+'|'+observed
        credible=profiles[other]['stats']['martial_skill']>=30
        threat=incoming['role'] in ('attack','combo','break','throw','control','counter')
        meaningful=(own['damage']>0 or incoming['damage']>0 or
                    threat and own['role'] in ('defence','counter','setup','mobility') and abs(f['arena']['positions'][side]-f['arena']['positions'][other])<=3)
        if credible and meaningful and signature!=r['last_exchange']:
            r['protocol_ready']=min(4,r['protocol_ready']+1)
        r['last_exchange']=signature
        if r['protocol_left']:
            r['protocol_left']-=1
            if not r['protocol_left']: r['protocol_strain']=2
        elif r['protocol_strain']: r['protocol_strain']-=1
        if trait(p,'War God'):
            if action.get('war_finisher'): r['war_momentum']=0
            elif own['damage']>0 and own['move_id']!=r['war_last']:
                r['war_momentum']=min(3,r['war_momentum']+1)
            elif r.get('staggered') or r.get('restrained') or abs(f['arena']['positions'][side]-f['arena']['positions'][other])>2:
                r['war_momentum']=max(0,r['war_momentum']-1)
            r['war_last']=own['move_id']
        if r['misanthropy']:
            r['endurance_left']-=1
            if r['endurance_left']<=0:
                r['misanthropy']=False
                if r.get('endurance_debt',0):
                    r['health']=0
                    f['log'].append(p['name']+' can no longer stand as Misanthropy ends; accumulated injuries remain.')
        r['control_immunity']=max(0,r['control_immunity']-1)
        own['states_after']={k:r[k] for k in ('protocol_left','protocol_strain','war_momentum','channel','soul_damage','endurance_left','endurance_debt')}


def status(p,r):
    ensure(r); parts=[]
    if trait(p,'Shinigami Protocol'):
        parts.append('Protocol '+(str(r['protocol_left'])+' exchanges' if r['protocol_left'] else 'spent' if r['protocol_used'] else str(r['protocol_ready'])+'/'+str(readiness_required(r))+' ready'))
        if r['protocol_strain']: parts.append('Recovery strain '+str(r['protocol_strain']))
    if trait(p,'War God'): parts.append('War God: '+('Ready','Engaged','Flowing','Dominant')[r['war_momentum']])
    if r['channel']: parts.append(r['channel']+(' · Tranquility' if r['tranquility'] else ''))
    if r['misanthropy']: parts.append('Misanthropy '+str(r['endurance_left'])+' · injury debt '+str(r['endurance_debt']))
    for key,label in (('restrained','Restrained'),('staggered','Staggered'),('marks','Weak points')):
        if r.get(key): parts.append(label+' '+str(r[key]))
    return ' · '.join(parts)
