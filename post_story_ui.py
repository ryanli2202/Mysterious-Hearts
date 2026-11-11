"""Reusable in-person protection board and remote Hamayashi administration."""
from tkinter import ttk
import post_story as story
import town


def board(parent,game,act):
    s=game.state_data
    def label(text):
        w=ttk.Label(parent,text=text,wraplength=700,justify='left');w.pack(fill='x',pady=5)
        w.bind('<Configure>',lambda e:w.configure(wraplength=max(100,e.width-12)))
    def button(text,fn,*args):
        ttk.Button(parent,text=text,command=lambda:act(fn,*args)).pack(fill='x',pady=4)
    label('POST-STORY · CIVILIAN PROTECTION')
    if not story.complete(s):
        label('Finish the personal story to unlock repeatable protection missions.');return
    d=story.read(s);a=d.get('active')
    if story.leader(s):label('Manage the successor in Bubblegram → Network → Hamayashi administration. Protection missions replenish its separate budget.')
    label('One successful mission of each type per story day. Verify consent, defeat the detail, then secure departure. Losing retains evidence and victories. No protection fees or civilian loot.')
    import combat
    if combat.recovering(s):button('Rest through knockout recovery',town.wait,combat.recovering(s))
    if a:
        spec=story.MISSIONS[a['key']];label(spec['title']+'\n'+spec['brief'])
        label('Objective: '+town.location_name(s,spec['venue']))
        if s['world']['location']!=spec['venue']:button('Travel to protection objective',town.travel,spec['venue'])
        elif not a['verified']:button('Verify the request and consent',story.verify)
        elif story.remaining(s):
            label(str(len(story.remaining(s)))+' opponents remain in this mission.')
            button('Fight next mission opponent',story.fight)
        else:button('Secure departure and record outcome',story.finish)
        button('Withdraw mission · no completion reward',story.withdraw)
    else:
        venue=story.base(s)
        label('Mission briefing: '+town.location_name(s,venue))
        if s['world']['location']!=venue:button('Travel to mission briefing',town.travel,venue)
        for key,spec in story.available(s).items():
            label(spec['title']+'\n'+spec['brief'])
            if d.get('completed',{}).get(key)==s['world']['minute']//1440:label('Completed today · available next story day')
            else:button('Accept · '+spec['title'],story.begin,key)
    label('Protection requests resolved: '+str(d.get('protected',0)))
    for row in d.get('history',[])[-6:]:label(row['text'])


def management(board,s):
    board.label('Hamayashi-kai · post-story administration',True)
    if not story.leader(s):
        board.label('Requires Rei’s completed leadership ending and current Hamayashi-kai leadership. Other endings receive their own in-person follow-up missions.');return
    m=story.data(s)['management']
    board.label(f'Organisation budget ${m["budget"]} · reserved shelter placements {m["shelter"]}')
    board.label('One remote directive per story day. Organisation funds are separate from your money. Each completed protection mission restores $100. Field interventions take place in person.')
    for key,(title,cost) in story.DIRECTIVES.items():
        board.button(title+f' · ${cost}',story.manage,key,enabled=m['budget']>=cost and m['last_day']!=s['world']['minute']//1440)
    for row in story.read(s).get('history',[])[-6:]:board.label(row['text'])
    ttk.Button(board.body,text='Open protection missions in person',command=lambda:__import__('campaign_ui').open_in_person(board.game,'After the story')).pack(fill='x',pady=5)
