"""Story missions, guard encounters and property management on the in-person stage."""
import tkinter as tk
from tkinter import ttk
import organisation_guards as guards
import rei_story
import town
import phone_theme
import winterfield_ui as ui

def open_in_person(game, page='Guards'):
    if game.busy: return
    game.hide_phone_for_location()
    view=getattr(game,'campaign_view',None)
    if view is None or not view.winfo_exists():
        view=game.campaign_view=CampaignView(game.presence_view.master,game)
    view.page='Story' if page=='Rei’s story' else page; view.place(x=0,y=0,relwidth=1,relheight=1); view.lift(); view.draw()

class CampaignView(tk.Frame):
    def __init__(self,parent,game):
        super().__init__(parent,bg=ui.INK,padx=16,pady=12)
        self.game=game; self.page='Guards'; self.notice=''
        ttk.Label(self,text='WINTERFIELD · STORIES & ORGANISATIONS',font=('Segoe UI',18,'bold')).pack(anchor='w')
        nav=ttk.Frame(self); nav.pack(fill='x',pady=6)
        for page in ('Story','After the story','Guards','Properties'):
            ttk.Button(nav,text=page,command=lambda p=page:self.change(p)).pack(side='left',padx=3)
        ttk.Button(nav,text='Return to location',command=self.leave).pack(side='right')
        self.canvas=tk.Canvas(self,bg=ui.INK,highlightthickness=0)
        scroll=ttk.Scrollbar(self,command=self.canvas.yview); scroll.pack(side='right',fill='y')
        self.canvas.pack(fill='both',expand=True); self.canvas.configure(yscrollcommand=scroll.set)
        self.body=ttk.Frame(self.canvas,padding=8); item=self.canvas.create_window(0,0,window=self.body,anchor='nw')
        self.body.bind('<Configure>',lambda e:self.canvas.configure(scrollregion=self.canvas.bbox('all')))
        self.canvas.bind('<Configure>',lambda e:self.canvas.itemconfigure(item,width=e.width))
        self.canvas.bind('<MouseWheel>',lambda e:self.canvas.yview_scroll(-int(e.delta/120),'units'))

    def leave(self): self.place_forget(); self.game.show_in_person()
    def change(self,p): self.page=p; self.draw(); self.canvas.yview_moveto(0)
    def label(self,text):
        w=ttk.Label(self.body,text=text,wraplength=730,justify='left');w.pack(fill='x',pady=6)
        w.bind('<Configure>',lambda e:w.configure(wraplength=max(90,e.width-12)))
    def button(self,text,fn,*args):
        ttk.Button(self.body,text=text,command=lambda:self.act(fn,*args)).pack(fill='x',pady=4)
    def act(self,fn,*args):
        if self.game.busy:return
        try:
            if __import__('campaign_dialogue').maybe_open(self.game,fn,args):return
            self.notice=fn(self.game.state_data,*args) or '';self.game.persist()
        except ValueError as exc:self.notice=str(exc)
        self.draw()
        if __import__('combat').active(self.game.state_data): __import__('combat_ui').open_combat(self.game)
    def draw(self):
        for w in self.body.winfo_children():w.destroy()
        s=self.game.state_data
        self.label('IN PERSON · '+town.location_name(s,s['world']['location']))
        if self.notice:self.label(self.notice)
        import combat
        if combat.recovering(s):self.button('Rest through knockout recovery',town.wait,combat.recovering(s))
        if self.page in ('Story','Rei’s story'):self.story(s)
        elif self.page=='After the story':__import__('post_story_ui').board(self.body,self.game,self.act)
        elif self.page=='Properties':self.properties(s)
        else:self.guards(s)
        phone_theme.apply_tree(self)
    def story(self,s):
        if s['player']=='garrett':
            self.label('GARRETT’S STORY · Find Charles')
            __import__('charles_quest_ui').story_board(self.body,self.game,self.act)
            return
        if s['player'] in ('fox','gordon'):
            self.label(('FOX' if s['player']=='fox' else 'GORDON')+'’S STORY · Interpol campaign')
            import interpol_ui, interpol
            interpol_ui.CaseBoard(self.body,self.game,self.act).cases(s,interpol.ensure(s))
            return
        if s['player']!='rei':
            self.label('No personal story campaign is available for this character yet.')
            return
        __import__('campaign_prose_ui').board(self.body,self.game,self.act)
        d=rei_story.data(s)
        import campaign_flashbacks
        memory=campaign_flashbacks.pending(s)
        if memory:
            scene=campaign_flashbacks.SCENES[memory]
            self.label('MANDATORY FLASHBACK · '+scene['title'])
            self.label('Return home alone for this chapter memory. Each memory returns to the present with a reflection; you can pause or visit an available friend between them.')
            if s['world']['location']!=scene['venue']:self.button('Travel to the memory’s starting point',town.travel,scene['venue'])
            else:self.button('Begin flashback · '+scene['title'],campaign_flashbacks.start,memory)
            return
        if d['complete']:
            ttk.Button(self.body,text='Repeatable protection missions',command=lambda:self.change('After the story')).pack(fill='x',pady=5)
        self.label('WHAT REMAINS · '+('Complete' if d['complete'] else 'Investigation in progress'))
        if d['stage']<len(rei_story.SCENES):
            title,venue,scene,choices,_=rei_story.SCENES[d['stage']]
            self.label(title+'\nObjective: '+town.location_name(s,venue))
            if s['world']['location']!=venue:self.button('Travel to objective',town.travel,venue)
            else:
                self.label('Read this scripted scene in the illustrated in-person hangout. Your response is recorded after its final line.')
                for i,c in enumerate(choices):self.button(c,rei_story.advance,i)
        else:
            self.label('Hamayashi-kai: '+str(d['hamayashi'] or 'Decision pending')+' · Richter: '+('Defeated' if d['richter'] else 'Unresolved'))
            if not d['hamayashi']:
                self.button('Travel to Kurose House',town.travel,'hamayashi_house')
                for key,title in (('destroy','Attack and dismantle the successor'),('lead','Accept leadership under the new charter'),('leave','Leave the successor alone')):
                    self.button(title,rei_story.choose,key)
            sites=(guards.HAMAYASHI if d['hamayashi']=='destroy' else ())+(guards.BLACKSTONE if not d['richter'] else ())
            for venue in sites:
                scope='rei:hamayashi' if venue in guards.HAMAYASHI else 'rei:blackstone'
                self.label(town.location_name(s,venue)+f' · {len(guards.remaining(s,venue,scope))} guards remaining')
                if s['world']['location']!=venue:self.button('Travel here',town.travel,venue)
                elif guards.remaining(s,venue,scope):self.button('Fight next mission guard',rei_story.fight_guards)
            if not d['richter'] and s['world']['location']=='blackstone_command' and guards.cleared(s,guards.BLACKSTONE,'rei:blackstone'):
                self.label('The command perimeter is clear. Confront Richter in person.')
                self.button('Confront Richter · mandatory fight',rei_story.confront)
        self.label('Private evidence notebook')
        for r in d['journal']:self.label(r['text'])
    def guards(self,s):
        venue=s['world']['location']; rows=list(guards.npc_rows(s).values())
        self.label('Local guard posts · patrols replenish each story day. Mission defeats persist separately.')
        for r in rows:
            name,kind,art,equipment,power,skill=guards.spec(s,r['type'])
            self.guard_card(s,r['type'],f'{name} · {kind} · {art}'+(' · '+equipment if equipment else ''))
        self.guard_desk(s)
        if rows:
            self.button('Challenge next local guard',guards.begin)
            for ally in guards.patrol_allies(s):
                self.button('Challenge with '+__import__('combat').profile(s,ally)['name']+' supporting',guards.begin,venue,'patrol',ally)
        else:self.label('No active guards at this location.')
        self.label('Member deployment directory · only your organisations are listed')
        for venue,faction,count,types in guards.directory(s):
            self.label(town.location_name(s,venue)+f' · {count} active · '+', '.join(types))
            self.label(guards.ORGANISATIONS.get(faction,'Local crew protection, lookout and enforcement duties.'))
            self.button('Travel to deployment',town.travel,venue)
    def talk_guard(self,name):
        if self.game.busy:return
        try:
            __import__('groups').open_local(self.game.state_data,name)
            self.game.persist();self.place_forget();self.game.show_in_person()
        except ValueError as exc:self.notice=str(exc);self.draw()

    def guard_desk(self,s):
        import guard_dialogue as dialogue
        names=list(guards.npc_rows(s))
        if not names:return
        self.label('Guard desk · talk, visitor requests and command')
        selected=ttk.Combobox(self.body,state='readonly',values=names);selected.set(names[0]);selected.pack(fill='x')
        ttk.Button(self.body,text='Talk to selected guard · in person',command=lambda:self.talk_guard(selected.get())).pack(fill='x',pady=4)
        for label,key in (('Ask for directions','directions'),('Ask who is in charge','leadership'),
                          ('Check credentials / visitor authorisation','credentials'),('Lodge a visit request','appointment'),
                          ('Approach restricted boundary','boundary'),
                          ('Order a post status report','status'),('Order a referral','refer')):
            ttk.Button(self.body,text=label,command=lambda k=key:self.act(dialogue.act,selected.get(),k)).pack(fill='x',pady=2)
        self.label('Report a problem · describe what happened (up to 500 characters)')
        report=ttk.Entry(self.body);report.pack(fill='x',pady=3)
        ttk.Button(self.body,text='Record problem report',command=lambda:self.act(dialogue.act,selected.get(),'report',report.get())).pack(fill='x',pady=3)
        present=[who for who,p in s['world']['cast'].items() if who!=s['player'] and p.get('location')==s['world']['location'] and not p.get('journey')]
        self.label('Command · authorise a present visitor at this post for today')
        target=ttk.Combobox(self.body,state='readonly',values=present);target.pack(fill='x')
        if present:target.set(present[0])
        for label,key in (('Authorise visitor','admit'),('Revoke visitor authorisation','revoke')):
            ttk.Button(self.body,text=label,state='normal' if present else 'disabled',command=lambda k=key:self.act(dialogue.act,selected.get(),k,target.get())).pack(fill='x',pady=2)
        legacy=s.get('guard_social',{}).get('legacy',{})
        histories=[v for v in legacy.values() if isinstance(v,dict) and v.get('history')]
        if histories:
            self.label('Archived guard conversations · retained from older saves')
            for record in histories:
                for line in record['history']:
                    self.label(str(line.get('speaker',''))+': '+str(line.get('text','')))

    def properties(self,s):
        d=guards.data(s)
        self.label('Custom gang sites · purchase and recruitment take place at the property. Twelve guard posts per site.')
        for venue,(name,price,_) in guards.PROPERTIES.items():
            owned=d['properties'].get(venue)
            self.label(name+' · '+(owned['owner']+' / '+owned['use'] if owned else f'Vacant · ${price:,}'))
            if venue!=s['world']['location']:self.button('Visit property',town.travel,venue)
            elif not owned:
                for use in ('Hideout','Affiliate'):self.button('Purchase as '+use,guards.buy,venue,use)
            else:
                self.label('Guard type name')
                name_entry=ttk.Entry(self.body);name_entry.insert(0,'House guard');name_entry.pack(fill='x',pady=4)
                category=ttk.Combobox(self.body,state='readonly',values=('unawakened','awakened','robotic'));category.set('unawakened');category.pack(fill='x')
                self.label('Recruitment: unawakened $1,500 · awakened $6,000 · robotic $9,000')
                ttk.Button(self.body,text='Recruit and station guard',command=lambda v=venue,n=name_entry,c=category:self.act(guards.recruit,n.get(),c.get(),v)).pack(fill='x',pady=4)
                for r in d['roster']:
                    self.guard_card(s,r['type'],guards.spec(s,r['type'])[0]+' · '+town.location_name(s,r['venue']))
                    ttk.Button(self.body,text='Rename this type using the name above',command=lambda k=r['type'],n=name_entry:self.act(guards.rename_type,k,n.get())).pack(fill='x',pady=4)
                    if r['venue']!=venue:self.button('Station this guard here',guards.station,r['id'],venue)

    def guard_card(self,s,kind,text):
        import guard_portraits
        ident=guard_portraits.type_id(s,kind)
        card=ttk.Frame(self.body,padding=6);card.pack(fill='x',pady=4)
        if ident and guard_portraits.path(ident).is_file():
            photo=self.game.portrait('guard_art_'+ident,(90,135),s['world']['location'],s['world']['minute'])
            portrait=ttk.Label(card,image=photo);portrait.image=photo;portrait.pack(side='left',padx=(0,12))
        ttk.Label(card,text=text,wraplength=580,justify='left').pack(side='left',fill='x',expand=True)

def phone_directory(parent,game):
    """Read-only phone directory and a handoff; no recruitment or combat here."""
    s=game.state_data
    ttk.Label(parent,text='Guard deployments · members only',wraplength=300).pack(fill='x',pady=4)
    rows=guards.directory(s)
    for venue,faction,count,types in rows:
        ttk.Label(parent,text=town.location_name(s,venue)+f' · {count}\n'+', '.join(types),wraplength=300).pack(fill='x',pady=4)
    if not rows:ttk.Label(parent,text='Join an organisation to see its deployments.',wraplength=300).pack(fill='x')
    ttk.Button(parent,text='Guards & properties · open in person',command=lambda:open_in_person(game)).pack(fill='x',pady=5)
