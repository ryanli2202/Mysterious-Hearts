"""Draft lifecycle controls shared by the existing portrait/Trait creator."""
import copy
import json
import tkinter as tk
from tkinter import ttk
from PIL import Image
import creator_drafts as drafts
import custom_protagonist as custom
import phone_theme
from phone_dialogs import AppWindow
import winterfield_ui as ui


class Workspace:
    def setup_workspace(self, form, heading):
        import game_core as core
        self.draft_root = core.SAVE.parent.parent / 'character_drafts'
        self.draft = drafts.new()
        self.undo_stack = drafts.Undo()
        self.workspace_epoch = 0
        self.workspace_loading = False
        self.edit_profile_id = None
        self.edit_profile_baseline = None
        self.extra_text = {}
        self.writing = {}
        self.identity = {}
        self.specialisation = ''
        self.starting_signature = None
        self.import_provenance = None
        import character_origins
        self.origin = character_origins.validate({})
        toolbar = ttk.Frame(heading); toolbar.pack(fill='x', pady=6)
        for title, action in (('Save draft', self.save_draft), ('Resume draft', self.draft_browser),
                              ('Revision history', self.history_browser), ('Undo', self.undo_edit),
                              ('Redo', self.redo_edit), ('Review', self.review_character)):
            ttk.Button(toolbar, text=title, command=action).pack(side='left', padx=(0, 5))
        self.draft_status = ttk.Label(heading, text='Unsaved draft · incomplete fields are welcome', style='Muted.TLabel')
        self.draft_status.pack(anchor='w')
        ttk.Button(heading, text='Save draft as copy', command=self.save_draft_copy).pack(anchor='e')
        ttk.Button(heading, text='Choose career, criminal background & combat kit',
                   command=lambda:__import__('creator_origin_ui').open_picker(self)).pack(anchor='w')
        self.origin_summary = ttk.Label(heading, text='Newcomer · Looking for work · Clean slate', style='Muted.TLabel')
        self.origin_summary.pack(anchor='w')
        advanced=ttk.Frame(heading); advanced.pack(fill='x')
        ttk.Button(advanced, text='Writing, identity & packages',
                   command=lambda:__import__('creator_tools_ui').open_tools(self)).pack(side='left')
        ttk.Button(advanced, text='Trait builder & practice',
                   command=lambda:__import__('creator_combat_ui').open_review(self)).pack(side='left',padx=8)
        row = 21
        for key, title, prompt in (
            ('preferred_name', 'Preferred address · optional', 'Leave blank to use your full name.'),
            ('pronunciation', 'Pronunciation · optional', 'Guidance for dialogue; this does not add a speech engine.'),
            ('hometown', 'Hometown · optional', 'Where did you grow up? Unanswered prompts are not character facts.'),
            ('biography', 'Public biography · optional', 'Describe past work, formative events and why you moved. This text does not grant jobs, powers or local acquaintances.'),
            ('motivation', 'Motivations and goals · optional', 'What would you like to work toward? Goals are not completed achievements.'),
            ('private_history', 'Private history · optional', 'Stored for your own dossier; never included in public biography or ordinary NPC context.')):
            ttk.Label(form, text=title, style='Section.TLabel').grid(row=row, column=0, columnspan=2, sticky='w', pady=(16, 4))
            ttk.Label(form, text=prompt, wraplength=410, style='Muted.TLabel').grid(row=row+1, column=0, columnspan=2, sticky='w')
            widget = tk.Text(form, height=3 if key in ('biography', 'motivation', 'private_history') else 2,
                             bg=ui.CARD, fg=ui.CREAM, insertbackground=ui.CREAM,
                             selectbackground=ui.EDGE, wrap='word', relief='flat', font=('Segoe UI', 10), undo=True)
            widget.grid(row=row+2, column=0, columnspan=2, sticky='ew', pady=5)
            self.extra_text[key] = widget
            self.controls.append((widget, 'normal'))
            row += 3
        self.last_snapshot = self.snapshot()
        self.undo_stack.record(self.last_snapshot)
        self.workspace_timer = self.after(1200, self.workspace_tick)

    def snapshot(self):
        return dict(origin=copy.deepcopy(self.origin), writing=copy.deepcopy(self.writing), identity=copy.deepcopy(self.identity),
                    import_provenance=copy.deepcopy(self.import_provenance),
                    specialisation=self.specialisation,starting_signature=copy.deepcopy(self.starting_signature),values={k:v.get() for k,v in self.values.items()}, home_choice=self.home_choice.get(),
                    creator_step=getattr(self,'creator_step','Identity & Appearance'),
                    edit_profile_id=self.edit_profile_id, edit_profile_baseline=self.edit_profile_baseline,
                    appearance=self.appearance.get('1.0','end-1c'), awakened=self.awakened.get(),trait_enabled=self.trait_enabled.get(),mana_potential=self.mana_potential.get(),
                    awakening_description=self.awakening_description.get('1.0','end-1c'),
                    extra={k:w.get('1.0','end-1c') for k,w in self.extra_text.items()},
                    portrait=self.portrait, generated_signature=self.generated_signature,
                    trait_signature=self.trait_signature, trait_amplifications=copy.deepcopy(self.trait_amplifications),
                    previous_trait_amplifications=copy.deepcopy(self.previous_trait_amplifications),
                    trait_reviewed=self.trait_reviewed.get(), step=self.form_canvas.yview()[0])

    def workspace_tick(self):
        if self.closed: return
        snapshot = self.snapshot()
        self.refresh_live_review()
        # Scrolling alone is not a text edit or an undo checkpoint.
        previous = dict(self.last_snapshot); previous['step'] = snapshot['step']
        if not self.workspace_loading and snapshot != previous:
            content_previous=dict(previous); content_previous['creator_step']=snapshot['creator_step']
            if snapshot!=content_previous:
                self.undo_stack.record(self.last_snapshot)
                self.workspace_epoch += 1
            self.last_snapshot = copy.deepcopy(snapshot)
            self.draft_status.configure(text='Saving recovery copy…')
            try:
                self.draft = drafts.autosave(self.draft_root, self.draft, snapshot)
                self.draft_status.configure(text='Recovery copy saved · use Save draft for a revision')
            except (OSError, ValueError) as exc:
                self.draft_status.configure(text='Save failed · changes remain open: ' + str(exc))
        self.workspace_timer = self.after(1200, self.workspace_tick)

    def request_stamp(self):
        """Flush edits before capturing an asynchronous request's revision."""
        import creator_writing
        snap=self.snapshot()
        previous=dict(self.last_snapshot)
        for key in ('step','creator_step'): previous[key]=snap[key]
        if previous!=snap:
            self.undo_stack.record(self.last_snapshot); self.workspace_epoch+=1
        self.draft=drafts.autosave(self.draft_root,self.draft,snap)
        self.last_snapshot=copy.deepcopy(snap)
        return creator_writing.token(snap,self.draft['id'],self.workspace_epoch)

    def save_draft(self):
        try:
            self.draft = drafts.save(self.draft_root, self.draft, self.snapshot())
            self.draft_status.configure(text='Draft saved · ' + self.draft['updated'])
            return True
        except (OSError, ValueError) as exc:
            self.draft_status.configure(text='Save failed · previous draft preserved: ' + str(exc))
            return False

    def save_draft_copy(self):
        try:
            self.draft = drafts.save(self.draft_root, drafts.new(), self.snapshot(), 'Independent draft copy')
            self.draft_status.configure(text='Saved an independent draft copy; the original is preserved.')
            return True
        except (OSError, ValueError) as exc:
            self.draft_status.configure(text='Could not save draft copy: '+str(exc)); return False

    def restore_snapshot(self, snapshot):
        if self.cancel_event:
            self.status.configure(text='Cancel or finish the current generation before restoring a draft.')
            return False
        self.workspace_loading = True
        self.workspace_epoch += 1
        try:
            import character_origins
            self.origin = character_origins.validate(snapshot.get('origin', {}))
            self.writing = copy.deepcopy(snapshot.get('writing', {}))
            self.identity = __import__('character_identity').validate(snapshot.get('identity', {}))
            self.specialisation = snapshot.get('specialisation','')
            self.starting_signature = copy.deepcopy(snapshot.get('starting_signature'))
            self.import_provenance = copy.deepcopy(snapshot.get('import_provenance'))
            self.edit_profile_id = snapshot.get('edit_profile_id')
            self.edit_profile_baseline = snapshot.get('edit_profile_baseline')
            self.origin_summary.configure(text=self.origin['experience']+' · '+self.origin['crime'])
            for key, var in self.values.items(): var.set(snapshot.get('values', {}).get(key, ''))
            home = snapshot.get('home_choice')
            if home in self.home_labels: self.home_choice.set(home)
            self.awakened.set(bool(snapshot.get('awakened')))
            self.trait_enabled.set(snapshot.get('trait_enabled',True))
            self.mana_potential.set(snapshot.get('mana_potential',True))
            self.update_awakening()
            for widget, value in ((self.appearance, snapshot.get('appearance','')),
                                  (self.awakening_description, snapshot.get('awakening_description','')),
                                  *((w,snapshot.get('extra',{}).get(k,'')) for k,w in self.extra_text.items())):
                widget.configure(state='normal'); widget.delete('1.0','end'); widget.insert('1.0', value)
                widget.edit_modified(False)
            self.trait_signature = tuple(snapshot['trait_signature']) if snapshot.get('trait_signature') else None
            self.trait_amplifications = copy.deepcopy(snapshot.get('trait_amplifications', []))
            self.previous_trait_amplifications = copy.deepcopy(snapshot.get('previous_trait_amplifications', []))
            self.trait_reviewed.set(bool(snapshot.get('trait_reviewed')) and self.trait_signature == self.current_trait())
            if self.trait_amplifications:
                try:
                    from combat_workshop import validate_amplifications
                    self.trait_amplifications = validate_amplifications(self.trait_amplifications)
                except ValueError:
                    self.trait_amplifications = []; self.trait_reviewed.set(False)
            self.portrait = snapshot.get('portrait')
            self.generated_signature = tuple(snapshot['generated_signature']) if snapshot.get('generated_signature') else None
            self.source = None; self.canvas.delete('all')
            if self.portrait:
                try:
                    path = custom.portrait_path({'portrait':self.portrait})
                    with Image.open(path) as source: self.source = source.convert('RGBA')
                    self.redraw()
                except (OSError, ValueError):
                    self.portrait = None
                    self.status.configure(text='Draft restored, but its portrait is missing. Generate a replacement explicitly.')
            self.update_awakening()
            self.trait_review.configure(text='Restored reviewed Trait options.' if self.trait_ready() else 'Evaluate and accept the current Trait before completion.')
            self.last_snapshot = self.snapshot()
            self.form_canvas.yview_moveto(snapshot.get('step', 0))
        finally:
            self.workspace_loading = False
        if hasattr(self, 'show_step') and hasattr(self, 'step_widgets'):
            self.show_step(snapshot.get('creator_step', 'Identity & Appearance'))
            self.form_canvas.yview_moveto(snapshot.get('step', 0))
        return True

    def edit_profile(self, raw):
        """Open a new independent draft linked to one reusable profile revision."""
        import custom_library
        profile = custom_library.normalise(raw)
        self.edit_profile_id = profile['profile_id']
        self.edit_profile_baseline = custom_library.fingerprint(profile)
        snap = self.snapshot()
        snap['values'].update({k:(', '.join(profile[k]) if isinstance(profile[k], list) else str(profile[k]))
                               for k in self.values if k in profile})
        snap.update(appearance=profile['appearance'], awakened=profile['awakened'],
                    trait_enabled=profile.get('trait_enabled',True),
                    mana_potential=profile.get('mana_potential',True),
                    awakening_description=profile.get('awakening_description',''),
                    origin=profile.get('origin',{}), portrait=profile['portrait'],
                    home_choice=next(k for k,v in self.home_labels.items() if v==profile['home']),
                    extra={k:profile.get(k,'') for k in self.extra_text},
                    identity=profile.get('identity',{}),
                    specialisation=profile.get('specialisation',''),starting_signature=profile.get('starting_signature'),
                    import_provenance=profile.get('import_provenance'),
                    generated_signature=[str(profile[k]) for k in ('gender','age','height','hairstyle')]+[profile['appearance']],
                    trait_signature=[profile.get('awakening_trait',''),profile.get('awakening_description','')],
                    trait_amplifications=profile.get('trait_amplifications',[]),
                    trait_reviewed=bool(profile.get('trait_amplifications')))
        self.restore_snapshot(snap)
        self.undo_stack = drafts.Undo(); self.last_snapshot = self.snapshot()
        self.title('Edit reusable character · '+profile['name'])
        self.status.configure(text='Editing a library profile. Save character updates this profile only; existing stories keep their own snapshots.')

    def undo_edit(self):
        if not self.cancel_event:
            self.restore_snapshot(self.undo_stack.undo(self.snapshot()))
            self.recover_restored()

    def redo_edit(self):
        if not self.cancel_event:
            self.restore_snapshot(self.undo_stack.redo(self.snapshot()))
            self.recover_restored()

    def recover_restored(self):
        try: self.draft=drafts.autosave(self.draft_root,self.draft,self.snapshot())
        except (OSError,ValueError) as exc: self.draft_status.configure(text='Recovery save failed; restored text remains open: '+str(exc))

    def workspace_window(self, title):
        window = AppWindow(self)
        window.title(title); window.geometry('780x600'); window.configure(bg=ui.INK)
        return window

    def draft_browser(self):
        if self.cancel_event:
            self.status.configure(text='Finish or cancel generation before switching drafts.'); return
        window = self.workspace_window('Drafts · never playable until saved as a character')
        records, errors = drafts.listing(self.draft_root)
        listing = tk.Listbox(window, bg=ui.PANEL, fg=ui.CREAM, selectbackground=ui.EDGE,
                             selectforeground=ui.CREAM, exportselection=False, font=('Segoe UI',11))
        listing.pack(fill='both', expand=True, padx=14, pady=14)
        for doc in records:
            snap = drafts.recovery(doc) or doc['current']
            listing.insert('end', (snap.get('values',{}).get('name') or 'Untitled')+' · '+doc['id'][:8]+' · '+doc['updated'])
        status = ttk.Label(window, text='Choose Manual revision or Recovery copy. Switching saves your current draft first.\n'+'\n'.join(errors), wraplength=720)
        status.pack(fill='x', padx=14)
        preview_frame = ttk.Frame(window); preview_frame.pack(fill='x', padx=14, pady=8)
        preview_scroll = ttk.Scrollbar(preview_frame); preview_scroll.pack(side='right', fill='y')
        preview = tk.Text(preview_frame, height=9, wrap='word', bg=ui.CARD, fg=ui.CREAM, relief='flat', yscrollcommand=preview_scroll.set)
        preview.pack(fill='x'); preview_scroll.configure(command=preview.yview)
        def show(*_):
            if not listing.curselection(): return
            doc = records[listing.curselection()[0]]
            manual, recovery = doc['current'], drafts.recovery(doc)
            sections = []
            for title, snap in (('Manual revision', manual), ('Recovery copy', recovery)):
                if not snap:
                    sections.append(title+': unavailable'); continue
                sections.append(title+'\n'+(snap.get('values',{}).get('name') or 'Untitled')+
                                '\nStep: '+snap.get('creator_step','Identity & Appearance')+
                                '\nOccupation: '+snap.get('values',{}).get('occupation','')+
                                '\nBiography: '+snap.get('extra',{}).get('biography','')[:300])
            if recovery:
                changed = sorted(k.replace('_',' ') for k in set(manual)|set(recovery) if manual.get(k)!=recovery.get(k))
                sections.append('Recovery differs in: '+', '.join(changed))
            preview.configure(state='normal'); preview.delete('1.0','end'); preview.insert('end','\n\n'.join(sections)); preview.configure(state='disabled')
        listing.bind('<<ListboxSelect>>', show)
        if records: listing.selection_set(0); show()
        def resume(recovery=False):
            if not listing.curselection(): return
            doc = records[listing.curselection()[0]]
            snapshot = drafts.recovery(doc) if recovery else doc['current']
            if not snapshot:
                status.configure(text='No '+('recovery copy' if recovery else 'manual revision')+' is available.'); return
            # Avoid replacing an unsaved working document with the browser snapshot.
            if not self.save_draft(): return
            try:
                # Re-read after saving the current editor: the selection may be
                # this same draft, or another window may have updated it.
                latest = drafts.read(self.draft_root, doc['id'])
                if doc['id'] != self.draft['id'] and latest != doc:
                    status.configure(text='This draft changed while the browser was open. Close and reopen Resume draft to review the latest copies.'); return
                self.draft = drafts.save(self.draft_root, latest, snapshot, 'Resume recovery' if recovery else 'Resume manual revision')
            except (OSError, ValueError) as exc:
                status.configure(text='Could not resume: '+str(exc)); return
            self.undo_stack = drafts.Undo()
            self.restore_snapshot(snapshot); window.destroy()
        ttk.Button(window, text='Resume manual revision', command=lambda:resume(False)).pack(side='left', padx=14, pady=14)
        ttk.Button(window, text='Resume recovery copy', command=lambda:resume(True)).pack(side='left', padx=14, pady=14)
        phone_theme.apply_tree(window)

    def history_browser(self):
        window = self.workspace_window('Draft revisions · restore is reversible')
        records = list(reversed(self.draft['revisions']))
        listing = tk.Listbox(window, bg=ui.PANEL, fg=ui.CREAM, selectbackground=ui.EDGE, selectforeground=ui.CREAM, exportselection=False)
        listing.pack(fill='x', padx=14, pady=14)
        body = ttk.Frame(window); body.pack(fill='both', expand=True, padx=14)
        scroll = ttk.Scrollbar(body); scroll.pack(side='right', fill='y')
        preview = tk.Text(body, bg=ui.CARD, fg=ui.CREAM, wrap='word', height=14, yscrollcommand=scroll.set)
        preview.pack(fill='both', expand=True); scroll.configure(command=preview.yview)
        def revision_label(r):
            return ('[Pinned] ' if r.get('pinned') else '') + r['at']+' · '+r['label']
        for r in records: listing.insert('end', revision_label(r))
        def show(*_):
            if not listing.curselection(): return
            snap = records[listing.curselection()[0]]['snapshot']
            current = self.snapshot()
            changed = [key for key in set(snap)|set(current) if snap.get(key)!=current.get(key)]
            preview.configure(state='normal'); preview.delete('1.0','end')
            labels = {'values':'Identity', 'extra':'Background and address', 'origin':'Starting choices',
                      'appearance':'Appearance', 'awakened':'Awakening', 'awakening_description':'Trait description',
                      'trait_signature':'Trait review', 'trait_amplifications':'Trait options',
                      'trait_reviewed':'Trait acceptance', 'portrait':'Portrait', 'generated_signature':'Portrait compatibility', 'step':'Editor position'}
            lines = ['Changed sections: '+(', '.join(dict.fromkeys(labels.get(k,k.replace('_',' ').title()) for k in changed)) or 'No changes'), '']
            lines += [k.replace('_',' ').title()+': '+str(v) for k,v in snap.get('values',{}).items() if k!='home']
            lines += ['Home: '+snap.get('home_choice','Unspecified'), '\nAppearance\n'+snap.get('appearance','')]
            lines += ['\n'+k.replace('_',' ').title()+'\n'+v for k,v in snap.get('extra',{}).items() if v]
            o=snap.get('origin',{})
            import job_apps, combat_moves
            job=job_apps.JOBS.get(o.get('job'))
            lines += ['\nStarting choices', 'Combat history: '+o.get('experience','Newcomer'),
                      'Employment: '+(job['ranks'][o.get('job_rank',0)] if job else 'Looking for work'),
                      'Criminal background: '+o.get('crime','Clean slate'),
                      'Martial arts: '+(', '.join(o.get('arts',[])) or 'None'),
                      'Chosen techniques: '+(', '.join(combat_moves.MOVES[m]['name'] for m in o.get('moves',[]) if m in combat_moves.MOVES) or 'Utilities / basic techniques only'),
                      '\nTrait description\n'+snap.get('awakening_description',''),
                      'Trait review: '+('Accepted for the saved inputs; revalidated on restore.' if snap.get('trait_reviewed') else 'Not accepted.'),
                      'Portrait: '+('Saved reference; checked on restore.' if snap.get('portrait') else 'Not generated.')]
            preview.insert('end', '\n'.join(lines))
            preview.configure(state='disabled')
        listing.bind('<<ListboxSelect>>', show)
        if records:
            listing.selection_set(0); show()
        status = ttk.Label(window, text='Keeps 40 ordinary checkpoints plus pinned revisions. Restoring never edits an existing story.'); status.pack()
        def toggle_pin():
            if not listing.curselection(): return
            index = listing.curselection()[0]
            selected = records[index]
            try:
                self.draft = drafts.pin(self.draft_root, self.draft, selected['id'], not selected.get('pinned'))
                selected['pinned'] = not selected.get('pinned')
                listing.delete(index); listing.insert(index, revision_label(selected)); listing.selection_set(index)
                status.configure(text='Revision '+('pinned; kept beyond ordinary history retention.' if selected['pinned'] else 'unpinned; ordinary retention applies on the next save.'))
            except (OSError, ValueError) as exc: status.configure(text='Pin change failed: '+str(exc))
        ttk.Button(window, text='Pin / unpin selected revision', command=toggle_pin).pack(pady=4)
        def restore():
            if not listing.curselection() or self.cancel_event: return
            try:
                self.draft = drafts.restore(self.draft_root, self.draft, records[listing.curselection()[0]]['id'], self.snapshot())
                self.restore_snapshot(self.draft['current']); window.destroy()
            except (OSError, ValueError) as exc: status.configure(text=str(exc))
        ttk.Button(window, text='Restore selected revision', command=restore).pack(pady=12)
        phone_theme.apply_tree(window)

    def review_character(self):
        import character_dossier
        try:
            p = self.collect()
            d = character_dossier.starting('custom_preview', p | {'portrait':self.portrait or ''})
        except ValueError as exc:
            self.status.configure(text='Review needs attention: '+str(exc)); return
        window = self.workspace_window('Review · starting profile')
        frame = ttk.Frame(window); frame.pack(fill='both', expand=True)
        scroll = ttk.Scrollbar(frame); scroll.pack(side='right', fill='y')
        body = tk.Text(frame, bg=ui.PANEL, fg=ui.CREAM, wrap='word', font=('Segoe UI',11), padx=16, pady=16, yscrollcommand=scroll.set)
        body.pack(fill='both', expand=True)
        scroll.configure(command=body.yview)
        body.insert('end', '\n\n'.join(character_dossier.text(d, tab) for tab in ('Overview','Backstory','Details','Awakened')))
        body.configure(state='disabled')
        ttk.Button(window, text='Return to editing', command=window.destroy).pack(pady=12)
        phone_theme.apply_tree(window)

    def save_character(self, begin=False, as_copy=False):
        import custom_library
        import game_core as core
        if self.needs_trait() and not self.trait_ready():
            self.status.configure(text='Evaluate your Trait and accept its amplification options first.'); return
        if self.cancel_event or not self.portrait or self.signature()!=self.generated_signature:
            self.status.configure(text='Generate a portrait matching your current appearance first.'); return
        try:
            custom.verify_portrait(custom.portrait_path({'portrait':self.portrait}))
            p = custom_library.save_profile(self.collect() | {'portrait':self.portrait, 'profile_id':self.edit_profile_id or self.draft['id']},
                    core.SAVE.parent, separate=as_copy, expected=None if as_copy else self.edit_profile_baseline)
            self.edit_profile_id = p['profile_id']; self.edit_profile_baseline = custom_library.fingerprint(p)
            if self.on_saved: self.on_saved(p)
            if begin: self.game.start_custom(p, self.portrait)
        except (OSError, ValueError) as exc:
            self.status.configure(text=str(exc)+' · any successfully saved character remains in the roster.'); return
        self.destroy()
