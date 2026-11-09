"""Embedded dark phone icon editor with an unsaved live preview."""
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk
import gang_icons as icons
import custom_gangs
import winterfield_ui as ui


def draw(board, state):
    board.label('Gang icon creator',True)
    try: gang=custom_gangs.crew(state)
    except ValueError as exc:
        board.label(str(exc)); return
    board.label('Choose a badge, symbol and colours. Preview changes are saved only when you select Use this icon. Your icon travels with this story save.')
    draft=icons.saved(gang)
    preview=tk.Label(board.body,bg=ui.PANEL,bd=0); preview.pack(pady=8)
    vars={key:tk.StringVar(master=board.body,value=value) for key,value in draft.items()}
    status=ttk.Label(board.body,text='',wraplength=270); status.pack(fill='x')
    for key,choices in (('shape',icons.SHAPES),('symbol',icons.SYMBOLS),('background',tuple(icons.BACKGROUNDS)),('accent',tuple(icons.ACCENTS))):
        board.label(key.title())
        ttk.Combobox(board.body,textvariable=vars[key],values=choices,state='readonly').pack(fill='x',pady=3)
    board.label('Initials · 1–3 letters or numbers')
    ttk.Entry(board.body,textvariable=vars['initials']).pack(fill='x',pady=3)
    def current(): return {key:var.get() for key,var in vars.items()}
    def update(*_):
        try: picture=icons.render(current(),176)
        except ValueError as exc:
            status.configure(text=str(exc)); use.configure(state='disabled'); return
        preview.art=ImageTk.PhotoImage(picture,master=board.body); preview.configure(image=preview.art)
        status.configure(text='Saved icon' if icons.validate(current())==gang.get('icon') else 'Preview · unsaved')
        use.configure(state='disabled' if board.game.busy else 'normal')
    use=ttk.Button(board.body,text='Use this icon',command=lambda:board.act(icons.apply,current())); use.pack(fill='x',pady=8)
    board.button('Restore default gang icon',icons.reset)
    ttk.Button(board.body,text='Back to My gang',command=lambda:board.change('My gang')).pack(fill='x',pady=3)
    for var in vars.values(): var.trace_add('write',update)
    board.icon_editor=dict(variables=vars,preview=preview,status=status,save=use)
    update()
