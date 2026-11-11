"""Preview staged MH-013 masters through real loaders; never install or save.

Image.open is redirected only for the frozen roster's exact runtime paths.
No wardrobe, historical, custom or combat-variant paths are redirected.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import json
import time
import tkinter as tk
from unittest.mock import patch
from PIL import Image, ImageGrab
import game
import game_core as core
import grove
import groups
import combat
import combat_ui
import organisation_guards as guards
import lifestyle_ui
import portrait_framing
from test_major_campaigns import arrive

BASE = core.ROOT / 'roadmap/artwork-stage-02'
OUT = BASE / ('height-review/installed' if '--live' in sys.argv else 'height-review/staged')
if '--variation' in sys.argv:
    OUT = BASE/'height-variation/presentation'
SHOTS = OUT / 'screenshots'
SHOTS.mkdir(parents=True, exist_ok=True)
(OUT/'checks').mkdir(exist_ok=True)
ROSTER = json.loads((BASE/'roster.json').read_text(encoding='utf-8'))['assets']
PATHS = {(core.ROOT/r['path']).resolve(): BASE/'candidates'/(r['id']+'.png') for r in ROSTER}
opened = set()
real_open = Image.open
portrait_framing._load.cache_clear()

def staged_open(fp, *args, **kwargs):
    if isinstance(fp, (str, Path)):
        source = Path(fp).resolve()
        if source in PATHS:
            opened.add(source)
            if '--live' not in sys.argv:
                fp = PATHS[source]
    return real_open(fp, *args, **kwargs)

with patch.object(Image, 'open', staged_open), \
     patch.object(game.Game, 'check'), patch.object(game.Game, 'begin_incoming'), \
     patch.object(game.Game, 'persist'), patch.object(core, 'save'), \
     patch.object(core, 'request', side_effect=AssertionError('Unexpected AI request')), \
     patch.object(grove.GrovePump, 'tick'):
    app = game.Game()
    errors, screenshots = [], []
    app.report_callback_exception = lambda *e: errors.append(str(e))
    def shot(name, widget=None):
        app.update()
        time.sleep(.12)
        target = widget or app
        ImageGrab.grab(window=target.winfo_id()).save(SHOTS/(name+'.png'))
        screenshots.append(name+'.png')
    def wardrobe_shots():
        app.phone_window(); phone=app.phone_activity
        phone.open_app('Wardrobe'); app.update()
        view=phone.lifestyle_view
        view.preview('assets/portraits/ivan-selection.png')
        app.update(); view.body.master.yview_moveto(1)
        shot('wardrobe-preview',phone)
        phone.withdraw()
    try:
        if '--wardrobe-only' in sys.argv:
            app.state_data=core.fresh('ivan')
            app.state_data['world']['time_mode']='paused'
            app.play_screen(); wardrobe_shots()
            assert not errors,errors
            print('Runtime wardrobe RGBA preview captured on dark phone surface.')
            raise SystemExit(0)
        for size in ('1280x900', '1000x800'):
            app.geometry(size)
            selection_roster = ('garrett', 'rei', 'emily', 'sophie', 'neo')
            if '--variation' in sys.argv:
                selection_roster += ('gordon','fox')
            for who in selection_roster:
                app.start_screen.select(who)
                app.start_screen.show_dossier('Details')
                app.update()
                app.start_screen.preview.render()
                shot(f'selection-{who}-{size}')
        s = app.state_data = core.fresh('ivan')
        s['world']['time_mode'] = 'paused'
        s['world']['location'] = 'cafe'
        # Every staged asset must decode through the actual Game.portrait loader
        # at both game-sized and compact thumbnail dimensions.
        gallery = tk.Toplevel(app)
        gallery.title('MH-013 Stage 2 staged loader review')
        gallery.configure(bg='#18232b')
        gallery.geometry('1220x800+0+0')
        for start in range(0, len(ROSTER), 12):
            for child in gallery.winfo_children(): child.destroy()
            for i, row in enumerate(ROSTER[start:start+12]):
                card = tk.Frame(gallery, bg='#273744', width=300, height=260)
                card.grid(row=i//4, column=i%4, padx=2, pady=2)
                card.grid_propagate(False)
                tk.Label(card, text=row['id'], bg='#273744', fg='#e9e4dc').grid(row=0,column=0,columnspan=2)
                key = 'guard_art_'+row['character'] if row['role'] else row['character']
                for column, size in enumerate(((150,225),(86,129))):
                    photo = app.portrait(key, size)
                    assert photo and photo.width()>0, row['id']
                    tk.Label(card, image=photo, bg='#273744').grid(row=1,column=column,sticky='s')
            shot(f'loader-roster-{start//12+1:02d}', gallery)
        gallery.destroy()
        assert set(PATHS) <= opened, [str(p) for p in set(PATHS)-opened]
        # Contemporary scene contexts only; variants have separate future stages.
        for who in ('ivan','rei','garrett','emily'):
            s['world']['cast'][who].update(location='cafe', journey=None)
        gid=groups.open_solo(s,'rei')
        s['groups'][gid]['history'].append(dict(speaker=core.PLAYERS['rei'],text='A quiet moment at the cafe.'))
        app.play_screen()
        for size in ('1280x900','1000x800'):
            app.geometry(size); app.show_in_person(); app.update()
            assert set(app.hangout_view.canvas.portrait_items)=={'ivan','rei'}
            shot('solo-'+size)
        groups.close_active(s,'Fixture complete')
        for who in ('ivan','rei','garrett','emily'):
            s['world']['cast'][who].update(location='cafe', journey=None)
        gid=groups.open_group(s,['garrett','rei','emily'])
        for size in ('1280x900','1000x800'):
            app.geometry(size); app.show_in_person(); app.update()
            assert set(app.hangout_view.canvas.portrait_items)=={'ivan','garrett','rei','emily'}
            shot('group-'+size)
        groups.close_active(s,'Fixture complete')
        s['world']['party']=[]
        for who in ('Arthur Finch','Keiko Tan','Jonah Price'):
            arrive(s,core.town.town_residents.routine(who,s['world']['minute']))
            s['world']['npcs']=[who]
            groups.open_local(s,who)
            app.show_in_person(); app.update()
            assert who in app.hangout_view.canvas.portrait_items
            shot('resident-'+who.lower().replace(' ','-'))
            groups.close_active(s,'Fixture complete')
        # Existing dark wardrobe preview, using a contemporary staged master.
        wardrobe_shots()
        guard_ids = ('spades','team9','yokai')
        if '--variation' in sys.argv:
            guard_ids += ('oni','custom_robotic')
        for ident in guard_ids:
            s=app.state_data=core.fresh('ivan'); s['world']['time_mode']='paused'
            arrive(s,'market'); app.play_screen(); app.update()
            kind = ident
            if ident == 'custom_robotic':
                # Custom guards resolve via their saved type, not a built-in ID.
                kind = 'height_fixture_robotic'
                guards.data(s)['types'][kind] = ['Custom robotic guard','robotic','MMA','weapon systems',40,52]
            guards.start(s,'stage2:'+ident,guards.profile(s,kind),'stage2-art')
            for size in ('1280x900','1000x800'):
                app.geometry(size); combat_ui.open_combat(app); app.update()
                assert app.combat_view.execute_button.winfo_viewable()
                assert app.combat_view.master is app.presence_view.master
                shot('combat-'+ident+'-'+size)
        assert not errors, errors
        (OUT/'checks/presentation-render.json').write_text(json.dumps(dict(
            scope=('Current installed assets' if '--live' in sys.argv else 'Staged path substitution') + '; actual shared stature renderer and wardrobe alpha; harness writes no assets or saves',
            rendered_assets=len(opened), screenshots=screenshots, callback_errors=errors,
            visual_review='pending', integration='Stage 2 height follow-up; later wardrobe/context stages pending'),indent=2)+'\n',encoding='utf-8')
        print(f'{len(opened)} '+('installed' if '--live' in sys.argv else 'staged')+f' paths rendered; {len(screenshots)} screenshots; no callback errors.')
    finally:
        app.sounds.close(); app.destroy()
