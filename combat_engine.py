"""Deterministic, shared combat resolution. Narration never mutates mechanics."""
import copy
import hashlib
import json
import random
import re
import combat_moves as moves
import combat_path as path


def ensure_arena(f):
    if 'arena' not in f:
        props=[dict(id='wall',name='concrete partition',material='concrete',integrity=150,max_integrity=150,position=3,cover=True),
               dict(id='ground',name='arena floor',material='ground',integrity=220,max_integrity=220,position=3,cover=False)]
        if f['location'] in ('park','downtown','blackhaven','street','warehouse','docks','industrial_district'):
            props.append(dict(id='vehicle',name='parked car',material='metal',integrity=190,max_integrity=190,position=5,cover=True))
        else:
            props.append(dict(id='cover',name='timber barrier',material='wood',integrity=75,max_integrity=75,position=2,cover=True))
        f['arena']=dict(positions={'player':1,'enemy':4},objects=props,rubble=[],hazards=[],light='normal')
    for side in ('player','enemy'):
        r=f[side]
        for key,value in dict(cover=None,restrained=0,staggered=0,marks=0,heat=0,focus=0).items(): r.setdefault(key,value)
    f.setdefault('exchanges',[])
    moves.initialise(f['opponent_profile'],f['opponent'])
    return f['arena']


def active_form(f,side):
    r=f[side]
    return r.get('active_form') if r.get('form_until',0)>f['elapsed'] else None


def preview(s):
    import combat
    f=copy.deepcopy(combat.active(s)); ensure_arena(f)
    choice=combat.tactics.form_choice(s,f)
    if choice:
        spec=path.form_spec(f['opponent_profile'],choice)
        f['enemy'].update(active_form=spec,form_used=True,form_until=f['elapsed']+spec['duration'])
        f['enemy']['energy']-=spec['cost']
    path.upkeep(f)
    return f,choice


def choose_action(p,r,f,side,rng):
    """Intent depends on saved circumstances, not on the player's current draft."""
    if r['stamina']<15: return dict(move_id='utility:recover',amp_id=None,target='opponent')
    unique=[a for a in moves.actions(p) if a['kind'] in ('unique','signature')]
    martial=[a for a in moves.actions(p) if a['kind']=='martial']
    # Include counters and positioning, but maintain offensive initiative most turns.
    pool=unique if unique and f['turn']%3!=1 else martial
    if not pool: pool=martial or moves.UTILITIES[:1]
    affordable=[]
    for a in pool:
        move=moves.selection(p,a['id'])
        if moves.can_pay(r,move): affordable.append(move)
    if not affordable:
        affordable=[moves.selection(p,a['id']) for a in martial if moves.can_pay(r,moves.selection(p,a['id']))]
    if not affordable: return dict(move_id='utility:recover',amp_id=None,target='opponent')
    def weight(a):
        n=3 if a['role'] in ('attack','break','combo','throw') else 1
        if r['health']<r['max_health']*.35 and a['role'] in ('defence','counter'): n+=2
        if r.get('stored',0)>15 and 'stored' in a['tags']: n+=4
        if r.get('momentum',0)>1 and 'momentum' in a['tags']: n+=2
        return n*(.5+p['arts'].get(a['art'],p['stats']['martial_skill'])/100)
    move=rng.choices(affordable,weights=[weight(a) for a in affordable])[0]
    amp=None
    options=[a for a in moves.amps(p,move) if moves.can_pay(r,moves.selection(p,move['id'],a['id']))]
    if options and f['turn']%4!=3: amp=rng.choice(options)['id']
    target='opponent'
    other='enemy' if side=='player' else 'player'
    cover=f[other].get('cover')
    if cover and ('breach' in move['tags'] or p['stats']['fight_iq']>=70): target=cover
    return dict(move_id=move['id'],amp_id=amp,target=target)


