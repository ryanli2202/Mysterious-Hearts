"""Render every awakened portrait and check both fighters on the in-person stage."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from unittest.mock import patch
from PIL import ImageGrab
import game
import game_core as core
import grove
import combat
import combat_ui
import combat_portraits as art

with patch.object(game.Game, 'check'), patch.object(game.Game, 'begin_incoming'), patch.object(game.Game, 'persist'), patch.object(grove.GrovePump, 'tick'):
    app = game.Game()
    errors = []
    app.report_callback_exception = lambda *e: errors.append(e)
    try:
        s = app.state_data = core.fresh('samantha')
        s['world']['time_mode'] = 'paused'
        s['world']['location'] = 'park'
        for who in ('samantha', 'alyssa'):
            s['world']['cast'][who].update(location='park', journey=None)
        app.play_screen()
        for who in art.CAST:
            photo = art.portrait(app, who, (160, 190), 'park', s['world']['minute'])
            assert (photo.width(), photo.height()) == (160, 190), who
        with patch.object(combat, 'consent', return_value=(True, 'UI fixture')):
            combat.start(s, 'alyssa', 'challenge')
        combat_ui.open_combat(app)
        app.geometry('1000x800')
        app.update()
        view = app.combat_view
        assert view.master is app.presence_view.master
        assert set(view.combat_portrait_images) == {'player', 'opponent'}
        for widget in view.combat_portrait_rail.winfo_children():
            assert widget.winfo_viewable()
            assert widget.winfo_rooty() + widget.winfo_height() <= view.combat_portrait_rail.winfo_rooty() + view.combat_portrait_rail.winfo_height()
        assert view.execute_button.winfo_rooty() + view.execute_button.winfo_height() <= app.winfo_rooty() + app.winfo_height()
        out = core.ROOT / 'tests' / 'screenshots' / 'awakened-combat-portraits.png'
        ImageGrab.grab(window=app.winfo_id()).save(out)
        assert not errors, errors
    finally:
        app.sounds.close()
        app.destroy()
print('All 24 awakened portraits rendered; both fighters and action controls fit the compact in-person window. No story saves or provider calls.')
