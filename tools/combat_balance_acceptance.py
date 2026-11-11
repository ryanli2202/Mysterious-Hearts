"""Fresh-seed acceptance check, separate from exploratory calibration seeds 0–5."""
import json,statistics,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from tools.combat_balance_matrix import run

# Frozen before this holdout run. These test automatic-policy benchmarks,
# not guaranteed player outcomes or universal lore win percentages.
GROUPS={
 'S+ versus S':(.55,.95,[('sylvanis','takeo'),('sylvanis','crow')]),
 'S versus A+':(.65,1.,[('takeo','ivan'),('crow','charles')]),
 'A+ versus A':(.55,.95,[('ivan','rei'),('charles','garrett')]),
 'A versus B':(.80,1.,[('rei','tyler'),('neo','samantha'),('thirteen','Keisuke Hachimura'),('elias','tyler'),('camila','emily'),('fox','alyssa'),('mavis','samantha'),('daniel','emily')]),
 'Apex versus B':(.95,1.,[('takeo','tyler'),('crow','minsu'),('sylvanis','valentina')]),
 'B versus C':(.65,1.,[('samantha','guard:yokai'),('minsu','arena:200'),('valentina','guard:headhunter')]),
 'C versus D':(.80,1.,[('guard:yokai','guard:pmc')]),
 'Rei versus equipped Richter':(.60,.95,[('rei','richter:enhanced')]),
 'Rei versus contender':(.60,1.,[('rei','arena:2')]),
 'Adjacent bands':(.25,.75,[('arena:300','arena:301'),('arena:100','arena:101'),('arena:10','arena:11')]),
}

if __name__=='__main__':
 report={'seeds':list(range(100,112)),'assumptions':'Healthy solo baseline, identical policies on both sides, no forms in tier comparisons. Forms enabled for four-exchange Protocol window comparisons. No provider, persistent saves or campaign outcomes. Criteria declared before holdout run; exploratory tuning used seeds 0–5.','groups':{},'protocol_windows':[]}
 failed=[]
 for name,(lo,hi,pairs) in GROUPS.items():
  wins=total=0; rows=[]
  for a,b in pairs:
   results=[run(a,b,seed) for seed in range(100,112)]+[run(b,a,seed) for seed in range(100,112)]
   count=sum(r['winner']==a for r in results); wins+=count; total+=len(results)
   rows.append(dict(a=a,b=b,wins=count,runs=len(results),mean_turns=round(statistics.mean(r['turns'] for r in results),2)))
  fraction=wins/total; passed=lo<=fraction<=hi
  report['groups'][name]=dict(criteria=[lo,hi],rate=fraction,passed=passed,pairs=rows)
  if not passed: failed.append(name)
  print(name,round(fraction,3),'PASS' if passed else 'FAIL',flush=True)
 for a,b in [('neo','ivan'),('thirteen','charles')]:
  results=[(run(a,b,seed,True),'player') for seed in range(100,112)]+[(run(b,a,seed,True),'enemy') for seed in range(100,112)]
  windows=[r['protocol_windows'][side] for r,side in results]
  activation=sum(w['exchanges']>0 for w in windows)/len(windows)
  dealt=sum(w['dealt'] for w in windows); received=sum(w['received'] for w in windows)
  ratio=dealt/max(1,received)
  passed=activation>=.75 and ratio>=.8
  report['protocol_windows'].append(dict(a=a,b=b,activation_rate=activation,window_damage_ratio=ratio,criteria='activation >= 0.75; active-window dealt/received >= 0.8',passed=passed))
  if not passed: failed.append(a+' Protocol')
  print(a,'Protocol',round(activation,3),round(ratio,3),'PASS' if passed else 'FAIL',flush=True)
 report['passed']=not failed; report['failed']=failed
 Path('roadmap/combat-holdout-results.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
 raise SystemExit(bool(failed))
