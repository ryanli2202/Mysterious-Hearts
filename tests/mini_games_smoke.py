"""Render every arcade game and exercise timer cleanup without AI or saves."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import tkinter as tk
from PIL import ImageGrab
from mini_games_ui import Arcade, ENGINES

root = tk.Tk()
root.title('Mini Games smoke test')
root.geometry('480x530')
errors = []
root.report_callback_exception = lambda *args: errors.append(args)
arcade = Arcade(root, {})
root.update()
for name in ENGINES:
    arcade.open(name)
    root.update()
    assert arcade.canvas.winfo_height() > 200
    controls = arcade.winfo_children()[-1]
    assert controls.winfo_ismapped()
    assert controls.winfo_y() + controls.winfo_height() <= arcade.winfo_height()
    if name in ('Snake', 'Pong', 'Tetris', 'Breakout'):
        arcade.toggle()
        assert arcade.timer is not None
        arcade.action('up')
        arcade.cancel_timer()
        arcade.tick()
        arcade.toggle()
    elif name == 'Connect 4': arcade.action('4')
    elif name == 'Blackjack': arcade.action('stand')
    elif name == '2048': arcade.action('left')
    elif name == 'Memory Match': arcade.extra_click(50, 50)
    elif name == 'Minesweeper': arcade.extra_click(50, 50)
    elif name == 'Match-3':
        a, b = arcade.model.legal_moves()[0]
        arcade.extra_click((a[0] + .5) * 400 / 7, (a[1] + .5) * 400 / 7)
        arcade.extra_click((b[0] + .5) * 400 / 7, (b[1] + .5) * 400 / 7)
    elif name == 'Solitaire': arcade.extra_click(25, 25)
    root.update()
    arcade.menu()
    assert arcade.timer is None
    assert arcade.animation_timer is None
    assert not arcade.jobs
arcade.open('Tetris')
root.update()
screenshots = Path(__file__).parent / 'screenshots'
screenshots.mkdir(exist_ok=True)
ImageGrab.grab(window=root.winfo_id()).save(screenshots / 'mini-games-tetris.png')
arcade.menu()
root.update()
ImageGrab.grab(window=root.winfo_id()).save(screenshots / 'mini-games-menu.png')
arcade.open('Snake')
arcade.toggle()
arcade.destroy()
root.update()
root.destroy()
assert not errors, errors
print('All thirteen arcade views and timer cleanup passed.')
