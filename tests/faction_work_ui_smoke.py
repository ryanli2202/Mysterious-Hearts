"""Joint work through normal location UI, without AI or save writes."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from unittest.mock import patch
from PIL import ImageGrab
import game, grove, crime_operations as ops
from test_faction_work import workplace
from careers_ui_smoke import audit

def labels(widget):
    result=[]
    for child in widget.winfo_children():
        try:result.append(str(child.cget('text')))
        except Exception:pass
        result.extend(labels(child))
    return result

with patch.object(game.Game,'check',lambda self:None),patch.object(game.Game,'persist',lambda self:None),patch.object(grove.GrovePump,'tick',lambda self:None),patch.object(game.Game,'begin_incoming',lambda self:None):
    app=game.Game();errors=[];app.report_callback_exception=lambda *args:errors.append(args)
    try:
        app.state_data,key=workplace();app.play_screen();app.update()
        panel=app.presence_view.site_activities
        assert any('Review request with Camila' in text for text in labels(panel))
        assert any('Discuss mandate with Camila' in text for text in labels(panel))
        assert any('Talk / hang out' in text for text in labels(app.presence_view))
        panel.act(ops.begin,key,'command','camila');app.update();audit(panel)
        panel.viewport.yview_moveto(.38);app.update()
        ImageGrab.grab(window=app.winfo_id()).save(Path('.test-tmp/faction-joint-command.png'))
        panel.act(ops.resolve,0);app.update()
        assert ops.read(app.state_data)['history']
        app.state_data,key=workplace('rei','martos',2*1440+10*60)
        app.presence_view.signature=None;app.render();app.geometry('1100x760');app.update()
        panel=app.presence_view.site_activities;audit(panel)
        assert not any('Discuss mandate' in text for text in labels(panel))
        assert not any('Ace of' in text for text in labels(app.presence_view))
        ImageGrab.grab(window=app.winfo_id()).save(Path('.test-tmp/faction-public-cover.png'))
        assert not errors,errors
        print('PASS: on-site talk, joint work, private mandates, public cover, compact layout and dark controls.')
    finally:app.destroy()
