"""Ivan's campaign uses the existing dark in-person Story stage."""
from tkinter import ttk
import ivan_campaigns as route

def reread(parent,game):
    completed=[key for key in route.CHAPTER_IDS if key in route.read(game.state_data).get('completed',[])]
    if not completed:return
    panel=ttk.Frame(parent)
    def toggle():
        if panel.winfo_manager():panel.pack_forget()
        else:panel.pack(fill='x',pady=4,after=toggle_button)
    toggle_button=ttk.Button(parent,text='Revisit completed chapters',command=toggle)
    toggle_button.pack(fill='x',pady=4)
    ttk.Label(panel,text='Expanded story · read only · your saved choices',wraplength=650).pack(fill='x',pady=4)
    def open_chapter(key):
        pages=route.reread_pages(game.state_data,key)
        __import__('campaign_prose_ui').open_archive(game)
        reader=game.hangout_view.prose_reader
        reader.cancel_flip();reader.history_pages=pages;reader.history_cursor=0;reader.identity=None;reader.display()
    import ivan_campaign_content as content
    for key in completed:
        ttk.Button(panel,text=key+' · '+content.CHAPTERS[key]['title'],command=lambda key=key:open_chapter(key)).pack(fill='x',pady=2)


def board(parent,game,act):
    s=game.state_data;d=route.data(s)
    def label(text):
        w=ttk.Label(parent,text=text,wraplength=720,justify='left');w.pack(fill='x',pady=5)
        w.bind('<Configure>',lambda e:w.configure(wraplength=max(90,e.width-12)))
    def action(text,key,value=''):ttk.Button(parent,text=text,command=lambda:act(route.perform_action,key,value)).pack(fill='x',pady=4)
    label('IVAN · A LIFE ON LOAN')
    if d['complete']:
        label('Complete · Still here. Ivan remains in the Syndicate. His friends support an effort toward restraint; freedom and absolution have not been granted.')
        reread(parent,game);__import__('ivan_history_ui').selector(parent,game);return
    if route.availability(s):label(route.availability(s));reread(parent,game);return
    label(route.CHAPTER_IDS[d['chapter']]+' · '+route.chapter(s)['title'])
    label(f"Chapters {len(d['completed'])}/18 · Historical accounts {len(d['memories'])}/8")
    import interiors
    guests=route.required_cast(s)
    waiting=[who for who in guests if s['world']['cast'].get(who,{}).get('journey') or not interiors.same_room(s,'ivan',who)]
    unrelated=set(interiors.occupants(s,route.room_target(s)))-{'ivan',*guests}
    if guests and (waiting or unrelated):
        ttk.Button(parent,text='Request the chapter appointment',command=lambda:act(route.request_appointment)).pack(fill='x',pady=4)
    if waiting:
        ttk.Button(parent,text='Wait 10 minutes for actual arrivals',command=lambda:act(__import__('town').wait,10)).pack(fill='x',pady=4)
    if interiors.building(s['world']['location'])!=route.destination(s) or interiors.room(s)!=route.room_target(s):
        __import__('campaign_navigation').directions(parent,game,route.destination(s));label('Required room: '+interiors.ROOMS[route.room_target(s)].label)
    elif d['pending_return']:action('Continue the chapter','return_scene')
    elif d['phase']=='briefing':action('Continue the story','scene')
    elif d['phase']=='memory':action('Continue the recollection','recollection')
    elif d['phase']=='choice':
        for key,(title,_) in route.chapter(s)['choices'].items():action(title,'respond',key)
    elif d['phase']=='combat':
        label('Fixed story outcome · tactics and strain are recorded through actual exchanges. Concede before the first exchange to cancel without advancing.')
        action('Enter the next confrontation','combat')
    elif d['phase']=='spare':action('Deliberately spare all five friends','spare')
    elif d['phase']=='aftermath':action('Read the aftermath and continue','aftermath')
    __import__('ivan_history_ui').selector(parent,game)
    reread(parent,game)
