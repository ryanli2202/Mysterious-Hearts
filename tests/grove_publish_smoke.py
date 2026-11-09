"""Exercise Gallery selection, caption validation and publish without live AI."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import tkinter as tk
from tkinter import ttk
from types import SimpleNamespace
from unittest.mock import patch
import camera
import game_core as core
import grove_gallery as gallery
import grove_gallery_ui as view
import phone_apps as apps
import winterfield_ui as ui


def descendants(widget):
    for child in widget.winfo_children():
        yield child
        yield from descendants(child)


root = tk.Tk()
root.withdraw()
ui.install(root)
state = core.fresh('rei')
saved, opened = [], []
root.game = SimpleNamespace(state_data=state, persist=lambda: saved.append(True))
root.open_app = opened.append
root.refresh_feed = lambda: None
def scroll(parent):
    frame = ttk.Frame(parent)
    frame.pack(fill='both', expand=True)
    return frame
root.scroll_area = scroll
record = dict(id='smoke', path=gallery.catalog()[0]['image'], date='2050-01-01',
              mode='Selfie', snapshot={'mode': 'Selfie'})
try:
    with patch.object(camera, 'photos', return_value=[record]), \
         patch.object(camera, 'photo_path', return_value=gallery.ROOT / record['path']):
        picker = view.compose(root)
        root.update()
        next(w for w in descendants(picker) if isinstance(w, ttk.Button) and 'Choose' in str(w['text'])).invoke()
        root.update()
        composer = next(w for w in root.winfo_children() if isinstance(w, tk.Toplevel))
        submit = next(w for w in descendants(composer) if isinstance(w, ttk.Button) and w['text'] == 'Post photo to Grove')
        submit.invoke()
        assert not apps.ensure(state)['posts']
        next(w for w in descendants(composer) if isinstance(w, tk.Text)).insert('1.0', 'New favourite photo.')
        submit.invoke()
        root.update()
        assert saved == [True] and opened == ['Grove']
        post = apps.ensure(state)['posts'][-1]
        assert post['image'] == record['path'] and post['text'] == 'New favourite photo.'
        detail = view.show_post(root, post)
        root.update()
        detail.destroy()
        job = apps.ensure(state)['grove_pending'][0]
        apps.commit_grove(state, job, dict(text='Love this shot!', parent=post['id']))
        notifications = view.show_notifications(root)
        root.update()
        assert notifications.cget('background') == ui.PANEL
        assert len(gallery.unread_comments(state)) == 1
        next(w for w in descendants(notifications) if isinstance(w, ttk.Button)).invoke()
        root.update()
        assert not gallery.unread_comments(state)
        print('Comment notification opens the photo and clears its unread status.')
        print('Photo picker, caption validation, publishing, persistence and post detail passed.')
finally:
    root.destroy()
