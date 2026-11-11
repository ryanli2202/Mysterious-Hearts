"""Everyday residents with repeatable public routines, independent of the player."""
import story_calendar
import weather
import outskirts
import street_recruits
import public_venues
import json
from functools import lru_cache
from pathlib import Path


@lru_cache(maxsize=1)
def portrait_references():
    path = Path(__file__).resolve().parent / 'assets' / 'portraits' / 'town-residents-manifest.json'
    return {entry['name']: entry['appearance'] for entry in json.loads(path.read_text(encoding='utf-8'))['portraits']}


def portrait_reference(name):
    if name in street_recruits.RESIDENTS: return street_recruits.RESIDENTS[name]['appearance']
    return portrait_references()[name]

# Append names here and in phone_numbers.RESIDENTS; identities survive old saves.
# Daily public windows: morning 08-12, afternoon 12-17, evening 17-22.
RESIDENTS = {
    'Priya Shah': dict(role='public librarian', age=38,
        places=('library', 'library', 'chess'), weekend=('public_park', 'library', 'chess'),
        voice='Warm, precise, with a very dry sense of humour; asks what someone enjoys before recommending a book.',
        life='Runs a no-pressure reading circle. Friends with Theo, who supplies secondhand copies; they disagree cheerfully about writing in margins.',
        topics=('Choosing a short novel for people who say they never finish books.', 'Repairing a reading-circle copy with a loose cover.', 'Comparing readers’ very different interpretations of the ending.')),
    'Otis Bell': dict(role='retired harbour mechanic', age=67,
        places=('sailing_club', 'public_park', 'marios_pizza'), weekend=('sailing_club', 'square', 'marios_pizza'),
        voice='Unhurried and practical; tells specific small stories instead of dispensing universal wisdom.',
        life='Repairs model boats for his own enjoyment. June trades him cuttings for repaired garden tools. He is learning to cook after years of relying on takeaway.',
        topics=('A model boat keeps turning left and he wants to know why.', 'Trying a new soup recipe without treating the kitchen like a workshop.', 'Looking for somebody willing to compare two model sail designs.')),
    'Nadia Flores': dict(role='harbour shuttle driver', age=44,
        places=('downtown', 'square', 'bowling_alley'), weekend=('public_park', 'shopping_mall', 'bowling_alley'),
        voice='Brisk, friendly and amused by small logistical disasters; does not hurry people who need help.',
        life='On foot only during her public breaks. Keeps paper route cards for passengers. She and Ben run a casual bowling team that loses more often than it wins.',
        topics=('Passengers keep confusing two similarly named stops.', 'Choosing a terrible bowling-team name with Ben.', 'Her new walking shoes squeak on polished floors.')),
    'Ben Okafor': dict(role='bowling-alley technician', age=31,
        places=('bowling_alley', 'bowling_alley', 'bar'), weekend=('public_park', 'bowling_alley', 'bowling_alley'),
        voice='Playful, patient with beginners, and quietly proud of careful repair work.',
        life='Maintains the lanes and bowls with Nadia. Trades repair advice with Otis. Wants to learn dancing but keeps joking instead of signing up.',
        topics=('Restoring the lettering on an old team trophy.', 'Nadia wants matching shirts for their very unsuccessful team.', 'Considering a beginner dance class and trying not to overthink it.')),
    'Tess Morgan': dict(role='cinema projectionist', age=29,
        places=('library', 'cinema', 'cinema'), weekend=('shopping_mall', 'cinema', 'cinema'),
        voice='Enthusiastic about sound and practical effects; avoids spoiling a film even when excited.',
        life='Maintains the Bijou programme and makes miniature sets at home. Iris sometimes plays before a screening; Tess borrows old film magazines from Priya.',
        topics=('Choosing between two restored comedies for the programme.', 'A miniature cinema foyer will not fit through her model doorway.', 'Comparing the audience reaction to a silent film with last week’s crowd.')),
    'Farah Haddad': dict(role='tailor and alterations specialist', age=52,
        places=('boutique', 'shopping_mall', 'square'), weekend=('boutique', 'shopping_mall', 'marios_pizza'),
        voice='Matter-of-fact, warmly teasing, and attentive to comfort rather than labels or price.',
        life='Keeps useful fabric scraps for community repairs. Iris brings stage clothes to mend; Farah wants a free evening to hear her actually perform.',
        topics=('Turning a worn jacket into something its owner wants to keep.', 'Sorting donated fabric for a community mending table.', 'Planning an evening off instead of taking one more rush job.')),
    'Gabe Turner': dict(role='bicycle repairer', age=26,
        places=('downtown', 'downtown', 'arcade'), weekend=('public_park', 'downtown', 'arcade'),
        voice='Easygoing and a little competitive about arcade scores; explains repairs without patronising.',
        life='Maintains Leo’s delivery bicycle. Likes repairing things more than selling replacements. Friends with arcade attendant Wren and never quite believes her high scores.',
        topics=('Restoring an old bicycle bell because its owner loves the sound.', 'Leo’s delivery bike needs a sturdier basket.', 'Trying to beat Wren’s score without blaming the cabinet.')),
    'Wren Park': dict(role='arcade attendant and animation student', age=22,
        places=('campus', 'arcade', 'arcade'), weekend=('library', 'arcade', 'cinema'),
        voice='Quick, observant, with playful exaggeration about games; becomes thoughtful when discussing animation.',
        life='Draws tiny looping animations between classes. Trades film recommendations with Tess and friendly high-score challenges with Gabe. Work and coursework sometimes compete for time.',
        topics=('Animating a pigeon that looks accidentally like a potato.', 'Trying to finish an assignment before the next shift.', 'Comparing hand-drawn movement with an old arcade character.')),
    'Celia Brooks': dict(role='community nurse', age=46,
        places=('square', 'library', 'public_park'), weekend=('public_park', 'shopping_mall', 'marios_pizza'),
        voice='Grounded, kind, and willing to talk about something other than work. Keeps professional boundaries.',
        life='Her appearances are off-duty breaks, not clinic appointments. Walks with June and is attempting balcony gardening. Never shares patient information or diagnoses a stranger in conversation.',
        topics=('Her balcony herbs survived because June labelled the watering cans.', 'Choosing a book that has nothing to do with work.', 'Trying to leave work on time for an ordinary walk.')),
    'Arthur Finch': dict(role='local-history volunteer', age=73,
        places=('archive', 'library', 'chess'), weekend=('square', 'archive', 'chess'),
        voice='Curious and gently pedantic; happy to admit that a favourite old story may be wrong.',
        life='Catalogues donated postcards with consent. Priya helps him distinguish dates from guesses. He has no privileged knowledge of police cases or the protagonists’ pasts.',
        topics=('Two postcards show the same shop with different names.', 'Trying to identify a parade year from a public photograph.', 'Learning to scan photographs without cropping the handwritten captions.')),
    'Luz Moreno': dict(role='community-garden coordinator', age=34,
        places=('public_park', 'flowers', 'square'), weekend=('public_park', 'public_park', 'square'),
        voice='Energetic and practical; offers small manageable invitations rather than guilt about volunteering.',
        life='Shares seedlings with June and asks Emily about hardy flowers. Competes amicably with Otis over whose repaired tools last longer. Wants a garden accessible to people with little free time.',
        topics=('Choosing sturdy labels that will survive the rain.', 'Finding a use for more courgettes than anyone expected.', 'Planning a seed swap where beginners have something to take home.')),
    'Samir Dutta': dict(role='bakery delivery driver', age=40,
        places=('square', 'marios_pizza', 'beach'), weekend=('shopping_mall', 'public_park', 'beach'),
        voice='Sociable, a keen listener, with affectionate jokes about his own baking experiments.',
        life='Chats during delivery breaks, not while driving. Trades lunch recommendations with Mario and knows Nadia from early shifts. Practises breadmaking on days off despite seeing bread all week.',
        topics=('His own loaf came out much flatter than the ones he delivers.', 'Comparing two lunches that travel well in a delivery bag.', 'Looking forward to a quiet shoreline walk after an early start.')),
}

