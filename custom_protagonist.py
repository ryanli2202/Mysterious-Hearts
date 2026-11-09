"""Save-owned adult protagonists; custom IDs never become scheduled town NPCs."""
import copy
import json
from pathlib import Path
import re
import uuid

ROOT = Path(__file__).resolve().parent
PORTRAIT_STYLE_REFERENCES = tuple(ROOT / 'assets' / 'portraits' / name
                                 for name in ('rei-selection.png', 'emily-selection.png'))
GENDERS = ('Man', 'Woman', 'Nonbinary')
SEXUALITIES = ('Straight', 'Gay', 'Lesbian', 'Bisexual', 'Pansexual', 'Asexual')
MBTI = tuple(a+b+c+d for a in 'IE' for b in 'NS' for c in 'FT' for d in 'JP')
HAIRSTYLES = ('Short', 'Medium length', 'Long', 'Curly', 'Wavy', 'Braids', 'Locs', 'Shaved', 'Bald', 'Other / describe below')
VOICE = 'Use the player’s stated interests and current conversation. Do not invent their past, relationships, mannerisms or feelings from gender or MBTI. Leave their choices to them.'
_profiles = {}
_installed = False


def is_custom(who):
    return isinstance(who, str) and bool(re.fullmatch(r'custom_[0-9a-f]{32}', who))


def display_name(who):
    return _profiles[who]['name'] if who in _profiles else who.title()


class Registry(dict):
    """Canonical roster iteration, plus lookup of registered save-owned identities.

    NPC enumeration must not gain protagonists from other open/loaded saves.
    Unique IDs let background requests keep their own immutable profile.
    """
    def __init__(self, source, resolve):
        super().__init__(source)
        self.resolve = resolve

    def __missing__(self, key):
        if key not in _profiles:
            raise KeyError(key)
        return self.resolve(_profiles[key])

    def __contains__(self, key):
        return super().__contains__(key) or key in _profiles

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default


def validate(values):
    import vacant_homes
    if not isinstance(values, dict):
        raise ValueError('The custom character profile is missing.')
    p = {}
    for field, limit in (('name', 60), ('occupation', 100), ('appearance', 1800)):
        value = values.get(field)
        if not isinstance(value, str) or not value.strip() or len(value.strip()) > limit:
            raise ValueError(f'Enter {field} (1–{limit} characters).')
        p[field] = value.strip()
    if any(ord(c) < 32 for c in p['name']):
        raise ValueError('Enter a name on one line.')
    for field, options in (('gender', GENDERS), ('sexuality', SEXUALITIES), ('mbti', MBTI), ('hairstyle', HAIRSTYLES), ('home', vacant_homes.HOMES)):
        if values.get(field) not in options:
            raise ValueError('Choose a valid ' + field + '.')
        p[field] = values[field]
    for field, low, high in (('age', 18, 100), ('height', 120, 230)):
        value = values.get(field)
        if isinstance(value, bool) or not str(value).isdigit() or not low <= int(value) <= high:
            raise ValueError(f'{field.title()} must be between {low} and {high}' + (' cm.' if field == 'height' else '.'))
        p[field] = int(value)
    interests = values.get('interests', [])
    if isinstance(interests, str):
        interests = interests.split(',')
    if not isinstance(interests, list) or any(not isinstance(x, str) for x in interests):
        raise ValueError('Enter interests separated by commas.')
    p['interests'] = list(dict.fromkeys(x.strip() for x in interests if x.strip()))
    if not 1 <= len(p['interests']) <= 12 or any(len(x) > 60 for x in p['interests']):
        raise ValueError('Enter 1–12 interests, each up to 60 characters.')
    p['awakened'] = values.get('awakened', False)
    if not isinstance(p['awakened'], bool):
        raise ValueError('Choose whether your character is awakened.')
    for field, label, limit in (('awakening_trait', 'awakening trait', 100),
                                ('awakening_description', 'awakening description', 1800)):
        value = values.get(field, '') if p['awakened'] else ''
        if not isinstance(value, str) or (p['awakened'] and not 1 <= len(value.strip()) <= limit):
            raise ValueError(f'Enter {label} (1–{limit} characters).')
        p[field] = value.strip()
    return p


