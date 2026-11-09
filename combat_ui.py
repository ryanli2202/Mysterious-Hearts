"""Combat occupies the in-person stage, never a phone page or native dialog."""
import copy
import queue
import threading
import tkinter as tk
from tkinter import ttk
import combat
import combat_path as path
from combat_profiles import ARTS, TEACHERS, STATS, profile
import winterfield_ui as ui

def open_combat(game, dialogue=False):
    if game.busy: return
    if dialogue:
        from hangout_combat_ui import open_dialogue
        return open_dialogue(game)
    game.hide_phone_for_location()
    view=getattr(game,'combat_view',None)
    if view is None or not view.winfo_exists():
        view=game.combat_view=CombatView(game.presence_view.master,game)
    view.place(x=0,y=0,relwidth=1,relheight=1)
    view.lift(); view.refresh()

class CombatView(tk.Frame):
    def __init__(self,parent,game):
        super().__init__(parent,bg=ui.INK,padx=18,pady=12)
        self.game=game; self.working=False; self.mail=queue.Queue(); self.error=''
        self.title=ttk.Label(self,text='COMBAT · IN PERSON',font=('Segoe UI',20,'bold'))
        self.title.pack(anchor='w')
        self.body=tk.Frame(self,bg=ui.INK); self.body.pack(fill='both',expand=True,pady=8)
        self.status=tk.Label(self,bg=ui.INK,fg=ui.GOLD,anchor='w',wraplength=900)
        self.status.pack(fill='x')

    def label(self,parent,text):
        widget=ttk.Label(parent,text=text,wraplength=850,justify='left')
        widget.bind('<Configure>',lambda event:widget.configure(wraplength=max(100,event.width-8)))
        widget.pack(fill='x',pady=4); return widget

    def button(self,parent,text,fn):
        b=ttk.Button(parent,text=text,command=lambda:self.run(fn))
        b.pack(side='left',padx=(0,6),pady=4); return b

    def row(self,parent=None):
        f=tk.Frame(parent or self.body,bg=ui.INK); f.pack(fill='x'); return f

    def run(self,fn):
        if self.working or self.game.busy: return
        try:
            result=fn()
            if isinstance(result,str): self.error=result
            self.game.persist()
        except (ValueError,RuntimeError) as exc: self.error=str(exc)
        self.refresh()

    def async_job(self,work,commit):
        if self.working or self.game.busy: return
        original_state=self.game.state_data
        self.working=True; self.game.busy=True; self.error='Gamemaster is considering the exchange…'
        self.status.configure(text=self.error)
        def worker():
            try: self.mail.put((True,work()))
            except Exception as exc: self.mail.put((False,str(exc)))
        threading.Thread(target=worker,daemon=True).start()
        def poll():
            if not self.winfo_exists(): return
            try: ok,value=self.mail.get_nowait()
            except queue.Empty: self.after(100,poll); return
            self.working=False; self.game.busy=False
            if self.game.state_data is not original_state:
                self.error='Story changed; discarded the unfinished combat request.'; self.refresh(); return
            if ok:
                try: commit(value); self.game.persist(); self.error=''
                except (ValueError,RuntimeError) as exc: self.error=str(exc)
            else: self.error='Gamemaster unavailable: '+value+' Retry; no turn or resources were spent.'
            self.refresh()
        self.after(100,poll)

    def refresh(self):
        if self.working: return
        for child in self.body.winfo_children(): child.destroy()
        s=self.game.state_data; d=combat.ensure(s); f=d['active']
        self.status.configure(text=self.error)
        if f: self.fight(s,f)
        elif getattr(self,'path_who',None): self.render_path()
        else: self.hub(s,d)

    def hub(self,s,d):
        self.title.configure(text='COMBAT · TRAINING & CHALLENGES')
        p=profile(s,s['player'])
        self.label(self.body,'Combat stats · '+ '   |   '.join(k.replace('_',' ').title()+': '+str(p['stats'][k]) for k in STATS))
        self.label(self.body,'The Path · '+p['path']['stage']+' · Awakened power = mana potency')
        self.button(self.row(),'The Path · progression & breakthroughs',lambda:self.path_page(s['player']))
        if p['trait']: self.label(self.body,p['trait']['name']+' — '+p['trait']['description'])
        if p.get('abilities'): self.label(self.body,p['abilities'])
        self.label(self.body,'Martial arts: '+(', '.join(f'{k} {v}' for k,v in p['arts'].items()) or 'None yet; meet a teacher.'))
        if combat.recovering(s):
            self.label(self.body,f'Recovering: {combat.recovering(s)} in-game minutes remaining. No physical activities until recovered.')
            self.button(self.row(),'Rest through recovery',lambda:self.recover(s))
        else:
            row=self.row()
            self.button(row,'Hone Trait · 30 min',lambda:combat.train(s,'Trait refinement'))
            self.button(row,'Study fight IQ · 30 min',lambda:combat.train(s,'Combat analysis'))
        columns=self.row(); columns.pack_configure(fill='both',expand=True)
        columns.columnconfigure((0,1),weight=1,uniform='combat-columns'); columns.rowconfigure(0,weight=1)
        left=tk.Frame(columns,bg=ui.INK); left.grid(row=0,column=0,sticky='nsew',padx=(0,16))
        right=tk.Frame(columns,bg=ui.INK); right.grid(row=0,column=1,sticky='nsew')
        self.label(left,'Nearby opponents / teachers')
        people=[who for who in s['world']['cast'] if combat.present(s,who)]
        people+= [who for who in s['world'].get('npcs',[]) if who not in people and who!=s['player']]
        self.people=people
        self.list=tk.Listbox(left,bg=ui.CARD,fg=ui.CREAM,selectbackground=ui.EDGE,
            selectforeground=ui.CREAM,highlightthickness=0,exportselection=False,height=5)
        self.list.pack(fill='both',expand=True)
        import game_core as core
        for who in people: self.list.insert('end',core.CONTACTS.get(who,(who,))[0])
        self.list.bind('<<ListboxSelect>>',lambda e:self.teacher_options())
        if people: self.list.selection_set(0)
        row=self.row(left)
        self.button(row,'Friendly spar',lambda:self.challenge('spar'))
        self.button(row,'Agreed fight',lambda:self.challenge('challenge'))
        self.button(row,'View Path',lambda:self.path_page(self.selected()))
        ttk.Button(row,text='Attack…',command=self.attack_warning).pack(side='left',padx=4)
        self.attack_panel=tk.Frame(left,bg=ui.INK)
        self.label(right,'Learn with selected teacher / practise known art')
        self.styles=tk.Listbox(right,bg=ui.CARD,fg=ui.CREAM,selectbackground=ui.EDGE,
            selectforeground=ui.CREAM,highlightthickness=0,exportselection=False,height=5)
        self.styles.pack(fill='both',expand=True)
        self.art_detail=self.label(right,'')
        self.styles.bind('<<ListboxSelect>>',lambda e:self.describe_art())
        row=self.row(right)
        self.button(row,'Ask for a lesson · 30 min',lambda:self.training(True))
        self.button(row,'Practise alone · 30 min',lambda:self.training(False))
        self.teacher_options()
        for key,o in combat.pending_offers(s):
            row=self.row(); self.label(row,o['who']+' proposes a '+o['kind']+'.')
            self.button(row,'Accept',lambda key=key:combat.respond_offer(s,key,True))
            self.button(row,'Decline',lambda key=key:combat.respond_offer(s,key,False))
        if s['world']['location']=='iron_circle':
            if not d['ledger']:
                self.label(self.body,'Iron Circle ledger · Join at rank 450. Two cards per week; three five-minute rounds.')
                row=self.row(); self.signature=tk.Entry(row,bg=ui.CARD,fg=ui.CREAM,insertbackground=ui.CREAM)
                self.signature.pack(side='left',fill='x',expand=True)
                self.button(row,'Sign ledger',lambda:combat.sign_ledger(s,self.signature.get()))
            else:
                ready=combat.card_ready(s); ledger=d['ledger']
                import story_calendar
                due=ledger['next']; date=story_calendar.story_date(due)
                self.label(self.body,f"Iron Circle rank {ledger['rank']} · {ledger['wins']} wins / {ledger['losses']} losses · Next card {date:%a %d %b}, 18:00–21:00")
                row=self.row()
                self.button(row,'Generate opponent & enter card' if ready else 'Next card not open',self.circle)
                if not ready: self.button(row,'Wait until the next card',lambda:combat.wait_for_card(s))
        self.button(self.row(),'Return to location',self.leave)

    def selected(self):
        selection=self.list.curselection()
        if not selection: raise ValueError('Select someone who is here.')
        return self.people[selection[0]]

    def path_page(self,who):
        self.path_who=who
        self.render_path()

    def render_path(self):
        for child in self.body.winfo_children(): child.destroy()
        s=self.game.state_data; who=self.path_who; p=profile(s,who); record=p['path']
        self.title.configure(text='THE PATH · '+p['name'])
        self.label(self.body,path.summary(s,who))
        self.label(self.body,'Mana potency: '+str(p['stats']['awakened_power'])+' / 100 · Trait refinement: '+str(p['stats']['trait_refinement'])+' / 100')
        text=(path.LORE+'\n\nDormancy → Awakening: 30 strenuous encounters with latent mana. Awakening grants +18 power, +5 martial skill and +5 fight IQ; a Trait is not guaranteed.\n\n'
              'Awakening → Ascension: 15 encounters in Awakening, plus refinement 40 if you have a Trait. Mana potency stays fixed throughout Awakening.\n\n'
              'Ascension → Totality: 40 encounters in Ascension, plus refinement 80 if you have a Trait. Each strenuous encounter gives +1 mana potency, capped at 100. Totality locks further potency growth.\n\n'
              'Trait practice: each four valid, paid Trait uses in strenuous encounters give +1 refinement. Hone your Trait between fights for additional refinement.\n\n'
              'Totality → Transcendence 1: an established Trait, refinement 93+ and 30 full game days in Totality.\n\n'
              'Transcendence 1 → Transcendence 2: refinement 100 and 30 full game days in Transcendence 1. A new gamemaster-created trump card develops your existing Trait. Both stages resume encounter-based potency growth up to 100.\n\n'
              'A strenuous encounter deals at least 10 damage in total and lasts four exchanges or ends in a knockout. Wins, losses and substantial spars count; immediate concessions and guard-only sessions do not. Both fighters progress.\n\n'
              'Stage-entry boosts (power / refinement / martial skill / fight IQ): Ascension +8/+5/+4/+4; Totality +10/+5/+4/+4; Transcendence 1 +8/+0/+3/+3; Transcendence 2 +5/+0/+3/+3. Refinement boosts require a Trait. Established cast ratings already include their starting stage: no duplicate boosts.\n\n')
        if record['trump_card']:
            card=record['trump_card']; spec=path.form_spec(p)
            text=card['name']+'\n'+card['description']+'\nLimits: '+card['limitations']+f"\nActivation: {spec['cost']} mana; upkeep: {spec['upkeep']} per exchange; duration: {spec['duration']} seconds. Once per encounter.\n\n"+text
        if p.get('form')=='Conduit State': text+='Conduit State is Ivan’s Trait technique, not Transcendence. Its five-minute, once-per-day rules remain.\n\n'
        text+='Stage history:\n'+('\n'.join(x['previous']+' → '+x['stage']+' · game minute '+str(x['minute']) for x in record['history']) or 'Seeded at '+record['stage']+'; no retrospective progression awards.')
        panel=self.row(); panel.pack_configure(fill='both',expand=True)
        box=tk.Text(panel,bg=ui.PANEL,fg=ui.CREAM,wrap='word',relief='flat',font=('Segoe UI',11),height=10)
        scroll=ttk.Scrollbar(panel,command=box.yview); scroll.pack(side='right',fill='y')
        box.configure(yscrollcommand=scroll.set); box.pack(fill='both',expand=True)
        box.insert('end',text); box.configure(state='disabled')
        row=self.row()
        ready,reason=path.readiness(s,who)
        self.label(self.body,reason)
        button=ttk.Button(row,text='Attempt breakthrough · ask gamemaster' if who==s['player'] else 'Invite breakthrough attempt',command=self.breakthrough)
        button.pack(side='left',padx=4)
        if not ready or combat.recovering(s) or combat.recovering(s,who) or (who!=s['player'] and not combat.present(s,who)):
            button.configure(state='disabled')
        ttk.Button(row,text='Back to combat hub',command=self.back_from_path).pack(side='left',padx=4)

    def back_from_path(self):
        self.path_who=None; self.refresh()

    def breakthrough(self):
        s=self.game.state_data; who=self.path_who
        try: path.access(s,who)
        except ValueError as exc: self.status.configure(text=str(exc)); return
        snapshot=copy.deepcopy(s)
        self.async_job(lambda:path.generate_breakthrough(snapshot,who),lambda result:path.commit_breakthrough(s,result))

    def teacher_options(self):
        try: who=self.selected()
        except ValueError: who=None
        known=profile(self.game.state_data,self.game.state_data['player'])['arts']
        self.disciplines=list(dict.fromkeys([*TEACHERS.get(who,[]),*known]))
        self.styles.delete(0,'end')
        for art in self.disciplines: self.styles.insert('end',art)
        if self.disciplines: self.styles.selection_set(0)
        self.describe_art()

    def describe_art(self):
        choice=self.styles.curselection()
        art=self.disciplines[choice[0]] if choice else ''
        self.art_detail.configure(text=ARTS.get(art,'Combat analysis trains fight IQ: evasion, counters and bypassing counters.' if art else ''))

    def training(self,lesson):
        choice=self.styles.curselection()
        if not choice: raise ValueError('Select a discipline.')
        if lesson:
            from hangout_combat_ui import open_dialogue
            return open_dialogue(self.game,self.selected(),self.disciplines[choice[0]])
        return combat.train(self.game.state_data,self.disciplines[choice[0]])

    def challenge(self,kind):
        return self.begin_dialogue(self.selected())

    def attack_warning(self):
        try: who=self.selected()
        except ValueError as exc: self.status.configure(text=str(exc)); return
        for w in self.attack_panel.winfo_children(): w.destroy()
        self.attack_panel.pack(fill='x')
        self.label(self.attack_panel,'Attack '+who+' without consent? This permanently destroys the relationship, harms ties with their allies, and may cause expulsion or diplomatic damage.')
        self.button(self.attack_panel,'Open dialogue',lambda:self.begin_dialogue(who))
        self.button(self.attack_panel,'Cancel',self.attack_panel.pack_forget)
        # run() normally rebuilds; preserve this inline review panel.
        self.error='Attack requires the explicit confirmation below.'

    def begin_dialogue(self,who):
        from hangout_combat_ui import open_dialogue
        return open_dialogue(self.game,who)

    def circle(self):
        s=self.game.state_data
        if not combat.card_ready(s): raise ValueError('Return during the next card, 18:00–21:00.')
        snapshot=copy.deepcopy(s)
        self.async_job(lambda:combat.generate_opponent(snapshot),lambda p:combat.start(s,'circle:'+p['name'],'circle',p))

    def fight(self,s,f):
        q=f['opponent_profile']; self.title.configure(text=f['kind'].upper()+' · '+q['name'])
        if f['kind']=='circle':
            remaining=max(0,300-f['elapsed']%300) if f['status']=='active' else 0
            self.label(self.body,f"Round {min(3,f['elapsed']//300+1)} / 3 · {remaining//60}:{remaining%60:02d} remaining · Each response advances 30 seconds")
        else: self.label(self.body,'Untimed encounter · '+('Practice has no winner or loser; stop at any time.' if f['kind']=='spar' else 'Ends at knockout or concession. No deaths.'))
        self.label(self.body,'Opponent: '+' | '.join(k.replace('_',' ')+': '+str(q['stats'][k]) for k in STATS)+' · '+', '.join(q['arts']))
        if q['trait']: self.label(self.body,q['trait']['name']+' — '+q['trait']['description'])
        self.label(self.body,'Path: you — '+profile(s,s['player'])['path']['stage']+' · opponent — '+q['path']['stage'])
        for side,label in (('player','You'),('enemy',q['name'])):
            r=f[side]
            self.label(self.body,f"{label}  •  Health {r['health']}/{r['max_health']}  •  Stamina {r['stamina']}/100  •  Awakened energy {r['energy']}/{r['max_energy']}")
            if r.get('active_form') and r['form_until']>f['elapsed']:
                self.label(self.body,r['active_form']['name']+f" · {r['form_until']-f['elapsed']} seconds remaining · {r['active_form']['upkeep']} mana per exchange")
        if f.get('ally_resources'):
            r=f['ally_resources']
            self.label(self.body,f"Field partner {f['ally_profile']['name']} · Health {r['health']}/{r['max_health']} · Mana {r['energy']}/{r['max_energy']} · Stamina {r['stamina']}/100")
        if f['status']=='active':
            plan,_=combat.tactics.prepare(s)
            self.opponent_intent=self.label(self.body,'Opponent intent · '+combat.tactics.describe(plan,f))
        transcript=tk.Text(self.body,bg=ui.PANEL,fg=ui.CREAM,wrap='word',height=8,relief='flat',font=('Segoe UI',11))
        transcript.pack(fill='both',expand=True,pady=6)
        transcript.insert('end','\n\n'.join(f['log'][-30:]) or 'The opponent is already preparing their move. Describe your defence and intended attack. Each submission resolves both actions, including when you guard or recover.')
        transcript.configure(state='disabled'); transcript.see('end')
        if f['status']=='finished':
            self.label(self.body,f['result'])
            self.button(self.row(),'Leave fight',lambda:combat.close(s)); return
        row=self.row(); self.mode=tk.StringVar(value=getattr(self,'draft_mode','Martial')); self.style=tk.StringVar(value=getattr(self,'draft_style',next(iter(profile(s,s['player'])['arts']),'Untrained')))
        ttk.Combobox(row,textvariable=self.mode,values=['Martial','Trait','Guard','Recover'],state='readonly',width=12).pack(side='left',padx=4)
        ttk.Combobox(row,textvariable=self.style,values=['Untrained',*profile(s,s['player'])['arts']],state='readonly',width=25).pack(side='left',padx=4)
        self.button(row,'Activate advanced form',lambda:combat.activate_form(s))
        p=profile(s,s['player'])
        if p.get('technique_form')=='Conduit State' and p['path']['stage'] in (path.TRANSCENDENCE_1,path.TRANSCENDENCE_2):
            self.button(row,'Conduit State',lambda:combat.activate_form(s,form_choice='Conduit State'))
        self.button(row,'Stop practice' if f['kind']=='spar' else 'Concede',lambda:combat.concede(s))
        self.action=tk.Text(self.body,bg=ui.CARD,fg=ui.CREAM,insertbackground=ui.CREAM,height=3,wrap='word')
        self.action.pack(fill='x',pady=4)
        self.action.insert('1.0',getattr(self,'draft',''))
        self.button(self.row(),'Submit defence / attack to gamemaster',self.submit)

    def submit(self):
        s=self.game.state_data; action=self.action.get('1.0','end').strip(); style=self.style.get(); mode=self.mode.get()
        if not action: raise ValueError('Describe your intended move first.')
        self.draft=action
        self.draft_mode=mode; self.draft_style=style
        snapshot=copy.deepcopy(s)
        def commit(result):
            combat.commit_turn(s,result); self.draft=''
        self.async_job(lambda:combat.adjudicate(snapshot,action,style,mode),commit)

    def recover(self,s):
        import world_loop
        world_loop.advance(s,combat.recovering(s))
        return 'Recovery complete.'

    def leave(self):
        if combat.active(self.game.state_data): raise ValueError('Finish this fight first.')
        self.place_forget(); self.game.render()
