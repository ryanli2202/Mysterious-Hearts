"""Local presentation components for every in-person combat surface."""
import tkinter as tk
import winterfield_ui as ui

class Panel(ui.TextureFrame):
    """Woven slate edging leaves the centre clear for readable controls."""
    def __init__(self, parent, **kw):
        kw.setdefault('bg', ui.PANEL)
        kw.setdefault('highlightbackground', ui.EDGE)
        kw.setdefault('highlightthickness', 1)
        super().__init__(parent, **kw)


def heading(parent, text):
    label = tk.Label(parent, text=text, bg=ui.PANEL, fg=ui.GOLD,
                     font=('Segoe UI', 10, 'bold'), anchor='w', padx=10, pady=6)
    label.pack(fill='x', pady=(3, 5))
    return label


def stats(parent, profile):
    rail = Panel(parent, padx=6, pady=6)
    rail.pack(fill='x', pady=(2, 6))
    for col, (key, value) in enumerate(profile['stats'].items()):
        rail.columnconfigure(col, weight=1, uniform='stats')
        card = tk.Frame(rail, bg=ui.CARD, padx=6, pady=4)
        card.grid(row=0, column=col, sticky='nsew', padx=3)
        tk.Label(card, text=key.replace('_', ' ').title(), bg=ui.CARD,
                 fg=ui.MUTED, font=('Segoe UI', 9), wraplength=115).pack()
        tk.Label(card, text=str(value), bg=ui.CARD, fg=ui.MINT,
                 font=('Georgia', 20, 'bold')).pack()
    return rail


def scrolling_body(parent):
    """Keep long hub profiles and Iron Circle controls reachable at any height."""
    from tkinter import ttk
    canvas = tk.Canvas(parent, bg=ui.INK, highlightthickness=0)
    scroll = ttk.Scrollbar(parent, command=canvas.yview)
    scroll.pack(side='right', fill='y')
    canvas.pack(fill='both', expand=True)
    canvas.configure(yscrollcommand=scroll.set)
    body = tk.Frame(canvas, bg=ui.INK)
    item = canvas.create_window(0, 0, window=body, anchor='nw')
    def resize(event=None):
        canvas.itemconfigure(item, width=max(1, canvas.winfo_width()),
                             height=max(body.winfo_reqheight(), canvas.winfo_height()))
        canvas.configure(scrollregion=canvas.bbox('all'))
    canvas.bind('<Configure>', resize)
    body.bind('<Configure>', resize)
    def wheel(event):
        canvas.yview_scroll(-int(event.delta / 120), 'units')
        return 'break'
    def bind_wheel():
        def visit(widget):
            # Listboxes and text retain their own local scrolling.
            if widget.winfo_class() not in ('Listbox', 'Text'):
                widget.bind('<MouseWheel>', wheel, add='+')
            for child in widget.winfo_children(): visit(child)
        visit(body)
    body.after_idle(bind_wheel)
    return body
