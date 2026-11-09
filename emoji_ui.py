"""Emoji picker for message drafts; no messages are sent by the picker."""
import tkinter as tk
from tkinter import ttk
from phone_dialogs import AppWindow, messagebox, simpledialog
import unicodedata


EMOJI_GROUPS = {
    'Smiles': '😀 😃 😄 😁 😆 😅 🤣 😂 🙂 🙃 🫠 🫫 😉 😊 😇',
    'Affection': '🥰 😍 🤩 😘 😗 ☺ 😚 😙 🥲',
    'Playful': '😋 😛 😜 🤪 😝 🤑',
    'Hands and faces': '🤗 🤭 🫢 🫣 🤫 🤔 🫡',
    'Neutral and skeptical': '🤐 🤨 😐 😑 😶 🫥 😶‍🌫️ 😏 😒 🙄 😬 😮‍💨 🤥 🫨 🙂‍↔️ 🙂‍↕️',
    'Sleepy': '😌 😔 😪 🤤 😴 🫩',
    'Unwell': '😷 🤒 🤕 🤢 🤮 🤧 🥵 🥶 🥴 😵 😵‍💫 🤯',
    'Hats and glasses': '🤠 🥳 🥸 😎 🤓 🧐',
    'Concerned': '😕 🫤 😟 🙁 ☹ 😮 😯 😲 😳 🫪 🥺 🥹 😦 😧 😨 😰 😥 😢 😭 😱 😖 😣 😞 😓 😩 😫 🥱',
    'Angry': '😤 😡 😠 🤬 😈 👿 💀 ☠',
    'Costumes': '💩 🤡 👹 👺 👻 👽 👾 🤖',
    'Cats and monkeys': '😺 😸 😹 😻 😼 😽 🙀 😿 😾 🙈 🙉 🙊',
    'Hearts': '💌 💘 💝 💖 💗 💓 💞 💕 💟 ❣ 💔 ❤️‍🔥 ❤️‍🩹 ❤ 🩷 🧡 💛 💚 💙 🩵 💜 🤎 🖤 🩶 🤍',
    'Emotion': '💋 💯 💢 🫯 💥 💫 💦 💨 🕳 💬 👁️‍🗨️ 🗨 🗯 💭 💤',
    'Open hands': '👋 🤚 🖐 ✋ 🖖 🫱 🫲 🫳 🫴 🫷 🫸',
    'Hand gestures': '👌 🤌 🤏 ✌ 🤞 🫰 🤟 🤘 🤙',
    'Pointing': '👈 👉 👆 🖕 👇 ☝ 🫵',
    'Thumbs and fists': '👍 👎 🫹 🫺 ✊ 👊 🤛 🤜',
}

NAMES = {
    '🫫': 'cracking face', '🫪': 'distorted face', '🫯': 'fight cloud',
    '🫹': 'leftwards thumb sign', '🫺': 'rightwards thumb sign',
    '🫩': 'face with bags under eyes', '🩷': 'pink heart',
    '🩵': 'light blue heart', '🩶': 'grey heart', '🫨': 'shaking face',
    '😶‍🌫️': 'face in clouds', '😮‍💨': 'face exhaling',
    '🙂‍↔️': 'head shaking horizontally', '🙂‍↕️': 'head shaking vertically',
    '😵‍💫': 'face with spiral eyes', '❤️‍🔥': 'heart on fire',
    '❤️‍🩹': 'mending heart', '👁️‍🗨️': 'eye in speech bubble',
}


def emoji_name(emoji):
    return NAMES.get(emoji) or ' '.join(
        unicodedata.name(char, 'emoji').lower() for char in emoji
        if char not in '\ufe0f\u200d')


