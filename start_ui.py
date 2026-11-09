"""Cinematic native start screen; character selection is separate from starting."""
import json
import tkinter as tk
from PIL import Image, ImageOps, ImageTk
import game_core as core
import qol_ui
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
for _who, _spec in playable_cast.STARTS.items():
    CAST[_who] = (_spec['title'].upper(), f"${_spec['money']:,} starting funds.\n{_spec['project']}.",
                  ' · '.join(_spec['home']), _spec['accent'])


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

    def select(self, key):
        self.selected = key
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
        path = core.ROOT / 'assets' / 'portraits' / (self.selected+'-selection.png')
        with Image.open(path) as source:
            portrait = source.convert('RGBA')
            box = portrait.getbbox()
            if box: portrait = portrait.crop(box)
            portrait.thumbnail((round(w*.60), round(h*.91)), Image.Resampling.LANCZOS)
            scene.alpha_composite(portrait, (w-portrait.width-12, h-portrait.height))
        fade = Image.new('RGBA', (1, h))
        fade.putdata([(16, 24, 31, round(220 * max(0, (y/h-.70)/.30))) for y in range(h)])
        scene = Image.alpha_composite(scene, fade.resize((w, h)))
        self.photo = ImageTk.PhotoImage(scene, master=self)
        self.delete('all')
        self.create_image(0, 0, image=self.photo, anchor='nw')
        x = 28 if w < 750 else 40
        tag, mood, interests, accent = CAST[self.selected]
        self.create_line(x, 39, x+28, 39, fill=accent, width=2)
        self.create_text(x+39, 39, text='M E E T   Y O U R   P R O T A G O N I S T',
                         anchor='w', fill=CREAM, font=('Segoe UI', 8))
        self.create_text(x, h*.24, text=tag, anchor='nw', fill=accent,
                         font=('Segoe UI', 9, 'bold'))
        name = core.PLAYERS[self.selected].replace(' ', '\n', 1)
        self.create_text(x-2, h*.24+33, text=name, anchor='nw', fill=CREAM,
                         font=('Georgia', 34 if w < 750 else 42), justify='left')
        self.create_text(x, h*.24+165, text=mood, anchor='nw', fill=CREAM,
                         font=('Georgia', 12, 'italic'), width=max(150, int(w*.39)))
        self.create_text(x, h-75, text=interests.replace(' · ', '\n'), anchor='sw',
                         fill='#d3dbd8', font=('Segoe UI', 10), justify='left')
        self.create_line(x, h-47, w-x, h-47, fill='#64716f')
        self.create_text(x, h-25, text='WINTERFIELD  /  A LIFE WAITING TO UNFOLD',
                         anchor='w', fill=CREAM, font=('Segoe UI', 8))
        self.create_text(w-x, h-25, text=f'{list(CAST).index(self.selected)+1:02} / {len(CAST):02}',
                         anchor='e', fill=accent, font=('Segoe UI', 9))


