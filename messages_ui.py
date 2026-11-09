"""Phone-style message history, kept separate from spoken conversations."""
import json
import tkinter as tk
from pathlib import Path
from PIL import Image, ImageDraw, ImageOps, ImageTk
from typing_ui import TypingIndicator

PROFILE_DIR = Path(__file__).resolve().parent / 'assets' / 'profiles'


def text_messages(state, pending=None, group=None):
    import game_core as core
    messages = []
    if group:
        identities = {core.CONTACTS.get(k, (k,))[0]: k for k in group['members']}
        for line in group['history']:
            speaker = line.get('speaker', '')
            if speaker == 'Narrator' or line.get('kind') == 'action':
                continue
            outgoing = speaker.endswith(' (You)')
            names = {core.CONTACTS.get(k, (k,))[0]: core.contact_name(state, k) for k in group['members']}
            character = state['player'] if outgoing else identities.get(speaker)
            messages.append((names.get(speaker, speaker), line['text'], 'out' if outgoing else 'in', character, line.get('minute'), line.get('receipt'), line.get('photo')))
    else:
        history = state['routes'][state['active']]['history']
        for index, message in enumerate(history):
            if message['role'] == 'status':
                if not any(term in message['content'] for term in ('In-person conversation', 'Hangout', 'left the shared location')):
                    messages.append(('', message['content'], 'status', None))
            elif message['role'] == 'assistant' and message.get('channel') == 'text':
                messages.append(('', json.loads(message['content'])['dialogue'], 'in', state['active'], message.get('minute'), None, message.get('photo')))
            elif message['role'] == 'user':
                # The response records the channel of the exchange, including transitions.
                response = next((m for m in history[index+1:] if m['role'] == 'assistant'), {})
                if (message.get('channel') == 'text' or response.get('channel') == 'text') and core.player_message(state, message['content'])['kind'] == 'player_reply':
                    messages.append(('', message['content'], 'out', state['player'], message.get('minute', response.get('minute')), message.get('receipt'), message.get('photo')))
    if pending and core.player_message(state, pending)['kind'] == 'player_reply':
        messages.append(('', pending, 'out', state['player'], state['world']['minute']))
    return messages


