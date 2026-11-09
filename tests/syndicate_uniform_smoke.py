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
        preview = tk.Toplevel(app, bg='#172130')
        preview.title('Syndicate headquarters uniform check')
        preview.geometry('1340x430')
        for who in four_aces.UNIFORM_IDS:
            portrait = app.portrait(who, (210, 350), location=hidden_cast.HQ)
            assert portrait is app.portrait(who, (210, 350), outfit='syndicate')
            assert portrait is not app.portrait(who, (210, 350), location='studio')
            if who == 'ivan':
                assert app.portrait(who, (210, 350), location=hidden_cast.HQ, outfit='selection') is portrait
            else:
                assert app.portrait(who, (210, 350), location=hidden_cast.HQ, outfit='selection') is app.portrait(who, (210, 350), outfit='selection')
            panel = tk.Frame(preview, bg='#172130')
            panel.pack(side='left', padx=4, pady=10)
            tk.Label(panel, image=portrait, bg='#172130').pack()
            tk.Label(panel, text=core.CONTACTS[who][0], bg='#172130', fg='#dce4ed').pack()
        app.update()
        ImageGrab.grab(window=preview.winfo_id()).save(folder / 'syndicate-uniforms.png')
        app.state_data['world']['player_outfit'] = 'Gym tank and shorts'
        core.town.travel(app.state_data, 'studio')
        civilian = app.portrait('ivan', (210, 350), location='studio')
        core.town.travel(app.state_data, hidden_cast.HQ)
        uniform = app.portrait('ivan', (210, 350), location=app.state_data['world']['location'])
        assert civilian is not uniform
        assert any(key[2].endswith('ivan-syndicate.png') and photo is uniform for key, photo in app.photos.items())
        core.town.travel(app.state_data, 'studio')
        assert app.portrait('ivan', (210, 350), location='studio') is civilian
        assert app.state_data['world']['player_outfit'] == 'Gym tank and shorts'
        assert not errors, errors
        print('Six automatic HQ uniforms, civilian overrides and Ivan/Sylvanis contacts rendered successfully.')
    finally:
        app.sounds.close()
        app.destroy()
