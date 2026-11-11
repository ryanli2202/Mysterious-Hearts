"""Pure custom identity views and explicit, save-local disclosures."""
import copy


def validate(raw):
    if not isinstance(raw, dict): raise ValueError('Identity settings must be an object.')
    result = {}
    for key in ('public_name', 'alias', 'nickname'):
        value = raw.get(key, '')
        if not isinstance(value, str) or len(value) > 60 or any(ord(c)<32 for c in value):
            raise ValueError('Identity names must be one line, up to 60 characters.')
        result[key] = value.strip()
    result['legal_public'] = raw.get('legal_public', True)
    if type(result['legal_public']) is not bool: raise ValueError('Choose legal-name visibility.')
    return result


def visible(profile, context='public', disclosed=(), familiar=False, state=None):
    ident = validate(profile.get('identity', {}))
    public = ident['public_name'] or profile.get('preferred_name') or (profile['name'] if ident['legal_public'] else 'New arrival')
    name = ident['alias'] if context=='underworld' and ident['alias'] else public
    data = dict(name=name, biography=profile.get('biography',''), hometown=profile.get('hometown',''),
                aspirations=profile.get('motivation',''), pronunciation=profile.get('pronunciation',''))
    if familiar and ident['nickname']: data['address'] = ident['nickname']
    if ident['legal_public'] or 'identity' in disclosed: data['legal_name'] = profile['name']
    if 'identity' in disclosed: data['alias'] = ident['alias']
    if 'history' in disclosed: data['disclosed_history'] = profile.get('private_history','')
    data['employment'] = (state.get('world',{}).get('job') or 'No current employment') if state else profile.get('occupation','')
    origin=profile.get('origin',{})
    if origin.get('prior_job'):
        import job_apps
        data['prior_work']=job_apps.JOBS[origin['prior_job']]['ranks'][origin.get('prior_rank',0)]+' (past experience, not current authority)'
    if origin.get('background') in __import__('character_origins').BACKGROUNDS[:9]:
        data['starting_background']=origin['background']
    if context=='underworld':
        membership=(state or {}).get('job_apps',{}).get('membership')
        if membership: data['recognised_role']={k:membership[k] for k in ('faction','branch','rank')}
        data.pop('biography',None); data.pop('hometown',None); data.pop('prior_work',None)
        if not ident['legal_public'] and 'identity' not in disclosed: data.pop('legal_name',None)
    return data


def disclose(state, observer, kind):
    if kind not in ('identity','history'): raise ValueError('Choose identity or history disclosure.')
    if not isinstance(observer,str) or not observer: raise ValueError('Choose a recipient.')
    known = state.setdefault('custom_disclosures', {}).setdefault(observer, [])
    if kind not in known: known.append(kind)


def dialogue(state, observer):
    p = state.get('custom_protagonist')
    if not p: return None
    connection=state.get('npc_chats',{}).get(observer,{}).get('connection',{})
    familiar=connection.get('status','strangers') not in ('strangers','acquaintance')
    route=state.get('routes',{}).get(observer,{})
    familiar=familiar or route.get('affection',0)>=40
    membership=state.get('job_apps',{}).get('membership') or {}
    faction=__import__('criminal_dynamics').faction(observer)
    underworld=bool(membership and faction==membership.get('faction','').lower())
    result=visible(p,context='underworld' if underworld else 'public',disclosed=state.get('custom_disclosures',{}).get(observer,[]), familiar=familiar,state=state)
    result['witnessed_trait_applications']=copy.deepcopy(state.get('trait_application_witnesses',{}).get(observer,[])[-10:])
    return result


def audience(state, observers):
    p=state.get('custom_protagonist')
    if not p: return None
    common={'identity','history'} if observers else set()
    for who in observers: common &= set(state.get('custom_disclosures',{}).get(who,[]))
    return visible(p,disclosed=common,state=state)
