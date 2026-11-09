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

with patch.object(game.Game,'check',lambda self:None), patch.object(game.Game,'persist',lambda self:None), patch.object(game.Game,'begin_incoming',lambda self:None), patch.object(grove.GrovePump,'tick',lambda self:None):
    app=game.Game();errors=[];app.report_callback_exception=lambda *args:errors.append(args)
    try:
        s=app.state_data=core.fresh('ivan');town.travel(s,'glasshouse_lab');town.meet(s,'charles')
        app.play_screen();app.show_in_person();app.update()
        out=core.ROOT/'.test-tmp';out.mkdir(exist_ok=True)
        ImageGrab.grab(window=app.winfo_id()).save(out/'charles-laboratory.png')
        town.end_hangouts(s);app.phone_window();phone=app.phone_activity
        for width,height in ((430,740),(390,690)):
            phone.geometry(f'{width}x{height}');phone.open_app('Contacts');phone.contact_detail('charles')
            app.update();audit(phone)
            assert phone.avatars._avatar('charles') is not None
            ImageGrab.grab(window=phone.winfo_id()).save(out/f'charles-profile-{width}.png')
        assert not errors,errors
        print('PASS: main-character lab scene, supplied portrait, phone contact and compact dark profile.')
    finally: app.sounds.close();app.destroy()
