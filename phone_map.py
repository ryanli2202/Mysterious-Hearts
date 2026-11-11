"""Offline, zoomable Winterfield street map drawn with native Tk vectors."""
import math
import random
import tkinter as tk
import unicodedata
from tkinter import ttk
from PIL import ImageTk

import game_core as core
import phone_apps as apps
import town
import public_venues
import vacant_homes
import outskirts
import crime_sites

# Illustrative town geography, not real-world coordinates or travel distances.
POINTS = {
    'blackhaven': (-60,670), 'fox_hideout':(-180,800), 'fox_home':(-175,820),
    'gordon_apartments':(985,285), 'gordon_home':(1000,300),
    'martos_home':(1075,745), 'elias_home':(810,285),
    'mavis_home':(1090,895), 'camila_home':(1180,570),
    'interpol_briefing':(880,320), 'interpol_training':(855,350), 'interpol_containment':(910,350),
    'neo_home': (215, 950),
    'square': (620, 510), 'flowers': (485, 465), 'boutique': (750, 470),
    'chess': (480, 590), 'marios_pizza': (745, 590), 'noodle_shop': (620, 680),
    'studio': (620, 350), 'arena': (880, 675), 'iron_circle': (880, 810),
    'syndicate': (750, 810), 'campus': (355, 260), 'track': (200, 245),
    'cafe': (350, 380), 'park': (1010, 450), 'blackstone_hq': (750, 350),
    'interpol_hq': (880, 350), 'syndicate_office': (1010, 680),
    'syndicate_hq': (1010, 810), 'archive': (485, 350), 'cycle_shop': (1010, 570),
    'planetarium': (480, 105), 'makerspace': (355, 810), 'market': (620, 810),
    'wetlands': (1010, 950), 'boxing_club': (880, 570),
    'sailing_club': (1150, 680), 'cinema': (485, 680),
    'emily_home': (350, 500), 'sophie_home': (200, 380),
    'amy_home': (350, 120), 'minsu_home': (200, 120),
    'samantha_home': (880, 950), 'april_home': (620, 120),
    'garrett_home': (200, 810), 'rei_home': (750, 240),
    'lena_home': (480, 240), 'naomi_home': (1010, 240),
    'celeste_home': (750, 120), 'dev_home': (350, 950),
    'rosa_home': (620, 950), 'elliot_home': (1150, 950),
    'tyler_home': (880, 470), 'valentina_home': (1150, 810),
    'daniel_home': (485, 810), 'sylvanis_home': (750, 950),
}
POINTS.update({key: v[1] for key, v in public_venues.VENUES.items()})
import organisation_guards
POINTS.update(organisation_guards.POINTS)
POINTS['glasshouse_lab'] = (330, 1030)
POINTS.update({key: data['point'] for key, data in vacant_homes.HOMES.items()})
POINTS.update({key: data['point'] for key, data in crime_sites.SITES.items()})
POINTS.update(lantern_house=(520,880), saints_depot=(310,1080), purple_clubhouse=(910,1080),
              hamayashi_house=(580,1120), rojos_courtyard=(780,1100), consortium_house=(1310,720))
SHORT = {'square': 'Town square', 'flowers': 'Petal & Stem', 'campus': 'University',
         'track': 'University track', 'cafe': 'Campus café', 'studio': 'Modelling studio',
         'noodle_shop': 'Golden Dragon', 'syndicate': 'Red Dragons', 'iron_circle': 'Iron Circle',
         'blackstone_hq': 'Blackstone HQ', 'interpol_hq': 'Interpol HQ',
         'syndicate_office': 'Waterfront offices', 'syndicate_hq': 'Underground HQ',
         'sailing_club': 'Boathouse', 'wetlands': 'Wetland boardwalk',
         'planetarium': 'Planetarium', 'boxing_club': 'Boxing club', 'cinema': 'Bijou cinema',
         'archive': 'Old town archive', 'makerspace': 'Makerspace', 'market': 'Lantern market',
         'cycle_shop': 'Cycle workshop', 'valentina_home': 'Ferry Signal House'}
