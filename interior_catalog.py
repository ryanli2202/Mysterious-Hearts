"""Runtime room catalogue; no runtime dependency on planning or production tools."""
import json
from pathlib import Path
import interior_residential as homes


def load(room_type):
    data=json.loads(Path(__file__).with_suffix('.json').read_text(encoding='utf-8'))
    rooms,arrivals={},{}
    for building in data['buildings']:
        place=building['id']
        arrivals[place]=building['arrival']
        for row in building['rooms']:
            key=row['id'].split('__',1)[1]
            bathroom='bathroom' in key or 'restroom' in key
            private=(homes.private(key) and (place in homes.HOUSEHOLDS or place.startswith('vacant_'))
                     or key.startswith('private_') and place in ('lantern_house','saints_depot','purple_clubhouse','hamayashi_house','rojos_courtyard','consortium_house')
                     or key in ('rear_residence_living_room','upstairs_living_guitar_room','upper_apartment_living_chart_room'))
            staff=key in __import__('interior_workplaces').STAFF_ROOMS.get(row['id'].split('__',1)[0],())
            secure=(place.startswith('site_') or place in ('interpol_hq','blackstone_hq')
                    or place=='syndicate_office' and key=='guarded_access_passage'
                    or place in ('syndicate','lantern_house','saints_depot','purple_clubhouse','hamayashi_house','rojos_courtyard','consortium_house','hamayashi_annex','hamayashi_store'))
            rooms[row['id']]=room_type(row['id'],place,row['label'],tuple(row['neighbours']),row['art'],
                owners=homes.owners(place,key) if private else (),private=private,
                bathroom=bathroom,outdoor=row['outdoor'],capacity=1 if bathroom else 8 if place in homes.HOUSEHOLDS else 24,
                safe_exit=building['arrival'],physical_space=row['physical_space'],
                policy='staff' if staff else 'security' if secure else 'shared',
                reservable=key in ('reservable_study_room','lesson_alcove_view','meeting_room','boardroom'))
    return rooms,arrivals
