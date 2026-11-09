"""Mysterious Hearts native desktop client."""
import copy
import queue
import threading
import time
import qol
import qol_ui
import suggestions as reply_suggestions
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from phone_dialogs import AppWindow, messagebox, simpledialog
from PIL import Image, ImageTk, ImageDraw
import groups
import game_core as core
from sound import SoundSystem
from notifications_ui import NotificationPopups
import winterfield_ui as ui

BG, PANEL, CARD, TEXT, MUTED, GOLD = '#10121c', '#191c2b', '#222638', '#f3eee7', '#aaaabd', '#dfba78'
OUTFITS = {
    'ivan': {
        'Black blazer and mock neck': 'selection',
        'Gym tank and shorts': 'gym-tank',
        'Gym performance set': 'gym-training',
        'Ivory sculptural tailoring': 'fashion-ivory',
        'Burgundy silk couture': 'fashion-burgundy',
        'Pearl grey runway': 'fashion-pearl',
        'Midnight crystal stagewear': 'idol-midnight',
        'White and gold stagewear': 'idol-white',
        'Crimson stagewear': 'idol-crimson',
        'Layered denim streetwear': 'street-denim',
        'Navy varsity streetwear': 'street-varsity',
        'Monochrome streetwear': 'street-monochrome',
        'Sage knit streetwear': 'street-knit',
        'Shirtless beachwear': 'beach',
    },
    'garrett': {
        'Black suit': 'selection', 'Ivory linen suit': 'ivory',
        'Midnight tuxedo': 'formal-tuxedo', 'Burgundy evening suit': 'formal-burgundy',
        'Jade streetwear': 'street-jade', 'Ink streetwear': 'street-ink',
        'Brocade changshan': 'traditional-changshan', 'Jade hanfu': 'traditional-hanfu',
        'Asymmetric runway': 'fashion-asymmetric', 'Pearl couture': 'fashion-pearl',
        'Summer linen shirt': 'summer-linen', 'Winter wool coat': 'winter-coat',
        'Gym training tank': 'gym-tank', 'Gym compression shirt': 'gym-compression',
        'Shirtless beach shorts': 'beach-shorts',
    },
    'rei': {
        'Black suit': 'selection', 'Black leather moto jacket': 'moto',
        'Black knit sweater': 'black-sweater', 'Charcoal hoodie': 'charcoal-hoodie',
        'Washed denim jacket': 'denim-jacket', 'Burgundy satin shirt': 'burgundy-shirt',
        'Cream cardigan': 'cream-cardigan', 'Olive bomber jacket': 'olive-bomber',
        'Tailored waistcoat': 'tailored-waistcoat', 'Camel overcoat': 'camel-overcoat',
        'Japanese techwear': 'streetwear-techwear', 'Sukajan streetwear': 'streetwear-sukajan',
        'Navy yukata': 'navy-yukata', 'Haori and hakama': 'haori-hakama',
        'Gym tank and shorts': 'gym', 'Shirtless beachwear': 'beach',
    },
    'minsu': {
        'Black bomber jacket': 'selection', 'Forest varsity jacket': 'varsity',
        'Seoul denim layers': 'street-denim', 'Monochrome streetwear': 'street-monochrome',
        'Retro track streetwear': 'street-track',
        'Gym training tank': 'gym-tank', 'Gym compression shirt': 'gym-compression',
        'College rugby shirt': 'college-rugby', 'College plaid overshirt': 'college-overshirt',
        'College knit polo': 'college-knit',
        'Library cardigan': 'study-cardigan', 'Late-night study hoodie': 'study-hoodie',
        'Medical student white coat': 'med-white-coat', 'Medical student scrubs': 'med-scrubs',
        'Shirtless beach shorts': 'beach-shorts',
    },
}

def wardrobe_options(player):
    if core.custom_protagonist.is_custom(player):
        return {'Signature portrait': 'selection'}
    if player == 'ivan':
        return OUTFITS[player]
    return OUTFITS[player] | {'Home clothes': 'home', 'Sleepwear': 'sleep'}

