"""Mobile layouts, live search, shortcuts and populated gallery; no external services."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import tkinter as tk
from tkinter import ttk
from unittest.mock import Mock, patch
from PIL import Image, ImageGrab
import camera
import game_core as core
import lifestyle_apps
import phone_ui
import winterfield_ui
from phone_controls import PhoneButton


def descendants(widget):
    for child in widget.winfo_children():
        yield child
        yield from descendants(child)


def main():
    root = tk.Tk()
    root.withdraw()
    winterfield_ui.install(root)
    root.state_data = core.fresh('rei')
    from supafast_fixtures import seed
    seed(root.state_data)
    from supafast_fixtures import disable_images
    disable_images(root)
    root.busy = False
    for name in ('sounds', 'persist', 'render', 'update_phone_notification', 'show_in_person', 'open_calendar'):
        setattr(root, name, Mock())
    errors = []
    root.report_callback_exception = lambda *args: errors.append(args)
    shots = []
    folder = core.ROOT / 'tests/screenshots'
    folder.mkdir(exist_ok=True)
    lifestyle_apps.save_playlist(root.state_data, 'After the rain', 'River lights — Local band\nStay a while — Winterfield', 'For the walk home')
    phone = phone_ui.PhoneWindow(root)
    try:
        for size in ('430x740', '560x780'):
            phone.geometry(size)
            for name in ('Supafast', 'Doober Eats', 'Mixtape', 'Wardrobe', 'Out & About', 'Pocket Wallet', 'Postcards', 'Campus Portal', 'Mini Games', 'Recipe Box', 'Winterfield Exchange'):
                phone.open_app(name)
                root.update()
                buttons = [w for w in descendants(phone.screen) if isinstance(w, PhoneButton)]
                if name == 'Mixtape':
                    phone.lifestyle_view.go('search')
                    root.update()
                    phone.lifestyle_view.go('home')
                    root.update()
                elif name in lifestyle_apps.NAMES:
                    view = phone.lifestyle_view
                    view.jump(view.form_position)
                    root.update()
                    view.jump(0)
                    root.update()
                if name in ('Supafast', 'Doober Eats'):
                    search = next(w for w in descendants(phone.screen) if isinstance(w, ttk.Entry) and not isinstance(w, ttk.Combobox))
                    search.insert(0, 'NO_MATCH_123')
                    root.update()
                    assert any(isinstance(w, tk.Label) and w.cget('text') == 'No matches' for w in descendants(phone.screen))
                    search.delete(0, 'end')
                    root.update()
                    assert any(isinstance(w, PhoneButton) and w.cget('text') in ('Buy / send', 'Order / send') for w in descendants(phone.screen))
                    next(w for w in buttons if w.cget('text') == 'Orders').invoke()
                    root.update()
                    assert phone.selected == 'Deliveries'
                    phone.open_app(name)
                    root.update()
                if size == '430x740':
                    shots.append(ImageGrab.grab(window=phone.winfo_id()).convert('RGB').resize((258, 444)))
        source = core.ROOT / 'assets/ui/phone-wallpaper-rei.png'
        records = [dict(id=str(i), date='November 7', minute=600+i, mode='Selfie', location='Winterfield') for i in range(4)]
        with patch.object(camera, 'photos', return_value=records), patch.object(camera, 'photo_path', return_value=source):
            phone.geometry('430x740')
            phone.open_app('Gallery')
            root.update()
            shots.append(ImageGrab.grab(window=phone.winfo_id()).convert('RGB').resize((258, 444)))
            assert len([w for w in descendants(phone.screen) if isinstance(w, PhoneButton) and w.cget('text') == 'View']) == 4
        assert not errors, errors
        sheet = Image.new('RGB', (258*4, 444*3), '#17171b')
        for i, shot in enumerate(shots): sheet.paste(shot, (i%4*258, i//4*444))
        sheet.save(folder/'phone-app-redesign.png')
    finally:
        phone.destroy()
        root.destroy()
    print('Mobile app layouts, two device sizes, live search, order navigation, section shortcuts and populated gallery passed.')

if __name__ == '__main__': main()
