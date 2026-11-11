"""Real UI controls with a deterministic provider response; no live model calls."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import copy
import json
import time
import threading
import tkinter as tk
from unittest.mock import patch
from tkinter import ttk
from PIL import ImageGrab
import game,game_core as core,grove,groups
import flashback_visits as visits
import flashback_visit_ui as view
from test_flashback_visits import fresh


def descendants(widget):
    for child in widget.winfo_children():
        yield child
        yield from descendants(child)


def response(path,body,**kwargs):
    context=json.loads(body['messages'][1]['content'])
    return {'message':{'content':json.dumps(dict(narration='The school courtyard is quiet around you.',
        lines=[dict(speaker=person['id'],text='Let’s sit together and work on that idea.') for person in context['companions']]))}}


def top_levels(app):
    return {str(w) for w in descendants(app) if isinstance(w,tk.Toplevel)}


def embedded(app,panel,windows):
    assert panel.winfo_viewable() and panel.winfo_toplevel() is app
    assert panel.master is app.play_body and not isinstance(panel,tk.Toplevel)
    assert top_levels(app)==windows,'Flashback opened a separate window'
    assert app.grab_current() is panel
    assert app.clock_label.cget('text')=='Flashback · Present-day time paused'
    assert app.time_button.cget('text')=='Time · Paused ▾'


out=core.ROOT/'tests/screenshots';out.mkdir(exist_ok=True)
with patch.object(game.Game,'check'),patch.object(game.Game,'begin_incoming'),patch.object(game.Game,'persist'),patch.object(grove.GrovePump,'tick'),patch.object(core,'request',side_effect=response):
    app=game.Game();errors=[];app.report_callback_exception=lambda *e:errors.append(e)
    def finish(window):
        until=time.monotonic()+3
        # Use Tk's real event loop while worker threads run. Repeated update()
        # calls cannot service cross-thread font cleanup from garbage collection.
        def check():
            if not window.busy or time.monotonic()>=until:app.quit()
            else:app.after(10,check)
        app.after(0,check);app.mainloop()
        assert not window.busy,(errors,window.results.qsize(),window.status.cget('text'))
    try:
        for who in ('rei','emily','sophie','garrett'):
            s=app.state_data=fresh(who);app.play_screen();app.update()
            app.geometry('1180x940+0+0')
            app.phone_window();app.update()
            windows=top_levels(app)
            before=copy.deepcopy(s['world'])
            buttons=[w for w in descendants(app.presence_view) if isinstance(w,ttk.Button) and str(w.cget('text'))=='Visit flashback area']
            assert len(buttons)==1;buttons[0].invoke();app.update();window=app.flashback_view
            embedded(app,window,windows)
            assert not app.phone_activity.winfo_viewable()
            visit_id=visits.active(s)['id']
            for route in (app.render,app.layout_presence,app.show_in_person,app.phone_window):
                route();app.update()
                assert app.flashback_view is window and visits.active(s)['id']==visit_id
                embedded(app,window,windows)
            assert set(window.canvas.portrait_items)==set(visits.AREAS[visits.area_for(who)]['cast'])
            assert window.canvas.artwork==visits.AREAS[visits.area_for(who)]['background']
            for stem in visits.portraits(s).values():assert any(str(key[2]).endswith(stem+'.png') for key in app.photos)
            window.entry.insert(0,'What should we do after lunch?');window.submit(window.entry.get(),'speak');finish(window)
            assert len(visits.record(s)['history'])==1
            app.update();ImageGrab.grab(window=app.winfo_id()).save(out/f'visit-{who}.png')
            window.canvas.turn_speaker(1);app.update()
            if who!='garrett':
                for key,var in window.selections.items():var.set(key=='marcus')
                window.select();app.update()
                assert set(window.canvas.portrait_items)=={who,'marcus'}
            app.geometry('1000x800+0+0');window.submit('Share a snack','action');finish(window);app.update()
            assert len(visits.record(s)['history'])==2
            if who=='rei':
                release=threading.Event()
                def delayed(*args):
                    release.wait(3)
                    return dict(narration='A late reply.',lines=[dict(speaker='marcus',text='Hello.')])
                with patch.object(visits,'generate',side_effect=delayed):
                    window.submit('Cancel this reply','speak');window.cancel_reply();release.set()
                    until=time.monotonic()+.2
                    while time.monotonic()<until:app.update();time.sleep(.01)
                assert len(visits.record(s)['history'])==2
                window.journal();app.update()
                journal=app.grab_current()
                assert journal is window.journal_view and journal.winfo_toplevel() is app
                assert top_levels(app)==windows
                ImageGrab.grab(window=app.winfo_id()).save(out/'visit-rei-journal.png')
                next(w for w in descendants(journal) if isinstance(w,ttk.Button)).invoke();app.update()
                assert app.grab_current()==window
                window.journal();app.update()
                # Invoked buttons do not guarantee Windows foreground focus.
                window.journal_view.focus_force();app.update()
                app.event_generate('<Escape>');app.update()
                assert window.journal_view is None and visits.active(s)
            ImageGrab.grab(window=app.winfo_id()).save(out/f'visit-{who}-compact.png')
            assert window.entry.winfo_rooty()+window.entry.winfo_height()<=window.winfo_rooty()+window.winfo_height()
            with patch.object(core,'request',side_effect=RuntimeError('Offline test')):
                window.entry.insert(0,'Keep this draft');window.submit(window.entry.get(),'speak');finish(window)
            assert 'Retry' in window.status.cget('text') and window.entry.get()=='Keep this draft'
            assert len(visits.record(s)['history'])==2
            app.update()
            if who=='rei':ImageGrab.grab(window=app.winfo_id()).save(out/'visit-rei-error.png')
            saved=copy.deepcopy(s)
            assert s['world']==before
            window.leave();app.update();assert not visits.active(s)
            assert app.flashback_view is None and app.grab_current() is None
            assert app.presence_view.winfo_viewable()
            # Resume the saved active visit through normal game rendering.
            app.state_data=saved;app.play_screen();app.update();window=app.flashback_view
            embedded(app,window,set())
            assert len(visits.record(saved)['history'])==2
            # Rebuilding a loaded visit must cancel the old UI's poll and job.
            if who=='rei':
                release=threading.Event();done=threading.Event()
                def delayed_reload(*args):
                    release.wait(3);done.set()
                    return dict(narration='A discarded reply.',lines=[dict(speaker='marcus',text='Hello.')])
                with patch.object(visits,'generate',side_effect=delayed_reload):
                    window.submit('Rebuild during this reply','speak')
                    app.update()
                    assert str(window.entry.cget('state'))=='disabled'
                    ImageGrab.grab(window=app.winfo_id()).save(out/'visit-rei-pending.png')
                    app.play_screen();app.update()
                    assert window.closed and window.poll_id is None and window.job is None
                    release.set();assert done.wait(3)
                window=app.flashback_view
                embedded(app,window,set())
                assert len(visits.record(saved)['history'])==2
            window.entry.focus_force();app.update()
            app.event_generate('<Escape>');app.update();assert not visits.active(saved)
        # The hangout entry uses the same main window and restores the party.
        s=app.state_data=fresh('rei');s['world']['time_mode']='paused'
        for who in ('rei','emily'):s['world']['cast'][who].update(location=s['world']['location'],journey=None)
        s['world']['party']=['emily'];gid=groups.open_solo(s,'emily')
        app.play_screen();app.update();hangout=app.hangout_view
        assert hangout.winfo_viewable()
        next(w for w in descendants(hangout.header) if isinstance(w,ttk.Button) and str(w.cget('text'))=='Visit flashback area').invoke()
        app.update();embedded(app,app.flashback_view,set())
        app.flashback_view.leave();app.update()
        assert app.hangout_view is hangout and hangout.winfo_viewable() and s['active_group']==gid
        assert set(hangout.canvas.portrait_items)=={'rei','emily'}
        s=app.state_data=fresh('ivan');app.play_screen();app.update()
        assert not any(isinstance(w,ttk.Button) and str(w.cget('text'))=='Visit flashback area' for w in descendants(app.presence_view))
        assert view.open_in_person(app) is None
        assert not errors,errors
        print('PASS: main-window visits and journal without new top-level windows; both entry buttons; four protagonists; historical cast, selection, speaking/actions, paging, compact layout, cancel/error drafts, unchanged time, saved resume, rebuild cleanup, Escape/return and excluded-player access. Provider mocked.')
    finally:
        if getattr(app,'flashback_view',None) is not None:app.flashback_view.leave()
        app.sounds.close();app.destroy()
