"""Verify authored scenes use the existing hangout canvas and real portrait assets."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from unittest.mock import patch
from PIL import ImageGrab, Image
import game,game_core as core,grove,campaign_dialogue as dialogue,combat,artwork
import charles_quest,rei_story,organisation_guards as guards
from test_major_campaigns import arrive,clear,investigate
from flashback_helpers import finish_scene,finish_memories

out=core.ROOT/'tests/screenshots';out.mkdir(exist_ok=True)
with patch.object(game.Game,'check'),patch.object(game.Game,'begin_incoming'),patch.object(game.Game,'persist'),patch.object(grove.GrovePump,'tick'),patch.object(dialogue,'generate_action_narration',return_value='Rei records the fragment, leaving the gaps in the evidence visible.'):
    app=game.Game();errors=[];app.report_callback_exception=lambda *e:errors.append(e)
    def shot(name):
        app.update();ImageGrab.grab(window=app.winfo_id()).save(out/('script-'+name+'.png'))
    try:
        s=app.state_data=core.fresh('garrett');s['world']['time_mode']='paused'
        __import__('flashback_helpers').finish_memories(s)
        s['charles_quest']=dict(charles_quest.read(s),step=9)
        finish_memories(s)
        clear(s,('glasshouse_lab',),'charles:search');s['world']['minute']=20*60
        for who,a in s['world']['cast'].items():
            if who not in ('garrett','charles') and a['location']=='glasshouse_lab':a['location']='square'
        app.play_screen();app.update();view=app.hangout_view
        dialogue.begin(s,'charles_quest.security_action');dialogue.show(app);app.update()
        assert app.hangout_view is view and view.winfo_viewable()
        reader=view.prose_reader
        assert reader.winfo_viewable() and reader.text.cget('state')=='disabled'
        assert 'Charles' in str(s['campaign_dialogue']['beats'])
        assert not combat.active(s);shot('charles-confrontation')
        dialogue.next_line(s);dialogue.show(app);app.geometry('1000x800');shot('charles-compact')
        finish_scene(s)
        assert combat.active(s)['opponent']=='charles'
        dialogue.restore(view);combat.concede(s);combat.close(s)
        s=app.state_data=core.fresh('rei');s['world']['time_mode']='paused';investigate(s)
        clear(s,guards.BLACKSTONE,'rei:blackstone')
        dialogue.begin(s,'rei_story.confront');dialogue.show(app);shot('richter')
        assert 'Joseph' in str(s['campaign_dialogue']['beats'])
        finish_scene(s)
        combat.finish(s,'Victory — test');combat.close(s);dialogue.activate_epilogue(s);dialogue.show(app);shot('apology')
        finish_scene(s)
        dialogue.restore(view)
        for venue in guards.PROPERTIES:
            path=core.ROOT/'assets/ui/locations'/f'{venue}.png'
            assert Image.open(path).size==(1536,1024)
            assert artwork.scene_art(venue)=='locations/'+venue
        arrive(s,'crew_lot_docks');app.show_in_person();shot('property-background')
        s=app.state_data=core.fresh('rei');s['world']['time_mode']='paused'
        __import__('flashback_helpers').finish_memories(s)
        arrive(s,'rei_home');dialogue.begin(s,'rei_story.advance',(0,))
        s['campaign_dialogue']['cursor']=len(s['campaign_dialogue']['beats'])-1
        dialogue.show(app);reader.describe()
        import time
        deadline=time.monotonic()+3
        while not s['campaign_dialogue']['beats'][-1].get('gm_narration') and time.monotonic()<deadline:
            app.update();time.sleep(.02)
        assert reader.text.get('1.0','end').startswith('Rei records the fragment')
        assert rei_story.data(s)['stage']==0
        shot('action-narrator')
        assert not errors,errors
        print('Existing hangout canvas: novel reader, Charles/Garrett dialogue, compact layout, Richter confrontation/apology, combat gating, optional narration and four property backgrounds passed.')
    finally:app.sounds.close();app.destroy()
