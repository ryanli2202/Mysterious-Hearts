"""Offline invitation responses for tests that need an established relationship."""
from unittest.mock import patch
import dating
import town

GOALS = dict(conversation='Talk about a childhood ambition', activity='Teach each other a small dance step', kiss=dating.KISS)


def next_morning(state):
    """Simulate elapsed play time for scenarios spanning several days."""
    town.loop.advance(state,1440-state['world']['minute']%1440+480)


def afternoon_state(player='garrett'):
    """Start schedule-dependent scenarios at 14:00 without simulating errands."""
    import game_core
    original=town.ensure
    def ensure_at_afternoon(state, **kwargs):
        return original(state,start_minute=14*60)
    with patch.object(town,'ensure',side_effect=ensure_at_afternoon):
        return game_core.fresh(player)


def invite(state, who, kind='date'):
    bond = state['relationships'][who]
    for stat, floor in zip(dating.STATS, dating.minimums(state, who, kind)):
        bond[stat] = max(bond[stat], floor)
    data = dict(answer='yes', reply='I’d love that.')
    if kind == 'date':
        data['goals'] = GOALS
    with patch.object(dating, 'generate_invitation', return_value=data):
        town.relationship(state, who, kind)


def finish_date(state, who):
    # This fixture tests date progression, so arrange a rested daytime meeting.
    import autonomy
    if who in state['world']['cast'] and autonomy.sleep_window(state,who):
        state['world']['minute']=(state['world']['minute']//1440+1)*1440+12*60
        state['world']['cast'][who].update(location=state['world']['location'],journey=None,activity='Free time')
        town.meet(state,who)
    if who in state['world']['cast'] and not dating.in_hangout(state,who):
        journey=state['world']['cast'][who]['journey']
        if journey: town.loop.advance(state,max(0,journey['arrives']-state['world']['minute']))
        if not town.loop.together(state,who): town.summon(state,who)
        else: town.meet(state,who)
    invite(state, who)
    assert dating.in_hangout(state, who)
    dating.advance(state, who, ['conversation', 'activity'], kissed=True)
