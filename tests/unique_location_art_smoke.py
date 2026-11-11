"""Verify distinct room assets and render them through the real Tk scene loader."""
import hashlib
import json
from pathlib import Path
import sys
import tkinter as tk

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from PIL import Image, ImageGrab
import artwork
import town
import winterfield_ui

ROOT = Path(__file__).resolve().parents[1]
assets = json.loads((ROOT / 'assets/ui/locations/unique-rooms-prompts.json').read_text())['assets']
assert len(assets) == 23
hashes = set()
for spec in assets:
    key = spec['key']
    name = artwork.scene_art(key)
    assert name == 'locations/' + key, (key, name)
    assert artwork.scene_art(key, texting=True) == 'ui-header'
    assert artwork.scene_art(key, minute=720)[0] == name
    with Image.open(ROOT / spec['destination']) as im:
        assert im.width >= 1500 and im.height >= 1000
        hashes.add(hashlib.sha256(im.tobytes()).hexdigest())
assert len(hashes) == 23, 'Duplicate backgrounds'
for key in town.LOCATIONS:
    if key == 'home' or key.startswith('car:'):
        continue
    name = artwork.scene_art(key)
    assert name != 'ui-header', key
    assert (artwork.ASSETS / (name + '.png')).is_file(), key

root = tk.Tk()
root.title('Unique location artwork verification')
winterfield_ui.install(root)
errors = []
root.report_callback_exception = lambda *args: errors.append(args)
out = ROOT / 'tests/screenshots/unique-locations'
out.mkdir(parents=True, exist_ok=True)
try:
    for batch in range(0, len(assets), 6):
        for child in root.winfo_children():
            child.destroy()
        canvases = []
        for index, spec in enumerate(assets[batch:batch + 6]):
            frame = tk.Frame(root, bg='#18202d')
            frame.grid(row=index // 2, column=index % 2, sticky='nsew')
            root.grid_rowconfigure(index // 2, weight=1)
            root.grid_columnconfigure(index % 2, weight=1)
            tk.Label(frame, text=spec['key'], bg='#18202d', fg='#dce5ed').pack()
            canvas = artwork.ArtCanvas(frame, artwork.scene_art(spec['key']))
            canvas.pack(fill='both', expand=True)
            canvases.append((canvas, spec['key']))
        for mode, size in [('day', '1200x900'), ('night', '1000x750')]:
            root.geometry(size)
            for canvas, key in canvases:
                canvas.set_art((artwork.scene_art(key), mode, 'Rain' if mode == 'night' else 'Clear'))
            root.update()
            assert all(canvas.photo is not None for canvas, _ in canvases)
            ImageGrab.grab(window=root.winfo_id()).save(out / f'batch-{batch // 6 + 1}-{mode}.png')
    assert not errors, errors
    print('PASS: 23 unique assets, all named locations resolve, texting/time variants, Tk rendering and resizing.')
finally:
    root.destroy()
