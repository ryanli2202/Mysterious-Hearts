"""Reviewed origin signatures and disposable combat using the real resolver."""
import copy
import json
import uuid
import combat_moves as moves
import combat_workshop as workshop
import character_origins as origins


def signature_context(profile):
    origin=origins.resolve(profile.get('origin',{}),profile.get('awakened',False),bool(profile.get('awakening_trait')))
    if origins.EXPERIENCES.index(origin['experience'])<3 or not profile.get('awakened') or not profile.get('trait_amplifications'):
        raise ValueError('Starting signatures require Veteran or higher and accepted custom Trait amplifications.')
    return dict(trait=profile['awakening_trait'],description=profile['awakening_description'],
                amplifications=profile['trait_amplifications'],specialisation=profile.get('specialisation',''))


def supported_roles(profile):
    return sorted({r for a in profile.get('trait_amplifications',[]) for r in a['compatible']})


def generate(profile,role,theme=''):
    import combat,combat_profiles
    before=signature_context(profile)
    if role not in supported_roles(profile): raise ValueError('The accepted aspects do not support that signature role.')
    p=combat_profiles.make('custom_signature_preview',dict(profile,starting_signature=None))
    data=dict(context=before,stats=p['stats'],role=role,visual_theme=theme[:200])
    response=combat.ask_ai('Generate exactly THREE distinct starting signature candidates from these accepted Trait aspects. '
        'Requested role must match every candidate and every referenced aspect must support that role. '
        'Visual theme is cosmetic only. Preserve domains, limits and bounded engine tags. No new powers, guaranteed hits or forms. '
        'Minimum mana is 5 plus 3 per additional aspect. Include setup and counterplay. DATA: '+json.dumps(data),
        combat.schema({'skills':{'type':'array','minItems':3,'maxItems':3,'items':workshop.skill_schema([a['id'] for a in moves.amps(p)])}}),max_tokens=3000)
    candidates=workshop.validate_skills(response.get('skills'),p)
    distinct_candidates(candidates)
    for skill in candidates: check_role(skill,p,role)
    return dict(context=workshop.fingerprint(before),candidates=candidates,role=role,theme=theme[:200])


def check_role(skill,p,role):
    if skill['role']!=role or any(role not in a['compatible'] for a in moves.amps(p) if a['id'] in skill['aspect_ids']):
        raise ValueError('Signature role is incompatible with its accepted aspects.')


def distinct_candidates(candidates):
    keys=('role','tags','aspect_ids','range','stamina','mana','hits','counter_kind')
    mechanics=[workshop.fingerprint({k:sorted(c[k]) if isinstance(c.get(k),list) else c.get(k) for k in keys}) for c in candidates]
    if len(set(mechanics))!=3: raise ValueError('Candidates must differ mechanically; renaming the same skill is not a new option.')


def accept(profile,batch,index):
    import combat_profiles
    before=signature_context(profile)
    if workshop.fingerprint(before)!=batch['context']: raise ValueError('Trait or specialisation changed; generate again.')
    p=combat_profiles.make('custom_signature_preview',dict(profile,starting_signature=None))
    candidates=workshop.validate_skills([dict(c,aspects=c['aspect_ids']) for c in batch['candidates']],p)
    distinct_candidates(candidates)
    for skill in candidates: check_role(skill,p,batch['role'])
    return dict(context=batch['context'],skill=candidates[index],role=batch['role'],theme=batch['theme'])


def validate_signature(profile,record,p):
    if not record: return None
    if record.get('context')!=workshop.fingerprint(signature_context(profile)): raise ValueError('Starting signature review is stale.')
    raw=record.get('skill',{})
    # The workshop validates batches; construct distinct names to revalidate one blueprint.
    raws=[dict(raw,aspects=raw.get('aspect_ids'),name=raw.get('name','')+suffix) for suffix in ('',' · validation B',' · validation C')]
    clean=workshop.validate_skills(raws,p)[0]
    check_role(clean,p,record.get('role'))
    if clean['id']!=raw.get('id'): raise ValueError('Starting signature blueprint changed.')
    return clean


def specialise(p,choice):
    if not choice: return
    amps=p['moveset']['amplifications']
    if choice not in {a['id'] for a in amps}: raise ValueError('Choose an accepted Trait aspect for specialisation.')
    for amp in amps:
        amp['mana']=max(2,amp['mana']-1) if amp['id']==choice else min(18,amp['mana']+1)


def interaction(p,move_id,amp_id=None):
    before=moves.selection(p,move_id); after=moves.selection(p,move_id,amp_id)
    return dict(move=after['name'],role=after['role'],base={k:before[k] for k in ('mana','stamina','range','tags')},
                amplified={k:after[k] for k in ('mana','stamina','range','tags')},
                environment=(after.get('amplification') or {}).get('environment','No amplification'),
                note='Costs and range use the execution resolver. Damage, counters and terrain outcomes depend on target, setup and rolls.')


def sandbox(profile,seed=1,opponent=None):
    import combat,combat_profiles,combat_engine
    p=combat_profiles.make('custom_practice',profile)
    q=copy.deepcopy(opponent) if opponent else combat_profiles.make('training_target',dict(awakened=False,origin=dict(experience='Trained',arts=['Boxing'])))
    f=dict(id=uuid.uuid4().hex,kind='spar',opponent='training_target',opponent_profile=q,location='training_room',
           player=combat.resources(p),enemy=combat.resources(q),elapsed=0,turn=0,log=[],status='active',result=None,
           score=[0,0],seed=seed,path_form_rules=True)
    s=dict(creator_sandbox=True,player='custom_practice',world=dict(minute=0,location='training_room'),
           combat=dict(profiles={'custom_practice':p},active=f))
    combat_profiles.profile(s,'custom_practice')
    combat_engine.ensure_arena(f)
    return s


def exchange(state,move_id,amp_id=None,target='opponent'):
    if state.get('creator_sandbox') is not True: raise ValueError('Practice requires an isolated sandbox.')
    import combat_engine
    f=state['combat']['active']
    return combat_engine.resolve(state,dict(fight_id=f['id'],turn=f['turn'],move_id=move_id,amp_id=amp_id,target=target))
