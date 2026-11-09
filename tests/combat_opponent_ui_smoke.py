"""Actual in-person opponent intentions, failure/retry and forms; mocked AI only."""
import copy
import sys
import time
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from unittest.mock import patch
from PIL import ImageGrab
import combat
import combat_ui
import game
import game_core as core
import grove

out=core.ROOT/'tests/screenshots'; out.mkdir(exist_ok=True)
with patch.object(game.Game,'check'), patch.object(game.Game,'begin_incoming'), patch.object(game.Game,'persist'), patch.object(grove.GrovePump,'tick'):
    app=game.Game(); errors=[]
    app.report_callback_exception=lambda *e:errors.append(e)
    app.state_data=s=core.fresh('ivan'); s['world']['time_mode']='paused'
    s['world']['location']='iron_circle'
    for who in ('ivan','sylvanis'): s['world']['cast'][who].update(location='iron_circle',journey=None)
    app.play_screen(); app.update()
    f=combat.start(s,'sylvanis','challenge'); f['seed']=21
    combat_ui.open_combat(app); app.update(); view=app.combat_view

    def shot(name):
        app.update(); ImageGrab.grab(window=app.winfo_id()).save(out/name)

    def settle():
        deadline=time.monotonic()+5
        while view.working and time.monotonic()<deadline: app.update(); time.sleep(.02)
        assert not view.working

    def judged():
        plan,_=combat.tactics.prepare(s)
        return dict(player_feasible=True,complexity=10,advantage=0,enemy_mode=plan['mode'],enemy_art=plan['art'],
                    enemy_action=plan['action'],reason='Sylvanis initiates the declared attack; Ivan attempts to defend.')

    def bounds():
        app.update()
        for widget in (view.opponent_intent,view.action):
            assert widget.winfo_ismapped()
            assert widget.winfo_rooty()+widget.winfo_height()<=app.winfo_rooty()+app.winfo_height()
        buttons=[w for row in view.body.winfo_children() for w in row.winfo_children() if hasattr(w,'cget') and w.winfo_class()=='TButton']
        submit=next(w for w in buttons if 'Submit defence' in w.cget('text'))
        assert submit.winfo_ismapped()
        assert submit.winfo_rooty()+submit.winfo_height()<=app.winfo_rooty()+app.winfo_height()

    assert view.master is app.presence_view.master
    assert 'Preparing Black-eyed Shadow Dominion' in view.opponent_intent.cget('text')
    assert 'Umbrakinesis' in view.opponent_intent.cget('text')
    shot('combat-opponent-opening.png'); bounds()
    app.geometry('1000x800'); app.update(); bounds(); shot('combat-opponent-compact.png')
    view.mode.set('Guard'); view.action.insert('1.0','I keep my guard up and move off the shadow attack line.')
    before=copy.deepcopy(f)
    with patch.object(combat,'ask_ai',side_effect=ValueError('Test provider failure')):
        view.submit(); settle()
    assert f==before
    assert 'Test provider failure' in view.status.cget('text')
    assert view.action.get('1.0','end').strip()
    bounds(); shot('combat-opponent-retry.png')
    with patch.object(combat,'ask_ai',return_value=judged()): view.submit(); settle()
    assert f['turn']==1 and f['enemy']['trait_uses']==1
    assert f['enemy']['active_form']['name']=='Black-eyed Shadow Dominion'
    assert 'Initiate a ' in view.opponent_intent.cget('text')
    bounds(); shot('combat-opponent-active-form.png')
    f['enemy']['stamina']=7; view.refresh(); app.update()
    assert 'Recover stamina' in view.opponent_intent.cget('text')
    bounds(); shot('combat-opponent-recovery.png')
    f['enemy']['energy']=0; f['enemy']['stamina']=100; view.refresh(); app.update()
    assert 'Conserve mana' in view.opponent_intent.cget('text')
    view.action.insert('1.0','I hold position and protect my head.'); view.mode.set('Guard')
    with patch.object(combat,'ask_ai',return_value=judged()): view.submit(); settle()
    assert f['enemy']['form_until']<=f['elapsed']
    bounds(); shot('combat-opponent-exhausted-form.png')
    assert not errors,errors
    app.sounds.close(); app.destroy()
print('Opponent combat UI passed: opening intent, compact controls, failure/retry, active form, martial follow-up, recovery and mana expiry. Six screenshots; AI mocked, no story writes.')
