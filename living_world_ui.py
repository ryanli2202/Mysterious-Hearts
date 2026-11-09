"""Player-facing world stories and source-backed discovery controls."""
from tkinter import ttk
import living_world as living
import town

def show(phone,frame,s):
    d=living.ensure(s)
    ttk.Label(frame,text='Life in Winterfield',font=('Segoe UI',24,'bold')).pack(anchor='w')
    ttk.Label(frame,text='Small stories, familiar places, and things worth following up.').pack(anchor='w',pady=(4,12))
    body=phone.scroll_area(frame)
    def heading(text): ttk.Label(body,text=text,font=('Segoe UI',15,'bold')).pack(anchor='w',pady=(18,5))
    def text(value): ttk.Label(body,text=value,wraplength=460,justify='left').pack(anchor='w',pady=4)
    def button(label,fn,*args): ttk.Button(body,text=label,command=lambda:phone.act(fn,*args)).pack(anchor='w',pady=4)
    heading('Local bulletin')
    for item in living.news(s):
        text(item['title']+' — '+item['source']); text(item['text'])
    heading('Make this place yours')
    place=s['world']['location']
    if place in living.REGULARS:
        button(living.REGULARS[place][0]+'',living.visit)
    else: text('Visit the campus café, Mario’s Pizza, the Bijou, Petal & Stem, or the boathouse for a repeatable local activity.')
    for venue,days in d['visits'].items(): text(f'{town.LOCATIONS[venue]} · {len(days)} separate days visited')
    for item in d['keepsakes'][-4:]: text(item['text'])
    heading('Around your friends')
    for who in living.PROJECTS:
        if who==s['player'] or not town.hidden.contact(s,who): continue
        p=living.project(s,who)
        text(who.title()+' · '+p['title'])
        # The phone is not an omniscient tracker of private offscreen progress.
        if town.present(s,who):
            text(p['text'])
            if not p['helped'] and p['stage']<3: button(p['action']+'',living.participate,who)
        else: text('Ask how it is going when you next talk. Meet in person to help.')
        if p['helped']: text(p['result'])
    heading('Shared rituals')
    rituals=[(key,days) for key,days in d['rituals'].items() if len(days)>=3]
    if not rituals: text('Return with the same companion on three different days to build a shared ritual.')
    for key,days in rituals:
        who,venue=key.split(':'); text(f'{who.title()} · {town.LOCATIONS[venue]} · {len(days)} shared visits')
    heading('Follow through')
    import memory_store
    records=memory_store.sync(s)['records'].values()
    commitments=memory_store.open_commitments(s,[s['player']])[-5:]
    if not commitments: text('Promises and proposed plans from conversations will appear here. A proposal is not an agreement.')
    for r in commitments:
        text(r['text']); text(r['status'])
        others=[who for who in r['owners'] if who!=s['player'] and who in s['routes'] and town.hidden.contact(s,who)]
        if len(others)==1:
            ttk.Button(body,text='Continue with '+others[0].title(),command=lambda who=others[0]:phone.open_thread(who)).pack(anchor='w',pady=4)
    heading('Tell someone what happened')
    for report in d['reports']:
        text(report['text'])
        for who in s['relationships']:
            if who not in report['known'] and town.hidden.contact(s,who):
                button('Tell '+who.title()+' · private message',disclose,report['id'],who)
    if not d['reports']: text('A witnessed betrayal or an explicit disclosure gives each person their own source. Private events do not automatically become town gossip.')
    if s['player']=='garrett':
        import charles_quest
        title,venue,question=charles_quest.objective(s)
        heading('Find Charles')
        text('Next: '+title+' · '+town.LOCATIONS[venue])
        text('Investigation actions take place in person. Existing document leads carry forward.')
        ttk.Button(body,text='Open in-person investigation',command=phone.game.charles_search).pack(anchor='w')


def disclose(s,report_id,who):
    import consequences
    consequences.disclose(s,report_id,who)
