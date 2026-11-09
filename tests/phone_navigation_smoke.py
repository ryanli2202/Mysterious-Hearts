"""Exercise real Tk phone navigation without contacting AI or saving a player game."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from unittest.mock import patch
from PIL import ImageGrab
import game
import game_core as core
import groups
import grove
import tkinter as tk
import winterfield_ui as ui

with patch.object(game.Game, 'check', lambda self: None), \
     patch.object(game.Game, 'persist', lambda self: None), \
     patch.object(grove.GrovePump, 'tick', lambda self: None), \
     patch.object(game.Game, 'begin_incoming', lambda self: None):
    app = game.Game()
    app.state_data = core.fresh('rei')
    from supafast_fixtures import seed
    seed(app.state_data)
    from supafast_fixtures import disable_images
    disable_images(app)
    app.play_screen()
    app.update()
    assert app.presence_view.winfo_manager() == 'pack'
    app.phone_window()
    phone = app.phone_activity
    app.update()
    assert phone.selected == 'Home'
    screenshots = core.ROOT / 'tests' / 'screenshots'
    screenshots.mkdir(exist_ok=True)
    ImageGrab.grab(window=phone.winfo_id()).save(screenshots / 'phone-home.png')
    for name in ('Messages', 'Contacts', 'Maps', 'Calendar', 'Journal', 'Settings', 'More', 'Grove', 'Supafast', 'Doober Eats', 'Deliveries', 'Mini Games'):
        phone.open_app(name)
        app.update()
    phone.geometry('560x680')
    app.update()
    arcade = phone.screen.winfo_children()[0].winfo_children()[0]
    ImageGrab.grab(window=phone.winfo_id()).save(screenshots / 'phone-mini-games.png')
    from mini_games_ui import ENGINES
    for name in ENGINES:
        arcade.open(name)
        app.update()
        controls = arcade.winfo_children()[-1]
        assert controls.winfo_ismapped()
        assert controls.winfo_y() + controls.winfo_height() <= arcade.winfo_height()
    ImageGrab.grab(window=phone.winfo_id()).save(screenshots / 'phone-2048.png')
    phone.geometry('660x850')
    phone.open_app('Contacts')
    phone.contact_detail('emily')
    app.update()
    phone.open_thread('emily')
    app.update()
    assert phone.selected == 'Conversation'
    assert app.state_data['routes']['emily']['channel'] == 'text'
    app.busy = True
    app.pending = 'Still sending'
    token = app.token
    phone.open_app('Home')
    phone.open_app('Messages')
    phone.open_thread('emily')
    assert phone.selected == 'Conversation'
    assert phone.message_status.cget('text').startswith('Writing response · ')
    assert app.pending == 'Still sending' and app.token == token
    phone.close_phone()
    app.phone_window('Messages')
    phone.open_thread('emily')
    assert not phone.closing
    app.busy = False
    app.pending = None
    chat = app.state_data['routes']['emily']
    chat['choices'] = ['Hello.', 'Sounds good.', 'That was funny.', 'You look lovely.']
    chat['personal_choices'] = ['How was your morning?', 'What are you building?', 'I painted today.', 'Want to talk about it?']
    chat['suggestions_requested'] = ['main','personal']
    phone.set_message_mode(True)
    assert len(phone.message_choices) == 4
    assert phone.visible_message_choices == chat['personal_choices']
    with patch.object(app, 'submit') as submit:
        phone.message_choices[2].invoke()
        submit.assert_called_once_with('I painted today.')
    app.update()
    ImageGrab.grab(window=phone.winfo_id()).save(screenshots / 'phone-personal-replies.png')
    phone.set_message_mode(False)
    assert phone.visible_message_choices == chat['choices']
    gid = groups.create_text(app.state_data, 'Test group', ['emily', 'garrett'])
    app.state_data['groups'][gid]['choices'] = chat['choices'][:]
    app.state_data['groups'][gid]['personal_choices'] = chat['personal_choices'][:]
    app.state_data['groups'][gid]['suggestions_requested'] = ['main','personal']
    phone.open_thread(gid, True)
    app.busy = True
    phone.open_app('Home')
    phone.open_thread(gid, True)
    assert phone.selected == 'Conversation'
    assert app.group_selected == gid
    app.busy = False
    phone.set_message_mode(True)
    with patch.object(app, 'submit') as submit:
        phone.message_choices[0].invoke()
        submit.assert_called_once_with('How was your morning?')
    probe = tk.Canvas(phone)
    assert probe.cget('background') == ui.PANEL
    probe.destroy()
    phone.open_app('Grove')
    def descendants(widget):
        for child in widget.winfo_children():
            yield child
            yield from descendants(child)
    for widget in descendants(phone.screen):
        if isinstance(widget, tk.Canvas): assert widget.cget('background') == ui.PANEL
    phone.close_phone()
    app.update()
    assert app.presence_view.winfo_manager() == 'pack'
    s = app.state_data
    s['world']['cast']['emily']['location'] = s['world']['location']
    s['world']['cast']['emily']['journey'] = None
    groups.open_solo(s, 'emily')
    app.show_in_person()
    app.update()
    assert app.group_selected == 'solo:emily'
    assert app.in_person_chat.winfo_manager() == 'pack'
    app.phone_window()
    with patch('phone_ui.messagebox.showinfo') as notice:
        app.phone_activity.open_thread('emily')
        notice.assert_called_once()
    assert app.group_selected == 'solo:emily'
    app.phone_activity.open_thread('garrett')
    app.phone_activity.close_phone()
    app.update()
    assert app.group_selected == 'solo:emily'
    app.end_hangout()
    app.update()
    assert app.presence_view.winfo_manager() == 'pack'
    assert len(s['hangout_journal']) == 1
    app.phone_window('Journal')
    app.update()
    app.phone_activity.open_app('Maps')
    app.phone_activity.map_view.select(s['world']['location'])
    assert 'Emily Fields' in app.phone_activity.map_view.people_text.get('1.0', 'end')
    app.phone_activity.open_app('Contacts')
    app.phone_activity.act(core.town.summon, 'emily')
    assert 'emily' in s['world']['party']
    app.phone_activity.close_phone()
    app.update()
    ImageGrab.grab(window=app.winfo_id()).save(screenshots / 'in-person-location.png')
    app.destroy()
print('Phone navigation passed: apps, profiles, messages, close/resume, location fallback, and hangout journal.')
