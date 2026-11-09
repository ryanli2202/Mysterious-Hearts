"""Render the actual desktop screens and verify response controls without saving."""
import sys
import inspect
import json
import time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from PIL import ImageGrab
from unittest.mock import patch
import game
import game_core as c

out = c.ROOT / 'tests' / 'screenshots'
out.mkdir(exist_ok=True)
with patch.object(game.Game, 'check', lambda self: None):
    app = game.Game()
    app.update()
    def shot(name, window=app):
        app.update()
        if sys.platform == 'win32' and 'window' in inspect.signature(ImageGrab.grab).parameters:
            ImageGrab.grab(window=window.winfo_id()).save(out / name)
        else:
            x, y = window.winfo_rootx(), window.winfo_rooty()
            ImageGrab.grab(bbox=(x, y, x+window.winfo_width(), y+window.winfo_height())).save(out / name)
    shot('selection.png')
    app.state_data = c.fresh('rei')
    c.commit(app.state_data, 'Hello Emily.', {
        'narration': 'Late sunlight catches on the flower-shop windows. Emily sets a watering can beside a row of small clay pots.',
        'dialogue': 'Rei! I was hoping you would stop by. I have been building a little LEGO greenhouse after work. Would you like to see it?',
        'emotions': {'rei': 'curious', 'emily': 'happy'},
        'choices': ['I would love to. Show me what you have built.', 'Let me help you finish watering first.', 'A greenhouse? That sounds like the perfect project for you.', 'Would you like to get dinner after closing?'],
        'memory': 'Rei visited Emily after work. She invited him to see her LEGO greenhouse.'})
    app.play_screen(); app.update()
    shot('conversation.png')
    assert len(app.choices) == 4
    assert app.feelings.winfo_ismapped()
    assert app.feelings.labels == [('Rei Takamura (You)', 'curious'), ('Emily Fields', 'happy')]
    visible = app.dialogue.get('1.0', 'end')
    assert 'Rei Takamura (You)' in visible and 'Emily Fields' in visible and 'Narrator' not in visible
    assert 'Rei Takamura' in app.reply_heading['text']
    first_four = [b['text'] for b in app.choices]
    app.panel_switch.invoke()
    assert all(tone in b['text'] for tone, b in zip(c.PERSONAL_TONES, app.choices))
    with patch.object(app, 'submit') as send:
        app.choices[2].invoke()
        send.assert_called_once_with(c.personal_choices(app.state_data, app.state_data['routes']['emily'])[2])
    app.panel_switch.invoke()
    assert first_four == [b['text'] for b in app.choices]
    assert all(str(b['state']) == 'normal' for b in app.choices)
    app.set_busy(True)
    assert all(str(b['state']) == 'disabled' for b in app.choices)
    app.set_busy(False)
    assert app.send.winfo_ismapped()
    assert app.retry.winfo_rooty()+app.retry.winfo_height() <= app.winfo_rooty()+app.winfo_height(), 'Footer clipped'
    app.geometry('1000x800'); app.update()
    shot('conversation-compact.png')
    assert app.dialogue.winfo_ismapped() and app.dialogue.winfo_height() >= 50, 'Conversation clipped'
    assert app.retry.winfo_rooty()+app.retry.winfo_height() <= app.winfo_rooty()+app.winfo_height(), 'Compact footer clipped'
    scene = dict(speaker='Emily Fields', addressee='Rei Takamura', choices_speaker='Rei Takamura',
                 narration='A message arrives.', dialogue='wait. dinner as in… just us? (⁄ ⁄•⁄ω⁄•⁄ ⁄)',
                 choices=['Just us.', 'If you want.', 'And the greenhouse.', 'It’s a date.'],
                 memory='Rei asked Emily to dinner.', emotions={'rei':'flirty', 'emily':'flustered'},
                 social_event='welcomed_flirt', bond_moments={'emily':'none'})
    replies = dict(choices=scene['choices'], choices_speaker='Rei Takamura',
                   personal_choices=c.personal_choices(app.state_data, {}))
    initial_attraction = app.relationship_bars.stats['attraction']
    with patch.object(app, 'persist'), patch.object(c, 'request', side_effect=[
            {'message': {'content': json.dumps(data)}} for data in (scene, replies)]) as model:
        app.choices[3].invoke()
        deadline = time.monotonic() + 4
        while app.busy and time.monotonic() < deadline:
            app.after(20, app.quit); app.mainloop()
        assert not app.busy and model.call_count == 2
        move = json.loads(model.call_args_list[0].args[1]['messages'][-1]['content'])
        assert move['submitted_tone'] == 'Flirtatious'
        assert scene['dialogue'] in app.dialogue.get('1.0', 'end')
        assert app.feelings.labels == [('Rei Takamura (You)', 'flirty'), ('Emily Fields', 'flustered')]
        assert app.relationship_bars.stats['attraction'] == initial_attraction + 2
    app.state_data = c.fresh()
    with patch.object(app, 'submit') as send:
        app.play_screen(); app.update()
        send.assert_called_once_with(c.INCOMING_TEXT)
        assert str(app.send['state']) == 'disabled'
        assert str(app.entry['state']) == 'disabled'
    from account_ui import AccountWindow
    with patch.object(AccountWindow,'run'):
        account=AccountWindow(app)
        account.events.put(('ok',{'status':'connected','sharing':False},[]))
        account.poll(); app.update()
        assert str(account.use['state']) == 'disabled'
        account.events.put(('ok',{'status':'connected','sharing':True,'identity':{'email':'test@example.invalid'}},[{'slug':'test-model','displayName':'Test model'}]))
        account.poll(); app.update()
        assert str(account.use['state']) == 'normal'
        assert account.picker.current() == 0
        shot('account.png', account)
        account.destroy()
    from town_ui import TownWindow
    app.state_data = c.fresh()
    with patch.object(app, 'persist'), patch.object(app, 'submit'):
        town = TownWindow(app); app.update()
        titles = [town.tabs.tab(tab, 'text') for tab in town.tabs.tabs()]
        assert {'Town', 'Gifts', 'Relationships', 'Discoveries', 'Journal', 'Bonds', 'Homes & routines',
                'Travel & texts', 'Groups', 'Careers'} <= set(titles)
        town.tabs.select(titles.index('Bonds')); app.update()
        network = town.nametowidget(town.tabs.select())
        tree = next(child for child in network.winfo_children() if child.winfo_class() == 'Treeview')
        assert len(tree.get_children()) == 10
        tree.selection_set('amy:april'); tree.event_generate('<<TreeviewSelect>>'); app.update()
        detail = next(child for child in network.winfo_children() if child.winfo_class() == 'Text')
        assert 'Philosophy' in detail.get('1.0','end')
        town.tabs.select(0)
        town.act(c.town.travel, 'boutique'); town.act(c.town.finish_drive)
        town.tabs.select(1); town.act(c.town.buy, 'plush')
        assert town.tabs.index(town.tabs.select()) == 1
        assert app.state_data['world']['inventory']['plush'] == 1
        town.tabs.select(2); town.attributes('-topmost', True); town.lift(); app.update()
        town.after(250, lambda: None); app.update()
        shot('town-relationships.png', town)
        town.act(c.town.travel, 'flowers'); town.act(c.town.finish_drive)
        town.meet('emily')
        assert app.state_data['routes']['emily']['channel'] == 'in_person'
        app.submit.assert_called_with(c.SCENE_DIRECTIONS[0])
    app.update()
    assert app.action_panel.winfo_ismapped()
    assert 'In-person conversation' in app.dialogue.get('1.0', 'end')
    c.commit(app.state_data, c.ACTION_PREFIX + 'I wave hello.', {
        'narration': 'Emily smiles and waves back.', 'dialogue': 'Hello again!',
        'choices': ['How are you?', 'Nice flowers.', 'Busy today?', 'Shall we sit?'],
        'memory': 'They met in person.'})
    app.render(); app.update()
    assert 'Emily smiles and waves back.' not in app.actions.get('1.0', 'end')
    assert 'Emily smiles and waves back.' in app.dialogue.get('1.0', 'end')
    assert app.action_panel.winfo_x() > app.dialogue.master.winfo_x()
    assert app.action_send.winfo_ismapped()
    assert len(app.action_choices) == 4
    for tone, button in zip(c.REPLY_TONES, app.action_choices):
        assert tone + ' · ' in button['text']
        assert button.winfo_ismapped()
        assert button.winfo_rooty() + button.winfo_height() <= app.winfo_rooty() + app.winfo_height()
    assert app.actions.winfo_height() >= 40, 'Action history clipped'
    assert app.action_entry.winfo_ismapped()
    with patch.object(app, 'submit') as submit:
        app.action_choices[0].invoke()
        submit.assert_called_once_with(c.ACTION_PREFIX + c.action_choices(app.state_data)[0])
        submit.reset_mock()
        app.action_entry.insert(0, 'I look at the flowers.')
        app.custom_action()
        submit.assert_called_once_with(c.ACTION_PREFIX + 'I look at the flowers.')
    app.lift(); app.update()
    app.after(300, app.quit); app.mainloop()
    shot('hangout-compact.png')
    app.set_busy(True)
    assert str(app.action_send['state']) == 'disabled'
    assert all(str(b['state']) == 'disabled' for b in app.action_choices)
    app.set_busy(False)
    with patch.object(app, 'persist'):
        app.select('emily')
        assert not c.is_texting(app.state_data)
    c.town.travel(app.state_data, 'square'); app.render(); app.update()
    assert not app.action_panel.winfo_ismapped()
    assert 'Back to phone texts' in app.dialogue.get('1.0', 'end')
    with patch.object(app, 'persist'):
        app.pending = None
        app.idle_clock -= 61
        minute = app.state_data['world']['minute']
        app.poll()
        assert app.state_data['world']['minute'] == minute
    import groups
    app.state_data = c.fresh()
    with patch.object(app, 'persist'):
        c.town.travel(app.state_data, 'home'); c.town.finish_drive(app.state_data)
        app.render(); app.home_window(); app.update()
        home = app.home_activity
        before = app.state_data['world']['minute']
        home.act(c.town.home_action, c.town.HOME_ACTIONS['garrett'][0])
        assert app.state_data['world']['minute'] == before + 20
        assert 'noodle recipe' in home.journal.get('1.0','end')
        home.destroy()
        app.state_data = c.fresh()
        c.town.travel(app.state_data, 'flowers'); c.town.finish_drive(app.state_data)
        c.town.meet(app.state_data, 'emily')
        c.town.travel(app.state_data, 'track', 'emily'); c.town.finish_drive(app.state_data)
        app.render(); app.show_world_windows(); app.update()
        assert app.group_selected and app.action_panel.winfo_ismapped()
        assert str(app.group_button['state']) == 'normal'
        response={'narration':'They gather beside the track.',
                  'emotions': {'garrett':'content', 'emily':'grateful', 'sophie':'playful'},
                  'lines':[{'speaker':'Emily Fields','text':'Hello!'}, {'speaker':'Sophie Parker','text':'Glad you came.'}],
                  'action_choices':['I wave to the team.', 'I clap for Sophie.', 'I jog in slow motion.', 'I wink at Emily.'],
                  'choices':['How was practice?','Want a break?','Nice afternoon.','Show us the track.']}
        with patch.object(groups, 'generate', return_value=response):
            app.action_entry.insert(0, 'I wave to everyone.')
            app.action_send.invoke()
            deadline=time.monotonic()+3
            while app.busy and time.monotonic()<deadline:
                app.after(20,app.quit); app.mainloop()
        assert not app.busy
        assert app.feelings.labels == [('Garrett Han (You)', 'content'), ('Emily Fields', 'grateful'), ('Sophie Parker', 'playful')]
        assert 'Sophie Parker' in app.dialogue.get('1.0','end')
        assert all(str(b['state'])=='normal' for b in app.choices)
        assert 'Flirtatious · I wink at Emily.' in app.action_choices[3]['text']
        with patch.object(app, 'submit') as submit:
            app.action_choices[3].invoke()
            submit.assert_called_once_with(c.ACTION_PREFIX + response['action_choices'][3])
        assert not app.state_data['routes']['sophie']['dialogue']
        assert 'I wave to everyone.' in app.actions.get('1.0','end')
        assert 'I wave to everyone.' not in app.dialogue.get('1.0','end')
        assert response['narration'] in app.dialogue.get('1.0','end')
        assert response['narration'] not in app.actions.get('1.0','end')
        groups.disband(app.state_data)
        app.render()
        assert not app.group_selected and str(app.group_button['state']) == 'disabled'
        app.state_data = c.fresh('rei')
        app.state_data['active'] = 'yuriko'
        gestures = ['I give Yuriko a wave from the far end of the workbench.',
                    'I set my phone face down and lean in to see the little details on her model.',
                    'I give the tiny theatre a standing ovation from the tips of two fingers.',
                    'I hold the loose edge of the backdrop steady while Yuriko lines it up with the stage.']
        app.state_data['routes']['yuriko'].update(channel='in_person', ordered_action_tones=True, action_choices=gestures)
        app.render(); app.update()
        last = app.action_choices[3]
        assert last['text'] == '4  Supportive · ' + gestures[3]
        canvas = last.master.master
        canvas.yview_moveto(1); app.update()
        assert last.winfo_rooty() + last.winfo_height() <= canvas.winfo_rooty() + canvas.winfo_height()
        assert app.actions.winfo_height() >= 40 and app.action_send.winfo_ismapped()
        with patch.object(app, 'submit') as submit:
            last.invoke()
            submit.assert_called_once_with(c.ACTION_PREFIX + gestures[3])
        members = [who for who in c.CONTACTS if who != 'rei' and c.hidden.contact(app.state_data, who)]
        app.select_group(groups.create_text(app.state_data, 'Everyone', members))
        app.update()
        assert app.feelings.labels == c.feeling_labels(app.state_data, members)
        assert app.feelings.scroll.winfo_ismapped()
        app.feelings.canvas.xview_moveto(1)
        app.update()
        assert app.feelings.canvas.xview()[1] == 1

        from town_ui import LocalConversation
        app.state_data['world']['npcs'] = ['Maya']
        c.town.commit_npc(app.state_data, 'Maya', 'Good luck!', {
            'narration':'Maya waves.', 'lines':[{'speaker':'Maya', 'text':'Thanks!'}],
            'choices':['See you.', 'Any time.', 'Good shift?', 'Hi again.'],
            'emotions':{'rei':'hopeful', 'Maya':'grateful'}})
        window = TownWindow(app)
        local = LocalConversation(window, 'Maya')
        app.update()
        assert local.feelings.winfo_ismapped()
        assert local.bond.winfo_ismapped() and local.bond.stats['closeness'] == 2
        assert 'attraction' not in local.bond.stats
        assert local.feelings.labels == [('Rei Takamura (You)', 'hopeful'), ('Maya', 'grateful')]
        local.panel_switch.invoke()
        assert all(tone in button['text'] for tone, button in zip(c.PERSONAL_TONES, local.choices))
        with patch.object(local, 'submit') as submit:
            local.choices[3].invoke()
            submit.assert_called_once_with(c.personal_choices(app.state_data, local.chat())[3])
        window.destroy()
        app.state_data = c.fresh('rei')
        c.town.summon(app.state_data, 'emily')
        app.switch_chat(False)
        window = TownWindow(app)
        goals = dict(conversation='Ask about her greenhouse.', activity='Try a dance step together.', kiss=c.dating.KISS)
        def widgets(parent):
            for child in parent.winfo_children():
                yield child
                yield from widgets(child)
        with patch.object(c.dating, 'generate_invitation', return_value=dict(answer='yes', reply='just us? yes!', goals=goals)), patch.object(app, 'submit') as submit:
            window.tabs.select(2)
            ask = next(w for w in widgets(window.tabs) if w.winfo_class() == 'TButton' and w['text'] == 'Ask on a date'
                       and any(n.winfo_class()=='TLabel' and n['text'].startswith('Emily ·') for n in w.master.winfo_children()))
            ask.invoke()
            deadline = time.monotonic() + 5
            while app.busy and time.monotonic() < deadline:
                app.after(20, app.quit); app.mainloop()
            assert not app.busy
            dialog = next(w for w in window.winfo_children() if w.winfo_class() == 'Toplevel')
            assert any(w.winfo_class() == 'TLabel' and 'just us? yes!' in w['text'] for w in widgets(dialog))
            next(w for w in widgets(dialog) if w.winfo_class() == 'TButton' and w['text'] == 'Continue to hangout').invoke()
            app.update()
            assert app.goal_button.winfo_ismapped() and '0/3' in app.goal_button['text']
            with patch.object(game.messagebox, 'showinfo') as checklist:
                app.goal_button.invoke()
                assert all(label in checklist.call_args.args[1] for label in goals.values())
    with patch.object(app, 'persist'), patch.object(app, 'submit'):
        app.state_data = c.fresh('rei')
        app.play_screen(); app.update()
        view = app.open_profiles('emily'); app.update()
        assert view.status.cget('text') == 'Best friends'
        assert view.values['Birthday'].cget('text') == 'November 4'
        assert 'greenhouse' in view.notes.get('1.0', 'end')
        assert all('bedroom' not in str(path) for _, path in view.variants)
        view.next.invoke(); app.update()
        assert view.index == 1 and view.picture.cget('image')
        view.people.selection_clear(0, 'end')
        view.people.selection_set(view.keys.index('yuriko'))
        view.people.event_generate('<<ListboxSelect>>'); app.update()
        assert view.status.cget('text') == 'Siblings'
        view.refresh('emily')
        shot('profiles.png', view)
        view.destroy()
        app.open_calendar(); app.update()
        from datetime import date
        app.calendar_view.show(date(2050, 11, 4))
        shot('calendar.png', app.calendar_view)
        app.calendar_view.destroy()
        town_view = TownWindow(app); app.update()
        shot('town-roam.png', town_view)
        town_view.destroy()
        app.toggle_chat_window(); app.update()
        assert app.chat_detached and app.tk.call('wm','title', app.chat_shell) == 'Winterfield · Conversation'
        assert app.entry.winfo_toplevel() == app.chat_shell
        app.toggle_chat_window(); app.update()
        assert not app.chat_detached and app.entry.winfo_toplevel() == app
    app.destroy()
print('UI smoke checks passed. Screenshots saved in tests/screenshots.')
