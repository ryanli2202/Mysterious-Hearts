"""Fictional Winterfield weather. Pure forecasts share the simulation's calendar."""
import math
import random
import story_calendar

def daily(day):
    date = story_calendar.story_date(day * 1440)
    rng = random.Random(205000 + day)
    season = -math.cos((date.timetuple().tm_yday - 15) * 2 * math.pi / 365.25)
    high = round(17 + 12 * season + rng.randint(-4, 4))
    low = high - rng.randint(6, 10)
    wet = rng.random() < .32
    condition = ('Snow' if high < 4 else 'Rain') if wet else rng.choice(('Clear', 'Partly cloudy', 'Cloudy'))
    sunrise = round(390 - 65 * season)
    sunset = round(1080 + 90 * season)
    return dict(day=day, date=date.isoformat(), high=high, low=low, condition=condition,
                precipitation=85 if wet else (25 if condition == 'Cloudy' else 5),
                wind=rng.randint(5, 28), humidity=rng.randint(70, 95) if wet else rng.randint(35, 65),
                sunrise=sunrise, sunset=sunset)

def at(minute):
    d = daily(minute // 1440)
    time = minute % 1440
    temp = round(d['low'] + (d['high'] - d['low']) * (1 + math.cos((time - 900) * math.pi / 720)) / 2)
    light = 'night' if time < d['sunrise'] or time >= d['sunset'] else 'dawn' if time < d['sunrise'] + 60 else 'dusk' if time > d['sunset'] - 60 else 'day'
    return dict(d, minute=minute, temperature=temp, feels_like=temp - (2 if d['wind'] > 20 else 0),
                light=light, uv=0 if light == 'night' else (2 if d['precipitation'] > 50 else 5),
                visibility=5 if d['precipitation'] > 50 else 16)

def forecast(minute):
    return dict(current=at(minute), hourly=[at(minute + h * 60) for h in range(24)],
                daily=[daily(minute // 1440 + d) for d in range(10)])

def summary(minute):
    w = at(minute)
    return f"{w['condition']} · {w['temperature']}°C · {w['light'].title()} · Wind {w['wind']} km/h"

def shelter(minute):
    return at(minute)['precipitation'] > 50
