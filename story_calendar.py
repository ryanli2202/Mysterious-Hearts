"""Winterfield's calendar, derived from the existing save's elapsed minutes."""
import custom_protagonist
import calendar
import re
from datetime import date, timedelta
from functools import lru_cache
import hidden_cast
from dataclasses import dataclass

START = date(2050, 1, 1)
LEGACY_START = date(2024, 1, 1)
BIRTHDAYS = {'garrett':'August 18', 'rei':'February 18', 'minsu':'May 2', 'ivan':'March 4',
             'emily':'November 4', 'sophie':'April 28', 'amy':'August 8',
             'samantha':'January 31', 'april':'September 9', 'yuriko':'March 12'}
BIRTHDAYS.update({key: p['birthday'] for key, p in hidden_cast.CAST.items()})
FESTIVALS = {(4, 1):"April Fools’ Day", (10, 31):'Halloween'}
ACTIVITIES = {'April Fools’ Day':'Trade harmless pranks in the square',
              'Halloween':'Join the costume walk', 'Christmas':'Join the Christmas celebration',
              'Thanksgiving':'Share Thanksgiving dinner', 'New Year’s Day':'Make a New Year’s wish'}
MOMENTS = {'April Fools’ Day':'Someone has tied tiny paper neckties to every pigeon statue in the square.',
           'Halloween':'A little ghost lifts a corner of their sheet to inspect the candy bowl.',
           'Christmas':'The lights come on all at once. A few people miss their cue in the carol and start laughing.',
           'Thanksgiving':'There is one slice of pie left. Everyone cuts it a little smaller until there is enough to pass around.',
           'New Year’s Day':'The wish cards flutter on their ribbons as another one joins the tree.'}

@dataclass(frozen=True)
class Outing:
    title: str
    venue: str
    activities: dict


OUTINGS = {
    (1, 6): Outing('Golden Dragon Broth Swap', 'noodle_shop', {
        'Try the blind tasting': 'Two cups look identical. At the bottom of the second is a sliver of toasted ginger that gives the cook away.',
        'Write a recipe card': 'There is room for six lines on the exchange card. The instruction that needs a seventh ends up squeezed sideways along the edge.'}),
    (5, 11): Outing('Boathouse Launch Day', 'sailing_club', {
        'Tie a rescue line': 'The rope slips loose on the first pull. On the second it holds, and the little practice dinghy noses neatly against the dock.',
        'Race a model dinghy': 'The smallest paper sail catches the breeze first. Its boat finishes backwards to a cheer from the dock.'}),
    (9, 14): Outing('Bijou Lobby Card Ballot', 'cinema', {
        'Sketch a lobby card': 'The volunteer clips the drawing onto a length of twine. A patron stops beneath it to guess the film from the picture.',
        'Vote for the second feature': 'The ballot box is an old film can. Each folded vote makes a little metallic tick when it lands.'}),
}


