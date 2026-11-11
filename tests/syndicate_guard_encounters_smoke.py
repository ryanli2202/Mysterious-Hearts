"""Render actual in-person conversations and combat for every Syndicate type."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from unittest.mock import patch
from PIL import ImageGrab
import game, game_core as core, grove, groups, combat_ui
import organisation_guards as guards
from test_major_campaigns import arrive

out=core.ROOT/'tests/screenshots'
with patch.object(game.Game,'check'),patch.object(game.Game,'begin_incoming'),patch.object(game.Game,'persist'),patch.object(grove.GrovePump,'tick'):
    app=game.Game();errors=[]
    app.report_callback_exception=lambda *e: errors.append(e)
    try:
        for kind in ('clubs','spades','affiliate'):
            s=app.state_data=core.fresh('ivan')
            s['world']['time_mode']='paused';arrive(s,'site_04');guards.refresh(s)
            app.play_screen();app.update()
            name=next(n for n,r in guards.npc_rows(s).items() if r['type']==kind)
            groups.open_local(s,name);app.show_in_person();app.update()
            assert name in app.hangout_view.canvas.portrait_items
            ImageGrab.grab(window=app.winfo_id()).save(out/('syndicate-'+kind+'-conversation.png'))
            groups.close_active(s,'Review complete')
            slot=next(r for r in guards.slots(s,'site_04') if r['type']==kind)
            guards.start(s,slot['id'],guards.profile(s,kind),'art-review',slot)
            combat_ui.open_combat(app);app.update()
            assert app.combat_view.opponent_portrait.width()>0
            ImageGrab.grab(window=app.winfo_id()).save(out/('syndicate-'+kind+'-combat.png'))
        assert not errors,errors
        print('All three Syndicate types rendered in actual in-person conversations and combat.')
    finally:
        app.sounds.close();app.destroy()
