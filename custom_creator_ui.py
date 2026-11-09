"""Dark, nonblocking custom-character form using the existing Codex image jobs."""
import queue
import threading
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageOps, ImageTk
from phone_dialogs import AppWindow
import winterfield_ui as ui
import phone_theme
import vacant_homes
import custom_protagonist as custom


class CharacterCreator(AppWindow):
    def __init__(self, game):
        super().__init__(game)
        self.game = game
        self.title('Create your protagonist')
        self.geometry('1000x800')
        self.minsize(780, 650)
        self.events = queue.Queue()
        self.cancel_event = None
        self.closed = False
        self.portrait = None
        self.generated_signature = None
        self.photo = None
        self.source = None
        self.controls = []
        self.protocol('WM_DELETE_WINDOW', self.destroy)
        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=2)
        self.rowconfigure(1, weight=1)
        heading = ttk.Frame(self, padding=14)
        heading.grid(row=0, column=0, columnspan=2, sticky='ew')
        ttk.Label(heading, text='A new life in Winterfield', style='Title.TLabel').pack(anchor='w')
        ttk.Label(heading, text='Start as an adult newcomer. Meet people while exploring or through Meet-Cute.',
                  wraplength=900).pack(anchor='w', pady=5)
        left = ttk.Frame(self)
        left.grid(row=1, column=0, sticky='nsew', padx=(14, 7))
        scroll = ttk.Scrollbar(left)
        scroll.pack(side='right', fill='y')
        canvas = tk.Canvas(left, bg=ui.PANEL, highlightthickness=0, yscrollcommand=scroll.set)
        canvas.pack(fill='both', expand=True)
        self.form_canvas = canvas
        scroll.configure(command=canvas.yview)
        form = ttk.Frame(canvas, padding=6)
        item = canvas.create_window(0, 0, window=form, anchor='nw')
        def fit_form(event):
            canvas.itemconfigure(item, width=event.width)
            self.home_detail.configure(wraplength=max(180, event.width-20))
            self.appearance_label.configure(wraplength=max(180, event.width-20))
            self.awakening_label.configure(wraplength=max(180, event.width-20))
            self.awakening_hint.configure(wraplength=max(180, event.width-20))
        canvas.bind('<Configure>', fit_form)
        form.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        form.columnconfigure(1, weight=1)
        defaults = dict(name='', gender='Woman', age='25', height='170', sexuality='Bisexual',
                        hairstyle='Medium length', mbti='INFP', occupation='', interests='',
                        home=next(iter(vacant_homes.HOMES)))
        self.values = {key: tk.StringVar(value=value) for key, value in defaults.items()}
        self.home_labels = {data['name']: key for key, data in vacant_homes.HOMES.items()}
        self.home_choice = tk.StringVar(value=next(iter(self.home_labels)))
        fields = [('name', 'Name', None), ('gender', 'Gender', custom.GENDERS), ('age', 'Age · 18–100', None),
                  ('height', 'Height · cm', None), ('sexuality', 'Sexuality', custom.SEXUALITIES),
                  ('hairstyle', 'Hairstyle', custom.HAIRSTYLES), ('mbti', 'MBTI', custom.MBTI),
                  ('occupation', 'Occupation', None), ('interests', 'Interests · use commas', None)]
        for row, (key, title, options) in enumerate(fields):
            ttk.Label(form, text=title).grid(row=row, column=0, sticky='w', padx=(0, 10), pady=6)
            control = (ttk.Combobox(form, textvariable=self.values[key], values=options, state='readonly')
                       if options else ttk.Entry(form, textvariable=self.values[key]))
            control.grid(row=row, column=1, sticky='ew', pady=6)
            self.controls.append((control, 'readonly' if options else 'normal'))
        ttk.Label(form, text='Home').grid(row=9, column=0, sticky='w', pady=6)
        self.home_picker = ttk.Combobox(form, textvariable=self.home_choice, values=list(self.home_labels), state='readonly')
        self.home_picker.grid(row=9, column=1, sticky='ew', pady=6)
        self.controls.append((self.home_picker, 'readonly'))
        self.home_detail = ttk.Label(form, wraplength=460, style='Muted.TLabel')
        self.home_detail.grid(row=10, column=0, columnspan=2, sticky='ew', pady=6)
        self.home_choice.trace_add('write', self.update_home)
        self.update_home()
        self.appearance_label = ttk.Label(form, text='Appearance · hair colour, eyes, build, clothing and other details')
        self.appearance_label.grid(row=11, column=0, columnspan=2, sticky='w', pady=(12, 5))
        self.appearance = tk.Text(form, height=6, wrap='word', bg=ui.CARD, fg=ui.CREAM,
                                  insertbackground=ui.CREAM, relief='flat', font=('Segoe UI', 10))
        self.appearance.grid(row=12, column=0, columnspan=2, sticky='ew')
        self.controls.append((self.appearance, 'normal'))
        self.awakened = tk.BooleanVar(value=False)
        self.awakening_toggle = ttk.Checkbutton(form, text='Awakened · start with your own Trait',
                                                variable=self.awakened, command=self.update_awakening)
        self.awakening_toggle.grid(row=13, column=0, columnspan=2, sticky='w', pady=(16, 6))
        self.controls.append((self.awakening_toggle, 'normal'))
        self.values['awakening_trait'] = tk.StringVar()
        ttk.Label(form, text='Awakening Trait · name').grid(row=14, column=0, sticky='w', pady=6)
        self.awakening_trait = ttk.Entry(form, textvariable=self.values['awakening_trait'])
        self.awakening_trait.grid(row=14, column=1, sticky='ew', pady=6)
        self.awakening_label = ttk.Label(form, text='Description · powers, effects and limits (up to 1,800 characters)', wraplength=420)
        self.awakening_label.grid(row=15, column=0, columnspan=2, sticky='w', pady=6)
        self.awakening_description = tk.Text(form, height=5, wrap='word', bg=ui.CARD, fg=ui.CREAM,
                                             insertbackground=ui.CREAM, relief='flat', font=('Segoe UI', 10))
        self.awakening_description.grid(row=16, column=0, columnspan=2, sticky='ew')
        self.awakening_hint = ttk.Label(form, text='Awakened characters start on the Path at Awakening with this Trait. Unawakened characters begin in Dormancy and may awaken through strenuous combat.',
                                       style='Muted.TLabel', wraplength=420)
        self.awakening_hint.grid(row=17, column=0, columnspan=2, sticky='w', pady=6)
        self.controls.extend(((self.awakening_trait, 'normal'), (self.awakening_description, 'normal')))
        self.update_awakening()
        self.appearance.bind('<<Modified>>', self.changed)
        for key in ('gender', 'age', 'height', 'hairstyle'):
            self.values[key].trace_add('write', self.changed)
        right = ttk.Frame(self, padding=(7, 0, 14, 0))
        right.grid(row=1, column=1, sticky='nsew')
        ttk.Label(right, text='Your transparent portrait', style='Section.TLabel').pack(anchor='w', pady=6)
        self.canvas = tk.Canvas(right, bg=ui.INK, highlightthickness=0)
        self.canvas.pack(fill='both', expand=True)
        self.canvas.bind('<Configure>', self.redraw)
        ttk.Label(right, text='Generated from gender, age, height, hairstyle and your appearance description. '
                  'Uses your existing Codex ChatGPT login and plan allowance.', wraplength=330,
                  style='Muted.TLabel').pack(anchor='w', pady=10)
        bottom = ttk.Frame(self, padding=14)
        bottom.grid(row=2, column=0, columnspan=2, sticky='ew')
        self.status = ttk.Label(bottom, text='Complete your details, then generate a portrait.', wraplength=900)
        self.status.pack(anchor='w', pady=(0, 8))
        actions = ttk.Frame(bottom); actions.pack(fill='x')
        self.generate_button = ttk.Button(actions, text='Generate portrait with Codex', command=self.generate)
        self.generate_button.pack(side='left')
        self.cancel_button = ttk.Button(actions, text='Cancel generation', command=self.cancel, state='disabled')
        self.cancel_button.pack(side='left', padx=8)
        self.begin_button = ttk.Button(actions, text='Move to Winterfield', command=self.begin, state='disabled')
        self.begin_button.pack(side='right')
        phone_theme.apply_tree(self)
        self.poll_id = self.after(100, self.poll)

    def update_home(self, *_):
        key = self.home_labels[self.home_choice.get()]
        self.values['home'].set(key)
        self.home_detail.configure(text=vacant_homes.HOMES[key]['description'])

    def collect(self):
        return custom.validate({key: value.get() for key, value in self.values.items()} |
                               {'appearance': self.appearance.get('1.0', 'end').strip(),
                                'awakened': self.awakened.get(),
                                'awakening_description': self.awakening_description.get('1.0', 'end').strip()})

    def update_awakening(self):
        state = 'normal' if self.awakened.get() and not self.cancel_event else 'disabled'
        self.awakening_trait.configure(state=state)
        self.awakening_description.configure(state=state)

    def signature(self):
        return tuple(self.values[key].get() for key in ('gender', 'age', 'height', 'hairstyle')) + (self.appearance.get('1.0', 'end').strip(),)

    def changed(self, *_):
        if hasattr(self, 'begin_button'):
            self.begin_button.configure(state='normal' if self.portrait and not self.cancel_event and self.signature() == self.generated_signature else 'disabled')
        if self.appearance.edit_modified():
            self.appearance.edit_modified(False)

    def generate(self):
        if self.cancel_event:
            return
        try:
            values = self.collect()
        except ValueError as exc:
            self.status.configure(text=str(exc)); return
        signature = self.signature()
        self.cancel_event = threading.Event()
        self.generate_button.configure(state='disabled')
        self.begin_button.configure(state='disabled')
        self.cancel_button.configure(state='normal')
        for widget, _ in self.controls:
            widget.configure(state='disabled')
        cancel = self.cancel_event
        def work():
            try:
                path = custom.generate_portrait(values, cancel, lambda text: self.events.put(('progress', text)))
                self.events.put(('complete', (path, signature)))
            except Exception as exc:
                self.events.put(('error', str(exc)))
        threading.Thread(target=work, daemon=True).start()

    def cancel(self):
        if self.cancel_event:
            self.cancel_event.set()
            self.status.configure(text='Cancelling portrait generation…')

    def poll(self):
        if self.closed:
            return
        while not self.events.empty():
            kind, value = self.events.get_nowait()
            if kind == 'progress':
                self.status.configure(text=value); continue
            cancelled = self.cancel_event and self.cancel_event.is_set()
            self.cancel_event = None
            for widget, state in self.controls:
                widget.configure(state=state)
            self.update_awakening()
            self.generate_button.configure(state='normal')
            self.cancel_button.configure(state='disabled')
            if kind == 'complete' and not cancelled:
                try:
                    self.portrait, self.generated_signature = value
                    with Image.open(custom.ROOT / self.portrait) as source:
                        self.source = source.convert('RGBA')
                    self.redraw()
                    self.status.configure(text='Portrait ready. Review your character, then move to Winterfield.')
                except (OSError, ValueError) as exc:
                    self.portrait = None
                    self.status.configure(text=str(exc))
            else:
                self.status.configure(text='Generation cancelled.' if cancelled else value)
            self.changed()
        self.poll_id = self.after(100, self.poll)

    def redraw(self, event=None):
        if self.source is None:
            return
        width, height = max(1, self.canvas.winfo_width()), max(1, self.canvas.winfo_height())
        fitted = ImageOps.contain(self.source, (width, height), Image.Resampling.LANCZOS)
        self.photo = ImageTk.PhotoImage(fitted, master=self)
        self.canvas.delete('all')
        self.canvas.create_image(width/2, height/2, image=self.photo)

    def begin(self):
        if self.cancel_event or not self.portrait or self.signature() != self.generated_signature:
            self.status.configure(text='Generate a portrait matching your current appearance first.'); return
        try:
            self.game.start_custom(self.collect(), self.portrait)
        except (OSError, ValueError) as exc:
            self.status.configure(text=str(exc)); return
        self.destroy()

    def destroy(self):
        self.closed = True
        if self.cancel_event:
            self.cancel_event.set()
        if getattr(self, 'poll_id', None):
            self.after_cancel(self.poll_id)
            self.poll_id = None
        super().destroy()
