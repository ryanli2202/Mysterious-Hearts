"""Dark records on the phone; all field work lives on the in-person stage."""
import tkinter as tk
from tkinter import ttk
import interpol as law
import town
import winterfield_ui as ui
import phone_theme


def label(parent,text,accent=False):
    w=ttk.Label(parent,text=text,wraplength=760,justify='left',foreground=ui.MINT if accent else ui.CREAM)
    w.pack(fill='x',pady=5)
    w.bind('<Configure>',lambda e:w.configure(wraplength=max(90,e.width-12)))
    return w


def open_in_person(game):
    if game.busy: return
    game.hide_phone_for_location()
    view=getattr(game,'interpol_view',None)
    if view is None or not view.winfo_exists(): view=game.interpol_view=InterpolView(game.presence_view.master,game)
    view.place(x=0,y=0,relwidth=1,relheight=1); view.lift(); view.draw()


class RecordPanel(ttk.Frame):
    """No physical actions: a private record and remote fine payment only."""
    def __init__(self,parent,game,compact=False):
        super().__init__(parent,padding=6)
        self.game=game;self.compact=compact;self.notice='';self.pack(fill='x',pady=6);self.draw()

    def pay(self,ident):
        if self.game.busy:return
        try:self.notice=law.pay(self.game.state_data,ident);self.game.persist()
        except ValueError as exc:self.notice=str(exc)
        self.draw()

    def draw(self):
        for w in self.winfo_children():w.destroy()
        s=self.game.state_data;d=law.ensure(s)
        label(self,'INTERPOL · PRIVATE RECORD',True)
        role='Team 9 commander' if s['player']=='gordon' else 'Licensed associate' if s['player']=='fox' else 'Case assistant' if law.clearance(s,s['player']) else 'Public services'
        if 'interpol' in s.get('combat',{}).get('expelled',[]):role='Interpol access revoked'
        label(self,f'{role}\nOutstanding fines ${law.debt(s):,} · Available funds ${int(s["world"]["money"]):,}')
        area=law.district(s['world']['location'])
        label(self,f'{area.title()} influence {law.influence(s,area)}/100. Influence affects patrol observation; it does not establish guilt.')
        a=d['active']
        if a:label(self,'Current objective: '+law.objective(s)['title']+'\n'+town.location_name(s,law.objective(s)['venue']))
        ttk.Button(self,text='Open Interpol in person',command=lambda:open_in_person(self.game)).pack(fill='x',pady=4)
        fines=[f for f in d['fines'] if f['actor']==s['player']]
        for f in reversed(fines[-8:] if self.compact else fines):
            remaining=f['amount']-f['paid']
            label(self,f'{law.OFFENCES[f["kind"]][0]} · ${f["amount"]}\n{f["issuer"]}\nPaid ${f["paid"]} · remaining ${remaining}')
            if remaining:ttk.Button(self,text='Pay available funds toward this fine',command=lambda ident=f['id']:self.pay(ident)).pack(fill='x',pady=3)
        if not fines:label(self,'No fines recorded for this protagonist.')
        if not self.compact:
            for ident in d['knowledge'].get(s['player'],{}).get('identities',[]):
                import four_aces
                label(self,four_aces.CAST[ident]['name']+' · Ace of '+four_aces.CAST[ident]['suit'] if ident in four_aces.IDS else 'Crow command location established by the case file.',True)
        if self.notice:label(self,self.notice,True)
        phone_theme.apply_tree(self)


def bubblegram_header(parent,game):
    RecordPanel(parent,game,compact=True)


