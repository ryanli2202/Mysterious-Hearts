"""Phone views for anonymous conversations and contact notebooks."""
import tkinter as tk
from tkinter import ttk, messagebox
from phone_dialogs import AppWindow, messagebox, simpledialog
import mysterious_hearts as hearts
import contact_profiles as profiles
import game_core as core


def label(parent, text):
    widget=ttk.Label(parent,text=text,wraplength=360,justify='left')
    widget.pack(fill='x',pady=4)
    widget.bind('<Configure>',lambda e:widget.configure(wraplength=max(100,e.width-8)))


def button(parent, text, command):
    ttk.Button(parent, text=text, command=command).pack(anchor='w', pady=3)


def stamp(minute):
    if minute is None: return 'Earlier'
    import story_calendar
    return f'{story_calendar.story_date(minute):%b %d} · {minute % 1440 // 60:02}:{minute % 60:02}'


def source_name(s, source):
    return core.contact_name(s, source) if source in core.CONTACTS else 'Your recorded experience'


def mutate(phone, callback, refresh):
    if phone.game.busy:
        messagebox.showinfo('Phone', 'Wait for the current conversation to finish.', parent=phone); return
    try: callback()
    except ValueError as exc:
        messagebox.showinfo('Phone', str(exc), parent=phone); return
    phone.game.persist(); refresh()


def directory(phone):
    s = phone.game.state_data
    import phone_apps
    return {core.contact_name(s, w):w for w in phone_apps.contacts(s)}


def hearts_styles(parent):
    import winterfield_ui as ui
    style = ttk.Style(parent)
    style.configure('Hearts.TFrame', background=ui.CARD)
    for name, color, size in [('Title', '#edb4d2', 22), ('Caption', '#c5b8e7', 10), ('Card', ui.CREAM, 11)]:
        style.configure('Hearts'+name+'.TLabel', background=ui.CARD, foreground=color,
                        font=('Segoe UI', size, 'bold' if name == 'Title' else 'normal'))
    style.configure('Hearts.TButton', background='#493c59', foreground='#f1c6df', padding=(12, 8))
    style.map('Hearts.TButton', background=[('disabled', ui.PANEL), ('pressed', '#634b70'), ('active', '#574465')],
              foreground=[('disabled', ui.MUTED)])


def card(parent):
    panel = ttk.Frame(parent, style='Hearts.TFrame', padding=12)
    panel.pack(fill='x', pady=6)
    return panel


def note_label(parent, text, style='Card'):
    widget = ttk.Label(parent, text=text, style='Hearts'+style+'.TLabel', wraplength=360)
    widget.pack(anchor='w', fill='x', pady=3)
    widget.bind('<Configure>', lambda e: widget.configure(wraplength=max(100, e.width-8)))
    return widget


def pending_status(phone, body, s, ident=None):
    pending = [p for p in hearts.ensure(s)['pending'] if
               (p['thread'] == ident if ident is not None else s['player'] in (p['actor'], p['recipient']))]
    if not pending: return
    panel = card(body)
    failed = [p for p in pending if p.get('error')]
    note_label(panel, '♡ A little note is on its way…' if not failed else '♡ A note is waiting to arrive', 'Caption')
    if failed:
        note_label(panel, 'Check AI & account, then try again. Your conversation is saved.')
        def retry():
            for p in failed: p['error'] = None
            phone.game.persist()
            thread(phone, ident) if ident is not None else phone.refresh()
        ttk.Button(panel, text='Try again ♡', style='Hearts.TButton', command=retry).pack(anchor='w')


