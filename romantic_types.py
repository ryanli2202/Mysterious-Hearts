"""Authored, directional romantic types; preferences are tendencies, never gates.

Tags describe usual presentation and adult everyday life, not today's clothing.
Each row: height, appearance, fashion, interests, sociability, lifestyle;
then preferred height range, appearance, fashion, interests, sociability, lifestyle.
"""
import json
import random
import character_appearance
import personality_types

_FIELDS = ('height', 'appearance', 'fashion', 'interests', 'sociability', 'lifestyle')
_ROWS = {
    'rei': (184, 'delicate', 'artistic', 'art', 'introvert', 'creative', (150, 175), 'soft', 'casual', 'crafts', 'introvert', 'quiet'),
    'garrett': (188, 'athletic', 'bold', 'cooking', 'extrovert', 'social', (145, 172), 'delicate', 'classic', 'science', 'introvert', 'structured'),
    'minsu': (177, 'soft', 'streetwear', 'gaming', 'extrovert', 'active', (155, 178), 'athletic', 'sporty', 'sports', 'extrovert', 'active'),
    'ivan': (193, 'striking', 'tailored', 'music', 'introvert', 'structured', (165, 190), 'striking', 'artistic', 'music', 'introvert', 'creative'),
    'emily': (154, 'soft', 'casual', 'crafts', 'introvert', 'quiet', (178, 195), 'delicate', 'artistic', 'art', 'introvert', 'creative'),
    'sophie': (170, 'athletic', 'sporty', 'sports', 'extrovert', 'active', (170, 193), 'athletic', 'streetwear', 'sports', 'extrovert', 'active'),
    'amy': (163, 'delicate', 'artistic', 'art', 'introvert', 'creative', (170, 190), 'soft', 'artistic', 'art', 'introvert', 'creative'),
    'samantha': (168, 'striking', 'bold', 'sports', 'extrovert', 'active', (178, 198), 'athletic', 'bold', 'sports', 'extrovert', 'active'),
    'april': (150, 'delicate', 'classic', 'science', 'introvert', 'structured', (175, 193), 'athletic', 'classic', 'cooking', 'extrovert', 'structured'),
    'yuriko': (159, 'soft', 'practical', 'crafts', 'extrovert', 'creative', (170, 188), 'soft', 'casual', 'crafts', 'extrovert', 'creative'),
    'lena': (168, 'striking', 'artistic', 'photography', 'extrovert', 'adventurous', (165, 190), 'striking', 'artistic', 'photography', 'introvert', 'adventurous'),
    'naomi': (175, 'athletic', 'practical', 'crafts', 'introvert', 'active', (160, 185), 'athletic', 'practical', 'outdoors', 'introvert', 'active'),
    'celeste': (172, 'soft', 'classic', 'music', 'extrovert', 'creative', (170, 195), 'delicate', 'artistic', 'music', 'introvert', 'quiet'),
    'valentina': (170, 'athletic', 'sporty', 'outdoors', 'extrovert', 'adventurous', (170, 195), 'athletic', 'casual', 'outdoors', 'extrovert', 'adventurous'),
    'dev': (181, 'soft', 'casual', 'gaming', 'introvert', 'quiet', (160, 190), 'soft', 'practical', 'science', 'introvert', 'creative'),
    'elliot': (186, 'delicate', 'practical', 'outdoors', 'introvert', 'quiet', (170, 195), 'athletic', 'casual', 'outdoors', 'introvert', 'quiet'),
    'tyler': (184, 'athletic', 'sporty', 'sports', 'extrovert', 'active', (165, 193), 'athletic', 'sporty', 'sports', 'extrovert', 'active'),
    'daniel': (180, 'delicate', 'classic', 'film', 'introvert', 'creative', (175, 195), 'striking', 'artistic', 'art', 'introvert', 'creative'),
    'rosa': (160, 'soft', 'casual', 'cooking', 'extrovert', 'social', (170, 190), 'soft', 'practical', 'cooking', 'extrovert', 'social'),
    'neo': (183, 'athletic', 'practical', 'science', 'introvert', 'quiet', (155, 178), 'soft', 'artistic', 'crafts', 'introvert', 'quiet'),
    'alyssa': (170, 'soft', 'artistic', 'crafts', 'introvert', 'quiet', (175, 190), 'athletic', 'practical', 'science', 'introvert', 'quiet'),
    'sylvanis': (198, 'striking', 'tailored', 'sports', 'introvert', 'structured', (165, 185), 'striking', 'tailored', 'art', 'extrovert', 'social'),
    'Theo': (None, 'soft', 'classic', 'books', 'introvert', 'quiet', (170, 195), 'delicate', 'artistic', 'books', 'introvert', 'quiet'),
    'Noah': (None, 'soft', 'casual', 'science', 'extrovert', 'social', (160, 190), 'soft', 'streetwear', 'gaming', 'extrovert', 'social'),
    'Leo': (None, 'athletic', 'practical', 'outdoors', 'extrovert', 'active', (155, 180), 'athletic', 'sporty', 'outdoors', 'extrovert', 'adventurous'),
}
TRAITS = {who: dict(zip(_FIELDS, row[:6])) for who, row in _ROWS.items()}
CANON = {who: dict(zip(_FIELDS, row[6:])) for who, row in _ROWS.items()}


