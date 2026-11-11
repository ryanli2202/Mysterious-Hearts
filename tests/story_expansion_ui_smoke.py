"""Render the authored defeat and ongoing-resistance ending without provider calls."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from unittest.mock import patch
from PIL import ImageGrab
import game, game_core as core, grove, combat, combat_ui, interpol as law, interpol_ui
import campaign_dialogue as dialogue
from test_story_expansion import crow_fight
from careers_ui_smoke import audit

out=core.ROOT/'.test-tmp'
with patch.object(game.Game,'check'),patch.object(game.Game,'persist'),patch.object(game.Game,'begin_incoming'),patch.object(grove.GrovePump,'tick'):
    app=game.Game();errors=[];app.report_callback_exception=lambda *e:errors.append(e)
    try:
        app.state_data=s=crow_fight();s['world']['time_mode']='paused'
        app.play_screen();app.geometry('1000x800');app.update()
        combat_ui.open_combat(app);app.update()
        ImageGrab.grab(window=app.winfo_id()).save(out/'story-crow-combat.png')
        combat.concede(s);combat.close(s);app.combat_view.place_forget()
        s['world']['minute']+=1440
        if s['world']['location']!=law.objective(s)['venue']:law.travel_objective(s)
        interpol_ui.open_in_person(app);app.update();audit(app.interpol_view)
        ImageGrab.grab(window=app.winfo_id()).save(out/'story-crow-withdrawal.png')
        for _ in range(4):
            if s['world']['location']!=law.objective(s)['venue']:law.travel_objective(s)
            dialogue.begin(s,'interpol.advance');dialogue.show(app);app.update()
            assert app.hangout_view.winfo_viewable()
            assert not app.phone_activity.winfo_viewable() if getattr(app,'phone_activity',None) else True
            if law.objective(s)['kind']=='ongoing':
                ImageGrab.grab(window=app.winfo_id()).save(out/'story-crow-acceptance.png')
            while s.get('campaign_dialogue'):dialogue.next_line(s)
            dialogue.restore(app.hangout_view)
        assert law.read(s)['syndicate_outcome']=='ongoing resistance'
        interpol_ui.open_in_person(app);app.update()
        assert not errors,errors
        print('PASS: Crow combat, withdrawal, four debrief scenes and ongoing ending on the in-person stage at compact size.')
    finally:app.sounds.close();app.destroy()
