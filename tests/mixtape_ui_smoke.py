"""Browse, search, edit and send with isolated state and real dark phone widgets."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import tkinter as tk
from tkinter import ttk
from unittest.mock import Mock
from PIL import ImageGrab
import game_core as core
import lifestyle_apps as apps
import mixtape_catalog as music
import phone_ui
import phone_theme
import winterfield_ui

root=tk.Tk(); root.withdraw(); winterfield_ui.install(root)
root.state_data=core.fresh('rei'); root.busy=False
for name in ('sounds','persist','render','update_phone_notification','show_in_person','open_calendar'):
    setattr(root,name,Mock())
errors=[]; root.report_callback_exception=lambda *args:errors.append(args)
phone=phone_ui.PhoneWindow(root)
shots=core.ROOT/'tests/screenshots'; shots.mkdir(exist_ok=True)
def view():
    root.update(); return phone.lifestyle_view
def shot(name):
    root.update(); ImageGrab.grab(window=phone.winfo_id()).save(shots/f'mixtape-{name}.png')
def go(page, **kwargs):
    view().go(page,**kwargs); return view()
def audit(widget):
    if isinstance(widget, ttk.Widget):
        style=ttk.Style(widget); name=str(widget.cget('style')) or widget.winfo_class()
        if isinstance(widget,ttk.Scrollbar) and name==widget.winfo_class(): name=str(widget.cget('orient')).title()+'.'+name
        for option in phone_theme.STYLE_OPTIONS:
            for state in phone_theme.STATES:
                assert not phone_theme.is_light_surface(widget,style.lookup(name,option,state)),(name,option,state)
    else:
        for option in phone_theme.SURFACE_OPTIONS:
            if option in widget.keys(): assert not phone_theme.is_light_surface(widget,widget.cget(option)),(widget,option)
    for child in widget.winfo_children(): audit(child)
try:
    phone.geometry('430x740'); phone.open_app('Mixtape')
    assert view().page=='home'; shot('home')
    v=go('search'); v.fields['query'].insert(0,'haneul'); v.search_results(); root.update()
    assert '1 artist' in v.results.winfo_children()[0].cget('text')
    shot('search')
    v.fields['query'].delete(0,'end'); v.fields['query'].insert(0,'zzzzz'); v.search_results()
    assert any('No matches' in str(w.cget('text')) for w in v.results.winfo_children() if isinstance(w,tk.Label))
    v.fields['query'].delete(0,'end'); v.fields['query'].insert(0,'Moonlight'); v.search_results()
    assert 'songs' in v.results.winfo_children()[0].cget('text')
    v=go('artist',artist_id='haneul'); v.add_song('haneul-01'); v.add_song('haneul-01')
    def artwork_widgets(widget):
        return ([widget] if hasattr(widget, 'artwork_path') else []) + [w for c in widget.winfo_children() for w in artwork_widgets(c)]
    art=artwork_widgets(v.body)
    assert any(w.artwork_path.endswith('haneul-portrait.png') for w in art)
    assert sum(w.artwork_path.endswith('haneul-cover.png') for w in art)==24
    assert len(v.draft['workspace']['entries'])==1; shot('artist')
    v.body.master.yview_moveto(.15); shot('song-artwork')
    phone.open_app('Home'); phone.open_app('Mixtape')
    assert len(view().draft['workspace']['entries'])==1
    v=go('editor'); v.fields['title'].insert(0,'Moonlight collection'); v.fields['memory'].insert('1.0','Under the stars')
    v.add_song('voss-01'); v.remove_song(1); v=view()
    assert v.fields['title'].get()=='Moonlight collection'
    shot('editor'); v.save(); v=view()
    assert v.page=='playlist' and not v.draft['workspace']['entries']
    item=apps.ensure(root.state_data)['playlists'][0]
    assert item['tracks']==['달빛 (Moonlight) — Haneul']; shot('playlist')
    v=go('send'); assert v.send_button.winfo_exists()
    combo=v.fields['recipient']; combo.tk.call('ttk::combobox::Post',str(combo)); root.update()
    popup=combo.tk.call('ttk::combobox::PopdownWindow',str(combo))
    for option in ('background','selectbackground'):
        assert not phone_theme.is_light_surface(combo,combo.tk.call(str(popup)+'.f.l','cget','-'+option))
    combo.tk.call('ttk::combobox::Unpost',str(combo)); shot('send')
    v.send(); v=view()
    assert len(apps.ensure(root.state_data)['shares'])==1 and v.page=='playlist'
    v.begin_edit(); v=view(); v.add_song('voss-01'); v.save(); v=view()
    assert len(item['tracks'])==2 and len(apps.ensure(root.state_data)['playlists'])==1
    assert len(apps.ensure(root.state_data)['shares'][0]['content']['tracks'])==1
    v.add_song('voss-02'); v.begin_edit()
    assert v.draft['workspace']['entries'][0]['id']=='voss-02'
    v.draft['workspace']['entries']=[dict(id=i,label=music.track_label(i)) for i in list(music.SONGS)[:30]]
    v.add_song('haneul-01'); assert len(v.draft['workspace']['entries'])==30
    v.draft['workspace']['entries']=[]
    phone.geometry('560x780'); v=go('library'); shot('library')
    for page in ('home','search','library','artist','editor','playlist','send'):
        go(page)
        audit(phone)
        assert all(b.winfo_ismapped() for b in view().nav_buttons.values())
    assert not errors,errors
finally:
    phone.destroy(); root.destroy()
print('Mixtape Home/Search/Library, artist profiles, empty search, draft persistence, duplicate/limit checks, editing, private send snapshots, dark recipient popup and resize passed.')
