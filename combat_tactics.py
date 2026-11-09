"""Opponent intentions chosen before player input; mechanics own their limits."""
import copy
import random

import combat_path as path
from combat_profiles import ARTS


# Attempts, never guaranteed outcomes. Unknown/custom Traits use their saved limits.
TRAIT_ATTACKS = {
    'shadow': ('project a narrow shadow strike toward an opening',
               'sweep a shaped shadow across the approach to pressure the guard'),
    'flame': ('drive a flame-reinforced strike through an opening',
              'advance behind a controlled flame attack'),
    'elemental': ('launch a controlled lightning attack to pressure the guard',
                  'drive a wind-assisted entry into a fire-reinforced strike'),
    'flow': ('build movement into a forceful advancing strike',
             'carry accumulated motion into an angled attack'),
    'armour': ('advance behind reinforcement into an adaptive weapon strike',
               'press forward with an armoured close-range attack'),
    'analysis': ('read observed guard habits and lead with a calculated feint and strike',
                 'test a new angle and attack the opening suggested by observed movement'),
    'rage': ('drive forward with rage-reinforced striking pressure',
             'press the guard with a forceful close-range combination'),
    'mist': ('use a brief veil of vapour to obscure an attacking entry',
             'shift behind dark vapour and attempt an off-angle strike'),
    'blood': ('shape accessible blood into a short striking edge',
              'spend a little of their own blood on a directed weapon thrust'),
    'impact': ('release stored impact through a committed strike',
               'channel stored impact into a short combination'),
    'speed': ('burst forward with accelerated footwork and a fast strike',
              'change angle with a short speed burst before attacking'),
    'wind': ('send a concentrated cutting gust toward the guard',
             'pressure the approach with a directed wind strike'),
    'critical': ('attempt to create and strike a weak point',
                 'probe the defence for a new weak-point attack'),
    'senses': ('track physical movement cues and launch a precisely timed attack',
               'use sound and air displacement to guide an angled strike'),
    'biocreation': ('grow a biological handgun and fire a controlled shot',
                    'form a rifle-like construct for a directed high-impact shot'),
}


def trait_cost(p, complexity):
    return 10 + complexity // 10 + (5 if (p.get('trait') or {}).get('effect') == 'biocreation' else 0)


def form_choice(s, f):
    """Choose an earned, affordable form, respecting encounter and daily limits."""
    p=f['opponent_profile']; r=f['enemy']
    if r['form_used'] or r['stamina'] < 16: return None
    pressured=(r['health'] < r['max_health']*.6 or f['turn'] >= 4 or
               f['player']['form_until'] > f['elapsed'])
    # His established temperament is to go all out in a real confrontation.
    if not pressured and not (f['opponent']=='sylvanis' and f['kind']!='spar'): return None
    choices=[('Advanced form',path.form_spec(p))]
    if p.get('technique_form')=='Conduit State':
        choices.append(('Conduit State',path.form_spec(p,'Conduit State')))
    for choice,spec in choices:
        if not spec: continue
        if spec['name']=='Conduit State' and s.get('combat',{}).get('form_cooldowns',{}).get(f['opponent'],0)>s['world']['minute']:
            continue
        # Keep enough mana for a basic Trait attack after the first upkeep.
        reserve=trait_cost(p,0) if p.get('trait') else 0
        if r['energy'] >= spec['cost']+spec['upkeep']+reserve: return choice
    return None


def prepare(s):
    """Pure preview: activation and upkeep match the next committed exchange.

    A seed/turn makes refresh, failed requests and save/load keep the same intent.
    Neither the player's draft nor their selected mode is an input to tactics.
    """
    original=s['combat']['active']; f=copy.deepcopy(original)
    p=f['opponent_profile']; r=f['enemy']; choice=form_choice(s,f)
    if choice:
        spec=path.form_spec(p,choice)
        r.update(active_form=spec,form_used=True,form_until=f['elapsed']+spec['duration'])
        r['energy']-=spec['cost']
    path.upkeep(f)
    rng=random.Random(f"{f['seed']}:{f['turn']}:opponent")
    arts=list(p['arts'])
    # Proficiency affects both selection and the strike; only learned arts qualify.
    art=rng.choices(arts,weights=[max(1,p['arts'][a]) for a in arts])[0] if arts else 'Untrained'
    trait=p.get('trait'); complexity=min(60,p['stats']['trait_refinement'])
    while complexity>0 and trait_cost(p,complexity)>r['energy']: complexity-=1
    can_trait=bool(trait and r['energy']>=trait_cost(p,complexity))
    form=r.get('active_form') if r['form_until']>f['elapsed'] else None
    if r['stamina']<16:
        mode='Recover'; action='Recover stamina and mana while looking for the next opening.'
    elif can_trait and (f['turn']%3!=1 or (form and f['turn']%2==0)):
        mode='Trait'
        effect=trait.get('effect','custom')
        if effect=='impact' and not r.get('stored'):
            attack='advance with a probing strike while preparing to store incoming impact'
        else:
            attacks=TRAIT_ATTACKS.get(effect,('launch an offensive application within the saved Trait description and limitations',))
            attack=attacks[(f['turn']//2)%len(attacks)]
        if f['opponent']=='sylvanis' and form and p['path']['stage']==path.TRANSCENDENCE_2:
            attack='project a piercing shadow attack with second-stage Umbrakinesis, using predictive perception to choose its line'
        action=trait['name']+': attempt to '+attack+'.'
        if form: action+=' Active form: '+form['name']+'.'
        if art!='Untrained': action+=' Support the attack with learned '+art+' positioning: '+ARTS.get(art,'Use the saved discipline within its limits.')
    else:
        mode='Martial'
        action=('Initiate a '+art+' attack: '+ARTS.get(art,'Use a basic direct strike and keep a protective guard.'))
        if trait and not can_trait: action+=' Conserve mana; use physical technique.'
    # Initiative is independent of the player's submitted prose and final hit roll.
    player=s['combat']['profiles'][s['player']]
    chance=max(.2,min(.8,.5+(p['stats']['fight_iq']-player['stats']['fight_iq'])*.003))
    enemy_first=rng.random()<chance
    plan=dict(mode=mode,art=art,complexity=complexity if mode=='Trait' else 0,
              action=action,activate_form=choice,enemy_first=enemy_first)
    return plan,f


def describe(plan, f):
    prefix='Preparing '+path.form_spec(f['opponent_profile'],plan['activate_form'])['name']+'. ' if plan['activate_form'] else ''
    return prefix+plan['action']
