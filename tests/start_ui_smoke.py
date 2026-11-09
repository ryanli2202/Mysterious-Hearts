"""Visual and interaction check for the start screen; no AI or player-save writes."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from unittest.mock import patch
import tkinter as tk
from PIL import ImageGrab
import game
import game_core as core

out = core.ROOT/'tests/screenshots'
out.mkdir(exist_ok=True)
with patch.object(game.Game, 'check'), patch.object(game.Game, 'begin_incoming'), patch.object(core, 'save'), patch.object(game.Game, 'start') as start:
    app = game.Game()
    errors=[]
    app.report_callback_exception=lambda *e:errors.append(e)
    app.update()
    screen=app.start_screen
    for who in core.PLAYERS:
        screen.select(who); screen.choices[who].invoke(); app.update()
        assert screen.selected == who
        assert not start.called, 'Preview should not start a story'
        assert core.PLAYERS[who].split()[0] in screen.begin.cget('text')
    screen.begin.invoke(); start.assert_called_once_with('gordon')
    screen.change_page(1); assert screen.selected == 'garrett'
    screen.change_page(-1); assert screen.selected == 'mavis'
    for size, who in [('1220x940','rei'), ('1000x800','garrett')]:
        app.geometry(size); screen.select(who); app.update()
        screen.preview.render(); app.update()
        for widget in [screen.begin, screen.sound, *[w for w in screen.choices.values() if w.winfo_ismapped()]]:
            assert widget.winfo_ismapped()
            assert widget.winfo_rooty()+widget.winfo_height() <= app.winfo_rooty()+app.winfo_height()
        ImageGrab.grab(window=app.winfo_id()).save(out/f'start-{size}.png')
    assert not errors, errors
    import custom_library
    from test_custom_protagonist import PROFILE
    def descendants(widget):
        for child in widget.winfo_children():
            yield child
            yield from descendants(child)
    with patch.object(custom_library, 'profiles', return_value=[PROFILE | {'portrait': 'assets/generated/example.png'}]), patch.object(app, 'start_custom') as custom_start:
        screen.saved_characters(); app.update()
        window = next(w for w in app.winfo_children() if isinstance(w, tk.Toplevel)) if any(isinstance(w, tk.Toplevel) for w in app.winfo_children()) else next(w for w in descendants(screen) if isinstance(w, tk.Toplevel))
        ImageGrab.grab(window=window.winfo_id()).save(out/'saved-characters.png')
        next(w for w in descendants(window) if isinstance(w, tk.Button) and w.cget('text') == 'Begin new playthrough').invoke()
        custom_start.assert_called_once()
    assert not errors, errors
    app.sounds.close(); app.destroy()
print('Start UI passed: 28 previews, paging, explicit begin, default and minimum layouts.')
