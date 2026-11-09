"""Authored personality profiles and directional partner preferences.

Grounded in Character References, RPG Game biographies and hidden_cast.CAST.
Traits describe everyday behaviour, not an MBTI inference or private history.
Each row contains interests, personality traits, lifestyle and sociability.
Preferences are newly authored tastes, independent of a person's own profile.
"""
import hidden_cast

FIELDS = ('interests', 'personality_traits', 'lifestyle', 'sociability')
WEIGHTS = dict(interests=.30, personality_traits=.35, lifestyle=.25, sociability=.10)

_PROFILE_ROWS = {
    'martos': ('restoring watches; strength training; cooking rice dishes', 'dependable; patient; disciplined; stubborn; reserved; responsible', 'structured; hands-on; quiet; disciplined', 'introvert'),
    'mavis': ('field recording; repairing headphones; night walks', 'independent; blunt; resourceful; irreverent; guarded; spontaneous', 'independent; hands-on; quiet; spontaneous', 'introvert'),
    'camila': ('chess problems; fountain pens; tango', 'competitive; analytical; assertive; exacting; decisive; articulate', 'structured; active; independent; study', 'extrovert'),
    'elias': ('repertory cinema; judo; jiujitsu; aikido; dance rehearsals', 'expressive; playful; attentive; vain; persuasive; theatrical', 'creative; social; active; independent', 'extrovert'),
    'rei': ('drawing; painting; poetry; cooking; martial arts', 'reserved; attentive; creative; dry humour; guarded; dependable', 'creative; quiet; independent; family; disciplined', 'introvert'),
    'garrett': ('cooking; jeet kune do; sanda; hospitality', 'charismatic; playful; generous; proud; impulsive; confident', 'social; active; family; entrepreneurial', 'extrovert'),
    'minsu': ('science; medicine; video games; co-op games; anime; taekwondo; food reviewing', 'enthusiastic; curious; considerate; analytical; playful; disciplined', 'active; study; social; family; disciplined', 'extrovert'),
    'ivan': ('singing; piano; music; modelling; repairs; martial arts', 'reserved; practical; precise; dependable; protective; disciplined', 'structured; creative; quiet; family; active', 'introvert'),
    'emily': ('flower arranging; lego; miniatures; plush collecting', 'gentle; shy; attentive; creative; precise; assertive', 'quiet; creative; hands-on; friendship', 'introvert'),
    'sophie': ('running; athletics; parties; training; social media', 'ambitious; hardworking; competitive; playful; self-critical; candid', 'active; social; disciplined; study; friendship', 'extrovert'),
    'amy': ('painting; philosophy; psychology; interviewing; reading', 'introspective; thoughtful; curious; creative; sensitive; analytical', 'creative; quiet; study; friendship', 'introvert'),
    'samantha': ('motorcycling; fighting; training', 'blunt; playful; confident; independent; practical; flirtatious', 'active; independent; spontaneous; social', 'extrovert'),
    'april': ('chess; science; reading', 'logical; precise; observant; dry humour; candid; cautious', 'structured; quiet; study; friendship', 'introvert'),
    'yuriko': ('theatre design; miniatures; model making; fantasy books', 'creative; expressive; independent; assertive; playful; resourceful', 'creative; hands-on; study; family; independent', 'extrovert'),
    'lena': ('photography; history; conservation', 'curious; irreverent; resourceful; witty; independent', 'creative; adventurous; hands-on; independent', 'extrovert'),
    'naomi': ('bicycle repair', 'grounded; observant; dry humour; practical; patient', 'active; structured; hands-on; quiet; independent', 'introvert'),
    'celeste': ('astronomy; teaching', 'expressive; attentive; curious; playful; independent', 'creative; community; quiet; hands-on', 'extrovert'),
    'dev': ('teaching', 'inventive; patient; absent-minded; curious; practical', 'quiet; hands-on; creative; community', 'introvert'),
    'elliot': ('wildlife; trail maintenance', 'reserved; independent; perceptive; playful; practical', 'quiet; outdoors; active; independent; hands-on', 'introvert'),
    'tyler': ('coaching', 'reserved; practical; patient; dependable; considerate', 'active; structured; family; community; disciplined', 'introvert'),
    'daniel': ('film programming', 'reserved; attentive; opinionated; creative; dry humour', 'creative; active; structured; family; quiet', 'introvert'),
    'valentina': ('teaching', 'competitive; independent; confident; practical; playful; assertive', 'active; adventurous; social; family; hands-on', 'extrovert'),
    'rosa': ('cooking', 'sociable; candid; generous; assertive; practical', 'community; social; hands-on; active', 'extrovert'),
    'neo': ('electronics', 'reserved; practical; considerate; guarded; independent', 'quiet; hands-on; active; domestic; independent', 'introvert'),
    'alyssa': ('bookbinding', 'gentle; observant; independent; playful; creative', 'quiet; creative; hands-on; domestic; independent', 'introvert'),
    'sylvanis': ('psychological suspense; social collapse; fight patronage', 'theatrical; sadistic; brilliant; volatile; manipulative; unpredictable', 'spontaneous; independent', 'extrovert'),
    'Theo': ('books; reading; recommendations', 'thoughtful; candid; attentive; reflective', 'quiet; community; structured', 'introvert'),
    'Noah': ('games; television; campus life', 'sociable; curious; reflective; impulsive', 'social; study; community', 'extrovert'),
    'Leo': ('walking; local exploration; television', 'observant; practical; considerate; sociable', 'active; outdoors; community; independent', 'extrovert'),
}

