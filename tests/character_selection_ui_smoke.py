"""MH-002 offline roster/draft/picker checks; all writes use a temporary root."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import tempfile
import shutil
import tkinter as tk
from tkinter import ttk
from unittest.mock import patch
from PIL import ImageGrab
import game
import game_core as core
import custom_library
import custom_creator_ui
import creator_origin_ui
import phone_theme
from test_custom_protagonist import PROFILE

out=core.ROOT/'tests'/'screenshots'; out.mkdir(exist_ok=True)
def children(w):
    for child in w.winfo_children():
        yield child
        yield from children(child)
def button(w,title):
    return next(c for c in children(w) if isinstance(c,(tk.Button,ttk.Button)) and c.cget('text')==title)
def capture(w,name):
    w.update(); ImageGrab.grab(window=w.winfo_id()).save(out/name)

with tempfile.TemporaryDirectory(dir=core.ROOT/'assets'/'generated') as folder:
    folder=Path(folder); portrait=folder/'portrait.png'
    shutil.copyfile(core.ROOT/'assets'/'portraits'/'rei-selection.png',portrait)
    raw=PROFILE|dict(portrait=portrait.relative_to(core.ROOT).as_posix(), biography='An artist with a long public history. '*30, private_history='Only the creator may see this.')
    save=folder/'saves'/'story.json'
    a=custom_library.save_profile(raw,save.parent,separate=True)
    b=custom_library.save_profile(raw,save.parent,separate=True)
    with patch.object(core,'SAVE',save), patch.object(game.Game,'check'), patch.object(game.Game,'begin_incoming'), patch.object(core,'save'), patch.object(core,'request',side_effect=AssertionError('unexpected AI')):
        app=game.Game(); errors=[]; app.report_callback_exception=lambda *e:errors.append(e)
        app.update(); screen=app.start_screen
        assert len(screen.custom_profiles)==2
        with patch.object(app,'start_custom') as start:
            screen.filter.set('My Characters'); screen.select(b['profile_id']); app.update()
            assert not start.called
            screen.show_dossier('Backstory'); app.update()
            assert 'Only the creator' in screen.dossier_text.get('1.0','end')
            capture(app,'mh002-custom-roster.png')
            screen.begin.invoke(); assert start.call_args.args[0]['profile_id']==b['profile_id']
        screen.search.set('no such person'); app.update()
        assert str(screen.begin['state'])=='disabled'
        capture(app,'mh002-empty-roster.png')
        screen.search.set(''); screen.filter.set('All'); screen.select('emily'); screen.show_dossier('Awakened')
        capture(app,'mh002-emily-awakened.png')
        for who in core.PLAYERS:
            screen.select(who); screen.show_dossier('Backstory'); app.update()
            assert len(screen.dossier_text.get('1.0','end').strip().split('\n\n'))==2,who
            screen.show_dossier('Details'); app.update()
            assert 'MBTI' in screen.dossier_text.get('1.0','end'),who
        screen.select('ivan'); screen.show_dossier('Details')
        capture(app,'mh002-ivan-details.png')
        screen.select('garrett'); screen.show_dossier('Backstory')
        capture(app,'mh002-garrett-biography.png')
        app.geometry('1000x740'); app.update()
        screen.select('rei'); screen.show_dossier('Backstory')
        screen.dossier_text.yview_moveto(1)
        capture(app,'mh002-rei-biography-compact.png')
        app.geometry('1440x900'); app.update()
        creator=custom_creator_ui.CharacterCreator(app,on_saved=screen.profile_saved)
        for k,v in PROFILE.items():
            if k in creator.values: creator.values[k].set(', '.join(v) if isinstance(v,list) else v)
        creator.appearance.insert('1.0',PROFILE['appearance'])
        creator.extra_text['biography'].insert('1.0','An artist moving to Winterfield.')
        creator.portrait=raw['portrait']; creator.generated_signature=creator.signature()
        creator.changed(); creator.save_draft(); assert creator.draft['current']['values']['name']==PROFILE['name']
        from creator_steps_ui import STEPS
        before=creator.collect()
        for step in STEPS:
            creator.show_step(step); app.update()
            assert creator.collect()==before,step
            assert creator.step_choice.get()==step
        assert 'Ready: character fields' in creator.checklist.get('1.0','end')
        creator.geometry('780x650'); creator.show_step('Review'); app.update()
        creator.preview_tabs.select(1); app.update()
        capture(creator,'mh002-staged-review-compact.png')
        creator.show_step('Backstory'); creator.save_draft()
        snap=creator.snapshot(); creator.show_step('Combat'); creator.restore_snapshot(snap)
        assert creator.creator_step=='Backstory'
        capture(creator,'mh002-staged-backstory.png')
        creator.extra_text['motivation'].insert('end','A recoverable goal.')
        import creator_drafts
        creator.draft=creator_drafts.autosave(creator.draft_root,creator.draft,creator.snapshot())
        creator.draft_browser(); app.update()
        browser=next(w for w in creator.winfo_children() if isinstance(w,tk.Toplevel))
        capture(browser,'mh002-recovery-preview.png'); browser.destroy()
        picker=creator_origin_ui.open_picker(creator); app.update()
        for widget in children(picker):
            if isinstance(widget,ttk.Combobox):
                popup=widget.tk.call('ttk::combobox::PopdownWindow',str(widget))
                assert not phone_theme.is_light_surface(widget,widget.tk.call(str(popup)+'.f.l','cget','-background'))
                values=widget.cget('values')
                if 'Exceptional Veteran' in values: widget.set('Veteran')
                if 'Florist' in values: widget.set('Florist')
                if 'Faction specialist' in values: widget.set('Faction specialist')
        button(picker,'Use recommended kit').invoke(); app.update()
        capture(picker,'mh002-origin-picker.png')
        button(picker,'Apply starting choices').invoke(); app.update()
        assert creator.origin['experience']=='Veteran'; assert creator.origin['job']=='florist'
        creator.save_draft(); creator.history_browser(); app.update()
        history=next(w for w in creator.winfo_children() if isinstance(w,tk.Toplevel))
        button(history,'Pin / unpin selected revision').invoke(); app.update()
        assert any(r.get('pinned') for r in creator.draft['revisions'])
        capture(history,'mh002-draft-history.png'); history.destroy()
        creator.review_character(); app.update()
        review=next(w for w in creator.winfo_children() if isinstance(w,tk.Toplevel))
        capture(review,'mh002-review.png'); review.destroy()
        creator.save_character(); app.update()
        assert len(screen.custom_profiles)==3 and app.state_data is None
        screen.select(a['profile_id']); screen.edit_selected(); app.update()
        editor=next(w for w in app.winfo_children() if isinstance(w,custom_creator_ui.CharacterCreator))
        assert editor.edit_profile_id==a['profile_id'] and editor.generated_signature==editor.signature()
        editor.extra_text['biography'].delete('1.0','end'); editor.extra_text['biography'].insert('end','A revised public history.')
        editor.show_step('Review'); capture(editor,'mh002-profile-edit-review.png')
        editor.save_character(); app.update()
        assert len(screen.custom_profiles)==3 and screen.selected==a['profile_id']
        assert screen.custom_profiles[a['profile_id']]['biography']=='A revised public history.'
        assert screen.custom_profiles[b['profile_id']]['biography']==b['biography']
        screen.edit_selected(); app.update()
        editor=next(w for w in app.winfo_children() if isinstance(w,custom_creator_ui.CharacterCreator))
        custom_library.save_profile(screen.custom_profiles[a['profile_id']]|{'biography':'Newer external edit.'},save.parent)
        editor.save_character(); app.update()
        assert editor.winfo_exists() and 'changed or was removed' in editor.status['text']
        editor.save_character(as_copy=True); app.update()
        assert len(screen.custom_profiles)==4
        assert screen.custom_profiles[a['profile_id']]['biography']=='Newer external edit.'
        screen.select('martos'); screen.show_dossier('Details'); capture(app,'mh002-ace-details.png')
        assert not errors,errors
        app.sounds.close(); app.destroy()
print('MH-002 UI: duplicate profiles, filters, preview isolation, draft/history, picker and Save character passed.')
