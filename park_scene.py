"""Deterministic layered pixel scenery and movement for Winterfield Park."""
from dataclasses import dataclass
from pathlib import Path
import math
import random
import json
from PIL import Image, ImageDraw

WIDTH, HEIGHT, VIEW, GROUND = 1600, 320, 384, 268
SPEED = 48.0
ROOT = Path(__file__).resolve().parent
STOPS = [(88, 'West gate', 'The west gate opens onto Winterfield. Use Back to return to the location overview.'),
         (410, 'Garden bench', 'Pause beside the garden bench beneath the lanterns. Move again to continue.'),
         (830, 'Duck pond', 'Ripples drift through the reeds. The pond stays behind the walking path.'),
         (1180, 'Old oak', 'A broad old oak shades this end of the park. Leaves whisper overhead.'),
         (1510, 'East gate', 'The riverside gate marks the end of the park trail. Use Back to return to the location overview.')]


@dataclass
class Walker:
    x: float = 100
    direction: str = 'right'
    phase: float = 0
    moving: bool = False
    seated: bool = False

    def step(self, axis, dt):
        dt = max(0, min(dt, .05))
        old = self.x
        self.x = max(32, min(WIDTH-32, self.x + axis*SPEED*dt))
        self.moving = abs(self.x-old) > .0001
        if axis: self.direction = 'right' if axis > 0 else 'left'
        if self.moving:
            self.seated = False
            # Match the authored stance-foot speed to actual world movement.
            self.phase = (self.phase + abs(self.x-old)/(14/.6)) % 1
        else: self.phase = 0

    @property
    def camera(self): return max(0, min(WIDTH-VIEW, self.x-VIEW*.43))

    @property
    def nearby(self): return next((s for s in STOPS if abs(s[0]-self.x) < 48), None)


