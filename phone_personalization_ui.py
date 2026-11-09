"""Personal phone screens and fixed-proportion device controls."""
import custom_protagonist
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from phone_dialogs import AppWindow, messagebox, simpledialog
from PIL import Image, ImageOps, ImageTk, ImageEnhance
import phone_personalization as personal
from phone_controls import PhoneButton


class PersonalPhone:
    def apply_device_size(self):
        w, h = personal.size(self.winfo_screenwidth(), self.winfo_screenheight())
        self.device_height = h
        self.resizable(False, False)
        self.minsize(1, 1)
        self.geometry(f'{w}x{h}')

    def back(self):
        if getattr(self, 'dialogs', []):
            self.dialogs[-1]._close()
            return 'break'
        if getattr(self, 'detail_open', False):
            self.detail_open = False
            self.open_app('Contacts')
        elif self.selected == 'Conversation': self.open_app('Messages')
        elif self.selected == 'Keepsake': self.open_app('Gallery')
        elif self.selected == 'Customise': self.open_app('Settings')
        elif self.selected != 'Home': self.open_app('Home')
        else: self.close_phone()
        return 'break'

    def personal_home(self, frame, s, locked=False):
        if not locked:
            from phone_home import home
            return home(self, frame, s)
        import phone_icons
        import town
        d = personal.ensure(s)
        canvas = tk.Canvas(frame, highlightthickness=0, bg='#111925', takefocus=True)
        canvas.pack(side='left', fill='both', expand=True)
        canvas.bind('<MouseWheel>', lambda e: 'break')
        self.messages_icon = self.hearts_icon = self.grove_icon = self.unread_label = None
        names = list(dict.fromkeys(d['app_order'] + list(phone_icons.COLORS)))
        self.home_icons = []
        def draw(event=None):
            for icon in self.home_icons: icon.destroy()
            self.home_icons = []
            canvas.delete('all')
            width = max(180, canvas.winfo_width())
            height = max(300, canvas.winfo_height())
            columns = 2 if width < 310 else 3 if width < 540 else 4
            total = height if locked else max(height, 215 + ((len(names)+columns-1)//columns)*118)
            try:
                with Image.open(personal.wallpaper_path(s)) as source:
                    art = ImageOps.fit(source.convert('RGB'), (width, total), Image.Resampling.LANCZOS)
                art = ImageEnhance.Brightness(art).enhance(.53)
                canvas.wallpaper = ImageTk.PhotoImage(art, master=canvas)
                canvas.create_image(0, 0, image=canvas.wallpaper, anchor='nw')
            except (OSError, ValueError): pass
            minute = s['world']['minute'] % 1440
            canvas.create_text(width/2, 40, text=f'{minute//60:02}:{minute%60:02}', fill='#dce4ed', font=('Segoe UI', 38, 'bold'))
            canvas.create_text(width/2, 82, text=town.loop.dates.story_date(s['world']['minute']).strftime('%A, %B %d'), fill='#dce4ed', font=('Segoe UI', 11))
            canvas.create_text(width/2, 111, text=f'{custom_protagonist.display_name(s["player"])}’s {personal.preferences()["device"].lower()}', fill=d['accent'], font=('Segoe UI', 13, 'bold'))
            unread = phone_icons.unread_messages(s)
            self.home_unread_item = canvas.create_text(width/2, 141, text=f'{unread} unread messages' if unread else '', fill='#dce4ed', font=('Segoe UI', 11))
            if locked:
                previews = []
                mode = personal.preferences()['preview']
                for who, route in s['routes'].items():
                    if not route.get('unread'): continue
                    text = 'New message'
                    if mode != 'Hidden': text = personal.name(s, who)
                    if mode == 'Full':
                        rows = [r for r in personal.records(s) if r['who'] == who and not r['earlier'] and r['kind'] == 'in']
                        if rows: text += ': ' + rows[-1]['text'][:140]
                    previews.append(text)
                for key, group in s.get('groups', {}).items():
                    if group.get('channel') == 'text' and group.get('unread'):
                        previews.append('New message' if mode == 'Hidden' else group['name'])
                canvas.create_text(width/2, 180, text='\n\n'.join(previews[:4]), width=width-40, anchor='n', fill='#dce4ed', font=('Segoe UI', personal.preferences()['text_size']))
                button = PhoneButton(canvas, text='Unlock', command=lambda: self.open_app('Home'))
                canvas.create_window(width/2, height-45, window=button)
                self.home_icons.append(button)
            else:
                for i, name in enumerate(names):
                    x, y = (i%columns+.5)*width/columns, 213+(i//columns)*118
                    icon = phone_icons.AppIcon(canvas, name, lambda name=name: self.open_app(name))
                    canvas.create_window(x, y, window=icon)
                    canvas.create_text(x, y+52, text=name, fill='#dce4ed', font=('Segoe UI', 10), width=width/columns-8)
                    self.home_icons.append(icon)
                    if name == 'Messages': self.messages_icon = icon; icon.set_unread(unread)
                    elif name == 'Mysterious Hearts': self.hearts_icon = icon
                    elif name == 'Grove': self.grove_icon = icon
            canvas.config(scrollregion=(0, 0, width, total))
        canvas.bind('<Configure>', draw)
        self.home_canvas = canvas

    def lock_page(self, frame, s): self.personal_home(frame, s, locked=True)

    def keepsake_page(self, frame, s):
        captions = {'rei': 'A quiet landscape saved for inspiration.',
                    'garrett': 'City lights, saved for a quiet moment.',
                    'minsu': 'A campus view, saved between study and training.',
                    'ivan': 'A studio scene saved for inspiration.'}
        ttk.Label(frame, text='Saved image · Before the story', font=('Segoe UI', 16, 'bold')).pack(anchor='w')
        ttk.Label(frame, text=captions.get(s['player'], 'Your new life in Winterfield.'), wraplength=300).pack(fill='x', pady=8)
        label = ttk.Label(frame); label.pack(fill='both', expand=True)
        def draw(event=None):
            try:
                with Image.open(personal.wallpaper_path(s, 'default')) as source:
                    art = ImageOps.contain(source.convert('RGB'), (max(1,label.winfo_width()),max(1,label.winfo_height())))
                label.photo=ImageTk.PhotoImage(art,master=self); label.config(image=label.photo)
            except OSError: label.config(text='Image unavailable')
        label.bind('<Configure>',draw)
        PhoneButton(frame, text='Use as wallpaper', command=lambda: (personal.ensure(s).__setitem__('wallpaper','default'),self.game.persist())).pack(fill='x')

    def notes_page(self, frame, s):
        d = personal.ensure(s)
        ttk.Label(frame, text='Notes', font=('Segoe UI', 22, 'bold')).pack(anchor='w')
        ttk.Label(frame, text='From before the story · '+d['story_note'], wraplength=320).pack(fill='x', pady=10)
        ttk.Label(frame, text='Your notes · private, not sent to characters').pack(anchor='w')
        self.notes_editor = tk.Text(frame, wrap='word', undo=True, font=('Segoe UI', personal.preferences()['text_size']), height=10)
        self.notes_editor.insert('1.0', d['notes'])
        self.notes_editor.pack(fill='both', expand=True, pady=8)
        def save():
            d['notes'] = self.notes_editor.get('1.0', 'end-1c')
            self.game.persist()
        PhoneButton(frame, text='Save notes', command=save).pack(fill='x')
        self.notes_editor.bind('<FocusOut>', lambda e: save() if self.notes_editor.winfo_exists() else None)

    def message_library(self, frame, s):
        d = personal.ensure(s)
        ttk.Label(frame, text=f'Pinned messages · {len(d["pins"])}/3', font=('Segoe UI', 18, 'bold')).pack(anchor='w')
        ttk.Label(frame, text='Three pins across your phone. Unpin one to make room.', wraplength=320).pack(anchor='w', pady=4)
        query = tk.StringVar(value=getattr(self, 'library_query', ''))
        entry = ttk.Entry(frame, textvariable=query)
        entry.pack(fill='x', pady=6)
        entry.insert(0, '')
        ttk.Label(frame, text='Search seen messages by contact or words').pack(anchor='w')
        body = self.scroll_area(frame)
        rows = personal.records(s)
        def render(*args):
            self.library_query = query.get()
            for child in body.winfo_children(): child.destroy()
            ordered = sorted(rows, key=lambda r: r['id'] not in d['pins'])
            found = 0
            for r in ordered:
                label = s['groups'][r['who']]['name'] if r['group'] else personal.name(s, r['who'])
                if query.get().casefold() not in (label+' '+r['text']).casefold(): continue
                found += 1
                card = ttk.Frame(body, padding=8); card.pack(fill='x', pady=4)
                pinned = r['id'] in d['pins']
                ttk.Label(card, text=('★ ' if pinned else '') + label + (' · Earlier' if r['earlier'] else ' · You' if r['kind']=='out' else ''), wraplength=300).pack(anchor='w')
                ttk.Label(card, text=r['text'], wraplength=300, font=('Segoe UI', personal.preferences()['text_size'])).pack(fill='x', pady=5)
                PhoneButton(card, text='Unpin' if pinned else 'Pin message', command=lambda r=r, pinned=pinned: toggle(r, pinned)).pack(anchor='w')
                PhoneButton(card, text='Open conversation', command=lambda r=r: self.open_thread(r['who'], r['group'])).pack(anchor='w', pady=2)
            if not found: ttk.Label(body, text='No matching messages.').pack(pady=12)
        def toggle(row, pinned):
            try: (personal.unpin if pinned else personal.pin)(s, row['id'])
            except ValueError as exc: messagebox.showinfo('Pinned messages', str(exc), parent=self); return
            self.game.persist(); self.refresh()
        query.trace_add('write', render)
        render()

    def edit_contact(self, who):
        s = self.game.state_data
        value = simpledialog.askstring('Contact name', 'Name shown on your phone (story dialogue stays unchanged):', initialvalue=personal.name(s, who), parent=self)
        if value is None: return
        try: personal.rename(s, who, value)
        except ValueError as exc: messagebox.showinfo('Contact name', str(exc), parent=self); return
        self.game.persist(); self.refresh()

    def favourite_contact(self, who):
        fav = personal.ensure(self.game.state_data)['favourites']
        if who in fav: fav.remove(who)
        else: fav.append(who)
        self.game.persist(); self.refresh()

    def pin_chat(self, key, group=False):
        pins = personal.ensure(self.game.state_data)['pinned_chats']
        ident = ('group:' if group else 'route:') + key
        if ident in pins: pins.remove(ident)
        else: pins.append(ident)
        self.game.persist(); self.refresh()

    def scroll_phone(self, event):
        from messages_ui import MessageBubbles
        widget = event.widget
        # Widgets with their own wheel behavior keep it (maps, messages, games).
        if isinstance(widget, MessageBubbles) or widget.bind('<MouseWheel>'): return
        while widget is not self:
            widget = getattr(widget, 'master', self)
            if isinstance(widget, tk.Canvas) and widget.cget('scrollregion'):
                widget.yview_scroll(-int(event.delta/120), 'units')
                return 'break'

    def contact_custom_controls(self, card, s, who):
        d = personal.ensure(s)
        PhoneButton(card, text='Edit contact name', command=lambda: self.edit_contact(who)).pack(fill='x', pady=2)
        PhoneButton(card, text='★ Favourite' if who in d['favourites'] else '☆ Add favourite', command=lambda: self.favourite_contact(who)).pack(fill='x', pady=2)
        tones = ttk.Combobox(card, values=['Default', 'Chime', 'Soft', 'Silent'], state='readonly')
        tones.set(d['tones'].get(who, 'Default')); tones.pack(fill='x', pady=2)
        tones.bind('<<ComboboxSelected>>', lambda e: (d['tones'].__setitem__(who, tones.get()), self.game.persist()))
        choices = {'Character portrait': 'default'}
        for ident, (label, _) in personal.photos(s).items(): choices[label+' · '+ident[-6:]] = ident
        avatar = ttk.Combobox(card, values=list(choices), state='readonly')
        avatar.set(next((k for k, v in choices.items() if v == d['avatars'].get(who, 'default')), 'Character portrait'))
        avatar.pack(fill='x', pady=2)
        def choose(e):
            d['avatars'][who] = choices[avatar.get()]
            self.avatars._avatars.clear(); self.game.persist(); self.refresh()
        avatar.bind('<<ComboboxSelected>>', choose)

    def customization_page(self, frame, s):
        import phone_icons
        d = personal.ensure(s); p = personal.preferences()
        body = self.scroll_area(frame)
        ttk.Label(body, text='Make it yours', font=('Segoe UI', 22, 'bold')).pack(anchor='w')
        ttk.Label(body, text='Appearance and contacts belong to this story. Controls and accessibility apply to all stories.', wraplength=320).pack(fill='x', pady=8)
        def choice(label, values, current, callback):
            ttk.Label(body, text=label).pack(anchor='w', pady=(10, 3))
            var = tk.StringVar(value=str(current))
            widget = ttk.Combobox(body, textvariable=var, values=values, state='readonly')
            widget.pack(fill='x'); widget.bind('<<ComboboxSelected>>', lambda e: callback(var.get()))
        def setting(key, value):
            personal.save_preferences({key: value})
            if key in ('device', 'scale'): self.apply_device_size()
        choice('Device proportions', ['Phone', 'Tablet'], p['device'], lambda v: setting('device', v))
        choice('Device size (%)', [60, 75, 85, 100, 120], p['scale'], lambda v: setting('scale', int(v)))
        PhoneButton(body, text='Fit to screen', command=lambda: (setting('scale', 100), self.refresh())).pack(fill='x', pady=5)
        choice('Message text size', [10, 12, 14, 16, 18, 20], p['text_size'], lambda v: setting('text_size', int(v)))
        choice('Lock screen previews', ['Hidden', 'Sender only', 'Full'], p['preview'], lambda v: setting('preview', v))
        choice('New message text reveal', ['Instant', 'Fast', 'Gentle'], p['reveal'], lambda v: setting('reveal', v))
        for label, key in [('Reduce animation', 'reduced_motion'), ('Show typing indicator', 'typing_indicator'), ('Confirm before sending replies', 'confirm_send')]:
            var = tk.BooleanVar(value=p[key])
            ttk.Checkbutton(body, text=label, variable=var, command=lambda key=key, var=var: setting(key, var.get())).pack(anchor='w', pady=7)
        meters = tk.BooleanVar(value=d.get('relationship_meters', True))
        ttk.Checkbutton(body, text='Show relationship meters in contact profiles', variable=meters,
                        command=lambda: (d.__setitem__('relationship_meters', meters.get()),self.game.persist())).pack(anchor='w',pady=7)
        for label, key in [('Notification volume', 'notification_volume'), ('Typing sound volume', 'typing_volume'), ('Voicemail volume', 'voicemail_volume')]:
            choice(label, [0, 25, 50, 75, 100], p[key], lambda v, key=key: setting(key, int(v)))
        wallpapers = {'Protagonist original': 'default'}
        wallpapers.update({label+' · '+ident[-6:]: ident for ident, (label, _) in personal.photos(s).items()})
        selected = tk.StringVar(value=next((k for k, v in wallpapers.items() if v == d['wallpaper']), 'Protagonist original'))
        ttk.Label(body, text='Wallpaper · Gallery photos unlock here').pack(anchor='w', pady=(16, 4))
        picker = ttk.Combobox(body, values=list(wallpapers), textvariable=selected, state='readonly'); picker.pack(fill='x')
        preview = ttk.Label(body); preview.pack(pady=8)
        def preview_art(event=None):
            try:
                with Image.open(personal.wallpaper_path(s, wallpapers[selected.get()])) as source:
                    art = ImageOps.fit(source.convert('RGB'), (144, 256))
                preview.image = ImageTk.PhotoImage(art, master=self)
                preview.configure(image=preview.image, text='')
            except OSError: preview.configure(text='Wallpaper unavailable', image='')
        picker.bind('<<ComboboxSelected>>', preview_art); preview_art()
        PhoneButton(body, text='Apply wallpaper', command=lambda: (d.__setitem__('wallpaper', wallpapers[selected.get()]), self.game.persist())).pack(fill='x')
        palette = {'Sea glass': '#80c6ba', 'Gold': '#d5b371', 'Lavender': '#bda3e0', 'Coral': '#edaaa4'}
        choice('Home accent', list(palette), next((k for k,v in palette.items() if v==d['accent']), 'Sea glass'), lambda v: (d.__setitem__('accent', palette[v]), self.game.persist()))
        order = tk.Listbox(body, height=6, exportselection=False)
        for app in dict.fromkeys(d['app_order']+list(phone_icons.COLORS)): order.insert('end', app)
        ttk.Label(body, text='Home app order · select an app, then move it').pack(anchor='w', pady=(16,4)); order.pack(fill='x')
        def move(delta):
            if not order.curselection(): return
            old = order.curselection()[0]; new = max(0, min(order.size()-1, old+delta))
            value = order.get(old); order.delete(old); order.insert(new, value); order.selection_set(new)
            d['app_order'] = list(order.get(0, 'end')); d.pop('home_pages', None); self.game.persist()
        PhoneButton(body, text='Move up', command=lambda: move(-1)).pack(fill='x', pady=2)
        PhoneButton(body, text='Move down', command=lambda: move(1)).pack(fill='x', pady=2)
        def reset():
            if messagebox.askyesno('Reset appearance?', 'Restore this protagonist’s wallpaper, contact names, photos, tones, favourites and app order? Your notes and pinned messages will stay.', parent=self):
                personal.reset(s); self.game.persist(); self.refresh()
        PhoneButton(body, text='Restore protagonist appearance', command=reset).pack(fill='x', pady=12)
