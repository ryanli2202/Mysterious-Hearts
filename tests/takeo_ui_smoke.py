"""Takeo's existing dark phone surfaces, artwork and rank lock; no AI or save writes."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import tkinter as tk
from unittest.mock import Mock
from PIL import ImageGrab
import game_core as core
import winterfield_ui
import phone_ui
import hidden_cast
import takeo
import phone_numbers
from careers_ui_smoke import audit

root=tk.Tk(); root.withdraw(); winterfield_ui.install(root)
root.state_data=core.fresh('rei'); root.busy=False
for name in ('persist','render','update_phone_notification','show_in_person','open_calendar','sounds'):
    setattr(root,name,Mock())
import game
root.photos={}
root.portrait=lambda *args,**kwargs:game.Game.portrait(root,*args,**kwargs)
errors=[]; root.report_callback_exception=lambda *args:errors.append(args)
phone=phone_ui.PhoneWindow(root); root.phone_activity=phone
phone.geometry('430x740');root.update()
out=core.ROOT/'.test-tmp';out.mkdir(exist_ok=True)
try:
    s=root.state_data
    phone.open_app('Bubblegram');phone.job_board.change('Network');root.update();audit(phone)
    ImageGrab.grab(window=phone.winfo_id()).save(out/'takeo-network.png')
    s['world']['location']=takeo.HQ;hidden_cast.mark_met(s,'takeo')
    assert not hidden_cast.contact(s,'takeo')
    s['job_apps']['membership']=dict(faction='Shinokami',branch='Shinokami',rank=6,strikes=0,assignments=38,sponsor='@moonrelay')
    phone_numbers.add(s,phone_numbers.number(s,'takeo'))
    for width,height in ((430,740),(390,690)):
        phone.geometry(f'{width}x{height}')
        phone.contact_detail('takeo');root.update();audit(phone)
        ImageGrab.grab(window=phone.winfo_id()).save(out/f'takeo-contact-{width}.png')
    phone.open_app('Contacts');root.update();audit(phone)
    assert phone.avatars._avatar('takeo') is not None
    ImageGrab.grab(window=phone.winfo_id()).save(out/'takeo-contacts.png')
    assert not errors,errors
    print('PASS: Takeo contact rank lock, profile photo, dark contact details, contacts and compact resize.')
finally:
    root.destroy()
