"""Local outfit gallery with character filtering and full-resolution inspection."""
import json
from pathlib import Path
import tkinter as tk
from tkinter import ttk
from phone_dialogs import AppWindow, messagebox, simpledialog
from PIL import Image, ImageOps, ImageTk

ROOT = Path(__file__).resolve().parent
BG, PANEL, TEXT, GOLD = '#10121c', '#191c2b', '#f3eee7', '#dfba78'


def unlocked(entry, state):
    if entry.get('outfit') != 'bedroom':
        return True
    return (state or {}).get('relationships', {}).get(entry['character'], {}).get('status') == 'official'


class GalleryWindow(AppWindow):
    def __init__(self, parent, state_provider=None):
        super().__init__(parent)
        self.state_provider = state_provider or (lambda: getattr(parent, 'state_data', None))
        self.access_job = None
        self.title('Mysterious Hearts · Gallery')
        self.geometry('1050x800')
        self.minsize(760, 560)
        self.configure(bg=BG)
        self.entries = json.loads((ROOT / 'assets/gallery/catalog.json').read_text(encoding='utf-8'))
        self.current = None
        self.source = None
        self.photo = None
        self.zoom = False
        self.resize_job = None
        top = tk.Frame(self, bg=BG)
        top.pack(fill='x', padx=18, pady=12)
        tk.Label(top, text='PORTRAIT GALLERY', bg=BG, fg=GOLD, font=('Segoe UI', 18)).pack(side='left')
        self.filter = ttk.Combobox(top, state='readonly', values=['All characters'] + sorted({e['character'].title() for e in self.entries}), width=18)
        self.filter.current(0)
        self.filter.pack(side='right')
        self.filter.bind('<<ComboboxSelected>>', self.filter_entries)
        body = tk.Frame(self, bg=BG)
        body.pack(fill='both', expand=True, padx=18)
        sidebar = tk.Frame(body, bg=PANEL)
        sidebar.pack(side='left', fill='y', padx=(0, 14))
        scroll = ttk.Scrollbar(sidebar)
        scroll.pack(side='right', fill='y')
        self.listbox = tk.Listbox(sidebar, bg=PANEL, fg=TEXT, selectbackground='#675337', selectforeground=TEXT, font=('Segoe UI', 11), width=28, relief='flat', exportselection=False, yscrollcommand=scroll.set)
        self.listbox.pack(fill='both', expand=True)
        scroll.configure(command=self.listbox.yview)
        self.listbox.bind('<<ListboxSelect>>', self.select)
        viewer = tk.Frame(body, bg=BG)
        viewer.pack(side='left', fill='both', expand=True)
        viewer.rowconfigure(0, weight=1)
        viewer.columnconfigure(0, weight=1)
        self.canvas = tk.Canvas(viewer, bg=PANEL, highlightthickness=0)
        self.canvas.grid(row=0, column=0, sticky='nsew')
        vertical = ttk.Scrollbar(viewer, orient='vertical', command=self.canvas.yview)
        vertical.grid(row=0, column=1, sticky='ns')
        horizontal = ttk.Scrollbar(viewer, orient='horizontal', command=self.canvas.xview)
        horizontal.grid(row=1, column=0, sticky='ew')
        self.canvas.configure(xscrollcommand=horizontal.set, yscrollcommand=vertical.set)
        self.image_item = self.canvas.create_image(0, 0, anchor='nw')
        self.lock_item = self.canvas.create_text(0, 0, text='', fill=GOLD, font=('Segoe UI', 14), justify='center')
        self.canvas.bind('<Configure>', self.schedule_redraw)
        self.canvas.bind('<ButtonPress-1>', lambda e: self.canvas.scan_mark(e.x, e.y))
        self.canvas.bind('<B1-Motion>', lambda e: self.canvas.scan_dragto(e.x, e.y, gain=1))
        footer = tk.Frame(self, bg=BG)
        footer.pack(fill='x', padx=18, pady=12)
        self.caption = tk.Label(footer, bg=BG, fg=TEXT, font=('Segoe UI', 11), anchor='w')
        self.caption.pack(fill='x', pady=(0, 8))
        ttk.Button(footer, text='Previous', command=lambda: self.step(-1)).pack(side='left')
        ttk.Button(footer, text='Next', command=lambda: self.step(1)).pack(side='left', padx=8)
        ttk.Button(footer, text='Image studio · Generate', command=self.open_studio).pack(side='left', padx=8)
        self.zoom_button = ttk.Button(footer, text='Inspect at 100%', command=self.toggle_zoom)
        self.zoom_button.pack(side='right')
        self.bind('<Escape>', lambda e: self.destroy())
        self.protocol('WM_DELETE_WINDOW', self.destroy)
        self.filter_entries()
        self.access_signature = self.permissions()
        self.access_job = self.after(250, self.refresh_access)

    def open_studio(self):
        from image_studio_ui import ImageStudio
        ImageStudio(self)

    def permissions(self):
        state = self.state_provider()
        return tuple(unlocked(entry, state) for entry in self.entries)

    def refresh_access(self):
        if self.access_job:
            self.after_cancel(self.access_job)
            self.access_job = None
        signature = self.permissions()
        if signature != self.access_signature:
            index = self.current
            self.access_signature = signature
            self.filter_entries()
            if index is not None and index < len(self.visible):
                self.listbox.selection_clear(0, 'end')
                self.listbox.selection_set(index)
                self.select()
        if self.current is not None and not unlocked(self.visible[self.current], self.state_provider()):
            self.show_locked(self.visible[self.current])
        self.access_job = self.after(250, self.refresh_access)

    def show_locked(self, entry):
        self.source = None
        self.photo = None
        self.canvas.itemconfigure(self.image_item, image='')
        self.canvas.itemconfigure(self.lock_item, text='Locked\nBecome official with ' + entry['character'].title() + ' to view this photo.')
        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)
        self.zoom_button.config(state='disabled')
        self.caption.config(text=entry['character'].title() + ' · Locked bedroom photo')
        self.position_lock()

    def position_lock(self):
        width, height = max(1, self.canvas.winfo_width()), max(1, self.canvas.winfo_height())
        self.canvas.coords(self.lock_item, width / 2, height / 2)
        self.canvas.itemconfigure(self.lock_item, width=max(1, width - 40))
        self.canvas.configure(scrollregion=(0, 0, width, height))

    def filter_entries(self, event=None):
        who = self.filter.get().lower()
        self.visible = [e for e in self.entries if who == 'all characters' or e['character'] == who]
        self.listbox.delete(0, 'end')
        for entry in self.visible:
            suffix = '' if unlocked(entry, self.state_provider()) else ' · Locked'
            self.listbox.insert('end', entry['character'].title() + ' · ' + entry['title'] + suffix)
        if self.visible:
            self.listbox.selection_set(0)
            self.select()

    def select(self, event=None):
        selection = self.listbox.curselection()
        if not selection:
            return
        self.current = selection[0]
        entry = self.visible[self.current]
        if not unlocked(entry, self.state_provider()):
            self.show_locked(entry)
            return
        self.canvas.itemconfigure(self.lock_item, text='')
        self.zoom_button.config(state='normal')
        try:
            with Image.open(ROOT / entry['path']) as image:
                self.source = image.convert('RGB')
        except (OSError, ValueError):
            self.source = None
            self.canvas.itemconfigure(self.image_item, image='')
            self.caption.config(text='This portrait could not be loaded.')
            return
        self.caption.config(text=f"{entry['character'].title()} — {entry['title']}  ·  {self.current + 1} / {len(self.visible)}")
        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)
        self.redraw()

    def step(self, offset):
        if not self.visible:
            return
        index = ((self.current or 0) + offset) % len(self.visible)
        self.listbox.selection_clear(0, 'end')
        self.listbox.selection_set(index)
        self.listbox.see(index)
        self.select()

    def toggle_zoom(self):
        self.zoom = not self.zoom
        self.zoom_button.config(text='Fit to window' if self.zoom else 'Inspect at 100%')
        self.redraw()

    def schedule_redraw(self, event=None):
        if self.resize_job:
            self.after_cancel(self.resize_job)
        self.resize_job = self.after(80, self.redraw)

    def redraw(self):
        self.resize_job = None
        if self.current is not None and not unlocked(self.visible[self.current], self.state_provider()):
            self.show_locked(self.visible[self.current])
            return
        if self.source is None:
            return
        width, height = max(1, self.canvas.winfo_width()), max(1, self.canvas.winfo_height())
        image = self.source if self.zoom else ImageOps.contain(self.source, (width, height), Image.Resampling.LANCZOS)
        self.photo = ImageTk.PhotoImage(image, master=self)
        x, y = max(0, (width-image.width)//2), max(0, (height-image.height)//2)
        self.canvas.coords(self.image_item, x, y)
        self.canvas.itemconfigure(self.image_item, image=self.photo)
        self.canvas.configure(scrollregion=(0, 0, max(width, image.width), max(height, image.height)))

    def destroy(self):
        if self.access_job:
            self.after_cancel(self.access_job)
            self.access_job = None
        if self.resize_job:
            self.after_cancel(self.resize_job)
            self.resize_job = None
        super().destroy()
