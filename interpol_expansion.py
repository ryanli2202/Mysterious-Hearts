"""Authored Interpol expansion compiler; runtime uses the frozen prose catalogue.

Existing source addresses remain stable for core paintings and annotations.
Saved beats are never regenerated or migrated by this module.
"""
import copy
import re
from pathlib import Path

SOURCE = Path(__file__).parent / 'campaign_prose/interpol_expansion.md'
PAST = {'fox': 'fox-organisation', 'kaden': 'sylvanis-kaden',
        'conspirator': 'sylvanis-conspirator', 'sylvanis': 'sylvanis-early'}
NEW_MEMORIES = {
    'FM05': ('fg-organisation', 'locations/campaign/interpol/organisation-infirmary', PAST),
    'FM06': ('fg-coup', 'locations/campaign/interpol/organisation-infirmary',
             {'fox': 'fox-organisation', 'kaden': 'sylvanis-kaden'}),
    'FM07': ('fg-after-coup', 'locations/campaign/interpol/fox-mourning-workbench',
             {'fox': 'fox-organisation'}),
}


def sections():
    result = []
    current = None
    for paragraph in re.split(r'\n\s*\n', SOURCE.read_text(encoding='utf-8')):
        if paragraph.startswith('## '):
            key, _, suffix = paragraph[3:].partition(' ')
            current = dict(key=key, suffix=suffix, elements=[])
            result.append(current)
        elif paragraph and not paragraph.startswith('# '):
            speaker, separator, text = paragraph.partition('> ')
            if current is None or not separator:
                raise ValueError('Malformed Interpol authored paragraph: '+paragraph[:80])
            element = dict(text=text, authored=True)
            if speaker in ('memory', 'present'):
                element['mode'] = speaker
            elif speaker in ('fox-pov', 'gordon-pov'):
                element['when'] = {'player': speaker[:-4]}
            elif speaker != 'n':
                if speaker not in ('fox', 'gordon', 'kaden', 'conspirator', 'sylvanis',
                                   'crow', 'martos', 'elias', 'camila', 'mavis'):
                    raise ValueError('Unknown Interpol speaker: '+speaker)
                element.update(speaker=speaker, text='“'+text+'”')
            if current['suffix'] in ('before', 'after', 'interview'):
                element.setdefault('when', {})['phase'] = current['suffix']
            current['elements'].append(element)
    return result


def install(library):
    # Editorial leakage is replaced at source without changing the old addresses.
    replacements = {
        'FD09': {10: 'Gordon waited. Fox tried once more, then handed over the stubborn catch.'},
        'FD25': {13: 'Gordon crossed out the unsupported name. The Crow’s birth identity remained unknown. The authenticated transfer would have to carry the enquiry forward.'},
        'FD30': {
            0: 'The opaque beaked mask gave them no expression to read. Robes and draped cloth concealed the person beneath. Fox could find nothing human in the surface offered to him.',
            12: 'The Crow let the demand hang between them. He offered neither an explanation nor a concession. Gordon waited for an answer; Fox watched for movement.'},
        'FD35': {10: 'Gordon smiled faintly. The recollection belonged to their early partnership; neither man tried to make it more precise than it was.'},
    }
    for key, scene in library.items():
        if not key.startswith(('FD', 'FM')):
            continue
        for index, element in enumerate(scene['elements']):
            element['legacy_element'] = index
            if index in replacements.get(key, {}):
                element['text'] = replacements[key][index]
        # Same action once, not duplicate movements from two draft assemblies.
        if key == 'FD32':
            scene['elements'] = [e for e in scene['elements'] if e['legacy_element'] not in (64, 70, 83)]
    for section in sections():
        key = section['key']
        additions = copy.deepcopy(section['elements'])
        if section['suffix'].startswith('new '):
            library[key] = dict(title=section['suffix'][4:], chapter='The people left behind',
                                source='campaign_prose/interpol_expansion.md', elements=additions)
            if key in NEW_MEMORIES:
                library[key]['memory_owner'] = 'fox'
                era, background, portraits = NEW_MEMORIES[key]
                mode = 'present'
                selected = copy.deepcopy(portraits)
                for element in additions:
                    mode = element.get('mode', mode)
                    if mode == 'memory':
                        if key == 'FM06' and element['text'].startswith('Fox hated how often'):
                            selected = {'fox': 'fox-organisation'}
                        element.update(background=background, portraits=copy.deepcopy(selected))
                    elif element.get('mode') == 'present':
                        element.update(portraits={}, background=None)
            continue
        elements = library[key]['elements']
        if section['suffix'] == 'memory':
            # Add inside the historical scene, before its explicit return.
            index = next((i for i, e in enumerate(elements) if e.get('mode') == 'present'), len(elements))
            elements[index:index] = additions
        else:
            elements.extend(additions)
        library[key]['expansion_source'] = 'campaign_prose/interpol_expansion.md'
    return library
