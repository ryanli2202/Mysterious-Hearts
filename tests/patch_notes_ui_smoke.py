"""Real Tk interactions and screenshots, isolated preferences, no AI or story writes."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import tempfile
import tkinter as tk
from unittest.mock import patch
from PIL import ImageGrab
import winterfield_ui
import patch_notes as notes
import patch_notes_ui as ui

root=tk.Tk(); root.withdraw(); winterfield_ui.install(root)
errors=[]; root.report_callback_exception=lambda *e:errors.append(e)
with tempfile.TemporaryDirectory() as folder:
    prefs=Path(folder)/'prefs.json'; exports=Path(folder)/'exports'
    window=ui.PatchNotesWindow(root,prefs,exports); window.update()
    assert len(window.visible)>=47
    window.read_button.invoke(); window.bookmark_button.invoke(); window.update()
    assert len(notes.preferences(prefs)['read'])==1
    assert len(notes.preferences(prefs)['bookmarks'])==1
    window.query.set('canonical compatibility'); window.update()
    # Other patches can also mention these words; choose the intended result explicitly.
    selected=next(i for i,r in enumerate(window.visible) if r['id']=='history-sexuality')
    window.list.selection_clear(0,'end'); window.list.selection_set(selected); window.choose()
    assert window.current['id']=='history-sexuality'
    window.export_button.invoke(); window.update()
    assert len(list(exports.glob('*.md')))==1
    # A newly bookmarked release may also mention canonical compatibility.
    # Exercise the empty filter with a deliberately absent query instead.
    window.query.set('no-match-zzzzz')
    window.status.set('Bookmarked'); window.refresh(); window.update()
    assert not window.visible
    assert str(window.read_button['state'])=='disabled'
    window.query.set(''); window.update()
    assert len(window.visible)==1
    window.status.set('All entries'); window.refresh()
    out=notes.ROOT/'tests/screenshots'; out.mkdir(exist_ok=True)
    for size in ('1100x760','850x600'):
        window.geometry(size); window.update()
        ImageGrab.grab(window=window.winfo_id()).save(out/f'patch-notes-{size}.png')
        for widget in (window.search,window.read_button,window.export_all):
            assert widget.winfo_ismapped()
            assert widget.winfo_rooty()+widget.winfo_height()<=window.winfo_rooty()+window.winfo_height()
    window.reports.set(True); window.kind.set('Development report'); window.refresh(); window.update()
    assert window.visible and all(r['kind']=='Development report' for r in window.visible)
    window.query.set('no-match-zzzzz'); window.update()
    assert 'No matching updates' in window.detail.get('1.0','end')
    window.destroy()
    with patch.object(notes,'load',side_effect=ValueError('Damaged catalogue')):
        window=ui.PatchNotesWindow(root,prefs,exports); window.update()
        assert 'Damaged catalogue' in window.detail.get('1.0','end')
        window.destroy()
    assert not errors,errors
root.destroy()
print('Patch notes UI passed: search, filters, state, export, empty/error states and two sizes.')
