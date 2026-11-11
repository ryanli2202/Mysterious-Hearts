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
    import combat_identity
    player_line=LINES[kind].format(art=art)
    if kind in ('spar','challenge','learn'):
        voice=(s.get('custom_protagonist') or conversation_lore.speaker_reference(s['player'],[who],0,'Combat invitation',state=s))
        request_context=dict(player=s['player'],recipient=who,intent=kind,art=art,
            personality=voice,custom=s.get('custom_protagonist') if s['player'] not in __import__('game_core').PLAYERS else None,
            relationship=relationship_dynamics.stats(s,who),location=s['world']['location'],
            recent=s.get('combat',{}).get('dialogue',[])[-6:])
        invitation=combat.ask_ai('Write ONE brief spoken invitation in the protagonist voice. '
            'Preserve intent exactly: spar is friendly practice, challenge asks agreement to a fight, learn asks this teacher for the selected martial art. '
            'For learn include the exact art name. No attack, threat, wager, romance, invented grievance, private disclosure or completed lesson. '
            'Return intent unchanged and player_line. Context: '+json.dumps(request_context,ensure_ascii=False),
            combat.schema({'intent':{'type':'string','enum':[kind]},'player_line':{'type':'string'}}))
        player_line=invitation.get('player_line')
        if (invitation.get('intent')!=kind or not isinstance(player_line,str) or not 3<=len(player_line.strip())<=500
                or kind=='learn' and art.casefold() not in player_line.casefold()):
            raise ValueError('Invalid protagonist invitation; no encounter or lesson was started.')
        player_line=player_line.strip()
    reaction = combat.attack_reaction(s, who) if kind == 'attack' else None
    context = dict(character=who, player=s['player'], kind=kind, art=art, action=player_line,
        location=s['world']['location'], relationship=relationship_dynamics.stats(s, who),
        lore=conversation_lore.speaker_reference(who,[s['player']],0,'Combat response',state=s),
        combat_identity=combat_identity.public(s,who,[s['player']]),
        known_operational_reputations=combat_identity.public_titles(s,[s['player'],who]),
        recent=[r for r in s.get('combat', {}).get('dialogue', []) if r['who']==who][-6:], allowed=allowed,
        reason=reason, attack_reaction=reaction)
    group=s.get('groups',{}).get(s.get('active_group'),{})
    if who in group.get('members',[]): context['conversation']=group.get('history',[])[-10:]
    prompt = ('Write a brief natural in-person response in this character’s voice and a short physical reaction. '
        'For invitations or lessons, accepted may be true only if allowed; you may decline based on character/context. '
        'For an attack, accepted must be true and the supplied flee/fight reaction is mandatory. '
        'Describe the player initiating the attack in narration as Game Master, followed by the physical reaction; '
        'never put the attack action in dialogue or invent a resolved hit or fight outcome. '
        'An attack permanently ruptures trust and ends an existing romantic relationship; reflect that if applicable. '
        'Respond to the exact requested kind: a challenge is an agreed fight, not a spar. Never accept by changing the selected activity. If you require a different activity, decline. A lesson stays with the selected art and takes thirty minutes. '
        'Do not narrate a completed lesson or fight. No invented shared history or gratuitous disclosure of private lore. Context: '+json.dumps(context))
    data = combat.ask_ai(prompt, combat.schema({'dialogue': {'type':'string'},
        'narration': {'type':'string'}, 'accepted': {'type':'boolean'}}))
    if (type(data.get('accepted')) is not bool or
        any(not isinstance(data.get(k), str) or not data[k].strip() or len(data[k])>4000
            for k in ('dialogue','narration'))):
        raise ValueError('Invalid dialogue response; retry without spending a turn.')
    if data['accepted'] and kind=='challenge' and any(x in data['dialogue'].casefold() for x in ('if you mean a spar', "let's spar", 'just a spar', 'only a spar')):
        raise ValueError('The response changed the requested fight into a spar; retry.')
    if data['accepted'] and not allowed or kind == 'attack' and not data['accepted']:
        raise ValueError('Response contradicted the encounter rules; retry.')
    return dict(id=uuid.uuid4().hex, who=who, kind=kind, art=art, location=s['world']['location'],
                minute=s['world']['minute'], player=s['player'], player_line=player_line, dialogue=data['dialogue'],
                narration=data['narration'], accepted=data['accepted'])

def commit(s, result):
    if any(r.get('id')==result['id'] for r in s.get('combat',{}).get('dialogue',[])):
        raise ValueError('This response has already been applied.')
    who, kind, art = result['who'], result['kind'], result['art']
    if result.get('player',s['player'])!=s['player']: raise ValueError('The protagonist changed; ask again.')
    if 'player_line' in result and (not isinstance(result['player_line'],str) or not result['player_line'].strip()): raise ValueError('Invalid saved invitation.')
    if s['world']['location'] != result['location'] or s['world']['minute'] != result['minute']:
        raise ValueError('The scene changed; ask again.')
    allowed, reason = eligibility(s, who, kind, art)
    if result['accepted'] and not allowed: raise ValueError(reason)
    record = copy.deepcopy(result)
    record['player_line'] = result.get('player_line',LINES[kind].format(art=art))
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
            dict(speaker=game_core.PLAYERS[s['player']],text=record['player_line'],channel='in_person',kind='action' if kind == 'attack' else 'dialogue'),
            dict(speaker='Narrator',text=record['narration']+' '+record['outcome'],channel='in_person'),
            dict(speaker=game_core.contact_name(s,who),text=record['dialogue'],channel='in_person')])
        if not group.get('open'):
            # Fleeing archived the hangout before this generated response was appended.
            for journal in reversed(s.get('hangout_journal',[])):
                if journal.get('members')==group['members'] and journal.get('ended')==s['world']['minute']:
                    journal['history']=copy.deepcopy(group['history'][group.get('journal_offset',0):])
                    break
    return record
