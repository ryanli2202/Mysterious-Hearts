"""Rounded, keyboard-operable controls scoped to the phone."""
import tkinter as tk
from tkinter import font as tkfont
import winterfield_ui as ui


class PhoneButton(tk.Canvas):
    def __init__(self, parent, text='', command=None, state='normal', style='',
                 width=None, icon=None, **kwargs):
        self.options = dict(text=text, command=command, state=state, style=style)
        self.icon = icon
        self.hover = False
        self.pressed = False
        self.fixed_width = width
        self.font = tkfont.Font(family='Segoe UI', size=10)
        super().__init__(parent, height=38, bg='#17171b', highlightthickness=0,
                         takefocus=True, cursor='hand2', **kwargs)
        self.bind('<Configure>', self._draw)
        self.bind('<Enter>', lambda e: self._hover(True))
        self.bind('<Leave>', lambda e: self._hover(False))
        self.bind('<ButtonPress-1>', self._press)
        self.bind('<ButtonRelease-1>', self._release)
        self.bind('<Return>', lambda e: self.invoke())
        self.bind('<space>', lambda e: self.invoke())
        self.bind('<FocusIn>', self._draw)
        self.bind('<FocusOut>', self._draw)
        self._size()

    def _size(self):
        super().configure(width=40 if self.icon else max(44, self.font.measure(self.options['text']) + 30,
                          (self.fixed_width or 0) * 8))
        self._draw()

    def configure(self, cnf=None, **kwargs):
        if cnf:
            kwargs.update(cnf)
        changed = False
        for key in tuple(kwargs):
            if key in self.options:
                self.options[key] = kwargs.pop(key)
                changed = True
        if kwargs:
            super().configure(**kwargs)
        if changed:
            self._size()

    config = configure

    def cget(self, key):
        return self.options[key] if key in self.options else super().cget(key)

    def invoke(self):
        if self.options['state'] != 'disabled' and self.options['command']:
            return self.options['command']()

    def _hover(self, value):
        self.hover = value
        self.pressed = False
        self._draw()

    def _press(self, event):
        if self.options['state'] != 'disabled':
            self.focus_set()
            self.pressed = True
            self._draw()

    def _release(self, event):
        activate = self.pressed and 0 <= event.x < self.winfo_width() and 0 <= event.y < self.winfo_height()
        self.pressed = False
        self._draw()
        if activate:
            self.invoke()

    def _draw(self, event=None):
        self.delete('all')
        w, h = self.winfo_width() if self.winfo_width() > 1 else int(super().cget('width')), 38
        disabled = self.options['state'] == 'disabled'
        accent = self.options['style'] == 'Accent.TButton' or self.icon == 'send'
        fill = '#0a84ff' if accent else '#2c2c2e'
        if self.hover and not disabled:
            fill = '#409cff' if accent else '#3a3a3c'
        if self.pressed:
            fill = '#0062cc' if accent else '#243044'
        if disabled:
            fill = '#232326'
        ink = '#788598' if disabled else '#dce4ed'
        # Combobox popdowns are Tcl-only widgets, which focus_get cannot resolve.
        outline = '#80bfff' if str(self.tk.call('focus')) == str(self) else fill
        self.create_polygon(20,2, w-20,2, w-2,2, w-2,19, w-2,h-2,
                            w-20,h-2, 20,h-2, 2,h-2, 2,19, 2,2,
                            smooth=True, splinesteps=24, fill=fill, outline=outline, width=2)
        if self.icon == 'send':
            self.delete('all')
            self.create_oval(w/2-17,2,w/2+17,36, fill=fill, outline=outline, width=2)
            self.create_line(w/2,27, w/2,11, fill=ink, width=3, capstyle='round')
            self.create_line(w/2-6,17, w/2,11, w/2+6,17, fill=ink, width=3,
                             capstyle='round', joinstyle='round')
        else:
            self.create_text(w/2,h/2, text=self.options['text'], fill=ink, font=self.font,
                             width=max(20,w-16), justify='center')


class MessageField(tk.Canvas):
    def __init__(self, parent):
        super().__init__(parent, height=44, width=100, bg='#17171b', highlightthickness=0)
        self.entry = tk.Entry(self, bg='#232326', fg='#dce4ed', insertbackground='#dce4ed',
                              relief='flat', bd=0, font=('Segoe UI', 12), exportselection=False)
        self.bind('<Configure>', self._draw)
        self.entry.bind('<FocusIn>', self._draw)
        self.entry.bind('<FocusOut>', self._draw)

    def _draw(self, event=None):
        self.delete('all')
        w = self.winfo_width()
        self.create_polygon(22,2, w-22,2, w-2,2, w-2,22, w-2,42,
                            w-22,42, 22,42, 2,42, 2,22, 2,2, smooth=True,
                            splinesteps=24, fill='#232326',
                            outline='#0a84ff' if self.entry.focus_get() is self.entry else '#48484a')
        self.create_window(16,22, window=self.entry, anchor='w', width=max(20,w-32))
