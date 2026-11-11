"""Guard Part 2 in-person desk, conversation and contact migration render checks."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from unittest.mock import patch
from PIL import ImageGrab
import game,game_core as core,grove,campaign_ui,groups,guard_dialogue as gd
import organisation_guards as guards
from test_major_campaigns import arrive

out=core.ROOT/'tests/screenshots';out.mkdir(exist_ok=True)
with patch.object(game.Game,'check'),patch.object(game.Game,'begin_incoming'),patch.object(game.Game,'persist'),patch.object(grove.GrovePump,'tick'):
    app=game.Game();errors=[];app.report_callback_exception=lambda *e:errors.append(e)
    def shot(name):
        app.update();ImageGrab.grab(window=app.winfo_id()).save(out/('guard-part2-'+name+'.png'))
    def buttons(root):
        return [w for child in root.winfo_children() for w in ([child] if child.winfo_class()=='TButton' else [])+buttons(child)]
    try:
        s=app.state_data=core.fresh('ivan');s['world']['time_mode']='paused';arrive(s,'site_04');guards.refresh(s)
        app.play_screen();app.update();campaign_ui.open_in_person(app);shot('desk')
        view=app.campaign_view
        b=next(w for w in buttons(view) if w.cget('text')=='Order a post status report');b.invoke();app.update()
        assert 'operational' in view.notice
        view.canvas.yview_moveto(.45);shot('commands')
        b=next(w for w in buttons(view) if str(w.cget('text')).startswith('Talk to selected'));b.invoke();app.update()
        g=s['groups'][s['active_group']];assert g.get('guard_session')
        assert 'At your command' in g['history'][-1]['text'];shot('conversation')
        import time
        import json
        name=g['local']
        provider=patch.object(core,'request',return_value={'message':{'content':json.dumps(dict(narration='',lines=[dict(speaker=name,text='The visitor area is beside reception.')]))}})
        provider.start()
        text=gd.TOPICS['Directions'];app.submit(text)
        deadline=time.monotonic()+8
        while app.busy and time.monotonic()<deadline:
            app.update();time.sleep(.02)
        provider.stop()
        assert not app.busy, 'Guard reply did not finish'
        assert 'visitor area' in g['history'][-1]['text'], g['history'][-1]
        app.geometry('1000x800');app.update();shot('conversation-compact')
        assert not any(gd.is_guard(k) for k in s.get('npc_chats',{}))
        assert not any(g.get('channel')=='text' and any(gd.is_guard(m) for m in g['members']) for g in s['groups'].values())
        groups.close_active(s,'Done');s['combat']['expelled']=['syndicate']
        campaign_ui.open_in_person(app);view.canvas.yview_moveto(.5)
        next(w for w in buttons(view) if w.cget('text')=='Order a post status report').invoke();shot('refusal')
        assert 'no command' in view.notice
        assert not errors,errors
        print('Guard desk, command status, in-person handoff, compact conversation, refusal and no-contact checks passed.')
    finally:app.sounds.close();app.destroy()
