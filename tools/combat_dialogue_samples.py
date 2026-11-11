"""Review actual configured-provider dialogue, without committing any story effects."""
import copy,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import game_core as core,combat_dialogue
rows=[]
for player,who,kind,art in [('garrett','rei','spar',None),('daniel','rei','learn','Judo'),('neo','rei','challenge',None)]:
    s=core.fresh(player); s['world']['location']='park'
    for ident in (player,who): s['world']['cast'][ident].update(location='park',journey=None)
    before=copy.deepcopy(s)
    try:
        result=combat_dialogue.generate(copy.deepcopy(s),who,kind,art)
        row=dict(player=player,who=who,kind=kind,art=art,player_line=result['player_line'],dialogue=result['dialogue'],accepted=result['accepted'])
    except Exception as exc:
        row=dict(player=player,kind=kind,error=type(exc).__name__+': '+str(exc))
    assert s==before
    rows.append(row); print(json.dumps(row,ensure_ascii=False),flush=True)
    if 'error' in row: break
Path('roadmap/combat-dialogue-samples.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