class CaseBoard:
    """Shared case controls for the Interpol window and protagonist Story tab."""
    def __init__(self,parent,game,act):
        self.body=parent;self.game=game;self.act=act

    def button(self,text,fn,*args,enabled=True):
        b=ttk.Button(self.body,text=text,command=lambda:self.act(fn,*args),
                     state='normal' if enabled and not self.game.busy else 'disabled')
        b.pack(fill='x',pady=4)
        return b

    def desk(self,s):
        if s['world']['location']!='interpol_hq':self.button('Travel to Interpol public desk',town.travel,'interpol_hq')
        elif not law.clearance(s,s['player']):self.button('Register as a civilian case assistant',law.enrol)
        label(self.body,'Assemble at the public desk with your field partner: Gordon normally 08:00–12:00; Fox 13:00–16:00. Resuming requires another in-person briefing. Existing appointments and recovery can change attendance.')
        if s['world']['location']=='interpol_hq':self.button('Wait 30 story minutes',town.loop.advance,30)

    def active(self,s,d):
        a=d['active'];step=law.objective(s)
        label(self.body,(law.OPERATIONS if a['repeatable'] else law.CASES)[a['key']]['title'],True)
        label(self.body,'Objective: '+step['title']+'\nLocation: '+town.location_name(s,step['venue'])+'\nPartner: '+a['partner'].title())
        import combat
        if combat.active(s):self.button('Continue operation combat',lambda state:__import__('combat_ui').open_combat(self.game))
        elif law.regroup_delay(s):
            label(self.body,f'The team needs {law.regroup_delay(s)} story minutes to regroup or recover before another attempt.')
            self.button('Rest through the team’s recovery',law.regroup)
        elif s['world']['location']!=step['venue']:self.button('Travel to objective with field partner',law.travel_objective)
        else:self.button('Begin field combat' if step['kind']=='combat' else step['title']+' · 20 min',law.advance)
        self.button('Suspend operation · retain evidence',law.suspend)
        if not a['repeatable']:
            file=d['files'][a['key']]
            label(self.body,f'Stage {file["step"]+1}/{len(law.CASES[a["key"]]["steps"])} · unsuccessful attempts {file["attempts"]}')
            for entry in file['evidence']:label(self.body,entry['title']+'\n'+entry['finding'])

    def cases(self,s,d):
        __import__('campaign_prose_ui').board(self.body,self.game,self.act)
        if d['active']:self.active(s,d);return
        self.desk(s)
        for key,spec in law.CASES.items():
            file=d['files'].get(key,{})
            ready=law.available(s,key);done=file.get('complete')
            label(self.body,spec['title']+(' · Complete' if done else ''),True)
            label(self.body,spec['brief'])
            if done:
                for entry in file.get('evidence',[])[-1:]:label(self.body,entry['finding'])
            elif ready:self.button('Resume case' if file else 'Assemble this case team',law.begin,key)
            else:label(self.body,'Requires: '+', '.join(law.CASES[k]['title'] for k in spec['requires']))



