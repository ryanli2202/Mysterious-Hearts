"""Dark, asynchronously updated product photography for Supafast cards."""
import tkinter as tk
from PIL import Image, ImageOps, ImageTk
from phone_controls import PhoneButton
import supafast


class ProductPhoto(tk.Frame):
    def __init__(self, parent, manager, product, noun="product"):
        super().__init__(parent, bg='#18212e')
        self.manager, self.product = manager, product
        self.noun = noun
        self.bundled = getattr(manager, 'bundled', False) is True
        self.photo = None
        self.loaded = None
        self.broken = False
        self.label = tk.Label(self, bg='#18212e', fg='#a9bdd4',
                              font=('Segoe UI', 10), text=f'Preparing {noun} photo…',
                              height=7, wraplength=260)
        self.label.pack(fill='x', padx=6, pady=6)
        self.retry = PhoneButton(self, text=f'Retry {noun} photos', command=self.retry_images)
        self.timer = None
        self.bind('<Destroy>', self.cleanup, add='+')
        self.tick()

    def retry_images(self):
        if self.broken:
            self.product.pop('image', None)
            self.product.pop('image_job', None)
            self.manager.game.persist()
            self.broken = False
        self.loaded = None
        self.manager.request(retry=True)
        self.retry.pack_forget()

    def tick(self):
        self.timer = None
        path = (self.manager.image_path(self.product) if self.bundled
                else supafast.image_path(self.product))
        if path and str(path) != self.loaded:
            try:
                with Image.open(path) as source:
                    # Preserve the complete product rather than cropping important details.
                    picture = ImageOps.contain(source.convert('RGB'), (240, 150))
                self.photo = ImageTk.PhotoImage(picture, master=self)
                self.label.configure(image=self.photo, text='', height=0)
                self.loaded = str(path)
                self.retry.pack_forget()
            except (OSError, ValueError):
                self.broken = True
                self.loaded = str(path)
                if not self.bundled:
                    self.retry.pack(fill='x', padx=6, pady=(0,6))
                self.label.configure(image='', text=f'{self.noun.title()} photo unavailable', height=7)
        elif not path:
            self.loaded = None
            if self.bundled:
                self.label.configure(image='', height=7,
                                     text='Bundled food illustration unavailable')
                self.retry.pack_forget()
                return
            failed = self.manager.status(self.product) == 'error'
            self.label.configure(image='', height=7, text='Photo unavailable · check Codex ChatGPT login or wait for other image jobs.' if failed else f'Preparing {self.noun} photo…')
            if failed: self.retry.pack(fill='x', padx=6, pady=(0,6))
            else: self.retry.pack_forget()
        if not self.bundled:
            self.timer = self.after(500, self.tick)

    def cleanup(self, event):
        if event.widget is self and self.timer:
            self.after_cancel(self.timer)
            self.timer = None
