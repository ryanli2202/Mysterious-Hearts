"""Inline address-book controls; no extra desktop or dialog windows."""
from tkinter import ttk
import phone_numbers as numbers
from phone_controls import PhoneButton


def add_form(phone,frame,s):
    data=numbers.ensure(s)
    ttk.Label(frame,text='Your number · '+numbers.number(s,s['player'])).pack(anchor='w',pady=4)
    ttk.Label(frame,text='Add a contact by phone number').pack(anchor='w',pady=(8,2))
    entry=phone.contact_number_entry=ttk.Entry(frame)
    entry.insert(0,data['draft'])
    entry.pack(fill='x',pady=3)
    status=ttk.Label(frame,text='',wraplength=350)
    status.pack(fill='x',pady=3)
    phone.contact_number_status=status
    def add():
        data['draft']=entry.get()
        if phone.game.busy:
            status.configure(text='Wait for the current conversation to finish.');return
        try:who=numbers.add(s,entry.get())
        except ValueError as exc:
            status.configure(text=str(exc));return
        data['draft']=''
        entry.delete(0,'end')
        data['last_added']=who
        phone.game.persist();phone.game.render();phone.refresh()
    phone.add_number_action=add
    entry.bind('<Return>',lambda event:add())
    PhoneButton(frame,text='Add contact',command=add).pack(fill='x',pady=3)
    if data.get('last_added'):
        who=data['last_added']
        ttk.Label(frame,text='Saved · '+numbers.name(who)+' · '+numbers.saved_number(s,who),wraplength=350).pack(fill='x')


def local_contacts(phone,body,s):
    for who,item in numbers.ensure(s)['contacts'].items():
        if who in s['routes'] or who==s['player']:continue
        card=ttk.Frame(body,padding=12);card.pack(fill='x',pady=4)
        avatar=phone.avatars._avatar(who)
        if avatar: ttk.Label(card,image=avatar).pack(anchor='w',pady=(0,4))
        ttk.Label(card,text=numbers.name(who),font=('Segoe UI',13,'bold')).pack(anchor='w')
        ttk.Label(card,text='Town NPC · ordinary phone contact').pack(anchor='w')
        ttk.Label(card,text=numbers.format_number(item['number'])).pack(anchor='w',pady=4)
        PhoneButton(card,text='Message',command=lambda w=who:phone.open_thread('npc:'+w,True)).pack(fill='x',pady=4)
