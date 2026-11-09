"""An incoming-message typing bubble with gently staggered dots."""
import math
import time
import tkinter as tk


class TypingIndicator(tk.Frame):
    def __init__(self, parent, *, bg, foreground):
        super().__init__(parent, bg=bg)
        self._timer = None
        self._started = 0
        self.bubble = tk.Canvas(self, width=80, height=40, bg=bg, highlightthickness=0)
        self.bubble.pack(side='left')
        fill = '#383b49'
        self.bubble.create_oval(5, 3, 37, 35, fill=fill, outline='')
        self.bubble.create_rectangle(21, 3, 53, 35, fill=fill, outline='')
        self.bubble.create_oval(37, 3, 69, 35, fill=fill, outline='')
        self.bubble.create_oval(6, 27, 19, 38, fill=fill, outline='')
        self.bubble.create_oval(1, 35, 7, 40, fill=fill, outline='')
        self._dots = [self.bubble.create_oval(x-4, 15, x+4, 23, fill=foreground, outline='')
                      for x in (23, 37, 51)]
        self.caption = tk.Label(self, text='', bg=bg, fg=foreground, font=('Segoe UI', 10))
        self.caption.pack(side='left', padx=(3, 0))

    def show(self, caption, *, before=None):
        self.caption.config(text=caption)
        if self._timer is None:
            if before is not None:
                self.pack(side='bottom', fill='x', pady=(3, 7), before=before)
            self._started = time.monotonic()
            self._animate()

    def _animate(self):
        import phone_personalization
        if phone_personalization.preferences()['reduced_motion']:
            for index, dot in enumerate(self._dots):
                x = 23 + index * 14
                self.bubble.coords(dot, x-4, 15, x+4, 23)
            self._timer = self.after(400, self._animate)
            return
        elapsed = time.monotonic() - self._started
        for index, dot in enumerate(self._dots):
            pulse = max(0, math.sin(elapsed * 5 - index * 0.8))
            x, y = 23 + index * 14, 19 - pulse * 3
            shade = round(150 + pulse * 80)
            self.bubble.coords(dot, x-4, y-4, x+4, y+4)
            self.bubble.itemconfig(dot, fill=f'#{shade:02x}{shade:02x}{shade:02x}')
        self._timer = self.after(40, self._animate)

    def hide(self):
        if self._timer is not None:
            self.after_cancel(self._timer)
            self._timer = None
        self.pack_forget()

    def destroy(self):
        self.hide()
        super().destroy()
