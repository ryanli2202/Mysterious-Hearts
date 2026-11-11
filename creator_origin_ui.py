"""Dark starting-choice picker; Apply affects only the creator draft."""
import copy
import tkinter as tk
from tkinter import ttk
import character_origins as origins
import job_apps
import phone_theme
import winterfield_ui as ui
from phone_dialogs import AppWindow


def open_picker(creator):
    window=AppWindow(creator); window.title('Starting background, career and combat kit')
    window.geometry('960x760'); window.minsize(780,650)
    window.columnconfigure(0,weight=1,uniform='origin'); window.columnconfigure(1,weight=1,uniform='origin'); window.rowconfigure(1,weight=1)
    ttk.Label(window,text='Advanced starts are freely selectable. Apply changes your draft only.',style='Section.TLabel').grid(row=0,column=0,columnspan=2,padx=14,pady=12)
    left_area=ttk.Frame(window); left_area.grid(row=1,column=0,sticky='nsew')
    scrollbar=ttk.Scrollbar(left_area); scrollbar.pack(side='right',fill='y')
    canvas=tk.Canvas(left_area,bg=ui.PANEL,highlightthickness=0,yscrollcommand=scrollbar.set)
    canvas.pack(fill='both',expand=True); scrollbar.configure(command=canvas.yview)
    left=ttk.Frame(canvas,padding=14); item=canvas.create_window(0,0,window=left,anchor='nw')
    def fit(e):
        canvas.itemconfigure(item,width=e.width)
        for widget in left.winfo_children():
            if isinstance(widget,ttk.Label): widget.configure(wraplength=max(160,e.width-32))
    canvas.bind('<Configure>',fit)
    left.bind('<Configure>',lambda e:canvas.configure(scrollregion=canvas.bbox('all')))
    right=ttk.Frame(window,padding=14); right.grid(row=1,column=1,sticky='nsew')
    p=origins.resolve(creator.origin,creator.awakened.get(),creator.needs_trait() and bool(creator.current_trait()[0]))['choices']
    job_labels={'Looking for work':None, **{spec['title']:key for key,spec in job_apps.JOBS.items()}}
    experience=tk.StringVar(value=p['experience'])
    job=tk.StringVar(value=next(k for k,v in job_labels.items() if v==p['job']))
    rank=tk.StringVar()
    crime=tk.StringVar(value=p['crime'])
    organisation=tk.StringVar()
    def combo(title,var,values):
        ttk.Label(left,text=title).pack(anchor='w',pady=(8,3))
        control=ttk.Combobox(left,textvariable=var,values=values,state='readonly')
        control.pack(fill='x'); return control
    combo('Combat history · independent of job and faction rank',experience,origins.EXPERIENCES)
    combo('Current civilian employment',job,list(job_labels))
    ranks=combo('Career experience · actual title',rank,())
    interest=tk.StringVar(value=next(k for k,v in job_labels.items() if v==p['career_interest']))
    combo('Career interest · saved listing, not employment',interest,list(job_labels))
    combo('Criminal background',crime,tuple(origins.CRIME))
    organisations=combo('Organisation · selected role only',organisation,())
    background=tk.StringVar(value=p['background']); combo('Narrative background',background,origins.BACKGROUNDS)
    prior_job=tk.StringVar(value=next(k for k,v in job_labels.items() if v==p['prior_job']))
    combo('Prior career · no current wages or authority',prior_job,list(job_labels))
    prior_rank=tk.StringVar(value=str(p['prior_rank'])); combo('Prior career rank',prior_rank,('0','1','2','3'))
    crew_name=tk.StringVar(value=p['crew_name'])
    ttk.Label(left,text='Original crew name · founder only').pack(anchor='w')
    ttk.Entry(left,textvariable=crew_name).pack(fill='x')
    ttk.Label(left,text='Martial arts · selection order sets primary/secondary',wraplength=390).pack(anchor='w',pady=(12,3))
    arts=tk.Listbox(left,selectmode='multiple',exportselection=False,bg=ui.PANEL,fg=ui.CREAM,
                    selectbackground=ui.EDGE,selectforeground=ui.CREAM,height=7)
    arts.pack(fill='both',expand=True)
    for art in origins.ARTS: arts.insert('end',art)
    for art in p['arts']: arts.selection_set(origins.ARTS.index(art))
    ttk.Label(right,text='Learned advanced/master techniques',style='Section.TLabel').pack(anchor='w')
    ttk.Label(right,text='Basics are included for selected arts. Recommended kit is an explicit replacement; review the costs below.',wraplength=400).pack(anchor='w',pady=6)
    filters=ttk.Frame(right); filters.pack(fill='x')
    role_filter=tk.StringVar(value='All roles'); tier_filter=tk.StringVar(value='All tiers')
    ttk.Combobox(filters,textvariable=role_filter,values=('All roles',*origins.combat_moves.ROLES),state='readonly',width=16).pack(side='left',fill='x',expand=True)
    ttk.Combobox(filters,textvariable=tier_filter,values=('All tiers','advanced','master'),state='readonly',width=12).pack(side='left',fill='x',expand=True)
    moves=tk.Listbox(right,selectmode='multiple',exportselection=False,bg=ui.PANEL,fg=ui.CREAM,
                    selectbackground=ui.EDGE,selectforeground=ui.CREAM,height=12)
    moves.pack(fill='both',expand=True)
    preview=tk.Text(right,height=12,wrap='word',bg=ui.CARD,fg=ui.CREAM,insertbackground=ui.CREAM,font=('Segoe UI',10))
    preview.pack(fill='both',expand=True,pady=8)
    ids=[]; org_labels={}; ordered_arts=list(p['arts']); busy=False; selected_moves=set(p['moves'])
    def sync_moves():
        selected_moves.difference_update(ids)
        selected_moves.update(ids[i] for i in moves.curselection())
    def selected_arts():
        selected=[origins.ARTS[i] for i in arts.curselection()]
        ordered_arts[:]=[a for a in ordered_arts if a in selected]+[a for a in selected if a not in ordered_arts]
        return list(ordered_arts)
    def fill_moves(learned=None):
        if learned is None: sync_moves()
        else: selected_moves.clear(); selected_moves.update(learned)
        learned=selected_moves
        ids.clear(); moves.delete(0,'end')
        for m in origins.combat_moves.MOVES.values():
            if m['art'] in selected_arts() and m['tier']!='basic':
                if role_filter.get()!='All roles' and m['role']!=role_filter.get(): continue
                if tier_filter.get()!='All tiers' and m['tier']!=tier_filter.get(): continue
                index=origins.experience_index(dict(experience=experience.get(),crime=crime.get(),background=background.get()))
                allowed=(origins.KITS[index][2 if m['tier']=='master' else 1]>0 and (m['tier']!='master' or creator.awakened.get()))
                availability='Learned now' if m['id'] in learned else 'Eligible later' if allowed else 'Unavailable for this build'
                ids.append(m['id']); moves.insert('end',f"{m['name']} · {m['tier']} · {m['art']} · {availability}")
                if m['id'] in learned: moves.selection_set(len(ids)-1)
    def collect():
        sync_moves()
        key=job_labels[job.get()]
        return dict(version=1,experience=experience.get(),job=key,
                    job_rank=list(job_apps.JOBS[key]['ranks']).index(rank.get()) if key else 0,
                    crime=crime.get(),organisation=org_labels.get(organisation.get()),
                    background=background.get(),prior_job=job_labels[prior_job.get()],prior_rank=int(prior_rank.get()),crew_name=crew_name.get(),
                    career_interest=job_labels[interest.get()],
                    arts=selected_arts(),moves=sorted(selected_moves))
    def update(*_):
        if busy: return
        try:
            resolved=origins.resolve(collect(),creator.awakened.get(),creator.needs_trait() and bool(creator.current_trait()[0]))
            text=(resolved['experience']+' · '+resolved['target']+'\nPath: '+resolved['stage']+'\n\n'+
                  '\n'.join(k.replace('_',' ').title()+': '+str(v) for k,v in resolved['stats'].items())+
                  '\n\n'+'\n'.join(resolved['contributions'])+
                  f"\nReputation {resolved['reputation']} · heat {resolved['heat']}\nLearned techniques: {len(resolved['learned'])}")
            if resolved['employment']:
                e=resolved['employment']; text+=f"\n{e['title']} · pay {e['pay']} · hours {e['hours'][0]}–{e['hours'][1]}"
            career_rank=max(int(prior_rank.get()),collect()['job_rank'])
            if career_rank>=2: text+='\nRecognised prior credential: Professional practice.'
            if career_rank>=3: text+='\nTeam leadership credential and prior portfolio. Local projects fund department budget; no cash or coworker trust is granted.'
            if crime.get()=='Small-crew founder': text+='\nFounder of '+crew_name.get()+': initial network tier, empty roster. Recruit willing residents through play.'
            text+='\n\nNo past shifts, contracts, victories or personal friendships are awarded. Master moves require Awakening.'
            for ident in [ids[i] for i in moves.curselection()]:
                text+='\n\n'+origins.combat_moves.details(origins.combat_moves.MOVES[ident])
        except (ValueError,KeyError) as exc: text='Needs attention: '+str(exc)
        preview.configure(state='normal'); preview.delete('1.0','end'); preview.insert('end',text); preview.configure(state='disabled')
    def job_change(*_):
        key=job_labels[job.get()]
        options=job_apps.JOBS[key]['ranks'] if key else ('No employment',)
        ranks.configure(values=options); rank.set(options[min(p['job_rank'],len(options)-1)])
        update()
    def crime_change(*_):
        nonlocal org_labels
        if crime.get() in ('Trusted crew member','Crew lieutenant','Crew captain'):
            org_labels={v['name']:k for k,v in job_apps.progression.GANGS.items()}
        elif crime.get() in ('Established faction member','Faction specialist','Faction field leader'):
            org_labels={k:k for k in job_apps.BRANCHES}
        else: org_labels={'None':None}
        organisations.configure(values=list(org_labels))
        organisation.set(next((k for k,v in org_labels.items() if v==p['organisation']),next(iter(org_labels))))
        update()
    def recommend():
        tier=origins.experience_index(dict(experience=experience.get(),crime=crime.get(),background=background.get()))
        selected=selected_arts()
        if tier and not selected: selected=origins.DEFAULT_ARTS.get(org_labels.get(organisation.get()),['Streetfighting','Boxing','MMA','Muay Thai'])
        selected,learned=origins.recommended(origins.EXPERIENCES[tier],selected,creator.awakened.get())
        arts.selection_clear(0,'end')
        for a in selected: arts.selection_set(origins.ARTS.index(a))
        fill_moves(learned); update()
    def apply():
        try:
            values=collect(); origins.resolve(values,creator.awakened.get(),creator.needs_trait() and bool(creator.current_trait()[0]))
            import creator_drafts
            creator.draft=creator_drafts.save(creator.draft_root,creator.draft,creator.snapshot(),'Before preset replacement')
            creator.undo_stack.record(creator.snapshot()); creator.origin=values
            if origins.experience_index(values)<3 and creator.starting_signature:
                creator.writing['parked_signature']=copy.deepcopy(creator.starting_signature)
                creator.starting_signature=None
            creator.origin_summary.configure(text=values['experience']+' · '+values['crime']+' · '+job.get())
            creator.workspace_epoch+=1
            window.destroy()
        except (OSError,ValueError) as exc:
            preview.configure(state='normal'); preview.delete('1.0','end'); preview.insert('end',str(exc)); preview.configure(state='disabled')
    bar=ttk.Frame(window,padding=12); bar.grid(row=2,column=0,columnspan=2,sticky='ew')
    ttk.Button(bar,text='Use recommended kit',command=recommend).pack(side='left')
    ttk.Button(bar,text='Cancel',command=window.destroy).pack(side='right')
    ttk.Button(bar,text='Apply starting choices',command=apply).pack(side='right',padx=8)
    window.bind('<Escape>',lambda e:window.destroy())
    job.trace_add('write',job_change); crime.trace_add('write',crime_change)
    for var in (experience,rank,organisation,background,prior_job,prior_rank,crew_name,interest): var.trace_add('write',update)
    arts.bind('<<ListboxSelect>>',lambda e:(fill_moves(),update()))
    moves.bind('<<ListboxSelect>>',update)
    for variable in (role_filter,tier_filter): variable.trace_add('write',lambda *_:(fill_moves(),update()))
    job_change(); crime_change(); fill_moves(p['moves']); update()
    phone_theme.apply_tree(window)
    return window
