"""Shared dark mobile presentation primitives; no game state or network access."""
import tkinter as tk
from phone_controls import PhoneButton

BG = '#17171b'
PANEL = '#202a38'
TEXT = '#dce4ed'
MUTED = '#9aadc2'
ACCENTS = {'Mixtape': '#66d998', 'Wardrobe': '#e4a6c5', 'Out & About': '#f2b476',
           'Pocket Wallet': '#79b9fa', 'Postcards': '#7ebfff', 'Campus Portal': '#b4a4ed',
           'Supafast': '#f3b75f', 'Doober Eats': '#75dc9b', 'Mini Games': '#bb9afa',
           'Gallery': '#94baff', 'Winterfield Exchange': '#dec57f', 'Recipe Box': '#efa380'}


def text(parent, value, size=11, color=TEXT, bold=False):
    label = tk.Label(parent, text=value, bg=parent.cget('background'), fg=color,
                     font=('Segoe UI', size, 'bold' if bold else 'normal'), anchor='w', justify='left')
    label.pack(fill='x', pady=3)
    label.bind('<Configure>', lambda e: label.configure(wraplength=max(80, e.width-8)))
    return label


def hero(parent, app, eyebrow, title, subtitle=''):
    tones = {'Mixtape': '#19362c', 'Pocket Wallet': '#203653', 'Campus Portal': '#2c2948',
             'Doober Eats': '#1c3028', 'Supafast': '#303044', 'Wardrobe': '#352b3b'}
    panel = tk.Frame(parent, bg=tones.get(app, PANEL), padx=16, pady=13)
    panel.pack(fill='x', pady=(0, 12))
    text(panel, eyebrow.upper(), 9, ACCENTS.get(app, '#94baff'), True)
    text(panel, title, 25, TEXT, True)
    if subtitle: text(panel, subtitle, 10, MUTED)
    return panel


def card(parent, title, subtitle='', accent='#94baff', symbol=None):
    panel = tk.Frame(parent, bg=PANEL, padx=12, pady=10,
                     highlightthickness=1, highlightbackground='#344155')
    panel.pack(fill='x', pady=5)
    if symbol: text(panel, symbol, 23, accent, True)
    text(panel, title, 14, TEXT, True)
    if subtitle: text(panel, subtitle, 10, MUTED)
    return panel


def navigation(parent, links):
    bar = tk.Frame(parent, bg=BG, pady=5)
    bar.pack(side='bottom', fill='x')
    for title, callback in links:
        PhoneButton(bar, text=title, command=callback).pack(side='left', fill='x', expand=True, padx=2)
    return bar


def album_art(parent, index=0):
    """Small original cover artwork, rendered locally at device resolution."""
    cover = tk.Canvas(parent, width=96, height=96, bg='#23483e', highlightthickness=0)
    cover.pack(anchor='w', pady=(0, 8), before=parent.winfo_children()[0])
    for row in range(8):
        y = 10 + row * 10
        cover.create_line(8, y, 30, y+6, 62, y-5, 88, y+2,
                          fill=('#68c8a0', '#a3d5bd', '#438779')[(row+index)%3], width=3, smooth=True)
    return cover
