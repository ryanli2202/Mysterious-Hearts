"""Seeded resolver benchmark. No provider, world clock, rewards or story saves."""
import copy,json,random,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from unittest.mock import patch
from contextlib import nullcontext
import combat,combat_engine as engine,combat_profiles as profiles,combat_states as states
import game_core as core

PAIRS=[('sylvanis','takeo'),('sylvanis','crow'),('takeo','ivan'),('crow','charles'),
       ('ivan','rei'),('charles','garrett'),('rei','tyler'),('neo','samantha'),
       ('thirteen','Keisuke Hachimura'),('martos','minsu'),('camila','emily'),
       ('gordon','valentina'),('takeo','tyler'),('crow','minsu'),('sylvanis','valentina'),
       ('april','samantha'),('rei','richter:enhanced'),('fox','alyssa'),('elias','tyler'),('mavis','samantha'),('daniel','emily'),
       ('samantha','guard:yokai'),('guard:yokai','guard:pmc'),('rei','arena:2'),
       ('arena:300','arena:301'),('arena:100','arena:101'),('arena:10','arena:11')]

def make(who):
    if who.startswith('guard:'):
        import organisation_guards
        return organisation_guards.profile(core.fresh('rei'),who.split(':')[1])
    if who.startswith('arena:'):
        import combat_balance,combat_path,combat_moves
        band,category,values=combat_balance.arena_profile(int(who.split(':')[1]))
        p=profiles.make(who,dict(awakened=category!='unawakened'))
        p.update(stats=dict(zip(profiles.STATS,values)),arts={'Boxing':values[2]},arena_band=band)
        p['path']['stage']=combat_path.TOTALITY if category in ('trait','contender') else combat_path.AWAKENING if p['awakened'] else combat_path.DORMANCY
        if category in ('trait','contender'): p['trait']=dict(name='Spark',description='Contact reinforcement only.',effect='custom')
        p.pop('moveset'); combat_moves.initialise(p); combat_balance.configure_arena(p)
        return p
    if who=='richter:enhanced':
        import organisation_guards,combat_boss
        return combat_boss.install(organisation_guards.profile(core.fresh('rei'),'headhunter'))
    return profiles.make(who)


def run(left,right,seed,forms=False,resources=None):
    s=core.fresh('garrett'); p=make(left); q=make(right)
    s['combat']=dict(profiles={'garrett':p},path_epoch=s['world']['minute'])
    f=dict(id='bench',kind='challenge',opponent=right,opponent_profile=q,location='park',
           player=combat.resources(p),enemy=combat.resources(q),elapsed=0,turn=0,log=[],status='active',
           result=None,score=[0,0],seed=seed,path_form_rules=True)
    s['combat']['active']=f; engine.ensure_arena(f)
    for side,fractions in (resources or {}).items():
        for field,fraction in fractions.items(): f[side][field]=round(f[side][field]*fraction)
    def tick(state):
        f['turn']+=1; f['elapsed']+=30
        if min(f['player']['health'],f['enemy']['health'])<=0: f['status']='finished'
    with patch.object(combat,'complete_exchange',tick), (nullcontext() if forms else patch.object(combat.tactics,'form_choice',return_value=None)), (nullcontext() if forms else patch.object(states,'protocol_available',return_value=False)):
        for turn in range(50):
            if forms:
                if states.protocol_choice(s,f,'player',p): states.activate_protocol(s)
                mirrored=dict(f,opponent=left,opponent_profile=p,player=f['enemy'],enemy=f['player'])
                form=combat.tactics.form_choice(s,mirrored)
                if form: combat.activate_form(s,'player',form)
            options=states.channels(p)
            if options and f['player']['energy']>=12 and turn%3==0:
                states.set_channel(s,options[1+(turn//3)%(len(options)-1)])
            r=f['player']
            if options and r['health']<r['max_health']*.5 and not r['misanthropy_used'] and r['energy']>=22:
                states.activate_endurance(s)
            if f['player']['energy']<4: f['player']['channel']=''; f['player']['tranquility']=False
            choice=engine.choose_action(p,f['player'],f,'player',random.Random(f'{seed}:{turn}:left'))
            engine.resolve(s,engine.request(s,choice['move_id'],choice['amp_id'],choice['target']))
            if f['status']=='finished': break
    l=f['player']['health']/f['player']['max_health']; r=f['enemy']['health']/f['enemy']['max_health']
    windows={}
    for side in ('player','enemy'):
        active=[]
        for exchange in f['exchanges']:
            records={r['side']:r for r in exchange['records']}
            if records[side].get('protocol_active'): active.append(records)
        other='enemy' if side=='player' else 'player'
        windows[side]=dict(exchanges=len(active),dealt=sum(x[side]['damage'] for x in active),received=sum(x[other]['damage'] for x in active))
    return dict(protocol_windows=windows,winner=left if l>r else right if r>l else 'draw',turns=f['turn'],damage=f['score'],
                stamina=[f[x]['stamina'] for x in ('player','enemy')],mana=[f[x]['energy'] for x in ('player','enemy')])

if __name__=='__main__':
    report={'assumptions':'Healthy baseline; advanced forms and Shinigami windows disabled; ordinary AI choices and matching channel policies on both sides, 50 exchange limit. Six seeds per side; descriptive small-sample evidence, not guaranteed matchup outcomes.', 'pairs':[]}
    for a,b in PAIRS:
        results=[run(a,b,seed) for seed in range(6)]+[run(b,a,seed) for seed in range(6)]
        row=dict(a=a,b=b,a_wins=sum(x['winner']==a for x in results),runs=len(results),mean_turns=round(sum(x['turns'] for x in results)/len(results),2),results=results)
        report['pairs'].append(row); print(a,b,row['a_wins'],'/',row['runs'],flush=True)
    report['state_comparisons']=[]
    for a,b in [('neo','ivan'),('thirteen','charles'),('garrett','ivan'),('sylvanis','takeo')]:
        results=[run(a,b,seed,True) for seed in range(6)]+[run(b,a,seed,True) for seed in range(6)]
        report['state_comparisons'].append(dict(a=a,b=b,a_wins=sum(x['winner']==a for x in results),runs=len(results),results=results))
        print('State-enabled',a,b,report['state_comparisons'][-1]['a_wins'],'/ 12',flush=True)
    target=Path(__file__).resolve().parents[1]/'roadmap/combat-balance-results.json'
    target.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
