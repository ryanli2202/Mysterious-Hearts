import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from unittest.mock import patch
from PIL import ImageGrab
import game,game_core as core,grove,town,charles_quest as quest
from test_charles_quest import arrive
from careers_ui_smoke import audit

with patch.object(game.Game,'check',lambda self:None),patch.object(game.Game,'persist',lambda self:None),patch.object(game.Game,'begin_incoming',lambda self:None),patch.object(grove.GrovePump,'tick',lambda self:None):
    app=game.Game();errors=[];app.report_callback_exception=lambda *a:errors.append(a)
    try:
        s=app.state_data=core.fresh('garrett');app.play_screen();app.phone_window('Winterfield');app.update()
        app.charles_search();app.geometry('1100x820');app.update()
        panel=app.area_view;assert panel.winfo_toplevel() is app
        assert not app.phone_activity.winfo_viewable()
        out=core.ROOT/'.test-tmp'
        for i in range(len(quest.STEPS)):
            arrive(s,i);panel.draw();app.update();audit(panel)
            if i in (0,8,9):ImageGrab.grab(window=app.winfo_id()).save(out/f'charles-quest-stage-{i}.png')
            panel.act(quest.advance,0);app.update()
        panel.canvas.yview_moveto(0);app.update()
        ImageGrab.grab(window=app.winfo_id()).save(out/'charles-quest-complete.png')
        app.phone_window('Contacts');app.phone_activity.contact_detail('charles');app.update();audit(app.phone_activity)
        ImageGrab.grab(window=app.phone_activity.winfo_id()).save(out/'charles-private-number.png')
        assert not errors,errors
        print('PASS: phone-to-main-window quest, eleven chapters, evidence scroll, completion and private-number profile.')
    finally:app.sounds.close();app.destroy()
