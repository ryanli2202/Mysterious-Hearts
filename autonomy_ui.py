"""Player time controls, needs and reviewable NPC invitations."""
import custom_protagonist
import tkinter as tk
from tkinter import ttk, messagebox
from phone_dialogs import AppWindow, messagebox, simpledialog
import autonomy
import world_loop


def open_window(game):
    win=AppWindow(game); win.title('Life & availability'); win.geometry('740x760')
    canvas=tk.Canvas(win,highlightthickness=0); bar=ttk.Scrollbar(win,orient='vertical',command=canvas.yview)
    canvas.configure(yscrollcommand=bar.set); bar.pack(side='right',fill='y'); canvas.pack(fill='both',expand=True)
    body=ttk.Frame(canvas,padding=16); item=canvas.create_window(0,0,window=body,anchor='nw')
    body.bind('<Configure>',lambda e:canvas.configure(scrollregion=canvas.bbox('all')))
    canvas.bind('<Configure>',lambda e:canvas.itemconfigure(item,width=e.width))
    def act(fn,*args):
        if game.busy: return
        game.simulation_clock.tick(game.state_data,game.in_game)
        try: fn(game.state_data,*args)
        except ValueError as exc: messagebox.showinfo('Life & availability',str(exc),parent=win); return
        game.simulation_clock.reset(game.state_data)
        game.persist(); game.render(); render()
    def time_action(action):
        act(autonomy.advance_player,action)
    def render():
        for child in body.winfo_children(): child.destroy()
        s=game.state_data; a=autonomy.ensure(s); player=a['people'][s['player']]
        ttk.Label(body,text=world_loop.clock(s),font=('Segoe UI',16,'bold')).pack(anchor='w')
        for key,label in (('energy','Energy'),('social','Social battery'),('happiness','Happiness')):
            ttk.Label(body,text=f'{label}: {player[key]:.0f}/100').pack(anchor='w',pady=(8,0))
            ttk.Progressbar(body,maximum=100,value=player[key]).pack(fill='x')
        ttk.Label(body,text='Use Time in the main toolbar: 2-hour, 40-minute or 15-minute days, or pause.\nSleep speeds below multiply that rate; pausing also pauses sleep.').pack(anchor='w',pady=8)
        row=ttk.Frame(body); row.pack(fill='x',pady=12)
        for action,label in (('nap','Nap'),('sleep','Sleep'),('wake','Wake up')):
            ttk.Button(row,text=label,command=lambda x=action:time_action(x)).pack(side='left',padx=3)
        sleeping=(player.get('sleep_until') or 0)>s['world']['minute']
        row=ttk.Frame(body); row.pack(fill='x',pady=6)
        for action,label in (('sleep_normal','Normal · 1×'),('sleep_fast','Fast · 4×'),('sleep_faster','Faster · 12×'),('sleep_skip','Skip to waking')):
            ttk.Button(row,text=label,state='normal' if sleeping else 'disabled',command=lambda x=action:time_action(x)).pack(side='left',padx=3)
        if sleeping:
            until=player['sleep_until']
            ttk.Label(body,text=f'Sleeping at {s["world"].get("sleep_speed",1)}× · Wake {world_loop.dates.story_date(until):%b %d} at {until%1440//60:02d}:{until%60:02d}').pack(anchor='w')
        ttk.Label(body,text='Invitations & visitors',font=('Segoe UI',13,'bold')).pack(anchor='w')
        offers=[o for o in a['offers'] if o['state']=='pending']
        if not offers: ttk.Label(body,text='No pending invitations. Characters make plans as game time passes.').pack(anchor='w')
        for o in offers:
            card=ttk.LabelFrame(body,text=o['who'].title()+' · '+o['kind'],padding=8); card.pack(fill='x',pady=5)
            import town
            description='A request for a separate sleeping place tonight.' if o['kind']=='overnight' else 'Meet at '+town.LOCATIONS[o['venue']]+'.'
            if o.get('guests'): description+=' With '+', '.join(w.title() for w in o['guests'])+'.'
            description+=f" Available until {o['expires']%1440//60:02d}:{o['expires']%60:02d}."
            ttk.Label(card,text=description,wraplength=630).pack(anchor='w')
            for choice,label in (('accept','Welcome / accept'),('decline','Not this time'),('later','Ask again later')):
                ttk.Button(card,text=label,command=lambda i=o['id'],c=choice:act(autonomy.respond,i,c)).pack(side='left',padx=3)
        ttk.Label(body,text='Known contacts · usual sleep schedules',font=('Segoe UI',13,'bold')).pack(anchor='w',pady=(12,4))
        import hidden_cast
        for who,p in a['people'].items():
            if who==s['player'] or not hidden_cast.contact(s,who): continue
            bedtime=f"{p['bedtime']//60:02d}:{p['bedtime']%60:02d}"
            wake=f"{p['wake']//60:02d}:{p['wake']%60:02d}"
            visible=autonomy.status(s,who) if world_loop.together(s,who) else 'Away · availability may vary'
            ttk.Label(body,text=f'{custom_protagonist.display_name(who)} · {visible} · sleep {bedtime}–{wake}').pack(anchor='w',pady=3)
        ttk.Label(body,text='Recent shared events',font=('Segoe UI',13,'bold')).pack(anchor='w',pady=(12,4))
        for e in [e for e in a['events'] if s['player'] in e['owners']][-8:]:
            ttk.Label(body,text=e['text'],wraplength=650).pack(anchor='w',pady=3)
    render()
    last=[None]
    def refresh_clock():
        if not win.winfo_exists(): return
        s=game.state_data
        stamp=(s['world']['minute'],autonomy.person(s,s['player']).get('sleep_until'),s['world'].get('sleep_speed',1))
        if stamp!=last[0]:
            last[0]=stamp
            render()
        win.after(500,refresh_clock)
    win.after(500,refresh_clock)
    return win
