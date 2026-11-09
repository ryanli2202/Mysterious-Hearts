"""Capture expanded arcade views for visual review and exercise real timers."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import tkinter as tk
from PIL import Image, ImageGrab, ImageDraw
from mini_games_ui import Arcade
from arcade_extra_ui import EXTRA_ENGINES

root = tk.Tk()
root.geometry('480x630')
root.title('Arcade visual check')
errors = []
root.report_callback_exception = lambda *args: errors.append(args)
arcade = Arcade(root, {})
root.update()
shots = []
for name in EXTRA_ENGINES:
    arcade.open(name)
    root.update()
    if name == 'Memory Match':
        arcade.extra_click(50, 50)
    elif name == 'Minesweeper':
        arcade.extra_click(50, 50)
    elif name == 'Breakout':
        arcade.toggle()
        arcade.action('space')
    elif name == 'Match-3':
        for x, y in arcade.model.legal_moves()[0]: arcade.extra_click((x+.5)*400/7, (y+.5)*400/7)
    elif name == 'Word Search':
        cells = arcade.model.paths[arcade.model.words[0]]
        for x, y in (cells[0], cells[-1]): arcade.extra_click(x*40+20, y*32+16)
    elif name == 'Solitaire': arcade.extra_click(25, 25)
    root.after(900, root.quit)
    root.mainloop()
    shots.append(ImageGrab.grab(window=root.winfo_id()).convert('RGB'))
    arcade.menu()
    assert not arcade.jobs and arcade.timer is None and arcade.animation_timer is None
root.update()
shots.append(ImageGrab.grab(window=root.winfo_id()).convert('RGB'))
root.destroy()
assert not errors, errors
output = Path(__file__).parent / 'screenshots' / 'arcade-expanded.png'
output.parent.mkdir(exist_ok=True)
sheet = Image.new('RGB', (4*360, 2*500), '#141c2e')
for i, shot in enumerate(shots):
    shot.thumbnail((360, 500))
    sheet.paste(shot, (i%4*360, i//4*500))
sheet.save(output)
print(output)