class Game(tk.Tk):
    def __init__(self):
        super().__init__()
        ui.install(self)
        self.profile_view = None
        self.title('Mysterious Hearts')
        self.geometry('1220x940')
        self.minsize(1000, 800)
        self.configure(bg=BG)
        self.state_data = None
        self.sounds = SoundSystem()
        self.notification_popups = NotificationPopups(self)
        self.events = queue.Queue()
        self.busy = False
        self.in_game = False
        self.idle_clock = time.monotonic()
        from simulation_clock import SimulationClock
        self.simulation_clock = SimulationClock()
        self.token = 0
        self.pending = None
        self.generation_started = 0
        self.generation_stage = 'Writing response'
        self.preview_dialogue = ''
        self.suggestion_job = None
        self.suggestion_serial = 0
        self.suggestion_status = ''
        self.suggestion_status_target = None
        self.photos = {}
        self.home_activity = None
        self.town_activity = None
        self.calendar_view = None
        self.last_world_location = None
        self.shown_group = None
        self.model_status = 'Checking AI connection…'
        self.protocol('WM_DELETE_WINDOW', self.close)
        self.home()
        from grove import GrovePump
        self.grove_pump = GrovePump(self)
        from messaging import MessagePump
        self.message_pump = MessagePump(self)
        from meet_cute_ai import ReplyPump
        self.meet_cute_pump = ReplyPump(self)
        from hearts_ai import NotePump
        self.hearts_pump = NotePump(self)
        self.after(1000, self.poll_grove)
        self.after(100, self.poll)
        threading.Thread(target=self.check, daemon=True).start()

    def poll_grove(self):
        self.grove_pump.tick()
        self.after(1000, self.poll_grove)

    def label(self, parent, text, size=12, color=TEXT, **kw):
        return tk.Label(parent, text=text, font=('Segoe UI', size), bg=parent['bg'], fg=color, **kw)

    def button(self, parent, text, command, accent=False, **kw):
        return tk.Button(parent, text=text, command=command, font=('Segoe UI', 11),
            bg=GOLD if accent else CARD, fg=BG if accent else TEXT, activebackground='#d2b47e',
            activeforeground=BG, disabledforeground='#686b7b', relief='flat', bd=0,
            padx=14, pady=10, cursor='hand2', **kw)

    def clear(self):
        self.unbind('<F11>')
        self.unbind('<Escape>')
        self.attributes('-fullscreen', False)
        self.notification_popups.pending.clear()
        self.notification_popups.dismiss(show_next=False)
        for widget in self.winfo_children(): widget.destroy()

    def portrait(self, key, size, location=None, minute=None, outfit=None):
        if key in {person[0] for person in (*core.town.NPCS, *core.town.VENUE_STAFF.values(), core.town.HQ_EXECUTIVE)}:
            key = key.lower().replace(' ', '-')
        variant = 'home' if key in core.town.HOMES and location == core.town.HOMES[key] else 'selection'
        # April keeps one daytime outfit per game day; sleepwear still takes priority.
        april_looks = ('selection', 'sage-knit', 'plaid-blazer', 'blue-oxford',
                       'rose-cardigan', 'burgundy-dress', 'denim-weekend',
                       'cream-cable-knit', 'camel-trench')
        daytime_variant = (april_looks[(int(minute) // 1440) % len(april_looks)]
                           if key == 'april' and minute is not None else variant)
        if key == 'april' and minute is not None:
            occasion_index = (int(minute) // 1440) % 2
            if location == 'beach':
                daytime_variant = ('beach-bikini', 'beach-swimsuit')[occasion_index]
            elif location in ('track', 'boxing_club'):
                daytime_variant = 'gym-plum'
            elif location in ('bar', 'nightclub') and minute % 1440 >= 17 * 60:
                daytime_variant = ('formal-emerald', 'formal-ivory-suit')[occasion_index]
        if key == 'samantha' and minute is not None:
            day = int(minute) // 1440
            casual_looks = ('selection', 'red-moto', 'denim-cargo', 'charcoal-hoodie',
                            'olive-bomber', 'black-mockneck', 'red-flannel')
            daytime_variant = casual_looks[day % len(casual_looks)]
            if location == 'beach':
                daytime_variant = ('beach-black-bikini', 'beach-red-bikini',
                                   'beach-teal-bikini')[day % 3]
            elif location in ('track', 'boxing_club'):
                daytime_variant = ('gym-charcoal', 'gym-olive')[day % 2]
            elif location in ('bar', 'nightclub') and minute % 1440 >= 17 * 60:
                daytime_variant = ('formal-black-suit', 'formal-burgundy-dress')[day % 2]
        path = core.ROOT / 'assets' / 'portraits' / (key + '-' + daytime_variant + '.png')
        if key == 'neo':
            # Keep the Grove photo separate from the transparent dialogue sprite.
            path = path.with_name('neo-scene.png')
        # Sleepwear follows the clock, including for the player whose activity
        # is controlled manually. Being away from home always uses outdoor art.
        if variant == 'home' and minute is not None and core.town.loop.appointment(key, minute)[2] == 'Sleep':
            sleep_path = path.with_name(key + '-sleep.png')
            if sleep_path.exists():
                path = sleep_path
        if outfit:
            path = path.with_name(key + '-' + outfit + '.png')
        import four_aces
        if key == (getattr(self, 'state_data', None) or {}).get('player'):
            import camera
            chosen = self.state_data['world'].get('player_outfit')
            available = camera.outfits(self.state_data, key)
            if chosen in available:
                path = core.ROOT / available[chosen]
        # Headquarters attire overrides Ivan's saved player wardrobe without changing it.
        # A location-less portrait is a profile preview, not the current scene.
        if four_aces.uniform_at(key, location) and (not outfit or key == 'ivan'):
            path = core.ROOT / 'assets' / 'portraits' / (key + '-syndicate.png')
        if not path.exists():
            path = core.ROOT / 'assets' / 'portraits' / (key + '-selection.png')
        if key == 'charles':
            path = core.ROOT / 'assets' / 'portraits' / 'charles-selection-v2.png'
        if core.custom_protagonist.is_custom(key):
            path = core.custom_protagonist.portrait_path(core.custom_protagonist._profiles[key])
        cache = (key, size, str(path))
        if cache not in self.photos:
            if not path.exists():
                im = Image.new('RGBA', size, CARD)
                draw = ImageDraw.Draw(im)
                name = core.CONTACTS[key][0] if key in core.CONTACTS else key.replace('-', ' ').title()
                draw.text((size[0]//2, size[1]//2), ''.join(part[0] for part in name.split()), fill=GOLD, anchor='mm', font_size=max(18, size[0]//4))
                self.photos[cache] = ImageTk.PhotoImage(im)
                return self.photos[cache]
            with Image.open(path) as source:
                im = source.convert('RGBA')
                heights = {'garrett': 188, 'rei': 184, 'minsu': 177, 'ivan': 193}
                if key in heights:
                    # Use Garrett's framing as the common scale, rather than letting
                    # different source aspect ratios change the apparent height.
                    reference_height = min(size[1], size[0] * 1374 / 1145)
                    target_height = min(size[1], round(reference_height * heights[key] / 188))
                    im.thumbnail((size[0], target_height), Image.Resampling.LANCZOS)
                    frame = Image.new('RGBA', size, (0, 0, 0, 0))
                    frame.alpha_composite(im, ((size[0] - im.width) // 2, size[1] - im.height))
                    im = frame
                else:
                    im.thumbnail(size, Image.Resampling.LANCZOS)
                self.photos[cache] = ImageTk.PhotoImage(im)
        return self.photos[cache]

    def home(self):
        self.cancel_suggestions()
        self.sounds.set_typing(False)
        self.in_game = False
        self.pending = None
        self.clear()
        from start_ui import StartScreen
        self.start_screen = StartScreen(self)

    def sound_button(self, parent):
        def toggle():
            self.sounds.toggle()
            button.config(text='Sound: On' if self.sounds.enabled else 'Sound: Off')
        button = self.button(parent, 'Sound: On' if self.sounds.enabled else 'Sound: Off', toggle)
        return button

    def accounts(self):
        if self.busy: return
        from account_ui import AccountWindow
        AccountWindow(self)

    def gallery_window(self):
        from gallery_ui import GalleryWindow
        if self.state_data is None:
            try:
                saved_state = core.load()
            except (OSError, ValueError):
                saved_state = None
            GalleryWindow(self, lambda: self.state_data if self.state_data is not None else saved_state)
        else:
            GalleryWindow(self)

    def check(self):
        try:
            model = core.check_model()
            self.events.put(('status', 'AI ready · ' + model))
        except Exception as exc: self.events.put(('status', str(exc)))

    def start(self, player):
        if self.busy: return
        try:
            previous = self.state_data or core.load()
            if previous: core.save(previous)
        except (ValueError, OSError, KeyError) as exc:
            messagebox.showerror('Could not preserve previous story', str(exc)); return
        self.state_data = core.fresh(player)
        self.persist()
        self.play_screen()

    def continue_game(self):
        try:
            state = core.load()
            if state is None:
                messagebox.showinfo('No saved story', 'Choose a protagonist to begin.')
                return
            self.state_data = state
            self.play_screen()
            qol_ui.overview(self, True)
        except Exception as exc:
            qol_ui.recover(self, exc)

    def start_custom(self, profile, portrait):
        if self.busy:
            raise ValueError('Wait for the current action to finish.')
        state = core.custom_protagonist.create(profile, portrait)
        previous = self.state_data or core.load()
        if previous:
            core.save(previous)
        core.save(state)
        self.state_data = state
        self.play_screen()
        self.town_window()

    def persist(self):
        if not self.state_data: return
        if self.state_data:
            self.capture_draft()
        try: core.save(self.state_data)
        except OSError as exc: messagebox.showerror('Could not save', 'Your story is still open, but could not be saved:\n' + str(exc))

    def wardrobe_menu(self, parent):
        state = self.state_data
        import camera
        looks = camera.outfits(state, state['player'])
        button = tk.Menubutton(parent, text='Wardrobe ▾', bg=CARD, fg=TEXT, padx=12, pady=8,
                               font=('Segoe UI', 11), relief='flat')
        menu = tk.Menu(button, tearoff=False)
        button.configure(menu=menu)
        def wear(label):
            if label == 'Automatic':
                state['world'].pop('player_outfit', None)
            else:
                state['world']['player_outfit'] = label
            self.persist()
            self.render()
        for label in ('Automatic', *looks):
            menu.add_radiobutton(label=label, variable=self.outfit_name, value=label,
                                 command=lambda choice=label: wear(choice))
        return button

    def play_screen(self):
        self.cancel_suggestions()
        self.sounds.observe(self.state_data)
        self.notification_popups.observe(self.state_data)
        self.in_game = True
        self.simulation_clock.reset(self.state_data)
        self.idle_clock = time.monotonic()
        self.clear()
        self.shown_group = None
        self.group_selected = False
        self.personal_panel = False
        self.navigation = []
        self.contact_buttons = {}
        top = tk.Frame(self, bg=BG, padx=20, pady=12)
        top.pack(fill='x')
        self.label(top, 'MYSTERIOUS HEARTS', 17, GOLD).pack(side='left')
        tools = tk.Menubutton(top, text='Tools ▾', bg=CARD, fg=TEXT, padx=12, pady=8)
        menu = tk.Menu(tools, tearoff=False)
        menu.add_command(label='Daily agenda', command=lambda:qol_ui.overview(self))
        menu.add_command(label='Life & availability · Wait / sleep', command=lambda:__import__('autonomy_ui').open_window(self))
        menu.add_command(label='Saves & recovery', command=lambda:qol_ui.saves(self))
        menu.add_command(label='Patch notes & update history', command=lambda:__import__('patch_notes_ui').open_window(self))
        menu.add_command(label='Interpol · cases, fines & operations', command=lambda:__import__('interpol_ui').open_in_person(self))
        menu.add_command(label='Search conversations', command=lambda:qol_ui.journal(self))
        tools.configure(menu=menu); tools.pack(side='right', padx=4)
        self.clock_label = self.label(top, '', 11, MUTED)
        self.clock_label.pack(side='left', padx=24)
        import simulation_clock
        self.time_mode = tk.StringVar(value=simulation_clock.mode(self.state_data))
        self.time_button = tk.Menubutton(top, text='Time ▾', bg=CARD, fg=TEXT, padx=8, pady=8)
        time_menu = tk.Menu(self.time_button, tearoff=False)
        for value, label in simulation_clock.LABELS.items():
            time_menu.add_radiobutton(label=label, value=value, variable=self.time_mode,
                                     command=lambda value=value: self.set_time_mode(value))
        self.time_button.configure(menu=time_menu)
        self.time_button.pack(side='left')
        self.calendar_button = self.button(top, 'Calendar', self.open_calendar)
        if self.state_data['player'] == 'garrett':
            lead_button = self.button(top, 'Find Charles', self.charles_search)
            self.navigation.append(lead_button)
        b = self.button(top, 'Save & menu', self.menu)
        b.pack(side='right'); self.navigation.append(b)
        self.outfit_name = tk.StringVar(value=self.state_data['world'].get('player_outfit', 'Automatic'))
        body = tk.Frame(self, bg=BG)
        self.play_body = body
        body.pack(fill='both', expand=True, padx=18, pady=(0, 15))
        sidebar = tk.Frame(body, bg=PANEL, width=205, padx=12, pady=15)
        # Retain the conversation controllers, but navigation lives on the phone.
        sidebar.pack_propagate(False)
        contact_canvas = tk.Canvas(sidebar, bg=PANEL, highlightthickness=0)
        contact_scroll = ttk.Scrollbar(sidebar, command=contact_canvas.yview)
        contact_scroll.pack(side='right', fill='y'); contact_canvas.pack(fill='both', expand=True)
        contact_canvas.configure(yscrollcommand=contact_scroll.set)
        sidebar = tk.Frame(contact_canvas, bg=PANEL)
        contact_panel = contact_canvas.create_window((0,0), window=sidebar, anchor='nw')
        sidebar.bind('<Configure>', lambda e: contact_canvas.configure(scrollregion=contact_canvas.bbox('all')))
        contact_canvas.bind('<Configure>', lambda e: contact_canvas.itemconfigure(contact_panel, width=e.width))
        self.label(sidebar, 'PEOPLE OF WINTERFIELD', 10, GOLD).pack(anchor='w', pady=(0, 12))
        for key, person in core.CONTACTS.items():
            if key == self.state_data['player']: continue
            b = self.button(sidebar, person[0], lambda k=key: self.select(k), anchor='w')
            b.pack(fill='x', pady=2); self.navigation.append(b)
            self.contact_buttons[key] = b
        self.group_button = self.button(sidebar, 'Hangouts', self.select_group, anchor='w')
        self.group_button.pack(fill='x', pady=2)
        self.button(sidebar, 'Rename contact', self.rename_contact).pack(fill='x', pady=2)
        self.text_groups = tk.Frame(sidebar, bg=PANEL)
        self.text_groups.pack(fill='x')
        self.text_buttons = {}
        add_group = self.button(sidebar, '+  New group text', self.new_text_group, anchor='w')
        add_group.pack(fill='x', pady=2)
        self.navigation.append(add_group)
        self.home_button = self.button(sidebar, 'Home · Self actions', self.home_window)
        self.home_button.pack(fill='x', pady=6); self.navigation.append(self.home_button)
        town_button = self.button(sidebar, 'Town · Free roam', self.town_window, True)
        town_button.pack(fill='x', pady=12); self.navigation.append(town_button)
        phone_button = self.button(sidebar, 'Phone · Grove & delivery', self.phone_window)
        phone_button.pack(fill='x', pady=4); self.navigation.append(phone_button)
        self.button(sidebar, 'Conversation journal', self.journal).pack(fill='x')
        self.button(sidebar, 'Character profiles', self.open_profiles).pack(fill='x', pady=3)
        self.button(sidebar, 'Portrait gallery', self.gallery_window).pack(fill='x', pady=6)
        account_button = self.button(sidebar, 'AI & account', self.accounts)
        account_button.pack(fill='x', pady=8); self.navigation.append(account_button)
        main = tk.Frame(body, bg=BG)
        self.in_person_chat = main
        main.pack(side='left', fill='both', expand=True)
        from hangout_ui import HangoutView
        self.hangout_view = HangoutView(main, self)
        self.hangout_view.pack(fill='both', expand=True)
        self.bind('<F11>', lambda e: self.hangout_view.toggle_fullscreen())
        self.bind('<Escape>', lambda e: self.hangout_view.set_fullscreen(False))
        from presence_ui import PresenceView
        self.presence_view = PresenceView(body, self)
        self.open_phone_button = self.button(top, 'Open phone', self.phone_window, True)
        self.open_phone_button.pack(side='left', padx=8)
        self.phone_notification = tk.Label(self.open_phone_button, text='●', fg='#ff453a',
                                           bg=GOLD, font=('Segoe UI', 11), bd=0)
        self.phone_notification.bind('<Button-1>', lambda e: self.phone_window())
        self.update_phone_notification()
        self.button(top, 'In person', self.show_in_person).pack(side='left', padx=4)
        self.render()
        self.restore_draft()
        self.after_idle(self.show_world_windows)
        self.after_idle(lambda:self.show_in_person(hide_phone=False))

    def update_phone_notification(self):
        from phone_icons import unread_messages
        from grove_gallery import unread_comments
        import meet_cute
        dot = getattr(self, 'phone_notification', None)
        if dot is not None and dot.winfo_exists():
            if self.state_data and (unread_messages(self.state_data) or unread_comments(self.state_data) or meet_cute.unread(self.state_data)):
                dot.place(relx=1, x=-2, y=0, anchor='ne')
            else:
                dot.place_forget()

    def begin_incoming(self):
        if self.group_selected or self.busy or self.pending: return
        route = self.state_data['routes'][self.state_data['active']]
        if not route['dialogue']:
            self.retry_or_begin()

    def chat_available(self, key):
        state = self.state_data
        return core.hidden.contact(state, key) or (
            core.hidden.known(state, key)
            and state['routes'][key].get('channel') == 'in_person'
            and core.town.loop.together(state, key))

    def open_calendar(self, day=None):
        from calendar_ui import CalendarWindow
        if self.calendar_view and self.calendar_view.winfo_exists():
            self.calendar_view.show(self.calendar_view.today())
            self.calendar_view.lift()
        else:
            self.calendar_view = CalendarWindow(self)
        if day: self.calendar_view.show(day)

    def open_profiles(self, who=None):
        from profile_ui import ProfileWindow
        if self.profile_view and self.profile_view.winfo_exists():
            self.profile_view.refresh(who)
            self.profile_view.deiconify()
            self.profile_view.lift()
        else:
            self.profile_view = ProfileWindow(self, who)
        return self.profile_view

    def rename_contact(self):
        win = AppWindow(self)
        win.title('Rename contact')
        state = self.state_data
        keys = [k for k in self.contact_buttons if self.chat_available(k)]
        for key in keys:
            def edit(who=key):
                name = simpledialog.askstring('Rename contact', core.CONTACTS[who][0]+' · Leave blank to reset',
                                              initialvalue=core.contact_name(state,who), parent=win)
                if name is None: return
                name = name.strip()
                if len(name) > 32:
                    messagebox.showinfo('Rename contact','Use up to 32 characters.',parent=win)
                    return
                names = state.setdefault('nicknames', {})
                if name and name != core.CONTACTS[who][0]: names[who] = name
                else: names.pop(who, None)
                self.persist()
                self.render()
                win.destroy()
            tk.Button(win,text=core.contact_name(state,key),command=edit).pack(fill='x',padx=12,pady=2)

    def render(self):
        state = self.state_data
        groups.sync_contacts(state)
        # Migrate an older save's current spoken conversation into Hangouts.
        if not state.get('active_group'):
            who = state['active']
            if state['routes'][who].get('channel') == 'in_person' and core.town.loop.together(state, who):
                groups.open_solo(state, who)
        for key, button in self.contact_buttons.items():
            if self.chat_available(key):
                if not button.winfo_manager(): button.pack(fill='x', pady=2, before=self.group_button)
            else: button.pack_forget()
            unread = state['routes'][key].get('unread', 0)
            button.config(text=core.contact_name(state,key) + (f' ({unread})' if unread else ''))
        gid = state.get('active_group')
        if gid != self.shown_group:
            self.shown_group = gid
            if gid and not self.selected_text_group():
                self.switch_chat(gid)
        for key, chat in state['groups'].items():
            if chat.get('channel') != 'text': continue
            if key not in self.text_buttons:
                button = self.button(self.text_groups, chat['name'], lambda k=key: self.select_group(k),
                                     anchor='w', wraplength=135)
                button.pack(fill='x', pady=2)
                self.text_buttons[key] = button
            self.text_buttons[key].config(state='disabled' if self.busy else 'normal')
        self.group_button.config(text='Hangouts · Active' if gid else 'Hangouts',
                                 state='normal' if (gid or state.get('last_hangout')) and not self.busy else 'disabled')
        who = state['active']; person = core.CONTACTS[who]; route = state['routes'][who]
        name = core.contact_name(state, who)
        self.home_button.config(state='normal' if not self.busy and state['world']['location']==core.town.HOMES[state['player']] else 'disabled')
        self.clock_label.config(text=core.town.loop.clock(state) + f" · ${core.town.ensure(state)['money']:,}")
        import simulation_clock
        selected_time = simulation_clock.mode(state)
        self.time_mode.set(selected_time)
        self.time_button.config(text={'slow': 'Time · 0.5× ▾', 'normal': 'Time · 1× ▾', 'fast': 'Time · 3× ▾',
                                     'faster': 'Time · 8× ▾', 'paused': 'Time · Paused ▾'}[selected_time])
        today = core.town.loop.dates.story_date(state['world']['minute'])
        occasions = core.town.loop.dates.events(state, today)
        self.calendar_button.config(text='Calendar •' if occasions else 'Calendar')
        if self.calendar_view and self.calendar_view.winfo_exists():
            self.calendar_view.draw()
        if self.profile_view and self.profile_view.winfo_exists():
            self.profile_view.refresh()
        group = state['groups'].get(self.group_selected)
        members = group['members'] if group else [who]
        texting = not group or group.get('channel') == 'text'
        town_only = bool(members) and all(core.town.character_types.is_town(member) for member in members)
        if town_only:
            self.personal_panel = False
        enabled = not self.busy and not self.hangout_view.combat_actions.response and (texting or group.get('open'))
        tones = core.choice_tones(state, group)
        choices = reply_suggestions.visible(group or route, 'personal' if self.personal_panel else 'main')
        action_choices = reply_suggestions.visible(group or route, 'actions')
        reply_tones = core.PERSONAL_TONES if self.personal_panel else tones
        for i, button in enumerate(self.choices):
            prefix = reply_tones[i] + ' · ' if self.personal_panel or (group or route).get('ordered_tones') else ''
            button.configure(text=f'{i+1}  {prefix}{choices[i]}' if choices else '',
                             state='normal' if enabled and choices else 'disabled')
        for i, button in enumerate(self.action_choices):
            button.configure(text=f'{i+1}  {tones[i]} · {action_choices[i]}' if action_choices else '',
                             state='normal' if enabled and not texting and action_choices else 'disabled')
        for widget in (self.send, self.entry):
            widget.configure(state='normal' if enabled else 'disabled')
        for widget in (self.action_send, self.action_entry):
            widget.configure(state='normal' if enabled and not texting else 'disabled')
        self.send.configure(text=('Text as ' if texting else 'Say as ') + core.PLAYERS[state['player']].split()[0])
        self.panel_switch.configure(text='Main replies' if self.personal_panel else 'Personal talk',
                                    state='normal' if enabled and not town_only else 'disabled')
        self.retry.configure(text='Retry response' if self.pending else 'Continue hangout',
                             state='normal' if enabled and (not group or self.pending or group.get('solo') or group.get('local')) else 'disabled')
        self.end_hangout_button.configure(state='normal' if enabled and not texting else 'disabled')
        self.cancel_button.configure(state='normal' if self.busy else 'disabled')
        date = core.dating.session(state, (group or {}).get('solo', who)) if not group or group.get('solo') else None
        if date:
            self.goal_button.configure(text=f"Date goals {len(date['done'])}/3")
            self.goal_button.pack(side='left', padx=3)
        else:
            self.goal_button.pack_forget()
        available = enabled and reply_suggestions.ready(state, self.suggestion_target())
        self.suggest_button.configure(text='Cancel suggestions' if self.suggestion_job else 'Suggest personal replies' if self.personal_panel else 'Suggest replies',
                                      state='normal' if available else 'disabled')
        self.suggest_actions.configure(text='Cancel suggestions' if self.suggestion_job else 'Suggest actions',
                                       state='normal' if available and not texting else 'disabled')
        self.group_button.configure(bg=GOLD if group and not texting else CARD,
                                    fg=BG if group and not texting else TEXT)
        for key, button in self.contact_buttons.items():
            button.configure(bg=GOLD if not group and key == who else CARD,
                             fg=BG if not group and key == who else TEXT)
        if not texting:
            self.hangout_view.refresh(group)
        self.layout_presence()

    def layout_presence(self):
        if not hasattr(self, 'presence_view') or not self.presence_view.winfo_exists(): return
        response=self.hangout_view.combat_actions.response
        if response:
            view=getattr(self,'combat_view',None)
            if view and view.winfo_exists(): view.place_forget()
            self.presence_view.pack_forget()
            self.in_person_chat.pack(side='left',fill='both',expand=True)
            group=self.state_data['groups'].get(self.hangout_view.combat_actions.gid,{})
            self.hangout_view.canvas.show(group)
            return
        import combat
        if combat.active(self.state_data):
            view=getattr(self,'combat_view',None)
            if view is None or not view.winfo_exists():
                from combat_ui import CombatView
                view=self.combat_view=CombatView(self.presence_view.master,self)
                view.refresh()
            view.place(x=0,y=0,relwidth=1,relheight=1); view.lift()
        group = self.state_data['groups'].get(self.group_selected, {})
        area=getattr(self,'area_view',None)
        if area is not None and area.winfo_exists():
            wrong_place=getattr(area,'location_key',None) not in (None,self.state_data['world']['location'])
            if wrong_place or (group.get('open') and group.get('channel')!='text'):
                self.area_view=None;area.destroy()
            else:
                self.presence_view.pack_forget();self.in_person_chat.pack_forget()
                area.pack(fill='both',expand=True)
                return
        if group.get('open') and group.get('channel') != 'text':
            self.presence_view.pack_forget()
            self.in_person_chat.pack(side='left', fill='both', expand=True)
        else:
            self.in_person_chat.pack_forget()
            self.presence_view.pack(fill='both', expand=True)
            self.presence_view.refresh()

    def show_in_person(self, hide_phone=True):
        if self.busy: return
        self.close_main_area()
        if hide_phone:self.hide_phone_for_location()
        s = self.state_data
        groups.reconcile(s)
        gid = s.get('active_group')
        if not gid and s['world']['party']:
            gid = groups.open_group(s, s['world']['party'])
        self.switch_chat(gid or False)
        if gid and s['groups'][gid].get('solo'):
            who = s['groups'][gid]['solo']
            s['active'] = who
            self.restore_channel(who, 'in_person')
        self.persist()
        self.render()


    def chat_blocks(self, pane=None):
        if not self.group_selected:
            return core.transcript(self.state_data, self.pending, pane=pane)
        blocks = []
        group = self.state_data['groups'][self.group_selected]
        labels = {core.CONTACTS.get(key, (key,))[0]:core.contact_name(self.state_data,key) for key in group['members']}
        for line in group['history']:
            action = line.get('kind') == 'action'
            if pane is None or (pane == 'actions') == action:
                tag = 'scene' if line['speaker'] == 'Narrator' else ''
                blocks.append((labels.get(line['speaker'], line['speaker']), line['text'], tag))
        return blocks

    def switch_chat(self, group):
        self.capture_draft()
        self.group_selected = group
        self.personal_panel = False
        self.pending = None
        for entry in (self.entry, self.action_entry):
            entry.config(state='normal')
            entry.delete(0, 'end')

    def selected_text_group(self):
        return self.state_data['groups'].get(self.group_selected, {}).get('channel') == 'text'

    def new_text_group(self):
        if self.busy: return
        win = AppWindow(self)
        win.title('New group text')
        win.configure(bg=PANEL)
        win.transient(self)
        win.grab_set()
        self.label(win, 'Group name').pack(anchor='w', padx=12, pady=4)
        name = tk.Entry(win, width=38)
        name.pack(fill='x', padx=12)
        self.label(win, 'Choose at least two contacts').pack(anchor='w', padx=12, pady=6)
        members = {}
        for key in dict.fromkeys([*core.CONTACTS, *self.state_data.get('npc_chats', {})]):
            if key == self.state_data['player'] or not core.hidden.contact(self.state_data, key): continue
            members[key] = tk.BooleanVar(win)
            tk.Checkbutton(win, text=core.contact_name(self.state_data,key), variable=members[key]).pack(anchor='w', padx=12)
        def create():
            try:
                gid = groups.create_text(self.state_data, name.get(), [k for k,v in members.items() if v.get()])
            except ValueError as exc:
                messagebox.showinfo('New group text', str(exc), parent=win)
                return
            self.persist()
            win.destroy()
            self.select_group(gid)
            phone = getattr(self, 'phone_activity', None)
            if phone and phone.winfo_exists(): phone.open_thread(gid, True)
        self.button(win, 'Create group text', create, True).pack(fill='x', padx=12, pady=8)
        name.focus_set()

    def select_group(self, gid=None):
        gid = gid or self.state_data.get('active_group') or self.state_data.get('last_hangout')
        if self.busy or not gid: return
        if self.state_data['groups'][gid].get('channel') == 'text':
            try: groups.require_text_available(self.state_data, self.state_data['groups'][gid]['members'])
            except ValueError as exc:
                messagebox.showinfo('Messages', str(exc), parent=self); return
        if self.group_selected != gid: self.switch_chat(gid)
        self.restore_draft()
        group = self.state_data['groups'][gid]
        if group.get('solo') and group.get('open'):
            self.state_data['active'] = group['solo']
            self.restore_channel(group['solo'], 'in_person')
        self.render()

    def select(self, key):
        if self.busy or not self.chat_available(key): return
        try: groups.require_text_available(self.state_data, [key])
        except ValueError as exc:
            messagebox.showinfo('Messages', str(exc), parent=self); return
        self.switch_chat(False)
        self.state_data['active'] = key
        self.restore_draft()
        self.restore_channel(key, 'text')
        self.persist(); self.render()
        self.begin_incoming()

    def end_hangout(self):
        if self.busy: return
        groups.disband(self.state_data)
        core.town.end_hangouts(self.state_data)
        self.persist()
        self.render()

    def restore_channel(self, who, channel):
        import json
        route = self.state_data['routes'][who]
        if route.get('channel') == channel: return
        route['channel'] = channel
        scene = next((json.loads(m['content']) for m in reversed(route['history'])
                      if m['role'] == 'assistant' and m.get('channel') == channel), {})
        route.update(dialogue=scene.get('dialogue', ''), scene=scene.get('narration', ''),
                     choices=scene.get('choices', []), personal_choices=scene.get('personal_choices', []),
                     action_choices=scene.get('action_choices', []), suggestions_requested=[],
                     suggestions_deferred=scene.get('suggestions_deferred',False))

    def show_date_goals(self):
        state = self.state_data
        messagebox.showinfo('Date with ' + core.contact_name(state, state['active']),
                            core.dating.describe(state, state['active']), parent=self)

    def toggle_panel(self):
        self.personal_panel = not self.personal_panel
        self.hangout_view.set_mode('reply')
        self.render()

    def choose(self, i):
        chat = self.state_data['groups'].get(self.group_selected) or self.state_data['routes'][self.state_data['active']]
        choices = reply_suggestions.visible(chat,'personal' if self.personal_panel else 'main')
        if choices: self.submit(choices[i])

    def custom(self):
        if not self.group_selected and not self.state_data['routes'][self.state_data['active']]['dialogue']: return
        text = self.entry.get().strip()
        if not text: return
        if len(text) > 2000:
            messagebox.showinfo('Long reply', 'Please keep your response under 2,000 characters.'); return
        self.submit(text)

    def choose_action(self, index):
        if self.busy or self.selected_text_group() or (not self.group_selected and core.is_texting(self.state_data)): return
        group = self.state_data['groups'].get(self.group_selected)
        choices = reply_suggestions.visible(group or self.state_data['routes'][self.state_data['active']],'actions')
        if choices: self.submit(core.ACTION_PREFIX + choices[index])

    def custom_action(self):
        if self.busy or self.selected_text_group() or (not self.group_selected and core.is_texting(self.state_data)): return
        text = self.action_entry.get().strip()
        if not text: return
        if len(text) > 2000:
            messagebox.showinfo('Long action', 'Please keep your action under 2,000 characters.')
            return
        self.submit(core.ACTION_PREFIX + text)

    def retry_or_begin(self):
        if self.group_selected:
            group = self.state_data['groups'][self.group_selected]
            if self.pending: self.submit(self.pending)
            elif group.get('open') and group.get('channel') != 'text': self.submit(core.SCENE_DIRECTIONS[1])
            return
        route = self.state_data['routes'][self.state_data['active']]
        if self.pending:
            action = self.pending
        elif not core.is_texting(self.state_data):
            action = core.SCENE_DIRECTIONS[1] if route['dialogue'] else core.SCENE_DIRECTIONS[0]
        else:
            action = core.SCENE_DIRECTIONS[1] if any(m['role']=='assistant' for m in route['history']) else core.INCOMING_TEXT
        self.submit(action)

    def set_busy(self, value):
        if value:
            self.generation_started = time.monotonic()
            self.generation_stage = 'Writing response'
            self.preview_dialogue = ''
        if not value:
            self.sounds.set_typing(False)
        self.busy = value
        self.cancel_button.config(state='normal' if value else 'disabled')
        for b in self.navigation + [self.send, self.retry]: b.config(state='disabled' if value else 'normal')
        self.entry.config(state='disabled' if value else 'normal')
        self.render()

    def submit(self, action, photo_id=None):
        import combat
        if combat.active(self.state_data) or combat.recovering(self.state_data):
            self.status.configure(text='Finish combat or recover before interacting.'); return
        group = self.state_data['groups'].get(self.group_selected)
        if group and any(combat.recovering(self.state_data,who) for who in group.get('members',[])):
            self.status.configure(text='A participant is recovering from a knockout.'); return
        if not group or group.get('channel') == 'text':
            import messaging
            self.cancel_suggestions()
            key = self.group_selected or self.state_data['active']
            try:
                if photo_id is None and action in (*core.SCENE_DIRECTIONS, core.INCOMING_TEXT):
                    t = messaging.thread(self.state_data, key, bool(group))
                    t['error'] = None
                    if not t['pending'] and not t['reason']:
                        if group:
                            t['reason'] = {'text': 'Initiate a natural group conversation.', 'offer': None}
                        else:
                            messaging.initiate(self.state_data, key, 'Initiate a natural conversation for your own reason. Do not answer an imaginary player message.')
                else:
                    messaging.send(self.state_data, key, action, bool(group), photo_id=photo_id)
                    self.state_data.setdefault('photo_drafts', {}).pop(self.draft_key(), None)
                    self.sounds.play('sent')
                    self.state_data.setdefault('drafts', {}).pop(self.draft_key(), None)
                    self.entry.delete(0, 'end')
                    phone = getattr(self, 'phone_activity', None)
                    if phone and phone.winfo_exists() and getattr(phone, 'selected', '') == 'Conversation': phone.message_entry.delete(0, 'end')
                self.persist(); self.render()
            except ValueError as exc: messagebox.showinfo('Messages', str(exc), parent=self)
            return
        if self.busy: return
        self.cancel_suggestions()
        group = self.state_data['groups'].get(self.group_selected)
        if not group or group.get('channel') == 'text':
            try: groups.require_text_available(self.state_data, group['members'] if group else [self.state_data['active']])
            except ValueError as exc:
                messagebox.showinfo('Messages', str(exc), parent=self); return
        if group and group.get('channel') != 'text' and not group.get('open'): return
        if not group:
            self.restore_channel(self.state_data['active'], 'text')
        self.idle_clock = time.monotonic()
        self.pending = action; self.token += 1
        self.generation_started = time.monotonic()
        self.generation_stage = 'Writing response'
        self.preview_dialogue = ''
        token = self.token; snapshot = copy.deepcopy(self.state_data)
        gid = self.group_selected
        snapshot['_text_only'] = not gid
        texting = self.state_data['groups'][gid].get('channel') == 'text' if gid else core.is_texting(self.state_data)
        if texting and core.player_message(self.state_data, action)['kind'] == 'player_reply':
            self.sounds.play('sent')
        self.set_busy(True)
        self.sounds.set_typing(texting)
        self.status.config(text='Writing the next scene with ' + core.provider_label() + '…')
        def work():
            try:
                def progress(stage, dialogue):
                    self.events.put(('progress', token, stage, dialogue))
                data = groups.generate(snapshot, gid, action, progress=progress) if gid else core.generate(snapshot, action, progress=progress)
                self.events.put(('result', token, action, data, gid))
            except Exception as exc: self.events.put(('error', token, str(exc)))
        threading.Thread(target=work, daemon=True).start()

    def set_time_mode(self, value):
        self.capture_draft()
        self.simulation_clock.set_mode(self.state_data, value, active=self.in_game)
        self.persist()
        self.render()

    def poll(self):
        hangout=getattr(self,'hangout_view',None)
        interaction=getattr(hangout,'combat_actions',None)
        reading_combat=bool(interaction and (interaction.working or interaction.response))
        elapsed = self.simulation_clock.tick(self.state_data, self.in_game and not reading_combat)
        import supafast
        supafast.tick(self)
        if elapsed:
            self.capture_draft()
            self.persist()
            self.render()
        if hasattr(self, 'message_pump'): self.message_pump.tick()
        if hasattr(self, 'meet_cute_pump'): self.meet_cute_pump.tick()
        if hasattr(self, 'hearts_pump'): self.hearts_pump.tick()
        self.update_phone_notification()
        try:
            while True:
                event = self.events.get_nowait()
                if event[0] == 'status':
                    self.model_status = event[1]
                    if not self.busy: self.status.config(text=event[1])
                elif event[0] == 'suggestions':
                    _, job, lines, error = event
                    if self.suggestion_job != job: continue
                    self.suggestion_job = None
                    try:
                        applied = not error and reply_suggestions.apply(self.state_data,job['target'],job['kind'],job['stamp'],lines)
                    except (KeyError, ValueError): applied = False
                    self.suggestion_status = error or ('Suggestions ready.' if applied else 'Suggestions discarded because the conversation changed.')
                    if applied: self.persist()
                    self.status.config(text=self.suggestion_status)
                    self.render()
                    callback=job.get('callback')
                    if callback: callback()
                elif event[1] == self.token:
                    if event[0] == 'progress':
                        self.generation_stage = event[2]
                        self.preview_dialogue = event[3]
                    elif event[0] == 'result':
                        try:
                            before = qol.stats(self.state_data)
                            phone = getattr(self, 'phone_activity', None)
                            key = event[4] or self.state_data['active']
                            read = bool(phone and phone.winfo_exists() and phone.is_reading_thread(key, bool(event[4])))
                            if event[4]:
                                groups.commit(self.state_data, event[4], event[2], event[3], mark_read=read)
                            else:
                                core.commit(self.state_data, event[2], event[3], mark_read=read)
                        except ValueError as exc:
                            self.set_busy(False)
                            self.status.config(text=str(exc))
                            continue
                        self.pending = None
                        self.state_data.setdefault('drafts', {}).pop(self.draft_key(), None)
                        phone = getattr(self, 'phone_activity', None)
                        if phone and phone.winfo_exists() and getattr(phone, 'selected', '') == 'Conversation':
                            phone.message_entry.delete(0, 'end')
                        self.set_busy(False); self.entry.delete(0, 'end'); self.action_entry.delete(0, 'end'); self.persist()
                        self.status.config(text='Story autosaved · Using ' + core.provider_label())
                        changes = qol.changes(before, self.state_data)
                        if changes and self.state_data.get('show_relationship_changes', True):
                            self.status.config(text=' · '.join(changes))
                        self.show_world_windows()
                    else:
                        self.set_busy(False)
                        self.status.config(text=event[2])
        except queue.Empty: pass
        if self.in_game and self.state_data:
            if self.busy:
                self.status.config(text=self.wait_status())
            reminders = self.state_data.get('event_notifications', [])
            if reminders and not self.busy:
                notices = '\n\n'.join(reminders); reminders.clear(); self.persist()
                messagebox.showinfo('Calendar reminder', notices, parent=self)
            self.sounds.observe(self.state_data)
            self.notification_popups.observe(self.state_data)
            self.update_phone_notification()
        self.after(100, self.poll)

    def suggestion_target(self):
        return ('group', self.group_selected) if self.group_selected else ('route', self.state_data['active'])

    def cancel_suggestions(self):
        self.suggestion_serial += 1
        self.suggestion_job = None
        self.suggestion_status = ''
        self.suggestion_status_target = None

    def request_suggestions(self, kind='main', target=None, callback=None):
        if self.busy: return
        target = target or self.suggestion_target()
        if self.suggestion_job:
            self.cancel_suggestions(); self.render()
            if callback: callback()
            return
        if not reply_suggestions.ready(self.state_data,target): return
        chat=reply_suggestions.chat(self.state_data,target)
        cached=reply_suggestions.visible(chat,kind)
        if cached:
            self.render()
            if callback: callback()
            return
        self.suggestion_serial += 1
        job=dict(serial=self.suggestion_serial,target=target,kind=kind,stamp=reply_suggestions.stamp(self.state_data,target),callback=callback)
        self.suggestion_job=job
        self.suggestion_status_target=target
        self.suggestion_status='Preparing suggestions. You can still type and send your own reply.'
        snapshot=copy.deepcopy(self.state_data)
        self.status.config(text=self.suggestion_status); self.render()
        def work():
            try: self.events.put(('suggestions',job,reply_suggestions.generate(snapshot,target,kind),None))
            except Exception as exc: self.events.put(('suggestions',job,None,str(exc)))
        threading.Thread(target=work,daemon=True).start()

    def draft_key(self):
        return ('group:' + str(self.group_selected)) if getattr(self, 'group_selected', False) else 'route:' + self.state_data['active']

    def capture_draft(self):
        if not self.state_data or not self.in_game: return
        phone = getattr(self, 'phone_activity', None)
        if phone and phone.winfo_exists(): phone.capture_message_draft()
        if phone and phone.winfo_exists():
            lifestyle = getattr(phone, 'lifestyle_view', None)
            if lifestyle is not None: lifestyle.capture()
            meet_cute_view = getattr(phone, 'meet_cute_view', None)
            if meet_cute_view is not None: meet_cute_view.capture()
            number_entry=getattr(phone,'contact_number_entry',None)
            if number_entry is not None and number_entry.winfo_exists():
                import phone_numbers
                phone_numbers.ensure(self.state_data)['draft']=number_entry.get()
        if phone and phone.winfo_exists() and phone.selected == 'Conversation': return
        entry = getattr(self, 'entry', None)
        if entry is not None and entry.winfo_exists():
            self.state_data.setdefault('drafts', {})[self.draft_key()] = entry.get()

    def restore_draft(self):
        self.entry.delete(0, 'end')
        self.entry.insert(0, self.state_data.get('drafts', {}).get(self.draft_key(), ''))

    def wait_status(self):
        return f'{self.generation_stage} · {int(time.monotonic()-self.generation_started)}s'

    def cancel_generation(self):
        if not self.busy: return
        external = getattr(self, 'external_cancel', None)
        if external:
            self.external_cancel = None
            external()
            return
        self.token += 1
        action = self.pending
        self.pending = None; self.preview_dialogue = ''
        physical_action = bool(action and action.startswith(core.ACTION_PREFIX))
        if action and not physical_action and action not in (*core.SCENE_DIRECTIONS, core.INCOMING_TEXT):
            self.state_data.setdefault('drafts', {})[self.draft_key()] = action
            phone = getattr(self, 'phone_activity', None)
            if phone and phone.winfo_exists() and phone.selected == 'Conversation':
                phone.message_entry.delete(0, 'end'); phone.message_entry.insert(0, action)
        self.set_busy(False); self.restore_draft()
        if physical_action:
            self.action_entry.delete(0, 'end')
            self.action_entry.insert(0, action[len(core.ACTION_PREFIX):])
            self.hangout_view.set_mode('action')
        self.persist()
        self.status.config(text='Response cancelled. Your unfinished turn was not applied.')

    def home_window(self):
        if self.busy or self.state_data['world']['location'] != core.town.HOMES[self.state_data['player']]: return
        from activity_ui import HomeWindow
        if self.home_activity and self.home_activity.winfo_exists():
            self.home_activity.render(); self.home_activity.lift()
        else: self.home_activity = HomeWindow(self)

    def show_world_windows(self):
        if self.busy: return
        self.last_world_location = self.state_data['world']['location']
        self.layout_presence()

    def phone_window(self, selected='Home'):
        import combat
        if self.state_data and (combat.active(self.state_data) or combat.recovering(self.state_data)):
            __import__('combat_ui').open_combat(self); return
        from phone_ui import PhoneWindow
        previous = getattr(self, 'phone_activity', None)
        if previous and previous.winfo_exists():
            previous.closing = False
            previous.deiconify()
            previous.open_app(selected)
            previous.lift()
            return
        self.phone_activity = PhoneWindow(self, selected)

    def town_window(self):
        if self.busy: return
        from town_ui import TownPanel
        self.close_main_area()
        self.hide_phone_for_location()
        self.town_activity=TownPanel(self)
        self.area_view=self.town_activity
        self.layout_presence()

    def hide_phone_for_location(self):
        phone=getattr(self,'phone_activity',None)
        if phone is not None and phone.winfo_exists():phone.withdraw()
        self.lift();self.focus_set()

    def close_main_area(self):
        area=getattr(self,'area_view',None)
        self.area_view=None
        if area is not None and area.winfo_exists():area.destroy()

    def leave_main_area(self):
        self.close_main_area()
        self.layout_presence()
        self.focus_set()

    def enter_park(self):
        if self.busy or self.state_data['world']['location']!='park':return
        if self.state_data['world']['cast'][self.state_data['player']]['journey']:return
        from park_ui import ParkView
        self.close_main_area()
        self.hide_phone_for_location()
        self.area_view=ParkView(self.play_body,self,self.leave_main_area)
        self.layout_presence()

    def open_living_world(self, window=None):
        if window is not None: window.destroy()
        self.phone_window('Winterfield')

    def charles_search(self):
        if self.busy or (self.state_data['player'] != 'garrett' and not __import__('charles_disclosure').eligible(self.state_data)): return
        from charles_quest_ui import QuestPanel
        core.town.end_hangouts(self.state_data)
        self.group_selected = False
        self.close_main_area()
        self.hide_phone_for_location()
        self.area_view = QuestPanel(self.play_body,self,self.leave_main_area)
        self.layout_presence()

    def journal(self):
        win = AppWindow(self); win.title('Conversation journal'); win.geometry('730x600'); win.configure(bg=BG)
        self.label(win, 'Conversation journal', 19, GOLD).pack(anchor='w', padx=18, pady=12)
        box = ui.transcript(win)
        scroll = ttk.Scrollbar(win, command=box.yview)
        scroll.pack(side='right', fill='y')
        box.configure(yscrollcommand=scroll.set)
        box.pack(fill='both', expand=True, padx=(12, 0), pady=(0, 12))
        for label, text, tag in self.chat_blocks():
            box.insert('end', label + '\n', 'player' if tag == 'player' else 'speaker')
            box.insert('end', text + '\n\n', 'aside' if tag in ('status','scene') else '')
        box.config(state='disabled'); box.see('end')

    def menu(self):
        if self.busy: return
        self.persist(); self.home()

    def close(self):
        if self.busy and not messagebox.askyesno('Leave conversation?', 'A response is still generating. Close without this unfinished response?'): return
        if self.state_data: self.persist()
        self.sounds.close()
        self.destroy()

if __name__ == '__main__':
    Game().mainloop()
