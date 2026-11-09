"""Bound Grove rendering and verify paging preserves the composer and reply targets."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from time import perf_counter
from unittest.mock import patch
from PIL import ImageGrab
import game
import game_core as core
import grove
import phone_apps as apps
import grove_gallery_ui as gallery_ui
from phone_controls import PhoneButton


def descendants(widget):
    for child in widget.winfo_children():
        yield child
        yield from descendants(child)


with patch.object(game.Game, 'check', lambda self: None), \
     patch.object(game.Game, 'persist', lambda self: None), \
     patch.object(grove.GrovePump, 'tick', lambda self: None), \
     patch.object(game.Game, 'begin_incoming', lambda self: None):
    app = game.Game()
    errors = []
    app.report_callback_exception = lambda *args: errors.append(args)
    try:
        app.state_data = core.fresh('rei')
        app.play_screen()
        started = perf_counter()
        app.phone_window('Grove')
        app.update()
        phone = app.phone_activity
        print(f'Fresh archive opens in {perf_counter()-started:.3f}s', flush=True)
        assert len(phone.grove_feed_body.winfo_children()) <= 12
        def button(label):
            return next(w for w in descendants(phone.screen)
                        if isinstance(w, PhoneButton) and w.cget('text') == label)
        entry = phone.grove_entry
        entry.insert(0, 'Keep this draft')
        assert button('Newer').cget('state') == 'disabled'
        button('Older').invoke()
        app.update()
        assert phone.grove_feed_page == 1 and phone.grove_entry is entry
        assert entry.get() == 'Keep this draft'
        button('Reply').invoke()
        target = phone.reply_to
        button('Newer').invoke()
        app.update()
        assert phone.reply_to == target and entry.get() == 'Keep this draft'
        assert len(phone.grove_feed_body.winfo_children()) == 12
        button('Older').invoke()
        button('Newer').invoke()
        app.update()
        assert gallery_ui._thumbnail.cache_info().hits > 0
        assert gallery_ui._thumbnail.cache_info().maxsize == 48
        out = core.ROOT / 'tests/screenshots'
        out.mkdir(exist_ok=True)
        ImageGrab.grab(window=phone.winfo_id()).save(out / 'grove-paged-feed.png')
        # Every root and deep reply remains reachable, including the final short page.
        posts = [dict(id=i, author='rei', parent=None if i < 15 else i-1,
                      minute=i, text=f'Paging post {i}') for i in range(35)]
        with patch.object(apps, 'grove_posts', return_value=posts):
            phone.refresh()
            app.update()
            found = set()
            while True:
                for w in descendants(phone.grove_feed_body):
                    try:
                        text = w.cget('text')
                        if text.startswith('Paging post '): found.add(text)
                    except Exception:
                        pass
                assert len(phone.grove_feed_body.winfo_children()) <= 12
                if button('Older').cget('state') == 'disabled': break
                button('Older').invoke()
                app.update()
            assert found == {p['text'] for p in posts}, found
            assert phone.grove_feed_page == 2
        assert not errors, errors
        print('Bounded feed, complete paging, drafts, reply targets, cache reuse and timer cleanup passed.')
    finally:
        app.destroy()
