"""Reproducible MH-002 origin comparisons on the shared combat resolver."""
import copy
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from unittest.mock import patch
import combat_balance_matrix as benchmark
import character_origins as origins
import combat_profiles
import combat_workshop
import combat_moves


def origin(index,awakened=True,signature=False):
    experience=origins.EXPERIENCES[index]
    arts,moves=origins.recommended(experience,['Military CQC','Judo','Boxing','Silat'],awakened)
    raw=dict(name=experience,awakened=awakened,origin=dict(experience=experience,arts=arts,moves=moves))
    if awakened:
        raw.update(awakening_trait='Contact resonance',awakening_description='Finite contact vibration with no ranged or passive effects.',
                   trait_amplifications=combat_workshop.validate_amplifications([dict(name='Contact pulse',description='Reinforces contact precision.',aspect='Contact vibration',role='Accurate contact',tags=['precision'],compatible=['attack','combo','counter','defence','control','throw','break'],mana=8,environment='Contacted surfaces only.')]))
    p=combat_profiles.make('origin_benchmark',raw)
    if signature:
        amp=p['moveset']['amplifications'][0]['id']
        candidates=[dict(name='Pulse '+str(i),description='One bounded contact strike.',role='attack',tags=['precision'],aspects=[amp],range=1,stamina=12,mana=12,hits=1,setup='Contact',counter='Guard or evade',environment='Contacted surface only') for i in range(3)]
        p['moveset']['unique']=[combat_workshop.validate_skills(candidates,p)[0]]
    return p


if __name__=='__main__':
    old=benchmark.make
    profiles={f'origin:{i}:{int(a)}':origin(i,a) for i in range(7) for a in (False,True)}
    profiles['origin:6:signature']=origin(6,True,True)
    def make(who): return copy.deepcopy(profiles[who]) if who in profiles else old(who)
    pairs=[(f'origin:{i}:1',f'origin:{i-1}:1') for i in range(1,7)]
    pairs += [(f'origin:{i}:0',f'origin:{i-1}:0') for i in range(1,7)]
    pairs += [('origin:6:'+variant,other) for variant in ('0','1','signature') for other in ('arena:10','arena:2','richter:enhanced','rei')]
    report=dict(assumptions='Healthy, symmetric six seeds per side, 50 exchanges, ordinary resolver policies; advanced temporary forms disabled. Representative contact Trait and four-style kits, not exhaustive generated powers. Wins at timeout use remaining health fraction.',pairs=[])
    with patch.object(benchmark,'make',make):
        for a,b in pairs:
            results=[benchmark.run(a,b,seed) for seed in range(6)]+[benchmark.run(b,a,seed) for seed in range(6)]
            row=dict(a=a,b=b,a_wins=sum(r['winner']==a for r in results),runs=len(results))
            report['pairs'].append(row); print(a,b,row['a_wins'],'/',row['runs'],flush=True)
    target=Path(__file__).resolve().parents[1]/'roadmap/creator-balance-results.json'
    target.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
