"""Render all new location images through the game's real Tk artwork loader."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import tkinter as tk
from PIL import ImageGrab
import artwork
import outskirts
import winterfield_ui

root = tk.Tk()
root.title('Winterfield outskirts artwork verification')
root.geometry('1200x820')
winterfield_ui.install(root)
root.configure(bg='#18202d')
errors = []
root.report_callback_exception = lambda *args: errors.append(args)
out = Path(__file__).parent / 'screenshots'
out.mkdir(exist_ok=True)
try:
    for i, (key, data) in enumerate(outskirts.VENUES.items()):
        frame = tk.Frame(root, bg='#18202d')
        frame.grid(row=i//3, column=i%3, sticky='nsew', padx=4, pady=4)
        root.grid_rowconfigure(i//3, weight=1)
        root.grid_columnconfigure(i%3, weight=1)
        tk.Label(frame, text=data[0], bg='#18202d', fg='#dce5ed').pack()
        art = artwork.ArtCanvas(frame, artwork.scene_art(key), height=160)
        art.pack(fill='both', expand=True)
    root.update()
    ImageGrab.grab(window=root.winfo_id()).save(out/'outskirts-art-gallery.png')
    for frame in root.winfo_children():
        art = frame.winfo_children()[1]
        base = art.artwork
        art.set_art((base, 'night', 'Rain'))
    root.update()
    ImageGrab.grab(window=root.winfo_id()).save(out/'outskirts-art-night-rain.png')
    assert not errors, errors
    print('All 12 backgrounds rendered through ArtCanvas in daylight and rainy night states.')
finally:
    root.destroy()
