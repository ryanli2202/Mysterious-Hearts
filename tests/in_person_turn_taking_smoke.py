"""Render uneven participation and a returning speaker in the main in-person window."""
import sys
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from PIL import ImageGrab
import game
import game_core as core
import grove
import groups

with patch.object(game.Game, 'check'), patch.object(game.Game, 'begin_incoming'), \
     patch.object(core, 'save'), patch.object(grove.GrovePump, 'tick'):
    app = game.Game()
    try:
        app.state_data = core.fresh('rei')
        app.play_screen()
        for person in app.state_data['autonomy']['people'].values(): person['next_decision'] = 10**12
        core.town.summon(app.state_data, 'emily')
        core.town.summon(app.state_data, 'sophie')
        gid = app.state_data['active_group']
        data = dict(narration='Sophie waits for Emily to answer.', choices=[], suggestions_deferred=True,
                    lines=[dict(speaker='Emily Fields', text='Tea. Definitely tea.')],
                    emotions={'rei':'content', 'emily':'content', 'sophie':'content'},
                    bond_moments={'emily':'none', 'sophie':'none'}, social_target='none', social_event='none')
        groups.commit(app.state_data, gid, 'What do you feel like?', data)
        data.update(narration='Emily glances at Sophie.', lines=[
            dict(speaker='Sophie Parker', text='You always say that.'),
            dict(speaker='Emily Fields', text='Because you keep asking.'),
            dict(speaker='Sophie Parker', text='Fair.')])
        groups.commit(app.state_data, gid, 'Tea it is.', data)
        app.show_in_person()
        app.select_group(gid)
        app.update()
        blocks = app.chat_blocks(pane='dialogue')
        rendered = '\n'.join(block[1] for block in blocks)
        for line in ['Tea. Definitely tea.', 'You always say that.', 'Because you keep asking.', 'Fair.']:
            assert line in rendered, rendered
        assert rendered.index('You always say that.') < rendered.index('Because you keep asking.') < rendered.index('Fair.')
        assert app.in_person_chat.winfo_ismapped()
        canvas = app.hangout_view.canvas
        assert canvas.exchange.speeches == [
            ('sophie', 'You always say that.'), ('emily', 'Because you keep asking.'), ('sophie', 'Fair.')]
        app.hangout_view.next_voice.invoke()
        app.update()
        assert canvas.speech_index == 1
        app.hangout_view.next_voice.invoke()
        app.update()
        assert canvas.speech_index == 2
        output = core.ROOT / '.test-tmp' / 'in-person-turn-taking.png'
        ImageGrab.grab(window=app.winfo_id()).save(output)
        print('In-person turn-taking smoke passed:', output)
    finally:
        app.sounds.close()
        app.destroy()
