"""Learned combat actions and Trait training on the in-person stage."""
import copy
import tkinter as tk
from tkinter import ttk
import combat
import combat_engine as engine
import combat_moves as moves
import combat_workshop as workshop
import combat_states as states
import combat_objectives as objectives
from combat_profiles import ARTS, TEACHERS, profile
import winterfield_ui as ui
import combat_style as style


class EnhancedCombat:
    def picker(self,parent,variable,values,callback,width=26):
        widget=ttk.Combobox(parent,textvariable=variable,values=values,state='readonly',width=width)
        widget.pack(side='left',padx=(0,6),pady=4)
        widget.bind('<<ComboboxSelected>>',lambda e:callback())
        return widget

    def listbox(self,parent,height=8):
        frame=tk.Frame(parent,bg=ui.INK); frame.pack(fill='both',expand=True,pady=5)
        box=tk.Listbox(frame,bg=ui.CARD,fg=ui.CREAM,selectbackground=ui.EDGE,
            selectforeground=ui.CREAM,highlightthickness=0,exportselection=False,height=height)
        scroll=ttk.Scrollbar(frame,command=box.yview); scroll.pack(side='right',fill='y')
        box.configure(yscrollcommand=scroll.set); box.pack(fill='both',expand=True)
        return box

    def read_panel(self,text,height=6):
        frame=self.row(); frame.pack_configure(fill='both',expand=True)
        box=tk.Text(frame,bg=ui.PANEL,fg=ui.CREAM,wrap='word',height=height,relief='flat',font=('Segoe UI',10),padx=12,pady=8,spacing3=4)
        scroll=ttk.Scrollbar(frame,command=box.yview); scroll.pack(side='right',fill='y')
        box.configure(yscrollcommand=scroll.set); box.pack(fill='both',expand=True)
        box.insert('end',text); box.configure(state='disabled')
        return box

    def set_page(self,page=None):
        self.training_page=page; self.path_who=None; self.refresh()

    def detail_panel(self,height=5):
        box=self.read_panel('',height); box.master.pack_configure(expand=False)
        return box

    def set_detail(self,box,text):
        box.configure(state='normal'); box.delete('1.0','end'); box.insert('end',text); box.configure(state='disabled')

    def combat_dossier(self):
        import combat_identity
        s=self.game.state_data; p=profile(s,s['player']); sheet=combat_identity.sheet(s['player'],p)
        overlay=style.Panel(self,bg=ui.INK,padx=18,pady=14)
        overlay.place(x=0,y=0,relwidth=1,relheight=1); overlay.lift()
        ttk.Button(overlay,text='Return to combat',command=overlay.destroy).pack(anchor='w',pady=5)
        box=tk.Text(overlay,bg=ui.PANEL,fg=ui.CREAM,wrap='word',font=('Segoe UI',11),relief='flat')
        scroll=ttk.Scrollbar(overlay,command=box.yview); scroll.pack(side='right',fill='y')
        box.configure(yscrollcommand=scroll.set); box.pack(fill='both',expand=True)
        text=sheet['name']+' · '+sheet['tier']+' baseline\n'+sheet['title']+'\n'+sheet['reputation']+'\n\n'
        text+=combat_identity.ability_details(p)+'\n\n'+sheet['assumptions']+'\n'+sheet['tactics']
        box.insert('end',text); box.configure(state='disabled')
        overlay.bind('<Escape>',lambda e:overlay.destroy()); overlay.focus_set()

    def fight(self,s,f):
        import combat_portraits
        root=self.body
        engine.ensure_arena(f)
        rail=tk.Canvas(root,bg=ui.PANEL,height=154,highlightthickness=0); rail.pack(fill='x',pady=(0,6))
        stage_panels=[]; stage_portraits=[]
        self.combat_portrait_rail=rail
        self.combat_portrait_images={}
        self.combat_hud={}
        for column,(side,who,p) in enumerate((('player',s['player'],profile(s,s['player'])),
                                              ('enemy',f['opponent'],f['opponent_profile']))):
            panel=tk.Frame(rail,bg=ui.PANEL,padx=6,pady=4)
            stage_panels.append(rail.create_window(0,0,window=panel,anchor='nw'))
            photo=combat_portraits.portrait(self.game,who,(108,128),f['location'],s['world']['minute'])
            self.combat_portrait_images['player' if side=='player' else 'opponent']=photo
            stage_portraits.append(rail.create_image(0,0,image=photo,anchor='nw'))
            info=tk.Frame(panel,bg=ui.PANEL); info.pack(fill='both',expand=True,padx=4)
            name=tk.Label(info,text=('YOU · ' if side=='player' else 'OPPONENT · ')+p['name'],
                          bg=ui.PANEL,fg=ui.GOLD,font=('Segoe UI',10,'bold'),anchor='w',justify='left')
            name.pack(fill='x')
            name.bind('<Configure>',lambda e,w=name:w.configure(wraplength=max(80,e.width-4)))
            r=f[side]; self.combat_hud[side]={}
            for key,label,maximum,colour in (('health','Health','max_health','#dc808d'),
                    ('stamina','Stamina',None,ui.MINT),('energy','Mana','max_energy','#81b9ef')):
                cap=r.get(maximum,100) if maximum else 100
                bar=tk.Canvas(info,height=19,bg=ui.CARD,highlightthickness=0)
                bar.pack(fill='x',pady=1)
                def draw(event,w=bar,value=r[key],limit=cap,title=label,fill=colour):
                    w.delete('all'); fraction=max(0,min(1,value/limit)) if limit else 0
                    w.create_rectangle(0,0,event.width*fraction,19,fill=fill,outline='')
                    # Dark text backing keeps the number readable on both empty and filled bars.
                    w.create_rectangle(3,1,146,18,fill=ui.PANEL,outline='')
                    w.create_text(7,9,text=f'{title} {value}/{limit}',fill=ui.CREAM,anchor='w',font=('Segoe UI',9))
                bar.bind('<Configure>',draw); self.combat_hud[side][key]=bar
            form=engine.active_form(f,side)
            state=(form['name']+f" · {r['form_until']-f['elapsed']}s") if form else p['path']['stage']
            if p.get('arena_band'): state+=' · '+p['arena_band']+' ring assessment'
            if p.get('boss'): state+=' · '+p.get('combat_band','Unranked')+' equipped boss'
            extra=states.status(p,r)
            if extra: state+='\n'+extra
            status=tk.Label(info,text=state,bg=ui.PANEL,fg=ui.MUTED,anchor='w',justify='left')
            status.pack(fill='x')
            status.bind('<Configure>',lambda e,w=status:w.configure(wraplength=max(80,e.width-4)))
        self.opponent_portrait=self.combat_portrait_images['opponent']
        from artwork import source_image,scene_art
        from PIL import Image,ImageOps,ImageTk
        backdrop=rail.create_image(0,0,anchor='nw'); rail.tag_lower(backdrop)
        def resize_stage(event):
            width=max(300,event.width); compact=self.winfo_height()<760
            pw=96 if compact else 132; ph=round(pw*1.185); height=max(148,ph+20)
            if int(rail.cget('height'))!=height: rail.configure(height=height)
            scene=ImageOps.fit(source_image(scene_art(f['location'],minute=s['world']['minute'])).convert('RGB'),(width,height))
            scene=Image.blend(scene,Image.new('RGB',scene.size,ui.INK),.40)
            self.combat_stage_background=ImageTk.PhotoImage(scene)
            rail.itemconfigure(backdrop,image=self.combat_stage_background)
            panel_width=max(120,(width-2*pw-52)//2)
            photos=combat_portraits.group(self.game,
                {s['player']:(pw,ph),f['opponent']:(pw,ph)},f['location'],s['world']['minute'])
            for index,(side,who) in enumerate((('player',s['player']),('opponent',f['opponent']))):
                photo=photos[who]
                self.combat_portrait_images[side]=photo
                rail.itemconfigure(stage_portraits[index],image=photo)
                rail.coords(stage_portraits[index],12 if index==0 else width-pw-12,(height-ph)//2)
                rail.coords(stage_panels[index],pw+20 if index==0 else width-pw-20-panel_width,8)
                rail.itemconfigure(stage_panels[index],width=panel_width)
            self.opponent_portrait=self.combat_portrait_images['opponent']
        rail.bind('<Configure>',resize_stage)
        controls=tk.Frame(root,bg=ui.INK);controls.pack(fill='both',expand=True)
        self.body=controls
        try:self.fight_controls(s,f)
        finally:self.body=root

    def fight_controls(self,s,f):
        engine.ensure_arena(f); p=profile(s,s['player']); q=f['opponent_profile']
        self.title.configure(text=('BOSS' if q.get('boss') else f['kind'].upper())+' · '+q['name'])
        clock=(f"Round {min(3,f['elapsed']//300+1)}/3 · {max(0,900-f['elapsed'])} seconds left" if f['kind']=='circle' else 'Until knockout or concession · no deaths')
        self.label(self.body,clock+' · Exchange '+str(f['turn']+1)+' · '+p['path']['stage']+' / '+q['path']['stage'])
        arena=f['arena']
        self.arena_label=self.label(self.body,'Arena · '+ ' · '.join(o['name']+': '+(str(o['integrity'])+'/'+str(o['max_integrity']) if o['integrity'] else 'DESTROYED') for o in arena['objects'])+
            f" · Distance {abs(arena['positions']['player']-arena['positions']['enemy'])}"+(' · Rubble affects footing' if arena['rubble'] else ''))
        from artwork import source_image,scene_art
        from PIL import Image,ImageOps,ImageTk
        arena_text=self.arena_label.cget('text'); self.arena_label.destroy()
        if f.get('ally_resources'):
            ally=f['ally_resources']; ap=f['ally_profile']
            arena_text='Partner '+ap['name']+f" · Health {ally['health']}/{ally['max_health']} · Stamina {ally['stamina']} · Mana {ally['energy']} · Position {arena['positions'].get('ally',arena['positions']['player'])}"+' · '+states.status(ap,ally)+'\n'+arena_text
        self.arena_label=tk.Canvas(self.body,height=48,bg=ui.INK,highlightthickness=0)
        self.arena_label.pack(fill='x',pady=2)
        def paint_arena(event):
            picture=ImageOps.fit(source_image(scene_art(f['location'],minute=s['world']['minute'])).convert('RGB'),(max(1,event.width),48))
            picture=Image.blend(picture,Image.new('RGB',picture.size,ui.INK),.58)
            self.arena_backdrop=ImageTk.PhotoImage(picture)
            self.arena_label.delete('all'); self.arena_label.create_image(0,0,image=self.arena_backdrop,anchor='nw')
            self.arena_label.create_text(8,24,text=arena_text,fill=ui.CREAM,anchor='w',width=max(80,event.width-16),font=('Segoe UI',9))
        self.arena_label.bind('<Configure>',paint_arena)
        if f.get('kind')=='spar': self.label(self.body,'Restrained practice · both sides use 55% striking output; no winner or full-strength claim.')
        if f['status']=='active': self.opponent_intent=self.label(self.body,'Opponent intent · '+engine.describe_plan(s))
        self.transcript=self.read_panel('\n\n'.join(f['log'][-24:]) or 'Choose a learned action. Both fighters act each exchange; attacks, counters and terrain resolve before narration.',4)
        self.transcript.see('end')
        if f['status']=='finished':
            self.label(self.body,f['result']); self.button(self.row(),'Leave fight',lambda:combat.close(s)); return
        row=self.row()
        if states.trait(p,'Shinigami Protocol'):
            b=self.button(row,'Shinigami Protocol · 20 stamina',lambda:states.activate_protocol(s))
            b.configure(state='normal' if states.protocol_available(s,f,'player',p) else 'disabled')
        channels=states.channels(p)
        if channels:
            channel=tk.StringVar(value=f['player']['channel'] or 'No channel')
            self.picker(row,channel,['No channel',*channels[1:]],lambda:self.run(lambda:states.set_channel(s,'' if channel.get()=='No channel' else channel.get())),16)
            endurance=self.button(row,'Misanthropy · 18 mana',lambda:states.activate_endurance(s))
            if f['player']['misanthropy_used'] or f['player']['energy']<18: endurance.configure(state='disabled')
        if not f['turn'] and len(objectives.choices(f))>1:
            goal=tk.StringVar(value=f.get('objective','Duel'))
            self.picker(row,goal,objectives.choices(f),lambda:self.run(lambda:objectives.select(s,goal.get())),14)
        self.objective_label=self.label(self.body,objectives.description(f))
        row=self.row(); self.action_kind=tk.StringVar(value=getattr(self,'saved_kind','Martial'))
        self.action_art=tk.StringVar(value=getattr(self,'saved_art','All arts'))
        self.picker(row,self.action_kind,['Martial','Unique skills','Awakened signatures','Utility'],self.populate_moves,20)
        self.picker(row,self.action_art,['All arts',*p['arts']],self.populate_moves,25)
        self.button(row,'Activate form',lambda:combat.activate_form(s))
        ttk.Button(row,text='Ability details',command=self.combat_dossier).pack(side='left',padx=3)
        if p.get('technique_form')=='Conduit State': self.button(row,'Conduit State',lambda:combat.activate_form(s,form_choice='Conduit State'))
        self.button(row,'Stop spar' if f['kind']=='spar' else 'Concede',lambda:combat.concede(s))
        row=self.row(); self.move_choice=tk.StringVar(); self.amp_choice=tk.StringVar(value='None'); self.target_choice=tk.StringVar(value='Opponent')
        self.move_picker=self.picker(row,self.move_choice,[],self.populate_amps,43)
        self.amp_picker=self.picker(row,self.amp_choice,['None'],self.selection_detail,24)
        self.target_map={'Opponent':'opponent',**{o['name']+(' (wreckage)' if not o['integrity'] else ''):o['id'] for o in arena['objects'] if o['integrity']>0 or o['material']!='ground'}}
        self.picker(row,self.target_choice,list(self.target_map),self.selection_detail,24)
        self.move_detail=self.detail_panel(3)
        self.execute_button=self.button(self.row(),'Resolve selected action',self.submit)
        self.populate_moves()

    def populate_moves(self):
        p=profile(self.game.state_data,self.game.state_data['player'])
        kind={'Martial':'martial','Unique skills':'unique','Awakened signatures':'signature','Utility':'utility'}[self.action_kind.get()]
        self.saved_kind=self.action_kind.get(); self.saved_art=self.action_art.get()
        options=[m for m in moves.actions(p) if m['kind']==kind and (kind!='martial' or self.action_art.get()=='All arts' or m['art']==self.action_art.get())]
        self.move_map={m['name']+(' · '+m['art'] if m['art'] else ''):m for m in options}
        self.move_picker.configure(values=list(self.move_map)); self.move_choice.set(next(iter(self.move_map),''))
        self.populate_amps()

    def populate_amps(self):
        p=profile(self.game.state_data,self.game.state_data['player']); move=self.move_map.get(self.move_choice.get())
        self.amp_map={'None':None}
        if move: self.amp_map.update({a['name']:a['id'] for a in moves.amps(p,move)})
        self.amp_picker.configure(values=list(self.amp_map)); self.amp_choice.set('None'); self.selection_detail()

    def selection_detail(self):
        s=self.game.state_data; p=profile(s,s['player']); move=self.move_map.get(self.move_choice.get())
        if not move:
            self.set_detail(self.move_detail,'No learned actions in this category. Learn martial arts with a teacher, or visit the Trait workshop.')
            self.execute_button.configure(state='disabled'); return
        selected=states.prepare_action(p,combat.active(s)['player'],moves.selection(p,move['id'],self.amp_map.get(self.amp_choice.get())))
        self.set_detail(self.move_detail,moves.details(selected))
        projected,_=engine.preview(s)
        self.execute_button.configure(state='normal' if moves.can_pay(projected['player'],selected) else 'disabled')

    def submit(self):
        if self.working or self.game.busy: return
        s=self.game.state_data; move=self.move_map.get(self.move_choice.get())
        if not move: raise ValueError('Select a learned action.')
        result=engine.resolve(s,engine.request(s,move['id'],self.amp_map.get(self.amp_choice.get()),self.target_map[self.target_choice.get()]))
        self.game.persist(); self.refresh()
        self.async_job(lambda:engine.narrate(result),lambda value:engine.commit_narration(s,value),resolved=True)

    def academy(self):
        s=self.game.state_data; p=profile(s,s['player'])
        self.title.configure(text='TRAINING · LEARNED TECHNIQUES')
        self.label(self.body,'Basics: first lesson · Advanced: martial skill 60+ · Master: martial skill 80+ and awakened. Each lesson takes 30 minutes; three sessions per day.')
        self.label(self.body,f"Martial skill {p['stats']['martial_skill']} · "+('Awakened' if p['awakened'] else 'Unawakened')+' · '+str(len(p['moveset']['learned']))+' learned techniques')
        row=self.row(); self.teacher_choice=tk.StringVar(value='Practise alone')
        self.teacher_map={'Practise alone':None,**{profile(s,x)['name']:x for x in TEACHERS if combat.present(s,x)}}
        self.picker(row,self.teacher_choice,list(self.teacher_map),self.academy_arts,26)
        self.lesson_art=tk.StringVar(); self.lesson_art_picker=self.picker(row,self.lesson_art,[],self.academy_moves,28)
        workspace=style.Panel(self.body,padx=10,pady=8); workspace.pack(fill='both',expand=True,pady=6)
        catalogue=tk.Frame(workspace,bg=ui.PANEL); catalogue.pack(side='left',fill='both',expand=True,padx=(0,12))
        detail=tk.Frame(workspace,bg=ui.PANEL,width=290); detail.pack(side='right',fill='both'); detail.pack_propagate(False)
        style.heading(catalogue,'01  /  TECHNIQUE LIBRARY')
        style.heading(detail,'02  /  TECHNIQUE BRIEF')
        self.lesson_list=self.listbox(catalogue,7)
        self.lesson_list.bind('<<ListboxSelect>>',lambda e:self.lesson_detail())
        self.lesson_description=self.label(detail,'')
        row=self.row(); self.learn_button=self.button(row,'Learn selected technique · 30 min',self.learn_selected)
        self.button(row,'Practise selected art · 30 min',lambda:combat.train(s,self.lesson_art.get(),self.teacher_map[self.teacher_choice.get()]))
        self.button(row,'Trait workshop',lambda:self.set_page('workshop'))
        self.button(row,'Back',lambda:self.set_page())
        self.academy_arts()

    def academy_arts(self):
        s=self.game.state_data; p=profile(s,s['player']); who=self.teacher_map[self.teacher_choice.get()]
        arts=list(dict.fromkeys([*p['arts'],*[x for x in TEACHERS.get(who,[]) if x in ARTS]]))
        self.lesson_art_picker.configure(values=arts); self.lesson_art.set(arts[0] if arts else '')
        self.academy_moves()

    def academy_moves(self):
        p=profile(self.game.state_data,self.game.state_data['player']); self.lesson_options=[m for m in moves.MOVES.values() if m['art']==self.lesson_art.get()]
        self.lesson_list.delete(0,'end')
        for m in self.lesson_options:
            state='Learned' if m['id'] in p['moveset']['learned'] else 'Available' if moves.eligible(p,m['tier']) else 'Locked'
            self.lesson_list.insert('end',state+' · '+m['tier'].title()+' · '+m['name']+' · '+m['role'])
        if self.lesson_options: self.lesson_list.selection_set(0)
        self.lesson_detail()

    def lesson_detail(self):
        selected=self.lesson_list.curselection(); p=profile(self.game.state_data,self.game.state_data['player'])
        move=self.lesson_options[selected[0]] if selected else None
        self.lesson_description.configure(text=moves.details(move) if move else 'Meet a martial teacher at this location to learn your first art.')
        self.learn_button.configure(state='normal' if move and moves.eligible(p,move['tier']) and move['id'] not in p['moveset']['learned'] else 'disabled')

    def learn_selected(self):
        selected=self.lesson_list.curselection()
        if not selected: raise ValueError('Select a technique.')
        return moves.lesson(self.game.state_data,self.lesson_options[selected[0]]['id'],self.teacher_map[self.teacher_choice.get()])

    def workshop_page(self):
        s=self.game.state_data; self.title.configure(text='TRAINING · TRAIT WORKSHOP')
        try: p=workshop.access(s)
        except ValueError as exc:
            self.label(self.body,str(exc)); self.button(self.row(),'Back to training',lambda:self.set_page('academy')); return
        w=workshop.book(s)
        self.label(self.body,p['trait']['name']+' — '+p['trait']['description'])
        self.label(self.body,'Generate three skills from your current stats and approved Trait aspects. Absorb one every 24 in-game hours. Learned skills and amplification remain usable during this learning cooldown.')
        style.heading(self.body,'TRAIT LABORATORY')
        self.label(self.body,'Next absorption: '+(str(workshop.remaining(s))+' in-game minutes' if workshop.remaining(s) else 'Ready now'))
        if not p['moveset']['amplifications']:
            pending=getattr(self,'pending_amplifications',None)
            if pending:
                self.read_panel('\n\n'.join(a['name']+' · '+a['role']+'\n'+a['description']+'\nMana '+str(a['mana'])+' · '+a['environment'] for a in pending['amplifications']))
                self.button(self.row(),'Accept reviewed amplification options',self.accept_amps)
            else: self.label(self.body,'This existing custom character needs reviewed amplification options before generating unique skills.')
            self.button(self.row(),'Evaluate Trait amplification',self.evaluate_amps)
        else:
            self.label(self.body,'Amplification: '+', '.join(a['name'] for a in p['moveset']['amplifications']))
            self.candidate_list=self.listbox(self.body,3)
            for a in w['candidates']: self.candidate_list.insert('end',a['name']+' · '+a['role'])
            self.candidate_detail=self.detail_panel(7)
            self.set_detail(self.candidate_detail,'Generate a candidate set to review it here.')
            self.candidate_list.bind('<<ListboxSelect>>',lambda e:self.describe_candidate())
            row=self.row(); self.button(row,'Generate unique skills',self.generate_skills)
            self.absorb_button=self.button(row,'Absorb selected skill',self.absorb_skill)
            if w['candidates']: self.candidate_list.selection_set(0)
            self.describe_candidate()
            self.label(self.body,'Learned: '+(', '.join(a['name'] for a in p['moveset']['unique']) or 'None yet'))
        self.button(self.row(),'Back to training',lambda:self.set_page('academy'))

    def evaluate_amps(self):
        snapshot=copy.deepcopy(self.game.state_data)
        self.async_job(lambda:workshop.generate_amplifications(snapshot),lambda result:setattr(self,'pending_amplifications',result))

    def accept_amps(self):
        result=workshop.accept_amplifications(self.game.state_data,self.pending_amplifications)
        self.pending_amplifications=None; return result

    def generate_skills(self):
        s=self.game.state_data; snapshot=copy.deepcopy(s)
        self.async_job(lambda:workshop.generate(snapshot),lambda result:workshop.commit_candidates(s,result))

    def describe_candidate(self):
        s=self.game.state_data; selected=self.candidate_list.curselection(); candidates=workshop.book(s)['candidates']
        skill=candidates[selected[0]] if selected else None
        if skill:
            self.set_detail(self.candidate_detail,moves.details(skill)+'\nEnvironment: '+skill['environment']+'\nSetup: '+skill['setup']+' · Counter: '+skill['counter'])
        self.absorb_button.configure(state='normal' if skill and not workshop.remaining(s) else 'disabled')

    def absorb_skill(self):
        s=self.game.state_data; selected=self.candidate_list.curselection(); w=workshop.book(s)
        if not selected: raise ValueError('Select a candidate to absorb.')
        return workshop.absorb(s,w['candidates'][selected[0]]['id'],w['batch'])
