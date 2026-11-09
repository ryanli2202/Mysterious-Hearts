"""Deterministic test-only stock; production never substitutes this catalogue."""
import supafast


def items(day=0):
    return [dict(name=f'Day {day} studio find {i}', description=f'A hand-finished object with a textured surface and useful storage feature {i}.',
                 category=('Home', 'Craft', 'Outdoors', 'Accessories')[i % 4], price=15+i*5) for i in range(12)]


def seed(state):
    day = state['world']['minute']//1440
    supafast.commit(state, day, items(day))


def disable_images(game):
    """Text/layout-only smoke checks must never invoke the real image provider."""
    from unittest.mock import Mock
    game.supafast_images = Mock()
    game.supafast_images.status.return_value = 'loading'

    game.doober_images = Mock()
    game.doober_images.status.return_value = 'loading'
