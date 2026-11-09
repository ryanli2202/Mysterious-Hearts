"""Conservative extraction of explicit self-disclosures, never guesses or questions."""
import re

ALIASES = {'film':'Movie', 'movie':'Movie', 'movies':'Movie', 'food':'Food',
           'breakfast':'Breakfast', 'lunch':'Lunch', 'dinner':'Dinner', 'snack':'Snack',
           'drink':'Drink', 'dessert':'Dessert', 'tv show':'TV show', 'show':'TV show',
           'book':'Book', 'author':'Author', 'music':'Music', 'song':'Song',
           'hobby':'Hobby', 'hobbies':'Hobby', 'colour':'Colour', 'color':'Colour'}


def extract(text):
    result = {}
    text = text.replace('’', "'")
    # Do not turn quoted dialogue, hypothetical statements or questions into facts.
    clauses = [clause for sentence in re.finditer(r'[^.!?\n]+[.!?]?', text)
               if not sentence[0].endswith('?')
               for clause in re.split(r';|,?\s+and\s+(?=my\b|I\b)', sentence[0].rstrip('.!'))]
    for clause in clauses:
        clause = clause.strip()
        if not clause: continue
        clause = re.sub(r'^(?:actually|these days|now|honestly)[, ]+', '', clause, flags=re.I)
        match = re.fullmatch(r"my (?:new )?favou?rite ([\w ]{1,30}?) (?:is|are) (.+)", clause, re.I)
        reverse = re.fullmatch(r"(.+?) (?:is|are) my (?:new )?favou?rite ([\w ]{1,30})", clause, re.I)
        absent = re.fullmatch(r"I (?:don't|do not) have a favou?rite ([\w ]{1,30}?)(?: anymore)?", clause, re.I)
        if match or reverse or absent:
            category = (match[1] if match else reverse[2] if reverse else absent[1]).lower()
            value = match[2] if match else reverse[1] if reverse else 'No favourite'
            if category in ALIASES and not re.search(r'\b(?:maybe|probably|would|might|used to)\b', value, re.I):
                result['favourite:'+ALIASES[category]] = value.strip(' \"')
            continue
        patterns = {
            'Likes': r'I (?:love|like) (.+)',
            'Dislikes': r"I (?:hate|dislike|don't like|do not like|no longer like) (.+)",
            'Hobbies': r'I enjoy (.+)',
            'Preferences': r'I prefer (.+)',
            'Allergies': r"I(?: am|'m) allergic to (.+)",
            'Hometown': r'I grew up in (.+)',
            'Occupation': r'I work as (.+)',
            'Studies': r'I study (.+)',
            'Boundaries': r"I(?: am|'m) not comfortable with (.+)",
        }
        for field, pattern in patterns.items():
            if match := re.fullmatch(pattern, clause, re.I):
                result[field] = match[1].strip(' \"')
    return result