def story_date(minute):
    return START + timedelta(days=minute // 1440)

def migrate_journals(s):
    old_start = date(s.get('calendar_start_year', LEGACY_START.year), 1, 1)
    old_stamps = {}
    if old_start != START:
        # Journal dates omit the year. Resolve them against days actually played.
        for offset in range(s['world']['minute'] // 1440 + 1):
            elapsed = timedelta(days=offset)
            old_stamps[f'{old_start + elapsed:%a, %b %d}'] = f'{START + elapsed:%a, %b %d}'
        for i, key in enumerate(s.get('celebrations', [])):
            stamp, title = key.split('/', 1)
            day = START + (date.fromisoformat(stamp) - old_start)
            s['celebrations'][i] = f'{day.isoformat()}/{title}'
    s['calendar_start_year'] = START.year

    def migrate_stamp(entry):
        stamp, separator, rest = entry.partition(' · ')
        match = re.fullmatch(r'Day ([1-9]\d*)', stamp)
        if separator and match:
            day = START + timedelta(days=int(match[1])-1)
            return f'{day:%a, %b %d}' + separator + rest
        return old_stamps.get(stamp, stamp) + separator + rest

    journals = [s['world']['log'], s['world'].get('home_journal', [])]
    journals.extend(b.get('events', []) for b in s['bond_details'].values())
    for relationship in s['relationships'].values():
        journals.append(relationship.get('milestones', []))
        for breakup in relationship.get('breakups', []):
            breakup['date'] = migrate_stamp(breakup['date'])
        firsts = relationship.get('firsts', {})
        for kind, stamp in firsts.items():
            firsts[kind] = migrate_stamp(stamp)
    for journal in journals:
        journal[:] = [migrate_stamp(entry) for entry in journal]

@lru_cache(maxsize=32)
def holidays(year):
    days = {}
    for month, day, name in [(1,1,'New Year’s Day'), (6,19,'Juneteenth'), (7,4,'Independence Day'),
                              (11,11,'Veterans Day'), (12,25,'Christmas')]:
        actual = date(year, month, day)
        days[actual] = name
        if actual.weekday() >= 5:
            offset = -1 if actual.weekday() == 5 else 1
            days[actual + timedelta(days=offset)] = name + ' (observed)'
    for month, weekday, occurrence, name in [(1,0,3,'Martin Luther King Jr. Day'),
            (2,0,3,'Washington’s Birthday'), (5,0,-1,'Memorial Day'), (9,0,1,'Labor Day'),
            (10,0,2,'Columbus Day'), (11,3,4,'Thanksgiving')]:
        matching = [d for d in calendar.Calendar().itermonthdates(year, month)
                    if d.month == month and d.weekday() == weekday]
        days[matching[occurrence-1 if occurrence > 0 else -1]] = name
    return days

@lru_cache(maxsize=800)
def holiday(day):
    return holidays(day.year).get(day) or holidays(day.year + 1).get(day)

def free_day(day):
    return day.weekday() >= 5 or bool(holiday(day))

def events(s, day):
    result = []
    outing = OUTINGS.get((day.month, day.day))
    if outing:
        result.append((outing.title, 'Choose an activity', None))
    for title in (holiday(day), FESTIVALS.get((day.month, day.day))):
        if title:
            result.append((title, ACTIVITIES.get(title, 'Celebrate ' + title), None))
    birthday = f'{calendar.month_name[day.month]} {day.day}'
    for who, when in BIRTHDAYS.items():
        if when == birthday and hidden_cast.known(s, who):
            title = who.title() + '’s birthday'
            result.append((title, 'Celebrate ' + title, who))
    return result

def context(s):
    day = story_date(s['world']['minute'])
    return dict(date=day.strftime('%A, %B %d, %Y'), day_off=free_day(day),
                occasions=[title for title, _, _ in events(s, day)])

def outing_companions(s):
    import town
    stats = {**s['friendships'], **s['relationships']}
    return [who for who, r in stats.items() if who != s['player']
            and hidden_cast.known(s, who)
            and (town.social_world.friendship(s, who) in ('Friends', 'Close friends', 'Best friends', 'Siblings')
                 or r['status'] in town.ROMANTIC_STATUSES
                 or (r['status'] == 'acquaintances' and r['closeness'] >= 6))
            and (town.present(s, who) or (who in s['routes'] and hidden_cast.contact(s, who)))]


def celebrate(s, title, companion=None, activity_choice=None):
    import town
    day = story_date(s['world']['minute'])
    for event, activity, who in events(s, day):
        if title != event: continue
        key = day.isoformat() + '/' + title
        done = s.setdefault('celebrations', [])
        if key in done: return False
        outing = OUTINGS.get((day.month, day.day))
        if outing and outing.title == title:
            if s['world']['location'] != outing.venue:
                raise ValueError('Travel to ' + town.LOCATIONS[outing.venue] + ' in Town first.')
            if companion not in outing_companions(s) or activity_choice not in outing.activities:
                raise ValueError('Choose a friend or partner and one of the listed activities.')
            if companion in s['routes'] and hidden_cast.contact(s, companion):
                town.summon(s, companion)
            name = s.get('nicknames', {}).get(companion) or companion.title()
            note = (f'{custom_protagonist.display_name(s["player"])} and {name} attended {title} together. '
                    f'{activity_choice}. {outing.activities[activity_choice]}')
            if outing.venue == 'sailing_club':
                import weather
                if weather.shelter(s['world']['minute']):
                    note = (f'{custom_protagonist.display_name(s["player"])} and {name} attended {title} together under the boathouse awning. '
                            + ('They tested a rescue line on a practice cleat.' if activity_choice == 'Tie a rescue line'
                               else 'They raced model dinghies in the sheltered demonstration trough.')
                            + ' Rain kept the full-sized boats ashore.')
            done.append(key)
            s.setdefault('shared_events', []).append(dict(minute=s['world']['minute'], text=note, witnesses=[companion]))
            relationship = town.character_stats(s, companion)
            relationship['closeness'] = min(100, relationship['closeness'] + 2)
            town.relationship_notice(s, companion, note)
            town.log(s, note)
            return note
        done.append(key)
        moment = ('The candles are lit and everyone sings for ' + who.title() + '.' if who else MOMENTS.get(title, 'The town takes a break to mark the occasion.'))
        note = f'{custom_protagonist.display_name(s["player"])} celebrated {title}. ' + moment
        witnesses = set(s['world'].get('party', []))
        if who and who != s['player']: witnesses.add(who)
        witnesses.update(k for k,r in s['routes'].items() if r.get('channel') == 'in_person'
                         and k != s['player'] and town.loop.together(s,k))
        s.setdefault('shared_events', []).append(dict(minute=s['world']['minute'], text=note,
                                                       witnesses=sorted(witnesses)))
        if who and who != s['player']:
            s['routes'][who]['history'].append({'role':'status', 'content':note})
        town.log(s, note)
        return note
    return False
