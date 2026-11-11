"""Recorded structural reviews; never mistake these for matchup simulations."""

def move_review(move,profile):
    import combat,combat_engine as engine,combat_states as states,combat_moves as moves
    r=combat.resources(profile); states.ensure(r)
    prepared=states.prepare_action(profile,r,move)
    scene=dict(player=r,enemy=r,kind='challenge',elapsed=0)
    raw=engine.raw_damage(profile,prepared,r,scene,'player')
    return dict(version=2,action=move['id'],scope='bounded generated-skill validation and current-profile force forecast',
        stats=dict(profile['stats']),costs=dict(stamina=move['stamina'],mana=move['mana']),
        force=move['force'],range=move['range'],hits=move['hits'],
        forecast=dict(raw_force=round(raw,2),prepared_mana=prepared['mana'],prepared_stamina=prepared['stamina'],
                      affordable=moves.can_pay(r,prepared),
                      interpretation='Pre-defence scalar, not guaranteed hit damage, combo total or win probability.'),
        effects=list(move['tags']),constraints=['Known approved Trait aspects only','No executable prose',
        'Normal resource costs','Counters require reach and an attack','Control resistance applies',
        'Returned force bounded by response capacity'],
        evidence='combat_workshop.validate_skills structural validation; runtime regressions in test_enhanced_combat.py',
        outcome='Accepted within engine bounds; no guaranteed tier promotion or claimed individual win rate.')


def progression_review(before,after,target):
    return dict(version=1,stage=target,before=before,after=dict(after),
        rules='Authored adjacent Path stage; existing 100 stat caps; no repeat stage-entry award.',
        evidence='combat_path.transition and test_combat_path.py',
        outcome='Earned numeric progression retained; stage alone does not assign a lore tier.')
