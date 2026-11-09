"""Home self-actions."""
import tkinter as tk
from tkinter import ttk, messagebox
from phone_dialogs import AppWindow, messagebox, simpledialog
import town
from artwork import ArtCanvas, scene_art
import winterfield_ui as ui

class HomeWindow(AppWindow):
    def __init__(self,game):
        super().__init__(game); self.game=game
        self.title('Home · Self actions'); self.geometry('640x650')
        home = town.HOMES[game.state_data['player']]
        ArtCanvas(self, scene_art(home), height=100).pack(fill='x')
        self.configure(bg=ui.PANEL)
        self.heading=ttk.Label(self,wraplength=590,font=(ui.SERIF,17)); self.heading.pack(anchor='w',padx=18,pady=(10,2))
        self.description=ttk.Label(self,wraplength=590,style='Muted.TLabel'); self.description.pack(anchor='w',padx=18,pady=(0,8))
        self.journal=ui.transcript(self,height=6); self.journal.pack(fill='both',expand=True,padx=18)
        for i,action in enumerate(town.HOME_ACTIONS[game.state_data['player']]):
            ttk.Button(self,text=f'{i+1}  {action}',command=lambda a=action:self.act(town.home_action,a)).pack(fill='x',padx=18,pady=4)
        ttk.Label(self,text='5  Custom self action').pack(anchor='w',padx=18)
        self.entry=ttk.Entry(self); self.entry.pack(fill='x',padx=18,pady=4)
        self.entry.bind('<Return>',lambda e:self.custom())
        ttk.Button(self,text='Do custom action',command=self.custom).pack(fill='x',padx=18,pady=4)
        ttk.Button(self,text='Rest at home',command=lambda:self.act(town.rest)).pack(fill='x',padx=18,pady=10)
        ttk.Button(self,text='Sleep speed / skip to waking',command=lambda:__import__('autonomy_ui').open_window(self.game)).pack(fill='x',padx=18,pady=4)
        ttk.Button(self,text='Needs · Nap / sleep / visitors',command=lambda:__import__('autonomy_ui').open_window(self.game)).pack(fill='x',padx=18,pady=4)
        self.render()
    def custom(self):
        self.act(town.home_action,self.entry.get())
    def act(self,fn,*args):
        if self.game.busy: return
        try: fn(self.game.state_data,*args)
        except ValueError as exc: messagebox.showinfo('Home',str(exc),parent=self); return
        self.entry.delete(0,'end'); self.game.persist(); self.game.render(); self.render()
    def render(self):
        s=self.game.state_data; data=town.loop.HOUSES[s['player']]
        self.heading.configure(text=data[1])
        self.description.configure(text=data[2]+'\n'+town.loop.clock(s))
        self.journal.configure(state='normal'); self.journal.delete('1.0','end')
        self.journal.insert('end','\n\n'.join(s['world'].get('home_journal',[])) or 'A little time for yourself.')
        keepsakes=s.get('career_keepsakes',[])
        if keepsakes:
            self.journal.insert('end','\n\nCareer keepsakes at home\n'+'\n'.join(item['title']+' — '+item['outcome'] for item in keepsakes[-8:]))
        self.journal.configure(state='disabled'); self.journal.see('end')
