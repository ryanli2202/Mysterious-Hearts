"""Live provider sample with a temporary custom identity; no save writes."""
import copy,json,sys
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tests'))
import custom_protagonist,combat_dialogue
from test_custom_protagonist import PROFILE
with patch.object(custom_protagonist,'verify_portrait'):
    s=custom_protagonist.create(PROFILE,'assets/generated/combat-test.png')
s['world']['location']='park'
for who in (s['player'],'rei'): s['world']['cast'][who].update(location='park',journey=None)
before=copy.deepcopy(s)
r=combat_dialogue.generate(copy.deepcopy(s),'rei','spar')
assert s==before
out={key:r[key] for key in ('player_line','dialogue','narration','accepted')}
out.update(protagonist='Alex Rivers',occupation='Illustrator',intent='spar',provider='Configured game provider; portrait validation mocked only; no commit or save writes.')
Path('roadmap/combat-custom-dialogue-sample.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(out,ensure_ascii=True))
