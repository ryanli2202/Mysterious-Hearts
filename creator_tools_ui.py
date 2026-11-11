"""Explicit writing, identity and package actions on independent draft snapshots."""
import copy
from pathlib import Path
import queue
import threading
import tkinter as tk
from tkinter import ttk
import creator_writing as writing
import creator_drafts as drafts
import phone_theme
import winterfield_ui as ui


def text(parent, height=6):
    frame=ttk.Frame(parent); frame.pack(fill='both',expand=True,pady=5)
    scroll=ttk.Scrollbar(frame); scroll.pack(side='right',fill='y')
    widget=tk.Text(frame,height=height,wrap='word',bg=ui.CARD,fg=ui.CREAM,insertbackground=ui.CREAM,
                   selectbackground=ui.EDGE,relief='flat',font=('Segoe UI',10),yscrollcommand=scroll.set)
    widget.pack(fill='both',expand=True); scroll.configure(command=widget.yview)
    return widget


def replace(widget,value):
    widget.delete('1.0','end'); widget.insert('1.0',value)


def commit(creator,snapshot,label):
    if creator.cancel_event: raise ValueError('Finish or cancel portrait/Trait generation first.')
    before=creator.snapshot()
    creator.draft=drafts.save(creator.draft_root,creator.draft,before,label)
    creator.undo_stack.record(before)
    if not creator.restore_snapshot(snapshot): raise ValueError('Finish or cancel portrait/Trait generation first.')
    creator.draft=drafts.autosave(creator.draft_root,creator.draft,creator.snapshot())


def scroll_page(tabs,name):
    shell=ttk.Frame(tabs); tabs.add(shell,text=name)
    scroll=ttk.Scrollbar(shell); scroll.pack(side='right',fill='y')
    canvas=tk.Canvas(shell,bg=ui.PANEL,highlightthickness=0,yscrollcommand=scroll.set)
    canvas.pack(fill='both',expand=True); scroll.configure(command=canvas.yview)
    body=ttk.Frame(canvas,padding=10); item=canvas.create_window(0,0,window=body,anchor='nw')
    def layout(event=None):
        canvas.itemconfigure(item,width=canvas.winfo_width())
        canvas.configure(scrollregion=canvas.bbox('all'))
        for widget in body.winfo_children():
            if isinstance(widget,ttk.Label): widget.configure(wraplength=max(180,canvas.winfo_width()-30))
    canvas.bind('<Configure>',layout); body.bind('<Configure>',layout)
    def focus(event):
        widget=event.widget
        if not str(widget).startswith(str(body)): return
        canvas.update_idletasks()
        y=widget.winfo_rooty()-body.winfo_rooty()
        top=canvas.canvasy(0); height=canvas.winfo_height()
        if y<top or y+widget.winfo_height()>top+height:
            canvas.yview_moveto(max(0,y-15)/max(1,body.winfo_height()))
    shell.winfo_toplevel().bind('<FocusIn>',focus,add='+')
    return body


