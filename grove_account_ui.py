"""Embedded, dark Grove account setup and editing."""
import tkinter as tk
from tkinter import ttk
from phone_dialogs import AppWindow
from phone_controls import PhoneButton
import phone_theme
import grove_accounts as accounts
import grove


def form(host, parent, s, done=None):
    data = accounts.account(s)
    ttk.Label(parent, text='Edit your Grove account' if data else 'Create your Grove account',
              font=('Segoe UI', 17, 'bold'), wraplength=360).pack(anchor='w', pady=(8, 10))
    ttk.Label(parent, text='Choose how you appear publicly. Your followers are an audience, not personal contacts.',
              wraplength=360).pack(anchor='w', pady=6)
    ttk.Label(parent, text='Handle · 3–24 letters, numbers, dots or underscores').pack(anchor='w', pady=(10, 4))
    handle = ttk.Entry(parent)
    handle.insert(0, data['handle'] if data else '')
    handle.pack(fill='x')
    ttk.Label(parent, text='Bio · up to 280 characters').pack(anchor='w', pady=(12, 4))
    bio = tk.Text(parent, height=5, wrap='word', font=('Segoe UI', 11),
                  bg='#293447', fg='#f5eedf', insertbackground='#f5eedf', relief='flat')
    bio.insert('1.0', data['bio'] if data else '')
    bio.pack(fill='x')
    status = ttk.Label(parent, text='', wraplength=360)
    status.pack(anchor='w', pady=8)
    def save():
        try:
            accounts.save(s, handle.get(), bio.get('1.0', 'end'))
        except ValueError as exc:
            status.configure(text=str(exc)); return
        host.game.persist()
        if done:
            done()
        host.refresh()
    button = PhoneButton(parent, text='Save account' if data else 'Create account', command=save)
    button.pack(fill='x', pady=8)
    introduction = 'Editing keeps your followers and pending growth. ' if data else 'Start with 0 followers. '
    ttk.Label(parent, text=introduction + 'Original posts, photos and replies earn followers gradually over '
              'the next 24 hours of game time. Up to 3 posts/photos and 5 replies per game day count; repeated '
              'content and replies to yourself do not earn more.', wraplength=360, style='Muted.TLabel').pack(anchor='w', pady=8)
    phone_theme.apply_tree(parent)
    return dict(handle=handle, bio=bio, status=status, save=button)


def edit(host):
    window = AppWindow(host)
    window.title('Grove account')
    window.geometry('520x600')
    body = host.scroll_area(window)
    controls = form(host, body, host.game.state_data, done=window.destroy)
    return window, controls


def stats(parent, s):
    label = ttk.Label(parent, wraplength=360)
    label.pack(anchor='w', pady=4)
    timer = None
    def update():
        nonlocal timer
        count = grove.profile(s, s['player'])['followers']
        pending = accounts.pending(s)
        label.configure(text=f'{count:,} followers' + (f' · {pending} more from recent activity' if pending else ''))
        timer = label.after(1000, update)
    def cleanup(event):
        if event.widget is label and timer is not None:
            label.after_cancel(timer)
    label.bind('<Destroy>', cleanup, add='+')
    update()
    return label
