"""Actual park entry, input, resize, interactions, teardown and dark errors."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from unittest.mock import patch
from PIL import ImageGrab
import game
import game_core as core
import grove
import park_ui
import phone_theme
import tkinter as tk
from tkinter import ttk

def audit(widget):
    if isinstance(widget,ttk.Widget):
        style=ttk.Style(widget);name=str(widget.cget('style')) or widget.winfo_class()
        for option in phone_theme.STYLE_OPTIONS:
            for state in phone_theme.STATES:
                assert not phone_theme.is_light_surface(widget,style.lookup(name,option,state)),(name,option,state)
    else:
        for option in phone_theme.SURFACE_OPTIONS:
            if option in widget.keys():assert not phone_theme.is_light_surface(widget,widget.cget(option)),option
    for child in widget.winfo_children():audit(child)

out=core.ROOT/'tests/screenshots';out.mkdir(exist_ok=True)
with patch.object(game.Game,'check',lambda self:None), patch.object(game.Game,'persist',lambda self:None), patch.object(grove.GrovePump,'tick',lambda self:None), patch.object(game.Game,'begin_incoming',lambda self:None):
    app=game.Game();errors=[]
    app.report_callback_exception=lambda *a:errors.append(a)
    try:
        app.state_data=core.fresh('garrett');app.play_screen();app.phone_window('Maps');app.update()
        phone=app.phone_activity;phone.geometry('560x820');app.update()
        view=phone.map_view;view.select('park');app.update()
        assert not hasattr(view,'park_button')
        view.drive_button.invoke();app.update()
        assert app.state_data['world']['location']=='park'
        def descendants(widget):
            for child in widget.winfo_children():
                yield child
                yield from descendants(child)
        entry=next(w for w in descendants(app.presence_view) if isinstance(w,ttk.Button) and str(w.cget('text')).startswith('Enter park'))
        entry.invoke();app.update()
        assert not errors,errors
        p=app.area_view
        assert p.master is app.play_body and p.winfo_toplevel() is app
        assert not phone.winfo_viewable() and not phone.dialogs
        assert p.renderer and p.timer
        app.render();app.update();assert app.area_view is p and p.alive
        audit(p)
        p.canvas.focus_force();app.update()
        p.canvas.event_generate('<KeyPress-d>');app.update();assert 'd' in p.held_keys
        p.canvas.event_generate('<KeyRelease-d>');app.update();assert 'd' not in p.held_keys
        p.hold('right');p.canvas.event_generate('<FocusOut>');assert not p.held_keys
        buttons=p.interact_button.master.winfo_children()
        buttons[0].event_generate('<ButtonPress-1>');assert 'left' in p.held_keys
        buttons[0].event_generate('<ButtonRelease-1>');assert not p.held_keys
        p.walker.x=410;p.interact();assert p.walker.seated
        for _ in range(60):p.walker.step(1,.05)
        assert p.walker.camera>0 and not p.walker.seated
        p.draw();app.update()
        ImageGrab.grab(window=app.winfo_id()).save(out/'park-main-game.png')
        p.walker.x=830;p.walker.step(0,0);p.interact();p.draw();app.update()
        ImageGrab.grab(window=app.winfo_id()).save(out/'park-main-pond.png')
        app.geometry('1000x720');app.update();p.draw();app.update()
        assert p.photo.width()<=p.canvas.winfo_width()
        ImageGrab.grab(window=app.winfo_id()).save(out/'park-main-small.png')
        p.back_button.invoke();app.update();assert not p.alive and p.timer is None
        assert app.presence_view.winfo_viewable()
        app.phone_window('Maps');app.update()
        app.town_window();app.update();panel=app.town_activity
        assert panel.master is app.play_body and panel.winfo_toplevel() is app
        assert not phone.winfo_viewable() and not phone.dialogs
        panel.refresh();app.update()
        ImageGrab.grab(window=app.winfo_id()).save(out/'location-controls-main.png')
        panel_entry=next(w for w in descendants(panel) if isinstance(w,ttk.Button) and str(w.cget('text')).startswith('Enter park'))
        panel_entry.invoke();app.update();assert isinstance(app.area_view,park_ui.ParkView)
        app.leave_main_area();app.update()
        with patch.object(park_ui,'Renderer',side_effect=OSError('missing asset')):
            app.enter_park();app.update();failed=app.area_view
            assert 'could not be loaded' in failed.status.get()
            audit(failed)
            assert not phone_theme.is_light_surface(failed.canvas,failed.canvas.cget('bg'))
            ImageGrab.grab(window=app.winfo_id()).save(out/'park-main-error.png')
            failed.back_button.invoke()
        app.enter_park();app.update();gate=app.area_view
        gate.walker.x=1510;gate.interact();app.update();assert not gate.alive
        app.enter_park();app.update();conversation_area=app.area_view
        app.state_data['groups']['park-smoke']={'open':True,'channel':'in_person'}
        app.group_selected='park-smoke';app.layout_presence();app.update()
        assert not conversation_area.alive and conversation_area.timer is None
        app.group_selected=False;del app.state_data['groups']['park-smoke'];app.layout_presence()
        import town,artwork
        app.enter_park();app.update();traveller=app.area_view
        town.travel(app.state_data,'public_park');app.render();phone.withdraw();app.update()
        assert not traveller.alive and traveller.timer is None
        assert artwork.scene_art('public_park')=='locations/public_park'
        assert artwork.source_image('locations/public_park').width>=1500
        ImageGrab.grab(window=app.winfo_id()).save(out/'winterfield-commons-artwork.png')
        assert not errors,errors
        app.enter_park();assert app.area_view is None  # Location gate rejects entry elsewhere.
        print('PASS main-screen entry and location controls, no phone dialogs, input, focus, resize, Back/gate/travel cleanup and error state')
    finally:app.sounds.close();app.destroy()
