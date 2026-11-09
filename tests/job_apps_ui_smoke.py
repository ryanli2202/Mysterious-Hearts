"""Real phone rendering, dark controls, actions and resize; no save or AI calls."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import tkinter as tk
from unittest.mock import Mock
from PIL import ImageGrab
import game_core as core
import winterfield_ui
import phone_ui
import job_apps as jobs
from careers_ui_smoke import audit

root=tk.Tk(); root.withdraw(); winterfield_ui.install(root)
root.state_data=core.fresh('rei'); root.busy=False
for name in ('persist','render','update_phone_notification','show_in_person','open_calendar','sounds'): setattr(root,name,Mock())
errors=[]; root.report_callback_exception=lambda *args: errors.append(args)
phone=phone_ui.PhoneWindow(root); root.phone_activity=phone; phone.geometry('430x740'); root.update()
out=core.ROOT/'.test-tmp'; out.mkdir(exist_ok=True)
try:
    for app in ('Jobseek','Bubblegram'):
        phone.open_app(app); root.update(); board=phone.job_board
        sections=('Find jobs','My career','Development','Workplace','Projects','Management','Journal') if app=='Jobseek' else ('Contracts','Network','Gangs','Reputation','Journal')
        for section in sections:
            board.change(section); root.update(); audit(phone)
            ImageGrab.grab(window=phone.winfo_id()).save(out/f'{app}-{section.replace(" ","-")}.png')
        if app=='Jobseek':
            board.act(jobs.apply,'model'); board.change('My career')
            s=root.state_data; s['world'].update(location='studio',minute=600); s['world']['cast']['rei'].update(location='studio',journey=None)
            jobs.begin_shift(s); board.draw(); root.update(); audit(phone)
            ImageGrab.grab(window=phone.winfo_id()).save(out/'Jobseek-decision.png')
            board.act(jobs.withdraw); board.notice='Review requires 3 shifts, 6 craft and 55 reliability.'; board.draw(); root.update(); audit(phone)
            ImageGrab.grab(window=phone.winfo_id()).save(out/'Jobseek-error.png')
            p=jobs.profile(s,'model'); p.update(rank=3,mentor=20)
            s['world']['money']=5000
            jobs.civilian.train(s,'craft')
            jobs.civilian.project(s)
            for section in ('Development','Workplace','Projects','Management'):
                board.change(section); root.update(); audit(phone)
                board.body.master.yview_moveto(.40); root.update()
                ImageGrab.grab(window=phone.winfo_id()).save(out/f'Jobseek-{section}-active.png')
                phone.geometry('390x690'); root.update(); audit(phone)
            p['project'].update(stages=3,quality=9)
            jobs.civilian.deliver(s)
            board.change('Management'); jobs.civilian.manage(s,'team'); board.draw()
            root.update(); audit(phone)
            board.body.master.yview_moveto(1); root.update()
            ImageGrab.grab(window=phone.winfo_id()).save(out/'Jobseek-management-earned.png')
        else:
            board.change('Contracts'); board.act(jobs.accept,'parcel'); root.update(); audit(phone)
            ImageGrab.grab(window=phone.winfo_id()).save(out/'Bubblegram-contract.png')
            board.act(jobs.withdraw)
            d=jobs.ensure(root.state_data); d.update(reputation=55,completed=10,gang=dict(name='Test crew',role='Founder',standing=3))
            d['connections']['Shinokami']=3
            board.act(jobs.sponsor,'Shinokami'); board.change('Network'); root.update(); audit(phone)
            ImageGrab.grab(window=phone.winfo_id()).save(out/'Bubblegram-probation.png')
            d['membership']=dict(faction='Syndicate',branch='Spades',rank=4,assignments=26,strikes=0,sponsor='@spades-liaison')
            d['reputation']=90; board.act(jobs.review); root.update(); audit(phone)
            # Scroll to the earned identity briefing and travel control.
            canvas=board.body.master; canvas.yview_moveto(.38); root.update()
            ImageGrab.grab(window=phone.winfo_id()).save(out/'Bubblegram-executive.png')
        phone.geometry('390x690'); root.update(); audit(phone)
        phone.open_app('Home'); root.update(); audit(phone)
    root.state_data=core.fresh('minsu'); s=root.state_data; d=jobs.ensure(s)
    d.update(reputation=50,completed=10)
    jobs.progression.join(s,'hamayashi')
    s['world']['location']='studio'
    for who in ('minsu','rei'): s['world']['cast'][who].update(location='studio',journey=None)
    phone.open_app('Bubblegram'); board=phone.job_board; board.change('Gangs')
    board.act(jobs.progression.reveal_hamayashi); root.update(); audit(phone)
    ImageGrab.grab(window=phone.winfo_id()).save(out/'Bubblegram-Rei-discovery.png')
    assert d['hamayashi_discovery']['affiliation_known']
    root.state_data=core.fresh('garrett'); phone.open_app('Bubblegram')
    phone.job_board.change('Network'); root.update(); audit(phone)
    ImageGrab.grab(window=phone.winfo_id()).save(out/'Bubblegram-established-leader.png')
    assert not errors,errors
    print('PASS: app navigation, all sections, decisions, error, probation, dark control states and compact resize.')
finally: root.destroy()
