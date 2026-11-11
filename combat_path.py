"""The Path: saved, earned progression; no historical dates or free seed boosts."""
import copy
import json

DORMANCY='Dormancy'
AWAKENING='Awakening'
ASCENSION='Ascension'
TOTALITY='Totality'
TRANSCENDENCE_1='Transcendence 1'
TRANSCENDENCE_2='Transcendence 2'
STAGES=(DORMANCY,AWAKENING,ASCENSION,TOTALITY,TRANSCENDENCE_1,TRANSCENDENCE_2)
MONTH=30*1440
# Authored balance for thresholds not specified by source lore.
ENCOUNTERS={DORMANCY:30, AWAKENING:15, ASCENSION:40}
REFINEMENT={AWAKENING:40, ASCENSION:80}
CAST_STAGES={
    'fox':TOTALITY,'gordon':TOTALITY,
    'garrett':TRANSCENDENCE_1,'charles':TRANSCENDENCE_1,'sylvanis':TRANSCENDENCE_2,
    **dict.fromkeys(('rei','takeo','crow','martos','elias','mavis','camila','ivan','neo','daniel','tyler','thirteen'),TOTALITY),
    **dict.fromkeys(('minsu','samantha','valentina','emily','alyssa','Keisuke Hachimura'),ASCENSION),
    'april':AWAKENING,
}
BOOSTS={AWAKENING:(18,5,5,5),ASCENSION:(8,5,4,4),TOTALITY:(10,5,4,4),
        TRANSCENDENCE_1:(8,0,3,3),TRANSCENDENCE_2:(5,0,3,3)}
LORE=('The Path develops base abilities and mastery; Awakening unlocks superhuman talent. '
      'Awakened power measures mana potency, the soul’s mana output/reserves; trait refinement measures expertise. '
      'Some dormant people have latent mana and others have none. Awakening does not guarantee a unique Trait. '
      'Velirium in the Sun is associated with born Awakened; artificial awakenings are unreliable lore, not available actions. '
      'Most people never awaken, most Awakened never ascend, and Totality is the usual final limit. '
      'Transcendence is a rare breakthrough beyond innate potential, with a temporary, mana-intensive trump card.')

def initialise(p,who=None,minute=None,stage=None):
    """Add metadata once. Existing stats/abilities remain exactly as saved."""
    if who=='ivan' or p.get('form')=='Conduit State': p.setdefault('technique_form','Conduit State')
    if 'path' not in p:
        chosen=stage or CAST_STAGES.get(who,AWAKENING if p.get('awakened') else DORMANCY)
        p['path']=dict(version=1,stage=chosen,entered=minute,encounters=0,stage_encounters=0,
                       trait_uses=0,refinement_remainder=0,history=[],mana_potential=p.get('mana_potential',True),
                       trump_card=None)
        if chosen in (TRANSCENDENCE_1,TRANSCENDENCE_2):
            name={'garrett':'Golden Flame Transcendence','charles':'White Flame Tiger',
                  'sylvanis':'Black-eyed Shadow Dominion'}.get(who,p.get('form') or chosen)
            p['path']['trump_card']=dict(name=name,trait_name=(p.get('trait') or {}).get('name',''),
                description=(p.get('trait') or {}).get('description','Refined awakened abilities.'),
                limitations='Temporary manifestation; ends when its duration or mana is exhausted.',
                expression='offence',stage=chosen,source='Established source-story form')
    path=p['path']
    if path.get('entered') is None and minute is not None: path['entered']=minute
    return path

def current(s,who=None):
    from combat_profiles import profile
    who=who or s['player']
    return profile(s,who)['path']

def add_stats(p,values):
    from combat_profiles import STATS
    for key,value in zip(STATS,values):
        if key=='trait_refinement' and not p.get('trait'): continue
        p['stats'][key]=min(100,p['stats'][key]+value)

def transition(p,target,minute):
    path=p['path']; previous=path['stage']
    if target not in STAGES or STAGES.index(target)!=STAGES.index(previous)+1:
        raise ValueError('The Path must be progressed one stage at a time.')
    before=dict(p['stats'])
    add_stats(p,BOOSTS[target]); p['awakened']=True
    path.update(stage=target,entered=minute,stage_encounters=0)
    path['history'].append(dict(previous=previous,stage=target,minute=minute,
        balance_review=__import__('combat_review').progression_review(before,p['stats'],target)))
    return previous+' → '+target

