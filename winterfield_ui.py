"""Shared palette and typography for Winterfield's native windows."""
import tkinter as tk
from tkinter import ttk
from functools import lru_cache
from PIL import Image, ImageDraw, ImageTk

INK, PANEL, CARD, EDGE = '#131823', '#1c2433', '#293447', '#3b4a60'
CREAM, MUTED, GOLD, MINT = '#f5eedf', '#b2c1cd', '#edc786', '#99d9c6'
SERIF = 'Georgia'


@lru_cache(maxsize=16)
def surface_texture(width, height, color=INK):
    """Quiet woven slate, generated locally; no random flicker on redraw."""
    art = Image.new('RGB', (max(1, width), max(1, height)), color)
    r, g, b = art.getpixel((0, 0))
    draw = ImageDraw.Draw(art)
    lighter = tuple(min(255, v + 4) for v in (r, g, b))
    darker = tuple(max(0, v - 3) for v in (r, g, b))
    for y in range(0, height, 4):
        draw.line((0, y, width, y), fill=darker)
    for x in range(0, width, 6):
        draw.line((x, 0, x, height), fill=lighter)
    return art


class TextureFrame(tk.Frame):
    """A normal layout container with a non-interactive woven backing."""
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self._backing = tk.Label(self, bd=0, highlightthickness=0, takefocus=0)
        self._backing.place(x=0, y=0, relwidth=1, relheight=1)
        self._backing.lower()
        self.bind('<Configure>', self._texture, add='+')

    def _texture(self, event):
        if event.widget is not self:
            return
        self._texture_photo = ImageTk.PhotoImage(
            surface_texture(event.width, event.height, self.cget('bg')), master=self)
        self._backing.configure(image=self._texture_photo)