def open_tools(creator):
    window=creator.workspace_window('Writing, ideas, identity & portable characters')
    window.geometry('880x760')
    tabs=ttk.Notebook(window); tabs.pack(fill='both',expand=True,padx=12,pady=12)
    status=ttk.Label(window,text='All changes affect this draft only.',wraplength=820); status.pack(fill='x',padx=12,pady=8)
    def safe(action):
        try: action()
        except (ValueError,OSError,KeyError) as exc: status.configure(text=str(exc))
    def page(name):
        return scroll_page(tabs,name)
    def button(parent,label,action):
        ttk.Button(parent,text=label,command=lambda:safe(action)).pack(side='left',padx=3,pady=4)
    def combo(parent,values):
        var=tk.StringVar(value=values[0]); ttk.Combobox(parent,textvariable=var,values=values,state='readonly').pack(fill='x',pady=4); return var
    pending={}; events=queue.Queue(); generation=[0]
    def async_request(work,done):
        generation[0]+=1; request_id=generation[0]
        stamp=creator.request_stamp()
        status.configure(text='Request running. You may keep writing or cancel; results never apply automatically.')
        def run():
            try: events.put((request_id,stamp,done,work(),None))
            except Exception as exc: events.put((request_id,stamp,done,None,str(exc)))
        threading.Thread(target=run,daemon=True).start()
    def poll():
        if not window.winfo_exists(): return
        while not events.empty():
            request_id,stamp,done,result,error=events.get()
            if request_id!=generation[0]: continue
            if error: status.configure(text='Request failed; writing preserved: '+error)
            elif stamp!=writing.token(creator.snapshot(),creator.draft['id'],creator.workspace_epoch):
                status.configure(text='Response is stale after draft changes. Request again; current writing is preserved.')
            else: safe(lambda:done(result,stamp))
        window.after(100,poll)
    def cancel():
        generation[0]+=1; pending.clear(); status.configure(text='Cancelled locally. Late results will be discarded.')
    w=page('Writing & locks')
    target=combo(w,tuple(writing.LIMITS)); mode=combo(w,('Expand','Rewrite','Format'))
    ttk.Label(w,text='Optional tone/length guidance').pack(anchor='w'); guidance=ttk.Entry(w); guidance.pack(fill='x')
    ttk.Label(w,text='Original (read-only reference) / editable suggestion').pack(anchor='w')
    original=text(w,4); proposal=text(w,6)
    ttk.Label(w,text='Locks: one per line, Field | Exact or Fact | wording. Fact locks need your semantic review.').pack(anchor='w')
    locks=text(w,3)
    replace(locks,'\n'.join(x['field']+' | '+x['mode']+' | '+x['text'] for x in creator.writing.get('locks',[])))
    def save_locks():
        entries=[]
        for line in locks.get('1.0','end').splitlines():
            if not line.strip(): continue
            parts=[x.strip() for x in line.split('|',2)]
            if len(parts)!=3 or parts[0] not in (*writing.LIMITS,*creator.values) or parts[1] not in ('Exact','Fact') or not parts[2]:
                raise ValueError('Each lock needs a supported field | Exact or Fact | nonempty wording.')
            entries.append(dict(field=parts[0],mode=parts[1],text=parts[2]))
        if len(entries)>40: raise ValueError('Use at most 40 locks.')
        snap=creator.snapshot(); snap.setdefault('writing',{})['locks']=entries
        commit(creator,snap,'Before changing writing locks'); status.configure(text='Locks saved. Existing requests are now stale.')
    def request():
        snap=creator.snapshot(); key=target.get(); action=mode.get()
        original.configure(state='normal'); replace(original,writing.field(snap,key)); original.configure(state='disabled')
        def received(value,stamp):
            replace(proposal,value); pending.update(stamp=stamp,field=key,mode=action)
            status.configure(text='Review proposed facts against active locks. No semantic checker can guarantee meaning. Apply, edit, retry or discard.')
        instructions=guidance.get()
        async_request(lambda:writing.propose(snap,key,action,instructions),received)
    reviewed=tk.BooleanVar(value=False)
    ttk.Checkbutton(w,text='I checked facts, locks and identity privacy in this suggestion',variable=reviewed).pack(anchor='w')
    def apply():
        if not reviewed.get(): raise ValueError('Review the suggestion and confirm its facts first.')
        if pending.get('stamp')!=writing.token(creator.snapshot(),creator.draft['id'],creator.workspace_epoch): raise ValueError('Suggestion is stale; request again.')
        snap=writing.apply(creator.snapshot(),pending['field'],proposal.get('1.0','end-1c'),pending['mode'])
        commit(creator,snap,'Before AI apply'); pending.clear(); reviewed.set(False); status.configure(text='Applied. Undo or revision history restores the original.')
    bar=ttk.Frame(w); bar.pack(fill='x')
    button(bar,'Save locks',save_locks); button(bar,'Request / retry',request); button(bar,'Apply',apply); button(bar,'Discard / cancel',cancel)

    ideas=page('Ideas & randomise')
    listing=tk.Listbox(ideas,bg=ui.PANEL,fg=ui.CREAM,selectbackground=ui.EDGE,exportselection=False,height=5); listing.pack(fill='x')
    label=ttk.Entry(ideas); label.pack(fill='x'); source=combo(ideas,tuple(writing.LIMITS)); passage=text(ideas,6)
    def refresh():
        listing.delete(0,'end')
        for idea in creator.writing.get('ideas',[]): listing.insert('end',idea['label']+' · '+idea['field'])
    def selected():
        if not listing.curselection(): raise ValueError('Select a bookmark.')
        return listing.curselection()[0]
    def choose(event=None):
        if not listing.curselection(): return
        idea=creator.writing['ideas'][selected()]; label.delete(0,'end'); label.insert(0,idea['label']); source.set(idea['field']); replace(passage,idea['text'])
    listing.bind('<<ListboxSelect>>',choose)
    def bookmark(edit=False):
        snap=creator.snapshot(); entries=snap.setdefault('writing',{}).setdefault('ideas',[])
        item=dict(label=label.get().strip()[:80] or 'Untitled idea',field=source.get(),text=passage.get('1.0','end-1c'))
        if len(item['text'])>12000 or len(entries)>=60 and not edit: raise ValueError('Ideas are limited to 60 entries of 12,000 characters.')
        if edit: entries[selected()]=item
        else: entries.append(item)
        commit(creator,snap,'Before bookmark edit'); refresh()
    def remove():
        snap=creator.snapshot(); del snap['writing']['ideas'][selected()]; commit(creator,snap,'Before removing idea'); refresh()
    def insert():
        snap=writing.apply(creator.snapshot(),source.get(),passage.get('1.0','end-1c'))
        commit(creator,snap,'Before inserting idea'); status.configure(text='Idea applied to its field; bookmark retained.')
    bar=ttk.Frame(ideas); bar.pack(fill='x')
    button(bar,'Save idea',bookmark); button(bar,'Update selected',lambda:bookmark(True)); button(bar,'Remove',remove); button(bar,'Insert into field',insert)
    button(bar,'Copy suggestion here',lambda:(source.set(target.get()),replace(passage,proposal.get('1.0','end-1c'))))
    choices={key:tk.BooleanVar(value=False) for key in writing.POOLS}
    for key,var in choices.items(): ttk.Checkbutton(ideas,text='Randomise '+key,variable=var).pack(anchor='w')
    random_preview=text(ideas,3); rolled={}
    def roll():
        creator.request_stamp()
        before=creator.snapshot(); after=writing.randomise(before,[k for k,v in choices.items() if v.get()])
        rolled.update(snapshot=after,stamp=writing.token(before,creator.draft['id'],creator.workspace_epoch))
        replace(random_preview,'\n'.join(k+': '+str(writing.field(after,k)) for k,v in choices.items() if v.get()))
    def apply_roll():
        if rolled.get('stamp')!=writing.token(creator.snapshot(),creator.draft['id'],creator.workspace_epoch): raise ValueError('Preview is stale. Roll again.')
        commit(creator,rolled['snapshot'],'Before selective randomisation'); rolled.clear()
    bar=ttk.Frame(ideas); bar.pack(fill='x'); button(bar,'Preview random choices',roll); button(bar,'Apply random choices',apply_roll)
    refresh()

    identity=page('Identity')
    iv={}
    for key in ('public_name','alias','nickname'):
        ttk.Label(identity,text=key.replace('_',' ').title()).pack(anchor='w'); iv[key]=tk.StringVar(value=creator.identity.get(key,'')); ttk.Entry(identity,textvariable=iv[key]).pack(fill='x',pady=6)
    legal=tk.BooleanVar(value=creator.identity.get('legal_public',True))
    ttk.Checkbutton(identity,text='Legal name is public',variable=legal).pack(anchor='w')
    ttk.Label(identity,text='Private identity links and history require explicit disclosure in a story. Rank does not disclose your legal identity.',wraplength=720).pack(fill='x',pady=10)
    def identity_apply():
        import character_identity
        snap=creator.snapshot(); snap['identity']=character_identity.validate({k:v.get() for k,v in iv.items()}|dict(legal_public=legal.get()))
        commit(creator,snap,'Before identity change')
    bar=ttk.Frame(identity); bar.pack(fill='x'); button(bar,'Apply identity',identity_apply)

    packages=page('Import / export')
    ttk.Label(packages,text='Enter a local .mhcharacter path. Export reads the last explicitly saved reusable character; unsaved edits and ideas are excluded.',wraplength=720).pack(fill='x')
    path=ttk.Entry(packages); path.pack(fill='x',pady=10)
    private=tk.BooleanVar(value=False); ttk.Checkbutton(packages,text='Include private history and identity in export',variable=private).pack(anchor='w')
    inspection=text(packages,10); imported={}; export_preview={}
    def inspect():
        import character_packages
        imported.clear(); imported.update(character_packages.inspect(path.get()))
        p=imported['profile']; origin=p.get('origin',{})
        replace(inspection,p['name']+'\n'+imported['source_format']+'\n'+imported['warning']+'\n\n'+p.get('biography','')+
                '\n\nExperience: '+str(origin.get('experience','Newcomer'))+'\nCivilian career: '+str(origin.get('job') or 'Looking for work')+
                '\nCriminal background: '+str(origin.get('crime','Clean slate'))+'\nOrganisation: '+str(origin.get('organisation') or 'None')+
                '\n\nPrivate history included: '+str(bool(p.get('private_history')))+'\nPortrait: transparent PNG; bundled and validated.\nNo story progress or NPC knowledge will be imported.')
    def accept_import():
        import character_packages
        if not imported: raise ValueError('Inspect a package first.')
        if not creator.save_draft(): raise ValueError('Save the current draft before importing.')
        snap=character_packages.draft_snapshot(imported,creator.snapshot())
        creator.draft=drafts.new(); creator.restore_snapshot(snap); creator.undo_stack=drafts.Undo()
        creator.save_draft(); status.configure(text='Imported as a separate draft. Review and explicitly save a character when ready.')
    def saved_profile():
        import character_packages,custom_library,game_core
        ident=creator.edit_profile_id or creator.draft['id']
        profiles,_=custom_library.enumerate_profiles(game_core.SAVE.parent)
        p=next((p for p in profiles if p['profile_id']==ident),None)
        if p is None: raise ValueError('Save character first; only accepted reusable data can be exported.')
        return p
    def preview_export():
        p=saved_profile()
        export_preview.update(profile=p,private=private.get(),path=path.get())
        replace(inspection,'EXPORT PREVIEW\n'+p['name']+'\nAccepted saved profile, starting choices and portrait.\n'+
                ('Includes private history and identity links.' if private.get() else 'Excludes private history and aliases. A private legal name is replaced with the public name.')+
                '\nExcludes story progress, credentials, ideas, revisions and sample conversations.\nDestination: '+path.get())
    def export():
        import character_packages
        p=saved_profile()
        if export_preview!=dict(profile=p,private=private.get(),path=path.get()): raise ValueError('Preview the current export contents first.')
        result=character_packages.export(p,path.get(),private.get()); status.configure(text='Exported '+str(result))
    bar=ttk.Frame(packages); bar.pack(fill='x'); button(bar,'Inspect import',inspect); button(bar,'Import as new draft',accept_import); button(bar,'Preview export',preview_export); button(bar,'Export saved character',export)

    dialogue=page('Sample dialogue')
    ttk.Label(dialogue,text='Non-canonical sample with a new acquaintance. Only public facts and what you type here are shared. No memories, time, relationships or saves change.',wraplength=720).pack(fill='x')
    transcript=text(dialogue,14); reply=ttk.Entry(dialogue); reply.pack(fill='x'); conversation=[]; sample_stamp=[None]
    def send():
        snap=creator.snapshot(); stamp=writing.token(snap,creator.draft['id'],creator.workspace_epoch)
        if sample_stamp[0] not in (None,stamp): raise ValueError('Draft changed. Clear/restart the sample.')
        line=reply.get().strip()
        if not line or len(line)>2000: raise ValueError('Enter a reply up to 2,000 characters.')
        profile=creator.collect(); messages=conversation+[dict(role='user',text=line)]
        def received(value,request_stamp):
            conversation[:]=messages+[dict(role='assistant',text=value)]; sample_stamp[0]=request_stamp
            replace(transcript,'\n\n'.join(m['role']+': '+m['text'] for m in conversation)); reply.delete(0,'end')
        async_request(lambda:writing.sample(profile,messages),received)
    def clear():
        cancel(); conversation.clear(); sample_stamp[0]=None; replace(transcript,'')
    bar=ttk.Frame(dialogue); bar.pack(fill='x'); button(bar,'Send sample reply',send); button(bar,'Clear / restart',clear); button(bar,'Cancel request',cancel)
    window.protocol('WM_DELETE_WINDOW',lambda:(cancel(),window.destroy()))
    phone_theme.apply_tree(window); poll()
    return window
