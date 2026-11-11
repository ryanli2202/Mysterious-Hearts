"""Review all staged MH-013 wardrobes through real rendering, without installation.

Only exact frozen wardrobe paths are redirected to byte-identical candidates.
Scene fixtures explicitly choose outfits through the existing resolver. Save writes
and AI calls are disabled; no runtime files or player stories are changed.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import json
import time
import tkinter as tk
from types import SimpleNamespace
from unittest.mock import patch
from PIL import Image, ImageGrab
import game
import game_core as core
import grove
import groups
import camera
import character_stature as stature
import portrait_framing as framing
from tools import artwork_stage_03 as ledger

BASE = ledger.OUT
SHOTS = BASE / 'screenshots'
SHOTS.mkdir(exist_ok=True)
ROWS = ledger.read(BASE / 'roster.json')['assets']
PATHS = {(core.ROOT/r['path']).resolve(): BASE/'candidates'/(r['id']+'.png') for r in ROWS}
opened = set()
real_open = Image.open
real_path = game.Game.portrait_path


def staged_open(fp, *args, **kwargs):
    if isinstance(fp, (str, Path)):
        source = Path(fp).resolve()
        if source in PATHS:
            opened.add(source)
            fp = PATHS[source]
    return real_open(fp, *args, **kwargs)


def span(image):
    box = framing.visible_bounds(image)
    return box[3] - box[1]


def audit():
    baseline = ledger.read(BASE/'before-state.json')
    assert all(ledger.digest(core.ROOT/p) == h for p, h in baseline.items())
    assert ledger.digest(core.ROOT/'assets/portraits/stature.json') == ledger.digest(BASE/'before-stature.json')
    reviews = ledger.read(BASE/'reviews.json')
    for row in ROWS:
        assert reviews[row['id']]['accepted_sha256'] == ledger.digest(PATHS[(core.ROOT/row['path']).resolve()])
    comparisons = []
    # Compare every variant with Ivan and with its own installed master, at
    # shared pixels/cm even when the participant slots have unequal widths.
    with patch.object(game.ImageTk, 'PhotoImage', side_effect=lambda im: im.copy()):
        app = SimpleNamespace(state_data={}, photos={})
        for row in ROWS:
            who = row['character']
            key, path = real_path(app, who, outfit=row['variant'])
            assert path.resolve() == (core.ROOT/row['path']).resolve()
            assert stature.height_cm(key, path) == row['height_cm']
            for size, reference_size in (((192,352),(368,352)), ((108,210),(176,210))):
                master = core.ROOT/row['master_path']
                ivan = core.ROOT/'assets/portraits/ivan-selection.png'
                scale = framing.shared_scale([(framing.load(path),size,row['height_cm']),
                    (framing.load(master),size,row['height_cm']),
                    (framing.load(ivan),reference_size,193)])
                image = game.Game.portrait(app,who,size,outfit=row['variant'],scale=scale)
                own = framing.fit(framing.load(master),size,row['height_cm'],scale)
                ref = framing.fit(framing.load(ivan),reference_size,193,scale)
                assert abs(span(image)-span(own)) <= 2, row['id']
                assert abs(span(image)-span(ref)*row['height_cm']/193) <= 2, row['id']
                comparisons.append(dict(id=row['id'],size=size,span=span(image),master_span=span(own),height_cm=row['height_cm']))
    saved_routes = []
    for who in ('ivan','garrett','rei','minsu'):
        state = core.fresh(who)
        for label, path in camera.outfits(state,who).items():
            if Path(path).resolve() not in PATHS:
                continue
            state['world']['player_outfit'] = label
            restored = json.loads(json.dumps(state))
            app = SimpleNamespace(state_data=restored)
            assert real_path(app,who)[1].resolve() == Path(path).resolve()
            saved_routes.append(dict(character=who,label=label,path=str(Path(path).relative_to(core.ROOT))))
    auto_routes = []
    app = SimpleNamespace(state_data=core.fresh('ivan'))
    for who in ('april','samantha'):
        for day in range(3):
            for location in ('beach','track','bar'):
                minute = day*1440+18*60
                path = real_path(app,who,location,minute)[1]
                assert path.resolve() in PATHS, (who,location,path)
                auto_routes.append(dict(character=who,location=location,minute=minute,path=path.name))
    for who in ('amy','april','emily','garrett','minsu','rei','samantha','sophie'):
        for minute in range(0,1440,30):
            if core.town.loop.appointment(who,minute)[2] == 'Sleep':
                path = real_path(app,who,core.town.HOMES[who],minute)[1]
                assert path.name == who+'-sleep.png', (who,path)
                auto_routes.append(dict(character=who,location='home asleep',minute=minute,path=path.name))
                break
    ledger.write(BASE/'checks/staged-routing-heights.json',dict(
        unchanged_live_assets=len(baseline),height_table_unchanged=True,
        accepted_hashes=len(ROWS),paired_height_checks=comparisons,
        saved_wardrobe_roundtrips=saved_routes,automatic_routes=auto_routes,
        scope='Staged Image.open substitution; existing portrait resolution and stature fitting; no installation or save writes'))


framing._load.cache_clear()
with patch.object(Image,'open',staged_open):
    audit()
    with patch.object(game.Game,'check'), patch.object(game.Game,'begin_incoming'), \
         patch.object(game.Game,'persist'), patch.object(core,'save'), \
         patch.object(core,'request',side_effect=AssertionError('Unexpected AI request')), \
         patch.object(grove.GrovePump,'tick'):
        app = game.Game()
        errors, screenshots = [], []
        app.report_callback_exception = lambda *e: errors.append(str(e))

        def shot(name, widget=None):
            app.update()
            time.sleep(.12)
            target = widget or app
            ImageGrab.grab(window=target.winfo_id()).save(SHOTS/(name+'.png'))
            screenshots.append(name+'.png')

        try:
            app.state_data = core.fresh('ivan')
            app.state_data['world']['time_mode'] = 'paused'
            gallery = tk.Toplevel(app)
            gallery.title('MH-013 Stage 3 staged wardrobe review')
            gallery.configure(bg='#18232b')
            gallery.geometry('1220x800+0+0')
            for start in range(0,len(ROWS),12):
                for child in gallery.winfo_children(): child.destroy()
                for i,row in enumerate(ROWS[start:start+12]):
                    card = tk.Frame(gallery,bg='#273744',width=300,height=260)
                    card.grid(row=i//4,column=i%4,padx=2,pady=2)
                    card.grid_propagate(False)
                    tk.Label(card,text=row['id'],bg='#273744',fg='#e9e4dc').grid(row=0,column=0,columnspan=2)
                    for column,size in enumerate(((150,225),(86,129))):
                        photo = app.portrait(row['character'],size,outfit=row['variant'])
                        assert photo and photo.width()>0,row['id']
                        tk.Label(card,image=photo,bg='#273744').grid(row=1,column=column,sticky='s')
                shot(f'loader-wardrobes-{start//12+1:02d}',gallery)
            gallery.destroy()
            assert set(PATHS) <= opened

            # Fixtures select ordinary outfits via the original explicit-outfit
            # resolver; only selection of the fixture outfit is injected.
            chosen = {'ivan':'fashion-ivory','garrett':'formal-tuxedo','rei':'tailored-waistcoat','emily':'formal-tailoring'}
            valid = {r['id'] for r in ROWS}
            assert all(w+'-'+v in valid for w,v in chosen.items())
            def scene_path(self,key,location=None,minute=None,outfit=None):
                return real_path(self,key,location,minute,outfit or chosen.get(key))
            with patch.object(game.Game,'portrait_path',scene_path):
                s=app.state_data
                s['world']['location']='cafe'
                for who in chosen: s['world']['cast'][who].update(location='cafe',journey=None)
                groups.open_solo(s,'rei')
                app.play_screen()
                for size in ('1280x900','1000x800'):
                    app.geometry(size);app.show_in_person();app.update()
                    assert set(app.hangout_view.canvas.portrait_items)=={'ivan','rei'}
                    shot('solo-'+size)
                groups.close_active(s,'Fixture complete')
                for who in chosen: s['world']['cast'][who].update(location='cafe',journey=None)
                groups.open_group(s,['garrett','rei','emily'])
                for size in ('1280x900','1000x800'):
                    app.geometry(size);app.show_in_person();app.update()
                    assert set(app.hangout_view.canvas.portrait_items)==set(chosen)
                    shot('group-'+size)
                groups.close_active(s,'Fixture complete')
            app.phone_window();phone=app.phone_activity
            phone.open_app('Wardrobe');app.update()
            for ident in ('minsu-sleep','emily-formal-tailoring','samantha-beach-black-bikini'):
                phone.lifestyle_view.preview(str(core.ROOT/'assets/portraits'/(ident+'.png')))
                app.update();phone.lifestyle_view.body.master.yview_moveto(1)
                shot('phone-'+ident,phone)
            assert not errors,errors
            ledger.write(BASE/'checks/presentation-render.json',dict(
                scope='146 staged wardrobe paths via real portrait loader; fixture outfits via original resolver; no installation/save writes',
                rendered_assets=len(opened),screenshots=screenshots,callback_errors=errors,visual_review='pending'))
            print(f'{len(opened)} staged paths; {len(screenshots)} screenshots; no callback errors.')
        finally:
            app.sounds.close();app.destroy()