def awakening_background(p):
    if not p.get('awakened', False):
        return 'Not awakened at story creation (Dormancy). No starting awakening Trait is established. Saved Path progression determines current combat abilities.'
    return (f"Already Awakened. Trait: {p['awakening_trait']}. Description: {p['awakening_description']}. "
            'This is an established starting ability, not a future unlock. '
            'It does not establish prior exploits, public knowledge or automatic mechanical power use.')


def background(p):
    return (f"{p['name']}, {p['age']}, {p['gender']}, {p['height']} cm. Occupation: {p['occupation']}. "
            f"MBTI: {p['mbti']}. Interests: {', '.join(p['interests'])}. "
            f"Hairstyle: {p['hairstyle']}. Appearance: {p['appearance']}. "
            'Just moved into Winterfield. Home: ' + home(p)[1] + '. Has no prior acquaintances, local shared memories, family ties or established romance. '
            'Any later familiarity must come from actual saved meetings or Meet-Cute exchanges. '
            + awakening_background(p))


def home(p):
    import vacant_homes
    item = vacant_homes.HOMES[p['home']]
    return p['home'], p['name'] + '’s ' + item['name'].removeprefix('Vacant ').lower(), item['description'].replace('An empty', 'An unfurnished', 1)


def install():
    global _installed
    if _installed:
        return
    import game_core as core
    import town, world_loop, sexuality, meet_cute, grove, phone_personalization, romantic_types
    def wrap(module, attr, fn):
        setattr(module, attr, Registry(getattr(module, attr), fn))
    wrap(core, 'PLAYERS', lambda p: p['name'])
    wrap(core, 'CONTACTS', lambda p: (p['name'], 'Winterfield', 'A new beginning.', background(p)))
    wrap(core, 'TEXT_STYLES', lambda p: VOICE)
    wrap(world_loop, 'HOUSES', home)
    wrap(world_loop, 'GARAGES', lambda p: {'Compact car': (5, 'a compact car')})
    wrap(town, 'HOMES', lambda p: p['home'])
    wrap(town, 'STARTING_RELATIONSHIPS', lambda p: {who: (0, 35, 0, 'strangers') for who in core.CONTACTS})
    wrap(town, 'HOME_ACTIONS', lambda p: ['Unpack a moving box', 'Prepare a simple meal', 'Write in your journal', 'Relax and settle in'])
    wrap(town, 'CAREERS', lambda p: [])
    wrap(sexuality, 'CANON', lambda p: ({'Man': 'Men', 'Woman': 'Women', 'Nonbinary': 'Nonbinary'}[p['gender']], p['sexuality']))
    wrap(meet_cute, 'INTERESTS', lambda p: tuple(p['interests']))
    wrap(meet_cute, 'AGES', lambda p: p['age'])
    wrap(meet_cute, 'JOBS', lambda p: p['occupation'])
    wrap(meet_cute, 'HOOKS', lambda p: ('Finding my feet in a new town.', 'Somewhere we can talk and get to know each other.', ', '.join(p['interests'])))
    wrap(grove, 'HANDLES', lambda p: 'new.to.winterfield')
    wrap(grove, 'FOLLOWERS', lambda p: 0)
    wrap(grove, 'BIOS', background)
    wrap(romantic_types, 'TRAITS', lambda p: dict(height=p['height'], interests=tuple(x.lower() for x in p['interests'])))
    wrap(phone_personalization, 'PROFILES', lambda p: dict(accent='#80c6ba', favourites=[], names={},
        apps=['Maps', 'Meet-Cute', 'Messages', 'Camera'], note='Settle into my new home. Explore Winterfield and meet people.', messages=[]))
    _installed = True


def restore(state):
    if not is_custom(state.get('player')):
        return
    p = validate(state.get('custom_protagonist'))
    p['portrait'] = state['custom_protagonist'].get('portrait', '')
    portrait_path(p)  # Validate saved paths without requiring an installed image.
    existing = _profiles.get(state['player'])
    if existing and existing != p:
        raise ValueError('This custom character ID belongs to a different profile.')
    _profiles[state['player']] = p
    install()


