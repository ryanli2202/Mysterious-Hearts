"""Trait review and an isolated in-person practice window."""
import copy
import json
import queue
import threading
import tkinter as tk
from tkinter import ttk
import creator_combat as kits
import creator_writing as writing
from creator_tools_ui import text,replace,commit,scroll_page
import combat_moves as moves
import phone_theme
import winterfield_ui as ui


def compare_amplifications(creator,old,new,signature):
    window=creator.workspace_window('Compare Trait mechanics before replacing')
    view=text(window,22); status=ttk.Label(window,wraplength=720); status.pack(fill='x',padx=12)
    def describe(options):
        rows=[]
        for a in options:
            applications=[spec['name'] for spec in __import__('trait_activities').ACTIONS.values() if spec['tags']&set(a['tags'])]
            rows.append(a['name']+' · baseline mana '+str(a['mana'])+'\nEffects: '+', '.join(a['tags'])+
                        '\nCompatible move roles: '+', '.join(a['compatible'])+'\nEnvironment: '+a['environment']+
                        '\nWork / exploration: '+(', '.join(applications) or 'No authored application'))
        return '\n\n'.join(rows)
    replace(view,'CURRENT / PREVIOUS\n'+describe(old)+'\n\nPROPOSED\n'+describe(new)+
            '\n\nReplacing these mechanics invalidates starting-signature approval. An aspect specialisation is retained only if still compatible. Identity, appearance, locks, career and existing stories stay unchanged.')
    stamp=creator.request_stamp()
    def apply():
        try:
            if stamp!=writing.token(creator.snapshot(),creator.draft['id'],creator.workspace_epoch): raise ValueError('Draft changed; evaluate again.')
            import creator_drafts
            creator.draft=creator_drafts.save(creator.draft_root,creator.draft,creator.snapshot(),'Before Trait mechanics replacement')
            creator.undo_stack.record(creator.snapshot()); creator.install_trait_options(new,signature); creator.workspace_epoch+=1
            window.destroy()
        except (ValueError,OSError) as exc: status.configure(text=str(exc))
    bar=ttk.Frame(window); bar.pack(fill='x',padx=12,pady=8)
    ttk.Button(bar,text='Apply proposed mechanics',command=apply).pack(side='left')
    ttk.Button(bar,text='Cancel',command=window.destroy).pack(side='right')
    phone_theme.apply_tree(window)
    return window


