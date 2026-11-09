"""Exercise embedded icon creation, previews, saving and dark popup states."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import tkinter as tk
from tkinter import ttk
from unittest.mock import Mock
from PIL import ImageGrab
import game_core as core
import phone_ui, winterfield_ui, job_apps, gang_icons
from careers_ui_smoke import audit

root=tk.Tk(); root.withdraw(); winterfield_ui.install(root)
root.state_data=core.fresh('minsu'); root.busy=False
for name in ('persist','render','update_phone_notification','sounds'): setattr(root,name,Mock())
errors=[]; root.report_callback_exception=lambda *args:errors.append(args)
phone=phone_ui.PhoneWindow(root); root.phone_activity=phone; phone.geometry('430x800')
out=core.ROOT/'.test-tmp'; out.mkdir(exist_ok=True)

def capture(name):
    root.update(); audit(phone)
    ImageGrab.grab(window=phone.winfo_id()).save(out/(name+'.png'))

try:
    d=job_apps.ensure(root.state_data); d.update(reputation=20,completed=4)
    job_apps.gang(root.state_data,'Night Circle'); g=d['gang']
    phone.open_app('Bubblegram'); board=phone.job_board; board.change('Gang icon')
    editor=board.icon_editor; capture('gang-icon-creator')
    for key,value in dict(shape='Hexagon',symbol='Initials',initials='NC',accent='Amber',background='Midnight').items(): editor['variables'][key].set(value)
    assert 'icon' not in g
    capture('gang-icon-monogram')
    editor['variables']['initials'].set('TOOLONG'); assert str(editor['save']['state'])=='disabled'
    capture('gang-icon-validation')
    editor['variables']['initials'].set('NC'); editor['save'].invoke(); root.update()
    assert g['icon']['initials']=='NC'; assert board.icon_editor['status']['text']=='Saved icon'
    combo=next(c for c in board.body.winfo_children() if isinstance(c,ttk.Combobox))
    combo.tk.call('ttk::combobox::Post',str(combo)); root.update(); audit(phone)
    popup=combo.tk.call('ttk::combobox::PopdownWindow',str(combo))
    import phone_theme
    assert not phone_theme.is_light_surface(combo,combo.tk.call(str(popup)+'.f.l','cget','-background'))
    ImageGrab.grab().save(out/'gang-icon-popup-desktop.png')
    combo.tk.call('ttk::combobox::Unpost',str(combo))
    board.change('My gang'); capture('gang-icon-applied')
    board.change('Leadership'); capture('gang-icon-leadership')
    board.change('Gang icon'); phone.geometry('390x690'); capture('gang-icon-compact')
    board.icon_editor['variables']['accent'].set('Rose'); board.change('My gang'); assert g['icon']['accent']=='Amber'
    board.change('Gang icon'); board.act(gang_icons.reset); assert 'icon' not in g
    phone.open_app('Home'); root.update(); audit(phone)
    assert not errors,errors
    print('PASS: live preview, validation, explicit save, cancel/navigation, reset, dark popup, gang/leadership headers and compact resize.')
finally: root.destroy()
