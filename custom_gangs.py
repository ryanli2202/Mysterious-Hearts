"""Save-local founder rosters, voluntary recruitment and assimilation offers."""
import job_apps as jobs
import town_residents
import street_recruits

# Existing adult residents retain their ordinary routines and personal histories.
RECRUITS = {
    'Gabe Turner': ('Quartermaster', 20, 40),
    'Ben Okafor': ('Quartermaster', 25, 45),
    'Nadia Flores': ('Coordinator', 30, 50),
    'Tess Morgan': ('Treasurer', 30, 50),
    'Wren Park': ('Envoy', 25, 45),
    'Farah Haddad': ('Deputy', 40, 60),
}
RECRUITS.update(street_recruits.RECRUITS)
ROLES = {
    'Member': 'No operation bonus; any number of members.',
    'Deputy': '+1 gang standing on a successful crew, network or leadership contract.',
    'Quartermaster': '+$50 on a successful crew, network or leadership contract.',
    'Coordinator': 'Reduces crew, network or leadership contract heat gain by 1.',
    'Treasurer': '+$50 on a successful crew, network or leadership contract.',
    'Envoy': '+1 relation with existing diplomatic contacts after a successful crew, network or leadership contract.',
}


def sync(s, d):
    g = d.get('gang') or {}
    if g.get('role') != 'Founder' or g.get('id') or g.get('established'): return
    g.setdefault('members', {})
    g.setdefault('charter', 'Independent crew')
    g.setdefault('assimilation', {})
    if not d.get('membership'):
        for faction, minimum in (('Syndicate', 60), ('Shinokami', 70)):
            if d['reputation'] >= minimum and faction not in g['assimilation']:
                g['assimilation'][faction] = dict(status='offered', reputation=d['reputation'], minute=s['world']['minute'])
                d['history'].append(dict(private=True, minute=s['world']['minute'], text=f'{faction} offers to assimilate {g["name"]}. Review the terms in Bubblegram → My gang.'))


def crew(s):
    d = jobs.ensure(s); g = d.get('gang') or {}
    if g.get('role') != 'Founder' or g.get('id') or g.get('established'):
        raise ValueError('Found your own gang first; existing organisations retain their own members.')
    return g


def capacity(g): return 3 + 2 * g.get('rank', 0)


def location(s, name):
    return town_residents.routine(name, s['world']['minute'])


def reason(s, name):
    g = crew(s)
    if name not in RECRUITS: return 'Choose a listed recruit.'
    if name in g['members']: return 'Already a member.'
    if len(g['members']) >= capacity(g): return 'Roster full. Advance your gang to increase capacity.'
    _, rep, trust = RECRUITS[name]
    if s['job_apps']['reputation'] < rep: return f'Requires reputation {rep}.'
    connection = s.get('npc_chats', {}).get(name, {}).get('connection', {})
    if connection.get('trust', 0) < trust: return f'Build trust to {trust} through conversations first.'
    if s['job_apps']['heat'] >= 30: return 'Reduce heat below 30.'
    return ''


def recruit(s, name):
    issue = reason(s, name)
    if issue: raise ValueError(issue)
    venue = location(s, name)
    if not venue: raise ValueError('This resident is off duty. Return between 08:00 and 22:00.')
    jobs.guard(s, venue, 15)
    if s['job_apps']['pending']: raise ValueError('Finish your assignment before recruitment.')
    g = crew(s)
    g['members'][name] = dict(role='Member', joined=s['world']['minute'])
    jobs.careers.spend_time(s, 15, 2)
    return jobs.log(s, name+' voluntarily joined '+g['name']+'. Their ordinary town routine continues.', True)


def assign(s, name, role):
    g = crew(s)
    if name not in g['members'] or role not in ROLES: raise ValueError('Choose a current member and a listed role.')
    if s['job_apps']['pending']: raise ValueError('Finish your assignment before changing roles.')
    if role != 'Member' and any(n != name and p['role'] == role for n,p in g['members'].items()):
        raise ValueError('That officer role is occupied. Reassign its holder first.')
    g['members'][name]['role'] = role
    return jobs.log(s, name+' assigned as '+role+'.', True)


def dismiss(s, name):
    g = crew(s)
    if s['job_apps']['pending']: raise ValueError('Finish your assignment before changing the roster.')
    if name not in g['members']: raise ValueError('Choose a current member.')
    del g['members'][name]
    return jobs.log(s, name+' left the roster. Their town life and relationship are retained.', True)


def charter(s, value):
    g = crew(s); value = value.strip()
    if not 3 <= len(value) <= 120: raise ValueError('Use a charter between 3 and 120 characters.')
    g['charter'] = value
    return jobs.log(s, 'Gang charter updated: '+value, True)


def respond(s, faction, accept=False, branch=None):
    g = crew(s); offer = g['assimilation'].get(faction)
    if not offer or offer['status'] != 'offered': raise ValueError('Choose an outstanding assimilation offer.')
    if not accept:
        offer['status'] = 'declined'
        return jobs.log(s, faction+' assimilation declined. Independence retained; no penalty.', True)
    branch = branch or ('Clubs' if faction == 'Syndicate' else 'Shinokami')
    if branch not in jobs.BRANCHES or jobs.BRANCHES[branch][0] != faction: raise ValueError('Choose a branch of the offering faction.')
    if s['job_apps']['pending']: raise ValueError('Finish your assignment first.')
    # The existing sponsorship gates and clearance ladder still apply.
    jobs.sponsor(s, branch)
    g['parent_faction'] = faction
    for other, invitation in g['assimilation'].items():
        if invitation['status'] == 'offered': invitation['status'] = 'accepted' if other == faction else 'closed'
    return jobs.log(s, g['name']+' assimilated into '+faction+'. Name, roster and roles retained; faction sponsorship is binding and starts at probation.', True)


def operation(s, key, success):
    g = s['job_apps'].get('gang') or {}
    if key not in ('crew', 'network', 'leadership'): return 0
    roles = {p['role'] for p in g.get('members', {}).values()}
    d = s['job_apps']
    if 'Coordinator' in roles: d['heat'] = max(0, d['heat']-1)
    if not success: return 0
    if 'Deputy' in roles: g['standing'] += 1
    if 'Envoy' in roles:
        book = s.get('crime_diplomacy', {}).get('organisations', {}).get('crew:'+g['name'].casefold(), {})
        for target in book.get('relations', {}): book['relations'][target] = min(100, book['relations'][target]+1)
    # Staffed properties provide practical security support to crew contracts.
    security=s.get('organisation_guards',{})
    staffed={r['venue'] for r in security.get('roster',[]) if security.get('properties',{}).get(r['venue'],{}).get('owner')==g.get('name')}
    if success and staffed: d['heat']=max(0,d['heat']-min(3,len(staffed)))
    return 50 * len(roles & {'Quartermaster', 'Treasurer'})
