"""Offline, dark desktop patch notes browser."""
import tkinter as tk
from tkinter import ttk
import patch_notes as notes
import winterfield_ui as theme


class PatchNotesWindow(tk.Toplevel):
    def __init__(self, parent, preferences_path=None, export_dir=None):
        super().__init__(parent)
        self.title('Mysterious Hearts · Patch notes')
        self.geometry('1100x760'); self.minsize(850, 600)
        self.configure(bg=theme.INK)
        self.prefs_path = preferences_path or notes.PREFERENCES
        self.export_dir = export_dir or notes.ROOT/'patch_notes'/'exports'
        self.prefs = notes.preferences(self.prefs_path)
        self.current = None
        self.entries = []
        self.query = tk.StringVar(self)
        self.category = tk.StringVar(self, 'All categories')
        self.kind = tk.StringVar(self, 'All types')
        self.status = tk.StringVar(self, 'All entries')
        self.order = tk.StringVar(self, 'Catalogue order')
        self.reports = tk.BooleanVar(self, False)
        header = tk.Frame(self, bg=theme.INK); header.pack(fill='x', padx=22, pady=(18, 8))
        tk.Label(header, text='The Winterfield update archive', font=('Georgia', 23),
                 bg=theme.INK, fg=theme.GOLD).pack(anchor='w')
        tk.Label(header, text='Detailed changes · preserved history · evidence you can trace',
                 bg=theme.INK, fg=theme.MUTED, font=('Segoe UI', 10)).pack(anchor='w', pady=(5, 0))
        search = tk.Frame(self, bg=theme.INK); search.pack(fill='x', padx=22, pady=8)
        ttk.Label(search, text='Search').pack(side='left', padx=(0, 8))
        self.search = ttk.Entry(search, textvariable=self.query); self.search.pack(side='left', fill='x', expand=True)
        ttk.Button(search, text='Clear', command=lambda:self.query.set('')).pack(side='left', padx=6)
        ttk.Checkbutton(search, text='Include original chat reports', variable=self.reports,
                        command=self.refresh).pack(side='left')
        filters = tk.Frame(self, bg=theme.INK); filters.pack(fill='x', padx=22, pady=(0, 10))
        try: self.entries = notes.load()
        except (OSError, ValueError, TypeError) as error: self.load_error = str(error)
        else: self.load_error = ''
        for variable, values, width in [
                (self.category, ['All categories']+sorted({r['category'] for r in self.entries}), 21),
                (self.kind, ['All types','Release','Retrospective','Development report'], 20),
                (self.status, ['All entries','Unread','Bookmarked'], 15),
                (self.order, ['Catalogue order','Dated first','Title'], 17)]:
            box = ttk.Combobox(filters, textvariable=variable, values=values, state='readonly', width=width)
            box.pack(side='left', padx=(0, 8)); box.bind('<<ComboboxSelected>>', self.refresh)
        self.count = tk.Label(self, bg=theme.INK, fg=theme.MUTED, anchor='w')
        self.count.pack(fill='x', padx=22)
        panes = tk.PanedWindow(self, orient='horizontal', bg=theme.INK, sashwidth=8, bd=0)
        panes.pack(fill='both', expand=True, padx=22, pady=10)
        left = tk.Frame(panes, bg=theme.PANEL); panes.add(left, minsize=220, width=310)
        self.list = tk.Listbox(left, bg=theme.PANEL, fg=theme.CREAM, selectbackground=theme.EDGE,
                               selectforeground=theme.GOLD, highlightthickness=0, bd=0,
                               font=('Segoe UI', 10), activestyle='dotbox', exportselection=False)
        scroll = ttk.Scrollbar(left, command=self.list.yview)
        scroll.pack(side='right', fill='y'); self.list.pack(fill='both', expand=True)
        self.list.configure(yscrollcommand=scroll.set)
        right = tk.Frame(panes, bg=theme.PANEL); panes.add(right, minsize=400)
        self.detail = tk.Text(right, wrap='word', bg=theme.PANEL, fg=theme.CREAM,
                              selectbackground=theme.EDGE, selectforeground=theme.CREAM,
                              insertbackground=theme.CREAM, relief='flat', padx=20, pady=15,
                              font=('Segoe UI', 10), spacing3=7)
        scrollbar = ttk.Scrollbar(right, command=self.detail.yview)
        scrollbar.pack(side='right', fill='y'); self.detail.pack(fill='both', expand=True)
        self.detail.configure(yscrollcommand=scrollbar.set)
        self.detail.tag_configure('title', font=('Georgia', 19), foreground=theme.GOLD, spacing3=14)
        self.detail.tag_configure('heading', font=('Segoe UI', 11, 'bold'), foreground=theme.MINT, spacing1=10)
        actions = tk.Frame(self, bg=theme.INK); actions.pack(fill='x', padx=22, pady=(0, 8))
        self.read_button = ttk.Button(actions, text='Mark read', command=self.toggle_read)
        self.read_button.pack(side='left')
        self.bookmark_button = ttk.Button(actions, text='Bookmark', command=self.toggle_bookmark)
        self.bookmark_button.pack(side='left', padx=6)
        self.copy_button = ttk.Button(actions, text='Copy note', command=self.copy)
        self.copy_button.pack(side='left')
        self.export_button = ttk.Button(actions, text='Export note', command=lambda:self.export(False))
        self.export_button.pack(side='left', padx=6)
        self.export_all = ttk.Button(actions, text='Export filtered list', command=lambda:self.export(True))
        self.export_all.pack(side='left')
        ttk.Button(actions, text='Close', command=self.destroy).pack(side='right')
        self.feedback = tk.Label(self, text='', bg=theme.INK, fg=theme.MINT, anchor='w', wraplength=1000)
        self.feedback.pack(fill='x', padx=22, pady=(0, 5))
        foot = tk.Label(self, text=notes.NOTICE, bg=theme.INK, fg=theme.MUTED,
                       font=('Segoe UI', 9), justify='left', anchor='w', wraplength=1020)
        foot.pack(fill='x', padx=22, pady=(0, 14))
        # Reserve footer/action space before assigning the expandable reader pane.
        for widget in (panes, actions, self.feedback, foot): widget.pack_forget()
        foot.pack(side='bottom', fill='x', padx=22, pady=(0, 14))
        self.feedback.pack(side='bottom', fill='x', padx=22, pady=(0, 5))
        actions.pack(side='bottom', fill='x', padx=22, pady=(0, 8))
        panes.pack(fill='both', expand=True, padx=22, pady=10)
        self.bind('<Configure>', lambda e:foot.configure(wraplength=max(700,self.winfo_width()-44)) if e.widget is self else None)
        self.list.bind('<<ListboxSelect>>', self.choose)
        self.query.trace_add('write', self.refresh)
        self.bind('<Control-f>', lambda e:self.search.focus_set())
        self.bind('<Escape>', lambda e:self.destroy())
        self.refresh()

    def refresh(self, *_):
        previous = self.current['id'] if self.current else None
        self.visible = notes.select(self.entries, self.query.get(), self.category.get(), self.kind.get(),
                                    self.status.get(), self.prefs, self.reports.get(), self.order.get())
        self.list.delete(0, 'end')
        for r in self.visible:
            marker = ('★ ' if r['id'] in self.prefs['bookmarks'] else '')+('● ' if notes.unread(r,self.prefs) else '')
            self.list.insert('end', marker+r['title'])
        unread = sum(notes.unread(r,self.prefs) for r in self.visible)
        self.count.configure(text=f'{len(self.visible)} entries shown · {unread} unread · ● unread / ★ bookmarked')
        self.current = None
        if self.visible:
            index = next((i for i,r in enumerate(self.visible) if r['id']==previous),0)
            self.list.selection_set(index); self.list.see(index); self.choose()
        else:
            self.show_text('Unable to load patch notes: '+self.load_error if self.load_error else
                           'No matching updates. Clear search or change the filters.\nEnable original chat reports to include development discussions.')
            self.update_buttons()
        self.export_all.configure(state='normal' if self.visible else 'disabled')

    def choose(self, *_):
        selected = self.list.curselection()
        if not selected: return
        self.current = self.visible[selected[0]]
        self.show_text(notes.render(self.current)); self.update_buttons()

    def show_text(self, text):
        self.detail.configure(state='normal'); self.detail.delete('1.0','end')
        for line in text.splitlines():
            tag = 'title' if line.startswith('# ') else 'heading' if line.startswith('## ') else ''
            self.detail.insert('end', line.lstrip('# ')+'\n' if tag else line+'\n', tag)
        self.detail.configure(state='disabled'); self.detail.yview_moveto(0)

    def update_buttons(self):
        state = 'normal' if self.current else 'disabled'
        for widget in (self.read_button,self.bookmark_button,self.copy_button,self.export_button): widget.configure(state=state)
        if self.current:
            self.read_button.configure(text='Mark read' if notes.unread(self.current,self.prefs) else 'Mark unread')
            self.bookmark_button.configure(text='Remove bookmark' if self.current['id'] in self.prefs['bookmarks'] else 'Bookmark')

    def persist(self):
        try: notes.save_preferences(self.prefs,self.prefs_path)
        except OSError as error:
            self.feedback.configure(text='Could not save reader preferences: '+str(error))
            self.prefs = notes.preferences(self.prefs_path)
        else: self.feedback.configure(text='Reader preferences saved. Story progress is unchanged.')
        self.refresh()

    def toggle_read(self):
        if not self.current: return
        key = self.current['id']
        if notes.unread(self.current,self.prefs): self.prefs['read'][key] = notes.revision(self.current)
        else: self.prefs['read'].pop(key,None)
        self.persist()

    def toggle_bookmark(self):
        if not self.current: return
        key = self.current['id']
        if key in self.prefs['bookmarks']: self.prefs['bookmarks'].remove(key)
        else: self.prefs['bookmarks'].append(key)
        self.persist()

    def copy(self):
        if self.current:
            self.clipboard_clear(); self.clipboard_append(notes.render(self.current))
            self.feedback.configure(text='Selected note copied as Markdown.')

    def export(self, all_visible):
        entries = self.visible if all_visible else [self.current] if self.current else []
        if not entries: return
        # Unique filenames preserve earlier exports; no native file dialog is needed.
        import uuid
        path = self.export_dir/('patch-notes-'+uuid.uuid4().hex[:10]+'.md')
        try: notes.export(entries,path)
        except OSError as error: self.feedback.configure(text='Export failed: '+str(error))
        else: self.feedback.configure(text='Exported to '+str(path))


def open_window(parent):
    window = getattr(parent, '_patch_notes_window', None)
    if window is not None and window.winfo_exists():
        window.deiconify(); window.lift(); return window
    parent._patch_notes_window = PatchNotesWindow(parent)
    return parent._patch_notes_window
