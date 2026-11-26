"""Takeo's campaign runs on the existing dark in-person Story surface."""
from tkinter import ttk
import takeo_campaigns as route

def board(parent,game,act):
    s=game.state_data;d=route.data(s)
    def label(text):
        w=ttk.Label(parent,text=text,wraplength=700,justify='left');w.pack(fill='x',pady=5);w.bind('<Configure>',lambda e:w.configure(wraplength=max(90,e.width-12)))
    def direct(text,fn,*args):ttk.Button(parent,text=text,command=lambda:act(fn,*args)).pack(fill='x',pady=4)
    def button(text,action,value=''):direct(text,route.perform_action,action,value)
    label('TAKEO MISHIMA · EMPIRE OF ONE')
    if 'TK-F01' in d['memories'] and not d.get('session'):
        ttk.Button(parent,text='Visit flashback area · Before the Orders Ended',command=lambda:__import__('flashback_visit_ui').open_in_person(game)).pack(fill='x',pady=4)
    if d['complete']:
        label('Complete. The bridgehead and Thirteen’s command survive. Takeo personally destroyed the local programme archive. Keisuke reports under supervision; Sylvanis remains independent.');return
    label(route.CHAPTER_IDS[d['chapter']]+' · '+route.chapter(s)['title']);label('Historical recollections: '+str(len(d['memories']))+'/8')
    if route.availability(s):label(route.availability(s));return
    item=route.session(s)
    if item:
        label('ISOLATED HISTORY · '+item['mission']+' · The present is paused.')
        def run(fn,*args):
            try:label(fn(s,*args));game.persist();game.campaign_view.draw()
            except ValueError as exc:label(str(exc))
        for text in item['events']:label(text)
        ttk.Button(parent,text='Continue the story',command=lambda:run(route.finish_legacy_memory,item['token'])).pack(fill='x',pady=4)
        ttk.Button(parent,text='Return safely · leave memory incomplete',command=lambda:run(route.abandon_session,item['token'])).pack(fill='x',pady=4);return
    if route.required_cast(s):direct('Arrange required in-person appointment',route.request_appointment)
    if d.get('local_appointment'):direct('Dismiss Keisuke from the completed appointment',route.finish_local)
    if 'sylvanis' in d.get('appointment',{}).get('guests',[]) and 'sylvanis' not in route.required_cast(s):
        label('An earlier supplier appointment is still recorded. End it before a private scene that does not include Sylvanis.')
        direct('End supplier appointment · return Sylvanis to Glasshouse',route.finish_supplier)
    import interiors, combat
    waiting=[]
    for who in ('takeo',*route.required_cast(s)):
        if s['world']['cast'].get(who,{}).get('journey'):waiting.append(who+' is travelling')
        if combat.recovering(s,who):waiting.append(who+' is recovering')
        event=d.get('appointment',{})
        if (who in event.get('guests',[]) and event.get('room')==route.room_target(s)
                and event.get('start',0)<=s['world']['minute']<event.get('end',0)
                and not s['world']['cast'].get(who,{}).get('journey')
                and not interiors.same_room(s,'takeo',who)):
            waiting.append(who+' is coming to the appointment room')
    appointment=d.get('local_appointment',{})
    if appointment.get('room')==route.room_target(s) and appointment.get('arrival',0)>s['world']['minute']:
        waiting.append('Keisuke arrives in '+str(appointment['arrival']-s['world']['minute'])+' minutes')
    if waiting:
        label('Waiting because: '+ '; '.join(waiting)+'.')
        direct('Wait ten minutes',__import__('town').wait,10)
    label('Next: '+('resume the saved scene' if d.get('scene_resume') else
                   'read the return to the present' if d['pending_return'] else
                   {'briefing':'read the chapter scene','memory':'complete the mandatory recollection',
                    'tasks':'complete the chapter objective','aftermath':'read the aftermath and continue'}.get(d['phase'],'continue the chapter'))+'.')
    if interiors.building(s['world']['location'])!=route.destination(s) or route.room_target(s) in interiors.ROOMS and interiors.room(s)!=route.room_target(s):
        if interiors.building(s['world']['location'])==route.destination(s):
            label('You are in the objective building. Return to location and enter '+interiors.ROOMS[route.room_target(s)].label+' to continue.');return
        __import__('campaign_navigation').directions(parent,game,route.room_target(s));return
    if d.get('scene_resume'):
        def resume():
            try:route.resume_scene(s);game.persist();__import__('campaign_dialogue').show(game)
            except ValueError as exc:label(str(exc))
        ttk.Button(parent,text='Resume saved scene in this room',command=resume).pack(fill='x');return
    if d['pending_return']:button('Read the return to the present','historical_return');return
    if d['phase']=='briefing':button('Read the chapter scene','briefing')
    elif d['phase']=='memory':button('Read recollection · '+route.pending_memory(s),'recollection')
    elif d['phase']=='aftermath':button('Read aftermath and continue','aftermath')
    elif d['phase']=='tasks':
        i=d['chapter']
        if i in (1,10):
            op=d['operations'].get({1:'breach',10:'supply'}[i],{})
            if op.get('secured'):button('Record the secured objective','confirm_objective')
            else:button('Enter actual resistance · retry checkpoint','objective')
        elif i==12:
            op=d['operations'].get('finale',{});wave=op.get('wave',0)
            label(f'Continuous Meridian checkpoints: {wave}/3. Resources carry between encounters. Failed objectives require recovery and retry.')
            if wave==2 and not op.get('preserved'):button('Commit the cleared route · preserve Thirteen’s command','preserve')
            elif wave<3:button('Enter next actual resistance encounter','objective')
            else:button('Personally destroy the unique programme archive','destroy')
        elif i==4:
            label('Transport capacity is finite. The choice changes the material cost of the later withdrawal.')
            button('Prioritise personnel · leave laboratory equipment','task','personnel');button('Prioritise heavy equipment · abandon two vehicle sections later','task','equipment')
        else:
            button('Continue the scene','task')
