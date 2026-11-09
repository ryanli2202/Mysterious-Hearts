"""Real dark phone roster, role popup and main-area recruitment rendering."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import tkinter as tk
from tkinter import ttk
from unittest.mock import Mock
from PIL import ImageGrab
import game_core as core
import phone_ui, winterfield_ui, custom_gangs as cg
from careers_ui_smoke import audit

root=tk.Tk(); root.withdraw(); winterfield_ui.install(root)
root.state_data=core.fresh('minsu'); root.busy=False
for name in ('persist','render','update_phone_notification','show_in_person','open_calendar','sounds','select_group',
             'close_main_area','hide_phone_for_location','layout_presence','leave_main_area'):
    setattr(root,name,Mock())
root.play_body=ttk.Frame(root); root.play_body.pack(fill='both',expand=True)
errors=[]; root.report_callback_exception=lambda *args:errors.append(args)
phone=phone_ui.PhoneWindow(root); root.phone_activity=phone; phone.geometry('430x740')
out=core.ROOT/'.test-tmp'; out.mkdir(exist_ok=True)

def capture(name):
    root.update(); audit(phone)
    ImageGrab.grab(window=phone.winfo_id()).save(out/(name+'.png'))

try:
    phone.open_app('Bubblegram'); board=phone.job_board; board.change('My gang'); capture('custom-gang-directory')
    d=cg.jobs.ensure(root.state_data); d.update(reputation=70,completed=10)
    cg.jobs.gang(root.state_data,'Evening Circle'); board.draw(); capture('custom-gang-founded')
    s=root.state_data; s['world']['minute']=600; venue=cg.location(s,'Gabe Turner')
    s['world']['location']=venue; s['world']['cast']['minsu'].update(location=venue,journey=None)
    s.setdefault('npc_chats',{})['Gabe Turner']=dict(history=[],connection=dict(trust=80,status='friends'))
    board.open_recruit('Gabe Turner')
    assert not cg.crew(s)['members']
    root.deiconify(); root.geometry('1000x500'); root.area_view.pack(fill='both',expand=True); root.update()
    ImageGrab.grab(window=root.winfo_id()).save(out/'custom-gang-in-person.png')
    root.area_view.recruit(); assert 'Gabe Turner' in cg.crew(s)['members']
    root.withdraw(); board.draw(); capture('custom-gang-roles')
    combo=next(c for c in board.body.winfo_children() if isinstance(c,ttk.Combobox))
    board.body.master.yview_moveto(combo.winfo_y()/board.body.winfo_height()); root.update()
    combo.tk.call('ttk::combobox::Post',str(combo)); capture('custom-gang-role-popup')
    combo.tk.call('ttk::combobox::Unpost',str(combo))
    board.act(cg.assign,'Gabe Turner','Quartermaster'); capture('custom-gang-assigned')
    phone.geometry('390x690'); board.body.master.yview_moveto(.5); capture('custom-gang-offers')
    board.act(cg.respond,'Syndicate',True,'Clubs'); assert 'requires' in board.notice.lower() or 'invitation' in board.notice.lower()
    capture('custom-gang-offer-error')
    board.act(cg.respond,'Syndicate'); assert cg.crew(s)['assimilation']['Syndicate']['status']=='declined'
    board.change('Leadership'); capture('custom-gang-relations')
    board.change('My gang'); root.update()
    heading=next(c for c in board.body.winfo_children() if isinstance(c,ttk.Label) and str(c.cget('text')).startswith('Jace Mercer'))
    board.body.master.yview_moveto(heading.winfo_y()/board.body.winfo_height()); capture('street-recruit-directory')
    s['world']['minute']=600; venue=cg.location(s,'Jace Mercer')
    s['world']['location']=venue; s['world']['cast']['minsu'].update(location=venue,journey=None)
    s.setdefault('npc_chats',{})['Jace Mercer']=dict(history=[],connection=dict(trust=65,status='friends'))
    board.open_recruit('Jace Mercer'); root.area_view.recruit()
    assert 'Jace Mercer' in cg.crew(s)['members']
    import phone_numbers
    phone_numbers.ensure(s)
    import groups
    groups.sync_contacts(s)
    phone.open_app('Contacts'); capture('street-recruit-contacts')
    phone.open_app('Home'); root.update(); audit(phone)
    assert not errors,errors
    print('PASS: directory, founding, in-person recruitment, roles and popup, offers/error/decline, founder diplomacy, dark states and resize.')
finally: root.destroy()
