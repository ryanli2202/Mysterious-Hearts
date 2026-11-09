"""Real phone-to-main-window handoff, travel guards, resume and workplace actions."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import json
from unittest.mock import patch
from PIL import ImageGrab
import game
import game_core as core
import grove
import job_apps as jobs
from jobseek_workplace_ui import open_workplace
from careers_ui_smoke import audit

out=core.ROOT/'.test-tmp'; out.mkdir(exist_ok=True)
with patch.object(game.Game,'check'), patch.object(game.Game,'persist'), \
     patch.object(game.Game,'begin_incoming'), patch.object(grove.GrovePump,'tick'):
    app=game.Game(); errors=[]
    app.report_callback_exception=lambda *e:errors.append(e)
    try:
        s=core.fresh('rei'); app.state_data=s
        jobs.apply(s,'barista')
        s['world'].update(location='downtown',minute=600)
        s['world']['cast']['rei'].update(location='downtown',journey=None)
        app.play_screen(); app.update()
        app.phone_window('Jobseek'); app.update()
        phone=app.phone_activity; board=phone.job_board
        board.change('My career'); board.act(jobs.begin_shift)
        assert jobs.ensure(s)['pending'] is None
        assert 'Travel' in board.notice
        audit(phone)
        # Use the actual travel action and advance until arrival.
        jobs.travel(s,'cafe')
        actor=s['world']['cast']['rei']
        import world_loop
        while actor.get('journey'): world_loop.advance(s,1)
        assert s['world']['location']=='cafe'
        board.act(jobs.begin_shift); app.update()
        assert phone.state()=='withdrawn'
        assert app.area_view.winfo_ismapped()
        assert jobs.ensure(s)['pending'] is None, 'Phone handoff must not start the shift'
        workplace=app.area_view.board
        workplace.act(jobs.begin_shift); app.update()
        assert jobs.ensure(s)['pending']['kind']=='shift'
        ImageGrab.grab(window=app.winfo_id()).save(out/'Jobseek-in-person-shift.png')
        audit(app.area_view)
        # Leaving and save/load retain the timed shift, without duplicating it.
        app.leave_main_area(); app.state_data=json.loads(json.dumps(s)); s=app.state_data
        open_workplace(app); app.update(); workplace=app.area_view.board
        before=s['world']['money']; workplace.act(jobs.resolve,1); app.update()
        assert s['world']['money']==before+180
        workplace.act(jobs.resolve,1)
        assert s['world']['money']==before+180
        p=jobs.profile(s,'barista'); p.update(rank=3,mentor=20)
        s['world']['money']=5000
        workplace.change('Development'); workplace.act(jobs.civilian.train,'craft')
        assert p['courses']['craft']==1
        workplace.change('Workplace'); workplace.act(jobs.civilian.network,'mentor')
        assert p['mentor']==30
        workplace.change('Projects'); workplace.act(jobs.civilian.project)
        assert p['project']
        p['project'].update(stages=3,quality=9)
        workplace.act(jobs.civilian.deliver)
        assert p['portfolio'] and p['project'] is None
        workplace.change('Management'); workplace.act(jobs.civilian.manage,'team')
        assert p['budget']==100
        for size in ('1220x940','1000x800'):
            app.geometry(size); app.update(); audit(app.area_view)
            workplace.body.master.yview_moveto(1); app.update()
            ImageGrab.grab(window=app.winfo_id()).save(out/f'Jobseek-in-person-{size}.png')
        # A stale window cannot award work after the player leaves.
        actor=s['world']['cast']['rei']; actor['journey']={'destination':'downtown'}
        before=p['leadership']; workplace.act(jobs.civilian.manage,'quality')
        assert p['leadership']==before and 'Travel' in workplace.notice
        actor['journey']=None
        app.leave_main_area(); app.show_in_person(); app.update()
        assert app.presence_view.winfo_ismapped()
        assert not errors,errors
        print('PASS: real travel, phone handoff without work, main-window activities, saved-shift resume, duplicate/stale guards and two sizes.')
    finally:
        app.sounds.close(); app.destroy()
