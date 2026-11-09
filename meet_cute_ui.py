"""Meet-Cute's phone profile editor, discovery feed, likes and private match chats."""
from datetime import timedelta
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageOps, ImageTk

import meet_cute as app
import camera
import story_calendar
import town
from lifestyle_ui import Screen
from phone_controls import PhoneButton
import meet_cute_widgets as design
from phone_dialogs import AppWindow


class ProfilePhotos(ttk.Frame):
    """One profile's carousel; pointer drags and keyboard/buttons share navigation."""
    def __init__(self, parent, paths, positions, who):
        super().__init__(parent, style='PhoneDark.Meet.Base.TFrame')
        self.paths, self.positions, self.who = paths, positions, who
        self.index = positions.get(who, 0) % len(paths)
        self.drag_start = None
        self.picture = ttk.Label(self, anchor='center', takefocus=True, style='PhoneDark.Meet.Base.Body.TLabel')
        self.picture.pack(fill='x', pady=6)
        controls = ttk.Frame(self, style='PhoneDark.Meet.Base.TFrame')
        controls.pack(fill='x')
        self.previous = design.button(controls, '‹', lambda:self.move(-1))
        self.previous.pack(side='left')
        self.counter = ttk.Label(controls, anchor='center', style='PhoneDark.Meet.Base.Muted.TLabel')
        self.counter.pack(side='left', expand=True, fill='x')
        self.next = design.button(controls, '›', lambda:self.move(1))
        self.next.pack(side='right')
        self.bind('<Configure>', self.resize)
        self.picture.bind('<ButtonPress-1>', self.press)
        self.picture.bind('<ButtonRelease-1>', self.release)
        self.picture.bind('<Left>', lambda event:self.move(-1))
        self.picture.bind('<Right>', lambda event:self.move(1))
        if len(paths) == 1:
            self.previous.configure(state='disabled')
            self.next.configure(state='disabled')
        self.show()

    def resize(self, event):
        width = max(180, min(event.width, 520))
        if width != getattr(self, '_image_width', None):
            self._image_width = width
            self.show()

    def press(self, event):
        self.picture.focus_set()
        self.drag_start = (event.x_root, event.y_root)

    def release(self, event):
        if self.drag_start is None:
            return
        dx, dy = event.x_root-self.drag_start[0], event.y_root-self.drag_start[1]
        self.drag_start = None
        if abs(dx) >= 40 and abs(dx) > abs(dy):
            self.move(1 if dx < 0 else -1)

    def move(self, step):
        self.index = (self.index+step) % len(self.paths)
        self.show()
        return 'break'

    def show(self):
        self.positions[self.who] = self.index
        try:
            with Image.open(self.paths[self.index]) as source:
                width = getattr(self, '_image_width', 300)
                image = ImageTk.PhotoImage(ImageOps.contain(source.convert('RGB'), (width, int(width*1.08))), master=self)
            self.picture.configure(image=image, text='')
            self.picture.image = image
        except (OSError, ValueError):
            self.picture.configure(image='', text='Profile photo unavailable.')
            self.picture.image = None
        self.counter.configure(text='  '.join('●' if i==self.index else '○' for i in range(len(self.paths)))
                               +f'   {self.index+1}/{len(self.paths)}')


