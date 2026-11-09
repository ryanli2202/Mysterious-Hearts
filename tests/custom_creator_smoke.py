"""Offline UI flow: mocked portrait job, real form/state/phone, no story saves."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import time
import tempfile
import shutil
from unittest.mock import patch
from PIL import ImageGrab
import game
import game_core as core
import grove
import custom_creator_ui
import custom_protagonist as custom
import phone_theme
import combat_workshop
from test_enhanced_combat import AMP
from tkinter import ttk
from test_custom_protagonist import PROFILE

out = core.ROOT / 'tests' / 'screenshots'
out.mkdir(exist_ok=True)
with tempfile.TemporaryDirectory(dir=core.ROOT/'assets'/'generated') as folder:
    portrait = Path(folder)/'portrait.png'
    shutil.copyfile(core.ROOT/'assets'/'portraits'/'rei-selection.png', portrait)
    relative = portrait.relative_to(core.ROOT).as_posix()
    with patch.object(game.Game, 'check'), patch.object(game.Game, 'persist'), \
         patch.object(game.Game, 'begin_incoming'), patch.object(grove.GrovePump, 'tick'), \
         patch.object(core, 'save'), patch.object(core, 'load', return_value=None), \
         patch.object(custom, 'generate_portrait', return_value=relative):
        app = game.Game()
        errors = []
        app.report_callback_exception = lambda *args: errors.append(args)
        creator = custom_creator_ui.CharacterCreator(app)
        for key, value in PROFILE.items():
            if key in ('appearance', 'home'): continue
            creator.values[key].set(', '.join(value) if key == 'interests' else str(value))
        creator.home_choice.set('Vacant beach cottage')
        creator.appearance.insert('1.0', PROFILE['appearance'])
        assert str(creator.awakening_trait['state']) == 'disabled'
        creator.awakening_toggle.invoke()
        creator.values['awakening_trait'].set('Resonance')
        creator.awakening_description.insert('1.0', 'Shapes nearby sound; requires concentration.')
        assert creator.collect()['awakened']
        creator.awakening_toggle.invoke()
        assert creator.collect()['awakening_trait'] == ''
        creator.awakening_toggle.invoke()
        app.update()
        for widget, _ in creator.controls:
            if isinstance(widget, ttk.Combobox):
                popup = widget.tk.call('ttk::combobox::PopdownWindow', str(widget))
                assert not phone_theme.is_light_surface(widget, widget.tk.call(str(popup)+'.f.l', 'cget', '-background'))
        creator.generate()
        for _ in range(40):
            app.update()
            if creator.portrait: break
            time.sleep(.025)
        assert creator.portrait
        assert str(creator.begin_button['state']) == 'disabled'
        with patch.object(combat_workshop,'evaluate_trait',side_effect=ValueError('Test Trait evaluation failure')):
            creator.evaluate_trait()
            for _ in range(80):
                app.update(); time.sleep(.025)
                if not creator.cancel_event: break
        assert 'Test Trait evaluation failure' in creator.status['text']
        assert creator.current_trait()[0]=='Resonance' and creator.portrait
        with patch.object(combat_workshop,'evaluate_trait',return_value=combat_workshop.validate_amplifications([AMP])):
            creator.evaluate_trait()
            for _ in range(80):
                app.update(); time.sleep(.025)
                if not creator.cancel_event: break
        assert creator.trait_amplifications and not creator.trait_reviewed.get()
        creator.trait_accept.invoke(); app.update()
        assert str(creator.begin_button['state']) == 'normal'
        ImageGrab.grab(window=creator.winfo_id()).save(out/'custom-creator.png')
        creator.geometry('780x650'); app.update()
        ImageGrab.grab(window=creator.winfo_id()).save(out/'custom-creator-compact.png')
        creator.form_canvas.yview_moveto(1); app.update()
        ImageGrab.grab(window=creator.winfo_id()).save(out/'custom-creator-awakening.png')
        creator.values['hairstyle'].set('Long'); app.update()
        assert str(creator.begin_button['state']) == 'disabled'
        creator.values['hairstyle'].set(PROFILE['hairstyle']); app.update()
        # Failed/cancelled replacement jobs do not discard the accepted portrait.
        creator.cancel_event = __import__('threading').Event()
        creator.events.put(('error', 'Test generation failure'))
        creator.poll()
        assert creator.portrait == relative
        assert 'Test generation failure' in creator.status['text']
        creator.cancel_event = __import__('threading').Event()
        creator.cancel()
        creator.events.put(('error', 'cancelled'))
        creator.poll()
        assert creator.status['text'] == 'Generation cancelled.'
        creator.begin()
        app.update()
        assert custom.is_custom(app.state_data['player'])
        assert app.state_data['custom_protagonist']['awakening_trait'] == 'Resonance'
        assert app.state_data['custom_protagonist']['trait_amplifications'][0]['name']=='Resonant force'
        assert app.state_data['world']['location'] == PROFILE['home']
        app.town_window(); app.update_idletasks()
        ImageGrab.grab(window=app.town_activity.winfo_id()).save(out/'custom-home.png')
        app.town_activity.destroy()
        from phone_icons import COLORS
        for name in ('Home', *COLORS, 'Customise', 'Lock', 'Keepsake'):
            app.phone_window(name)
            app.update()
        app.phone_activity.destroy()
        app.open_profiles(app.state_data['player'])
        app.update()
        app.destroy()
        assert not errors, errors
print('Custom creator form, mock generation, appearance invalidation, start, home and phone pages passed.')
