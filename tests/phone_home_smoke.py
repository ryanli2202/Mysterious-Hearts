"""Exercise placement with real Tk events, without player save writes."""
import sys, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import tkinter as tk
from types import SimpleNamespace
from unittest.mock import Mock
from PIL import ImageGrab
import game_core as core
import phone_home, phone_theme

root = tk.Tk()
root.geometry('430x720+50+50')
root._is_phone = True
phone_theme.install(root)
state = core.fresh('rei')
phone = SimpleNamespace(game=SimpleNamespace(persist=Mock()), open_app=Mock())
errors=[]
root.report_callback_exception=lambda *args: errors.append(args)
frame=tk.Frame(root, bg='#111925'); frame.pack(fill='both',expand=True)
phone_home.home(phone,frame,state)
root.update()
d=state['phone_personalization']

def icon(name):
    return phone.home_icons[phone.visible_home_apps.index(name)]

def tap(widget,x=20,y=20):
    widget.event_generate('<ButtonPress-1>',x=x,y=y)
    widget.event_generate('<ButtonRelease-1>',x=x,y=y)
    root.update()

def slot(index):
    c=phone.home_canvas
    columns=3 if c.winfo_width()<400 else 4
    rows=(d['home_capacity']+columns-1)//columns
    spacing=min(116,max(35,(c.winfo_height()-250)/rows))
    return int((index%columns+.5)*c.winfo_width()/columns),int(110+spacing/2+(index//columns)*spacing)

# Select, navigate to a new page, and place in an explicit empty position.
phone.edit_home(); root.update()
name=d['home_pages'][0][0]
tap(icon(name))
phone.change_home_page(page=phone.home_page_count-1); root.update()
target=d['home_page']
x,y=slot(2); tap(phone.home_canvas,x,y)
assert d['home_pages'][target][2]==name
assert d['home_pages'][0][0] is None
assert not phone.open_app.called
# Swap into the dock, then drag a dock app to an empty position.
tap(icon(name)); tap(icon('Camera'))
assert d['home_dock'][1]==name
assert d['home_pages'][target][2]=='Camera'
source=icon(name)
source.event_generate('<ButtonPress-1>',x=20,y=20)
x,y=slot(1)
phone.home_canvas.event_generate('<B1-Motion>',x=x,y=y)
phone.home_canvas.event_generate('<ButtonRelease-1>',x=x,y=y)
root.update()
assert d['home_pages'][target][1]==name
assert d['home_dock'][1] is None
folder=core.ROOT/'tests'/'screenshots'; folder.mkdir(exist_ok=True)
ImageGrab.grab(window=root.winfo_id()).save(folder/'phone-home-edit.png')
phone.edit_home(); root.update()
layout=json.loads(json.dumps(d['home_pages']))
# Resize and rebuild from JSON-round-tripped save state.
root.geometry('330x570'); root.update()
assert d['home_pages']==layout
frame.destroy(); frame=tk.Frame(root,bg='#111925'); frame.pack(fill='both',expand=True)
state=json.loads(json.dumps(state)); d=state['phone_personalization']
phone_home.home(phone,frame,state); root.update()
assert d['home_pages']==layout
assert d['home_dock'][1] is None
phone.edit_home(); root.update()
ImageGrab.grab(window=root.winfo_id()).save(folder/'phone-home-edit-small.png')
# Long press enters edit mode and never launches the app.
phone.edit_home(); root.update()
source=icon(name)
source.event_generate('<ButtonPress-1>',x=20,y=20)
root.after(650,root.quit); root.mainloop()
phone.home_canvas.event_generate('<ButtonRelease-1>',x=slot(1)[0],y=slot(1)[1]); root.update()
assert not phone.open_app.called
assert not errors, errors
assert phone.game.persist.called
# Drag to the left edge, dwell, then drop on the preceding page.
before=d['home_page']
source=icon(name)
source.event_generate('<ButtonPress-1>',x=20,y=20)
phone.home_canvas.event_generate('<B1-Motion>',x=5,y=220)
root.after(750,root.quit); root.mainloop()
assert d['home_page']==before-1
x,y=slot(0)
phone.home_canvas.event_generate('<ButtonRelease-1>',x=x,y=y); root.update()
assert d['home_pages'][before-1][0]==name
phone.edit_home(); root.update()
tap(icon(name))
phone.open_app.assert_called_once_with(name)
assert not errors, errors
root.destroy()
print('Home placement passed: page moves, dock swaps, drag, resize, save round-trip, long press.')