RESIDENTS.update(outskirts.RESIDENTS)
RESIDENTS.update(street_recruits.RESIDENTS)

TASTES = {
    'Priya Shah': ('Porridge with pears', 'Lentil soup', 'Spinach dal', 'Salted almonds', 'Cardamom tea', 'Detectorists', 'The Station Agent', 'Piranesi', 'Susanna Clarke'),
    'Otis Bell': ('Scrambled eggs on toast', 'Tomato soup', 'Fish pie', 'Oat biscuits', 'Black tea', 'The Repair Shop', 'The Straight Story', 'The Old Man and the Sea', 'Ernest Hemingway'),
    'Nadia Flores': ('Bean and egg wrap', 'Rice and beans', 'Roast chicken', 'Orange slices', 'Coffee with milk', 'Abbott Elementary', 'Paddington 2', 'None; prefers radio on days off', 'None'),
    'Ben Okafor': ('Banana pancakes', 'Chicken sandwich', 'Jollof rice', 'Roasted peanuts', 'Ginger beer', 'Taskmaster', 'School of Rock', 'The Hitchhiker’s Guide to the Galaxy', 'Douglas Adams'),
    'Tess Morgan': ('Yoghurt with granola', 'Mushroom toastie', 'Vegetable lasagne', 'Salted popcorn', 'Black coffee', 'The Twilight Zone', 'Singin’ in the Rain', 'The Invention of Hugo Cabret', 'Brian Selznick'),
    'Farah Haddad': ('Labneh and flatbread', 'Chickpea salad', 'Stuffed aubergine', 'Pistachios', 'Mint tea', 'The Great British Sewing Bee', 'Mrs. Harris Goes to Paris', 'Little Women', 'Louisa May Alcott'),
    'Gabe Turner': ('Peanut-butter toast', 'Bean burrito', 'Mushroom burgers', 'Pretzels', 'Lemon soda', 'MythBusters', 'Back to the Future', 'None; prefers illustrated repair manuals', 'None'),
    'Wren Park': ('Egg fried rice', 'Vegetable noodles', 'Tofu curry', 'Seaweed crackers', 'Peach iced tea', 'Hilda', 'Spider-Man: Into the Spider-Verse', 'Howl’s Moving Castle', 'Diana Wynne Jones'),
    'Celia Brooks': ('Toast and a boiled egg', 'Roast-vegetable wrap', 'Salmon and potatoes', 'Dark chocolate', 'Rooibos tea', 'The Good Place', 'Kiki’s Delivery Service', 'A Psalm for the Wild-Built', 'Becky Chambers'),
    'Arthur Finch': ('Marmalade toast', 'Cheese and pickle sandwich', 'Shepherd’s pie', 'Shortbread', 'English breakfast tea', 'Time Team', 'Local Hero', 'Three Men in a Boat', 'Jerome K. Jerome'),
    'Luz Moreno': ('Avocado toast', 'Garden vegetable soup', 'Black-bean tacos', 'Sunflower seeds', 'Hibiscus tea', 'Gardener’s World', 'My Neighbour Totoro', 'Braiding Sweetgrass', 'Robin Wall Kimmerer'),
    'Samir Dutta': ('Masala omelette', 'Chickpea wraps', 'Fish curry', 'Banana bread', 'Masala chai', 'The Great British Bake Off', 'Chef', 'None; enjoys recipe notebooks instead', 'None'),
}


