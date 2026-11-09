"""Exercise Grove photo screens without AI calls or saving a player game."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from unittest.mock import patch
from PIL import ImageGrab
from tkinter import ttk
import game
import game_core as core
import grove
import grove_gallery as gallery
import grove_gallery_ui as view
import phone_apps as apps
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
        app.phone_window('Grove')
        phone = app.phone_activity
        app.update()
        output = core.ROOT / 'tests/screenshots'
        output.mkdir(exist_ok=True)
        ImageGrab.grab(window=phone.winfo_id()).save(output / 'grove-photo-feed.png')
        for who in ('garrett', 'rei', 'ivan', 'minsu', 'emily'):
            profile = view.show_profile(phone, who)
            app.update()
            if who == 'rei':
                ImageGrab.grab(window=profile.winfo_id()).save(output / 'grove-profile-grid.png')
            profile.destroy()
        post = gallery.photos(app.state_data, 'garrett')[0]
        detail = view.show_post(phone, post)
        app.update()
        ImageGrab.grab(window=detail.winfo_id()).save(output / 'grove-photo-detail.png')
        buttons = [w for w in descendants(detail) if isinstance(w, ttk.Button)]
        next(w for w in buttons if 'likes' in str(w['text'])).invoke()
        assert post['liked_by'] == ['rei']
        next(w for w in buttons if 'Write a comment' in str(w['text'])).invoke()
        app.update()
        assert phone.reply_to == post['id']
        phone.grove_entry.insert(0, 'That cuff needs its own fan club.')
        next(w for w in descendants(phone.screen) if isinstance(w, (ttk.Button, PhoneButton)) and w.cget('text') == 'Post').invoke()
        app.update()
        assert apps.ensure(app.state_data)['posts'][-1]['parent'] == post['id']
        detail = view.show_post(phone, post)
        app.update()
        target = next(p for p in apps.grove_posts(app.state_data) if p['parent'] == post['id'])
        next(w for w in descendants(detail) if isinstance(w, ttk.Button) and w.cget('text') == 'Reply to comment').invoke()
        app.update()
        assert phone.reply_to == target['id']
        full = view.show_full_image(phone, post)
        app.update()
        full.destroy()
        assert not errors, errors
        print('Grove feed, five profile grids, photo detail, likes, archive replies and image viewer passed.')
    finally:
        app.destroy()
