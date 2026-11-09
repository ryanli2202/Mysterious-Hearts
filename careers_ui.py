"""Dark, phone-embeddable work and ambition dashboard."""
import tkinter as tk
import textwrap
from tkinter import ttk
from datetime import timedelta
import careers
import story_calendar as dates
import town
import winterfield_ui as ui
from phone_dialogs import AppWindow


class CareerControls:
    def __init__(self, game):
        super().__init__(game)
        self.game=game
        self.key=careers.available(game.state_data)[0]
        self.section='Work'
        self.notice=''
        self.replacing=None
        self.title('Work & ambitions')
        self.geometry('720x760')
        self.configure(bg=ui.INK)
        self.draw()

    def act(self, fn, *args):
        if self.game.busy:
            self.notice='Wait for the current conversation to finish.'
            self.draw(); return
        try:
            result=fn(self.game.state_data,*args)
            self.notice=result.get('text','Saved.') if isinstance(result,dict) else 'Saved.'
        except ValueError as exc:
            self.notice=str(exc)
        else:
            self.game.persist(); self.game.render()
        self.draw()

    def change(self, section):
        self.section=section; self.draw()

    def label(self, text, accent=False):
        ttk.Label(self.body,text=text,wraplength=560,justify='left',
                  foreground=ui.MINT if accent else ui.CREAM).pack(fill='x',pady=5)

    def button(self, text, fn, *args, enabled=True):
        button=ttk.Button(self.body,text=textwrap.fill(text,42) if self.phone else text,command=lambda:self.act(fn,*args),
                          state='normal' if enabled and not self.game.busy else 'disabled')
        button.pack(fill='x',pady=3)
        return button

    def draw(self):
        for child in self.winfo_children(): child.destroy()
        s=self.game.state_data; data=careers.ensure(s); d=careers.get(s,self.key); spec=careers.TRACKS[self.key]
        outer=ttk.Frame(self,padding=12); outer.pack(fill='both',expand=True)
        if getattr(self, 'embedded_main', False):
            ttk.Button(outer, text='‹ Back to location', command=self.game.leave_main_area).pack(anchor='w', pady=(0, 6))
        options=careers.available(s)
        self.track_box=ttk.Combobox(outer,values=[careers.TRACKS[k]['title'] for k in options],state='readonly')
        self.track_box.current(options.index(self.key)); self.track_box.pack(fill='x')
        def select(_):
            self.key=options[self.track_box.current()]; self.replacing=None; self.notice=''; self.draw()
        self.track_box.bind('<<ComboboxSelected>>',select)
        nav=ttk.Frame(outer); nav.pack(fill='x',pady=6)
        for text in ('Work','Project','Schedule','People','History'):
            ttk.Button(nav,text=text,width=8,command=lambda v=text:self.change(v)).pack(side='left',expand=True,fill='x')
        self.canvas=tk.Canvas(outer,bg=ui.PANEL,highlightthickness=0)
        scroll=ttk.Scrollbar(outer,command=self.canvas.yview); scroll.pack(side='right',fill='y')
        self.canvas.configure(yscrollcommand=scroll.set); self.canvas.pack(fill='both',expand=True)
        self.body=ttk.Frame(self.canvas,padding=6)
        item=self.canvas.create_window(0,0,window=self.body,anchor='nw')
        self.body.bind('<Configure>',lambda _:self.canvas.configure(scrollregion=self.canvas.bbox('all')))
        def fit(event):
            self.canvas.itemconfigure(item,width=event.width)
            for child in self.body.winfo_children():
                if isinstance(child,ttk.Label): child.configure(wraplength=max(160,event.width-20))
        self.canvas.bind('<Configure>',fit)
        self.canvas.bind('<MouseWheel>',lambda e:self.canvas.yview_scroll(-int(e.delta/120),'units'))
        self.label(town.loop.clock(s)+' · '+town.LOCATIONS[s['world']['location']],True)
        if self.notice: self.label(self.notice,True)
        self.label(f'Craft {d["craft"]} · Reputation {d["reputation"]} · Reliability {d["reliability"]}\n'
                   f'Fatigue {d["fatigue"]} · Autonomy {d["autonomy"]} · Preparation {d["training"]}/6')
        if self.section=='Work': self.work(s,data,d,spec)
        elif self.section=='Project': self.project(s,d,spec)
        elif self.section=='Schedule': self.schedule(s,data,spec)
        elif self.section=='People': self.people(s,d,spec)
        else:
            self.label('Private work journal. Only explicitly shared updates are supplied to other characters.')
            for item in reversed(data['history'][-40:]):
                if item['track']==self.key: self.label(stamp(item['minute'])+'\n'+item['text'])
            keepsakes=[x for x in s.get('career_keepsakes',[]) if x['track']==self.key]
            self.label('Keepsakes: '+('; '.join(x['title'] for x in keepsakes) or 'Complete a successful project to earn one.'))
        import phone_theme
        if self.phone:
            phone_theme.apply_tree(self.shell); self.after_idle(self._fit_content)

    def work(self,s,data,d,spec):
        if self.key in ('dragons','joker'):
            self.label('Organisation deals and executive meetings feed this career’s reputation, pressure and active project quality.')
            ttk.Button(self.body,text='Open Bubblegram leadership desk',command=self.open_leadership).pack(fill='x',pady=4)
        active=data['active']
        if active:
            current=careers.TRACKS[active['track']]
            scenario=careers.current_situation(active)
            self.label(current['title']+f' · decision {len(active["choices"])+1}/2',True)
            self.label(scenario[0])
            for i,text in enumerate(scenario[1:]):
                self.button(text+' · '+('craft','trust / reputation','autonomy / less fatigue')[i],careers.choose,i)
            self.button('Abandon session · no pay, reliability −3',careers.abandon)
            return
        self.label(f'{town.LOCATIONS[spec["venue"]]} · {spec["hours"][0]:02}:00–{spec["hours"][1]:02}:00\n'
                   'One work session per career each day. Longer sessions earn more and create more fatigue.')
        pay=0 if self.key in ('iron','taekwondo') else spec['pay']
        self.label(f'60 minutes: ${pay:,} · 120 minutes: ${pay*2:,}. Competitive preparation is unpaid.')
        self.button('Travel to workplace',town.travel,spec['venue'])
        self.button('Start 60-minute session · two decisions',careers.begin,self.key,60)
        self.button('Start 120-minute session · two decisions',careers.begin,self.key,120)
        self.button('Quick routine · 60 minutes, collaboration and boundaries',careers.quick,self.key)
        self.label('Preparation: once daily per career; recovery once daily. All take 60 minutes.')
        if self.key in ('iron','taekwondo'): self.button('Travel to daytime training · Arena lounge',town.travel,'arena')
        self.button('Practise technique · craft +2, preparation +1',careers.prepare,self.key,'technique')
        self.button('Get team feedback · trust +5, preparation +1',careers.prepare,self.key,'feedback')
        self.button('Travel home',town.travel,'home')
        self.button('Recover at home · fatigue −30',careers.prepare,self.key,'recovery')

    def open_leadership(self):
        if self.phone:
            self.phone.open_leadership()
        else:
            self.game.phone_window('Bubblegram')
            self.game.phone_activity.job_board.change('Leadership')

    def project(self,s,d,spec):
        self.label('Direction changes which decisions contribute most to project quality.')
        box=ttk.Combobox(self.body,values=careers.POLICIES[self.key],state='readonly')
        box.set(d['policy']); box.pack(fill='x',pady=4)
        box.bind('<<ComboboxSelected>>',lambda _:self.act(careers.set_policy,self.key,box.get()))
        if self.key=='iron':
            rival,target=careers.RIVALS[d['defences']%3]
            self.label(f'Rank #{d["rank"]} · Next rival: {rival} · Readiness target {target}\n'
                       'Defend or reclaim #1. Competitions require two preparations and seven days between bouts.')
            if d['defence_due']: self.label('Defence due: '+stamp(d['defence_due']))
            self.label('Match the rival: patient counters against pressure; draw out counter fighters; close distance against distance specialists. A matching plan adds 5 readiness.')
            plan=ttk.Combobox(self.body,values=('Counter patiently','Draw out an attack','Close distance carefully'),state='readonly')
            plan.set(d.get('match_plan','Counter patiently')); plan.pack(fill='x')
            plan.bind('<<ComboboxSelected>>',lambda _:self.act(careers.match_plan,self.key,plan.get()))
        if self.key=='taekwondo':
            self.label('Fictional future sporting pathway; these are game rules, not current Olympic qualification rules.')
            self.label(' → '.join(careers.PATHWAY))
            self.label('Next: '+(careers.PATHWAY[d['stage']] if d['stage']<5 else 'Post-Games invitational')+f' · Readiness target {58+min(d["stage"],4)*4}\n'
                       'Two preparations and seven days between competitions. Selection and medals must be earned.')
            self.label('Medals: '+(', '.join(x['medal'] for x in d['medals']) or 'None yet'))
        if self.key=='joker': self.label('A senior Joker Card balancing cross-branch obligations with a desire for independence. Private role; music contacts learn nothing automatically.')
        if self.key in ('dragons','joker'): self.label(f'Unresolved pressure: {d["pressure"]}. Mediation, boundaries and reviewed delegation reduce it.')
        p=d['project']
        if not p:
            self.button('Start '+spec['project'],careers.start_project,self.key)
            return
        self.label(p['title'],True)
        self.label(f'Work days: {len(p["days"])}/3 · Quality: {p["quality"]}\nDeadline: {stamp(p["deadline"])}'+(' · OVERDUE' if p['overdue'] else ''))
        self.label('Complete work on three separate days. Schedule a 60-minute finale and arrive within 15 minutes of the booked start. Late projects lose reliability once and receive a lower review score; they can still finish. Reputation 75 unlocks advanced project briefs after your first completion.')
        self.button('Negotiate three more days · reliability −2',careers.extend_project,self.key,enabled=not p['extended'])
        self.label('Readiness uses craft, project quality, preparation, reliability and fatigue. Leadership pressure and overdue work reduce it.')

    def schedule(self,s,data,spec):
        tomorrow=dates.story_date(s['world']['minute'])+timedelta(days=1)
        self.label('Book a commitment. Conflicts with Calendar events and other careers are rejected. Cancel ahead of time without penalty.')
        if self.replacing: self.label('Rescheduling the selected booking. Its original time stays reserved until the replacement succeeds.',True)
        self.fields={}
        for name,value in [('Date',tomorrow.isoformat()),('Time',f'{spec["hours"][0]:02}:00')]:
            self.label(name)
            entry=ttk.Entry(self.body); entry.insert(0,value); entry.pack(fill='x'); self.fields[name]=entry
        self.kind=ttk.Combobox(self.body,values=('shift','finale'),state='readonly'); self.kind.set('shift'); self.kind.pack(fill='x',pady=5)
        self.duration=ttk.Combobox(self.body,values=('60','120'),state='readonly'); self.duration.set('60'); self.duration.pack(fill='x',pady=5)
        ttk.Button(self.body,text='Save booking',command=self.save_booking).pack(fill='x',pady=6)
        for b in data['bookings'][-30:]:
            if b['track']!=self.key: continue
            self.label(stamp(b['start'])+' · '+b['kind']+' · '+b['status'])
            if b['status']!='booked': continue
            self.button('Travel to venue',town.travel,b['venue'])
            delta=b['start']-s['world']['minute']
            if delta>0: self.button('Wait until start (up to two days)',self.wait_booking,b['id'],enabled=delta<=2880)
            self.button('Begin booked work / finale',careers.begin,self.key,60,b['id'])
            self.button('Cancel booking',careers.cancel,b['id'])
            if delta>0:
                ttk.Button(self.body,text='Reschedule',command=lambda ident=b['id']:self.reschedule(ident)).pack(fill='x',pady=3)

    def save_booking(self):
        def save(s):
            item=careers.book(s,self.key,self.fields['Date'].get(),self.fields['Time'].get(),
                              self.kind.get(),int(self.duration.get()),self.replacing)
            self.replacing=None
            return item
        self.act(save)

    def reschedule(self, ident):
        self.replacing=ident; self.draw()

    def wait_booking(self,s,ident):
        b=next(b for b in careers.ensure(s)['bookings'] if b['id']==ident)
        delta=b['start']-s['world']['minute']
        if not 0<delta<=2880: raise ValueError('Wait in steps of up to two days.')
        if careers.ensure(s)['active']: raise ValueError('Finish your current session first.')
        town.loop.advance(s,delta)

    def people(self,s,d,spec):
        self.label('Recurring workplace roles; these relationships do not create romance routes or phone contacts.')
        for name,person in d['contacts'].items():
            self.label(f'{name} · Trust {person["trust"]} · Experience {person["competence"]}')
            if self.key in ('dragons','joker'):
                self.button('Delegate follow-up to '+name+' · 30 minutes',careers.delegate,self.key,name)
        if d['delegation']:
            self.label('Report from '+d['delegation']['person']+' due '+stamp(d['delegation']['due']))
            self.button('Review delegation · 30 minutes',careers.review_delegation,self.key)
        self.label('Share the latest recorded update with a known contact. This explicitly reveals that update, including private work if selected. It does not invent a reply or grant romance progress.')
        people=[who for who in s['world']['cast'] if who!=s['player'] and town.hidden.contact(s,who)]
        if people:
            box=ttk.Combobox(self.body,values=people,state='readonly'); box.current(0); box.pack(fill='x',pady=5)
            ttk.Button(self.body,text='Share latest update with selected contact',command=lambda:self.act(careers.share,self.key,box.get())).pack(fill='x')


class CareersWindow(CareerControls, AppWindow):
    pass


class CareersPanel(CareerControls, tk.Frame):
    """Expanded cast work takes place in the main in-person window."""
    embedded_main = True
    phone = None

    def __init__(self, game):
        tk.Frame.__init__(self, game.play_body, bg=ui.INK)
        self.game = game
        self.key = careers.available(game.state_data)[0]
        self.section = 'Work'
        self.notice = ''
        self.replacing = None
        self.draw()


def open_careers(game):
    import playable_cast
    if not playable_cast.is_new(game.state_data['player']): return CareersWindow(game)
    import groups
    active = game.state_data.get('active_group')
    if active and game.state_data['groups'].get(active, {}).get('channel') != 'text':
        groups.close_active(game.state_data, 'Left the conversation to focus on work.')
    game.close_main_area()
    game.hide_phone_for_location()
    panel = CareersPanel(game)
    game.area_view = panel
    game.layout_presence()
    return panel


def stamp(minute):
    return f'{dates.story_date(minute):%b %d} · {minute%1440//60:02}:{minute%60:02}'
