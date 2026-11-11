"""Exercise real campaign buttons, historical portraits, resizing and restoration."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from unittest.mock import patch
from tkinter import ttk
from PIL import ImageGrab
import game,game_core as core,grove,campaign_dialogue as dialogue,campaign_flashbacks as memories
import campaign_ui,charles_quest_ui,rei_story
from test_major_campaigns import arrive
from campaign_ui_helpers import finish_script

out=core.ROOT/'tests/screenshots';out.mkdir(exist_ok=True)
with patch.object(game.Game,'check'),patch.object(game.Game,'begin_incoming'),patch.object(game.Game,'persist'),patch.object(grove.GrovePump,'tick'):
    app=game.Game();errors=[];app.report_callback_exception=lambda *e:errors.append(e)
    try:
        for player,venue in (('rei','rei_home'),('garrett','noodle_shop'),('garrett','glasshouse_lab')):
            s=app.state_data=core.fresh(player);s['world']['time_mode']='paused'
            arrive(s,venue)
            if player=='rei':rei_story.data(s)['stage']=2
            elif venue=='glasshouse_lab':s['charles_quest']=dict(__import__('charles_quest').read(s),step=9)
            app.play_screen();app.update();view=app.hangout_view
            while memories.pending(s):
                key=memories.pending(s)
                if player=='rei':
                    campaign_ui.open_in_person(app,'Rei’s story');panel=app.campaign_view
                else:
                    panel=charles_quest_ui.QuestPanel(app.presence_view.master,app,lambda:None)
                    panel.pack(fill='both',expand=True)
                buttons=[w for w in panel.body.winfo_children() if isinstance(w,ttk.Button) and str(w.cget('text')).startswith('Begin flashback')]
                assert len(buttons)==1
                buttons[0].invoke()
                if player=='garrett':panel.destroy()
                app.update()
                assert app.hangout_view is view and view.winfo_viewable()
                reader=view.prose_reader
                s['campaign_dialogue']['cursor']=next(i for i,b in enumerate(s['campaign_dialogue']['beats']) if b.get('mode')=='memory')
                reader.display();app.update()
                assert set(reader.portraits)==set(memories.SCENES[key]['portraits'])
                assert reader.current()['background']==memories.SCENES[key]['background']
                for who,stem in memories.SCENES[key]['portraits'].items():
                    assert any(str(cache[2]).endswith(stem+'.png') for cache in app.photos),who
                # Inspect both speaking and narration-only states, with compact resizing.
                for index,size in ((0,'1280x820+0+0'),(min(4,len(s['campaign_dialogue']['beats'])-1),'1000x800+0+0')):
                    s['campaign_dialogue']['cursor']=index
                    app.geometry(size);dialogue.show(app);app.update()
                    button=reader.next
                    assert button.winfo_viewable()
                    assert button.winfo_rooty()+button.winfo_height()<=app.winfo_rooty()+app.winfo_height()
                    ImageGrab.grab(window=app.winfo_id()).save(out/f'flashback-{key}-{index}.png')
                finish_script(app)
                assert not getattr(view,'script_mode',False)
                assert s['world']['location']==venue
            app.show_in_person();app.update()
            assert memories.portrait_path(s,player) is None
        assert not errors,errors
        print('Five flashbacks: campaign launch buttons, historical portraits/backgrounds, compact layouts, Continue, completion and restoration passed.')
    finally:app.sounds.close();app.destroy()