class MessageBubbles(tk.Canvas):
    def __init__(self, parent, *, bg):
        super().__init__(parent, bg=bg, highlightthickness=0, height=60, width=1)
        self.messages = []
        self.message_ids = []
        self.pinned_ids = set()
        self.selected_message = 0
        self.configure(takefocus=True)
        self.bind('<Up>',lambda e:self._select_message(-1))
        self.bind('<Down>',lambda e:self._select_message(1))
        self.bind('<Return>',self._keyboard_menu)
        self._avatars = {}
        self._typing_character = None
        self._typing_caption = None
        self._reveal_timer = None
        self._reveal_count = None
        self.bind('<Destroy>', self._stop_reveal, add='+')
        self.typing_indicator = TypingIndicator(self, bg=bg, foreground='#aaaabd')
        self.latest_button = tk.Button(
            self, text='↓ Latest', command=self.jump_to_latest,
            bg='#007aff', fg='#dce4ed', activebackground='#0062cc',
            activeforeground='#dce4ed', font=('Segoe UI', 10, 'bold'),
            relief='flat', cursor='hand2', padx=12, pady=6)
        self.configure(yscrollcommand=self._update_latest_button)
        self.bind('<Configure>', self._resize)
        self.bind('<MouseWheel>', lambda e: self.yview_scroll(-int(e.delta / 120), 'units'))
        self.bind('<Button-4>', lambda e: self.yview_scroll(-1, 'units'))
        self.bind('<Button-5>', lambda e: self.yview_scroll(1, 'units'))

    def jump_to_latest(self):
        self.yview_moveto(1)

    def _select_message(self, delta):
        eligible=[i for i,m in enumerate(self.messages) if m[2]!='status']
        if not eligible: return 'break'
        old=eligible.index(self.selected_message) if self.selected_message in eligible else 0
        self.selected_message=eligible[max(0,min(len(eligible)-1,old+delta))]
        bounds=self.bbox(f'message:{self.selected_message}')
        if bounds:
            region=list(map(float,self.cget('scrollregion').split()))
            self.yview_moveto(max(0,bounds[1]-20)/max(1,region[3]))
        return 'break'

    def _keyboard_menu(self,event):
        from types import SimpleNamespace
        if hasattr(self,'on_message_action'):
            self.on_message_action(self.selected_message,SimpleNamespace(x_root=self.winfo_rootx()+30,y_root=self.winfo_rooty()+30))
        return 'break'

    def _update_latest_button(self, first, last):
        if float(last) < .999:
            self.latest_button.place(relx=1, rely=1, x=-12, y=-12, anchor='se')
            self.latest_button.lift()
        else:
            self.latest_button.place_forget()

    def set_messages(self, messages, *, typing_caption=None, typing_character=None):
        import phone_personalization as personal
        prefs = personal.preferences()
        animate = (bool(self.messages) and len(messages) > len(self.messages)
                   and messages[-1][2] == 'in' and prefs['reveal'] != 'Instant'
                   and not prefs['reduced_motion'])
        self._stop_reveal()
        position = self.yview()
        follow = not self.messages or position[1] >= .98
        self.messages = messages
        self._reveal_count = 0 if animate else None
        self._typing_caption = typing_caption
        self._typing_character = typing_character
        if typing_caption:
            self.typing_indicator.show(typing_caption)
        else:
            self.typing_indicator.hide()
        self._draw()
        self.yview_moveto(1 if follow else position[0])
        if animate: self._reveal_timer = self.after(30, self._reveal_step)

    def _stop_reveal(self, event=None):
        if event is not None and event.widget is not self: return
        if self._reveal_timer is not None:
            self.after_cancel(self._reveal_timer)
            self._reveal_timer = None
        self._reveal_count = None

    def _reveal_step(self):
        import phone_personalization as personal
        self._reveal_timer = None
        self._reveal_count += 8 if personal.preferences()['reveal'] == 'Fast' else 2
        follow = self.yview()[1] >= .98
        if self._reveal_count >= len(self.messages[-1][1]): self._reveal_count = None
        self._draw()
        if follow: self.yview_moveto(1)
        if self._reveal_count is not None: self._reveal_timer = self.after(30, self._reveal_step)

    def _resize(self, event):
        position = self.yview()[0]
        self._draw()
        self.yview_moveto(position)

    def _avatar(self, character):
        if not character:
            return None
        if character not in self._avatars:
            path = PROFILE_DIR / f'{character}.png'
            if character == 'charles': path = PROFILE_DIR / 'charles-contact-v3.png'
            import town_residents
            if not path.exists() and character in town_residents.RESIDENTS:
                path = PROFILE_DIR.parent / 'portraits' / (character.lower().replace(' ', '-') + '-selection.png')
            if hasattr(self, 'phone_state'):
                import phone_personalization as personal
                selection = personal.ensure(self.phone_state)['avatars'].get(character)
                if selection and selection != 'default':
                    path = personal.photos(self.phone_state).get(selection, ('', path))[1]
            try:
                with Image.open(path) as source:
                    portrait = ImageOps.fit(source.convert('RGB'), (120, 120), Image.Resampling.LANCZOS)
                mask = Image.new('L', (120, 120))
                ImageDraw.Draw(mask).ellipse((0, 0, 119, 119), fill=255)
                portrait.putalpha(mask)
                portrait = portrait.resize((40, 40), Image.Resampling.LANCZOS)
                self._avatars[character] = ImageTk.PhotoImage(portrait, master=self)
            except (OSError, ValueError):
                self._avatars[character] = None
        return self._avatars[character]

    def _draw(self):
        self.delete('all')
        self._photo_images = []
        width = max(100, self.winfo_width())
        compact = width < 340 or getattr(self,'iphone',False)
        margin = 12 if compact else 60
        wrap = max(40, min(540, int(width * (.9 if compact else .72)), width-2*margin) - 28)
        y = 12
        previous_day = None
        import phone_personalization as personal
        for index, message in enumerate(self.messages):
            sender, text, kind = message[:3]
            if index == len(self.messages)-1 and self._reveal_count is not None:
                text = text[:self._reveal_count] or ' '
            character = message[3] if len(message) > 3 else None
            if kind == 'status':
                item = self.create_text(width/2, y, text=text, anchor='n', width=width-32,
                                        fill='#aaaabd', font=('Segoe UI', 10), justify='center')
                y = self.bbox(item)[3] + 16
                continue
            minute = message[4] if len(message) > 4 else None
            if minute is not None:
                import story_calendar
                day = minute // 1440
                if day != previous_day:
                    if not getattr(self,'iphone',False): self.create_line(16, y+9, width-16, y+9, fill='#454550')
                    label = self.create_text(width/2, y, text=story_calendar.story_date(minute).strftime('%A, %B %d, %Y'),
                        anchor='n', fill='#aaaabd', font=('Segoe UI', 10))
                    bounds = self.bbox(label)
                    backing = self.create_rectangle(bounds[0]-10, bounds[1], bounds[2]+10, bounds[3], fill=self['bg'], outline='')
                    self.tag_lower(backing, label)
                    y += 32
                    previous_day = day
            outgoing = kind == 'out'
            ident=self.message_ids[index] if index<len(self.message_ids) else None
            if ident in self.pinned_ids:
                self.create_text(width-16 if outgoing else 16,y,text='📌 Pinned',anchor='ne' if outgoing else 'nw',fill='#ffd60a',font=('Segoe UI',9))
                y+=20
            if sender and not outgoing:
                self.create_text(margin+4, y, text=sender, anchor='nw', fill='#aaaabd', font=('Segoe UI', 9))
                y += 21
            item = self.create_text(0, 0, text=text, anchor='nw', width=wrap,
                                    fill='#dce4ed', font=('Segoe UI', personal.preferences()['text_size']))
            bounds = self.bbox(item)
            w, h = bounds[2]-bounds[0]+28, bounds[3]-bounds[1]+20
            photo = message[6] if len(message) > 6 else None
            thumbnail = None
            if photo:
                import camera
                try:
                    with Image.open(camera.photo_path(photo)) as source:
                        fitted = ImageOps.exif_transpose(source).convert('RGB')
                        fitted.thumbnail((max(40, int(wrap)), 220))
                    thumbnail = ImageTk.PhotoImage(fitted, master=self)
                    self._photo_images.append(thumbnail)
                    w = max(w, thumbnail.width()+28)
                    h += thumbnail.height()+8
                except (OSError, ValueError, KeyError):
                    pass
            x = width-w-margin if outgoing else margin
            color = '#007aff' if outgoing else '#3a3a3c'
            radius = min(18, h/2)
            bubble = self.create_polygon(
                x+radius,y, x+w-radius,y, x+w,y, x+w,y+radius,
                x+w,y+h-radius, x+w,y+h, x+w-radius,y+h,
                x+radius,y+h, x,y+h, x,y+h-radius, x,y+radius, x,y,
                smooth=True, splinesteps=24, fill=color, outline='')
            self.tag_lower(bubble, item)
            self.coords(item, x+14, y+10)
            tag=f'message:{index}'
            if thumbnail:
                self.create_image(x+14, y+h-thumbnail.height()-10, image=thumbnail, anchor='nw', tags=(tag,))
            self.addtag_withtag(tag,item); self.addtag_withtag(tag,bubble)
            if hasattr(self,'on_message_action'):
                for sequence in ('<ButtonRelease-1>','<Button-3>'):
                    self.tag_bind(tag,sequence,lambda e,i=index:self.on_message_action(i,e))
            avatar = self._avatar(character)
            if avatar is not None and not compact:
                self.create_image(width-28 if outgoing else 28, y+max(h, 40)-20,
                                  image=avatar, tags=('avatar', f'avatar:{character}'))
            y += max(h, 40)
            if minute is not None:
                hour, mins = divmod(minute % 1440, 60)
                stamp = f'{hour % 12 or 12}:{mins:02d} {"AM" if hour < 12 else "PM"}'
                if outgoing and len(message)>5 and message[5]: stamp += ' · '+message[5]
                self.create_text(x+w-6 if outgoing else x+6, y+3, text=stamp,
                    anchor='ne' if outgoing else 'nw', fill='#aaaabd', font=('Segoe UI', 9))
                y += 19
            y += 10
        if self._typing_caption:
            avatar = self._avatar(self._typing_character)
            if avatar is not None:
                self.create_image(28, y+20, image=avatar, tags=('typing-avatar',))
            self.create_window(60, y, window=self.typing_indicator, anchor='nw',
                               width=max(80, width-72), height=44, tags=('typing-bubble',))
            y += 56
        self.configure(scrollregion=(0, 0, width, max(y, self.winfo_height())))
