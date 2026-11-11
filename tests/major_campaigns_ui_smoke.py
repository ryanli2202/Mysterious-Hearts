"""Rendered campaign and dark phone handoff checks; isolated state, no providers."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from unittest.mock import patch
from PIL import ImageGrab
import game, game_core as core, grove, campaign_ui, rei_story, organisation_guards as guards
import combat, phone_theme
from campaign_ui_helpers import finish_script
from tkinter import ttk

def audit(w):
    if isinstance(w,ttk.Widget):
        style=ttk.Style(w);name=str(w.cget('style')) or w.winfo_class()
        if isinstance(w,(ttk.Scrollbar,ttk.Separator)):name=str(w.cget('orient')).title()+'.'+name if name==w.winfo_class() else name
        for option in phone_theme.STYLE_OPTIONS:
            for state in phone_theme.STATES:
                assert not phone_theme.is_light_surface(w,style.lookup(name,option,state)),(name,option,state)
        if isinstance(w,ttk.Combobox):
            popup=w.tk.call('ttk::combobox::PopdownWindow',str(w))
            for opt in ('background','selectbackground'):assert not phone_theme.is_light_surface(w,w.tk.call(str(popup)+'.f.l','cget','-'+opt))
    for child in w.winfo_children():audit(child)

out=core.ROOT/'tests/screenshots';out.mkdir(exist_ok=True)
with patch.object(game.Game,'check'),patch.object(game.Game,'begin_incoming'),patch.object(game.Game,'persist'),patch.object(grove.GrovePump,'tick'):
    app=game.Game();errors=[];app.report_callback_exception=lambda *e:errors.append(e)
    try:
        s=app.state_data=core.fresh('rei');s['world']['time_mode']='paused';app.play_screen();app.update()
        campaign_ui.open_in_person(app,'Rei’s story');v=app.campaign_view
        def shot(name):
            app.update();audit(v);ImageGrab.grab(window=app.winfo_id()).save(out/('major-'+name+'.png'))
        v.act(core.town.travel,'rei_home');shot('rei-opening')
        v.act(rei_story.advance,0);finish_script(app);campaign_ui.open_in_person(app,'Rei’s story');shot('evidence')
        v.act(core.town.travel,'hamayashi_house');v.change('Guards');shot('guards')
        v.act(guards.begin);app.update();assert combat.active(s) and app.combat_view.winfo_viewable()
        combat.concede(s);combat.close(s);app.combat_view.place_forget()
        import job_apps
        job_apps.ensure(s)['gang']=dict(name='Night workshop',role='Founder',rank=0,standing=0,members={})
        s['world']['money']=100000
        v.act(core.town.travel,'crew_lot_west');v.change('Properties');v.act(guards.buy,'crew_lot_west','Hideout');shot('properties')
        v.act(guards.recruit,'Night watch','robotic','crew_lot_west');shot('recruited')
        app.geometry('1000x800');app.update();shot('compact')
        assert v.winfo_rooty()+v.winfo_height()<=app.winfo_rooty()+app.winfo_height()
        v.leave();app.phone_window();phone=app.phone_activity;phone.open_app('Bubblegram');app.update()
        # Exercise the actual Bubblegram Network page, including the themed handoff.
        phone.job_board.change('Network');app.update();audit(phone)
        ImageGrab.grab(window=phone.winfo_id()).save(out/'major-phone.png')
        campaign_ui.open_in_person(app);app.update();assert v.winfo_viewable();assert not phone.winfo_viewable()
        assert not errors,errors
        print('Campaign screens, guard combat, property recruitment, compact layout and dark phone handoff passed.')
    finally:app.sounds.close();app.destroy()
