"""Phone child surfaces stay embedded and preserve drafts/navigation."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from unittest.mock import patch
import tkinter as tk
import game
import game_core as core
import grove
import grove_gallery_ui
from phone_dialogs import AppWindow

with patch.object(game.Game, 'check', lambda self: None), patch.object(game.Game, 'persist', lambda self: None), patch.object(grove.GrovePump, 'tick', lambda self: None), patch.object(game.Game, 'begin_incoming', lambda self: None):
    app = game.Game()
    try:
        app.state_data = core.fresh('rei')
        app.play_screen()
        app.phone_window('Grove')
        phone = app.phone_activity
        app.update()
        phone.grove_entry.insert(0, 'Keep this draft')
        def check():
            app.update()
            dialog = phone.dialogs[-1]
            assert dialog.winfo_toplevel() is phone
            assert dialog.shell.winfo_width() == phone.screen.winfo_width()
            assert dialog.shell.winfo_height() == phone.screen.winfo_height()
            assert dialog.shell.winfo_ismapped()
            return dialog
        phone.grove_profiles()
        check()
        grove_gallery_ui.show_profile(phone, 'rei')
        check()
        assert len(phone.dialogs) == 2
        phone.back()
        assert len(phone.dialogs) == 1
        phone.back()
        assert not phone.dialogs
        assert phone.grove_entry.get() == 'Keep this draft'
        grove_gallery_ui.compose(phone)
        check()
        phone.refresh_feed()
        check()
        phone.open_app('Home')
        assert not phone.dialogs
        for action in (app.rename_contact, app.open_calendar, app.accounts, app.journal):
            action()
            check()
            phone.back()
            assert not phone.dialogs
        from camera_ui import SelectionWheel
        wheel = SelectionWheel(phone, 'Pose', ['One', 'Two'], 'One', lambda value: None)
        check()
        phone.back()
        phone.withdraw()
        desktop = AppWindow(app)
        assert desktop.winfo_class() == 'Toplevel'
        desktop.destroy()
        print('Phone embedded-window smoke passed')
    finally:
        app.destroy()
