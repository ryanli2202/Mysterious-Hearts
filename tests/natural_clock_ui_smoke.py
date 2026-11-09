"""Native Tk smoke test with offline AI: live clock, drafts, travel and midnight."""
import sys
import time
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import game
import game_core as core
import grove
import messaging

def pump(app, predicate):
    deadline=time.monotonic()+8
    while not predicate() and time.monotonic()<deadline:
        app.update()
        time.sleep(.01)
    assert predicate(),'UI clock did not reach the expected state'

with patch.object(game.Game,'check',lambda self:None), \
     patch.object(game.Game,'persist',lambda self:None), \
     patch.object(game.Game,'begin_incoming',lambda self:None), \
     patch.object(grove.GrovePump,'tick',lambda self:None), \
     patch.object(messaging,'generate',return_value=dict(bubbles=['A live reply.'],moment='none',pause_minutes=0)):
    app=game.Game(); app.withdraw(); errors=[]
    app.report_callback_exception=lambda *error:errors.append(error)
    try:
        app.state_data=core.fresh('rei'); app.play_screen(); app.update()
        state=app.state_data
        assert app.time_mode.get()=='normal'
        time_menu=app.nametowidget(app.time_button.cget('menu'))
        time_menu.invoke(0)
        assert state['world']['time_mode']=='slow'
        assert '0.5×' in app.time_button.cget('text')
        from PIL import ImageGrab
        app.deiconify(); app.update()
        time_menu.post(app.time_button.winfo_rootx(),
                       app.time_button.winfo_rooty()+app.time_button.winfo_height())
        app.update()
        screenshot=Path(__file__).resolve().parent/'screenshots'/'half_speed_menu.png'
        screenshot.parent.mkdir(exist_ok=True)
        ImageGrab.grab().save(screenshot)
        time_menu.unpost(); app.withdraw()
        app.busy=True
        time_menu.invoke(4)
        assert state['world']['time_mode']=='paused'
        assert 'Paused' in app.time_button.cget('text')
        paused_minute=state['world']['minute']
        app.simulation_clock.last=time.monotonic()-600
        app.poll()
        assert state['world']['minute']==paused_minute
        time_menu.invoke(3)
        assert state['world']['time_mode']=='faster'
        time_menu.invoke(2)
        assert state['world']['time_mode']=='fast'
        app.busy=False
        app.phone_window('Messages'); phone=app.phone_activity; phone.open_thread('emily'); app.update()
        phone.message_entry.insert(0,'An unfinished draft')
        start=state['world']['minute']
        app.busy=True; app.pending='An in-progress scene'
        app.generation_started=time.monotonic()
        pump(app,lambda:state['world']['minute']>=start+2)
        assert phone.message_entry.get()=='An unfinished draft'
        assert app.pending=='An in-progress scene'
        app.busy=False; app.pending=None
        core.town.travel(state,'home')
        assert state['world']['location']=='rei_home'
        assert state['world']['cast']['rei']['journey'] is None
        phone.message_entry.delete(0,'end')
        phone.message_entry.insert(0,'Hello Emily'); phone.send_message()
        pump(app,lambda:state['routes']['emily']['dialogue']=='A live reply.')
        state['world']['minute']=1439; state['world']['clock_fraction']=0
        app.simulation_clock.reset(state)
        pump(app,lambda:state['world']['minute']==1440)
        assert '00:00' in app.clock_label.cget('text')
        import autonomy_ui
        controls=autonomy_ui.open_window(app)
        def find_button(widget,text):
            for child in widget.winfo_children():
                if child.winfo_class()=='TButton' and child.cget('text')==text: return child
                found=find_button(child,text)
                if found: return found
        find_button(controls,'Sleep').invoke()
        find_button(controls,'Faster · 12×').invoke()
        assert state['world']['sleep_speed']==12
        until=state['autonomy']['people']['rei']['sleep_until']
        find_button(controls,'Skip to waking').invoke()
        assert state['world']['minute']==until
        assert state['world']['sleep_speed']==1
        assert str(find_button(controls,'Skip to waking').cget('state'))=='disabled'
        controls.destroy()
        assert not errors,errors
    finally:
        if getattr(app,'phone_activity',None): app.phone_activity.destroy()
        app.sounds.close(); app.destroy()
print('Live Tk clock, AI-busy ticks, drafts, travel, queued reply, midnight and sleep speed/skip controls passed.')
