"""Authored techniques, saved learning and shared player/NPC action rules.

The checked-in catalogues own names and descriptions. Mechanics below translate
their roles into bounded effects; no model response can grant arbitrary stats.
"""
import copy
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent / 'combat_catalogue'
MARTIAL = json.loads((ROOT / 'martial.json').read_text(encoding='utf-8-sig'))
CAST = {p['id']: p for p in json.loads((ROOT / 'traits.json').read_text(encoding='utf-8-sig'))}
ROLES = ('attack', 'combo', 'counter', 'defence', 'mobility', 'setup', 'control', 'throw', 'break', 'recovery')


def slug(text):
    return re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')


def spec(ident, name, description, role='attack', tier='basic', kind='martial', art='', tags=(), aspects=''):
    return dict(id=ident, name=name, description=description, role=role, tier=tier,
                kind=kind, art=art, tags=list(tags), aspects=aspects, range=1,
                stamina={'basic':7,'advanced':12,'master':20}.get(tier,12), mana=0,
                health_cost=0, hits=3 if role=='combo' else 1,
                force={'basic':1.,'advanced':1.2,'master':1.5}.get(tier,1.25))


MOVES = {}
for school in MARTIAL:
    for tier in ('basic','advanced','master'):
        for line in school[tier]:
            name, role, description = line.split('|',2)
            role = {'Attack':'attack','Combo':'combo','Flurry':'combo','Control':'control',
                    'Counter':'counter','Defence':'defence','Guard break':'break','Mobility':'mobility',
                    'Pressure':'combo','Recovery':'recovery','Setup':'setup','Takedown':'throw','Throw':'throw'}[role]
            ident = 'martial:'+slug(school['art'])+':'+slug(name)
            tags=[]
            if tier=='master': tags.append('superhuman')
            if role in ('throw','break'): tags += ['breach','knockback']
            if role=='mobility': tags.append('speed')
            if 'weak point' in description.lower(): tags.append('precision')
            move=spec(ident,name,description,role,tier,art=school['art'],tags=tags)
            if 'flurry' in line.lower() or 'hurricane' in name.lower(): move['hits']=5
            MOVES[ident]=move

# Explicit vocabulary for the reviewed Trait roles, independent of numeric stats.
TAG_WORDS = {
    'precision':('accuracy','precision','tracking','prediction','timing','sensory'),
    'adapt':('adaptation','adaptive combo','pattern','synthesis','rhythm'),
    'speed':('speed','burst approach','burst entry','rush','rapid approach','rapid pursuit','angle change','aerial entry'),
    'reach':('reach','ranged','projectile','line attack','forward burst','line damage','firing'),
    'breach':('breach','destruction','structural','cover cutting','cover damage','terrain damage','ground damage','ground fracture','crater'),
    'knockback':('knockback','displacement','collision','debris','wreckage','launch'),
    'guard':('mitigation','defence','defensive','guard reinforcement','armour','bracing','guarded'),
    'barrier':('barrier','bulwark','aegis','grown shield'),
    'evade':('evasion','dispersal','escape','evasive','reposition'),
    'conceal':('conceal','sight-line','decept','stealth','shroud'),
    'restrain':('restraint','snare','bind','grapple','zone control'),
    'momentum':('momentum','buildup','sustained movement','run-up'),
    'heat':('heat','burning','fire trail','fire spread','hot trail'),
    'ice':('ice','icy','chilled','freeze'),
    'stagger':('stagger','balance','disrupt','suppression'),
    'stability':('stability','resistance','pain suppression','pain immunity'),
    'stored':('stored impact','stored-force','reserve spending','finite multi-hit release'),
    'collect':('impact collection','reserve gain','receive-and-return'),
    'mark':('weak-point','vulnerability','mark-and-exploit'),
    'critical':('critical','marked-target','weak-point finisher'),
    'area':('area','wide','multi-angle','rotating','nearby','local','ring'),
}


def tags_for(text):
    text=text.lower()
    return [tag for tag,words in TAG_WORDS.items() if any(word in text for word in words)]


