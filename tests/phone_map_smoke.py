"""Exercise actual phone map interactions without AI or player save writes."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from unittest.mock import patch
from PIL import ImageGrab
import game
import game_core as core
import grove
import phone_map


with patch.object(game.Game, 'check', lambda self: None), \
     patch.object(game.Game, 'persist', lambda self: None), \
     patch.object(grove.GrovePump, 'tick', lambda self: None), \
     patch.object(game.Game, 'begin_incoming', lambda self: None):
    app = game.Game()
    errors = []
    app.report_callback_exception = lambda *args: errors.append(args)
    app.state_data = core.fresh('rei')
    app.play_screen()
    app.phone_window('Maps')
    phone = app.phone_activity
    app.update()
    view = phone.map_view
    import public_venues
    for venue in public_venues.VENUES:
        view.select(venue, center=True)
        app.update()
        assert view.selected == venue
        assert view.place_title.cget('text') == public_venues.VENUES[venue][0]
        assert public_venues.VENUES[venue][3] in view.place_status.cget('text')
    view.select('square', center=True)
    screenshots = Path(__file__).parent / 'screenshots'
    screenshots.mkdir(exist_ok=True)
    view.fit()
    app.update()
    for key in phone_map.places(app.state_data):
        x, y = view.xy(*phone_map.POINTS[key])
        assert 0 <= x <= view.canvas.winfo_width()
        assert 0 <= y <= view.canvas.winfo_height()
    ImageGrab.grab(window=phone.winfo_id()).save(screenshots / 'phone-map-expanded-fit.png')
    view.query.set('hillside tea')
    view.search_first()
    app.update()
    assert view.selected == 'hill_tea_room'
    ImageGrab.grab(window=phone.winfo_id()).save(screenshots / 'phone-map-outskirts-search.png')
    view.query.set('')
    view.select('square', center=True)
    import vacant_homes
    for key, residence in vacant_homes.HOMES.items():
        view.select(key, center=True)
        app.update()
        assert view.place_title.cget('text') == residence['name']
        assert view.place_status.cget('text') == vacant_homes.STATUS
        ImageGrab.grab(window=phone.winfo_id()).save(screenshots / (key + '-map.png'))
    view.select('square', center=True)
    prior_view = (view.cx, view.cy, view.zoom, view.selected, view.layer)
    view.set_layer('Map')
    view.select('downtown', center=True)
    view.cx, view.cy, view.zoom = 700, 500, .25
    view.draw()
    app.update()
    ImageGrab.grab(window=phone.winfo_id()).save(screenshots / 'phone-map-metropolitan.png')
    view.set_layer('Satellite')
    app.update()
    ImageGrab.grab(window=phone.winfo_id()).save(screenshots / 'phone-map-metropolitan-satellite.png')
    view.cx, view.cy, view.zoom, view.selected, prior_layer = prior_view
    view.set_layer(prior_layer)
    view.draw()

    ImageGrab.grab(window=phone.winfo_id()).save(screenshots / 'phone-map-overview.png')
    camera = (view.cx, view.cy, view.zoom, view.selected)
    view.layer_buttons['Satellite'].invoke()
    app.update()
    assert view.layer == 'Satellite'
    assert view.canvas.find_withtag('satellite-terrain')
    assert (view.cx, view.cy, view.zoom, view.selected) == camera
    ImageGrab.grab(window=phone.winfo_id()).save(screenshots / 'phone-map-satellite.png')
    view.layer_buttons['Map'].invoke()
    assert not view.canvas.find_withtag('satellite-terrain')
    assert (view.cx, view.cy, view.zoom, view.selected) == camera
    view.layer_buttons['Satellite'].invoke()
    view.query.set('petal')
    view.search_first()
    app.update()
    assert view.selected == 'flowers'
    assert view.result_keys == ['flowers']
    view.set_layer('Map')
    assert view.query.get() == 'petal' and view.selected == 'flowers'
    view.set_layer('Satellite')
    view.query.set('')
    app.update()
    # Zoom preserves the world coordinate beneath the cursor.
    before = view.world_xy(120, 90)
    view.change_zoom(1.25, 120, 90)
    after = view.world_xy(120, 90)
    assert all(abs(a-b) < .0001 for a, b in zip(before, after))
    view.select('square', center=True)
    app.update()
    x, y = map(round, view.xy(*phone_map.POINTS['flowers']))
    view.canvas.event_generate('<ButtonPress-1>', x=x, y=y)
    view.canvas.event_generate('<ButtonRelease-1>', x=x, y=y)
    assert view.selected == 'flowers'
    camera = (view.cx, view.cy)
    view.canvas.event_generate('<ButtonPress-1>', x=100, y=100)
    view.canvas.event_generate('<B1-Motion>', x=160, y=140)
    view.canvas.event_generate('<ButtonRelease-1>', x=160, y=140)
    assert (view.cx, view.cy) != camera
    assert view.selected == 'flowers'  # A drag does not select a different pin.
    key, box = next((key, box) for key, box in view.label_boxes if key != 'flowers')
    x, y = (box[0] + box[2]) // 2, (box[1] + box[3]) // 2
    view.canvas.event_generate('<ButtonPress-1>', x=x, y=y)
    view.canvas.event_generate('<ButtonRelease-1>', x=x, y=y)
    assert view.selected == key
    view.select('flowers')
    world = app.state_data['world']
    world['cast']['emily'].update(location='flowers', journey=None)
    world['cast']['garrett'].update(location='car:garrett', journey={
        'destination': 'flowers', 'arrives': world['minute'] + 12})
    view.sync()
    details = view.people_text.get('1.0', 'end')
    assert 'Here now: Emily Fields' in details
    assert 'Arriving: Garrett Han' in details
    view.query.set('lena')
    assert 'lena_home' not in view.result_keys
    view.query.set('xyz-no-place')
    assert not view.result_keys
    view.query.set('')
    view.select('flowers', center=True)
    import public_venues
    for venue in public_venues.VENUES:
        view.select(venue, center=True)
        app.update()
        assert view.selected == venue
        assert view.place_title.cget('text') == public_venues.VENUES[venue][0]
        assert public_venues.VENUES[venue][3] in view.place_status.cget('text')
    view.select('square', center=True)
    screenshots = Path(__file__).parent / 'screenshots'
    screenshots.mkdir(exist_ok=True)
    prior_view = (view.cx, view.cy, view.zoom, view.selected, view.layer)
    view.set_layer('Map')
    view.select('downtown', center=True)
    view.cx, view.cy, view.zoom = 700, 500, .25
    view.draw()
    app.update()
    ImageGrab.grab(window=phone.winfo_id()).save(screenshots / 'phone-map-metropolitan.png')
    view.set_layer('Satellite')
    app.update()
    ImageGrab.grab(window=phone.winfo_id()).save(screenshots / 'phone-map-metropolitan-satellite.png')
    view.cx, view.cy, view.zoom, view.selected, prior_layer = prior_view
    view.set_layer(prior_layer)
    view.draw()

    app.update()
    ImageGrab.grab(window=phone.winfo_id()).save(screenshots / 'phone-map-interactive.png')
    phone.geometry('560x680')
    app.update()
    assert view.canvas.winfo_height() >= 180
    assert view.card.winfo_y() + view.card.winfo_height() <= view.winfo_height()
    ImageGrab.grab(window=phone.winfo_id()).save(screenshots / 'phone-map-compact.png')
    view.query.set('cafe')
    app.update()
    assert view.canvas.winfo_height() >= 130
    view.query.set('')
    saved = dict(phone.map_memory)
    phone.open_app('Home')
    phone.open_app('Maps')
    app.update()
    view = phone.map_view
    assert (view.cx, view.cy, view.zoom) == saved['camera']
    assert view.selected == saved['selected']
    assert view.layer == saved['layer'] == 'Satellite'
    # Exercise travel through the real phone action, including rebuilding the map.
    world['cast']['garrett'].update(location='noodle_shop', journey=None)
    view.select('flowers')
    view.drive()
    app.update()
    view = phone.map_view
    assert world['cast']['rei']['journey'] is None
    assert view.drive_button.cget('text') == 'You are here'
    assert world['location'] == 'flowers'
    assert not world['cast']['rei']['journey']
    assert str(phone.map_view.drive_button.cget('state')) == 'disabled'
    world['minute'] = 2*1440+9*60
    view.select('hill_tea_room', center=True)
    view.drive()
    app.update()
    assert world['location'] == 'hill_tea_room'
    assert 'Euan Marsh' in world['npcs']
    view = phone.map_view
    view.locate()
    app.update()
    assert (view.cx, view.cy) == phone_map.POINTS['hill_tea_room']
    ImageGrab.grab(window=phone.winfo_id()).save(screenshots / 'phone-map-outskirts-arrival.png')
    view.pan(-100000, -100000)
    left, top, right, bottom = phone_map.map_bounds(app.state_data)
    assert (view.cx, view.cy) == (left, top)
    view.pan(100000, 100000)
    assert (view.cx, view.cy) == (right, bottom)
    phone.open_app('Home')
    app.update()
    app.destroy()
    assert not errors, errors
print('Map search, click, pan, zoom, live presence, compact layout, memory, and travel passed.')
