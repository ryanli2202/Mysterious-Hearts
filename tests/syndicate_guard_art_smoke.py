"""Inspect the three Syndicate assets through the game's portrait loader."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import tkinter as tk
from unittest.mock import patch
from PIL import ImageGrab
import game
import grove
import game_core as core

with patch.object(game.Game, 'check'), patch.object(game.Game, 'begin_incoming'), patch.object(game.Game, 'persist'), patch.object(grove.GrovePump, 'tick'):
    app = game.Game()
    try:
        app.geometry('1080x720')
        stage = tk.Canvas(app, bg='#243448', highlightthickness=0)
        stage.place(x=0, y=0, relwidth=1, relheight=1)
        images = []
        for index, ident in enumerate(('clubs', 'spades', 'affiliate')):
            portrait = app.portrait('guard_art_' + ident, (330, 620))
            images.append(portrait)
            stage.create_image(180 + index * 360, 350, image=portrait)
            stage.create_text(180 + index * 360, 30, text=ident.title(), fill='#edf3fc', font=('Arial', 16))
        app.update()
        target = core.ROOT / 'tests/screenshots/syndicate-guard-redesign.png'
        ImageGrab.grab(window=app.winfo_id()).save(target)
        print('All three revised Syndicate portraits loaded; review saved to', target)
    finally:
        app.sounds.close()
        app.destroy()