def advance_early(p,minute):
    path=p['path']; stage=path['stage']
    if stage not in ENCOUNTERS or path['stage_encounters']<ENCOUNTERS[stage]: return None
    if stage==DORMANCY and not path['mana_potential']: return None
    if p.get('trait') and p['stats']['trait_refinement']<REFINEMENT.get(stage,0): return None
    return transition(p,STAGES[STAGES.index(stage)+1],minute)

def award_encounter(s,f):
    """Award once, to both fighters, only after a strenuous completed encounter."""
    if f.get('path_awarded'): return
    f['path_awarded']=True
    damage=sum(f.get('score',[0,0]))
    knocked=any(f[side]['health']<=0 for side in ('player','enemy'))
    if damage<10 or f.get('turn',0)<1 or (f['turn']<4 and not knocked):
        f['log'].append('Path: no progression — this encounter did not involve sustained exertion or a knockout.')
        return
    from combat_profiles import profile
    for side,who in (('player',s['player']),('enemy',f['opponent'])):
        # Generated opponents keep their progression in the saved encounter only.
        p=profile(s,who) if side=='player' or f['kind'] not in ('circle','guard') or (f.get('title_bout') and who in s.get('combat',{}).get('profiles',{})) else f['opponent_profile']
        path=initialise(p,who,s['world']['minute'])
        old=path['stage']; path['encounters']+=1; path['stage_encounters']+=1
        notes=[]
        if old in (ASCENSION,TRANSCENDENCE_1,TRANSCENDENCE_2):
            before=p['stats']['awakened_power']; p['stats']['awakened_power']=min(100,before+1)
            if p['stats']['awakened_power']>before: notes.append('mana potency +1')
        uses=f[side].get('trait_uses',0) if p.get('trait') else 0
        path['trait_uses']+=uses
        earned,path['refinement_remainder']=divmod(path['refinement_remainder']+uses,4)
        if earned and old!=DORMANCY:
            before=p['stats']['trait_refinement']; p['stats']['trait_refinement']=min(100,before+earned)
            if p['stats']['trait_refinement']>before: notes.append('trait refinement +'+str(p['stats']['trait_refinement']-before))
        changed=advance_early(p,s['world']['minute'])
        if changed: notes.append(changed)
        f['log'].append(p['name']+' · Path: '+(', '.join(notes) or 'strenuous encounter recorded; '+path['stage']+'.'))
        if side=='enemy': f['opponent_profile']=copy.deepcopy(p)

def readiness(s,who=None):
    from combat_profiles import profile
    who=who or s['player']; p=profile(s,who); path=p['path']; stage=path['stage']
    if stage==TRANSCENDENCE_2: return False,'Transcendence 2 reached — the final Path stage.'
    if stage not in (TOTALITY,TRANSCENDENCE_1): return False,'Reach Totality before attempting a breakthrough.'
    if not p.get('trait'): return False,'Transcendence requires an established Awakened Trait to master.'
    refinement=93 if stage==TOTALITY else 100
    elapsed=max(0,s['world']['minute']-path['entered'])
    remaining=max(0,MONTH-elapsed)
    if p['stats']['trait_refinement']<refinement or remaining:
        return False,f'Requires refinement {refinement}+ (now {p["stats"]["trait_refinement"]}) and 30 days in {stage}; {remaining//1440}d {remaining%1440//60}h {remaining%60}m remaining.'
    return True,'Ready for '+(TRANSCENDENCE_1 if stage==TOTALITY else TRANSCENDENCE_2)+'.'

def access(s,who):
    import combat
    combat.guard(s)
    if who!=s['player']:
        combat.check_pair(s,who)
        import relationship_dynamics
        if who in s.get('combat',{}).get('ruptures',[]) or relationship_dynamics.stats(s,who).get('trust',35)<25:
            raise ValueError('They decline your invitation to attempt a breakthrough.')
    ready,reason=readiness(s,who)
    if not ready: raise ValueError(reason)

def validate_card(card,trait,target):
    if not isinstance(card,dict): raise ValueError('Invalid breakthrough response.')
    for key,limit in (('name',100),('description',1200),('limitations',600),('trait_name',100)):
        if not isinstance(card.get(key),str) or not 1<=len(card[key].strip())<=limit:
            raise ValueError('The breakthrough requires a bounded name, description, limitations and Trait reference.')
    if card['trait_name']!=trait['name']: raise ValueError('The trump card must develop your own Trait.')
    if card.get('expression') not in ('offence','defence','precision','mobility','control'):
        raise ValueError('Invalid trump-card expression.')
    return {**{key:card[key].strip() for key in ('name','description','limitations','trait_name','expression')},
            'stage':target,'source':'AI gamemaster breakthrough'}

