"""Authored everyday stories, repeat visits, public news and private discoveries."""
import custom_protagonist
import public_venues
import weather
import memory_store
import story_calendar as dates

PROJECTS = {
 'garrett': ('A broth worth keeping', 'noodle_shop', ('Comparing two ideas for a seasonal broth.', 'Testing a small batch after lunch.', 'Writing a recipe card for the kitchen.', 'Listening to the kitchen’s verdict on the finished recipe.'), 'Taste the trial broth', 'Garrett offered you a small tasting and wrote down your reaction before changing the recipe.'),
 'rei': ('Light on the landing', 'studio', ('Making studies for a painting of a stairwell.', 'Trying a cooler colour in the shadows.', 'Finishing the light across the landing.', 'Setting the painting aside before deciding what to change.'), 'Look at the colour study', 'Rei showed you a colour study and listened to which part caught your eye.'),
 'emily': ('A window arrangement', 'flowers', ('Choosing stems for the shop window.', 'Testing how the stems hold their shape.', 'Putting the arrangement in the window.', 'The finished arrangement stays up for the week.'), 'Help arrange the display', 'You held stems while Emily tried a less crowded arrangement.'),
 'sophie': ('An honest split', 'track', ('Planning a practice time trial.', 'Practising an even opening lap.', 'Running the practice trial.', 'Reviewing the splits and taking a recovery day.'), 'Time a practice lap', 'You timed a practice lap for Sophie; she kept the split in her training notes.'),
 'minsu': ('The study demonstration', 'campus', ('Choosing a topic for a study-group demonstration.', 'Building a simple teaching diagram.', 'Rehearsing the explanation.', 'Reviewing which explanation helped the study group.'), 'Test the explanation', 'Minsu tried his explanation with you and revised the confusing part.'),
 'amy': ('A small sketch series', 'park', ('Choosing three corners of campus to sketch.', 'Comparing the light in her first studies.', 'Selecting the drawings for a small display.', 'Keeping the rejected sketches for another attempt.'), 'Sit for a sketch study', 'You sat for a quick sketch while Amy tested the composition.'),
 'yuriko': ('A stubborn staircase', 'campus', ('Measuring a miniature staircase.', 'Testing the support beneath the landing.', 'Fitting the staircase into the set model.', 'Photographing the finished model before rehearsal.'), 'Hold the model steady', 'You held the model steady while Yuriko fitted the staircase.'),
 'april': ('A clear patch of sky', 'chess', ('Planning a public sky chart.', 'Checking the labels against her notes.', 'Finishing the chart for curious beginners.', 'Collecting questions for a revised chart.'), 'Read the draft chart', 'April asked you to read the draft sky chart and marked one unclear label.'),
 'samantha': ('The loaner kit', 'arena', ('Checking the condition of the loaner equipment.', 'Sorting usable straps from worn ones.', 'Putting the checked kit back on the shelf.', 'Watching whether beginners can find the right kit.'), 'Sort the loaner kit', 'You helped Samantha sort the loaner equipment without interrupting training.'),
}
REGULARS = {
 'cafe': ('Order a house tea · $4', 4, 'Maya', 'house tea'),
 'marios_pizza': ('Order a cheese corner · $5', 5, 'Mario Romano', 'cheese corner'),
 'cinema': ('Add a lobby-card sketch', 0, 'Bijou lobby', 'lobby-card sketch'),
 'flowers': ('Help water the window plants', 0, 'Emily', 'window plants'),
 'sailing_club': ('Practise a rescue knot', 0, 'Boathouse staff', 'rescue-knot practice'),
}
REGULARS.update({key: (v[3], v[4], v[0], v[5]) for key, v in public_venues.VENUES.items()})
IDENTITY = (
 'The 2050 electric harbour shuttle displays its next departure on a low-power e-paper board; paper tickets remain available.',
 'University repair lockers lend tools against a student card. The makerspace still teaches people how to mend their own things.',
 'Waterfront flood-height tiles are set into the rebuilt promenade; removable ramps keep the public entrances accessible.',
 'The Bijou projects restored films digitally but commissions hand-drawn lobby cards from local artists.',
)

