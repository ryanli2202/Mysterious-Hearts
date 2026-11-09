"""Location-bound activities embedded in the ordinary in-person scene."""
import tkinter as tk
from tkinter import ttk
import crime_sites as sites
import crime_operations as ops
import town


class SiteActivities(ttk.Frame):
    def __init__(self, parent, game):
        super().__init__(parent)
        self.game = game
        self.location = game.state_data['world']['location']
        self.key = ops.site_of(self.location)
        self.notice = ''
        self.notice_owner = game.state_data['player']
        self.viewport = tk.Canvas(self, bg='#1c2433', highlightthickness=0, height=300)
        scroll = ttk.Scrollbar(self, command=self.viewport.yview)
        scroll.pack(side='right', fill='y')
        self.viewport.pack(fill='both', expand=True)
        self.viewport.configure(yscrollcommand=scroll.set)
        self.content = ttk.Frame(self.viewport)
        item = self.viewport.create_window(0, 0, window=self.content, anchor='nw')
        self.content.bind('<Configure>', lambda e:self.viewport.configure(scrollregion=self.viewport.bbox('all')))
        self.viewport.bind('<Configure>', lambda e:self.viewport.itemconfigure(item, width=e.width))
        self.draw()

    def act(self, fn, *args):
        if self.game.busy: return
        self.notice_owner = self.game.state_data['player']
        try:
            self.notice = fn(self.game.state_data, *args) or ''
            self.game.persist()
            self.game.render()
        except ValueError as exc:
            self.notice = str(exc)
        if self.winfo_exists(): self.draw()

    def draw(self):
        for child in self.content.winfo_children(): child.destroy()
        s = self.game.state_data
        box = ttk.Frame(self.content, padding=4); box.pack(fill='both', expand=True)
        if self.location == 'glasshouse_lab':
            import criminal_dynamics as dynamics
            if not dynamics.research_access(s['player'],s):
                ttk.Label(box,text='Private visitor appointment',style='Section.TLabel').pack(anchor='w')
                ttk.Label(box,text='Your visitor invitation grants no access to laboratory research or operational records.',wraplength=390).pack(fill='x',pady=6)
                if s['player']=='garrett':
                    ttk.Button(box,text='Find Charles · private meeting',command=self.game.charles_search).pack(fill='x',pady=4)
                self.notice=''
                __import__('phone_theme').apply_tree(self)
                return
            ttk.Label(box, text='Sylvanis’s private research desk', style='Section.TLabel').pack(anchor='w')
            ttk.Label(box, text='Blue Magic and Red Magic development. Personal clearance or Syndicate Jack rank required. Sylvanis normally works here from 10:00 to 18:00; mornings and evenings at headquarters.', wraplength=390).pack(fill='x', pady=6)
            ttk.Button(box, text='Review research and supply briefing', command=lambda:self.act(dynamics.laboratory_briefing)).pack(fill='x', pady=4)
            import laboratory_missions as missions
            allowed = missions.private(s)
            if self.notice_owner != s['player'] or (s['player'] in dynamics.INNER and not allowed):
                self.notice = ''
            if allowed:
                self.lab_missions(box, s, missions)
            ttk.Label(box, text=self.notice, wraplength=390, justify='left').pack(fill='x', pady=6)
            __import__('phone_theme').apply_tree(self)
            return
        if self.key not in sites.SITES:
            self.records(box, s)
            __import__('phone_theme').apply_tree(self)
            return
        for text,fn,args in (
            ('Enter public reception',ops.enter,(self.key,'reception')),
            ('Enter controlled briefing room',ops.enter,(self.key,'briefing')),
            ('Request a personal briefing pass',ops.request_pass,(self.key,)),
            ('Return outside',ops.exit_site,(self.key,)),
        ):
            if fn is ops.enter and args[1]=='reception' and self.location==self.key+'_reception': continue
            if fn is ops.enter and args[1]=='briefing' and self.location!=self.key+'_reception': continue
            if fn is ops.request_pass and self.location!=self.key+'_reception': continue
            if fn is ops.exit_site and self.location==self.key: continue
            ttk.Button(box,text=text,command=lambda f=fn,a=args:self.act(f,*a)).pack(fill='x',pady=3)
        ttk.Label(box,text=ops.access_text(s,self.key),wraplength=390).pack(fill='x',pady=6)
        ttk.Label(box,text=ops.hierarchy(s,self.key),wraplength=390).pack(fill='x',pady=6)
        active=ops.read(s).get('active')
        if active:
            ttk.Label(box,text='Active assignment: '+sites.label(s,active['site'])+'\n'+active['issuer']+'\n'+active['question'],wraplength=390).pack(fill='x',pady=6)
            if active.get('colleague'):
                ttk.Label(box,text='Joint review with '+active['colleague_label'],wraplength=390).pack(fill='x')
            for index,option in enumerate(active['options']):
                ttk.Button(box,text=option,command=lambda i=index:self.act(ops.resolve,i)).pack(fill='x',pady=3)
            ttk.Button(box,text='Abandon assignment',command=lambda:self.act(ops.abandon)).pack(fill='x',pady=3)
        else:
            for kind,text in (('reception','Reception: review a visitor packet'),('briefing','Briefing: handle a disputed request'),('command','Command: respond to an Ace mandate')):
                if kind=='reception' and self.location!=self.key+'_reception': continue
                if kind!='reception' and self.location!=self.key+'_briefing': continue
                button=ttk.Button(box,text=text,command=lambda k=kind:self.act(ops.begin,self.key,k))
                button.pack(fill='x',pady=3)
                if kind=='command' and not ops.authority(s['player'],self.key): button.state(['disabled'])
            import faction_work, game_core as core
            kind='reception' if self.location.endswith('_reception') else 'briefing'
            for who in faction_work.colleagues(s,self.key):
                ttk.Button(box,text='Review request with '+core.contact_name(s,who),command=lambda person=who:self.act(ops.begin,self.key,kind,person)).pack(fill='x',pady=3)
                if ops.authority(s['player'],self.key) and self.location.endswith('_briefing') and faction_work.disclosure(s):
                    ttk.Button(box,text='Discuss mandate with '+core.contact_name(s,who),command=lambda person=who:self.act(ops.begin,self.key,'command',person)).pack(fill='x',pady=3)
        p=ops.progress(s,self.key)
        ttk.Label(box,text=f'Local standing {p["standing"]} · pressure {p["pressure"]}\nUnresolved harm {p["harm"]} · evidence {p["evidence"]}\nReliable reception days {len(p["days"])}',wraplength=390).pack(fill='x',pady=6)
        for item in [x for x in ops.read(s).get('history',[]) if x['site']==self.key][-3:]:
            ttk.Label(box,text=item['text'],wraplength=390).pack(fill='x',pady=4)
        ttk.Label(box, text=sites.notebook(s, self.key), wraplength=390, justify='left').pack(fill='x', pady=6)
        if self.location == self.key:
            ttk.Button(box, text='Inspect exterior', command=lambda:self.act(sites.inspect,self.key)).pack(fill='x',pady=3)
        ttk.Label(box,text=self.notice,wraplength=390,foreground='#a8cde8').pack(fill='x',pady=6)
        __import__('phone_theme').apply_tree(self)

    def lab_missions(self, box, s, missions):
        ttk.Label(box, text='Private laboratory assignments', style='Section.TLabel').pack(anchor='w', pady=6)
        ttk.Label(box, text='Ivan and the Four Aces normally review work here from 17:00 to 18:00. Your specialist must be present. Reviews record internal preparation, not field deployment.', wraplength=390).pack(fill='x')
        d = missions.read(s)
        ttk.Label(box, text=f"Readiness {d.get('readiness', 0)} · unresolved concerns {d.get('concerns', 0)}", wraplength=390).pack(fill='x', pady=4)
        active = d.get('active')
        if active:
            index = len(active['choices'])
            question, choices = active['stages'][index]
            ttk.Label(box, text=active['title'] + f' · step {index+1}/2\n' + question, wraplength=390).pack(fill='x', pady=6)
            for i, label in enumerate(choices):
                button = ttk.Button(box, text=label, command=lambda n=i:self.act(missions.choose,n))
                button.pack(fill='x', pady=3)
                if not missions.present(s,active['partner']): button.state(['disabled'])
            ttk.Button(box, text='Set this review aside', command=lambda:self.act(missions.abandon)).pack(fill='x', pady=3)
        else:
            for key, spec in missions.MISSIONS.items():
                done = key in d.get('completed', {})
                ready = all(k in d.get('completed', {}) for k in spec['requires'])
                here = missions.present(s,missions.partner(s,key))
                status = 'Completed' if done else 'Prerequisites needed' if not ready else 'Colleague away' if not here else 'Begin'
                button = ttk.Button(box, text=spec['title'] + ' · ' + status, command=lambda k=key:self.act(missions.begin,k))
                button.pack(fill='x', pady=3)
                if done or not ready or not here: button.state(['disabled'])
        for record in d.get('history', [])[-2:]:
            ttk.Label(box, text=record['title'] + '\n' + record['outcome'], wraplength=390).pack(fill='x', pady=4)

    def records(self, box, s):
        ttk.Label(box,text='Public site records',style='Section.TLabel').pack(anchor='w')
        keys=[k for k in sites.SITES if sites.known_name(s,k)]
        if not keys:
            ttk.Label(box,text='Identify a site during a visit before requesting its records.',wraplength=390).pack(fill='x')
            return
        chosen = getattr(self, 'record_key', keys[0])
        picker=ttk.Combobox(box,state='readonly',values=[sites.label(s,k) for k in keys])
        picker.current(keys.index(chosen));picker.pack(fill='x',pady=4)
        def select(event):
            self.record_key=keys[picker.current()];self.notice='';self.draw()
        picker.bind('<<ComboboxSelected>>',select)
        fn=sites.research if self.location=='archive' else sites.verify
        ttk.Button(box,text='Read public records' if self.location=='archive' else 'Verify published exhibit',command=lambda:self.act(fn,chosen)).pack(fill='x',pady=4)
        ttk.Label(box,text=sites.notebook(s,chosen),wraplength=390).pack(fill='x')
        ttk.Label(box,text=self.notice,wraplength=390,foreground='#a8cde8').pack(fill='x',pady=6)
