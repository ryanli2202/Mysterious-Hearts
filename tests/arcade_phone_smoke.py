"""Exercise every arcade view inside the actual phone, without AI or saves."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from unittest.mock import patch
import game
import game_core as core
import grove
from mini_games_ui import ENGINES, REALTIME

with patch.object(game.Game, 'check', lambda self: None), \
     patch.object(game.Game, 'persist', lambda self: None), \
     patch.object(grove.GrovePump, 'tick', lambda self: None), \
     patch.object(game.Game, 'begin_incoming', lambda self: None):
    app = game.Game()
    errors = []
    app.report_callback_exception = lambda *args: errors.append(args)
    app.state_data = core.fresh('rei')
    app.play_screen()
    app.phone_window()
    phone = app.phone_activity
    phone.geometry('560x680')
    phone.open_app('Mini Games')
    app.update()
    arcade = phone.screen.winfo_children()[0].winfo_children()[0]
    assert arcade.sounds is app.sounds
    for name in ENGINES:
        arcade.open(name)
        app.update()
        assert arcade.canvas.winfo_height() > 150, name
        controls = arcade.winfo_children()[-1]
        assert controls.winfo_ismapped(), name
        assert controls.winfo_y() + controls.winfo_height() <= arcade.winfo_height(), name
        if name in REALTIME: arcade.toggle()
        elif name == 'Memory Match': arcade.extra_click(50, 50)
        elif name == 'Simon Says': arcade.simon_play()
        arcade.menu()
        assert not arcade.jobs and arcade.timer is None and arcade.animation_timer is None
    arcade.open('Simon Says')
    phone.open_app('Home')
    app.update()
    assert not arcade.winfo_exists()
    assert not arcade.jobs
    phone.close_phone()
    app.sounds.close()
    app.destroy()
    assert not errors, errors
print('All 13 games passed actual-phone layout and lifecycle checks.')
