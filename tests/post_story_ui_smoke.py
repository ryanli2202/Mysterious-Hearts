"""Render post-story boards, combat states and dark remote administration."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from unittest.mock import patch
from PIL import ImageGrab
import game,game_core as core,grove,post_story as post,campaign_ui,combat,interpol,interpol_ui
from test_post_story import finished
from test_major_campaigns import arrive,win
from careers_ui_smoke import audit

out=core.ROOT/'.test-tmp';out.mkdir(exist_ok=True)
with patch.object(game.Game,'check'),patch.object(game.Game,'persist'),patch.object(game.Game,'begin_incoming'),patch.object(grove.GrovePump,'tick'):
    app=game.Game();errors=[];app.report_callback_exception=lambda *e:errors.append(e)
    def shot(name):
        app.update();ImageGrab.grab(window=app.winfo_id()).save(out/('post-story-'+name+'.png'))
    try:
        app.state_data=s=finished('garrett');s['world']['time_mode']='paused'
        app.play_screen();app.geometry('1000x800');app.update()
        campaign_ui.open_in_person(app,'After the story');view=app.campaign_view
        audit(view);shot('garrett-board')
        view.act(post.begin,'dragon_market');arrive(s,'blackhaven');view.draw();view.act(post.verify)
        view.act(post.fight);app.update();assert combat.active(s)
        combat.concede(s);combat.close(s);app.combat_view.place_forget();view.draw();shot('retry')
        while post.remaining(s):post.fight(s);win(s)
        view.act(post.finish);shot('outcome')
        for route in ('leave','destroyed','lead'):
            app.state_data=s=finished('rei',route);s['world']['time_mode']='paused'
            view.notice=''
            campaign_ui.open_in_person(app,'After the story');audit(view);shot('rei-'+route)
        app.phone_window('Bubblegram');phone=app.phone_activity
        for size in ('440x780','390x690'):
            phone.geometry(size);phone.open_app('Bubblegram');b=phone.job_board
            b.change('Network');app.update();audit(phone)
            buttons=[w for w in b.body.winfo_children() if w.winfo_class()=='TButton']
            next(w for w in buttons if w.cget('text')=='Hamayashi administration').invoke()
            app.update();audit(phone)
            ImageGrab.grab(window=phone.winfo_id()).save(out/('post-story-management-'+size+'.png'))
        b.act(post.manage,'shelter');app.update();audit(phone)
        ImageGrab.grab(window=phone.winfo_id()).save(out/'post-story-management-disabled.png')
        b.act(post.manage,'departures');assert 'One management directive' in b.notice;app.update();audit(phone)
        phone.withdraw();view.place_forget()
        app.state_data=s=core.fresh('fox');interpol.ensure(s)['files']['crow_operation']=dict(complete=True)
        interpol_ui.open_in_person(app);app.interpol_view.change('Operations');app.update();audit(app.interpol_view)
        app.interpol_view.canvas.yview_moveto(0.45);shot('syndicate-operations')
        assert not errors,errors
        print('PASS: protection boards for all endings, retry/outcome, Bubblegram management at two sizes, disabled/error states and post-Night Ledger operations.')
    finally:app.sounds.close();app.destroy()
