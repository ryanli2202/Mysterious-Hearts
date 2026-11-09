"""Exercise the real in-person stage with a mocked AI, no network/save writes."""
import sys
import time
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from unittest.mock import patch
from PIL import ImageGrab
import game
import game_core as core
import combat
import combat_ui
import grove

out=core.ROOT/'tests/screenshots'; out.mkdir(exist_ok=True)
with patch.object(game.Game,'check'), patch.object(game.Game,'begin_incoming'), patch.object(game.Game,'persist'), patch.object(grove.GrovePump,'tick'):
    app=game.Game(); errors=[]
    app.report_callback_exception=lambda *e:errors.append(e)
    app.state_data=s=core.fresh('garrett'); s['world']['time_mode']='paused'
    s['world']['location']='iron_circle'
    for who in ('garrett','rei'):
        s['world']['cast'][who].update(location='iron_circle',journey=None)
    app.play_screen(); app.update(); combat_ui.open_combat(app); app.update()
    view=app.combat_view
    def shot(name):
        app.update(); ImageGrab.grab(window=app.winfo_id()).save(out/name)
    assert view.winfo_ismapped()
    assert view.master is app.presence_view.master
    shot('combat-training.png')
    view.signature.insert(0,'Garrett Han'); combat.sign_ledger(s,view.signature.get()); view.refresh(); app.update()
    index=view.people.index('rei'); view.list.selection_clear(0,'end'); view.list.selection_set(index)
    view.attack_warning(); app.update(); assert view.attack_panel.winfo_ismapped()
    shot('combat-attack-confirm.png')
    combat.start(s,'rei','challenge'); view.refresh(); app.update()
    shot('combat-fight.png')
    with patch.object(combat,'ask_ai',side_effect=ValueError('Offline narration fallback')):
        view.submit()
        deadline=time.monotonic()+5
        while view.working and time.monotonic()<deadline: app.update(); time.sleep(.02)
    assert not view.working
    assert combat.active(s)['turn']==1,view.error
    shot('combat-exchange.png')
    app.geometry('1000x800'); app.update(); shot('combat-compact.png')
    assert view.execute_button.winfo_rooty()+view.execute_button.winfo_height()<=app.winfo_rooty()+app.winfo_height()
    combat.finish(s,'Victory — opponent knocked out.','rei'); view.refresh(); shot('combat-result.png')
    combat.close(s); view.refresh(); view.leave(); app.update()
    assert not view.winfo_ismapped()
    app.destroy()
    assert not errors,errors
print('Combat UI smoke passed; six screenshots captured. AI mocked; no story saves written.')