def open_review(creator):
    window=creator.workspace_window('Trait builder, signature & kit review'); window.geometry('900x780')
    tabs=ttk.Notebook(window); tabs.pack(fill='both',expand=True,padx=12,pady=12)
    status=ttk.Label(window,text='Review changes before applying. Existing stories stay unchanged.',wraplength=840); status.pack(fill='x',padx=12,pady=8)
    def safe(fn):
        try: fn()
        except (ValueError,OSError,KeyError) as exc: status.configure(text=str(exc))
    def button(parent,title,fn): ttk.Button(parent,text=title,command=lambda:safe(fn)).pack(side='left',padx=4,pady=6)
    def page(title):
        return scroll_page(tabs,title)
    builder=page('Structured Trait')
    inputs={}
    for key in ('Domain','Intended effects','Activation / setup','Range','Costs','Limits'):
        ttk.Label(builder,text=key).pack(anchor='w'); entry=ttk.Entry(builder); entry.pack(fill='x',pady=4); inputs[key]=entry
    ttk.Label(builder,text='These prompts write a proposed description. Only evaluated and accepted amplification tags become executable mechanics.',wraplength=800).pack(fill='x')
    comparison=text(builder,9); proposed={}
    def preview_description():
        creator.request_stamp()
        result='\n'.join(k+': '+v.get().strip() for k,v in inputs.items() if v.get().strip())
        if not result: raise ValueError('Fill one or more optional prompts.')
        snap=creator.snapshot(); proposed.update(value=result,stamp=writing.token(snap,creator.draft['id'],creator.workspace_epoch))
        replace(comparison,'CURRENT\n'+snap['awakening_description']+'\n\nPROPOSED\n'+result+
                '\n\nApplying changes invalidates Trait acceptance and the starting signature. Appearance, identity and career are preserved. Re-evaluate before capabilities or work uses become available.')
    def apply_description():
        snap=creator.snapshot()
        if proposed.get('stamp')!=writing.token(snap,creator.draft['id'],creator.workspace_epoch): raise ValueError('Preview the current change first.')
        snap=writing.apply(snap,'awakening_description',proposed['value']); snap['starting_signature']=None; snap['specialisation']=''
        commit(creator,snap,'Before structured Trait replacement')
    bar=ttk.Frame(builder); bar.pack(fill='x'); button(bar,'Compare proposed description',preview_description); button(bar,'Apply description',apply_description)
    review=page('Kit & interactions')
    move_choice=tk.StringVar(); amp_choice=tk.StringVar(value='None'); focus=tk.StringVar(value='None')
    move_box=ttk.Combobox(review,textvariable=move_choice,state='readonly'); move_box.pack(fill='x',pady=4)
    amp_box=ttk.Combobox(review,textvariable=amp_choice,state='readonly'); amp_box.pack(fill='x',pady=4)
    detail=text(review,17); options={}; amp_options={}; profile=[None]
    ttk.Label(review,text='Specialise in one accepted aspect: baseline mana −1 (minimum 2); other aspects +1 (maximum 18). Refinement then scales real costs.').pack(fill='x')
    focus_box=ttk.Combobox(review,textvariable=focus,state='readonly'); focus_box.pack(fill='x')
    def refresh():
        import combat_profiles,combat
        raw=creator.collect(); p=combat_profiles.make('custom_kit_preview',raw); profile[0]=p
        options.clear(); options.update({m['name']+' · '+m['id']:m['id'] for m in moves.actions(p)})
        move_box.configure(values=list(options)); move_choice.set(next(iter(options)))
        amp_options.clear(); amp_options.update({'None':None,**{a['name']:a['id'] for a in moves.amps(p)}})
        amp_box.configure(values=list(amp_options)); amp_choice.set('None')
        focus_box.configure(values=list(amp_options)); focus.set(next((k for k,v in amp_options.items() if v==creator.specialisation),'None'))
        resources=combat.resources(p); roles=sorted({m['role'] for m in moves.actions(p)})
        unaffordable=[m['name'] for m in moves.actions(p) if not moves.can_pay(resources,moves.selection(p,m['id']))]
        replace(detail,'Path: '+p['path']['stage']+'\nStats: '+json.dumps(p['stats'])+'\nCoverage: '+', '.join(roles)+
                '\nUnaffordable at full resources: '+(', '.join(unaffordable) or 'None')+
                '\n\n'+ '\n'.join(moves.details(m) for m in moves.actions(p)))
        import trait_activities
        supported=trait_activities.options(p)
        detail.insert('end','\n\nAuthored in-person applications\n'+('\n'.join(trait_activities.ACTIONS[k]['name']+': '+trait_activities.ACTIONS[k]['description'] for k in supported) if supported else 'No supported work or exploration use for these accepted aspects.'))
    def explain():
        if profile[0] is None: refresh()
        item=kits.interaction(profile[0],options[move_choice.get()],amp_options[amp_choice.get()])
        replace(detail,item['move']+' · '+item['role']+'\n\nWithout → with amplification\n'+
                '\n'.join(k.title()+': '+str(item['base'][k])+' → '+str(item['amplified'][k]) for k in ('mana','stamina','range','tags'))+
                '\n\nEnvironment: '+item['environment']+'\n'+item['note'])
    def specialise():
        creator.request_stamp()
        choice=amp_options.get(focus.get()) or ''; snap=creator.snapshot()
        if not proposed.get('focus')==choice:
            proposed['focus']=choice; proposed['focus_stamp']=writing.token(snap,creator.draft['id'],creator.workspace_epoch)
            replace(detail,'Current specialisation: '+(creator.specialisation or 'None')+'\nProposed: '+focus.get()+
                    '\nFocused aspect costs 1 less baseline mana; others cost 1 more. Tags, roles, range and authored work/exploration eligibility stay unchanged. Starting signature acceptance is invalidated.\nPress Compare / apply specialisation again to accept, or close to cancel.')
            return
        if proposed.get('focus_stamp')!=writing.token(snap,creator.draft['id'],creator.workspace_epoch): raise ValueError('Draft changed; refresh and compare again.')
        snap.update(specialisation=choice,starting_signature=None); commit(creator,snap,'Before Trait specialisation'); proposed.pop('focus',None); refresh()
    bar=ttk.Frame(review); bar.pack(fill='x'); button(bar,'Refresh kit',refresh); button(bar,'Explain interaction',explain); button(bar,'Compare / apply specialisation',specialise)
    button(bar,'In-person practice',lambda:open_practice(creator))
    signatures=page('Starting signature')
    role=tk.StringVar(value='attack'); ttk.Combobox(signatures,textvariable=role,values=('attack','counter','defence','mobility','setup','control','combo','throw','break'),state='readonly').pack(fill='x')
    ttk.Label(signatures,text='Visual theme · cosmetic only').pack(anchor='w'); theme=ttk.Entry(signatures); theme.pack(fill='x')
    candidates=tk.Listbox(signatures,bg=ui.PANEL,fg=ui.CREAM,selectbackground=ui.EDGE,exportselection=False,height=3); candidates.pack(fill='x',pady=8)
    skill_detail=text(signatures,13); batch={}; events=queue.Queue(); serial=[0]
    def request():
        raw=creator.collect(); kits.signature_context(raw)
        if role.get() not in kits.supported_roles(raw): raise ValueError('Supported roles: '+', '.join(kits.supported_roles(raw)))
        stamp=creator.request_stamp()
        intent=(role.get(),theme.get()); serial[0]+=1; request_id=serial[0]
        def run():
            try: events.put((request_id,stamp,intent,kits.generate(raw,*intent),None))
            except Exception as exc: events.put((request_id,stamp,intent,None,str(exc)))
        threading.Thread(target=run,daemon=True).start(); status.configure(text='Generating three candidates; no cooldown or story changes.')
    def poll():
        if not window.winfo_exists(): return
        while not events.empty():
            request_id,stamp,intent,result,error=events.get()
            if request_id!=serial[0]: continue
            if error: status.configure(text=error); continue
            if stamp!=writing.token(creator.snapshot(),creator.draft['id'],creator.workspace_epoch) or intent!=(role.get(),theme.get()):
                status.configure(text='Stale candidates discarded.'); continue
            batch.clear(); batch.update(result); batch['stamp']=stamp; candidates.delete(0,'end')
            for skill in batch['candidates']: candidates.insert('end',skill['name'])
            status.configure(text='Select and inspect one signature, or skip it. Other candidates grant nothing.')
        window.after(100,poll)
    def inspect(event=None):
        if candidates.curselection():
            c=batch['candidates'][candidates.curselection()[0]]
            replace(skill_detail,moves.details(c)+'\nSetup: '+c['setup']+'\nCounters: '+c['counter']+'\nEnvironment: '+c['environment'])
    candidates.bind('<<ListboxSelect>>',inspect)
    def accept():
        if batch.get('stamp')!=writing.token(creator.snapshot(),creator.draft['id'],creator.workspace_epoch) or (batch.get('role'),batch.get('theme'))!=(role.get(),theme.get()): raise ValueError('Candidates are stale.')
        if not candidates.curselection(): raise ValueError('Choose one candidate.')
        result=kits.accept(creator.collect(),batch,candidates.curselection()[0]); snap=creator.snapshot(); snap['starting_signature']=result
        commit(creator,snap,'Before starting signature selection'); status.configure(text='One origin signature accepted. Normal in-story absorption remains available.')
    def skip():
        serial[0]+=1; snap=creator.snapshot(); snap['starting_signature']=None; commit(creator,snap,'Before skipping signature')
    bar=ttk.Frame(signatures); bar.pack(fill='x'); button(bar,'Generate three candidates',request); button(bar,'Accept selected',accept); button(bar,'Skip / cancel',skip)
    phone_theme.apply_tree(window); poll(); safe(refresh)
    return window


