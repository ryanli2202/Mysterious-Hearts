"""Portable, code-drawn gang badges; the design lives in the story save."""
import math
from functools import lru_cache
from PIL import Image, ImageDraw, ImageFont

SHAPES = ('Shield', 'Circle', 'Diamond', 'Hexagon')
SYMBOLS = ('Lightning', 'Star', 'Crown', 'Crossed blades', 'Initials')
BACKGROUNDS = {'Slate': '#202c40', 'Midnight': '#121b30', 'Charcoal': '#25252e', 'Forest': '#17372f', 'Plum': '#35233f'}
ACCENTS = {'Mint': '#63e6be', 'Amber': '#ffbf59', 'Crimson': '#ff647c', 'Violet': '#b69aff', 'Sky': '#6bcfff', 'Rose': '#ff91cf'}
DEFAULT = dict(shape='Shield', symbol='Lightning', background='Slate', accent='Mint', initials='GC')


def validate(design):
    if not isinstance(design, dict): raise ValueError('Choose an icon design.')
    result = {key: design.get(key, value) for key,value in DEFAULT.items()}
    for key, choices in (('shape',SHAPES), ('symbol',SYMBOLS), ('background',BACKGROUNDS), ('accent',ACCENTS)):
        if not isinstance(result[key],str) or result[key] not in choices: raise ValueError('Choose a listed '+key+'.')
    initials = result['initials']
    if not isinstance(initials,str): raise ValueError('Use 1–3 letters or numbers for initials.')
    initials = initials.strip().upper()
    if not 1 <= len(initials) <= 3 or any(c not in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789' for c in initials):
        raise ValueError('Use 1–3 letters or numbers for initials.')
    result['initials'] = initials
    return result


def saved(gang):
    try: return validate(gang.get('icon'))
    except ValueError: return dict(DEFAULT)


def apply(s, design):
    import custom_gangs
    gang = custom_gangs.crew(s)
    gang['icon'] = validate(design)
    return custom_gangs.jobs.log(s, 'Gang icon updated for '+gang['name']+'.', True)


def reset(s):
    import custom_gangs
    gang = custom_gangs.crew(s)
    gang.pop('icon', None)
    return custom_gangs.jobs.log(s, 'Restored the default gang icon for '+gang['name']+'.', True)


def render(design, size=96):
    design = validate(design)
    if not isinstance(size,int) or not 16 <= size <= 512: raise ValueError('Icon size must be 16–512 pixels.')
    return _render(tuple(design[k] for k in DEFAULT),size).copy()


@lru_cache(maxsize=128)
def _render(values, size):
    shape,symbol,background,accent,initials = values
    art = Image.new('RGBA',(512,512)); draw=ImageDraw.Draw(art)
    bg=BACKGROUNDS[background]; ink=ACCENTS[accent]
    if shape=='Circle': draw.ellipse((32,32,480,480),fill=bg,outline=ink,width=16)
    else:
        points = {'Shield':[(64,48),(448,48),(432,308),(368,408),(256,478),(144,408),(80,308)],
                  'Diamond':[(256,24),(488,256),(256,488),(24,256)],
                  'Hexagon':[(144,40),(368,40),(480,256),(368,472),(144,472),(32,256)]}[shape]
        draw.polygon(points,fill=bg); draw.line(points+[points[0]],fill=ink,width=16,joint='curve')
    if symbol=='Lightning': draw.polygon([(278,116),(170,278),(242,278),(218,390),(342,218),(268,218)],fill=ink)
    elif symbol=='Star':
        points=[]
        for i in range(10):
            angle=-math.pi/2+i*math.pi/5; radius=126 if i%2==0 else 55
            points.append((256+math.cos(angle)*radius,256+math.sin(angle)*radius))
        draw.polygon(points,fill=ink)
    elif symbol=='Crown':
        draw.polygon([(144,198),(204,238),(256,154),(308,238),(368,198),(342,330),(170,330)],fill=ink)
        draw.line([(178,352),(334,352)],fill=ink,width=14)
    elif symbol=='Crossed blades':
        for points in ([(152,140),(196,160),(350,330),(330,350),(160,196)],[(360,140),(316,160),(162,330),(182,350),(352,196)]):
            draw.polygon(points,fill=ink)
        draw.line([(292,348),(348,292)],fill=ink,width=16)
        draw.line([(164,292),(220,348)],fill=ink,width=16)
    else:
        font=ImageFont.load_default(size=112 if len(initials)<3 else 88)
        bounds=draw.textbbox((0,0),initials,font=font)
        x=(512-(bounds[2]-bounds[0]))/2-bounds[0]; y=(512-(bounds[3]-bounds[1]))/2-bounds[1]
        draw.text((x,y),initials,font=font,fill=ink)
    return art.resize((size,size),Image.Resampling.LANCZOS)
