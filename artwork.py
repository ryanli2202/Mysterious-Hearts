"""Responsive generated artwork, with live text and transparent character layers."""
from functools import lru_cache
from pathlib import Path
import tkinter as tk
from PIL import Image, ImageOps, ImageTk, ImageEnhance, ImageDraw
import outskirts

ASSETS = Path(__file__).resolve().parent / 'assets' / 'ui'


@lru_cache(maxsize=8)
def source_image(name):
    if isinstance(name, tuple):
        base, light, condition = name
        image = source_image(base).copy().convert('RGB')
        strength = {'night': .44, 'dawn': .76, 'dusk': .66, 'day': 1.0}[light]
        image = ImageEnhance.Brightness(image).enhance(strength)
        tint = '#243a65' if light == 'night' else '#ce906b' if light in ('dawn','dusk') else '#63778b'
        if light != 'day' or condition in ('Rain','Snow','Cloudy'):
            image = Image.blend(image, Image.new('RGB',image.size,tint), .17)
        # Rain on exterior scenes; indoor artwork keeps its sheltered lighting.
        outdoor = base in ('campus-day','winterfield-dusk') or base in ('locations/downtown','locations/park','locations/public_park','locations/beach','locations/wetlands','locations/track','locations/sailing_club')
        outdoor = outdoor or base in {'locations/' + place for place in outskirts.OUTDOORS}
        import crime_sites
        outdoor = outdoor or base in {'locations/' + place for place in crime_sites.SITES}
        outdoor = outdoor or base in {'locations/blackhaven','locations/fox_hideout','locations/gordon_apartments'}
        if outdoor and condition in ('Rain','Snow'):
            draw=ImageDraw.Draw(image)
            for x in range(10,image.width,47):
                for y in range((x*13)%91,image.height,91):
                    if condition=='Rain': draw.line((x,y,x-5,y+16),fill='#8fa9bf',width=1)
                    else: draw.ellipse((x,y,x+3,y+3),fill='#dce5ed')
        return image.convert('RGBA')
    path = ASSETS / (name + '.png')
    if not path.exists():
        return Image.new('RGB', (16, 16), '#10121c')
    with Image.open(path) as image:
        return image.convert('RGBA')


def scene_art(location, texting=False, minute=None):
    if location == 'glasshouse_lab': return 'locations/site_03_interior'
    import crime_operations
    if location in crime_operations.ROOMS and not texting:
        return 'locations/'+crime_operations.ROOMS[location][0]+'_interior'
    if minute is not None and not texting:
        import weather
        w=weather.at(minute)
        return (scene_art(location), w['light'], w['condition'])
    # Text conversations have no shared physical setting.
    if texting:
        return 'ui-header'
    if location == 'campus':
        return 'campus-day'
    if location == 'cafe':
        return 'cafe-evening'
    if location == 'square':
        return 'winterfield-dusk'
    if location.startswith('car:'):
        return 'locations/motorcycle' if location == 'car:samantha' else 'locations/transit'
    if location.isidentifier() and (ASSETS / 'locations' / (location + '.png')).is_file():
        return 'locations/' + location
    return 'ui-header'


class ArtCanvas(tk.Canvas):
    def __init__(self, parent, artwork, stretch=False, **kwargs):
        super().__init__(parent, bg='#10121c', highlightthickness=0, bd=0, **kwargs)
        self.artwork = artwork
        self.stretch = stretch
        self.background_item = self.create_image(0, 0, anchor='nw')
        self.photo = None
        self.render_key = None
        self.bind('<Configure>', self.redraw)

    def set_art(self, name):
        self.artwork = name
        self.redraw()

    def redraw(self, event=None):
        width, height = max(1, self.winfo_width()), max(1, self.winfo_height())
        key = (self.artwork, width, height)
        if key != self.render_key:
            source = source_image(self.artwork)
            fitted = (source.resize((width, height), Image.Resampling.LANCZOS) if self.stretch else
                      ImageOps.fit(source, (width, height), Image.Resampling.LANCZOS))
            self.photo = ImageTk.PhotoImage(fitted, master=self)
            self.itemconfigure(self.background_item, image=self.photo)
            self.render_key = key


