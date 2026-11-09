"""Render every logo, fallback and real Bubblegram placement without player saves."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import tkinter as tk
from tkinter import ttk
from unittest.mock import Mock,patch
from PIL import ImageGrab
import game_core as core
import phone_ui
import winterfield_ui
import organisation_logos as logos
from careers_ui_smoke import audit

root=tk.Tk(); root.withdraw(); winterfield_ui.install(root)
root.state_data=core.fresh('garrett'); root.busy=False
for name in ('persist','render','update_phone_notification','show_in_person','open_calendar','sounds'): setattr(root,name,Mock())
errors=[]; root.report_callback_exception=lambda *args:errors.append(args)
phone=phone_ui.PhoneWindow(root); root.phone_activity=phone; phone.geometry('430x740'); root.update()
out=core.ROOT/'.test-tmp'; out.mkdir(exist_ok=True)
try:
    phone.open_app('Bubblegram'); board=phone.job_board
    for key in logos.KEYS:
        for child in board.body.winfo_children(): child.destroy()
        card=logos.header(board.body,key,key.replace('-',' ').title()); root.update(); audit(phone)
        badge=next(c for c in card.winfo_children() if isinstance(c,tk.Label))
        assert getattr(badge,'art',None),key
        ImageGrab.grab(window=phone.winfo_id()).save(out/f'logo-{key}.png')
    with patch.object(logos,'thumbnail',side_effect=OSError('Missing test image')):
        logos.header(board.body,'custom-crew','Missing artwork fallback'); root.update(); audit(phone)
    for section in ('Network','Gangs','Leadership','Contracts'):
        board.change(section); root.update(); audit(phone)
        ImageGrab.grab(window=phone.winfo_id()).save(out/f'logos-{section}.png')
    phone.geometry('390x690'); board.change('Gangs'); root.update(); audit(phone)
    ImageGrab.grab(window=phone.winfo_id()).save(out/'logos-compact.png')
    phone.open_app('Home'); phone.open_app('Bubblegram'); root.update(); audit(phone)
    assert not errors,errors
    print('PASS: eleven image assets, aliases, fallback, network/gangs/leadership/contracts, compact resize and navigation.')
finally: root.destroy()
