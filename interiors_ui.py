"""Room controls embedded exclusively in the existing in-person window."""
import tkinter as tk
from tkinter import ttk

import interiors
import winterfield_ui as ui


class RoomPanel(tk.Frame):
    def __init__(self, parent, game, *, before=None):
        super().__init__(parent, bg=ui.PANEL)
        self.game = game
        self.stamp = None
        self.before = before
        self.alone = tk.BooleanVar(value=False)

    @property
    def message(self):
        return getattr(self.game, 'interiors_message', '')

    @message.setter
    def message(self, value):
        self.game.interiors_message = value

    def act(self, function, *args, **kwargs):
        if self.game.busy:
            return
        try:
            result = function(self.game.state_data, *args, **kwargs)
            self.message = result if isinstance(result, str) and result not in interiors.ROOMS else ''
            self.game.persist()
        except ValueError as error:
            self.message = str(error)
        self.stamp = None
        self.game.render()
        if self.winfo_exists():
            self.refresh()

    def refresh(self):
        state = self.game.state_data
        if getattr(self.game, 'interiors_story', None) != state.get('story_id'):
            self.game.interiors_story = state.get('story_id')
            self.message = ''
        target = interiors.ROOMS.get(interiors.room(state))
        if not target or not interiors.enabled(state, target.building):
            self.pack_forget()
            return
        self.pack(fill='x', **({'before': self.before} if self.before else {}))
        people = tuple(w for w in interiors.occupants(state, target.id) if w != state['player'])
        def name(who):
            return (__import__('game_core').contact_name(state, who)
                    if __import__('town').hidden.known(state, who) else 'Someone new')
        doors = tuple((ident, interiors.access(state, state['player'], ident)) for ident in target.neighbours)
        guidance=__import__('campaign_markers').room_guidance(state)
        roles = __import__('interior_presence').visible_roles(state)
        import careers
        career_keys = [key for key in careers.available(state)
                       if interiors.same_building(careers.TRACKS[key]['venue'], state['world']['location'])]
        date = state.get('date_session')
        date_ready = bool(date and not date.get('started') and __import__('town').present(state, date['partner']))
        # Time matters through visible results (expired doors/roles, sleep, dates),
        # not the minute itself. Keep controls stable on otherwise idle ticks.
        stamp = (target.id, people, doors, self.message, self.game.busy, self.alone.get(),
                 state.get('job_apps', {}).get('employment'),
                 tuple((who, name(who), state['world']['cast'][who].get('activity') == 'Sleep') for who in people),
                 tuple(state['world'].get('npcs', [])), tuple(state['world'].get('party', [])),
                 tuple((role['id'], role['label']) for role in roles), tuple(career_keys),
                 date.get('partner') if date_ready else None,guidance)
        if stamp == self.stamp:
            return
        self.stamp = stamp
        for child in self.winfo_children():
            child.destroy()
        visible = [*(name(w) for w in people), *state['world'].get('npcs', []),
                   *(role['label'] for role in roles)]
        title = target.label + (' · ' + ', '.join(visible[:3]) if visible else ' · No one else here')
        if guidance[2]:title='◆ Mission room · '+title
        if len(visible) > 3:
            title += f' · {len(visible)-3} more present'
        if target.physical_space == 'rei_home__shared_space':
            title += ' · Open-plan shared space'
        tk.Label(self, text=title, bg=ui.PANEL, fg=ui.GOLD, anchor='w', wraplength=600).pack(fill='x')
        for label in guidance[0]:
            tk.Label(self,text='◆ Campaign · '+label,bg=ui.PANEL,fg=ui.GOLD,anchor='w',wraplength=600).pack(fill='x')
        row = tk.Frame(self, bg=ui.PANEL)
        row.pack(fill='x')
        for index, (ident, outcome) in enumerate(doors):
            room = interiors.ROOMS[ident]
            action = interiors.knock if outcome == 'knock' else interiors.move
            kwargs = {} if outcome == 'knock' else {'companions': not self.alone.get()}
            text = ('Knock · ' if outcome == 'knock' else 'Wait · ' if outcome == 'wait' else '→ ') + room.label
            if ident in guidance[1]:text='◆ Mission route · '+text
            button = ttk.Button(row, text=text,
                state='disabled' if self.game.busy or outcome == 'wait' else 'normal',
                command=lambda f=action, r=ident, kw=kwargs: self.act(f, r, **kw))
            button.grid(row=index // 3, column=index % 3, sticky='ew', padx=2, pady=2)
        for index in range(3):
            row.columnconfigure(index, weight=1)
        options = tk.Frame(self, bg=ui.PANEL)
        options.pack(fill='x')
        if target.id == 'chess__playing_room':
            import chess_lounge
            table = ttk.Menubutton(self, text='Play chess', state='disabled' if self.game.busy else 'normal')
            menu = tk.Menu(table, tearoff=False, bg=ui.PANEL, fg=ui.CREAM)
            for who in chess_lounge.opponents(state):
                label = name(who) if who in people else who
                menu.add_command(label='Challenge · ' + label,
                                 command=lambda w=who, n=label: self.game.enter_chess(w, n))
            menu.add_command(label='Practice · Level 3', command=lambda: self.game.enter_chess(None, 'Practice board'))
            table.configure(menu=menu)
            table.pack(before=options, anchor='w')
            ttk.Button(self, text='Match history', command=self.game.open_chess_history,
                       state='disabled' if self.game.busy else 'normal').pack(before=options, anchor='w')
        tk.Checkbutton(options, text='Enter alone; companions wait here', variable=self.alone,
            command=self.refresh, bg=ui.PANEL, fg=ui.CREAM, selectcolor=ui.CARD,
            activebackground=ui.PANEL, activeforeground=ui.CREAM).pack(side='left')
        ttk.Button(options, text='Wait 30 min', state='disabled' if self.game.busy else 'normal',
                   command=lambda:self.act(__import__('town').wait, 30)).pack(side='right')
        invites = tk.Frame(self, bg=ui.PANEL)
        invites.pack(fill='x')
        for index, who in enumerate(people):
            ttk.Button(options, text='Talk · ' + name(who),
                state='disabled' if self.game.busy or state['world']['cast'][who].get('activity') == 'Sleep' else 'normal',
                command=lambda person=who:self.act(__import__('town').meet, person)).pack(side='left', padx=2)
            invite=ttk.Menubutton(invites,text='Invite · '+name(who),state='disabled' if self.game.busy else 'normal')
            menu=tk.Menu(invite,tearoff=False,bg=ui.PANEL,fg=ui.CREAM,activebackground=ui.CARD,activeforeground=ui.GOLD)
            for destination in target.neighbours:
                menu.add_command(label='Continue together · '+interiors.ROOMS[destination].label,
                    command=lambda person=who,door=destination:self.act(interiors.invite,person,door))
            invite.configure(menu=menu)
            invite.grid(row=index//3, column=index%3, sticky='w', padx=(0,4), pady=2)
        for who in state['world'].get('party', []):
            if who not in people:
                ttk.Button(options, text='Reunite · ' + __import__('game_core').contact_name(state, who),
                    state='disabled' if self.game.busy else 'normal',
                    command=lambda person=who:self.act(interiors.reunite, person)).pack(side='left', padx=2)
        if self.message:
            tk.Label(self, text=self.message, bg=ui.PANEL, fg=ui.CREAM, wraplength=600, anchor='w').pack(fill='x')
        if __import__('interior_work').active(state):
            work = tk.Frame(self, bg=ui.PANEL)
            work.pack(fill='x', pady=3)
            for purpose, caption in (('shift', 'Arrange shift access'), ('development', 'Arrange supervisor visit')):
                ttk.Button(work, text=caption, state='disabled' if self.game.busy else 'normal',
                    command=lambda task=purpose:self.act(__import__('interior_work').prepare, task)).pack(side='left', padx=2)
        for key in career_keys:
            ttk.Button(self,text='Arrange career access · '+careers.TRACKS[key]['title'],
                state='disabled' if self.game.busy else 'normal',
                command=lambda track=key:self.act(__import__('interior_work').prepare_career,track)).pack(anchor='w',pady=2)
        for role in roles:
            tk.Label(self, text=role['label']+' is here for the work meeting.', bg=ui.PANEL,
                     fg=ui.MUTED, anchor='w').pack(fill='x')
        if date_ready:
            ttk.Button(self, text='Begin planned date', state='disabled' if self.game.busy else 'normal',
                       command=lambda:self.act(__import__('dating').begin, date['partner'])).pack(anchor='w', pady=2)
