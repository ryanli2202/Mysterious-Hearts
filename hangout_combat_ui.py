"""Combat invitations use the regular hangout artwork, actors and speech bubbles."""
import copy
import queue
import threading
import tkinter as tk
from tkinter import ttk
import combat
import combat_dialogue
from combat_profiles import TEACHERS
import winterfield_ui as ui
import combat_style as style


def open_dialogue(game, who=None, art=None):
    if game.busy or combat.active(game.state_data): return
    import groups
    s=game.state_data
    group=s['groups'].get(s.get('active_group'),{})
    if who:
        combat.check_pair(s,who)
        if not group.get('open') or who not in group.get('members',[]):
            gid=groups.open_solo(s,who) if who in s['routes'] else groups.open_local(s,who)
        else: gid=s['active_group']
    else:
        gid=s.get('active_group')
        if not gid or not group.get('open'): return
    game.hide_phone_for_location()
    view=getattr(game,'combat_view',None)
    if view and view.winfo_exists(): view.place_forget()
    game.select_group(gid)
    game.hangout_view.combat_actions.open(who,art)
    game.persist()


class HangoutCombat:
    def __init__(self, view):
        self.view=view; self.game=view.game
        self.panel=tk.Frame(view.controls,bg=ui.PANEL)
        self.working=False; self.response=None; self.error=''; self.confirming=False
        self.mail=queue.Queue(); self.who=None; self.gid=None

    def open(self,who=None,art=None):
        if self.working or self.response: return
        self.gid=self.game.group_selected
        group=self.game.state_data['groups'][self.gid]
        self.people=[w for w in group['members'] if combat.present(self.game.state_data,w)]
        if not self.people: return
        self.who=who if who in self.people else self.people[0]
        self.art=art; self.confirming=False; self.error=''
        self.draw()

    def button(self,parent,text,fn):
        ttk.Button(parent,text=text,command=fn,state='disabled' if self.working else 'normal').pack(side='left',padx=3,pady=3)

    def draw(self):
        for child in self.panel.winfo_children(): child.destroy()
        self.panel.pack(fill='x',before=self.view.composer,pady=5)
        row=style.Panel(self.panel,padx=8,pady=5); row.pack(fill='x')
        if self.response:
            group=self.game.state_data['groups'].get(self.gid,{})
            label='Continue to fight' if combat.active(self.game.state_data) else 'Continue hangout' if group.get('open') else 'Return to location'
            self.button(row,label,self.continue_scene)
        elif self.confirming:
            ttk.Label(self.panel,text='Attacking permanently ruptures trust and ends an existing romance.',wraplength=650).pack(anchor='w')
            self.button(row,'Confirm attack',lambda:self.request('attack'))
            self.button(row,'Cancel',self.cancel_attack)
        else:
            import game_core
            names=[game_core.contact_name(self.game.state_data,w) for w in self.people]
            people=ttk.Combobox(row,values=names,state='disabled' if self.working else 'readonly',width=22)
            people.current(self.people.index(self.who)); people.pack(side='left',padx=3)
            def select(_):
                self.who=self.people[people.current()]; self.art=None; self.draw()
            people.bind('<<ComboboxSelected>>',select)
            self.button(row,'Ask to spar',lambda:self.request('spar'))
            self.button(row,'Challenge',lambda:self.request('challenge'))
            self.button(row,'Attack…',self.confirm_attack)
            self.button(row,'Close',self.panel.pack_forget)
            arts=TEACHERS.get(self.who,[])
            if arts:
                row=style.Panel(self.panel,padx=8,pady=5); row.pack(fill='x')
                selected=tk.StringVar(value=self.art if self.art in arts else arts[0])
                ttk.Combobox(row,values=arts,textvariable=selected,state='disabled' if self.working else 'readonly',width=24).pack(side='left',padx=3)
                self.button(row,'Ask to learn · 30 min',lambda:self.request('learn',selected.get()))
        if self.error or self.working:
            ttk.Label(self.panel,text='Writing their response…' if self.working else self.error,wraplength=700).pack(anchor='w')
        self.view.resize_controls()

    def confirm_attack(self):
        self.confirming=True; self.draw()

    def cancel_attack(self):
        self.confirming=False; self.draw()

    def request(self,kind,art=None):
        if self.game.busy or self.response: return
        s=self.game.state_data; who=self.who; gid=self.gid
        try: combat.check_pair(s,who)
        except ValueError as exc: self.error=str(exc); self.draw(); return
        snapshot=copy.deepcopy(s)
        self.working=True; self.error=''
        self.game.cancel_suggestions(); self.game.set_busy(True); self.draw()
        self.game.cancel_button.pack_forget()
        def work():
            try: self.mail.put((True,combat_dialogue.generate(snapshot,who,kind,art)))
            except Exception as exc: self.mail.put((False,str(exc)))
        threading.Thread(target=work,daemon=True).start()
        def poll():
            if not self.panel.winfo_exists(): return
            try: ok,value=self.mail.get_nowait()
            except queue.Empty: self.panel.after(100,poll); return
            self.working=False
            if s is not self.game.state_data or gid!=self.game.group_selected:
                ok=False; value='The hangout changed; ask again.'
            if ok:
                try:
                    self.response=combat_dialogue.commit(s,value)
                    self.game.persist()
                except (ValueError,RuntimeError) as exc: self.error=str(exc)
            else: self.error='Response unavailable: '+value+' Retry the action.'
            self.game.set_busy(False); self.draw()
            self.game.status.configure(text=self.error or 'Response ready.')
        self.panel.after(100,poll)

    def continue_scene(self):
        self.response=None; self.confirming=False; self.panel.pack_forget()
        if combat.active(self.game.state_data):
            import combat_ui
            combat_ui.open_combat(self.game)
        else: self.game.render()

    def refresh(self):
        if self.gid!=self.game.group_selected:
            self.panel.pack_forget()
        if self.working: self.game.cancel_button.pack_forget()
        if self.response:
            self.game.retry.pack_forget()
