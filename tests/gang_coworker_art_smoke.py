"""Validate all coworker assets and render their actual local/phone views."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import json
from unittest.mock import patch
from PIL import Image, ImageDraw, ImageGrab
import game
import game_core as core
import gang_members
import grove
import town
import groups
from careers_ui_smoke import audit


def main():
    manifest = json.loads((core.ROOT/'assets/gang-coworkers-art.json').read_text(encoding='utf-8-sig'))
    assert len(manifest['files']) == 28
    assert {(a['name'], a['kind']) for a in manifest['files']} == {
        (name, kind) for name in gang_members.NAMES for kind in ('portrait', 'contact')}
    preview = Image.new('RGB', (1400, 900), '#202938')
    draw = ImageDraw.Draw(preview)
    for i, name in enumerate(gang_members.NAMES):
        portrait = core.ROOT/'assets/portraits'/f"{name.lower().replace(' ', '-')}-selection.png"
        contact = core.ROOT/'assets/profiles'/f'{name}.png'
        with Image.open(portrait) as im:
            assert im.mode == 'RGBA' and min(im.size) >= 512, name
            alpha = im.getchannel('A')
            low, high = alpha.getextrema()
            assert low == 0 and high >= 250, name
            hist = alpha.histogram()
            assert hist[0] / (im.width*im.height) > .15, name
            # Inspection sheet composites the original alpha; source assets are untouched.
            p = im.copy(); p.thumbnail((150, 335))
            x, y = (i % 7)*200, (i // 7)*450
            preview.paste(p, (x+(200-p.width)//2, y+5), p)
        with Image.open(contact) as im:
            assert im.width == im.height and im.width >= 512, name
            assert im.convert('RGBA').getchannel('A').getextrema() == (255, 255), name
            preview.paste(im.resize((96, 96)), (x+52, y+325))
        draw.text((x+12, y+430), name, fill='#eeeeee')
    preview.save(core.ROOT/'assets/gang-coworkers-preview.png')
    with patch.object(game.Game, 'check', lambda self: None), \
         patch.object(game.Game, 'persist', lambda self: None), \
         patch.object(game.Game, 'begin_incoming', lambda self: None), \
         patch.object(grove.GrovePump, 'tick', lambda self: None):
        app = game.Game(); errors = []
        app.report_callback_exception = lambda *args: errors.append(args)
        try:
            s = app.state_data = core.fresh('garrett')
            app.play_screen(); app.phone_window(); phone = app.phone_activity
            out = core.ROOT/'.test-tmp'; out.mkdir(exist_ok=True)
            for name, person in gang_members.MEMBERS.items():
                town.end_hangouts(s)
                if s['world']['location'] != person['base']:
                    town.travel(s, person['base'])
                gid = groups.open_local(s, name)
                app.select_group(gid); app.show_in_person(); app.update()
                assert app.portrait(name, (260,350), outfit='selection') is not None, name
                groups.close_active(s, 'Artwork review')
                app.phone_window()
                phone.open_thread('npc:'+name, True); app.update()
                assert phone.avatars._avatar(name) is not None, name
                audit(phone)
            for width in (430, 390):
                phone.geometry(f'{width}x740')
                phone.open_thread('npc:Nessa Quinn', True); app.update(); audit(phone)
                ImageGrab.grab(window=phone.winfo_id()).save(out/f'gang-coworker-photo-{width}.png')
            town.travel(s, 'lantern_house')
            gid = groups.open_local(s, 'Nessa Quinn')
            app.select_group(gid); app.show_in_person(); app.update()
            ImageGrab.grab(window=app.winfo_id()).save(out/'gang-coworker-local-art.png')
            assert not errors, errors
            print('PASS: 14 transparent sprites, 14 opaque square photos, all local/phone loaders, dark states and two phone sizes.')
        finally:
            app.sounds.close(); app.destroy()


if __name__ == '__main__':
    main()