def page(phone, frame, s):
    hearts_styles(frame)
    phone.hearts_thread = None
    body = phone.scroll_area(frame)
    hero = card(body)
    note_label(hero, '♡ Mysterious Hearts', 'Title')
    note_label(hero, 'little notes · secret butterflies', 'Caption')
    note_label(hero, 'A small kindness. A quiet crush. A story between two people.')
    compose = card(body)
    note_label(compose, '✧ Send a little something', 'Caption')
    names = directory(phone)
    note_label(compose, 'To')
    to = ttk.Combobox(compose, values=list(names), state='readonly'); to.pack(fill='x')
    if names: to.current(0)
    note_label(compose, 'What is on your heart?')
    entry = ttk.Entry(compose); entry.pack(fill='x', pady=4)
    intent = ttk.Combobox(compose, values=('compliment', 'confession', 'apology', 'warning', 'question', 'appreciation', 'reconciliation'), state='readonly')
    intent.current(0); intent.pack(fill='x', pady=4)
    entry.insert(0, hearts.ensure(s)['drafts'].get('new', ''))
    entry.bind('<KeyRelease>', lambda e: hearts.ensure(s)['drafts'].__setitem__('new', entry.get()))
    def send():
        hearts.send(s, s['player'], names.get(to.get()), entry.get(), intent.get())
        hearts.ensure(s)['drafts'].pop('new', None)
    ttk.Button(compose, text='Seal with a heart ♡', style='Hearts.TButton',
               command=lambda: mutate(phone, send, phone.refresh)).pack(fill='x', pady=(8, 0))
    pending_status(phone, body, s)
    label(body, 'YOUR LETTERBOX')
    rows = hearts.inbox(s, s['player'])
    if not rows:
        empty = card(body)
        note_label(empty, '♡ A little quiet, for now', 'Caption')
        note_label(empty, 'Notes arrive as story time and relationships develop. You can send the first one.')
    for row in rows:
        panel = card(body)
        title = ('To ' + row['recipient'].title()) if row['outgoing'] else ('From '+row['sender'].title() if row['sender'] else 'A secret admirer')
        if not row['member']: title = 'Shared copy · ' + title
        ttk.Button(panel, text=('♡ NEW · ' if row['unread'] else '♡ ') + title,
                   style='Hearts.TButton', command=lambda ident=row['id']: thread(phone, ident)).pack(fill='x')
        note_label(panel, row['messages'][-1]['text'][:150])
        note_label(panel, stamp(row['messages'][-1]['minute']), 'Caption')
    import phone_theme
    phone_theme.apply_tree(frame)


