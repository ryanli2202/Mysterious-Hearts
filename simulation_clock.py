"""Active-play clock with saved day lengths and pause, without offline catch-up."""
import math
import time

DAY_LENGTHS = {'slow': 240, 'normal': 120, 'fast': 40, 'faster': 15}
LABELS = {'slow': 'Slow · 0.5× · 4-hour day', 'normal': 'Normal · 2-hour day', 'fast': 'Fast · 40-minute day',
          'faster': 'Faster · 15-minute day', 'paused': 'Paused'}
MINUTES_PER_SECOND = 1440 / (120 * 60)


def mode(state):
    value = state['world'].get('time_mode', 'normal')
    return value if value in LABELS else 'normal'


class SimulationClock:
    def __init__(self):
        self.state = None
        self.last = None

    def reset(self, state=None, now=None):
        self.state = state
        self.last = time.monotonic() if now is None else now

    def set_mode(self, state, value, active=True, now=None):
        if value not in LABELS:
            raise ValueError('Choose slow, normal, fast, faster or paused time.')
        now = time.monotonic() if now is None else now
        self.tick(state, active=active, now=now)
        state['world']['time_mode'] = value
        self.reset(state if active else None, now)

    def tick(self, state, active=True, now=None):
        now = time.monotonic() if now is None else now
        if not active or state is None:
            self.reset(None, now)
            return 0
        if state is not self.state or self.last is None:
            self.reset(state, now)
            return 0
        elapsed = max(0., now - self.last)
        self.last = now
        world = state['world']
        if state.get('combat',{}).get('active') or state.get('campaign_dialogue') or state.get('flashback_visit'): return 0
        selected = mode(state)
        if selected == 'paused': return 0
        base_rate = 1440 / (DAY_LENGTHS[selected] * 60)
        import autonomy
        import world_loop
        minutes = 0
        while elapsed > 1e-9:
            until = autonomy.person(state,state['player']).get('sleep_until')
            sleeping = until is not None and until > world['minute']
            speed = world.get('sleep_speed',1) if sleeping else 1
            if not sleeping: world['sleep_speed']=1
            rate = base_rate * speed
            fraction = world.get('clock_fraction',0.)
            total = fraction + elapsed * rate
            step = min(math.floor(total + 1e-9),2880)
            if sleeping: step = min(step,until-world['minute'])
            if not step:
                world['clock_fraction']=total
                break
            elapsed=max(0.,elapsed-(step-fraction)/rate)
            world['clock_fraction']=0.
            world_loop.advance(state, step)
            minutes += step
        until=autonomy.person(state,state['player']).get('sleep_until')
        if until is None or until<=world['minute']: world['sleep_speed']=1
        return minutes
