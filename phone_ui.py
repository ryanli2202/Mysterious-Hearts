"""Grove, Supafast and Doober Eats desktop phone views."""
import tkinter as tk
from tkinter import ttk, messagebox
from phone_dialogs import AppWindow, messagebox, simpledialog
import phone_apps as apps
import game_core as core
import grove
import grove_gallery
import grove_gallery_ui
import groups
import town
import winterfield_ui as ui
import suggestions as reply_suggestions
import phone_theme
from phone_icons import AppIcon, COLORS, unread_messages
from messages_ui import MessageBubbles
from phone_controls import PhoneButton, MessageField
import phone_personalization as personal
from phone_personalization_ui import PersonalPhone


class PhoneWindow(PersonalPhone, tk.Toplevel):
    def __init__(self, game, selected='Home'):
        super().__init__(game)
        self._is_phone = True
        self.dialogs = []
        self.game = game
        phone_theme.install(self)
        style=ttk.Style(self)
        style.configure('Phone.TFrame',background='#17171b')
        style.configure('Phone.TLabel',background='#17171b',foreground='#dce4ed')
        for name in ('Phone.TFrame', 'Phone.TLabel'):
            style.map(name, background=[('disabled', '#17171b'), ('active', '#17171b')])
        self.title('Phone · Winterfield')
        personal.ensure(game.state_data)
        self.apply_device_size()
        self.configure(bg='#10121c')
        self.protocol('WM_DELETE_WINDOW', self.close_phone)
        self.bind('<Escape>', lambda e: self.back())
        self.bind('<Alt-Left>', lambda e: self.back())
        self.bind('<Control-h>', lambda e: self.open_app('Home'))
        self.bind('<Control-f>', lambda e: self.open_app('Pinned messages'))
        self.bind('<MouseWheel>', self.scroll_phone)
        self.bind('<Configure>', self.resize_wrapping, add='+')
        self.selected = selected
        self.reply_to = None
        self.draft = ''
        self.restaurant = tk.StringVar(value=next(iter(apps.MENUS)))
        self.recipient = tk.StringVar(value='Yourself')
        self.avatars = MessageBubbles(self, bg='#20202a')
        self.avatars.phone_state = game.state_data
        self.thread = None
        self.closing = False
        self.message_stamp = None
        self.personal_messages = False
        self.arcade_sessions = {}
        self.map_memory = {}
        shell = ui.TextureFrame(self, bg='#101823', padx=8, pady=8)
        shell.pack(fill='both', expand=True)
        self.clock = tk.Label(shell, bg='#08080a', fg='#dce4ed', font=('Segoe UI', 10,'bold'))
        self.clock.configure(text=self.phone_status())
        self.clock.pack(fill='x', pady=(0, 6))
        self.chrome = ttk.Frame(shell, padding=(6, 8))
        self.chrome.pack(fill='x')
        PhoneButton(self.chrome, text='‹', width=3, command=self.back).pack(side='left')
        self.app_title = ttk.Label(self.chrome, text=selected, font=('Segoe UI', 14, 'bold'))
        PhoneButton(self.chrome, text='×', width=3, command=self.close_phone).pack(side='right')
        PhoneButton(self.chrome, text='Lock', command=lambda: self.open_app('Lock')).pack(side='right')
        self.home_button = PhoneButton(self.chrome, text='⌂', width=3, command=lambda: self.open_app('Home'))
        self.home_button.pack(side='right')
        self.app_title.pack(side='left', padx=8, fill='x', expand=True)
        self.screen = ttk.Frame(shell)
        self.screen.pack(fill='both', expand=True)
        home_bar=tk.Canvas(shell,height=22,bg='#08080a',highlightthickness=0,takefocus=True)
        home_bar.pack(fill='x')
        home_bar.bind('<Configure>',lambda e:(home_bar.delete('all'),home_bar.create_line(e.width/2-48,12,e.width/2+48,12,fill='#7891a9',width=5,capstyle='round')))
        home_bar.bind('<Button-1>',lambda e:self.open_app('Home'))
        home_bar.bind('<Return>',lambda e:self.open_app('Home'))
        self.refresh()
        phone_theme.apply_tree(self.chrome)
        self.after(400, self.tick)

    def close_phone(self):
        self.capture_draft()
        self.game.persist()
        self.game.sounds.stop_voicemail()
        if self.game.busy:
            self.closing = True
            self.withdraw()
            self.after(200, self.finish_close)
        else:
            self.destroy()
            self.game.show_in_person()

    def phone_status(self):
        minute=self.game.state_data['world']['minute']%1440
        return f'{minute//60:02}:{minute%60:02}                         Grove  ▰'

    def finish_close(self):
        if not self.closing: return
        if self.game.busy:
            self.after(200, self.finish_close)
        else:
            self.destroy()
            self.game.show_in_person()

    def open_app(self, name):
        for dialog in list(reversed(self.dialogs)): dialog.destroy()
        self.capture_draft()
        self.detail_open = False
        self.selected = name
        self.refresh()

    def open_leadership(self):
        self.open_app('Bubblegram')
        self.job_board.change('Leadership')

    def capture_draft(self):
        number_entry=getattr(self,'contact_number_entry',None)
        if number_entry is not None and number_entry.winfo_exists():
            import phone_numbers
            phone_numbers.ensure(self.game.state_data)['draft']=number_entry.get()
        meet_cute_view = getattr(self, 'meet_cute_view', None)
        if meet_cute_view is not None:
            meet_cute_view.capture()
        lifestyle = getattr(self, 'lifestyle_view', None)
        if lifestyle is not None:
            lifestyle.capture()
        notes = getattr(self, 'notes_editor', None)
        if notes is not None and notes.winfo_exists():
            personal.ensure(self.game.state_data)['notes'] = notes.get('1.0', 'end-1c')
        self.capture_message_draft()
        camera_view = getattr(self, 'camera_view', None)
        if self.selected == 'Camera' and camera_view is not None and camera_view.winfo_exists():
            camera_view.save_preferences()
        entry = getattr(self, 'grove_entry', None)
        if entry is not None and entry.winfo_exists(): self.draft = entry.get()

    def capture_message_draft(self):
        entry = getattr(self, 'message_entry', None)
        if self.selected != 'Conversation' or not self.thread or entry is None or not entry.winfo_exists(): return
        stamp = getattr(self, 'message_draft_key', None)
        if not stamp: return
        self.game.state_data.setdefault('drafts', {})[stamp] = entry.get()
        # The desktop composer shares this draft. Keep it in sync so selecting
        # a thread from Home cannot overwrite the phone draft with stale text.
        desktop = getattr(self.game, 'entry', None)
        if desktop is not None and desktop.winfo_exists() and self.game.draft_key() == stamp:
            mode = desktop.cget('state')
            desktop.configure(state='normal')
            desktop.delete(0, 'end'); desktop.insert(0, entry.get())
            desktop.configure(state=mode)
        bubbles = getattr(self, 'phone_messages', None)
        if bubbles is not None and bubbles.winfo_exists():
            self.game.state_data.setdefault('conversation_scroll', {})[stamp] = bubbles.yview()[0]

    def tick(self):
        self.clock.config(text=self.phone_status())
        if self.selected in ('Mysterious Hearts', 'Mysterious Hearts thread'):
            import mysterious_hearts as hearts
            import hearts_ui
            d = hearts.ensure(self.game.state_data)
            stamp = (sum(len(t['messages']) for t in d['threads']),
                     tuple((p['id'], p.get('error')) for p in d['pending']))
            if stamp != getattr(self, 'hearts_stamp', None):
                self.hearts_stamp = stamp
                if self.selected == 'Mysterious Hearts thread': hearts_ui.thread(self, self.hearts_thread)
                else: self.refresh()
        if self.selected == 'Meet-Cute':
            import meet_cute
            if getattr(self, 'meet_cute_stamp', None) != meet_cute.ensure(self.game.state_data)['revision']:
                self.refresh()
        if self.selected == 'Supafast':
            import supafast
            manager = supafast.jobs(self.game)
            manager.request()
            stamp = (manager.key(), manager.status())
            if stamp != getattr(self, 'supafast_stamp', None): self.refresh()
        if self.selected == 'Conversation': self.update_messages()
        if self.selected == 'Weather' and getattr(self, 'weather_stamp', None) != self.game.state_data['world']['minute']: self.refresh()
        if self.selected == 'Maps': self.update_map_people()
        self.update_notifications()
        if self.selected == 'Lock' and self.unread_stamp() != getattr(self, '_lock_stamp', None):
            self._lock_stamp = self.unread_stamp()
            self.refresh()
        self.after(400, self.tick)

    def update_notifications(self):
        state = self.game.state_data
        import meet_cute
        dating_icon = getattr(self, 'meet_cute_icon', None)
        if dating_icon is not None and dating_icon.winfo_exists():
            dating_icon.set_unread(meet_cute.unread(state))
        import mysterious_hearts
        heart_icon = getattr(self, 'hearts_icon', None)
        if heart_icon is not None and heart_icon.winfo_exists():
            heart_icon.set_unread(mysterious_hearts.unread(state, state['player']))
        unread = unread_messages(state)
        if self.selected in ('Home', 'Lock'):
            if getattr(self, 'home_canvas', None) is not None and self.home_canvas.winfo_exists() and hasattr(self, 'home_unread_item'):
                self.home_canvas.itemconfigure(self.home_unread_item, text=f'{unread} unread messages' if unread else '')
            grove_icon = getattr(self, 'grove_icon', None)
            if grove_icon is not None and grove_icon.winfo_exists():
                grove_icon.set_unread(len(grove_gallery.unread_comments(state)))
            icon = getattr(self, 'messages_icon', None)
            if icon is not None and icon.winfo_exists():
                icon.set_unread(unread)
            label = getattr(self, 'unread_label', None)
            if label is not None and label.winfo_exists():
                label.config(text=f'{unread} unread messages' if unread else '')
        elif self.selected == 'Messages':
            stamp = self.unread_stamp()
            if stamp != getattr(self, '_inbox_unread_stamp', None):
                self.refresh()
        self.game.update_phone_notification()

    def unread_stamp(self):
        state = self.game.state_data
        return (state['world']['minute']//1440, tuple((k, r.get('unread', 0), r.get('inbox_activity', {}).get('order', 0)) for k, r in state['routes'].items()),
                tuple((k, g.get('unread', 0), g.get('inbox_activity', {}).get('order', 0)) for k, g in state['groups'].items() if g.get('channel') == 'text'))

    def is_reading_thread(self, key, is_group=False):
        return (self.selected == 'Conversation' and self.thread == (key, is_group)
                and not self.closing and self.state() in ('normal', 'zoomed')
                and bool(self.winfo_viewable()))

    def act(self, fn, *args):
        if self.game.busy:
            messagebox.showinfo('Phone', 'Wait for the current conversation to finish.', parent=self)
            return
        try:
            fn(self.game.state_data, *args)
        except ValueError as exc:
            messagebox.showinfo('Phone', str(exc), parent=self)
            return
        self.reply_to = None
        if fn is apps.post:
            self.draft = ''
            self.grove_entry.delete(0, 'end')
        self.game.persist()
        self.game.render()
        self.refresh()

    def refresh(self):
        self.game.sounds.stop_voicemail()
        self.clock.config(text=self.phone_status())
        self.capture_draft()
        if self.selected in ('Home','Lock','Conversation'):
            self.chrome.pack_forget()
        elif not self.chrome.winfo_manager():
            self.chrome.pack(fill='x',before=self.screen)
        for child in self.screen.winfo_children():
            if child not in [d.shell for d in self.dialogs]: child.destroy()
        s = self.game.state_data
        apps.sync(s)
        import phone_numbers
        phone_numbers.ensure(s)
        self.game.persist()
        self.app_title.config(text={'Conversation': 'Messages', 'Pinned messages': 'Pins & search'}.get(self.selected, self.selected))
        frame = ttk.Frame(self.screen, padding=14)
        frame.pack(fill='both', expand=True)
        views = {'Home': self.home_screen, 'Grove': self.grove, 'Deliveries': self.deliveries,
                 'Messages': self.inbox, 'Conversation': self.conversation,
                 'Contacts': self.contacts_page, 'Maps': self.maps_page,
                 'Calendar': self.calendar_page, 'Journal': self.journal_page,
                 'Settings': self.settings_page, 'More': self.more_page,
                 'Mini Games': self.mini_games_page, 'Weather': self.weather_page, 'Winterfield': self.living_page,
                 'Camera': self.camera_page, 'Gallery': self.photos_page,
                 'Mysterious Hearts': self.hearts_page, 'Notes': self.notes_page,
                 'Pinned messages': self.message_library, 'Customise': self.customization_page, 'Lock': self.lock_page,
                 'Keepsake': self.keepsake_page}
        import job_apps_ui
        views.update({'Jobseek': lambda frame, state: job_apps_ui.show(self, frame),
                      'Bubblegram': lambda frame, state: job_apps_ui.show(self, frame, True)})
        import phone_app_design as design
        utility_links = {
            'Contacts': [('Messages', 'Messages'), ('People', 'Contacts')],
            'Calendar': [('Today', 'Calendar'), ('Activities', 'Out & About')],
            'Journal': [('Entries', 'Journal'), ('Notes', 'Notes')],
            'Notes': [('Notes', 'Notes'), ('Journal', 'Journal')],
            'Deliveries': [('Orders', 'Deliveries'), ('Shop', 'Supafast')],
            'Settings': [('Settings', 'Settings'), ('Appearance', 'Customise')],
            'More': [('Apps', 'More'), ('Settings', 'Settings')],
        }
        if self.selected in utility_links:
            design.navigation(frame, [(label, lambda target=target: self.open_app(target))
                                      for label, target in utility_links[self.selected]] +
                                     [('Home', lambda: self.open_app('Home'))])
        import lifestyle_apps
        if self.selected == 'Meet-Cute':
            from meet_cute_ui import MeetCuteScreen
            MeetCuteScreen(self, frame, s)
        elif self.selected in lifestyle_apps.NAMES:
            from lifestyle_ui import Screen
            Screen(self, frame, s)
        elif self.selected in views: views[self.selected](frame, s)
        else: self.store(frame, s, self.selected)
        for dialog in self.dialogs: dialog.shell.lift()
        self.after_idle(lambda: self.fit_wrapping(frame) if frame.winfo_exists() else None)

    def resize_wrapping(self, event):
        if event.widget is self and hasattr(self,'screen'):
            self.app_title.configure(wraplength=max(80, self.winfo_width()-210))
            self.after_idle(lambda: self.fit_wrapping(self.screen) if self.winfo_exists() else None)

    def fit_wrapping(self, widget):
        if isinstance(widget,ttk.Frame) and not str(widget.cget('style')).startswith(('Arcade.', 'PhoneDark.')):
            widget.configure(style='Phone.TFrame')
        elif isinstance(widget,ttk.Label) and not str(widget.cget('style')).startswith(('Arcade.', 'PhoneDark.')):
            widget.configure(style='Phone.TLabel')
        phone_theme.apply_widget(widget)
        # A newly opened toplevel can still be one pixel wide on its first idle.
        # Preserve authored wrapping until the window has its actual geometry.
        if self.winfo_width()<=100: return
        for child in widget.winfo_children():
            if isinstance(child, (ttk.Label, tk.Label, tk.Button)):
                try: child.configure(wraplength=getattr(child, '_fixed_wraplength', max(80, self.winfo_width()-100)))
                except tk.TclError: pass
            self.fit_wrapping(child)

    def hearts_page(self, frame, s):
        import hearts_ui
        hearts_ui.page(self, frame, s)

    def camera_page(self, frame, s):
        from camera_ui import CameraView
        self.camera_view = CameraView(self, self.scroll_area(frame), s)

    def photos_page(self, frame, s):
        from camera_ui import GalleryView
        PhoneButton(frame, text='Earlier saved image', command=lambda: self.open_app('Keepsake')).pack(fill='x', pady=4)
        GalleryView(self, frame, s)

    def weather_page(self, frame, s):
        from weather_ui import WeatherView
        self.weather_stamp = s['world']['minute']
        WeatherView(frame, s)

    def living_page(self, frame, s):
        import living_world_ui
        living_world_ui.show(self, frame, s)

    def mini_games_page(self, frame, s):
        from mini_games_ui import Arcade
        Arcade(frame, self.arcade_sessions, self.game.sounds)

    def refresh_feed(self):
        if self.selected in ('Home', 'Grove'): self.refresh()

    def retry_grove(self):
        pump = getattr(self.game, 'grove_pump', None)
        if pump: pump.retry()
        self.refresh()

    def home_screen(self, frame, s):
        self.personal_home(frame, s)

    def inbox(self, frame, s):
        from phone_chat import inbox
        inbox(self, frame, s)

    def open_thread(self, key, group=False):
        self.capture_message_draft()
        members = self.game.state_data['groups'][key]['members'] if group else [key]
        try: groups.require_text_available(self.game.state_data, members)
        except ValueError as exc:
            messagebox.showinfo('Messages', str(exc), parent=self); return
        if self.game.busy:
            active = self.game.group_selected if group else self.game.state_data['active']
            same_thread = active == key and bool(self.game.group_selected) == group
            if not same_thread:
                messagebox.showinfo('Messages', 'Another conversation is still being written. You can reopen that chat while you wait.', parent=self)
                return
            # Viewing an in-flight thread must not reset its pending text or token.
            self.thread = (key, group)
            self.open_app('Conversation')
            return
        self.thread = (key, group)
        self.personal_messages = False
        if group: self.game.select_group(key)
        else: self.game.select(key)
        self.open_app('Conversation')

    def conversation(self, frame, s):
        from phone_chat import build
        build(self, frame, s)

    def toggle_emoji_keyboard(self):
        self.emoji_keyboard_visible = not self.emoji_keyboard_visible
        if self.emoji_keyboard_visible:
            self.suggestion_actions.pack_forget()
            self.emoji_keyboard.pack(fill='x')
        else:
            self.emoji_keyboard.pack_forget()
            self.suggestion_actions.pack(fill='x', pady=4)
            self.message_entry.focus_set()
        self.message_emoji.config(text='ABC' if self.emoji_keyboard_visible else '☺',
                                  style='Accent.TButton' if self.emoji_keyboard_visible else '')
        self.apply_message_suggestions_visibility()

    def apply_message_suggestions_visibility(self):
        visible = self.game.state_data.get('ui_preferences', {}).get('show_suggested_replies', True)
        self.suggestions_toggle.config(text='Hide suggested replies ▴' if visible else 'Show suggested replies ▾')
        if visible and not getattr(self, 'emoji_keyboard_visible', False):
            self.suggestions_panel.pack(fill='x', after=self.suggestion_actions)
        else:
            self.suggestions_panel.pack_forget()

    def toggle_message_suggestions(self):
        preferences = self.game.state_data.setdefault('ui_preferences', {})
        preferences['show_suggested_replies'] = not preferences.get('show_suggested_replies', True)
        self.apply_message_suggestions_visibility()
        self.game.persist()

    def update_messages(self):
        if not self.thread or not hasattr(self, 'phone_messages') or not self.phone_messages.winfo_exists(): return
        from messages_ui import text_messages
        s = self.game.state_data
        key, is_group = self.thread
        group = s['groups'].get(key) if is_group else None
        # Opening another chat through an auxiliary control returns to the inbox.
        if (is_group and self.game.group_selected != key) or (not is_group and (s['active'] != key or self.game.group_selected)):
            self.open_app('Messages'); return
        chat = group if group is not None else s['routes'][key]
        if chat.get('unread', 0) and self.is_reading_thread(key, is_group):
            chat['unread'] = 0
            self.game.persist()
            self.game.update_phone_notification()
        messages = text_messages(s, self.game.pending, group)
        if not is_group:
            earlier = [('', m['text'], 'in', key) for m in personal.ensure(s)['archived_messages'] if m['who'] == key]
            if earlier: messages = [('', 'Earlier · before this story', 'status', None)] + earlier + [('', 'Current conversation', 'status', None)] + messages
        else:
            messages = [(personal.name(s, m[3]) if len(m)>3 and m[3] and m[2]=='in' else m[0], *m[1:]) for m in messages]
        typing = self.game.message_pump.typing(key, is_group) if hasattr(self.game, 'message_pump') else False
        caption = ('Someone is typing…' if group else personal.name(s, key) + ' is typing…') if typing else None
        if not personal.preferences()['typing_indicator']: caption = None
        from phone_chat import bind_records
        stamp = (messages, caption, tuple(personal.ensure(s)['pins']))
        if stamp != self.message_stamp:
            bind_records(self, messages)
            self.phone_messages.set_messages(messages, typing_caption=caption,
                                             typing_character=None if group else key)
            self.message_stamp = stamp
        chat = group or s['routes'][key]
        choices = reply_suggestions.visible(chat, 'personal' if self.personal_messages else 'main')
        self.visible_message_choices = choices
        blocked = bool(groups.hanging_out_with(s).intersection(group['members'] if group else [key]))
        busy = self.game.busy or blocked
        self.personal_suggestions.config(style='Accent.TButton' if self.personal_messages else 'TButton')
        self.regular_suggestions.config(style='TButton' if self.personal_messages else 'Accent.TButton')
        for index, button in enumerate(self.message_choices):
            if choices and not button.winfo_manager(): button.pack(fill='x', pady=2)
            elif not choices: button.pack_forget()
            prefix = core.PERSONAL_TONES[index] + ' · ' if self.personal_messages else ''
            button.config(text=prefix + choices[index] if index < len(choices) else '…',
                          state='normal' if index < len(choices) and not busy else 'disabled')
        import messaging
        t = messaging.thread(s, key, is_group)
        if hasattr(self,'availability_label') and self.availability_label.winfo_exists():
            statuses=[messaging.activity(s,w) for w in (group['members'] if is_group else [key])]
            self.availability_label.config(text='Availability · '+', '.join(dict.fromkeys(statuses)))
        delivery='Texts take no game time · Wait or continue your day for replies'
        if typing:
            import time
            elapsed=max(0,int(time.monotonic()-self.game.message_pump.started))
            delivery=f'Writing reply · {elapsed}s · You can message other chats'
        elif t.get('prepared'): delivery='Reply prepared · waiting for the sender to be available'
        elif t['pending'] and any(m['read_by'] for m in t['pending']): delivery='Read · reply queued or waiting for availability'
        self.message_status.config(text='You are hanging out together. Talk in person.' if blocked else t['error'] or delivery)
        photo_jobs=[p for p in s.get('message_photos',{}).get('pending',[]) if p['author']==key] if not is_group else []
        self.incoming_photo_status.config(text=next((p['error'] for p in photo_jobs if p.get('error')), 'A photo is developing…' if photo_jobs else ''))
        self.cancel_response.config(state='normal' if typing or t['pending'] or t['reason'] else 'disabled')
        self.response_preview.config(text=('Incoming response preview · '+self.game.preview_dialogue) if self.game.busy and self.game.preview_dialogue else '')
        self.message_send.config(state='disabled' if busy or not (self.message_entry.get().strip() or s.get('photo_drafts', {}).get(self.message_draft_key)) else 'normal')
        photo_id = s.get('photo_drafts', {}).get(self.message_draft_key)
        self.photo_attachment.config(text='Photo attached · Remove' if photo_id else '', state='normal' if photo_id else 'disabled')
        self.message_retry.config(state='disabled' if busy else 'normal')
        available = not busy and reply_suggestions.ready(s, ('group' if is_group else 'route', key))
        self.suggest_replies.config(text='Cancel suggestions' if self.game.suggestion_job else 'Suggest personal replies' if self.personal_messages else 'Suggest replies',
                                   state='normal' if available else 'disabled')
        if self.game.suggestion_status and self.game.suggestion_status_target == ('group' if is_group else 'route',key) and not busy:
            self.message_status.config(text=self.game.suggestion_status)

    def set_message_mode(self, personal):
        self.personal_messages = personal
        self.update_messages()

    def save_emoji_draft(self):
        self.capture_message_draft()
        self.update_messages()
        if self.game.draft_key() == self.message_draft_key:
            state = self.game.entry.cget('state')
            self.game.entry.configure(state='normal')
            self.game.restore_draft()
            self.game.entry.configure(state=state)
        self.game.persist()

    def clear_message(self):
        self.message_entry.delete(0, 'end')
        self.game.state_data.setdefault('photo_drafts', {}).pop(self.message_draft_key, None)
        self.game.state_data.setdefault('drafts', {}).pop(self.message_draft_key, None)
        if self.game.draft_key() == self.message_draft_key:
            self.game.restore_draft()
        self.game.persist()
        self.message_entry.focus_set()

    def send_message(self, choice=None):
        if self.game.busy: return
        if choice is None:
            text = self.message_entry.get().strip()
            photo_id = self.game.state_data.get('photo_drafts', {}).get(self.message_draft_key)
            if not text and not photo_id: return
            preview = text + ('\n[Attached photo]' if photo_id else '')
            if personal.preferences()['confirm_send'] and not messagebox.askyesno('Send reply?', preview, parent=self): return
            self.game.submit(text, photo_id=photo_id)
        elif choice < len(self.visible_message_choices):
            text = self.visible_message_choices[choice]
            if personal.preferences()['confirm_send'] and not messagebox.askyesno('Send reply?', text, parent=self): return
            self.game.submit(text)
        self.update_messages()

    def contacts_page(self, frame, s):
        ttk.Label(frame, text='Contacts', font=('Segoe UI', 24, 'bold')).pack(anchor='w')
        import phone_numbers, phone_numbers_ui
        phone_numbers_ui.add_form(self,frame,s)
        body = self.scroll_area(frame)
        for who in [s['player'], *apps.contacts(s)]:
            card = ttk.Frame(body, padding=12); card.pack(fill='x', pady=4)
            avatar = self.avatars._avatar(who)
            if avatar: ttk.Label(card, image=avatar).pack(anchor='w')
            ttk.Label(card, text=personal.name(s, who), font=('Segoe UI', 13, 'bold')).pack(anchor='w')
            ttk.Label(card, text=phone_numbers.number(s,who)).pack(anchor='w',pady=3)
            ttk.Label(card, text=apps.handle(who, self.game.state_data), foreground='#88cbb0').pack(anchor='w')
            ttk.Label(card, text=grove.profile(self.game.state_data, who)['bio'], wraplength=490).pack(anchor='w', pady=4)
            self.voicemail_controls(card, who)
            self.contact_custom_controls(card, s, who)
            if who != s['player']:
                ttk.Label(card, text=core.social_world.status_line(s, who)).pack(anchor='w')
                PhoneButton(card, text='Hanging out with you' if who in groups.hanging_out_with(s) else 'Message',
                           state='disabled' if who in groups.hanging_out_with(s) else 'normal',
                           command=lambda who=who: self.open_thread(who)).pack(fill='x', pady=5)
                PhoneButton(card, text='Command site only' if who in ('crow','takeo','thirteen') else 'Summon here', state='disabled' if who in ('crow','takeo','thirteen') else 'normal', command=lambda who=who: self.act(town.summon, who)).pack(fill='x', pady=5)
            PhoneButton(card, text='Full profile & shared history', command=lambda who=who: self.contact_detail(who)).pack(fill='x', pady=5)
        phone_numbers_ui.local_contacts(self,body,s)

    def voicemail_controls(self, parent, who):
        row = ttk.Frame(parent)
        row.pack(fill='x', pady=6)
        sounds = self.game.sounds
        if not sounds.voicemail_path(who):
            ttk.Label(row, text='Voicemail · No recording yet', foreground='#999999').pack(anchor='w')
            return
        status = ttk.Label(row, text='Voicemail greeting')
        timer = [None]
        row.bind('<Destroy>', lambda event: row.after_cancel(timer[0])
                 if event.widget is row and timer[0] else None)

        def update():
            if not row.winfo_exists():
                return
            playing = sounds.voicemail_playing(who)
            status.config(text='Playing voicemail…' if playing else 'Voicemail greeting')
            stop.config(state='normal' if playing else 'disabled')
            timer[0] = row.after(400, update)

        def play():
            try:
                sounds.play_voicemail(who)
            except ValueError as exc:
                messagebox.showinfo('Voicemail', str(exc), parent=self)
                return
            status.config(text='Playing voicemail…')
            stop.config(state='normal')

        def halt():
            if sounds.voicemail_playing(who):
                sounds.stop_voicemail()
            status.config(text='Voicemail greeting')
            stop.config(state='disabled')

        PhoneButton(row, text='▶ Listen to voicemail', command=play).pack(side='left')
        stop = PhoneButton(row, text='Stop', command=halt, state='disabled')
        stop.pack(side='left', padx=6)
        status.pack(side='left', padx=4)
        update()

    def contact_detail(self, who):
        self.detail_open = True
        self.game.sounds.stop_voicemail()
        for child in self.screen.winfo_children():
            if child not in [d.shell for d in self.dialogs]: child.destroy()
        frame = ttk.Frame(self.screen, padding=14); frame.pack(fill='both', expand=True)
        PhoneButton(frame, text='‹ Contacts', command=lambda: self.open_app('Contacts')).pack(anchor='w')
        body = self.scroll_area(frame)
        s = self.game.state_data
        import contact_profiles
        outfit = contact_profiles.public(s, who, s['player']).get('Profile picture') or 'selection'
        if who in ('fox','gordon') and outfit in ('selection','contact'):
            from PIL import Image, ImageOps, ImageTk
            with Image.open(personal.ROOT / 'assets' / 'portraits' / (who+'-contact.png')) as source:
                photo=ImageTk.PhotoImage(ImageOps.fit(source.convert('RGB'),(130,130)),master=body)
            self.interpol_contact_photo=photo
        elif who == 'charles' and outfit == 'selection':
            from PIL import Image, ImageOps, ImageTk
            with Image.open(personal.ROOT / 'assets' / 'profiles' / 'charles-contact-v3.png') as source:
                photo = ImageTk.PhotoImage(ImageOps.fit(source.convert('RGB'), (130, 130)), master=self)
            self.charles_contact_photo = photo
        else:
            photo = self.game.portrait(who, (130, 155), outfit=outfit)
        ttk.Label(body, image=photo).pack(anchor='w', pady=12)
        ttk.Label(body, text=personal.name(s, who), font=('Segoe UI', 21, 'bold')).pack(anchor='w')
        ttk.Label(body, text='Major character', style='Muted.TLabel').pack(anchor='w')
        import phone_numbers
        ttk.Label(body, text=(phone_numbers.saved_number(s,who) or ('Private number · not shared with you' if who == 'charles' else 'Number not saved'))).pack(anchor='w',pady=4)
        ttk.Label(body, text=apps.handle(who, self.game.state_data), foreground='#88cbb0').pack(anchor='w', pady=4)
        orientation=contact_profiles.public(s,who,s['player']).get('Sexuality')
        if orientation:
            ttk.Label(body,text='Sexuality · '+orientation,font=('Segoe UI',11,'bold')).pack(anchor='w',pady=4)
        ttk.Label(body, text=grove.profile(self.game.state_data, who)['bio'], wraplength=490).pack(anchor='w', pady=8)
        self.voicemail_controls(body, who)
        if who != s['player'] and personal.ensure(s).get('relationship_meters', True):
            from relationship_ui import RelationshipBars
            bars = RelationshipBars(body, bg=ui.PANEL)
            bars.pack(fill='x', pady=8)
            bars.update_stats(town.character_stats(s, who), romanceable=town.romanceable(s, who))
        import hearts_ui
        hearts_ui.contact(self, body, s, who)
        facts = core.social_world.demographics(who)
        ttk.Label(body, text=' · '.join(f'{key}: {value}' for key, value in facts.items() if key!='Sexuality'), wraplength=490).pack(anchor='w', pady=8)
        if who != s['player']:
            ttk.Label(body, text=core.social_world.status_line(s, who)).pack(anchor='w')
            PhoneButton(body, text='Hanging out with you' if who in groups.hanging_out_with(s) else 'Send a message',
                       state='disabled' if who in groups.hanging_out_with(s) else 'normal',
                       command=lambda: self.open_thread(who)).pack(anchor='w', pady=8)
            if who in ('crow', 'takeo', 'thirteen'):
                headquarters = 'Shinokami depot command' if who == 'thirteen' else 'Shinokami' if who == 'takeo' else 'Syndicate'
                ttk.Label(body, text='Meet at Pacific Relay Depot briefing room.' if who == 'thirteen' else 'Meet only at '+headquarters+' headquarters.').pack(anchor='w', pady=4)
            else:
                PhoneButton(body, text='Summon to my location', command=lambda: self.act(town.summon, who)).pack(anchor='w', pady=4)
        ttk.Label(body, text='Shared history', font=('Segoe UI', 14, 'bold')).pack(anchor='w', pady=(14, 6))
        notes = core.social_world.initial_notes(s, who)
        for note in notes: ttk.Label(body, text=note, wraplength=490).pack(anchor='w', pady=5)
        for note in s.get('profile_notes', {}).get(who, []):
            ttk.Label(body, text=f"{personal.name(s, note['source'])}: {note['quote']}", wraplength=490).pack(anchor='w', pady=5)
        if not notes and not s.get('profile_notes', {}).get(who):
            ttk.Label(body, text='Details you learn together will appear here.').pack(anchor='w')
        PhoneButton(body, text='Portraits & detailed relationship stats', command=lambda: self.game.open_profiles(who)).pack(anchor='w', pady=15)
        def fit_contact(event):
            for child in body.winfo_children():
                if isinstance(child,ttk.Label) and child.cget('text'):
                    child.configure(wraplength=max(100,event.width-10),justify='left')
                    child.pack_configure(fill='x')
        body.bind('<Configure>',fit_contact,add='+')
        # Contact details bypass open_app's idle traversal. Theme even hidden
        # or not-yet-mapped children before they can expose native state colours.
        phone_theme.apply_tree(frame)

    def maps_page(self, frame, s):
        from phone_map import MapView
        self.map_view = MapView(frame, self)

    def update_map_people(self):
        view = getattr(self, 'map_view', None)
        if view is not None and view.winfo_exists():
            view.sync()

    def calendar_page(self, frame, s):
        import syndicate_council
        syndicate_council.ensure(s)
        import scheduled_events
        import calendar
        from datetime import timedelta
        dates = town.loop.dates
        today = dates.story_date(s['world']['minute'])
        day = getattr(self, 'calendar_day', today)
        horizon = max(day.replace(day=28)+timedelta(days=4), today+timedelta(days=91))
        syndicate_council.ensure(s, (horizon-dates.START).days*1440)
        ttk.Label(frame, text='Calendar', font=('Segoe UI', 24, 'bold')).pack(anchor='w')
        nav = ttk.Frame(frame); nav.pack(fill='x', pady=12)
        def show(when):
            self.calendar_day = when
            self.refresh()
        PhoneButton(nav, text='‹', width=3, command=lambda: show(day.replace(day=1)-timedelta(days=1))).pack(side='left')
        ttk.Label(nav, text=f'{day:%B %Y}', font=('Segoe UI', 15, 'bold')).pack(side='left', padx=15)
        PhoneButton(nav, text='›', width=3, command=lambda: show(day.replace(day=28)+timedelta(days=4))).pack(side='left')
        PhoneButton(nav, text='Today', command=lambda: show(today)).pack(side='right')
        month = ttk.Frame(frame); month.pack(fill='x', pady=8)
        for col, name in enumerate(('M', 'T', 'W', 'T', 'F', 'S', 'S')):
            month.columnconfigure(col, weight=1)
            ttk.Label(month, text=name, anchor='center').grid(row=0, column=col, sticky='ew')
        for row, week in enumerate(calendar.monthcalendar(day.year, day.month), 1):
            for col, number in enumerate(week):
                if not number: continue
                when = day.replace(day=number)
                import crime_diplomacy
                planned = any(not e.get('cancelled') and dates.story_date(e['start']) == when for e in s.get('scheduled_events', [])) or any(dates.story_date(e['start'])==when for e in crime_diplomacy.commitments(s))
                label = str(number) + (' •' if dates.events(s, when) or planned else '')
                tk.Button(month, text=label, relief='flat', bg='#88cbb0' if when == day else '#222638',
                          fg='#10121c' if when == day else '#f3eee7', pady=8,
                          command=lambda when=when: show(when)).grid(row=row, column=col, sticky='ew', padx=2, pady=2)
        ttk.Label(frame, text=f'{day:%A, %d %B}', font=('Segoe UI', 12, 'bold')).pack(anchor='w', pady=6)
        for title, _, _ in dates.events(s, day): ttk.Label(frame, text=title, wraplength=490).pack(anchor='w', pady=3)
        for event in s.get('scheduled_events', []):
            if not event.get('cancelled') and dates.story_date(event['start']) == day:
                ttk.Label(frame, text=scheduled_events.describe(event), wraplength=490).pack(anchor='w', pady=3)
        import crime_diplomacy
        for event in crime_diplomacy.commitments(s):
            if dates.story_date(event['start'])==day:
                ttk.Label(frame,text=f'{event["start"]%1440//60:02}:{event["start"]%60:02} · Private leadership appointment',wraplength=280).pack(anchor='w')
                PhoneButton(frame,text='Open private leadership desk',command=self.open_leadership).pack(fill='x')
        if not dates.events(s, day): ttk.Label(frame, text='No special occasions today.').pack(anchor='w')
        PhoneButton(frame, text='Plan an outing / event activities', command=lambda:self.game.open_calendar(day)).pack(anchor='w', pady=8)
        body = self.scroll_area(frame)
        ttk.Label(body, text='Coming up', font=('Segoe UI', 13, 'bold')).pack(anchor='w', pady=8)
        for offset in range(91):
            day = today + timedelta(days=offset)
            events = dates.events(s, day)
            planned = [e for e in s.get('scheduled_events', []) if not e.get('cancelled') and e['end']>s['world']['minute'] and dates.story_date(e['start'])==day]
            if not events and not planned: continue
            ttk.Label(body, text=f'{day:%a, %b %d}', font=('Segoe UI', 12, 'bold')).pack(anchor='w', pady=(12, 3))
            for title, _, _ in events: ttk.Label(body, text=title, wraplength=490).pack(anchor='w', pady=3)
            for event in planned:
                ttk.Label(body,text=scheduled_events.describe(event),wraplength=270).pack(anchor='w',pady=3)
                PhoneButton(body,text='View meeting / event',command=lambda when=day:self.game.open_calendar(when)).pack(anchor='w')

    def journal_page(self, frame, s):
        ttk.Label(frame, text='Hangout journal', font=('Segoe UI', 24, 'bold')).pack(anchor='w')
        ttk.Label(frame, text='People, places and conversations from time spent together.', wraplength=510).pack(anchor='w', pady=8)
        body = self.scroll_area(frame)
        entries = s.get('hangout_journal', [])
        if not entries: ttk.Label(body, text='Completed hangouts will appear here.').pack(anchor='w', pady=12)
        for entry in reversed(entries):
            card = ttk.Frame(body, padding=12); card.pack(fill='x', pady=5)
            start = entry.get('started')
            stamp = f"{town.loop.dates.story_date(start):%b %d} · {start%1440//60:02}:{start%60:02}" if start is not None else 'Earlier hangout'
            ttk.Label(card, text=stamp, foreground='#88cbb0').pack(anchor='w')
            ttk.Label(card, text=', '.join(personal.name(s, m) for m in entry['members']), font=('Segoe UI', 12, 'bold'), wraplength=490).pack(anchor='w')
            ttk.Label(card, text=town.LOCATIONS.get(entry['location'], entry['location']), wraplength=490).pack(anchor='w', pady=4)
            PhoneButton(card, text='Read hangout', command=lambda entry=entry: self.read_journal(entry)).pack(anchor='w')
        # Old saves still have their original spoken threads even before dated entries existed.
        for group in s['groups'].values():
            if group.get('channel') != 'text' and group.get('history') and group.get('journal_started') is None:
                entry = dict(members=group['members'], location=group.get('location', ''), history=group['history'])
                PhoneButton(body, text='Earlier conversation · ' + ', '.join(personal.name(s, m) for m in group['members']),
                           command=lambda entry=entry: self.read_journal(entry)).pack(fill='x', pady=4)

    def read_journal(self, entry):
        self.capture_draft()
        for child in self.screen.winfo_children():
            if child not in [d.shell for d in self.dialogs]: child.destroy()
        frame = ttk.Frame(self.screen, padding=14); frame.pack(fill='both', expand=True)
        PhoneButton(frame, text='‹ Journal', command=lambda: self.open_app('Journal')).pack(anchor='w')
        body = self.scroll_area(frame)
        for line in entry['history']:
            ttk.Label(body, text=line.get('speaker', ''), font=('Segoe UI', 10, 'bold')).pack(anchor='w', pady=(10, 0))
            ttk.Label(body, text=line.get('text', ''), wraplength=490).pack(anchor='w')

    def settings_page(self, frame, s):
        frame = self.scroll_area(frame)
        PhoneButton(frame, text='Personalise phone & controls', command=lambda: self.open_app('Customise')).pack(fill='x', pady=8)
        def toggle_changes():
            s['show_relationship_changes'] = changes.get(); self.game.persist()
        changes = tk.BooleanVar(value=s.get('show_relationship_changes', True))
        ttk.Checkbutton(frame, text='Show relationship changes', variable=changes, command=toggle_changes).pack(anchor='w', pady=8)
        ttk.Label(frame, text='Settings', font=('Segoe UI', 24, 'bold')).pack(anchor='w')
        ttk.Label(frame, text=f"Signed in as {core.PLAYERS[s['player']]}\nBalance: ${s['world']['money']:,}").pack(anchor='w', pady=12)
        PhoneButton(frame, text='AI & account', command=self.game.accounts).pack(fill='x', pady=5)
        self.game.sound_button(frame).pack(fill='x', pady=5)
        self.game.wardrobe_menu(frame).pack(fill='x', pady=5)
        PhoneButton(frame, text='Rename a contact', command=self.game.rename_contact).pack(fill='x', pady=5)
        PhoneButton(frame, text='Save game', command=self.game.persist).pack(fill='x', pady=5)
        ttk.Label(frame, text='Close the phone to return to your current hangout or explore where you are.', wraplength=490).pack(anchor='w', pady=18)

    def more_page(self, frame, s):
        ttk.Label(frame, text='More apps', font=('Segoe UI', 24, 'bold')).pack(anchor='w', pady=12)
        for label, command in [('Photo gallery', self.game.gallery_window), ('Relationships & town guide', self.game.town_window),
                               ('Conversation notebook', self.game.journal)]:
            PhoneButton(frame, text=label, command=command).pack(fill='x', pady=8)
        if s['player'] == 'garrett': PhoneButton(frame, text='Find Charles', command=self.game.charles_search).pack(fill='x', pady=8)

    def grove_profiles(self):
        window = AppWindow(self)
        window.title('Grove profiles')
        window.geometry('650x550')
        body = self.scroll_area(window)
        for who in [self.game.state_data['player'], *apps.contacts(self.game.state_data)]:
            card = ttk.Frame(body, padding=12)
            card.pack(fill='x')
            avatar = self.avatars._avatar(who)
            if avatar: ttk.Label(card, image=avatar).pack(side='left', padx=10)
            text = ttk.Frame(card); text.pack(fill='x')
            ttk.Label(text, text=f'{core.CONTACTS[who][0]} · {apps.handle(who, self.game.state_data)}', font=('Segoe UI', 10, 'bold')).pack(anchor='w')
            ttk.Label(text, text=grove.profile(self.game.state_data, who)['bio'], wraplength=460).pack(anchor='w')
            ttk.Label(text, text=f"{grove.profile(self.game.state_data, who)['followers']:,} followers").pack(anchor='w')
            count = len(grove_gallery.photos(self.game.state_data, who))
            PhoneButton(text, text=f'View profile gallery · {count} photos',
                       command=lambda who=who: grove_gallery_ui.show_profile(self, who)).pack(anchor='w', pady=6)

    def scroll_area(self, parent):
        canvas = tk.Canvas(parent, bg=ui.PANEL, width=1, height=1, highlightthickness=0, borderwidth=0)
        scroll = ttk.Scrollbar(parent, command=canvas.yview)
        scroll.pack(side='right', fill='y')
        canvas.pack(fill='both', expand=True)
        canvas.configure(yscrollcommand=scroll.set)
        body = ttk.Frame(canvas)
        window = canvas.create_window(0, 0, window=body, anchor='nw')
        body.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        canvas.bind('<Configure>', lambda e: canvas.itemconfigure(window, width=e.width))
        canvas.bind('<MouseWheel>', lambda e: canvas.yview_scroll(-int(e.delta/120), 'units'))
        return body

    def grove(self, frame, s):
        ttk.Label(frame, text='Grove', font=('Segoe UI', 24, 'bold')).pack(anchor='w')
        if s['player']=='fox':
            ttk.Label(frame,text='Edward Fox has no Grove account.',wraplength=270).pack(fill='x',pady=12)
            ttk.Label(frame,text='Use Messages for private contacts and Bubblegram for Interpol records.',wraplength=270).pack(fill='x')
            return
        import grove_accounts, grove_account_ui
        if grove_accounts.needed(s) and grove_accounts.account(s) is None:
            self.grove_account_form = grove_account_ui.form(self, self.scroll_area(frame), s)
            return
        notifications = grove_gallery.unread_comments(s)
        if notifications:
            PhoneButton(frame, text=f'{len(notifications)} new comments & replies · Notifications',
                        command=lambda: grove_gallery_ui.show_notifications(self)).pack(anchor='w', pady=4)
        ttk.Label(frame, text=f'{apps.handle(s["player"], self.game.state_data)} · Posts and replies · 280 characters').pack(anchor='w')
        ttk.Label(frame, text=grove.profile(s, s['player'])['bio'], wraplength=700).pack(anchor='w')
        grove_account_ui.stats(frame, s)
        if grove_accounts.needed(s):
            PhoneButton(frame, text='Edit Grove account', command=lambda: grove_account_ui.edit(self)).pack(anchor='w', pady=4)
        PhoneButton(frame, text='Grove profiles & bios', command=self.grove_profiles).pack(anchor='w')
        PhoneButton(frame, text='My photo gallery',
                   command=lambda: grove_gallery_ui.show_profile(self, s['player'])).pack(anchor='w', pady=4)
        PhoneButton(frame, text='Post photo from Gallery',
                    command=lambda: grove_gallery_ui.compose(self)).pack(anchor='w', pady=4)
        pump = getattr(self.game, 'grove_pump', None)
        pending = apps.ensure(s)['grove_pending']
        status = pump.error if pump and pump.error else ('Characters are composing new posts…' if pending else 'All caught up. Characters post as game time passes.')
        ttk.Label(frame, text=status, wraplength=700).pack(anchor='w', pady=4)
        if pump and pump.error:
            PhoneButton(frame, text='Retry Grove', command=self.retry_grove).pack(anchor='w')
        photos = getattr(pump, 'photos', None)
        if photos and photos.error:
            ttk.Label(frame, text=photos.error, wraplength=540).pack(anchor='w')
            PhoneButton(frame, text='Retry character photos', command=self.retry_grove).pack(anchor='w')
        elif photos and photos.cancel:
            ttk.Label(frame, text='A contact is developing a photo with Codex…').pack(anchor='w')
        self.reply_label = ttk.Label(frame, text='New post')
        self.reply_label.pack(anchor='w', pady=(8, 0))
        entry = ttk.Entry(frame)
        self.grove_entry = entry
        entry.insert(0, self.draft)
        entry.pack(fill='x', pady=5)
        if self.reply_to is not None:
            target = next((p for p in apps.grove_posts(s) if p['id'] == self.reply_to), None)
            self.choose_reply(target)
        bar = ttk.Frame(frame); bar.pack(fill='x', pady=(0, 8))
        PhoneButton(bar, text='Post', command=lambda: self.act(apps.post, entry.get(), self.reply_to)).pack(side='left')
        PhoneButton(bar, text='Cancel reply', command=lambda: self.choose_reply(None)).pack(side='left', padx=5)
        PhoneButton(bar, text='Refresh feed', command=self.refresh).pack(side='right')
        posts = apps.grove_posts(s)
        children = {}
        for p in posts: children.setdefault(p['parent'], []).append(p)
        # Traverse data once, but bound widgets, image decoding and live timers.
        stack = [(p, 0) for p in children.get(None, [])]
        entries, seen = [], set()
        while stack:
            p, depth = stack.pop()
            if p['id'] in seen:
                continue
            seen.add(p['id'])
            entries.append((p, depth))
            stack.extend((child, depth+1) for child in reversed(children.get(p['id'], [])))
        page_size = 12
        navigation = ttk.Frame(frame)
        navigation.pack(fill='x')
        page_label = ttk.Label(navigation)
        body = self.scroll_area(frame)
        self.grove_feed_body = body
        def render_page(page):
            page = max(0, min(page, max(0, (len(entries)-1)//page_size)))
            self.grove_feed_page = page
            for child in body.winfo_children(): child.destroy()
            newer.configure(state='normal' if page else 'disabled')
            older.configure(state='normal' if (page+1)*page_size < len(entries) else 'disabled')
            page_label.configure(text=f'Page {page+1} of {max(1, (len(entries)+page_size-1)//page_size)}')
            if not entries:
                ttk.Label(body, text='A quiet feed. Share the first post!').pack(pady=20)
            for p, depth in entries[page*page_size:(page+1)*page_size]:
                card = ttk.Frame(body, padding=10, relief='groove')
                card.pack(fill='x', padx=(min(depth, 5)*20, 0), pady=4)
                avatar = self.avatars._avatar(p['author'])
                if avatar: ttk.Label(card, image=avatar).pack(side='left', anchor='n', padx=(0, 10))
                content = ttk.Frame(card); content.pack(fill='x', expand=True)
                PhoneButton(content, text=apps.handle(p['author'], self.game.state_data),
                           command=lambda who=p['author']: grove_gallery_ui.show_profile(self, who)).pack(anchor='w')
                ttk.Label(content, text=grove_gallery.timestamp(p), font=('Segoe UI', 9)).pack(anchor='w')
                if p.get('image'):
                    grove_gallery_ui.photo_button(content, p, 340,
                        lambda p=p: grove_gallery_ui.show_post(self, p)).pack(anchor='w', pady=5)
                ttk.Label(content, text=p['text'], wraplength=540).pack(anchor='w', pady=5)
                if p.get('image'):
                    grove_gallery_ui.like_button(content, self, p).pack(anchor='w', pady=3)
                PhoneButton(content, text='Reply', command=lambda p=p: self.choose_reply(p)).pack(anchor='w')
            self.fit_wrapping(body)
            body.master.yview_moveto(0)
        newer = PhoneButton(navigation, text='Newer', command=lambda: render_page(self.grove_feed_page-1))
        newer.pack(side='left')
        older = PhoneButton(navigation, text='Older', command=lambda: render_page(self.grove_feed_page+1))
        older.pack(side='right')
        page_label.pack()
        render_page(0)

    def choose_reply(self, post):
        self.reply_to = post['id'] if post else None
        self.reply_label.configure(text=f"Replying to {apps.handle(post['author'], self.game.state_data)}: {post['text'][:65]}" if post else 'New post')

    def store(self, frame, s, app):
        import phone_app_design as design
        food = app == 'Doober Eats'
        accent = design.ACCENTS.get(app, '#f3b75f')
        design.navigation(frame, [('Browse', lambda: self.open_app(app)),
                                  ('Orders', lambda: self.open_app('Deliveries')),
                                  ('Wallet', lambda: self.open_app('Pocket Wallet'))])
        design.hero(frame, app, 'DELIVERY / WINTERFIELD' if food else 'SUPAFAST / DAILY FINDS',
                    'What sounds good?' if food else 'Find a little happiness',
                    f"Instant delivery · Balance ${s['world']['money']:,}")
        recipients = {'Yourself': s['player']}
        recipients.update({f'{personal.name(s, who)} ({apps.handle(who, self.game.state_data)})': who for who in apps.contacts(s)})
        if self.recipient.get() not in recipients: self.recipient.set('Yourself')
        ttk.Label(frame, text='Deliver to', foreground=accent).pack(anchor='w')
        ttk.Combobox(frame, textvariable=self.recipient, values=list(recipients), state='readonly').pack(fill='x', pady=5)
        if food:
            picker = ttk.Combobox(frame, textvariable=self.restaurant, values=list(apps.MENUS), state='readonly')
            picker.pack(fill='x', pady=5)
            picker.bind('<<ComboboxSelected>>', lambda e: self.refresh())
            import doober_images
            products = doober_images.menu(s, self.restaurant.get())
            photo_jobs = doober_images.jobs(self.game, self.restaurant.get())
            photo_jobs.request()
        else:
            import supafast
            manager = supafast.jobs(self.game)
            manager.request()
            self.supafast_stamp = (manager.key(), manager.status())
            products = apps.catalog(s)
            ttk.Label(frame, text=f'Day {s["world"]["minute"] // 1440 + 1} · AI daily selection', foreground=accent).pack(anchor='w')
            if not products:
                body = self.scroll_area(frame)
                failed = manager.status() == 'error'
                design.card(body, 'Stock could not be loaded' if failed else 'Finding today’s discoveries…',
                    'Check AI & account, then retry. No purchases have been made.' if failed else
                    'Creating new products and descriptions. You can use other apps while this loads.', accent)
                if failed:
                    PhoneButton(body, text='Retry daily selection', command=lambda: (manager.request(retry=True), self.refresh())).pack(fill='x')
                return
        if not food:
            photo_jobs = supafast.image_jobs(self.game)
            photo_jobs.request()
        search = tk.StringVar()
        ttk.Label(frame, text='Search this menu' if food else 'Search daily finds').pack(anchor='w')
        ttk.Entry(frame, textvariable=search).pack(fill='x', pady=(4, 8))
        body = self.scroll_area(frame)
        def render(*_):
            for child in body.winfo_children(): child.destroy()
            matches = [(key, item) for key, item in products.items()
                       if search.get().casefold() in (item['name']+' '+item['category']+' '+item.get('description', '')).casefold()]
            if not matches:
                design.card(body, 'No matches', 'Try a different name or category.', accent)
            category = None
            for key, product in matches:
                if category != product['category']:
                    category = product['category']
                    ttk.Label(body, text=category, foreground=accent, font=('Segoe UI', 14, 'bold')).pack(anchor='w', pady=(14, 4))
                panel = design.card(body, product['name'],
                    'Prepared for instant delivery' if food else product['description'],
                    accent)
                from supafast_ui import ProductPhoto
                photo = ProductPhoto(panel, photo_jobs, product, noun='food' if food else 'product')
                photo.pack(fill='x', pady=(0, 10), before=panel.winfo_children()[0])
                design.text(panel, f"${product['price']}", 22, accent, True)
                PhoneButton(panel, text='Order / send' if food else 'Buy / send', command=lambda key=key: self.act(
                    apps.order, app, key, recipients[self.recipient.get()], self.restaurant.get())).pack(fill='x', pady=(6, 0))
        search.trace_add('write', render)
        render()

    def deliveries(self, frame, s):
        ttk.Label(frame, text='Delivered orders', font=('Segoe UI', 20, 'bold')).pack(anchor='w')
        body = self.scroll_area(frame)
        orders = apps.ensure(s)['orders']
        if not orders: ttk.Label(body, text='Your deliveries will appear here.').pack(pady=20)
        for order in reversed(orders):
            ttk.Label(body, text=f"{order['app']} · {order['name']} · ${order['price']}\nTo {order['recipient'].title()} · Day {order['minute']//1440+1} · Delivered", padding=10).pack(anchor='w')
