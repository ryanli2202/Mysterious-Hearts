"""Render anonymous-note states without AI calls or save writes."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from unittest.mock import patch
from tkinter import ttk
from PIL import ImageGrab
import game
import game_core as core
import grove
import hearts_ai
import hearts_ui
import mysterious_hearts as hearts

def widgets(parent):
    for child in parent.winfo_children():
        yield child
        yield from widgets(child)

def button(parent, text):
    return next(w for w in widgets(parent) if isinstance(w, ttk.Button) and text in str(w.cget('text')))

def labels(parent):
    return [str(w.cget('text')) for w in widgets(parent) if isinstance(w, ttk.Label)]

with patch.object(hearts_ai.NotePump, 'tick', lambda self: None), \
     patch.object(game.Game, 'check', lambda self: None), \
     patch.object(game.Game, 'persist', lambda self: None), \
     patch.object(grove.GrovePump, 'tick', lambda self: None), \
     patch.object(game.Game, 'begin_incoming', lambda self: None):
    app = game.Game()
    errors = []
    app.report_callback_exception = lambda *args: errors.append(args)
    app.state_data = core.fresh('rei')
    app.play_screen(); app.update()
    app.phone_window(); phone = app.phone_activity
    output = core.ROOT / '.test-tmp'; output.mkdir(exist_ok=True)
    def shot(name):
        app.update()
        ImageGrab.grab(window=phone.winfo_id()).save(output / name)
    phone.open_app('Mysterious Hearts'); shot('hearts-inbox.png')
    ident = hearts.send(app.state_data, 'emily', 'rei', 'You mean more to me than I know how to say.', 'confession')
    hearts.queue_note(app.state_data, 'emily', 'rei', 'reply', ident)
    hearts.ensure(app.state_data)['pending'][0]['error'] = 'Test failure'
    hearts_ui.thread(phone, ident); shot('hearts-thread.png')
    assert 'Sender: Unknown' in labels(phone)
    assert hearts.unread(app.state_data, 'rei') == 0
    button(phone, 'Open / close').invoke()
    phone.geometry('440x720'); shot('hearts-notebook-small.png')
    button(phone, 'Try again').invoke(); app.update()
    assert hearts.ensure(app.state_data)['pending'][0]['error'] is None
    shot('hearts-waiting-small.png')
    phone.open_app('Contacts'); phone.contact_detail('emily'); app.update()
    assert 'About & favourites' in labels(phone)
    shot('hearts-contact.png')
    phone.contact_detail('rei'); app.update()
    assert 'Private notebook · visible only to you' in labels(phone)
    assert not any('Not shared yet' in text for text in labels(phone))
    button(phone, 'Show / hide your full personal reference').invoke(); app.update()
    assert 'Your private history' in labels(phone)
    phone.open_app('Home'); app.update()
    assert phone.hearts_icon.winfo_exists()
    app.destroy()
    assert not errors, errors
print('Phone smoke passed: inbox, thread, retry, notebook, resize, contacts and app icon.')
