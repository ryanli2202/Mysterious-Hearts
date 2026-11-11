"""Read only the independent historical sheets; never fall back to adult lore."""
import copy
import hashlib
import json
from functools import lru_cache
from pathlib import Path

ROOT=Path(__file__).resolve().parent
REFERENCES=ROOT/'flashback_character_references.json'
GUIDES=ROOT/'flashback_dialogue_guides.json'


@lru_cache(maxsize=1)
def _load():
    try:
        raw_reference=REFERENCES.read_bytes();raw_guide=GUIDES.read_bytes()
        references=json.loads(raw_reference);guides=json.loads(raw_guide)
        if references['schema_version']!=1 or guides['schema_version']!=1:
            raise ValueError('Unsupported flashback reference schema.')
        if set(references['eras'])!=set(guides['eras']):
            raise ValueError('Flashback reference eras do not match the dialogue guides.')
        if not guides['rules'] or any(not isinstance(rule,str) or not rule.strip() for rule in guides['rules']):
            raise ValueError('Missing flashback dialogue rules.')
        for era,setting in references['eras'].items():
            if not setting['setting'] or not setting['knowledge_boundary']:
                raise ValueError('Missing historical setting or knowledge boundary.')
            if set(setting['characters'])!=set(guides['eras'][era]):
                raise ValueError('Missing historical character or voice.')
            for who,person in setting['characters'].items():
                for key in ('name','role','appearance','personality','present_concerns','relationships','private_boundaries'):
                    if not person[key]:raise ValueError('Incomplete historical character sheet: '+who)
                if person['age'] is not None and (type(person['age']) is not int or person['age']<=0):
                    raise ValueError('Invalid historical age.')
                for key in ('voice','habits','avoid','examples','unknown_response'):
                    if not guides['eras'][era][who][key]:raise ValueError('Incomplete historical dialogue guide: '+who)
    except (OSError,ValueError,KeyError,TypeError) as exc:
        raise ValueError('The separate flashback reference sheets or dialogue guides could not be loaded. Restore those files; present-day lore will not be substituted.') from exc
    revision=hashlib.sha256(raw_reference+b'\0'+raw_guide).hexdigest()
    return references,guides,revision


def revision():return _load()[2]


def era(key):return copy.deepcopy(_load()[0]['eras'][key])


def rules():return '\n'.join(_load()[1]['rules'])


def profile(era_key,who):
    try:
        sheet=copy.deepcopy(_load()[0]['eras'][era_key]['characters'][who])
        guide=copy.deepcopy(_load()[1]['eras'][era_key][who])
    except KeyError as exc:raise ValueError('No independent flashback reference for this character and era.') from exc
    return dict(id=who,name=sheet['name'],age=sheet['age'],character_reference=sheet,dialogue_guide=guide)


def display_people():
    """Names for the visit UI, sourced from the same school reference sheets."""
    return {who:dict(name=person['name'],age=person['age'])
        for key in ('school','hong-kong-school') for who,person in era(key)['characters'].items()}
