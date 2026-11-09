"""Exercise native Weather and world screens using a disposable story, no AI or save writes."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from unittest.mock import patch
from PIL import ImageGrab
import game
import game_core as core
import grove
import town

out=core.ROOT/'tests'/'screenshots'; out.mkdir(exist_ok=True)
with patch.object(game.Game,'check',lambda self:None), patch.object(game.Game,'persist',lambda self:None), patch.object(grove.GrovePump,'tick',lambda self:None), patch.object(game.Game,'begin_incoming',lambda self:None):
    app=game.Game(); errors=[]
    app.report_callback_exception=lambda *error:errors.append(error)
    app.state_data=core.fresh('garrett'); app.play_screen(); app.update()
    app.phone_window('Weather'); phone=app.phone_activity; app.update()
    for size in ('660x850','560x680'):
        phone.geometry(size); app.update()
        view=phone.screen.winfo_children()[0].winfo_children()[0]
        assert view.temperature.winfo_ismapped()
        assert view.winfo_width()>400
        ImageGrab.grab(window=phone.winfo_id()).save(out/('weather-'+size+'.png'))
        canvas=next(child for child in view.winfo_children() if child.winfo_class()=='Canvas')
        canvas.yview_moveto(1); app.update()
        ImageGrab.grab(window=phone.winfo_id()).save(out/('weather-details-'+size+'.png'))
        canvas.yview_moveto(0)
    app.state_data['world']['minute']=22*60
    phone.refresh(); app.update()
    ImageGrab.grab(window=phone.winfo_id()).save(out/'weather-night.png')
    phone.open_app('Winterfield'); app.update()
    ImageGrab.grab(window=phone.winfo_id()).save(out/'winterfield-stories.png')
    phone.open_app('Maps'); app.update()
    phone.open_app('Home'); app.update()
    ImageGrab.grab(window=phone.winfo_id()).save(out/'phone-world-apps.png')
    assert not errors, errors
    phone.destroy(); app.destroy()
print('Weather day/night, both phone sizes, Winterfield, Maps and Home passed.')
