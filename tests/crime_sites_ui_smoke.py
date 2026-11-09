"""Real dark phone notebook, discovery, validation and map-refresh checks."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from unittest.mock import patch
from PIL import ImageGrab
import game
import game_core as core
import grove
import crime_sites as sites
import town
from careers_ui_smoke import audit


with patch.object(game.Game,'check',lambda self:None), \
     patch.object(game.Game,'persist',lambda self:None), \
     patch.object(grove.GrovePump,'tick',lambda self:None), \
     patch.object(game.Game,'begin_incoming',lambda self:None):
    app=game.Game(); errors=[]
    app.report_callback_exception=lambda *args:errors.append(args)
    output=core.ROOT/'.test-tmp'; output.mkdir(exist_ok=True)
    try:
        app.state_data=core.fresh('rei'); app.play_screen(); app.phone_window('Maps'); app.update()
        phone=app.phone_activity; view=phone.map_view
        view.select('site_07',center=True); app.update()
        assert 'Unlabelled' in view.place_title.cget('text')
        view.drive();app.update()
        assert app.state_data['world']['location']=='site_07'
        app.hide_phone_for_location();app.update()
        window=app.presence_view.site_activities
        assert window is not None and getattr(app,'area_view',None) is None
        window.act(sites.inspect,'site_07');app.update()
        assert sites.known_name(app.state_data,'site_07')
        assert not sites.affiliation_known(app.state_data,'site_07')
        audit(window)
        ImageGrab.grab(window=app.winfo_id()).save(output/'city-sites-normal-location.png')
        town.travel(app.state_data,'site_01');app.render();app.update()
        app.presence_view.site_activities.act(sites.inspect,'site_01')
        for location,fn in [('archive',sites.research),('interpol_hq',sites.verify)]:
            town.travel(app.state_data,location);app.render();app.update()
            panel=app.presence_view.site_activities
            panel.record_key='site_01';panel.draw();panel.act(fn,'site_01');app.update()
        assert sites.affiliation_known(app.state_data,'site_01')
        town.travel(app.state_data,'square');app.render();app.update()
        assert app.presence_view.site_activities is None
        app.phone_window('Maps');app.update()
        view=app.phone_activity.map_view;view.select('site_07');app.update()
        assert view.place_title.cget('text')=='Oculus Winterfield Campus'
        assert not errors,errors
        print('PASS: normal map travel, local scene controls, Oculus privacy, archive research, Interpol verification, map label refresh and no controls at unrelated locations.')
    finally: app.destroy()
