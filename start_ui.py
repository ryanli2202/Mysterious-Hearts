"""Cinematic native start screen; character selection is separate from starting."""
import json
import tkinter as tk
from PIL import Image, ImageOps, ImageTk
import game_core as core
import qol_ui
import winterfield_ui as ui
from artwork import source_image

INK = '#10181f'
PANEL = '#18232b'
EDGE = '#344149'
CREAM = '#f4eddf'
MUTED = '#a5b3b7'
GOLD = '#dbb780'
CAST = {
    'garrett': ('THE FLAMING PRINCE', 'Charm. Fire. A softer side.',
                'Martial arts · Cooking · Charisma', '#d4a574'),
    'rei': ('THE QUIET MYSTERY', 'Some stories speak softly.',
            'Art · Martial arts · Introspection', '#a7becb'),
    'minsu': ('THE CAMPUS CHAMPION', 'A bright spark. An open heart.',
              'Medicine · Taekwondo · Friendship', '#abc5ac'),
    'ivan': ('THE JOKER CARD', 'Every smile holds a secret.',
             'Music · Ambition · Hidden depths', '#c8a6b8'),
}
import playable_cast
# Selection copy is authored separately from starting funds, jobs and home actions.
EXPANDED_DESCRIPTIONS = {
    'yuriko': ('THE SCENE MAKER', 'Small stages. Big possibilities.',
               'Theatre design · Miniatures · Costume sketches'),
    'emily': ('THE GENTLE BLOOM', 'Small kindnesses take root.',
              'Flowers · LEGO · Sewing'),
    'sophie': ('THE BRIGHT STRIDE', 'A little daring. A lot of heart.',
               'Athletics · Training · Friendship'),
    'amy': ('THE THOUGHTFUL DREAMER', 'Every colour holds a question.',
            'Painting · Philosophy · Sketching'),
    'samantha': ('THE FEARLESS SPARK', 'A fierce spirit. A ready laugh.',
                 'Martial arts · Motorcycles · Friendship'),
    'april': ('THE QUIET STRATEGIST', 'Still waters. A few moves ahead.',
              'Chess · Science · Astronomy'),
    'lena': ('THE CURIOUS CHRONICLER', 'Old photographs. New questions.',
             'Film photography · Local history · Salsa'),
    'naomi': ('THE STEADY HAND', 'Care lives in the little repairs.',
              'Bouldering · Ceramics · Mystery novels'),
    'celeste': ('THE STARLIT GUIDE', 'Wonder is better with company.',
                'Jazz piano · Birdwatching · Baking'),
    'dev': ('THE PATIENT INVENTOR', 'One loose wire. A new possibility.',
            'Electronics · Tabletop games · Night photography'),
    'rosa': ('THE NEIGHBOURHOOD HEART', 'There is room at the table.',
             'Cooking · Gardening · Roller skating'),
    'elliot': ('THE WILLOW WANDERER', 'Quiet paths have stories too.',
               'Field recording · Kayaking · Wood carving'),
    'tyler': ('THE CORNERSTONE', 'Steady hands. Room in your corner.',
              'Boxing · Dominoes · Baseball'),
    'valentina': ('THE FREE SAIL', 'A sure course. An off-key chorus.',
                  'Sailing · Sail repair · Karaoke'),
    'daniel': ('BLOOD OF LEGENDS', 'Some stories deserve another showing.',
               'Cinema · Judo · Drawing'),
    'neo': ('THE MISSING SHINIGAMI', 'An ordinary life worth building.',
            'Electronics · Co-op games · Cooking'),
    'alyssa': ('THE GENTLE BOOKBINDER', 'A little care between the pages.',
               'Bookbinding · Botanical sketching · Gardening'),
    'sylvanis': ('THE CRAZED DEMON', 'A delighted laugh. A dangerous turn.',
                 'Combat · Strategy · Chaos'),
    'martos': ('THE STEADFAST GUARDIAN', 'Quiet promises. Certain hands.',
               'Watch restoration · Strength training · Cooking'),
    'elias': ('THE GOLDEN PERFORMER', 'Beyond the spotlight, a life of his own.',
              'Cinema · Martial arts · Dance'),
    'mavis': ('THE RAIN LISTENER', 'Quiet company. On her own terms.',
              'Field recording · Electronics repair · Night walks'),
    'camila': ('THE KEEN STRATEGIST', 'A clear plan. An unexpected step.',
               'Chess · Fountain pens · Tango'),
    'fox': ('THE NIGHT’S BANE', 'The dark leaves clues of its own.',
            'Investigation · Fieldcraft · Martial arts'),
    'gordon': ('THE PRODIGAL SON', 'Resolve under pressure. Quiet off duty.',
               'Reading · Tactical training · Cooking'),
}
for _who, _spec in playable_cast.STARTS.items():
    CAST[_who] = (*EXPANDED_DESCRIPTIONS[_who], _spec['accent'])


