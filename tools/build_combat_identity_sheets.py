"""Export internal design sheets; private fields are never public UI defaults."""
import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import combat_identity,game_core
root=Path(__file__).resolve().parents[1]
sheets=combat_identity.all_sheets(game_core.fresh('rei'))
(root/'roadmap/COMBAT_IDENTITY_SHEETS.json').write_text(json.dumps({'schema':1,'privacy':'Internal design records. Use combat_identity.public for audience-facing text.','sheets':sheets},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Exported',len(sheets),'source-linked combat identity records.')
