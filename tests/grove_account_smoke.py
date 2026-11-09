"""Real account setup/edit/profile UI; no AI requests or player-save writes."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from unittest.mock import patch
from PIL import ImageGrab
import tkinter as tk
from tkinter import ttk
import test_custom_protagonist as fixture
import game
import game_core as core
import grove
import grove_accounts as accounts
import grove_account_ui as account_ui
import grove_gallery_ui
import phone_apps as apps
import phone_theme as theme


def audit(widget):
    if isinstance(widget, ttk.Widget):
        style = ttk.Style(widget)
        name = str(widget.cget('style')) or widget.winfo_class()
        if isinstance(widget, ttk.Scrollbar) and name == widget.winfo_class():
            name = str(widget.cget('orient')).title()+'.'+name
        for option in theme.STYLE_OPTIONS:
            for state in theme.STATES:
                assert not theme.is_light_surface(widget, style.lookup(name, option, state)), (name, option, state)
    else:
        for option in theme.SURFACE_OPTIONS:
            if option in widget.keys():
                assert not theme.is_light_surface(widget, widget.cget(option)), (str(widget), option)
    for child in widget.winfo_children(): audit(child)


case = fixture.CustomTests()
case.setUp()
try:
    with patch.object(game.Game, 'check'), patch.object(game.Game, 'persist'), \
         patch.object(game.Game, 'begin_incoming'), patch.object(grove.GrovePump, 'tick'):
        app = game.Game()
        errors = []
        app.report_callback_exception = lambda *args: errors.append(args)
        app.state_data = case.create()
        app.play_screen()
        app.phone_window('Grove')
        phone = app.phone_activity
        app.update()
        out = core.ROOT/'tests'/'screenshots'
        out.mkdir(exist_ok=True)
        form = phone.grove_account_form
        form['handle'].insert(0, 'secretvampire')
        form['bio'].insert('1.0', 'Sketches from a new life in Winterfield.')
        form['save'].invoke(); app.update()
        assert 'belongs' in form['status']['text']
        assert accounts.account(app.state_data) is None
        audit(phone)
        ImageGrab.grab(window=phone.winfo_id()).save(out/'grove-account-setup.png')
        phone.geometry('380x680'); app.update()
        audit(phone)
        ImageGrab.grab(window=phone.winfo_id()).save(out/'grove-account-compact.png')
        phone.geometry('540x960'); app.update()
        form['handle'].delete(0, 'end'); form['handle'].insert(0, 'alex.draws')
        form['save'].invoke(); app.update()
        s = app.state_data
        assert accounts.account(s)['handle'] == 'alex.draws'
        apps.post(s, 'First sketch from my new home.')
        s['world']['minute'] += 1440
        phone.refresh(); app.update()
        assert grove.profile(s, s['player'])['followers'] == 4
        ImageGrab.grab(window=phone.winfo_id()).save(out/'grove-account-growth.png')
        window, edit = account_ui.edit(phone); app.update()
        audit(phone)
        edit['handle'].delete(0, 'end'); edit['handle'].insert(0, 'alex.sketchbook')
        edit['bio'].delete('1.0', 'end'); edit['bio'].insert('1.0', 'Art, coffee and finding my feet.')
        app.update()
        ImageGrab.grab(window=phone.winfo_id()).save(out/'grove-account-edit.png')
        edit['save'].invoke(); app.update()
        assert accounts.account(s)['followers'] == 4
        assert apps.handle(s['player'], s) == '@alex.sketchbook'
        profile = grove_gallery_ui.show_profile(phone, s['player']); app.update()
        ImageGrab.grab(window=phone.winfo_id()).save(out/'grove-account-profile.png')
        audit(phone)
        profile.destroy()
        phone.open_app('Home'); phone.open_app('Grove'); app.update()
        audit(phone)
        assert not errors, errors
        app.destroy()
finally:
    case.doCleanups()
print('Grove account setup, validation, editing, growth, profile, navigation and dark states passed.')