def opponent_plan(s):
    f,choice=preview(s)
    rng=random.Random(f"{f['seed']}:{f['turn']}:catalogue")
    selected=choose_action(f['opponent_profile'],f['enemy'],f,'enemy',rng)
    move=moves.selection(f['opponent_profile'],selected['move_id'],selected['amp_id'])
    return dict(**selected,activate_form=choice,name=move['name'],role=move['role'],
                amplification=(move.get('amplification') or {}).get('name',''),kind=move['kind'])


def describe_plan(s):
    plan=opponent_plan(s); f=s['combat']['active']
    prefix=('Preparing '+path.form_spec(f['opponent_profile'],plan['activate_form'])['name']+' · ') if plan['activate_form'] else ''
    return prefix+plan['name']+(' + '+plan['amplification'] if plan['amplification'] else '')+' · '+plan['role']


def request(s,move_id,amp_id=None,target='opponent'):
    f=s['combat']['active']
    return dict(fight_id=f['id'],turn=f['turn'],move_id=move_id,amp_id=amp_id,target=target)


def object_at(f,ident):
    return next((o for o in f['arena']['objects'] if o['id']==ident),None)


def damage_object(f,obj,amount,events):
    if not obj or obj['integrity']<=0: return 0
    hardness={'concrete':18,'metal':24,'ground':24,'wood':4,'trait':8}.get(obj['material'],0)
    dealt=min(obj['integrity'],max(0,round(amount)-hardness)); obj['integrity']-=dealt
    if not dealt: events.append(obj['name']+' withstands the impact'); return 0
    if obj['integrity']==0:
        obj['cover']=False
        if obj['position'] not in f['arena']['rubble']: f['arena']['rubble'].append(obj['position'])
        for side in ('player','enemy'):
            if f[side].get('cover')==obj['id']: f[side]['cover']=None
        events.append(obj['name']+' shatters'+(', opening the route' if obj['material']!='ground' else ', leaving broken footing'))
    else: events.append(obj['name']+' cracks' if obj['material'] in ('concrete','ground') else obj['name']+' buckles')
    return dealt


def displace_object(f,obj,side,record):
    if obj['integrity']>0 or obj['material']=='ground': return False
    arena=f['arena']; old=obj['position']; actor=arena['positions'][side]
    obj['position']=max(0,min(6,old+(2 if old>=actor else -2)))
    if old==obj['position']: return False
    if old in arena['rubble'] and not any(o is not obj and o['integrity']==0 and o['position']==old for o in arena['objects']): arena['rubble'].remove(old)
    if obj['position'] not in arena['rubble']: arena['rubble'].append(obj['position'])
    record['terrain'].append(obj['name']+' wreckage is driven across the arena')
    return True


def terrain_force(p,m,damage):
    # Awakened strength is present in ordinary attacks, not reserved for masters.
    power=p['stats']['awakened_power'] if p['awakened'] else 0
    return (damage+power*1.7)*m['force']*(1.4 if 'breach' in m['tags'] else 1)