TASTES.update(outskirts.TASTES)
TASTES.update(street_recruits.TASTES)


def favourites(name):
    labels = ('Breakfast', 'Lunch', 'Dinner', 'Snack', 'Drink', 'TV show', 'Movie', 'Book', 'Author')
    return '; '.join(f'{label}: {value}' for label, value in zip(labels, TASTES[name]))


def profile(name):
    person = RESIDENTS[name]
    return (name, person['role'],
            f"Age {person['age']}. {person.get('appearance', '')} {person['voice']} {person['life']} "
            'An ordinary local, not a secret operative. Acquaintances do not confer private knowledge. '
            'Do not invent shared history with the player or promise services the game cannot perform.')


def routine(name, minute):
    person = RESIDENTS[name]
    hour = minute % 1440 / 60
    if not 8 <= hour < 22:
        return None
    slot = 0 if hour < 12 else 1 if hour < 17 else 2
    schedule = person['weekend'] if story_calendar.story_date(minute).weekday() >= 5 else person['places']
    place = schedule[slot]
    if place in (public_venues.OUTDOORS | {'square'}) and weather.shelter(minute):
        place = 'library'
    return place


def refresh(state):
    """Update only this roster; preserve legacy locals, venue staff and saved chats."""
    world = state['world']
    current = [name for name in world['npcs'] if name not in RESIDENTS]
    current.extend(name for name in RESIDENTS
                   if routine(name, world['minute']) == world['location'])
    world['npcs'] = list(dict.fromkeys(current))
    import keisuke
    keisuke.refresh(state)
    import gang_leaders
    gang_leaders.refresh(state)
    import gang_members
    gang_members.refresh(state)
    import organisation_guards
    organisation_guards.refresh(state)


def context(name, minute):
    if name not in RESIDENTS:
        return ''
    person = RESIDENTS[name]
    topic = person['topics'][(minute // 1440) % len(person['topics'])]
    return ('Current everyday conversation seed: ' + topic +
            ' This is their own interest, not proof of an event attended or help given by the player. '
            'Refer to actual conversation history for familiarity; do not repeat this topic if it has already been discussed.')
