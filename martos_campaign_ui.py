"""In-person Martos board and isolated historical combat stage."""
from tkinter import ttk
import martos_campaigns as route

def optional_conversations(parent, game, act):
    """Personal disclosures stay available without interrupting the story path."""
    details = ttk.Frame(parent)
    def toggle():
        if details.winfo_manager():
            details.pack_forget()
            reveal.configure(text='Optional personal conversations')
        else:
            details.pack(fill='x', after=reveal, pady=4)
            reveal.configure(text='Hide optional conversations')
    reveal = ttk.Button(parent, text='Optional personal conversations', command=toggle)
    reveal.pack(fill='x', pady=4)
    for who in ('mavis', 'camila', 'elias', 'sera'):
        name = who.title()
        if who == 'sera':
            ttk.Button(details, text='Arrange Sera’s voluntary private visit',
                       command=lambda: act(route.request_sera)).pack(fill='x', pady=3)
        else:
            ttk.Button(details, text='Request a private conversation with ' + name,
                       command=lambda person=who: act(route.request_appointment, person)).pack(fill='x', pady=3)
        ttk.Button(details, text='Tell ' + name + ' the personal account',
                   command=lambda person=who: act(route.perform_action, 'disclose', person + ':account')).pack(fill='x', pady=3)
        ttk.Button(details, text='Keep personal details private with ' + name,
                   command=lambda person=who: act(route.perform_action, 'disclose', person + ':private')).pack(fill='x', pady=3)
    return reveal, details


def board(parent,game,act):
    s=game.state_data;d=route.data(s);spec=route.chapter(s)
    def label(text):
        w=ttk.Label(parent,text=text,wraplength=740,justify='left');w.pack(fill='x',pady=6);w.bind('<Configure>',lambda e:w.configure(wraplength=max(90,e.width-12)))
    def button(text,action,value=''):ttk.Button(parent,text=text,command=lambda:act(route.perform_action,action,value)).pack(fill='x',pady=4)
    label('MARTOS · WHAT HE HOLDS')
    if d['complete']:
        label('Complete · '+{'promise_kept':'The promise kept','delivered_at_cost':'Delivered at a cost'}.get(d['ending'],d['ending'])+'. Lena and her unaltered records reached the agreed recipient. Martos remains Clubs and loyal to the Crow.')
        __import__('campaign_prose_ui').board(parent,game,act);return
    label(route.CHAPTER_IDS[d['chapter']]+' · '+spec['title']);label('Mandatory memories: '+str(len(d['memories']))+'/8')
    if d.get('ending')=='withdrawal_recovery':label('Withdrawal and recovery · The protection objective remains incomplete. Recover before retrying; committed costs remain.')
    if route.session(s):
        item=route.session(s);label('Isolated historical checkpoint · '+item['mission']+' · Present health, money, time, equipment and relationships remain unchanged.')
        def approach(action):
            route.historical_approach(s,item['token'],action);game.persist();game.campaign_view.draw()
            if item['checkpoint']=='confrontation':open_encounter(game)
        if item['checkpoint']=='reconnaissance':ttk.Button(parent,text='Observe the historical extraction route',command=lambda:approach('observe')).pack(fill='x',pady=4)
        elif item['checkpoint']=='approach':
            ttk.Button(parent,text='Covered route · spend 15 historical stamina',command=lambda:approach('covered')).pack(fill='x',pady=4)
            ttk.Button(parent,text='Direct route · lose 10% historical health',command=lambda:approach('direct')).pack(fill='x',pady=4)
        else:ttk.Button(parent,text='Resume historical encounter',command=lambda:open_encounter(game)).pack(fill='x',pady=4)
        if item.get('receipt'):
            if not item['receipt']['won'] or item['receipt']['ledger']['extraction_progress']<3:ttk.Button(parent,text='Retry historical checkpoint',command=lambda:(route.retry_session(s),game.persist(),game.campaign_view.draw())).pack(fill='x',pady=4)
            ttk.Button(parent,text='Return to the present',command=lambda:(route.return_session(s,item['token']),game.persist(),game.campaign_view.draw())).pack(fill='x',pady=4)
        else:ttk.Button(parent,text='Return safely · leave memory incomplete',command=lambda:(route.abandon_session(s,item['token']),game.persist(),game.campaign_view.draw())).pack(fill='x',pady=4)
        return
    if d['chapter'] in (5,7,13):
        ttk.Button(parent,text='Arrange Sera’s voluntary private visit',command=lambda:act(route.request_sera)).pack(fill='x',pady=4)
    if route.required_cast(s):ttk.Button(parent,text='Request the chapter’s professional appointment',command=lambda:act(route.request_appointment)).pack(fill='x',pady=4)
    if route.required_cast(s) or d.get('appointment') or d.get('sera_visit'):ttk.Button(parent,text='Wait 10 minutes for arrivals',command=lambda:act(__import__('town').wait,10)).pack(fill='x',pady=4)
    import interiors
    if interiors.building(s['world']['location'])!=route.destination(s) or (interiors.enabled(s) and interiors.room(s)!=route.room_target(s)):
        __import__('campaign_navigation').directions(parent,game,route.destination(s));label('Objective room: '+interiors.ROOMS[route.room_target(s)].label);return
    if d.get('scene_resume'):
        label('A saved scene awaits here. Travel and any required participant arrivals are real; its exact reading position is preserved.')
        pending=d['scene_resume']
        if pending['beats'][pending['cursor']].get('martos_closing_variants'):
            label('You may arrange a quiet lounge visit with Mavis, or continue the repair alone. Availability is checked at the actual meeting.')
            ttk.Button(parent,text='Request Mavis for the lounge watch repair',command=lambda:act(route.request_appointment,'mavis')).pack(fill='x',pady=4)
            ttk.Button(parent,text='Continue the watch repair alone',command=lambda:(route.dismiss_closing_colleague(s),route.resume_scene(s),game.persist(),__import__('campaign_dialogue').show(game))).pack(fill='x',pady=4)
            ttk.Button(parent,text='Wait 10 minutes for the lounge arrival',command=lambda:act(__import__('town').wait,10)).pack(fill='x',pady=4)
        ttk.Button(parent,text='Resume the saved scene',command=lambda:(route.resume_scene(s),game.persist(),__import__('campaign_dialogue').show(game))).pack(fill='x',pady=4)
        return
    phase=d['phase'];op=d['operations'].get(route.CHAPTER_IDS[d['chapter']],{})
    if phase=='briefing':button('Continue · '+spec['title'],'briefing')
    elif phase=='agreement':
        label('Lena controls her records and personal disclosures. An independent witness archive liaison receives her original account. Rejecting terms leaves her here safely until a revised arrangement is accepted.')
        button('Lena rejects the proposed terms · remain here','reject');button('Agree independent recipient, covered route and fallback','agree','revised' if d.get('rejected_terms') else 'archive')
    elif phase=='memory':button('Remember · '+__import__('martos_campaign_content').MEMORIES[route.MEMORY_AT[d['chapter']]]['title'],'memory')
    elif phase=='operation':
        if d['chapter']==12:
            ttk.Button(parent,text='Request all three final role arrivals',command=lambda:act(route.request_appointment,'team')).pack(fill='x',pady=4)
        if not op.get('recon'):button('Observe the present pursuit and departure route','recon')
        elif not op.get('approach'):
            label(op['observed']);button('Commit covered route','approach','covered');button('Commit direct route','approach','direct')
        else:button('Protect the departure leg · enter actual encounter','objective')
    elif phase=='escort_hold':
        label('The attacker is stopped; the protected departure leg remains incomplete.')
        button('Secure remaining departure leg · spend one game minute and 5 stamina','secure_departure')
    elif phase=='handover':
        ttk.Button(parent,text='Request agreed authentication and cover arrivals here',command=lambda:act(route.request_appointment,'team')).pack(fill='x',pady=4)
        label('Attack stopped. Protected departure: '+str(op.get('extraction_progress',0))+'/3. Delivery and custody are separate actions.')
        if op.get('extraction_progress',0)<3:button('Secure remaining departure leg · spend one game minute and 5 stamina','secure_departure')
        elif not op.get('delivered'):button('Deliver Lena and the original records to her agreed recipient','deliver')
        else:
            if not op.get('disarmed'):button('Disarm the defeated commander · 5 stamina, 1 game minute','disarm')
            elif not op.get('receiver_eta'):button('Secure custody perimeter with agreed cover · 15 stamina, 1 game minute','perimeter')
            else:
                arrival=op['receiver_eta']
                label(f'Authorised receiving team arrival: {arrival%1440//60:02d}:{arrival%60:02d}')
                ttk.Button(parent,text='Wait 5 minutes for custody receiver',command=lambda:act(__import__('town').wait,5)).pack(fill='x',pady=4)
                button('Transfer the secured commander to the arrived receiving team','custody')
            button('Prioritise protected delivery over secondary custody perimeter','prioritise_delivery')
    elif phase=='aftermath':
        if d['pending_return']:button('Read the historical return and present reflection','historical_return');return
        if d['chapter'] in (2,9,11):
            for who,role in route.ROLES.items():
                if who in d['support']:continue
                ttk.Button(parent,text='Request private role agreement with '+who,command=lambda person=who:act(route.request_appointment,person)).pack(fill='x',pady=4)
                button('Agree · '+who+' / '+role,'support',who)
        if d['chapter'] in (4,11):button('Commit to communicate strain before handing over','control','communicate')
        if d['chapter']==11:button('Confirm authentication, recipient, fallback and custody conditions','prepare')
        if d['chapter'] in (5,9,13):
            optional_conversations(parent,game,act)
        button('Continue the story','aftermath')

