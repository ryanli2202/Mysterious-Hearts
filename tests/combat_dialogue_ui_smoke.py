"""Render dialogue and exercise asynchronous responses without network/save writes."""
import sys
import time
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from unittest.mock import patch
from PIL import ImageGrab
import game, game_core as core, combat, combat_ui, grove, hangout_combat_ui

out=core.ROOT/'tests/screenshots'; out.mkdir(exist_ok=True)
with patch.object(game.Game,'check'), patch.object(game.Game,'begin_incoming'), patch.object(game.Game,'persist'), patch.object(grove.GrovePump,'tick'):
    app=game.Game(); errors=[]
    app.report_callback_exception=lambda *e:errors.append(e)
    app.state_data=s=core.fresh('garrett'); s['world']['time_mode']='paused'
    s['world']['location']='park'
    for who in ('garrett','rei','emily','samantha'):
        s['world']['cast'][who].update(location='park',journey=None)
    app.play_screen(); app.update(); combat_ui.open_combat(app)
    hub=app.combat_view
    view=app.hangout_view.combat_actions
    def shot(name):
        app.update(); ImageGrab.grab(window=app.winfo_id()).save(out/name)
    def respond(kind,accepted=True):
        responses=[] if kind=='attack' else [dict(intent=kind,player_line='Care for a friendly spar?')]
        responses.append(dict(dialogue='All right. Keep your guard up.' if accepted else 'Not today. I need some space.',narration='Garrett steps forward; she takes a step back.',accepted=accepted))
        with patch.object(combat,'ask_ai',side_effect=responses):
            view.request(kind)
            deadline=time.monotonic()+5
            while view.working and time.monotonic()<deadline: app.update(); time.sleep(.02)
        assert not view.working and view.response,view.error
    hangout_combat_ui.open_dialogue(app,'rei'); shot('combat-dialogue-options.png')
    assert app.in_person_chat.winfo_ismapped() and not hub.winfo_ismapped()
    respond('spar',False); shot('combat-dialogue-refusal.png')
    assert not combat.active(s)
    assert app.hangout_view.canvas.exchange.speeches == [('rei','Not today. I need some space.')]
    view.continue_scene(); hangout_combat_ui.open_dialogue(app,'rei'); respond('spar')
    shot('combat-dialogue-agreement.png')
    assert combat.active(s) and not hub.winfo_ismapped()
    assert app.hangout_view.canvas.exchange.player == 'Care for a friendly spar?'
    assert app.hangout_view.canvas.exchange.speeches == [('rei','All right. Keep your guard up.')]
    view.continue_scene(); app.update(); assert hub.title.cget('text').startswith('SPAR')
    assert hub.winfo_ismapped()
    combat.concede(s); combat.close(s)
    hangout_combat_ui.open_dialogue(app,'emily'); view.confirm_attack()
    assert view.confirming
    shot('combat-dialogue-attack.png')
    respond('attack'); assert not combat.active(s) and not combat.present(s,'emily')
    assert app.in_person_chat.winfo_ismapped() and app.hangout_view.canvas.exchange.speeches
    assert app.hangout_view.canvas.exchange.player == ''
    assert 'player' not in app.hangout_view.canvas.bubble_bounds
    shot('combat-dialogue-flee.png')
    view.continue_scene(); app.update(); assert not app.in_person_chat.winfo_ismapped()
    app.geometry('1000x800'); hangout_combat_ui.open_dialogue(app,'samantha')
    shot('combat-dialogue-compact.png')
    assert view.panel.winfo_rooty()+view.panel.winfo_height() <= app.winfo_rooty()+app.winfo_height()
    with patch.object(combat,'ask_ai',side_effect=RuntimeError('offline')):
        view.request('spar')
        deadline=time.monotonic()+5
        while view.working and time.monotonic()<deadline: app.update(); time.sleep(.02)
    assert not app.busy and not view.response and 'offline' in view.error
    import relationship_dynamics
    relationship_dynamics.stats(s,'samantha')['trust']=60
    with patch.object(combat,'ask_ai',side_effect=[dict(intent='learn',player_line='Would you teach me Streetfighting?'),dict(dialogue='Watch my stance.',narration='Samantha demonstrates her footwork.',accepted=True)]):
        view.request('learn','Streetfighting')
        deadline=time.monotonic()+5
        while view.working and time.monotonic()<deadline: app.update(); time.sleep(.02)
    assert view.response and view.response['kind']=='learn',view.error
    assert app.hangout_view.canvas.exchange.speeches==[('samantha','Watch my stance.')]
    assert not hub.winfo_ismapped()
    shot('combat-dialogue-lesson.png')
    app.destroy(); assert not errors,errors
print('Combat dialogue UI smoke passed; seven screenshots, failed-provider retry and lesson. AI mocked; no save writes.')
