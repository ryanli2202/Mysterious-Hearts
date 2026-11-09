"""Workspace-owned organisation artwork rendered on dark phone surfaces."""
from functools import lru_cache
from pathlib import Path
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import winterfield_ui as ui

ROOT=Path(__file__).resolve().parent/'assets'/'ui'/'organisations'
KEYS=('dragons','joker','lantern','rail','purple','hamayashi','rojos','waterfront','syndicate','shinokami','custom-crew')
ALIASES={'Red Dragons':'dragons','Black and White Joker network':'joker',
         'Lantern Crew':'lantern','Rail Yard Saints':'rail','Purple Skulls':'purple',
         'Hamayashi-kai':'hamayashi','Los Rojos':'rojos','Waterfront Consortium':'waterfront',
         'Syndicate':'syndicate','Shinokami':'shinokami',
         'Clubs':'syndicate','Hearts':'syndicate','Diamonds':'syndicate','Spades':'syndicate'}


def key(value):
    if isinstance(value,dict): value=value.get('id') or value.get('name','')
    import bubblegram_roles
    if value in {item['key'] for item in bubblegram_roles.ROLES.values()} | {item['name'] for item in bubblegram_roles.ROLES.values()}:
        return 'syndicate'
    return value if value in KEYS else ALIASES.get(value,'custom-crew')


@lru_cache(maxsize=32)
def thumbnail(ident,size=96):
    # Display scaling only; source PNGs, alpha and the supplied designs stay intact.
    name=key(ident)
    path=ROOT/(name+'.png')
    if name=='syndicate' and (ROOT/'syndicate-display.png').is_file():
        path=ROOT/'syndicate-display.png'
    with Image.open(path) as source:
        picture=source.convert('RGBA')
        picture.thumbnail((size,size),Image.Resampling.LANCZOS)
        return picture.copy()


def header(parent,ident,title):
    card=ttk.Frame(parent,padding=(4,8)); card.pack(fill='x',pady=4)
    badge=tk.Label(card,bg=ui.PANEL,bd=0,width=96,height=100)
    try:
        badge.art=ImageTk.PhotoImage(picture(ident),master=parent)
        badge.configure(image=badge.art)
    except (OSError,ValueError):
        # A damaged optional image must not break the entire job app.
        badge.configure(width=7,height=3,text='◇',fg=ui.MINT,font=('Segoe UI',22))
    badge.pack(side='left',padx=(0,10))
    text=ttk.Label(card,text=title,foreground=ui.MINT,justify='left',wraplength=170)
    text.pack(side='left',fill='x',expand=True)
    card.bind('<Configure>',lambda event:text.configure(wraplength=max(90,event.width-122)))
    return card


def picture(ident,size=96):
    if isinstance(ident,dict) and ident.get('role')=='Founder' and not ident.get('id') and not ident.get('established') and ident.get('icon'):
        import gang_icons
        try: return gang_icons.render(ident['icon'],size)
        except ValueError: pass
    return thumbnail(key(ident),size)
