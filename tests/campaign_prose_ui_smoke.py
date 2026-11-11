"""Render the MH-005 reader, its controls, transitions and optional-visit board."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from unittest.mock import patch
from PIL import ImageGrab
import game,game_core as core,grove
import campaign_dialogue as dialogue,campaign_prose as prose,campaign_prose_ui as reader_ui
import campaign_ui,combat
from test_major_campaigns import arrive
from test_campaign_prose import place_friend
from flashback_helpers import finish_memories,finish_scene
from careers_ui_smoke import audit

out=core.ROOT/'tests/screenshots';out.mkdir(exist_ok=True)
with patch.object(game.Game,'check'),patch.object(game.Game,'begin_incoming'),patch.object(game.Game,'persist'),patch.object(grove.GrovePump,'tick'),patch.object(dialogue,'generate_action_narration',return_value='Rei records what he can read, leaving the uncertain intervals open.'):
    app=game.Game();errors=[];app.report_callback_exception=lambda *e:errors.append(e)
    def shot(name):
        app.update();ImageGrab.grab(window=app.winfo_id()).save(out/('mh005-'+name+'.png'))
    try:
        s=app.state_data=core.fresh('garrett');s['world']['time_mode']='paused';arrive(s,'noodle_shop');place_friend(s,'april','noodle_shop')
        app.play_screen();app.geometry('1360x920');app.update()
        prose.begin_social(s,'GD01','share','help');dialogue.show(app);app.update()
        reader=app.hangout_view.prose_reader
        assert reader.winfo_viewable() and reader.text.cget('state')=='disabled'
        assert 'April moved' in reader.text.get('1.0','end');audit(reader);shot('pilot-opening')
        reader.next.invoke();app.update();cursor=s['campaign_dialogue']['cursor']
        reader.back.invoke();assert s['campaign_dialogue']['cursor']==cursor-1
        finish_scene(s);finish_memories(s)
        place_friend(s,'rei','noodle_shop');prose.begin_social(s,'GD03','share','help');dialogue.show(app)
        d=s['campaign_dialogue'];d['cursor']=next(i for i,b in enumerate(d['beats']) if b.get('mode')=='memory')
        reader.display();shot('shared-memory')
        d['cursor']=next(i for i,b in enumerate(d['beats']) if b.get('scene_id')=='GD04' and b.get('mode')=='present')
        reader.display();shot('present-return');finish_scene(s)

        s=app.state_data=core.fresh('rei');s['world']['time_mode']='paused';arrive(s,'rei_home')
        dialogue.begin(s,'rei_story.advance',(0,));dialogue.show(app);d=s['campaign_dialogue']
        d['cursor']=next(i for i,b in enumerate(d['beats']) if b.get('reflection'));reader.display()
        assert reader.next.instate(['disabled']);shot('reflection')
        reader.choose(1);assert not reader.next.instate(['disabled'])
        reader.next.invoke();app.geometry('1000x760');reader.resize(9);app.update()
        assert prose.data(s)['preferences']['size']==24
        assert reader.next.winfo_viewable();assert reader.text.winfo_height()>100
        shot('compact-large-text');audit(reader)
        reader.history();app.update();shot('history-empty');reader.return_current()
        assert s['rei_story']['stage']==0
        d['cursor']=len(d['beats'])-1;reader.display();reader.describe();app.update()
        import time
        deadline=time.monotonic()+3
        while not d['beats'][-1].get('gm_narration') and time.monotonic()<deadline:
            app.update();time.sleep(.02)
        assert d['beats'][-1].get('gm_narration');shot('optional-description')
        reader.next.invoke();app.update();assert s['rei_story']['stage']==1
        reader_ui.open_archive(app);app.update();shot('history');reader.recap();shot('recap')
        app.render();app.update();assert reader.winfo_viewable() and reader.history_mode
        assert not s.get('campaign_dialogue');reader.return_current()
        campaign_ui.open_in_person(app,'Story');app.update();audit(app.campaign_view);shot('story-visits')
        assert not errors,errors
        print('PASS: pilot, shared memory/return, reflection, instant text, previous/next, 24pt compact layout, optional generated description, history/recap and deferred/available visit controls.')
    finally:app.sounds.close();app.destroy()
