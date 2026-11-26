"""Dark, immediately displayed novel pages on the existing in-person stage."""
import tkinter as tk
from tkinter import ttk
from pathlib import Path
from PIL import Image, ImageOps, ImageTk
import winterfield_ui as ui
import campaign_prose as prose
import campaign_presentation as presentation
import campaign_voice


def speaker_label(who):
    if who=='takeo-one-child':return 'One'
    if who in ('mariko','tyler-father','soren','hachimura','thirteen','trainee'):return {'mariko':'Mariko Ishida','tyler-father':'Tyler’s father','soren':'Soren','hachimura':'Keisuke Hachimura','thirteen':'Number Thirteen','trainee':'Trainee'}[who]
    if who in ('takeo-deputy','takeo-kazama','takeo-medic','takeo-researcher','takeo-officer'):
        return {'takeo-deputy':'Kenji Arakawa','takeo-kazama':'Shinzo Kazama','takeo-medic':'Naomi Kuroda','takeo-researcher':'Haruka Senda','takeo-officer':'Daichi Mori'}[who]
    if who in ('kaden','conspirator','parent-one','parent-two'):return {'kaden':'Kaden Mourne','conspirator':'Conspirator','parent-one':'Garrett and Charles’s father','parent-two':'Garrett and Charles’s mother'}[who]
    if who in ('camila-elena','camila-pilar','camila-mara','camila-inez','camila-ansel'):
        return {'camila-elena':'Elena Sanz','camila-pilar':'Pilar','camila-mara':'Mara Esteve','camila-inez':'Inez Salcedo','camila-ansel':'Ansel Vey'}[who]
    return {'martos-lena':'Lena Varo','martos-sera':'Sera Dalm','martos-voss':'Adrien Voss','martos-tomas':'Tomas Reed','mavis-broker':'The Broker','mavis-previous-spade':'Previous Ace of Spades'}.get(who,str(who or 'Off-screen voice').title())


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
    if reader is not None and reader.winfo_exists():reader.cancel_flip();reader.place_forget()


