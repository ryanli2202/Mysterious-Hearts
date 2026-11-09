"""Render all career paths in the real phone; no AI calls or story save writes."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import tkinter as tk
from tkinter import ttk
from unittest.mock import Mock
from PIL import ImageGrab
import game_core as core
import careers
from careers_ui import CareersWindow
import phone_ui
import phone_theme
import winterfield_ui


def audit(widget):
    if isinstance(widget,ttk.Widget):
        style=ttk.Style(widget); name=str(widget.cget('style')) or widget.winfo_class()
        if isinstance(widget,ttk.Scrollbar) and name==widget.winfo_class(): name=str(widget.cget('orient')).title()+'.'+name
        for option in phone_theme.STYLE_OPTIONS:
            for state in phone_theme.STATES:
                assert not phone_theme.is_light_surface(widget,style.lookup(name,option,state)),(name,option,state)
        if isinstance(widget,ttk.Combobox):
            popup=widget.tk.call('ttk::combobox::PopdownWindow',str(widget))
            for option in ('background','selectbackground'):
                assert not phone_theme.is_light_surface(widget,widget.tk.call(str(popup)+'.f.l','cget','-'+option))
    else:
        for option in phone_theme.SURFACE_OPTIONS:
            if option in widget.keys(): assert not phone_theme.is_light_surface(widget,widget.cget(option)),(widget,option)
    for child in widget.winfo_children(): audit(child)


def main():
    root=tk.Tk(); root.withdraw(); winterfield_ui.install(root)
    root.state_data=core.fresh('rei'); root.busy=False
    for name in ('persist','render','update_phone_notification','show_in_person','open_calendar','sounds'):
        setattr(root,name,Mock())
    errors=[]; root.report_callback_exception=lambda *args:errors.append(args)
    phone=phone_ui.PhoneWindow(root); root.phone_activity=phone
    phone.geometry('430x740'); root.update()
    output=core.ROOT/'.test-tmp'; output.mkdir(exist_ok=True)
    try:
        for player in ('rei','garrett','ivan','minsu'):
            root.state_data=core.fresh(player)
            window=CareersWindow(root); root.update()
            assert window.phone is phone
            for key in careers.available(root.state_data):
                window.key=key
                for section in ('Work','Project','Schedule','People','History'):
                    window.section=section; window.draw(); root.update(); audit(window.shell)
                window.section='Project'; careers.start_project(root.state_data,key); window.draw(); root.update()
                if key in ('iron','taekwondo'):
                    ImageGrab.grab(window=phone.winfo_id()).save(output/('careers-'+key+'.png'))
            window.destroy(); root.update()
        for key in careers.CRIME_SITUATIONS:
            root.state_data=core.fresh(careers.TRACKS[key]['player']); s=root.state_data
            spec=careers.TRACKS[key]
            s['world']['location']=spec['venue']; s['world']['minute']=spec['hours'][0]*60
            s['world']['cast'][s['player']].update(location=spec['venue'],journey=None)
            window=CareersWindow(root); window.key=key; careers.begin(s,key)
            for index in range(3):
                careers.ensure(s)['active']['scenario']=index
                window.draw(); root.update(); audit(window.shell)
                ImageGrab.grab(window=phone.winfo_id()).save(output/f'careers-crime-{key}-{index}.png')
            window.destroy(); root.update()
        root.state_data=core.fresh('rei'); s=root.state_data
        s['world']['location']='studio'; s['world']['minute']=9*60
        s['world']['cast']['rei'].update(location='studio',journey=None)
        window=CareersWindow(root); window.act(careers.begin,'modelling'); root.update()
        audit(window.shell); ImageGrab.grab(window=phone.winfo_id()).save(output/'careers-decision.png')
        window.act(careers.choose,0); window.act(careers.choose,1); root.update()
        assert careers.get(s,'modelling')['last_day']==0
        window.act(careers.begin,'modelling'); root.update(); assert 'already worked' in window.notice
        audit(window.shell); ImageGrab.grab(window=phone.winfo_id()).save(output/'careers-error.png')
        window.section='Schedule'; window.draw(); root.update()
        window.save_booking(); root.update()
        assert careers.ensure(s)['bookings']
        window.replacing=careers.ensure(s)['bookings'][0]['id']; window.draw(); root.update(); audit(window.shell)
        # Real popup, selected/focus state and compact resizing.
        window.track_box.focus_set(); window.tk.call('ttk::combobox::Post',str(window.track_box)); root.update()
        audit(window.shell)
        ImageGrab.grab(bbox=(phone.winfo_rootx(),phone.winfo_rooty(),phone.winfo_rootx()+phone.winfo_width(),phone.winfo_rooty()+phone.winfo_height())).save(output/'careers-dropdown.png')
        window.tk.call('ttk::combobox::Unpost',str(window.track_box)); phone.geometry('390x690'); root.update(); audit(window.shell)
        window.destroy()
        from calendar_ui import CalendarWindow
        cal=CalendarWindow(root); cal.show(__import__('story_calendar').story_date(careers.ensure(s)['bookings'][0]['start']))
        root.update(); audit(cal.shell); ImageGrab.grab(window=phone.winfo_id()).save(output/'careers-calendar.png')
        cal.destroy()
        from activity_ui import HomeWindow
        s['career_keepsakes']=[dict(title='Editorial campaign',outcome='Successful review.',track='modelling',minute=s['world']['minute'])]
        home=HomeWindow(root); root.update(); audit(home.shell)
        assert 'Editorial campaign' in home.journal.get('1.0','end')
        ImageGrab.grab(window=phone.winfo_id()).save(output/'careers-home.png'); home.destroy()
        assert not errors,errors
        print('PASS: eight paths, five sections, decisions, duplicate error, booking, rescheduling, dropdown, resize and calendar; dark states audited.')
        print('Screenshots:',output)
    finally:
        root.destroy()


if __name__=='__main__': main()
