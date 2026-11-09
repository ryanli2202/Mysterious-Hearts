"""Render earned US command contact and portrait using real dark phone UI."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from unittest.mock import patch
from PIL import ImageGrab
import game
import game_core as core
import grove
import town
import groups
import thirteen
import job_apps as jobs
import crime_operations as ops
from test_keisuke import join
from careers_ui_smoke import audit

with patch.object(game.Game,'check',lambda self:None), \
     patch.object(game.Game,'persist',lambda self:None), \
     patch.object(game.Game,'begin_incoming',lambda self:None), \
     patch.object(grove.GrovePump,'tick',lambda self:None):
    app=game.Game();errors=[];app.report_callback_exception=lambda *args:errors.append(args)
    try:
        s=app.state_data=core.fresh('rei');join(s)
        d=jobs.ensure(s);d['membership'].update(rank=3,assignments=18);d['reputation']=80;jobs.review(s)
        town.end_hangouts(s);town.travel(s,'site_02');ops.enter(s,'site_02','reception');ops.enter(s,'site_02','briefing')
        town.meet(s,'thirteen');app.play_screen();app.show_in_person();app.update()
        out=core.ROOT/'.test-tmp';out.mkdir(exist_ok=True)
        ImageGrab.grab(window=app.winfo_id()).save(out/'thirteen-command.png')
        town.end_hangouts(s);app.phone_window();phone=app.phone_activity
        for width,height in ((430,740),(390,690)):
            phone.geometry(f'{width}x{height}');phone.open_app('Contacts');phone.contact_detail('thirteen')
            app.update();audit(phone)
            assert phone.avatars._avatar('thirteen') is not None
            ImageGrab.grab(window=phone.winfo_id()).save(out/f'thirteen-profile-{width}.png')
        phone.open_app('Bubblegram');phone.job_board.change('Network');app.update();audit(phone)
        phone.job_board.body.master.yview_moveto(.28);app.update()
        ImageGrab.grab(window=phone.winfo_id()).save(out/'thirteen-network.png')
        assert not errors,errors
        print('PASS: Executive unlock, command portrait, profile photo, dark profile/Network and compact resize.')
    finally:
        app.sounds.close();app.destroy()
