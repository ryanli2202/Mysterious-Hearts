"""Real Tk daily catalogue lifecycle with mocked AI; no requests or save writes."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import threading
import time
import tkinter as tk
from unittest.mock import Mock, patch
from PIL import Image, ImageGrab
import game_core as core
import phone_apps as apps
import phone_ui
import supafast
import winterfield_ui
from phone_controls import PhoneButton
from supafast_fixtures import items


def pump(root, predicate, seconds=6):
    deadline = time.monotonic()+seconds
    while not predicate() and time.monotonic()<deadline:
        root.update()
        time.sleep(.02)
    root.update()
    assert predicate(), 'Timed out waiting for catalogue state'


def children(widget):
    for child in widget.winfo_children():
        yield child
        yield from children(child)


def main():
    root = tk.Tk()
    root.withdraw()
    winterfield_ui.install(root)
    root.state_data = core.fresh('rei')
    from supafast_fixtures import disable_images
    disable_images(root)
    root.busy = False
    for name in ('sounds', 'persist', 'render', 'update_phone_notification', 'show_in_person'):
        setattr(root, name, Mock())
    errors = []
    root.report_callback_exception = lambda *args: errors.append(args)
    gate = threading.Event()
    fail = [False]
    def generate(state, day):
        gate.wait(4)
        if fail[0]: raise RuntimeError('Mock offline provider')
        return items(day)
    shots = []
    with patch.object(supafast, 'generate', side_effect=generate) as generate_mock:
        phone = phone_ui.PhoneWindow(root, 'Supafast')
        phone.geometry('430x740')
        try:
            root.update()
            manager = root.supafast_jobs
            assert manager.status() == 'loading'
            shots.append(ImageGrab.grab(window=phone.winfo_id()).convert('RGB'))
            phone.open_app('Supafast')
            assert generate_mock.call_count == 1
            phone.open_app('Notes')
            gate.set()
            pump(root, lambda: bool(apps.catalog(root.state_data)))
            root.persist.assert_called()
            phone.open_app('Supafast')
            root.update()
            assert any(isinstance(w, tk.Label) and 'textured surface' in w.cget('text') for w in children(phone.screen))
            shots.append(ImageGrab.grab(window=phone.winfo_id()).convert('RGB'))
            assert generate_mock.call_count == 1
            buy = next(w for w in children(phone.screen) if isinstance(w, PhoneButton) and w.cget('text') == 'Buy / send')
            buy.invoke()
            assert len(apps.ensure(root.state_data)['orders']) == 1
            fail[0] = True
            root.state_data['world']['minute'] += 1440
            pump(root, lambda: manager.status() == 'error')
            pump(root, lambda: any(isinstance(w, PhoneButton) and w.cget('text') == 'Retry daily selection' for w in children(phone.screen)))
            assert not apps.catalog(root.state_data)
            shots.append(ImageGrab.grab(window=phone.winfo_id()).convert('RGB'))
            attempts = generate_mock.call_count
            phone.open_app('Supafast')
            assert generate_mock.call_count == attempts
            fail[0] = False
            next(w for w in children(phone.screen) if isinstance(w, PhoneButton) and w.cget('text') == 'Retry daily selection').invoke()
            pump(root, lambda: bool(apps.catalog(root.state_data)))
            # A day changes during an in-flight request: only the later day can publish.
            gate.clear()
            root.state_data['world']['minute'] += 1440
            phone.open_app('Supafast')
            stale_day = root.state_data['world']['minute']//1440
            root.state_data['world']['minute'] += 1440
            gate.set()
            pump(root, lambda: bool(apps.catalog(root.state_data)))
            assert str(stale_day) not in apps.ensure(root.state_data)['catalogs']
            # Switching save while generating must not write results into either save.
            gate.clear()
            root.state_data['world']['minute'] += 1440
            phone.open_app('Supafast')
            old = root.state_data
            phone.open_app('Notes')
            root.state_data = core.fresh('garrett')
            gate.set()
            pump(root, lambda: manager.running is None)
            assert not apps.catalog(old) and not apps.catalog(root.state_data)
            assert not errors, errors
            folder = core.ROOT/'tests/screenshots'
            folder.mkdir(exist_ok=True)
            sheet = Image.new('RGB', (430*3, 740), '#17171b')
            for i, shot in enumerate(shots): sheet.paste(shot.resize((430,740)), (430*i,0))
            sheet.save(folder/'supafast-ai-states.png')
        finally:
            gate.set()
            phone.destroy()
            root.destroy()
    print('Supafast UI passed: loading, descriptions, purchase, no rerolls, background completion, midnight, failure/retry and stale-save protection.')

if __name__ == '__main__': main()
