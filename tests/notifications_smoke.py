"""Exercise actual reply delivery and phone badges without AI calls or saving."""
import sys
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from PIL import ImageGrab
import game
from phone_ui import PhoneWindow
from phone_icons import unread_messages
from test_game import SCENE


with patch.object(game.Game, 'check'), patch.object(game.Game, 'persist'), \
        patch.object(game.Game, 'begin_incoming'), patch.object(game.Game, 'show_world_windows'), \
        patch.object(game.Game, 'poll_grove'), patch('game.SoundSystem'):
    app = game.Game()
    app.state_data = game.core.fresh('garrett')
    app.play_screen()
    phone = PhoneWindow(app, 'Home')
    app.phone_activity = phone
    app.update()

    def deliver():
        app.token += 1
        app.busy = True
        app.pending = 'Hello'
        app.events.put(('result', app.token, 'Hello', dict(SCENE), False))
        app.poll()
        phone.update_notifications()
        app.update()

    deliver()
    route = app.state_data['routes']['emily']
    popup = app.notification_popups.window
    assert popup is not None and popup.winfo_viewable(), 'Incoming message must show a popup'
    app.notification_popups.dismiss()
    assert app.notification_popups.window is None
    assert route['unread'] == 1, 'A reply arriving on Home must remain unread'
    assert phone.messages_icon.find_withtag('notification-dot')
    deliver()
    assert route['unread'] == 2, 'Unseen replies must accumulate'
    phone.open_app('Messages'); app.update()
    assert route['unread'] == 2, 'Viewing the inbox must not read the thread'

    def has_sender_badge(widget):
        return ((isinstance(widget, game.tk.Canvas) and bool(widget.find_withtag('unread:emily')))
                or (isinstance(widget, game.ttk.Label) and str(widget.cget('text')).startswith('● Emily'))
                or any(has_sender_badge(child) for child in widget.winfo_children()))

    assert has_sender_badge(phone.screen), 'Unread sender needs a badge over their avatar'
    (game.core.ROOT / '.test-tmp').mkdir(exist_ok=True)
    ImageGrab.grab(window=phone.winfo_id()).save(game.core.ROOT / '.test-tmp' / 'unread-sender.png')
    phone.open_app('Home'); app.update()
    ImageGrab.grab(window=phone.winfo_id()).save(game.core.ROOT / '.test-tmp' / 'unread-app.png')
    phone.thread = ('emily', False)
    phone.open_app('Conversation'); app.update(); phone.update_messages()
    assert route['unread'] == 0
    deliver()
    assert route['unread'] == 0, 'A visible conversation reads replies immediately'
    phone.withdraw(); app.update()
    deliver()
    phone.update_messages()
    assert route['unread'] == 1, 'A hidden conversation must not read replies'
    phone.deiconify(); app.update(); phone.update_messages()
    assert route['unread'] == 0
    phone.open_app('Home'); app.update()
    assert unread_messages(app.state_data) == 0
    assert not phone.messages_icon.find_withtag('notification-dot')
    import phone_apps as apps
    import grove_gallery_ui
    app.notification_popups.pending.clear()
    app.notification_popups.dismiss()
    data = apps.ensure(app.state_data)
    post = apps._append(data, app.state_data['player'], 'A text post', 0)
    job = apps.queue_grove(app.state_data, 'emily', post['id'])
    apps.commit_grove(app.state_data, job, dict(text='Nice post!', parent=post['id']))
    app.notification_popups.observe(app.state_data)
    app.update()
    assert app.notification_popups.window.winfo_viewable()
    assert not data['grove_notifications'][-1]['read'], 'A popup must not mark comments read'
    app.notification_popups.dismiss()
    detail = grove_gallery_ui.show_post(phone, post)
    app.update()
    assert data['grove_notifications'][-1]['read']
    detail.destroy()
    app.destroy()
print('Real reply delivery: Home/inbox badges, accumulation, visible reading, hidden chat, and clearing passed.')
