"""Real embedded interior/clearance/activity screens; no AI or story-save writes."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from unittest.mock import patch
from PIL import ImageGrab
import game, game_core as core, grove, town, crime_sites, crime_operations as ops
from artwork import scene_art
from careers_ui_smoke import audit

import criminal_dynamics as dynamics
with patch.object(game.Game,'check',lambda self:None), patch.object(game.Game,'persist',lambda self:None), patch.object(grove.GrovePump,'tick',lambda self:None), patch.object(game.Game,'begin_incoming',lambda self:None):
    app=game.Game(); errors=[]; app.report_callback_exception=lambda *args:errors.append(args)
    out=core.ROOT/'.test-tmp'; out.mkdir(exist_ok=True)
    try:
        app.state_data=core.fresh('ivan'); app.play_screen(); app.phone_window('Maps'); app.update()
        phone=app.phone_activity; phone.map_view.select(dynamics.LAB,center=True); app.update()
        audit(phone)
        ImageGrab.grab(window=phone.winfo_id()).save(out/'glasshouse-map.png')
        phone.map_view.drive(); app.update(); app.hide_phone_for_location(); app.update()
        panel=app.presence_view.site_activities
        assert panel.winfo_toplevel() is app
        assert not phone.winfo_viewable()
        panel.act(dynamics.laboratory_briefing); app.update(); audit(panel)
        assert 'betray' in panel.notice
        app.geometry('1100x800'); app.update()
        ImageGrab.grab(window=app.winfo_id()).save(out/'glasshouse-briefing.png')
        panel.viewport.yview_moveto(1); app.update()
        ImageGrab.grab(window=app.winfo_id()).save(out/'glasshouse-briefing-scrolled.png')
        app.phone_window('Maps'); app.update(); audit(phone)
        app.state_data=core.fresh('rei')
        __import__('job_apps').ensure(app.state_data)['membership']=dict(faction='Syndicate',branch='Spades',rank=6,strikes=0)
        town.travel(app.state_data,dynamics.LAB); app.render(); app.hide_phone_for_location(); app.update()
        panel=app.presence_view.site_activities; panel.act(dynamics.laboratory_briefing); app.update(); audit(panel)
        assert 'Blue Magic' in panel.notice and 'betray' not in panel.notice
        ImageGrab.grab(window=app.winfo_id()).save(out/'glasshouse-jack-briefing.png')
        assert not errors,errors
        print('PASS: dark lab map, in-person private briefing, scrolling, compact layout and phone return.')
    finally: app.destroy()
