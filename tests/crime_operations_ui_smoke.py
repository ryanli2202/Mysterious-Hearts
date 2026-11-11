"""Real embedded interior/clearance/activity screens; no AI or story-save writes."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from unittest.mock import patch
from PIL import ImageGrab
import game, game_core as core, grove, town, crime_sites, crime_operations as ops
from artwork import scene_art
from careers_ui_smoke import audit

with patch.object(game.Game,'check',lambda self:None), patch.object(game.Game,'persist',lambda self:None), patch.object(grove.GrovePump,'tick',lambda self:None), patch.object(game.Game,'begin_incoming',lambda self:None):
    app=game.Game(); errors=[];app.report_callback_exception=lambda *args:errors.append(args)
    out=core.ROOT/'.test-tmp'
    try:
        app.state_data=core.fresh('rei');app.play_screen();app.phone_window('Maps');app.update()
        phone=app.phone_activity;phone.geometry('430x740')
        for key in crime_sites.SITES:
            s=app.state_data
            if s['world']['location']!=key:town.travel(s,key)
            app.render();app.hide_phone_for_location();app.update()
            app.presence_view.site_activities.act(ops.enter,key,'reception');app.update()
            window=app.presence_view.site_activities
            assert window.winfo_toplevel() is app and getattr(app,'area_view',None) is None
            assert not phone.winfo_viewable() and not phone.dialogs
            assert scene_art(s['world']['location'])=='locations/'+key+'_reception'
            audit(window)
            ImageGrab.grab(window=app.winfo_id()).save(out/f'interior-{key}.png')
            window.act(ops.enter,key,'briefing');assert 'clearance' in window.notice
            window.act(ops.begin,key,'reception');app.update();audit(window)
            if key=='site_01':
                window.viewport.yview_moveto(.38);app.update()
                ImageGrab.grab(window=app.winfo_id()).save(out/'interior-assignment.png')
            window.act(ops.resolve,0)
        app.state_data=core.fresh('ivan');s=app.state_data;town.travel(s,'site_06')
        app.render();app.update()
        app.presence_view.site_activities.act(ops.enter,'site_06','reception');app.update()
        app.presence_view.site_activities.act(ops.enter,'site_06','briefing');app.update()
        window=app.presence_view.site_activities
        window.act(ops.begin,'site_06','command');app.geometry('1100x760');app.update();audit(window)
        window.viewport.yview_moveto(.38);app.update()
        ImageGrab.grab(window=app.winfo_id()).save(out/'interior-command-compact.png')
        window.act(ops.resolve,2);assert ops.progress(s,'site_06')['pressure']==5
        location=s['world']['location']
        app.leave_main_area();app.update()
        assert app.area_view is None and s['world']['location']==location
        app.phone_window('Maps');app.update()
        assert app.phone_activity is phone and phone.winfo_viewable()
        assert not errors,errors
        print('PASS: eight illustrated reception interiors, locked briefing errors, assignments, command decisions, compact layout and dark controls.')
    finally:app.destroy()
