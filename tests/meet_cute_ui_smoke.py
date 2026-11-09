"""Real Tk screens and asynchronous replies; no live dialogue calls or player saves."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import time
import tkinter as tk
from unittest.mock import Mock, patch
from PIL import ImageGrab
import game_core as core
import hidden_cast
import meet_cute as mc
import phone_numbers
from meet_cute_ai import ReplyPump
from phone_ui import PhoneWindow
import winterfield_ui


def drain(root,pump,predicate):
    until=time.monotonic()+4
    while time.monotonic()<until:
        root.update(); pump.tick()
        if predicate():return
        time.sleep(.02)
    raise AssertionError('Reply worker did not settle')


def main():
    root=tk.Tk();root.withdraw();winterfield_ui.install(root)
    root.state_data=core.fresh('rei')
    root.state_data['world']['minute']=3*1440+10*60
    root.in_game=True;root.busy=False
    import game
    root.photos={}
    root.portrait=lambda who,size,**kw:game.Game.portrait(root,who,size,**kw)
    for name in ('persist','render','sounds','update_phone_notification','show_in_person','open_calendar'):
        setattr(root,name,Mock())
    errors=[]
    root.report_callback_exception=lambda *args:errors.append(args)
    phone=PhoneWindow(root,'Meet-Cute');phone.geometry('430x740');root.update()
    view=phone.meet_cute_view
    for key in view.interest_keys:
        field=view.fields[key]
        assert str(field.cget('state'))=='readonly'
        assert set(field['values'])=={'',*mc.INTERESTS['rei']}
    view.fields['Bio'].insert('1.0','Drawing, cooking, and a quiet evening.')
    view.fields['Interest 1'].set('Drawing')
    # Visual photo picker stays in the phone and feeds the editable preview.
    windows=set(root.tk.call('winfo','children','.'))
    view.pick_photo(1);root.update()
    assert set(root.tk.call('winfo','children','.'))==windows
    picker=view.photo_picker
    screenshots=core.ROOT/'tests'/'screenshots';screenshots.mkdir(exist_ok=True)
    ImageGrab.grab(window=phone.winfo_id()).save(screenshots/'meet-cute-picker.png')
    def descendants(widget):
        for child in widget.winfo_children():
            yield child
            yield from descendants(child)
    from tkinter import ttk
    grove_choice=next(w for w in descendants(picker) if isinstance(w,ttk.Button) and w.cget('text').startswith('Grove ·'))
    grove_choice.invoke();root.update()
    assert view.photo_choices[view.get('Photo 2')].startswith('grove:')
    view.profile_mode(True);root.update()
    assert view.preview.winfo_ismapped() and not view.editor.winfo_ismapped()
    ImageGrab.grab(window=phone.winfo_id()).save(screenshots/'meet-cute-preview.png')
    view.profile_mode(False);root.update()
    assert view.get('Bio')=='Drawing, cooking, and a quiet evening.'
    combo=view.fields['Interest 1'];before=combo.get()
    view.scroller.canvas.yview_moveto(0)
    combo.event_generate('<MouseWheel>',delta=-120);root.update()
    assert combo.get()==before and view.scroller.canvas.yview()[0]>0
    scroll_before=view.scroller.canvas.yview()[0]
    view.go('Profile');root.update();view=phone.meet_cute_view
    assert abs(view.scroller.canvas.yview()[0]-scroll_before)<.03
    view.save_profile();root.update()
    assert mc.ensure(root.state_data)['profile']['interests']==['Drawing']
    for tab in ('Preferences','Discover','Likes','Matches','Profile'):
        phone.meet_cute_view.go(tab);root.update()
        assert phone.meet_cute_view.body.winfo_ismapped()
    phone.meet_cute_view.fields['Bio'].insert('end',' A saved draft.')
    phone.open_app('Home');phone.open_app('Meet-Cute');root.update()
    assert 'saved draft' in phone.meet_cute_view.get('Bio')
    s=root.state_data
    mc.preferences(s,24,24,'Women','Open to either','Preferred')
    phone.meet_cute_view.go('Discover');root.update()
    view=phone.meet_cute_view
    target='Like on Lena Ortiz'; message='Message to Lena Ortiz'
    ImageGrab.grab(window=phone.winfo_id()).save(screenshots/'meet-cute-discover.png')
    from meet_cute_ui import ProfilePhotos
    carousel=next(w for w in view.body.winfo_children() if isinstance(w,ProfilePhotos))
    assert len(carousel.paths)>=2
    start=carousel.index
    carousel.next.invoke();root.update()
    assert carousel.index==(start+1)%len(carousel.paths)
    carousel.previous.invoke();root.update()
    assert carousel.index==start
    carousel.picture.event_generate('<ButtonPress-1>',rootx=220,rooty=100)
    carousel.picture.event_generate('<ButtonRelease-1>',rootx=100,rooty=105)
    root.update()
    assert carousel.index==(start+1)%len(carousel.paths)
    carousel.picture.event_generate('<ButtonPress-1>',rootx=100,rooty=100)
    carousel.picture.event_generate('<ButtonRelease-1>',rootx=220,rooty=105)
    root.update()
    assert carousel.index==start
    carousel.picture.event_generate('<ButtonPress-1>',rootx=100,rooty=100)
    carousel.picture.event_generate('<ButtonRelease-1>',rootx=110,rooty=220)
    root.update()
    assert carousel.index==start
    carousel.move(-start-1);root.update()
    assert carousel.index==len(carousel.paths)-1
    carousel.next.invoke();root.update()
    assert carousel.index==0
    carousel.next.invoke();root.update()
    view.go('Discover');root.update()
    view=phone.meet_cute_view
    restored=next(w for w in view.body.winfo_children() if isinstance(w,ProfilePhotos))
    assert restored.index==1
    assert sum(isinstance(w,ProfilePhotos) for w in view.body.winfo_children())==1
    view.select_like('lena','Ask me about');root.update()
    assert view.get(target)=='Ask me about'
    assert view.scroller.canvas.yview()[0]>0
    view.fields[target].set('Ask me about')
    view.fields[message].insert('1.0','Your film photography sounds fascinating. What is your favourite thing to photograph?')
    view.do(mc.like,'lena',view.get(target),view.get(message))
    s['world']['minute']+=200;mc.tick(s)
    assert 'lena' in mc.ensure(s)['matches']
    assert not hidden_cast.contact(s,'lena')
    phone.meet_cute_view.go('Chat','lena');root.update()
    phone.meet_cute_view.go('Character','lena');root.update()
    assert any(isinstance(w,ProfilePhotos) for w in phone.meet_cute_view.body.winfo_children())
    phone.meet_cute_view.go('Chat','lena');root.update()
    view=phone.meet_cute_view
    view.fields['Your message'].insert('1.0','What sort of photographs do you enjoy taking?')
    view.do(mc.send,'lena',view.get('Your message'),clear=('Your message',))
    assert phone.meet_cute_view.get('Your message')==''
    m=mc.match(s,'lena');s['world']['minute']=m['pending']['due']
    pump=ReplyPump(root)
    with patch.object(mc,'generate',return_value='Street corners with something unexpected in them.'):
        drain(root,pump,lambda:m['pending'] is None)
    phone.refresh();root.update()
    assert m['messages'][-1]['author']=='them'
    assert not hidden_cast.contact(s,'lena')
    screenshots=core.ROOT/'tests'/'screenshots';screenshots.mkdir(exist_ok=True)
    ImageGrab.grab(window=phone.winfo_id()).save(screenshots/'meet-cute-chat.png')
    mc.send(s,'lena','And what camera do you use?');s['world']['minute']=m['pending']['due']
    with patch.object(mc,'generate',side_effect=RuntimeError('Offline')):
        drain(root,pump,lambda:bool(m['pending']['error']))
    mc.retry(s,'lena')
    with patch.object(mc,'generate',return_value='A film camera I know well.'):
        drain(root,pump,lambda:m['pending'] is None)
    # Errors, confirmations, number exchange and Contacts stay in this phone.
    windows=set(root.tk.call('winfo','children','.'))
    phone.refresh();root.update()
    view=phone.meet_cute_view
    view.do(mc.send,'lena','')
    assert view.status.cget('text')
    assert set(root.tk.call('winfo','children','.'))==windows
    view.end_match('lena',False)
    assert view.confirmation.winfo_exists() and m['status']=='active'
    assert set(root.tk.call('winfo','children','.'))==windows
    view.confirmation.destroy()
    view.do(mc.request_numbers,'lena')
    s['world']['minute']+=100;mc.tick(s);phone.refresh();root.update()
    assert phone_numbers.saved_number(s,'lena') in m['messages'][-1]['text']
    phone.meet_cute_view.view_contact('lena');root.update()
    assert phone.selected=='Contacts'
    assert any(isinstance(w,ttk.Label) and w.cget('text')=='Sexuality · Straight' for w in descendants(phone.screen))
    ImageGrab.grab(window=phone.winfo_id()).save(screenshots/'contact-sexuality.png')
    assert set(root.tk.call('winfo','children','.'))==windows
    phone.open_app('Contacts');root.update()
    phone.contact_number_entry.insert(0,'not a number');phone.add_number_action()
    assert phone.contact_number_status.cget('text')
    assert set(root.tk.call('winfo','children','.'))==windows
    phone.contact_number_entry.delete(0,'end')
    phone.contact_number_entry.insert(0,phone_numbers.number(s,'naomi'));phone.add_number_action();root.update()
    assert hidden_cast.contact(s,'naomi') and not hidden_cast.ensure(s)['naomi']['met']
    assert set(root.tk.call('winfo','children','.'))==windows
    phone.open_app('Meet-Cute')
    phone.meet_cute_view.go('Profile');root.update()
    ImageGrab.grab(window=phone.winfo_id()).save(screenshots/'meet-cute-profile.png')
    mc.preferences(s,18,40,'Everyone','Open to either','Preferred')
    phone.meet_cute_view.go('Discover');root.update()
    view=phone.meet_cute_view
    first=view.discovery_who
    view.scroller.canvas.yview_moveto(.5);root.update()
    view.do(mc.skip,first);root.update()
    view=phone.meet_cute_view
    assert view.discovery_who!=first and view.scroller.canvas.yview()[0]==0
    for width in (380,520):
        phone.geometry(f'{width}x740');root.update()
        assert view.dock.winfo_ismapped()
        assert view.body.winfo_width()<=phone.winfo_width()
        assert view.scroller.canvas.winfo_height()>200
    for player in ('garrett','minsu','ivan'):
        phone.destroy()
        root.state_data=core.fresh(player)
        phone=PhoneWindow(root,'Meet-Cute');root.update()
        view=phone.meet_cute_view
        assert set(view.fields['Interest 1']['values'])=={'',*mc.INTERESTS[player]}
    from profile_ui import ProfileWindow
    profile=ProfileWindow(root,'ivan');root.update()
    assert profile.values['Sexuality'].cget('text')=='Bisexual'
    ImageGrab.grab(window=profile.winfo_id()).save(screenshots/'character-sexuality.png')
    profile.destroy()
    assert not errors,errors
    phone.destroy();root.destroy()
    print('Meet-Cute tabs, canon dropdowns for all protagonists, hidden match, drafts, chat, failure and retry passed.')


if __name__=='__main__':main()
