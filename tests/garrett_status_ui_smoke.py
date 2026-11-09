"""Render Garrett's authored membership and worker links without player-save writes."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import tkinter as tk
from unittest.mock import Mock
from PIL import ImageGrab
import game_core as core
import phone_ui
import winterfield_ui
from careers_ui_smoke import audit

root=tk.Tk(); root.withdraw(); winterfield_ui.install(root)
root.state_data=core.fresh('garrett'); root.busy=False
for name in ('persist','render','update_phone_notification','show_in_person','open_calendar','sounds','select_group'):
    setattr(root,name,Mock())
errors=[]; root.report_callback_exception=lambda *args:errors.append(args)
phone=phone_ui.PhoneWindow(root); root.phone_activity=phone
out=core.ROOT/'.test-tmp'; out.mkdir(exist_ok=True)
try:
    for size in ('430x740','390x690'):
        phone.geometry(size); phone.open_app('Bubblegram')
        for section in ('Network','Leadership'):
            phone.job_board.change(section); root.update(); audit(phone)
            ImageGrab.grab(window=phone.winfo_id()).save(out/f'garrett-{section}-{size}.png')
        buttons=[c for c in phone.job_board.body.winfo_children() if c.winfo_class()=='TButton']
        button=next(c for c in buttons if c.cget('text')=='Message Mina Cho')
        phone.open_thread=Mock()
        button.invoke(); root.update(); audit(phone)
        phone.open_thread.assert_called_with('npc:Mina Cho',True)
    assert not errors,errors
    print('PASS: Garrett Network, Leadership, worker messaging and compact dark layouts.')
finally:
    root.destroy()
