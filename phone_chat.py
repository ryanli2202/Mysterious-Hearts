"""Compact phone conversation layout, with a fixed composer and options page."""
import tkinter as tk
from tkinter import ttk, messagebox
from phone_dialogs import AppWindow, messagebox, simpledialog
import phone_personalization as personal
from phone_controls import PhoneButton, MessageField
from messages_ui import MessageBubbles


def avatar_identity(state, key, is_group):
    if not is_group:
        return key
    chat = state['groups'][key]
    members = chat.get('members', [])
    return members[0] if chat.get('direct') and len(members) == 1 else None


def latest_message_minute(chat, texts):
    minutes = [r['minute'] for r in texts if isinstance(r.get('minute'), (int, float))]
    activity_minute = chat.get('inbox_activity', {}).get('minute')
    if isinstance(activity_minute, (int, float)): minutes.append(activity_minute)
    return max(minutes, default=None)


def inbox_time(minute, now):
    if minute is None: return ''
    import story_calendar
    hour, mins = divmod(int(minute) % 1440, 60)
    clock = f'{hour % 12 or 12}:{mins:02d} {"AM" if hour < 12 else "PM"}'
    days = int(now)//1440 - int(minute)//1440
    if days == 0: return clock
    if days == 1: return 'Yesterday\n' + clock
    return story_calendar.story_date(minute).strftime('%d %b') + '\n' + clock


def inbox_sort_key(row, records, pinned_chats):
    key, is_group, chat, name = row
    texts = [r for r in records if r['who'] == key and r['group'] == is_group]
    minute = latest_message_minute(chat, texts)
    activity = chat.get('inbox_activity', {})
    return ((('group:' if is_group else 'route:')+key) not in pinned_chats,
            -(minute if minute is not None else -1), -activity.get('order', 0), not bool(texts), name.casefold(), key)


def inbox(phone, frame, s):
    import phone_apps as apps
    import groups
    phone._inbox_unread_stamp=phone.unread_stamp()
    title=ttk.Frame(frame); title.pack(fill='x',pady=(2,12))
    ttk.Label(title,text='Messages',font=('Segoe UI',27,'bold')).pack(side='left')
    PhoneButton(title,text='+',width=3,command=phone.game.new_text_group).pack(side='right')
    query=tk.StringVar(value=getattr(phone,'inbox_query',''))
    search=ttk.Entry(frame,textvariable=query,font=('Segoe UI',12)); search.pack(fill='x',ipady=7)
    ttk.Label(frame,text='Search contacts and conversations',foreground='#93939a',font=('Segoe UI',9)).pack(anchor='w',pady=(3,8))
    filters=ttk.Frame(frame); filters.pack(fill='x',pady=(0,8))
    unread=tk.BooleanVar(value=getattr(phone,'only_unread',False))
    ttk.Checkbutton(filters,text='Unread',variable=unread,command=lambda:render()).pack(side='left')
    PhoneButton(filters,text='📌 Saved',command=lambda:phone.open_app('Pinned messages')).pack(side='right')
    body=phone.scroll_area(frame)
    def render(*args):
        phone.inbox_query=query.get(); phone.only_unread=unread.get()
        for child in body.winfo_children(): child.destroy()
        groups.sync_contacts(s)
        data=personal.ensure(s)
        rows=[(key,False,s['routes'][key],personal.name(s,key)) for key in apps.contacts(s)]
        rows += [(key,True,g,g['name']) for key,g in s['groups'].items() if g.get('channel')=='text']
        records=personal.records(s)
        rows.sort(key=lambda row:inbox_sort_key(row,records,data['pinned_chats']))
        shown=0
        for key,is_group,chat,name in rows:
            if query.get().casefold() not in name.casefold() or (unread.get() and not chat.get('unread')): continue
            shown+=1
            row=ttk.Frame(body,padding=(2,12)); row.pack(fill='x')
            avatar=phone.avatars._avatar(avatar_identity(s, key, is_group))
            picture=ttk.Label(row,image=avatar,text='◉' if not avatar else '',width=4)
            picture.pack(side='left',padx=(0,10))
            detail=ttk.Frame(row); detail.pack(fill='x',expand=True)
            pinned=(('group:' if is_group else 'route:')+key) in data['pinned_chats']
            texts=[r for r in records if r['who']==key and r['group']==is_group]
            heading_row=ttk.Frame(detail); heading_row.pack(fill='x')
            timestamp=ttk.Label(heading_row,text=inbox_time(latest_message_minute(chat,texts),s['world']['minute']),
                                foreground='#93939a',font=('Segoe UI',9),justify='right')
            timestamp.pack(side='right',padx=(6,0))
            heading=ttk.Label(heading_row,text=('● ' if chat.get('unread') else '')+name+('  📌' if pinned else ''),font=('Segoe UI',12,'bold'))
            heading.pack(side='left',fill='x',expand=True)
            preview=texts[-1]['text'] if texts else 'Start a conversation'
            preview=' '.join(preview.split()); preview=preview[:80]+('…' if len(preview)>80 else '')
            subtitle=ttk.Label(detail,text=preview,foreground='#93939a',wraplength=max(120,phone.winfo_width()-150))
            subtitle.pack(anchor='w',pady=(4,0))
            def menu(event,key=key,is_group=is_group,pinned=pinned):
                options=tk.Menu(phone,tearoff=False)
                options.add_command(label='Unpin conversation' if pinned else 'Pin conversation',command=lambda:phone.pin_chat(key,is_group))
                phone.inbox_menu=options
                try: options.tk_popup(event.x_root,event.y_root)
                finally: options.grab_release()
            for widget in (row,picture,detail,heading_row,heading,timestamp,subtitle):
                widget.bind('<Button-1>',lambda e,key=key,is_group=is_group:phone.open_thread(key,is_group))
                widget.bind('<Button-3>',menu)
            row.configure(takefocus=True)
            row.bind('<Return>',lambda e,key=key,is_group=is_group:phone.open_thread(key,is_group))
            row.bind('<space>',menu)
            ttk.Separator(body).pack(fill='x',padx=(55,0))
        if not shown: ttk.Label(body,text='No matching conversations.').pack(pady=20)
        phone.fit_wrapping(body)
    query.trace_add('write',render); render()


