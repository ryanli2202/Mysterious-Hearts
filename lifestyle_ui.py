"""Phone screens for saved social activities and outfit design."""
import queue
import threading
import tkinter as tk
from tkinter import ttk
from datetime import timedelta

from PIL import Image, ImageOps, ImageTk
import lifestyle_apps as apps
import camera
import codex_images
import phone_apps
import scheduled_events
import story_calendar
import town
import phone_app_design as design
from phone_controls import PhoneButton
from phone_dialogs import messagebox


class DesignJobs:
    """Game-owned worker; only the Tk thread commits state or updates widgets."""
    def __init__(self, game):
        self.game = game
        self.events = queue.Queue()
        self.cancel_event = None
        self.status = 'Describe an outfit, then generate its portrait.'
        self.closed = False
        self.poll_id = game.after(150, self.poll)
        game.bind('<Destroy>', self.destroy, add='+')

    def start(self, title, description):
        if self.cancel_event:
            raise ValueError('An outfit design is already generating.')
        state = self.game.state_data
        request = apps.design_request(state, title, description)
        self.game.persist()
        self.cancel_event = threading.Event()
        cancel = self.cancel_event
        self.status = 'Designing your outfit… You can use other phone apps.'

        def work():
            try:
                result = codex_images.generate(request['prompt'], cancel,
                    lambda message: self.events.put(('progress', message)), references=request['references'])
                self.events.put(('complete', (state, request, result)))
            except Exception as exc:
                self.events.put(('error', str(exc)))
        threading.Thread(target=work, daemon=False).start()

    def cancel(self):
        if self.cancel_event:
            self.cancel_event.set()
            self.status = 'Cancelling outfit design…'

    def poll(self):
        try:
            while True:
                kind, payload = self.events.get_nowait()
                if kind == 'progress':
                    self.status = payload
                    continue
                cancelled = self.cancel_event and self.cancel_event.is_set()
                self.cancel_event = None
                if cancelled:
                    self.status = 'Design cancelled. Your description is saved for retry.'
                elif kind == 'error':
                    self.status = 'Design failed: '+payload
                else:
                    state, request, result = payload
                    if state is not self.game.state_data:
                        self.status = 'The game changed; this design was not added to the new save.'
                        continue
                    try:
                        apps.commit_design(state, request, result)
                        self.game.persist()
                        self.status = 'Design saved. Open My outfits to preview or wear it.'
                    except Exception as exc:
                        self.status = 'Could not save design: '+str(exc)
        except queue.Empty:
            pass
        if not self.closed:
            self.poll_id = self.game.after(150, self.poll)

    def destroy(self, event):
        if event.widget is self.game:
            self.closed = True
            self.cancel()
            self.game.after_cancel(self.poll_id)


