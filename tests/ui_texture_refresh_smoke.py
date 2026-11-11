"""MH-008: reachable phone chrome and textured layout without player saves."""
import sys
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from PIL import ImageGrab
import game
import game_core as core
import grove
import winterfield_ui as ui

out = core.ROOT / 'tests' / 'screenshots'
out.mkdir(exist_ok=True)
with patch.object(game.Game, 'check'), patch.object(game.Game, 'begin_incoming'), \
        patch.object(game.Game, 'persist'), patch.object(grove.GrovePump, 'tick'):
    app = game.Game()
    errors = []
    app.report_callback_exception = lambda *args: errors.append(args)
    try:
        app.state_data = core.fresh('rei')
        app.state_data['world']['time_mode'] = 'paused'
        app.play_screen()
        app.update()
        app.phone_window()
        phone = app.phone_activity
        app.update()
        for size in ('360x720', '560x800'):
            phone.geometry(size)
            phone.open_app('Mysterious Hearts')
            app.update()
            for widget in (phone.home_button, phone.app_title):
                assert widget.winfo_ismapped()
                assert widget.winfo_width() > 20
                assert widget.winfo_rootx() >= phone.winfo_rootx()
                assert widget.winfo_rootx() + widget.winfo_width() <= phone.winfo_rootx() + phone.winfo_width()
            phone.home_button.focus_force()
            phone.home_button.event_generate('<Enter>')
            app.update()
            ImageGrab.grab(window=phone.winfo_id()).save(out / f'texture-phone-title-{size}.png')
            phone.home_button.invoke()
            app.update()
            assert phone.selected == 'Home'
            ImageGrab.grab(window=phone.winfo_id()).save(out / f'texture-phone-home-{size}.png')
        assert len(ui.surface_texture(60, 60).getcolors()) > 1
        assert not errors, errors
    finally:
        app.sounds.close()
        app.destroy()
print('Textured UI passed: compact/wide phone chrome, long title and Home navigation.')