# Each tuple lists acceptable alternatives, not a checklist every partner must meet.
# Hair preferences can concern colour or styling; eyes can concern colour or shape.
_DETAIL_PREFERENCES = {
    'rei': ('blonde; long; wavy', 'blue; hazel', 'delicate; fine features', 'petite; slim'),
    'garrett': ('dark-brown; straight; shoulder-length', 'brown; dark', 'delicate; fine features', 'petite; slim'),
    'minsu': ('brunette; ponytail; bob', 'green; hazel', 'strong brows; expressive', 'athletic; lean'),
    'ivan': ('black; dark-brown; wavy', 'dark; grey-green', 'angular; strong brows', 'lean; broad shoulders'),
    'emily': ('black; layered; shaggy', 'dark', 'angular; sharp jaw', 'lean; defined shoulders'),
    'sophie': ('black; short; tousled', 'dark; green', 'soft contours; strong brows', 'athletic; muscular'),
    'amy': ('black; curly; wavy', 'dark; hazel', 'soft contours; delicate', 'lean; slim'),
    'samantha': ('blond; black; short', 'golden; dark', 'angular; strong brows', 'muscular; broad shoulders'),
    'april': ('blond; ash-brown; tousled', 'golden; brown', 'angular; strong brows', 'athletic; broad shoulders'),
    'yuriko': ('black; tousled; curly', 'dark; brown', 'soft contours; expressive', 'lean; slim'),
    'lena': ('dark-brown; auburn; curly', 'hazel; green', 'angular; fine features', 'lean; slender'),
    'naomi': ('black; short; bob', 'dark; brown', 'strong brows; fine features', 'athletic; lean'),
    'celeste': ('black; layered; wavy', 'dark; hazel', 'delicate; soft contours', 'lean; slim'),
    'valentina': ('sandy-blond; silver-grey; short', 'green; grey-green', 'strong brows; angular', 'athletic; muscular'),
    'dev': ('dark; curly; bob', 'dark; brown', 'soft contours; rectangular glasses', 'slim; curvy'),
    'elliot': ('black; dark-brown; tousled', 'dark; green', 'strong brows; clean-shaven', 'lean; athletic'),
    'tyler': ('black; short; locs', 'dark; hazel', 'strong brows; angular', 'athletic; muscular'),
    'daniel': ('black; layered; wavy', 'dark; grey-green', 'angular; sharp jaw', 'lean; broad shoulders'),
    'rosa': ('dark; curly; tousled', 'brown; dark', 'soft contours; moustache', 'broad shoulders; curvy'),
    'neo': ('near-black; long; wavy', 'purple; dark', 'fine features; elongated ears', 'slim; slender'),
    'alyssa': ('black; tousled; short', 'grey-green; dark', 'angular; strong brows', 'lean; muscular'),
    'sylvanis': ('black; long; straight', 'dark; green', 'angular; fine features', 'slender; lean'),
    'Theo': ('auburn; dark-brown; wavy', 'hazel; dark', 'delicate; rectangular glasses', 'slim; lean'),
    'Noah': ('dark; short; curly', 'dark; brown', 'soft contours; expressive', 'lean; curvy'),
    'Leo': ('brunette; ponytail; short', 'green; dark', 'strong brows; expressive', 'athletic; lean'),
}
PHYSICAL_FIELDS = _FIELDS[:3] + character_appearance.DETAIL_FIELDS
PERSONALITY_FIELDS = personality_types.FIELDS
for _who, _preferences in _DETAIL_PREFERENCES.items():
    CANON[_who].update({key: tuple(value.split('; '))
                       for key, value in zip(character_appearance.DETAIL_FIELDS, _preferences)})
    TRAITS[_who].update(character_appearance.traits(_who))

