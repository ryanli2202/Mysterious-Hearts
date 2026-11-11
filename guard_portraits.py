"""Context-sensitive artwork for rotating guard roles and Richter's boss form."""
from pathlib import Path

ROOT=Path(__file__).resolve().parent
IDS=('yokai','oni','tengu','clubs','spades','affiliate','headhunter','seeker','pmc',
     'team9','interpol','kai_sentinel','kai_guard','lookout','crew_enforcer',
     'custom_awakened','custom_unawakened','custom_robotic','richter_cybernetic')

def path(ident):
    return ROOT/'assets'/'portraits'/'guards'/(ident+'.png') if ident in IDS else None

def type_id(s,kind):
    import organisation_guards as guards
    if kind in guards.TYPES:return kind
    row=s.get('organisation_guards',{}).get('types',{}).get(kind)
    return 'custom_'+row[1] if row and row[1] in ('awakened','unawakened','robotic') else None

def resolve(s,who,location=None):
    """Never replace ordinary Richter reception/contact art with his hidden form."""
    s=s or {}
    if who.startswith('guard_art_'):return path(who[len('guard_art_'):])
    f=s.get('combat',{}).get('active') or {}
    e=s.get('organisation_guards',{}).get('encounter') or {}
    if who==f.get('opponent') and (location is None or location==f.get('location')):
        if who=='Joseph Richter' and (e.get('scope')=='rei:richter' or f.get('opponent_profile',{}).get('portrait')=='richter_cybernetic'):
            return path('richter_cybernetic')
        ident=f.get('opponent_profile',{}).get('portrait')
        if ident in IDS:return path(ident)
        # Active encounters created before the art update still have a saved slot.
        ident=type_id(s,(e.get('slot') or {}).get('type'))
        if ident:return path(ident)
    if who.startswith('Post guard · '):
        import organisation_guards as guards
        row=guards.npc_rows(s).get(who)
        if row:return path(type_id(s,row['type']))
    if who=='Joseph Richter' and location=='blackstone_command':
        d=s.get('campaign_dialogue') or {}
        speaks=any(speaker==who for beat in d.get('beats',[]) for speaker,_ in beat['speeches'])
        if (d.get('action')=='rei_story.confront' or speaks or s.get('rei_story',{}).get('richter')):
            return path('richter_cybernetic')
    return None