_PREFERENCE_ROWS = {
    'martos': ('crafts; cooking; books', 'candid; dependable; patient; considerate', 'quiet; structured; independent', 'introvert'),
    'mavis': ('music; crafts; outdoors', 'independent; candid; observant; playful', 'independent; quiet; spontaneous', 'introvert'),
    'camila': ('games; dance; books', 'confident; curious; articulate; independent', 'active; independent; creative', 'extrovert'),
    'elias': ('film; music; dance', 'candid; witty; creative; attentive', 'creative; social; independent', 'extrovert'),
    'rei': ('art; crafts; books; cooking', 'gentle; attentive; independent; creative', 'quiet; creative; domestic; independent', 'introvert'),
    'garrett': ('science; cooking; games; books', 'candid; analytical; independent; witty', 'structured; family; independent; social', 'introvert'),
    'minsu': ('sports; games; science; food', 'playful; curious; considerate; disciplined', 'active; study; social; family', 'extrovert'),
    'ivan': ('music; crafts; art; sports', 'dependable; independent; attentive; precise', 'quiet; creative; structured; family', 'introvert'),
    'emily': ('art; crafts; books; cooking', 'attentive; gentle; creative; dependable', 'quiet; creative; hands-on; friendship', 'introvert'),
    'sophie': ('sports; games; food; outdoors', 'playful; confident; candid; considerate', 'active; social; disciplined; friendship', 'extrovert'),
    'amy': ('art; books; science; film', 'thoughtful; curious; attentive; candid', 'creative; quiet; study; independent', 'introvert'),
    'samantha': ('sports; motorcycling; games; food', 'confident; candid; independent; playful', 'active; independent; spontaneous; social', 'extrovert'),
    'april': ('science; games; cooking; books', 'candid; dependable; curious; analytical', 'structured; family; study; independent', 'extrovert'),
    'yuriko': ('crafts; art; books; games', 'creative; playful; independent; considerate', 'creative; hands-on; independent; study', 'extrovert'),
    'lena': ('photography; history; dance; art', 'curious; witty; dependable; independent', 'adventurous; creative; independent; hands-on', 'introvert'),
    'naomi': ('sports; crafts; books; outdoors', 'patient; practical; candid; independent', 'active; structured; quiet; hands-on', 'introvert'),
    'celeste': ('music; science; outdoors; cooking', 'curious; attentive; playful; independent', 'creative; quiet; community; independent', 'introvert'),
    'dev': ('science; games; crafts; photography', 'curious; patient; inventive; considerate', 'hands-on; creative; quiet; community', 'introvert'),
    'elliot': ('outdoors; crafts; music; sports', 'independent; perceptive; patient; playful', 'quiet; outdoors; independent; active', 'introvert'),
    'tyler': ('sports; games; music; cooking', 'dependable; considerate; candid; playful', 'active; family; structured; community', 'extrovert'),
    'daniel': ('film; art; books; sports', 'attentive; thoughtful; creative; patient', 'creative; quiet; structured; family', 'introvert'),
    'valentina': ('outdoors; sports; music; crafts', 'independent; confident; playful; dependable', 'adventurous; active; social; hands-on', 'extrovert'),
    'rosa': ('cooking; gardening; sports; food', 'generous; candid; considerate; independent', 'community; social; hands-on; domestic', 'extrovert'),
    'neo': ('crafts; games; cooking; outdoors', 'gentle; observant; independent; playful', 'quiet; domestic; hands-on; independent', 'introvert'),
    'alyssa': ('crafts; games; cooking; outdoors', 'practical; considerate; independent; attentive', 'quiet; domestic; hands-on; independent', 'introvert'),
    'sylvanis': ('art; music; sports', 'confident; precise; independent', 'structured; social; independent', 'extrovert'),
    'Theo': ('books; art; film; games', 'thoughtful; curious; candid; attentive', 'quiet; creative; community; independent', 'introvert'),
    'Noah': ('games; science; television; food', 'playful; curious; candid; considerate', 'social; study; community; spontaneous', 'extrovert'),
    'Leo': ('outdoors; sports; food; television', 'independent; playful; practical; considerate', 'active; adventurous; outdoors; community', 'extrovert'),
}

