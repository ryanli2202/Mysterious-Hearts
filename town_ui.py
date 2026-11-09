"""Free-roam town and relationship controls for the desktop client."""
import custom_protagonist
import tkinter as tk
from tkinter import ttk, messagebox
from phone_dialogs import AppWindow, messagebox, simpledialog
import copy
import queue
import threading
import town
import groups
import dating
import game_core as core
import winterfield_ui as ui
from relationship_ui import RelationshipBars
from artwork import ArtCanvas, scene_art

def LocalConversation(window, name):
    """Legacy callers enter the same illustrated hangout used by town navigation."""
    window.talk(name)
    window.game.show_in_person()
    return window.game.hangout_view


class TownControls:
    def __init__(self, game):
        super().__init__(game)
        self.game = game
        self.title('Winterfield · Free roam')
        self.geometry('1080x760')
        self.minsize(880, 650)
        self.configure(bg=ui.INK)
        self.refresh()

    def act(self, fn, *args):
        if self.game.busy:
            messagebox.showinfo('Conversation in progress', 'Wait for the current reply before taking a town action.', parent=self)
            return
        import qol
        before = qol.stats(self.game.state_data)
        try:
            result = fn(self.game.state_data, *args)
        except ValueError as exc:
            messagebox.showinfo('Winterfield', str(exc), parent=self)
            return
        self.game.pending = None
        self.game.persist(); self.game.render()
        changes = qol.changes(before, self.game.state_data)
        if changes and self.game.state_data.get('show_relationship_changes', True):
            self.game.status.config(text=' · '.join(changes))
        if self.winfo_exists():self.refresh()
        self.game.show_world_windows()
        return result

    def pizza_menu(self):
        if self.conversation_busy(): return
        s = self.game.state_data
        menu = AppWindow(self.game)
        menu.title("Mario's Pizza · Order at the counter")
        menu.transient(self)
        menu.grab_set()
        panel = ttk.Frame(menu, padding=16)
        panel.pack(fill='both', expand=True)
        item = tk.StringVar(value=next(iter(town.PIZZA_MENU)))
        ttk.Label(panel, text='Mario Romano’s menu · one slice per person').pack(anchor='w')
        for dish, (price, _) in town.PIZZA_MENU.items():
            ttk.Radiobutton(panel, text=f'{dish} · ${price}', variable=item, value=dish).pack(anchor='w')
        guests = [who for who in town.pizza_companions(s) if town.present(s, who)]
        ttk.Label(panel, text='Eating with you').pack(anchor='w', pady=(12, 0))
        ttk.Label(panel, text='Order solo or select guests here. Bring friends by shared drive or summon them in Town.',
                  wraplength=350).pack(anchor='w')
        selections = {}
        def update(*_):
            chosen = [who for who, value in selections.items() if value.get()]
            can_date = len(chosen) == 1 and dating.in_hangout(s, chosen[0])
            if not can_date: romantic.set(False)
            date_button.config(state='normal' if can_date else 'disabled')
            cost = town.PIZZA_MENU[item.get()][0] * (1 + len(chosen))
            order.config(text=f'Order from Mario · ${cost}')
        for who in guests:
            selected = tk.BooleanVar()
            selections[who] = selected
            name = s.get('nicknames', {}).get(who) or who.title()
            ttk.Checkbutton(panel, text=name, variable=selected, command=update).pack(anchor='w')
        romantic = tk.BooleanVar()
        date_button = ttk.Checkbutton(panel, text='Order for our date', variable=romantic)
        date_button.pack(anchor='w', pady=6)
        def submit():
            chosen = [who for who, value in selections.items() if value.get()]
            dish, is_date = item.get(), romantic.get()
            menu.destroy()
            receipt = self.act(town.order_pizza, dish, chosen, is_date)
            if receipt: messagebox.showinfo("Mario's Pizza", receipt, parent=self)
        order = ttk.Button(panel, command=submit)
        order.pack(fill='x')
        item.trace_add('write', update)
        update()

    def meet(self, who):
        if self.conversation_busy(): return
        s = self.game.state_data
        try:
            town.meet(s, who)
        except ValueError as exc:
            messagebox.showinfo('Winterfield', str(exc), parent=self)
            return
        self.game.select_group(s.get('active_group'))
        self.game.shown_group = s.get('active_group')
        self.game.persist(); self.game.render()
        self.destroy()
        self.game.lift()
        self.game.focus_set()
        if not s['routes'][who]['dialogue']:
            self.game.submit(core.SCENE_DIRECTIONS[0])

    def talk(self, name):
        if self.conversation_busy(): return
        try:
            gid = groups.open_local(self.game.state_data, name)
            self.game.select_group(gid)
            self.game.persist()
            self.withdraw()
            self.game.lift()
            if not self.game.state_data['groups'][gid]['history']:
                self.game.submit(core.SCENE_DIRECTIONS[0])
        except ValueError as exc: messagebox.showinfo('Winterfield', str(exc), parent=self)

    def conversation_busy(self):
        if self.game.busy:
            messagebox.showinfo('Conversation in progress', 'A reply is still being written. Try again when it finishes.', parent=self)
        return self.game.busy

    def ask_relationship(self, who, kind):
        if self.conversation_busy(): return
        state = self.game.state_data
        try:
            dating.decision(state, who, kind)
        except ValueError as exc:
            messagebox.showinfo('Relationship invitation', str(exc), parent=self)
            return
        name = core.contact_name(state, who) if who in state['routes'] else who
        message = AppWindow(self)
        message.title('Messages · ' + name)
        message.transient(self)
        message.grab_set()
        panel = ttk.Frame(message, padding=18)
        panel.pack(fill='both', expand=True)
        ttk.Label(panel, text='Messages', style='Section.TLabel').pack(anchor='w')
        ttk.Label(panel, text=name, style='Title.TLabel').pack(anchor='w', pady=(0,12))
        ttk.Label(panel, text=core.PLAYERS[state['player']] + ' (You)', foreground=ui.MINT).pack(anchor='e')
        ttk.Label(panel, text=dating.ASK[kind], wraplength=360, padding=10, background=ui.CARD).pack(anchor='e', pady=(2, 14))
        ttk.Label(panel, text=name, foreground=ui.GOLD).pack(anchor='w')
        response = ttk.Label(panel, wraplength=420, justify='left')
        response.pack(anchor='w', fill='x', pady=(2, 12))
        actions = ttk.Frame(panel)
        actions.pack(fill='x')
        results = queue.Queue()

        def close():
            if self.game.busy: return
            message.destroy()
            self.refresh()

        def join():
            close()
            if who in state['routes']:
                self.meet(who)
            else:
                self.talk(who)

        def poll():
            if not message.winfo_exists(): return
            try: token, data, error = results.get_nowait()
            except queue.Empty:
                if not self.game.busy: return
                response.configure(text=self.game.wait_status())
                message.after(80, poll)
                return
            if token != self.game.token:
                if self.game.busy: message.after(80,poll)
                return
            self.game.external_cancel = None
            if error is None:
                try:
                    dating.commit_invitation(state, who, kind, data)
                except ValueError as exc:
                    error = str(exc)
            self.game.set_busy(False)
            if error:
                response.configure(text=error)
                ttk.Button(actions, text='Retry', command=send).pack(side='right')
            else:
                self.game.pending = None
                self.game.persist()
                checklist = dating.describe(state, who) if kind == 'date' and data['answer'] == 'yes' else ''
                response.configure(text=data['reply'] + ('\n\n' + checklist if checklist else ''))
                if checklist and town.present(state, who):
                    ttk.Button(actions, text='Continue to hangout', command=join).pack(side='right')
            ttk.Button(actions, text='Close', command=close).pack(side='left')

        def send():
            for child in actions.winfo_children(): child.destroy()
            response.configure(text=name + ' is typing…')
            snapshot = copy.deepcopy(state)
            self.game.token += 1
            token = self.game.token
            def cancel():
                self.game.token += 1; self.game.set_busy(False)
                response.configure(text='Invitation cancelled; no relationship changes applied.')
                for child in actions.winfo_children(): child.destroy()
                ttk.Button(actions, text='Close', command=close).pack()
            self.game.external_cancel = cancel
            ttk.Button(actions, text='Cancel response', command=self.game.cancel_generation).pack(side='left')
            self.game.set_busy(True)
            def work():
                try: results.put((token, dating.generate_invitation(snapshot, who, kind), None))
                except Exception as exc: results.put((token, None, str(exc)))
            threading.Thread(target=work, daemon=True).start()
            message.after(80, poll)
        message.protocol('WM_DELETE_WINDOW', close)
        send()
        return message

    def refresh(self):
        selected = self.tabs.index(self.tabs.select()) if hasattr(self, 'tabs') else 0
        for child in self.winfo_children(): child.destroy()
        s = self.game.state_data; w = town.ensure(s)
        mast = tk.Frame(self, bg=ui.INK)
        mast.pack(fill='x', padx=18, pady=(12,8))
        if getattr(self,'embedded_main',False):
            ttk.Button(mast,text='‹ Back to location',command=self.game.leave_main_area).pack(side='left',padx=(0,12))
        tk.Label(mast, text='Winterfield', bg=ui.INK, fg=ui.CREAM, font=(ui.SERIF, 23)).pack(side='left')
        tk.Label(mast, text=town.loop.clock(s), bg=ui.INK, fg=ui.MUTED, font=('Segoe UI', 10)).pack(side='left', padx=15)
        ttk.Button(mast, text='Profiles', command=self.game.open_profiles).pack(side='right', padx=(6,0))
        ttk.Button(mast, text='Calendar', command=self.game.open_calendar).pack(side='right')
        tk.Label(mast, text=f"${w['money']:,}", bg=ui.INK, fg=ui.GOLD, font=('Segoe UI', 12, 'bold')).pack(side='right', padx=15)
        tabs = ttk.Notebook(self); self.tabs = tabs; tabs.pack(fill='both', expand=True, padx=15, pady=(0,15))
        explore = ttk.Frame(tabs, padding=15); tabs.add(explore, text='Town')
        left_shell = ttk.Frame(explore); left_shell.pack(side='left', fill='y', padx=(0,18))
        left_canvas = tk.Canvas(left_shell, width=275, bg=ui.PANEL, highlightthickness=0)
        left_scroll = ttk.Scrollbar(left_shell, command=left_canvas.yview); left_scroll.pack(side='right', fill='y')
        left_canvas.configure(yscrollcommand=left_scroll.set); left_canvas.pack(side='left', fill='y')
        left = ttk.Frame(left_canvas)
        left_canvas.create_window((0,0), window=left, anchor='nw', width=268)
        left.bind('<Configure>', lambda _:left_canvas.configure(scrollregion=left_canvas.bbox('all')))
        left_canvas.bind('<MouseWheel>', lambda e:left_canvas.yview_scroll(-int(e.delta/120), 'units'))
        ttk.Label(left, text='Plan a drive', font=(ui.SERIF, 18)).pack(anchor='w', pady=(0,6))
        player = s['player']
        garage = town.loop.player_garage(s)
        model = tk.StringVar(value=town.loop.selected_car(s, player))
        if len(garage) > 1:
            picker = ttk.Combobox(left, textvariable=model, values=list(garage),
                                  state='disabled' if w['cast'][player]['journey'] else 'readonly')
            picker.pack(fill='x', pady=3)
            def choose_car(_):
                if self.conversation_busy():
                    model.set(town.loop.selected_car(s, player))
                    return
                town.select_car(s, model.get())
                self.game.persist()
                show_vehicle()
                self.shortcut_model.set(town.loop.trip_vehicle(s, player, len(w['party'])))
            picker.bind('<<ComboboxSelected>>', choose_car)
        else:
            ttk.Label(left, text=model.get()).pack(anchor='w')
        destinations = {k:town.location_name(s, k) for k in town.LOCATIONS if not k.startswith('car:') and k != 'home' and town.hidden.visible_place(s,k)}
        destination = tk.StringVar(value=next((v for k,v in destinations.items() if k != w['location']), next(iter(destinations.values()))))
        ttk.Label(left, text='Destination', style='Section.TLabel').pack(anchor='w', pady=(6,0))
        ttk.Combobox(left, textvariable=destination, values=list(destinations.values()), state='readonly', width=30).pack(fill='x', pady=8)
        companion = tk.BooleanVar(value=False)
        ttk.Checkbutton(left, text='Travel together with active contact', variable=companion).pack(anchor='w')
        def drive():
            key = next(k for k,v in destinations.items() if v == destination.get())
            self.act(town.travel, key, s['active'] if companion.get() else None)
        drive_button = ttk.Button(left, command=drive, style='Accent.TButton')
        def show_vehicle(*_):
            riders = set(w['party'])
            if companion.get(): riders.add(s['active'])
            vehicle = town.loop.trip_vehicle(s, player, len(riders))
            label = 'Call your driver' if player == 'ivan' else 'Drive'
            drive_button.config(text=label + ' · ' + vehicle)
        companion.trace_add('write', show_vehicle)
        show_vehicle()
        drive_button.pack(fill='x', pady=6)
        import qol
        travel_preview_label = ttk.Label(left, wraplength=275)
        travel_preview_label.pack(fill='x', pady=5)
        def update_preview(*_):
            place = next(k for k,v in destinations.items() if v == destination.get())
            travel_preview_label.config(text=qol.travel_preview(s, place))
        destination.trace_add('write', update_preview); update_preview()
        ttk.Button(left, text='Go home', command=lambda:self.act(town.travel, town.HOMES[player])).pack(fill='x', pady=3)
        def favourite():
            place = next(k for k,v in destinations.items() if v == destination.get())
            favourites = s.setdefault('favourite_places', [])
            if place in favourites: favourites.remove(place)
            else: favourites.append(place)
            self.game.persist(); self.refresh()
        ttk.Button(left, text='★ Toggle favourite destination', command=favourite).pack(fill='x', pady=3)
        for place in s.get('favourite_places', []):
            if place in destinations:
                ttk.Button(left, text='★ '+destinations[place], command=lambda p=place:destination.set(destinations[p])).pack(fill='x')
        driving = bool(w['cast'][player]['journey'])
        if driving: ttk.Label(left, text='Finish your current drive before starting another.', wraplength=275).pack(anchor='w')
        drive_button.configure(state='disabled' if driving else 'normal')
        ttk.Button(left, text='Life & availability · Sleep / wake', command=lambda:__import__('autonomy_ui').open_window(self.game)).pack(fill='x', pady=6)
        ttk.Button(left, text='Refresh whereabouts', command=self.refresh).pack(fill='x', pady=6)
        contacts = [key for key in s['routes']
                    if key != s['player'] and town.hidden.contact(s, key) and key not in w['party']]
        summon_picker = ttk.Combobox(left, values=[core.contact_name(s,k) if k not in s.get('nicknames', {}) else
                                    core.contact_name(s,k)+' ('+core.CONTACTS[k][0]+')' for k in contacts],
                                    state='readonly', width=30)
        summon_picker.pack(fill='x', pady=(12, 3))
        if contacts: summon_picker.current(0)
        ttk.Button(left, text='Summon to my location',
                   state='normal' if contacts and not w['cast'][s['player']]['journey'] else 'disabled',
                   command=lambda: self.act(town.summon, contacts[summon_picker.current()])).pack(fill='x')
        ttk.Label(left, text='Travel is instant. Your party arrives with you.', style='Muted.TLabel', wraplength=250).pack(anchor='w', pady=8)
        right = ttk.Frame(explore); right.pack(side='left', fill='both', expand=True)
        preview = ArtCanvas(right, scene_art(w['location'], minute=w['minute']), height=140)
        preview.pack(fill='x', pady=(0, 10))
        if w['location']=='park' and getattr(self,'embedded_main',False):
            ttk.Button(right,text='Enter park · explore on foot',command=self.game.enter_park,
                       state='disabled' if self.game.busy or driving else 'normal').pack(fill='x',pady=(0,8))
        if w['location'] in town.vacant_homes.HOMES:
            residence = town.vacant_homes.HOMES[w['location']]
            ttk.Label(right, text=residence['description'] + '\n' + town.vacant_homes.status(s, w['location']),
                      style='Muted.TLabel', wraplength=540).pack(anchor='w', pady=(0, 8))
        import weather
        ttk.Label(right, text=weather.summary(w['minute'])).pack(anchor='w', pady=(0,6))
        ttk.Button(right, text='Life in Winterfield · activities & news', command=self.game.open_living_world).pack(anchor='w', pady=(0,8))
        plaque = tk.Frame(preview, bg=ui.INK, padx=12, pady=5)
        plaque.place(x=10, rely=1, y=-10, anchor='sw')
        tk.Label(plaque, text=town.loop.place_name(s), bg=ui.INK, fg=ui.CREAM, font=(ui.SERIF, 17)).pack(anchor='w')
        nearby = ttk.Frame(right)
        nearby.pack(fill='both', expand=True)
        canvas = tk.Canvas(nearby, bg=ui.PANEL, highlightthickness=0)
        scroll = ttk.Scrollbar(nearby, command=canvas.yview)
        scroll.pack(side='right', fill='y')
        canvas.configure(yscrollcommand=scroll.set)
        canvas.pack(side='left', fill='both', expand=True)
        right = ttk.Frame(canvas)
        content = canvas.create_window((0, 0), window=right, anchor='nw')
        right.bind('<Configure>', lambda e, cv=canvas: cv.configure(scrollregion=cv.bbox('all')))
        canvas.bind('<Configure>', lambda e, cv=canvas:cv.itemconfigure(content, width=e.width))
        ttk.Label(right, text='Around you', font=(ui.SERIF, 17)).pack(anchor='w', pady=(0,5))
        if w['location'] == 'marios_pizza':
            ttk.Button(right, text='Order from Mario · Pizza menu', command=self.pizza_menu).pack(fill='x', pady=4)
        scene = w.get('arrival_scene', {})
        if scene.get('place') == w['location'] and scene['observations']:
            reactions = []
            for who, notes in scene['observations'].items():
                if who in w['cast'] and not town.loop.together(s, who): continue
                name = who.title() if town.hidden.known(s, who) else 'A stranger'
                reactions.append(name + ' ' + ', then '.join(note.rstrip('.') for note in notes) + '.')
            if reactions:
                box = tk.Text(right, width=1, height=3, wrap='word', font=('Segoe UI', 10))
                box.insert('1.0', '\n'.join(reactions))
                box.configure(state='disabled')
                box.pack(fill='x')
        for who in town.loop.HOUSES:
            if who != s['player'] and town.loop.together(s, who):
                known = town.hidden.known(s, who)
                row = tk.Frame(right, bg=ui.CARD, padx=7, pady=4)
                row.pack(fill='x', pady=3)
                if known:
                    portrait = self.game.portrait(who, (44,48), outfit='selection')
                    tk.Button(row, image=portrait, bg=ui.CARD, bd=0, cursor='hand2',
                              command=lambda g=who:self.game.open_profiles(g)).pack(side='left', padx=(0,8))
                title = core.contact_name(s,who) if known else 'Someone new'
                tk.Label(row, text=title, bg=ui.CARD, fg=ui.CREAM, font=('Segoe UI',11,'bold')).pack(side='left')
                ttk.Button(row, text='Meet', command=lambda g=who:self.meet(g)).pack(side='right')
        for name in w['npcs']:
            ttk.Button(right, text='Talk to ' + name,
                       command=lambda n=name: self.talk(n)).pack(fill='x', pady=6)
        if not w['npcs'] and not any(town.loop.together(s, other) for other in w['cast'] if other != player):
            ttk.Label(right, text='No one else is here right now.', style='Muted.TLabel').pack(anchor='w')
        if w['location'] in town.JOBS:
            name, pay = town.JOBS[w['location']]
            local = s.get('careers',{}).get('local_jobs',{}).get(w['location'],{})
            pay += min(100,local.get('shifts',0)//3*20)
            worked = w['last_shift_day'] == w['minute']//1440+1
            ttk.Button(right, text=f'Work: {name} · 60 min · +${pay}', state='disabled' if worked else 'normal', command=lambda: self.act(town.work)).pack(fill='x', pady=8)
            ttk.Label(right,text='Local shifts: 08:00–20:00. Repeat work builds reliability and pay.',wraplength=280).pack(anchor='w')
            if worked: ttk.Label(right,text='You have already completed a shift today.').pack(anchor='w')
        if w['location'] == town.HOMES[player]:
            ttk.Button(right, text='Rest at home', command=lambda: self.act(town.rest)).pack(fill='x', pady=8)
        if not driving:
            def visit(place):
                destination.set(destinations[place])
                drive()
            self.visit_cards(right, s, destinations, visit)
        shop = ttk.Frame(tabs, padding=15); tabs.add(shop, text='Phone apps')
        ttk.Label(shop, text='Catch up on Grove, browse daily Supafast finds, or send a meal with Doober Eats.').pack(anchor='w', pady=10)
        for app in ('Grove', 'Supafast', 'Doober Eats'):
            ttk.Button(shop, text=app, command=lambda a=app: self.game.phone_window(a)).pack(fill='x', pady=8)
        social_page = ttk.Frame(tabs); tabs.add(social_page, text='Relationships')
        canvas = tk.Canvas(social_page, bg=ui.PANEL, highlightthickness=0)
        scroll = ttk.Scrollbar(social_page, orient='vertical', command=canvas.yview)
        scroll.pack(side='right', fill='y'); canvas.pack(side='left', fill='both', expand=True)
        canvas.configure(yscrollcommand=scroll.set)
        social = ttk.Frame(canvas, padding=15)
        panel = canvas.create_window((0, 0), window=social, anchor='nw')
        social.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        canvas.bind('<Configure>', lambda e: canvas.itemconfigure(panel, width=e.width))
        ttk.Label(social, text='Send a private invitation. An accepted date costs $150 when you meet. Finish its three goals to complete the date.\nYou can ask to be official once you’re dating. Each person has their own minimums.\nFriendly gifts are platonic. Repairing hurt takes an honest conversation, follow-through over time and their forgiveness.').pack(anchor='w', pady=(0,15))
        import phone_apps
        gift_items = phone_apps.gift_options(s)
        owned = [key for key in gift_items if w['inventory'].get(key, 0) > 0]
        self.gift = tk.StringVar(value=owned[0] if owned else '')
        picker = ttk.Combobox(social, textvariable=self.gift, values=owned, state='readonly'); picker.pack(anchor='w', pady=6)
        for who, r in s['relationships'].items():
            if not town.hidden.known(s,who): continue
            row = ttk.Frame(social); row.pack(fill='x', pady=3)
            ttk.Label(row, text=f'{who.title()} · {core.social_world.status_line(s, who)}', font=(ui.SERIF,15)).pack(anchor='w')
            bars = RelationshipBars(row, bg=ui.PANEL, fg=ui.CREAM, horizontal=True)
            bars.pack(fill='x'); bars.update_stats(r, romanceable=town.romanceable(s, who))
            initial = town.STARTING_RELATIONSHIPS[s['player']].get(who)
            points = ['Starting connection: ' + (initial[3] if initial else 'friends')]
            levels = [' / '.join(map(str, dating.minimums(s, who, kind))) for kind in dating.ASK]
            points.append(f'Closeness / trust / attraction    ·    Date {levels[0]}    ·    Official {levels[1]}')
            if dating.session(s, who):
                points.append(dating.describe(s, who))
            if r.get('jealousy'): points.append(f"Jealousy: {r['jealousy']}/100")
            if r.get('breakups'):
                last = r['breakups'][-1]
                points.append(f"{last['date']} · {last['kind'].title()} breakup · {last['reason']}")
            for kind, stamp in r.get('firsts', {}).items():
                points.append(town.character_memory.FIRSTS[kind] + ' · ' + stamp)
            import memory_store
            memory = memory_store.summary(s,who)['text']
            if memory: points.append('Story so far: ' + memory)
            points += r.get('milestones', [])[-3:] + r.get('known_betrayals', [])[-2:]
            place = town.loop.place_name(s,who) if who in s['routes'] else ('Here' if town.present(s,who) else 'Elsewhere in town')
            ttk.Label(row, text='Now: ' + place + ('\n' + '\n'.join(points) if points else '\nNo shared milestones recorded yet.'), wraplength=780).pack(anchor='w', pady=4)
            breakup = 'End strained relationship' if r.get('unresolved_harm') or r['status']=='strained' else 'Agree to part ways'
            gift_reason = 'Buy a gift on Supafast first.' if not owned else 'Meet in person to give a gift.' if not town.present(s,who) else 'Repair the strained relationship before giving gifts.' if r['status']=='strained' else ''
            if gift_reason: ttk.Label(row,text=gift_reason).pack(anchor='w')
            if r.get('unresolved_harm'):
                ttk.Label(row, text='To make amends, discuss the hurt in chat and follow through on a later day. They decide when to forgive.', wraplength=780).pack(anchor='w')
            if s.get('date_session'): ttk.Label(row,text='Finish or cancel your existing date before planning another.').pack(anchor='w')
            for label, action in [('Gift', 'gift'), ('Ask on a date', 'date'), ('Ask to be official', 'official'), ('Make amends', 'repair'), (breakup, 'breakup')]:
                command = (lambda g=who,a=action: self.ask_relationship(g, a)) if action in dating.ASK else (
                    lambda g=who,a=action: self.act(town.relationship,g,a,self.gift.get()))
                button = ttk.Button(row, text=label, command=command)
                button.pack(side='left', padx=(0,6), pady=3)
                if action == 'repair' and r.get('unresolved_harm'):
                    button.config(state='disabled', text='Repair through conversation')
                if action == 'date' and s.get('date_session'):
                    button.config(state='disabled')
                if action == 'gift':
                    button.config(text='Gift · 5 min',state='disabled' if gift_reason else 'normal')
            if dating.session(s, who):
                if town.present(s, who):
                    ttk.Button(row, text='Join date', command=lambda g=who: self.meet(g) if g in s['routes'] else self.talk(g)).pack(side='left')
                ttk.Button(row, text='Cancel date', command=lambda g=who: self.act(dating.cancel, g)).pack(side='left')
        for other in s['friendships']:
            if not town.hidden.known(s,other): continue
            if other == s['player'] or other in s['relationships']: continue
            ttk.Label(social, text=other.title() + ' · ' + core.social_world.status_line(s, other) + ' · ' + town.loop.place_name(s, other), wraplength=780).pack(anchor='w', pady=(15,4))
            friendship = RelationshipBars(social, bg=ui.PANEL, fg=ui.CREAM, horizontal=True)
            friendship.pack(fill='x'); friendship.update_stats(s['friendships'][other], romanceable=town.romanceable(s, other))
        self.add_discoveries(tabs, s)
        journal = ttk.Frame(tabs, padding=15); tabs.add(journal, text='Journal')
        box = tk.Text(journal, wrap='word', font=('Segoe UI',11)); box.pack(fill='both',expand=True)
        box.insert('end', 'BETWEEN THE GIRLS\n' + '\n'.join(k.replace(':',' & ').title()+': '+v for k,v in s['girl_bonds'].items() if all(town.hidden.known(s,who) for who in k.split(':'))) + '\n\nTOWN EVENTS\n' + '\n'.join(w['log']))
        box.configure(state='disabled')
        self.add_world_pages(tabs, s)
        self.add_activity_pages(tabs, s)
        tabs.select(selected)

    def visit_cards(self, parent, s, destinations, travel):
        world = s['world']
        contacts = [who for who, actor in world['cast'].items() if who != s['player']
                    and town.hidden.contact(s, who) and not actor['journey']
                    and actor['location'] in destinations and actor['location'] != world['location']]
        records = {**s['friendships'], **s['relationships']}
        contacts.sort(key=lambda who: (who == s['active'], records.get(who, {}).get('closeness', 0)), reverse=True)
        if not contacts: return
        ttk.Label(parent, text='People to visit', font=(ui.SERIF, 17)).pack(anchor='w', pady=(18,8))
        strip = ttk.Frame(parent)
        strip.pack(fill='x')
        for i, who in enumerate(contacts[:3]):
            strip.columnconfigure(i, weight=1, uniform='visit')
            place = world['cast'][who]['location']
            card = tk.Frame(strip, bg=ui.CARD)
            card.grid(row=0,column=i, sticky='nsew', padx=(0,6))
            art = ArtCanvas(card, scene_art(place), width=1, height=90)
            art.pack(fill='x')
            art.configure(cursor='hand2')
            art.bind('<Button-1>', lambda _, person=who:self.game.open_profiles(person))
            portrait = self.game.portrait(who, (65,80), place, world['minute'])
            art.create_image(6, 90, image=portrait, anchor='sw')
            tk.Label(card, text=core.contact_name(s, who), font=('Segoe UI', 11, 'bold'), bg=ui.CARD, fg=ui.CREAM).pack(anchor='w', padx=7, pady=(5,0))
            tk.Label(card, text=destinations[place], fg=ui.MUTED, bg=ui.CARD, wraplength=148,
                     anchor='w', justify='left').pack(anchor='w', padx=7)
            ttk.Button(card, text='Drive here', command=lambda p=place:travel(p)).pack(side='bottom', fill='x', padx=7,pady=6)

    def add_discoveries(self, tabs, s):
        page = ttk.Frame(tabs, padding=12); tabs.add(page, text='Discoveries')
        ttk.Label(page, text='Explore bowling, the arcade, nightclub, bar, public park, beach, library and shopping mall.\nLocals choose outings around work, weather and interests; nightlife starts in the evening.\nMeet someone nearby, add their contact, then build 6 closeness to discover their home.', wraplength=820).pack(anchor='w', pady=8)
        people = [who for who in town.hidden.ensure(s) if town.hidden.known(s,who)]
        if not people:
            ttk.Label(page, text='No hidden residents met yet. Explore a new neighbourhood.').pack(anchor='w')
            return
        chosen = tk.StringVar(value=people[0])
        ttk.Combobox(page, textvariable=chosen, values=people, state='readonly').pack(anchor='w')
        info = ttk.Label(page, wraplength=800, justify='left'); info.pack(anchor='w', pady=15)
        def show(*args):
            who = chosen.get(); d = town.hidden.ensure(s)[who]
            profile = town.hidden.profile(who, sibling=town.sibling_route(s, who)) if who in town.hidden.CAST else core.CONTACTS[who][0] + '\n' + core.CONTACTS[who][3]
            info.config(text=profile + '\n\nContact: ' + ('added' if d['contact'] else 'available to add') + '\nHome: ' + (town.loop.HOUSES[who][1] if d['home'] else 'undiscovered'))
        chosen.trace_add('write',show); show()
        ttk.Button(page, text='Add contact', command=lambda:self.act(town.hidden.add_contact,chosen.get())).pack(anchor='w',pady=6)
        ttk.Button(page, text='Ask for home address · requires 6 closeness', command=lambda:self.act(town.hidden.discover_home,chosen.get())).pack(anchor='w',pady=6)

    def add_world_pages(self, tabs, s):
        w = s['world']
        def text_page(title):
            page = ttk.Frame(tabs, padding=12); tabs.add(page, text=title)
            box = tk.Text(page, wrap='word', font=('Segoe UI', 11), padx=12, pady=12)
            scroll = ttk.Scrollbar(page, command=box.yview); scroll.pack(side='right', fill='y')
            box.configure(yscrollcommand=scroll.set); box.pack(fill='both', expand=True)
            return box
        bonds = ttk.Frame(tabs, padding=12); tabs.add(bonds, text='Bonds')
        picker = ttk.Treeview(bonds, columns=('type','trust','close','tension'), show='tree headings', height=10)
        picker.heading('#0', text='Pair'); picker.column('#0', width=160)
        for key, title in [('type','Bond'),('trust','Trust'),('close','Closeness'),('tension','Tension')]:
            picker.heading(key,text=title); picker.column(key,width=140 if key=='type' else 75)
        picker.pack(fill='x')
        details = tk.Text(bonds, wrap='word', height=9, font=('Segoe UI',11), padx=12,pady=12)
        details.pack(fill='both',expand=True,pady=10)
        for key,bond in s['bond_details'].items():
            if not all(town.hidden.known(s,who) for who in key.split(':')): continue
            picker.insert('', 'end', iid=key, text=key.replace(':',' & ').title(),
                          values=(bond['type'],bond['trust'],bond['closeness'],bond['tension']))
        def show_bond(event=None):
            if not picker.selection(): return
            key=picker.selection()[0]; bond=s['bond_details'][key]
            details.configure(state='normal'); details.delete('1.0','end')
            details.insert('end', key.replace(':',' & ').title()+'\n\nKEY POINTS\n'+
                           '\n'.join(bond['key_points'])+'\n\nRECENT DEVELOPMENTS\n'+
                           ('\n'.join(bond['events']) or 'No new events yet.')+'\n\nShared romance tension: '+s['girl_bonds'].get(key,'neutral'))
            details.configure(state='disabled')
        picker.bind('<<TreeviewSelect>>', show_bond)
        if picker.get_children():
            picker.selection_set(picker.get_children()[0])
            show_bond()
        box=text_page('Homes & routines')
        if 'custom_protagonist' in s:
            _, name, description = town.loop.HOUSES[s['player']]
            box.insert('end', core.PLAYERS[s['player']] + ' — ' + name + '\n' + description + '\nYour home; choose your own daily routine.\n\n')
        for who,(home,name,description) in town.loop.HOUSES.items():
            if not town.hidden.visible_place(s,home): continue
            box.insert('end', who.title()+' — '+name+'\n'+description+'\nNOW: '+town.loop.place_name(s,who)+'\n')
            if who == 'yuriko':
                box.insert('end', core.lore.character_tables()['yuriko']['Public life']+'\n\n')
            if who in s['world']['party'] or s['world']['cast'][who].get('waiting_for_hangout'):
                box.insert('end', 'Current activity: '+s['world']['cast'][who]['activity']+'\n')
            if who != s['player'] and who != 'sylvanis' and town.loop.dates.free_day(town.loop.dates.story_date(w['minute'])):
                box.insert('end', 'Day off · Planned outings (needs and agreed plans can change these):\n')
                day_start = w['minute']//1440*1440
                previous = None
                for hour in (8, 11, 14, 17, 20, 22):
                    _, place, activity = town.loop.appointment(who, day_start+hour*60)
                    if (place, activity) != previous and town.hidden.visible_place(s, place):
                        box.insert('end', f'  {hour:02d}:00 · {town.LOCATIONS[place]} · {activity}\n')
                    previous = (place, activity)
                box.insert('end', '\n')
                continue
            box.insert('end', 'Routine (player-controlled protagonist is free to deviate):\n' if who==s['player'] else 'Weekday routine:\n')
            routine=town.loop.SCHEDULES[who]
            if who in ('ivan','sylvanis','valentina','martos','elias','camila','mavis'):
                routine=list(dict.fromkeys(town.loop.appointment(who,w['minute']//1440*1440+h*60) for h in range(24)))
            for hour,place,activity in routine:
                if town.hidden.visible_place(s, place):
                    box.insert('end',f'  {hour:02d}:00 · {town.LOCATIONS[place]} · {activity}\n')
            box.insert('end','\n')
        box.configure(state='disabled')
        box=text_page('Travel & texts')
        for who in town.loop.HOUSES:
            if who in town.hidden.CAST and not town.hidden.ensure(s)[who]['home']: continue
            box.insert('end',who.title()+': '+town.loop.place_name(s,who)+'\n')
        box.insert('end','\nDRIVE HISTORY\n')
        for trip in s['world']['journeys'][-30:]:
            if not town.hidden.known(s,trip['driver']) or not all(town.hidden.visible_place(s,p) for p in (trip['origin'],trip['destination'])): continue
            service = f" · Driven by {trip['chauffeur']}" if trip.get('chauffeur') else ''
            box.insert('end',f"{trip['driver'].title()} · {town.LOCATIONS[trip['origin']]} → {town.LOCATIONS[trip['destination']]} · {trip['vehicle']}{service} · passengers: {', '.join(trip['passengers']) or 'none'} · depart {trip['departed']} / arrive {trip['arrives']} game minutes\n")
        box.insert('end','\nMESSAGES\nReplies and follow-ups depend on availability, needs and the conversation.\n')
        for who,route in s['routes'].items():
            if who==s['player'] or not town.hidden.contact(s,who): continue
            import messaging
            pending=messaging.thread(s,who)
            box.insert('end',f"{who.title()}: {len(pending['pending'])} messages awaiting replies · {pending['followups']} follow-ups · {pending['error'] or 'Ready'}\n")
        box.configure(state='disabled')

    def add_activity_pages(self,tabs,s):
        page=ttk.Frame(tabs,padding=16); tabs.add(page,text='Groups')
        ttk.Label(page,text='Choose who to hang out with from the people here: one person or a group.\nOnly selected companions join your conversation and travel with you. Nearby contacts do not join automatically.',wraplength=800).pack(anchor='w',pady=8)
        selections={}
        for who in town.loop.HOUSES:
            if who==s['player'] or not town.hidden.contact(s,who): continue
            if not town.hidden.known(s,who): continue
            selected=tk.BooleanVar(value=who in s['world']['party']); selections[who]=selected
            ttk.Checkbutton(page,text=who.title()+' · '+town.loop.place_name(s,who),variable=selected,
                            state='normal' if town.loop.together(s,who) else 'disabled').pack(anchor='w',pady=5)
        ttk.Button(page,text='Form party / meet as a group',command=lambda:self.act(groups.form,[who for who,v in selections.items() if v.get()])).pack(fill='x',pady=8)
        ttk.Button(page,text='Disband party',command=lambda:self.act(groups.disband)).pack(fill='x',pady=4)
        def open_current():
            self.game.select_group()
            self.destroy()
        ttk.Button(page,text='Open current group conversation',command=open_current,
                   state='normal' if s.get('active_group') else 'disabled').pack(fill='x',pady=4)
        page=ttk.Frame(tabs,padding=16); tabs.add(page,text='Careers')
        self.shortcut_model = tk.StringVar(value=town.loop.trip_vehicle(s, s['player'], len(s['world']['party'])))
        ttk.Label(page, textvariable=self.shortcut_model).pack(anchor='w')
        ttk.Label(page,text=custom_protagonist.display_name(s["player"])+' · Day and night careers',font=('Segoe UI',15)).pack(anchor='w',pady=10)
        import careers
        for key in careers.available(s):
            spec=careers.TRACKS[key]
            ttk.Label(page,text=spec['title']+' · '+town.LOCATIONS[spec['venue']],wraplength=600).pack(anchor='w',pady=6)
        def open_work():
            from careers_ui import open_careers
            open_careers(self.game)
        ttk.Button(page,text='Open work & ambitions',command=open_work).pack(fill='x',pady=12)
        ttk.Label(page,text='Projects, meaningful shifts, preparation, leadership, competition and weekly commitments. Bookings also appear in Calendar. Each protagonist has a daytime path and a separate ambition.',wraplength=600).pack(anchor='w',pady=8)
        ttk.Button(page,text='Drive to your home',command=lambda:self.act(town.travel,'home')).pack(fill='x',pady=5)
        ttk.Button(page,text='Open home self-actions',command=self.game.home_window).pack(fill='x',pady=5)


class TownWindow(TownControls, AppWindow):
    """Compatibility host for callers that explicitly request a separate window."""


class TownPanel(TownControls, tk.Frame):
    """The in-person location controls live in the main game's content area."""
    embedded_main = True

    def __init__(self, game):
        tk.Frame.__init__(self,game.play_body,bg=ui.INK)
        self.game=game
        self.refresh()

    def title(self, text=None):return 'Winterfield · Location controls'
    def protocol(self, name=None, func=None):pass
    def withdraw(self):self.game.leave_main_area()
    def deiconify(self):self.pack(fill='both',expand=True)

    def destroy(self):
        if not self.winfo_exists():return
        if getattr(self.game,'area_view',None) is self:self.game.area_view=None
        tk.Frame.destroy(self)
        self.game.after_idle(self.game.layout_presence)
