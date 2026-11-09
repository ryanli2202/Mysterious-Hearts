"""Find Charles: in-person actions and a private, persistent evidence notebook."""
import tkinter as tk
from tkinter import ttk
import charles_quest as quest
import town


class QuestPanel(ttk.Frame):
    def __init__(self,parent,game,close):
        super().__init__(parent,padding=18)
        self.game=game;self.close=close;self.notice=''
        ttk.Label(self,text=('Find Charles · Garrett’s private investigation' if game.state_data['player']=='garrett' else 'Charles sighting · helping Garrett'),font=('Segoe UI',18,'bold')).pack(anchor='w')
        ttk.Label(self,text='IN PERSON · Evidence and choices persist with your story.').pack(anchor='w',pady=4)
        ttk.Button(self,text='Return to location',command=close).pack(anchor='w',pady=5)
        self.canvas=tk.Canvas(self,bg='#1c2433',highlightthickness=0)
        scroll=ttk.Scrollbar(self,command=self.canvas.yview);scroll.pack(side='right',fill='y')
        self.canvas.pack(fill='both',expand=True);self.canvas.configure(yscrollcommand=scroll.set)
        self.body=ttk.Frame(self.canvas);item=self.canvas.create_window(0,0,window=self.body,anchor='nw')
        self.body.bind('<Configure>',lambda e:self.canvas.configure(scrollregion=self.canvas.bbox('all')))
        self.canvas.bind('<Configure>',lambda e:self.canvas.itemconfigure(item,width=e.width))
        self.draw()

    def act(self,fn,*args):
        if self.game.busy:return
        try:
            self.notice=fn(self.game.state_data,*args) or ''
            self.game.persist();self.game.render()
        except ValueError as exc:self.notice=str(exc)
        if self.winfo_exists():self.draw()

    def draw(self):
        for c in self.body.winfo_children():c.destroy()
        s=self.game.state_data
        if s['player']!='garrett':
            self.draw_report(s);return
        d=quest.read(s);title,venue,question=quest.objective(s)
        def label(text):ttk.Label(self.body,text=text,wraplength=760,justify='left').pack(fill='x',pady=6)
        label(('Search resolved · '+str(d['ending']) if d['step']>=len(quest.STEPS) else f'Chapter {d["step"]+1}/{len(quest.STEPS)} · '+title))
        label('Objective: '+town.location_name(s,venue)+'\n'+question)
        if s['world']['location']!=venue:
            ttk.Button(self.body,text='Travel to the current objective',command=lambda:self.act(town.travel,venue)).pack(anchor='w',pady=5)
        elif d['step']<len(quest.STEPS):
            for i,text in enumerate(quest.STEPS[d['step']][3]):
                ttk.Button(self.body,text=text,command=lambda n=i:self.act(quest.advance,n)).pack(anchor='w',pady=4)
        else:
            ttk.Button(self.body,text='Read today’s written check-in',command=lambda:self.act(quest.check_in)).pack(anchor='w',pady=4)
        if s['world']['location']==quest.LAB and d['step']<9:
            ttk.Button(self.body,text='I recognise Charles · request a private explanation',command=lambda:self.act(quest.recognise)).pack(anchor='w',pady=5)
        if 2<=d['step']<=8:label('One document response per story day. Use the story clock to wait, or return tomorrow.')
        if d['step'] in (9,10):label('Private meeting: 19:00–23:00. Come alone and wait until other laboratory staff have left. Your invitation grants visitor access only.')
        if d['setbacks']:label(f'Unverified approaches: {d["setbacks"]}. A setback never permanently closes the search.')
        label(self.notice)
        ttk.Separator(self.body).pack(fill='x',pady=8)
        label('Evidence notebook · verified findings only')
        for r in d['evidence']:label(r['title']+'\n'+r['finding'])
        for r in d['checkins'][-3:]:label(r['text'])
        __import__('phone_theme').apply_tree(self)

    def draw_report(self,s):
        import charles_disclosure as report
        d=report.read(s);stage=d.get('stage',0)
        def label(text):ttk.Label(self.body,text=text,wraplength=760,justify='left').pack(fill='x',pady=7)
        steps=('Tell Garrett what you witnessed','Ask Charles for a family reply','Deliver Charles’s sealed reply','Allow the brothers their private meeting','Ask Garrett about the reunion','Garrett has thanked you')
        label(steps[min(stage,5)])
        label('Speak privately and in person. You share your sighting, not knowledge of Charles’s motives. This does not unlock his phone number.')
        if stage==3:label('The visit is planned from 20:00 tomorrow after delivery, or the next available evening before 23:00. Leave the lab empty for twenty minutes. Other commitments and interruptions postpone the conversation.')
        elif stage<5:
            who='charles' if stage==1 else 'garrett';venue=s['world']['cast'][who]['location']
            label(who.title()+' is currently at '+town.location_name(s,venue))
            if s['world']['location']!=venue:ttk.Button(self.body,text='Travel to '+who.title(),command=lambda:self.act(town.travel,venue)).pack(anchor='w',pady=5)
            ttk.Button(self.body,text=steps[stage],command=lambda:self.act(report.act)).pack(anchor='w',pady=5)
        if self.notice not in d.get('journal',[]):label(self.notice)
        for entry in d.get('journal',[]):label(entry)
        __import__('phone_theme').apply_tree(self)
