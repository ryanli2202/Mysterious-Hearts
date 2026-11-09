"""Resolve established-cast Bubblegram work in the in-person window."""
from types import SimpleNamespace
from tkinter import ttk
import phone_theme


def open_workplace(game, section='Contracts'):
    if game.busy: return
    import groups
    groups.close_active(game.state_data, 'Focused on a private work appointment.')
    game.close_main_area()
    game.hide_phone_for_location()
    panel = ttk.Frame(game.play_body, padding=16)
    ttk.Label(panel, text='IN PERSON · Private work', font=('Segoe UI', 19, 'bold')).pack(anchor='w')
    ttk.Button(panel, text='Back to location', command=game.leave_main_area).pack(anchor='w', pady=6)
    ttk.Label(panel, text='Opening this desk does not complete work. Arrive at the listed venue, then choose your approach.', wraplength=850).pack(anchor='w', pady=6)
    content = ttk.Frame(panel); content.pack(fill='both', expand=True)
    from job_apps_ui import JobBoard
    # Retain phone navigation callbacks for optional contact/meeting links.
    phone = getattr(game, 'phone_activity', None) or SimpleNamespace(game=game)
    panel.board = JobBoard(phone, content, criminal=True, in_person=True, section=section)
    phone_theme.apply_tree(panel)
    game.area_view = panel
    game.layout_presence()
    game.persist()
    return panel
