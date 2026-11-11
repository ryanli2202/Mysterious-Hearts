"""Dark, immediately displayed novel pages on the existing in-person stage."""
import tkinter as tk
from tkinter import ttk
from pathlib import Path
from PIL import Image, ImageOps, ImageTk
import winterfield_ui as ui
import campaign_prose as prose


def show(game):
    game.hide_phone_for_location()
    for name in ('campaign_view','interpol_view','combat_view'):
        panel=getattr(game,name,None)
        if panel is not None and panel.winfo_exists():panel.place_forget()
    area=getattr(game,'area_view',None)
    if area is not None and area.winfo_exists():area.pack_forget()
    game.presence_view.pack_forget();game.in_person_chat.pack(side='left',fill='both',expand=True)
    view=game.hangout_view
    reader=getattr(view,'prose_reader',None)
    if reader is None or not reader.winfo_exists():reader=view.prose_reader=Reader(view.canvas,game)
    reader.place(x=0,y=0,relwidth=1,relheight=1);reader.lift();reader.open_current()


def hide(game):
    reader=getattr(getattr(game,'hangout_view',None),'prose_reader',None)
    if reader is not None and reader.winfo_exists():reader.place_forget()


class Reader(ui.TextureFrame):
    def __init__(self,parent,game):
        super().__init__(parent,bg=ui.INK,padx=12,pady=10)
        self.game=game;self.history_mode=False;self.origin=None;self.identity=None;self.history_pages=[];self.history_cursor=0;self.archive_state=None
        self.rowconfigure(1,weight=1);self.columnconfigure(1,weight=1)
        header=tk.Frame(self,bg=ui.INK);header.grid(row=0,column=0,columnspan=2,sticky='ew',pady=(0,10))
        self.kicker=tk.Label(header,text='IN PERSON · STORY',bg=ui.INK,fg=ui.MINT,font=('Segoe UI',10,'bold'),anchor='w')
        self.kicker.pack(fill='x')
        self.heading=tk.Label(header,bg=ui.INK,fg=ui.CREAM,font=('Georgia',20),anchor='w',justify='left')
        self.heading.pack(fill='x',pady=4)
        self.heading.bind('<Configure>',lambda e:self.heading.configure(wraplength=max(160,e.width-8)))
        self.illustration=tk.Canvas(self,bg=ui.INK,highlightthickness=0,width=240)
        self.illustration.grid(row=1,column=0,sticky='nsew',padx=(0,12))
        self.illustration.bind('<Configure>',self.paint)
        self.illustration.bind('<Map>',lambda e:self.after_idle(self.paint))
        paper=tk.Frame(self,bg=ui.PANEL,highlightbackground=ui.EDGE,highlightthickness=1,padx=15,pady=10)
        paper.grid(row=1,column=1,sticky='nsew');paper.rowconfigure(1,weight=1);paper.columnconfigure(0,weight=1)
        self.chapter=tk.Label(paper,bg=ui.PANEL,fg=ui.GOLD,font=('Segoe UI',10),anchor='w',justify='left')
        self.chapter.grid(row=0,column=0,columnspan=2,sticky='ew',pady=(0,8))
        self.chapter.bind('<Configure>',lambda e:self.chapter.configure(wraplength=max(100,e.width-5)))
        self.text=tk.Text(paper,wrap='word',bg=ui.PANEL,fg=ui.CREAM,insertbackground=ui.CREAM,
                          selectbackground=ui.EDGE,selectforeground=ui.CREAM,relief='flat',borderwidth=0,
                          highlightthickness=0,padx=3,pady=6,spacing1=3,spacing3=7,takefocus=True,width=38)
        self.text.grid(row=1,column=0,sticky='nsew')
        scroll=ttk.Scrollbar(paper,orient='vertical',command=self.text.yview);scroll.grid(row=1,column=1,sticky='ns')
        self.text.configure(yscrollcommand=lambda a,b:self.scrolled(a,b,scroll))
        self.options=tk.Frame(paper,bg=ui.PANEL);self.options.grid(row=2,column=0,columnspan=2,sticky='ew',pady=(8,0))
        self.notice=tk.Label(paper,bg=ui.PANEL,fg=ui.MUTED,anchor='w',justify='left',wraplength=450)
        self.notice.grid(row=3,column=0,columnspan=2,sticky='ew')
        controls=tk.Frame(self,bg=ui.INK);controls.grid(row=2,column=0,columnspan=2,sticky='ew',pady=(10,0))
        toolbar=tk.Frame(controls,bg=ui.INK);toolbar.pack(fill='x')
        ttk.Button(toolbar,text='A−',width=4,command=lambda:self.resize(-1)).pack(side='left')
        ttk.Button(toolbar,text='A+',width=4,command=lambda:self.resize(1)).pack(side='left',padx=4)
        self.font_label=tk.Label(toolbar,bg=ui.INK,fg=ui.MUTED);self.font_label.pack(side='left',padx=5)
        ttk.Button(toolbar,text='Scene history',command=self.history).pack(side='right')
        ttk.Button(toolbar,text='Story so far',command=self.recap).pack(side='right',padx=4)
        nav=tk.Frame(controls,bg=ui.INK);nav.pack(fill='x',pady=(7,0))
        self.back=ttk.Button(nav,text='← Previous page',command=lambda:self.advance(-1));self.back.pack(side='left')
        self.progress=tk.Label(nav,bg=ui.INK,fg=ui.MUTED);self.progress.pack(side='left',expand=True)
        self.next=ttk.Button(nav,text='Continue →',command=lambda:self.advance(1));self.next.pack(side='right')
        self.return_button=ttk.Button(nav,text='Return to current scene',command=self.return_current)
        self.bind('<Configure>',self.layout,add='+')
        self.text.bind('<Control-plus>',lambda e:self.resize(1))
        self.text.bind('<Control-minus>',lambda e:self.resize(-1))
        self.text.bind('<Alt-Right>',lambda e:self.advance(1))
        self.text.bind('<Alt-Left>',lambda e:self.advance(-1))

    def layout(self,event):
        if event.widget is not self:return
        if event.width<790:self.illustration.grid_remove()
        else:
            self.illustration.grid();self.illustration.configure(width=min(270,int(event.width*.26)))
        self.notice.configure(wraplength=max(180,event.width-340))

    def open_current(self):
        d=self.game.state_data.get('campaign_dialogue')
        if self.origin is not d:
            self.history_mode=False;self.origin=d;self.identity=None
        if not self.history_mode:self.display();self.after_idle(self.paint)

    def current(self):
        if self.history_mode:return self.history_pages[self.history_cursor]
        d=self.game.state_data['campaign_dialogue'];return d['beats'][d['cursor']]

    def display(self):
        b=self.current();d=self.game.state_data.get('campaign_dialogue') or {}
        identity=(id(b),self.history_mode,b.get('selected'),b.get('gm_narration'))
        self.heading.configure(text=b.get('title') or d.get('title') or 'Story')
        self.chapter.configure(text=b.get('chapter',''))
        self.kicker.configure(text=('SCENE HISTORY · READ ONLY' if self.history_mode else 'IN PERSON · '+('MEMORY' if b.get('mode')=='memory' else 'PRESENT DAY')))
        size=prose.read(self.game.state_data).get('preferences',{}).get('size',15)
        self.text.configure(font=('Georgia',size));self.font_label.configure(text=f'{size} pt · instant text')
        if identity!=self.identity:
            self.text.configure(state='normal');self.text.delete('1.0','end')
            text=b.get('gm_narration') or b.get('narration','')
            if not b.get('prose'):
                text+='\n\n'+('\n'.join(str(w)+': '+t for w,t in b.get('speeches',[])))
                if b.get('player'):text=d.get('player','Player').title()+': '+b['player']+'\n\n'+text
            self.text.insert('1.0',text);self.text.configure(state='disabled')
            self.text.yview_moveto(b.get('scroll',0));self.identity=identity
        for w in self.options.winfo_children():w.destroy()
        self.notice.configure(text='')
        if b.get('reflection'):
            for index,option in enumerate(b['options']):
                selected=b.get('selected')==index
                button=ttk.Button(self.options,text=('✓ ' if selected else '')+option['label'],
                                 command=lambda i=index:self.choose(i),state='disabled' if self.history_mode or b.get('selected') is not None else 'normal')
                button.pack(fill='x',pady=3)
        if not self.history_mode and b.get('optional_narration') and not b.get('gm_narration'):
            ttk.Button(self.options,text='Optional Game Master description' if not b.get('_narration_error') else 'Retry optional description',command=self.describe).pack(fill='x')
            self.notice.configure(text=b.get('_narration_error') or 'Authored text is ready. Optional description uses your configured provider.')
        cursor=self.history_cursor if self.history_mode else d['cursor'];total=len(self.history_pages) if self.history_mode else len(d['beats'])
        self.progress.configure(text=f'{cursor+1} / {total}')
        self.back.configure(state='normal' if cursor else 'disabled')
        if self.history_mode:
            self.next.configure(text='Next page →',state='normal' if cursor<total-1 else 'disabled')
            self.return_button.pack(side='right',padx=5)
        else:
            self.return_button.pack_forget()
            self.next.configure(text='Continue →' if cursor<total-1 else ('Finish conversation' if not d.get('action') else 'Continue to outcome'),
                                state='disabled' if b.get('reflection') and b.get('selected') is None else 'normal')
            d['portraits']=b.get('portraits',{});d['background']=b.get('background')
        self.paint()

    def scrolled(self,a,b,scroll):
        scroll.set(a,b)
        if self.identity and not self.history_mode and self.game.state_data.get('campaign_dialogue') is self.origin:
            self.current()['scroll']=float(a)

    def resize(self,delta):
        pref=prose.data(self.game.state_data)['preferences'];pref['size']=min(24,max(11,pref.get('size',15)+delta))
        self.game.persist();self.display()

    def choose(self,index):
        try:prose.choose_reflection(self.game.state_data,index);self.game.persist();self.display()
        except ValueError as exc:self.notice.configure(text=str(exc))

    def describe(self):
        import campaign_dialogue
        b=self.current();b['_request_narration']=True
        self.game._campaign_narration_job=None
        campaign_dialogue.request_narration(self.game,self.origin,b)
        self.notice.configure(text='Requesting an optional description. You can continue with the authored text.')

    def advance(self,delta):
        import campaign_dialogue,combat
        if self.history_mode:
            self.history_cursor=max(0,min(len(self.history_pages)-1,self.history_cursor+delta));self.display();return
        d=self.game.state_data.get('campaign_dialogue')
        try:
            if delta<0:d['cursor']=max(0,d['cursor']-1)
            else:campaign_dialogue.next_line(self.game.state_data)
            self.game.persist()
        except ValueError as exc:self.notice.configure(text=str(exc));return
        if self.game.state_data.get('campaign_dialogue'):self.display()
        else:
            self.place_forget();campaign_dialogue.restore(self.game.hangout_view);self.game.render()
            if combat.active(self.game.state_data):__import__('combat_ui').open_combat(self.game)

    def history(self):
        self.history_pages=[]
        for entry in self.game.state_data.get('campaign_dialogue_history',[]):
            if entry.get('player')==self.game.state_data['player']:
                self.history_pages.extend(entry['beats'])
        if not self.history_pages:self.history_pages=[prose.page('Completed scenes will appear here. Reading history never repeats an action or reward.',title='Scene history')]
        self.history_mode=True;self.history_cursor=0;self.display()

    def recap(self):
        self.history_pages=[prose.page(text,title='Story so far') for text in prose.recap(self.game.state_data)]
        self.history_mode=True;self.history_cursor=0;self.display()

    def return_current(self):
        self.history_mode=False;self.archive_state=None
        if self.game.state_data.get('campaign_dialogue'):self.display()
        else:self.place_forget();self.game.show_in_person()

    def paint(self,event=None):
        if not self.winfo_exists() or not self.illustration.winfo_ismapped():return
        import artwork
        c=self.illustration;w,h=c.winfo_width(),c.winfo_height()
        if w<30 or h<30:return
        b=self.current();s=self.game.state_data
        art=b.get('background') or artwork.scene_art(b.get('venue',s['world']['location']),minute=b.get('minute',s['world']['minute']))
        c.delete('all')
        im=ImageOps.fit(artwork.source_image(art).convert('RGB'),(w,h))
        shade=Image.new('RGB',im.size,ui.INK);im=Image.blend(im,shade,.30)
        self.backdrop=ImageTk.PhotoImage(im,master=c)
        c.create_image(0,0,image=self.backdrop,anchor='nw')
        # Period-specific cast art only where the library has a verified asset.
        self.portraits={}
        if not self.history_mode and (b.get('mode')!='memory' or b.get('portraits')):
            cast=list(b.get('portraits',{})) or [s['player']]
            width=max(70,int((w-12)/len(cast)))
            photos=self.game.portrait_group({who:(width,min(h-50,int(width*1.85))) for who in cast},
                s['world']['location'],s['world']['minute'])
            for index,who in enumerate(cast):
                picture=photos[who]
                self.portraits[who]=picture
                c.create_image((index+.5)*w/len(cast),h-25,image=picture,anchor='s')
        c.create_text(14,16,text=s['player'].upper()+'\n'+('REMEMBERING' if b.get('mode')=='memory' else 'WINTERFIELD'),anchor='nw',fill=ui.CREAM,font=('Segoe UI',11,'bold'))


