"""The existing in-person visit stage owns history; locked data stays explicit."""
from tkinter import ttk
import ivan_history as history

def selector(parent,game):
    s=game.state_data
    ttk.Label(parent,text='HISTORICAL AREAS · three collections / eight periods',wraplength=700).pack(fill='x',pady=(16,5))
    for period,title,gate,collection,bg,age in history.PERIODS:
        seen=gate in s.get('ivan_campaign',{}).get('memories',[])
        # A locked future recruit stays unnamed until the authored history is read.
        label=collection+' · '+title if seen else collection+' · history not yet revealed'
        reason=history.reason(s,period)
        ttk.Label(parent,text=label+(' — '+reason if reason else ''),wraplength=700).pack(fill='x',pady=3)
        if not reason:
            ttk.Button(parent,text='Visit the waiting interval in person',command=lambda:__import__('flashback_visit_ui').open_in_person(game)).pack(fill='x',pady=3)
