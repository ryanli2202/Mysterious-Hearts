"""Exercise all eight phone apps and async design jobs without paid generation."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import tempfile
import time
import threading
import tkinter as tk
from unittest.mock import Mock, patch
from PIL import Image, ImageGrab
import camera
import codex_images
import game_core as core
import lifestyle_apps
import phone_ui
import winterfield_ui


def pump(root, predicate, seconds=5):
    until = time.monotonic()+seconds
    while not predicate() and time.monotonic() < until:
        root.update()
        time.sleep(.02)
    root.update()
    assert predicate()


def main():
    with tempfile.TemporaryDirectory(dir=core.ROOT / '.test-tmp') as folder:
        folder = Path(folder)
        path = folder/'outfit.png'
        Image.new('RGB', (200, 300), '#6688aa').save(path)
        root = tk.Tk()
        root.withdraw()
        winterfield_ui.install(root)
        root.state_data = core.fresh('rei')
        root.busy = False
        root.sounds = Mock()
        root.persist = Mock()
        root.render = Mock()
        root.update_phone_notification = Mock()
        root.show_in_person = Mock()
        root.open_calendar = Mock()
        errors = []
        root.report_callback_exception = lambda *args: errors.append(args)
        with patch.object(codex_images, 'STORE', folder), patch.object(camera, 'ALBUMS', folder/'albums'):
            phone = phone_ui.PhoneWindow(root)
            phone.geometry('430x740')
            root.update()
            for name in lifestyle_apps.NAMES:
                phone.open_app(name)
                root.update()
                assert phone.lifestyle_view.root.winfo_ismapped(), name
            phone.open_app('Mixtape')
            view = phone.lifestyle_view
            view.go('editor')
            view = phone.lifestyle_view
            view.fields['title'].insert(0, 'The river walk')
            view.add_song('voss-01')
            view.save()
            assert lifestyle_apps.ensure(root.state_data)['playlists']
            phone.open_app('Wardrobe')
            phone.lifestyle_view.wardrobe_tab('design')
            view = phone.lifestyle_view
            view.fields['Design name'].insert(0, 'Test coat')
            view.fields['Outfit description'].insert('1.0', 'A blue wool coat with silver buttons')
            ready = threading.Event()
            def generate(prompt, cancel, progress, references):
                assert 'blue wool coat' in prompt and references
                ready.wait(2)
                return dict(id='smoke-design', path=str(path))
            with patch.object(codex_images, 'generate', side_effect=generate):
                view.generate()
                phone.open_app('Pocket Wallet')
                ready.set()
                pump(root, lambda: root.outfit_jobs.cancel_event is None)
            assert len(lifestyle_apps.ensure(root.state_data)['designs']) == 1
            phone.open_app('Wardrobe')
            assert phone.lifestyle_view.get('Design name') == 'Test coat'
            phone.lifestyle_view.wardrobe_tab('closet')
            label = lifestyle_apps.ensure(root.state_data)['designs'][0]['label']
            assert label in phone.lifestyle_view.fields['Outfit']['values']
            phone.lifestyle_view.fields['Outfit'].set(label)
            phone.lifestyle_view.act(lifestyle_apps.wear, label)
            assert root.state_data['world']['player_outfit'] == label
            import game
            root.photos = {}
            portrait = game.Game.portrait(root, 'rei', (165, 195))
            assert portrait.width() == 165 and portrait.height() == 195
            assert any(str(path) in key for key in root.photos)
            phone.lifestyle_view.show_outfit(camera.outfits(root.state_data, 'rei'))
            root.update()
            screenshots = core.ROOT/'tests'/'screenshots'
            screenshots.mkdir(exist_ok=True)
            ImageGrab.grab(window=phone.winfo_id()).save(screenshots/'lifestyle-wardrobe.png')
            phone.lifestyle_view.wardrobe_tab('design')
            with patch.object(codex_images, 'generate', side_effect=RuntimeError('Test offline error')):
                phone.lifestyle_view.generate()
                pump(root, lambda: root.outfit_jobs.cancel_event is None)
            assert 'Test offline error' in root.outfit_jobs.status
            with patch.object(codex_images, 'generate', side_effect=generate):
                phone.lifestyle_view.generate()
                root.outfit_jobs.cancel()
                pump(root, lambda: root.outfit_jobs.cancel_event is None)
            assert len(lifestyle_apps.ensure(root.state_data)['designs']) == 1
            phone.open_app('Home')
            root.update()
            assert not errors, errors
            phone.destroy()
        root.destroy()
    print('Eight app screens, saved drafts, outfit generation, switching apps, failure and cancellation passed.')


if __name__ == '__main__': main()