def label(parent, text, size=11, color=CREAM, **kwargs):
    return tk.Label(parent, text=text, bg=parent['bg'], fg=color,
                    font=('Segoe UI', size), **kwargs)


def button(parent, text, command, primary=False, **kwargs):
    bg, fg = (GOLD, INK) if primary else (PANEL, CREAM)
    widget = tk.Button(parent, text=text, command=command, bg=bg, fg=fg,
                       activebackground='#ead0a7' if primary else '#293943',
                       activeforeground=INK if primary else CREAM,
                       font=('Segoe UI', 11, 'bold' if primary else 'normal'),
                       relief='flat', bd=0, padx=kwargs.pop('padx',16), pady=kwargs.pop('pady',12), cursor='hand2',
                       highlightthickness=1, highlightbackground=bg,
                       highlightcolor=GOLD, disabledforeground='#718088', **kwargs)
    widget.bind('<Enter>', lambda e: widget.configure(bg='#ead0a7' if primary else '#293943')
                if str(widget['state']) != 'disabled' else None)
    widget.bind('<Leave>', lambda e: widget.configure(bg=bg)
                if str(widget['state']) != 'disabled' else None)
    return widget


class CharacterPreview(tk.Canvas):
    def __init__(self, parent):
        super().__init__(parent, bg=PANEL, highlightthickness=0, bd=0)
        self.selected = 'garrett'
        self.dossier = None
        self.photo = None
        self.render_key = None
        self.pending = None
        self.bind('<Configure>', self.schedule)
        self.bind('<Destroy>', self.cleanup)

    def cleanup(self, event):
        if event.widget is self and self.pending:
            self.after_cancel(self.pending); self.pending = None

    def schedule(self, event=None):
        if self.pending: self.after_cancel(self.pending)
        self.pending = self.after(35, self.render)

    def select(self, key, dossier=None):
        self.selected = key
        self.dossier = dossier
        self.render_key = None
        self.render()

    def render(self):
        if self.pending: self.after_cancel(self.pending); self.pending = None
        w, h = self.winfo_width(), self.winfo_height()
        if w < 10 or h < 10: return
        key = (w, h, self.selected)
        if self.render_key == key: return
        self.render_key = key
        scene = ImageOps.fit(source_image('winterfield-dusk'), (w, h), Image.Resampling.LANCZOS).convert('RGBA')
        # Directional shade keeps live text readable while retaining the town lights.
        shade = Image.new('RGBA', (w, 1))
        shade.putdata([(10, 22, 29, round(235 - 125 * x/max(1, w-1))) for x in range(w)])
        scene = Image.alpha_composite(scene, shade.resize((w, h)))
        # Neo's selection asset is his square contact photo; use his existing cutout.
        path = self.dossier['portrait'] if self.dossier else core.ROOT / 'assets' / 'portraits' / ('neo-scene.png' if self.selected == 'neo' else self.selected+'-selection.png')
        if path and path.is_file():
            try:
                with Image.open(path) as source:
                    portrait = source.convert('RGBA')
                    import character_stature
                    import portrait_framing
                    box = portrait_framing.visible_bounds(portrait)
                    if box: portrait = portrait.crop(box)
                    size = (round(w*.60), round(h*.91))
                    height = character_stature.height_cm(self.selected, path)
                    if self.dossier and self.dossier.get('custom'):
                        # Saved menu previews need not be in the live registry.
                        height = float(self.dossier['details']['Height'].removesuffix(' cm'))
                    # A fixed reference makes selecting another person preserve
                    # stature; do not enlarge every character to the same height.
                    scale = size[1] / (211 * portrait_framing.VISIBLE_BODY_FRACTION)
                    scale = min(scale, portrait_framing.capacity(portrait, size, height))
                    portrait = portrait_framing.fit(portrait, size, height, scale)
                    scene.alpha_composite(portrait, (w-portrait.width-12, h-portrait.height))
            except (OSError, ValueError):
                pass
        fade = Image.new('RGBA', (1, h))
        fade.putdata([(16, 24, 31, round(220 * max(0, (y/h-.70)/.30))) for y in range(h)])
        scene = Image.alpha_composite(scene, fade.resize((w, h)))
        self.photo = ImageTk.PhotoImage(scene, master=self)
        self.delete('all')
        self.create_image(0, 0, image=self.photo, anchor='nw')
        x = 28 if w < 750 else 40
        d = self.dossier
        tag, mood, interests, accent = (d['tag'], d['hook'], d['interests'], d['accent']) if d else CAST[self.selected]
        if h < 330:
            self.create_text(x, 26, text=tag, anchor='nw', fill=accent, font=('Segoe UI', 9, 'bold'))
            self.create_text(x, 58, text=d['name'] if d else core.PLAYERS[self.selected], anchor='nw',
                             fill=CREAM, font=('Georgia', 25), width=max(180, int(w*.62)))
            self.create_text(x, h-42, text='STARTING PROFILE', anchor='nw', fill=MUTED, font=('Segoe UI', 9))
            if not path or not path.is_file():
                self.create_text(w*.8, h*.45, text=''.join(part[0] for part in (d['name'] if d else core.PLAYERS[self.selected]).split()[:2]), fill=MUTED, font=('Georgia', 38))
            return
        self.create_line(x, 39, x+28, 39, fill=accent, width=2)
        self.create_text(x+39, 39, text='M E E T   Y O U R   P R O T A G O N I S T',
                         anchor='w', fill=CREAM, font=('Segoe UI', 8))
        self.create_text(x, h*.24, text=tag, anchor='nw', fill=accent,
                         font=('Segoe UI', 9, 'bold'))
        name = (d['name'] if d else core.PLAYERS[self.selected]).replace(' ', '\n', 1)
        self.create_text(x-2, h*.24+33, text=name, anchor='nw', fill=CREAM,
                         font=('Georgia', 23 if w < 750 else 34), justify='left', width=max(170, int(w*.55)))
        self.create_text(x, h*.24+118, text=mood, anchor='nw', fill=CREAM,
                         font=('Georgia', 12, 'italic'), width=max(150, int(w*.39)))
        self.create_text(x, h-75, text=interests.replace(' · ', '\n'), anchor='sw',
                         fill='#d3dbd8', font=('Segoe UI', 10), justify='left')
        self.create_line(x, h-47, w-x, h-47, fill='#64716f')
        self.create_text(x, h-25, text='WINTERFIELD  /  A LIFE WAITING TO UNFOLD',
                         anchor='w', fill=CREAM, font=('Segoe UI', 8))
        self.create_text(w-x, h-25, text='CUSTOM' if d and d['custom'] else 'STARTING PROFILE',
                         anchor='e', fill=accent, font=('Segoe UI', 9))


