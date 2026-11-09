"""Repeatable, interest-led public destinations for free time and social plans."""
import hashlib
import public_venues

OUTDOORS={'park','wetlands','track','square','sailing_club'} | public_venues.OUTDOORS
PREFERENCES={
    'alyssa': ('archive', 'library', 'park', 'flowers', 'market', 'makerspace', 'cinema', 'cafe'),
    'neo': ('makerspace', 'boxing_club', 'cinema', 'park', 'noodle_shop', 'library', 'arcade'),
    'emily': ('flowers','park','makerspace','market','cafe','cinema'),
    'sophie': ('track','park','boxing_club','noodle_shop','market','cinema'),
    'amy': ('makerspace','archive','park','cinema','wetlands','cafe'),
    'samantha': ('boxing_club','arena','cycle_shop','noodle_shop','marios_pizza','park'),
    'april': ('chess','planetarium','archive','makerspace','park','cafe'),
    'rei': ('archive','makerspace','cinema','park','chess','market'),
    'minsu': ('track','boxing_club','noodle_shop','campus','park','marios_pizza'),
    'garrett': ('market','noodle_shop','marios_pizza','park','cinema','sailing_club'),
    'ivan': ('cinema','sailing_club','market','park','chess','marios_pizza'),
    'yuriko': ('makerspace','cinema','boutique','archive','park','marios_pizza'),
    'lena': ('archive','cinema','square','market','park','makerspace'),
    'naomi': ('cycle_shop','makerspace','market','boxing_club','archive','park'),
    'celeste': ('planetarium','wetlands','flowers','market','cinema','park'),
    'dev': ('makerspace','cycle_shop','archive','chess','cafe','market'),
    'rosa': ('flowers','market','park','makerspace','cafe','wetlands'),
    'elliot': ('wetlands','park','archive','planetarium','market','cinema'),
    'tyler': ('boxing_club','arena','track','noodle_shop','park','cinema'),
    'valentina': ('sailing_club','market','cinema','park','marios_pizza','archive'),
    'daniel': ('cinema','archive','market','makerspace','park','cafe'),
    'sylvanis': ('arena','boxing_club','chess','park','noodle_shop'),
}
EXTRA_PREFERENCES = {
    'emily': ('public_park', 'library', 'shopping_mall', 'bowling_alley'),
    'sophie': ('beach', 'bowling_alley', 'arcade', 'nightclub', 'bar'),
    'amy': ('library', 'public_park', 'beach', 'shopping_mall'),
    'samantha': ('bowling_alley', 'arcade', 'bar', 'nightclub'),
    'april': ('library', 'public_park', 'arcade'),
    'rei': ('library', 'beach', 'bar', 'shopping_mall'),
    'minsu': ('library', 'arcade', 'bowling_alley', 'beach'),
    'garrett': ('bowling_alley', 'bar', 'nightclub', 'beach'),
    'ivan': ('nightclub', 'bar', 'beach', 'shopping_mall'),
    'yuriko': ('arcade', 'shopping_mall', 'library', 'bowling_alley'),
    'lena': ('library', 'shopping_mall', 'public_park'),
    'naomi': ('arcade', 'bowling_alley', 'bar'),
    'celeste': ('beach', 'library', 'public_park'),
    'dev': ('arcade', 'library', 'bowling_alley'),
    'rosa': ('public_park', 'shopping_mall', 'beach'),
    'elliot': ('beach', 'library', 'public_park'),
    'tyler': ('bowling_alley', 'arcade', 'nightclub', 'bar'),
    'valentina': ('beach', 'bar', 'shopping_mall'),
    'daniel': ('library', 'arcade', 'shopping_mall'),
    'sylvanis': ('bar', 'bowling_alley'),
}
for who, venues in EXTRA_PREFERENCES.items():
    PREFERENCES[who] += venues

for who in ('rei', 'ivan', 'amy', 'yuriko', 'garrett', 'sophie', 'lena', 'daniel', 'valentina'):
    PREFERENCES[who] += ('downtown',)

for who, venues in {
    'emily': ('orchard', 'farm_shop'), 'sophie': ('pine_trail', 'ridge_lookout'),
    'amy': ('pottery_studio', 'lighthouse_walk'), 'april': ('hill_tea_room', 'railway_museum'),
    'garrett': ('southbank_diner', 'harbour_market'), 'elliot': ('marine_centre', 'coastal_pier'),
    'rei': ('pottery_studio', 'ridge_lookout'), 'valentina': ('coastal_pier', 'harbour_market'),
}.items():
    PREFERENCES[who] += venues

ACTIVITIES={
    'flowers':'Browsing seasonal flowers', 'park':'Taking a riverside walk',
    'makerspace':'Exploring a hobby at the makerspace', 'market':'Browsing the market stalls',
    'cafe':'Enjoying tea and a quiet conversation', 'cinema':'Browsing films at the cinema',
    'track':'Enjoying a casual run', 'boxing_club':'Spending free time at the boxing club',
    'noodle_shop':'Sharing a bowl of noodles', 'archive':'Exploring local history and art',
    'wetlands':'Watching birds along the boardwalk', 'arena':'Watching a bout at the arena',
    'cycle_shop':'Browsing bikes and accessories', 'marios_pizza':'Sharing pizza',
    'chess':'Playing a casual game of chess', 'planetarium':'Enjoying a sky exhibition',
    'square':'Wandering around the town square', 'sailing_club':'Spending time by the boathouse',
    'campus':'Relaxing on campus', 'boutique':'Browsing gifts and clothes',
}

ACTIVITIES.update({key: v[2] for key, v in public_venues.VENUES.items()})


def choose(who, minute, *, other=None, recent=(), indoor=False, preferred=(), crowd=None, meals=False):
    import weather
    first=PREFERENCES.get(who,('market','park','cinema','archive','cafe'))
    second=PREFERENCES.get(other,())
    candidates=set(first)|set(second)|set(preferred)
    candidates &= ACTIVITIES.keys()  # Never select a private home or restricted venue.
    if meals: candidates &= {'cafe','noodle_shop','marios_pizza','market'}
    if indoor or weather.shelter(minute): candidates -= OUTDOORS
    if not candidates: candidates={'cinema','archive','noodle_shop'}
    candidates = {place for place in candidates if public_venues.suitable(place, minute)}
    if not candidates: candidates = {'cinema', 'archive', 'noodle_shop'}
    if recent and len(candidates)>1: candidates.discard(recent[-1])
    def score(place):
        seed=f'{who}:{other}:{minute//1440}:{minute%1440//180}:{place}'
        variety=int(hashlib.sha256(seed.encode()).hexdigest()[:8],16)/0xffffffff
        interest=(1 if place in first else 0)+(1 if place in second else 0)
        return variety*4+interest+(1 if place in preferred else 0)-recent.count(place)*1.5-(crowd or {}).get(place,0)*.35
    return max(sorted(candidates),key=score)


def social_destination(s,who,other=None,*,indoor=False,preferred=()):
    people=s['autonomy']['people']
    recent=list(people[who].get('recent_venues',[]))
    if other in people: recent=list(people[other].get('recent_venues',[]))+recent
    crowd={}
    for actor in s['world']['cast'].values():
        place=actor['location']; crowd[place]=crowd.get(place,0)+1
    return choose(who,s['world']['minute'],other=other,recent=recent,indoor=indoor,preferred=preferred,crowd=crowd)