def open_practice(creator):
    raw=creator.collect(); state=kits.sandbox(raw)
    stamp=creator.request_stamp()
    # A dedicated physical-scene window, never an embedded phone AppWindow.
    window=tk.Toplevel(creator.game); window.title('In person · disposable creator practice'); window.geometry('900x700'); window.configure(bg=ui.INK)
    ttk.Label(window,text='In-person training · trained D target · restrained spar\nNo rewards, time, learning, memories or saved injuries. This target is not a lore matchup benchmark.',wraplength=840).pack(fill='x',padx=12,pady=12)
    p=state['combat']['profiles']['custom_practice']; options={m['name']+' · '+m['id']:m['id'] for m in moves.actions(p)}
    choice=tk.StringVar(value=next(iter(options))); ttk.Combobox(window,textvariable=choice,values=list(options),state='readonly').pack(fill='x',padx=12)
    amps={'None':None,**{a['name']:a['id'] for a in moves.amps(p)}}; amp=tk.StringVar(value='None'); ttk.Combobox(window,textvariable=amp,values=list(amps),state='readonly').pack(fill='x',padx=12,pady=6)
    targets={'Opponent':'opponent',**{o['name']:o['id'] for o in state['combat']['active']['arena']['objects']}}
    target=tk.StringVar(value='Opponent'); ttk.Combobox(window,textvariable=target,values=list(targets),state='readonly').pack(fill='x',padx=12,pady=6)
    log=text(window,18)
    def act():
        try:
            if stamp!=writing.token(creator.snapshot(),creator.draft['id'],creator.workspace_epoch): raise ValueError('Creator changed. Close and reopen practice.')
            result=kits.exchange(state,options[choice.get()],amps[amp.get()],targets[target.get()]); log.insert('end',result['narration']+'\n'+result['summary']+'\n\n'); log.see('end')
        except (ValueError,KeyError) as exc: log.insert('end',str(exc)+'\n')
    ttk.Button(window,text='Execute training exchange',command=act).pack(pady=10)
    phone_theme.apply_tree(window)
    return window
