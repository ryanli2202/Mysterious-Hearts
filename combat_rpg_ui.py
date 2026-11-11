"""MH-007 in-person arena. Presentation reads the authoritative combat engine."""
import copy
import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont
from PIL import Image, ImageOps, ImageTk
import combat
import combat_engine as engine
import combat_moves as moves
import combat_states as states
import combat_objectives as objectives
import combat_identity as identity
import combat_portraits
from combat_profiles import profile
from artwork import source_image, scene_art
import winterfield_ui as ui
import combat_style as style

CATEGORIES = {'Martial': 'martial', 'Unique skills': 'unique',
              'Awakened signatures': 'signature', 'Utility': 'utility'}


def preferences(s):
    raw = s.get('combat', {}).get('ui_preferences', {}).get(s['player'], {})
    if not isinstance(raw, dict): raw = {}
    favourites = raw.get('favourites', [])
    return dict(density=raw.get('density') if raw.get('density') in ('Detailed', 'Cinematic') else 'Detailed',
                text_size=raw.get('text_size') if raw.get('text_size') in (10, 12, 14) else 10,
                hints_dismissed=raw.get('hints_dismissed') is True,
                favourites=[x for x in favourites if isinstance(x, str)][:6] if isinstance(favourites, list) else [])


def resource_snapshot(f):
    return {side: copy.deepcopy(f[side]) for side in ('player', 'enemy', 'ally_resources') if side in f}


def breakdown(f):
    if not f.get('exchanges'): return 'No exchange has resolved yet.'
    exchange = f['exchanges'][-1]
    lines = [f"EXCHANGE {exchange['turn'] + 1}"]
    for r in exchange['records']:
        lines.append(f"\n{r['name']} · {r['move']}\n{r['outcome']} · {r['damage']} damage · "
                     f"{r['hits']}/{r['beats']} hits\nPaid {r['stamina']} stamina / {r['mana']} mana")
        lines.extend(r.get('terrain', []))
    for support in f.get('support_exchanges', []):
        if support.get('turn') != exchange['turn']: continue
        lines.append('\nFIELD PARTNER EXCHANGE')
        for r in support['records']:
            if r.get('outcome') == 'waiting': continue
            lines.append(f"{r['name']} · {r['move']} · {r['outcome']} · {r['damage']} damage")
            lines.extend(r.get('terrain', []))
    audit = exchange.get('ui_resource_audit')
    if audit:
        for side, before in audit['before'].items():
            after = audit['after'].get(side, before)
            changes = [f"{label}: {before.get(key, 0)} → {after.get(key, 0)}"
                       for key, label in (('health', 'Health'), ('stamina', 'Stamina'), ('energy', 'Mana'))]
            lines.append('\n' + {'player': 'You', 'enemy': 'Opponent', 'ally_resources': 'Partner'}[side]
                         + ' · net exchange changes\n' + '\n'.join(changes))
            for key in ('restrained', 'staggered', 'focus', 'protocol_left', 'war_momentum', 'channel',
                        'endurance_left', 'soul_damage', 'endurance_debt', 'active_form'):
                if before.get(key) != after.get(key):
                    def display(v): return v.get('name', 'None') if isinstance(v, dict) else str(v or 'None')
                    lines.append(key.replace('_', ' ').title() + ': ' + display(before.get(key)) + ' → ' + display(after.get(key)))
    else:
        lines.append('\nThis older exchange has no saved resource snapshots. Recorded outcomes and costs are shown above.')
    return '\n'.join(lines)


def inspection(s, f, side):
    own = side == 'player'
    p = profile(s, s['player']) if own else f['opponent_profile']
    who = s['player'] if own else f['opponent']
    r = f[side]
    public = identity.public(s, who, [s['player']], p)
    parts = [p['name'], public['title'], states.status(p, r) or 'No active special states.']
    for key,description in (('restrained','Movement restricted'),('staggered','Balance disrupted'),('focus','Prepared focus')):
        if r.get(key): parts.append(f"{description}: {r[key]} exchange(s) remaining.")
    form = engine.active_form(f, side)
    if form: parts.append(f"Active form: {form['name']} · {max(0, r['form_until'] - f['elapsed'])} seconds")
    if own:
        parts.append(identity.ability_details(p))
    else:
        seen = s.get('combat', {}).get('recognition', {}).get(s['player'], {}).get(who, {}).get('observed_actions', [])
        known = [m for m in moves.actions(copy.deepcopy(p)) if m['id'] in seen]
        parts.append('Observed techniques only; undisclosed abilities and identity links remain hidden.')
        parts.extend(moves.details(m) for m in known)
        if not known: parts.append('No techniques observed yet.')
    return '\n\n'.join(x for x in parts if x)


