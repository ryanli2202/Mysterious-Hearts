"""Jobseek's workplace activities live in the main in-person area, not the phone."""
from types import SimpleNamespace
from tkinter import ttk
import job_apps as jobs
import phone_theme


def require_workplace(s, key=None):
    current, _ = jobs.civilian.current(s)
    if key is not None and current != key:
        raise ValueError('Your employer changed. Reopen the current workplace from Jobseek.')
    jobs.guard(s, jobs.JOBS[current]['venue'], 0)
    return current


def open_workplace(game, section='My career'):
    if game.busy:
        raise ValueError('Wait for the current conversation to finish.')
    key = require_workplace(game.state_data)
    # A workplace visit takes over the main area just like other location activities.
    import groups
    groups.close_active(game.state_data, 'Started a workplace visit.')
    game.close_main_area()
    game.hide_phone_for_location()
    game.area_view = WorkplaceView(game.play_body, game, key, section)
    game.layout_presence()
    game.persist()


class WorkplaceView(ttk.Frame):
    def __init__(self, parent, game, key, section):
        super().__init__(parent, padding=16)
        self.game = game
        self.job_key = key
        self.location_key = jobs.JOBS[key]['venue']
        top = ttk.Frame(self); top.pack(fill='x')
        ttk.Label(top, text='IN PERSON · '+jobs.JOBS[key]['title'],
                  font=('Segoe UI', 19, 'bold')).pack(side='left')
        ttk.Button(top, text='Back to location', command=game.leave_main_area).pack(side='right')
        ttk.Label(self, text=jobs.civilian.WORKPLACES[key][3]+' · '+jobs.JOBS[key]['brief'],
                  wraplength=850).pack(fill='x', pady=8)
        ttk.Label(self, text='Choose an activity below. Opening this workplace does not spend time or start work. '
                  'Shift decisions and reviews happen here; leaving does not pause an active shift or project deadline.',
                  wraplength=850).pack(fill='x', pady=4)
        content = ttk.Frame(self); content.pack(fill='both', expand=True)
        from job_apps_ui import JobBoard
        self.board = JobBoard(SimpleNamespace(game=game), content, in_person=True,
                              section=section, workplace_key=key)
        phone_theme.apply_tree(self)
