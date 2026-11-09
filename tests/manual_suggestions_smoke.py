"""Actual Tk workflow with mocked AI: no automatic choices, responsive manual controls."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import json
import time
import threading
from unittest.mock import patch
from PIL import ImageGrab
import game
import game_core as core
import grove
import groups
import messaging


with patch.object(game.Game,'check'), patch.object(game.Game,'begin_incoming'), \
     patch.object(core,'save'), patch.object(grove.GrovePump,'tick'):
    app=game.Game(); app.state_data=core.fresh('rei'); app.play_screen(); app.update()
    errors=[]; app.report_callback_exception=lambda *e:errors.append(e)
    def pump(condition,seconds=5):
        until=time.monotonic()+seconds
        while condition() and time.monotonic()<until:
            app.update(); time.sleep(.01)
        app.update()
        assert not condition(), 'UI request timed out'
    for person in app.state_data['autonomy']['people'].values(): person['next_decision']=10**12
    scene=dict(bubbles=['hi rei'],moment='none',pause_minutes=0,hangout_decision='none',feeling='content',social_event='none')
    with patch.object(core,'request',return_value={'message':{'content':json.dumps(scene)}}) as request:
        app.submit('hello'); core.town.loop.advance(app.state_data,20)
        pump(lambda:bool(messaging.thread(app.state_data,'emily')['pending']))
        assert request.call_count==1
    app.phone_window('Messages'); phone=app.phone_activity; phone.open_thread('emily'); app.update()
    assert app.state_data['routes']['emily']['dialogue']=='hi rei'
    phone.message_entry.insert(0,'A draft'); phone.update_messages()
    assert str(phone.message_send.cget('state'))=='normal', (app.busy,groups.hanging_out_with(app.state_data),app.state_data['world']['cast']['emily'])
    phone.message_entry.delete(0,'end')
    assert not phone.visible_message_choices
    assert all(not b.winfo_ismapped() for b in phone.message_choices)
    phone.set_message_mode(True)
    answer=dict(choices_speaker='Rei Takamura',choices=['How was work?', 'What did you paint?', 'I read today.', 'Anything on your mind?'])
    before=app.state_data['turn'],app.state_data['world']['minute']
    with patch.object(core,'request',return_value={'message':{'content':json.dumps(answer)}}) as request:
        phone.suggest_replies.invoke(); pump(lambda:app.suggestion_job is not None)
        phone.update_messages(); app.update()
        assert request.call_count==1
    assert before==(app.state_data['turn'],app.state_data['world']['minute'])
    assert app.state_data['routes']['emily']['choices']==[]
    assert phone.visible_message_choices==answer['choices']
    with patch.object(app,'submit') as submit:
        phone.message_choices[0].invoke(); submit.assert_called_once_with(answer['choices'][0])
    # A slow suggestion job does not disable the custom composer; cancellation ignores its eventual result.
    gate=threading.Event()
    def delayed(*args,**kwargs):
        gate.wait(4)
        return {'message':{'content':json.dumps(answer)}}
    phone.set_message_mode(False)
    with patch.object(core,'request',side_effect=delayed):
        phone.suggest_replies.invoke(); app.update(); phone.update_messages()
        phone.message_entry.insert(0,'My own reply')
        phone.update_messages()
        assert not app.busy and str(phone.message_send.cget('state'))=='normal'
        phone.suggest_replies.invoke(); gate.set()
        time.sleep(.05); app.update()
        assert app.state_data['routes']['emily']['choices']==[]
        assert phone.message_entry.get()=='My own reply'
    phone.set_message_mode(True); phone.update_messages(); app.update()
    out=core.ROOT/'tests'/'screenshots'; out.mkdir(exist_ok=True)
    ImageGrab.grab(window=phone.winfo_id()).save(out/'manual-suggestions.png')
    phone.close_phone()
    # In-person personal choices are usable even without generating the main set.
    core.town.summon(app.state_data,'emily')
    gid=app.state_data['active_group']; app.show_in_person(); app.update()
    group=app.state_data['groups'][gid]
    group['personal_choices']=answer['choices']; group['suggestions_requested']=['personal']
    app.personal_panel=True; app.render(); app.update()
    with patch.object(app,'submit') as submit:
        app.choices[0].invoke(); submit.assert_called_once_with(answer['choices'][0])
    assert not errors,errors
    app.sounds.close(); app.destroy()
print('Manual suggestions UI passed: response-first, personal-only, custom composer, cancellation and in-person selection.')