def movement(f,side,p,m,target_pos,retreat=False):
    arena=f['arena']; r=f[side]; old=arena['positions'][side]
    steps=1+(p['stats']['awakened_power']//35 if p['awakened'] else 0)+('speed' in m['tags'])
    if r['restrained']: steps=max(0,steps-2)
    if old in arena['rubble'] and 'speed' not in m['tags'] and steps: steps=max(1,steps-1)
    for obj in arena['objects']:
        if obj['cover'] and obj['integrity']>0 and min(old,target_pos)<obj['position']<max(old,target_pos) and 'speed' not in m['tags']:
            steps=max(1,steps-1); break
    direction=1 if target_pos>old else -1
    if retreat: direction=-direction
    distance=steps if retreat else min(steps,max(0,abs(target_pos-old)-(0 if 'cover' in m['tags'] else m['range'])))
    arena['positions'][side]=max(0,min(6,old+direction*distance))
    if arena['positions'][side]!=old: r['cover']=None
    return abs(arena['positions'][side]-old)


def pay(r,m):
    r['stamina']-=m['stamina']; r['energy']-=m['mana']; r['health']-=m.get('health_cost',0)
    if m['mana']: r['trait_uses']=r.get('trait_uses',0)+1


def raw_damage(p,m,r,f,side):
    a=p['stats']; art=p['arts'].get(m['art'],a['martial_skill'])
    power=a['awakened_power'] if p['awakened'] else 0
    value=(8+power*.52+(a['martial_skill']+art)*.065)*m['force']
    if m['mana']: value*=1.12+a['trait_refinement']*.001
    tags=m['tags']
    if 'momentum' in tags: value*=1+r.get('momentum',0)*.1
    if 'heat' in tags: value+=r.get('heat',0)*.6
    if 'stored' in tags: value+=min(65,r.get('stored',0)*.6)
    if (p.get('trait') or {}).get('effect')=='rage' and m['mana']: value*=1+(1-r['health']/r['max_health'])*.45
    form=active_form(f,side)
    if form: value*=form['damage']*(1.1 if form['expression']=='offence' else 1)
    return value


def hurt(f,side,amount,record):
    r=f[side]; actual=min(r['health'],max(0,round(amount)))
    r['health']-=actual; r['stored']=min(120,r['stored']+actual)
    f['score'][0 if side=='enemy' else 1]+=actual
    record['damage']+=actual
    return actual


def attack(f,side,p,q,m,defence,rng,record,counter_record=None):
    other='enemy' if side=='player' else 'player'; r=f[side]; t=f[other]; arena=f['arena']
    target=record['target']; obj=object_at(f,target) if target!='opponent' else None
    target_pos=obj['position'] if obj else arena['positions'][other]
    travelled=movement(f,side,p,m,target_pos)
    if m.get('build_release'): r['momentum']=min(5,r['momentum']+2+travelled)
    record['blur']=bool(travelled and p['awakened'] and (p['stats']['awakened_power']>=35 or 'speed' in m['tags']))
    if abs(arena['positions'][side]-target_pos)>m['range']:
        record['outcome']='out of range'; return
    a=p['stats']; b=q['stats']; tags=m['tags']; dtags=defence['tags']
    technique=(a['martial_skill']+p['arts'].get(m['art'],a['martial_skill']))/2
    chance=.66+(technique-b['martial_skill'])*.002+(a['fight_iq']-b['fight_iq'])*.002
    if m['mana']: chance+=(a['trait_refinement']-50)*.001
    if 'precision' in tags: chance+=.12
    if 'adapt' in tags: chance+=min(.16,f['turn']*.025)
    if 'conceal' in tags and 'precision' not in dtags: chance+=.08
    if 'evade' in dtags: chance-=.16
    if 'conceal' in dtags and 'precision' not in tags: chance-=.1
    if defence['role']=='defence': chance-=.1
    chance+=r.get('focus',0)*.04
    if r.get('staggered'): chance-=.13
    if arena['positions'][side] in arena['rubble'] and 'stability' not in tags: chance-=.06
    if active_form(f,side): chance+=active_form(f,side)['accuracy']
    chance=max(.08,min(.96,chance)); record['chance']=round(chance,3)
    raw=raw_damage(p,m,r,f,side)
    if 'stored' in tags: r['stored']=0
    if 'heat' in tags and m['role'] not in ('mobility','setup'): r['heat']=max(0,r['heat']-10)
    if obj:
        damage_object(f,obj,terrain_force(p,m,raw),record['terrain'])
        if p['awakened'] and 'knockback' in tags and displace_object(f,obj,side,record):
            if obj['position']==arena['positions'][other]: hurt(f,other,raw*.25,record)
        record.update(outcome='terrain hit',hits=m['hits']); return
    # Counters answer the actual incoming category. Flowing Stream has no range/type exclusion.
    multiplier=1.
    if counter_record is not None and not counter_record.get('triggered'):
        counter_record['triggered']=True
        can_reach=defence.get('universal_counter') or abs(arena['positions'][side]-arena['positions'][other])<=defence['range']
        if can_reach:
            clash=max(.1,min(.85,.5+(b['fight_iq']-a['fight_iq'])*.003+(b['awakened_power']-a['awakened_power'])*.002+
                (.1 if 'precision' in dtags else 0)+(min(.12,f['turn']*.02) if 'adapt' in dtags else 0)))
            roll=rng.random()
            if roll<clash*.65: multiplier=0.; counter_record['outcome']='full counter'
            elif roll<clash: multiplier=.5; counter_record['outcome']='partial counter'
            else: counter_record['outcome']='counter missed'
            if multiplier<1:
                returned=raw*(.85 if multiplier==0 else .4)+raw_damage(q,defence,t,f,other)*.3
                hurt(f,side,returned*(1-a['awakened_power']*.003),counter_record)
                counter_record['hits']=1
                if 'knockback' in dtags: arena['positions'][side]=max(0,min(6,arena['positions'][side]+(-1 if side=='player' else 1)))
        else: counter_record['outcome']='counter out of range'
    if r['health']<=0 or multiplier==0: record['outcome']='countered'; return
    damage_per=raw/m['hits']*(1-b['awakened_power']*.0035)*multiplier
    if defence['role']=='defence' or 'guard' in dtags: damage_per*=.55 if 'breach' not in tags else .8
    defending=active_form(f,other)
    if defending: damage_per*=defending['mitigation']*(.85 if defending['expression']=='defence' else 1)
    if t.get('marks') and ('critical' in tags or 'precision' in tags):
        damage_per*=1.4; t['marks']=max(0,t['marks']-1)
    for _ in range(m['hits']):
        if t['health']<=0: break
        if rng.random()>chance: continue
        record['hits']+=1; portion=damage_per
        cover=object_at(f,t.get('cover'))
        if cover and cover['integrity']>0:
            damage_object(f,cover,terrain_force(p,m,raw)/m['hits'],record['terrain'])
            portion*=.65 if 'breach' in tags else .25
        hurt(f,other,portion,record)
    record['outcome']='landed' if record['hits']==m['hits'] else 'partial' if record['hits'] else 'missed'
    if record['hits']:
        if 'mark' in tags: t['marks']=min(3,t['marks']+1)
        if 'stagger' in tags and 'stability' not in dtags: t['staggered']=2; t['momentum']=0
        if 'restrain' in tags or m['role']=='control': t['restrained']=2; t['momentum']=0
        if 'momentum' in tags: r['momentum']=min(5,r['momentum']+1)
        if 'heat' in tags: r['heat']=min(40,r['heat']+8)
        if 'collect' in dtags: t['stored']=min(120,t['stored']+round(record['damage']*.5))
        if 'knockback' in tags or m['role']=='throw':
            old=arena['positions'][other]; direction=1 if old>=arena['positions'][side] else -1
            arena['positions'][other]=max(0,min(6,old+direction*(2 if p['awakened'] else 1))); t['cover']=None
            collision=next((o for o in arena['objects'] if o['integrity']>0 and min(old,arena['positions'][other])<=o['position']<=max(old,arena['positions'][other]) and o['material']!='ground'),None)
            if collision:
                damage_object(f,collision,terrain_force(p,m,raw),record['terrain'])
                hurt(f,other,raw*.15,record)
        if ('area' in tags or m['role']=='throw') and p['awakened']:
            ground=object_at(f,'ground'); damage_object(f,ground,terrain_force(p,m,raw)*.7,record['terrain'])
        if 'ice' in tags or 'heat' in tags:
            for kind in ('ice','heat'):
                if kind not in tags: continue
                arena['hazards']=[h for h in arena['hazards'] if (h['position'],h['type'])!=(target_pos,kind)]
                arena['hazards'].append(dict(position=target_pos,type=kind,expires=f['turn']+3,owner=side))
    elif m['role']!='counter': r['momentum']=max(0,r['momentum']-1)
    if m.get('build_release'): r['momentum']=0


def form_action(f,side,p,action):
    """The earned active form extends the base technique; never gates its use."""
    form=active_form(f,side)
    if not form: return action
    action=copy.deepcopy(action)
    extra={'offence':['breach'],'defence':['guard','stability'],'precision':['precision'],
           'mobility':['speed','evade'],'control':['restrain']}.get(form['expression'],[])
    if (p.get('trait') or {}).get('effect')=='shadow' and p['path']['stage']==path.TRANSCENDENCE_2:
        extra+=['breach','heat']; action['range']=max(3,action['range'])
    action['tags']=list(dict.fromkeys(action['tags']+extra))
    return action


def utility(f,side,p,m,record):
    other='enemy' if side=='player' else 'player'; r=f[side]; a=f['arena']; tags=m['tags']
    if m['role']=='recovery':
        r['stamina']=min(100,r['stamina']+25); r['energy']=min(r['max_energy'],r['energy']+15)
        r['momentum']=0; r['heat']=max(0,r['heat']-10); record['outcome']='recovered'; return
    if m['role']=='mobility':
        movement(f,side,p,m,a['positions'][other],retreat='retreat' in tags or 'evade' in tags)
        if 'momentum' in tags: r['momentum']=min(5,r['momentum']+2)
        if 'heat' in tags: r['heat']=min(40,r['heat']+12)
        r['focus']=min(3,r['focus']+1); record['outcome']='repositioned'
        record['blur']=p['awakened']; return
    if 'cover' in tags:
        obj=object_at(f,record['target'])
        if obj and obj['cover'] and obj['integrity']>0:
            movement(f,side,p,m,obj['position'])
            if abs(a['positions'][side]-obj['position'])<=1: r['cover']=obj['id']
        record['outcome']='took cover' if r['cover'] else 'approached cover'; return
    if 'barrier' in tags:
        ident='barrier:'+f.get('entity_ids',{}).get(side,side); obj=object_at(f,ident)
        value=round(40+p['stats']['awakened_power']*.9)
        if obj: obj.update(integrity=value,max_integrity=value,position=a['positions'][side],cover=True)
        else: a['objects'].append(dict(id=ident,name=p['name']+'’s barrier',material='trait',integrity=value,max_integrity=value,position=a['positions'][side],cover=True))
        r['cover']=ident; record['outcome']='raised a barrier'; return
    if m['role']=='setup':
        if 'mark' in tags:
            distance=abs(a['positions'][side]-a['positions'][other])
            movement(f,side,p,m,a['positions'][other])
            if abs(a['positions'][side]-a['positions'][other])<=m['range']:
                f[other]['marks']=min(3,f[other]['marks']+1); record['outcome']='marked a weak point'
            else: record['outcome']='out of range'
        else: r['focus']=min(3,r['focus']+2); record['outcome']='prepared an opening'
        return
    r['stamina']=min(100,r['stamina']+5); record['outcome']='guarded'


def fallback(records):
    sentences=[]
    for r in records:
        action=r['name']+' uses '+r['move']+(' with '+r['amplification'] if r['amplification'] else '')
        if r.get('blur'): action+=', moving faster than ordinary perception'
        outcome={'landed':'and lands the attack','partial':f"and lands {r['hits']} of {r['beats']} beats",'missed':'but misses',
                 'countered':'but is turned back by the counter','counter missed':'but misses the counter',
                 'full counter':'and redirects the attack back into the opponent','partial counter':'and returns part of the force while taking the remainder',
                 'waiting':'and waits for an attack that never comes','out of range':'but cannot reach the target',
                 'interrupted':'but is stopped before completing it','terrain hit':'and strikes the selected obstacle'}.get(r['outcome'])
        if outcome: action+=' '+outcome
        else: action+='; '+r['outcome']
        if r['terrain']: action+=' as '+', '.join(dict.fromkeys(r['terrain']))
        sentences.append(action+'.')
    return ' '.join(sentences)


def resolve(s,chosen):
    import combat
    from combat_profiles import profile
    f=combat.active(s)
    if not f or f['status']!='active' or (chosen.get('fight_id'),chosen.get('turn'))!=(f['id'],f['turn']):
        raise ValueError('This selection belongs to an old exchange.')
    ensure_arena(f); p=profile(s,s['player']); q=f['opponent_profile']
    m=moves.selection(p,chosen['move_id'],chosen.get('amp_id'))
    target=chosen.get('target','opponent'); obj=object_at(f,target)
    if target!='opponent' and not obj: raise ValueError('Choose an arena object.')
    if 'cover' in m['tags'] and (not obj or not obj['cover'] or obj['integrity']<=0): raise ValueError('Choose an intact cover object.')
    projected,choice=preview(s)
    if not moves.can_pay(projected['player'],m): raise ValueError('Insufficient stamina, mana or blood after form upkeep. Recover or choose another move.')
    plan=opponent_plan(s); enemy=moves.selection(q,plan['move_id'],plan['amp_id'])
    if choice: combat.activate_form(s,'enemy',choice)
    path.upkeep(f)
    m=form_action(f,'player',p,m); enemy=form_action(f,'enemy',q,enemy)
    rng=random.Random(f"{f['seed']}:{f['turn']}:resolve")
    selected={'player':m,'enemy':enemy}; profiles={'player':p,'enemy':q}; records={}
    for side in ('player','enemy'):
        action=selected[side]; pay(f[side],action)
        records[side]=dict(side=side,name=profiles[side]['name'],move=action['name'],move_id=action['id'],
            description=action['description'],aspects=action['aspects'],role=action['role'],
            amplification=(action.get('amplification') or {}).get('name',''),target=target if side=='player' else plan['target'],
            hits=0,beats=action['hits'],damage=0,terrain=[],outcome='waiting',mana=action['mana'],stamina=action['stamina'])
        if action['role'] in ('defence','mobility','setup','recovery'): utility(f,side,profiles[side],action,records[side])
    # Reaction stances are committed before initiative; each counter triggers at most once.
    initiative={side:profiles[side]['stats']['fight_iq']+rng.randrange(40)+(15 if 'speed' in selected[side]['tags'] else 0) for side in selected}
    order=sorted(selected,key=lambda side:initiative[side],reverse=True)
    for side in order:
        other='enemy' if side=='player' else 'player'; action=selected[side]
        if f[side]['health']<=0 or f[other]['health']<=0:
            if records[side]['outcome']=='waiting': records[side]['outcome']='interrupted'
            continue
        if action['role'] in ('attack','combo','break','throw','control'):
            counter=records[other] if selected[other]['role']=='counter' else None
            attack(f,side,profiles[side],profiles[other],action,selected[other],rng,records[side],counter)
    for side in ('player','enemy'):
        r=f[side]
        for key in ('restrained','staggered','focus'): r[key]=max(0,r[key]-1)
        for hazard in f['arena']['hazards']:
            if hazard['owner']!=side and hazard['expires']>f['turn'] and hazard['position']==f['arena']['positions'][side]:
                if hazard['type']=='ice': r['staggered']=1
                else:
                    source=records[hazard['owner']]; hurt(f,side,4,source)
                    source['terrain'].append('the hot ground scorches the opposing footing')
    f['arena']['hazards']=[h for h in f['arena']['hazards'] if h['expires']>f['turn']]
    record=dict(id=f['id']+':'+str(f['turn']),turn=f['turn'],records=[records[x] for x in order],
                narration='',log_index=len(f['log']))
    record['narration']=fallback(record['records'])
    record['summary']=' · '.join(r['name']+f": {r['damage']} damage, {r['hits']}/{r['beats']} hits, {r['stamina']} stamina / {r['mana']} mana" for r in record['records'])
    f['log'].append(record['narration']+'\n'+record['summary']); f['exchanges'].append(record)
    f['enhanced_rules']=True
    import interpol
    interpol.support_turn(s,f,rng)
    combat.complete_exchange(s)
    return copy.deepcopy(record)


def narrate(record):
    """One paragraph after resolution. Failed/malformed output leaves the fallback."""
    import combat
    digest=hashlib.sha256(json.dumps(record['records'],sort_keys=True).encode()).hexdigest()
    result=combat.ask_ai('Write 2–3 concise narrative sentences, 35–65 words, for this RESOLVED fictional superhuman combat exchange. '
        'Use the named moves, actual hits/misses/counters and destroyed terrain exactly as recorded. '
        'Describe action and outcome together in past/present narrative prose. No advice, rules lecture, probability, new powers or future actions. '
        'Never claim an unrecorded hit or destroyed object. Return the supplied outcome token unchanged. Data: '+
        json.dumps(dict(outcome_token=digest,resolution=record['records']),ensure_ascii=False),
        combat.schema({'outcome_token':{'type':'string'},'narration':{'type':'string'}}))
    text=result.get('narration','')
    if (result.get('outcome_token')!=digest or not isinstance(text,str) or not 15<=len(text.split())<=65 or len(text)>600
            or not 2<=len([x for x in re.split(r'[.!?]+(?:\s|$)',text) if x.strip()])<=3):
        raise ValueError('Invalid narration; the resolved exchange is preserved.')
    return dict(id=record['id'],records=record['records'],narration=text.strip())


def commit_narration(s,result):
    f=s.get('combat',{}).get('active')
    if not f: raise ValueError('The fight has closed; its recorded outcome remains unchanged.')
    rec=next((x for x in f.get('exchanges',[]) if x['id']==result.get('id')),None)
    if not rec or rec['records']!=result.get('records'): raise ValueError('Discarded stale narration.')
    rec['narration']=result['narration']
    f['log'][rec['log_index']]=rec['narration']+'\n'+rec['summary']


def support_turn(s,f,rng):
    """Interpol partners and their counterattacks use the same catalogue rules."""
    import combat
    p=f['ally_profile']; q=f['opponent_profile']; r=f['ally_resources']
    if min(r['health'],f['enemy']['health'],f['player']['health'])<=0: return
    moves.initialise(p,f['ally'])
    arena=copy.deepcopy(f['arena'])
    arena['positions']['player']=f['arena']['positions']['player']
    scene=dict(f,player=r,arena=arena,entity_ids={'player':f['ally']})
    ensure_arena(scene)
    chosen=choose_action(p,r,scene,'player',rng)
    ally=moves.selection(p,chosen['move_id'],chosen['amp_id'])
    retaliation=f['turn']%2==0
    reply=choose_action(q,f['enemy'],scene,'enemy',rng) if retaliation else dict(move_id='utility:guard',amp_id=None,target='opponent')
    enemy=form_action(scene,'enemy',q,moves.selection(q,reply['move_id'],reply['amp_id']))
    actions={'player':ally,'enemy':enemy}; people={'player':p,'enemy':q}; records={}
    for side,action in actions.items():
        if side=='enemy' and not retaliation: continue
        pay(scene[side],action)
        records[side]=dict(side=side,name=people[side]['name'],move=action['name'],amplification=(action.get('amplification') or {}).get('name',''),
            target=chosen['target'] if side=='player' else reply['target'],damage=0,hits=0,beats=action['hits'],terrain=[],outcome='waiting')
        if action['role'] in ('defence','mobility','setup','recovery'): utility(scene,side,people[side],action,records[side])
    for side in records:
        other='enemy' if side=='player' else 'player'; action=actions[side]
        if min(scene[side]['health'],scene[other]['health'])<=0: records[side]['outcome']='interrupted'; continue
        if action['role'] in ('attack','combo','break','throw','control'):
            attack(scene,side,people[side],people[other],action,actions[other],rng,records[side],records.get(other) if actions[other]['role']=='counter' else None)
    f['arena']['objects']=arena['objects']; f['arena']['rubble']=arena['rubble']; f['arena']['hazards']=arena['hazards']
    f['arena']['positions']['enemy']=arena['positions']['enemy']
    cover=object_at(f,f['player'].get('cover'))
    if cover and cover['integrity']<=0: f['player']['cover']=None
    for key in ('restrained','staggered','focus'): r[key]=max(0,r.get(key,0)-1)
    f['log'].append(fallback(list(records.values()))+'\nField partner exchange · '+str(records['player']['damage'])+' damage dealt.')
    if r['health']<=0:
        s['combat']['recovery'][f['ally']]=s['world']['minute']+1440
        f['log'].append(p['name']+' is incapacitated and needs a day of recovery.')
