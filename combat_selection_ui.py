"""Learned combat actions and Trait training on the in-person stage."""
import copy
import tkinter as tk
from tkinter import ttk
import combat
import combat_engine as engine
import combat_moves as moves
import combat_workshop as workshop
from combat_profiles import ARTS, TEACHERS, profile
import winterfield_ui as ui


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
        box=tk.Text(frame,bg=ui.PANEL,fg=ui.CREAM,wrap='word',height=height,relief='flat',font=('Segoe UI',10))
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

    def fight(self,s,f):
        engine.ensure_arena(f); p=profile(s,s['player']); q=f['opponent_profile']
        self.title.configure(text=f['kind'].upper()+' · '+q['name'])
        clock=(f"Round {min(3,f['elapsed']//300+1)}/3 · {max(0,900-f['elapsed'])} seconds left" if f['kind']=='circle' else 'Until knockout or concession · no deaths')
        self.label(self.body,clock+' · Exchange '+str(f['turn']+1)+' · '+p['path']['stage']+' / '+q['path']['stage'])
        for side,name in (('player',p['name']),('enemy',q['name'])):
            r=f[side]; form=engine.active_form(f,side)
            self.label(self.body,f"{name} · Health {r['health']}/{r['max_health']} · Stamina {r['stamina']}/100 · Mana {r['energy']}/{r['max_energy']}"+
                (' · '+form['name']+f" ({r['form_until']-f['elapsed']}s)" if form else ''))
        arena=f['arena']
        self.arena_label=self.label(self.body,'Arena · '+ ' · '.join(o['name']+': '+(str(o['integrity'])+'/'+str(o['max_integrity']) if o['integrity'] else 'DESTROYED') for o in arena['objects'])+
            f" · Distance {abs(arena['positions']['player']-arena['positions']['enemy'])}"+(' · Rubble affects footing' if arena['rubble'] else ''))
        if f['status']=='active': self.opponent_intent=self.label(self.body,'Opponent intent · '+engine.describe_plan(s))
        self.transcript=self.read_panel('\n\n'.join(f['log'][-24:]) or 'Choose a learned action. Both fighters act each exchange; attacks, counters and terrain resolve before narration.',7)
        self.transcript.see('end')
        if f['status']=='finished':
            self.label(self.body,f['result']); self.button(self.row(),'Leave fight',lambda:combat.close(s)); return
        row=self.row(); self.action_kind=tk.StringVar(value=getattr(self,'saved_kind','Martial'))
        self.action_art=tk.StringVar(value=getattr(self,'saved_art','All arts'))
        self.picker(row,self.action_kind,['Martial','Unique skills','Awakened signatures','Utility'],self.populate_moves,20)
        self.picker(row,self.action_art,['All arts',*p['arts']],self.populate_moves,25)
        self.button(row,'Activate form',lambda:combat.activate_form(s))
        if p.get('technique_form')=='Conduit State': self.button(row,'Conduit State',lambda:combat.activate_form(s,form_choice='Conduit State'))
        self.button(row,'Stop spar' if f['kind']=='spar' else 'Concede',lambda:combat.concede(s))
        row=self.row(); self.move_choice=tk.StringVar(); self.amp_choice=tk.StringVar(value='None'); self.target_choice=tk.StringVar(value='Opponent')
        self.move_picker=self.picker(row,self.move_choice,[],self.populate_amps,43)
        self.amp_picker=self.picker(row,self.amp_choice,['None'],self.selection_detail,24)
        self.target_map={'Opponent':'opponent',**{o['name']+(' (wreckage)' if not o['integrity'] else ''):o['id'] for o in arena['objects'] if o['integrity']>0 or o['material']!='ground'}}
        self.picker(row,self.target_choice,list(self.target_map),self.selection_detail,24)
        self.move_detail=self.detail_panel(4)
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
        selected=moves.selection(p,move['id'],self.amp_map.get(self.amp_choice.get()))
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
        self.lesson_list=self.listbox(self.body,9)
        self.lesson_list.bind('<<ListboxSelect>>',lambda e:self.lesson_detail())
        self.lesson_description=self.label(self.body,'')
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
