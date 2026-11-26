"""Neo's route is embedded in the existing dark in-person Story stage."""
from tkinter import ttk
import neo_campaigns as route

def board(parent,game,act):
    s=game.state_data;d=route.data(s)
    def label(text):
        w=ttk.Label(parent,text=text,wraplength=730,justify='left');w.pack(fill='x',pady=6);w.bind('<Configure>',lambda e:w.configure(wraplength=max(90,e.width-12)))
    def button(text,action,value=''):ttk.Button(parent,text=text,command=lambda:act(route.perform_action,action,value)).pack(fill='x',pady=4)
    def direct(text,fn,*args):ttk.Button(parent,text=text,command=lambda:act(fn,*args)).pack(fill='x',pady=4)
    label('NEO ISHIDA · A LIFE OF HIS OWN')
    if route.unavailable(s):label(route.unavailable(s));return
    if not d['started']:label('A life built around home, friendship and ordinary work is threatened by the world Neo escaped. Fourteen chapters and six memories follow what he chooses to protect.');button('Start Neo’s campaign','start');return
    if d['complete']:label('Complete · ten captives safe. Hachimura and Thirteen alive in secure custody. Neo and Alyssa return to their own home.');visits(parent,game,label);return
    label(route.CHAPTER_IDS[d['chapter']]+' · '+route.chapter(s)['title'])
    item=route.session(s)
    if item:
        label('ISOLATED RECOLLECTION · '+item['mission']+' · '+item['era']+'. Live world and resources remain unchanged.')
        tasks=__import__('neo_campaign_content').MEMORY_TASKS[item['mission']]
        for event in item['events']:label(event['text'])
        if item['cursor']<len(tasks):
            task=tasks[item['cursor']];label(task['prompt'])
            for key,(text,_) in task['options'].items():direct(text,route.memory_step,item['token'],key)
        else:direct('Return with the completed recollection',route.return_session,item['token'])
        direct('Return safely · leave recollection incomplete',route.abandon_session,item['token']);return
    visits(parent,game,label)
    direct('Arrange required participants at this objective',route.request_appointment)
    direct('Wait ten minutes for arrival / recovery',__import__('town').wait,10)
    import interiors
    if interiors.building(s['world']['location'])!=route.destination(s) or interiors.room(s)!=route.room_target(s):
        __import__('campaign_navigation').directions(parent,game,route.destination(s));label('Objective room: '+interiors.ROOMS[route.room_target(s)].label);return
    if d.get('pending_return'):button('Read the return to the present','historical_return');return
    if d['phase']=='briefing':
        button('Read the chapter scene','briefing');return
    if d['phase']=='memory':button('Remember · '+__import__('neo_campaign_content').MEMORIES[route.pending_memory(s)]['title'],'memory');return
    i=d['chapter']
    if i in route.CHOICES:
        key,options=route.CHOICES[i]
        if key not in d['choices'] and (i not in (11,12) or d['operations'].get('hachimura' if i==11 else 'formation')):
            prompt,labels=__import__('neo_campaign_content').CHOICE_LABELS[key]
            label(prompt)
            for option in options:button(labels[option],'choice',option)
    if i in (4,9) and d['choices'].get('later_disclosure' if i==9 else 'disclosure') not in (None,'private'):
        label('Optional deeper disclosures require a private meeting with the named listener. Core safety information is already shared.')
        for who in route.TEAM:
            direct('Arrange private meeting · '+who,route.request_appointment,who)
            for topic in ('programme','parentage'):
                if topic=='parentage' and d['choices'].get('later_disclosure' if i==9 else 'disclosure')!='parentage':continue
                if topic not in d['disclosures'].get(who,[]):button('Disclose '+topic+' · '+who,'disclose',who+':'+topic)
    mission='records' if i==10 and d['operations'].get('entry') else route.FIGHTS.get(i)
    if mission and not d['operations'].get(mission):
        if d.get('last_attempt',{}).get('retry'):label('Checkpoint remains incomplete. Recover and retry; no additional deaths or success awarded.')
        label('Hold the exit for three exchanges.' if mission=='evacuation' else 'Earn three supported openings while holding the corridor.' if mission=='formation' else 'Win the encounter to clear the way. Defeat leaves this checkpoint available to retry.')
        button({'evacuation':'Hold the evacuation route','formation':'Face Thirteen together','hachimura':'Confront Hachimura'}.get(mission,'Continue into the encounter'),'objective')
    for step in route.STEPS.get(i,()):
        if step not in d['operations']:
            if d['operations'].get('transport' if i==7 else 'records'):
                button({'open':'Open the compartment','account':'Help Alyssa account for the passengers','handoff':'Bring the passengers to the receiving team','annex_handoff':'Escort the remaining captives to medical care'}[step],'step',step)
            break
    if route.tasks_done(s):button('Read aftermath and continue','aftermath')

def visits(parent,game,label):
    import neo_history as history
    for area,title in history.TITLES.items():
        reason=history.locked(game.state_data,area)
        if reason:label(title+' · Locked: '+reason)
        else:
            def open_area(key=area):
                history.choose(game.state_data,key);__import__('flashback_visit_ui').open_in_person(game)
            ttk.Button(parent,text='Visit flashback area · '+title,command=open_area).pack(fill='x',pady=3)
