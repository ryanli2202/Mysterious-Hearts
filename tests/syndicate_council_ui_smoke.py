"""Render council calendar and leadership at phone sizes without touching saves."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import tkinter as tk
from unittest.mock import Mock
from PIL import ImageGrab
import game_core as core
import phone_ui
import calendar_ui
import winterfield_ui
import syndicate_council as council
from careers_ui_smoke import audit

root=tk.Tk(); root.withdraw(); winterfield_ui.install(root)
root.state_data=core.fresh('ivan'); root.busy=False
for name in ('persist','render','update_phone_notification','show_in_person','open_calendar','sounds'):
    setattr(root,name,Mock())
errors=[]; root.report_callback_exception=lambda *args:errors.append(args)
phone=phone_ui.PhoneWindow(root); root.phone_activity=phone; phone.geometry('430x740'); root.update()
out=core.ROOT/'.test-tmp'; out.mkdir(exist_ok=True)
try:
    phone.open_app('Bubblegram'); phone.job_board.change('Network'); root.update(); audit(phone)
    ImageGrab.grab(window=phone.winfo_id()).save(out/'ivan-membership.png')
    phone.job_board.change('Leadership'); root.update(); audit(phone)
    ImageGrab.grab(window=phone.winfo_id()).save(out/'council-leadership.png')
    phone.open_app('Calendar'); root.update(); audit(phone)
    ImageGrab.grab(window=phone.winfo_id()).save(out/'ivan-coming-up.png')
    win=calendar_ui.CalendarWindow(root)
    e=root.state_data['scheduled_events'][0]
    win.show(council.calendar.story_date(e['start'])); root.update(); audit(phone)
    ImageGrab.grab(window=phone.winfo_id()).save(out/'council-calendar.png')
    phone.geometry('390x690'); root.update(); audit(phone)
    assert all(int(label.cget('wraplength'))==188 for label in win._agenda_labels)
    ImageGrab.grab(window=phone.winfo_id()).save(out/'council-calendar-compact.png')
    win._agenda_labels[0].master.master.yview_moveto(.5); root.update(); audit(phone)
    ImageGrab.grab(window=phone.winfo_id()).save(out/'council-calendar-actions.png')
    assert not errors,errors
    print('PASS: council calendar and Bubblegram leadership; dark controls and compact resize.')
finally: root.destroy()
