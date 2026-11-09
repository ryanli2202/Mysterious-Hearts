"""Real Tk checks with no network requests or player-save writes."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from unittest.mock import patch
from PIL import ImageGrab
import game
import game_core as core
import phone_personalization as p
from phone_ui import PhoneWindow

with patch.object(game.Game, 'check', lambda self: None), \
     patch.object(game.Game, 'persist', lambda self: None), \
     patch.object(game.Game, 'poll', lambda self: None), \
     patch.object(game.Game, 'poll_grove', lambda self: None), \
     patch.object(game.Game, 'begin_incoming', lambda self: None), \
     patch.object(p, '_preferences', dict(p.DEFAULTS)):
    app=game.Game()
    errors=[]
    app.report_callback_exception=lambda *args: errors.append(args)
    app.state_data=core.fresh('rei'); app.play_screen(); app.update()
    phone=PhoneWindow(app); app.phone_activity=phone; app.update()
    folder=core.ROOT/'tests'/'screenshots'; folder.mkdir(exist_ok=True)
    assert phone.winfo_width()*16 == phone.winfo_height()*9
    assert phone.home_page_count>1
    from phone_icons import COLORS
    visible=set()
    for n in range(phone.home_page_count):
        phone.change_home_page(page=n); app.update(); visible.update(phone.visible_home_apps)
    assert visible==set(COLORS)
    phone.change_home_page(page=0); app.update()
    assert not phone.home_canvas.cget('scrollregion')
    first=phone.visible_home_apps[:]
    phone.change_home_page(1); app.update()
    assert phone.visible_home_apps!=first
    assert all(name in phone.visible_home_apps for name in ('Messages','Contacts','Camera'))
    phone.open_app('Settings'); phone.open_app('Home'); app.update()
    assert p.ensure(app.state_data)['home_page']==1
    phone.change_home_page(page=0); app.update()
    phone.home_canvas.event_generate('<ButtonPress-1>',x=220,y=200)
    phone.home_canvas.event_generate('<ButtonRelease-1>',x=100,y=200)
    app.update(); assert p.ensure(app.state_data)['home_page']==1
    phone.change_home_page(page=0); app.update()
    ImageGrab.grab(window=phone.winfo_id()).save(folder/'personal-phone-home.png')
    for page in ('Contacts','Settings','Customise','Pinned messages','Notes','Lock','Gallery','Keepsake','Messages'):
        phone.open_app(page); app.update()
        if page in ('Contacts','Customise','Pinned messages','Lock'):
            ImageGrab.grab(window=phone.winfo_id()).save(folder/f'personal-{page.lower().replace(" ","-")}.png')
        if page=='Notes': phone.notes_editor.insert('end','My test theory')
    assert p.ensure(app.state_data)['notes']=='My test theory'
    phone.open_thread('emily'); app.update()
    assert phone.phone_messages.winfo_height()>100, phone.phone_messages.winfo_height()
    assert phone.message_entry.winfo_ismapped()
    from phone_chat import message_menu, toggle_pin, toggle_options
    from types import SimpleNamespace
    ids=phone.phone_messages.message_ids
    first_pin=next(ident for ident in ids if ident)
    index=ids.index(first_pin)
    message_menu(phone,index,SimpleNamespace(x_root=phone.winfo_rootx()+70,y_root=phone.winfo_rooty()+220))
    assert phone.message_context_menu.entrycget(0,'label')=='Unpin message'
    phone.message_context_menu.unpost(); phone.message_context_menu.invoke(0)
    assert first_pin not in p.ensure(app.state_data)['pins']
    toggle_pin(phone,first_pin)
    assert first_pin in phone.phone_messages.pinned_ids
    import json
    app.state_data['routes']['emily']['history'].append(dict(role='assistant',channel='text',minute=500,content=json.dumps({'dialogue':'A new pinnable message.'})))
    phone.update_messages(); app.update()
    last_pin=phone.phone_messages.message_ids[-1]
    assert last_pin and last_pin!=first_pin
    with patch('phone_chat.messagebox.showinfo') as notice:
        toggle_pin(phone,last_pin); notice.assert_called_once()
    assert len(p.ensure(app.state_data)['pins'])==3
    toggle_pin(phone,first_pin); toggle_pin(phone,last_pin)
    assert last_pin in phone.phone_messages.pinned_ids
    toggle_options(phone,True); app.update()
    assert phone.chat_options.winfo_ismapped() and phone.message_entry.winfo_ismapped()
    toggle_options(phone,False); app.update()
    app.pending='Uncommitted test draft'
    phone.update_messages()
    assert phone.phone_messages.message_ids[-1] is None
    app.pending=None; phone.update_messages()
    ImageGrab.grab(window=phone.winfo_id()).save(folder/'personal-conversation.png')
    phone.message_entry.insert(0,'Saved draft'); phone.open_app('Home'); phone.open_thread('emily'); app.update()
    assert phone.message_entry.get()=='Saved draft'
    with patch.object(app, 'submit') as submit, patch('phone_ui.messagebox.askyesno', return_value=False):
        p.preferences()['confirm_send']=True
        phone.send_message(); submit.assert_not_called()
    import groups
    gid=groups.create_text(app.state_data,'Pin test',['amy','sophie'])
    app.state_data['groups'][gid]['history']=[dict(speaker='Amy Hansen',text='Group message to pin',minute=510)]
    phone.open_thread(gid,True); app.update()
    group_id=next(ident for ident in phone.phone_messages.message_ids if ident)
    p.unpin(app.state_data,p.ensure(app.state_data)['pins'][0]); toggle_pin(phone,group_id)
    assert group_id in phone.phone_messages.pinned_ids
    phone.open_thread('emily'); app.update()
    phone.back(); assert phone.selected=='Messages'
    phone.open_app('Contacts'); phone.contact_detail('emily'); phone.back(); assert phone.selected=='Contacts'
    p.preferences()['device']='Tablet'; phone.apply_device_size(); app.update()
    assert phone.winfo_width()*4==phone.winfo_height()*3
    p.preferences()['text_size']=20
    phone.open_thread('emily'); app.update()
    ImageGrab.grab(window=phone.winfo_id()).save(folder/'personal-tablet-conversation.png')
    p.preferences().update(device='Phone',scale=60)
    phone.apply_device_size(); phone.open_thread('emily'); app.update()
    assert phone.winfo_width()*16==phone.winfo_height()*9
    assert phone.phone_messages.winfo_height()>=190, (phone.winfo_height(),phone.phone_messages.winfo_height(),phone.phone_messages.master.winfo_height())
    # The composer remains fixed within the device; only message history scrolls.
    assert phone.message_composer.winfo_rooty()+phone.message_composer.winfo_height()<=phone.winfo_rooty()+phone.winfo_height()
    app.update()
    ImageGrab.grab(window=phone.winfo_id()).save(folder/'personal-small-conversation.png')
    for player in core.PLAYERS:
        app.state_data=core.fresh(player)
        phone.open_app('Home'); app.update()
    phone.destroy(); app.sounds.close(); app.destroy()
    assert not errors, errors
print('Phone personalization UI passed: portrait/tablet, screens, drafts, notes, confirmation, back navigation, all protagonists.')
