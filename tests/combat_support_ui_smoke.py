"""Real in-person patrol entry, partner HUD and revealed boss presentation."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from unittest.mock import patch
from PIL import ImageGrab
import game,game_core as core,grove,combat,campaign_ui,combat_ui,combat_boss
import organisation_guards as guards
from campaign_ui_helpers import finish_script

def widgets(root):
    for child in root.winfo_children():
        yield child
        yield from widgets(child)

with patch.object(game.Game,'check'),patch.object(game.Game,'begin_incoming'),patch.object(game.Game,'persist'),patch.object(grove.GrovePump,'tick'):
    app=game.Game(); errors=[]; app.report_callback_exception=lambda *e:errors.append(e)
    try:
        s=app.state_data=core.fresh('rei'); s['world']['time_mode']='paused'
        core.town.travel(s,'hamayashi_house')
        s['world']['cast']['april'].update(location='hamayashi_house',journey=None)
        s.setdefault('friendships',{})['april']={'trust':80}
        if s.get('relationships',{}).get('april'): s['relationships']['april']['trust']=80
        s['groups']['support']=dict(members=['april'],open=True,channel='in_person',history=[],location='hamayashi_house',choices=[],name='Field party')
        s['active_group']='support'
        app.play_screen(); campaign_ui.open_in_person(app); app.campaign_view.change('Guards'); app.geometry('1000x800'); app.update()
        buttons=[w for w in widgets(app.campaign_view) if w.winfo_class()=='TButton' and 'supporting' in str(w.cget('text'))]
        assert len(buttons)==1
        ImageGrab.grab(window=app.winfo_id()).save(core.ROOT/'tests/screenshots/combat-support-entry.png')
        buttons[0].invoke(); finish_script(app); app.update(); f=combat.active(s)
        assert f is not None,app.campaign_view.notice
        assert f['ally']=='april' and app.combat_view.winfo_viewable()
        assert app.combat_view.execute_button.winfo_rooty()+app.combat_view.execute_button.winfo_height()<app.winfo_rooty()+app.winfo_height()
        ImageGrab.grab(window=app.winfo_id()).save(core.ROOT/'tests/screenshots/combat-support-hud.png')
        combat.concede(s); combat.close(s)
        # Rendering fixture only; campaign boss access remains tested by major-campaign tests.
        p=combat_boss.install(guards.profile(s,'headhunter')); p.update(name='Joseph Richter',portrait='richter_cybernetic')
        guards.start(s,'boss:fixture',p,'render-only'); combat_ui.open_combat(app); app.update()
        assert app.combat_view.title.cget('text').startswith('BOSS')
        ImageGrab.grab(window=app.winfo_id()).save(core.ROOT/'tests/screenshots/combat-richter-hud.png')
        assert not errors,errors
    finally: app.sounds.close(); app.destroy()
print('Trusted in-person companion entry, compact partner HUD and revealed boss framing passed; no saves or providers.')
