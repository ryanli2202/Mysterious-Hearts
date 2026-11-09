"""Product image queue, caching, retry and real Tk rendering without generation charges."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import json
import tempfile
import threading
import time
import tkinter as tk
from unittest.mock import Mock, patch
from PIL import Image, ImageGrab
import codex_images
import game_core as core
import phone_apps as apps
import phone_ui
import supafast
import winterfield_ui
from supafast_fixtures import seed
from supafast_ui import ProductPhoto


def pump(root, predicate, seconds=12):
    end=time.monotonic()+seconds
    while not predicate() and time.monotonic()<end:
        root.update(); time.sleep(.02)
    root.update()
    assert predicate(), 'Timed out waiting for product images'


def descendants(widget):
    for child in widget.winfo_children():
        yield child
        yield from descendants(child)


def main():
    with tempfile.TemporaryDirectory(dir=core.ROOT/'.test-tmp') as tmp:
        folder=Path(tmp)
        imagefile=folder/'product.png'
        # Fixture only: production images always come from codex_images.generate.
        source=core.ROOT/'assets/ui/phone-wallpaper-rei.png'
        with Image.open(source) as picture: picture.resize((512,512)).save(imagefile)
        root=tk.Tk(); root.withdraw(); winterfield_ui.install(root)
        root.state_data=core.fresh('rei'); seed(root.state_data)
        root.busy=False
        for name in ('sounds','persist','render','update_phone_notification','show_in_person'):
            setattr(root,name,Mock())
        errors=[];root.report_callback_exception=lambda *e:errors.append(e)
        gate=threading.Event();fail=[False];calls=[]
        def generate(prompt,cancel):
            calls.append(prompt)
            while not gate.wait(.02):
                if cancel.is_set(): raise RuntimeError('cancelled')
            if cancel.is_set() or fail[0]: raise RuntimeError('test failure')
            return {'id':str(len(calls)), 'path':str(imagefile)}
        with patch.object(codex_images,'STORE',folder),patch.object(codex_images,'generate',side_effect=generate), patch.object(supafast,'generate',side_effect=RuntimeError('Mock text provider')):
            phone=phone_ui.PhoneWindow(root,'Supafast');phone.geometry('430x740');root.update()
            try:
                manager=root.supafast_images
                assert len(calls)==1
                phone.open_app('Supafast');root.update();assert len(calls)==1
                fail[0]=True;gate.set()
                pump(root,lambda:manager.failure is not None)
                pump(root,lambda:any(isinstance(w,ProductPhoto) and w.retry.winfo_ismapped() for w in descendants(phone.screen)))
                fail[0]=False;manager.request(retry=True)
                pump(root,lambda:all(supafast.image_path(p) for p in apps.catalog(root.state_data).values()))
                assert len(calls)==13
                assert 'dark slate' in calls[0] and 'description' in calls[0]
                pump(root,lambda:any(isinstance(w,ProductPhoto) and w.photo is not None for w in descendants(phone.screen)))
                output=core.ROOT/'tests/screenshots';output.mkdir(exist_ok=True)
                ImageGrab.grab(window=phone.winfo_id()).save(output/'supafast-product-photos.png')
                root.state_data=json.loads(json.dumps(root.state_data))
                phone.open_app('Supafast');root.update();assert len(calls)==13
                # Missing image is eligible for regeneration without rerolling the item.
                first=next(iter(apps.catalog(root.state_data).values()))
                first['image']='assets/generated/missing-product.png'
                manager.request();pump(root,lambda:supafast.image_path(first) is not None)
                assert len(calls)==14
                # Next day cancels outstanding work and never attaches it to new stock.
                gate.clear();root.state_data['world']['minute']+=1440;seed(root.state_data)
                phone.open_app('Supafast');root.update()
                token=manager.cancel
                root.state_data['world']['minute']+=1440
                pump(root,lambda:token.is_set())
                phone.open_app('Notes')
                # Avoid starting text AI at midnight while checking the image queue.
                gate.set();pump(root,lambda:manager.running is None)
                # A different story also cancels without attaching its predecessor's image.
                seed(root.state_data);gate.clear();manager.request();token=manager.cancel
                root.state_data=core.fresh('garrett');seed(root.state_data)
                pump(root,lambda:token.is_set())
                gate.set();pump(root,lambda:manager.running is None)
                assert all(not p.get('image') for p in apps.catalog(root.state_data).values())
                assert not errors,errors
            finally:
                gate.set();phone.destroy();root.destroy()
    print('Product photos passed: sequential queue, failure/retry, rendering, persistence, no rerolls, missing-file recovery and day cancellation.')

if __name__=='__main__':main()
