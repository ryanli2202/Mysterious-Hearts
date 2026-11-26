"""Flashback visits embedded in the main in-person window."""
import copy
import queue
import threading
import tkinter as tk
from tkinter import ttk
import flashback_visits as visits
import campaign_voice
import phone_theme
import winterfield_ui as ui
from hangout_ui import HangoutCanvas, Exchange


def open_in_person(game):
    if game.busy or not visits.area_for(game.state_data.get('player')):return
    existing=getattr(game,'flashback_view',None)
    if existing is not None and existing.winfo_exists():
        if existing.state is game.state_data:
            existing.lift();return existing
        existing.destroy()
    try:visits.enter(game.state_data)
    except ValueError as exc:
        if game.state_data.get('player')=='neo' and visits.active(game.state_data):
            game.hide_phone_for_location()
            view=game.flashback_view=FlashbackReferenceError(game.play_body,game,str(exc))
            view.place(x=0,y=0,relwidth=1,relheight=1);view.lift();view.focus_set()
            return view
        from phone_dialogs import messagebox
        messagebox.showinfo('Flashback area',str(exc),parent=game);return
    game.hide_phone_for_location()
    game.cancel_suggestions()
    game.clock_label.configure(text='Flashback · Present-day time paused')
    game.time_button.configure(text='Time · Paused ▾')
    view=game.flashback_view=FlashbackView(game.play_body,game)
    view.place(x=0,y=0,relwidth=1,relheight=1);view.lift()
    view.grab_set();view.entry.focus_set()
    game.simulation_clock.reset(game.state_data)
    game.persist()
    return view


