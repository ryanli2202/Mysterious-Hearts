"""The world outside the phone: current location, companions and activities."""
import tkinter as tk
from tkinter import ttk, messagebox
from phone_dialogs import AppWindow, messagebox, simpledialog
import town
import groups
import game_core as core
from artwork import ArtCanvas, scene_art


class PresenceView(ttk.Frame):
    def __init__(self, parent, game):
        super().__init__(parent, padding=18)
        self.game = game
        self.signature = None

    def refresh(self):
        import autonomy
        s = self.game.state_data
        w = s['world']
        people = [who for who in w['cast'] if who != s['player'] and town.loop.together(s, who)]
        signature = (w['location'], tuple((who,w['cast'][who]['activity']) for who in people), tuple(w['npcs']), tuple(w['party']),
                     bool(w['cast'][s['player']]['journey']), self.game.busy, s.get('active_group'),autonomy.status(s,s['player']),
                     s.get('job_apps',{}).get('employment'))
        if signature == self.signature:
            self.location_title.configure(text=town.loop.place_name(s))
            return
        self.signature = signature
        for child in self.winfo_children(): child.destroy()
        ArtCanvas(self, scene_art(w['location']), height=210).pack(fill='x', pady=(0, 12))
        self.location_title = ttk.Label(self, text=town.loop.place_name(s), font=('Segoe UI', 23, 'bold'))
        self.location_title.pack(anchor='w')
        ttk.Label(self, text='IN PERSON  ·  The world outside your phone', foreground='#88cbb0').pack(anchor='w', pady=(4, 15))
        columns = ttk.Frame(self); columns.pack(fill='both', expand=True)
        activities = ttk.Frame(columns, padding=(0, 0, 24, 0)); activities.pack(side='left', fill='both', expand=True)
        ttk.Label(activities, text='What would you like to do?', font=('Segoe UI', 14, 'bold')).pack(anchor='w', pady=8)
        actions = [('Open phone', lambda: self.game.phone_window()),
                   ('Maps · travel somewhere', lambda: self.game.phone_window('Maps'))]
        if __import__('flashback_visits').area_for(s['player']):
            actions.insert(0,('Visit flashback area',lambda:__import__('flashback_visit_ui').open_in_person(self.game)))
        actions.insert(0, ('Interpol · cases, fines & field operations', lambda:__import__('interpol_ui').open_in_person(self.game)))
        actions.insert(0, ('Stories, guards & gang properties', lambda:__import__('campaign_ui').open_in_person(self.game,'Story')))
        actions.insert(0, ('Combat · Iron Circle / training / challenges', lambda:__import__('combat_ui').open_combat(self.game)))
        import job_apps
        employed=s.get('job_apps',{}).get('employment')
        if employed in job_apps.JOBS and job_apps.JOBS[employed]['venue']==w['location']:
            actions.insert(0,('Jobseek · enter workplace',self.workplace))
        if w['location']=='park' and not w['cast'][s['player']]['journey']:
            actions.insert(0,('Enter park · explore on foot',self.game.enter_park))
        if autonomy.status(s,s['player'])=='Asleep':
            actions.append(('Sleep speed / skip to waking',lambda:__import__('autonomy_ui').open_window(self.game)))
        if w['location'] in town.JOBS:
            name, pay = town.JOBS[w['location']]
            actions.append((f'{name} · +${pay}', lambda: self.act(town.work)))
        if w['location'] == town.HOMES[s['player']]:
            actions += [('Home activities', self.game.home_window), ('Rest at home', lambda: self.act(town.rest))]
        if w['location'] == 'marios_pizza': actions.append(("Order at Mario’s counter", self.pizza))
        if s['player']=='garrett': actions.append(('Find Charles · investigation', self.game.charles_search))
        elif __import__('charles_disclosure').eligible(s): actions.append(('Charles sighting · tell Garrett', self.game.charles_search))
        actions.append(('More location & relationship options', self.game.town_window))
        for label, callback in actions:
            ttk.Button(activities, text=label, command=callback, state='disabled' if self.game.busy else 'normal').pack(fill='x', pady=5)
        import crime_operations, crime_sites
        self.site_activities = None
        if crime_operations.site_of(w['location']) in crime_sites.SITES or w['location'] in ('archive','interpol_hq','glasshouse_lab'):
            from crime_sites_ui import SiteActivities
            self.site_activities = SiteActivities(activities, self.game)
            self.site_activities.pack(fill='both', expand=True)
        nearby = ttk.Frame(columns); nearby.pack(side='left', fill='both', expand=True)
        ttk.Label(nearby, text='People here', font=('Segoe UI', 14, 'bold')).pack(anchor='w', pady=8)
        canvas = tk.Canvas(nearby, highlightthickness=0, bg='#191c2b')
        scroll = ttk.Scrollbar(nearby, command=canvas.yview); scroll.pack(side='right', fill='y')
        canvas.pack(fill='both', expand=True); canvas.configure(yscrollcommand=scroll.set)
        body = ttk.Frame(canvas); win = canvas.create_window(0, 0, window=body, anchor='nw')
        body.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        canvas.bind('<Configure>', lambda e: canvas.itemconfigure(win, width=e.width))
        if not people and not w['npcs']: ttk.Label(body, text='A little time to yourself.').pack(anchor='w', pady=10)
        for who in people:
            known = town.hidden.known(s, who)
            name = core.contact_name(s, who) if known else 'Someone new'
            row = ttk.Frame(body, padding=6); row.pack(fill='x')
            ttk.Label(row, text=name + (' · In your party' if who in w['party'] else '')).pack(anchor='w')
            ttk.Button(row, text='Talk / hang out', command=lambda who=who: self.meet(who), state='disabled' if self.game.busy else 'normal').pack(anchor='w', pady=4)
        for name in w['npcs']:
            ttk.Button(body, text='Talk to ' + name, command=lambda name=name: self.local(name), state='disabled' if self.game.busy else 'normal').pack(fill='x', pady=4)
        if len(people) > 1:
            ttk.Button(body, text='Choose hangout companions', command=self.choose_companions,
                       state='disabled' if self.game.busy else 'normal').pack(fill='x', pady=10)

    def workplace(self):
        from jobseek_workplace_ui import open_workplace
        try: open_workplace(self.game)
        except ValueError as exc:
            messagebox.showinfo('Workplace',str(exc),parent=self.game)

    def choose_companions(self):
        if self.game.busy: return
        s = self.game.state_data
        dialog = AppWindow(self)
        dialog.title('Choose hangout companions')
        dialog.transient(self.winfo_toplevel())
        frame = ttk.Frame(dialog, padding=20); frame.pack(fill='both', expand=True)
        ttk.Label(frame, text='Who would you like to hang out with?', font=('Segoe UI', 14, 'bold')).pack(anchor='w')
        ttk.Label(frame, text='Choose one person for a private hangout, or several for a group.\nOnly selected companions join you and travel with you.').pack(anchor='w', pady=10)
        current = groups.hanging_out_with(s) | set(s['world']['party'])
        selections = {}
        for who in s['world']['cast']:
            if who == s['player'] or not town.loop.together(s, who): continue
            selected = tk.BooleanVar(value=who in current)
            selections[who] = selected
            name = core.contact_name(s, who) if town.hidden.known(s, who) else 'Someone new'
            ttk.Checkbutton(frame, text=name, variable=selected).pack(anchor='w', pady=4)
        count = tk.StringVar()
        ttk.Label(frame, textvariable=count).pack(anchor='w', pady=10)
        buttons = ttk.Frame(frame); buttons.pack(fill='x')
        def start():
            if self.game.busy: return
            try:
                groups.form(self.game.state_data, [who for who, value in selections.items() if value.get()])
            except ValueError as exc:
                messagebox.showinfo('Hangout companions', str(exc), parent=dialog)
                return
            dialog.destroy()
            self.game.persist()
            self.game.show_in_person()
        submit = ttk.Button(buttons, text='Start hangout', command=start); submit.pack(side='right')
        ttk.Button(buttons, text='Cancel', command=dialog.destroy).pack(side='right', padx=8)
        def update(*_):
            total = sum(value.get() for value in selections.values())
            count.set(f'{total} selected' + (' · One-on-one' if total == 1 else ''))
            submit.configure(state='normal' if total else 'disabled')
        for value in selections.values(): value.trace_add('write', update)
        update()
        dialog.grab_set()

    def act(self, fn, *args):
        if self.game.busy: return
        try: fn(self.game.state_data, *args)
        except ValueError as exc:
            messagebox.showinfo('Winterfield', str(exc), parent=self); return
        self.game.persist()
        self.game.show_in_person()

    def meet(self, who):
        self.act(town.meet, who)

    def local(self, name):
        self.act(groups.open_local, name)

    def pizza(self):
        self.game.town_window()
        self.game.town_activity.pizza_menu()
