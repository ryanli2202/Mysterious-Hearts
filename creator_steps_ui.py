"""Staged editing and read-only live review; no story initialisation or AI."""
import tkinter as tk
from tkinter import ttk
import winterfield_ui as ui

STEPS = ('Identity & Appearance', 'Backstory', 'Combat', 'Career', 'Underworld', 'Review')
HELP = {
    STEPS[0]: 'Choose adult identity, appearance and home. Appearance changes require a matching portrait before saving a playable character.',
    'Backstory': 'Optional writing prompts describe the past and aspirations. They do not grant employment, powers, friendships or completed missions.',
    'Combat': 'Awakening is the ability to use mana. A Trait is a distinct power; amplification options require explicit review. Starting kits determine actual Path stage and learned techniques.',
    'Career': 'Descriptive occupation is biography. The starting-choice picker separately grants supported employment, title, hours and pay for a new story only.',
    'Underworld': 'Choose an approved starting background and organisation in the picker. Narrative history alone grants no authority or membership. Existing story progress is never reseeded.',
    'Review': 'Check the resolved starting profile and completion requirements. Save character updates the reusable library; Save & begin explicitly starts a new story.',
}


class Steps:
    def setup_steps(self, form, heading, right):
        self.creator_step = STEPS[0]
        self.step_widgets = {name: [] for name in STEPS}
        # Preserve widget instances, values, focus order and their grid options.
        for widget in form.winfo_children():
            row = int(widget.grid_info()['row'])
            stage = ('Career' if row == 7 else 'Combat' if 13 <= row <= 20 else
                     'Identity & Appearance' if row < 13 or 21 <= row <= 26 else 'Backstory')
            self.step_widgets[stage].append(widget)
        self.step_choice = tk.StringVar(value=self.creator_step)
        nav = ttk.Frame(heading); nav.pack(fill='x', pady=(6, 0))
        self.back_step = ttk.Button(nav, text='Back', command=lambda:self.move_step(-1)); self.back_step.pack(side='left')
        self.step_picker = ttk.Combobox(nav, textvariable=self.step_choice, values=STEPS, state='readonly', width=26)
        self.step_picker.pack(side='left', padx=8)
        self.step_picker.bind('<<ComboboxSelected>>', lambda e:self.show_step(self.step_choice.get()))
        self.next_step = ttk.Button(nav, text='Next', command=lambda:self.move_step(1)); self.next_step.pack(side='left')
        self.step_count = ttk.Label(nav); self.step_count.pack(side='left', padx=10)
        self.step_help = ttk.Label(form, wraplength=440, style='Muted.TLabel')
        self.step_help.grid(row=0, column=0, columnspan=2, sticky='ew', pady=(0, 12))
        # Shift existing rows once to keep contextual help above the current page.
        for widgets in self.step_widgets.values():
            for widget in widgets: widget.grid_configure(row=int(widget.grid_info()['row'])+1)
        for stage in ('Career', 'Underworld'):
            frame = ttk.Frame(form, padding=8); frame.grid(row=2, column=0, columnspan=2, sticky='ew')
            summary = ttk.Label(frame, wraplength=420, justify='left'); summary.pack(fill='x', pady=10)
            setattr(self, stage.lower()+'_summary', summary)
            ttk.Button(frame, text='Choose '+stage.lower()+' starting choices',
                       command=lambda:__import__('creator_origin_ui').open_picker(self)).pack(anchor='w')
            self.step_widgets[stage].append(frame)
        self.checklist = tk.Text(form, height=16, width=1, wrap='word', bg=ui.CARD, fg=ui.CREAM,
                                 insertbackground=ui.CREAM, relief='flat', font=('Segoe UI', 10))
        self.checklist.grid(row=2, column=0, columnspan=2, sticky='ew')
        self.step_widgets['Review'].append(self.checklist)
        full = ttk.Button(form, text='Open full starting dossier', command=self.review_character)
        full.grid(row=3, column=0, columnspan=2, sticky='ew', pady=8); self.step_widgets['Review'].append(full)
        fix=ttk.Button(form,text='Go to first required field',command=self.focus_issue)
        fix.grid(row=4,column=0,columnspan=2,sticky='ew',pady=6); self.step_widgets['Review'].append(fix)
        live = ttk.Frame(self.preview_tabs)
        self.preview_tabs.add(live, text='Live starting profile')
        scroll = ttk.Scrollbar(live); scroll.pack(side='right', fill='y')
        self.live_preview = tk.Text(live, height=8, width=1, wrap='word', bg=ui.CARD, fg=ui.CREAM,
                                    relief='flat', font=('Segoe UI', 10), yscrollcommand=scroll.set)
        self.live_preview.pack(fill='both', expand=True); scroll.configure(command=self.live_preview.yview)
        self.show_step(self.creator_step)
        self.bind('<Alt-Left>', lambda e:self.move_step(-1))
        self.bind('<Alt-Right>', lambda e:self.move_step(1))

    def move_step(self, offset):
        self.show_step(STEPS[max(0, min(len(STEPS)-1, STEPS.index(self.creator_step)+offset))])

    def show_step(self, stage):
        if stage not in STEPS: stage = STEPS[0]
        self.creator_step = stage; self.step_choice.set(stage)
        for name, widgets in self.step_widgets.items():
            for widget in widgets:
                if name == stage: widget.grid()
                else: widget.grid_remove()
        self.step_help.configure(text=HELP[stage])
        index = STEPS.index(stage)
        self.back_step.configure(state='disabled' if index==0 else 'normal')
        self.next_step.configure(state='disabled' if index==len(STEPS)-1 else 'normal')
        self.step_count.configure(text=f'{index+1} / {len(STEPS)}')
        self.form_canvas.yview_moveto(0)
        self.refresh_live_review()

    def refresh_live_review(self):
        if not hasattr(self, 'live_preview'): return
        import character_origins
        import character_dossier
        checks = []
        self.first_issue=None
        try:
            p = self.collect()
            d = character_dossier.starting('custom_preview', p | {'portrait':self.portrait or ''})
            checks.append('Ready: character fields and starting choices are valid.')
            text = d['name']+'\n'+character_dossier.text(d, 'Details')
        except (ValueError, KeyError) as exc:
            self.first_issue=str(exc)
            checks.append('Needs attention: '+str(exc))
            text = (self.values['name'].get() or 'Untitled character')+'\n\n'+str(exc)+'\n\nIncomplete drafts can always be saved.'
        portrait_ready = bool(self.portrait and self.signature()==self.generated_signature)
        if not self.first_issue and not portrait_ready: self.first_issue='appearance portrait'
        if not self.first_issue and self.needs_trait() and not self.trait_ready(): self.first_issue='awakening trait'
        checks.append(('Ready: matching portrait.' if portrait_ready else 'Needs attention: generate a portrait matching the current appearance.'))
        checks.append('Ready: unawakened start.' if not self.awakened.get() else
                      'Ready: awakened without a named Trait.' if not self.needs_trait() else
                      'Ready: Trait options accepted.' if self.trait_ready() else 'Needs attention: evaluate and accept this Trait in Combat.')
        if self.cancel_event: checks.append('Needs attention: finish or cancel generation.')
        checks += ['Optional: biography, hometown, goals, private history, preferred address and pronunciation.',
                   'Saving a reusable profile never edits an existing story.',
                   'Appearance edits do not silently generate artwork.']
        for widget, value in ((self.live_preview, text), (self.checklist, '\n\n'.join(checks))):
            widget.configure(state='normal'); widget.delete('1.0','end'); widget.insert('end', value); widget.configure(state='disabled')
        try:
            resolved = character_origins.resolve(self.origin, self.awakened.get(), self.needs_trait() and bool(self.current_trait()[0]))
            job = resolved['employment']
            self.career_summary.configure(text=(f"{job['title']}\n{job['venue']}\nPay {job['pay']} · hours {job['hours'][0]}–{job['hours'][1]}" if job else 'Looking for work · no starting employment.')+'\n\nDescriptive occupation: '+self.values['occupation'].get())
            self.underworld_summary.configure(text=self.origin['crime']+'\nOrganisation: '+str(self.origin.get('organisation') or 'None')+f"\nReputation {resolved['reputation']} · heat {resolved['heat']}\n\nNo completed contracts, shifts or friendships are awarded.")
        except ValueError as exc:
            self.career_summary.configure(text=str(exc)); self.underworld_summary.configure(text=str(exc))

    def focus_issue(self):
        issue=(getattr(self,'first_issue',None) or '').lower()
        if not issue: return
        if any(word in issue for word in ('trait','awakening','signature','specialisation','martial','technique')):
            stage='Combat'; widget=self.awakening_trait
        elif 'occupation' in issue:
            stage='Career'; widget=self.field_controls['occupation']
        else:
            stage='Identity & Appearance'; widget=self.appearance
            for key,control in self.field_controls.items():
                if key in issue: widget=control; break
        self.show_step(stage); widget.focus_set()
        self.form_canvas.update_idletasks()
        y=widget.winfo_y(); total=max(1,widget.master.winfo_reqheight())
        self.form_canvas.yview_moveto(max(0,y-30)/total)