class MeetCuteScreen(Screen):
    def __init__(self, phone, frame, state):
        self.phone, self.s, self.root = phone, state, frame
        self.data = app.ensure(state)
        self.tab = self.data.setdefault('tab', 'Profile' if not self.data['profile'] else 'Discover')
        self.who_selected = self.data.get('selected_match')
        key = self.tab+(':'+self.who_selected if self.tab in ('Chat','Character') and self.who_selected else '')
        self.draft = self.data['drafts'].setdefault(key, {})
        self.fields = {}
        design.install(frame)
        frame.configure(style='PhoneDark.Meet.Base.TFrame', padding=8)
        phone.meet_cute_view = self
        header=ttk.Frame(frame, style='PhoneDark.Meet.Base.TFrame');header.pack(fill='x')
        design.button(header,'Filters',lambda:self.go('Preferences')).pack(side='right')
        design.label(header,'meet-cute','Title')
        tabs = ttk.Frame(frame, style='PhoneDark.Meet.Base.TFrame'); tabs.pack(side='bottom',fill='x',pady=(8,0))
        active = 'Matches' if self.tab in ('Chat','Character') else self.tab
        for i, (name, title) in enumerate((('Discover','Discover'),('Likes','Likes'),('Matches','Chats'),('Profile','You'))):
            design.button(tabs,title,lambda n=name:self.go(n),active==name).grid(row=0,column=i,sticky='ew',padx=1)
            tabs.columnconfigure(i,weight=1,uniform='navigation')
        self.dock=ttk.Frame(frame,style='PhoneDark.Meet.Base.TFrame')
        self.dock.pack(side='bottom',fill='x',pady=(5,0))
        self.status = ttk.Label(frame, text='', wraplength=320, style='PhoneDark.Meet.Base.Muted.TLabel')
        self.status.pack(fill='x')
        self.scroller=design.Scroll(frame);self.scroller.pack(fill='both',expand=True)
        self.body = self.scroller.body
        if self.data['paused']: self.label('Discovery paused · Existing matches can still talk.')
        if self.data['exclusive_with']: self.label('Exclusive with '+camera.name(self.data['exclusive_with']))
        {'Discover':self.discover, 'Likes':self.likes, 'Matches':self.matches, 'Profile':self.profile,
         'Preferences':self.preferences, 'Chat':self.chat, 'Character':self.character}.get(self.tab,self.discover)()
        phone.meet_cute_stamp = self.data['revision']
        self.scroller.connect()
        self.scroll_key=key+(':'+getattr(self,'discovery_who','') if self.tab=='Discover' else '')
        position=self.data.setdefault('scroll_positions',{}).get(self.scroll_key,0)
        def restore_scroll():
            if self.scroller.winfo_exists():
                self.scroller.update_idletasks()
                self.scroller.canvas.yview_moveto(position)
        self.root.after_idle(restore_scroll)

    def capture(self):
        super().capture()
        if hasattr(self,'scroll_key') and self.scroller.winfo_exists():
            self.data.setdefault('scroll_positions',{})[self.scroll_key]=self.scroller.canvas.yview()[0]

    def label(self,value,heading=False):
        return design.label(self.body,value,'Heading' if heading else 'Body')

    def button(self,title,callback):
        widget=design.button(self.body,title,callback)
        widget.pack(fill='x',pady=5)
        return widget

    def field(self,key,default='',values=None,multiline=False):
        field=super().field(key,default,values,multiline)
        if multiline:
            field.configure(height=3,bg=design.CARD,fg=design.INK,insertbackground=design.INK,
                            relief='flat',padx=12,pady=10,highlightthickness=1,highlightbackground='#514052')
            field.bind('<KeyRelease>',lambda e:self.update_completion() if hasattr(self,'completion') else None)
        return field

    def section(self,title,subtitle=''):
        box=ttk.Frame(self.body,padding=14,style='PhoneDark.Meet.Card.TFrame')
        box.pack(fill='x',pady=(12,8))
        design.label(box,title,'Heading',True)
        if subtitle:design.label(box,subtitle,'Muted',True)
        return box

    def go(self, tab, who=None):
        self.capture()
        self.data['tab'] = tab
        if who: self.data['selected_match'] = who
        self.phone.refresh()

    def do(self, fn, *args, clear=()):
        self.capture()
        if self.phone.game.busy:
            self.status.configure(text='Wait for the current conversation to finish.')
            return
        try: fn(self.s,*args)
        except ValueError as exc:
            self.status.configure(text=str(exc))
            return
        for key in clear:
            self.draft[key]=''
            f=self.fields.get(key)
            if isinstance(f,tk.Text): f.delete('1.0','end')
            elif f is not None: f.delete(0,'end')
        self.phone.game.persist()
        self.phone.game.render()
        self.phone.refresh()

    def photo(self, path):
        try:
            with Image.open(path) as source:
                image=ImageTk.PhotoImage(ImageOps.contain(source.convert('RGB'),(275,260)),master=self.body)
            label=ttk.Label(self.body,image=image); label.image=image
            label.pack(pady=6)
        except (OSError,ValueError): self.label('Profile photo unavailable.')

    def profile(self):
        identity=app.identity(self.s['player'])
        saved=self.data['profile'] or {}
        design.label(self.body,'Make it feel like you.','Title')
        self.completion=design.label(self.body,'','Muted')
        self.editor_root=self.body
        modes=ttk.Frame(self.body,style='PhoneDark.Meet.Base.TFrame');modes.pack(fill='x',pady=6)
        design.button(modes,'Edit profile',lambda:self.profile_mode(False)).pack(side='left',fill='x',expand=True,padx=2)
        design.button(modes,'Preview',lambda:self.profile_mode(True)).pack(side='left',fill='x',expand=True,padx=2)
        self.editor=ttk.Frame(self.body,style='PhoneDark.Meet.Base.TFrame');self.editor.pack(fill='x')
        self.preview=ttk.Frame(self.body,style='PhoneDark.Meet.Base.TFrame')
        self.body=self.editor
        self.label('01  Your photos',True)
        design.label(self.body,'Add up to three. Tap a photo to change it.','Muted')
        self.photo_choices={'None':''}
        self.available_photos=app.photos(self.s)
        for ident,record in self.available_photos.items():
            self.photo_choices[record['label']+' · '+ident]=ident
        self.photo_slots=[]
        slots=ttk.Frame(self.body,style='PhoneDark.Meet.Base.TFrame');slots.pack(fill='x',pady=8)
        for i in range(3):
            ident=saved.get('photos',['portrait'])[i] if i<len(saved.get('photos',['portrait'])) else ''
            default=next((label for label,value in self.photo_choices.items() if value==ident),'None')
            field=ttk.Combobox(self.body,values=list(self.photo_choices),state='readonly')
            field.set(self.draft.get(f'Photo {i+1}',default))
            self.fields[f'Photo {i+1}']=field
            slot=design.button(slots,'',lambda n=i:self.pick_photo(n))
            slot.grid(row=0,column=i,sticky='nsew',padx=3)
            slots.columnconfigure(i,weight=1,uniform='photos')
            self.photo_slots.append(slot)
            self.refresh_slot(i)
        self.label('02  The essentials',True)
        design.label(self.body,f'{identity["name"]} · {identity["age"]} · {identity["orientation"]} · Winterfield','Muted')
        self.field('Bio',saved.get('bio',''),multiline=True)
        self.field('Looking for',saved.get('intention',app.INTENTIONS[0]),values=app.INTENTIONS)
        self.field('Availability',saved.get('availability','Evenings'),values=('Mornings','Afternoons','Evenings','Flexible'))
        self.field('Show occupation','Yes' if saved.get('show_job',True) else 'No',values=('Yes','No'))
        self.label('03  Your interests',True)
        design.label(self.body,'A few things you could talk about for hours.','Muted')
        selected=saved.get('interests',[])
        self.interest_keys=[]
        for i in range(min(5,len(app.interest_options(self.s)))):
            key=f'Interest {i+1}';self.interest_keys.append(key)
            field=self.field(key,selected[i] if i<len(selected) else '',values=('',*app.interest_options(self.s)))
            field.bind('<<ComboboxSelected>>',lambda e:self.update_completion())
        self.label('04  Give them an opening',True)
        design.label(self.body,'Three prompts. Three ways to start something.','Muted')
        for i,prompt in enumerate(app.PROMPTS):
            self.field(prompt,saved.get('answers',app.HOOKS[self.s['player']])[i],multiline=True)
        self.button('Resume discovery' if self.data['paused'] else 'Pause discovery',lambda:self.do(app.pause,not self.data['paused']))
        self.body=self.editor_root
        design.button(self.dock,'Save & publish profile',self.save_profile,True).pack(fill='x')
        self.update_completion()

    def update_completion(self):
        if not hasattr(self,'interest_keys'):return
        photos=sum(bool(self.photo_choices.get(self.get(f'Photo {i+1}'))) for i in range(3))
        prompts=sum(bool(self.get(k).strip()) for k in app.PROMPTS if k in self.fields)
        bio=bool(self.get('Bio').strip()) if 'Bio' in self.fields else False
        interests=any(self.get(k) for k in self.interest_keys)
        done=int(photos>0)+int(prompts==3)+int(bio)+int(interests)
        self.completion.configure(text=f'{done}/4 essentials ready · {photos}/3 photos · {prompts}/3 prompts')

    def refresh_slot(self,index):
        slot=self.photo_slots[index]
        record=self.available_photos.get(self.photo_choices.get(self.get(f'Photo {index+1}')))
        image=None
        if record:
            try:
                with Image.open(record['path']) as source:
                    image=ImageTk.PhotoImage(ImageOps.fit(source.convert('RGB'),(76,96)),master=slot)
            except (OSError,ValueError):pass
        slot.configure(image=image or '',compound='top',text=('Cover' if index==0 else f'Photo {index+1}') if image else '+ Add photo')
        slot.image=image

    def pick_photo(self,index):
        picker=AppWindow(self.root);picker.title(f'Choose photo {index+1}')
        design.label(picker,'Your photos','Title')
        design.label(picker,'From your Grove gallery and generated images.','Muted')
        def choose(ident):
            label=next(k for k,v in self.photo_choices.items() if v==ident)
            self.fields[f'Photo {index+1}'].set(label)
            self.refresh_slot(index);self.update_completion();self.capture()
            picker.destroy()
        design.button(picker,'Remove photo',lambda:choose('')).pack(fill='x',padx=8,pady=6)
        grid=ttk.Frame(picker,style='PhoneDark.Meet.Base.TFrame');grid.pack(fill='x',padx=8)
        for i,(ident,record) in enumerate(self.available_photos.items()):
            cell=design.button(grid,('Grove' if ident.startswith('grove:') else 'Gallery')+f' · Photo {i+1}',lambda value=ident:choose(value))
            try:
                with Image.open(record['path']) as source:
                    image=ImageTk.PhotoImage(ImageOps.fit(source.convert('RGB'),(128,132)),master=cell)
                cell.configure(image=image,compound='top');cell.image=image
            except (OSError,ValueError):pass
            cell.grid(row=i//2,column=i%2,sticky='nsew',padx=3,pady=4)
            grid.columnconfigure(i%2,weight=1,uniform='picker')
        self.photo_picker=picker

    def profile_mode(self,preview):
        self.capture()
        self.scroller.canvas.yview_moveto(0)
        if not preview:
            self.preview.pack_forget();self.editor.pack(fill='x');return
        self.editor.pack_forget()
        for child in self.preview.winfo_children():child.destroy()
        self.preview.pack(fill='x')
        identity=app.identity(self.s['player'])
        design.label(self.preview,f'{identity["name"]}, {identity["age"]}','Title')
        paths=[self.available_photos[ident]['path'] for i in range(3)
               if (ident:=self.photo_choices.get(self.get(f'Photo {i+1}'))) in self.available_photos]
        if paths:ProfilePhotos(self.preview,paths,{},'preview').pack(fill='x')
        else:design.label(self.preview,'Add a photo to introduce yourself.','Muted')
        design.label(self.preview,self.get('Bio') or 'Your introduction goes here.','Answer')
        if self.get('Show occupation')=='Yes':design.label(self.preview,identity['occupation'],'Muted')
        design.label(self.preview,self.get('Looking for')+' · '+self.get('Availability'),'Muted')
        design.label(self.preview,identity['orientation'],'Muted')
        design.label(self.preview,' · '.join(self.get(k) for k in self.interest_keys if self.get(k)),'Muted')
        for prompt in app.PROMPTS:
            panel=ttk.Frame(self.preview,style='PhoneDark.Meet.Card.TFrame',padding=16);panel.pack(fill='x',pady=8)
            design.label(panel,prompt,'Muted',True)
            design.label(panel,self.get(prompt) or 'Your answer goes here.','Answer',True)
        self.scroller.connect(self.preview)

    def preview_photos(self):
        self.profile_mode(True)

    def save_profile(self):
        self.do(app.publish,self.get('Bio'),[self.get(k) for k in self.interest_keys if self.get(k)],
                [self.get(k) for k in app.PROMPTS],
                [self.photo_choices[self.get(f'Photo {i+1}')] for i in range(3) if self.photo_choices[self.get(f'Photo {i+1}')]],
                self.get('Looking for'),self.get('Availability'),self.get('Show occupation')=='Yes')

    def preferences(self):
        p=self.data['preferences']
        self.label('Your orientation: '+app.identity(self.s['player'])['orientation'],True)
        self.label('Discovery only shows mutually compatible orientations. These filters narrow that selection; they cannot override anyone’s sexuality.')
        self.label('Age and gender always filter discovery. “Must have” also filters intention, shared interest and neighbourhood; “Preferred” ranks those instead. Neighbourhood is a profile detail, not live tracking.')
        self.field('Minimum age',str(p['min_age']),values=[str(i) for i in range(18,101)])
        self.field('Maximum age',str(p['max_age']),values=[str(i) for i in range(18,101)])
        self.field('Who to meet',p['gender'],values=('Everyone','Women','Men'))
        self.field('Relationship intention',p['intention'],values=app.INTENTIONS)
        self.field('Shared interest',p['interest'],values=('',*app.interest_options(self.s)))
        self.field('Distance',p['distance'],values=('Anywhere in Winterfield','Nearby neighbourhood'))
        self.field('Matching these preferences',p['mode'],values=('Must have','Preferred'))
        self.button('Save preferences',lambda:self.do(app.preferences,int(self.get('Minimum age')),int(self.get('Maximum age')),
                    self.get('Who to meet'),self.get('Relationship intention'),self.get('Matching these preferences'),
                    self.get('Shared interest'),self.get('Distance')))

    def card(self,who,interactive=False):
        p=app.public_profile(self.s,who)
        design.label(self.body,p['name'],'Title')
        design.label(self.body,f'{p["age"]} · {p["neighbourhood"]}','Muted')
        carousel = ProfilePhotos(self.body, p['photos'], self.data.setdefault('photo_positions', {}), who)
        carousel.pack(fill='x', pady=6)
        if interactive:self.button('♡  Like this photo',lambda:self.select_like(who,'Photo'))
        facts=self.section('A little about me')
        design.label(facts,p['occupation'],'Body',True)
        design.label(facts,p['orientation'],'Body',True)
        design.label(facts,p['intention'],'Body',True)
        design.label(facts,' · '.join(p['interests']),'Muted',True)
        for prompt,answer in p['prompts']:
            panel=self.section(prompt)
            design.label(panel,answer,'Answer',True)
            if interactive:
                design.button(panel,'♡',lambda target=prompt:self.select_like(who,target)).pack(anchor='e')
        design.label(self.body,p['activity'],'Muted')

    def select_like(self,who,target):
        name=app.identity(who)['name']
        self.fields[f'Like on {name}'].set(target)
        self.like_heading.configure(text='Your like · '+target)
        self.root.update_idletasks()
        height=max(1,self.body.winfo_height())
        self.scroller.canvas.yview_moveto(self.composer.winfo_y()/height)
        self.fields[f'Message to {name}'].focus_set()

    def character(self):
        self.card(self.who_selected)
        design.button(self.dock,'Back to conversation',lambda:self.go('Chat',self.who_selected)).pack(fill='x')

    def discover(self):
        if not self.data['profile']:
            design.label(self.body,'A little you.\nA real beginning.','Title')
            self.label('Build your profile with photos, interests and three conversation starters.')
            self.button('Create my profile',lambda:self.go('Profile'))
            return
        profiles=app.feed(self.s)
        if not profiles:
            design.label(self.body,'You’re all caught up.','Title')
            self.label('New possibilities arrive with a new story day. You can also adjust your preferences.')
            self.button('Discovery preferences',lambda:self.go('Preferences'))
            if self.data['paused'] and not self.data['exclusive_with']:
                self.button('Resume discovery',lambda:self.do(app.pause,False))
            return
        p=profiles[0];who=p['who'];self.discovery_who=who
        design.label(self.body,f'Discover · {len(profiles)} in today’s selection','Muted')
        self.card(who,True)
        self.composer=self.section('Make the first move','A thoughtful comment gives them something to reply to.')
        old=self.body;self.body=self.composer
        self.like_heading=design.label(self.body,'Your like · Photo','Heading',True)
        target=f'Like on {p["name"]}';message=f'Message to {p["name"]}'
        field=ttk.Combobox(self.body,values=('Photo',*app.PROMPTS),state='readonly')
        field.set(self.draft.get(target,'Photo'));self.fields[target]=field
        self.like_heading.configure(text='Your like · '+field.get())
        self.field(message,multiline=True)
        self.button('Send like',lambda:self.do(app.like,who,self.get(target),self.get(message)))
        self.body=old
        design.button(self.dock,'×  Pass',lambda:self.do(app.skip,who)).pack(side='left',fill='x',expand=True,padx=(0,4))
        design.button(self.dock,'♡  Add a like',lambda:self.select_like(who,'Photo'),True).pack(side='left',fill='x',expand=True)

    def likes(self):
        incoming=[x for x in self.data['likes'] if x['status']=='incoming']
        self.label('Interested in you',True)
        if not incoming:self.label('Incoming likes will appear here as story time passes.')
        for item in reversed(incoming):
            self.card(item['who'])
            self.label('Liked: '+item['target'])
            self.label(item['message'])
            self.button('Match & open conversation',lambda x=item:self.accept(x))
            self.button('Decline politely',lambda x=item:self.do(app.incoming_action,x['id'],False))
        self.label('Likes you sent',True)
        for item in reversed(self.data['likes']):
            if item['direction']!='outgoing':continue
            self.label(camera.name(item['who'])+' · '+{'pending':'Awaiting a response','matched':'Matched','declined':'No match'}.get(item['status'],item['status']),True)
            self.label(item['message'])
            if item['status']=='matched':self.button('Open match',lambda w=item['who']:self.go('Chat',w))

    def accept(self,item):
        self.do(app.incoming_action,item['id'],True)
        if item['who'] in self.data['matches'] and self.data['matches'][item['who']]['status']=='active':
            self.go('Chat',item['who'])

    def matches(self):
        design.label(self.body,'Your conversations','Title')
        active=[m for m in self.data['matches'].values() if m['status']=='active']
        if not active:self.label('Your mutual matches will appear here. Matching starts an online acquaintance, not an in-person meeting.')
        for m in sorted(active,key=lambda x:(-x['unread'],-x['created'])):
            if m['pending']: status='Reply failed · retry available' if m['pending'].get('error') else 'Waiting for their reply'
            else: status='Your turn' if m['messages'] and m['messages'][-1]['author']=='them' else 'Conversation open'
            panel=self.section(camera.name(m['who'])+(f' · {m["unread"]} new' if m['unread'] else ''),status)
            if m['messages']:design.label(panel,m['messages'][-1]['text'][:110],'Body',True)
            design.button(panel,'Continue conversation  →',lambda w=m['who']:self.go('Chat',w)).pack(fill='x')
        for m in self.data['matches'].values():
            if m['status']!='active':self.label(camera.name(m['who'])+' · '+m['status'])

    def chat(self):
        who=self.who_selected
        try:m=app.match(self.s,who)
        except ValueError:
            self.label('This match is closed.'); return
        m['unread']=0
        design.label(self.body,camera.name(who),'Title')
        self.button('View profile & photos',lambda:self.go('Character',who))
        self.label('Met in person after matching' if m['first_meeting'] else 'Known before Meet-Cute' if m.get('known_before') else 'Online acquaintance · No in-person meeting recorded')
        self.label('Numbers exchanged' if m['numbers'] else 'Chatting privately inside Meet-Cute')
        if m['numbers']:
            import phone_numbers
            self.label(phone_numbers.saved_number(self.s,who) or phone_numbers.number(self.s,who),True)
            self.label('Saved in Contacts')
            self.button('View saved contact',lambda:self.view_contact(who))
        for line in m['messages'][-40:]:
            minute=line['minute']
            stamp=f'{story_calendar.story_date(minute):%b %d} {minute%1440//60:02}:{minute%60:02}'
            bubble=ttk.Frame(self.body,padding=12,style='PhoneDark.Meet.Card.TFrame')
            bubble.pack(fill='x',padx=(35,0) if line['author']=='you' else (0,35),pady=6)
            design.label(bubble,('You' if line['author']=='you' else camera.name(who) if line['author']=='them' else 'Meet-Cute')+' · '+stamp,'Muted',True)
            design.label(bubble,line['text'],'Body',True)
        body=self.body;self.body=self.dock
        composer=self.field('Your message',multiline=True);composer.configure(height=2)
        self.button('Send message',lambda:self.do(app.send,who,self.get('Your message'),clear=('Your message',)))
        self.body=body
        if m['pending']:
            self.label(m['pending'].get('error') or 'Reply queued. Continue your day or wait for story time to pass.')
            if m['pending'].get('error'):self.button('Retry reply',lambda:self.do(app.retry,who))
        if not m['numbers']:
            self.button('Ask to exchange numbers',lambda:self.do(app.request_numbers,who))
        elif hidden_contact(self.s,who):
            self.button('Open Messages',lambda:self.phone.open_thread(who))
        self.label('Plan a first date',True)
        self.label('Send an invitation to a public place. It enters Calendar only after they agree. You can meet before exchanging numbers.')
        venues={town.LOCATIONS[v]:v for v in app.PUBLIC_VENUES}
        self.field('Public venue',values=venues)
        tomorrow=story_calendar.story_date(app.now(self.s))+timedelta(days=1)
        self.field('Date (YYYY-MM-DD)',tomorrow.isoformat())
        self.field('Time (HH:MM)','17:00')
        self.button('Propose date',lambda:self.do(app.propose_date,who,venues[self.get('Public venue')],self.get('Date (YYYY-MM-DD)'),self.get('Time (HH:MM)')))
        p=m['proposal']
        if p:self.label(p['kind'].title()+' request · '+p['status'])
        for event in app.dates(self.s,who):
            import scheduled_events
            self.label(scheduled_events.describe(event),True)
            self.label('Cancelled' if event.get('cancelled') else 'Ended' if event['end']<=app.now(self.s) else 'Both agreed')
            if not event.get('cancelled') and event['end']>app.now(self.s):
                self.button('Join date at the venue',lambda e=event:self.do(scheduled_events.join,e))
                self.button('Cancel this date',lambda e=event:self.do(app.cancel_date,who,e['id']))
        if app.dates(self.s,who):
            self.button('Open Calendar',lambda:self.phone.open_app('Calendar'))
            self.button('Open Maps',lambda:self.phone.open_app('Maps'))
        self.button('Discuss exclusivity',lambda:self.do(app.request_exclusive,who))
        self.button('Unmatch',lambda:self.end_match(who,False))
        self.button('Block this match',lambda:self.end_match(who,True))

    def end_match(self,who,block):
        previous=getattr(self,'confirmation',None)
        if previous is not None and previous.winfo_exists():previous.destroy()
        panel=self.confirmation=ttk.Frame(self.body,padding=10)
        panel.pack(fill='x',pady=8)
        ttk.Label(panel,text=('Block' if block else 'Unmatch')+' '+camera.name(who)+'? This closes this app conversation and cancels upcoming Meet-Cute dates.',wraplength=300).pack(fill='x')
        def confirm():
            self.do(app.unmatch,who,block)
            if self.data['matches'][who]['status']!='active':self.go('Matches')
        PhoneButton(panel,text='Confirm',command=confirm).pack(fill='x',pady=4)
        PhoneButton(panel,text='Keep match',command=panel.destroy).pack(fill='x')

    def view_contact(self,who):
        self.phone.open_app('Contacts')
        self.phone.contact_detail(who)


def hidden_contact(s,who):
    import hidden_cast
    return hidden_cast.contact(s,who)
