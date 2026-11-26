"""Scene-to-era bindings; no lookup of present-day lore as historical fallback."""
SCENES={
    'RD36':'rei-childhood','RD37':'rei-escape','RD38':'rei-escape',
    **{f'NE-M{i:02}':era for i,era in enumerate(('neo_home12','neo_school16','neo_home16','neo_facility10','neo_raid10','neo_home16'),1)},
    **{key:spec['era'] for key,spec in __import__('takeo_campaign_content').MEMORIES.items()},
    **{f'SY-M{i:02}':era for i,era in enumerate(('sylvanis_arrival','sylvanis_mastery','sylvanis_organisation','sylvanis_proposal','sylvanis_coup','sylvanis_expansion','sylvanis_trials','sylvanis_eastern','sylvanis_charles','sylvanis_takeo'),1)},
    'CA-F01':'camila_adoption7','CA-F02':'camila_home8','CA-F03':'camila_waiting11','CA-F04':'camila_correction16',
    'CA-F05':'camila_operation22','CA-F06':'camila_diamonds24','CA-F07':'camila_heir26','CA-F08':'camila_delegation28',
    'EL-F01':'elias_childhood10','EL-F02':'elias_actor21',
    'EL-F03':'elias_defence23','EL-F04':'elias_defence23',
    'EL-F05':'elias_duel23','EL-F06':'elias_settlement23',
    'EL-F07':'elias_service24','EL-F08':'elias_acknowledgement24',
    'EL-APPOINTMENT':'elias_appointment25',
    'GD02':'missing-charles','GD04':'golden-dragon-early','RD04':'golden-dragon-early',
    'GD15':'golden-dragon-early','RD08':'golden-dragon-early','GD17':'family-broth',
    'GD21':'hong-kong-school','RD09':'school','RD11':'school-loss','RD13':'school-administration',
    'FM01':'fg-early-partnership','FM02':'fg-early-partnership',
    'FM03':'fg-early-partnership','FM04':'fg-early-partnership',
    'FM05':'fg-organisation','FM06':'fg-coup','FM07':'fg-after-coup',
}


def validate(scene,speaker):
    import flashback_lore
    return flashback_lore.profile(SCENES[scene],speaker)
