"""Audit phone surfaces and native control states without AI or save writes."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from unittest.mock import patch
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageGrab
import game
import game_core as core
import grove
import phone_theme as theme
from phone_icons import COLORS
from phone_dialogs import AppWindow


def audit(widget, failures):
    if isinstance(widget, ttk.Widget):
        style = ttk.Style(widget)
        name = str(widget.cget('style')) or widget.winfo_class()
        if isinstance(widget, (ttk.Scrollbar, ttk.Scale, ttk.Progressbar, ttk.Separator)) and name == widget.winfo_class():
            name = str(widget.cget('orient')).title() + '.' + name
        for option in theme.STYLE_OPTIONS:
            for state in theme.STATES:
                color = style.lookup(name, option, state)
                if theme.is_light_surface(widget, color): failures.append((str(widget), name, option, state, color))
        if isinstance(widget, ttk.Combobox):
            popup = widget.tk.call('ttk::combobox::PopdownWindow', str(widget))
            for option in ('background', 'selectbackground'):
                color = widget.tk.call(str(popup) + '.f.l', 'cget', '-' + option)
                assert not theme.is_light_surface(widget, color), (popup, option, color)
    else:
        for option in theme.SURFACE_OPTIONS:
            if option in widget.keys() and theme.is_light_surface(widget, widget.cget(option)):
                failures.append((str(widget), option, widget.cget(option)))
        if isinstance(widget, tk.Canvas):
            for item in widget.find_all():
                if widget.type(item) in ('text', 'image', 'window'): continue
                for option in ('fill', 'outline'):
                    if option not in widget.itemconfigure(item): continue
                    color = widget.itemcget(item, option)
                    if theme.is_light_surface(widget, color): failures.append((str(widget), item, option, color))
    for child in widget.winfo_children(): audit(child, failures)


with patch.object(game.Game, 'check', lambda self: None), \
     patch.object(game.Game, 'persist', lambda self: None), \
     patch.object(grove.GrovePump, 'tick', lambda self: None), \
     patch.object(game.Game, 'begin_incoming', lambda self: None):
    app = game.Game()
    errors, failures, shots = [], [], []
    app.report_callback_exception = lambda *args: errors.append(args)
    try:
        app.state_data = core.fresh('rei')
        from supafast_fixtures import seed
        seed(app.state_data)
        from supafast_fixtures import disable_images
        disable_images(app)
        app.play_screen()
        app.phone_window()
        phone = app.phone_activity
        phone.geometry('560x780')
        for page in ['Home', *COLORS, 'Customise', 'Lock', 'Keepsake']:
            print('Checking', page, flush=True)
            phone.open_app(page)
            app.update()
            audit(phone, failures)
            if page == 'Home':
                phone.edit_home()
                app.update()
                audit(phone, failures)
                shots.append(ImageGrab.grab(window=phone.winfo_id()).convert('RGB'))
                phone.edit_home()
                app.update()
            if page in ('Settings', 'Contacts', 'Customise', 'Notes'):
                shots.append(ImageGrab.grab(window=phone.winfo_id()).convert('RGB'))
        phone.open_thread('emily')
        app.update()
        audit(phone, failures)
        phone.contact_detail('emily')
        app.update()
        audit(phone, failures)
        # Explicitly exercise light defaults, disabled/readonly controls and a
        # custom ttk style in a dynamically mounted embedded child window.
        dialog = AppWindow(phone)
        dialog.title('Dark controls check')
        ttk.Style(dialog).configure('Audit.TEntry', fieldbackground='white')
        for widget in (tk.Entry(dialog, bg='white', disabledbackground='SystemButtonFace'),
                       tk.Text(dialog, bg='white', height=2),
                       tk.Listbox(dialog, bg='white', height=2),
                       ttk.Entry(dialog, style='Audit.TEntry', state='readonly'),
                       ttk.Combobox(dialog, values=['One', 'Two'], state='readonly'),
                       ttk.Checkbutton(dialog, text='Check'), ttk.Radiobutton(dialog, text='Radio'),
                       ttk.Scale(dialog), ttk.Scrollbar(dialog)):
            widget.pack(fill='x')
        app.update()
        audit(phone, failures)
        shots.append(ImageGrab.grab(window=phone.winfo_id()).convert('RGB'))
        dialog.destroy()
        assert not errors, errors
        assert not failures, failures
        folder = core.ROOT / 'tests' / 'screenshots'
        folder.mkdir(exist_ok=True)
        sheet = Image.new('RGB', (len(shots) * 280, 420), theme.BACKGROUND)
        for i, shot in enumerate(shots):
            shot.thumbnail((280, 420))
            sheet.paste(shot, (i * 280, 0))
        sheet.save(folder / 'phone-dark-theme.png')
        print(f'Dark surfaces verified across {len(COLORS) + 4} phone pages, chat, contact details, and embedded controls.')
    finally:
        app.sounds.close()
        app.destroy()
