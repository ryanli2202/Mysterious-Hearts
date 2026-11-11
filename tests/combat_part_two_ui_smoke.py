"""New combat states in the real compact in-person stage; no provider/save calls."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from unittest.mock import patch
from PIL import ImageGrab
import game,game_core as core,grove,combat,combat_ui,combat_states as states

with patch.object(game.Game,'check'),patch.object(game.Game,'begin_incoming'),patch.object(game.Game,'persist'),patch.object(grove.GrovePump,'tick'):
    app=game.Game(); errors=[]; app.report_callback_exception=lambda *e:errors.append(e)
    try:
        for who,enemy in (('neo','thirteen'),('ivan','rei'),('daniel','neo'),('rei','ivan')):
            app.state_data=s=core.fresh(who); s['world']['time_mode']='paused'; s['world']['location']='park'
            for ident in (who,enemy): s['world']['cast'][ident].update(location='park',journey=None)
            app.play_screen()
            with patch.object(combat,'consent',return_value=(True,'')): combat.start(s,enemy,'challenge')
            f=combat.active(s)
            if who=='neo':
                f['player']['protocol_ready']=4; states.activate_protocol(s)
            elif who=='ivan': states.set_channel(s,'Ice'); states.activate_endurance(s)
            elif who=='daniel': f['player']['war_momentum']=3
            else:
                import combat_profiles,combat_engine
                ap=combat_profiles.profile(s,'april')
                f.update(kind='guard',ally='april',ally_profile=ap,ally_resources=combat.resources(ap),objective='Rescue ally')
                combat_engine.ensure_arena(f); f['arena']['positions']['ally']=1
            combat_ui.open_combat(app); app.geometry('1000x800'); app.update()
            v=app.combat_view
            assert v.execute_button.winfo_viewable()
            assert v.execute_button.winfo_rooty()+v.execute_button.winfo_height()<=app.winfo_rooty()+app.winfo_height()
            ImageGrab.grab(window=app.winfo_id()).save(core.ROOT/'tests/screenshots'/('combat-part-two-'+who+'.png'))
            v.combat_dossier(); app.update()
            ImageGrab.grab(window=app.winfo_id()).save(core.ROOT/'tests/screenshots'/('combat-dossier-'+who+'.png'))
            # New game screens destroy previous overlays naturally.
        assert not errors,errors
    finally:
        app.sounds.close(); app.destroy()
print('Part 2 compact HUD and ability dossiers rendered for Shinigami, Conduit/Tranquility/Misanthropy and War God.')
