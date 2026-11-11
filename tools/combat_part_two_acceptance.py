"""Additional Part 2 acceptance: attrition and bounded action combinations."""
import copy,itertools,json,math,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import combat,combat_moves as moves,combat_states as states,combat_engine as engine
import combat_profiles as profiles,combat_path as path
from tools.combat_balance_matrix import run

report={'scope':'Deterministic resolver evidence; no providers, campaign awards or persistent saves.', 'boss':[], 'combinations':{}}
for label,resources in [('fresh',None),('depleted',{'player':{'health':.6,'stamina':.5,'energy':.5}})]:
    rows=[run('rei','richter:enhanced',seed,resources=resources) for seed in range(200,212)]
    report['boss'].append(dict(condition=label,wins=sum(r['winner']=='rei' for r in rows),runs=len(rows),results=rows))
    print(label,report['boss'][-1]['wins'],'/12',flush=True)
assert report['boss'][0]['wins']>report['boss'][1]['wins'], 'Attrition must matter without lowering the boss.'

count=0; maxima={}; failures=[]
for who in ('neo','thirteen','daniel','ivan','valentina','charles','garrett','camila','sylvanis','takeo','rei','april'):
    p=profiles.make(who); highest=0
    for stage in path.STAGES[1:]:
        varied=copy.deepcopy(p); varied['path']['stage']=path.DORMANCY
        for earned in path.STAGES[1:path.STAGES.index(stage)+1]:
            path.transition(varied,earned,0)
        for base in moves.actions(varied):
            for amp in [None]+[a['id'] for a in moves.amps(varied,base)]:
                for loaded in (False,True):
                    r=combat.resources(varied); states.ensure(r)
                    if loaded:
                        r.update(protocol_left=4,war_momentum=3,observations={'seen':3},channel='Wind' if states.channels(p) else '',stored=120,heat=100,marks=3,focus=3)
                    m=states.prepare_action(varied,r,moves.selection(varied,base['id'],amp))
                    f=dict(player=r,enemy=combat.resources(p),opponent=who,opponent_profile=p,kind='challenge',location='park',elapsed=0)
                    engine.ensure_arena(f)
                    damage=engine.raw_damage(varied,m,r,f,'player')
                    assert math.isfinite(damage) and 0<=damage<10000,(who,base['id'],damage)
                    assert m['stamina']>=0 and m['mana']>=0
                    if moves.can_pay(r,m):
                        engine.pay(r,m)
                        assert r['stamina']>=0 and r['energy']>=0
                    count+=1; highest=max(highest,damage)
    maxima[who]=round(highest,2)
report['combinations']=dict(cases=count,maximum_raw_damage=maxima,passed=True,
    limits='Exhaustive over this finite matrix of current learned actions, compatible amplifications, five awakened stages and baseline/loaded stress states for twelve representative profiles. Stress states deliberately combine counters beyond normal eligibility. Not a proof about arbitrary future generated prose or every matchup.')
report['passed']=True
Path('roadmap/combat-part-two-acceptance.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print('Combination checks',count,'PASS',flush=True)