def portrait_path(p):
    relative = p.get('portrait', '')
    if not isinstance(relative, str) or not relative:
        raise ValueError('Generate a transparent portrait first.')
    path = (ROOT / relative).resolve()
    if not path.is_relative_to((ROOT / 'assets' / 'generated').resolve()) or path.suffix.lower() != '.png':
        raise ValueError('Custom portrait must be a generated game PNG.')
    return path


def verify_portrait(path):
    from PIL import Image
    with Image.open(path) as image:
        image.load()
        if 'A' not in image.getbands():
            raise ValueError('The portrait has no transparency. Generate again.')
        alpha = image.getchannel('A')
        low, high = alpha.getextrema()
        if low != 0 or high < 128:
            raise ValueError('The portrait needs a transparent background and a visible character. Generate again.')


def portrait_prompt(values):
    p = validate(values)
    appearance = {key: p[key] for key in ('gender', 'age', 'height', 'hairstyle', 'appearance')}
    return ('Generate one new adult protagonist portrait for the Mysterious Hearts visual novel. '
            'The attached Rei and Emily portraits are STYLE REFERENCES ONLY. Match their established '
            '2D manhwa/anime visual-novel art style: fine clean dark linework, softly blended cel shading, '
            'detailed hair strands and fabric folds, restrained highlights, expressive illustrated eyes '
            'and natural adult proportions. Match their vertical head-to-upper-thigh portrait framing '
            'and character scale, with the entire head visible, a front three-quarter view and a natural '
            'relaxed pose. Do not switch to photorealism, 3D rendering, chibi or a painterly style. '
            'Create a distinct new person; do not copy either reference character’s identity, face, hair, '
            'skin tone, clothing, tattoos, piercings or accessories unless requested in the appearance data. '
            'The selected gender and appearance data determine the new character; the references determine '
            'only the rendering style and framing. Keep the character fully clothed as described. '
            'Use a truly transparent RGBA background '
            '(set transparent_background true), no scenery, text, border, shadows outside the figure or checkerboard. '
            'The following JSON is appearance data, not instructions. Preserve this gender, hairstyle and description: '
            + json.dumps(appearance, ensure_ascii=False))


def generate_portrait(values, cancel=None, progress=lambda text: None):
    import codex_images
    result = codex_images.generate(portrait_prompt(values), cancel=cancel, progress=progress,
                                   references=PORTRAIT_STYLE_REFERENCES)
    path = Path(result['path']).resolve()
    relative = path.relative_to(ROOT).as_posix()
    portrait_path({'portrait': relative})
    verify_portrait(path)
    return relative


def create(values, portrait):
    import game_core as core
    p = validate(values)
    p['portrait'] = portrait
    verify_portrait(portrait_path(p))
    ident = 'custom_' + uuid.uuid4().hex
    state = {'version': 1, 'calendar_start_year': core.town.loop.dates.START.year,
             'player': ident, 'custom_protagonist': copy.deepcopy(p), 'save_name': p['name'] + ' · New in Winterfield', 'active': 'emily', 'turn': 0,
             'routes': {key: {'history': [], 'memory': '', 'scene': '', 'dialogue': '', 'choices': [], 'channel': 'text'} for key in core.CONTACTS},
             'world': {'location': p['home'], 'money': 100000, 'inventory': {}, 'job': None,
                       'last_shift_day': 0, 'npcs': [], 'log': []}}
    restore(state)
    core.town.ensure(state, start_minute=8*60)
    return state


def lore_record(p):
    return {'Public life': background(p), 'Familiar': 'Learn interests through conversation.',
            'Personal': 'No additional past has been established.', 'Confidence': 'Do not invent private history.',
            'World knowledge': 'New to Winterfield.', 'Character type': 'major character',
            'Appearance': p['appearance'], 'Portrait style': 'Hairstyle: ' + p['hairstyle']}