def build(phone, frame, s):
    if not phone.thread: return phone.inbox(frame,s)
    key,is_group=phone.thread
    name=s['groups'][key]['name'] if is_group else personal.name(s,key)
    header=ttk.Frame(frame); header.pack(fill='x',pady=(0,6))
    PhoneButton(header,text='‹',width=3,command=lambda:phone.open_app('Messages')).pack(side='left')
    PhoneButton(header,text='•••',width=3,command=lambda:toggle_options(phone)).pack(side='right')
    identity=ttk.Frame(header); identity.pack(fill='x',expand=True)
    avatar=phone.avatars._avatar(avatar_identity(s, key, is_group))
    if avatar: ttk.Label(identity,image=avatar,anchor='center').pack(fill='x')
    ttk.Label(identity,text=name,anchor='center',font=('Segoe UI',13,'bold')).pack(fill='x')
    phone.availability_label=ttk.Label(frame,anchor='center',font=('Segoe UI',9),foreground='#93939a')
    phone.availability_label.pack(fill='x',pady=(0,4))
    phone.chat_pins=PhoneButton(frame,text='Pinned messages',command=lambda:show_pins(phone))
    phone.chat_pins.pack(fill='x',pady=(0,4))
    # Pack the composer first at the bottom, so it cannot be squeezed offscreen.
    composer=ttk.Frame(frame); composer.pack(side='bottom',fill='x',pady=(8,0))
    phone.photo_attachment=PhoneButton(frame,text='',command=lambda:remove_photo(phone))
    phone.photo_attachment.pack(side='bottom',fill='x')
    phone.message_composer=composer
    phone.emoji_keyboard_visible=False
    phone.message_emoji=PhoneButton(composer,text='+',width=3,command=lambda:toggle_options(phone))
    phone.message_emoji.pack(side='left',padx=(0,4))
    phone.message_send=PhoneButton(composer,icon='send',command=phone.send_message)
    phone.message_send.pack(side='right',padx=(4,0))
    field=MessageField(composer); field.pack(fill='x',expand=True)
    phone.message_entry=field.entry
    stamp=('group:' if is_group else 'route:')+key
    phone.message_draft_key=stamp
    phone.message_entry.insert(0,s.get('drafts',{}).get(stamp,''))
    phone.message_entry.bind('<Return>',lambda e:phone.send_message())
    phone.message_entry.bind('<KeyRelease>',lambda e:phone.update_messages())
    phone.chat_area=ttk.Frame(frame); phone.chat_area.pack(fill='both',expand=True)
    phone.phone_messages=MessageBubbles(phone.chat_area,bg='#17171b')
    phone.phone_messages.phone_state=s
    phone.phone_messages.iphone=True
    phone.phone_messages.on_message_action=lambda i,e:message_menu(phone,i,e)
    phone.phone_messages.pack(fill='both',expand=True)
    phone.chat_options=ttk.Frame(phone.chat_area)
    options=phone.scroll_area(phone.chat_options)
    PhoneButton(options,text='Done',command=lambda:toggle_options(phone,False)).pack(fill='x',pady=4)
    phone.message_status=ttk.Label(options,wraplength=300); phone.message_status.pack(fill='x',pady=4)
    phone.suggestion_actions=ttk.Frame(options); phone.suggestion_actions.pack(fill='x')
    phone.suggest_replies=PhoneButton(phone.suggestion_actions,text='Suggest replies',command=lambda:phone.game.request_suggestions('personal' if phone.personal_messages else 'main'))
    phone.suggest_replies.pack(fill='x',pady=2)
    phone.suggestions_toggle=PhoneButton(phone.suggestion_actions,command=phone.toggle_message_suggestions)
    phone.suggestions_toggle.pack(fill='x',pady=2)
    phone.suggestions_panel=ttk.Frame(options)
    phone.regular_suggestions=PhoneButton(phone.suggestions_panel,text='Regular suggestions',command=lambda:phone.set_message_mode(False))
    phone.regular_suggestions.pack(fill='x',pady=2)
    phone.personal_suggestions=PhoneButton(phone.suggestions_panel,text='Personal suggestions',command=lambda:phone.set_message_mode(True))
    phone.personal_suggestions.pack(fill='x',pady=2)
    import character_types
    participants = s['groups'][key]['members'] if is_group else [key]
    if participants and all(character_types.is_town(who) for who in participants):
        phone.personal_messages = False
        phone.personal_suggestions.pack_forget()
    phone.message_choices=[]
    for index in range(4):
        button=tk.Button(phone.suggestions_panel,text='',anchor='w',justify='left',wraplength=280,
                         bg='#2c2c2e',fg='#dce4ed',relief='flat',padx=10,pady=8,
                         command=lambda i=index:phone.send_message(choice=i))
        button.pack(fill='x',pady=3); phone.message_choices.append(button)
    from emoji_ui import EmojiKeyboard
    phone.emoji_keyboard=EmojiKeyboard(options,phone.message_entry,phone.save_emoji_draft,phone.toggle_emoji_keyboard)
    PhoneButton(options,text='Attach photo from Gallery',command=lambda:choose_photo(phone)).pack(fill='x',pady=4)
    PhoneButton(options,text='Emoji keyboard',command=phone.toggle_emoji_keyboard).pack(fill='x',pady=4)
    phone.message_clear=PhoneButton(options,text='Clear draft',command=phone.clear_message); phone.message_clear.pack(fill='x',pady=2)
    phone.incoming_photo_status=ttk.Label(options,wraplength=280)
    phone.incoming_photo_status.pack(fill='x',pady=2)
    PhoneButton(options,text='Retry incoming photos',command=phone.game.message_pump.photos.retry).pack(fill='x',pady=2)
    phone.message_retry=PhoneButton(options,text='Continue / retry',command=phone.game.retry_or_begin); phone.message_retry.pack(fill='x',pady=2)
    phone.cancel_response=PhoneButton(options,text='Pause reply',command=lambda:phone.game.message_pump.cancel(*phone.thread)); phone.cancel_response.pack(fill='x',pady=2)
    PhoneButton(options,text='Wait / sleep',command=lambda:__import__('autonomy_ui').open_window(phone.game)).pack(fill='x',pady=2)
    PhoneButton(options,text='Search messages',command=lambda:phone.open_app('Pinned messages')).pack(fill='x',pady=2)
    phone.response_preview=ttk.Label(options,wraplength=300); phone.response_preview.pack(fill='x')
    phone.chat_options_visible=False
    phone.message_stamp=None
    phone.apply_message_suggestions_visibility(); phone.update_messages()
    phone.phone_messages.yview_moveto(s.get('conversation_scroll',{}).get(stamp,1))