def install(root):
    root.configure(background=INK)
    root.tk_setPalette(background=PANEL, foreground=CREAM, activeBackground=CARD,
                       activeForeground=CREAM, selectBackground=EDGE, selectForeground=CREAM,
                       highlightBackground=PANEL, highlightColor=MINT, insertBackground=CREAM)
    style = ttk.Style(root)
    style.theme_use('clam')
    style.configure('.', background=PANEL, foreground=CREAM, fieldbackground=CARD,
                    bordercolor=EDGE, lightcolor=PANEL, darkcolor=PANEL, font=('Segoe UI', 10))
    style.configure('TButton', background=CARD, padding=(9, 5), relief='flat', borderwidth=0)
    for name in ('TFrame', 'TLabel', 'TLabelframe', 'TLabelframe.Label'):
        style.configure(name, background=PANEL, foreground=CREAM)
    style.configure('TCombobox', fieldbackground=CARD, background=CARD, foreground=CREAM,
                    arrowcolor=CREAM)
    style.map('TButton', background=[('pressed', '#405469'), ('active', '#35485c')],
              foreground=[('disabled', '#8494a4')])
    style.configure('Accent.TButton', background=GOLD, foreground=INK, font=('Segoe UI', 10, 'bold'))
    style.map('Accent.TButton', background=[('active', '#ffdca3')], foreground=[('active', INK)])
    style.configure('Title.TLabel', font=(SERIF, 23), foreground=CREAM)
    style.configure('Section.TLabel', font=('Segoe UI', 10, 'bold'), foreground=GOLD)
    style.configure('Muted.TLabel', foreground=MUTED)
    style.configure('Scene.TButton', padding=(10, 7), background=CARD)
    style.configure('SceneAccent.TButton', padding=(10, 7), background='#304b4c',
                    foreground=MINT, font=('Segoe UI', 10, 'bold'))
    style.map('SceneAccent.TButton', background=[('pressed', '#365e5b'), ('active', '#3a5558')],
              foreground=[('disabled', MUTED)])
    style.configure('TNotebook', background=INK, borderwidth=0, tabmargins=(0, 0, 0, 5))
    style.configure('TNotebook.Tab', background=INK, foreground=MUTED, padding=(9, 7))
    style.map('TNotebook.Tab', background=[('selected', CARD)], foreground=[('selected', GOLD)])
    style.configure('Treeview', background=PANEL, fieldbackground=PANEL, rowheight=28)
    style.configure('Treeview.Heading', background=CARD, foreground=GOLD)
    style.map('Treeview', background=[('selected', '#3e5564')], foreground=[('selected', CREAM)])
    for name in ('TCombobox', 'TEntry', 'TSpinbox'):
        style.configure(name, fieldbackground=CARD, background=CARD, foreground=CREAM,
                        insertcolor=CREAM, selectbackground=EDGE, selectforeground=CREAM,
                        arrowcolor=MUTED, bordercolor=EDGE, lightcolor=EDGE, darkcolor=EDGE)
        style.map(name, fieldbackground=[('disabled', PANEL), ('readonly', CARD), ('focus', CARD)],
                  background=[('active', EDGE), ('disabled', PANEL)],
                  foreground=[('disabled', MUTED), ('readonly', CREAM)],
                  selectbackground=[('!disabled', EDGE)], selectforeground=[('!disabled', CREAM)])
    style.configure('TEntry', fieldbackground=CARD, foreground=CREAM, insertcolor=CREAM)
    style.map('TEntry', fieldbackground=[('disabled', PANEL), ('readonly', CARD)])
    style.configure('TScrollbar', background=CARD, troughcolor=INK, arrowcolor=MUTED,
                    bordercolor=INK, lightcolor=CARD, darkcolor=CARD)
    style.map('TScrollbar', background=[('active', EDGE), ('pressed', EDGE)])
    for name in ('TCheckbutton', 'TRadiobutton'):
        style.configure(name, background=PANEL, foreground=CREAM, indicatorbackground=CARD,
                        indicatorforeground=CREAM, upperbordercolor=EDGE, lowerbordercolor=EDGE,
                        lightcolor=EDGE, darkcolor=EDGE)
        style.map(name, background=[('active', PANEL)], foreground=[('disabled', MUTED)],
                  indicatorbackground=[('disabled', PANEL), ('pressed', EDGE), ('selected', '#356757'), ('!selected', CARD)])
    style.configure('TMenubutton', background=CARD, foreground=CREAM, arrowcolor=MUTED)
    style.map('TMenubutton', background=[('active', EDGE), ('pressed', EDGE)])
    style.configure('TSeparator', background=EDGE)
    for orient in ('Horizontal', 'Vertical'):
        style.configure(orient+'.TProgressbar', background='#356757', troughcolor=INK,
                        bordercolor=EDGE, lightcolor='#356757', darkcolor='#356757')
        style.configure(orient+'.TScale', background=CARD, troughcolor=INK, bordercolor=EDGE)
    # Classic Tk widgets do not inherit ttk's palette. Cover empty scroll areas,
    # popup forms and native scrollbars as well as their focused/active states.
    for widget in ('Toplevel', 'Canvas', 'Frame', 'Label', 'Checkbutton', 'Radiobutton'):
        root.option_add(f'*{widget}.Background', PANEL)
        root.option_add(f'*{widget}.highlightBackground', PANEL)
    for widget in ('Entry', 'Listbox', 'Spinbox'):
        root.option_add(f'*{widget}.Background', CARD)
        root.option_add(f'*{widget}.Foreground', CREAM)
        root.option_add(f'*{widget}.selectBackground', EDGE)
        root.option_add(f'*{widget}.selectForeground', CREAM)
        root.option_add(f'*{widget}.insertBackground', CREAM)
        root.option_add(f'*{widget}.disabledBackground', PANEL)
    for widget in ('Checkbutton', 'Radiobutton'):
        root.option_add(f'*{widget}.Foreground', CREAM)
        root.option_add(f'*{widget}.activeBackground', CARD)
        root.option_add(f'*{widget}.activeForeground', CREAM)
        root.option_add(f'*{widget}.selectColor', CARD)
    for widget in ('Button', 'Menubutton', 'Menu', 'Scale'):
        for option,value in {'Background':CARD, 'Foreground':CREAM, 'activeBackground':EDGE,
                             'activeForeground':CREAM, 'disabledForeground':MUTED,
                             'highlightBackground':PANEL}.items():
            root.option_add(f'*{widget}.{option}',value)
    root.option_add('*Scale.troughColor',INK)
    root.option_add('*Scrollbar.Background', CARD)
    root.option_add('*Scrollbar.troughColor', INK)
    root.option_add('*Scrollbar.activeBackground', EDGE)
    root.option_add('*TCombobox*Listbox.background', CARD)
    root.option_add('*TCombobox*Listbox.foreground', CREAM)
    root.option_add('*TCombobox*Listbox.selectBackground', EDGE)
    root.option_add('*TCombobox*Listbox.selectForeground', CREAM)
    root.option_add('*Text.Background', INK)
    root.option_add('*Text.Foreground', CREAM)
    root.option_add('*Text.insertBackground', CREAM)
    root.option_add('*Text.selectBackground', EDGE)
    root.option_add('*Text.selectForeground', CREAM)
    root.option_add('*Text.relief', 'flat')
    root.option_add('*Text.highlightThickness', 0)


def transcript(parent, **kw):
    box = tk.Text(parent, wrap='word', bg=INK, fg=CREAM, padx=16, pady=12,
                  spacing3=4, font=('Segoe UI', 11), relief='flat', **kw)
    box.tag_configure('speaker', foreground=GOLD, font=('Segoe UI', 10, 'bold'), spacing1=8)
    box.tag_configure('player', foreground=MINT, font=('Segoe UI', 10, 'bold'), spacing1=8)
    box.tag_configure('aside', foreground=MUTED, font=(SERIF, 11, 'italic'))
    return box