class RPGCombat:
    def rpg_text(self, parent, text='', colour=None, **kwargs):
        widget = tk.Label(parent, text=text, bg=ui.PANEL, fg=colour or ui.CREAM,
                          font=('Segoe UI', self.ui_prefs['text_size']), anchor='w', justify='left', **kwargs)
        widget.bind('<Configure>', lambda e: widget.configure(wraplength=max(80, e.width-12)))
        return widget

    def rpg_button(self, parent, text, command):
        widget = tk.Button(parent, text=text, command=command, bg=ui.CARD, fg=ui.CREAM,
                         activebackground=ui.EDGE, activeforeground=ui.CREAM, disabledforeground=ui.MUTED,
                         font=('Segoe UI', self.ui_prefs['text_size']), relief='flat', padx=8, pady=2,
                         highlightthickness=1, highlightbackground=ui.EDGE, highlightcolor=ui.GOLD)
        widget.bind('<Return>',lambda e:(widget.invoke(),'break')[-1])
        widget.bind('<Escape>',lambda e:self.close_rpg_drawer())
        return widget

    def close_rpg_drawer(self):
        panel=getattr(self,'rpg_drawer',None)
        if panel is not None and panel.winfo_exists(): panel.destroy()
        previous=getattr(self,'rpg_restore_focus',None)
        if previous is not None and previous.winfo_exists(): previous.focus_set()
        return 'break'

    def save_ui(self, **updates):
        s = self.game.state_data
        prefs = preferences(s); prefs.update(updates)
        s.setdefault('combat', {}).setdefault('ui_preferences', {})[s['player']] = prefs
        self.ui_prefs = prefs
        self.game.persist()

    def ui_setting(self, **updates):
        self.save_ui(**updates); self.refresh()

    def drawer(self, title, text):
        old = getattr(self, 'rpg_drawer', None)
        if old is not None and old.winfo_exists(): old.destroy()
        previous = self.focus_get()
        self.rpg_restore_focus=previous
        panel = self.rpg_drawer = style.Panel(self.body, bg=ui.PANEL, padx=14, pady=12,
                                          highlightbackground=ui.GOLD, highlightthickness=1)
        panel.place(relx=.04, rely=.02, relwidth=.92, relheight=.94); panel.lift()
        def close():
            panel.destroy()
            if previous is not None and previous.winfo_exists(): previous.focus_set()
        self.rpg_button(panel, 'Close · Esc', close).pack(anchor='e')
        self.rpg_text(panel, title, ui.GOLD).pack(fill='x', pady=6)
        box = tk.Text(panel, bg=ui.CARD, fg=ui.CREAM, insertbackground=ui.CREAM, relief='flat', wrap='word',
                      font=('Segoe UI', self.ui_prefs['text_size']), padx=12, pady=10)
        scroll = ttk.Scrollbar(panel, command=box.yview); scroll.pack(side='right', fill='y')
        box.configure(yscrollcommand=scroll.set); box.pack(fill='both', expand=True)
        box.insert('end', text); box.configure(state='disabled')
        box.bind('<Escape>', lambda e: close()); panel.bind('<Escape>', lambda e: close()); box.focus_set()
        return panel

    def inspect_fighter(self, side):
        f = combat.active(self.game.state_data)
        if f: self.drawer('FIGHTER INSPECTION', inspection(self.game.state_data, f, side))

    def terrain_text(self, f):
        arena = f['arena']
        text = f"Distance {abs(arena['positions']['player']-arena['positions']['enemy'])} · "
        text += ' · '.join(o['name']+f" {o['integrity']}/{o['max_integrity']}" for o in arena['objects'])
        if arena['rubble']: text += '\nRubble affects footing.'
        if f.get('ally_resources'):
            r = f['ally_resources']
            text += f"\nPartner {f['ally_profile']['name']} · Health {r['health']}/{r['max_health']} · Stamina {r['stamina']} · Mana {r['energy']} · Position {arena['positions'].get('ally', 1)}"
            text += '\n' + states.status(f['ally_profile'], r)
        return text

    def fight(self, s, f):
        engine.ensure_arena(f)
        self.ui_prefs = preferences(s); self.rpg_fight = f; self.rpg_ghost = {}
        self.rpg_drawer = None
        p = profile(s, s['player']); q = f['opponent_profile']
        self.title.configure(text=('BOSS' if q.get('boss') else f['kind'].upper())+' · '+q['name'][:55], font=('Segoe UI', 16, 'bold'))
        # Bottom dock is reserved first so it remains reachable in compact windows.
        dock = style.Panel(self.body, bg=ui.PANEL, padx=8, pady=3)
        dock.pack(side='bottom', fill='x')
        top = tk.Frame(self.body, bg=ui.PANEL); top.pack(fill='x')
        self.phase_label = self.rpg_text(top, 'FINISHED' if f['status']=='finished' else 'CHOOSE ACTION', ui.GOLD, width=19)
        self.phase_label.pack(side='left', padx=6)
        self.rpg_button(top, 'History', lambda: self.drawer('COMBAT HISTORY', '\n\n'.join(f['log']) or 'No exchanges yet.')).pack(side='right')
        self.rpg_button(top, 'Breakdown', lambda: self.drawer('LAST EXCHANGE', breakdown(f))).pack(side='right')
        self.rpg_button(top, 'Display / help', self.display_settings).pack(side='right')
        self.rpg_button(top, 'Tactics', self.toggle_tactics).pack(side='right')
        clock = f"Round {min(3, f['elapsed']//300+1)}/3 · {max(0,900-f['elapsed'])}s remaining" if f['kind']=='circle' else 'Both fighters act each exchange'
        self.objective_label = self.rpg_text(self.body, f"{f['location'].replace('_',' ').title()} · Exchange {f['turn']+1} · {clock}\n" + objectives.description(f))
        self.objective_label.pack(fill='x')
        # Latest narration has a fixed height; the entire history lives in a drawer.
        self.transcript = tk.Text(self.body, height=1 if self.ui_prefs['density']=='Cinematic' or self.ui_prefs['text_size']>10 else 2, wrap='word', bg=ui.PANEL, fg=ui.CREAM,
                                  relief='flat', font=('Segoe UI', self.ui_prefs['text_size']), padx=10, pady=2)
        self.transcript.pack(side='bottom', fill='x', pady=(4, 0))
        self.transcript.insert('end', f['log'][-1] if f['log'] else 'Select a technique, choose its target, then resolve the exchange.')
        self.transcript.configure(state='disabled')
        self.opponent_intent = self.rpg_text(self.body, 'Opponent intent · '+engine.describe_plan(s) if f['status']=='active' else f.get('result', ''), ui.GOLD)
        self.opponent_intent.pack(side='bottom', fill='x')
        self.build_stage(s, f)
        if f['status']=='finished':
            self.rpg_text(dock, f.get('result', 'Encounter finished'), ui.GOLD).pack(fill='x')
            self.rpg_button(dock, 'Return to location', lambda: self.run(self.close_encounter)).pack(side='right')
            return
        self.build_commands(dock, s, f, p)

    def build_stage(self, s, f):
        self.combat_portrait_images = {}; self.combat_hud = {}; self.stage_panels = []; self.stage_items = []
        self.combat_portrait_rail = stage = tk.Canvas(self.body, bg=ui.INK, height=400, highlightthickness=1,
                                                     highlightbackground=ui.GOLD if f['opponent_profile'].get('boss') else ui.EDGE)
        stage.pack(fill='both', expand=True, pady=3)
        self.stage_background = stage.create_image(0, 0, anchor='nw')
        self.portrait_items = {}
        for side, who, p in (('player', s['player'], profile(s, s['player'])), ('enemy', f['opponent'], f['opponent_profile'])):
            item = stage.create_image(0, 0, anchor='s'); self.stage_items.append(item); self.portrait_items[who] = item
            stage.tag_bind(item, '<Button-1>', lambda e, side=side: self.inspect_fighter(side))
            panel = style.Panel(stage, bg=ui.PANEL, padx=7, pady=2)
            self.stage_panels.append(stage.create_window(0, 0, window=panel, anchor='nw'))
            name_limit=16 if self.ui_prefs['text_size']>10 else 22
            short_name=p['name'][:name_limit]+('…' if len(p['name'])>name_limit else '')
            prefix=('YOU · ' if side=='player' else 'OPPONENT · ') if self.ui_prefs['text_size']==10 else ''
            name = self.rpg_button(panel, prefix+short_name, lambda side=side: self.inspect_fighter(side))
            name.pack(fill='x'); name.bind('<Configure>', lambda e,w=name: w.configure(wraplength=max(50,e.width-12)))
            public = identity.public(s, who, [s['player']], p)
            if public['title'] and self.ui_prefs['density']=='Detailed' and self.ui_prefs['text_size']==10:
                self.rpg_text(panel, public['title'], ui.GOLD).pack(fill='x')
            self.combat_hud[side] = {}
            for key in ('health', 'stamina', 'energy'):
                bar = tk.Canvas(panel, height=self.ui_prefs['text_size']+12, bg=ui.CARD, highlightthickness=0)
                bar.pack(fill='x', pady=2); self.combat_hud[side][key] = bar
                bar.bind('<Configure>', lambda e,side=side,key=key: self.draw_bar(side,key))
            form = engine.active_form(f, side)
            state = form['name']+f" · {max(0,f[side]['form_until']-f['elapsed'])}s" if form else p['path']['stage']
            status = states.status(p, f[side])
            if status or any(f[side].get(key) for key in ('restrained','staggered','focus')):
                state += '\nStates active · inspect fighter'
            if p.get('boss'):
                intent = __import__('combat_boss').intent(p, f)
                state += '\nEquipped boss' + (' · '+{'target':'Targeting', 'burst':'Committed burst', 'recover':'Recovery opening', 'ram':'Committed ram'}[intent] if intent else '')
            if self.ui_prefs['text_size']>10:
                state = ('Form · '+str(max(0,f[side]['form_until']-f['elapsed']))+'s · inspect' if form else
                         'States · inspect' if '\n' in state else state)
            label = self.rpg_text(panel, state, ui.MUTED); label.pack(fill='x')
        stage.bind('<Configure>', self.paint_stage)

    def draw_bar(self, side, key):
        f = self.rpg_fight; r = f[side]; bar = self.combat_hud[side][key]
        width = max(1, bar.winfo_width()); height = int(bar['height']); value = r[key]
        limit = r.get({'health':'max_health','energy':'max_energy'}.get(key,''),100)
        colour = {'health':'#c7687d','stamina':'#60bca6','energy':'#72a8da'}[key]
        bar.delete('all'); end = width*max(0,min(1,value/max(1,limit)))
        bar.create_rectangle(0,0,end,height,fill=colour,outline='')
        for x in range(0, int(end), 10):
            bar.create_line(x,height-3,min(end,x+7),height-3,fill=ui.PANEL)
        cost = self.rpg_ghost.get(key,0) if side=='player' else 0
        if cost:
            start = width*max(0,min(1,(value-cost)/max(1,limit)))
            bar.create_rectangle(start,0,end,height,fill=ui.GOLD,stipple='gray50',outline=ui.GOLD)
        label = {'health':'HP','stamina':'STA','energy':'MANA'}[key]+f' {value}/{limit}'
        if cost and self.ui_prefs['text_size']==10: label += f'  −{cost} preview'
        label_width=tkfont.Font(family='Segoe UI',size=self.ui_prefs['text_size']).measure(label)+10
        bar.create_rectangle(2,2,min(width-2,label_width),height-2,fill=ui.PANEL,outline='')
        # Keep a visible preview strip below the number backing.
        if cost: bar.create_rectangle(start,height-4,end,height,fill=ui.GOLD,stipple='gray50',outline='')
        bar.create_text(5,height/2,text=label,fill=ui.CREAM,anchor='w',font=('Segoe UI',self.ui_prefs['text_size']))

    def paint_stage(self, event=None):
        stage = self.combat_portrait_rail
        if not stage.winfo_exists(): return
        w,h = max(1,stage.winfo_width()),max(1,stage.winfo_height())
        if w<100 or h<60: return
        f = self.rpg_fight; s = self.game.state_data
        scene = ImageOps.fit(source_image(scene_art(f['location'],minute=s['world']['minute'])).convert('RGB'),(w,h))
        scene = Image.blend(scene,Image.new('RGB',(w,h),ui.INK),.22)
        self.combat_stage_background = ImageTk.PhotoImage(scene,master=self.game)
        stage.itemconfigure(self.stage_background,image=self.combat_stage_background)
        pw = max(80,int(w*.26)); ph = max(60,min(620,h-12))
        panel_w = max(140,min(260,int(w*.23)))
        photos = combat_portraits.group(self.game,
            {s['player']:(pw,ph),f['opponent']:(pw,ph)},f['location'],s['world']['minute'])
        for index,(side,who) in enumerate((('player',s['player']),('opponent',f['opponent']))):
            try: photo = photos[who]
            except (OSError,ValueError): photo = ImageTk.PhotoImage(Image.new('RGBA',(pw,ph)),master=self.game)
            self.combat_portrait_images[side] = photo
            stage.itemconfigure(self.stage_items[index],image=photo)
            stage.coords(self.stage_items[index],w*.14 if index==0 else w*.86,h-6)
            stage.coords(self.stage_panels[index],w*.275 if index==0 else w*.725-panel_w,8)
            stage.itemconfigure(self.stage_panels[index],width=panel_w)
        self.opponent_portrait = self.combat_portrait_images['opponent']
        stage.delete('target'); stage.delete('tactics')
        target = getattr(self,'target_choice',None)
        if f['status']=='active' and target and target.get()=='Opponent':
            stage.create_rectangle(w*.73,4,w-5,h-3,outline=ui.GOLD,width=2,tags='target')
            stage.create_text(w*.86,h-15,text='SELECTED TARGET',fill=ui.GOLD,font=('Segoe UI',10,'bold'),tags='target')
        elif f['status']=='active' and target:
            stage.create_rectangle(w*.28,h-38,w*.72,h-5,fill=ui.PANEL,outline=ui.GOLD,tags='target')
            stage.create_text(w*.5,h-22,text='TARGET · '+target.get(),fill=ui.GOLD,width=w*.42,font=('Segoe UI',10,'bold'),tags='target')
        if getattr(self,'tactics_visible',False):
            text = self.terrain_text(f)
            stage.create_rectangle(6,max(0,h-100),w-6,h-4,fill=ui.PANEL,outline=ui.EDGE,tags='tactics')
            stage.create_text(16,h-95,text=text,fill=ui.CREAM,anchor='nw',width=w-32,font=('Segoe UI',self.ui_prefs['text_size']),tags='tactics')

    def toggle_tactics(self):
        self.tactics_visible = not getattr(self,'tactics_visible',False); self.paint_stage()

    def build_commands(self, dock, s, f, p):
        tabs = tk.Frame(dock,bg=ui.PANEL); tabs.pack(fill='x')
        self.action_kind = tk.StringVar(value=getattr(self,'saved_kind','Martial'))
        self.action_art = tk.StringVar(value=getattr(self,'saved_art','All arts'))
        self.category_buttons = {}
        for kind in CATEGORIES:
            b = self.rpg_button(tabs,kind,lambda kind=kind:self.select_category(kind)); b.pack(side='left',padx=2)
            self.category_buttons[kind] = b
        self.rpg_button(tabs,'Forms / rules',self.combat_options).pack(side='right')
        selection = tk.Frame(dock,bg=ui.PANEL); selection.pack(fill='x',pady=3)
        self.move_choice=tk.StringVar(); self.amp_choice=tk.StringVar(value='None'); self.target_choice=tk.StringVar(value='Opponent')
        # Existing combobox variables remain the authoritative draft and support saved UI/test callers.
        self.move_picker=ttk.Combobox(selection,textvariable=self.move_choice,state='readonly',font=('Segoe UI',self.ui_prefs['text_size']))
        self.move_picker.bind('<<ComboboxSelected>>',lambda e:self.populate_amps())
        self.amp_map={'None':None}
        self.amp_picker=ttk.Combobox(selection,textvariable=self.amp_choice,state='readonly',width=18,font=('Segoe UI',self.ui_prefs['text_size']))
        self.amp_picker.bind('<<ComboboxSelected>>',lambda e:self.selection_detail())
        self.target_map={'Opponent':'opponent',**{o['name']+(' (wreckage)' if not o['integrity'] else ''):o['id'] for o in f['arena']['objects'] if o['integrity']>0 or o['material']!='ground'}}
        target=ttk.Combobox(selection,textvariable=self.target_choice,values=list(self.target_map),state='readonly',width=22,font=('Segoe UI',self.ui_prefs['text_size']))
        target.bind('<<ComboboxSelected>>',lambda e:self.selection_detail())
        for col,(label,widget) in enumerate((('Technique',self.move_picker),('Amplification',self.amp_picker),('Target',target))):
            selection.columnconfigure(col,weight=2 if col==0 else 1)
            self.rpg_text(selection,label,ui.MUTED).grid(row=0,column=col,sticky='ew',padx=3)
            widget.grid(row=1,column=col,sticky='ew',padx=3)
        # Slots live in a drawer so six pins cannot displace the resource HUD at larger text sizes.
        self.move_detail=tk.Text(dock,height=2,wrap='word',bg=ui.CARD,fg=ui.CREAM,relief='flat',font=('Segoe UI',self.ui_prefs['text_size']),padx=7)
        self.move_detail.pack(fill='x',pady=3)
        footer=tk.Frame(dock,bg=ui.PANEL); footer.pack(fill='x')
        self.execute_button=self.rpg_button(footer,'RESOLVE EXCHANGE',lambda:self.run(self.submit)); self.execute_button.configure(bg='#315d58',activebackground='#417b70',fg=ui.CREAM,font=('Segoe UI',self.ui_prefs['text_size'],'bold')); self.execute_button.pack(side='right')
        self.rpg_button(footer,'Moves',self.technique_cards).pack(side='left')
        self.rpg_button(footer,'Details',self.show_move_details).pack(side='left')
        self.favourite_button=self.rpg_button(footer,'☆ Pin move',self.toggle_favourite); self.favourite_button.pack(side='left',padx=4)
        self.rpg_button(footer,'Quick slots',self.quick_slots).pack(side='left')
        self.availability_label=self.rpg_text(footer,'',ui.GOLD); self.availability_label.pack(side='left',fill='x',expand=True)
        self.populate_moves()
        if not self.ui_prefs['hints_dismissed'] and self.selected_action and str(self.execute_button['state'])=='normal':
            self.availability_label.configure(text='Tip: select → target → resolve. Display / help for a guide.')

    def select_category(self, kind):
        self.action_kind.set(kind); self.populate_moves()
        self.technique_cards()

    def technique_cards(self):
        panel=self.drawer(self.action_kind.get().upper()+' · CHOOSE A TECHNIQUE', '')
        # Replace the drawer's reading area with a scrolling, keyboard-accessible card catalogue.
        for child in panel.winfo_children()[2:]: child.destroy()
        canvas=tk.Canvas(panel,bg=ui.PANEL,highlightthickness=0)
        scroll=ttk.Scrollbar(panel,command=canvas.yview); scroll.pack(side='right',fill='y')
        canvas.configure(yscrollcommand=scroll.set); canvas.pack(fill='both',expand=True)
        cards=tk.Frame(canvas,bg=ui.PANEL); item=canvas.create_window(0,0,window=cards,anchor='nw')
        canvas.bind('<Configure>',lambda e:canvas.itemconfigure(item,width=e.width))
        cards.bind('<Configure>',lambda e:canvas.configure(scrollregion=canvas.bbox('all')))
        s=self.game.state_data; f=combat.active(s); p=profile(s,s['player']); projected,_=engine.preview(s)
        if not self.move_map: self.rpg_text(cards,'No learned techniques in this category. Utility remains available.').pack(fill='x')
        first=None
        for name,m in self.move_map.items():
            action=states.prepare_action(p,f['player'],moves.selection(p,m['id']))
            available=moves.can_pay(projected['player'],action)
            text=f"{m['name']} · {m['role']}\n{action['stamina']} stamina / {action['mana']} mana · Range {action['range']}"
            text+='\n'+m['description']
            if not available: text+='\nUnavailable: insufficient resources after form upkeep.'
            def choose(name=name):
                self.move_choice.set(name); self.populate_amps(); panel.destroy(); self.execute_button.focus_set()
            card=self.rpg_button(cards,text,choose); card.configure(anchor='w',justify='left',pady=10)
            card.pack(fill='x',pady=4)
            if name==self.move_choice.get(): card.configure(highlightbackground=ui.GOLD,highlightthickness=2)
            card.bind('<Configure>',lambda e,w=card:w.configure(wraplength=max(80,e.width-20)))
            def focus(e,w=card):
                canvas.yview_moveto(w.winfo_y()/max(1,cards.winfo_height()))
            card.bind('<FocusIn>',focus)
            card.bind('<MouseWheel>',lambda e:canvas.yview_scroll(-int(e.delta/120),'units'))
            card.bind('<Escape>',lambda e:panel.destroy())
            if first is None: first=card
        if first: first.focus_set()

    def populate_moves(self):
        super().populate_moves()
        if hasattr(self,'category_buttons'):
            for kind,b in self.category_buttons.items(): b.configure(bg=ui.EDGE if kind==self.action_kind.get() else ui.CARD)

    def quick_slots(self):
        panel=self.drawer('FAVOURITE MOVES · SIX QUICK SLOTS','Pin a learned move from the command dock. Slots select a move; they never resolve an exchange. Unavailable learned moves remain pinned until cleared.')
        row=tk.Frame(panel,bg=ui.PANEL); row.pack(fill='x',before=panel.winfo_children()[2])
        p=profile(self.game.state_data,self.game.state_data['player'])
        known={m['id']:m for m in moves.actions(p)}
        for index,ident in enumerate(self.ui_prefs['favourites']):
            m=known.get(ident)
            def choose(ident=ident):
                self.choose_favourite(ident); panel.destroy(); self.execute_button.focus_set()
            button=self.rpg_button(row,f'{index+1} · '+(m['name'] if m else 'Unavailable move'),choose)
            button.pack(fill='x',pady=3)
            if not m: button.configure(state='disabled')
        self.rpg_button(row,'Clear all pins',lambda:(self.clear_favourites(),panel.destroy())).pack(anchor='w')

    def clear_favourites(self):
        self.save_ui(favourites=[]); self.selection_detail()

    def choose_favourite(self, ident):
        p=profile(self.game.state_data,self.game.state_data['player'])
        m=next((m for m in moves.actions(p) if m['id']==ident),None)
        if not m: return
        self.action_kind.set(next(k for k,v in CATEGORIES.items() if v==m['kind'])); self.action_art.set('All arts')
        self.populate_moves()
        self.move_choice.set(next(name for name,move in self.move_map.items() if move['id']==ident)); self.populate_amps()

    def toggle_favourite(self):
        m=self.move_map.get(self.move_choice.get())
        if not m: return
        ids=list(self.ui_prefs['favourites'])
        if m['id'] in ids: ids.remove(m['id'])
        elif len(ids)<6: ids.append(m['id'])
        else:
            self.drawer('QUICK SLOTS FULL','Unpin a move or clear pins before adding another. Six slots are available.'); return
        self.save_ui(favourites=ids); self.selection_detail()

    def selection_detail(self):
        s=self.game.state_data; f=combat.active(s); p=profile(s,s['player'])
        m=self.move_map.get(self.move_choice.get()); self.rpg_ghost={}; self.selected_action=None
        reason='No learned moves in this category. Choose Utility or visit training.'
        if m:
            selected=states.prepare_action(p,f['player'],moves.selection(p,m['id'],self.amp_map.get(self.amp_choice.get())))
            self.selected_action=selected
            projected,_=engine.preview(s)
            reason='' if moves.can_pay(projected['player'],selected) else 'Insufficient resources after form upkeep.'
            target=self.target_map.get(self.target_choice.get())
            obj=engine.object_at(f,target)
            if target is None: reason='Choose a valid target.'
            elif 'cover' in selected['tags'] and (not obj or not obj['cover'] or obj['integrity']<=0): reason='Select intact cover as the target.'
            self.rpg_ghost={key:max(0,f['player'][key]-projected['player'][key])+selected.get(cost,0)
                            for key,cost in (('health','health_cost'),('stamina','stamina'),('energy','mana'))}
            text=f"{selected['name']} → {self.target_choice.get()} · {selected['role']}\nStamina {selected['stamina']} · Mana {selected['mana']} · Blood {selected.get('health_cost',0)} · Range {selected['range']} · Preview includes form upkeep; recovery/hits are not guaranteed."
            self.favourite_button.configure(text='★ Unpin move' if m['id'] in self.ui_prefs['favourites'] else '☆ Pin move',state='normal')
        else:
            text=reason; self.favourite_button.configure(state='disabled')
        self.set_detail(self.move_detail,text)
        self.availability_label.configure(text=reason or 'Ready · selection spends nothing')
        self.execute_button.configure(state='disabled' if reason or self.working or self.game.busy else 'normal')
        for side,bars in self.combat_hud.items():
            for key in bars: self.draw_bar(side,key)
        self.paint_stage()

    def show_move_details(self):
        if self.selected_action:
            detail=moves.details(self.selected_action)
            amp=self.selected_action.get('amplification')
            if amp:
                from combat_profiles import profile
                p=profile(self.game.state_data,self.game.state_data['player'])
                comparison=__import__('creator_combat').interaction(p,self.selected_action['id'],amp['id'])
                base=comparison['base']; changed=comparison['amplified']
                detail+=f"\n\nWithout / with amplification: mana {base['mana']} / {changed['mana']}; stamina {base['stamina']} / {changed['stamina']}; range {base['range']} / {changed['range']}.\nSupported environment: "+comparison['environment']+'\n'+comparison['note']
            self.drawer('SELECTED TECHNIQUE',detail)

    def display_settings(self):
        panel=self.drawer('DISPLAY & FIRST-FIGHT GUIDE',
            '1. Choose a category and learned technique.\n2. Select amplification and a target; terrain can be targeted too.\n3. Review costs and availability, then resolve. Both fighters act in the same exchange.\n\nGold hatching previews costs including form upkeep, not damage or guaranteed recovery. Selecting, pinning and inspecting never spends resources.\n\nClick either portrait or its name to inspect. Tactics shows terrain and partners; History and Breakdown review resolved outcomes. Tab and Enter operate controls; Escape closes drawers.')
        row=tk.Frame(panel,bg=ui.PANEL); row.pack(fill='x',before=panel.winfo_children()[2])
        for col,density in enumerate(('Detailed','Cinematic')):
            self.rpg_button(row,density,lambda density=density:self.ui_setting(density=density)).grid(row=0,column=col,sticky='ew')
        for col,size in enumerate((10,12,14)): self.rpg_button(row,f'Text {size}',lambda size=size:self.ui_setting(text_size=size)).grid(row=1,column=col,sticky='ew')
        self.rpg_button(row,'Dismiss hints' if not self.ui_prefs['hints_dismissed'] else 'Restore hints',
                         lambda:self.ui_setting(hints_dismissed=not self.ui_prefs['hints_dismissed'])).grid(row=0,column=2,sticky='ew')

    def combat_options(self):
        s=self.game.state_data; f=combat.active(s); p=profile(s,s['player'])
        import combat_path
        form=combat_path.form_spec(p)
        form_text=(f"\n{form['name']}: {form['cost']} mana to activate; {form['upkeep']} mana upkeep per exchange; {form['duration']} seconds." if form else '\nNo unlocked form is available.')
        panel=self.drawer('FORMS, RULES & TERRAIN',self.terrain_text(f)+'\n\n'+objectives.description(f)+
                          ('\nRestrained practice: 55% striking output; no full-strength superiority claim.' if f['kind']=='spar' else '')+
                          form_text+'\n\nForm activation and channel changes spend resources immediately. Switching to an elemental channel costs 8 mana. Unavailable actions report the engine reason without spending.')
        row=tk.Frame(panel,bg=ui.PANEL); row.pack(fill='x',before=panel.winfo_children()[2])
        self.rpg_button(row,'Activate form',lambda:self.run(lambda:combat.activate_form(s))).pack(side='left')
        if p.get('technique_form')=='Conduit State': self.rpg_button(row,'Conduit State',lambda:self.run(lambda:combat.activate_form(s,form_choice='Conduit State'))).pack(side='left')
        if states.trait(p,'Shinigami Protocol'):
            self.rpg_button(row,'Shinigami · 20 stamina',lambda:self.run(lambda:states.activate_protocol(s))).pack(side='left')
        channels=states.channels(p)
        if channels:
            channel=tk.StringVar(value=f['player']['channel'] or 'No channel')
            self.picker(row,channel,['No channel',*channels[1:]],lambda:self.run(lambda:states.set_channel(s,'' if channel.get()=='No channel' else channel.get())),16)
            self.rpg_button(row,'Misanthropy · 18 mana',lambda:self.run(lambda:states.activate_endurance(s))).pack(side='left')
        extra=tk.Frame(panel,bg=ui.PANEL); extra.pack(fill='x',after=row)
        self.picker(extra,self.action_art,['All arts',*p['arts']],self.populate_moves,22)
        if not f['turn'] and len(objectives.choices(f))>1:
            goal=tk.StringVar(value=f.get('objective','Duel'))
            self.picker(extra,goal,objectives.choices(f),lambda:self.run(lambda:objectives.select(s,goal.get())),18)
        self.rpg_button(extra,'Stop spar' if f['kind']=='spar' else 'Concede',lambda:self.run(lambda:combat.concede(s))).pack(side='left')

    def submit(self):
        if self.working or self.game.busy: return
        if self.rpg_drawer is not None and self.rpg_drawer.winfo_exists(): return
        s=self.game.state_data; f=combat.active(s)
        if not f or f['status']!='active': return
        m=self.move_map.get(self.move_choice.get())
        if not m: raise ValueError('Select a learned action.')
        self.phase_label.configure(text='RESOLVING'); self.execute_button.configure(state='disabled')
        before=resource_snapshot(f)
        result=engine.resolve(s,engine.request(s,m['id'],self.amp_map.get(self.amp_choice.get()),self.target_map[self.target_choice.get()]))
        f['exchanges'][-1]['ui_resource_audit']={'before':before,'after':resource_snapshot(f)}
        self.game.persist(); self.refresh()
        self.phase_label.configure(text='NARRATING')
        if f['status']=='active': self.execute_button.configure(state='disabled')
        self.async_job(lambda:engine.narrate(result),lambda value:engine.commit_narration(s,value),resolved=True)

    def close_encounter(self):
        combat.close(self.game.state_data)
        self.leave()
