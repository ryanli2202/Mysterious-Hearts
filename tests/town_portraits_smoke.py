"""Check generated town assets through actual Tk portrait and phone loaders."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import json
import tkinter as tk
from unittest.mock import patch
from PIL import Image, ImageGrab, ImageTk
import game
import game_core as core
import grove
import phone_chat
import phone_numbers
import town_residents
import town
import outskirts
import gang_leaders
import gang_members
import street_recruits

names = [person[0] for person in (*town.NPCS, *town.VENUE_STAFF.values(), town.HQ_EXECUTIVE)]

folder = core.ROOT / 'assets' / 'portraits'
manifest = json.loads((folder / 'town-residents-manifest.json').read_text(encoding='utf-8'))
assert {entry['name'] for entry in manifest['portraits']} == set(town_residents.RESIDENTS)
for entry in manifest['portraits']:
    with Image.open(folder / entry['file']) as image:
        assert image.mode == 'RGBA', entry['name']
        low, high = image.getchannel('A').getextrema()
        assert low == 0 and high >= 250, entry['name']
        assert min(image.size) >= 512

for name in names:
    with Image.open(folder / (name.lower().replace(' ', '-') + '-selection.png')) as portrait:
        assert portrait.mode == 'RGBA', name
        low,high=portrait.getchannel('A').getextrema()
        assert low==0 and high>=250, name
    with Image.open(core.ROOT / 'assets' / 'profiles' / (name + '.png')) as photo:
        assert photo.width == photo.height and photo.width >= 512, name
        if name in outskirts.RESIDENTS:
            assert photo.convert('RGBA').getchannel('A').getextrema() == (255, 255), name

with patch.object(game.Game, 'check', lambda self: None), \
     patch.object(game.Game, 'persist', lambda self: None), \
     patch.object(game.Game, 'begin_incoming', lambda self: None), \
     patch.object(grove.GrovePump, 'tick', lambda self: None):
    app = game.Game()
    errors = []
    app.report_callback_exception = lambda *args: errors.append(args)
    try:
        app.state_data = core.fresh('rei')
        app.play_screen()
        app.phone_window()
        phone = app.phone_activity
        # New street residents have dedicated transparent portraits and contact photos.
        for name in street_recruits.NAMES:
            phone_numbers.add(app.state_data, phone_numbers.NUMBERS[name])
            assert app.portrait(name, (145,180), outfit='selection') is not None
            phone.open_thread('npc:'+name, True)
            app.update()
        for name in outskirts.RESIDENTS:
            phone_numbers.add(app.state_data, phone_numbers.NUMBERS[name])
            assert app.portrait(name, (145, 180), outfit='selection') is not None
            phone.open_thread('npc:'+name, True)
            app.update()
        for name in names:
            if name in gang_members.MEMBERS:
                town.end_hangouts(app.state_data)
                if app.state_data['world']['location'] != gang_members.MEMBERS[name]['base']:
                    town.travel(app.state_data, gang_members.MEMBERS[name]['base'])
                import groups
                groups.open_local(app.state_data, name)
                groups.close_active(app.state_data, 'Portrait check complete')
            if name in gang_leaders.BY_NAME:
                p=gang_leaders.BY_NAME[name]
                town.end_hangouts(app.state_data); town.travel(app.state_data,p['base'])
                import groups
                groups.open_local(app.state_data,name); groups.close_active(app.state_data,'Portrait check complete')
            if name == 'Keisuke Hachimura':
                from test_keisuke import join
                join(app.state_data)
            phone_numbers.add(app.state_data, phone_numbers.NUMBERS[name])
            assert phone.avatars._avatar(name) is not None, name
            assert phone_chat.avatar_identity(app.state_data, 'npc:'+name, True) == name
            direct = app.portrait(name, (145,180), outfit='selection')
            slug = app.portrait(name.lower().replace(' ','-'), (145,180), outfit='selection')
            assert direct is slug, name
        phone.open_app('Contacts')
        app.update()
        out = core.ROOT / 'tests' / 'screenshots'
        out.mkdir(exist_ok=True)
        ImageGrab.grab(window=phone.winfo_id()).save(out/'outskirts-profile-contacts.png')
        phone.open_thread('npc:Hazel Reed', True)
        app.update()
        ImageGrab.grab(window=phone.winfo_id()).save(out/'outskirts-profile-messages.png')
        gallery = tk.Toplevel(app)
        gallery.title('Winterfield town portraits')
        gallery.configure(bg='#18202d')
        profile_images = []
        for i, name in enumerate(outskirts.RESIDENTS):
            card = tk.Frame(gallery, bg='#18202d', padx=10, pady=8)
            card.grid(row=i//4, column=i%4)
            with Image.open(core.ROOT / 'assets' / 'profiles' / (name+'.png')) as source:
                photo = ImageTk.PhotoImage(source.resize((200,200), Image.Resampling.LANCZOS), master=gallery)
            profile_images.append(photo)
            tk.Label(card, image=photo, bg='#18202d').pack()
            tk.Label(card, image=phone.avatars._avatar(name), bg='#18202d').pack()
            tk.Label(card,text=name,bg='#18202d',fg='#eee7db',font=('Segoe UI',10)).pack()
        app.update()
        ImageGrab.grab(window=gallery.winfo_id()).save(out/'outskirts-profile-gallery.png')
        for child in gallery.winfo_children(): child.destroy()
        profile_images.clear()
        for i,name in enumerate(street_recruits.NAMES):
            card=tk.Frame(gallery,bg='#18202d',padx=8,pady=8); card.grid(row=i//3,column=i%3)
            tk.Label(card,text=name,bg='#18202d',fg='#eee7db').pack()
            row=tk.Frame(card,bg='#18202d'); row.pack()
            tk.Label(row,image=app.portrait(name,(130,170),outfit='selection'),bg='#18202d').pack(side='left')
            with Image.open(core.ROOT/'assets'/'profiles'/(name+'.png')) as source:
                assert source.convert('RGBA').getchannel('A').getextrema()==(255,255)
                photo=ImageTk.PhotoImage(source.resize((160,160),Image.Resampling.LANCZOS),master=gallery)
            profile_images.append(photo); tk.Label(row,image=photo,bg='#18202d').pack(side='left')
        app.update()
        ImageGrab.grab(window=gallery.winfo_id()).save(out/'street-recruit-art-gallery.png')
        phone.open_thread('npc:Keira Shaw',True); app.update()
        ImageGrab.grab(window=phone.winfo_id()).save(out/'street-recruit-art-messages.png')
        assert not errors, errors
        print(f'All {len(names)} transparent portraits, direct-name lookup, contact photos or portrait-backed avatars, and message headers verified.')
    finally:
        app.sounds.close()
        app.destroy()
