"""Save-scoped phone activities. All spending and sharing happens through actions."""
import copy
import uuid
from pathlib import Path

import camera
import phone_apps
import scheduled_events
import story_calendar
import town
import mixtape_catalog

NAMES = ('Mixtape', 'Wardrobe', 'Out & About', 'Pocket Wallet',
         'Winterfield Exchange', 'Recipe Box', 'Postcards', 'Campus Portal')
BOOKINGS = {
    'Cinema for two': ('cinema', 24, 120),
    'Dinner table for two': ('noodle_shop', 12, 90),
    'Bowling for two': ('bowling_alley', 30, 60),
    'Creative workshop': ('makerspace', 20, 90),
}
RECIPES = {
    'Ginger noodle bowl': (12, 'Simmer ginger in broth. Cook noodles, add greens, and finish with sesame oil.'),
    'Garden pasta': (10, 'Cook pasta. Sauté tomatoes and greens, toss together, and finish with herbs.'),
    'Honey toast': (5, 'Toast bread, spread with butter, drizzle with honey, and serve with sliced fruit.'),
}
CLUBS = {'Sketch club': ('makerspace', 'Bring a sketchbook and draw an everyday object.'),
         'Reading circle': ('library', 'Read a chapter and prepare a discussion question.'),
         'Running club': ('track', 'Plan a gentle warm-up and a training goal.')}
COURSES = {'Creative writing': ('library', 'Write a short scene about a place in Winterfield.'),
           'Design fundamentals': ('makerspace', 'Sketch an outfit using two contrasting textures.'),
           'Independent study': ('campus', 'Review your notes and write three questions for further study.')}


def ensure(s):
    d = s.setdefault('lifestyle_apps', {})
    for key in ('playlists', 'shares', 'receipts', 'bookings', 'designs', 'postcards', 'purchases', 'cooked'):
        d.setdefault(key, [])
    d.setdefault('recipes', ['Honey toast'])
    d.setdefault('clubs', {})
    d.setdefault('courses', {})
    d.setdefault('drafts', {})
    return d


def text(value, limit=500):
    value = value.strip()
    if not value or len(value) > limit:
        raise ValueError(f'Enter between 1 and {limit} characters.')
    return value


def contact(s, who):
    if who not in phone_apps.contacts(s):
        raise ValueError('Choose someone in your contacts.')


def record(s, collection, **values):
    item = dict(id=uuid.uuid4().hex, minute=s['world']['minute'], **values)
    ensure(s)[collection].append(item)
    return item


def spend(s, amount, title):
    if not isinstance(amount, int) or amount <= 0:
        raise ValueError('Enter a positive whole-dollar amount.')
    if s['world']['money'] < amount:
        raise ValueError('Not enough money.')
    s['world']['money'] -= amount
    return record(s, 'receipts', title=title, amount=amount)


def share(s, who, kind, content):
    contact(s, who)
    item = record(s, 'shares', recipient=who, kind=kind, content=copy.deepcopy(content))
    if isinstance(content, dict):
        detail = content.get('title') or content.get('message', '')
        if content.get('tracks'): detail += ' — '+ '; '.join(content['tracks'])
        if content.get('memory'): detail += '. '+content['memory']
        if content.get('method'): detail += '. '+content['method']
    else:
        detail = str(content)
    note = f'{camera.name(s["player"])} shared {kind}: {detail}'
    s['routes'][who]['history'].append(dict(role='status', content=note))
    s.setdefault('shared_events', []).append(dict(minute=s['world']['minute'], text=note, witnesses=[who]))
    return item


def save_playlist(s, title, tracks, memory=''):
    title = text(title, 80)
    tracks = [text(t, 120) for t in tracks.splitlines() if t.strip()]
    if not 1 <= len(tracks) <= 30:
        raise ValueError('Add 1–30 songs, one title and artist per line.')
    if len(memory) > 500:
        raise ValueError('Keep the memory to 500 characters.')
    return record(s, 'playlists', title=title, tracks=tracks, memory=memory.strip())


def share_playlist(s, ident, who):
    item = next((p for p in ensure(s)['playlists'] if p['id'] == ident), None)
    if item is None:
        raise ValueError('That playlist is no longer available.')
    return share(s, who, 'a Mixtape playlist', {k: item[k] for k in ('title', 'tracks', 'memory')})


def save_catalog_playlist(s, title, song_ids, memory=''):
    """Resolve stable catalogue IDs while keeping legacy playlist snapshots readable."""
    if not 1 <= len(song_ids) <= 30:
        raise ValueError('Choose 1–30 songs from the artists below.')
    if len(set(song_ids)) != len(song_ids):
        raise ValueError('This playlist already contains that song.')
    if any(ident not in mixtape_catalog.SONGS for ident in song_ids):
        raise ValueError('Choose songs from the Mixtape catalogue.')
    item = save_playlist(s, title, '\n'.join(mixtape_catalog.track_label(i) for i in song_ids), memory)
    item['song_ids'] = list(song_ids)
    return item


