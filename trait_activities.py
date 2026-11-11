"""Authored in-person Trait applications; prose never creates capabilities."""
import copy
import combat
import combat_profiles
import job_apps
import careers

ACTIONS = {
    'work_precision': dict(name='Precision-assisted work check',tags={'precision','stability'},context='work',
                           minutes=10,energy=4,description='Check one ordinary workplace task. +1 craft; no shift, wage, project completion or promotion.'),
    'explore_observe': dict(name='Survey public surroundings',tags={'precision'},context='exploration',
                            minutes=5,energy=3,description='Inspect visible footing and public surroundings at the park, beach or downtown. Records one bounded observation; no secrets or quest completion.'),
}


def options(profile):
    tags={t for a in __import__('combat_moves').amps(profile) for t in a['tags']}
    return [key for key,a in ACTIONS.items() if a['tags']&tags]


def execute(state,key,request_id):
    if not isinstance(request_id,str) or not request_id or len(request_id)>100: raise ValueError('Invalid action request.')
    ledger=state.get('trait_activities',{})
    if request_id in ledger.get('receipts',{}): return ledger['receipts'][request_id]
    # Validate and run existing activity handlers on a copy; failures commit nothing.
    s=copy.deepcopy(state); combat.guard(s)
    if combat.active(s): raise ValueError('Finish combat first.')
    p=combat_profiles.profile(s,s['player'])
    if key not in ACTIONS or key not in options(p): raise ValueError('No accepted Trait aspect supports this authored application.')
    spec=ACTIONS[key]; now=s['world']['minute']; location=s['world']['location']
    if s.get('careers',{}).get('active') or s.get('job_apps',{}).get('pending'): raise ValueError('Finish the active work event first.')
    ledger=s.setdefault('trait_activities',dict(receipts={},days={}))
    if ledger['days'].get(key)==now//1440: raise ValueError('This application is available once per day.')
    if spec['context']=='work':
        jobs=job_apps.ensure(s); job=jobs['employment']
        if not job: raise ValueError('A current supported job is required.')
        job_apps.guard(s,job_apps.JOBS[job]['venue'],spec['minutes'])
        start,end=job_apps.JOBS[job]['hours']
        if not start<=now%1440/60<end: raise ValueError('Visit during workplace hours.')
    else:
        if location not in ('park','beach','downtown'): raise ValueError('Visit the public park, beach or downtown.')
        job_apps.guard(s,location,spec['minutes'])
    import town
    town.ensure(s)
    needs=__import__('autonomy').person(s,s['player'])
    if needs['energy']<spec['energy']: raise ValueError('Not enough daily energy; rest first.')
    if spec['context']=='work':
        job_apps.profile(s,job)['craft']+=1
        result='A careful Trait-assisted check improves one ordinary task: craft +1.'
    else:
        observations={'park':'You identify uneven footing on the public path.', 'beach':'You trace safe footing above the visible tide line.', 'downtown':'You identify an unobstructed public pedestrian route.'}
        result=observations[location]
    careers.spend_time(s,spec['minutes'],spec['energy']*2)
    ledger['days'][key]=now//1440; ledger['receipts'][request_id]=result
    # Bounded history; daily ledger also prevents replay after receipt eviction.
    while len(ledger['receipts'])>100: ledger['receipts'].pop(next(iter(ledger['receipts'])))
    witnesses=[who for who,actor in s['world'].get('cast',{}).items() if who!=s['player'] and actor.get('location')==location and not actor.get('journey')]
    for who in witnesses:
        s.setdefault('trait_application_witnesses',{}).setdefault(who,[]).append(dict(action=key,minute=now))
    town.log(s,result+' '+str(spec['minutes'])+' minutes; energy −'+str(spec['energy'])+'. Visible Trait use may be noticed; no private history or identity link is disclosed.')
    state.clear(); state.update(s)
    return result


def open_in_person(game):
    import tkinter as tk
    from tkinter import ttk
    import phone_theme,winterfield_ui as ui,uuid
    from creator_tools_ui import text
    window=tk.Toplevel(game); window.title('In person · Trait applications & disclosure'); window.geometry('820x650'); window.configure(bg=ui.INK)
    status=text(window,12)
    def show(message): status.insert('end',message+'\n\n'); status.see('end')
    def act(key):
        try:
            message=execute(game.state_data,key,uuid.uuid4().hex); game.persist(); game.render(); show(message)
        except ValueError as exc: show(str(exc))
    p=combat_profiles.profile(game.state_data,game.state_data['player'])
    for key in options(p):
        a=ACTIONS[key]; ttk.Button(window,text=a['name'],command=lambda k=key:act(k)).pack(fill='x',padx=12,pady=4)
        show(a['description']+f" Costs {a['minutes']} minutes and {a['energy']} daily energy; once daily. Visible use is recorded for present witnesses.")
    if not options(p): show('Your accepted Trait has no supported work/exploration application. New prose does not grant one.')
    if game.state_data.get('custom_protagonist'):
        ttk.Label(window,text='Explicit disclosure to a present acquaintance').pack(anchor='w',padx=12)
        recipients=[who for who in __import__('game_core').CONTACTS if combat.present(game.state_data,who)]
        who=tk.StringVar(value=recipients[0] if recipients else '')
        ttk.Combobox(window,textvariable=who,values=recipients,state='readonly').pack(fill='x',padx=12)
        def disclose(kind):
            if not combat.present(game.state_data,who.get()): show('Meet the recipient in person first.'); return
            __import__('character_identity').disclose(game.state_data,who.get(),kind); game.persist(); show('Disclosed '+kind+' to '+who.get()+'.')
        ttk.Button(window,text='Share private history',command=lambda:disclose('history')).pack(pady=4)
        ttk.Button(window,text='Link legal name and underworld alias',command=lambda:disclose('identity')).pack(pady=4)
    phone_theme.apply_tree(window)
    return window