SHORT.update({key: key.replace('_', ' ').title() for key in public_venues.VENUES})
SHORT.update({key: data['name'] for key, data in vacant_homes.HOMES.items()})
FOOD = {'cafe', 'chess', 'marios_pizza', 'noodle_shop', 'bar', 'shopping_mall'} | outskirts.FOOD
GREEN = {'park', 'wetlands', 'track', 'sailing_club'} | public_venues.OUTDOORS


def normalize(text):
    return ''.join(c for c in unicodedata.normalize('NFKD', text.casefold())
                   if not unicodedata.combining(c))


def map_bounds(state, padding=100):
    """Visible destinations determine camera limits without leaking private pins."""
    points = [POINTS[key] for key in places(state)]
    xs, ys = zip(*points)
    return min(xs)-padding, min(ys)-padding, max(xs)+padding, max(ys)+padding


def fit_camera(state, width, height):
    left, top, right, bottom = map_bounds(state)
    return ((left+right)/2, (top+bottom)/2,
            max(.05, min(2.8, max(1, width)/(right-left), max(1, height)/(bottom-top))))


def metropolitan_view(width, height, cx, cy, zoom, satellite=False):
    from city_map import render
    return render(width, height, cx, cy, zoom, satellite)


def places(state, query='', category='All'):
    """The same visibility gate is used for pins, search, and selection."""
    query = normalize(query.strip())
    return {key: town.location_name(state, key) for key, label in town.LOCATIONS.items()
            if key in POINTS and town.hidden.visible_place(state, key)
            and (not query or query in normalize(town.location_name(state, key) + (' ' + key.replace('_', ' ') if key not in crime_sites.SITES else '')))
            and (category == 'All' or category == 'Food' and key in FOOD
                 or category == 'Outdoors' and key in GREEN
                 or category == 'Homes' and key.endswith('_home'))}


