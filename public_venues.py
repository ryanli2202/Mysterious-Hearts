"""Shared public venue details for maps, outings and repeat visits."""
VENUES = {
    'downtown': ('Downtown · Winterfield metropolitan district', (640, 420), 'Exploring the downtown boulevards', 'Stroll through Downtown', 0, 'a downtown boulevard walk'),
    'bowling_alley': ('Winterfield Lanes · Bowling alley', (200, 590), 'Playing a friendly round of bowling', 'Play a round · $12', 12, 'a round of bowling'),
    'arcade': ('Pixel Pier · Arcade', (350, 680), 'Chasing high scores at the arcade', 'Play the arcade cabinets · $8', 8, 'arcade games'),
    'nightclub': ('Afterglow · Nightclub', (620, 1060), 'Dancing at Afterglow', 'Join the dance floor · $15', 15, 'a dance-floor session'),
    'bar': ('The Copper Lantern · Bar', (750, 1060), 'Relaxing over drinks at the bar', 'Order a house mocktail · $7', 7, 'a house mocktail'),
    'public_park': ('Winterfield Commons · Public park', (200, 470), 'Walking the community gardens', 'Explore the community gardens', 0, 'a community-garden walk'),
    'beach': ('Silver Sands · Beach', (1280, 570), 'Walking along the beach', 'Take a shoreline walk', 0, 'a shoreline walk'),
    'library': ('Winterfield Public Library', (355, 590), 'Browsing books in the library', 'Browse the reading room', 0, 'a reading-room visit'),
    'shopping_mall': ('Winterfield Galleria · Shopping mall', (1310, 350), 'Browsing shops at the mall', 'Browse the seasonal displays', 0, 'a stroll through the shop displays'),
}
import outskirts
VENUES.update(outskirts.VENUES)
OUTDOORS = {'public_park', 'beach', 'downtown'} | outskirts.OUTDOORS
EVENING = {'nightclub': 20, 'bar': 17}


def suitable(place, minute):
    return place not in EVENING or minute % 1440 >= EVENING[place] * 60
