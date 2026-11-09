"""Real Tk Path views and async breakthrough, with no AI network or save writes."""
import sys
import time
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from unittest.mock import patch
from PIL import ImageGrab
import game
import game_core as core
import grove
import combat
import combat_path as path
import combat_ui
from combat_profiles import profile

out=core.ROOT/'tests/screenshots'; out.mkdir(exist_ok=True)
with patch.object(game.Game,'check'),patch.object(game.Game,'begin_incoming'),patch.object(game.Game,'persist'),patch.object(grove.GrovePump,'tick'):
    app=game.Game(); errors=[]; app.report_callback_exception=lambda *e:errors.append(e)
    app.state_data=s=core.fresh('garrett'); s['world']['time_mode']='paused'
    s['world']['location']='iron_circle'
    for who in ('garrett','rei'): s['world']['cast'][who].update(location='iron_circle',journey=None)
    app.play_screen(); app.update(); combat_ui.open_combat(app); app.update()
    view=app.combat_view
    def shot(name):
        app.update(); ImageGrab.grab(window=app.winfo_id()).save(out/name)
    def settle():
        until=time.monotonic()+5
        while view.working and time.monotonic()<until: app.update(); time.sleep(.02)
        assert not view.working
    view.run(lambda:view.path_page('garrett')); app.update()
    assert 'THE PATH' in view.title.cget('text')
    shot('path-locked.png')
    app.geometry('1000x800'); app.update(); shot('path-compact.png')
    p=profile(s,'garrett'); s['world']['minute']+=path.MONTH; p['stats']['trait_refinement']=100
    view.refresh(); app.update(); shot('path-ready.png')
    with patch.object(combat,'ask_ai',side_effect=ValueError('Test response failure')):
        view.breakthrough(); settle()
    assert p['path']['stage']==path.TRANSCENDENCE_1
    assert 'Test response failure' in view.status.cget('text')
    shot('path-error.png')
    card=dict(name='Golden Flame Dominion',trait_name=p['trait']['name'],description='Golden fire follows the fighter’s precise intercepting steps and strengthens close-range pressure.',
              limitations='Requires concentration, ongoing mana and valid positioning; no automatic hits.',expression='control')
    with patch.object(combat,'ask_ai',return_value=card): view.breakthrough(); settle()
    assert p['path']['stage']==path.TRANSCENDENCE_2
    shot('path-breakthrough.png')
    view.back_from_path(); app.update()
    combat.start(s,'rei','challenge'); view.refresh(); combat.activate_form(s); view.refresh(); app.update()
    assert combat.active(s)['player']['active_form']['cost']==55
    shot('path-trump-card.png')
    assert view.action.winfo_rooty()+view.action.winfo_height()<=app.winfo_rooty()+app.winfo_height()
    app.sounds.close(); app.destroy()
    assert not errors,errors
print('Path UI passed: locked/ready, compact, AI failure/retry, stage-two breakthrough and paid trump card. Six screenshots; no live AI or saves.')