class InterpolView(tk.Frame, CaseBoard):
    def __init__(self,parent,game):
        super().__init__(parent,bg=ui.INK,padx=16,pady=12)
        self.game=game;self.page='Cases';self.notice='';self.selection=None
        ttk.Label(self,text='INTERPOL · AWAKENED OPERATIONS',font=('Segoe UI',20,'bold')).pack(anchor='w')
        label(self,'IN PERSON · Regional casework, enforcement and field operations')
        nav=ttk.Frame(self);nav.pack(fill='x',pady=4)
        for name in ('Cases','Operations','Law & fines','Organisation'):
            ttk.Button(nav,text=name,command=lambda n=name:self.change(n)).pack(side='left',padx=3)
        ttk.Button(nav,text='Return to location',command=self.leave).pack(side='right')
        self.canvas=tk.Canvas(self,bg=ui.INK,highlightthickness=0)
        scroll=ttk.Scrollbar(self,command=self.canvas.yview);scroll.pack(side='right',fill='y')
        self.canvas.pack(fill='both',expand=True);self.canvas.configure(yscrollcommand=scroll.set)
        self.body=ttk.Frame(self.canvas,padding=8);item=self.canvas.create_window(0,0,window=self.body,anchor='nw')
        self.body.bind('<Configure>',lambda e:self.canvas.configure(scrollregion=self.canvas.bbox('all')))
        self.canvas.bind('<Configure>',lambda e:self.canvas.itemconfigure(item,width=e.width))
        self.canvas.bind('<MouseWheel>',lambda e:self.canvas.yview_scroll(-int(e.delta/120),'units'))

    def change(self,name):self.page=name;self.draw();self.canvas.yview_moveto(0)

    def button(self,text,fn,*args,enabled=True):
        b=ttk.Button(self.body,text=text,command=lambda:self.act(fn,*args),state='normal' if enabled and not self.game.busy else 'disabled')
        b.pack(fill='x',pady=4);return b

    def act(self,fn,*args):
        if self.game.busy:return
        try:
            if __import__('campaign_dialogue').maybe_open(self.game,fn,args):return
            self.notice=fn(self.game.state_data,*args) or '';self.game.persist()
        except ValueError as exc:self.notice=str(exc)
        self.game.clock_label.configure(text=town.loop.clock(self.game.state_data)+f' · ${self.game.state_data["world"]["money"]:,}')
        self.draw()
        import combat
        if combat.active(self.game.state_data):
            import combat_ui
            combat_ui.open_combat(self.game)

    def draw(self):
        for w in self.body.winfo_children():w.destroy()
        s=self.game.state_data;d=law.ensure(s)
        label(self.body,town.loop.clock(s)+' · '+town.location_name(s,s['world']['location']),True)
        if self.notice:label(self.body,self.notice,True)
        if self.page=='Law & fines':self.enforcement(s,d)
        elif self.page=='Organisation':self.organisation(s,d)
        elif self.page=='Operations':self.operations(s,d)
        else:self.cases(s,d)
        phone_theme.apply_tree(self)

    def operations(self,s,d):
        if d['active']:self.active(s,d);return
        self.desk(s)
        label(self.body,'Repeatable field operations unlock after the Blackhaven case. One successful operation of each type per story day. Combat outcomes are real; failure retains the objective for a later attempt.')
        for key,spec in law.OPERATIONS.items():
            if spec.get('post_story'):
                label(self.body,spec['title']+'\n'+spec['brief'])
                if s['player'] not in ('fox','gordon') or not d['files'].get('crow_operation',{}).get('complete'):
                    label(self.body,'Requires completing Night Ledger as Fox or Gordon.');continue
                label(self.body,'Repeatable local disruption. No Crow rematch, new Ace reveal or permanent Syndicate defeat.')
            self.button(spec['title']+' · assemble at public desk',law.begin,key,True)
        for faction,until in d['disruption'].items():
            if until>s['world']['minute']:label(self.body,f'{faction.title()} commissions disrupted for {until-s["world"]["minute"]} more story minutes.')

    def enforcement(self,s,d):
        RecordPanel(self.body,self.game)
        label(self.body,'Witnessed or documented offences open a regional review. Gordon issues fines immediately when present. He normally declines to fine Fox for attacking a criminal target. Sparring and authorised operations do not create assault charges. Paying a fine does not repair a damaged relationship.')
        if s['world']['location'] in ('blackhaven','downtown','market','syndicate_office'):
            label(self.body,'Street actions · these commit actual offences. Theft yields $90 against a base $300 fine; intimidation carries a base $600 fine. Witnesses can report either, and local patrol observation follows district influence.',True)
            self.button('Steal unattended cash · commit theft',law.street_action,'theft')
            self.button('Intimidate a street witness · commit offence',law.street_action,'intimidation')
        for i in reversed(d['incidents'][-20:]):
            if i['actor']==s['player']:label(self.body,law.OFFENCES[i['kind']][0]+' · '+i['status']+'\n'+i.get('reason',i['evidence']))

    def organisation(self,s,d):
        label(self.body,'Interpol · global police authority under the unified UN government',True)
        label(self.body,'Geneva is global headquarters. Winterfield hosts a regional branch with a public desk, briefing room, controlled training hall and secure interview wing. Nine Awakened squads serve globally; Jeremy Gordon commands Team 9. Edward Fox is a licensed associate based in Blackhaven, not a subordinate gang recruit.')
        label(self.body,'Regional roles: public liaison Dana Lin; Team 9 commander Jeremy Gordon; licensed associate Edward Fox; registered civilian case assistants. Operational access is personal and does not confer criminal-faction membership.')
        for area in law.BASE_INFLUENCE:label(self.body,f'{area.title()} · influence {law.influence(s,area)}/100')
        for venue in law.SECURE_ROOMS:self.button('Visit '+town.LOCATIONS[venue],town.travel,venue,enabled=law.clearance(s,s['player']))
        label(self.body,'Established discoveries are private until explicitly shared in person.',True)
        discoveries=d['knowledge'].get(s['player'],{}).get('identities',[])
        import four_aces
        for ident in discoveries:
            title=four_aces.CAST[ident]['name']+' · Ace of '+four_aces.CAST[ident]['suit'] if ident in four_aces.IDS else 'Crow command location'
            label(self.body,title)
            for who in s['world']['cast']:
                if who!=s['player'] and law.here(s,who) and not law.known_identity(s,who,ident):
                    self.button('Brief '+who.title()+' on this finding',law.share_identity,who,ident)
        if not discoveries:label(self.body,'No identity discoveries in this protagonist’s case record.')

    def leave(self):
        self.place_forget();self.game.render()