def edit_mixtape_playlist(s, title, entries, memory='', playlist_id=None):
    """Save a catalogue selection, preserving legacy tracks only from its source playlist."""
    original = next((p for p in ensure(s)['playlists'] if p['id'] == playlist_id), None)
    if playlist_id and original is None:
        raise ValueError('That playlist is no longer available.')
    if not 1 <= len(entries) <= 30:
        raise ValueError('Choose 1–30 songs for your playlist.')
    tracks, ids = [], []
    for entry in entries:
        ident = entry.get('id')
        if ident in mixtape_catalog.SONGS:
            label = mixtape_catalog.track_label(ident)
        elif not ident and original and entry.get('label') in original['tracks']:
            label = entry['label']
        else:
            raise ValueError('Choose songs from the Mixtape catalogue.')
        if ident and ident in ids:
            raise ValueError('This playlist already contains that song.')
        tracks.append(text(label, 120)); ids.append(ident)
    title = text(title, 80)
    if len(memory) > 500:
        raise ValueError('Keep the memory to 500 characters.')
    values = dict(title=title, tracks=tracks, song_ids=ids, memory=memory.strip())
    if original is not None:
        original.update(values)
        return original
    return record(s, 'playlists', **values)


def wear(s, label):
    if label == 'Automatic':
        s['world'].pop('player_outfit', None)
    elif label in camera.outfits(s, s['player']):
        s['world']['player_outfit'] = label
    else:
        raise ValueError('Choose an available outfit.')


def design_request(s, title, description):
    title, description = text(title, 60), text(description, 500)
    options = camera.outfits(s, s['player'])
    reference = options.get('Signature outfit') or next(iter(options.values()), None)
    if not reference:
        raise ValueError('A character portrait is needed to design an outfit.')
    return dict(title=title, description=description, player=s['player'],
                references=[reference], prompt=(
        f'Create a full-length outfit design portrait of {camera.name(s["player"])}. '
        'Preserve the reference character identity, face, body proportions and illustration style. '
        'Replace the clothing with the following design. Show the entire outfit including shoes, '
        'neutral studio background, clear fabric details, no text or watermark. '
        f'Outfit: {description}'))


def commit_design(s, request, generated):
    import codex_images
    from PIL import Image
    if request['player'] != s['player']:
        raise ValueError('This design belongs to a different character.')
    prior = next((d for d in ensure(s)['designs'] if d['job'] == generated['id']), None)
    if prior:
        return prior
    path = Path(generated['path']).resolve()
    if not path.is_relative_to(codex_images.STORE.resolve()) or not path.is_file():
        raise ValueError('The generated design image is missing.')
    with Image.open(path) as image:
        image.verify()
    item = record(s, 'designs', title=request['title'], description=request['description'],
                  player=request['player'], job=generated['id'],
                  path=path.relative_to(codex_images.ROOT).as_posix())
    item['label'] = f'{item["title"]} · Design {len(ensure(s)["designs"])}'
    return item


def book(s, offer, day, time, who):
    contact(s, who)
    if offer not in BOOKINGS:
        raise ValueError('Choose a listed outing.')
    venue, price, duration = BOOKINGS[offer]
    if s['world']['money'] < price:
        raise ValueError('Not enough money.')
    event = scheduled_events.create(s, offer, day, time, venue, [who], duration)
    spend(s, price, offer)
    return record(s, 'bookings', event=event['id'], title=offer, price=price)


def cancel_booking(s, ident):
    item = next((b for b in ensure(s)['bookings'] if b['id'] == ident), None)
    if not item:
        raise ValueError('Booking not found.')
    event = next(e for e in s['scheduled_events'] if e['id'] == item['event'])
    if item.get('refunded') or s['world']['minute'] >= event['start']:
        raise ValueError('Refunds are available once, before the booking starts.')
    scheduled_events.cancel(s, event)
    s['world']['money'] += item['price']
    record(s, 'receipts', title='Refund · '+item['title'], amount=-item['price'])
    item['refunded'] = True


