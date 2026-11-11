"""Exercise save library actions in Tk using isolated saves, with no AI requests."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import tempfile
import tkinter as tk
from unittest.mock import patch
import game
import game_core as core
import qol_ui
import save_system

scratch = core.ROOT / '.test-tmp'
scratch.mkdir(exist_ok=True)
with tempfile.TemporaryDirectory(dir=scratch) as folder:
    active = Path(folder) / 'story.json'
    real_save = core.save
    def isolated_save(state, path=None): return real_save(state, path or active)
    with patch.object(core, 'SAVE', active), patch.object(core, 'save', side_effect=isolated_save), patch.object(game.Game, 'check'), patch.object(game.Game, 'begin_incoming'):
        app = game.Game(); errors=[]
        app.report_callback_exception=lambda *args: errors.append(args)
        app.state_data = core.fresh('rei'); app.persist()
        app.play_screen(); app.update()
        qol_ui.saves(app); app.update()
        win = next(w for w in app.winfo_children() if isinstance(w, tk.Toplevel) and w.title() == 'Story library and recovery')
        def buttons(parent):
            for child in parent.winfo_children():
                if child.winfo_class() == 'TButton': yield child
                yield from buttons(child)
        controls={b.cget('text'): b for b in buttons(win)}
        listing=next(w for w in win.winfo_children() if isinstance(w,tk.Listbox))
        listing.selection_set(0)
        before={p:p.read_bytes() for p in active.parent.rglob('*.json')}
        with patch.object(core,'load',side_effect=AssertionError('preview must not load gameplay')):
            controls['Saved progress'].invoke(); app.update()
        preview=next(w for w in win.winfo_children() if isinstance(w,tk.Toplevel))
        text=next(w for w in preview.winfo_children() if isinstance(w,tk.Text)).get('1.0','end')
        assert 'Saved progress' in text and 'Current funds' in text
        assert before=={p:p.read_bytes() for p in before}
        from PIL import ImageGrab
        ImageGrab.grab(window=preview.winfo_id()).save(core.ROOT/'tests'/'screenshots'/'mh002-saved-progress.png')
        preview.destroy()
        with patch.object(qol_ui.simpledialog, 'askstring', return_value='Checkpoint'):
            controls['Save named copy'].invoke(); app.update()
        assert len(list(active.parent.rglob('slot-*.json'))) == 1
        with patch.object(qol_ui.messagebox, 'askyesno', return_value=True):
            controls['Clear all saves'].invoke(); app.update()
        assert app.state_data is None and not app.in_game
        app.persist()
        assert not save_system.entries(active.parent), 'Deleted story recreated itself'
        assert not errors, errors
        app.sounds.close(); app.destroy()
print('Save library UI passed: named copy, clear all, no autosave resurrection.')