def ensure(s):
    d=s.setdefault('living_world', dict(version=2, started=s['world']['minute']//1440,
        projects={}, visits={}, rituals={}, keepsakes=[], discoveries=[], mystery=[], reports=[]))
    if d.get('version',1)<2:
        baseline=min(3,max(0,s['world']['minute']//1440-d['started'])//2)*120
        for who in PROJECTS: d['projects'].setdefault(who,{}).setdefault('work_minutes',baseline)
        d['version']=2
    return d

def project(s, who):
    d = ensure(s); elapsed = max(0, s['world']['minute']//1440-d['started'])
    title, venue, stages, action, result = PROJECTS[who]
    record = d['projects'].get(who, {})
    # Preserve the stage reached before migration; future progress requires work.
    record = d['projects'].setdefault(who, record)
    if 'work_minutes' not in record:
        record['work_minutes'] = 0
    stage = min(3, record['work_minutes']//120)
    return dict(who=who, title=title, venue=venue, stage=stage, text=stages[stage], action=action,
                helped=record.get('helped', False), result=record.get('result'))

def record(s, key, text, owners, location=None):
    memory_store.add(s, source='living:'+key, text=text, owners=owners, minute=s['world']['minute'],
                     location=location, importance=3)

def participate(s, who):
    import town
    p = project(s, who)
    if who == s['player'] or not town.present(s, who): raise ValueError('Meet them in person first.')
    if p['helped']: raise ValueError('You already helped with this project.')
    if p['stage'] == 3: raise ValueError('This project is finished. Ask them how it went.')
    result = PROJECTS[who][4]
    ensure(s)['projects'].setdefault(who,{}).update(helped=True, result=result)
    record(s, 'project:'+who, result, [s['player'], who], s['world']['location'])
    town.log(s, result)

def visit(s):
    import town
    place=s['world']['location']; day=s['world']['minute']//1440; d=ensure(s)
    if place not in REGULARS: raise ValueError('There is no regular activity here.')
    if not public_venues.suitable(place, s['world']['minute']):
        raise ValueError('This activity starts at ' + str(public_venues.EVENING[place]) + ':00.')
    if place in public_venues.OUTDOORS and weather.shelter(s['world']['minute']):
        raise ValueError('Wait for better weather before starting this outdoor activity.')
    title, cost, host, item = REGULARS[place]
    previous=d['visits'].setdefault(place, [])
    if day in previous: raise ValueError('You have already done this today.')
    if s['world']['money'] < cost: raise ValueError('Not enough spending money.')
    s['world']['money']-=cost; previous.append(day)
    owners=[s['player'], host.lower() if host == 'Emily' else host]
    companions=[who for who in s['routes'] if who != s['player'] and town.present(s,who)
                and (who in s['world']['party'] or s['routes'][who].get('channel') == 'in_person')]
    owners += companions
    text=f"{custom_protagonist.display_name(s["player"])} returned for {item} at {town.LOCATIONS[place]}." if len(previous)>1 else f"{custom_protagonist.display_name(s["player"])} tried {item} at {town.LOCATIONS[place]}."
    if place=='sailing_club':
        text+=(' Rain moved the practice beneath the boathouse awning; nobody launched a boat.' if weather.shelter(s['world']['minute']) else ' The practice line held on the dock cleat; nobody launched a boat.')
    for who in companions:
        key=who+':'+place
        days=d['rituals'].setdefault(key, [])
        if day not in days: days.append(day)
        if len(days)==3: text+=f' Three separate visits with {who.title()} have made this a shared ritual.'
    if place=='cinema': d['keepsakes'].append(dict(day=day, place=place, text='Your lobby-card sketch is pinned beside the programme.'))
    record(s, f'visit:{place}:{day}', text, owners, place)
    town.log(s,text)
    s['world']['camera_activity'] = dict(text=text, location=place, minute=s['world']['minute'])

def news(s):
    day=dates.story_date(s['world']['minute']); rows=[]
    from datetime import timedelta
    for offset in range(-2,4):
        when=day+timedelta(days=offset)
        outing=dates.OUTINGS.get((when.month,when.day))
        if outing:
            phase='Today' if offset==0 else 'Preparing' if offset>0 else 'Afterward'
            details=('Activity tables are open today.' if offset==0 else 'Volunteers are setting out signs and preparing materials.' if offset>0 else 'The signs are coming down; the organisers are sorting materials for next year.')
            rows.append(dict(source='Winterfield community board', title=outing.title+' · '+phase,
                             text=f'{when:%b %d}: {details} Attendance is recorded separately.'))
    w=weather.at(s['world']['minute'])
    rows.append(dict(source='Municipal boathouse',title='Dock conditions',text='Rain practice moves under the boathouse awning: knots and model boats, no launch.' if weather.shelter(s['world']['minute']) else 'The dock is open for ordinary practice. Check with staff before launching.'))
    rows.append(dict(source='Winterfield civic bulletin · 2050',title='Around town',text=IDENTITY[(s['world']['minute']//1440)//2%len(IDENTITY)]))
    rows.append(dict(source='Bijou programme desk',title='This week at the Bijou',text=('A silent-comedy double feature; compare the hand-drawn lobby cards.','Restored adventure matinees; the lobby sketch table is open.','An animation retrospective; patrons can leave a drawing on the display.')[s['world']['minute']//10080%3]))
    return rows

MYSTERY = (
 ('Compare the dispatch totals', 'archive', 'A duplicate tally separates six packed crates from four collected crates. The correction reconciles those totals; it does not identify the handwriting or the driver.', 'Two crates remained at dispatch. Who authorised the collection?'),
 ('Check the public receiving procedure', 'interpol_hq', 'Dana explains that the receiving stamp records delivery acceptance, not the identity of a passenger. She provides a public records enquiry form, without confirming any investigation.', 'A dated dispatch authorisation could identify who ordered the collection.'),
 ('Review Mei’s dispatch index', 'noodle_shop', 'Mei sends an index entry matching the consignment number. Its authorisation page is missing from her copy. She can ask the former records custodian to look for it.', 'The missing authorisation page is the next lead. Charles’s location and motives remain unknown.'),
)

def investigate(s):
    import town
    d=ensure(s); index=len(d['mystery'])
    if s['player']!='garrett' or s.get('charles_lead')!='traced': raise ValueError('Read both of Mei’s original documents in Find Charles first.')
    if index>=len(MYSTERY): raise ValueError('All currently available leads have been examined.')
    title, place, finding, question=MYSTERY[index]
    if s['world']['location']!=place: raise ValueError('Visit '+town.LOCATIONS[place]+' to examine this lead.')
    if d['mystery'] and d['mystery'][-1]['day']==s['world']['minute']//1440: raise ValueError('The next response arrives on the next story day.')
    d['mystery'].append(dict(title=title, finding=finding, question=question, day=s['world']['minute']//1440))
    record(s,'mystery:'+str(index),finding+' Open question: '+question,[s['player']],place)
    town.log(s,finding)

def context(s, members):
    d=ensure(s); place=s['world']['location']; listeners=set(members)
    shared=[]
    for key,days in d['rituals'].items():
        who,venue=key.split(':')
        if len(days)>=3 and listeners=={who}: shared.append(f'{who} and the player returned to {venue} on {len(days)} different days.')
    projects={who:project(s,who) for who in members if who in PROJECTS}
    commitments=memory_store.open_commitments(s,[s['player'],*members])[-3:]
    regular_memory=[]
    for venue, days in d['visits'].items():
        host=REGULARS[venue][2]
        if host in members or host.lower() in members:
            regular_memory.append(f"{host} remembers {len(days)} visits for {REGULARS[venue][3]}. Ask whether they want the same again; do not presume an order.")
    return dict(weather=weather.at(s['world']['minute']), public_news=news(s), own_projects=projects,
                shared_rituals=shared, regular_memories=regular_memory,
                unfinished_conversations=[dict(text=r['text'],status=r['status']) for r in commitments],
                local_keepsakes=[k for k in d['keepsakes'] if k['place']==place][-3:],
                direction='Project progress is independent of the player. Only helped=true proves participation. Weather never moves a player or cancels an appointment; offer a sheltered alternative. Rituals recall actual visits, not automatic romance. Do not invent completed promises.')
