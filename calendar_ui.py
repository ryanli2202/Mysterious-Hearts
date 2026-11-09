import calendar
from datetime import date, timedelta
import tkinter as tk
from tkinter import ttk, messagebox
from phone_dialogs import AppWindow, messagebox, simpledialog
import story_calendar as dates
import town
import winterfield_ui as ui
import careers
import crime_diplomacy


class CalendarWindow(AppWindow):
    def __init__(self, game):
        super().__init__(game)
        self.game = game
        self.title('Winterfield calendar')
        self.geometry('900x680')
        self.minsize(680, 445)
        self.configure(bg=ui.INK)
        self.selected = self.today()
        self.draw()

    def today(self):
        return dates.story_date(self.game.state_data['world']['minute'])

    def show(self, day):
        self.selected = day
        self.draw()

    def draw(self):
        import syndicate_council
        syndicate_council.ensure(self.game.state_data)
        for child in self.winfo_children():
            if not isinstance(child, tk.Toplevel):
                child.destroy()
        panel = ttk.Frame(self, padding=16)
        panel.pack(fill='both', expand=True, padx=12, pady=12)
        day = self.selected
        today = self.today()
        first = day.replace(day=1)
        following = first + timedelta(days=calendar.monthrange(day.year, day.month)[1])
        syndicate_council.ensure(self.game.state_data, (following-dates.START).days*1440)
        head = ttk.Frame(panel)
        head.pack(fill='x', pady=(0, 14))
        ttk.Button(head, text='Plan an event', command=self.plan_event).pack(side='left', padx=8)
        if self.phone:
            ttk.Label(panel,text=f'{day:%B %Y}',style='Title.TLabel').pack(before=head,anchor='w',pady=(0,8))
        else:
            ttk.Label(head, text=f'{day:%B %Y}', style='Title.TLabel').pack(side='left')
        for text, dest, enabled in [('›', following, True), ('Today', today, True),
                                    ('‹', first-timedelta(days=1), first > dates.START)]:
            ttk.Button(head, text=text, width=len(text)+2, command=lambda d=dest:self.show(d),
                       state='normal' if enabled else 'disabled').pack(side='right', padx=2)
        body = ttk.Frame(panel)
        body.pack(fill='both', expand=True)
        month = tk.Frame(body, bg=ui.PANEL)
        month.pack(side='top' if self.phone else 'left', fill='x' if self.phone else 'both', expand=not bool(self.phone), padx=0 if self.phone else (0,16))
        side = ttk.Frame(body); side.pack(side='top' if self.phone else 'right', fill='both' if self.phone else 'y',expand=bool(self.phone))
        canvas = tk.Canvas(side, bg=ui.INK, width=270, height=320, highlightthickness=0)
        scroll = ttk.Scrollbar(side, command=canvas.yview); scroll.pack(side='right', fill='y')
        canvas.configure(yscrollcommand=scroll.set); canvas.pack(side='left', fill='both', expand=True)
        agenda = tk.Frame(canvas, bg=ui.INK, padx=14, pady=12)
        canvas.create_window((0,0), window=agenda, anchor='nw', width=270)
        agenda.bind('<Configure>', lambda _:canvas.configure(scrollregion=canvas.bbox('all')))
        canvas.bind('<MouseWheel>', lambda e:canvas.yview_scroll(-int(e.delta/120), 'units'))
        self._agenda_labels = []
        def label(text, color=ui.CREAM, font=('Segoe UI', 10)):
            item = tk.Label(agenda, text=text, fg=color, bg=ui.INK, font=font, anchor='w',
                            justify='left', wraplength=188)
            item.pack(fill='x', pady=(0, 5))
            item._fixed_wraplength = 188
            self._agenda_labels.append(item)
        for col, weekday in enumerate(calendar.day_abbr):
            month.columnconfigure(col, weight=1, uniform='day')
            ttk.Label(month, text=weekday, style='Muted.TLabel').grid(row=0,column=col,pady=(0,6))
        for row, week in enumerate(calendar.Calendar().monthdatescalendar(day.year,day.month),1):
            month.rowconfigure(row, weight=1, uniform='week')
            for col, d in enumerate(week):
                if d.month != day.month: continue
                has_event = dates.events(self.game.state_data, d) or any(not e.get('cancelled') and dates.story_date(e['start']) == d for e in self.game.state_data.get('scheduled_events', [])) or any(e['status']=='booked' and dates.story_date(e['start'])==d for e in self.game.state_data.get('careers',{}).get('bookings',[]))
                has_event = has_event or any(dates.story_date(e['start'])==d for e in crime_diplomacy.commitments(self.game.state_data))
                tk.Button(month, text=str(d.day) + (' •' if has_event else ''), width=3, bd=0,
                          font=('Segoe UI', 11, 'bold' if d == today or has_event else 'normal'),
                          bg=ui.GOLD if d == day else ui.CARD if col < 5 else '#263b43',
                          fg=ui.INK if d == day else ui.MINT if has_event else ui.CREAM,
                          activebackground='#40576a', activeforeground=ui.CREAM, cursor='hand2',
                          command=lambda value=d:self.show(value)).grid(row=row,column=col,sticky='nsew',padx=2,pady=2)
        label(f'{day:%A}', ui.MINT)
        label(f'{day:%B} {day.day}', font=(ui.SERIF, 19))
        import scheduled_events
        for item in crime_diplomacy.commitments(self.game.state_data):
            if dates.story_date(item['start'])!=day: continue
            label('Leadership meeting · '+item.get('representative',''))
            label(f'{item["start"]%1440//60:02}:{item["start"]%60:02} · {town.LOCATIONS[item["venue"]]}')
            label('Ends '+f'{item["end"]%1440//60:02}:{item["end"]%60:02}'+' · '+item['status'])
            label('Agenda: '+'; '.join(item.get('agenda',[])))
            ttk.Button(agenda,text='Open Bubblegram leadership',command=self.open_leadership).pack(anchor='w')
        for item in self.game.state_data.get('careers',{}).get('bookings',[]):
            if dates.story_date(item['start']) != day: continue
            label(item['title']+' · '+item['status'])
            label(f"{item['start']%1440//60:02}:{item['start']%60:02} · {town.LOCATIONS[item['venue']]}")
            ttk.Button(agenda,text='Open work & ambitions',command=lambda k=item['track']:self.open_career(k)).pack(anchor='w')
        for item in self.game.state_data.get('scheduled_events', []):
            if dates.story_date(item['start']) != day or item.get('cancelled'): continue
            label(scheduled_events.describe(item))
            council = item.get('source') == syndicate_council.SOURCE
            label(syndicate_council.details(item) if council else 'Guests: ' + ', '.join(w.title() for w in item['guests']))
            if item['end'] > self.game.state_data['world']['minute']:
                if not council:
                    ttk.Button(agenda, text='Cancel event', command=lambda e=item:self.cancel_event(e)).pack(anchor='w')
                ttk.Button(agenda, text='Join event', command=lambda e=item:self.join_event(e)).pack(anchor='w')
                if self.game.state_data['world']['minute'] < item['start']:
                    label('Join at the scheduled time after travelling to the venue.', ui.MUTED)
        if dates.free_day(day): label('Day off', ui.GOLD)
        events = dates.events(self.game.state_data, day)
        if not events and not any(dates.story_date(e['start'])==day and e['status']=='booked' for e in self.game.state_data.get('careers',{}).get('bookings',[])) and not any(dates.story_date(e['start'])==day and not e.get('cancelled') for e in self.game.state_data.get('scheduled_events',[])):
            if not any(dates.story_date(e['start'])==day for e in crime_diplomacy.commitments(self.game.state_data)):
                label('No events scheduled.', ui.MUTED)
        for title,activity,_ in events:
            outing = dates.OUTINGS.get((day.month, day.day))
            is_outing = outing and outing.title == title
            details = title + ('\n' + town.LOCATIONS[outing.venue] if is_outing else '')
            label(details)
            if day == today:
                done = day.isoformat()+'/'+title in self.game.state_data.get('celebrations', [])
                ttk.Button(agenda,text='Celebrated' if done else activity,
                           state='disabled' if done or self.game.busy else 'normal',
                           command=(lambda o=outing:self.choose_outing(o)) if is_outing else
                                   (lambda event=title:self.celebrate(event))).pack(anchor='w', pady=4)
        ttk.Separator(agenda).pack(fill='x', pady=10)
        label('Coming up', ui.GOLD)
        shown = 0
        for offset in range(1, 91):
            when = day + timedelta(days=offset)
            upcoming = dates.events(self.game.state_data, when)
            if upcoming:
                tk.Button(agenda, text=f'{when:%b %d}  ·  {upcoming[0][0]}', wraplength=178, anchor='w',
                          justify='left', bg=ui.INK, fg=ui.CREAM, activebackground=ui.CARD,
                          activeforeground=ui.CREAM, relief='flat', cursor='hand2',
                          command=lambda d=when:self.show(d)).pack(fill='x')
                shown += 1
                if shown == 3: break

    def open_career(self, key):
        from careers_ui import open_careers
        window=open_careers(self.game)
        window.key=key; window.section='Schedule'; window.draw()

    def open_leadership(self):
        if self.phone:
            self.phone.open_leadership()
        else:
            self.game.phone_window('Bubblegram')
            self.game.phone_activity.job_board.change('Leadership')

    def cancel_event(self, event):
        if self.game.busy: return
        import scheduled_events
        scheduled_events.cancel(self.game.state_data, event)
        self.game.persist()
        self.game.render()
        self.draw()

    def join_event(self, event):
        import scheduled_events
        if self.game.busy: return
        try: scheduled_events.join(self.game.state_data, event)
        except ValueError as exc:
            messagebox.showinfo('Join event', str(exc), parent=self); return
        self.game.persist(); self.game.render(); self.game.show_in_person()

    def plan_event(self):
        import scheduled_events
        import hidden_cast
        if self.game.busy: return
        win = AppWindow(self); win.title('Plan an outing or event'); win.geometry('520x650')
        form = ttk.Frame(win, padding=16); form.pack(fill='both', expand=True)
        fields = {}
        for label, default in [('Title', 'An afternoon together'), ('Date (YYYY-MM-DD)', self.selected.isoformat()), ('Time (HH:MM)', '17:00')]:
            ttk.Label(form, text=label).pack(anchor='w')
            field = ttk.Entry(form); field.insert(0, default); field.pack(fill='x', pady=(0,8)); fields[label] = field
        places = {k:v for k,v in town.LOCATIONS.items() if k != 'home' and not k.startswith('car:') and hidden_cast.visible_place(self.game.state_data,k)}
        ttk.Label(form, text='Venue').pack(anchor='w')
        venue = ttk.Combobox(form, values=list(places.values()), state='readonly'); venue.current(0); venue.pack(fill='x')
        ttk.Label(form, text='Duration (minutes)').pack(anchor='w')
        duration = ttk.Combobox(form, values=[30,60,90,120,180], state='readonly'); duration.set('60'); duration.pack(fill='x')
        ttk.Label(form, text='Guests · select one or several').pack(anchor='w', pady=(10,0))
        people = [w for w in self.game.state_data['world']['cast'] if w != self.game.state_data['player'] and hidden_cast.contact(self.game.state_data,w)]
        guests = tk.Listbox(form, selectmode='multiple', exportselection=False, height=9)
        for who in people: guests.insert('end', who.title())
        guests.pack(fill='both', expand=True)
        ttk.Label(form, text='Game-time reminders: 1 hour and 15 minutes before.\nGuests attend automatically for the chosen duration.').pack(anchor='w', pady=8)
        def save_event():
            if self.game.busy: return
            try:
                scheduled_events.create(self.game.state_data, fields['Title'].get(), fields['Date (YYYY-MM-DD)'].get(),
                    fields['Time (HH:MM)'].get(), next(k for k,v in places.items() if v == venue.get()),
                    [people[i] for i in guests.curselection()], int(duration.get()))
            except (ValueError, StopIteration) as exc:
                messagebox.showinfo('Check event details', str(exc), parent=win); return
            self.game.persist(); self.draw(); win.destroy()
        ttk.Button(form, text='Schedule event', command=save_event).pack(fill='x')

    def choose_outing(self, outing):
        s = self.game.state_data
        if self.game.busy or self.selected != self.today(): return
        if s['world']['location'] != outing.venue:
            messagebox.showinfo(outing.title, 'Visit ' + town.LOCATIONS[outing.venue] +
                                ' in Town, then open today’s calendar to take part.', parent=self)
            return
        people = dates.outing_companions(s)
        if not people:
            messagebox.showinfo(outing.title, 'Meet a friend here or exchange contact details so you can invite them.', parent=self)
            return
        win = AppWindow(self)
        win.title(outing.title)
        win.transient(self)
        win.grab_set()
        panel = ttk.Frame(win, padding=14)
        panel.pack()
        ttk.Label(panel, text='Choose a friend or partner to join you').pack()
        names = [s.get('nicknames', {}).get(p) or p.title() for p in people]
        picker = ttk.Combobox(panel, values=names, state='readonly')
        picker.pack(pady=6)
        picker.current(0)
        def select_activity(choice):
            index = picker.current()
            win.destroy()
            self.celebrate(outing.title, people[index], choice)
        for choice in outing.activities:
            ttk.Button(panel, text=choice, command=lambda c=choice:select_activity(c)).pack(fill='x', pady=2)

    def celebrate(self, title, companion=None, activity=None):
        if self.game.busy or self.selected != self.today(): return
        try:
            note = dates.celebrate(self.game.state_data, title, companion, activity)
        except ValueError as exc:
            messagebox.showinfo(title, str(exc), parent=self)
            return
        if note:
            self.game.persist()
            self.game.render()
            messagebox.showinfo(title, note, parent=self)