def unique_role(text):
    text=text.lower()
    if any(x in text for x in ('counter','reversal','intercept','reactive')): return 'counter'
    if any(x in text for x in ('barrier','defence','defensive','guarded advance','guard ·')): return 'defence'
    if any(x in text for x in ('throw','grapple')): return 'throw'
    if any(x in text for x in ('combo','sequence','multi-hit','burst across','multi-angle fire')): return 'combo'
    if any(x in text for x in ('restraint','zone','concealment · sight')): return 'control'
    if any(x in text for x in ('weak-point mark','observed-pattern advantage','weapon restoration')): return 'setup'
    if any(x in text for x in ('movement buildup','evasion · reposition','traversal','planned reposition','predictive movement')): return 'mobility'
    if any(x in text for x in ('breach','heavy impact','structural damage','finisher')): return 'break'
    return 'attack'


AMPLIFICATIONS = {}
UNIQUES = {}
for who, data in CAST.items():
    amps=[]; skills=[]
    for name, description, role in data['amplifications']:
        tags=tags_for(role+' '+name)
        amps.append(dict(id='amp:'+slug(who)+':'+slug(name), name=name, description=description,
                         aspect=name, role=role, tags=tags, compatible=list(ROLES), mana=8,
                         environment='Uses the selected aspect against breakable arena objects.'))
    for name, aspects, description, role in data['skills']:
        ident='unique:'+slug(who)+':'+slug(name)
        tags=tags_for(role)
        skill=spec(ident,name,description,unique_role(role),'unique',
                   'unique' if data['kind']=='trait' else 'signature',tags=tags,aspects=aspects)
        skill.update(mana=min(40,18+6*aspects.count('/')) if data['kind']=='trait' else 0, stamina=14,
                     range=4 if 'reach' in tags else 1, effect_summary=role)
        if any(x in role.lower() for x in ('high resource','high mana','multi-element')): skill['mana']=30
        if who=='samantha': skill['health_cost']=4
        if name=='Flowing Stream': skill.update(role='counter',universal_counter=True,range=6)
        if name=='Thousand Sparks': skill.update(role='attack',tags=['momentum','speed','breach','knockback'],build_release=True,stamina=22,mana=26,force=1.6)
        if name=='Descending Tempest': skill.update(tags=['speed','stagger','area','breach'],force=1.5)
        if name=='Dragon Kick': skill.update(tags=['speed','heat','area','breach','knockback'],force=1.5)
        if name in ('Fivefold Ruin','Shadow Requiem'): skill.update(role='combo',hits=5,force=1.65,mana=36,stamina=24)
        if name=='Fivefold Ruin': skill['tags']=['speed','precision','heat','ice','stagger','breach','knockback','area']
        if name=='Fracture Point': skill.update(role='setup',tags=['mark'],range=1)
        if name=='Regrowth Reload': skill.update(role='setup',tags=['precision','guard'],mana=12)
        skills.append(skill)
    AMPLIFICATIONS[who]=amps; UNIQUES[who]=skills

UTILITIES = [
    spec('utility:strike','Direct strike','A simple direct strike; awakened strength still applies.'),
    spec('utility:guard','Guard','Brace against incoming pressure and regain a little stamina.','defence'),
    spec('utility:recover','Recover','Regain stamina and mana, leaving your defence open.','recovery'),
    spec('utility:advance','Advance','Close the gap; awakened movement can cross it in a blur.','mobility',tags=['advance']),
    spec('utility:retreat','Retreat','Create distance and evade the approach.','mobility',tags=['retreat','evade']),
    spec('utility:cover','Take cover','Move behind the selected intact object. Cover can be destroyed.','defence',tags=['cover']),
]
for move in UTILITIES:
    move['kind']='utility'
    if move['id'] in ('utility:recover','utility:guard'): move['stamina']=0


def eligible(p,tier):
    return tier=='basic' or (p['stats']['martial_skill']>=60 if tier=='advanced'
                            else p['stats']['martial_skill']>=80 and p['awakened'])