for _who in CANON:
    TRAITS[_who].update(personality_types.PROFILES[_who])
    CANON[_who].update(personality_types.PREFERENCES[_who])


def match(actor, other, phase):
    """0..1 fit; unknown traits contribute neutral evidence, not rejection."""
    if phase not in ('physical', 'personality'):
        raise ValueError('Unknown romantic type phase.')
    keys = PHYSICAL_FIELDS if phase == 'physical' else PERSONALITY_FIELDS
    preferred, traits = CANON.get(actor, {}), TRAITS.get(other, {})
    if phase == 'personality':
        return personality_types.score(preferred, traits)
    scores = []
    for key in keys:
        want, actual = preferred.get(key), traits.get(key)
        if want is None or actual is None:
            scores.append(.5)
        elif key == 'height':
            scores.append(float(want[0] <= actual <= want[1]))
        elif key in character_appearance.DETAIL_FIELDS:
            scores.append(float(bool(set(want) & set(actual))))
        else:
            scores.append(float(want == actual))
    return sum(scores) / len(scores)


def probability(actor, other, phase):
    """A full match is 85%, a complete mismatch 15%; neither guarantees consent."""
    return .15 + .70 * match(actor, other, phase)


def initial_attraction(actor, other, baseline):
    # Zero is intentional on friendship-first routes. Preserve authored history.
    return round(max(0, min(100, baseline * (.3 + 1.4 * match(actor, other, 'physical')))))


def affection_step(actor, other, delta, *, draw=None):
    """Only positive long-term growth is probabilistic; harm still takes effect."""
    if delta <= 0:
        return delta
    roll = random.random() if draw is None else draw
    return delta if roll < probability(actor, other, 'personality') else 0


def direction(player, members):
    records = {who: dict(preferences=CANON[who],
                        personality_fit=personality_types.breakdown(CANON[who], TRAITS.get(player, {})),
                        physical_reciprocation_chance=round(probability(who, player, 'physical'), 3),
                        personality_growth_chance=round(probability(who, player, 'personality'), 3))
               for who in members if who in CANON}
    return (' Canonical romantic types (private guidance for each speaker): ' + json.dumps(records) +
            '. Physical preferences (height in cm, appearance, usual fashion, hair, eyes, facial features and body type) strongly bias initial attraction '
            'and early reciprocation; personality preferences (multiple interests, character traits, sociability and lifestyle) strongly bias '
            'lasting affection. Matches are much more likely, but exceptions in either direction are possible. '
            'Use these probabilities as tendencies when choosing a response, never as dialogue or guarantees. '
            'Existing feelings and actual shared experiences matter. Do not negate a delivered reciprocal response. '
            'Physical detail lists are alternatives: matching one item fits that physical dimension. '
            'Personality fit measures coverage of multiple preferred facets: interests 30%, character traits 35%, '
            'lifestyle 25%, sociability 10%. Related hobbies may share a domain without being identical. '
            'Extra interests never count against someone; no one must share every hobby or trait. '
            'These private fit scores do not grant knowledge of undisclosed interests or personal history. '
            'These traits are preferences, not beauty rankings or exhaustive descriptions. '
            'Use only established appearance facts; unknown features are neutral, never invented to fit a type. '
            'Never override orientation, family boundaries, refusal, consent or established commitments. '
            'Only disclose your own preferences naturally; do not announce another person’s private type. ')
