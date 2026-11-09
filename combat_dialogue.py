"""In-person combat requests: generated speech, authoritative game outcomes."""
import copy
import json
import uuid
import combat
from combat_profiles import TEACHERS

LINES = {'spar': 'Would you like to spar with me?',
         'challenge': 'I challenge you to a fight. Do you accept?',
         'attack': 'I attack you.', 'learn': 'Would you teach me {art}?'}

def eligibility(s, who, kind, art=None):
    combat.check_pair(s, who)
    if kind == 'learn':
        trial = copy.deepcopy(s)
        try: combat.train(trial, art, who)
        except ValueError as exc: return False, str(exc)
        return True, 'May agree to a thirty-minute lesson.'
    return combat.consent(s, who, kind)

def generate(s, who, kind, art=None):
    allowed, reason = eligibility(s, who, kind, art)
    import conversation_lore, relationship_dynamics
    reaction = combat.attack_reaction(s, who) if kind == 'attack' else None
    context = dict(character=who, player=s['player'], action=LINES[kind].format(art=art),
        location=s['world']['location'], relationship=relationship_dynamics.stats(s, who),
        lore=conversation_lore.character_tables().get(who, {}),
        recent=[r for r in s.get('combat', {}).get('dialogue', []) if r['who']==who][-6:], allowed=allowed,
        reason=reason, attack_reaction=reaction)
    group=s.get('groups',{}).get(s.get('active_group'),{})
    if who in group.get('members',[]): context['conversation']=group.get('history',[])[-10:]
    prompt = ('Write a brief natural in-person response in this character’s voice and a short physical reaction. '
        'For invitations or lessons, accepted may be true only if allowed; you may decline based on character/context. '
        'For an attack, accepted must be true and the supplied flee/fight reaction is mandatory. '
        'An attack permanently ruptures trust and ends an existing romantic relationship; reflect that if applicable. '
        'Do not narrate a completed lesson or fight. No invented shared history or gratuitous disclosure of private lore. Context: '+json.dumps(context))
    data = combat.ask_ai(prompt, combat.schema({'dialogue': {'type':'string'},
        'narration': {'type':'string'}, 'accepted': {'type':'boolean'}}))
    if (type(data.get('accepted')) is not bool or
        any(not isinstance(data.get(k), str) or not data[k].strip() or len(data[k])>4000
            for k in ('dialogue','narration'))):
        raise ValueError('Invalid dialogue response; retry without spending a turn.')
    if data['accepted'] and not allowed or kind == 'attack' and not data['accepted']:
        raise ValueError('Response contradicted the encounter rules; retry.')
    return dict(id=uuid.uuid4().hex, who=who, kind=kind, art=art, location=s['world']['location'],
                minute=s['world']['minute'], dialogue=data['dialogue'],
                narration=data['narration'], accepted=data['accepted'])

def commit(s, result):
    if any(r.get('id')==result['id'] for r in s.get('combat',{}).get('dialogue',[])):
        raise ValueError('This response has already been applied.')
    who, kind, art = result['who'], result['kind'], result['art']
    if s['world']['location'] != result['location'] or s['world']['minute'] != result['minute']:
        raise ValueError('The scene changed; ask again.')
    allowed, reason = eligibility(s, who, kind, art)
    if result['accepted'] and not allowed: raise ValueError(reason)
    record = copy.deepcopy(result)
    record['player_line'] = LINES[kind].format(art=art)
    record['outcome'] = 'Declined.'
    group=s.get('groups',{}).get(s.get('active_group'),{})
    if result['accepted']:
        if kind == 'learn': record['outcome'] = combat.train(s, art, who)
        else:
            fight = combat.start(s, who, kind)
            record['outcome'] = 'Continue to the fight.' if fight else 'They ran away. The relationship is permanently ruptured.'
    combat.ensure(s).setdefault('dialogue', []).append(record)
    if who in group.get('members',[]):
        import game_core
        group.setdefault('history',[]).extend([
            dict(speaker=game_core.PLAYERS[s['player']],text=record['player_line'],channel='in_person'),
            dict(speaker='Narrator',text=record['narration']+' '+record['outcome'],channel='in_person'),
            dict(speaker=game_core.contact_name(s,who),text=record['dialogue'],channel='in_person')])
        if not group.get('open'):
            # Fleeing archived the hangout before this generated response was appended.
            for journal in reversed(s.get('hangout_journal',[])):
                if journal.get('members')==group['members'] and journal.get('ended')==s['world']['minute']:
                    journal['history']=copy.deepcopy(group['history'][group.get('journal_offset',0):])
                    break
    return record
