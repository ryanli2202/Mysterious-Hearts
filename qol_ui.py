"""Save library, searchable journal and daily overview."""
import json
import uuid
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from phone_dialogs import AppWindow, messagebox, simpledialog
import game_core as core
import qol


def text_window(game, title, text):
    win = AppWindow(game); win.title(title); win.geometry('720x560')
    box = tk.Text(win, wrap='word', padx=16, pady=16, font=('Segoe UI', 12))
    scroll = ttk.Scrollbar(win, command=box.yview); scroll.pack(side='right', fill='y')
    box.configure(yscrollcommand=scroll.set); box.pack(fill='both', expand=True)
    box.insert('end', text); box.configure(state='disabled')
    return win


def overview(game, recap=False):
    text = qol.recap(game.state_data) if recap else '\n'.join(qol.agenda(game.state_data))
    win = text_window(game, 'Welcome back' if recap else 'Daily agenda', text)
    ttk.Button(win, text='Calendar / plan event', command=game.open_calendar).pack(pady=8)


def activate_story(game, state):
    game.cancel_suggestions()
    for attr in ('phone_activity','town_activity','home_activity','calendar_view','profile_view'):
        child = getattr(game, attr, None)
        if child and child.winfo_exists(): child.destroy()
        setattr(game, attr, None)
    game.token += 1
    game.pending = None
    game.in_game = False
    game.state_data = state
    game.persist()
    game.play_screen()
    overview(game, True)


def recover(game, error):
    import save_system
    for path in save_system.recovery(core.SAVE.parent):
        try: state = core.load(path)
        except (ValueError, OSError, KeyError, TypeError, AttributeError): continue
        label = state.get('save_name', state['player'].title())
        if messagebox.askyesno('Recover saved story',
                f'The active save could not load: {error}\n\nRestore the newest valid save?\n{label} · {path.name}'):
            activate_story(game, state)
        return
    messagebox.showerror('Could not load story', f'{error}\nNo valid recovery save was found.')


def saves(game):
    from tkinter import filedialog
    import datetime as dt
    import save_system
    import story_calendar
    win = AppWindow(game); win.title('Story library and recovery'); win.geometry('1040x560')
    box = tk.Listbox(win, exportselection=False); box.pack(fill='both', expand=True, padx=12, pady=12)
    paths = []
    def refresh():
        paths.clear(); box.delete(0,'end')
        for path in save_system.entries(core.SAVE.parent):
            try:
                s = json.loads(path.read_text(encoding='utf-8'))
                label = s.get('save_name', s.get('player','Story').title())
                minute = s.get('world', {}).get('minute', 0)
                place = s.get('world', {}).get('location', 'Unknown')
                kind = ('Continue' if path == core.SAVE else 'Daily checkpoint' if path.parent.name == 'daily'
                        else 'Recovery' if path.parent.name == 'recent' or '.backup' in path.name
                        else 'Autosave' if path.name == 'autosave.json' else 'Manual save')
                stamp = dt.datetime.fromtimestamp(path.stat().st_mtime).strftime('%d %b %Y %H:%M')
                text = f"{label} · {s.get('player', '')} · {story_calendar.story_date(minute)} {minute%1440//60:02}:{minute%60:02} · {place} · {kind} · {stamp}"
            except (OSError, ValueError, TypeError, AttributeError):
                text = f'Damaged save · {path.relative_to(core.SAVE.parent)}'
            box.insert('end', text); paths.append(path)
    def selected():
        return paths[box.curselection()[0]] if box.curselection() else None
    def guarded(action):
        if game.busy: return
        try: action()
        except Exception as exc: messagebox.showerror('Save library', str(exc), parent=win)
    def snapshot():
        if not game.state_data: return
        name = simpledialog.askstring('Save story', 'Save name:', parent=win)
        if not name or not name.strip(): return
        game.capture_draft()
        sid = save_system.identity(game.state_data)
        state = dict(game.state_data, save_name=name.strip()[:100])
        core.save(state, core.SAVE.parent / 'stories' / sid / ('slot-'+uuid.uuid4().hex+'.json')); refresh()
    def load():
        path = selected()
        if not path: return
        state = core.load(path)
        if game.state_data: game.persist()
        win.destroy()
        activate_story(game, state)
    def rename():
        path = selected()
        if not path: return
        name = simpledialog.askstring('Rename save', 'New name:', parent=win)
        if name and name.strip():
            state = core.load(path); state['save_name'] = name.strip()[:100]
            core.save(state,path)
            if path == core.SAVE and game.state_data:
                game.state_data['save_name'] = state['save_name']
            refresh()
    def remove(all_saves=False):
        path = None if all_saves else selected()
        if not all_saves and path is None: return
        prompt = ('Permanently delete ALL stories, manual saves and recovery checkpoints?'
                  if all_saves else 'Permanently delete this story and all of its manual saves and recovery checkpoints?')
        if not messagebox.askyesno('Delete saves', prompt, parent=win): return
        active = all_saves or path == core.SAVE
        if path and game.state_data:
            try:
                sid = json.loads(path.read_text(encoding='utf-8')).get('story_id')
                active |= bool(sid and sid == game.state_data.get('story_id'))
            except ValueError: pass
            sid = game.state_data.get('story_id')
            if sid:
                active |= path.is_relative_to(core.SAVE.parent / 'stories' / sid)
        save_system.delete(core.SAVE.parent, path)
        if active:
            game.cancel_suggestions()
            game.token += 1; game.pending = None; game.in_game = False; game.state_data = None
            win.destroy(); game.home()
        else: refresh()
    def export():
        path = selected()
        if not path: return
        destination = filedialog.asksaveasfilename(parent=win, title='Export story with photos',
                         defaultextension='.zip', filetypes=[('Story bundle', '*.zip')])
        if destination:
            save_system.export_story(core.load(path), destination, core.ROOT)
            messagebox.showinfo('Story exported', 'Your story and its available generated photos were exported.', parent=win)
    def import_bundle():
        source = filedialog.askopenfilename(parent=win, title='Import story bundle', filetypes=[('Story bundle', '*.zip')])
        if source:
            save_system.import_story(source, core.ROOT, core.SAVE.parent); refresh()
    bar = ttk.Frame(win); bar.pack(fill='x', padx=12, pady=6)
    for title, fn in [('Save named copy',snapshot),('Load / restore',load),('Rename',rename),('Export with photos',export),('Import',import_bundle)]:
        ttk.Button(bar,text=title,command=lambda f=fn:guarded(f)).pack(side='left',padx=4)
    danger = ttk.Frame(win); danger.pack(fill='x', padx=12, pady=6)
    for title, fn in [('Delete selected story',remove),('Clear all saves',lambda:remove(True))]:
        ttk.Button(danger,text=title,command=lambda f=fn:guarded(f)).pack(side='left',padx=4)
    refresh()