# Related hobbies count in a shared domain without pretending the exact hobbies match.
INTEREST_DOMAINS = {
    'art': ('drawing', 'painting', 'poetry', 'drawing lobby cards', 'sketching', 'botanical sketching'),
    'books': ('reading', 'poetry', 'fantasy books', 'mystery novels', 'psychological suspense', 'bookbinding'),
    'crafts': ('lego', 'miniatures', 'model making', 'theatre design', 'ceramics', 'wood carving', 'repairs', 'electronics', 'electronics repair', 'repairing old electronics', 'bicycle repair', 'mending old sails', 'bookbinding', 'conservation'),
    'sports': ('martial arts', 'jeet kune do', 'sanda', 'taekwondo', 'running', 'athletics', 'training', 'fighting', 'boxing', 'controlled boxing drills', 'judo', 'bouldering', 'roller skating', 'dinghy racing', 'kayaking', 'calling baseball games with his dad', 'coaching'),
    'music': ('singing', 'piano', 'jazz piano', 'late-night karaoke', 'field recording'),
    'science': ('medicine', 'astronomy', 'electronics', 'electronics repair', 'repairing old electronics'),
    'games': ('video games', 'co-op games', 'tabletop games', 'dominoes', 'chess'),
    'food': ('cooking', 'food reviewing', 'baking bread', 'recipe swaps', 'cooking with Alyssa', 'cooking with Neo'),
    'cooking': ('baking bread', 'recipe swaps', 'cooking with Alyssa', 'cooking with Neo'),
    'outdoors': ('birdwatching', 'kayaking', 'wildlife', 'trail maintenance', 'walking', 'local exploration', 'quiet riverside walks', 'community gardening', 'dinghy racing'),
    'photography': ('film photography', 'night photography'),
    'history': ('urban history',), 'dance': ('salsa',),
    'film': ('repertory films', 'film programming'), 'gardening': ('community gardening', 'flower arranging', 'balcony herb gardening'),
}


def tokens(value):
    if value is None:
        return None
    if isinstance(value, str):
        value = value.split(';')
    return frozenset(item.strip().casefold() for item in value if item.strip())


def expand_interests(values):
    result = set(tokens(values) or ())
    for domain, hobbies in INTEREST_DOMAINS.items():
        if result.intersection(tokens(hobbies)):
            result.add(domain)
    return result


def _rows(rows):
    return {who: {key: tuple(sorted(tokens(value))) for key, value in zip(FIELDS, row)}
            for who, row in rows.items()}


PROFILES = _rows(_PROFILE_ROWS)
PREFERENCES = _rows(_PREFERENCE_ROWS)
for _who, _profile in PROFILES.items():
    # Preserve every explicitly authored hidden-cast hobby, not only its broad domain.
    _profile['interests'] = tuple(sorted(set(_profile['interests']) |
                                       set(hidden_cast.CAST.get(_who, {}).get('hobbies', ()))))


def breakdown(preferred, actual):
    """Coverage of desired facets; extra hobbies never dilute an existing match."""
    scores = {}
    for key in FIELDS:
        want, have = tokens(preferred.get(key)), tokens(actual.get(key))
        if not want or not have:
            scores[key] = .5
            continue
        if key == 'interests':
            have = expand_interests(have)
        scores[key] = len(want & have) / len(want)
    return scores


def score(preferred, actual):
    return sum(WEIGHTS[key] * value for key, value in breakdown(preferred, actual).items())
