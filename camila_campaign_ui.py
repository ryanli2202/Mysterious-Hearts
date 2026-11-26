"""Camila's Story board stays on the existing in-person stage."""
from tkinter import ttk
import camila_campaigns as route

def board(parent,game,act):
    s=game.state_data;d=route.data(s)
    def label(text):
        w=ttk.Label(parent,text=text,wraplength=740,justify='left');w.pack(fill='x',pady=6);w.bind('<Configure>',lambda event:w.configure(wraplength=max(90,event.width-12)))
    def button(text,action,value=''):ttk.Button(parent,text=text,command=lambda:act(route.perform_action,action,value)).pack(fill='x',pady=4)
    def direct(text,fn,*args):ttk.Button(parent,text=text,command=lambda:act(fn,*args)).pack(fill='x',pady=4)
    label('CAMILA · THE INHERITANCE')
    if d['complete']:
        label('Complete · '+d['ending'].replace('_',' ')+'. Remaining reserve: '+str(d['reserve'])+'. Camila remains Diamonds and intended successor. Crow remains Cardmaster.');return
    label(route.CHAPTER_IDS[d['chapter']]+' · '+route.chapter(s)['title']);label('Required memories: '+str(len(d['memories']))+'/8 · Meridian reserve: '+str(d['reserve'])+' fictional allocation units')
    if d.get('ending')=='account_remains_open':label('The account remains open. Recover and retry the actual obstruction. Committed costs remain spent.')
    item=route.session(s)
    if item:
        label('RECOLLECTION · '+item['mission']+' · age '+str(item['age']))
        def run(fn,*args):
            try:label(fn(s,*args));game.persist();game.campaign_view.draw()
            except ValueError as exc:label(str(exc))
        tasks=__import__('camila_campaign_content').MEMORY_TASKS[item['mission']]
        for event in item['events']:label(event['text'])
        if item.get('narrative'):
            label('The memory settles. Meridian is waiting.')
            ttk.Button(parent,text='Return to the present',command=lambda:run(route.return_session,item['token'])).pack(fill='x',pady=4)
        elif item['cursor']<len(tasks):
            task=tasks[item['cursor']];label(task['prompt'])
            for key,(text,_) in task['options'].items():ttk.Button(parent,text=text,command=lambda k=key:run(route.memory_step,item['token'],k)).pack(fill='x',pady=4)
        else:ttk.Button(parent,text='Return with the completed recollection',command=lambda:run(route.return_session,item['token'])).pack(fill='x',pady=4)
        ttk.Button(parent,text='Leave without completing the recollection',command=lambda:run(route.abandon_session,item['token'])).pack(fill='x',pady=4)
        return
    for who in route.LOCAL:
        direct('Arrange voluntary appointment · '+who.removeprefix('camila-').title(),route.request_local,who)
        if route.local_here(s,who):direct('Finish local appointment · '+who.removeprefix('camila-').title(),route.finish_local,who)
    direct('Request required professional appointment',route.request_appointment)
    if d['chapter']==9:
        for who in route.ROLES:direct('Request private appointment · '+who,route.request_appointment,who)
    if d['chapter']==12:direct('Request all three agreed specialists',route.request_appointment,'team')
    if d['phase']=='tasks' and d['chapter'] in (0,11):direct('Request the finite-mandate meeting · Crow',route.request_appointment,'crow')
    direct('Wait 10 minutes for actual arrivals',__import__('town').wait,10)
    import interiors
    if interiors.building(s['world']['location'])!=route.destination(s) or interiors.room(s)!=route.room_target(s):
        __import__('campaign_navigation').directions(parent,game,route.destination(s));label('Objective room: '+interiors.ROOMS[route.room_target(s)].label);return
    if d.get('scene_resume'):
        def resume():
            try:route.resume_scene(s);game.persist();__import__('campaign_dialogue').show(game)
            except ValueError as exc:label(str(exc))
        ttk.Button(parent,text='Resume the exact saved scene here',command=resume).pack(fill='x',pady=4);return
    if d.get('pending_return'):button('Read the historical return and present reflection','historical_return');return
    if d['phase']=='briefing':button('Read the chapter scene','briefing')
    elif d['phase']=='memory':button('Enter required memory · '+route.MEMORY_AT[d['chapter']],'memory')
    elif d['phase']=='aftermath':button('Read aftermath and continue','aftermath')
    elif d['phase']=='tasks':
        i=d['chapter']
        if i==8:
            label('Both plans preserve payroll and core operations. Neither restores the two lost shifts. Selecting a plan commits 10 bridge units once.')
            button('Release East concession · 20 final units · 40 retained','plan','release');button('Retain East concession · 45 final units · 15 retained','plan','retain')
        elif i==9:
            for who,role in route.ROLES.items():
                if who not in d['support']:button('Agree '+role+' · '+who,'support',who)
                if who not in d['disclosures']:
                    button('Privately share adoption/upbringing · '+who,'disclose',who+':family');button('Keep family account private · '+who,'disclose',who+':private')
            button('Confirm the three accepted roles','task','roles')
        elif i==12:
            op=d['operations'].get('CA-13',{})
            if not op.get('cover'):button('Separate public approach with Elias','cover')
            elif not op.get('attack_stopped'):button('Enter actual armed-obstruction encounter','objective')
            else:
                if not op.get('seal'):button('Recover, authenticate and seal originals with Mavis','seal')
                if not op.get('escort'):button('Escort dispatch team to Inez with Martos · 8 stamina, 2 minutes','escort')
                if op.get('seal') and op.get('escort'):button('Execute signed allocation once and expire mandate','allocate')
        else:
            task=route.TASKS[i]
            label({'mandate':'Record the bounded mandate with Crow present.','schedule':'Examine Inez’s actual original schedule.','correction':'Correct the hypothesis against the observed source.','testimony':'Record the named impact with Inez present.','pledge':'Examine Ansel’s signed original undertaking.','corroborate':'Compare both originals · 6 stamina, 3 minutes.','agreement':'Record Inez’s signed conditions and Ansel’s acknowledged refusal.','prepare':'Confirm the final finite mandate with Crow present.'}[task])
            if task in ('mandate','prepare'):direct('Request Crow at this authored private venue',route.request_appointment,'crow')
            button('Complete this observed objective','task',task)
