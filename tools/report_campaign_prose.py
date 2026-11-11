"""Reproducible reading inventory, not a claim about measured player playtime."""
import json
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import campaign_prose as prose


def report():
    result={}
    for player,prefix in [('garrett','GD'),('rei','RD'),('fox','FD'),('gordon','FD')]:
        excluded={'garrett':['GD43'],'rei':['RD24','RD25'],'fox':['FD37','FD38'],'gordon':['FD37','FD38']}[player]
        ctx=dict(player=player,choice=0,authenticated=True,direct=False,disclosure='share',support='help',
                 visitor='emily' if player=='rei' else 'april',richter=False,ending='lead',last_ace=True)
        chapters={};sections=0
        for key,scene in prose.library().items():
            if not (key.startswith(prefix) or prefix=='FD' and key.startswith('FM')) or key in excluded:continue
            words=0
            for e in scene['elements']:
                # Include each applicable introduction/outcome once, retaining
                # both halves of split scenes without duplicating shared prose.
                when={k:v for k,v in e.get('when',{}).items() if k!='phase'}
                if all(ctx.get(k)==v for k,v in when.items()) and e.get('when',{}).get('phase')!='failure':
                    words+=len(e['text'].split())
            chapters[scene['chapter']]=chapters.get(scene['chapter'],0)+words;sections+=1
        total=sum(chapters.values())
        result[player]=dict(sections=sections,words=total,minutes_at_200_wpm=round(total/200,1),chapters=chapters)
    return dict(method='Selected authored route inventory: normal Garrett reunion, Rei leadership before Richter, current Crow defeat; all eligible social prose with sharing/help and April follow-through. Counts each selected paragraph once. Excludes UI, generated text, guard/retry boilerplate and reflection responses. Reading estimates at 200 words/minute exclude gameplay and are not measured playtime.',routes=result)


if __name__=='__main__':
    print(json.dumps(report(),ensure_ascii=True,indent=2))
