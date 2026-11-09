"""Exercise convenience screens with fresh in-memory state and no live AI or saves."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from unittest.mock import patch
import tkinter as tk
import game
import game_core as core
import qol_ui
import scheduled_events
from calendar_ui import CalendarWindow
from town_ui import TownWindow
from PIL import ImageGrab

with patch.object(game.Game, 'check'), patch.object(game.Game, 'begin_incoming'), patch.object(core, 'save'):
    app = game.Game()
    app.state_data = core.fresh('rei')
    app.play_screen(); app.update()
    errors=[]
    app.report_callback_exception=lambda *e:errors.append(e)
    app.phone_window('Messages'); phone=app.phone_activity; app.update()
    phone.open_thread('emily'); app.update()
    phone.message_entry.insert(0,'Emily draft')
    phone.open_thread('sophie'); app.update()
    assert phone.message_entry.get() == '', phone.message_entry.get()
    phone.message_entry.insert(0,'Sophie draft')
    phone.open_thread('emily'); app.update()
    assert phone.message_entry.get() == 'Emily draft', app.state_data['drafts']
    phone.close_phone(); app.update()
    app.phone_window('Messages'); phone=app.phone_activity
    phone.open_thread('sophie'); app.update()
    assert phone.message_entry.get() == 'Sophie draft'
    app.pending='Unfinished message'; app.set_busy(True); app.generation_started=__import__('time').monotonic()
    old=app.token; app.cancel_generation(); app.update()
    assert app.token == old+1 and not app.busy and app.pending is None
    assert phone.message_entry.get() == 'Unfinished message'
    state_before = __import__('copy').deepcopy(app.state_data)
    app.events.put(('result',old,'Ignored',{},None)); app.poll()
    assert app.state_data == state_before, 'Cancelled result mutated the story'
    for page in ('Calendar','Settings','Messages'):
        phone.open_app(page); app.update()
    phone.close_phone()
    cal=CalendarWindow(app); cal.plan_event(); app.update()
    out=core.ROOT/'tests'/'screenshots'; out.mkdir(exist_ok=True)
    planner=next(w for w in cal.winfo_children() if isinstance(w,tk.Toplevel))
    ImageGrab.grab(window=planner.winfo_id()).save(out/'event-planner.png')
    form = planner.winfo_children()[0]
    guests = next(w for w in form.winfo_children() if isinstance(w,tk.Listbox))
    guests.selection_set(0,1)
    schedule = next(w for w in form.winfo_children() if str(w.winfo_class()) == 'TButton')
    schedule.invoke(); app.update()
    assert len(app.state_data['scheduled_events']) == 1
    assert len(app.state_data['scheduled_events'][0]['guests']) == 2
    cal.destroy()
    town=TownWindow(app); app.update()
    ImageGrab.grab(window=town.winfo_id()).save(out/'qol-town.png')
    town.destroy()
    qol_ui.overview(app); qol_ui.journal(app); qol_ui.saves(app); app.update()
    assert not errors, errors
    app.sounds.close(); app.destroy()
print('QOL UI smoke passed: drafts, cancellation, calendar, planner, town, overview, search and saves.')
