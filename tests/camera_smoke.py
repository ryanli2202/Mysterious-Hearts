"""Real phone UI and asynchronous camera/gallery flow; no generation charges."""
import copy
from pathlib import Path
import sys
import tempfile
import threading
import time
import tkinter as tk
from unittest.mock import Mock, patch
from PIL import Image, ImageGrab

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import camera
import camera_ui
import codex_images
import game_core as core
import phone_ui
import town
import winterfield_ui


def pump(root, predicate, seconds=4):
    until = time.monotonic() + seconds
    while not predicate() and time.monotonic() < until:
        root.update()
        time.sleep(.02)
    root.update()
    assert predicate()


def main():
    with tempfile.TemporaryDirectory(dir=core.ROOT / '.test-tmp') as tmp:
        folder = Path(tmp)
        root = tk.Tk()
        root.withdraw()
        winterfield_ui.install(root)
        root.state_data = core.fresh('rei')
        root.state_data['world']['location'] = town.HOMES['rei']
        root.state_data['world']['cast']['rei']['location'] = town.HOMES['rei']
        root.state_data['world']['party'] = ['emily']
        root.state_data['world']['cast']['emily'].update(location=town.HOMES['rei'], activity='Hanging out', journey=None)
        root.state_data['relationships']['emily']['status'] = 'dating'
        root.persist = Mock()
        root.sounds = Mock()
        root.busy = False
        root.update_phone_notification = Mock()
        root.show_in_person = Mock()
        with patch.object(camera, 'ALBUMS', folder / 'albums'), patch.object(codex_images, 'STORE', folder):
            phone = phone_ui.PhoneWindow(root, 'Home')
            root.update()
            phone.open_app('Camera')
            root.update()
            view = phone.camera_view
            assert 'Mirror selfie' in view.mode_picker['values']
            root.state_data['world']['location'] = 'studio'
            view.context = camera.scene(root.state_data); view.update_controls()
            assert 'Modelling portrait' in view.mode_picker['values']
            view.mode.set('Modelling portrait'); view.update_controls()
            view.choices('rei').update(expression='Editorial gaze', pose='Runway walk')
            root.state_data['world']['location'] = town.HOMES['rei']
            view.context = camera.scene(root.state_data); view.update_controls()
            assert view.mode.get() == 'Selfie'
            assert view.choices('rei')['pose'] == 'Relaxed'
            assert view.choices('rei')['expression'] == 'Natural smile'
            view.mode.set('Group selfie'); view.update_controls()
            view.wheel('expression')
            custom_wheel = next(w for w in phone.dialogs if isinstance(w, camera_ui.SelectionWheel))
            custom_wheel.destroy()
            view.custom_selection('expression', '', lambda value: (
                view.choices('rei').update(expression=value), view.save_preferences(), root.persist()))
            custom_window = phone.dialogs[-1]
            custom_body = custom_window.winfo_children()[0]
            from tkinter import ttk
            custom_field = next(w for w in custom_body.winfo_children() if isinstance(w, ttk.Combobox))
            custom_field.set('A subtle crooked smile')
            next(w for w in custom_body.winfo_children() if isinstance(w, camera_ui.PhoneButton)).invoke()
            assert view.choices('rei')['expression'] == 'Custom: A subtle crooked smile'
            assert camera.saved_selections(root.state_data, 'expression') == ['A subtle crooked smile']
            view.person.set(camera.name('emily')); view.update_labels()
            view.wheel('group_pose')
            wheel = next(w for w in phone.dialogs if isinstance(w, camera_ui.SelectionWheel))
            assert 'Hold hands · Emily Fields' in wheel.options
            wheel.page(-1)
            assert wheel.index == ((len(wheel.options) - 1) // 8) * 8
            wheel.page(1)
            assert wheel.index == 0
            wheel.pick(wheel.options.index('Hold hands · Emily Fields')); wheel.choose()
            assert view.settings['group_pose'] == 'Hold hands · Emily Fields'
            view.outfit_dialog()
            outfit_window = phone.dialogs[-1]
            def descendants(widget):
                for child in widget.winfo_children():
                    yield child
                    yield from descendants(child)
            from tkinter import ttk
            combos = [w for w in descendants(outfit_window) if isinstance(w, ttk.Combobox)]
            assert len(combos) == 4
            combos[0].set('Custom'); combos[1].set('A navy cardigan')
            apply_button = next(w for w in descendants(outfit_window)
                                if isinstance(w, camera_ui.PhoneButton) and w.cget('text') == 'Use outfits for photo')
            apply_button.invoke()
            assert 'A navy cardigan' in camera.ensure(root.state_data)['custom_outfits']['rei']
            view.detail.set('By the living room window')
            phone.open_app('Gallery'); root.update()
            assert camera.ensure(root.state_data)['preferences']['mode'] == 'Group selfie'
            phone.open_app('Camera'); root.update()
            view = phone.camera_view
            assert view.choices('rei')['custom'] == 'A navy cardigan'
            assert view.choices('rei')['expression'] == 'Custom: A subtle crooked smile'
            source = folder / 'test.png'
            Image.new('RGB', (600, 600), '#728da6').save(source)
            ready = threading.Event()
            def generate(prompt, cancel, progress, references):
                assert len(references) == 2
                progress('Developing test photo')
                ready.wait(3)
                return dict(id='test', path=str(source), created=time.time())
            with patch.object(codex_images, 'generate', side_effect=generate):
                view.take()
                captured = root.state_data['world']['minute']
                assert view.controller.cancel_event
                phone.open_app('Gallery')
                root.state_data['world']['minute'] += 1440
                ready.set()
                pump(root, lambda: len(camera.photos(root.state_data)) == 1)
                gallery = next(w for w in phone.screen.winfo_children()[0].winfo_children() if isinstance(w, camera_ui.GalleryView))
                pump(root, lambda: bool(gallery.images))
                assert camera.photos(root.state_data)[0]['minute'] == captured
                phone.open_app('Camera')
                root.update()
                assert phone.camera_view.photo is not None
                for size in ('660x850', '560x680'):
                    phone.geometry(size)
                    root.update()
                    view = phone.camera_view
                    assert view.shutter.winfo_ismapped()
                    assert view.shutter.winfo_rooty() + view.shutter.winfo_height() <= phone.winfo_rooty() + phone.winfo_height()
                screenshot = core.ROOT / 'tests' / 'screenshots' / 'camera-phone.png'
                ImageGrab.grab(window=phone.winfo_id()).save(screenshot)
                phone.open_app('Gallery'); root.update()
                ImageGrab.grab(window=phone.winfo_id()).save(screenshot.with_name('camera-gallery.png'))
            phone.open_app('Camera'); root.update()
            view = phone.camera_view
            view.manage_custom(phone, 'expression')
            manager = phone.dialogs[-1]
            manager_body = manager.winfo_children()[0]
            editor = next(w for w in manager_body.winfo_children() if isinstance(w, tk.Text))
            editor.delete('1.0', 'end'); editor.insert('1.0', 'A bright, confident smile')
            actions = manager_body.winfo_children()[-1]
            buttons = {w.cget('text'): w for w in actions.winfo_children()}
            original_snapshot = copy.deepcopy(camera.photos(root.state_data)[0]['snapshot'])
            buttons['Save changes'].invoke()
            assert view.choices('rei')['expression'] == 'Custom: A bright, confident smile'
            buttons['Delete saved'].invoke()
            assert view.choices('rei')['expression'] == camera.EXPRESSIONS[0]
            assert not camera.saved_selections(root.state_data, 'expression')
            assert camera.photos(root.state_data)[0]['snapshot'] == original_snapshot
            assert buttons['Delete saved'].cget('state') == 'disabled'
            buttons['Done'].invoke()
            phone.close_phone()
        root.destroy()
    print('PASS: phone modes, romance wheel, preferences, reference request, app switching, auto-gallery, preview, compact layout')


if __name__ == '__main__': main()
