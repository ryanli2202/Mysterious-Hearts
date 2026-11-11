"""Exercise actual art scenes and controls without AI calls or player-save writes."""
import sys
import threading
import time
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from PIL import ImageGrab
import game
import game_core as core
import groups
import grove


out = core.ROOT / 'tests' / 'screenshots'
out.mkdir(exist_ok=True)
with patch.object(game.Game, 'check'), patch.object(game.Game, 'begin_incoming'), \
     patch.object(game.Game, 'persist'), patch.object(grove.GrovePump, 'tick'):
    app = game.Game()
    errors = []
    app.report_callback_exception = lambda *e: errors.append(e)
    app.state_data = s = core.fresh('rei')
    s['world']['location'] = 'cafe'
    for who in ('rei', 'emily', 'sophie'):
        s['world']['cast'][who].update(location='cafe', journey=None)
    s['world']['time_mode'] = 'paused'
    gid = groups.open_solo(s, 'emily')
    g = s['groups'][gid]
    g['history'].extend([
        dict(speaker='Rei Takamura (You)', text='This is a good spot. Shall we stay a little longer?'),
        dict(speaker='Narrator', text='Warm light pools across the table as the café settles into a quiet afternoon.'),
        dict(speaker='Emily Fields', text='I would like that. There is something about this place that makes it easy to forget the time.')])
    app.play_screen()
    app.update()
    view = app.hangout_view
    canvas = view.canvas

    def shot(name):
        app.update()
        ImageGrab.grab(window=app.winfo_id()).save(out / name)

    def fits():
        app.update()
        assert canvas.winfo_ismapped()
        for widget in (app.entry if view.mode == 'reply' else app.action_entry, app.end_hangout_button, app.status):
            assert widget.winfo_ismapped()
            assert widget.winfo_rooty() + widget.winfo_height() <= app.winfo_rooty() + app.winfo_height()
        assert canvas.controls_height < canvas.winfo_height() / 2
        for x, y, right, bottom in canvas.bubble_bounds.values():
            assert 0 <= x < right <= canvas.winfo_width()
            assert 0 <= y < bottom < canvas.winfo_height() - canvas.controls_height - 80

    assert set(canvas.portrait_items) == {'rei', 'emily'}
    assert canvas.exchange.player.startswith('This is a good spot.')
    assert canvas.narration_font.actual('slant') == 'italic'
    fits()
    shot('hangout-art-solo.png')
    app.geometry('1000x800')
    app.update()
    fits()
    shot('hangout-art-compact.png')
    with patch.object(app, 'submit') as submit:
        app.entry.insert(0, 'My spoken reply.')
        app.send.invoke()
        submit.assert_called_once_with('My spoken reply.')
        submit.reset_mock()
        view.action_tab.invoke()
        assert app.action_send.cget('text') == 'Do action'
        app.update()
        shot('hangout-art-actions.png')
        app.action_entry.insert(0, 'I wave hello.')
        app.action_send.invoke()
        submit.assert_called_once_with(core.ACTION_PREFIX + 'I wave hello.')
    view.reply_tab.invoke()
    g['personal_choices'] = ['A thoughtful question about your afternoon.']*4
    g['suggestions_requested'] = ['personal']
    app.panel_switch.invoke()
    app.update()
    assert all(b.winfo_ismapped() for b in app.choices)
    fits()
    shot('hangout-art-suggestions.png')
    with patch.object(app, 'submit') as submit:
        app.choices[0].invoke()
        submit.assert_called_once_with(g['personal_choices'][0])
    app.panel_switch.invoke()
    # Pending player speech is visible before a response arrives; cancelling restores the draft.
    gate = threading.Event()
    def delayed(*args, **kwargs):
        gate.wait(3)
        raise ValueError('Cancelled mock response')
    with patch.object(groups, 'generate', side_effect=delayed):
        app.submit('I am speaking now.')
        app.update()
        assert canvas.exchange.player == 'I am speaking now.'
        assert not canvas.exchange.speeches
        assert str(app.send['state']) == 'disabled'
        shot('hangout-art-pending.png')
        app.cancel_button.invoke()
        gate.set()
        app.update()
        assert not app.busy and app.entry.get() == 'I am speaking now.'
    # A completed generated response must replace pending speech, preserve the journal,
    # clear the composer, and return to the same scene after opening the phone.
    response = dict(narration='Emily sets her cup on the table.', dialogue='Then let us stay a while.',
                    choices=[], suggestions_deferred=True, memory='They lingered over coffee.')
    with patch.object(groups, 'generate', return_value=response):
        app.submit('Shall we stay?')
        deadline = time.monotonic()+5
        while app.busy and time.monotonic() < deadline:
            app.update()
            time.sleep(.01)
        assert not app.busy and app.pending is None, app.status['text']
        assert canvas.exchange.speeches == [('emily', response['dialogue'])]
        assert canvas.exchange.narration == response['narration']
        assert app.entry.get() == ''
        assert g['history'][-1]['text'] == response['dialogue']
    app.phone_window('Home')
    app.update()
    app.phone_activity.close_phone()
    app.update()
    assert canvas.winfo_ismapped() and canvas.exchange.speeches[0][1] == response['dialogue']
    # Physical actions stay out of speech bubbles, including after cancellation.
    gate.clear()
    with patch.object(groups, 'generate', side_effect=delayed):
        app.submit(core.ACTION_PREFIX+'I lift my cup.')
        app.update()
        assert canvas.exchange.player == '' and canvas.exchange.narration == 'I lift my cup.'
        app.cancel_button.invoke()
        gate.set()
        app.update()
        assert view.mode == 'action' and app.action_entry.get() == 'I lift my cup.'
        assert core.ACTION_PREFIX not in app.entry.get()
    view.reply_tab.invoke()
    gid = groups.open_group(s, ['emily', 'sophie'])
    g = s['groups'][gid]
    long_line = 'Every word of this long response should remain readable, even in a smaller window. ' * 24
    g['history'].extend([
        dict(speaker='Rei Takamura (You)', text='I am glad we could all meet.'),
        dict(speaker='Narrator', text='They gather around the café table.'),
        dict(speaker='Emily Fields', text=long_line),
        dict(speaker='Sophie Parker', text='I brought enough stories to keep us here all afternoon.')])
    app.show_in_person()
    app.update()
    assert set(canvas.portrait_items) == {'rei', 'emily', 'sophie'}
    assert len(canvas.pages['speech']) > 1
    canvas.page_controls['speech'][3].invoke()
    assert canvas.page_indices['speech'] == 1
    app.render()
    assert canvas.page_indices['speech'] == 1, 'Clock refresh must not reset reading position'
    fits()
    shot('hangout-art-group-long.png')
    view.next_voice.invoke()
    assert canvas.exchange.speeches[canvas.speech_index][0] == 'sophie'
    canvas.select_speaker('emily')
    assert canvas.exchange.speeches[canvas.speech_index][0] == 'emily'
    assert str(app.retry['state']) == 'disabled', 'Groups require an actual player turn'
    g['history'][-3]['text'] = 'The conversation continues around the table. ' * 48
    app.render()
    app.update()
    assert len(canvas.pages['narration']) > 1
    canvas.page_controls['narration'][3].invoke()
    assert canvas.page_indices['narration'] == 1
    shot('hangout-art-long-narration.png')
    # A town resident uses the same stage, with their portrait and correct speech anchor.
    groups.close_active(s, 'Test complete')
    s['world']['location'] = 'cafe'
    name = core.town.NPCS[0][0]
    s['world']['npcs'] = [name]
    local = groups.open_local(s, name)
    s['groups'][local]['history'].extend([
        dict(speaker='Narrator', text='You stop for a friendly conversation.'),
        dict(speaker=name, text='It is good to see you around town.')])
    app.show_in_person()
    app.update()
    assert name in canvas.portrait_items
    assert canvas.exchange.speeches == [(name, 'It is good to see you around town.')]
    shot('hangout-art-local.png')
    view.toggle_fullscreen()
    app.update()
    assert app.attributes('-fullscreen')
    view.set_fullscreen(False)
    app.update()
    app.end_hangout_button.invoke()
    app.update()
    assert app.presence_view.winfo_ismapped()
    assert not app.in_person_chat.winfo_ismapped()
    assert not errors, errors
    app.destroy()
print('Hangout art smoke passed: solo, group, locals, compact layout, paging, suggestions, pending speech, cancellation, full screen and ending.')