def thread(phone, ident):
    phone.selected = 'Mysterious Hearts thread'
    phone.hearts_thread = ident
    hearts_styles(phone)
    for child in phone.screen.winfo_children(): child.destroy()
    frame = ttk.Frame(phone.screen, padding=14); frame.pack(fill='both', expand=True)
    button(frame, '‹ Mysterious Hearts', lambda: phone.open_app('Mysterious Hearts'))
    s = phone.game.state_data; actor = s['player']; row = hearts.view(s, ident, actor)
    hearts._thread(s, ident)['unread'][actor] = 0
    phone.game.persist()
    body = phone.scroll_area(frame)
    heading = card(body)
    note_label(heading, '♡ Between the lines', 'Title')
    label(body, 'Sender: '+(row['sender'].title() if row['sender'] else 'Unknown'))
    label(body, 'Recipient: '+row['recipient'].title())
    for m in row['messages']:
        role = ('You' if (m['role'] == 'sender') == row['outgoing'] and row['member'] else
                row['recipient'].title() if m['role'] == 'recipient' else row['sender'].title() if row['sender'] else 'Anonymous')
        bubble = card(body)
        note_label(bubble, role + ' · ' + stamp(m['minute']), 'Caption')
        note_label(bubble, m['text'])
    pending_status(phone, body, s, ident)
    refresh = lambda: thread(phone, ident)
    def act(kind, target=None): mutate(phone, lambda: hearts.action(s, ident, actor, kind, target), refresh)
    if row['member'] and not row['blocked'] and not row['closed']:
        entry = ttk.Entry(body); entry.pack(fill='x')
        key = str(ident); entry.insert(0, hearts.ensure(s)['drafts'].get(key, ''))
        entry.bind('<KeyRelease>', lambda e: hearts.ensure(s)['drafts'].__setitem__(key, entry.get()))
        def reply():
            hearts.reply(s, ident, actor, entry.get()); hearts.ensure(s)['drafts'].pop(key, None)
        button(body, 'Reply', lambda: mutate(phone, reply, refresh))
        button(body, 'Reveal myself' if row['outgoing'] else 'Welcome the attention', lambda: act('reveal' if row['outgoing'] else 'welcome'))
        button(body, 'Close this conversation', lambda: act('close'))
        if not row['outgoing']: button(body, 'Ask sender to stop / Block', lambda: act('block'))
    elif row['member']: label(body, 'This conversation is closed.' if row['closed'] else 'Sender blocked.')
    notebook = ttk.Frame(body)
    def toggle_notebook():
        if notebook.winfo_manager(): notebook.pack_forget()
        else: notebook.pack(fill='x', pady=8)
    ttk.Button(body, text='✧ Open / close mystery notebook', style='Hearts.TButton',
               command=toggle_notebook).pack(fill='x', pady=10)
    label(notebook, '✧ The mystery notebook · Guesses are not confirmed identities.')
    button(notebook, 'Compare with my shared memories', lambda: act('inspect'))
    names = directory(phone)
    target = ttk.Combobox(notebook, values=list(names), state='readonly'); target.pack(fill='x')
    if names: target.current(0)
    for title, kind in [('Choose my suspect', 'suspect'), ('Approach my suspect warmly', 'approach'), ('Ask directly', 'ask'), ('Accuse', 'accuse'), ('Share a copy / Ask a friend', 'share')]:
        button(notebook, title, lambda kind=kind: act(kind, names.get(target.get())))
    button(notebook, 'Leave this mystery alone', lambda: act('ignore'))
    clue = ttk.Entry(notebook); clue.pack(fill='x')
    for title, weight in [('Add supporting clue', 15), ('Add conflicting clue', -15)]:
        button(notebook, title, lambda weight=weight: mutate(phone,
            lambda: hearts.clue(s, ident, actor, names.get(target.get()), clue.get(), weight), refresh))
    label(notebook, 'Your main suspect: '+str(row['case']['selected'] or 'Undecided'))
    for suspect, score in row['case']['suspects'].items():
        label(notebook, f"{suspect.title()}: {'Likely' if score >= 60 else 'Possible' if score else 'Little support'}")
    for c in row['case']['clues']: label(notebook, f"{c['suspect'].title()} · {c['source']}: {c['text']}")

    import phone_theme
    phone_theme.apply_tree(frame)