def journal(game):
    s = game.state_data
    win = AppWindow(game); win.title('Search conversations'); win.geometry('900x680')
    controls = ttk.Frame(win, padding=10); controls.pack(fill='x')
    query = tk.StringVar(); person = tk.StringVar(value='All'); day = tk.StringVar()
    records = qol.history(s); names = sorted(set(r[1] for r in records))
    ttk.Label(controls,text='Phrase').pack(side='left')
    ttk.Entry(controls,textvariable=query,width=22).pack(side='left',padx=5)
    ttk.Combobox(controls,textvariable=person,values=['All',*names],state='readonly',width=20).pack(side='left')
    ttk.Label(controls,text='Date YYYY-MM-DD').pack(side='left',padx=5)
    ttk.Entry(controls,textvariable=day,width=12).pack(side='left')
    only = tk.BooleanVar(); ttk.Checkbutton(win,text='Bookmarks only',variable=only).pack(anchor='w',padx=12)
    results = tk.Listbox(win,exportselection=False,height=11); results.pack(fill='x',padx=12)
    detail = tk.Text(win,wrap='word',font=('Segoe UI',11)); detail.pack(fill='both',expand=True,padx=12,pady=8)
    matches = []
    marks = s.setdefault('bookmarks', [])
    def search(*_):
        matches[:] = [r for r in records if query.get().casefold() in r[3].casefold()
                      and (person.get() == 'All' or person.get() == r[1])
                      and day.get() in r[2] and (not only.get() or r[0] in marks)]
        results.delete(0,'end')
        for r in matches: results.insert('end', ('★ ' if r[0] in marks else '')+f'{r[2]} · {r[1]} · {r[3][:90]}')
    def selected(): return matches[results.curselection()[0]] if results.curselection() else None
    def context(*_):
        r = selected()
        if not r: return
        thread = [x for x in records if x[4:6] == r[4:6]]
        detail.configure(state='normal'); detail.delete('1.0','end')
        for x in thread:
            start = detail.index('end-1c'); detail.insert('end',f'{x[2]} · {x[1]}\n{x[3]}\n\n')
            if x[0] == r[0]: detail.tag_add('match',start,'end-1c'); target=start
        detail.tag_configure('match',background='#ead7a2',foreground='#191919')
        detail.see(target); detail.configure(state='disabled')
    def bookmark():
        r = selected()
        if not r: return
        if r[0] in marks: marks.remove(r[0])
        else: marks.append(r[0])
        game.persist(); search()
    ttk.Button(win,text='Bookmark / remove bookmark',command=bookmark).pack(pady=6)
    results.bind('<<ListboxSelect>>',context)
    for var in (query, person, day, only): var.trace_add('write',search)
    search()
