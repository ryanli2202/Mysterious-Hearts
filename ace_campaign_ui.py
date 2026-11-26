"""Mavis's Story board and scoped use of the ordinary in-person combat stage."""
from tkinter import ttk
import ace_campaigns as route


def board(parent, game, act):
    import campaign_navigation
    s=game.state_data; d=route.data(s); spec=route.chapter(s)
    def label(text):
        w=ttk.Label(parent,text=text,wraplength=740,justify='left'); w.pack(fill='x',pady=6)
        w.bind('<Configure>',lambda e:w.configure(wraplength=max(90,e.width-12)))
    def button(text,action,value=''):
        ttk.Button(parent,text=text,command=lambda:act(route.perform_action,action,value)).pack(fill='x',pady=4)
    label('MAVIS · THE VACANT SEAT')
    if d['complete']:
        label('Complete · Mavis remains Ace of Spades. The Broker’s operation is ended and his removal is permanent. '+d.get('archive_outcome',''))
        __import__('campaign_prose_ui').board(parent,game,act)
        return
    label(route.CHAPTER_IDS[d['chapter']]+' · '+spec['title'])
    label('Completed memories: '+str(len(d['memories']))+'/6 · Exposure: '+str(d['exposure']))
    if route.required_cast(s):
        ttk.Button(parent,text='Request the chapter’s professional appointment',command=lambda:act(route.request_appointment)).pack(fill='x',pady=4)
    if route.required_cast(s) or d.get('appointment'):
        ttk.Button(parent,text='Wait 10 minutes for actual arrivals',command=lambda:act(__import__('town').wait,10)).pack(fill='x',pady=4)
    if route.session(s):
        item=route.session(s)
        label('Memory encounter · '+item['mission']+' · Health, supplies and time in the present are unchanged.')
        def approach(action):
            route.historical_approach(s,item['token'],action); game.persist(); game.campaign_view.draw()
            if item['checkpoint']=='confrontation':open_encounter(game)
        if item['checkpoint']=='reconnaissance':
            label('Age 20 · Infiltration checkpoint. Observe the landing and service passage before approaching the target.')
            ttk.Button(parent,text='Observe the historical patrol and light sweep',command=lambda:approach('observe')).pack(fill='x',pady=4)
        elif item['checkpoint']=='approach':
            label(item['observation'])
            ttk.Button(parent,text='Guarded stair · lose 15% historical health',command=lambda:approach('stair')).pack(fill='x',pady=4)
            ttk.Button(parent,text='Service passage · spend 20 historical mana',command=lambda:approach('service')).pack(fill='x',pady=4)
        elif item['checkpoint']=='authority_case':
            label('Venn’s route authority travels in a separate case. Secure that case before confronting him; defeating him alone will not recover it.')
            ttk.Button(parent,text='Secure the separate route-authority case',command=lambda:approach('secure_case')).pack(fill='x',pady=4)
        else:ttk.Button(parent,text='Resume encounter',command=lambda:open_encounter(game)).pack(fill='x',pady=4)
        if item.get('receipt'):
            if not item['receipt']['won']:
                ttk.Button(parent,text='Retry checkpoint',command=lambda:(route.retry_session(s),game.persist(),open_encounter(game))).pack(fill='x',pady=4)
            ttk.Button(parent,text='Return to present',command=lambda:(route.return_session(s,item['token']),game.persist(),game.campaign_view.draw())).pack(fill='x',pady=4)
        else:
            ttk.Button(parent,text='Leave encounter incomplete · return safely',command=lambda:(route.abandon_session(s,item['token']),game.persist(),game.campaign_view.draw())).pack(fill='x',pady=4)
        return
    import interiors
    if interiors.building(s['world']['location'])!=route.destination(s) or (interiors.enabled(s) and route.room_target(s) and interiors.room(s)!=route.room_target(s)):
        campaign_navigation.directions(parent,game,route.destination(s))
        target=route.room_target(s)
        if target:label('Objective room: '+interiors.ROOMS[target].label)
        return
    phase=d['phase']; op=d['operations'].get(route.CHAPTER_IDS[d['chapter']],{})
    if phase=='briefing': button('Continue · '+spec['title'],'briefing')
    elif phase=='operation':
        if not op.get('recon'): button('Observe patrols and identify the objective','recon')
        elif not op.get('approach'):
            label(op['observed'])
            button('Service return · quiet approach, lose secondary copy','approach','service')
            button('Direct entrance · retain access, increase exposure','approach','direct')
        elif d['chapter']==10:
            if not op.get('authenticated'):button('Authenticate the transfer chain','objective')
            elif not op.get('contained'):button('Contain the authenticated transfer with agreed support','contain')
            else:button('Confront the Broker in the inner room','confront')
        else: button('Secure the objective and extract','objective')
    elif phase=='memory':
        from ace_campaign_content import MEMORIES
        button('Remember · '+MEMORIES[route.MEMORY_AT[d['chapter']]]['title'],'memory')
    elif phase=='aftermath':
        if d['pending_return']:
            button('Read the resolved historical mission and return','historical_return')
            return
        if d['chapter']==8:
            for who in ('martos','elias','camila'):
                ttk.Button(parent,text='Request private debrief with '+who,command=lambda person=who:act(route.request_appointment,person)).pack(fill='x',pady=4)
                button('Tell '+who+' the contract history','disclose',who+':contract')
                button('Keep personal history private with '+who,'disclose',who+':private')
        if d['chapter']==9:
            for who,task in (('martos','extraction'),('elias','cover'),('camila','authentication')):
                ttk.Button(parent,text='Request role agreement with '+who,command=lambda person=who:act(route.request_appointment,person)).pack(fill='x',pady=4)
                button(('Agreed · ' if who in d['support'] else 'Agree · ')+who+' / '+task,'support',who)
            button('Priority · contain transfer, risk secondary material','priority','contain')
            button('Priority · retrieve secondary material, expose entry','priority','retrieve')
        button('Continue the story','aftermath')


