"""Exercise the real background worker with a slow mocked response."""
import sys,time,threading
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from unittest.mock import patch
import game,game_core as core,grove,messaging,message_photos

gate=threading.Event()
def generate(s,job):
    if job['who']=='emily': gate.wait(5)
    return dict(bubbles=['A reply from '+job['who']],moment='none',pause_minutes=0)

with patch.object(message_photos.PhotoPump,'tick',lambda self:None), patch.object(game.Game,'check',lambda self:None), patch.object(game.Game,'persist',lambda self:None), patch.object(grove.GrovePump,'tick',lambda self:None), patch.object(game.Game,'begin_incoming',lambda self:None), patch.object(messaging,'generate',side_effect=generate):
    app=game.Game(); errors=[]; app.report_callback_exception=lambda *e:errors.append(e)
    app.state_data=core.fresh('rei'); app.play_screen(); app.update()
    s=app.state_data; start=s['world']['minute']
    app.phone_window('Messages'); phone=app.phone_activity; phone.open_thread('emily'); app.update()
    def pump(done):
        end=time.monotonic()+5
        while not done() and time.monotonic()<end:
            app.update(); time.sleep(.01)
        assert done(), 'UI timed out'
    phone.message_entry.insert(0,'First message'); phone.send_message()
    pump(lambda:app.message_pump.running is not None)
    assert not app.busy
    phone.message_entry.insert(0,'Another thought'); phone.send_message()
    phone.open_thread('sophie'); app.update()
    phone.message_entry.insert(0,'Hello Sophie'); phone.send_message()
    phone.message_entry.insert(0,'Are you free?'); phone.send_message()
    assert s['world']['minute']==start
    assert len(messaging.thread(s,'emily')['pending'])==2
    assert len(messaging.thread(s,'sophie')['pending'])==2
    gate.set()
    pump(lambda:not messaging.thread(s,'emily')['pending'] and not messaging.thread(s,'sophie')['pending'])
    assert s['world']['minute']==start
    assert not errors,errors
    phone.destroy(); app.sounds.close(); app.destroy()
print('Slow background reply, double texts, chat switching, independent delivery and zero clock cost passed.')