class Screen:
    def __init__(self, phone, frame, state):
        self.phone, self.s = phone, state
        self.data = apps.ensure(state)
        self.draft = self.data['drafts'].setdefault(phone.selected, {})
        self.fields = {}
        self.root = frame
        self.accent = design.ACCENTS.get(phone.selected, '#94baff')
        if phone.selected == 'Mixtape':
            from mixtape_ui import MixtapeScreen
            phone.lifestyle_view = MixtapeScreen(phone, frame, state)
            return
        links = {'Mixtape': ('Library', 'Create'), 'Wardrobe': ('Closet', 'Style'),
                 'Out & About': ('Explore', 'Book'), 'Pocket Wallet': ('Account', 'Split bill'),
                 'Postcards': ('Sent mail', 'Compose'), 'Campus Portal': ('Campus', 'Study'),
                 'Winterfield Exchange': ('Discover', 'Shop'), 'Recipe Box': ('Kitchen', 'Recipes')}
        first, second = links[phone.selected]
        design.navigation(frame, [(first, lambda: self.jump(0)), (second, lambda: self.jump(self.form_position)),
                                  ('Home', lambda: phone.open_app('Home'))])
        self.body = phone.scroll_area(frame)
        self.form_position = 0
        headings = {
            'Mixtape': ('YOUR LIBRARY', 'Made for your moments', f'{len(self.data["playlists"])} playlists · saved songs & dedications'),
            'Wardrobe': ('PERSONAL STYLE', 'Your everyday edit', 'Outfits, inspiration and your own designs'),
            'Out & About': ('DISCOVER WINTERFIELD', 'Make a little plan', f'{len(self.data["bookings"])} saved bookings · activities with your people'),
            'Pocket Wallet': ('EVERYDAY ACCOUNT', f'${state["world"]["money"]:,}', 'Available balance · Winterfield dollars'),
            'Postcards': ('MAILBOXES / SENT', 'Postcards', f'{len(self.data["postcards"])} sent · a photo and a few words'),
            'Campus Portal': ('WINTERFIELD / CAMPUS', 'Welcome to campus', f'{len(self.data["courses"])} courses · {len(self.data["clubs"])} clubs joined'),
            'Winterfield Exchange': ('COMMUNITY MARKET', 'Find your next favourite', 'Local finds · collect in town'),
            'Recipe Box': ('YOUR KITCHEN', 'Something delicious', f'{len(self.data["recipes"])} saved recipes')}
        design.hero(self.body, phone.selected, *headings[phone.selected])
        phone.lifestyle_view = self
        methods = dict(zip(apps.NAMES, (None, self.wardrobe, self.outings, self.wallet,
                                      self.exchange, self.recipes, self.postcards, self.campus)))
        methods[phone.selected]()

    def jump(self, position):
        if isinstance(position, tk.Widget):
            position = position.winfo_y() / max(1, self.body.winfo_height())
        self.body.master.yview_moveto(position)

    def form_start(self):
        self.form_position = ttk.Frame(self.body, height=1)
        self.form_position.pack(fill='x')

    def label(self, value, heading=False):
        label = ttk.Label(self.body, text=value, wraplength=390, justify='left',
                          foreground=self.accent if heading else '#b6c5d8',
                          font=('Segoe UI', 12, 'bold') if heading else ('Segoe UI', 10))
        label.pack(anchor='w', fill='x', pady=(10 if heading else 3, 4))
        return label

    def field(self, key, default='', values=None, multiline=False):
        self.label(key)
        value = self.draft.get(key, default)
        if values is not None:
            field = ttk.Combobox(self.body, values=list(values), state='readonly')
            field.set(value if value in values else next(iter(values), ''))
        elif multiline:
            field = tk.Text(self.body, height=4, wrap='word', font=('Segoe UI', 11))
            field.insert('1.0', value)
        else:
            field = ttk.Entry(self.body)
            field.insert(0, value)
        field.pack(fill='x', pady=(0, 5))
        self.fields[key] = field
        return field

    def get(self, key):
        f = self.fields[key]
        return f.get('1.0', 'end-1c') if isinstance(f, tk.Text) else f.get()

    def capture(self):
        for key, field in self.fields.items():
            if field.winfo_exists():
                self.draft[key] = self.get(key)

    def button(self, title, callback):
        PhoneButton(self.body, text=title, command=callback).pack(fill='x', pady=4)

    def act(self, fn, *args):
        self.capture()
        self.phone.act(fn, *args)

    def people(self):
        # IDs make similarly named or renamed contacts unambiguous.
        self.people_map = {f'{camera.name(w)} · {w}': w for w in phone_apps.contacts(self.s)}
        self.field('Contact', values=self.people_map)
        if not self.people_map:
            self.label('Meet someone and exchange contact details to share or make plans.')

    def who(self):
        return self.people_map.get(self.get('Contact'), '')

    def preview(self, path):
        old = getattr(self, 'preview_label', None)
        if old is not None and old.winfo_exists():
            old.destroy()
        try:
            with Image.open(path) as source:
                photo = ImageTk.PhotoImage(ImageOps.contain(source.convert('RGBA'), (310, 330)), master=self.body)
            label = ttk.Label(self.body, image=photo)
            label.image = photo
            label.pack(pady=8)
            self.preview_label = label
        except (OSError, ValueError):
            self.label('Image unavailable. Restore its file to preview this item.')

    def wardrobe(self):
        design.card(self.body, self.s['world'].get('player_outfit', 'Automatic'), 'Your current look', self.accent, '◇')
        self.form_start()
        self.label('Current outfit: '+self.s['world'].get('player_outfit', 'Automatic'))
        self.button('My outfits', lambda: self.wardrobe_tab('closet'))
        self.button('Design outfit', lambda: self.wardrobe_tab('design'))
        if self.draft.get('tab', 'closet') == 'design':
            self.label('Design outfit', True)
            self.label('Generate a character portrait with your Codex ChatGPT login. Uses your plan allowance. Designs are saved in this wardrobe and available in Camera.')
            self.field('Design name')
            self.field('Outfit description', multiline=True)
            manager = getattr(self.phone.game, 'outfit_jobs', None)
            if manager is None:
                manager = self.phone.game.outfit_jobs = DesignJobs(self.phone.game)
            self.button('Generate outfit', self.generate)
            self.button('Cancel generation', manager.cancel)
            status = self.label(manager.status)
            timer = [None]
            def update():
                if status.winfo_exists():
                    status.configure(text=manager.status)
                    timer[0] = status.after(300, update)
            timer[0] = status.after(300, update)
            status.bind('<Destroy>', lambda e: status.after_cancel(timer[0]) if e.widget is status and timer[0] else None)
        else:
            choices = {'Automatic': None, **camera.outfits(self.s, self.s['player'])}
            self.field('Outfit', values=choices)
            self.button('Wear selected outfit', lambda: self.act(apps.wear, self.get('Outfit')))
            self.button('Preview selected outfit', lambda: self.show_outfit(choices))
            for item in reversed(self.data['designs']):
                self.label(item['label'], True)
                self.label(item['description'])
            if not self.data['designs']:
                self.label('Your custom designs will appear here.')

    def show_outfit(self, choices):
        path = choices.get(self.get('Outfit'))
        if path: self.preview(path)

    def wardrobe_tab(self, tab):
        self.capture()
        self.draft['tab'] = tab
        self.phone.refresh()

    def generate(self):
        self.capture()
        if self.phone.game.busy:
            messagebox.showinfo('Wardrobe', 'Wait for the conversation to finish.', parent=self.phone)
            return
        try:
            self.phone.game.outfit_jobs.start(self.get('Design name'), self.get('Outfit description'))
        except ValueError as exc:
            messagebox.showinfo('Wardrobe', str(exc), parent=self.phone)

    def outings(self):
        for name, (_, price, description) in apps.BOOKINGS.items():
            design.card(self.body, name, f'${price} · Book with a contact', self.accent, '↗')
        self.form_start()
        self.label('Reserve your activity', True)
        self.label('Book an activity with a contact. These use Calendar’s scheduled-event rules: your guest attends automatically. Cancel before the start for a full refund.')
        offers = {f'{name} · ${price}': name for name, (_, price, _) in apps.BOOKINGS.items()}
        self.field('Activity', values=offers)
        tomorrow = story_calendar.story_date(self.s['world']['minute'])+timedelta(days=1)
        self.field('Date (YYYY-MM-DD)', tomorrow.isoformat())
        self.field('Time (HH:MM)', '17:00')
        self.people()
        self.button('Book and add to Calendar', lambda: self.act(apps.book, offers[self.get('Activity')],
                    self.get('Date (YYYY-MM-DD)'), self.get('Time (HH:MM)'), self.who()))
        self.button('Open Calendar', lambda: self.phone.open_app('Calendar'))
        for item in reversed(self.data['bookings']):
            event = next((e for e in self.s.get('scheduled_events', []) if e['id'] == item['event']), None)
            if not event: continue
            self.label(scheduled_events.describe(event), True)
            self.label('Refunded' if item.get('refunded') else 'Cancelled' if event.get('cancelled') else 'Booked')
            if not item.get('refunded') and self.s['world']['minute'] < event['start']:
                self.button('Cancel & refund', lambda b=item: self.act(apps.cancel_booking, b['id']))

    def wallet(self):
        import interpol_ui
        interpol_ui.RecordPanel(self.body,self.phone.game,compact=True)
        design.card(self.body, 'Account activity', f'{len(self.data["receipts"])} lifestyle receipts · purchases and refunds', self.accent)
        self.form_start()
        self.label('Split a new bill', True)
        self.label('Pay only your rounded-up share from your balance. This records a new expense; it does not charge your friends or alter an earlier receipt.')
        self.field('Bill description', 'Meal together')
        self.field('Total bill ($)', '40')
        self.field('Number of diners', values=[str(i) for i in range(2, 13)])
        self.button('Pay my share', self.pay_share)
        self.label('Purchase receipts', True)
        receipts = list(self.data['receipts'])
        receipts += [dict(minute=o['minute'], title=o['app']+' · '+o['name'], amount=o['price'])
                     for o in phone_apps.ensure(self.s)['orders']]
        for item in sorted(receipts, key=lambda r:r['minute'], reverse=True):
            self.label(f'{story_calendar.story_date(item["minute"]):%b %d} · {item["title"]} · '
                       + (f'Refund ${-item["amount"]}' if item['amount'] < 0 else f'${item["amount"]}'))
        if not receipts: self.label('No app purchases yet. Other world income and expenses are reflected in your balance.')

    def pay_share(self):
        try: total, people = int(self.get('Total bill ($)')), int(self.get('Number of diners'))
        except ValueError:
            messagebox.showinfo('Pocket Wallet', 'Use whole numbers for the bill and diners.', parent=self.phone)
            return
        self.act(apps.split_bill, total, people, self.get('Bill description'))

    def exchange(self):
        self.form_start()
        self.label('Reserve a secondhand find, then collect it from its community stall. Collected items can be given as gifts. Listings renew each game day.')
        owned = {x['listing'] for x in self.data['purchases']}
        for item in apps.listings(self.s):
            self.label(f'{item["title"]} · ${item["price"]}', True)
            self.label(item['seller']+' · '+town.LOCATIONS[item['venue']])
            if item['id'] not in owned:
                self.button('Buy for collection', lambda x=item: self.act(apps.buy_listing, x['id']))
            else: self.label('Purchased')
        self.label('Your purchases', True)
        for item in reversed(self.data['purchases']):
            self.label(item['title']+' · '+('Collected' if item['collected'] else 'Waiting at '+town.LOCATIONS[item['venue']]))
            if not item['collected']:
                self.button('Collect item', lambda x=item: self.act(apps.collect, x['id']))
        self.button('Open Maps', lambda: self.phone.open_app('Maps'))

    def recipes(self):
        self.form_start()
        self.label('Save community recipes, cook in a home kitchen, or send a recipe to a friend. Ingredients are purchased when you cook.')
        self.people()
        for title, (price, method) in apps.RECIPES.items():
            self.label(title, True)
            self.label(method+f' Ingredients: ${price}.')
            if title not in self.data['recipes']:
                self.button('Save recipe', lambda t=title: self.act(apps.save_recipe, t))
            else:
                self.button('Cook · $'+str(price), lambda t=title: self.act(apps.cook, t))
                self.button('Share recipe', lambda t=title, m=method: self.act(apps.share, self.who(), 'a recipe', dict(title=t, method=m)))
        self.button('Plan a cooking night in Calendar', lambda: self.phone.game.open_calendar(story_calendar.story_date(self.s['world']['minute'])))
        for item in reversed(self.data['cooked'][-10:]): self.label('Cooked '+item['title'])

    def postcards(self):
        for item in reversed(self.data['postcards']):
            panel = design.card(self.body, 'To '+camera.name(item['recipient']), item['message'], self.accent, '✉')
            PhoneButton(panel, text='View attachment', command=lambda x=item: self.preview(camera.photo_path(x['photo']))).pack(fill='x')
        if not self.data['postcards']:
            design.card(self.body, 'No sent mail', 'Your photo messages will be collected here.', self.accent, '✉')
        self.form_start()
        self.label('New postcard', True)
        self.label('Send a Gallery photo and a personal message directly to a contact. Sent cards remain here and in Messages.')
        self.people()
        photos = camera.photos(self.s)
        choices = {f'{p["date"]} · {p["mode"]} · {p["id"][:8]}': p for p in photos}
        if choices:
            self.field('Gallery photo', values=choices)
            self.field('Postcard message', multiline=True)
            self.button('Preview photo', lambda: self.preview(camera.photo_path(choices[self.get('Gallery photo')])))
            self.button('Send postcard', lambda: self.act(apps.send_postcard, choices[self.get('Gallery photo')]['id'], self.who(), self.get('Postcard message')))
        else:
            self.label('Take a photo in Camera to make your first postcard.')
            self.button('Open Camera', lambda: self.phone.open_app('Camera'))

    def campus(self):
        design.card(self.body, 'Learning dashboard', f'{len(apps.COURSES)} community courses · weekly assignments', self.accent, '▤')
        for course in self.data['courses']:
            design.card(self.body, course, 'Enrolled · '+str(len(self.data['courses'][course]['submitted']))+' assignments submitted', self.accent, '▤')
        self.form_start()
        self.label('Courses & assignments', True)
        self.label('Community courses and clubs · open to students and local residents. Complete a weekly assignment, practise on location, or arrange a study session.')
        self.field('Course', values=apps.COURSES)
        self.button('Enroll in selected course', lambda: self.act(apps.enroll, self.get('Course')))
        for course, (_, assignment) in apps.COURSES.items():
            self.label(course, True)
            self.label('This week: '+assignment)
            if course in self.data['courses']:
                self.label(f'Enrolled · {len(self.data["courses"][course]["submitted"])} assignments submitted')
        self.field('Assignment response', multiline=True)
        self.button('Submit to selected course', lambda: self.act(apps.submit_assignment, self.get('Course'), self.get('Assignment response')))
        self.label('Club noticeboard', True)
        for club, (venue, assignment) in apps.CLUBS.items():
            self.label(club, True)
            self.label(town.LOCATIONS[venue]+' · '+assignment)
            if club not in self.data['clubs']:
                self.button('Join club', lambda c=club: self.act(apps.join_club, c))
            else:
                done = self.data['clubs'][club]['completed']
                self.label(f'{len(done)} practices completed'+(' · Today complete' if self.s['world']['minute']//1440 in done else ''))
                self.button('Complete today’s practice', lambda c=club: self.act(apps.complete_assignment, c))
        self.button('Plan a study session in Calendar', lambda: self.phone.game.open_calendar(story_calendar.story_date(self.s['world']['minute'])))
        self.button('Open Maps', lambda: self.phone.open_app('Maps'))
