"""Render all four new contact cards and verify dark phone controls offline."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from unittest.mock import patch
from PIL import ImageGrab
import game
import game_core as core
import grove
import four_aces

with patch.object(game.Game, 'check', lambda self: None), \
     patch.object(game.Game, 'persist', lambda self: None), \
     patch.object(grove.GrovePump, 'tick', lambda self: None), \
     patch.object(game.Game, 'begin_incoming', lambda self: None):
    app = game.Game()
    errors = []
    app.report_callback_exception = lambda *args: errors.append(args)
    try:
        app.state_data = core.fresh('ivan')
        app.play_screen()
        app.phone_window()
        phone = app.phone_activity
        phone.geometry('560x780')
        folder = core.ROOT / 'tests' / 'screenshots'
        folder.mkdir(exist_ok=True)
        for who in four_aces.IDS:
            phone.contact_detail(who)
            app.update()
            ImageGrab.grab(window=phone.winfo_id()).save(folder / ('four-aces-' + who + '.png'))
            phone.open_thread(who)
            app.update()
        assert not errors, errors
        print('Four Ace contact cards and message threads rendered without callback errors.')
    finally:
        app.sounds.close()
        app.destroy()
