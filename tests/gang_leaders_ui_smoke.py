"""Real in-person leadership agenda, new base art, portraits, phone contacts and resize."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from unittest.mock import patch
from PIL import Image, ImageGrab
import game
import game_core as core
import grove
import town
import groups
import job_apps as jobs
import gang_leaders as leaders
import crime_diplomacy as dip
from careers_ui_smoke import audit

with patch.object(game.Game,'check',lambda self:None), \
     patch.object(game.Game,'persist',lambda self:None), \
     patch.object(game.Game,'begin_incoming',lambda self:None), \
     patch.object(grove.GrovePump,'tick',lambda self:None):
    app=game.Game(); errors=[];app.report_callback_exception=lambda *args:errors.append(args)
    out=core.ROOT/'.test-tmp';out.mkdir(exist_ok=True)
    try:
        app.state_data=core.fresh('garrett'); app.play_screen()
        for key,p in leaders.LEADERS.items():
            s=app.state_data=core.fresh('garrett')
            m=dip.book(s,key,2520)
            town.travel(s,m['venue']); s['world']['minute']=m['start']
            gid=dip.begin(s,m['id']);app.select_group(gid);app.show_in_person();app.update()
            assert app.portrait(p['name'],(260,350),outfit='selection') is not None
            assert app.hangout_view.meeting_panel.winfo_ismapped()
            with Image.open(core.ROOT/'assets/ui/locations'/f'{p["base"]}.png') as img:
                assert img.width>img.height and img.width>=1024
            ImageGrab.grab(window=app.winfo_id()).save(out/f'leader-{key}-meeting.png')
            if key=='lantern':
                for _ in range(3): app.hangout_view.meeting_action(dip.discuss,m['id'])
                app.update();assert m['agenda_index']==3
                ImageGrab.grab(window=app.winfo_id()).save(out/'leader-decision-controls.png')
            groups.close_active(s,'End preview');app.show_in_person()
        s=app.state_data=core.fresh('minsu');d=jobs.ensure(s);d.update(reputation=60,completed=12)
        jobs.progression.join(s,'lantern');app.render();app.phone_window();phone=app.phone_activity
        for w,h in ((430,740),(390,690)):
            phone.geometry(f'{w}x{h}');phone.open_thread('npc:Mara Voss',True);app.update();audit(phone)
            assert phone.avatars._avatar('Mara Voss') is not None
            ImageGrab.grab(window=phone.winfo_id()).save(out/f'leader-contact-{w}.png')
        phone.open_app('Bubblegram');phone.job_board.change('Gangs');app.update();audit(phone)
        ImageGrab.grab(window=phone.winfo_id()).save(out/'leaders-gang-directory.png')
        import gang_members
        for width in (430,390):
            phone.geometry(f'{width}x740')
            phone.open_thread('npc:'+gang_members.coworkers(s)[0],True)
            app.update();audit(phone)
            ImageGrab.grab(window=phone.winfo_id()).save(out/f'coworker-contact-{width}.png')
            phone.open_app('Bubblegram');phone.job_board.change('Contracts')
            if not jobs.ensure(s)['pending']: jobs.accept(s,'crew')
            phone.job_board.draw();app.update();audit(phone)
            ImageGrab.grab(window=phone.winfo_id()).save(out/f'coworker-assignment-{width}.png')
        assert not errors,errors
        print('PASS: six rendered bases/leaders, in-person agendas, timer and decisions, membership contact and dark phone resize.')
    finally: app.sounds.close();app.destroy()
