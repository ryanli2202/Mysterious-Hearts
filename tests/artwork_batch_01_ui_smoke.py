"""Render the MH-013 pilot in actual selection, solo/group and combat consumers."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import copy
import json
from unittest.mock import patch
from PIL import ImageGrab
import game
import game_core as core
import grove
import groups
import combat
import combat_ui
import organisation_guards as guards
from test_major_campaigns import arrive

out = core.ROOT/'roadmap/artwork-batch-01/screenshots'
out.mkdir(exist_ok=True)
with patch.object(game.Game,'check'), patch.object(game.Game,'begin_incoming'), \
     patch.object(game.Game,'persist'), patch.object(core,'save'), \
     patch.object(core,'request',side_effect=AssertionError('Unexpected AI request')), \
     patch.object(grove.GrovePump,'tick'):
    app=game.Game(); errors=[]
    app.report_callback_exception=lambda *e:errors.append(e)
    def shot(name):
        app.update()
        ImageGrab.grab(window=app.winfo_id()).save(out/(name+'.png'))
    try:
        for size in ('1280x900','1000x800'):
            app.geometry(size)
            for who in ('ivan','minsu','emily'):
                app.start_screen.select(who);app.update()
                app.start_screen.preview.render()
                shot(f'selection-{who}-{size}')
        s=app.state_data=core.fresh('ivan')
        s['world']['time_mode']='paused';s['world']['location']='cafe'
        for who in ('ivan','emily','minsu'):
            s['world']['cast'][who].update(location='cafe',journey=None)
        gid=groups.open_solo(s,'emily')
        s['groups'][gid]['history'].append(dict(speaker='Emily Fields',text='It is a lovely afternoon.'))
        app.play_screen();app.update()
        for size in ('1280x900','1000x800'):
            app.geometry(size);app.show_in_person();app.update()
            canvas=app.hangout_view.canvas
            assert set(canvas.portrait_items)=={'ivan','emily'}
            shot('solo-'+size)
        groups.close_active(s,'Fixture complete')
        for who in ('ivan','emily','minsu'):
            s['world']['cast'][who].update(location='cafe',journey=None)
        gid=groups.open_group(s,['emily','minsu'])
        s['groups'][gid]['history'].append(dict(speaker='Minsu Park',text='We found a table for everyone.'))
        for size in ('1280x900','1000x800'):
            app.geometry(size);app.show_in_person();app.update()
            assert set(canvas.portrait_items)=={'ivan','emily','minsu'}
            shot('group-'+size)
        groups.close_active(s,'Fixture complete')
        s['world']['party']=[]
        # Charles remains laboratory-bound; review him in his actual venue.
        arrive(s,'glasshouse_lab')
        groups.open_solo(s,'charles')
        app.show_in_person();app.update()
        assert 'charles' in canvas.portrait_items
        shot('charles-laboratory')
        groups.close_active(s,'Fixture complete')
        # The same in-person scene renderer must resolve direct town names.
        for who in ('Priya Shah','Otis Bell'):
            arrive(s,core.town.town_residents.routine(who,s['world']['minute']))
            s['world']['npcs']=[who]
            gid=groups.open_local(s,who)
            s['groups'][gid]['history'].append(dict(speaker=who,text='Good to see you.'))
            app.show_in_person();app.update()
            assert who in canvas.portrait_items
            shot('resident-'+who.lower().replace(' ','-'))
            groups.close_active(s,'Fixture complete')
        # Current and restored saved guard encounters route to the existing role ID.
        s=app.state_data=core.fresh('ivan');s['world']['time_mode']='paused'
        arrive(s,'market');app.play_screen();app.update()
        guards.start(s,'pilot:clubs',guards.profile(s,'clubs'),'pilot-art')
        restored=json.loads(json.dumps(s));before=copy.deepcopy(restored)
        app.state_data=restored
        for size in ('1280x900','1000x800'):
            app.geometry(size);combat_ui.open_combat(app);app.update()
            assert app.combat_view.master is app.presence_view.master
            assert app.combat_view.execute_button.winfo_viewable()
            shot('combat-clubs-'+size)
        # Rendering does not change selected outfits or combat identity in an old save.
        assert restored['world'].get('player_outfit')==before['world'].get('player_outfit')
        assert combat.active(restored)['opponent']==combat.active(before)['opponent']
        assert not errors,errors
        print('Pilot: 6 selection renders, 4 solo/group sizes, Charles laboratory, 2 residents, 2 restored-save combat renders; in-person routing and outfit identity passed.')
    finally:
        app.sounds.close();app.destroy()