def open_archive(game,kind='history'):
    """Read-only view, even when no active scene exists; no gameplay placeholder."""
    game.hide_phone_for_location()
    for name in ('campaign_view','interpol_view'):
        panel=getattr(game,name,None)
        if panel is not None and panel.winfo_exists():panel.place_forget()
    game.presence_view.pack_forget();game.in_person_chat.pack(side='left',fill='both',expand=True)
    view=game.hangout_view
    if not getattr(view,'prose_reader',None) or not view.prose_reader.winfo_exists():view.prose_reader=Reader(view.canvas,game)
    reader=view.prose_reader;reader.place(x=0,y=0,relwidth=1,relheight=1);reader.lift()
    reader.archive_state=game.state_data
    reader.origin=game.state_data.get('campaign_dialogue')
    (reader.recap if kind=='recap' else reader.history)()


def board(parent,game,act):
    s=game.state_data
    if s['player'] not in ('garrett','rei','fox','gordon'):return
    ttk.Separator(parent).pack(fill='x',pady=8)
    tools=ttk.Frame(parent);tools.pack(fill='x')
    ttk.Button(tools,text='Story so far',command=lambda:open_archive(game,'recap')).pack(side='left',padx=3)
    ttk.Button(tools,text='Read scene history',command=lambda:open_archive(game)).pack(side='left',padx=3)
    offers=prose.offers(s)
    if offers:
        ttk.Label(parent,text='Time with the people in your story · optional in-person visits',foreground=ui.MINT).pack(anchor='w',pady=(10,3))
        for key in offers:
            spec=prose.SOCIAL[key];card=ttk.Frame(parent,padding=8);card.pack(fill='x',pady=4)
            ttk.Label(card,text=prose.library()[key]['title'],font=('Segoe UI',11,'bold')).pack(anchor='w')
            reason=prose.unavailable(s,key)
            info=ttk.Label(card,text=reason or 'Available here. Choose what to share; privacy carries no penalty.',wraplength=620,justify='left');info.pack(fill='x',pady=3)
            info.bind('<Configure>',lambda e,w=info:w.configure(wraplength=max(120,e.width-8)))
            if s['world']['location']!=spec['venue']:
                ttk.Button(card,text='Visit '+__import__('town').location_name(s,spec['venue']),command=lambda v=spec['venue']:act(__import__('town').travel,v)).pack(anchor='w')
            row=ttk.Frame(card);row.pack(fill='x')
            enabled='disabled' if reason else 'normal'
            ttk.Button(row,text='Share this subject' if spec.get('topic') else 'Spend time together',state=enabled,
                       command=lambda k=key:act(prose.begin_social,k,'share','help')).pack(side='left',padx=2)
            ttk.Button(row,text='Keep details private',state=enabled,
                       command=lambda k=key:act(prose.begin_social,k,'private','quiet')).pack(side='left',padx=2)
            if key not in prose.read(s).get('deferred',[]):
                ttk.Button(row,text='Another time',command=lambda k=key:act(prose.defer,k)).pack(side='left',padx=2)
    for f in s.get('interpol',{}).get('files',{}).values():
        for hypothesis in f.get('hypotheses',{}).values():
            ttk.Label(parent,text=hypothesis['title']+' · tested inference\n'+hypothesis['conclusion'],wraplength=700,justify='left').pack(fill='x',pady=5)
    __import__('phone_theme').apply_tree(parent)
