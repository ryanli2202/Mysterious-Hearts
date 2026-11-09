"""Stable fictional phone numbers and a save-scoped address book."""
import re

# Append new residents; never reorder this registry or recycle a number.
RESIDENTS = ('garrett', 'rei', 'minsu', 'ivan', 'yuriko', 'emily', 'sophie', 'amy',
    'samantha', 'april', 'lena', 'naomi', 'celeste', 'dev', 'rosa', 'elliot', 'tyler',
    'valentina', 'daniel', 'sylvanis', 'Maya', 'Theo', 'June', 'Noah', 'Iris', 'Leo',
    'Mario Romano', 'Robin Vale', 'Dana Lin', 'Joseph Richter', 'neo', 'alyssa',
    'Priya Shah', 'Otis Bell', 'Nadia Flores', 'Ben Okafor', 'Tess Morgan',
    'Farah Haddad', 'Gabe Turner', 'Wren Park', 'Celia Brooks', 'Arthur Finch',
    'Luz Moreno', 'Samir Dutta')
import outskirts
RESIDENTS += outskirts.NAMES
import four_aces
RESIDENTS += four_aces.IDS
RESIDENTS += ('crow', 'takeo')
RESIDENTS += ('Keisuke Hachimura',)
import gang_leaders
RESIDENTS += gang_leaders.NAMES
RESIDENTS += ('thirteen',)
import gang_members
RESIDENTS += gang_members.NAMES
import street_recruits
RESIDENTS += street_recruits.NAMES
RESIDENTS += ('charles',)
RESIDENTS += ('fox', 'gordon')  # Append only: preserve every existing number.
# Charles retains his stable private registry slot.
NUMBERS = {who: f'1202555{100+i:04d}' for i,who in enumerate(RESIDENTS)}


def normalize(value):
    if not isinstance(value,str) or not re.fullmatch(r'\+?[\d ()\-.]+',value.strip()):
        raise ValueError('Enter a phone number using digits, with an optional +1 country code.')
    digits = re.sub(r'\D','',value)
    if len(digits)==10: digits='1'+digits
    if len(digits)!=11 or not digits.startswith('1'):
        raise ValueError('Enter the full ten-digit number, optionally starting with +1.')
    return digits


def format_number(value):
    n=normalize(value)
    return f'+1 ({n[1:4]}) {n[4:7]}-{n[7:]}'


def ensure(s):
    import keisuke
    keisuke.ensure(s)
    gang_leaders.ensure(s)
    import gang_members
    gang_members.ensure(s)
    import hidden_cast
    d=s.setdefault('phone_numbers',{})
    directory=d.setdefault('directory',{})
    import custom_protagonist
    if custom_protagonist.is_custom(s['player']):
        directory.setdefault(s['player'], '12025550199')
    for who,number in NUMBERS.items(): directory.setdefault(who,number)
    import charles_han
    saved=d.setdefault('contacts',{})
    if not charles_han.number_allowed(s):
        directory.pop('charles',None); saved.pop('charles',None)
    else:
        saved.setdefault('charles',dict(number=NUMBERS['charles'],source='Private direct contact',minute=None))
    import the_crow
    if not the_crow.number_allowed(s): saved.pop('crow', None)
    import takeo
    if not takeo.number_allowed(s): saved.pop('takeo', None)
    import thirteen
    thirteen.ensure(s)
    d.setdefault('draft','')
    # Existing contacts retain access. Unknown residents are not listed in the UI.
    known=[s['player'],*[who for who in s.get('routes',{}) if hidden_cast.contact(s,who)],
           *s.get('npc_chats',{})]
    for who in known:
        if who == 'takeo' and not takeo.number_allowed(s): continue
        if who == 'thirteen' and not thirteen.number_allowed(s): continue
        if who in directory:
            saved.setdefault(who,dict(number=directory[who],source='Existing contact',minute=None))
    return d


def number(s,who):
    value=ensure(s)['directory'].get(who)
    if not value: raise ValueError('This resident does not have an assigned phone number.')
    return format_number(value)


def saved_number(s,who):
    item=ensure(s)['contacts'].get(who)
    return format_number(item['number']) if item else None


def name(who):
    import game_core
    return game_core.CONTACTS.get(who,(who,))[0]


def add(s,value,source='Added by number'):
    import hidden_cast
    import groups
    canonical=normalize(value)
    # Validate before migration so invalid input cannot change the address book.
    directory={**NUMBERS,**s.get('phone_numbers',{}).get('directory',{})}
    who=next((who for who,number in directory.items() if number==canonical),None)
    import charles_han
    if who == 'charles' and not charles_han.number_allowed(s):
        raise ValueError('Charles has not shared his private number with you.')
    import the_crow
    if who == 'crow' and (not the_crow.number_allowed(s) or not hidden_cast.known(s, who)):
        raise ValueError('The Crow reserves his number for known high-ranking Syndicate officials.')
    import takeo
    if who == 'takeo' and (not takeo.number_allowed(s) or not hidden_cast.known(s, who)):
        raise ValueError('Meet Takeo and earn Shinokami Regional commander rank in good standing first.')
    import keisuke
    if who == keisuke.NAME and not keisuke.member(s):
        raise ValueError('Join the Shinokami through Bubblegram to receive Keisuke’s contact.')
    import thirteen
    if who == 'thirteen' and not thirteen.number_allowed(s):
        raise ValueError('Earn Shinokami Executive rank in good standing to contact Number Thirteen.')
    if who is None: raise ValueError('No Winterfield resident has that number. Check the digits.')
    if who in gang_members.MEMBERS and who not in s.get('npc_chats',{}):
        raise ValueError('Join this gang or meet this coworker in person before adding their number.')
    if who in gang_leaders.BY_NAME and who not in s.get('npc_chats',{}):
        raise ValueError('Join this gang or meet its leader in person before adding their number.')
    import custom_protagonist
    if custom_protagonist.is_custom(s['player']) and not hidden_cast.known(s, who) and source != 'Meet-Cute' and who != s['player']:
        raise ValueError('Meet this resident while travelling or exchange numbers through Meet-Cute first.')
    if who==s['player']: raise ValueError('That is your own number. It is already on your contact card.')
    d=ensure(s)
    if who in d['contacts']: return who
    if who in hidden_cast.ensure(s):
        discovery=hidden_cast.ensure(s)[who]
        discovery.update(online=True,contact=True)
        stats=s['relationships'].get(who,s['friendships'].get(who))
        if stats and stats['status']=='strangers':stats['status']='acquaintances'
    elif who not in s['routes']:
        chat=s.setdefault('npc_chats',{}).setdefault(who,{'history':[]})
        chat.setdefault('connection',dict(status='acquaintances',trust=35,closeness=0))
        groups.sync_contacts(s)
    d['contacts'][who]=dict(number=canonical,source=source,minute=s['world']['minute'])
    app=s.get('meet_cute',{})
    match=app.get('matches',{}).get(who)
    if match:
        match['numbers']=True
        match['phone_number']=format_number(canonical)
        app['revision']=app.get('revision',0)+1
    if who in s['routes']:
        s['routes'][who]['history'].append(dict(role='status',content=f'Saved {name(who)} as a phone contact · {format_number(canonical)}. This does not establish an in-person meeting.'))
    return who


def context(s,members):
    """Only numbers the player saved and the current speakers' own numbers."""
    d=ensure(s)
    return {who:format_number(d['contacts'][who]['number']) for who in members if who in d['contacts'] and (who != 'charles' or set(members)<={'charles',s['player']})}
