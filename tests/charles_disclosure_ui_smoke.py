import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from unittest.mock import patch
from PIL import ImageGrab
import game, game_core as core, grove, hidden_cast
import charles_disclosure as report
from test_charles_disclosure import meet
from careers_ui_smoke import audit
with patch.object(game.Game,'check',lambda self:None),patch.object(game.Game,'persist',lambda self:None),patch.object(game.Game,'begin_incoming',lambda self:None),patch.object(grove.GrovePump,'tick',lambda self:None):
    app=game.Game();errors=[];app.report_callback_exception=lambda *a:errors.append(a)
    try:
        s=app.state_data=core.fresh('ivan');meet(s,'charles',report.LAB);hidden_cast.mark_met(s,'charles')
        app.play_screen();app.update();app.charles_search();app.geometry('1100x820');app.update()
        panel=app.area_view;assert panel.winfo_toplevel() is app
        meet(s,'garrett','park');panel.act(report.act);app.update();audit(panel)
        ImageGrab.grab(window=app.winfo_id()).save(core.ROOT/'.test-tmp/charles-eyewitness.png')
        meet(s,'charles',report.LAB);panel.act(report.act)
        meet(s,'garrett','park');panel.act(report.act);app.update();audit(panel)
        ImageGrab.grab(window=app.winfo_id()).save(core.ROOT/'.test-tmp/charles-pending-reunion.png')
        assert not errors,errors
        print('PASS: eyewitness report, sealed reply and pending private reunion in main window.')
    finally:app.sounds.close();app.destroy()
