"""Render guard roster, combat portrait rail, a guard hangout and enhanced Richter."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from unittest.mock import patch
from PIL import ImageGrab
import game,game_core as core,grove,campaign_ui,combat,combat_ui,campaign_dialogue,guard_portraits as art
import organisation_guards as guards
from test_major_campaigns import arrive,investigate,clear

out=core.ROOT/'tests/screenshots';out.mkdir(exist_ok=True)
with patch.object(game.Game,'check'),patch.object(game.Game,'begin_incoming'),patch.object(game.Game,'persist'),patch.object(grove.GrovePump,'tick'):
    app=game.Game();errors=[];app.report_callback_exception=lambda *e:errors.append(e)
    def shot(name):
        app.update();ImageGrab.grab(window=app.winfo_id()).save(out/('guard-art-'+name+'.png'))
    try:
        s=app.state_data=core.fresh('rei');s['world']['time_mode']='paused';arrive(s,'site_01');app.play_screen();app.update()
        campaign_ui.open_in_person(app);shot('roster')
        # Every generated image must render as a PhotoImage, including custom archetypes.
        for ident in art.IDS:assert app.portrait('guard_art_'+ident,(140,230)).width()>0
        guards.begin(s,scope='art-test');combat_ui.open_combat(app);shot('combat')
        app.geometry('1000x800');app.update();shot('combat-compact')
        view=app.combat_view
        assert view.opponent_portrait.width()>0
        assert view.execute_button.winfo_viewable()
        assert view.execute_button.winfo_rooty()+view.execute_button.winfo_height()<=app.winfo_rooty()+app.winfo_height()
        combat.concede(s);combat.close(s);view.place_forget()
        name=next(iter(guards.npc_rows(s)))
        campaign_dialogue.epilogue(s,[campaign_dialogue.beat('Who is on duty?',name,'This post is guarded. Speak to the desk for authorised access.')])
        campaign_dialogue.show(app);shot('hangout')
        assert name in app.hangout_view.canvas.portrait_items
        campaign_dialogue.next_line(s);campaign_dialogue.restore(app.hangout_view)
        investigate(s);clear(s,guards.BLACKSTONE,'rei:blackstone')
        campaign_dialogue.begin(s,'rei_story.confront');campaign_dialogue.show(app);shot('richter-dialogue')
        while s.get('campaign_dialogue'):campaign_dialogue.next_line(s)
        campaign_dialogue.restore(app.hangout_view);combat_ui.open_combat(app);shot('richter-combat')
        assert not errors,errors
        print('Guard portraits rendered in roster, combat, compact controls and existing hangout; enhanced Richter rendered in dialogue and combat.')
    finally:app.sounds.close();app.destroy()
