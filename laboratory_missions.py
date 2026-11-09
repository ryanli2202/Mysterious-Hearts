"""Private, in-person Glasshouse reviews; authored decisions, never drug recipes."""
import copy
import criminal_dynamics as canon

OPERATIVES = frozenset(('ivan', 'martos', 'elias', 'camila', 'mavis'))
# Each choice has an explicit local outcome. Readiness is preparation, not conquest.
MISSIONS = {
    'blue': dict(title='Blue Magic: short-window assessment', specialist='martos', requires=(),
        stages=(('Martos compares Blue Magic reports: the superhuman window lasts only minutes and recovery varies.',
                 ('Record the weakest recovery result', 'Use only the strongest result')),
                ('A security brief assumes the temporary awakening lasts through a whole deployment.',
                 ('Correct the brief and require a fallback', 'Leave the optimistic assumption')))),
    'red': dict(title='Red Magic: adverse-effect review', specialist='mavis', requires=(),
        stages=(('Mavis finds that Red Magic reports show greater power alongside worse disorientation and physical strain.',
                 ('Retain every adverse-effect report', 'Set aside the inconvenient reports')),
                ('Sylvanis wants a decision on the disputed research file before further consideration.',
                 ('Flag the file for restricted review', 'Mark the file ready despite the unresolved risks')))),
    'accounts': dict(title='Supply ledger: rival demands', specialist='camila', requires=('blue', 'red'),
        stages=(('Camila compares Syndicate and local-gang demand for Blue Magic and Red Magic. Buyers fear larger powers, while Red Dragons reject narcotics.',
                 ('Separate verified obligations from rumours', 'Treat every rumour as a confirmed obligation')),
                ('Support for Shinokami expansion could create financial dependence, but the current ledger has gaps.',
                 ('Record limits before proposing commitments', 'Recommend commitments without resolving the gaps')))),
    'cover': dict(title='Hearts brief: outward cooperation', specialist='elias', requires=('blue', 'red'),
        stages=(('Elias prepares an internal draft describing Syndicate support for Shinokami expansion. The future betrayal must remain compartmentalised.',
                 ('Keep the draft limited to the outward agreement', 'Mix strategic assumptions into the draft')),
                ('The draft makes claims about Blue Magic and Red Magic that the research cannot support.',
                 ('Remove the unsupported claims', 'Retain the claims for impact')))),
    'strategy': dict(title='Sylvanis: Winterfield strategy review', specialist='sylvanis', requires=('accounts', 'cover'),
        stages=(('Sylvanis reviews the Aces’ work with Ivan’s cross-Suit remit. He handles Takeo directly; the Crow sets strategy through him.',
                 ('Reconcile the four specialist reports', 'Skip conflicts between the reports')),
                ('The plan is to assist Shinokami expansion and betray them later. Today’s decision concerns internal preparedness only.',
                 ('Keep the betrayal contingent on a later order', 'Recommend advancing despite unresolved exposure')))),
}


def read(s):
    return s.get('laboratory_missions', {}).get('people', {}).get(s['player'], {})


def private(s):
    w = s['world']; actor = w['cast'][s['player']]
    return (s['player'] in OPERATIVES and w['location'] == canon.LAB
            and actor['location'] == canon.LAB and not actor.get('journey')
            and not w.get('npcs')
            and all(who in canon.INNER for who, a in w['cast'].items()
                    if a['location'] == canon.LAB and not a.get('journey')))


def present(s, who):
    a = s['world']['cast'].get(who, {})
    return a.get('location') == canon.LAB and not a.get('journey') and a.get('activity') != 'Sleep'


def partner(s, key):
    specialist = MISSIONS[key]['specialist']
    return 'ivan' if s['player'] == specialist else specialist


def guard(s):
    if not private(s):
        raise ValueError('Private work requires Ivan or an Ace in the laboratory, with no uncleared listeners.')
    if s['world']['cast'][s['player']].get('activity') == 'Sleep':
        raise ValueError('Wake up before reviewing laboratory work.')


def data(s):
    return s.setdefault('laboratory_missions', {'version': 1, 'people': {}})['people'].setdefault(
        s['player'], dict(active=None, completed={}, history=[], readiness=0, concerns=0))


def begin(s, key):
    guard(s)
    if key not in MISSIONS: raise ValueError('Choose a laboratory assignment.')
    d = read(s); spec = MISSIONS[key]
    if d.get('active'): raise ValueError('Finish or abandon the current laboratory review first.')
    if s.get('careers', {}).get('active') or __import__('crime_operations').read(s).get('active'):
        raise ValueError('Finish your other work session first.')
    if any(k not in d.get('completed', {}) for k in spec['requires']):
        raise ValueError('Complete the prerequisite laboratory reviews first.')
    if key in d.get('completed', {}): raise ValueError('This review is already completed.')
    colleague = partner(s,key)
    if not present(s,colleague): raise ValueError('Your specialist colleague must be physically present and awake.')
    data(s)['active'] = dict(key=key, title=spec['title'], partner=colleague,
                            stages=copy.deepcopy(spec['stages']), choices=[], started=s['world']['minute'])
    return 'Private review opened with ' + colleague.title() + '.'


def choose(s, choice):
    guard(s)
    active = read(s).get('active')
    if not active or type(choice) is not int or choice not in (0,1):
        raise ValueError('Choose a response to the active review.')
    if not present(s,active['partner']): raise ValueError('Resume when your specialist colleague is here again.')
    active['choices'].append(choice)
    if len(active['choices']) < len(active['stages']):
        return 'Assessment recorded. Continue to the decision review.'
    d = data(s)
    quality = active['choices'].count(0)
    concerns = active['choices'].count(1)
    d['readiness'] += quality
    d['concerns'] += concerns
    outcome = ('Review completed: readiness +' + str(quality) + '; unresolved concerns +' + str(concerns) +
               '. Internal preparation only; no shipment, human trial, public statement or betrayal was executed.')
    record = dict(key=active['key'], title=active['title'], partner=active['partner'],
                  minute=s['world']['minute'], choices=copy.deepcopy(active['choices']),
                  decisions=[stage[1][choice] for stage, choice in zip(active['stages'],active['choices'])], outcome=outcome)
    d['completed'][active['key']] = copy.deepcopy(record)
    d['history'].append(record)
    d['active'] = None
    return outcome


def abandon(s):
    guard(s)
    if not read(s).get('active'): raise ValueError('No laboratory review is active.')
    data(s)['active'] = None
    return 'Review set aside without progress or reward. You may restart it.'


def context(s, who, listeners):
    if not s or who not in canon.INNER or not listeners or any(p not in canon.INNER for p in listeners): return {}
    # Only colleagues who actually participated receive the record.
    records = [r for owner, d in s.get('laboratory_missions', {}).get('people', {}).items()
               for r in d.get('history', []) if who in (owner, r['partner'])]
    return dict(recent=copy.deepcopy(records[-3:]), boundary='These are completed internal reviews only, not implemented shipments, human trials, territorial gains or betrayal.') if records else {}
