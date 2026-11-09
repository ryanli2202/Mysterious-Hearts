"""Render bundled Doober art offline, including missing/corrupt dark states."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import tkinter as tk
from tkinter import ttk
from unittest.mock import Mock, patch
from PIL import ImageGrab
import doober_images as food
import game_core as core
import phone_apps as apps
import phone_ui
import winterfield_ui
from supafast_ui import ProductPhoto

def descendants(widget):
    for child in widget.winfo_children():
        yield child
        yield from descendants(child)

def main():
    root = tk.Tk()
    root.withdraw()
    winterfield_ui.install(root)
    root.state_data = core.fresh('rei')
    root.busy = False
    for name in ('sounds', 'persist', 'render', 'update_phone_notification', 'show_in_person'):
        setattr(root, name, Mock())
    errors = []
    root.report_callback_exception = lambda *e: errors.append(e)
    folder = core.ROOT / 'tests/screenshots'
    folder.mkdir(exist_ok=True)
    with patch('codex_images.generate', side_effect=AssertionError('No runtime generation')) as generate:
        phone = phone_ui.PhoneWindow(root, 'Doober Eats')
        try:
            for index, restaurant in enumerate(apps.MENUS):
                phone.restaurant.set(restaurant)
                phone.refresh()
                for size in ('430x740', '560x780'):
                    phone.geometry(size)
                    root.update()
                    photos = [w for w in descendants(phone.screen) if isinstance(w, ProductPhoto)]
                    assert len(photos) == 20
                    assert all(p.photo and p.timer is None and not p.retry.winfo_ismapped() for p in photos)
                    ImageGrab.grab(window=phone.winfo_id()).save(folder / f'doober-bundled-{index}-{size}.png')
            search = next(w for w in descendants(phone.screen)
                          if isinstance(w, ttk.Entry) and not isinstance(w, ttk.Combobox))
            search.insert(0, 'Classic beef burger')
            root.update()
            assert len([w for w in descendants(phone.screen) if isinstance(w, ProductPhoto)]) == 1
            ImageGrab.grab(window=phone.winfo_id()).save(folder / 'doober-bundled-search.png')
            search.delete(0, 'end')
            search.insert(0, 'no-such-food-123')
            root.update()
            assert not any(isinstance(w, ProductPhoto) for w in descendants(phone.screen))
            ImageGrab.grab(window=phone.winfo_id()).save(folder / 'doober-bundled-empty.png')
            for player in ('rei', 'garrett'):
                root.state_data = core.fresh(player)
                root.state_data['world']['minute'] += 1440
                phone.open_app('Doober Eats')
                root.update()
                assert all(w.photo for w in descendants(phone.screen) if isinstance(w, ProductPhoto))
            with patch.object(food.FoodImages, 'image_path', staticmethod(lambda p: None)):
                phone.refresh()
                root.update()
                photos = [w for w in descendants(phone.screen) if isinstance(w, ProductPhoto)]
                assert all('unavailable' in p.label.cget('text') and not p.retry.winfo_ismapped() for p in photos)
                ImageGrab.grab(window=phone.winfo_id()).save(folder / 'doober-bundled-missing.png')
            with patch('supafast_ui.Image.open', side_effect=OSError('corrupt fixture')):
                phone.refresh()
                root.update()
                assert all(not w.retry.winfo_ismapped() for w in descendants(phone.screen) if isinstance(w, ProductPhoto))
            generate.assert_not_called()
            assert not errors, errors
        finally:
            phone.destroy()
            root.destroy()
    print('PASS: 80 bundled images, four restaurants, two sizes, search/empty, days/saves, missing/corrupt states; zero image generation calls.')

if __name__ == '__main__':
    main()
