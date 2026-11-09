"""Nonblocking subscription-only image requests and persistent generated-image viewer."""
import queue
import threading
import tkinter as tk
from tkinter import ttk
from phone_dialogs import AppWindow, messagebox, simpledialog
from PIL import Image, ImageOps, ImageTk
import codex_images


class ImageStudio(AppWindow):
    def __init__(self, parent):
        super().__init__(parent)
        self.title('Mysterious Hearts · Image studio')
        self.geometry('980x800')
        self.minsize(720, 600)
        self.events = queue.Queue()
        self.cancel_event = None
        self.source = None
        self.photo = None
        self.poll_job = None
        self.resize_job = None
        self.closed = False
        self.protocol('WM_DELETE_WINDOW', self.destroy)
        top = ttk.Frame(self, padding=14)
        top.pack(fill='x')
        ttk.Label(top, text='Image studio', font=('Segoe UI', 20, 'bold')).pack(anchor='w')
        ttk.Label(top, text='Uses your Codex ChatGPT login and plan allowance. No paid API fallback.\n'
                  'Describe an image; it will appear below when ready and remain in your library.',
                  wraplength=870).pack(anchor='w', pady=6)
        self.prompt = tk.Text(top, height=4, wrap='word', font=('Segoe UI', 11))
        self.prompt.pack(fill='x', pady=6)
        actions = ttk.Frame(top)
        actions.pack(fill='x')
        self.generate_button = ttk.Button(actions, text='Generate image', command=self.generate)
        self.generate_button.pack(side='left')
        self.cancel_button = ttk.Button(actions, text='Cancel', command=self.cancel, state='disabled')
        self.cancel_button.pack(side='left', padx=8)
        self.status = ttk.Label(top, text='Ready · Codex must be signed in with ChatGPT.', wraplength=870)
        self.status.pack(anchor='w', pady=8)
        self.progress = ttk.Progressbar(top, mode='indeterminate')
        self.progress.pack(fill='x')
        body = ttk.Frame(self, padding=(14, 0, 14, 14))
        body.pack(fill='both', expand=True)
        self.listbox = tk.Listbox(body, width=28, exportselection=False)
        self.listbox.pack(side='left', fill='y', padx=(0, 12))
        self.listbox.bind('<<ListboxSelect>>', self.select)
        self.canvas = tk.Canvas(body, bg='#191c2b', highlightthickness=0)
        self.canvas.pack(side='left', fill='both', expand=True)
        self.image_item = self.canvas.create_image(0, 0, anchor='center')
        self.canvas.bind('<Configure>', self.schedule_redraw)
        self.refresh_library()
        self.poll_job = self.after(100, self.poll)

    def refresh_library(self, selected=None):
        self.entries = codex_images.library()
        self.listbox.delete(0, 'end')
        for item in self.entries:
            self.listbox.insert('end', item['prompt'].replace('\n', ' ')[:65])
        if self.entries:
            index = next((i for i, item in enumerate(self.entries) if item['id'] == selected), 0)
            self.listbox.selection_set(index)
            self.listbox.see(index)
            self.select()

    def select(self, event=None):
        indices = self.listbox.curselection()
        if not indices:
            return
        try:
            with Image.open(self.entries[indices[0]]['path']) as image:
                self.source = image.convert('RGBA')
            self.redraw()
        except (OSError, ValueError):
            self.status.config(text='This saved image could not be loaded.')

    def schedule_redraw(self, event=None):
        if self.resize_job:
            self.after_cancel(self.resize_job)
        self.resize_job = self.after(80, self.redraw)

    def redraw(self):
        if self.resize_job:
            self.after_cancel(self.resize_job)
            self.resize_job = None
        if self.source is None:
            return
        w, h = max(1, self.canvas.winfo_width()), max(1, self.canvas.winfo_height())
        fitted = ImageOps.contain(self.source, (w, h), Image.Resampling.LANCZOS)
        self.photo = ImageTk.PhotoImage(fitted, master=self)
        self.canvas.coords(self.image_item, w / 2, h / 2)
        self.canvas.itemconfigure(self.image_item, image=self.photo)

    def generate(self):
        if self.cancel_event is not None:
            return
        prompt = self.prompt.get('1.0', 'end').strip()
        if not prompt or len(prompt) > 6000:
            self.status.config(text='Enter an image description between 1 and 6,000 characters.')
            return
        self.cancel_event = threading.Event()
        cancel = self.cancel_event
        self.generate_button.config(state='disabled')
        self.cancel_button.config(state='normal')
        self.progress.start(15)

        def work():
            try:
                result = codex_images.generate(prompt, cancel, lambda text: self.events.put(('progress', text)))
                self.events.put(('complete', result))
            except Exception as exc:
                self.events.put(('error', str(exc)))
        # Let cancellation reap the CLI process even when the main game window closes.
        threading.Thread(target=work, daemon=False).start()

    def cancel(self):
        if self.cancel_event:
            self.cancel_event.set()
            self.status.config(text='Cancelling image request…')
            self.cancel_button.config(state='disabled')

    def poll(self):
        self.poll_job = None
        try:
            while True:
                kind, value = self.events.get_nowait()
                if kind == 'progress':
                    self.status.config(text=value)
                    continue
                self.cancel_event = None
                self.progress.stop()
                self.generate_button.config(state='normal')
                self.cancel_button.config(state='disabled')
                if kind == 'complete':
                    self.refresh_library(value['id'])
                    self.status.config(text='Image saved and loaded · ChatGPT plan used.')
                else:
                    self.status.config(text=value)
        except queue.Empty:
            pass
        if not self.closed:
            self.poll_job = self.after(100, self.poll)

    def destroy(self):
        self.closed = True
        self.cancel()
        for job in (self.poll_job, self.resize_job):
            if job:
                self.after_cancel(job)
        self.progress.stop()
        super().destroy()
