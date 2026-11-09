"""Phone camera, selection wheels and the player's dated photo library."""
import copy
import math
import queue
import threading
import tkinter as tk
from tkinter import ttk
from phone_dialogs import AppWindow, messagebox, simpledialog
from PIL import Image, ImageOps, ImageTk

import camera
import codex_images
from phone_controls import PhoneButton


class CameraJobs:
    """Owned by the game, so changing phone apps doesn't discard an exposure."""
    def __init__(self, game):
        self.game = game
        self.events = queue.Queue()
        self.cancel_event = None
        self.status = 'Ready · Uses your Codex ChatGPT plan. No paid API fallback.'
        self.last = None
        self.revision = 0
        self.closed = False
        self.poll_job = game.after(150, self.poll)
        game.bind('<Destroy>', self.on_destroy, add='+')

    def on_destroy(self, event):
        if event.widget is self.game:
            self.closed = True
            if self.cancel_event:
                self.cancel_event.set()
            if self.poll_job:
                self.game.after_cancel(self.poll_job)

    def start(self, settings):
        if self.cancel_event:
            raise ValueError('A photo is already developing.')
        state = self.game.state_data
        shot = camera.request(state, settings)
        camera.ensure(state)['preferences'] = copy.deepcopy(settings)
        self.game.persist()  # Persist album identity before the background job starts.
        self.cancel_event = threading.Event()
        cancel = self.cancel_event
        self.status = 'Developing photo with your ChatGPT plan…'
        self.last = None

        def work():
            try:
                generated = codex_images.generate(shot['prompt'], cancel,
                    lambda text: self.events.put(('progress', text)), references=shot['references'])
                if cancel.is_set():
                    raise ValueError('Photo cancelled.')
                self.events.put(('complete', (state, shot, generated)))
            except Exception as exc:
                self.events.put(('error', str(exc)))
        threading.Thread(target=work, daemon=False).start()

    def cancel(self):
        if self.cancel_event:
            self.cancel_event.set()
            self.status = 'Cancelling photo…'

    def poll(self):
        self.poll_job = None
        try:
            while True:
                kind, payload = self.events.get_nowait()
                if kind == 'progress':
                    self.status = payload
                    continue
                cancelled = self.cancel_event and self.cancel_event.is_set()
                self.cancel_event = None
                if kind == 'complete' and not cancelled:
                    try:
                        state, shot, generated = payload
                        self.last = camera.commit(state, shot, generated)
                        self.status = 'Photo saved to Gallery.'
                        self.revision += 1
                    except Exception as exc:
                        self.status = 'Could not add photo to Gallery: ' + str(exc)
                else:
                    self.status = 'Photo cancelled.' if cancelled else payload
        except queue.Empty:
            pass
        if not self.closed:
            self.poll_job = self.game.after(150, self.poll)


def jobs(game):
    controller = getattr(game, 'camera_jobs', None)
    if controller is None:
        controller = game.camera_jobs = CameraJobs(game)
    return controller


