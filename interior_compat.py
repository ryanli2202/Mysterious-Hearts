"""Legacy named rooms retain their exact source meaning and save fields."""
ROOMS={
 'interpol_briefing':'interpol_hq__awakened_operations_briefing_room',
 'interpol_training':'interpol_hq__controlled_training_hall',
 'interpol_containment':'interpol_hq__interview_containment_wing',
 'blackstone_loading':'blackstone_hq__loading_compound',
 'blackstone_records':'blackstone_hq__research_records',
 'blackstone_lab':'blackstone_hq__experimental_wing',
 'blackstone_command':'blackstone_hq__executive_command',
}
for number in range(1,9):
    site='site_'+str(number).zfill(2)
    ROOMS[site+'_reception']=site+('__reception_public_displays' if number==7 else '__reception')
    ROOMS[site+'_briefing']=site+'__briefing_room'
LOCATIONS={room:location for location,room in ROOMS.items()}


def location(room,building):
    return LOCATIONS.get(room,building)


def assign(s,who,destination):
    import interiors
    actor=interiors.actor_record(s,who)
    place=interiors.ROOMS[destination].building
    raw=location(destination,place)
    actor.update(location=raw,room=destination,room_location=raw)
    if who==s['player']:
        s['world'].update(location=raw,room=destination)
