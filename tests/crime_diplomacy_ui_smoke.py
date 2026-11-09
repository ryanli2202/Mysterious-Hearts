"""Leadership desk, meetings, deals, calendar and careers in the real dark phone."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import tkinter as tk
from tkinter import ttk
from unittest.mock import Mock
from PIL import ImageGrab
import game_core as core
import winterfield_ui
import phone_ui
import job_apps as jobs
import crime_diplomacy as dip
from careers_ui_smoke import audit

root=tk.Tk(); root.withdraw(); winterfield_ui.install(root)
root.state_data=core.fresh('garrett'); root.busy=False
for name in ('persist','render','update_phone_notification','show_in_person','open_calendar','sounds'): setattr(root,name,Mock())
errors=[]; root.report_callback_exception=lambda *args:errors.append(args)
phone=phone_ui.PhoneWindow(root); root.phone_activity=phone; phone.geometry('430x740'); root.update()
out=core.ROOT/'.test-tmp'; out.mkdir(exist_ok=True)

def capture(name,heading=None):
    root.update(); board=phone.job_board
    if heading:
        child=next(c for c in board.body.winfo_children() if isinstance(c,ttk.Label) and heading in str(c.cget('text')))
        board.body.master.yview_moveto(child.winfo_y()/max(1,board.body.winfo_height())); root.update()
    audit(phone); ImageGrab.grab(window=phone.winfo_id()).save(out/(name+'.png'))

try:
    phone.open_leadership(); capture('leadership-garrett')
    board=phone.job_board; board.act(dip.request,'waterfront')
    capture('leadership-meeting','Meetings and negotiations')
    b=dip.ensure(root.state_data); m=b['meetings'][-1]
    board.act(dip.begin,m['id']); assert 'Arrive' in board.notice
    capture('leadership-error')
    from calendar_ui import CalendarWindow
    import story_calendar
    cal=CalendarWindow(root); cal.show(story_calendar.story_date(m['start'])); root.update(); audit(phone)
    ImageGrab.grab(window=phone.winfo_id()).save(out/'leadership-calendar.png')
    cal.open_leadership(); root.update(); assert phone.job_board.section=='Leadership'
    s=root.state_data; s['world'].update(location=m['venue'],minute=m['start'],party=[])
    s['world']['cast'][s['player']].update(location=m['venue'],journey=None)
    dip.begin(s,m['id'])
    for _ in range(3): dip.discuss(s,m['id'])
    board=phone.job_board; board.act(dip.conclude,m['id'],'measured')
    capture('leadership-deal','Active deals')
    board.act(dip.settle,b['deals'][0]['id']); assert b['deals'][0]['status']=='completed'
    capture('leadership-outcome')
    from careers_ui import CareersWindow
    career=CareersWindow(root); career.key='dragons'; career.draw(); root.update(); audit(phone)
    career.open_leadership(); root.update(); assert phone.job_board.section=='Leadership'
    for player in ('ivan','minsu'):
        root.state_data=core.fresh(player)
        phone.open_leadership(); capture('leadership-'+player)
    d=jobs.ensure(root.state_data)
    d['membership']=dict(faction='Shinokami',branch='Shinokami',rank=4,strikes=0,assignments=18,sponsor='@moonrelay')
    phone.open_leadership(); phone.geometry('390x690'); capture('leadership-earned')
    phone.open_app('Home'); root.update(); audit(phone)
    assert not errors,errors
    print('PASS: Garrett, Ivan, locked and earned desks, meeting/error/deal/outcome, calendar and career links, dark states and resize.')
finally: root.destroy()
