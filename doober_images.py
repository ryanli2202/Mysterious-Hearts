"""Bundled manhwa menu illustrations; browsing never generates images."""
import json
from pathlib import Path
from functools import lru_cache
import phone_apps as apps

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / 'assets' / 'doober'

@lru_cache(maxsize=1)
def manifest():
    try:
        return json.loads((ASSETS / 'manifest.json').read_text(encoding='utf-8'))['items']
    except (OSError, ValueError, KeyError):
        return {}

def menu(state, restaurant):
    # Fresh display records leave legacy save-specific photos and saves intact.
    records = manifest().get(restaurant, {})
    products = {}
    for ident, item in apps.MENUS[restaurant].items():
        product = dict(item)
        art = records.get(ident, {})
        if all(art.get(k) == item[k] for k in ('name', 'category')):
            product['image'] = art['image']
        products[ident] = product
    return products

def image_path(product):
    value = product.get('image')
    if not value:
        return None
    path = (ROOT / value).resolve()
    return path if path.is_relative_to(ASSETS.resolve()) and path.is_file() else None

class FoodImages:
    """Static adapter for the shared dark photo widget, without timers or jobs."""
    bundled = True
    image_path = staticmethod(image_path)

    def __init__(self, game):
        self.game = game

    def request(self, retry=False):
        pass

    def status(self, product):
        return 'ready' if image_path(product) else 'error'

def jobs(game, restaurant):
    manager = getattr(game, 'doober_images', None)
    if manager is None:
        manager = game.doober_images = FoodImages(game)
    return manager
