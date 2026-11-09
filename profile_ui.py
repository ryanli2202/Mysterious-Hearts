"""The player's directory of met residents, shared history and attributed discoveries."""
import json
import tkinter as tk
from tkinter import ttk
from phone_dialogs import AppWindow, messagebox, simpledialog
from PIL import Image, ImageOps, ImageTk

import game_core as core
import gallery_ui
import social_world as social
from relationship_ui import RelationshipBars
from winterfield_ui import INK, PANEL, CARD, CREAM, MINT, SERIF, transcript


class ProfileWindow(AppWindow):
    def __init__(self, game, who=None):
        super().__init__(game)
        self.game = game
        self.title('Winterfield · Character profiles')
        self.geometry('920x615')
        self.minsize(745, 510)
        self.configure(bg=INK)
        self.who, self.index, self.image_key = None, 0, None
        self.catalog = json.loads((core.ROOT / 'assets/gallery/catalog.json').read_text(encoding='utf-8'))
        body = ttk.Frame(self, padding=14)
        body.pack(fill='both', expand=True, padx=10, pady=10)
        sidebar = ttk.Frame(body)
        sidebar.pack(side='left', fill='y', padx=(0, 16))
        ttk.Label(sidebar, text='Character profiles', font=(SERIF, 17)).pack(anchor='w', pady=(0, 10))
        self.people = tk.Listbox(sidebar, bg=INK, fg=CREAM, width=21, activestyle='none',
            selectbackground='#385565', selectforeground=CREAM, relief='flat', bd=0,
            font=('Segoe UI', 11), highlightthickness=0, exportselection=False)
        scroll = ttk.Scrollbar(sidebar, command=self.people.yview)
        scroll.pack(side='right', fill='y')
        self.people.configure(yscrollcommand=scroll.set)
        self.people.pack(fill='both', expand=True)
        self.people.bind('<<ListboxSelect>>', self.pick)
        detail = ttk.Frame(body)
        detail.pack(side='left', fill='both', expand=True)
        self.name = ttk.Label(detail, style='Title.TLabel')
        self.name.pack(anchor='w')
        self.status = ttk.Label(detail, foreground=MINT)
        self.status.pack(anchor='w', pady=(0, 10))
        top = ttk.Frame(detail)
        top.pack(fill='x')
        art = tk.Frame(top, bg=CARD)
        art.pack(side='left', padx=(0, 15))
        self.picture = tk.Label(art, bg=CARD, bd=0)
        self.picture.pack(fill='both', expand=True)
        nav = ttk.Frame(art)
        nav.pack(fill='x')
        self.back = ttk.Button(nav, text='‹', width=2, command=lambda:self.step(-1))
        self.back.pack(side='left')
        self.next = ttk.Button(nav, text='›', width=2, command=lambda:self.step(1))
        self.next.pack(side='right')
        self.caption = ttk.Label(nav, anchor='center', wraplength=120, style='Muted.TLabel')
        self.caption.pack(fill='x', expand=True)
        bio = ttk.Frame(top)
        bio.pack(side='left', fill='both', expand=True)
        self.values = {}
        for row, field in enumerate(('Birthday', 'Age', 'Height', 'MBTI', 'Sexuality')):
            ttk.Label(bio, text=field, style='Muted.TLabel').grid(row=row, column=0, sticky='w', padx=(0, 14), pady=3)
            self.values[field] = ttk.Label(bio, font=('Segoe UI', 11, 'bold'))
            self.values[field].grid(row=row, column=1, sticky='w')
        self.bars = RelationshipBars(bio, bg=PANEL)
        self.bars.grid(row=5, column=0, columnspan=2, sticky='ew', pady=12)
        bio.columnconfigure(1, weight=1)
        ttk.Label(detail, text='Your notebook', font=(SERIF, 16)).pack(anchor='w', pady=(12, 4))
        notes = ttk.Frame(detail)
        notes.pack(fill='both', expand=True)
        self.notes = transcript(notes, width=1, height=5)
        ns = ttk.Scrollbar(notes, command=self.notes.yview)
        ns.pack(side='right', fill='y')
        self.notes.configure(yscrollcommand=ns.set)
        self.notes.pack(fill='both', expand=True)
        self.refresh(who)

    def display_name(self, who):
        return core.contact_name(self.game.state_data, who) if who in core.CONTACTS else who

    def refresh(self, who=None):
        s = self.game.state_data
        visible = {key for key in s['routes'] if core.hidden.known(s, key)}
        visible.add(s['player'])
        visible.update(s.get('npc_chats', {}))
        visible.update(s.get('profile_notes', {}))
        keys = sorted(visible, key=self.display_name)
        if who not in visible: who = self.who if self.who in visible else s['active']
        names = tuple(self.display_name(key) for key in keys)
        if self.people.get(0, 'end') != names:
            self.people.delete(0, 'end')
            self.people.insert('end', *names)
        self.keys = keys
        if who != self.who: self.index = 0
        self.who = who
        self.people.selection_clear(0, 'end')
        self.people.selection_set(keys.index(who))
        self.people.see(keys.index(who))
        self.name.config(text=self.display_name(who))
        met = who == s['player'] or core.hidden.known(s, who)
        own = who == s['player']
        self.status.config(text='Your profile' if own else social.status_line(s, who) if met else 'Heard about in conversation')
        facts = social.demographics(who)
        for field, label in self.values.items():
            label.configure(text=facts[field] if met else 'Unknown')
        if met and not own:
            self.bars.grid()
            self.bars.update_stats(core.town.character_stats(s, who), romanceable=core.town.romanceable(s, who))
        else: self.bars.grid_remove()
        slug = who.casefold().replace(' ', '-')
        folder = core.ROOT / 'assets/portraits'
        self.variants = []
        if met:
            for path in sorted(folder.glob(slug + '-*.png'), key=lambda p:(p.stem != slug+'-selection', p.name)):
                outfit = path.stem[len(slug)+1:]
                import four_aces, interpol
                if outfit == 'syndicate' and who in four_aces.UNIFORM_IDS and not (four_aces.knows_identities(s, s['player']) or interpol.known_identity(s,s['player'],who)):
                    continue
                self.variants.append(('Portrait' if outfit == 'selection' else outfit.replace('-', ' ').title(), path))
            self.variants += [(entry['title'], core.ROOT / entry['path']) for entry in self.catalog
                              if entry['character'] == who and gallery_ui.unlocked(entry, s)]
        self.index = min(self.index, max(0, len(self.variants)-1))
        self.show_portrait()
        self.notes.config(state='normal')
        self.notes.delete('1.0', 'end')
        def entry(label, text):
            self.notes.insert('end', label+'\n', 'speaker')
            self.notes.insert('end', text+'\n\n')
        if own:
            import contact_profiles
            for title, text in contact_profiles.self_reference(who, s['player']).items():
                entry(title + ' · Private', text)
        import interpol, four_aces
        if who in four_aces.IDS and interpol.known_identity(s,s['player'],who):
            entry('Verified Interpol case finding',four_aces.CAST[who]['name']+' is the Ace of '+four_aces.CAST[who]['suit']+'. Established through the saved case file, not inferred from their public occupation.')
        if who=='crow' and interpol.known_identity(s,s['player'],'crow_location'):
            entry('Verified Interpol case finding','The Crow’s command location was established. His birth identity remains unconfirmed.')
        history = social.initial_notes(s, who)
        if history: entry('Shared history', '\n'.join(history))
        import relationship_dynamics
        dynamics = relationship_dynamics.notebook(s, who)
        if dynamics: entry('Relationship notes', '\n'.join(dynamics))
        familiar = social.familiar_detail(s, who)
        if familiar: entry('Personal details', familiar)
        confessed = s['relationships'].get(who, {}).get('confessed_at')
        if confessed is not None:
            stamp = core.town.loop.dates.story_date(confessed)
            entry(f'{stamp:%b %d}  ·  Confession', self.display_name(who)+' told you about their romantic feelings for you.')
        for note in reversed(s.get('profile_notes', {}).get(who, [])):
            stamp = core.town.loop.dates.story_date(note['minute'])
            entry(f'{self.display_name(note["source"])}  ·  {stamp:%b %d}', '“'+note['quote']+'”')
        for line in social.earlier_exchanges(s, who):
            entry('From your conversations', '“'+line+'”')
        if not self.notes.get('1.0', 'end').strip():
            entry('Personal notes', 'Details shared in conversation will appear here.')
        self.notes.config(state='disabled')

    def pick(self, event=None):
        selected = self.people.curselection()
        if selected and self.keys[selected[0]] != self.who:
            self.refresh(self.keys[selected[0]])

    def step(self, direction):
        if self.variants:
            self.index = (self.index + direction) % len(self.variants)
            self.show_portrait()

    def show_portrait(self):
        title, path = self.variants[self.index] if self.variants else ('Portrait unavailable', None)
        if self.image_key != (self.who, path):
            im = Image.new('RGBA', (174, 172), CARD)
            if path:
                with Image.open(path) as original:
                    image = ImageOps.contain(original.convert('RGBA'), im.size, Image.Resampling.LANCZOS)
                im.alpha_composite(image, ((im.width-image.width)//2, im.height-image.height))
            self.photo = ImageTk.PhotoImage(im, master=self)
            self.picture.configure(image=self.photo)
            self.image_key = self.who, path
        self.caption.configure(text=title)
        for button in (self.back, self.next):
            button.configure(state='normal' if len(self.variants)>1 else 'disabled')
