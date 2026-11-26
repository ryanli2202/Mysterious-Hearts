"""Elias's in-person campaign and token-owned historical stage."""
from tkinter import ttk
import elias_campaigns as route

def board(parent,game,act):
    s=game.state_data;d=route.data(s)
    def label(text):
        w=ttk.Label(parent,text=text,wraplength=740,justify='left');w.pack(fill='x',pady=6);w.bind('<Configure>',lambda event:w.configure(wraplength=max(90,event.width-12)))
    def button(text,action,value=''):ttk.Button(parent,text=text,command=lambda:act(route.perform_action,action,value)).pack(fill='x',pady=4)
    def direct(text,fn,*args):ttk.Button(parent,text=text,command=lambda:act(fn,*args)).pack(fill='x',pady=4)
    label('ELIAS · THE LAST APPLAUSE')
    if d['complete']:
        label('Complete · '+d['ending'].replace('_',' ')+'. The affiliate is retained under Johanna. Acting, Hearts service and the need for the Crow’s acknowledgement continue.');return
    label(route.CHAPTER_IDS[d['chapter']]+' · '+route.chapter(s)['title']);label('Mandatory memories: '+str(len(d['memories']))+'/8')
    if d.get('ending')=='unfinished_business':label('Unfinished business. Actual costs and injuries remain. Recover, renew required appointments and retry the missing objective.')
    item=route.session(s)
    if item:
        label('ISOLATED HISTORY · '+item['mission']+' · Present time, health, equipment, money and social knowledge are unchanged.')
        def run(fn,*args):
            try:fn(s,*args);game.persist();game.campaign_view.draw()
            except ValueError as exc:label(str(exc))
        if item['mission']=='EL-F05':
            label('AUTHORED HISTORICAL ENCOUNTER · FIRST DEFEAT FIXED. Healthy Elias commits three methods; the Crow personally defeats him. No ordinary boss health bar.')
            label('Committed exchanges: '+str(item['duel_cursor'])+'/3')
            for event in item['duel_events']:label(event['witnessed_counter'])
            if item['duel_cursor']<3:
                for method,text in (('rhythm','Commit changed rhythm and earned heat'),('leverage','Commit trained throw and control'),('distance','Commit changed distance and combination')):ttk.Button(parent,text=text,command=lambda m=method:run(route.duel_step,item['token'],m)).pack(fill='x',pady=4)
            else:ttk.Button(parent,text='Return to the present · first defeat witnessed',command=lambda:run(route.return_session,item['token'])).pack(fill='x',pady=4)
        else:
            label('Formation '+str(item['formation_index']+1)+'/2 · '+route.FORMATIONS[item['mission']][item['formation_index']])
            if item['checkpoint']=='reconnaissance':ttk.Button(parent,text='Observe the formation and its approach',command=lambda:run(route.historical_approach,item['token'],'observe')).pack(fill='x',pady=4)
            elif item['checkpoint']=='approach':
                for approach,text in (('angle','Take an angle · 8 historical stamina'),('pressure','Meet the approach · 3 historical stamina')):ttk.Button(parent,text=text,command=lambda a=approach:(run(route.historical_approach,item['token'],a),open_encounter(game))).pack(fill='x',pady=4)
            elif item.get('receipt'):
                if not item['receipt']['won']:ttk.Button(parent,text='Retry this historical formation',command=lambda:run(route.retry_session)).pack(fill='x',pady=4)
                elif item['formation_index']==0:ttk.Button(parent,text='Continue to the second formation',command=lambda:run(route.next_formation,item['token'])).pack(fill='x',pady=4)
                else:ttk.Button(parent,text='Return with both genuine formation victories',command=lambda:run(route.return_session,item['token'])).pack(fill='x',pady=4)
            else:ttk.Button(parent,text='Resume the actual historical encounter',command=lambda:open_encounter(game)).pack(fill='x',pady=4)
        ttk.Button(parent,text='Return safely · leave mandatory memory incomplete',command=lambda:run(route.abandon_session,item['token'])).pack(fill='x',pady=4)
        return
    for who in route.required_cast(s):
        if who in route.LOCAL:direct('Arrange voluntary appointment · '+who.removeprefix('elias-').title(),route.request_local,who)
    if any(who not in route.LOCAL for who in route.required_cast(s)):direct('Request required professional appointment',route.request_appointment)
    direct('Wait 10 minutes for actual arrivals',__import__('town').wait,10)
    import interiors
    if interiors.building(s['world']['location'])!=route.destination(s) or interiors.room(s)!=route.room_target(s):
        __import__('campaign_navigation').directions(parent,game,route.destination(s));label('Objective room: '+interiors.ROOMS[route.room_target(s)].label);return
    if d.get('scene_resume'):
        def resume():
            try:route.resume_scene(s);game.persist();__import__('campaign_dialogue').show(game)
            except ValueError as exc:label(str(exc))
        ttk.Button(parent,text='Resume exact saved scene here',command=resume).pack(fill='x',pady=4);return
    phase=d['phase'];i=d['chapter'];op=d['operations'].get(route.CHAPTER_IDS[i],{})
    if d.get('pending_return'):button('Read the historical return and present reflection','historical_return');return
    if phase=='briefing':button('Read the chapter scene','briefing')
    elif phase=='memory':button('Enter mandatory memory · '+route.MEMORY_AT[i],'memory')
    elif phase in ('tasks','handover'):
        if i==0:button('Accept the assignment · continue saved scene','task','assignment')
        elif i==1:
            direct('Arrange Lotte’s rehearsal appointment',route.request_local,'elias-lotte');button('Complete the scheduled rehearsal','task','rehearsal')
        elif i in (3,4,6,7):
            if i!=4:direct('Arrange Johanna’s private review',route.request_local,'elias-johanna')
            value={3:'commitment',4:'dispatch',6:'obligation',7:'corroborate'}[i]
            button({'commitment':'Read what Konrad promised in your name','dispatch':'Follow the dispatch trail · 6 stamina, 3 minutes','obligation':'Hear what survival has cost Johanna','corroborate':'Let Johanna finish the account'}[value],'task',value)
        elif i==8:
            direct('Arrange Lotte’s professional scheduling conversation',route.request_local,'elias-lotte')
            button('Keep the agreed rehearsal commitment','rehearsal_choice','keep');button('Agree a revised rehearsal time with Lotte · 5 minutes','rehearsal_choice','renegotiate');button('Miss this rehearsal for unrequested extra preparation · 10 stamina, 20 minutes','rehearsal_choice','extra')
        elif i==9:
            for who,role in route.ROLES.items():
                direct('Request '+who+' privately',route.request_appointment,who);button('Agree '+role+' with '+who,'support',who);button('Share selected private account with '+who,'disclose',who+':account');button('Keep personal account private with '+who,'disclose',who+':private')
            if set(d['support'])==set(route.ROLES):button('Continue the agreed work · saved preparation','task','roles')
        elif i==10:
            label('Both methods can fulfil the objective. The conspicuous private demonstration uses a reserve allocation and delays the production reset; the cost remains in the report.')
            button('Coordinate a quiet containment plan','method','quiet');button('Commit viable conspicuous demonstration · 18 stamina, 15 minutes','method','bold')
        elif i==11:
            direct('Meet Johanna for the receiving instruction',route.request_local,'elias-johanna');button('Accept Johanna’s signed receiving instruction','task','prepare')
        elif i==12:
            direct('Request all three agreed role arrivals',route.request_appointment,'team');direct('Arrange Johanna’s signing and receiving appointment',route.request_local,'elias-johanna')
            if not op.get('civilians_separated'):button('Separate public audience and service routes with Mavis','separate')
            elif not op.get('attack_stopped'):button('Enter actual armed containment encounter','objective')
            else:
                label('The armed resistance is defeated. Records, weapons, authority and custody remain separate.')
                if not op.get('records_sealed'):button('Authenticate and seal the original ledger with Camila','seal')
                if not op.get('disarmed'):button('Disarm the defeated resistance · 5 stamina, 1 minute','disarm')
                if op.get('disarmed') and op.get('records_sealed') and not op.get('revoked'):button('Johanna signs revocation of Konrad’s authority','revoke')
                if op.get('revoked') and not op.get('receiver_eta'):button('Secure receiving perimeter with Martos · 8 stamina, 2 minutes','perimeter')
                if op.get('receiver_eta'):
                    label('Authorised affiliate receiver due at minute '+str(op['receiver_eta'])+'. Until arrival, Konrad remains held at the secured site.');direct('Wait 5 minutes for receiver',__import__('town').wait,5);button('Transfer disarmed Konrad to the arrived authorised receiver','custody')
    elif phase=='aftermath':
        button('Continue the story','aftermath')
        if i==9:
            label('The three roles are agreed. Personal conversations are optional; each needs a private appointment.')
            for who in route.ROLES:
                direct('Meet '+who+' privately',route.request_appointment,who)
                button('Tell '+who+' why the judgement matters','disclose',who+':account')
                button('Keep the personal account private with '+who,'disclose',who+':private')

class EncounterGame:
    def __init__(self,game,item):self.owner=game;self.origin=game.state_data;self.item=item;self.expired=__import__('game_core').fresh('elias')
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
    game.hide_phone_for_location();old=getattr(game,'elias_encounter_view',None)
    if old is not None and old.winfo_exists():old.destroy()
    proxy=EncounterGame(game,item)
    class EncounterView(combat_ui.CombatView):
        def close_encounter(self):
            if game.state_data is not proxy.origin or route.session(game.state_data) is not item:self.place_forget();return
            route.finish_session(game.state_data,item['token']);self.place_forget();game.persist();__import__('campaign_ui').open_in_person(game,'Story')
        def leave(self):self.close_encounter()
    view=game.elias_encounter_view=EncounterView(game.presence_view.master,proxy);view.place(x=0,y=0,relwidth=1,relheight=1);view.lift();view.refresh()