def toggle_options(phone, visible=None):
    phone.chat_options_visible=not phone.chat_options_visible if visible is None else visible
    if phone.chat_options_visible:
        phone.phone_messages.pack_forget(); phone.chat_options.pack(fill='both',expand=True)
    else:
        phone.chat_options.pack_forget(); phone.phone_messages.pack(fill='both',expand=True)
        phone.message_entry.focus_set()


def bind_records(phone, messages):
    s=phone.game.state_data; key,is_group=phone.thread
    rows=[r for r in personal.records(s) if r['who']==key and r['group']==is_group]
    index=0; ids=[]
    for message in messages:
        if message[2]=='status': ids.append(None); continue
        if index<len(rows) and rows[index]['text']==message[1] and rows[index]['kind']==message[2]:
            ids.append(rows[index]['id']); index+=1
        else: ids.append(None)  # Uncommitted/pending text cannot be pinned.
    phone.phone_messages.message_ids=ids
    phone.phone_messages.pinned_ids=set(personal.ensure(s)['pins'])
    local=[r for r in rows if r['id'] in personal.ensure(s)['pins']]
    phone.chat_pins.config(text=f'📌 {len(local)} pinned in this chat  ·  {len(personal.ensure(s)["pins"])}/3 total  ›')


def toggle_pin(phone, ident):
    s=phone.game.state_data
    try:
        (personal.unpin if ident in personal.ensure(s)['pins'] else personal.pin)(s,ident)
    except ValueError as exc:
        messagebox.showinfo('Pinned messages',str(exc),parent=phone); return
    phone.game.persist(); phone.message_stamp=None; phone.update_messages()


