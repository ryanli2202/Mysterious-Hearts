"""Compact reusable relationship meters with numeric, accessible labels."""
import tkinter as tk
from tkinter import ttk

class EmotionStrip(tk.Frame):
    """A single row of named feelings, scrollable when a large party is present."""
    def __init__(self, parent, bg='#191c2b'):
        super().__init__(parent, bg=bg)
        self.canvas = tk.Canvas(self, bg=bg, width=1, height=1, bd=0, highlightthickness=0)
        self.canvas.pack(fill='x')
        self.scroll = ttk.Scrollbar(self, orient='horizontal', command=self.canvas.xview)
        self.canvas.configure(xscrollcommand=self.show_scroll)
        self.labels = []

    def show_scroll(self, first, last):
        if float(first) > 0 or float(last) < 1:
            self.scroll.pack(fill='x')
        else:
            self.scroll.pack_forget()

    def set_feelings(self, labels):
        if labels == self.labels:
            return
        self.labels = labels
        canvas = self.canvas
        canvas.delete('all')
        x = 0
        for name, feeling in labels:
            label = canvas.create_text(x + 9, 3, anchor='nw', text=name, fill='#f3eee7',
                                       font=('Segoe UI', 10))
            value = canvas.create_text(canvas.bbox(label)[2] + 6, 3, anchor='nw',
                                       text=feeling.title(), fill='#a2ddd3', font=('Segoe UI', 10, 'bold'))
            right, bottom = canvas.bbox(value)[2:]
            chip = canvas.create_rectangle(x, 0, right + 9, bottom + 3, outline='', fill='#272d40')
            canvas.tag_lower(chip)
            x = right + 15
        bounds = canvas.bbox('all')
        canvas.configure(scrollregion=bounds, height=bounds[3])
        canvas.xview_moveto(0)


class RelationshipBars(tk.Canvas):
    def __init__(self, parent, bg='#191c2b', fg='#f3eee7', horizontal=False):
        super().__init__(parent, height=38 if horizontal else 57, width=280,
                         bg=bg, highlightthickness=0, bd=0)
        self.fg = fg
        self.horizontal = horizontal
        self.stats = {}
        self.bind('<Configure>', lambda e: self.draw())

    def update_stats(self, stats, *, romanceable=None):
        self.stats = dict(stats or {})
        if romanceable is False:
            self.stats.pop('attraction', None)
        elif romanceable and stats:
            self.stats.setdefault('attraction', 0)
        self.draw()

    def draw(self):
        self.delete('all')
        width = max(100, self.winfo_width())
        for i, (key, label, color) in enumerate((('attraction', 'Attraction', '#e58ca9'),
                                                ('trust', 'Trust', '#7bc4ba'),
                                                ('closeness', 'Closeness', '#b6a0ec'))):
            value = self.stats.get(key)
            number = max(0, min(100, value)) if value is not None else 0
            if self.horizontal:
                x = i * width / 3; end = (i+1)*width/3-14
                self.create_text(x, 0, text=f'{label}  {number}/100' if value is not None else f'{label}  N/A', anchor='nw', fill=self.fg, font=('Segoe UI', 9))
                left, top, right = x, 22, end
            else:
                top = i*19+6; left, right = 76, width-53
                self.create_text(0, top+4, text=label, anchor='w', fill=self.fg, font=('Segoe UI', 9))
                self.create_text(width, top+4, text=f'{number}/100' if value is not None else 'N/A', anchor='e', fill=self.fg, font=('Segoe UI', 9))
            self.create_rectangle(left, top, right, top+7, fill='#353b4d', outline='')
            if number:
                self.create_rectangle(left, top, left+(right-left)*number/100, top+7, fill=color, outline='')
