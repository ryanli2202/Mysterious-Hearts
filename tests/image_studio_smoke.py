"""Exercise the real Tk viewer and background completion flow without consuming usage."""
from pathlib import Path
import sys
import time
from unittest.mock import patch
import tkinter as tk

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import codex_images
from image_studio_ui import ImageStudio
from gallery_ui import GalleryWindow


def main():
    entries = codex_images.library()
    assert entries, 'Run the live image bridge test first.'
    root = tk.Tk()
    root.withdraw()
    gallery = GalleryWindow(root)
    gallery.open_studio()
    studio = next(w for w in gallery.winfo_children() if isinstance(w, ImageStudio))
    root.update()
    studio.redraw()
    assert studio.photo is not None
    assert studio.photo.width() > 1
    studio.prompt.insert('1.0', 'Test completion display')
    with patch.object(codex_images, 'generate', return_value=entries[0]):
        studio.generate()
        deadline = time.monotonic() + 5
        while studio.cancel_event is not None and time.monotonic() < deadline:
            root.update()
            time.sleep(0.02)
    assert studio.cancel_event is None
    assert 'saved and loaded' in studio.status.cget('text')
    assert studio.photo is not None
    assert str(studio.generate_button['state']) == 'normal'
    studio.geometry('760x620')
    root.update()
    studio.redraw()
    assert studio.photo.width() <= studio.canvas.winfo_width()
    studio.events.put(('error', 'Usage limit reached. No fallback.'))
    studio.after_cancel(studio.poll_job)
    studio.poll()
    assert 'Usage limit' in studio.status.cget('text')
    studio.destroy()
    gallery.destroy()
    root.destroy()
    print('PASS: gallery entry point, persisted library, worker completion, automatic preview, resize and errors')


if __name__ == '__main__':
    main()
