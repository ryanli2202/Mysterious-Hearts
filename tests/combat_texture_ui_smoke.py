"""Compact hub scrolling, stats, dossier and academy presentation; no saves."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from unittest.mock import patch
from PIL import ImageGrab
import game, game_core as core, grove, combat_ui

with patch.object(game.Game, 'check'), patch.object(game.Game, 'begin_incoming'), patch.object(game.Game, 'persist'), patch.object(grove.GrovePump, 'tick'):
    app = game.Game()
    errors = []
    app.report_callback_exception = lambda *e: errors.append(e)
    try:
        s = app.state_data = core.fresh('garrett')
        s['world']['time_mode'] = 'paused'
        s['world']['location'] = 'iron_circle'
        app.play_screen(); app.geometry('1000x800'); combat_ui.open_combat(app); app.update()
        v = app.combat_view
        def shot(name):
            ImageGrab.grab(window=app.winfo_id()).save(core.ROOT / ('tests/screenshots/combat-texture-' + name + '.png'))
        shot('hub')
        canvas = v.body.master
        canvas.yview_moveto(1); app.update()
        assert v.signature.winfo_rooty() + v.signature.winfo_height() <= canvas.winfo_rooty() + canvas.winfo_height()
        shot('ledger')
        v.combat_dossier(); app.update(); shot('dossier')
        # The dossier is an overlay directly on the combat view.
        overlay = v.winfo_children()[-1]; overlay.destroy()
        v.set_page('academy'); app.update()
        assert v.learn_button.winfo_viewable()
        shot('academy')
        v.set_page(); app.update(); canvas = v.body.master
        canvas.yview_moveto(1); app.update()
        assert not errors, errors
    finally:
        app.sounds.close(); app.destroy()
print('Combat texture smoke passed: compact hub, scrollable ledger, dossier, academy and return navigation.')
