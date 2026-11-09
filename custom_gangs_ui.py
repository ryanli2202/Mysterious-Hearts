"""Recruitment decisions belong to the main in-person area."""
from tkinter import ttk
import custom_gangs as gangs
import phone_theme


def open_recruit(game, name):
    if game.busy: raise ValueError('Wait for the current conversation to finish.')
    gangs.crew(game.state_data)
    if name not in gangs.RECRUITS: raise ValueError('Choose a listed recruit.')
    venue = gangs.location(game.state_data, name)
    if not venue: raise ValueError('This resident is off duty. Return between 08:00 and 22:00.')
    gangs.jobs.guard(game.state_data, venue, 0)
    import groups
    groups.close_active(game.state_data, 'Started a recruitment discussion.')
    game.close_main_area(); game.hide_phone_for_location()
    game.area_view = RecruitmentView(game.play_body, game, name, venue)
    game.layout_presence(); game.persist()


class RecruitmentView(ttk.Frame):
    def __init__(self, parent, game, name, venue):
        super().__init__(parent, padding=16)
        self.game=game; self.name=name; self.location_key=venue
        ttk.Label(self,text='IN PERSON · Recruitment · '+name,font=('Segoe UI',19,'bold')).pack(anchor='w')
        ttk.Label(self,text='Offer a place in your crew. This is voluntary membership; their ordinary town life continues.\n'
                  'The discussion takes 15 minutes. Roles can be assigned later in Bubblegram → Network → My gang.',wraplength=800).pack(fill='x',pady=12)
        self.status=ttk.Label(self,text=gangs.reason(game.state_data,name) or 'Ready to hear your offer.',wraplength=800)
        self.status.pack(fill='x',pady=8)
        self.offer=ttk.Button(self,text='Offer membership · 15 minutes',command=self.recruit); self.offer.pack(anchor='w',pady=8)
        ttk.Button(self,text='Back to location',command=game.leave_main_area).pack(anchor='w')
        phone_theme.apply_tree(self)

    def recruit(self):
        if self.game.busy: return
        try: result=gangs.recruit(self.game.state_data,self.name)
        except ValueError as exc: self.status.configure(text=str(exc))
        else:
            self.status.configure(text=result); self.offer.configure(state='disabled'); self.game.persist()