class TitleArt(ArtCanvas):
    def __init__(self, parent, title, subtitle='', **kwargs):
        super().__init__(parent, 'ui-header', **kwargs)
        self.title_item = self.create_text(0, 0, text=title, fill='#dfba78', font=('Segoe UI', 25))
        self.subtitle_item = self.create_text(0, 0, text=subtitle, fill='#f3eee7', font=('Segoe UI', 10))
        self.logo_item = self.create_image(0, 0)
        self.logo_photo = None

    def redraw(self, event=None):
        super().redraw(event)
        width, height = self.winfo_width(), self.winfo_height()
        self.coords(self.title_item, width / 2, height * .40)
        self.coords(self.subtitle_item, width / 2, height * .78)
        if (ASSETS / 'title-logo.png').exists():
            logo = source_image('title-logo')
            logo = logo.crop(logo.getbbox())
            logo = ImageOps.contain(logo, (min(720, max(1, width - 180)), max(1, height - 30)), Image.Resampling.LANCZOS)
            self.logo_photo = ImageTk.PhotoImage(logo, master=self)
            self.itemconfigure(self.logo_item, image=self.logo_photo)
            self.itemconfigure(self.title_item, state='hidden')
            self.coords(self.logo_item, width / 2, (height - 25) / 2)
            self.coords(self.subtitle_item, width / 2, height - 12)


class SelectionLabel(ArtCanvas):
    def __init__(self, parent, text, **kwargs):
        super().__init__(parent, 'selection-nameplate', stretch=True, **kwargs)
        self.text_item = self.create_text(0, 0, text=text, fill='#f3eee7', font=('Segoe UI', 14))

    def redraw(self, event=None):
        super().redraw(event)
        self.coords(self.text_item, self.winfo_width() / 2, self.winfo_height() / 2)


class SelectionCard(ArtCanvas):
    def __init__(self, parent, portrait, name, tagline, command):
        super().__init__(parent, 'selection-frame', stretch=True, width=236, height=400)
        self.portrait = portrait
        self.create_image(118, 260, image=portrait, anchor='s')
        self.nameplate = SelectionLabel(self, name, width=212, height=44)
        self.create_window(118, 287, window=self.nameplate)
        self.create_text(118, 324, text=tagline, fill='#c6bdcf', font=('Segoe UI', 10), justify='center')
        self.begin = tk.Button(self, text='Begin as ' + name.split()[0], command=command,
                               font=('Segoe UI', 11), bg='#dfba78', fg='#10121c',
                               activebackground='#f3d79d', activeforeground='#10121c',
                               relief='flat', bd=0, padx=12, pady=9, cursor='hand2',
                               highlightthickness=2, highlightbackground='#8f7045',
                               highlightcolor='#fff1d0')
        self.create_window(118, 365, window=self.begin, width=200)


class SceneArt(ArtCanvas):
    group_width = 312
    portrait_height = 195

    @classmethod
    def group_layout(cls, count):
        # Pick the grid that leaves the most room for each upright portrait.
        def scale(columns):
            rows = (count + columns - 1) // columns
            return min(cls.group_width / (columns * 165), 1 / rows)
        columns = max(range(1, count + 1), key=scale)
        rows = (count + columns - 1) // columns
        return columns, (cls.group_width // columns, cls.portrait_height // rows)

    def __init__(self, parent, **kwargs):
        super().__init__(parent, 'ui-header', **kwargs)
        self.left_item = self.create_image(0, 0, anchor='s')
        self.right_items = []
        self.centre_item = None
        self.portraits = ()

    def set_centre(self, widget):
        self.centre_item = self.create_window(0, 0, window=widget, anchor='center')

    def set_scene(self, artwork, left, participants):
        while len(self.right_items) < len(participants):
            self.right_items.append(self.create_image(0, 0, anchor='s'))
        while len(self.right_items) > len(participants):
            self.delete(self.right_items.pop())
        self.portraits = (left, *participants)
        self.itemconfigure(self.left_item, image=left)
        for item, portrait in zip(self.right_items, participants):
            self.itemconfigure(item, image=portrait)
        self.set_art(artwork)

    def redraw(self, event=None):
        super().redraw(event)
        width, height = self.winfo_width(), self.winfo_height()
        self.coords(self.left_item, 100, height)
        centre_x = width / 2
        centre_width = max(220, min(310, width - 380))
        count = len(self.right_items)
        if count == 1:
            self.coords(self.right_items[0], width - 100, height)
        elif count > 1:
            columns, (cell_width, cell_height) = self.group_layout(count)
            right_centre = width - 8 - self.group_width / 2
            rows = (count + columns - 1) // columns
            for i, item in enumerate(self.right_items):
                row, col = divmod(i, columns)
                in_row = min(columns, count - row * columns)
                x = right_centre + (col - (in_row - 1) / 2) * cell_width
                self.coords(item, x, height - (rows - row - 1) * cell_height)
            right_edge = width - self.group_width - 16
            centre_x = (185 + right_edge) / 2
            centre_width = max(1, min(310, right_edge - 185))
        if self.centre_item is not None:
            self.coords(self.centre_item, centre_x, height / 2)
            self.itemconfigure(self.centre_item, width=centre_width)
