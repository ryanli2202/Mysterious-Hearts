"""Offline automatic wardrobe and Ivan phone roster rendering."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from unittest.mock import patch
import tkinter as tk
from PIL import ImageGrab
import game
import game_core as core
import grove
import four_aces
import hidden_cast
import phone_apps

with patch.object(game.Game, 'check', lambda self: None), \
     patch.object(game.Game, 'persist', lambda self: None), \
     patch.object(grove.GrovePump, 'tick', lambda self: None), \
     patch.object(game.Game, 'begin_incoming', lambda self: None):
    app = game.Game()
    errors = []
    app.report_callback_exception = lambda *args: errors.append(args)
    try:
        app.state_data = core.fresh('ivan')
        assert set(phone_apps.contacts(app.state_data)) == set(hidden_cast.IVAN_STARTING_CONTACTS)
        app.play_screen()
        app.phone_window()
        phone = app.phone_activity
        phone.geometry('560x780')
        phone.open_app('Contacts')
        app.update()
        folder = core.ROOT / 'tests/screenshots'
        folder.mkdir(exist_ok=True)
        ImageGrab.grab(window=phone.winfo_id()).save(folder / 'ivan-contact-roster.png')
        phone.contact_detail('sylvanis')
        app.update()
        ImageGrab.grab(window=phone.winfo_id()).save(folder / 'ivan-sylvanis-contact.png')
        phone.contact_detail('crow')
        app.update()
        ImageGrab.grab(window=phone.winfo_id()).save(folder / 'crow-contact.png')
        assert app.portrait('crow', (210, 350), location=hidden_cast.HQ) is not None
        assert not errors, errors
        print('The Crow contact card and headquarters portrait rendered successfully.')
    finally:
        app.sounds.close()
        app.destroy()