class EncounterGame:
    """Forward UI services while exposing only the nested playable state.

    The actual game's state_data is never replaced. Loading a different save
    invalidates every old proxy and asynchronous UI result by object identity.
    """
    def __init__(self,game,item):
        self.owner=game; self.origin=game.state_data; self.item=item
        self.expired=__import__('game_core').fresh('mavis')
    @property
    def state_data(self):
        if self.owner.state_data is not self.origin or route.session(self.origin) is not self.item:
            return self.expired
        return self.item['state']
    @property
    def busy(self): return self.owner.busy
    @busy.setter
    def busy(self,value): self.owner.busy=value
    def persist(self):
        if self.owner.state_data is self.origin and route.session(self.origin) is self.item: self.owner.persist()
    def __getattr__(self,name): return getattr(self.owner,name)


def open_encounter(game):
    if game.busy:return
    import combat_ui
    if route.repair_historical_kit(game.state_data):game.persist()
    if __import__('historical_combat').repair(game.state_data):game.persist()
    item=route.session(game.state_data)
    if not item or game.busy:return
    if item['checkpoint']!='confrontation':
        __import__('campaign_ui').open_in_person(game,'Story');return
    game.hide_phone_for_location()
    old=getattr(game,'ace_encounter_view',None)
    if old is not None and old.winfo_exists(): old.destroy()
    proxy=EncounterGame(game,item)
    class EncounterView(combat_ui.CombatView):
        def refresh(self):
            if not game.busy and not self.working and game.state_data is proxy.origin and route.repair_historical_kit(game.state_data):game.persist()
            if not game.busy and not self.working and game.state_data is proxy.origin and __import__('historical_combat').repair(game.state_data):game.persist()
            super().refresh()
        def close_encounter(self):
            if game.state_data is not proxy.origin or route.session(game.state_data) is not item:
                self.place_forget(); return
            route.finish_session(game.state_data,item['token'])
            self.place_forget(); game.persist()
            __import__('campaign_ui').open_in_person(game,'Story')
        def leave(self): self.close_encounter()
    view=game.ace_encounter_view=EncounterView(game.presence_view.master,proxy)
    view.place(x=0,y=0,relwidth=1,relheight=1); view.lift(); view.refresh()