class Reader(ui.TextureFrame):
    def __init__(self,parent,game):
        super().__init__(parent,bg=ui.INK,padx=12,pady=10)
        self.game=game;self.history_mode=False;self.origin=None;self.identity=None;self.history_pages=[];self.history_cursor=0;self.archive_state=None
        self.voice=campaign_voice.Playback(game.sounds)
        self.rowconfigure(1,weight=1);self.columnconfigure(1,weight=1)
        header=tk.Frame(self,bg=ui.INK);header.grid(row=0,column=0,columnspan=2,sticky='ew',pady=(0,10))
        self.kicker=tk.Label(header,text='IN PERSON · STORY',bg=ui.INK,fg=ui.MINT,font=('Segoe UI',10,'bold'),anchor='w')
        self.kicker.pack(fill='x')
        self.heading=tk.Label(header,bg=ui.INK,fg=ui.CREAM,font=('Georgia',20),anchor='w',justify='left')
        self.heading.pack(fill='x',pady=4)
        self.heading.bind('<Configure>',lambda e:self.heading.configure(wraplength=max(160,e.width-8)))
        self.illustration=tk.Canvas(self,bg=ui.INK,highlightthickness=0,width=240)
        self.illustration.grid(row=1,column=0,columnspan=2,sticky='nsew')
        self.illustration.bind('<Configure>',self.paint)
        self.illustration.bind('<Map>',lambda e:self.after_idle(self.paint))
        paper=self.paper=tk.Frame(self.illustration,bg=ui.PANEL,highlightbackground=ui.EDGE,highlightthickness=1,padx=20,pady=10)
        paper.rowconfigure(1,weight=1);paper.columnconfigure(0,weight=1)
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
        audio=tk.Frame(controls,bg=ui.INK);audio.pack(fill='x',pady=(6,0))
        preferences=prose.read(game.state_data).get('preferences',{})
        self.voice_on=tk.BooleanVar(value=preferences.get('voice_enabled',True))
        self.voice_volume=tk.DoubleVar(value=preferences.get('voice_volume',70))
        ttk.Checkbutton(audio,text='Voice',variable=self.voice_on,command=self.voice_changed).pack(side='left')
        self.replay_button=ttk.Button(audio,text='Replay voice',command=self.replay_voice)
        self.replay_button.pack(side='left',padx=6)
        tk.Label(audio,text='Volume',bg=ui.INK,fg=ui.MUTED).pack(side='left')
        style=ttk.Style(self)
        scale_style='CampaignVoice.Horizontal.TScale'
        style.configure(scale_style,background=ui.INK,troughcolor=ui.PANEL,bordercolor=ui.EDGE,lightcolor=ui.EDGE,darkcolor=ui.INK)
        style.map(scale_style,background=[('disabled',ui.PANEL),('active',ui.EDGE),('!disabled',ui.INK)])
        self.voice_scale=ttk.Scale(audio,style=scale_style,from_=0,to=100,variable=self.voice_volume,length=95)
        self.voice_scale.bind('<ButtonRelease-1>',self.voice_changed)
        self.voice_scale.bind('<KeyRelease>',self.voice_changed)
        self.voice_scale.pack(side='left',padx=6)
        self.voice_status=tk.Label(audio,text='',bg=ui.INK,fg=ui.MUTED,anchor='w')
        self.voice_status.pack(side='left',fill='x',expand=True)
        nav=tk.Frame(controls,bg=ui.INK);nav.pack(fill='x',pady=(7,0))
        self.back=ttk.Button(nav,text='← Previous page',command=lambda:self.advance(-1));self.back.pack(side='left')
        self.progress=tk.Label(nav,bg=ui.INK,fg=ui.MUTED);self.progress.pack(side='left',expand=True)
        self.next=ttk.Button(nav,text='Continue →',command=lambda:self.advance(1));self.next.pack(side='right')
        self.return_button=ttk.Button(nav,text='Return to current scene',command=self.return_current)
        self.motion=tk.BooleanVar(value=prose.read(game.state_data).get('preferences',{}).get('reduced_motion',False))
        ttk.Checkbutton(toolbar,text='Reduced motion',variable=self.motion,command=self.motion_changed).pack(side='left',padx=6)
        self.flip_job=None;self.flip_generation=0;self.last_shot=None
        self.bind('<Unmap>',lambda e:self.cancel_flip(),add='+')
        self.bind('<Unmap>',lambda e:self.voice.stop() if e.widget is self else None,add='+')
        self.bind('<Destroy>',lambda e:self.voice.stop() if e.widget is self else None,add='+')
        self.bind('<Configure>',self.layout,add='+')
        self.text.bind('<Control-plus>',lambda e:self.resize(1))
        self.text.bind('<Control-minus>',lambda e:self.resize(-1))
        self.text.bind('<Alt-Right>',lambda e:self.advance(1))
        self.text.bind('<Alt-Left>',lambda e:self.advance(-1))

    def layout(self,event):
        if event.widget is not self:return
        self.cancel_flip()
        self.notice.configure(wraplength=max(180,event.width-100))

    def open_current(self):
        d=self.game.state_data.get('campaign_dialogue')
        if self.origin is not d:
            self.cancel_flip()
            self.history_mode=False;self.origin=d;self.identity=None
            preferences=prose.read(self.game.state_data).get('preferences',{})
            self.voice_on.set(preferences.get('voice_enabled',True));self.voice_volume.set(preferences.get('voice_volume',70))
        if not self.history_mode:self.display();self.after_idle(self.paint)

    def current(self):
        if self.history_mode:return self.history_pages[self.history_cursor]
        d=self.game.state_data['campaign_dialogue'];return d['beats'][d['cursor']]

    def display(self):
        b=self.current();d=self.game.state_data.get('campaign_dialogue') or {}
        if self.history_mode:
            self.unit=presentation.units(b,d.get('player',self.game.state_data['player']))[0];unit_index=0;unit_total=1
        else:self.unit,unit_index,unit_total=presentation.position(d)
        identity=(id(b),self.history_mode,b.get('selected'),b.get('gm_narration'),unit_index)
        self.heading.configure(text=b.get('title') or d.get('title') or 'Story')
        narrator = b.get('memory_owner', self.game.state_data['player']).title()
        if b.get('memory_owner'):narrator += '’s recollection'
        self.chapter.configure(text=(speaker_label(self.unit.get('speaker'))+' · DIALOGUE' if self.unit['phase']=='dialogue' else 'NARRATION · '+narrator))
        self.kicker.configure(text=('SCENE HISTORY · READ ONLY' if self.history_mode else 'IN PERSON · '+('MEMORY' if b.get('mode')=='memory' else 'PRESENT DAY')))
        size=prose.read(self.game.state_data).get('preferences',{}).get('size',15)
        self.text.configure(font=('Georgia',size));self.font_label.configure(text=f'{size} pt · instant text')
        if identity!=self.identity:
            self.text.configure(state='normal');self.text.delete('1.0','end')
            text=self.unit['text']
            self.text.insert('1.0',text);self.text.configure(state='disabled')
            self.scroll_target=None
            key=f'{self.unit["segment"]}:{self.unit["page"]}'
            self.text.yview_moveto(b.get('presentation_scroll',{}).get(key,b.get('scroll',0) if unit_index==0 else 0))
            self.identity=identity;self.scroll_target=(d,b,key)
        for w in self.options.winfo_children():w.destroy()
        self.set_notice('')
        if b.get('reflection'):
            for index,option in enumerate(b['options']):
                selected=b.get('selected')==index
                button=ttk.Button(self.options,text=('✓ ' if selected else '')+option['label'],
                                 command=lambda i=index:self.choose(i),state='disabled' if self.history_mode or b.get('selected') is not None else 'normal')
                button.pack(fill='x',pady=3)
        if not self.history_mode and d.get('action')=='campaign_gauntlet.continue_wave':
            ttk.Button(self.options,text='Return to location · keep cleared posts',command=self.withdraw_gauntlet).pack(fill='x')
        if not self.history_mode and b.get('optional_narration') and not b.get('gm_narration'):
            ttk.Button(self.options,text='Optional Game Master description' if not b.get('_narration_error') else 'Retry optional description',command=self.describe).pack(fill='x')
            self.set_notice(b.get('_narration_error') or 'Authored text is ready. Optional description uses your configured provider.')
        cursor=self.history_cursor if self.history_mode else d['cursor'];total=len(self.history_pages) if self.history_mode else len(d['beats'])
        self.progress.configure(text=f'{cursor+1} / {total} · {self.unit["phase"]} {unit_index+1}/{unit_total}')
        self.back.configure(state='normal' if cursor or unit_index else 'disabled')
        if self.history_mode:
            self.next.configure(text='Next page →',state='normal' if cursor<total-1 else 'disabled')
            self.return_button.pack(side='right',padx=5)
        else:
            self.return_button.pack_forget()
            self.next.configure(text='Continue →' if cursor<total-1 or unit_index<unit_total-1 else ('Finish conversation' if not d.get('action') else 'Continue to outcome'),
                                state='disabled' if b.get('reflection') and b.get('selected') is None else 'normal')
            d['portraits']=b.get('portraits',{});d['background']=b.get('background')
        self.paint()
        self.sync_voice()

    def sync_voice(self,autoplay=True):
        b=self.current();d=self.game.state_data.get('campaign_dialogue') or {}
        player=self.game.state_data['player']
        record=campaign_voice.resolve(b,self.unit,player)
        if not self.history_mode and (d.get('player')!=player or d.get('venue')!=self.game.state_data['world']['location']):record=None
        self.voice.configure(self.voice_on.get(),self.voice_volume.get())
        token=(id(self.game.state_data),id(d) if d else None,id(b),self.history_mode,self.unit['segment'],self.unit['page'])
        self.voice.enter(token,record,autoplay=autoplay and not self.history_mode and self.unit['page']==0)
        available=record is not None and self.voice_on.get() and self.game.sounds.enabled
        self.replay_button.configure(state='normal' if available else 'disabled')
        self.voice_status.configure(text=self.voice.error or ('Voice off' if not self.voice_on.get() or not self.game.sounds.enabled else
                                          ('Recording available' if record else 'Text only')))

    def voice_changed(self,*args):
        pref=prose.data(self.game.state_data)['preferences']
        pref.update(voice_enabled=bool(self.voice_on.get()),voice_volume=round(self.voice_volume.get()))
        self.voice.configure(self.voice_on.get(),self.voice_volume.get())
        self.game.persist()
        if hasattr(self,'unit'):self.sync_voice()

    def replay_voice(self):
        # Re-resolve before replay: navigation, saved state or files may have changed.
        self.sync_voice(autoplay=False)
        self.voice.replay()
        if self.voice.error:self.voice_status.configure(text=self.voice.error)

    def withdraw_gauntlet(self):
        self.cancel_flip();__import__('campaign_gauntlet').withdraw(self.game.state_data)
        self.game.persist();self.place_forget();self.game.render()

    def motion_changed(self):
        prose.data(self.game.state_data)['preferences']['reduced_motion']=bool(self.motion.get())
        self.cancel_flip();self.game.persist()

    def cancel_flip(self):
        self.flip_generation+=1
        if self.flip_job is not None:
            try:self.after_cancel(self.flip_job)
            except tk.TclError:pass
        self.flip_job=None
        if self.illustration.winfo_exists():self.illustration.delete('page_fold')

    def flip(self,direction,outgoing=None):
        if self.motion.get():return
        self.cancel_flip();generation=self.flip_generation
        def frame(index):
            if generation!=self.flip_generation or not self.winfo_ismapped():return
            c=self.illustration;c.delete('page_fold');w,h=c.winfo_width(),c.winfo_height()
            progress=1-(1-index/10)**3
            remaining=max(1,int(w*(1-progress)))
            edge=remaining if direction>0 else w-remaining
            if outgoing is not None and index<10:
                folded=outgoing.resize((remaining,h),Image.Resampling.BICUBIC)
                self.flip_image=ImageTk.PhotoImage(folded,master=c)
                c.create_image(0 if direction>0 else w,0,image=self.flip_image,
                               anchor='nw' if direction>0 else 'ne',tags='page_fold')
            c.create_polygon(edge,0,edge+direction*24,h/2,edge,h,edge-direction*5,h/2,
                             fill=ui.EDGE,outline=ui.GOLD,tags='page_fold')
            if index<10:self.flip_job=self.after(18,lambda:frame(index+1))
            else:c.delete('page_fold');self.flip_job=None
        frame(0)

    def scrolled(self,a,b,scroll):
        scroll.set(a,b)
        target=getattr(self,'scroll_target',None)
        if target and self.identity and not self.history_mode and self.game.state_data.get('campaign_dialogue') is target[0] and self.current() is target[1]:
            target[1].setdefault('presentation_scroll',{})[target[2]]=float(a)

    def set_notice(self,text):
        self.notice.configure(text=text)
        if text:self.notice.grid()
        else:self.notice.grid_remove()

    def resize(self,delta):
        self.cancel_flip()
        pref=prose.data(self.game.state_data)['preferences'];pref['size']=min(24,max(11,pref.get('size',15)+delta))
        self.game.persist();self.display()

    def choose(self,index):
        try:prose.choose_reflection(self.game.state_data,index);self.game.persist();self.display()
        except ValueError as exc:self.set_notice(str(exc))

    def describe(self):
        import campaign_dialogue
        b=self.current();b['_request_narration']=True
        self.game._campaign_narration_job=None
        campaign_dialogue.request_narration(self.game,self.origin,b)
        self.set_notice('Requesting an optional description. You can continue with the authored text.')

    def advance(self,delta):
        import campaign_dialogue,combat
        if self.flip_job is not None:return
        self.voice.stop()
        if self.history_mode:
            previous=self.unit['shot_id'];outgoing=getattr(self,'stage_raster',None)
            self.history_cursor=max(0,min(len(self.history_pages)-1,self.history_cursor+delta));self.display()
            if self.unit['shot_id']!=previous:self.flip(delta,outgoing)
            return
        d=self.game.state_data.get('campaign_dialogue')
        if not d:return
        previous=presentation.position(d)[0]['shot_id'];outgoing=getattr(self,'stage_raster',None)
        try:
            presentation.advance(self.game.state_data,delta)
            self.game.persist()
        except ValueError as exc:self.set_notice(str(exc));return
        if self.game.state_data.get('campaign_dialogue'):
            self.open_current()
            if self.unit['shot_id']!=previous:self.flip(delta,outgoing)
        else:
            self.place_forget();campaign_dialogue.restore(self.game.hangout_view);self.game.render()
            if combat.active(self.game.state_data):__import__('combat_ui').open_combat(self.game)
            elif __import__('martos_campaigns').session(self.game.state_data):__import__('martos_campaign_ui').open_encounter(self.game)
            elif __import__('elias_campaigns').session(self.game.state_data):__import__('elias_campaign_ui').open_encounter(self.game)
            elif __import__('ace_campaigns').session(self.game.state_data):__import__('ace_campaign_ui').open_encounter(self.game)

    def history(self):
        self.cancel_flip()
        self.history_pages=[]
        for entry in self.game.state_data.get('campaign_dialogue_history',[]):
            if entry.get('player')==self.game.state_data['player']:
                self.history_pages.extend(presentation.archive(entry))
        if not self.history_pages:self.history_pages=[prose.page('Completed scenes will appear here. Reading history never repeats an action or reward.',title='Scene history')]
        self.history_mode=True;self.history_cursor=0;self.display()

    def recap(self):
        self.cancel_flip()
        self.history_pages=[prose.page(text,title='Story so far') for text in prose.recap(self.game.state_data)]
        self.history_mode=True;self.history_cursor=0;self.display()

    def return_current(self):
        self.cancel_flip()
        self.history_mode=False;self.archive_state=None
        if self.game.state_data.get('campaign_dialogue'):self.display()
        else:self.place_forget();self.game.show_in_person()

    def paint(self,event=None):
        if not self.history_mode and not self.game.state_data.get('campaign_dialogue'):return
        if not self.winfo_exists() or not self.illustration.winfo_ismapped():return
        import artwork
        c=self.illustration;w,h=c.winfo_width(),c.winfo_height()
        if w<30 or h<30:return
        b=self.current().copy();s=self.game.state_data
        b.update({k:self.unit[k] for k in ('background','portraits') if k in self.unit})
        art=b.get('background') or artwork.scene_art(b.get('venue',s['world']['location']),minute=b.get('minute',s['world']['minute']))
        room = __import__('interiors').ROOMS.get(b.get('room'))
        if room and b.get('mode') != 'memory' and not b.get('background'):
            art = room.art
        c.delete('all')
        core_id=getattr(self,'unit',{}).get('core_id')
        core_art=Path(__file__).parent/('assets/campaigns/takeo/core' if core_id and core_id.startswith('CS-TK') else 'assets/campaigns/ivan/core' if core_id and core_id.startswith('CS-IV') else 'assets/campaigns/neo/core' if core_id and core_id.startswith('CS-NE-') else 'assets/campaigns/sylvanis/core' if core_id and core_id.startswith('CS-SY') else 'assets/campaigns/camila/core' if core_id and core_id.startswith('CS-CA') else 'assets/campaigns/elias/core' if core_id and core_id.startswith('CS-EL') else 'assets/campaigns/martos/core' if core_id and core_id.startswith('CS-MT') else 'assets/campaigns/core')/str(core_id+'.png') if core_id else None
        is_core=False
        try:
            if core_art:
                # Keep every core gesture/object visible above the prose bubble.
                # A wide/compact stage must never crop faces or hide the selected
                # dramatic action underneath its reading area.
                with Image.open(core_art) as source:
                    fitted=ImageOps.contain(source.convert('RGB'),(w,max(60,h-max(155,min(230,int(h*.30)))-28)))
                im=Image.new('RGB',(w,h),ui.INK);im.paste(fitted,((w-fitted.width)//2,6))
                is_core=True
            else:im=ImageOps.fit(artwork.source_image(art).convert('RGB'),(w,h))
        except (OSError,ValueError):
            im=ImageOps.fit(artwork.source_image(art).convert('RGB'),(w,h))
            self.set_notice('Scene illustration unavailable. Your text and progress are preserved; continue or restore the artwork.')
        shade=Image.new('RGB',im.size,ui.INK);im=Image.blend(im,shade,.08 if is_core else .30)
        self.backdrop=ImageTk.PhotoImage(im,master=c)
        c.create_image(0,0,image=self.backdrop,anchor='nw')
        # Period-specific cast art only where the library has a verified asset.
        self.portraits={};cast=[]
        if not is_core and (b.get('mode')!='memory' or b.get('portraits')):
            cast=list(b.get('portraits',{}))
            if not cast and b.get('mode')!='memory':
                def drawable(who):
                    if who not in b.get('stage_cast',b.get('wardrobe_snapshot',{})) and ('stage_cast' in b or 'wardrobe_snapshot' in b):return False
                    if who in s['world']['cast']:return True
                    if not who:return False
                    _,path=self.game.portrait_path(who)
                    return path.is_file()
                cast=list(dict.fromkeys([s['player']]+[u.get('speaker') for u in presentation.units(b,s['player']) if drawable(u.get('speaker'))]))
            width=max(70,int((w-12)/len(cast)))
            sizes={who:(width,min(h-50,int(width*1.85))) for who in cast}
            if b.get('portraits') or b.get('wardrobe_snapshot'):
                # Explicit historical snapshot paths also apply to read-only
                # history; never borrow the currently active scene's wardrobe.
                import portrait_framing,character_stature
                loaded={}
                for who in cast:
                    if b.get('portraits'):
                        path=Path(__file__).parent/'assets/portraits'/(b['portraits'][who]+'.png')
                    else:
                        saved=__import__('camera').outfits(s,who).get(b['wardrobe_snapshot'].get(who)) if who in s['world']['cast'] else None
                        path=Path(__file__).parent/saved if saved else self.game.portrait_path(who,b.get('venue'),b.get('minute'))[1]
                    try:loaded[who]=(portrait_framing.load(path),sizes[who],character_stature.height_cm(who,path))
                    except (OSError,ValueError):
                        self.set_notice('Historical portrait unavailable. Text and progress are preserved; restore the matching era artwork.')
                scale=portrait_framing.shared_scale(list(loaded.values())) if loaded else None
                photos={who:ImageTk.PhotoImage(portrait_framing.fit(*entry,scale=scale),master=c) for who,entry in loaded.items()}
            else:photos=self.game.portrait_group(sizes,b.get('venue',s['world']['location']),b.get('minute',s['world']['minute']))
            for index,who in enumerate(cast):
                if who not in photos:continue
                picture=photos[who]
                self.portraits[who]=picture
                c.create_image((index+.5)*w/len(cast),h-25,image=picture,anchor='s')
                # Save the composed image for a deterministic outgoing page fold.
                portrait=ImageTk.getimage(picture)
                im.paste(portrait,(int((index+.5)*w/len(cast)-portrait.width/2),h-25-portrait.height),portrait)
        self.stage_raster=im.copy()
        caption='EARLIER · HONG KONG' if core_id=='CS-G05' else ('REMEMBERING' if b.get('mode')=='memory' else 'WINTERFIELD')
        owner=b.get('memory_owner',s['player'])
        if b.get('memory_owner') and owner!=s['player']:caption='RECOLLECTION HEARD'
        c.create_text(14,16,text=owner.upper()+'\n'+caption,anchor='nw',fill=ui.CREAM,font=('Segoe UI',11,'bold'))
        # Usually 30% of the stage, with a readable compact minimum now that the
        # voice controls occupy a row. Overflow stays scrollable and intact.
        box_width=max(140,min(840,w-48));box_height=max(155,min(230,int(h*.30)))
        # Empty choice/error rows used to reserve space even in ordinary prose,
        # leaving barely one line at large type sizes in a compact window.
        if self.options.winfo_children():self.options.grid()
        else:self.options.grid_remove()
        if self.notice.cget('text'):self.notice.grid()
        else:self.notice.grid_remove()
        compact=h<500
        self.paper.configure(pady=6 if compact else 10)
        self.chapter.grid_configure(pady=(0,4 if compact else 8))
        self.text.configure(pady=3 if compact else 6,spacing1=2 if compact else 3,spacing3=4 if compact else 7)
        dialogue_phase=self.unit['phase']=='dialogue'
        self.paper.configure(highlightbackground=ui.MINT if dialogue_phase else ui.EDGE)
        if dialogue_phase:
            left=(w-box_width)/2;top=h-14-box_height
            speaker=self.unit.get('speaker');anchor=(cast.index(speaker)+.5)*w/len(cast) if speaker in cast else w/2
            tail=max(left+30,min(left+box_width-50,anchor))
            c.create_polygon(tail,top,tail+22,top,tail+10,top-16,fill=ui.PANEL,outline=ui.MINT)
        c.create_window(w/2,h-14,window=self.paper,anchor='s',width=box_width,height=box_height)


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
    memories=prose.interpol_recollections(s)
    if memories:
        ttk.Label(parent,text='Fox’s recollections · meet your partner in the Interpol briefing room',foreground=ui.MINT,wraplength=620).pack(anchor='w',pady=(10,3))
        for key in memories:
            ttk.Button(parent,text='Revisit: '+prose.library()[key]['title'],
                       command=lambda k=key:act(prose.revisit_interpol,k)).pack(fill='x',pady=3)
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
                __import__('campaign_navigation').directions(card,game,spec['venue'])
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