class StartScreen(ui.TextureFrame):
    def __init__(self, game):
        super().__init__(game, bg=INK)
        self.game = game
        self.selected = getattr(game, 'menu_character', 'garrett')
        self.custom_profiles = {}
        self.dossier_tab = 'Overview'
        self.filtered = list(CAST)
        self.pack(fill='both', expand=True)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        rail = tk.Frame(self, bg=INK, width=230)
        self.rail = rail
        rail.grid(row=0, column=0, sticky='nsew', padx=(18, 14), pady=(22, 16))
        rail.grid_propagate(False)
        rail.columnconfigure(0, weight=1)
        rail.rowconfigure(3, weight=1)
        brand = tk.Frame(rail, bg=INK); brand.grid(row=0, column=0, sticky='ew')
        label(brand, 'A   W I N T E R F I E L D   S T O R Y', 8, GOLD, anchor='w').pack(fill='x')
        tk.Label(brand, text='Mysterious\nHearts', bg=INK, fg=CREAM,
                 font=('Georgia', 29), justify='left', anchor='w').pack(fill='x', pady=(10, 8))
        label(brand, 'A town full of lives.\nA story only you can tell.', 11, MUTED,
              justify='left', anchor='w').pack(fill='x')
        tk.Frame(brand, bg=EDGE, height=1).pack(fill='x', pady=(14, 12))
        resume = tk.Frame(rail, bg=INK); resume.grid(row=1, column=0, sticky='ew')
        available = False
        unreadable = False
        if core.SAVE.exists():
            try:
                candidate = json.loads(core.SAVE.read_text(encoding='utf-8'))
                available = isinstance(candidate, dict) and candidate.get('player') in core.PLAYERS and isinstance(candidate.get('routes'), dict)
                if isinstance(candidate, dict) and __import__('custom_protagonist').is_custom(candidate.get('player')):
                    __import__('custom_protagonist').validate(candidate.get('custom_protagonist'))
                    available = isinstance(candidate.get('routes'), dict)
                unreadable = not available
            except (OSError, ValueError, TypeError):
                unreadable = True
        self.continue_button = button(resume, 'Continue your story   →', game.continue_game, primary=True, anchor='w')
        self.continue_button.pack(fill='x')
        if not available: self.continue_button.configure(state='disabled', bg='#26343b', highlightbackground='#26343b')
        summary = 'Recovery available in your story library.' if unreadable else 'Your next chapter starts here.'
        if available:
            try:
                saved = json.loads(core.SAVE.read_text(encoding='utf-8'))
                summary = 'Last played as '+saved.get('custom_protagonist', {}).get('name', core.PLAYERS.get(saved.get('player'), 'your protagonist'))
            except (OSError, ValueError, AttributeError): summary = 'Recovery available in your story library.'
        label(resume, summary, 9, MUTED, anchor='w', wraplength=280, justify='left').pack(fill='x', pady=(9, 18))
        button(resume, 'New Story', self.new_story, primary=not available, anchor='w').pack(fill='x', pady=(0, 8))
        button(resume, 'Story library & backups', lambda: qol_ui.saves(game), anchor='w').pack(fill='x', pady=(0, 8))
        button(resume, 'Portrait gallery', game.gallery_window, anchor='w').pack(fill='x')
        button(resume, 'Patch notes & update history', lambda:__import__('patch_notes_ui').open_window(game), anchor='w').pack(fill='x', pady=(8, 0))
        bottom = tk.Frame(rail, bg=INK); bottom.grid(row=4, column=0, sticky='sew')
        label(bottom, 'MAKE YOURSELF AT HOME', 8, GOLD, anchor='w').pack(fill='x', pady=(16, 12))
        button(bottom, 'AI & account', game.accounts, anchor='w').pack(fill='x', pady=(0, 8))
        self.sound = button(bottom, '', self.toggle_sound, anchor='w')
        self.sound.pack(fill='x'); self.sound_label()
        label(bottom, 'Your choices. Your pace. Your story.', 9, MUTED, anchor='w').pack(fill='x', pady=(20, 0))
        right = tk.Frame(self, bg=INK)
        right.grid(row=0, column=1, sticky='nsew', padx=(0, 18), pady=(22, 16))
        right.columnconfigure(0, weight=1); right.rowconfigure(1, weight=1)
        heading = tk.Frame(right, bg=INK); heading.grid(row=0, column=0, sticky='ew', pady=(0, 16))
        label(heading, 'Begin a new chapter', 18, CREAM, anchor='w').pack(side='left')
        label(heading, 'CHOOSE YOUR PERSPECTIVE', 8, MUTED).pack(side='right')
        self.stage = tk.Frame(right, bg=INK)
        self.stage.grid(row=1, column=0, sticky='nsew')
        self.stage.columnconfigure(0, weight=3)
        self.stage.columnconfigure(1, weight=2)
        self.stage.rowconfigure(0, weight=1)
        self.preview = CharacterPreview(self.stage)
        self.preview.configure(highlightthickness=1, highlightbackground=EDGE)
        self.preview.grid(row=0, column=0, sticky='nsew')
        self.build_dossier()
        choices = tk.Frame(right, bg=INK); choices.grid(row=2, column=0, sticky='ew', pady=(12, 16))
        paging = tk.Frame(choices, bg=INK); paging.grid(row=0, column=0, columnspan=4, sticky='ew', pady=(0, 6))
        button(paging, '‹ Previous', lambda:self.change_page(-1)).pack(side='left')
        self.page_label = label(paging, '', 9, MUTED); self.page_label.pack(side='left', expand=True)
        button(paging, 'Next ›', lambda:self.change_page(1)).pack(side='right')
        self.page = 0
        self.choice_parent = choices
        self.choices = {}
        self.tile_photos = {}
        for index, key in enumerate(CAST):
            col = index % 4
            choices.columnconfigure(col, weight=1, uniform='cast')
            control = button(choices, core.PLAYERS[key], lambda k=key:self.select(k))
            control.configure(padx=4, pady=7, wraplength=140)
            self.tile_art(control, key)
            control.grid(row=1, column=col, sticky='ew', padx=(0 if col == 0 else 4, 0 if col == 3 else 4))
            # Selection colours remain visible after the pointer leaves.
            control.bind('<Leave>', lambda e,k=key:self.paint_choice(k))
            self.roster_keys(control, key)
            self.choices[key] = control
        action = tk.Frame(right, bg=INK); action.grid(row=3, column=0, sticky='ew')
        self.begin = button(action, '', self.begin_selected, primary=True)
        self.begin.pack(side='right')
        button(action, 'Create your own', lambda: __import__('custom_creator_ui').CharacterCreator(game, on_saved=self.profile_saved)).pack(side='left')
        button(action, 'Saved characters', self.saved_characters).pack(side='left', padx=8)
        self.edit_character = button(action, 'Edit selected', self.edit_selected)
        self.edit_character.pack(side='left')
        footer = tk.Frame(self, bg='#0c1319')
        footer.grid(row=1, column=0, columnspan=2, sticky='ew')
        game.status = label(footer, game.model_status, 9, MUTED, anchor='w')
        game.status.pack(side='left', padx=32, pady=13)
        label(footer, 'MYSTERIOUS HEARTS', 8, '#77888f').pack(side='right', padx=30)
        self.bind('<Configure>', self.resize, add='+')
        self.refresh_roster(recover=True)

    def resize(self, event):
        if event.widget is self:
            self.game.status.configure(wraplength=max(350, self.winfo_width()-260))
            compact = self.winfo_width() < 1180
            if getattr(self, '_compact', None) != compact:
                self._compact = compact
                self.dossier_panel.grid_forget()
                self.stage.columnconfigure(1, weight=0 if compact else 2)
                self.stage.rowconfigure(1, weight=1 if compact else 0)
                self.dossier_panel.grid(row=1 if compact else 0, column=0 if compact else 1, sticky='nsew', padx=0 if compact else (12, 0))

    def saved_characters(self):
        import custom_library
        window = tk.Toplevel(self)
        window.title('Saved characters')
        window.configure(bg=INK)
        window.geometry('620x480')
        label(window, 'Your characters · New playthrough', 18).pack(pady=16)
        label(window, 'Profiles and portraits stay here when story saves are deleted.', 10, MUTED).pack()
        status = label(window, '', 10, GOLD, wraplength=560)
        status.pack(pady=8)
        try:
            profiles = custom_library.profiles(core.SAVE.parent)
        except OSError as exc:
            status.configure(text='Could not open character library: ' + str(exc))
            return
        listing = tk.Listbox(window, bg=PANEL, fg=CREAM, selectbackground=EDGE,
                             selectforeground=CREAM, font=('Segoe UI', 12),
                             highlightbackground=EDGE, relief='flat', exportselection=False)
        listing.pack(fill='both', expand=True, padx=20, pady=8)
        for profile in profiles:
            listing.insert('end', f"{profile['name']} · {profile['age']} · {profile['occupation']}")
        def begin():
            if not listing.curselection(): return
            profile = profiles[listing.curselection()[0]]
            try:
                self.game.start_custom(profile, profile['portrait'])
            except Exception as exc:
                status.configure(text=str(exc))
                return
            if window.winfo_exists(): window.destroy()
        control = button(window, 'Begin new playthrough', begin, primary=True)
        control.pack(pady=14)
        if profiles:
            listing.selection_set(0)
        else:
            status.configure(text='No saved characters yet. Choose Create your own to make one.')
            control.configure(state='disabled')

    def paint_choice(self, key):
        selected = self.selected == key
        self.choices[key].configure(bg='#35434a' if selected else PANEL,
                                    fg=GOLD if selected else MUTED,
                                    highlightbackground=GOLD if selected else PANEL)

    def build_dossier(self):
        from tkinter import ttk
        import phone_theme
        self.dossier_panel = tk.Frame(self.stage, bg=PANEL)
        self.dossier_panel.grid(row=0, column=1, sticky='nsew', padx=(12, 0))
        tabs = tk.Frame(self.dossier_panel, bg=PANEL); tabs.pack(fill='x')
        for tab in ('Overview', 'Backstory', 'Details', 'Awakened'):
            button(tabs, tab, lambda t=tab:self.show_dossier(t), padx=4, pady=8).pack(side='left', expand=True, fill='x')
        body = tk.Frame(self.dossier_panel, bg=PANEL); body.pack(fill='both', expand=True)
        scroll = ttk.Scrollbar(body); scroll.pack(side='right', fill='y')
        self.dossier_text = tk.Text(body, bg=PANEL, fg=CREAM, insertbackground=CREAM,
            selectbackground=EDGE, selectforeground=CREAM, wrap='word', relief='flat',
            font=('Segoe UI', 10), width=30, height=8, padx=12, pady=12, yscrollcommand=scroll.set)
        self.dossier_text.pack(fill='both', expand=True); scroll.configure(command=self.dossier_text.yview)
        searchbar = tk.Frame(self.stage.master, bg=INK)
        searchbar.grid(row=4, column=0, sticky='ew', pady=(8, 0))
        self.search = tk.StringVar()
        entry = tk.Entry(searchbar, textvariable=self.search, bg=PANEL, fg=CREAM, insertbackground=CREAM,
                         selectbackground=EDGE, relief='flat', font=('Segoe UI', 10))
        label(searchbar, 'Search name', 9, MUTED).pack(side='left', padx=(0, 8))
        entry.pack(side='left', fill='x', expand=True)
        self.filter = tk.StringVar(value='All')
        picker = ttk.Combobox(searchbar, textvariable=self.filter, values=('All', 'Canonical', 'My Characters'), state='readonly', width=14)
        picker.pack(side='right', padx=(8, 0))
        self.search.trace_add('write', lambda *_:self.filter_roster())
        self.filter.trace_add('write', lambda *_:self.filter_roster())
        self.library_status = label(self.stage.master, '', 9, MUTED, anchor='w', wraplength=680)
        self.library_status.grid(row=5, column=0, sticky='ew')
        phone_theme.apply_tree(self.dossier_panel)
        phone_theme.apply_tree(searchbar)

    def tile_art(self, control, key, profile=None):
        try:
            import character_dossier
            path = character_dossier.starting(key, profile)['portrait']
            if path and path.is_file():
                with Image.open(path) as source:
                    art = ImageOps.fit(source.convert('RGBA'), (52, 60), Image.Resampling.LANCZOS, centering=(.5, .15))
                self.tile_photos[key] = ImageTk.PhotoImage(art, master=self)
                control.configure(image=self.tile_photos[key], compound='top')
        except (OSError, ValueError):
            pass

    def refresh_roster(self, recover=False, select=None):
        import custom_library
        errors = custom_library.recover(core.SAVE.parent) if recover else []
        profiles, read_errors = custom_library.enumerate_profiles(core.SAVE.parent)
        errors += read_errors
        for key in self.custom_profiles:
            if key in self.choices: self.choices.pop(key).destroy()
        self.custom_profiles = {p['profile_id']:p for p in profiles}
        for index, (key, p) in enumerate(self.custom_profiles.items(), len(CAST)):
            control = button(self.choice_parent, p['name'] + ' · Custom · ' + key[:6], lambda k=key:self.select(k), padx=4, pady=7)
            control.configure(wraplength=140)
            self.tile_art(control, key, p)
            control.grid(row=1, column=index%4, sticky='ew', padx=4)
            control.bind('<Leave>', lambda e,k=key:self.paint_choice(k))
            self.roster_keys(control, key)
            self.choices[key] = control
        self.library_status.configure(text=('Library needs attention: ' + ' | '.join(errors)) if errors else 'Profiles start new stories. Drafts are kept separately.')
        self.selected = select or self.selected
        self.filter_roster()

    def profile_saved(self, profile):
        self.search.set(''); self.filter.set('All')
        self.refresh_roster(select=profile['profile_id'])

    def edit_selected(self):
        if self.selected not in self.custom_profiles: return
        import custom_creator_ui
        custom_creator_ui.CharacterCreator(self.game, on_saved=self.profile_saved,
                                           profile=self.custom_profiles[self.selected])

    def roster_keys(self, control, key):
        def move(offset):
            if key not in self.filtered: return 'break'
            chosen = self.filtered[(self.filtered.index(key)+offset) % len(self.filtered)]
            self.select(chosen); self.choices[chosen].focus_set()
            return 'break'
        control.bind('<Left>', lambda e:move(-1))
        control.bind('<Right>', lambda e:move(1))
        control.bind('<Return>', lambda e:self.select(key))

    def filter_roster(self):
        query, category = self.search.get().casefold().strip(), self.filter.get()
        self.filtered = [k for k in self.choices if
            (category != 'Canonical' or k in CAST) and (category != 'My Characters' or k in self.custom_profiles)
            and query in (self.custom_profiles[k]['name'] if k in self.custom_profiles else core.PLAYERS[k]).casefold()]
        if self.selected not in self.filtered:
            self.selected = self.filtered[0] if self.filtered else None
        if self.selected: self.select(self.selected)
        else:
            for control in self.choices.values(): control.grid_remove()
            self.preview.grid_remove()
            self.begin.configure(text='No character selected', state='disabled')
            self.edit_character.configure(state='disabled')
            self.page_label.configure(text='No matches · clear search or create a character')
            self.dossier_text.configure(state='normal'); self.dossier_text.delete('1.0', 'end')
            self.dossier_text.insert('end', 'No matching characters. Clear the search, choose All, or Create your own.')
            self.dossier_text.configure(state='disabled')

    def show_dossier(self, tab=None):
        import character_dossier
        if tab: self.dossier_tab = tab
        if not self.selected: return
        self.dossier_text.configure(state='normal'); self.dossier_text.delete('1.0', 'end')
        self.dossier_text.insert('end', character_dossier.text(self.current_dossier, self.dossier_tab))
        self.dossier_text.configure(state='disabled')

    def select(self, key):
        import character_dossier
        if key not in self.choices: key = next(iter(self.choices))
        if key not in self.filtered:
            self.search.set(''); self.filter.set('All')
        self.selected = self.game.menu_character = key
        self.page = self.filtered.index(key) // 4
        for control in self.choices.values(): control.grid_remove()
        for index, who in enumerate(self.filtered[self.page*4:self.page*4+4]):
            self.choices[who].grid(row=1, column=index)
        self.page_label.configure(text=f'Characters {self.page + 1} / {(len(self.filtered)+3)//4}')
        for who in self.choices: self.paint_choice(who)
        self.current_dossier = character_dossier.starting(key, self.custom_profiles.get(key))
        self.preview.grid()
        self.preview.select(key, self.current_dossier)
        self.show_dossier()
        self.begin.configure(text='Begin as '+self.current_dossier['name']+'   →', state='normal', wraplength=300)
        self.edit_character.configure(state='normal' if key in self.custom_profiles else 'disabled')

    def change_page(self, direction):
        if not self.filtered: return
        page = (self.page + direction) % ((len(self.filtered)+3)//4)
        self.select(self.filtered[page*4])

    def begin_selected(self):
        if not self.selected: return
        if self.selected in self.custom_profiles:
            p = self.custom_profiles[self.selected]
            try: self.game.start_custom(p, p['portrait'])
            except (OSError, ValueError) as exc: self.library_status.configure(text=str(exc))
        else: self.game.start(self.selected)

    def new_story(self):
        self.search.set(''); self.filter.set('All')
        if self.selected: self.choices[self.selected].focus_set()

    def sound_label(self):
        self.sound.configure(text='Sound   ·   '+('On' if self.game.sounds.enabled else 'Off'))

    def toggle_sound(self):
        self.game.sounds.toggle(); self.sound_label()