def generate_breakthrough(s,who=None):
    import combat
    from combat_profiles import profile
    who=who or s['player']; access(s,who); p=profile(s,who); path=p['path']
    target=TRANSCENDENCE_1 if path['stage']==TOTALITY else TRANSCENDENCE_2
    card=combat.ask_ai('Generate a '+target+' trump card as a higher expression of ONLY this established Trait. '
        'Do not invent unrelated abilities, guaranteed victories, permanent invulnerability or new base statistics. '
        'Return its exact trait_name, a name, a concrete description of usable techniques, and meaningful limitations. '
        'Choose an expression from offence, defence, precision, mobility, control. The engine fixes mana costs, duration and bounded bonuses. '
        'Stage 1 costs 35 mana plus 8 per exchange for up to 180 seconds; stage 2 costs 55 plus 12 per exchange for up to 300 seconds. '
        +json.dumps(dict(trait=p['trait'],previous_card=path['trump_card'],stats=p['stats']),ensure_ascii=False),
        combat.schema({**{key:{'type':'string'} for key in ('name','description','limitations','trait_name')},
                       'expression':{'type':'string','enum':['offence','defence','precision','mobility','control']}}))
    card=validate_card(card,p['trait'],target)
    return dict(who=who,previous=path['stage'],entered=path['entered'],trait=copy.deepcopy(p['trait']),card=card)

def commit_breakthrough(s,result):
    from combat_profiles import profile
    who=result['who']; access(s,who); p=profile(s,who); path=p['path']
    if (path['stage'],path['entered'],p['trait'])!=(result['previous'],result['entered'],result['trait']):
        raise ValueError('The character changed; discard this stale breakthrough and try again.')
    target=TRANSCENDENCE_1 if path['stage']==TOTALITY else TRANSCENDENCE_2
    card=validate_card(result['card'],p['trait'],target)
    transition(p,target,s['world']['minute']); path['trump_card']=card; p['form']=card['name']
    return p['name']+' reached '+target+' — '+card['name']+'.'

def summary(s,who=None):
    from combat_profiles import profile
    p=profile(s,who or s['player']); path=p['path']; stage=path['stage']
    text=stage+' · '+str(path['stage_encounters'])+' strenuous encounters in this stage'
    if stage in ENCOUNTERS:
        text+=f' / {ENCOUNTERS[stage]} needed'
        if p.get('trait') and stage in REFINEMENT: text+=f' · refinement {REFINEMENT[stage]}+ required'
    elif stage in (TOTALITY,TRANSCENDENCE_1): text+=' · '+readiness(s,who)[1]
    if not path['mana_potential'] and stage==DORMANCY: text+=' · No latent mana: cannot awaken through combat.'
    return text

def form_spec(p,choice=None):
    if choice=='Conduit State':
        if p.get('technique_form')!='Conduit State' and p.get('form')!='Conduit State': return None
        return dict(name='Conduit State',cost=0,upkeep=0,duration=300,damage=1.35,accuracy=.07,
                    mitigation=1,expression='offence')
    path=p.get('path',{})
    if path.get('stage') in (TRANSCENDENCE_1,TRANSCENDENCE_2) and path.get('trump_card'):
        second=path['stage']==TRANSCENDENCE_2
        return dict(name=path['trump_card']['name'],cost=55 if second else 35,upkeep=12 if second else 8,
                    duration=300 if second else 180,damage=1.85 if second else 1.5,
                    accuracy=.15 if second else .10,mitigation=.7 if second else .85,
                    expression=path['trump_card']['expression'])
    if p.get('form')=='Conduit State':
        return form_spec(p,'Conduit State')
    return None

def upkeep(f):
    for side in ('player','enemy'):
        r=f[side]; form=r.get('active_form')
        if not form or r['form_until']<=f['elapsed']: continue
        if r['energy']<form['upkeep']:
            r['form_until']=f['elapsed']; f['log'].append(('Your' if side=='player' else 'Opponent’s')+' trump card ends: insufficient mana.')
        else: r['energy']-=form['upkeep']
