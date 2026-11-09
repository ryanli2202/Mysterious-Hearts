"""Build lightweight illustrated venue backgrounds using native drawing primitives."""
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]

def render(key):
    im = Image.new('RGB', (1200, 600), '#202c40')
    d = ImageDraw.Draw(im)
    d.rectangle((0, 390, 1200, 600), fill='#514c57')
    d.polygon([(0,0),(1200,0),(1080,100),(120,100)], fill='#152032')
    d.line((0,390,1200,390), fill='#c6a878', width=4)
    if key == 'bowling_alley':
        for x in range(0,1200,240):
            d.polygon([(x+70,250),(x+170,250),(x+240,600),(x,600)], fill='#c39b69')
            for y in range(4):
                for j in range(y+1):
                    px=x+120+(j-y/2)*17; py=270+y*16
                    d.ellipse((px-5,py-16,px+5,py),fill='#fff6de')
                    d.line((px-4,py-10,px+4,py-10),fill='#b84c54',width=3)
        d.ellipse((720,480,785,545),fill='#3e658f')
    elif key == 'arcade':
        for i,x in enumerate(range(80,1150,180)):
            color=['#64cbbb','#b677ce','#db957b'][i%3]
            d.polygon([(x,180),(x+120,180),(x+130,480),(x-15,480)],fill='#111c30',outline=color,width=5)
            d.rectangle((x+14,220,x+106,320),fill='#283b58',outline=color,width=3)
            for j in range(4): d.rectangle((x+26+j*18,250+j%2*20,x+36+j*18,262+j%2*20),fill=color)
            d.polygon([(x+5,340),(x+114,340),(x+128,380),(x-9,380)],fill=color)
    elif key == 'nightclub':
        for x,color in [(180,'#4e537f'),(580,'#694f80'),(980,'#375d74')]:
            d.polygon([(x,70),(x-180,440),(x+200,440)],fill=color)
        d.rectangle((380,240,820,365),fill='#172037',outline='#d78bcd',width=5)
        for x in (470,650): d.ellipse((x,270,x+75,315),outline='#84d1d0',width=4)
        for y in range(430,600,55):
            for x in range(100,1100,100): d.rectangle((x,y,x+93,y+48),fill=['#657baa','#896285','#4d8f92'][(x//100+y//55)%3])
    elif key == 'bar':
        d.rectangle((180,100,1020,320),fill='#3a2c35')
        for y in (150,230,310):
            d.line((180,y,1020,y),fill='#bd9262',width=7)
            for x in range(215,1000,65):
                d.rectangle((x,y-34,x+19,y-6),fill='#738f80'); d.rectangle((x+6,y-43,x+13,y-32),fill='#b7ab7c')
        d.rectangle((100,350,1100,410),fill='#b58c63')
        d.rectangle((120,411,1080,545),fill='#664d43')
        for x in range(220,1100,200):
            d.ellipse((x-45,440,x+45,470),fill='#9b6261'); d.line((x,470,x,590),fill='#292b36',width=12)
    elif key in ('public_park','beach'):
        d.rectangle((0,0,1200,600),fill='#9abcc5')
        d.ellipse((920,60,1000,140),fill='#f9e7b9')
        if key=='beach':
            d.rectangle((0,260,1200,600),fill='#568e9e')
            d.polygon([(0,430),(400,380),(850,420),(1200,360),(1200,600),(0,600)],fill='#d9c59e')
            for x in range(0,1200,140): d.arc((x,310,x+200,350),0,150,fill='#d5e8df',width=4)
            d.line((900,410,900,540),fill='#665e55',width=7)
            d.polygon([(790,420),(900,350),(1010,420)],fill='#b36f70')
        else:
            d.rectangle((0,290,1200,600),fill='#6e8a6c')
            d.polygon([(520,300),(620,300),(920,600),(260,600)],fill='#c8b79b')
            for x,y in [(100,270),(300,240),(900,260),(1100,260)]:
                d.rectangle((x-10,y,x+10,y+180),fill='#77614e'); d.ellipse((x-100,y-100,x+100,y+70),fill='#466d57')
            d.rectangle((800,460,1020,480),fill='#9c7956')
            for x in (820,1000): d.line((x,480,x,540),fill='#3a4c49',width=9)
    elif key=='library':
        for x in (80,380,680,980):
            d.rectangle((x,100,x+180,420),fill='#5d4c45')
            for y in (180,260,340,420):
                for j in range(8): d.rectangle((x+8+j*21,y-65,x+23+j*21,y-6),fill=['#a78670','#647e87','#9c7776','#b2aa88'][j%4])
                d.line((x,y,x+180,y),fill='#c2a981',width=6)
        d.ellipse((340,440,860,530),fill='#b79b78')
        d.rectangle((550,462,650,490),fill='#eee1c7')
    elif key=='shopping_mall':
        d.rectangle((420,40,780,290),fill='#accbd3')
        for x in (450,530,610,690,770): d.line((x,40,x,290),fill='#dee2db',width=6)
        for x in (30,260,800,1030):
            d.rectangle((x,230,x+150,450),fill='#304655',outline='#ccb795',width=6)
            d.rectangle((x,200,x+150,240),fill='#ad7e7e')
            for j in range(3): d.ellipse((x+15+j*40,320,x+40+j*40,350),fill='#c2a58b')
        d.polygon([(480,390),(720,390),(1000,600),(200,600)],fill='#b7b7b0')
        for x in (430,770): d.ellipse((x-40,340,x+40,430),fill='#527960')
    return im

if __name__ == '__main__':
    import sys
    sys.path.insert(0,str(ROOT))
    from public_venues import VENUES
    for key in VENUES:
        if key in ('downtown', 'public_park'): continue  # Preserve generated scene artwork.
        render(key).save(ROOT/'assets'/'ui'/'locations'/f'{key}.png')
