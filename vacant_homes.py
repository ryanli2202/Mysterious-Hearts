"""Unassigned residences reserved for a potential future custom protagonist.

Keep these out of world_loop.HOUSES: that registry creates cast members.
These are visitable locations, not a home-selection or ownership system.
"""
HOMES = {
    'vacant_downtown_home': {
        'name': 'Vacant downtown apartment', 'point': (770, 420),
        'description': 'An empty downtown apartment with an open living room, fitted kitchen, bare timber floors and broad windows above the city streets.',
    },
    'vacant_suburbs_home': {
        'name': 'Vacant suburban house', 'point': (90, 675),
        'description': 'An empty two-bedroom house in the suburbs, with a fitted kitchen, a small garden and windows facing a quiet, leafy residential street.',
    },
    'vacant_beach_home': {
        'name': 'Vacant beach cottage', 'point': (1280, 720),
        'description': 'An empty cottage near Silver Sands beach, with bare timber floors, a fitted kitchen and a small deck looking across the dunes toward the ocean.',
    },
    'vacant_university_home': {
        'name': 'Vacant university apartment', 'point': (235, 305),
        'description': 'An empty apartment near Winterfield University, with a separate bedroom, fitted kitchenette and room for a study area overlooking the campus paths.',
    },
}

STATUS = 'Vacant and unfurnished. Unassigned; reserved for a potential future custom protagonist.'


def status(state, location):
    if state.get('custom_protagonist', {}).get('home') == location:
        return 'Your home · You have just moved to Winterfield.'
    return STATUS
