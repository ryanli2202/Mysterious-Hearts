"""One protagonist-specific Story tab; isolated saves and no AI requests."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from unittest.mock import patch
from tkinter import ttk
from PIL import ImageGrab
import game, game_core as core, grove, campaign_ui, interpol, charles_quest
from flashback_helpers import finish_memories


def widgets(parent):
    for child in parent.winfo_children():
        yield child
        yield from widgets(child)


def text(parent):
    return '\n'.join(str(w.cget('text')) for w in widgets(parent) if 'text' in w.keys())


out=core.ROOT/'tests/screenshots';out.mkdir(exist_ok=True)
with patch.object(game.Game,'check'), patch.object(game.Game,'begin_incoming'), patch.object(game.Game,'persist'), patch.object(grove.GrovePump,'tick'):
    app=game.Game();errors=[];app.report_callback_exception=lambda *e:errors.append(e)
    try:
        for player in ('rei','garrett','fox','gordon','emily'):
            s=app.state_data=core.fresh(player);s['world']['time_mode']='paused'
            finish_memories(s)
            app.play_screen();app.update()
            campaign_ui.open_in_person(app,'Story');view=app.campaign_view;app.update()
            buttons=[str(w.cget('text')) for w in widgets(view) if isinstance(w,ttk.Button)]
            assert buttons.count('Story')==1
            assert not any(name in buttons for name in ('Rei’s story','Garrett’s story','Fox’s story','Gordon’s story'))
            content=text(view.body)
            if player=='rei':assert 'WHAT REMAINS' in content and 'Find Charles' not in content
            elif player=='garrett':
                assert 'Find Charles' in content and 'WHAT REMAINS' not in content
                travel=next(w for w in widgets(view.body) if isinstance(w,ttk.Button) and str(w.cget('text'))=='Travel to the current objective')
                travel.invoke();app.update()
                assert s['world']['location']==charles_quest.objective(s)[1]
                choice=next(w for w in widgets(view.body) if isinstance(w,ttk.Button) and str(w.cget('text'))==charles_quest.STEPS[0][3][0])
                with patch('campaign_dialogue.maybe_open',return_value=True) as opened:
                    choice.invoke()
                    opened.assert_called_once_with(app,charles_quest.advance,(0,))
            elif player in ('fox','gordon'):
                assert player.upper()+'’S STORY' in content and 'Find Charles' not in content and 'WHAT REMAINS' not in content
                view.act(core.town.travel,'interpol_hq')
                partner='gordon' if player=='fox' else 'fox'
                s['world']['cast'][partner].update(location='interpol_hq',journey=None,activity='Available')
                view.act(interpol.begin,'blackhaven');app.update()
                assert interpol.read(s)['active']['partner']==partner
                assert 'Travel to objective with field partner' in text(view.body)
                assert 'Suspend operation' in text(view.body)
            else:
                assert 'No personal story campaign' in content
                assert 'WHAT REMAINS' not in content and 'Find Charles' not in content and 'Interpol campaign' not in content
            app.geometry('1000x800');app.update()
            ImageGrab.grab(window=app.winfo_id()).save(out/('player-story-'+player+'.png'))
            assert view.winfo_viewable() and view.winfo_toplevel() is app
            assert view.winfo_rooty()+view.winfo_height()<=app.winfo_rooty()+app.winfo_height()
        assert not errors,errors
        print('Player Story tab passed: Rei, Garrett, Fox, Gordon, empty state, travel, action routing, active cases and compact layout.')
    finally:app.sounds.close();app.destroy()
