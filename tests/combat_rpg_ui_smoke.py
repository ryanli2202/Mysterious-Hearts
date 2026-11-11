"""MH-007 real Tk interaction, compact/large states, no saves or providers."""
import copy
import json
import sys
import time
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from unittest.mock import patch
from PIL import ImageGrab
import game, game_core as core, grove, combat, combat_ui, combat_engine as engine
import combat_rpg_ui as rpg
import combat_moves as moves
from combat_profiles import profile

out=core.ROOT/'tests/screenshots'; out.mkdir(exist_ok=True)
with patch.object(game.Game,'check'),patch.object(game.Game,'begin_incoming'),patch.object(game.Game,'persist'),patch.object(grove.GrovePump,'tick'):
    app=game.Game(); errors=[]; app.report_callback_exception=lambda *e:errors.append(e)
    try:
        s=app.state_data=core.fresh('ivan'); s['world']['time_mode']='paused'; s['world']['location']='park'
        for who in ('ivan','sylvanis'): s['world']['cast'][who].update(location='park',journey=None)
        app.play_screen()
        with patch.object(combat,'consent',return_value=(True,'')): f=combat.start(s,'sylvanis','challenge')
        combat_ui.open_combat(app); v=app.combat_view
        def shot(name):
            app.update(); time.sleep(.12); app.update()
            ImageGrab.grab(window=app.winfo_id()).save(out/('rpg-combat-'+name+'.png'))
        def fits():
            app.update()
            assert v.execute_button.winfo_viewable()
            assert v.body.winfo_rootx()>=app.winfo_rootx(), ('left edge',v.body.winfo_rootx(),app.winfo_rootx(),v.winfo_width(),v.body.winfo_width())
            assert v.execute_button.winfo_rootx()+v.execute_button.winfo_width()<=app.winfo_rootx()+app.winfo_width()
            assert v.execute_button.winfo_rooty()+v.execute_button.winfo_height()<=app.winfo_rooty()+app.winfo_height()
            for panel in v.combat_portrait_rail.winfo_children():
                assert panel.winfo_rooty()+panel.winfo_height()<=v.combat_portrait_rail.winfo_rooty()+v.combat_portrait_rail.winfo_height(), 'HUD clipped'
        app.geometry('1280x900'); app.update(); fits(); shot('large')
        assert v.combat_portrait_images['player'].height()>=320
        app.geometry('1000x800'); app.update(); fits(); shot('compact')
        assert v.combat_portrait_images['player'].height()>250
        before=copy.deepcopy(f)
        v.toggle_favourite(); favourite=v.ui_prefs['favourites'][0]
        v.choose_favourite(favourite); v.toggle_tactics(); app.update(); shot('tactics')
        assert f==before, 'Selection and preferences changed combat state'
        v.inspect_fighter('enemy'); app.update(); shot('inspection'); v.rpg_drawer.destroy()
        v.technique_cards(); app.update(); shot('techniques'); v.rpg_drawer.destroy()
        app.focus_force(); v.technique_cards(); app.update()
        card=app.focus_get(); assert card.winfo_class()=='Button'
        card.event_generate('<Return>'); app.update()
        assert not v.rpg_drawer.winfo_exists() and f==before
        v.display_settings(); app.update(); shot('settings'); v.rpg_drawer.destroy()
        v.combat_options(); app.update(); shot('forms'); v.rpg_drawer.destroy()
        v.tactics_visible=False
        v.amp_choice.set('Fire'); v.selection_detail()
        assert v.rpg_ghost['energy']>0 and f==before
        v.target_choice.set('concrete partition'); v.selection_detail(); shot('terrain-target')
        assert f==before
        ids=[m['id'] for m in moves.actions(profile(s,s['player']))][:6]
        v.save_ui(favourites=ids,hints_dismissed=True,text_size=14); v.refresh(); app.update(); fits(); shot('large-text-pins')
        v.quick_slots(); app.update(); shot('quick-slots'); v.rpg_drawer.destroy()
        v.combat_options(); app.update(); shot('forms-large-text'); v.rpg_drawer.destroy()
        original_name=f['opponent_profile']['name']; f['opponent_profile']['name']='A very long generated opponent name for layout checks'
        f['enemy']['restrained']=2; v.refresh(); app.update(); fits(); shot('long-name-states')
        f['opponent_profile']['name']=original_name; f['enemy']['restrained']=0
        v.ui_setting(text_size=12); app.update(); fits()
        v.ui_setting(text_size=14)
        assert rpg.preferences(json.loads(json.dumps(s)))==v.ui_prefs
        v.ui_setting(density='Cinematic'); app.update(); fits(); shot('cinematic')
        v.ui_setting(text_size=10,favourites=[favourite]); v.choose_favourite(favourite)
        # Empty categories and removed move IDs remain understandable and safe.
        v.action_art.set('Unknown legacy art'); v.populate_moves()
        assert not v.move_map and str(v.execute_button['state'])=='disabled'
        shot('empty-category'); v.action_art.set('All arts'); v.populate_moves()
        v.save_ui(favourites=['removed:move']); v.quick_slots(); app.update(); shot('unavailable-slot'); v.rpg_drawer.destroy()
        v.choose_favourite('removed:move'); assert f['turn']==0
        v.save_ui(favourites=[favourite]); v.choose_favourite(favourite)
        # A saved active fight restores preferences and authoritative encounter state.
        restored=json.loads(json.dumps(s)); app.state_data=restored; v.refresh(); app.update(); fits()
        assert v.ui_prefs['favourites']==[favourite] and combat.active(restored)['turn']==0
        app.state_data=s; v.refresh(); app.update()
        with patch.object(combat,'ask_ai',side_effect=ValueError('Offline test')):
            v.submit(); v.submit()
            assert f['turn']==1
            deadline=time.monotonic()+8
            while v.working and time.monotonic()<deadline: app.update(); time.sleep(.02)
        assert not v.working and f['turn']==1
        assert 'ui_resource_audit' in f['exchanges'][-1]
        assert 'resolved outcome' in v.status.cget('text')
        v.drawer('LAST EXCHANGE',rpg.breakdown(f)); app.update(); shot('breakdown'); v.rpg_drawer.destroy()
        f['player']['stamina']=0; f['player']['energy']=0; v.refresh(); app.update()
        assert str(v.execute_button['state'])=='disabled'; shot('depleted')
        v.select_category('Utility'); v.rpg_drawer.destroy()
        v.move_choice.set('Recover'); v.populate_amps(); assert str(v.execute_button['state'])=='normal'
        # Missing image providers use safe dark/transparent fallback without blocking actions.
        with patch.object(rpg,'source_image',return_value=__import__('PIL.Image',fromlist=['Image']).new('RGB',(16,16),'#10121c')),patch.object(rpg.combat_portraits,'portrait',side_effect=OSError('missing fixture')):
            v.paint_stage(); app.update(); shot('missing-art')
        combat.concede(s); v.refresh(); app.update(); shot('finished')
        assert v.phase_label.cget('text')=='FINISHED'
        v.run(v.close_encounter); app.update()
        assert combat.active(s) is None and not v.winfo_ismapped()
        assert not errors, errors
    finally:
        app.sounds.close(); app.destroy()
print('MH-007 smoke passed: large/compact, all eight features, preferences, nonmutating selection, once-only resolve, fallback, depleted resources and missing art. Providers/saves mocked.')