class FlashbackView(tk.Frame):
    def __init__(self,parent,game):
        super().__init__(parent,bg=ui.INK)
        self.game=game;self.busy=False;self.closed=False;self.job=None;self.results=queue.Queue()
        self.state=game.state_data;self.journal_view=None;self.poll_id=None
        self.fox_voice=campaign_voice.Playback(game.sounds)
        self.bind('<Unmap>',self.stop_fox_voice,add='+')
        self.bind('<Destroy>',self.stop_fox_voice,add='+')
        area=visits.AREAS[visits.active(game.state_data)['area']]
        header=tk.Frame(self,bg=ui.PANEL,padx=12,pady=9);header.pack(fill='x')
        ttk.Button(header,text='Return to the present',command=self.leave).pack(side='right')
        ttk.Label(header,text=area['title'],font=('Segoe UI',14,'bold')).pack(anchor='w')
        ttk.Label(header,text='Past selves · Time is paused · Conversations stay in this memory').pack(anchor='w')
        content=self
        if game.state_data.get('player')=='neo':
            scroller=tk.Frame(self,bg=ui.INK);scroller.pack(fill='both',expand=True)
            self.neo_scroll=tk.Canvas(scroller,bg=ui.INK,highlightthickness=0)
            bar=ttk.Scrollbar(scroller,orient='vertical',command=self.neo_scroll.yview);bar.pack(side='right',fill='y')
            self.neo_scroll.pack(fill='both',expand=True);self.neo_scroll.configure(yscrollcommand=bar.set)
            content=tk.Frame(self.neo_scroll,bg=ui.INK);window=self.neo_scroll.create_window(0,0,window=content,anchor='nw')
            content.bind('<Configure>',lambda e:self.neo_scroll.configure(scrollregion=self.neo_scroll.bbox('all')))
            self.neo_scroll.bind('<Configure>',lambda e:self.neo_scroll.itemconfigure(window,width=e.width))
            self.neo_scroll.bind('<MouseWheel>',lambda e:self.neo_scroll.yview_scroll(-int(e.delta/120),'units'))
        cast=tk.Frame(content,bg=ui.PANEL,padx=12,pady=5);cast.pack(fill='x')
        self.selections={};self.change_controls=[];self.cast_buttons={}
        for who in area['cast']:
            if who==game.state_data['player']:continue
            var=tk.BooleanVar(value=who in visits.active(game.state_data)['members']);self.selections[who]=var
            button=ttk.Checkbutton(cast,text=visits.name(who),variable=var)
            button.pack(side='left',padx=(0,10));self.change_controls.append(button);self.cast_buttons[who]=button
        choose=ttk.Button(cast,text='Speak with selected' if visits.active(game.state_data)['area']=='takeo-command-history' else 'Hang out with selected',command=self.select)
        choose.pack(side='left');self.change_controls.append(choose)
        ttk.Button(cast,text='Memory journal',command=self.journal).pack(side='right')
        import campaign_memory_areas as spaces
        rooms=tk.Frame(content,bg=ui.PANEL,padx=12,pady=5);rooms.pack(fill='x')
        self.period=tk.StringVar(value=visits.active(game.state_data).get('period',spaces.PERIODS[visits.active(game.state_data)['area']][0][0]))
        ttk.Label(rooms,text='Period').pack(side='left')
        self.period_control=ttk.Combobox(rooms,state='readonly',textvariable=self.period,width=12,
            values=list(dict(spaces.periods(game.state_data,visits.active(game.state_data)['area']))))
        self.period_control.pack(side='left',padx=5);self.period_control.bind('<<ComboboxSelected>>',lambda e:self.change_area(visits.change_period,self.period.get()))
        self.room_buttons={}
        room_buttons_parent=rooms
        if visits.active(game.state_data)['area'] in ('elias-family-stage','camila-house','sylvanis-before-cards','neo-school','neo-adoptive-home','neo-shinigami-facility','takeo-command-history','ivan-network-history'):
            room_buttons_parent=tk.Frame(content,bg=ui.PANEL,padx=12,pady=3)
            room_buttons_parent.pack(fill='x')
        for index,(ident,room) in enumerate(spaces.ROOMS[visits.active(game.state_data)['area']].items()):
            button=ttk.Button(room_buttons_parent,text=room[0],command=lambda r=ident:self.change_area(visits.move_room,r))
            if visits.active(game.state_data)['area']=='sylvanis-before-cards':
                button.grid(row=index//3,column=index%3,sticky='ew',padx=2,pady=2);room_buttons_parent.columnconfigure(index%3,weight=1)
            else:button.pack(side='left',padx=2)
            self.room_buttons[ident]=button
        self.room_status=ttk.Label(content,text='',wraplength=900);self.room_status.pack(fill='x',padx=12,pady=3)
        if visits.active(game.state_data)['area']=='martos-service-years':
            appointments=rooms
            self.voss_appointment=ttk.Button(appointments,text='Arrange unit appointment with Voss',command=lambda:self.change_area(lambda s,v:visits.arrange_voss(s),None));self.voss_appointment.pack(side='left',padx=3)
            self.sera_appointment=ttk.Button(appointments,text='Arrange Sera’s voluntary early-service visit',command=lambda:self.change_area(lambda s,v:visits.arrange_sera(s),None));self.sera_appointment.pack(side='left',padx=3)
        if visits.active(game.state_data)['area']=='elias-family-stage':
            self.site_cut=ttk.Button(rooms,text='Site cut · family house ⇄ theatre',command=lambda:self.change_area(lambda s,v:visits.site_cut(s),None))
            self.site_cut.pack(side='left',padx=3)
            self.crow_appointment=ttk.Button(rooms,text='Arrange private Crow appointment',command=lambda:self.change_area(lambda s,v:visits.arrange_elias_crow(s),None))
            self.crow_appointment.pack(side='left',padx=3)
        if visits.active(game.state_data)['area']=='fg-early-partnership':
            ttk.Button(rooms,text='Ask to use annex table',command=lambda:self.change_area(lambda s,v:visits.request_annex(s),None)).pack(side='left',padx=3)
        self.stage=MemoryStage(content,game);self.stage.pack(fill='both',expand=True)
        if game.state_data.get('player')=='neo':self.stage.canvas.configure(height=330)
        self.canvas=self.stage.canvas
        controls=tk.Frame(content,bg=ui.PANEL,padx=12,pady=8);controls.pack(fill='x')
        topics=tk.Frame(controls,bg=ui.PANEL);topics.pack(fill='x',pady=(0,5));self.topic_buttons=[]
        for index in range(3):
            button=ttk.Button(topics,command=lambda i=index:self.ask_topic(i));button.pack(side='left',fill='x',expand=True,padx=2)
            self.topic_buttons.append(button);self.change_controls.append(button)
        voice=tk.Frame(controls,bg=ui.PANEL);voice.pack(fill='x')
        ttk.Button(voice,text='‹ Speaker',command=lambda:self.canvas.turn_speaker(-1)).pack(side='left')
        ttk.Button(voice,text='Speaker ›',command=lambda:self.canvas.turn_speaker(1)).pack(side='left',padx=4)
        self.status=ttk.Label(voice,text='Choose a participant or discuss the report.' if visits.active(game.state_data)['area']=='takeo-command-history' else 'Choose a friend, say something, or spend time together.');self.status.pack(side='left',padx=8)
        actions=tk.Frame(controls,bg=ui.PANEL);actions.pack(fill='x',pady=5)
        self.action_controls=[];self.activity_buttons=[]
        for i,text in enumerate(area['activities']):
            button=ttk.Button(actions,text=text,command=lambda text=text:self.submit(text,'action'))
            button.grid(row=i//2,column=i%2,sticky='ew',padx=2,pady=2);self.change_controls.append(button);self.action_controls.append(button);self.activity_buttons.append(button)
        actions.columnconfigure((0,1),weight=1)
        compose=tk.Frame(controls,bg=ui.PANEL);compose.pack(fill='x')
        self.entry=tk.Entry(compose,bg=ui.CARD,fg=ui.CREAM,insertbackground=ui.CREAM,
            disabledbackground=ui.PANEL,disabledforeground=ui.MUTED,relief='flat',font=('Segoe UI',12))
        self.entry.pack(side='left',fill='x',expand=True,ipady=5)
        self.entry.bind('<Return>',lambda event:self.submit(self.entry.get(),'speak'))
        for title,kind in (('Say','speak'),('Do action · no time','action')):
            button=ttk.Button(compose,text=title,command=lambda kind=kind:self.submit(self.entry.get(),kind))
            button.pack(side='left',padx=4);self.change_controls.append(button);self.action_controls.append(button)
        self.cancel=ttk.Button(compose,text='Cancel',command=self.cancel_reply,state='disabled');self.cancel.pack(side='left')
        phone_theme.apply_tree(self)
        self.refresh()
        self.poll_id=self.after(80,self.poll)

    def stop_fox_voice(self,event=None):
        if (event is None or event.widget is self) and self.fox_voice.record:
            self.fox_voice.enter(None,None,autoplay=False)

    def refresh(self):
        s=self.game.state_data;visit=visits.active(s)
        if not visit:return
        self.period.set(visit.get('period',self.period.get()))
        exchange=visits.record(s)['exchange']
        record=None
        if visit['area']=='fg-early-partnership' and visit['members'][:1]==['fox'] and len(exchange['lines'])==1:
            line=exchange['lines'][0]
            if line['speaker']=='fox':
                record=campaign_voice.fixed_record(exchange.get('fox_opening_voice'),s['player'],
                                                  'fg-early-partnership',line['text'])
        if record or self.fox_voice.record:
            campaign_voice.sync_fixed(self.fox_voice,s,(id(exchange),visit['revision']),record)
        self.canvas.members=list(visit['members'])
        self.canvas.exchange=Exchange(player=exchange['player'],narration=exchange['narration'],
            speeches=[(row['speaker'],row['text']) for row in exchange['lines']])
        import campaign_memory_areas as spaces
        self.canvas.artwork=spaces.background(s)
        current=spaces.room(s);room=spaces.ROOMS[visit['area']][current]
        topics=spaces.topics(s,visit['members'][0]) if visit['members'] else ()
        for index,button in enumerate(self.topic_buttons):button.configure(text=topics[index] if topics else 'No companion here',state='normal' if topics and not self.busy else 'disabled')
        if visit['area'] in ('elias-family-stage','camila-house','sylvanis-before-cards','neo-school','neo-adoptive-home','neo-shinigami-facility','takeo-command-history','ivan-network-history'):
            for index,button in enumerate(self.activity_buttons):
                local=spaces.activities(s)
                if index<len(local):
                    label=local[index];button.configure(text=label,command=lambda label=label:self.submit(label,'action'));button.grid()
                else:button.grid_remove()
        for button in self.action_controls:button.configure(state='normal' if visit['members'] and not self.busy else 'disabled')
        if visit['area']=='ivan-network-history':
            for button in self.activity_buttons:button.configure(state='normal' if not self.busy else 'disabled')
        self.entry.configure(state='normal' if visit['members'] and not self.busy else 'disabled')
        if not visit['members']:self.status.configure(text='No companion in this interval. Observe the room or practise harmlessly.' if visit['area']=='ivan-network-history' else 'This room is quiet. Move to a room with a historical companion.')
        elif str(self.status.cget('text')).startswith('This room is quiet.'):self.status.configure(text='A historical companion is present. Time stays paused.')
        route_note=('Family house / separate theatre: use the labelled site cut. ' if visit['area']=='elias-family-stage' and visit.get('period') in ('EL-A','EL-D') else 'Family house rooms only in this period. ' if visit['area']=='elias-family-stage' else 'Adjacent rooms only; ')
        self.room_status.configure(text=room[0]+' · '+dict(spaces.periods(s,visit['area'])).get(visit.get('period'),'Historical interval')+' · '+route_note+'This visit changes no present-day progress.')
        for who,button in self.cast_buttons.items():
            self.selections[who].set(who in visit['members'])
            button.configure(state='normal' if who in visits.available(s) and not self.busy else 'disabled')
        if hasattr(self,'voss_appointment'):
            if visit.get('period') in ('MT-A','MT-B'):self.voss_appointment.pack(side='left',padx=3);self.sera_appointment.pack_forget()
            elif visit.get('period')=='MT-D':self.sera_appointment.pack(side='left',padx=3);self.voss_appointment.pack_forget()
            else:self.voss_appointment.pack_forget();self.sera_appointment.pack_forget()
            self.voss_appointment.configure(state='normal' if visit.get('period') in ('MT-A','MT-B') and spaces.room(s) in ('T1','T2') else 'disabled')
            self.sera_appointment.configure(state='normal' if visit.get('period')=='MT-D' else 'disabled')
        if hasattr(self,'crow_appointment'):
            current=spaces.room(s);period=visit.get('period')
            self.crow_appointment.configure(state='normal' if period in ('EL-C','EL-D') and current=='E4' and not self.busy else 'disabled')
            self.site_cut.configure(state='normal' if ((period=='EL-A' and current in ('E1','E5')) or (period=='EL-D' and current in ('E4','E5'))) and not self.busy else 'disabled')
        for index,(ident,button) in enumerate(self.room_buttons.items()):
            if visit['area']=='sylvanis-before-cards':
                if ident in spaces.allowed_rooms(s):button.grid(row=index//3,column=index%3,sticky='ew',padx=2,pady=2)
                else:button.grid_remove()
            elif ident in spaces.allowed_rooms(s):button.pack(side='left',padx=2)
            else:button.pack_forget()
            button.configure(state='normal' if ident in room[2] and not self.busy and not (visit['area']=='elias-family-stage' and ((current=='E4' and ident=='E5') or (current=='E5' and ident=='E4'))) else 'disabled')
        self.canvas.speech_index=0;self.canvas.page_indices=dict.fromkeys(self.canvas.page_indices,0)
        self.canvas.redraw()

    def ask_topic(self,index):
        import campaign_memory_areas as spaces
        visit=visits.active(self.game.state_data)
        topic=spaces.topics(self.game.state_data,visit['members'][0])[index]
        self.submit('What would you like to say about '+topic.lower()+'?','speak')

    def change_area(self,fn,value):
        if self.busy:return
        try:fn(self.game.state_data,value)
        except ValueError as exc:self.status.configure(text=str(exc));return
        self.period.set(visits.active(self.game.state_data).get('period',''))
        self.game.persist();self.refresh()

    def working(self,value):
        self.busy=value
        for control in self.change_controls:control.configure(state='disabled' if value else 'normal')
        self.entry.configure(state='disabled' if value else 'normal')
        self.cancel.configure(state='normal' if value else 'disabled')
        self.period_control.configure(state='disabled' if value else 'readonly')
        self.refresh()

    def select(self):
        if self.busy:return
        try:visits.select(self.game.state_data,[who for who,var in self.selections.items() if var.get()])
        except ValueError as exc:self.status.configure(text=str(exc));return
        self.refresh();self.game.persist();self.status.configure(text='The selected participants are here. Time stays paused.' if visits.active(self.game.state_data)['area']=='takeo-command-history' else 'Your selected friends are here. Time stays paused.')

    def submit(self,text,kind):
        if self.busy:return
        if visits.active(self.game.state_data)['area']=='ivan-network-history':
            try:
                if kind!='action':raise ValueError('No historical companion is present. Observe the room or practise harmlessly.')
                self.status.configure(text=__import__('ivan_history').inspect(self.game.state_data,text));self.refresh();self.game.persist()
            except ValueError as exc:self.status.configure(text=str(exc))
            return
        if not visits.active(self.game.state_data)['members']:
            self.status.configure(text='This room is quiet. Move to a room with a historical companion.');return
        try:
            text=visits.input_text(text,kind)
            expected=visits.stamp(self.game.state_data)
        except ValueError as exc:self.status.configure(text=str(exc));return
        snapshot=copy.deepcopy(self.game.state_data);job=object();self.job=job
        self.working(True);self.status.configure(text='Writing a memory response…')
        results=self.results
        def work():
            try:results.put((job,expected,text,kind,visits.generate(snapshot,text,kind),None))
            except Exception as exc:results.put((job,expected,text,kind,None,str(exc)))
        threading.Thread(target=work,daemon=True).start()

    def poll(self):
        if self.closed:return
        try:
            while True:
                job,expected,text,kind,data,error=self.results.get_nowait()
                if job is not self.job:continue
                self.job=None;self.working(False)
                if error:self.status.configure(text='Could not write the response. Retry your message.');continue
                try:visits.commit(self.game.state_data,expected,text,kind,data)
                except ValueError as exc:self.status.configure(text=str(exc));continue
                self.entry.delete(0,'end');self.refresh();self.game.persist()
                self.status.configure(text='Memory saved · No present-day time passed.')
        except queue.Empty:pass
        self.poll_id=self.after(80,self.poll)

    def cancel_reply(self):
        self.job=None;self.working(False)
        self.status.configure(text='Response cancelled. Your message has not been committed.')

    def journal(self):
        self.stop_fox_voice()
        if self.journal_view is not None:
            self.journal_view.lift();return
        panel=self.journal_view=tk.Frame(self,bg=ui.PANEL,padx=12,pady=12)
        header=tk.Frame(panel,bg=ui.PANEL);header.pack(fill='x',pady=(0,8))
        ttk.Label(header,text='Memory journal',font=('Segoe UI',14,'bold')).pack(side='left')
        ttk.Button(header,text='Back to the memory',command=self.close_journal).pack(side='right')
        body=tk.Frame(panel,bg=ui.PANEL);body.pack(fill='both',expand=True)
        text=tk.Text(body,bg=ui.INK,fg=ui.CREAM,insertbackground=ui.CREAM,wrap='word',relief='flat',padx=12,pady=12)
        scroll=ttk.Scrollbar(body,command=text.yview);scroll.pack(side='right',fill='y')
        text.configure(yscrollcommand=scroll.set);text.pack(fill='both',expand=True)
        history=visits.record(self.game.state_data)['history']
        if not history:text.insert('end','Your conversations in this memory will appear here.')
        for row in history:
            text.insert('end',('You: ' if row['kind']=='speak' else 'Your action: ')+row['text']+'\n')
            text.insert('end',row['response']['narration']+'\n')
            for line in row['response']['lines']:text.insert('end',visits.name(line['speaker'])+': '+line['text']+'\n')
            text.insert('end','\n')
        text.configure(state='disabled')
        phone_theme.apply_tree(panel)
        panel.place(x=0,y=0,relwidth=1,relheight=1);panel.lift();panel.grab_set();text.focus_set()

    def close_journal(self):
        if self.journal_view is None:return
        self.journal_view.destroy();self.journal_view=None
        self.grab_set();self.entry.focus_set()

    def escape(self):
        if self.journal_view is not None:self.close_journal()
        else:self.leave()

    def destroy(self):
        self.closed=True;self.job=None
        if self.poll_id is not None:
            self.after_cancel(self.poll_id);self.poll_id=None
        if self.grab_current() in (self,self.journal_view):self.grab_release()
        if getattr(self.game,'flashback_view',None) is self:self.game.flashback_view=None
        super().destroy()

    def leave(self):
        if self.closed:return
        visits.leave(self.game.state_data)
        self.game.simulation_clock.reset(self.game.state_data)
        self.destroy()
        self.game.persist();self.game.render()
        self.game.focus_set()


class FlashbackHangoutCanvas(HangoutCanvas):
    def page(self,kind,text,width,lines,font):
        # Keep enlarged text inside the fixed in-person narration strip and
        # speech bubbles. The shared canvas still supplies the page controls.
        if int(font.actual()['size'])>=20:lines=1
        return super().page(kind,text,width,lines,font)


class MemoryStage(tk.Frame):
    def __init__(self,parent,game):
        super().__init__(parent,bg=ui.INK)
        self.canvas=FlashbackHangoutCanvas(self,game);self.canvas.controls_height=0
        self.canvas.pack(fill='both',expand=True)

    def position_controls(self):pass
    def update_voice_controls(self):pass

class FlashbackReferenceError(tk.Frame):
    """A saved visit with missing guidance always retains a safe in-person exit."""
    def __init__(self,parent,game,message):
        super().__init__(parent,bg=ui.INK,padx=18,pady=18)
        self.game=game;self.state=game.state_data;self.closed=False;self.busy=False
        ttk.Label(self,text='Historical references unavailable',font=('Segoe UI',16,'bold')).pack(anchor='w',pady=8)
        label=ttk.Label(self,text=message+' The saved historical visit and present-day state are preserved. Return safely; no adult profile will be substituted.',wraplength=640,justify='left');label.pack(fill='x',pady=8)
        label.bind('<Configure>',lambda e:label.configure(wraplength=max(100,e.width-10)))
        ttk.Button(self,text='Return to the present',command=self.leave).pack(anchor='w',pady=8)
        self.bind('<Escape>',lambda e:self.leave());phone_theme.apply_tree(self)
    def leave(self):
        if self.closed:return
        visits.leave(self.game.state_data);self.game.simulation_clock.reset(self.game.state_data)
        self.destroy();self.game.persist();self.game.render();self.game.focus_set()
    def escape(self):self.leave()
    def destroy(self):
        self.closed=True
        if getattr(self.game,'flashback_view',None) is self:self.game.flashback_view=None
        super().destroy()


