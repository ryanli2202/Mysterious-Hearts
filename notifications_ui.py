"""Non-modal notifications for newly delivered phone activity."""
from collections import deque
import json
import tkinter as tk


class NotificationPopups:
    def __init__(self, game):
        self.game = game
        self.state = None
        self.counts = {}
        self.seen_comments = set()
        self.pending = deque()
        self.window = None
        self.timer = None

    def observe(self, state):
        import game_core as core
        import phone_apps as apps
        streams = {}
        for key, route in state.get('routes', {}).items():
            messages = [m for m in route.get('history', [])
                        if m.get('role') == 'assistant' and m.get('channel') == 'text']
            streams[('route', key)] = (core.CONTACTS.get(key, (key,))[0], messages)
        for key, group in state.get('groups', {}).items():
            if group.get('channel') == 'text':
                messages = [m for m in group.get('history', [])
                            if m.get('speaker') != 'Narrator' and not m.get('speaker', '').endswith(' (You)')]
                streams[('group', key)] = (group.get('name', 'Group message'), messages)
        comments = state.get('phone_apps', {}).get('grove_notifications', [])
        streams[('meet_cute', 'app')] = ('Meet-Cute', [dict(text=core.CONTACTS.get(n['who'], (n['who'],))[0]+': '+n['text'])
            for n in state.get('meet_cute', {}).get('notices', [])])
        if self.state is state:
            for key, (name, messages) in streams.items():
                for message in messages[self.counts.get(key, 0):]:
                    preview = message.get('text', '')
                    if key[0] == 'route':
                        try:
                            preview = json.loads(message.get('content', '{}')).get('dialogue', '')
                        except (ValueError, AttributeError):
                            preview = 'New message'
                    elif message.get('speaker'):
                        preview = message['speaker'] + ': ' + preview
                    self.pending.append((name if key[0]=='meet_cute' else 'Message · ' + name, preview or 'New message'))
            for notice in comments:
                if notice['comment_id'] not in self.seen_comments:
                    action = ' replied to your comment' if notice.get('kind') == 'reply' else ' commented on your post'
                    self.pending.append(('Grove · ' + apps.handle(notice['author'], state) + action, notice['text']))
        else:
            self.pending.clear()
            self.dismiss(show_next=False)
        self.state = state
        self.counts = {key: len(messages) for key, (_, messages) in streams.items()}
        self.seen_comments = {n['comment_id'] for n in comments}
        self.show_next()

    def show_next(self):
        if self.window is not None or not self.pending:
            return
        title, preview = self.pending.popleft()
        window = self.window = tk.Toplevel(self.game)
        window.withdraw()
        window.overrideredirect(True)
        window.attributes('-topmost', True)
        window.configure(bg='#dfba78', padx=1, pady=1)
        card = tk.Frame(window, bg='#222638', padx=14, pady=12)
        card.pack(fill='both', expand=True)
        tk.Button(card, text='×', command=self.dismiss, bg='#222638', fg='#f3eee7',
                  relief='flat', font=('Segoe UI', 13)).pack(side='right', anchor='n')
        tk.Label(card, text=title, bg='#222638', fg='#dfba78', font=('Segoe UI', 10, 'bold'),
                 wraplength=310, justify='left', anchor='w').pack(fill='x')
        preview = ' '.join(str(preview).split())
        tk.Label(card, text=preview[:177] + '…' if len(preview) > 180 else preview,
                 bg='#222638', fg='#f3eee7', font=('Segoe UI', 10),
                 wraplength=310, justify='left', anchor='w').pack(fill='x', pady=(7, 0))
        window.update_idletasks()
        x = max(0, window.winfo_screenwidth() - 390)
        window.geometry(f'370x{window.winfo_reqheight()}+{x}+40')
        window.deiconify()
        self.timer = self.game.after(5000, self.dismiss)

    def dismiss(self, show_next=True):
        if self.timer is not None:
            self.game.after_cancel(self.timer)
            self.timer = None
        if self.window is not None:
            self.window.destroy()
            self.window = None
        if show_next:
            self.show_next()