class EmojiKeyboard(ttk.Frame):
    """An embedded emoji keyboard; selecting a key only edits the draft."""
    SECTIONS = {
        '☺ Faces': list(EMOJI_GROUPS)[:14],
        '♡ Hearts': ['Hearts', 'Emotion', 'Affection'],
        '☝ Hands': ['Hands and faces', 'Open hands', 'Hand gestures', 'Pointing', 'Thumbs and fists'],
        '♧ Fun': ['Costumes', 'Cats and monkeys', 'Hats and glasses'],
    }

    def __init__(self, parent, entry, on_change, on_close):
        super().__init__(parent, padding=(4, 4))
        from phone_controls import PhoneButton
        self.entry, self.on_change = entry, on_change
        self.query = tk.StringVar(self)
        self.section = next(iter(self.SECTIONS))
        top = ttk.Frame(self)
        top.pack(fill='x')
        ttk.Label(top, text='Search emoji').pack(side='left', padx=(0, 8))
        search = ttk.Entry(top, textvariable=self.query)
        search.pack(side='left', fill='x', expand=True)
        PhoneButton(top, text='⌄ Done', command=on_close).pack(side='right', padx=(6, 0))
        search.bind('<Escape>', lambda event: (on_close(), 'break')[-1])
        area = ttk.Frame(self)
        area.pack(fill='x', pady=4)
        self.canvas = tk.Canvas(area, height=132, highlightthickness=0, bg='#222638')
        scrollbar = ttk.Scrollbar(area, orient='vertical', command=self.canvas.yview)
        scrollbar.pack(side='right', fill='y')
        self.canvas.pack(side='left', fill='x', expand=True)
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.grid_frame = tk.Frame(self.canvas, bg='#222638')
        self.window = self.canvas.create_window(0, 0, window=self.grid_frame, anchor='nw')
        self.columns = 8
        self.canvas.bind('<Configure>', self.resize)
        self.grid_frame.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox('all')))
        self.caption = ttk.Label(self, text='', font=('Segoe UI', 9))
        self.caption.pack(anchor='w')
        tabs = ttk.Frame(self)
        tabs.pack(fill='x')
        self.tabs = {}
        for name in self.SECTIONS:
            button = PhoneButton(tabs, text=name, command=lambda name=name: self.select(name))
            button.pack(side='left', fill='x', expand=True, padx=1)
            self.tabs[name] = button
        self.query.trace_add('write', lambda *args: self.render())
        self.render()

    def resize(self, event):
        self.canvas.itemconfigure(self.window, width=event.width)
        columns = max(1, event.width // 48)
        if columns != self.columns:
            self.columns = columns
            self.render()

    def select(self, name):
        self.section = name
        self.query.set('')

    def render(self):
        for child in self.grid_frame.winfo_children():
            child.destroy()
        query = self.query.get().strip().lower()
        emojis = list(dict.fromkeys(emoji for group, values in EMOJI_GROUPS.items()
                      if query or group in self.SECTIONS[self.section]
                      for emoji in values.split()
                      if not query or query in emoji_name(emoji) or query in emoji or query in group.lower()))
        for index, emoji in enumerate(emojis):
            button = tk.Button(self.grid_frame, text=emoji, font=('Segoe UI Emoji', 19),
                               relief='flat', bd=0, bg='#222638', fg='#dce4ed',
                               activebackground='#40516b', activeforeground='#dce4ed', cursor='hand2',
                               command=lambda emoji=emoji: self.insert(emoji))
            button.grid(row=index // self.columns, column=index % self.columns, sticky='ew')
            button.bind('<MouseWheel>', self.scroll)
            button.bind('<Enter>', lambda e, emoji=emoji: self.caption.config(text=emoji_name(emoji)))
        for col in range(self.columns):
            self.grid_frame.columnconfigure(col, weight=1)
        for name, button in self.tabs.items():
            button.config(style='Accent.TButton' if name == self.section else '')
        self.canvas.bind('<MouseWheel>', self.scroll)
        self.canvas.yview_moveto(0)
        self.caption.config(text='Tap an emoji to add it to your message' if emojis else 'No matching emoji')

    def scroll(self, event):
        self.canvas.yview_scroll(-int(event.delta / 120), 'units')
        return 'break'

    def insert(self, emoji):
        if self.entry.selection_present():
            self.entry.delete('sel.first', 'sel.last')
        self.entry.insert('insert', emoji)
        self.entry.xview_moveto(1)
        self.on_change()
        self.caption.config(text='Inserted ' + emoji_name(emoji))


class EmojiPicker(AppWindow):
    def __init__(self, entry, on_change):
        super().__init__(entry)
        self.entry = entry
        self.on_change = on_change
        self.title('Choose an emoji')
        self.transient(entry.winfo_toplevel())
        self.geometry('440x380')
        self.minsize(440, 300)
        self.bind('<Escape>', lambda event: (self.destroy(), 'break')[-1])
        body = ttk.Frame(self, padding=12)
        body.pack(fill='both', expand=True)
        self.query = tk.StringVar()
        ttk.Label(body, text='Search emoji').pack(anchor='w')
        search = ttk.Entry(body, textvariable=self.query)
        search.pack(fill='x', pady=(4, 8))
        self.category = tk.StringVar(value='Smiles')
        categories = ttk.Combobox(body, textvariable=self.category, state='readonly',
                                  values=['All emojis', *EMOJI_GROUPS])
        categories.pack(fill='x', pady=(0, 8))
        area = ttk.Frame(body)
        area.pack(fill='both', expand=True)
        self.canvas = tk.Canvas(area, highlightthickness=0, bg='#191c2b')
        scrollbar = ttk.Scrollbar(area, orient='vertical', command=self.canvas.yview)
        scrollbar.pack(side='right', fill='y')
        self.canvas.pack(side='left', fill='both', expand=True)
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.grid_frame = tk.Frame(self.canvas, bg='#191c2b')
        self.canvas.create_window(0, 0, window=self.grid_frame, anchor='nw')
        self.grid_frame.bind('<Configure>', lambda event:
                             self.canvas.configure(scrollregion=self.canvas.bbox('all')))
        self.caption = ttk.Label(body, text='Choose an emoji to insert into your message.', wraplength=410)
        self.caption.pack(fill='x', pady=(8, 0))
        ttk.Button(body, text='Done', command=self.destroy).pack(anchor='e', pady=(6, 0))
        self.query.trace_add('write', lambda *args: self.render())
        categories.bind('<<ComboboxSelected>>', lambda event: self.render())
        self.render()
        search.focus_set()

    def render(self):
        for child in self.grid_frame.winfo_children():
            child.destroy()
        query = self.query.get().strip().lower()
        selected = self.category.get()
        emojis = [emoji for group, values in EMOJI_GROUPS.items()
                  if query or selected == 'All emojis' or group == selected
                  for emoji in values.split()
                  if not query or query in emoji_name(emoji) or query in emoji or query in group.lower()]
        for index, emoji in enumerate(emojis):
            button = tk.Button(self.grid_frame, text=emoji, font=('Segoe UI Emoji', 19),
                               width=2, relief='flat', bg='#222638', fg='#dce4ed',
                               activebackground='#007aff', activeforeground='#dce4ed',
                               command=lambda value=emoji: self.insert(value))
            button.grid(row=index // 8, column=index % 8, padx=2, pady=2)
            button.bind('<Enter>', lambda event, value=emoji: self.caption.config(text=emoji_name(value)))
            button.bind('<FocusIn>', lambda event, value=emoji: self.caption.config(text=emoji_name(value)))
            button.bind('<MouseWheel>', self.scroll)
        self.canvas.bind('<MouseWheel>', self.scroll)
        self.canvas.yview_moveto(0)
        self.caption.config(text='Choose an emoji to insert into your message.' if emojis else 'No matching emoji.')

    def scroll(self, event):
        self.canvas.yview_scroll(-int(event.delta / 120), 'units')
        return 'break'

    def insert(self, emoji):
        if not self.entry.winfo_exists():
            self.destroy()
            return
        if self.entry.selection_present():
            self.entry.delete('sel.first', 'sel.last')
        self.entry.insert('insert', emoji)
        self.entry.xview_moveto(1)
        self.on_change()
        self.caption.config(text='Inserted ' + emoji_name(emoji))
