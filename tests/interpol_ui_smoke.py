"""Real desktop and dark phone checks; no provider requests or story writes."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from unittest.mock import patch
import tkinter as tk
from tkinter import ttk
from PIL import ImageGrab
import game
import game_core as core
import grove
import interpol as law
import interpol_ui
import combat
import combat_ui
import phone_theme
from campaign_ui_helpers import finish_script


def audit(w):
    if isinstance(w,ttk.Widget):
        style=ttk.Style(w);name=str(w.cget('style')) or w.winfo_class()
        if isinstance(w,(ttk.Scrollbar,ttk.Scale,ttk.Progressbar,ttk.Separator)) and name==w.winfo_class():name=str(w.cget('orient')).title()+'.'+name
        for option in phone_theme.STYLE_OPTIONS:
            for state in phone_theme.STATES:
                assert not phone_theme.is_light_surface(w,style.lookup(name,option,state)),(name,option,state)
        if isinstance(w,ttk.Combobox):
            popup=w.tk.call('ttk::combobox::PopdownWindow',str(w))
            for option in ('background','selectbackground'):
                assert not phone_theme.is_light_surface(w,w.tk.call(str(popup)+'.f.l','cget','-'+option))
    else:
        for option in phone_theme.SURFACE_OPTIONS:
            if option in w.keys():assert not phone_theme.is_light_surface(w,w.cget(option)),(str(w),option)
    for child in w.winfo_children():audit(child)


out=core.ROOT/'tests/screenshots';out.mkdir(exist_ok=True)
with patch.object(game.Game,'check'),patch.object(game.Game,'begin_incoming'),patch.object(game.Game,'persist'),patch.object(grove.GrovePump,'tick'):
    app=game.Game();errors=[];app.report_callback_exception=lambda *e:errors.append(e)
    def shot(name,window=None):
        app.update();ImageGrab.grab(window=(window or app).winfo_id()).save(out/('interpol-'+name+'.png'))
    try:
        app.start_screen.select('fox');app.update();app.start_screen.preview.render();shot('fox-selection')
        app.start_screen.select('gordon');app.update();app.start_screen.preview.render();shot('gordon-selection')
        app.state_data=s=core.fresh('fox');s['world']['time_mode']='paused'
        app.play_screen();app.update();shot('fox-home')
        interpol_ui.open_in_person(app);view=app.interpol_view;app.update()
        assert view.master is app.presence_view.master
        assert view.winfo_viewable()
        view.act(core.town.travel,'interpol_hq')
        s['world']['cast']['gordon'].update(location='interpol_hq',journey=None,activity='Receiving reports')
        view.act(law.begin,'blackhaven');view.act(law.travel_objective);view.act(law.advance)
        finish_script(app);interpol_ui.open_in_person(app)
        shot('casework');audit(view)
        view.act(law.advance);finish_script(app);interpol_ui.open_in_person(app)
        view.act(law.advance);finish_script(app);app.update()
        assert combat.active(s) and app.combat_view.winfo_viewable()
        shot('field-combat')
        combat.concede(s);combat.close(s);app.combat_view.place_forget()
        interpol_ui.open_in_person(app)
        view.change('Law & fines');shot('law')
        s['world']['cast']['emily'].update(location=s['world']['location'],journey=None,activity='Walking')
        law.record_offence(s,'assault','emily',event_id='ui-smoke-assault')
        view.change('Organisation');shot('organisation');audit(view)
        app.geometry('1000x800');app.update();view.change('Cases');shot('compact')
        assert view.winfo_rooty()+view.winfo_height()<=app.winfo_rooty()+app.winfo_height()
        view.leave();app.phone_window();phone=app.phone_activity;phone.geometry('440x780')
        for page in ('Bubblegram','Pocket Wallet','Grove','Contacts','Maps'):
            phone.open_app(page);app.update();audit(phone);shot('phone-'+page.lower().replace(' ','-'),phone)
        phone.open_app('Contacts');phone.contact_detail('gordon');app.update();audit(phone);shot('gordon-contact',phone)
        phone.contact_detail('fox');app.update();audit(phone);shot('fox-contact',phone)
        assert not any(j['author']=='fox' for j in s['phone_apps'].get('grove_pending',[]))
        assert not any(j['author']=='fox' for j in s['phone_apps'].get('grove_photo_pending',[]))
        phone.withdraw();view.place_forget()
        for venue in ('blackhaven','fox_hideout','gordon_apartments','gordon_home','interpol_briefing','interpol_training','interpol_containment'):
            s['world']['location']=venue
            s['world']['cast']['fox'].update(location=venue,journey=None,activity='Available')
            app.render();app.update();shot('location-'+venue)
        assert not errors,errors
    finally:app.sounds.close();app.destroy()
print('Interpol UI smoke passed: portraits, casework, combat, records, compact layout, dark phone states and contact photos. No provider calls or story writes.')
