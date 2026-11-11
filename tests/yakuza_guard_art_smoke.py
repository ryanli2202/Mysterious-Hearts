"""Review the five yakuza designs through the actual portrait loader."""
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
        app.geometry('1250x650')
        stage = tk.Canvas(app, bg='#243448', highlightthickness=0)
        stage.place(x=0, y=0, relwidth=1, relheight=1)
        images = []
        for index, ident in enumerate(('kai_sentinel', 'kai_guard', 'yokai', 'tengu', 'oni')):
            portrait = app.portrait('guard_art_' + ident, (240, 570))
            assert portrait.width() > 0
            images.append(portrait)
            stage.create_image(125 + index * 250, 335, image=portrait)
            stage.create_text(125 + index * 250, 30, text=ident.replace('_', ' ').title(), fill='#edf3fc', font=('Arial', 16))
        app.update()
        target = core.ROOT / 'tests/screenshots/yakuza-guard-redesign.png'
        target.parent.mkdir(exist_ok=True)
        ImageGrab.grab(window=app.winfo_id()).save(target)
        print('All five yakuza portraits loaded; review saved to', target)
    finally:
        app.sounds.close()
        app.destroy()
