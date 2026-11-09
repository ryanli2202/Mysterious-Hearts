"""Meet-Cute's scoped visual language and single scrolling surface."""
import tkinter as tk
from tkinter import ttk

BG = '#201b24'
CARD = '#302735'
INK = '#f4eaf1'
MUTED = '#bcaabd'
ACCENT = '#d7a7cc'


def install(parent):
    style = ttk.Style(parent)
    for name, color in (('Base', BG), ('Card', CARD)):
        style.configure(f'PhoneDark.Meet.{name}.TFrame', background=color)
        for kind, font, ink in (('Body', ('Segoe UI', 11), INK),
                                ('Muted', ('Segoe UI', 9), MUTED),
                                ('Title', ('Georgia', 23, 'bold'), INK),
                                ('Answer', ('Georgia', 17), INK),
                                ('Heading', ('Segoe UI', 12, 'bold'), INK)):
            style.configure(f'PhoneDark.Meet.{name}.{kind}.TLabel',
                            background=color, foreground=ink, font=font)
    style.configure('PhoneDark.Meet.TButton', background=CARD, foreground=INK,
                    padding=(10, 9), font=('Segoe UI', 10, 'bold'), borderwidth=0)
    style.map('PhoneDark.Meet.TButton', background=[('active', '#49384b'), ('pressed', '#59415a')])
    style.configure('PhoneDark.Meet.Primary.TButton', background='#694663', foreground=INK,
                    padding=(12, 11), font=('Segoe UI', 10, 'bold'), borderwidth=0)
    style.map('PhoneDark.Meet.Primary.TButton', background=[('active', '#825878')])


def label(parent, text, kind='Body', card=False):
    widget = ttk.Label(parent, text=text, style=f'PhoneDark.Meet.{"Card" if card else "Base"}.{kind}.TLabel',
                       wraplength=300, justify='left')
    widget.pack(fill='x', pady=(4, 7))
    return widget


def button(parent, text, command, primary=False):
    return ttk.Button(parent, text=text, command=command,
                      style='PhoneDark.Meet.'+('Primary.' if primary else '')+'TButton')


class Scroll(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, style='PhoneDark.Meet.Base.TFrame')
        self.canvas = tk.Canvas(self, bg=BG, width=1, height=1, highlightthickness=0, yscrollincrement=18)
        bar = ttk.Scrollbar(self, command=self.canvas.yview)
        bar.pack(side='right', fill='y')
        self.canvas.pack(fill='both', expand=True)
        self.canvas.configure(yscrollcommand=bar.set)
        self.body = ttk.Frame(self.canvas, style='PhoneDark.Meet.Base.TFrame')
        self.item = self.canvas.create_window(0, 0, window=self.body, anchor='nw')
        self.body.bind('<Configure>', lambda e:self.canvas.configure(scrollregion=self.canvas.bbox('all')))
        self.canvas.bind('<Configure>', lambda e:self.canvas.itemconfigure(self.item, width=e.width))
        self.tag = 'MeetScroll'+str(id(self))
        self.canvas.bind_class(self.tag, '<MouseWheel>', self.wheel)
        self.bind('<Destroy>', self.cleanup)
        self.remainder = 0

    def connect(self, widget=None):
        widget = widget or self.body
        if self.tag not in widget.bindtags():
            widget.bindtags((self.tag, *widget.bindtags()))
        for child in widget.winfo_children(): self.connect(child)

    def wheel(self, event):
        # Consume the event before Text/Combobox class bindings and the phone handler.
        self.remainder += -event.delta / 120 * 3
        units = int(self.remainder)
        self.remainder -= units
        if units: self.canvas.yview_scroll(units, 'units')
        return 'break'

    def cleanup(self, event):
        if event.widget is self:
            self.canvas.unbind_class(self.tag, '<MouseWheel>')
