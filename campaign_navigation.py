"""MH-016: campaign directions hand off to the general, unselected Maps view.

The existing travel and case handlers own permissions, party checks and arrival.
No story board performs physical travel as a side effect of opening Maps.
"""
from tkinter import ttk


def open_maps(game):
    for name in ('campaign_view', 'interpol_view'):
        panel = getattr(game, name, None)
        if panel is not None and panel.winfo_exists():
            panel.place_forget()
    game.phone_window('Maps')


def directions(parent, game, destination):
    import town, interiors
    place=interiors.building(destination)
    room_name = (interiors.ROOMS[destination].label if destination in interiors.ROOMS
                 else town.location_name(game.state_data, destination))
    label = ttk.Label(parent, text='Find '+town.location_name(game.state_data, place)+
                      ' in Maps. Select its marker, then travel and enter in person.'+
                      (' Objective room: '+room_name+'.' if place!=destination else ''),
                      wraplength=650, justify='left')
    label.pack(fill='x', pady=5)
    label.bind('<Configure>', lambda e: label.configure(wraplength=max(90, e.width-12)))
    button = ttk.Button(parent, text='Open Maps', command=lambda: open_maps(game))
    button.pack(fill='x', pady=4)
    return button


def travel(s, destination):
    """Selected Maps destination, with the saved field-team travel contract."""
    import interpol, town, interiors
    objective = interpol.objective(s)
    if objective and interiors.building(objective['venue']) == destination:
        # The old case travel handler restores its partner to the party before
        # calling normal travel. Validate on a copy so a denied stale selection
        # cannot leave that partial party mutation behind.
        import copy
        interpol.travel_objective(copy.deepcopy(s))
        return interpol.travel_objective(s)
    return town.travel(s, destination)
