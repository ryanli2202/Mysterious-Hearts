"""Render wallpapers, Charles's contact photo and six playable Bubblegram desks."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from unittest.mock import patch
from PIL import ImageGrab
import game
import game_core as core
import grove
import job_apps as jobs
import bubblegram_roles
import phone_personalization as personal
from careers_ui_smoke import audit

out = core.ROOT / '.test-tmp'
with patch.object(game.Game, 'check'), patch.object(game.Game, 'persist'), patch.object(game.Game, 'begin_incoming'), patch.object(grove.GrovePump, 'tick'):
    app = game.Game(); errors = []
    app.report_callback_exception = lambda *args: errors.append(args)
    try:
        app.geometry('1100x850')
        for who in core.PLAYERS:
            print('Wallpaper', who, flush=True)
            app.close_main_area(); app.state_data = core.fresh(who)
            app.play_screen(); app.phone_window(); app.update()
            phone = app.phone_activity
            phone.geometry('430x740'); phone.open_app('Home'); app.update()
            assert hasattr(phone.home_canvas, 'background_art'), who
            audit(phone)
            ImageGrab.grab(window=phone.winfo_id()).save(out / ('wallpaper-phone-' + who + '.png'))
        for who in bubblegram_roles.ROLES:
            print('Bubblegram', who, flush=True)
            app.close_main_area(); app.state_data = core.fresh(who)
            app.play_screen(); app.phone_window('Bubblegram'); app.update()
            phone = app.phone_activity; phone.geometry('430x740')
            for section in ('Contracts', 'Network', 'Leadership', 'Reputation'):
                phone.job_board.change(section); app.update(); audit(phone)
            phone.job_board.change('Leadership'); app.update()
            ImageGrab.grab(window=phone.winfo_id()).save(out / ('bubblegram-role-' + who + '.png'))
            phone.job_board.change('Contracts')
            phone.job_board.act(jobs.accept, 'leadership'); app.update()
            before = app.state_data['world']['minute']
            phone.job_board.act(jobs.resolve, 0); app.update()
            assert not phone.winfo_viewable()
            assert app.state_data['world']['minute'] == before
            assert jobs.ensure(app.state_data)['pending']
            panel = app.area_view
            assert panel.master is app.play_body and panel.board.in_person
            destination = jobs.ensure(app.state_data)['pending']['venue']
            for _ in range(3):
                if app.state_data['world']['location'] == destination: break
                jobs.travel(app.state_data, destination)
            panel.board.draw(); app.update()
            audit(panel)
            ImageGrab.grab(window=app.winfo_id()).save(out / ('bubblegram-work-' + who + '.png'))
            panel.board.act(jobs.resolve, 0); app.update()
            assert jobs.ensure(app.state_data)['pending'] is None
        app.close_main_area(); app.state_data = core.fresh('garrett')
        app.play_screen(); app.phone_window(); app.update()
        phone = app.phone_activity; phone.contact_detail('charles'); app.update()
        assert hasattr(phone, 'charles_contact_photo')
        audit(phone)
        ImageGrab.grab(window=phone.winfo_id()).save(out / 'charles-contact-v3-phone.png')
        assert not errors, errors
    finally:
        app.sounds.close(); app.destroy()
print('Passed 26 phone wallpapers, Charles contact detail, six Bubblegram desks and in-person contract routing.')
