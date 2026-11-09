"""Real joining, liaison message, depot NPC portrait and dark phone; no AI/save writes."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from unittest.mock import patch
from PIL import ImageGrab
import game
import game_core as core
import groups
import grove
import town
import crime_operations
import keisuke
import phone_chat
from test_keisuke import join
from careers_ui_smoke import audit

with patch.object(game.Game,'check',lambda self:None), \
     patch.object(game.Game,'persist',lambda self:None), \
     patch.object(game.Game,'begin_incoming',lambda self:None), \
     patch.object(grove.GrovePump,'tick',lambda self:None):
    app=game.Game();errors=[]
    app.report_callback_exception=lambda *args:errors.append(args)
    try:
        s=app.state_data=core.fresh('rei');join(s)
        town.end_hangouts(s);town.travel(s,'site_02')
        crime_operations.enter(s,'site_02','reception')
        app.play_screen()
        gid=groups.open_local(s,keisuke.NAME);app.select_group(gid);app.update()
        assert app.portrait(keisuke.NAME,(260,350),outfit='selection') is not None
        assert not town.romanceable(s,keisuke.NAME)
        out=core.ROOT/'.test-tmp';out.mkdir(exist_ok=True)
        ImageGrab.grab(window=app.winfo_id()).save(out/'keisuke-depot.png')
        groups.close_active(s,'The meeting ended.')
        app.phone_window();phone=app.phone_activity
        for width,height in ((430,740),(390,690)):
            phone.geometry(f'{width}x{height}')
            phone.open_thread('npc:'+keisuke.NAME,True);app.update();audit(phone)
            assert phone_chat.avatar_identity(s,'npc:'+keisuke.NAME,True)==keisuke.NAME
            assert not phone.personal_suggestions.winfo_manager()
            ImageGrab.grab(window=phone.winfo_id()).save(out/f'keisuke-message-{width}.png')
        phone.open_app('Bubblegram');phone.job_board.change('Network');app.update();audit(phone)
        phone.job_board.body.master.yview_moveto(.26);app.update()
        ImageGrab.grab(window=phone.winfo_id()).save(out/'keisuke-network.png')
        phone.open_app('Contacts');app.update();audit(phone)
        assert phone.avatars._avatar(keisuke.NAME) is not None
        assert not errors,errors
        print('PASS: joining introduction, depot NPC portrait, dark liaison messaging, compact resize and Network/Contacts.')
    finally:
        app.sounds.close();app.destroy()
