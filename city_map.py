"""Deterministic street geometry and road-aligned buildings for Winterfield."""
import math
import random
from functools import lru_cache
from PIL import Image, ImageDraw


def junction(i, j):
    rng = random.Random(f'junction:{i}:{j}')
    x, y = i*175, j*150
    return (x + 65*math.sin(y/410) + rng.uniform(-32, 32),
            y + 55*math.sin(x/360) + rng.uniform(-28, 28))


def curve(a, b, bend=0):
    dx, dy = b[0]-a[0], b[1]-a[1]
    length = max(1, math.hypot(dx, dy))
    return [(a[0]+dx*t-dy/length*bend*math.sin(math.pi*t),
             a[1]+dy*t+dx/length*bend*math.sin(math.pi*t))
            for t in (n/12 for n in range(13))]


@lru_cache(maxsize=4096)
def local_streets(i, j):
    rng = random.Random(f'streets:{i}:{j}')
    a = junction(i, j)
    paths = []
    # Long connectors alternate with short residential streets and T junctions.
    for di, dj in ((1, 0), (0, 1)):
        if (di and j % 3 == 0) or (dj and i % 4 == 0) or rng.random() > .22:
            paths.append((curve(a, junction(i+di, j+dj), rng.uniform(-22, 22)), 9))
    return paths


def arterial_paths():
    # A curving cross-city avenue, hillside diagonal and river-following boulevard.
    return [([(x, 535+60*math.sin((x-620)/540)) for x in range(-6000, 7001, 25)], 19),
            ([(585+85*math.sin(y/450), y) for y in range(-6000, 7001, 25)], 17),
            ([(x, 1080-.65*x+35*math.sin(x/210)) for x in range(-6000, 7001, 25)], 15),
            ([(1070+45*math.sin(y/250), y) for y in range(-6000, 7001, 25)], 14)]


def render(width, height, cx, cy, zoom, satellite=False):
    # Supersampling keeps curved roads and angled roofs legible when zoomed out.
    image = _render(max(1, width)*2, max(1, height)*2, cx, cy, zoom*2, satellite)
    return image.resize((max(1, width), max(1, height)), Image.Resampling.LANCZOS)


def _render(width, height, cx, cy, zoom, satellite=False):
    width, height = max(1, width), max(1, height)
    left, top = cx-width/(2*zoom), cy-height/(2*zoom)
    right, bottom = left+width/zoom, top+height/zoom
    def xy(p): return ((p[0]-left)*zoom, (p[1]-top)*zoom)
    surface = Image.new('RGB', (width, height), '#777e75' if satellite else '#1c2433')
    draw = ImageDraw.Draw(surface)
    paths = []
    for i in range(math.floor((left-230)/175), math.ceil((right+230)/175)):
        for j in range(math.floor((top-200)/150), math.ceil((bottom+200)/150)):
            paths.extend(local_streets(i, j))
    arteries = arterial_paths()
    # Reserve road corridors before placing buildings; no footprints across junctions.
    mask = Image.new('L', surface.size)
    md = ImageDraw.Draw(mask)
    for path, road_width in [*paths, *arteries]:
        md.line([xy(p) for p in path], fill=255, width=max(2, round((road_width+12)*zoom)), joint='curve')
    for path, _ in paths:
        rng = random.Random(f'frontage:{path[0]}')
        for n in (2, 5, 8, 11):
            a, b = path[n-1], path[n]
            dx, dy = b[0]-a[0], b[1]-a[1]
            length = math.hypot(dx, dy)
            ux, uy = dx/length, dy/length
            for side in (-1, 1):
                downtown = 400 < b[0] < 920 and 230 < b[1] < 760
                bw, bh = (rng.uniform(25, 40), rng.uniform(28, 50)) if downtown else (rng.uniform(17, 35), rng.uniform(16, 40))
                offset = 16+bh/2
                bx, by = b[0]-uy*offset*side, b[1]+ux*offset*side
                points = [(bx+ux*x-uy*y, by+uy*x+ux*y)
                          for x,y in ((-bw/2,-bh/2),(bw/2,-bh/2),(bw/2,bh/2),(-bw/2,bh/2))]
                pixels = [xy(p) for p in points]
                bounds = (max(0, int(min(p[0] for p in pixels))), max(0, int(min(p[1] for p in pixels))),
                          min(width, math.ceil(max(p[0] for p in pixels))), min(height, math.ceil(max(p[1] for p in pixels))))
                if bounds[0]>=bounds[2] or bounds[1]>=bounds[3] or mask.crop(bounds).getbbox(): continue
                if rng.random() < (.04 if downtown else .16):
                    x,y = xy((bx,by)); r=max(2, 8*zoom)
                    draw.ellipse((x-r,y-r,x+r,y+r), fill='#4b6950' if satellite else '#2e493d')
                    continue
                if satellite:
                    draw.polygon([(x+4*zoom,y+5*zoom) for x,y in pixels], fill='#4f554f')
                draw.polygon(pixels, fill=rng.choice(('#9e9c90','#a6adb0','#879594','#b4ac9a')) if satellite
                             else rng.choice(('#303e50','#364354','#35494b','#43434c')),
                             outline='#737e7c' if satellite else '#3b4a60')
    for paths_to_draw, major in ((paths, False), (arteries, True)):
        for path, road_width in paths_to_draw:
            pixels = [xy(p) for p in path]
            draw.line(pixels, fill='#96988a' if satellite else '#344355', width=max(2, round((road_width+3)*zoom)), joint='curve')
            draw.line(pixels, fill=('#555d60' if satellite else '#65758a') if major else
                      ('#616766' if satellite else '#45556b'), width=max(1, round(road_width*zoom)), joint='curve')
    return surface