class StartScreen(tk.Frame):
    def __init__(self, game):
        super().__init__(game, bg=INK)
        self.game = game
        self.selected = getattr(game, 'menu_character', 'garrett')
        self.pack(fill='both', expand=True)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        rail = tk.Frame(self, bg=INK, width=295)
        rail.grid(row=0, column=0, sticky='nsew', padx=(32, 24), pady=(38, 20))
        rail.grid_propagate(False)
        rail.columnconfigure(0, weight=1)
        rail.rowconfigure(3, weight=1)
        brand = tk.Frame(rail, bg=INK); brand.grid(row=0, column=0, sticky='ew')
        label(brand, 'A   W I N T E R F I E L D   S T O R Y', 8, GOLD, anchor='w').pack(fill='x')
        tk.Label(brand, text='Mysterious\nHearts', bg=INK, fg=CREAM,
                 font=('Georgia', 35), justify='left', anchor='w').pack(fill='x', pady=(20, 14))
        label(brand, 'A town full of lives.\nA story only you can tell.', 11, MUTED,
              justify='left', anchor='w').pack(fill='x')
        tk.Frame(brand, bg=EDGE, height=1).pack(fill='x', pady=(26, 25))
        resume = tk.Frame(rail, bg=INK); resume.grid(row=1, column=0, sticky='ew')
        available = core.SAVE.exists()
        self.continue_button = button(resume, 'Continue your story   →', game.continue_game, primary=True, anchor='w')
        self.continue_button.pack(fill='x')
        if not available: self.continue_button.configure(state='disabled', bg='#26343b', highlightbackground='#26343b')
        summary = 'Your next chapter starts here.'
        if available:
            try:
                saved = json.loads(core.SAVE.read_text(encoding='utf-8'))
                summary = 'Last played as '+saved.get('custom_protagonist', {}).get('name', core.PLAYERS.get(saved.get('player'), 'your protagonist'))
            except (OSError, ValueError, AttributeError): summary = 'Recovery available in your story library.'
        label(resume, summary, 9, MUTED, anchor='w', wraplength=280, justify='left').pack(fill='x', pady=(9, 18))
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
        right.grid(row=0, column=1, sticky='nsew', padx=(0, 30), pady=(38, 20))
        right.columnconfigure(0, weight=1); right.rowconfigure(1, weight=1)
        heading = tk.Frame(right, bg=INK); heading.grid(row=0, column=0, sticky='ew', pady=(0, 16))
        label(heading, 'Begin a new chapter', 18, CREAM, anchor='w').pack(side='left')
        label(heading, 'CHOOSE YOUR PERSPECTIVE', 8, MUTED).pack(side='right')
        self.preview = CharacterPreview(right)
        self.preview.grid(row=1, column=0, sticky='nsew')
        choices = tk.Frame(right, bg=INK); choices.grid(row=2, column=0, sticky='ew', pady=(12, 16))
        paging = tk.Frame(choices, bg=INK); paging.grid(row=0, column=0, columnspan=4, sticky='ew', pady=(0, 6))
        button(paging, '‹ Previous', lambda:self.change_page(-1)).pack(side='left')
        self.page_label = label(paging, '', 9, MUTED); self.page_label.pack(side='left', expand=True)
        button(paging, 'Next ›', lambda:self.change_page(1)).pack(side='right')
        self.page = 0
        self.choices = {}
        for index, key in enumerate(CAST):
            col = index % 4
            choices.columnconfigure(col, weight=1, uniform='cast')
            control = button(choices, core.PLAYERS[key].split()[0], lambda k=key:self.select(k))
            control.configure(padx=4, pady=13)
            control.grid(row=1, column=col, sticky='ew', padx=(0 if col == 0 else 4, 0 if col == 3 else 4))
            # Selection colours remain visible after the pointer leaves.
            control.bind('<Leave>', lambda e,k=key:self.paint_choice(k))
            self.choices[key] = control
        action = tk.Frame(right, bg=INK); action.grid(row=3, column=0, sticky='ew')
        self.begin = button(action, '', lambda:game.start(self.selected), primary=True)
        self.begin.pack(side='right')
        button(action, 'Create your own', lambda: __import__('custom_creator_ui').CharacterCreator(game)).pack(side='left')
        button(action, 'Saved characters', self.saved_characters).pack(side='left', padx=8)
        footer = tk.Frame(self, bg='#0c1319')
        footer.grid(row=1, column=0, columnspan=2, sticky='ew')
        game.status = label(footer, game.model_status, 9, MUTED, anchor='w')
        game.status.pack(side='left', padx=32, pady=13)
        label(footer, 'MYSTERIOUS HEARTS', 8, '#77888f').pack(side='right', padx=30)
        self.bind('<Configure>', self.resize, add='+')
        self.select(self.selected)

    def resize(self, event):
        if event.widget is self:
            self.game.status.configure(wraplength=max(350, self.winfo_width()-260))

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

    def select(self, key):
        self.selected = self.game.menu_character = key
        self.page = list(CAST).index(key) // 4
        for index, (who, control) in enumerate(self.choices.items()):
            if index // 4 == self.page: control.grid()
            else: control.grid_remove()
        self.page_label.configure(text=f'Cast {self.page + 1} / {(len(CAST)+3)//4}')
        for who in self.choices: self.paint_choice(who)
        self.preview.select(key)
        self.begin.configure(text='Begin as '+core.PLAYERS[key].split()[0]+'   →')

    def change_page(self, direction):
        page = (self.page + direction) % ((len(CAST)+3)//4)
        self.select(list(CAST)[page*4])

    def sound_label(self):
        self.sound.configure(text='Sound   ·   '+('On' if self.game.sounds.enabled else 'Off'))

    def toggle_sound(self):
        self.game.sounds.toggle(); self.sound_label()