def contact(phone, body, s, who):
    actor = s['player']; data = profiles.view(s, who, actor)
    refresh = lambda: phone.contact_detail(who)
    label(body, 'About & favourites')
    for field in profiles.FIELDS:
        label(body, field+': '+profiles.field_value(data, field, own=who == actor))
    if who == actor:
        label(body, 'You already know your established tastes and history. Editing what you share does not make your private history public.')
        field = ttk.Combobox(body, values=profiles.EDITABLE_FIELDS, state='readonly'); field.current(0); field.pack(fill='x')
        value = ttk.Combobox(body); value.pack(fill='x')
        visibility = ttk.Combobox(body, values=('public', 'private', 'selected'), state='readonly'); visibility.current(0); visibility.pack(fill='x')
        names = directory(phone)
        recipients = tk.Listbox(body, selectmode='multiple', exportselection=False, height=4)
        for name in names: recipients.insert('end', name)
        recipients.pack(fill='x')
        label(body, 'For selected visibility, choose the contacts allowed to see this field.')
        def load(event=None):
            p = profiles.ensure(s)['people'][actor]
            current = profiles.field_value(data, field.get(), own=True)
            value.delete(0, 'end'); value.insert(0, '' if current == 'Not set — add your preference' else current)
            value.configure(values=([path.stem[len(actor)+1:] for path in (core.ROOT/'assets/portraits').glob(actor+'-*.png')]
                                    if field.get() == 'Profile picture' else []))
            visibility.set(p['visibility'].get(field.get(), 'public'))
            recipients.selection_clear(0, 'end')
            for i, who in enumerate(names.values()):
                if who in p['shared'].get(field.get(), []): recipients.selection_set(i)
        field.bind('<<ComboboxSelected>>', load); load()
        button(body, 'Save profile field', lambda: mutate(phone, lambda: profiles.edit(s, actor, field.get(), value.get(), visibility.get(),
            [names[recipients.get(i)] for i in recipients.curselection()]), refresh))
        reference = ttk.Frame(body)
        def toggle_reference():
            if reference.winfo_children():
                for child in reference.winfo_children(): child.destroy()
            else:
                for title, text in data['self_reference'].items():
                    label(reference, title)
                    label(reference, text)
        button(body, 'Show / hide your full personal reference · Private', toggle_reference)
        reference.pack(fill='x')
    for title, key in [('Discovered details · attributed statements', 'discoveries'), ('Shared memories', 'memories'), ('Promises & plans · completion unconfirmed', 'promises')]:
        label(body, title)
        for r in data[key]: label(body, f"{stamp(r.get('minute'))} · {source_name(s, r.get('source'))} · {r.get('certainty', 'recorded')}\n{r['text']}")
    for field, fact in data['favourites'].items():
        label(body, f"Favourite {field.lower()}: {fact['value']} · {fact.get('provenance') or source_name(s, fact['source'])}")
    if data['details']:
        label(body, 'Personal details you have learned')
        for field, fact in data['details'].items():
            if not field.startswith('favourite:'):
                label(body, f"{field}: {fact['value']} · {stamp(fact.get('minute'))} · Self-reported")
    if who != actor:
        bond = core.town.character_stats(s, who)
        label(body, 'Relationship milestones')
        if bond.get('unresolved_harm'): label(body, 'Trust needs repair.')
        if bond.get('confessed_at') is not None: label(body, 'Shared a romantic confession.')
        for milestone in bond.get('milestones', []): label(body, milestone)
        for name, milestone_time in bond.get('firsts', {}).items(): label(body, f'First {name} · {milestone_time}')
    button(body, 'Open photo keepsakes in Gallery', lambda: phone.open_app('Gallery'))
    label(body, 'Private notebook · visible only to you')
    kind = ttk.Combobox(body, values=('Private note', 'Question', 'Memory', 'Keepsake', 'Promise', 'Plan'), state='readonly')
    kind.current(0); kind.pack(fill='x')
    text = ttk.Entry(body); text.pack(fill='x')
    button(body, 'Add to notebook', lambda: mutate(phone, lambda: profiles.add(s, actor, who, kind.get(), text.get()), refresh))
    for r in data['notebook']:
        label(body, f"{'★ ' if r['pinned'] else ''}{r['kind']}{' · Done' if r['done'] else ''}: {r['text']}")
        button(body, 'Unpin' if r['pinned'] else 'Pin', lambda ident=r['id']: mutate(phone, lambda: profiles.toggle(s, actor, who, ident, 'pinned'), refresh))
        if r['kind'] in ('Promise', 'Plan'):
            button(body, 'Toggle completed', lambda ident=r['id']: mutate(phone, lambda: profiles.toggle(s, actor, who, ident, 'done'), refresh))
    label(body, 'Anonymous investigations')
    for row in hearts.inbox(s, actor):
        if row['case']['selected'] == who or who in row['case']['suspects'] or row['sender'] == who:
            button(body, f"Thread {row['id']} · {'Confirmed' if row['sender'] == who else 'Unconfirmed'}", lambda ident=row['id']: thread(phone, ident))