def split_bill(s, total, people, title):
    title = text(title, 80)
    if not isinstance(total, int) or total <= 0 or not 2 <= people <= 12:
        raise ValueError('Enter a positive whole-dollar total and 2–12 diners.')
    # Player pays their rounded-up share; no invented transfers from NPCs.
    return spend(s, (total+people-1)//people, f'{title} · your 1/{people} share of ${total}')


def listings(s):
    day = s['world']['minute']//1440
    offers = [('Vintage sketchbook', 18, 'makerspace'), ('Wooden chess set', 25, 'library'),
              ('Pressed-flower frame', 14, 'flowers'), ('Pocket star atlas', 12, 'planetarium')]
    sellers = ('rei', 'april', 'emily', 'celeste')
    known = phone_apps.contacts(s)
    return [dict(id=f'{day}:{i}', title=title, price=price, venue=venue,
                 seller=camera.name(sellers[i]) if sellers[i] in known else 'Winterfield community stall',
                 seller_id=sellers[i] if sellers[i] in known else None, day=day)
            for i, (title, price, venue) in enumerate(offers)
            if town.hidden.visible_place(s, venue)]


def buy_listing(s, ident):
    listing = next((x for x in listings(s) if x['id'] == ident), None)
    if not listing:
        raise ValueError('This listing has expired.')
    if any(x['listing'] == ident for x in ensure(s)['purchases']):
        raise ValueError('You already bought this item.')
    spend(s, listing['price'], 'Exchange · '+listing['title'])
    return record(s, 'purchases', listing=ident, **{k: listing[k] for k in ('title', 'price', 'venue', 'seller', 'seller_id')}, collected=False)


def collect(s, ident):
    item = next((x for x in ensure(s)['purchases'] if x['id'] == ident), None)
    if not item or item['collected']:
        raise ValueError('There is no purchase waiting for collection.')
    if s['world']['location'] != item['venue'] or s['world']['cast'][s['player']].get('journey'):
        raise ValueError('Travel to '+town.LOCATIONS[item['venue']]+' to collect this item.')
    item['collected'] = True
    key = 'exchange:'+item['listing']
    s['world']['inventory'][key] = s['world']['inventory'].get(key, 0)+1
    town.log(s, 'Collected '+item['title']+' from the community stall.')
    seller = item.get('seller_id')
    if seller and town.present(s, seller):
        share(s, seller, 'an Exchange pickup', 'Collected '+item['title']+' while you were there.')


def save_recipe(s, title):
    if title not in RECIPES:
        raise ValueError('Recipe not found.')
    if title not in ensure(s)['recipes']:
        ensure(s)['recipes'].append(title)


def cook(s, title):
    if title not in ensure(s)['recipes'] or title not in RECIPES:
        raise ValueError('Save this recipe first.')
    scene = camera.scene(s)
    if not scene['at_home']:
        raise ValueError('Visit a home kitchen before cooking.')
    spend(s, RECIPES[title][0], 'Ingredients · '+title)
    note = f'{camera.name(s["player"])} cooked {title}.'
    record(s, 'cooked', title=title, companions=scene['companions'])
    s['world']['camera_activity'] = dict(text=title, location=s['world']['location'], minute=s['world']['minute'])
    s.setdefault('shared_events', []).append(dict(minute=s['world']['minute'], text=note, witnesses=scene['companions']))
    town.log(s, note)


def send_postcard(s, photo_id, who, message):
    contact(s, who)
    message = text(message)
    photo = next((p for p in camera.photos(s) if p['id'] == photo_id), None)
    if not photo or not camera.photo_path(photo).is_file():
        raise ValueError('Choose an available Gallery photo.')
    postcard = record(s, 'postcards', recipient=who, message=message, photo=copy.deepcopy(photo))
    share(s, who, 'a postcard', dict(message=message, location=photo['location'], date=photo['date']))
    # A real outgoing photo message, understood by the existing message renderer.
    s['routes'][who]['history'].append(dict(role='user', channel='text', minute=s['world']['minute'],
                                           content=message, photo=copy.deepcopy(photo)))
    import messaging
    messaging.mark_inbox_activity(s, s['routes'][who])
    return postcard


def join_club(s, club):
    if club not in CLUBS:
        raise ValueError('Choose a campus club.')
    ensure(s)['clubs'].setdefault(club, dict(joined=s['world']['minute'], completed=[]))


def complete_assignment(s, club):
    if club not in ensure(s)['clubs']:
        raise ValueError('Join this club first.')
    venue, task = CLUBS[club]
    day = s['world']['minute']//1440
    done = ensure(s)['clubs'][club]['completed']
    if day in done:
        raise ValueError('Today’s practice is already complete.')
    if s['world']['location'] != venue or s['world']['cast'][s['player']].get('journey'):
        raise ValueError('Visit '+town.LOCATIONS[venue]+' for this practice.')
    done.append(day)
    town.log(s, club+' practice: '+task)


def enroll(s, course):
    if course not in COURSES:
        raise ValueError('Choose an available course.')
    ensure(s)['courses'].setdefault(course, dict(enrolled=s['world']['minute'], submitted=[]))


def submit_assignment(s, course, response):
    response = text(response, 2000)
    if course not in ensure(s)['courses']:
        raise ValueError('Enroll in this course first.')
    data = ensure(s)['courses'][course]
    week = s['world']['minute']//(7*1440)
    if any(x['week'] == week for x in data['submitted']):
        raise ValueError('This week’s assignment is already submitted.')
    data['submitted'].append(dict(week=week, minute=s['world']['minute'], response=response))
    town.log(s, 'Submitted this week’s '+course+' assignment.')


def context(s, members):
    d = ensure(s)
    return dict(shared_items=[copy.deepcopy(x) for x in d['shares'] if x['recipient'] in members][-12:],
                instruction='Only each named recipient knows their shared items. Sharing is not proof of liking, '
                'listening, replying, or accepting a new invitation. Never invent those actions.')