class EncounterGame:
    def __init__(self,game,item):self.owner=game;self.origin=game.state_data;self.item=item;self.expired=__import__('game_core').fresh('martos')
    @property
    def state_data(self):return self.item['state'] if self.owner.state_data is self.origin and route.session(self.origin) is self.item else self.expired
    @property
    def busy(self):return self.owner.busy
    @busy.setter
    def busy(self,value):self.owner.busy=value
    def persist(self):
        if self.owner.state_data is self.origin and route.session(self.origin) is self.item:self.owner.persist()
    def __getattr__(self,name):return getattr(self.owner,name)

def open_encounter(game):
    import combat_ui
    item=route.session(game.state_data)
    if not item or game.busy:return
    if __import__('historical_combat').repair(game.state_data):game.persist()
    if item['checkpoint']!='confrontation':__import__('campaign_ui').open_in_person(game,'Story');return
    game.hide_phone_for_location();old=getattr(game,'martos_encounter_view',None)
    if old is not None and old.winfo_exists():old.destroy()
    proxy=EncounterGame(game,item)
    class EncounterView(combat_ui.CombatView):
        def close_encounter(self):
            if game.state_data is not proxy.origin or route.session(game.state_data) is not item:self.place_forget();return
            route.finish_session(game.state_data,item['token']);self.place_forget();game.persist();__import__('campaign_ui').open_in_person(game,'Story')
        def leave(self):self.close_encounter()
    view=game.martos_encounter_view=EncounterView(game.presence_view.master,proxy);view.place(x=0,y=0,relwidth=1,relheight=1);view.lift();view.refresh()
