"""Exercise new protagonists in the real desktop and dark phone, without AI/saves."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from unittest.mock import patch
from PIL import ImageGrab
import game
import game_core as core
import playable_cast
import careers_ui
import careers
import grove
import tkinter as tk
from tkinter import ttk
import phone_theme


def audit(widget):
    if isinstance(widget, ttk.Widget):
        style = ttk.Style(widget)
        name = str(widget.cget('style')) or widget.winfo_class()
        if isinstance(widget, (ttk.Scrollbar, ttk.Scale, ttk.Progressbar, ttk.Separator)) and name == widget.winfo_class():
            name = str(widget.cget('orient')).title() + '.' + name
        for option in phone_theme.STYLE_OPTIONS:
            for state in phone_theme.STATES:
                assert not phone_theme.is_light_surface(widget, style.lookup(name, option, state)), (name, option, state)
    else:
        for option in phone_theme.SURFACE_OPTIONS:
            if option in widget.keys(): assert not phone_theme.is_light_surface(widget, widget.cget(option)), (widget, option)
    for child in widget.winfo_children(): audit(child)


out = core.ROOT / '.test-tmp'
with patch.object(game.Game, 'check'), patch.object(game.Game, 'persist'), patch.object(game.Game, 'begin_incoming'), patch.object(grove.GrovePump, 'tick'):
    app = game.Game()
    errors = []
    app.report_callback_exception = lambda *args: errors.append(args)
    try:
        app.geometry('1100x850'); app.update()
        app.start_screen.select('camila'); app.update()
        app.start_screen.preview.render(); app.update()
        ImageGrab.grab(window=app.winfo_id()).save(out / 'playable-selection.png')
        for who in playable_cast.STARTS:
            print('Checking', who, flush=True)
            app.close_main_area()
            app.state_data = core.fresh(who)
            app.play_screen(); app.update()
            app.phone_window(); app.update()
            audit(app.phone_activity)
            if who == 'alyssa': ImageGrab.grab(window=app.phone_activity.winfo_id()).save(out / 'playable-alyssa-phone.png')
            panel = careers_ui.open_careers(app); app.update()
            assert panel is app.area_view and panel.master is app.play_body
            assert not app.phone_activity.winfo_viewable()
            for section in ('Work', 'Project', 'Schedule', 'People', 'History'):
                panel.change(section); app.update()
            panel.change('Work')
            spec = careers.TRACKS[panel.key]
            panel.act(core.town.travel, spec['venue']); core.town.finish_drive(app.state_data)
            app.state_data['world']['minute'] = max(10, spec['hours'][0])*60
            app.state_data['autonomy']['people'][who]['sleep_until'] = None
            panel.act(careers.begin, panel.key); app.update()
            assert careers.ensure(app.state_data)['active']
            if who == 'camila': ImageGrab.grab(window=app.winfo_id()).save(out / 'playable-camila-work.png')
            panel.act(careers.choose, 0); panel.act(careers.choose, 2); app.update()
            assert careers.ensure(app.state_data)['active'] is None
            assert not errors, errors
    finally:
        app.sounds.close(); app.destroy()
assert not errors, errors
print(f'Passed all {len(playable_cast.STARTS)} expanded protagonists: desktop, dark phone, in-person careers and work decisions.')
