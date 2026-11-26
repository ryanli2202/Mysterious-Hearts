"""Separate private dorm thresholds opening onto one public access corridor."""
PLACES=frozenset(('amy_home','minsu_home','nest_dorm_corridor'))
CORRIDOR='nest_dorm_corridor__public_dorm_corridor'


def link(rooms,room_type):
    from dataclasses import replace
    doors=('amy_home__dorm_room','minsu_home__dorm_room')
    rooms[CORRIDOR]=replace(rooms[CORRIDOR],neighbours=doors)
    for who,door in zip(('amy','minsu'),doors):
        rooms[door]=replace(rooms[door],neighbours=(CORRIDOR,),private=True,owners=(who,),safe_exit=CORRIDOR)


def register():
    import town
    town.LOCATIONS.setdefault('nest_dorm_corridor','The Nest · public dorm corridor')
