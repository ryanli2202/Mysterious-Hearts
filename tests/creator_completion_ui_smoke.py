"""Offline interactive creator checks, with isolated drafts/profiles and mocked AI."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import tempfile
import time
import tkinter as tk
from tkinter import ttk
from unittest.mock import patch
from PIL import Image,ImageGrab
import game,game_core as core
import custom_creator_ui,creator_tools_ui,creator_combat_ui,creator_origin_ui
from test_creator_completion import armed

def children(w):
    for c in w.winfo_children():
        yield c
        yield from children(c)

def button(w,label): return next(c for c in children(w) if isinstance(c,ttk.Button) and c.cget('text')==label)
out=core.ROOT/'tests'/'screenshots'; out.mkdir(exist_ok=True)

with tempfile.TemporaryDirectory(dir=core.ROOT/'assets'/'generated') as folder:
    root=Path(folder); portrait=root/'p.png'; picture=Image.new('RGBA',(32,64),(0,0,0,0)); picture.putpixel((16,32),(10,120,100,255)); picture.save(portrait)
    errors=[]
    with patch.object(core,'SAVE',root/'saves'/'story.json'),patch.object(game.Game,'check'),patch.object(game.Game,'begin_incoming'),patch.object(core,'save'),patch.object(core,'request',side_effect=AssertionError('Unexpected AI')):
        app=game.Game(); app.report_callback_exception=lambda *args:errors.append(args); app.update()
        creator=custom_creator_ui.CharacterCreator(app); snap=creator.snapshot(); p=armed()
        snap['values'].update({k:', '.join(p[k]) if isinstance(p[k],list) else str(p[k]) for k in snap['values'] if k in p})
        snap.update(appearance=p['appearance'],awakened=True,awakening_description=p['awakening_description'],origin=p['origin'],
                    trait_amplifications=p['trait_amplifications'],trait_signature=[p['awakening_trait'],p['awakening_description']],trait_reviewed=True,
                    portrait=portrait.relative_to(core.ROOT).as_posix(),generated_signature=[str(p[k]) for k in ('gender','age','height','hairstyle')]+[p['appearance']])
        creator.restore_snapshot(snap); app.update()
        tools=creator_tools_ui.open_tools(creator); app.update()
        tabs=next(c for c in children(tools) if isinstance(c,ttk.Notebook))
        for i in range(len(tabs.tabs())):
            tabs.select(i); app.update(); ImageGrab.grab(window=tools.winfo_id()).save(out/f'mh002-tools-{i}.png')
        tabs.select(0)
        # Failure leaves fields intact and no callback tries to use a destroyed window.
        with patch('creator_writing.propose',side_effect=RuntimeError('Provider offline')):
            button(tools,'Request / retry').invoke()
            for _ in range(8): app.update(); time.sleep(.04)
        assert 'Provider offline' in '\n'.join(str(c.cget('text')) for c in children(tools) if isinstance(c,ttk.Label))
        button(tools,'Discard / cancel').invoke()
        combos=[c for c in children(tabs.nametowidget(tabs.tabs()[0])) if isinstance(c,ttk.Combobox)]
        combos[0].set('biography')
        creator.extra_text['biography'].insert('1.0','Born in Brisbane.')
        texts=[c for c in children(tabs.nametowidget(tabs.tabs()[0])) if isinstance(c,tk.Text)]
        texts[2].insert('1.0','biography | Exact | Born in Brisbane.')
        button(tools,'Save locks').invoke()
        def delayed(*args):
            time.sleep(1.5)
            return 'Born in Brisbane. An observant artist.'
        with patch('creator_writing.propose',side_effect=delayed):
            button(tools,'Request / retry').invoke()
            for _ in range(48): app.update(); time.sleep(.04)
        check=next(c for c in children(tabs.nametowidget(tabs.tabs()[0])) if isinstance(c,ttk.Checkbutton))
        check.invoke(); button(tools,'Apply').invoke(); app.update()
        assert 'observant artist' in creator.extra_text['biography'].get('1.0','end')
        creator.undo_edit(); app.update(); assert creator.extra_text['biography'].get('1.0','end').strip()=='Born in Brisbane.'
        for scale in (1.25,1.75):
            app.tk.call('tk','scaling',scale); tools.geometry('780x650'); app.update()
            for i in range(len(tabs.tabs())):
                tabs.select(i); app.update()
                page=tabs.nametowidget(tabs.tabs()[i])
                for widget in children(page):
                    if isinstance(widget,ttk.Button): widget.focus_force(); app.update()
            ImageGrab.grab(window=tools.winfo_id()).save(out/f'mh002-tools-scaled-{scale}.png')
        app.tk.call('tk','scaling',1.333333); tools.destroy()
        combat=creator_combat_ui.open_review(creator); app.update()
        tabs=next(c for c in children(combat) if isinstance(c,ttk.Notebook))
        for i in range(len(tabs.tabs())):
            tabs.select(i); app.update(); ImageGrab.grab(window=combat.winfo_id()).save(out/f'mh002-combat-tools-{i}.png')
        amp=creator.trait_amplifications[0]['id']
        candidates=[dict(name='Echo '+str(i),description='A finite contact strike.',role='attack',tags=['precision'],aspects=[amp],range=1,stamina=9+i,mana=12,hits=1,environment='Contact only',setup='None',counter='Guard',counter_kind='none') for i in range(3)]
        with patch('combat.ask_ai',return_value={'skills':candidates}):
            button(combat,'Generate three candidates').invoke()
            for _ in range(10): app.update(); time.sleep(.04)
        listing=next(c for c in children(combat) if isinstance(c,tk.Listbox))
        assert listing.size()==3
        listing.selection_set(0); listing.event_generate('<<ListboxSelect>>'); app.update()
        ImageGrab.grab(window=combat.winfo_id()).save(out/'mh002-origin-signature-review.png')
        button(combat,'Accept selected').invoke(); app.update(); assert creator.starting_signature
        practice=creator_combat_ui.open_practice(creator); app.update(); button(practice,'Execute training exchange').invoke(); app.update()
        ImageGrab.grab(window=practice.winfo_id()).save(out/'mh002-in-person-practice.png'); practice.destroy(); combat.destroy()
        picker=creator_origin_ui.open_picker(creator); picker.geometry('780x650'); app.update()
        ImageGrab.grab(window=picker.winfo_id()).save(out/'mh002-complete-picker-compact.png'); picker.destroy()
        creator.geometry('780x650'); creator.show_step('Review'); app.update()
        ImageGrab.grab(window=creator.winfo_id()).save(out/'mh002-complete-creator-compact.png')
        creator._close()
        app.start_custom(p,portrait.relative_to(core.ROOT).as_posix()); app.update()
        s=app.state_data; s['world']['location']='park'; s['world']['cast'][s['player']].update(location='park',journey=None)
        import trait_activities
        activity=trait_activities.open_in_person(app); app.update()
        button(activity,'Survey public surroundings').invoke(); app.update()
        ImageGrab.grab(window=activity.winfo_id()).save(out/'mh002-in-person-trait-applications.png')
        activity.destroy(); app.destroy()
        assert not errors,errors
print('Creator writing/identity/package tabs, provider failure, Trait tabs, actual in-person practice and compact picker rendered successfully.')