def layers():
    """Code-native scenery, with independent transparent planes for parallax."""
    rng = random.Random(1709)
    result = []
    sky = Image.new('RGB', (VIEW, HEIGHT))
    d = ImageDraw.Draw(sky)
    for y in range(HEIGHT):
        t=y/HEIGHT
        d.line((0,y,VIEW,y), fill=(int(17+24*t),int(25+20*t),int(48+18*t)))
    for _ in range(65):
        x,y=rng.randrange(VIEW),rng.randrange(12,150)
        d.rectangle((x,y,x+1,y+1), fill='#8193b0')
    d.ellipse((288,28,312,52),fill='#b6b79c')
    d.ellipse((281,24,305,48),fill='#17223d')
    result.append(('sky',0,sky))
    def plane():
        im=Image.new('RGBA',(2048,HEIGHT));return im,ImageDraw.Draw(im)
    im,d=plane()
    pts=[(0,230)]+[(x,145+int(21*math.sin(x/150)+13*math.sin(x/61))) for x in range(0,2050,16)]+[(2048,320),(0,320)]
    d.polygon(pts,fill='#26374e')
    for x in range(20,2048,48):
        top=rng.randrange(164,198)
        d.rectangle((x,top,x+27,231),fill='#2b4051')
        for yy in range(top+7,220,9):
            if rng.random()<.65:d.rectangle((x+8,yy,x+10,yy+2),fill='#70735b')
    result.append(('distant-hills',.16,im))
    im,d=plane()
    for x in range(-25,2090,26):
        top=rng.randrange(115,180)
        d.rectangle((x+9,top+35,x+15,257),fill='#273c40')
        d.polygon([(x-14,top+60),(x+12,top),(x+40,top+60)],fill='#294b4c')
        d.polygon([(x-19,top+82),(x+12,top+20),(x+46,top+82)],fill='#2c5150')
    result.append(('woodland',.35,im))
    im,d=plane()
    d.rectangle((0,218,2048,320),fill='#23463e')
    d.ellipse((620,222,1000,264),fill='#304c61')
    for x in range(650,970,27):d.line((x,239+(x%17),x+18,239+(x%17)),fill='#5c8086',width=1)
    for x in range(0,2048,72):
        d.ellipse((x,211,x+85,248),fill='#315746')
        d.rectangle((x+12,228,x+15,234),fill='#73916a')
    result.append(('pond-and-shrubs',.7,im))
    im,d=plane()
    for x in [210,540,1060,1250,1460,1840]:
        d.polygon([(x,248),(x+12,248),(x+15,93),(x+7,82)],fill='#493d3c')
        d.line((x+8,156,x-20,124),fill='#493d3c',width=5)
        for dx,dy,r in [(-33,57,44),(0,40,48),(29,65,39),(-6,86,40)]:
            d.ellipse((x+dx-r,dy-r//2,x+dx+r,dy+r),fill='#254b42')
            d.arc((x+dx-r+8,dy-r//2+6,x+dx+r-7,dy+r-10),190,300,fill='#3d6650',width=5)
    result.append(('near-trees',.9,im))
    im,d=plane()
    d.rectangle((0,256,2048,267),fill='#395d48')
    d.rectangle((0,268,2048,297),fill='#655d57')
    d.line((0,268,2048,268),fill='#94806a',width=2)
    d.rectangle((0,298,2048,320),fill='#203a35')
    for x in range(0,2048,22):
        y=rng.randrange(274,294); d.line((x,y,x+6,y),fill='#7a6b5b')
    for x in [90,380,700,1030,1390,1720]:
        d.rectangle((x,191,x+3,260),fill='#26313a')
        d.rectangle((x-5,183,x+8,196),fill='#37464d')
        d.rectangle((x-3,185,x+6,193),fill='#c3a369')
        d.rectangle((x-7,180,x+10,183),fill='#27313b')
    for x in [385,1160]:
        d.rectangle((x,232,x+43,244),fill='#8d6c50')
        d.line((x,238,x+43,238),fill='#4e4440',width=2)
        d.rectangle((x-3,248,x+47,252),fill='#9a7957')
        for dx in [3,39]:d.rectangle((x+dx,251,x+dx+3,267),fill='#29333a')
    for x in [55,1490]:
        d.rectangle((x,225,x+3,265),fill='#776049')
        d.rectangle((x-12,218,x+27,235),fill='#384c4b')
        d.line((x-6,226,x+20,226),fill='#a3ac8c',width=2)
    result.append(('playable-path',1,im))
    im,d=plane()
    for x in range(0,2048,9):
        y=rng.randrange(304,319)
        d.line((x,320,x+4,y),fill=rng.choice(['#355c42','#41694a','#274737']),width=2)
        if x%63==0:d.rectangle((x+2,y-2,x+4,y),fill='#a17d85')
    result.append(('foreground-grass',1.12,im))
    return result


class Renderer:
    def __init__(self):
        folder=ROOT/'assets/world/park'
        if (folder/'layers.json').exists():
            entries=json.loads((folder/'layers.json').read_text(encoding='utf-8'))
            self.planes=[(e['name'],e['parallax'],Image.open(folder/e['file']).convert('RGBA')) for e in entries]
        else:self.planes=layers()
        folder=ROOT/'assets/sprites/chibi-preview/garrett-v5'
        self.sprites={side:[Image.open(folder/f'walk-{side}-{i:02}.png').convert('RGBA') for i in range(1,25)] for side in ('left','right')}
        self.idle={side:Image.open(folder/f'idle-{side}.png').convert('RGBA') for side in self.sprites}

    def render(self, walker):
        canvas=self.planes[0][2].convert('RGBA').copy()
        for name,factor,im in self.planes[1:]:
            if name=='foreground-grass':continue
            offset=int(walker.camera*factor)
            canvas.alpha_composite(im.crop((offset,0,offset+VIEW,HEIGHT)))
        sprite=self.sprites[walker.direction][int(walker.phase*24)%24] if walker.moving else self.idle[walker.direction]
        canvas.alpha_composite(sprite,(round(walker.x-walker.camera-24),GROUND-61))
        name,factor,im=self.planes[-1];offset=int(walker.camera*factor)
        canvas.alpha_composite(im.crop((offset,0,offset+VIEW,HEIGHT)))
        return canvas
