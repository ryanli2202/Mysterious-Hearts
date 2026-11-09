"""Child windows that stay inside an active phone, with desktop fallback."""
import tkinter as tk
from tkinter import ttk, messagebox as native_messages, simpledialog as native_simple


def find_phone(parent):
    while parent is not None:
        if getattr(parent, '_is_phone', False):
            return parent
        phone = getattr(parent, 'phone_activity', None)
        if phone is not None and phone.winfo_exists() and phone.winfo_viewable():
            return phone
        parent = getattr(parent, 'master', None)
    return None


class AppWindow(tk.Toplevel):
    """Use a frame for phone content; preserve normal Toplevel behavior elsewhere."""
    def __init__(self, master=None, **kwargs):
        self.phone = find_phone(master)
        self._close = self.destroy
        if self.phone is None:
            super().__init__(master, **kwargs)
            return
        phone = self.phone
        try:
            self._previous_focus = phone.focus_get()
        except KeyError:
            # Native combobox popdowns have no Python widget wrapper.
            self._previous_focus = phone
        self.shell = tk.Frame(phone.screen, bg='#17171b')
        self.shell.place(x=0, y=0, relwidth=1, relheight=1)
        self.shell.lift()
        bar = ttk.Frame(self.shell, padding=6)
        bar.pack(fill='x')
        ttk.Button(bar, text='‹ Back', command=lambda: self._close()).pack(side='left')
        self.heading = ttk.Label(bar, wraplength=210)
        self.heading.pack(side='left', fill='x', expand=True, padx=6)
        ttk.Button(bar, text='×', width=3, command=lambda: self._close()).pack(side='right')
        self.viewport = tk.Canvas(self.shell, highlightthickness=0, bg='#17171b')
        vertical = ttk.Scrollbar(self.shell, command=self.viewport.yview)
        vertical.pack(side='right', fill='y')
        horizontal = ttk.Scrollbar(self.shell, orient='horizontal', command=self.viewport.xview)
        horizontal.pack(side='bottom', fill='x')
        self.viewport.pack(fill='both', expand=True)
        self.viewport.configure(yscrollcommand=vertical.set, xscrollcommand=horizontal.set)
        tk.Frame.__init__(self, self.viewport, **kwargs)
        self._item = self.viewport.create_window(0, 0, window=self, anchor='nw')
        def layout(event=None):
            if not self.winfo_exists(): return
            self.viewport.itemconfigure(self._item,
                width=max(self.viewport.winfo_width(), self.winfo_reqwidth()),
                height=max(self.viewport.winfo_height(), self.winfo_reqheight()))
            self.viewport.configure(scrollregion=self.viewport.bbox('all'))
        self.bind('<Configure>', layout, add='+')
        self.viewport.bind('<Configure>', layout)
        phone.dialogs.append(self)
        self.focus_set()
        self.after_idle(self._fit_content)

    def _fit_content(self):
        if not self.winfo_exists(): return
        import phone_theme
        phone_theme.apply_tree(self.shell)
        limit = max(120, self.phone.winfo_width()-110)
        def fit(widget):
            for child in widget.winfo_children():
                if isinstance(child, (tk.Label, ttk.Label)):
                    child.configure(wraplength=getattr(child, '_fixed_wraplength', limit))
                elif isinstance(child, tk.Text):
                    child.configure(width=max(16, limit//9))
                fit(child)
        fit(self)

    def lift(self, aboveThis=None):
        if self.phone is None: return super().lift(aboveThis)
        self.shell.lift()
        if self in self.phone.dialogs:
            self.phone.dialogs.remove(self)
            self.phone.dialogs.append(self)

    def title(self, text=None):
        if self.phone is None: return super().title(text)
        if text is not None: self.heading.configure(text=text)
        return self.heading.cget('text')

    def geometry(self, value=None):
        if self.phone is None: return super().geometry(value)
        return f'{self.winfo_width()}x{self.winfo_height()}'

    def minsize(self, *args):
        if self.phone is None: return super().minsize(*args)

    def resizable(self, *args):
        if self.phone is None: return super().resizable(*args)

    def transient(self, *args):
        if self.phone is None: return super().transient(*args)

    def grab_set(self):
        if self.phone is None: return super().grab_set()

    def grab_release(self):
        if self.phone is None: return super().grab_release()

    def protocol(self, name=None, func=None):
        if self.phone is None: return super().protocol(name, func)
        if name == 'WM_DELETE_WINDOW' and func is not None: self._close = func

    def destroy(self):
        if self.phone is None: return super().destroy()
        if not self.winfo_exists(): return
        if self in self.phone.dialogs: self.phone.dialogs.remove(self)
        tk.Frame.destroy(self)
        self.shell.destroy()
        focus = self._previous_focus
        if focus is not None and focus.winfo_exists(): focus.focus_set()


def _prompt(title, message, parent, confirm=False, initial=None):
    window = AppWindow(parent)
    window.title(title)
    body = ttk.Frame(window, padding=16)
    body.pack(fill='both', expand=True)
    ttk.Label(body, text=message, wraplength=250).pack(fill='x', pady=8)
    result = [False if confirm else None]
    entry = None
    if initial is not None:
        entry = ttk.Entry(body)
        entry.insert(0, initial)
        entry.pack(fill='x', pady=8)
        entry.focus_set()
    def accept():
        result[0] = entry.get() if entry is not None else True
        window.destroy()
    ttk.Button(body, text='Yes' if confirm else 'OK', command=accept).pack(pady=8)
    if confirm or entry is not None:
        ttk.Button(body, text='No' if confirm else 'Cancel', command=window.destroy).pack()
    parent.wait_window(window)
    return result[0]


class Messages:
    def __getattr__(self, name):
        def show(title, message, **kwargs):
            parent = kwargs.get('parent')
            if find_phone(parent) is None:
                return getattr(native_messages, name)(title, message, **kwargs)
            return _prompt(title, message, parent, confirm=name == 'askyesno')
        return show


class SimpleDialogs:
    def askstring(self, title, prompt, **kwargs):
        parent = kwargs.get('parent')
        if find_phone(parent) is None:
            return native_simple.askstring(title, prompt, **kwargs)
        return _prompt(title, prompt, parent, initial=kwargs.get('initialvalue', ''))


messagebox = Messages()
simpledialog = SimpleDialogs()
