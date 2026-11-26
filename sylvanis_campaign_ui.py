"""The personal campaign runs exclusively on the existing in-person stage."""
from tkinter import ttk
import sylvanis_campaigns as route

def board(parent,game,act):
    s=game.state_data;d=route.data(s)
    def label(text):
        w=ttk.Label(parent,text=text,wraplength=720,justify='left');w.pack(fill='x',pady=5);w.bind('<Configure>',lambda e:w.configure(wraplength=max(90,e.width-12)))
    def button(text,action,value=''):ttk.Button(parent,text=text,command=lambda:act(route.perform_action,action,value)).pack(fill='x',pady=4)
    def direct(text,fn,*args):ttk.Button(parent,text=text,command=lambda:act(fn,*args)).pack(fill='x',pady=4)
    label('SYLVANIS · THE CROW’S PATIENCE')
    if route.availability(s):label(route.availability(s));return
    if d['complete']:
        label('Complete · '+d['ending'].replace('_',' ')+'. Arena permanently closed. Remaining operating units: '+str(d['reserve'])+'. Charles’s separate evidence remains intact.');return
    label(route.CHAPTER_IDS[d['chapter']]+' · '+route.chapter(s)['title'])
    item=route.session(s)
    if item:
        label('Continue from the remembered scene.')
        def run(fn,*args):
            try:fn(s,*args);game.persist();game.campaign_view.draw()
            except ValueError as exc:label(str(exc))
        def continue_legacy(state):
            route.complete_read_history(s)
            route.finish_reading(s,'legacy_return')
            if s.get('campaign_dialogue'):__import__('campaign_dialogue').show(game)
        ttk.Button(parent,text='Continue the story',command=lambda:run(continue_legacy)).pack(fill='x',pady=4)
        ttk.Button(parent,text='Return safely · leave mandatory history incomplete',command=lambda:run(route.abandon_session,item['token'])).pack(fill='x',pady=4);return
    for who in route.required_cast(s):direct('Request authored appointment · '+who,route.request_appointment,who)
    direct('Wait 10 minutes for actual arrivals',__import__('town').wait,10)
    import interiors
    if interiors.building(s['world']['location'])!=route.destination(s) or (route.room_target(s) in interiors.ROOMS and interiors.room(s)!=route.room_target(s)):
        __import__('campaign_navigation').directions(parent,game,route.destination(s));label('Required room: '+(interiors.ROOMS[route.room_target(s)].label if route.room_target(s) in interiors.ROOMS else route.room_target(s)));return
    if d.get('scene_resume'):
        def resume():
            try:route.resume_scene(s);game.persist();__import__('campaign_dialogue').show(game)
            except ValueError as exc:label(str(exc))
        ttk.Button(parent,text='Resume the exact saved scene here',command=resume).pack(fill='x',pady=4);return
    if d.get('pending_return'):button('Read the return to the present','historical_return');return
    if d['phase']=='briefing':button('Continue the story','briefing')
    elif d['phase']=='memory':button('Continue into the memory','memory')
    elif d['phase']=='aftermath':button('Continue the story','aftermath')
    elif d['phase']=='tasks':
        task=route.TASKS[d['chapter']]
        if task=='provocation':
            for key,text in (('buyer','Provoke the buyer’s anger'),('supervisors','Humiliate the rehearsed supervisors'),('crow','Seek the Crow’s personal intervention')):button(text,'provocation',key)
        else:
            label(__import__('sylvanis_campaign_content').ACTION_TEXT[task]);button('Enter the exhibition' if task=='exhibition' else 'Confront the Crow' if task=='finale' else 'Continue the story','task',task)
