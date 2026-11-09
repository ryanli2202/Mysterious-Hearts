"""Native UI regression with mocked AI and disposable in-memory state."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from unittest.mock import patch
from PIL import ImageGrab
import game
import game_core as core
import grove
import messaging
import autonomy
import autonomy_ui

with patch.object(game.Game,'check',lambda self:None), patch.object(game.Game,'persist',lambda self:None), patch.object(grove.GrovePump,'tick',lambda self:None), patch.object(messaging.MessagePump,'tick',lambda self:None), patch.object(game.Game,'begin_incoming',lambda self:None):
    app=game.Game(); errors=[]
    app.report_callback_exception=lambda *error:errors.append(error)
    app.state_data=core.fresh('rei'); app.play_screen(); app.update()
    app.phone_window('Messages'); phone=app.phone_activity; app.update()
    phone.open_thread('emily'); app.update()
    phone.message_entry.insert(0,'Hello Emily'); phone.send_message(); app.update()
    phone.message_entry.insert(0,'One more thing'); phone.send_message(); app.update()
    phone.open_thread('sophie'); app.update()
    phone.message_entry.insert(0,'How was training?'); phone.send_message(); app.update()
    assert not app.busy
    assert len(messaging.thread(app.state_data,'emily')['pending'])==2
    assert len(messaging.thread(app.state_data,'sophie')['pending'])==1
    phone.open_thread('emily'); app.update()
    rows=phone.phone_messages.messages
    assert any('Read' in row for row in rows),rows
    assert app.state_data['world']['minute']==8*60
    assert 'No time cost' in app.reply_heading.cget('text')
    out=core.ROOT/'tests'/'screenshots'; out.mkdir(exist_ok=True)
    ImageGrab.grab(window=phone.winfo_id()).save(out/'autonomy-messages.png')
    win=autonomy_ui.open_window(app); app.update()
    ImageGrab.grab(window=win.winfo_id()).save(out/'autonomy-needs.png')
    assert not errors,errors
    win.destroy(); phone.destroy(); app.destroy()
print('Native messages: double text, switch chats, delivered receipts and needs controls passed. No saves or live AI used.')
