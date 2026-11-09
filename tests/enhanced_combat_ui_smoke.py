"""Real Tk selection, training and workshop flow; mocked provider and saves."""
import copy
import sys
import time
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from unittest.mock import patch
from PIL import ImageGrab
import game
import game_core as core
import grove
import combat
import combat_ui
import combat_engine as engine
import combat_workshop as workshop
from combat_profiles import profile
from test_enhanced_combat import custom_state,candidates

out=core.ROOT/'tests/screenshots'; out.mkdir(exist_ok=True)
with patch.object(game.Game,'check'),patch.object(game.Game,'begin_incoming'),patch.object(game.Game,'persist'),patch.object(grove.GrovePump,'tick'):
    app=game.Game(); errors=[]; app.report_callback_exception=lambda *e:errors.append(e)
    app.state_data=s=core.fresh('ivan'); s['world']['time_mode']='paused'; s['world']['location']='park'
    for who in ('ivan','sylvanis'): s['world']['cast'][who].update(location='park',journey=None)
    app.play_screen(); app.update(); f=combat.start(s,'sylvanis','challenge'); f['seed']=17
    combat_ui.open_combat(app); app.update(); v=app.combat_view
    def settle():
        until=time.monotonic()+8
        while v.working and time.monotonic()<until: app.update(); time.sleep(.02)
        app.update(); assert not v.working
    def shot(name):
        app.update(); ImageGrab.grab(window=app.winfo_id()).save(out/name)
    def bounds(w):
        app.update(); assert w.winfo_ismapped()
        assert w.winfo_rooty()+w.winfo_height()<=app.winfo_rooty()+app.winfo_height(),str(w)
    app.geometry('1000x800'); app.update()
    assert v.master is app.presence_view.master
    bounds(v.execute_button); shot('enhanced-combat-selection.png')
    v.amp_choice.set('Fire'); v.selection_detail(); assert 'Mana' in v.move_detail.get('1.0','end')
    v.action_kind.set('Unique skills'); v.populate_moves(); v.move_choice.set('Fivefold Ruin'); v.populate_amps()
    assert list(v.amp_map)==['None']; bounds(v.execute_button); shot('enhanced-combat-unique.png')
    v.action_kind.set('Utility'); v.populate_moves(); v.move_choice.set('Direct strike'); v.populate_amps()
    v.target_choice.set('concrete partition'); v.selection_detail()
    with patch.object(combat,'ask_ai',side_effect=ValueError('Test narration failure')): v.submit(); settle()
    assert f['turn']==1 and f['exchanges'][0]['narration']
    assert 'resolved outcome' in v.status['text']; bounds(v.execute_button); shot('enhanced-combat-fallback.png')
    assert f['enemy']['active_form'] and f['enemy']['trait_uses']
    f['enemy']['stamina']=5; v.refresh(); app.update(); assert 'Recover' in v.opponent_intent['text']
    f['enemy']['energy']=0; f['enemy']['stamina']=100; v.refresh(); app.update()
    assert engine.opponent_plan(s)['kind'] in ('martial','utility')
    combat.concede(s); combat.close(s); v.set_page('academy'); app.update()
    bounds(v.learn_button); shot('enhanced-combat-training.png')
    app.state_data=s=custom_state(); s['world']['time_mode']='paused'
    v.set_page('workshop'); app.update()
    with patch.object(combat,'ask_ai',return_value={'skills':candidates(s)}): v.generate_skills(); settle()
    assert len(workshop.book(s)['candidates'])==3; bounds(v.absorb_button); shot('enhanced-combat-candidates.png')
    v.run(v.absorb_skill); app.update()
    assert len(profile(s,s['player'])['moveset']['unique'])==1 and workshop.remaining(s)==1440
    shot('enhanced-combat-absorbed.png')
    more=candidates(s)
    for i,item in enumerate(more): item['name']='New Echo '+str(i)
    with patch.object(combat,'ask_ai',return_value={'skills':more}): v.generate_skills(); settle()
    assert str(v.absorb_button['state'])=='disabled'; bounds(v.absorb_button); shot('enhanced-combat-cooldown.png')
    old=copy.deepcopy(workshop.book(s))
    with patch.object(combat,'ask_ai',side_effect=ValueError('Test workshop failure')): v.generate_skills(); settle()
    assert workshop.book(s)==old; shot('enhanced-combat-workshop-error.png')
    assert not errors,errors
    app.sounds.close(); app.destroy()
print('Enhanced combat UI passed: compact selection, unique actions, opponent form/initiative, resolved fallback, academy, skill generation/absorption/cooldown and failed generation persistence. Eight screenshots; provider and saves mocked.')
