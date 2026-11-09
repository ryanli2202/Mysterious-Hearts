"""Exercise Game.poll's midnight dispatch with no phone and mocked providers."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import json
import queue
import threading
import time
import tkinter as tk
from unittest.mock import Mock,patch
import game
import game_core as core
import phone_apps as apps
import supafast
from supafast_fixtures import seed,items


def pump(root,predicate,seconds=5):
    end=time.monotonic()+seconds
    while not predicate() and time.monotonic()<end:
        root.update();time.sleep(.02)
    root.update();assert predicate()


def main():
    root=tk.Tk();root.withdraw()
    root.state_data=core.fresh('rei');root.state_data['world']['minute']=1439;seed(root.state_data)
    root.in_game=True;root.busy=False;root.events=queue.Queue()
    root.simulation_clock=Mock();root.simulation_clock.tick.return_value=0
    for name in ('capture_draft','persist','render','update_phone_notification','sounds','notification_popups','poll'):
        setattr(root,name,Mock())
    errors=[];root.report_callback_exception=lambda *e:errors.append(e)
    gate=threading.Event();failure=[False]
    def generate(state,day):
        gate.wait(4)
        if failure[0]:raise RuntimeError('mock offline')
        return items(day)
    photos=Mock()
    with patch.object(supafast,'generate',side_effect=generate) as request,patch.object(supafast,'image_jobs',return_value=photos):
        try:
            # Existing day: no text reroll, and no phone has ever been instantiated.
            game.Game.poll(root);assert request.call_count==0
            def midnight(*args):
                root.state_data['world']['minute']=1440
                return 1
            root.simulation_clock.tick.side_effect=midnight
            game.Game.poll(root)
            pump(root,lambda:request.call_count==1)
            assert request.call_args.args[1]==1
            assert apps.catalog(root.state_data)=={}
            root.simulation_clock.tick.side_effect=None
            for _ in range(4):game.Game.poll(root)
            assert request.call_count==1
            gate.set();pump(root,lambda:bool(apps.catalog(root.state_data)))
            game.Game.poll(root);assert photos.request.call_count==2
            assert apps.ensure(root.state_data)['catalog_ai_day']==1
            root.persist.assert_called()
            # Reopening/loading today's completed save does not request new stock.
            root.state_data=json.loads(json.dumps(root.state_data))
            game.Game.poll(root);assert request.call_count==1
            # Time jumps request the destination day only, not every skipped day.
            root.state_data['world']['minute']=5*1440+480
            game.Game.poll(root);pump(root,lambda:bool(apps.catalog(root.state_data)))
            assert request.call_count==2 and request.call_args.args[1]==5
            # A failed day stays failed until explicit retry or the next day.
            failure[0]=True;root.state_data['world']['minute']=6*1440
            game.Game.poll(root);pump(root,lambda:root.supafast_jobs.status()=='error')
            for _ in range(4):game.Game.poll(root)
            assert request.call_count==3
            failure[0]=False;root.state_data['world']['minute']=7*1440
            game.Game.poll(root);pump(root,lambda:bool(apps.catalog(root.state_data)))
            assert request.call_count==4
            # Start screen does not schedule work, even if an old story remains loaded.
            root.in_game=False;root.state_data['world']['minute']=8*1440
            game.Game.poll(root);assert request.call_count==4
            assert not errors,errors
        finally:
            gate.set();root.destroy()
    print('Midnight refresh passed through Game.poll with no phone: 23:59/00:00, single request, persistence, images, reload, time jumps, failure and inactive game.')

if __name__=='__main__':main()