def message_menu(phone, index, event):
    view=phone.phone_messages
    if index>=len(view.messages): return
    ident=view.message_ids[index] if index<len(view.message_ids) else None
    menu=tk.Menu(phone,tearoff=False,bg='#2c2c2e',fg='#dce4ed',activebackground='#0a84ff')
    if ident:
        menu.add_command(label='Unpin message' if ident in view.pinned_ids else 'Pin message',command=lambda:toggle_pin(phone,ident))
    photo=view.messages[index][6] if len(view.messages[index])>6 else None
    if photo:
        from camera_ui import show_photo
        menu.add_command(label='View photo',command=lambda:show_photo(phone,photo))
    menu.add_command(label='Copy text',command=lambda:(phone.clipboard_clear(),phone.clipboard_append(view.messages[index][1])))
    phone.message_context_menu=menu
    try: menu.tk_popup(event.x_root,event.y_root)
    finally: menu.grab_release()


def show_pins(phone):
    s=phone.game.state_data; key,is_group=phone.thread
    rows=[r for r in personal.records(s) if r['id'] in personal.ensure(s)['pins'] and r['who']==key and r['group']==is_group]
    menu=tk.Menu(phone,tearoff=False)
    for row in rows:
        menu.add_command(label=row['text'][:65],command=lambda ident=row['id']:jump(phone,ident))
    if not rows: menu.add_command(label='Tap a message to pin it',state='disabled')
    menu.add_separator(); menu.add_command(label='Manage all three pins…',command=lambda:phone.open_app('Pinned messages'))
    phone.pins_menu=menu
    try: menu.tk_popup(phone.chat_pins.winfo_rootx(),phone.chat_pins.winfo_rooty()+38)
    finally: menu.grab_release()


def jump(phone,ident):
    toggle_options(phone,False)
    view=phone.phone_messages
    if ident in view.message_ids:
        index=view.message_ids.index(ident); bounds=view.bbox(f'message:{index}')
        if bounds:
            region=list(map(float,view.cget('scrollregion').split()))
            view.yview_moveto(max(0,bounds[1]-20)/max(1,region[3]))


def remove_photo(phone):
    phone.game.state_data.setdefault('photo_drafts', {}).pop(phone.message_draft_key, None)
    phone.game.persist()
    phone.update_messages()


def choose_photo(phone):
    import camera
    from PIL import Image, ImageOps, ImageTk
    s = phone.game.state_data
    draft_key = phone.message_draft_key
    window = AppWindow(phone)
    window.title('Attach photo')
    window.geometry('340x500')
    window.images = []
    ttk.Label(window, text='Choose a Gallery photo', font=('Segoe UI', 16, 'bold')).pack(pady=12)
    body = phone.scroll_area(window)
    try:
        records = camera.photos(s)
    except (OSError, ValueError):
        records = []
    count = 0
    for record in records:
        try:
            with Image.open(camera.photo_path(record)) as source:
                picture = ImageOps.exif_transpose(source).convert('RGB')
                picture.thumbnail((240, 160))
            thumbnail = ImageTk.PhotoImage(picture, master=window)
        except (OSError, ValueError, KeyError):
            continue
        count += 1
        window.images.append(thumbnail)
        def select(record=record):
            s.setdefault('photo_drafts', {})[draft_key] = record['id']
            phone.game.persist()
            window.destroy()
            if phone.message_draft_key == draft_key:
                toggle_options(phone, False)
                phone.update_messages()
        ttk.Button(body, image=thumbnail, text=record.get('mode', 'Photo')+' · '+record.get('location', ''),
                   compound='top', command=select).pack(fill='x', pady=6)
    if not count:
        ttk.Label(body, text='No photos available. Take a photo in Camera first.', wraplength=270).pack(pady=24)
    PhoneButton(window, text='Cancel', command=window.destroy).pack(pady=8)