def initialise(p,who='',custom=None):
    """One-time migration, then only first-lesson basics are granted automatically."""
    fresh='moveset' not in p
    book=p.setdefault('moveset',dict(version=1,learned=[],arts=[],amplifications=[],unique=[]))
    if fresh:
        book['amplifications']=copy.deepcopy(AMPLIFICATIONS.get(who,[]))
        book['unique']=copy.deepcopy(UNIQUES.get(who,[]))
        if custom and custom.get('trait_amplifications'):
            book['amplifications']=copy.deepcopy(custom['trait_amplifications'])
        # Generated circuit opponents use the saved Trait, never an invented element.
        if p.get('trait') and not book['amplifications'] and p['trait'].get('effect')!='custom':
            book['amplifications']=[dict(id='amp:established',name=p['trait']['name'],
                description=p['trait']['description'],aspect=p['trait']['name'],role='Trait reinforcement',
                tags=['precision'],compatible=list(ROLES),mana=8,environment='Contact force against arena objects.')]
        for move in MOVES.values():
            rating=p['arts'].get(move['art'],0)
            if move['art'] in p['arts'] and eligible(p,move['tier']) and (move['tier']=='basic' or rating>=(60 if move['tier']=='advanced' else 80)):
                book['learned'].append(move['id'])
    for art in p['arts']:
        if art not in book['arts']:
            for move in MOVES.values():
                if move['art']==art and move['tier']=='basic' and move['id'] not in book['learned']: book['learned'].append(move['id'])
            book['arts'].append(art)
    return book


def actions(p):
    book=initialise(p)
    result=copy.deepcopy(UTILITIES)
    result += [MOVES[x] for x in book['learned'] if x in MOVES and (MOVES[x]['tier']!='master' or p['awakened'])]
    if p['awakened']:
        result += [x for x in book['unique'] if x['kind']=='signature' or p.get('trait')]
    return result


def amps(p,move=None):
    if not p['awakened'] or not p.get('trait'): return []
    if move and move['kind'] in ('unique','signature'): return []
    return [a for a in initialise(p)['amplifications'] if not move or move['role'] in a['compatible']]


def selection(p,move_id,amp_id=None):
    move=next((copy.deepcopy(x) for x in actions(p) if x['id']==move_id),None)
    if not move: raise ValueError('Learn this move before selecting it.')
    amp=next((a for a in amps(p,move) if a['id']==amp_id),None) if amp_id else None
    if amp_id and not amp: raise ValueError('That amplification is incompatible with this action.')
    move['amplification']=copy.deepcopy(amp)
    if amp:
        move['tags']=list(dict.fromkeys(move['tags']+amp['tags']))
        move['mana']+=amp['mana']
        if p.get('trait',{}).get('effect')=='blood': move['health_cost']+=3
        if 'reach' in amp['tags']: move['range']=max(2,move['range'])
    if move['mana']:
        move['mana']=max(1,round(move['mana']*(1-p['stats']['trait_refinement']*.003)))
    return move


def can_pay(r,move):
    return r['stamina']>=move['stamina'] and r['energy']>=move['mana'] and r['health']>move.get('health_cost',0)


def lesson(s,move_id,teacher=None):
    import combat
    from combat_profiles import profile
    p=profile(s,s['player']); move=MOVES.get(move_id)
    if not move: raise ValueError('Choose a catalogue technique.')
    if move_id in initialise(p)['learned']: raise ValueError('You already know this technique; practise the art to improve it.')
    if not eligible(p,move['tier']):
        raise ValueError('Advanced techniques require martial skill 60; master techniques require martial skill 80 and Awakening.')
    result=combat.train(s,move['art'],teacher)
    if move_id not in p['moveset']['learned']: p['moveset']['learned'].append(move_id)
    return result+' Learned '+move['name']+'.'


def details(move):
    return (move['name']+' · '+move.get('tier','')+' · '+move['role']+'\n'+move['description']+
            f"\nStamina {move['stamina']} · Mana {move['mana']} · Range {move['range']} · {move['hits']} strike(s)"+
            (' · Blood cost '+str(move['health_cost']) if move.get('health_cost') else '')+
            ('\nEffects: '+', '.join(move['tags']) if move['tags'] else ''))
