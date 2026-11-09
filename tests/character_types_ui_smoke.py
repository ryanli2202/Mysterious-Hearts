"""Render simple NPC chat and phone controls without model calls or save writes."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from unittest.mock import patch
from PIL import ImageGrab
import game
import game_core as core
import groups
import grove
import phone_numbers

with patch.object(game.Game, 'check', lambda self: None), \
     patch.object(game.Game, 'persist', lambda self: None), \
     patch.object(game.Game, 'begin_incoming', lambda self: None), \
     patch.object(grove.GrovePump, 'tick', lambda self: None):
    app = game.Game()
    errors = []
    app.report_callback_exception = lambda *args: errors.append(args)
    try:
        s = app.state_data = core.fresh('rei')
        s['world']['location'] = 'cafe'
        s['world']['cast']['rei'].update(location='cafe', journey=None)
        s['world']['npcs'] = ['Maya']
        s['npc_chats'] = {'Maya':dict(history=[dict(speaker='Maya', text='Good morning. What can I get you?')],
            connection=dict(status='familiar face', trust=35, closeness=0))}
        app.play_screen()
        gid = groups.open_local(s, 'Maya')
        app.select_group(gid)
        app.update()
        assert str(app.panel_switch.cget('state')) == 'disabled'
        assert not app.relationship_bars.winfo_manager()
        assert app.details.cget('text') == 'Town NPC · familiar face'
        out = core.ROOT/'tests'/'screenshots'
        out.mkdir(exist_ok=True)
        ImageGrab.grab(window=app.winfo_id()).save(out/'town-npc-simple-chat.png')
        groups.close_active(s, 'The conversation ended.')
        phone_numbers.add(s, phone_numbers.NUMBERS['Maya'])
        app.phone_window()
        phone = app.phone_activity
        phone.open_thread('npc:Maya', True)
        app.update()
        assert not phone.personal_suggestions.winfo_manager()
        assert not phone.personal_messages
        ImageGrab.grab(window=phone.winfo_id()).save(out/'town-npc-simple-phone.png')
        assert not errors, errors
        print('Town NPC familiarity, hidden relationship meters and ordinary phone chat verified.')
    finally:
        app.sounds.close()
        app.destroy()
