"""Flashback visits embedded in the main in-person window."""
import copy
import queue
import threading
import tkinter as tk
from tkinter import ttk
import flashback_visits as visits
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
        area=visits.AREAS[visits.active(game.state_data)['area']]
        header=tk.Frame(self,bg=ui.PANEL,padx=12,pady=9);header.pack(fill='x')
        ttk.Button(header,text='Return to the present',command=self.leave).pack(side='right')
        ttk.Label(header,text=area['title'],font=('Segoe UI',14,'bold')).pack(anchor='w')
        ttk.Label(header,text='Past selves · Time is paused · Conversations stay in this memory').pack(anchor='w')
        cast=tk.Frame(self,bg=ui.PANEL,padx=12,pady=5);cast.pack(fill='x')
        self.selections={};self.change_controls=[]
        for who in visits.available(game.state_data):
            var=tk.BooleanVar(value=who in visits.active(game.state_data)['members']);self.selections[who]=var
            button=ttk.Checkbutton(cast,text=visits.name(who),variable=var)
            button.pack(side='left',padx=(0,10));self.change_controls.append(button)
        choose=ttk.Button(cast,text='Hang out with selected',command=self.select)
        choose.pack(side='left');self.change_controls.append(choose)
        ttk.Button(cast,text='Memory journal',command=self.journal).pack(side='right')
        self.stage=MemoryStage(self,game);self.stage.pack(fill='both',expand=True)
        self.canvas=self.stage.canvas
        controls=tk.Frame(self,bg=ui.PANEL,padx=12,pady=8);controls.pack(fill='x')
        voice=tk.Frame(controls,bg=ui.PANEL);voice.pack(fill='x')
        ttk.Button(voice,text='‹ Speaker',command=lambda:self.canvas.turn_speaker(-1)).pack(side='left')
        ttk.Button(voice,text='Speaker ›',command=lambda:self.canvas.turn_speaker(1)).pack(side='left',padx=4)
        self.status=ttk.Label(voice,text='Choose a friend, say something, or spend time together.');self.status.pack(side='left',padx=8)
        actions=tk.Frame(controls,bg=ui.PANEL);actions.pack(fill='x',pady=5)
        for i,text in enumerate(area['activities']):
            button=ttk.Button(actions,text=text,command=lambda text=text:self.submit(text,'action'))
            button.grid(row=i//2,column=i%2,sticky='ew',padx=2,pady=2);self.change_controls.append(button)
        actions.columnconfigure((0,1),weight=1)
        compose=tk.Frame(controls,bg=ui.PANEL);compose.pack(fill='x')
        self.entry=tk.Entry(compose,bg=ui.CARD,fg=ui.CREAM,insertbackground=ui.CREAM,
            disabledbackground=ui.PANEL,disabledforeground=ui.MUTED,relief='flat',font=('Segoe UI',12))
        self.entry.pack(side='left',fill='x',expand=True,ipady=5)
        self.entry.bind('<Return>',lambda event:self.submit(self.entry.get(),'speak'))
        for title,kind in (('Say','speak'),('Do action · no time','action')):
            button=ttk.Button(compose,text=title,command=lambda kind=kind:self.submit(self.entry.get(),kind))
            button.pack(side='left',padx=4);self.change_controls.append(button)
        self.cancel=ttk.Button(compose,text='Cancel',command=self.cancel_reply,state='disabled');self.cancel.pack(side='left')
        phone_theme.apply_tree(self)
        self.refresh()
        self.poll_id=self.after(80,self.poll)

    def refresh(self):
        s=self.game.state_data;visit=visits.active(s)
        if not visit:return
        exchange=visits.record(s)['exchange']
        self.canvas.members=list(visit['members'])
        self.canvas.exchange=Exchange(player=exchange['player'],narration=exchange['narration'],
            speeches=[(row['speaker'],row['text']) for row in exchange['lines']])
        self.canvas.artwork=visits.AREAS[visit['area']]['background']
        self.canvas.speech_index=0;self.canvas.page_indices=dict.fromkeys(self.canvas.page_indices,0)
        self.canvas.redraw()

    def working(self,value):
        self.busy=value
        for control in self.change_controls:control.configure(state='disabled' if value else 'normal')
        self.entry.configure(state='disabled' if value else 'normal')
        self.cancel.configure(state='normal' if value else 'disabled')

    def select(self):
        if self.busy:return
        try:visits.select(self.game.state_data,[who for who,var in self.selections.items() if var.get()])
        except ValueError as exc:self.status.configure(text=str(exc));return
        self.refresh();self.game.persist();self.status.configure(text='Your selected friends are here. Time stays paused.')

    def submit(self,text,kind):
        if self.busy:return
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


class MemoryStage(tk.Frame):
    def __init__(self,parent,game):
        super().__init__(parent,bg=ui.INK)
        self.canvas=HangoutCanvas(self,game);self.canvas.controls_height=0
        self.canvas.pack(fill='both',expand=True)

    def position_controls(self):pass
    def update_voice_controls(self):pass