class SelectionWheel(AppWindow):
    def __init__(self, parent, title, options, current, callback, custom_callback=None):
        super().__init__(parent)
        self.title(title)
        self.geometry('470x575')
        self.resizable(False, False)
        self.transient(parent.winfo_toplevel())
        self.options = list(options)
        self.index = self.options.index(current) if current in self.options else 0
        self.callback = callback
        ttk.Label(self, text=title, font=('Segoe UI', 16, 'bold')).pack(pady=8)
        self.canvas = tk.Canvas(self, width=440, height=420, bg='#191c2b', highlightthickness=0)
        self.canvas.pack()
        row = ttk.Frame(self)
        row.pack(fill='x', padx=16, pady=10)
        PhoneButton(row, text='‹ Rotate', command=lambda: self.rotate(-1)).pack(side='left')
        PhoneButton(row, text='Choose', command=self.choose).pack(side='left', expand=True)
        PhoneButton(row, text='Rotate ›', command=lambda: self.rotate(1)).pack(side='right')
        pages = ttk.Frame(self)
        pages.pack(fill='x', padx=16)
        PhoneButton(pages, text='‹ Previous set', command=lambda: self.page(-1)).pack(side='left')
        if custom_callback:
            def custom():
                self.destroy()
                custom_callback()
            PhoneButton(pages, text='Custom…', command=custom).pack(side='left', expand=True)
        PhoneButton(pages, text='Next set ›', command=lambda: self.page(1)).pack(side='right')
        self.bind('<Left>', lambda e: self.rotate(-1))
        self.bind('<Right>', lambda e: self.rotate(1))
        self.bind('<MouseWheel>', lambda e: self.rotate(-1 if e.delta > 0 else 1))
        self.bind('<Return>', lambda e: self.choose())
        self.bind('<Escape>', lambda e: (self.destroy(), 'break')[-1])
        self.draw()
        self.grab_set()
        self.focus_set()

    def rotate(self, delta):
        self.index = (self.index + delta) % len(self.options)
        self.draw()

    def page(self, delta):
        page_count = (len(self.options) + 7) // 8
        self.index = ((self.index // 8 + delta) % page_count) * 8
        self.draw()

    def draw(self):
        self.canvas.delete('all')
        start = self.index // 8 * 8
        visible = self.options[start:start + 8]
        for offset, label in enumerate(visible):
            index = start + offset
            angle = 2 * math.pi * offset / len(visible) - math.pi / 2
            x, y = 220 + 145 * math.cos(angle), 210 + 145 * math.sin(angle)
            tag = 'choice' + str(index)
            self.canvas.create_oval(x-57, y-36, x+57, y+36,
                fill='#dfba78' if index == self.index else '#30354a', outline='#68637a', tags=tag)
            self.canvas.create_text(x, y, text=label if len(label) <= 52 else label[:49] + '…', width=105,
                fill='#10121c' if index == self.index else '#f3eee7', font=('Segoe UI', 9), tags=tag)
            self.canvas.tag_bind(tag, '<Button-1>', lambda e, i=index: self.pick(i))
        current = self.options[self.index]
        self.canvas.create_text(220, 205, text=current if len(current) <= 80 else current[:77] + '…', width=130,
                                fill='#dfba78', font=('Segoe UI', 11, 'bold'))
        self.canvas.create_text(220, 260, text=f'{self.index+1} / {len(self.options)}', fill='#aaaabd')

    def pick(self, index):
        self.index = index
        self.draw()

    def choose(self):
        self.callback(self.options[self.index])
        self.destroy()


class CameraView(ttk.Frame):
    def __init__(self, host, parent, state):
        super().__init__(parent)
        self.pack(fill='both', expand=True)
        self.host, self.state = host, state
        self.controller = jobs(host.game)
        self.settings = copy.deepcopy(camera.ensure(state)['preferences'])
        self.settings.setdefault('people', {})
        self.context = camera.scene(state)
        self.mode = tk.StringVar(value=self.settings.get('mode', 'Selfie'))
        self.detail = tk.StringVar(value=self.settings.get('detail', ''))
        self.person = tk.StringVar()
        self.photo = None
        self.shown_id = None
        self.timer = None
        self.heading = ttk.Label(self, text='Camera', font=('Segoe UI', 23, 'bold'))
        self.heading.pack(anchor='w')
        self.scene_label = ttk.Label(self, wraplength=460)
        self.scene_label.pack(anchor='w', pady=5)
        toolbar = ttk.Frame(self)
        toolbar.pack(fill='x')
        self.mode_picker = ttk.Combobox(toolbar, state='readonly', textvariable=self.mode, width=25)
        self.mode_picker.pack(side='left', fill='x', expand=True)
        self.mode_picker.bind('<<ComboboxSelected>>', lambda e: self.update_controls())
        PhoneButton(toolbar, text='Gallery', command=lambda: host.open_app('Gallery')).pack(side='right', padx=(6, 0))
        ttk.Label(self, text='Hobby, food, activity or extra photo details:').pack(anchor='w', pady=(10, 3))
        self.detail_entry = ttk.Combobox(self, textvariable=self.detail)
        self.detail_entry.pack(fill='x')
        self.detail_entry.bind('<KeyRelease>', lambda e: self.update_modes())
        self.detail_entry.bind('<<ComboboxSelected>>', lambda e: self.update_modes())
        self.people_frame = ttk.Frame(self)
        self.people_frame.pack(fill='x', pady=7)
        self.person_picker = ttk.Combobox(self.people_frame, textvariable=self.person, state='readonly')
        self.person_picker.pack(fill='x')
        self.person_picker.bind('<<ComboboxSelected>>', lambda e: self.update_labels())
        buttons = ttk.Frame(self.people_frame)
        buttons.pack(fill='x', pady=5)
        self.expression_button = PhoneButton(buttons, text='Expression wheel', command=lambda: self.wheel('expression'))
        self.expression_button.pack(side='left', expand=True, fill='x')
        self.pose_button = PhoneButton(buttons, text='Pose wheel', command=lambda: self.wheel('pose'))
        self.pose_button.pack(side='left', expand=True, fill='x', padx=(5, 0))
        self.group_button = PhoneButton(self.people_frame, text='Group pose wheel', command=lambda: self.wheel('group_pose'))
        self.group_button.pack(fill='x')
        PhoneButton(self.people_frame, text='Choose outfits · You & companions', command=self.outfit_dialog).pack(fill='x', pady=4)
        self.selection_label = ttk.Label(self.people_frame, wraplength=460)
        self.selection_label.pack(anchor='w')
        actions = ttk.Frame(self)
        actions.pack(fill='x', pady=7)
        self.shutter = PhoneButton(actions, text='Take photo', command=self.take)
        self.shutter.pack(side='left', fill='x', expand=True)
        self.cancel_button = PhoneButton(actions, text='Cancel', command=self.controller.cancel)
        self.cancel_button.pack(side='right', padx=(8, 0))
        self.status = ttk.Label(self, wraplength=460)
        self.status.pack(anchor='w', pady=4)
        self.preview = ttk.Label(self, anchor='center')
        self.preview.pack(fill='both', expand=True)
        self.update_controls()
        self.tick()

    def participants(self):
        return [self.state['player']] + (self.context['companions'] if self.mode.get().startswith('Group') else [])

    def person_id(self):
        return next((p for p in self.participants() if camera.name(p) == self.person.get()), self.state['player'])

    def choices(self, who):
        choice = self.settings['people'].setdefault(who, dict(expression=camera.EXPRESSIONS[0], pose=camera.POSES[0],
                    outfit=camera.default_outfit(self.state, who, self.context), custom=''))
        if choice.get('expression') not in camera.selection_options(self.state, self.context, 'expression'):
            choice['expression'] = camera.EXPRESSIONS[0]
        if choice.get('pose') not in camera.selection_options(self.state, self.context, 'pose'):
            choice['pose'] = camera.POSES[0]
        return choice

    def update_modes(self):
        available = camera.modes(self.context, self.detail.get())
        self.mode_picker['values'] = available
        if self.mode.get() not in available:
            self.mode.set(available[0])
            self.update_controls()

    def update_controls(self):
        self.update_modes()
        self.detail_entry['values'] = (camera.town.HOME_ACTIONS.get(self.state['player'], []) if self.context['at_home']
                                      else [self.context['activity']] if self.context['activity'] else [])
        self.scene_label.config(text=f"{self.context['location_name']} · {camera.story_calendar.story_date(self.context['minute']):%d %b %Y}\n"
                                    + (', '.join(camera.name(p) for p in self.context['companions']) or 'Just you')
                                    + ('\nModelling portrait and studio wheel options available' if self.context['location'] == 'studio' else ''))
        people = self.mode.get() in camera.PEOPLE_MODES
        if people:
            for who in self.participants():
                self.choices(who)
            self.people_frame.pack(fill='x', pady=7, after=self.detail_entry)
            self.person_picker['values'] = [camera.name(p) for p in self.participants()]
            if self.person.get() not in self.person_picker['values']:
                self.person.set(camera.name(self.state['player']))
            self.group_button.config(state='normal' if self.mode.get().startswith('Group') else 'disabled')
            if self.settings.get('group_pose') not in camera.selection_options(self.state, self.context, 'group_pose'):
                self.settings['group_pose'] = camera.GROUP_POSES[0]
            self.update_labels()
        else:
            self.people_frame.pack_forget()

    def update_labels(self):
        choice = self.choices(self.person_id())
        self.selection_label.config(text=f"{choice['expression']} · {choice['pose']} · {choice['custom'] if choice['outfit']=='Custom' else choice['outfit']}"
            + ('\nGroup: ' + self.settings.get('group_pose', camera.GROUP_POSES[0]) if self.mode.get().startswith('Group') else ''))

    def wheel(self, kind):
        who = self.person_id()
        options = camera.selection_options(self.state, self.context, kind)
        current = self.settings.get(kind, options[0]) if kind == 'group_pose' else self.choices(who)[kind]
        def select(value):
            if kind == 'group_pose': self.settings[kind] = value
            else: self.choices(who)[kind] = value
            self.update_labels()
            self.save_preferences()
            self.host.game.persist()
        SelectionWheel(self, kind.replace('_', ' ').title(), options, current, select,
                       custom_callback=lambda: self.custom_selection(kind, current, select))

    def custom_selection(self, kind, current, select):
        window = AppWindow(self)
        window.title('Custom ' + kind.replace('_', ' '))
        window.geometry('530x340')
        window.transient(self.winfo_toplevel())
        body = ttk.Frame(window, padding=16)
        body.pack(fill='both', expand=True)
        ttk.Label(body, text='Type a description or reuse one you saved.', wraplength=470).pack(anchor='w', pady=8)
        value = tk.StringVar(value=camera.selection_description(current) if current.startswith(camera.CUSTOM_PREFIX) else '')
        field = ttk.Combobox(body, textvariable=value, values=camera.saved_selections(self.state, kind))
        field.pack(fill='x', pady=8)
        ttk.Label(body, text='Saved for this game and reusable for any person.\nFor group poses, describe who does what.', wraplength=470).pack(anchor='w')
        feedback = ttk.Label(body, wraplength=470)
        feedback.pack(fill='x', pady=8)
        def save():
            try:
                selected = camera.save_selection(self.state, kind, value.get())
            except ValueError as exc:
                feedback.config(text=str(exc))
                return
            select(selected)
            window.destroy()
        PhoneButton(body, text='Save & use', command=save).pack(fill='x')
        def refresh_custom(old, replacement):
            field['values'] = camera.saved_selections(self.state, kind)
            if value.get() == old:
                value.set(replacement or '')
        PhoneButton(body, text='Manage saved descriptions',
                    command=lambda: self.manage_custom(window, kind, on_change=refresh_custom)).pack(fill='x', pady=5)
        field.bind('<Return>', lambda e: save())
        window.bind('<Escape>', lambda e: (window.destroy(), 'break')[-1])
        window.grab_set()
        field.focus_set()

    def outfit_dialog(self):
        window = AppWindow(self)
        window.title('Camera · Outfits')
        window.geometry('530x600')
        window.transient(self.winfo_toplevel())
        row = ttk.Frame(window, padding=10)
        row.pack(side='bottom', fill='x')
        feedback = ttk.Label(row, wraplength=470)
        feedback.pack(fill='x')
        body = self.host.scroll_area(window)
        variables = {}
        for who in self.participants():
            box = ttk.LabelFrame(body, text=camera.name(who), padding=12)
            box.pack(fill='x', padx=10, pady=7)
            choice = self.choices(who)
            outfit = tk.StringVar(value=choice['outfit'])
            custom = tk.StringVar(value=choice.get('custom', ''))
            ttk.Combobox(box, state='readonly', textvariable=outfit,
                         values=[*camera.outfits(self.state, who), 'Custom']).pack(fill='x')
            ttk.Label(box, text='Custom outfit · type or choose a saved description').pack(anchor='w', pady=(8, 3))
            custom_field = ttk.Combobox(box, textvariable=custom,
                values=camera.ensure(self.state)['custom_outfits'].get(who, []))
            custom_field.pack(fill='x')
            def refreshed(old, replacement, who=who, outfit=outfit, custom=custom, field=custom_field):
                field['values'] = camera.custom_items(self.state, 'outfit', who)
                if custom.get() == old:
                    custom.set(replacement or '')
                    if replacement is None and outfit.get() == 'Custom':
                        outfit.set(camera.default_outfit(self.state, who, self.context))
            PhoneButton(box, text='Manage saved outfits', command=lambda who=who, callback=refreshed:
                        self.manage_custom(window, 'outfit', who, callback)).pack(fill='x', pady=(5, 0))
            variables[who] = (outfit, custom)
        def apply():
            for who, (outfit, custom) in variables.items():
                if outfit.get() == 'Custom' and not 1 <= len(custom.get().strip()) <= 500:
                    feedback.config(text=f'Enter a custom outfit for {camera.name(who)} (1–500 characters).')
                    return
            for who, (outfit, custom) in variables.items():
                self.choices(who).update(outfit=outfit.get(), custom=custom.get().strip())
                if outfit.get() == 'Custom':
                    saved = camera.ensure(self.state)['custom_outfits'].setdefault(who, [])
                    if custom.get().strip() not in saved: saved.append(custom.get().strip())
            self.save_preferences()
            self.host.game.persist()
            self.update_labels()
            window.destroy()
        PhoneButton(row, text='Use outfits for photo', command=apply).pack(fill='x', pady=5)

    def manage_custom(self, parent, kind, who=None, on_change=lambda old, new: None):
        window = AppWindow(parent)
        title = 'Saved ' + kind.replace('_', ' ') + 's'
        if who: title += ' · ' + camera.name(who)
        window.title(title)
        window.geometry('540x370')
        window.transient(parent)
        body = ttk.Frame(window, padding=16)
        body.pack(fill='both', expand=True)
        ttk.Label(body, text='Choose a saved description to edit or delete.').pack(anchor='w', pady=6)
        selected = tk.StringVar()
        picker = ttk.Combobox(body, state='readonly', textvariable=selected)
        picker.pack(fill='x', pady=6)
        editor = tk.Text(body, height=6, wrap='word', font=('Segoe UI', 11))
        editor.pack(fill='both', expand=True, pady=6)
        feedback = ttk.Label(body, wraplength=490)
        feedback.pack(fill='x', pady=6)
        actions = ttk.Frame(body)
        actions.pack(fill='x')
        def load(event=None):
            editor.delete('1.0', 'end')
            editor.insert('1.0', selected.get())
        def refresh(preferred=None):
            items = camera.custom_items(self.state, kind, who)
            picker['values'] = items
            selected.set(preferred if preferred in items else items[0] if items else '')
            load()
            for button in (edit_button, delete_button):
                button.config(state='normal' if items else 'disabled')
            if not items: feedback.config(text='No saved descriptions in this category.')
        def change(delete=False):
            old = selected.get()
            try:
                new = camera.change_custom(self.state, kind, old,
                    None if delete else editor.get('1.0', 'end').strip(), who, self.settings)
            except ValueError as exc:
                feedback.config(text=str(exc))
                return
            on_change(old, new)
            self.save_preferences()
            self.host.game.persist()
            self.update_labels()
            feedback.config(text='Deleted. Existing photos are unchanged.' if delete else 'Changes saved.')
            refresh(new)
        edit_button = PhoneButton(actions, text='Save changes', command=change)
        edit_button.pack(side='left', fill='x', expand=True)
        delete_button = PhoneButton(actions, text='Delete saved', command=lambda: change(True))
        delete_button.pack(side='left', padx=8)
        PhoneButton(actions, text='Done', command=lambda: close()).pack(side='right')
        picker.bind('<<ComboboxSelected>>', load)
        def close():
            window.destroy()
            if parent.winfo_exists(): parent.grab_set()
        window.protocol('WM_DELETE_WINDOW', close)
        window.bind('<Escape>', lambda e: close())
        refresh()
        window.grab_set()

    def save_preferences(self):
        self.settings.update(mode=self.mode.get(), detail=self.detail.get())
        camera.ensure(self.state)['preferences'] = copy.deepcopy(self.settings)

    def take(self):
        self.save_preferences()
        try:
            self.controller.start(copy.deepcopy(self.settings))
        except (ValueError, RuntimeError) as exc:
            self.controller.status = str(exc)
        self.tick_status()

    def tick_status(self):
        self.status.config(text=self.controller.status)
        working = self.controller.cancel_event is not None
        self.shutter.config(state='disabled' if working else 'normal')
        self.cancel_button.config(state='normal' if working else 'disabled')
        record = self.controller.last
        if record and record.get('album') == camera.ensure(self.state)['album'] and record['id'] != self.shown_id:
            try:
                with Image.open(camera.photo_path(record)) as image:
                    image = ImageOps.contain(image.convert('RGB'), (420, 180))
                self.photo = ImageTk.PhotoImage(image, master=self)
                self.preview.config(image=self.photo)
                self.shown_id = record['id']
            except (OSError, ValueError):
                pass

    def tick(self):
        self.timer = None
        context = camera.scene(self.state)
        if any(context[key] != self.context[key] for key in ('location', 'companions', 'romance', 'activity', 'minute')):
            self.context = context
            self.update_controls()
        self.tick_status()
        self.timer = self.after(250, self.tick)

    def destroy(self):
        self.save_preferences()
        if self.timer:
            self.after_cancel(self.timer)
        super().destroy()


class GalleryView(ttk.Frame):
    def __init__(self, host, parent, state):
        super().__init__(parent)
        self.pack(fill='both', expand=True)
        self.host, self.state = host, state
        self.controller = jobs(host.game)
        self.revision = self.controller.revision
        self.timer = None
        self.images = []
        self.top = ttk.Frame(self)
        self.top.pack(fill='x')
        ttk.Label(self.top, text='Library', font=('Segoe UI', 27, 'bold')).pack(side='left')
        PhoneButton(self.top, text='Camera', command=lambda: host.open_app('Camera')).pack(side='right')
        self.note = ttk.Label(self, wraplength=460)
        self.note.pack(fill='x', pady=6)
        self.area = ttk.Frame(self)
        self.area.pack(fill='both', expand=True)
        self.render()
        self.tick()

    def render(self):
        for child in self.area.winfo_children(): child.destroy()
        self.images.clear()
        body = self.host.scroll_area(self.area)
        try:
            entries = camera.photos(self.state)
        except (OSError, ValueError):
            ttk.Label(body, text='This photo album could not be loaded.').pack()
            return
        if not entries:
            ttk.Label(body, text='No photos yet. Take your first photo in Camera.', wraplength=430).pack(pady=24)
        date = None
        grid = None
        index = 0
        for item in entries:
            if item['date'] != date:
                date = item['date']
                ttk.Label(body, text=date, font=('Segoe UI', 15, 'bold')).pack(anchor='w', pady=(18, 6))
                grid = ttk.Frame(body)
                grid.pack(fill='x')
                grid.columnconfigure((0, 1), weight=1, uniform='photos')
                index = 0
            card = ttk.Frame(grid, padding=3)
            card.grid(row=index // 2, column=index % 2, sticky='nsew')
            index += 1
            try:
                with Image.open(camera.photo_path(item)) as image:
                    thumbnail = ImageOps.fit(image.convert('RGB'), (150, 150))
                photo = ImageTk.PhotoImage(thumbnail, master=self)
                self.images.append(photo)
                ttk.Button(card, image=photo, command=lambda p=item: show_photo(self, p)).pack(fill='x')
            except (OSError, ValueError):
                ttk.Label(card, text='Photo unavailable', padding=12).pack(fill='x')
            minute = item['minute'] % 1440
            ttk.Label(card, text=f"{minute//60:02d}:{minute%60:02d} · {item['mode']}", wraplength=150).pack(anchor='w', pady=4)
            PhoneButton(card, text='View', command=lambda p=item: show_photo(self, p)).pack(fill='x')
            from grove_gallery_ui import compose
            PhoneButton(card, text='Share', command=lambda p=item: compose(self.host, p)).pack(fill='x', pady=2)

    def tick(self):
        self.timer = None
        self.note.config(text=self.controller.status if self.controller.cancel_event else 'All photos · newest first · tap a photo to open')
        if self.controller.revision != self.revision:
            self.revision = self.controller.revision
            self.render()
        self.timer = self.after(300, self.tick)

    def destroy(self):
        if self.timer: self.after_cancel(self.timer)
        super().destroy()


def show_photo(parent, record):
    window = AppWindow(parent)
    window.title(f"{record['date']} · {record['mode']}")
    window.geometry('760x800')
    minute = record['minute'] % 1440
    ttk.Label(window, text=f"{record['date']} · {minute//60:02d}:{minute%60:02d}\n{record['location']} · {record['mode']}",
              padding=12).pack()
    try:
        with Image.open(camera.photo_path(record)) as image:
            source = image.convert('RGB')
    except (OSError, ValueError):
        ttk.Label(window, text='The photo file could not be loaded.').pack()
        return window
    label = ttk.Label(window, anchor='center')
    label.pack(fill='both', expand=True)
    def redraw(event=None):
        fitted = ImageOps.contain(source, (max(1, label.winfo_width()), max(1, label.winfo_height())))
        label.photo = ImageTk.PhotoImage(fitted, master=window)
        label.config(image=label.photo)
    label.bind('<Configure>', redraw)
    window.bind('<Escape>', lambda e: (window.destroy(), 'break')[-1])
    return window