class MapView(ttk.Frame):
    def __init__(self, parent, phone):
        super().__init__(parent)
        self.pack(fill='both', expand=True)
        self.phone = phone
        import weather
        self.weather_label=ttk.Label(self, text=weather.summary(phone.game.state_data['world']['minute']))
        self.weather_label.pack(anchor='w', padx=8, pady=4)
        self.memory = phone.map_memory
        self.layer = self.memory.get('layer', 'Map')
        self.terrain_photo = None
        self.cx, self.cy, self.zoom = self.memory.get('camera', (700, 500, .60))
        self.selected = self.memory.get('selected')
        self.category = 'All'
        self.people = {}
        self.stamp = None
        self.drag = None
        self.hitboxes = []
        self.label_boxes = []
        self.query = tk.StringVar()
        search = ttk.Frame(self)
        search.pack(fill='x', pady=(0, 6))
        ttk.Label(search, text='⌕', font=('Segoe UI', 18)).pack(side='left', padx=(0, 6))
        self.entry = ttk.Entry(search, textvariable=self.query, font=('Segoe UI', 11))
        self.entry.pack(side='left', fill='x', expand=True)
        self.entry.bind('<Return>', self.search_first)
        ttk.Button(search, text='Search', command=self.search_first).pack(side='left', padx=(5, 0))
        ttk.Button(search, text='×', width=3, command=lambda: self.query.set('')).pack(side='left')
        ttk.Label(self, text='Search Winterfield · drag to pan · scroll to zoom',
                  foreground='#9da9be').pack(anchor='w', pady=(0, 6))
        self.results = tk.Listbox(self, height=3, bg='#293447', fg='#a4b8d0',
                                  selectbackground='#354d69', selectforeground='#99c4ed',
                                  relief='flat', highlightthickness=0, exportselection=False)
        self.results.bind('<<ListboxSelect>>', self.choose_result)
        self.result_keys = []
        filters = ttk.Frame(self)
        filters.pack(fill='x', pady=(0, 7))
        self.filter_buttons = {}
        for name in ('All', 'Food', 'Outdoors', 'Homes'):
            button = ttk.Button(filters, text=name, width=9, command=lambda n=name: self.filter(n))
            button.pack(side='left', padx=(0, 3))
            self.filter_buttons[name] = button
        self.filter_buttons['All'].state(['pressed'])
        self.map_area = tk.Frame(self, bg='#1c2433')
        # Reserve the detail card before giving the map the remaining space.
        self.card = ttk.Frame(self, padding=(0, 8, 0, 0))
        self.card.pack(side='bottom', fill='x')
        self.place_title = ttk.Label(self.card, font=('Segoe UI', 13, 'bold'), wraplength=465)
        self.place_title.pack(anchor='w')
        self.place_status = ttk.Label(self.card, wraplength=465, foreground='#9da9be')
        self.place_status.pack(anchor='w', pady=(2, 5))
        people_frame = ttk.Frame(self.card)
        people_frame.pack(fill='x')
        self.people_text = tk.Text(people_frame, height=3, wrap='word', relief='flat',
                                   bg='#202b3e', fg='#edf1fa', font=('Segoe UI', 10),
                                   padx=8, pady=6, state='disabled')
        scroll = ttk.Scrollbar(people_frame, command=self.people_text.yview)
        scroll.pack(side='right', fill='y')
        self.people_text.pack(side='left', fill='x', expand=True)
        self.people_text.config(yscrollcommand=scroll.set)
        actions = ttk.Frame(self.card)
        actions.pack(fill='x', pady=(6, 0))
        self.drive_button = ttk.Button(actions, text='Drive here', command=self.drive)
        self.drive_button.pack(side='right')
        self.trip_label = ttk.Label(actions, text='', wraplength=300)
        self.trip_label.pack(side='left', fill='x', expand=True)
        self.map_area.pack(fill='both', expand=True)
        self.canvas = tk.Canvas(self.map_area, bg='#1c2433', highlightthickness=0,
                                height=350, takefocus=True, cursor='hand2')
        self.canvas.pack(fill='both', expand=True)
        self.canvas.bind('<Configure>', lambda event: self.draw())
        self.canvas.bind('<ButtonPress-1>', self.press)
        self.canvas.bind('<B1-Motion>', self.motion)
        self.canvas.bind('<ButtonRelease-1>', self.release)
        self.canvas.bind('<MouseWheel>', self.wheel)
        self.canvas.bind('<Button-4>', lambda e: self.change_zoom(1.25, e.x, e.y))
        self.canvas.bind('<Button-5>', lambda e: self.change_zoom(.8, e.x, e.y))
        self.canvas.bind('<KeyPress>', self.key)
        layers = tk.Frame(self.map_area, bg='#293447', padx=3, pady=3)
        layers.place(x=10, y=10)
        self.layer_buttons = {}
        for name in ('Map', 'Satellite'):
            button = tk.Button(layers, text=name, relief='flat', font=('Segoe UI', 9, 'bold'),
                               command=lambda n=name: self.set_layer(n))
            button.pack(side='left')
            self.layer_buttons[name] = button
        self.update_layer_buttons()
        tools = tk.Frame(self.map_area, bg='#1c2433', padx=3, pady=3)
        tools.place(relx=1, x=-10, y=10, anchor='ne')
        for label, command in (('+', lambda: self.change_zoom(1.25)),
                               ('−', lambda: self.change_zoom(.8)),
                               ('↑', lambda: self.pan(0, -100)),
                               ('←', lambda: self.pan(-100, 0)),
                               ('→', lambda: self.pan(100, 0)),
                               ('↓', lambda: self.pan(0, 100))):
            tk.Button(tools, text=label, command=command, width=2, relief='flat',
                      bg='#293447', fg='#a4b8d0', font=('Segoe UI', 11)).pack()
        bottom = tk.Frame(self.map_area, bg='#1c2433')
        bottom.place(x=10, rely=1, y=-10, anchor='sw')
        for label, command in (('◎ My location', self.locate), ('Fit town', self.fit)):
            tk.Button(bottom, text=label, command=command, relief='flat', bg='#293447',
                      fg='#99c4ed', font=('Segoe UI', 9, 'bold')).pack(side='left', padx=3)
        self.query.trace_add('write', lambda *args: self.search())
        self.sync()
        if self.selected not in places(self.state):
            current = self.state['world']['location']
            self.selected = current if current in places(self.state) else 'square'
        self.detail()

    @property
    def state(self):
        return self.phone.game.state_data

    def save_camera(self):
        self.memory.update(camera=(self.cx, self.cy, self.zoom), selected=self.selected, layer=self.layer)

    def update_layer_buttons(self):
        for name, button in self.layer_buttons.items():
            button.config(bg='#354d69' if name == self.layer else '#293447',
                          fg='#99c4ed' if name == self.layer else '#a4b8d0',
                          relief='sunken' if name == self.layer else 'flat')

    def set_layer(self, name):
        if name not in ('Map', 'Satellite'): return
        self.layer = name
        self.update_layer_buttons()
        self.save_camera()
        self.draw()

    def filter(self, category):
        self.category = category
        for name, button in self.filter_buttons.items():
            button.state(['pressed'] if name == category else ['!pressed'])
        self.search()

    def search(self):
        found = places(self.state, self.query.get(), self.category)
        self.result_keys = sorted(found, key=lambda k: found[k])
        self.results.delete(0, 'end')
        if self.query.get().strip():
            for key in self.result_keys: self.results.insert('end', found[key])
            if not found: self.results.insert('end', 'No matching locations')
            self.results.config(height=min(3, max(1, len(found))))
            self.results.pack(before=self.filter_buttons['All'].master, fill='x', pady=(0, 6))
        else:
            self.results.pack_forget()
        self.draw()

    def search_first(self, event=None):
        self.search()
        if self.result_keys:
            self.select(self.result_keys[0], center=True)
        return 'break'

    def choose_result(self, event):
        selected = self.results.curselection()
        if selected and selected[0] < len(self.result_keys):
            self.select(self.result_keys[selected[0]], center=True)

    def select(self, key, center=False):
        if key not in places(self.state):
            return
        self.selected = key
        if center:
            self.cx, self.cy = POINTS[key]
            self.zoom = max(1., self.zoom)
        self.save_camera()
        self.detail()
        self.draw()

    def sync(self):
        import weather
        self.weather_label.config(text=weather.summary(self.state['world']['minute']))
        people = apps.location_people(self.state)
        world = self.state['world']
        trip = world['cast'][self.state['player']]['journey']
        stamp = (repr(people), repr(trip), world['minute'], world['location'],
                 tuple(places(self.state).items()), tuple(world['party']))
        if stamp == self.stamp:
            return
        self.stamp, self.people = stamp, people
        if self.selected not in places(self.state):
            self.selected = None
        self.detail()
        self.search()

    def detail(self):
        world = self.state['world']
        trip = world['cast'][self.state['player']]['journey']
        self.place_title.config(text=town.location_name(self.state, self.selected) if self.selected in town.LOCATIONS else 'Explore Winterfield')
        self.place_status.config(text=('Your current location' if self.selected == world['location'] and not trip
                                      else 'Click a marker to see people and plan a drive.' if not self.selected
                                      else 'Live presence · arrivals shown separately'))
        if self.selected in public_venues.VENUES:
            venue = public_venues.VENUES[self.selected]
            detail = venue[2] + ' · ' + venue[3]
            if self.selected in public_venues.EVENING:
                detail += ' · Activity from ' + str(public_venues.EVENING[self.selected]) + ':00'
            self.place_status.config(text=detail)
        if self.selected in vacant_homes.HOMES:
            self.place_status.config(text=vacant_homes.status(self.state, self.selected))
        if self.selected in crime_sites.SITES:
            self.place_status.config(text='Visit this location to inspect the frontage or enter reception. Restricted rooms require clearance.')
        names = self.people.get(self.selected, [])
        present = [n for n in names if ' · On the way (' not in n]
        incoming = [n for n in names if ' · On the way (' in n]
        text = 'Here now: ' + (', '.join(present) or 'Nobody here right now')
        if incoming: text += '\nArriving: ' + '; '.join(incoming)
        self.people_text.config(state='normal')
        self.people_text.delete('1.0', 'end')
        self.people_text.insert('1.0', text)
        self.people_text.config(state='disabled')
        party = ', '.join(core.contact_name(self.state, p) for p in world['party'])
        self.trip_label.config(text='Instant travel · With: ' + (party or 'Just you'))
        self.drive_button.config(text='You are here' if self.selected == world['location'] else 'Travel here',
                                 state='normal' if self.selected and self.selected != world['location'] else 'disabled')

    def drive(self):
        if self.selected in places(self.state):
            self.phone.act(town.travel, self.selected)

    def xy(self, x, y):
        return ((x - self.cx) * self.zoom + self.canvas.winfo_width() / 2,
                (y - self.cy) * self.zoom + self.canvas.winfo_height() / 2)

    def world_xy(self, x, y):
        return ((x - self.canvas.winfo_width() / 2) / self.zoom + self.cx,
                (y - self.canvas.winfo_height() / 2) / self.zoom + self.cy)

    def pan(self, dx, dy):
        left, top, right, bottom = map_bounds(self.state)
        self.cx = max(left, min(right, self.cx + dx / self.zoom))
        self.cy = max(top, min(bottom, self.cy + dy / self.zoom))
        self.save_camera()
        self.draw()

    def change_zoom(self, factor, x=None, y=None):
        x = self.canvas.winfo_width() / 2 if x is None else x
        y = self.canvas.winfo_height() / 2 if y is None else y
        wx, wy = self.world_xy(x, y)
        self.zoom = max(.05, min(2.8, self.zoom * factor))
        self.cx = wx - (x - self.canvas.winfo_width() / 2) / self.zoom
        self.cy = wy - (y - self.canvas.winfo_height() / 2) / self.zoom
        self.save_camera()
        self.draw()
        return 'break'

    def wheel(self, event):
        return self.change_zoom(1.25 if event.delta > 0 else .8, event.x, event.y)

    def key(self, event):
        directions = {'Left': (-100, 0), 'Right': (100, 0), 'Up': (0, -100), 'Down': (0, 100)}
        if event.keysym in directions: self.pan(*directions[event.keysym])
        elif event.char in ('+', '='): self.change_zoom(1.25)
        elif event.char == '-': self.change_zoom(.8)
        else: return
        return 'break'

    def press(self, event):
        self.canvas.focus_set()
        self.drag = (event.x, event.y, self.cx, self.cy)
        self.moved = False

    def motion(self, event):
        if not self.drag: return
        x, y, cx, cy = self.drag
        if math.hypot(event.x - x, event.y - y) > 5: self.moved = True
        if self.moved:
            left, top, right, bottom = map_bounds(self.state)
            self.cx = max(left, min(right, cx - (event.x - x) / self.zoom))
            self.cy = max(top, min(bottom, cy - (event.y - y) / self.zoom))
            self.draw()

    def release(self, event):
        if not self.drag: return
        if not self.moved:
            picked = False
            for key, x, y in reversed(self.hitboxes):
                if math.hypot(event.x - x, event.y - y) <= 17:
                    self.select(key)
                    picked = True
                    break
            if not picked:
                for key, (x1, y1, x2, y2) in self.label_boxes:
                    if x1 <= event.x <= x2 and y1 <= event.y <= y2:
                        self.select(key)
                        break
        self.drag = None
        self.save_camera()

    def player_position(self):
        world = self.state['world']
        trip = world['cast'][self.state['player']]['journey']
        if trip:
            # Show only known geography; do not expose private destinations.
            visible = places(self.state)
            if trip['origin'] in visible and trip['destination'] in visible:
                a, b = POINTS[trip['origin']], POINTS[trip['destination']]
                t = max(0, min(1, (world['minute'] - trip['departed']) / max(1, trip['arrives'] - trip['departed'])))
                return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)
            return None
        import crime_operations
        key = crime_operations.site_of(world['location'])
        return POINTS.get(key) if key in places(self.state) else None

    def locate(self):
        point = self.player_position()
        if point:
            self.cx, self.cy = point
            self.zoom = max(.9, self.zoom)
            import crime_operations
            current = crime_operations.site_of(self.state['world']['location'])
            if current in places(self.state): self.select(current)
            self.save_camera()
            self.draw()
        else:
            self.place_status.config(text='Your current location is private or unavailable on this map.')

    def fit(self):
        self.cx, self.cy, self.zoom = fit_camera(
            self.state, self.canvas.winfo_width(), self.canvas.winfo_height())
        self.save_camera()
        self.draw()

    def polygon(self, coords, **kw):
        return self.canvas.create_polygon(*[n for point in coords for n in self.xy(*point)], **kw)

    def road(self, coords, color, width):
        self.canvas.create_line(*[n for point in coords for n in self.xy(*point)],
                                fill=color, width=max(1, width * self.zoom), joinstyle='round', capstyle='round', smooth=True, splinesteps=24)

    def draw(self):
        if not hasattr(self, 'canvas'): return
        c = self.canvas
        c.delete('all')
        w, h = c.winfo_width(), c.winfo_height()
        satellite = self.layer == 'Satellite'
        c.config(bg='#777c7b' if satellite else '#1c2433')
        terrain = metropolitan_view(w, h, self.cx, self.cy, self.zoom, satellite)
        self.terrain_photo = ImageTk.PhotoImage(terrain, master=c)
        c.create_image(0, 0, image=self.terrain_photo, anchor='nw',
                       tags='satellite-terrain' if satellite else 'metropolitan-terrain')
        # Parks, university grounds, and a curving river form the base map texture.
        for coords, color in (
            ([(70, 50), (680, 50), (680, 175), (70, 175)], '#2c4337'),
            ([(120, 190), (410, 190), (410, 420), (120, 420)], '#293447'),
            ([(145, 450), (250, 450), (250, 535), (145, 535)], '#2c4b3e'),
            ([(1250, 490), (1320, 490), (1340, 650), (1230, 650)], '#514937'),
            ([(950, 300), (1090, 300), (1110, 530), (950, 530)], '#2c4b3e'),
            ([(940, 870), (1250, 870), (1250, 1060), (940, 1060)], '#2b463c'),
            ([(1130, -100000), (1100, 200), (1180, 480), (1160, 700), (1270, 1100), (1380, 100000),
              (1490, 100000), (1370, 1100), (1240, 700), (1260, 480), (1180, 200), (1230, -100000)], '#244659')):
            aerial_colors = {'#2c4337': '#556744', '#293447': '#77786b',
                             '#2c4b3e': '#4e683f', '#2b463c': '#4c6142', '#244659': '#315c62', '#514937': '#b6a37f'}
            self.polygon(coords, fill=aerial_colors[color] if satellite else color, outline='', smooth=True, splinesteps=24)
        if satellite:
            foliage = random.Random(88)
            for _ in range(550):
                x, y = foliage.uniform(950, 1080), foliage.uniform(315, 520)
                if foliage.random() < .3: y += 570
                sx, sy = self.xy(x, y)
                if not (-20 < sx < w+20 and -20 < sy < h+20): continue
                r = foliage.uniform(2, 7) * self.zoom
                c.create_oval(sx-r+2, sy-r+3, sx+r+2, sy+r+3, fill='#30422d', outline='')
                c.create_oval(sx-r, sy-r, sx+r, sy+r, fill=foliage.choice(('#3c5634', '#587849', '#496a3e')), outline='')
        # The continuous street geometry is rendered in the base layer.
        # These bridges preserve crossings over the river overlay.
        for bridge in ([(1070, 570), (1180, 580), (1320, 610)],
                       [(1070, 190), (1140, 190), (1260, 210)]):
            self.road(bridge, '#8d928b' if satellite else '#344355', 20)
            self.road(bridge, '#60676a' if satellite else '#65758a', 14)
        self.road([(1010, 345), (1040, 400), (985, 470), (1040, 505)], '#a79d7b' if satellite else '#65758a', 5)
        self.road([(990, 910), (1040, 955), (1120, 975), (1180, 920)], '#a79d7b' if satellite else '#65758a', 4)
        for x, y in ((975, 330), (1060, 350), (980, 410), (1055, 480), (975, 500), (1020, 900), (1080, 980)):
            sx, sy = self.xy(x, y)
            r = 9 * self.zoom
            c.create_oval(sx-r, sy-r, sx+r, sy+r, fill='#61804d' if satellite else '#456750', outline='')
        for x, y, text in ((340, 215, 'UNIVERSITY'), (655, 385, 'DOWNTOWN'),
                           (300, 760, 'HILLSIDE'), (900, 900, 'EAST WARD')):
            if self.zoom >= .5:
                c.create_text(*self.xy(x, y), text=text, fill='#d6dcc9' if satellite else '#abbfae', font=('Segoe UI', 9))
        if self.zoom > .65:
            for x, y, text in ((720, 535, 'Winterfield Avenue'), (410, 700, 'Market Street'), (890, 310, 'College Road')):
                c.create_text(*self.xy(x, y), text=text, fill='#e0d8bc' if satellite else '#c7bda3', font=('Segoe UI', 8))
        c.create_text(*self.xy(1210, 430), text='Winter River', angle=75, fill='#a4d6e1' if satellite else '#4c93b2', font=('Segoe UI', 10, 'italic'))
        for x, y, label in outskirts.DISTRICTS:
            sx, sy = self.xy(x, y)
            if 0 <= sx <= w and 0 <= sy <= h-45:
                anchor = 'w' if sx < 110 else 'e' if sx > w-110 else 'center'
                if anchor == 'e':
                    sx = min(sx, w-55)  # Keep district text clear of the pan controls.
                c.create_text(sx, sy, text=label, anchor=anchor,
                              fill='#9da9be', font=('Segoe UI', 9, 'bold'))
        trip = self.state['world']['cast'][self.state['player']]['journey']
        visible = places(self.state)
        if trip and trip['origin'] in visible and trip['destination'] in visible:
            self.road([POINTS[trip['origin']], POINTS[trip['destination']]], '#8fb9ed', 6)
        shown = places(self.state, self.query.get(), self.category)
        self.hitboxes = []
        self.label_boxes = []
        occupied = []
        # Selected marker is drawn last, and its label takes priority.
        order = sorted(shown, key=lambda key: key == self.selected)
        label_order = sorted(shown, key=lambda key: key != self.selected)
        for key in order:
            x, y = self.xy(*POINTS[key])
            if not (-30 < x < w + 30 and -30 < y < h + 30): continue
            color = '#d97927' if key in FOOD else '#43936b' if key in GREEN else '#8c78a9' if key.endswith('_home') else '#517fba'
            radius = 10 if key == self.selected else 7
            if key == self.selected:
                c.create_oval(x-15, y-15, x+15, y+15, fill='#354d69', outline='#99c4ed', width=2)
            c.create_oval(x-radius, y-radius, x+radius, y+radius, fill=color, outline='#a4b8d0', width=2)
            c.create_oval(x-2, y-2, x+2, y+2, fill='#a4b8d0', outline='')
            self.hitboxes.append((key, x, y))
            count = sum(' · On the way (' not in name for name in self.people.get(key, []))
            if count and self.zoom >= .6:
                c.create_oval(x+5, y-17, x+21, y-1, fill='#273e51', outline='#a4b8d0')
                c.create_text(x+13, y-9, text=str(count), fill='#a4b8d0', font=('Segoe UI', 7, 'bold'))
        for key in label_order:
            x, y = self.xy(*POINTS[key])
            if not (15 < x < w-70 and 10 < y < h-15): continue
            if self.zoom < .55 and key != self.selected: continue
            label = (town.location_name(self.state, key).split(' · ')[0] if key in crime_sites.SITES
                     else SHORT.get(key, town.LOCATIONS[key].split(' · ')[0]))
            if self.state.get('custom_protagonist', {}).get('home') == key:
                label = 'Your home'
            if key.endswith('_home') and key not in SHORT: label = label.split('’')[0] + '’s home'
            item = c.create_text(x+14, y+5, text=label, anchor='nw', fill='#a4b8d0' if satellite else '#a4b8d0', font=('Segoe UI', 9, 'bold' if key == self.selected else 'normal'))
            box = c.bbox(item)
            if key != self.selected and any(box[0] < b[2]+6 and box[2] > b[0]-6 and box[1] < b[3]+5 and box[3] > b[1]-5 for b in occupied):
                c.delete(item)
                continue
            occupied.append(box)
            self.label_boxes.append((key, box))
            bg = c.create_rectangle(box[0]-2, box[1]-1, box[2]+2, box[3]+1, fill='#2f3b34' if satellite else '#1c2433', outline='')
            c.tag_lower(bg, item)
        position = self.player_position()
        if position:
            x, y = self.xy(*position)
            c.create_oval(x-13, y-13, x+13, y+13, fill='#354d69', outline='')
            c.create_oval(x-7, y-7, x+7, y+7, fill='#1a73e8', outline='#a4b8d0', width=2)
        caption = 'simulated aerial' if satellite else 'illustrated map'
        c.create_text(w-8, h-7, anchor='se', text=f'Winterfield · {caption} · {round(self.zoom*100)}%',
                      fill='#edf2df' if satellite else '#b2c1cd', font=('Segoe UI', 8))
