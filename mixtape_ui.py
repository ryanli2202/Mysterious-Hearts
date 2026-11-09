"""Dark, browse-first Mixtape pages and a persistent playlist workspace."""
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk
import camera
import lifestyle_apps as apps
import mixtape_catalog as music
import mixtape_art
import phone_apps
import phone_app_design as design
import phone_theme
from phone_controls import PhoneButton

GREEN = '#66d998'
TONES = ('#244c42', '#393654', '#483449', '#24485a', '#4a3e30')


class MixtapeScreen:
    def __init__(self, phone, frame, state):
        self.phone, self.root, self.s = phone, frame, state
        self.data = apps.ensure(state)
        self.draft = self.data['drafts'].setdefault('Mixtape', {})
        self.fields = {}
        if 'workspace' not in self.draft:
            self.draft['workspace'] = dict(title=self.draft.get('Playlist title', ''),
                memory=self.draft.get('Memory or dedication', ''), playlist_id=None,
                entries=[dict(id=i, label=music.track_label(i)) for i in self.draft.get('song_ids', []) if i in music.SONGS])
        self.page = self.draft.get('page', 'home')
        nav = tk.Frame(frame, bg=design.BG)
        nav.pack(side='bottom', fill='x')
        self.nav_buttons = {}
        active = self.page if self.page in ('home', 'search', 'library') else ('search' if self.page == 'artist' else 'library')
        for key, title in [('home', 'Home'), ('search', 'Search'), ('library', 'Your library')]:
            cell = tk.Frame(nav, bg=design.BG)
            cell.pack(side='left', fill='x', expand=True)
            tk.Frame(cell, height=3, bg=GREEN if key == active else design.BG).pack(fill='x')
            self.nav_buttons[key] = self.button(cell, title, lambda p=key: self.go(p))
        self.body = phone.scroll_area(frame)
        self.notice = self.text(self.body, self.draft.pop('notice', ''), color=GREEN)
        self.status = self.notice
        getattr(self, 'show_'+self.page, self.show_home)()
        phone_theme.apply_tree(frame)

    def text(self, parent, value, size=11, color=design.TEXT, bold=False):
        # Shared labels require a classic parent with a background option.
        if isinstance(parent, ttk.Frame):
            panel = tk.Frame(parent, bg=design.BG)
            panel.pack(fill='x')
            parent = panel
        return design.text(parent, value, size, color, bold)

    def button(self, parent, title, callback, state='normal'):
        button = PhoneButton(parent, text=title, command=callback, state=state)
        button.pack(fill='x', pady=3)
        return button

    def heading(self, title, subtitle=''):
        self.text(self.body, title, 25, bold=True)
        if subtitle: self.text(self.body, subtitle, 10, design.MUTED)

    def capture(self):
        for key, widget in self.fields.items():
            if widget.winfo_exists():
                value = widget.get('1.0', 'end-1c') if isinstance(widget, tk.Text) else widget.get()
                if key in ('title', 'memory'): self.draft['workspace'][key] = value
                else: self.draft[key] = value

    def go(self, page, **values):
        self.capture()
        self.draft.update(values, page=page)
        self.phone.refresh()

    def cover(self, parent, name, index=0, artist=False):
        ident = next((a['id'] for a in music.ARTISTS if a['name']==name), None)
        path = mixtape_art.artist_path(ident, 'portrait' if artist else 'cover')
        if path and self.artwork(parent, path, 160 if artist else 180):
            return
        canvas = tk.Canvas(parent, height=100, bg=TONES[index % len(TONES)], highlightthickness=0)
        canvas.pack(fill='x', pady=(0, 7))
        def draw(event):
            canvas.delete('all'); w=event.width
            if artist:
                canvas.create_oval(w/2-37, 13, w/2+37, 87, fill='#202a38', outline=GREEN, width=2)
                initials = ''.join(word[0] for word in name.split()[:2])
                canvas.create_text(w/2, 50, text=initials, fill=GREEN, font=('Segoe UI', 24, 'bold'))
            else:
                for i in range(9):
                    x=w/2-64+i*16; h=15+(i*23+index*11)%54
                    canvas.create_line(x,50-h/2,x,50+h/2,fill=GREEN,width=6,capstyle='round')
        canvas.bind('<Configure>', draw)

    def artwork(self, parent, path, size=64, before=None):
        if path is None: return False
        try:
            photo = ImageTk.PhotoImage(mixtape_art.thumbnail(str(path), size), master=parent)
        except (OSError, ValueError):
            return False
        label = tk.Label(parent, image=photo, bg=parent.cget('background'), bd=0)
        label.image = photo
        label.artwork_path = str(path)
        options = dict(anchor='w', pady=(0, 7))
        if before is not None: options['before'] = before
        label.pack(**options)
        return True

    def artist_tile(self, parent, artist, index=0):
        panel = tk.Frame(parent, bg=design.PANEL, padx=10, pady=10)
        self.cover(panel, artist['name'], index, True)
        self.text(panel, artist['name'], 13, bold=True)
        self.text(panel, artist['genre'], 9, design.MUTED)
        self.button(panel, 'View artist', lambda: self.go('artist', artist_id=artist['id']))
        return panel

    def artist_grid(self, parent, artists):
        grid = tk.Frame(parent, bg=design.BG)
        grid.pack(fill='x', pady=6)
        for column in range(2): grid.columnconfigure(column, weight=1, uniform='artists')
        for i, artist in enumerate(artists):
            self.artist_tile(grid, artist, music.ARTISTS.index(artist)).grid(row=i//2, column=i%2, sticky='nsew', padx=3, pady=3)

    def playlist_row(self, parent, item):
        panel = design.card(parent, item['title'], f'{len(item["tracks"])} songs · Playlist', GREEN)
        self.button(panel, 'Open playlist', lambda: self.go('playlist', playlist_id=item['id']))

    def show_home(self):
        self.heading('Find your next favourite', 'MIXTAPE  /  Music for your moments')
        hero = tk.Frame(self.body, bg='#19362c', padx=14, pady=12); hero.pack(fill='x', pady=10)
        self.cover(hero, 'Voss')
        self.text(hero, 'A little late-night feeling', 20, bold=True)
        self.text(hero, 'Meet Voss. Intimate vocals, quiet heartbreak and 808s.', 11, design.MUTED)
        self.button(hero, 'Explore Voss', lambda: self.go('artist', artist_id='voss'))
        self.button(self.body, 'Make a playlist', lambda: self.go('editor'))
        if self.data['playlists']:
            self.text(self.body, 'Your recent playlists', 17, bold=True)
            for item in reversed(self.data['playlists'][-3:]): self.playlist_row(self.body, item)
        self.text(self.body, 'Discover artists', 17, bold=True)
        self.artist_grid(self.body, [music.ARTISTS[i] for i in (4, 12, 20, 28)])
        self.text(self.body, '44 artists · 1,056 songs · 11 genres', 10, design.MUTED)
        self.text(self.body, 'Collect and share songs. Audio playback is not available.', 10, design.MUTED)

    def show_search(self):
        self.heading('Search', 'Artists, songs, and something that fits your mood.')
        entry = ttk.Entry(self.body); entry.insert(0, self.draft.get('query', ''))
        entry.pack(fill='x', pady=8); self.fields['query'] = entry
        entry.bind('<KeyRelease>', lambda event: self.search_results())
        self.text(self.body, 'Browse by genre', 12, bold=True)
        combo = ttk.Combobox(self.body, values=['All genres', *music.GENRES], state='readonly')
        combo.set(self.draft.get('genre', 'All genres')); combo.pack(fill='x', pady=5)
        self.fields['genre'] = combo
        combo.bind('<<ComboboxSelected>>', lambda event: self.search_results())
        self.results = tk.Frame(self.body, bg=design.BG); self.results.pack(fill='x')
        self.search_results()

    def search_results(self):
        self.capture()
        for child in self.results.winfo_children(): child.destroy()
        query = self.draft.get('query', '').casefold().strip()
        genre = self.draft.get('genre', 'All genres')
        pool = [a for a in music.ARTISTS if genre == 'All genres' or a['genre'] == genre]
        artists = [a for a in pool if not query or query in a['name'].casefold()]
        songs = [(a, s) for a in pool for s in a['songs'] if query and query in s['title'].casefold()]
        self.text(self.results, f'{len(artists)} artist' + ('' if len(artists)==1 else 's') + (f' · {len(songs)} songs' if query else ''), 10, GREEN)
        if not artists and not songs:
            self.text(self.results, 'No matches. Try another name or choose All genres.', 12)
        self.artist_grid(self.results, artists)
        if songs:
            self.text(self.results, 'Songs' + (' · first 40 matches' if len(songs)>40 else ''), 17, bold=True)
            for artist, song in songs[:40]: self.song_row(self.results, song, artist)
        phone_theme.apply_tree(self.results)

    def show_artist(self):
        artist = next((a for a in music.ARTISTS if a['id']==self.draft.get('artist_id')), music.ARTISTS[0])
        self.button(self.body, '‹ Back to search', lambda: self.go('search'))
        panel = tk.Frame(self.body, bg=TONES[music.ARTISTS.index(artist)%5], padx=14, pady=12); panel.pack(fill='x')
        self.cover(panel, artist['name'], music.ARTISTS.index(artist), True)
        self.text(panel, 'ARTIST  /  '+artist['genre'], 10, GREEN)
        self.text(panel, artist['name'], 28, bold=True)
        self.text(panel, artist['description'], 11)
        self.text(panel, '24 songs', 10, design.MUTED)
        self.button(self.body, 'View playlist draft', lambda: self.go('editor'))
        self.status = self.text(self.body, 'Add songs to your playlist draft below.', 10, GREEN)
        self.text(self.body, 'Discography', 18, bold=True)
        for song in artist['songs']: self.song_row(self.body, song, artist)

    def song_row(self, parent, song, artist):
        panel = design.card(parent, song['title'], artist['name'], GREEN)
        self.artwork(panel, mixtape_art.song_path(song['id']), before=panel.winfo_children()[0])
        self.text(panel, song['description'], 10, design.MUTED)
        added = any(e.get('id')==song['id'] for e in self.draft['workspace']['entries'])
        button = self.button(panel, 'Added ✓' if added else '+ Add to playlist', lambda: None, 'disabled' if added else 'normal')
        button.configure(command=lambda: self.add_song(song['id'], button))

    def add_song(self, ident, button=None):
        entries = self.draft['workspace']['entries']
        if any(e.get('id')==ident for e in entries):
            self.status.configure(text='This song is already in your draft.'); return
        if len(entries)>=30:
            self.status.configure(text='Your draft has 30 songs. Remove one in Your library → Playlist draft.'); return
        entries.append(dict(id=ident, label=music.track_label(ident)))
        self.status.configure(text=f'Added · {len(entries)} / 30 songs in your playlist draft')
        if button: button.configure(text='Added ✓', state='disabled')

    def show_library(self):
        self.heading('Your library', f'{len(self.data["playlists"])} playlists · Made by you')
        self.button(self.body, 'Create / continue playlist draft', lambda: self.go('editor'))
        if not self.data['playlists']:
            self.text(self.body, 'Your collection starts with a song.', 18, bold=True)
            self.text(self.body, 'Search for an artist, add a few favourites, then save your first playlist.', 11, design.MUTED)
            self.button(self.body, 'Find artists', lambda: self.go('search'))
        for item in reversed(self.data['playlists']): self.playlist_row(self.body, item)
        shares=[s for s in self.data['shares'] if s['kind']=='a Mixtape playlist']
        if shares:
            self.text(self.body, 'Sent to your people', 17, bold=True)
            for share in reversed(shares[-8:]):
                self.text(self.body, share['content']['title']+' → '+camera.name(share['recipient']), 11, design.MUTED)

    def selected_playlist(self):
        return next((p for p in self.data['playlists'] if p['id']==self.draft.get('playlist_id')), None)

    def show_playlist(self):
        item = self.selected_playlist()
        if item is None:
            self.heading('Playlist unavailable'); self.button(self.body, 'Your library', lambda: self.go('library')); return
        self.button(self.body, '‹ Your library', lambda: self.go('library'))
        panel=tk.Frame(self.body,bg='#19362c',padx=14,pady=12); panel.pack(fill='x')
        self.cover(panel, item['title'], sum(map(ord,item['title'])))
        self.text(panel, 'YOUR PLAYLIST', 10, GREEN)
        self.text(panel, item['title'], 26, bold=True)
        self.text(panel, f'{len(item["tracks"])} songs', 10, design.MUTED)
        if item['memory']: self.text(panel, item['memory'])
        self.button(self.body, 'Edit playlist', self.begin_edit)
        self.button(self.body, 'Send playlist', lambda: self.go('send'))
        ids = item.get('song_ids', [])
        for i, label in enumerate(item['tracks'],1):
            row = tk.Frame(self.body, bg=design.PANEL, padx=10, pady=8)
            row.pack(fill='x', pady=3)
            self.artwork(row, mixtape_art.song_path(ids[i-1] if i<=len(ids) else None))
            self.text(row, f'{i:02}   {label}', 12)

    def begin_edit(self):
        item=self.selected_playlist()
        workspace=self.draft['workspace']
        if workspace['entries'] or workspace['title'] or workspace['memory']:
            if workspace.get('playlist_id') == item['id']:
                self.go('editor')
            else:
                self.status.configure(text='Save your current draft before editing another playlist.')
            return
        ids=item.get('song_ids', [])
        self.draft['workspace']=dict(title=item['title'],memory=item['memory'],playlist_id=item['id'],
            entries=[dict(label=t,id=ids[i] if i<len(ids) else None) for i,t in enumerate(item['tracks'])])
        self.go('editor')

    def show_editor(self):
        workspace=self.draft['workspace']
        self.heading('Edit playlist' if workspace.get('playlist_id') else 'Make it yours', 'A title, a few songs, a little meaning.')
        for key, title in [('title','Playlist name'),('memory','Memory or dedication')]:
            self.text(self.body,title,10,design.MUTED)
            widget=ttk.Entry(self.body) if key=='title' else tk.Text(self.body,height=3,wrap='word',font=('Segoe UI',11))
            widget.insert(0 if key=='title' else '1.0',workspace[key]); widget.pack(fill='x',pady=5)
            self.fields[key]=widget
        self.button(self.body,'+ Find songs',lambda:self.go('search'))
        self.button(self.body,'Save playlist',self.save)
        self.status=self.text(self.body,f'{len(workspace["entries"])} / 30 songs',11,GREEN)
        if not workspace['entries']: self.text(self.body,'Your playlist is waiting. Find an artist to add your first song.',12)
        for i, entry in enumerate(workspace['entries']):
            panel=design.card(self.body,f'{i+1}. {entry["label"]}',accent=GREEN)
            self.artwork(panel, mixtape_art.song_path(entry.get('id')), before=panel.winfo_children()[0])
            self.button(panel,'Remove',lambda index=i:self.remove_song(index))
        old=self.draft.get('Songs · one title and artist per line')
        if old: self.text(self.body,'Previous typed draft (reference):\n'+old,10,design.MUTED)

    def remove_song(self,index):
        self.capture(); self.draft['workspace']['entries'].pop(index); self.go('editor')

    def save(self):
        self.capture()
        def commit(state):
            w=self.draft['workspace']
            item=apps.edit_mixtape_playlist(state,w['title'],w['entries'],w['memory'],w.get('playlist_id'))
            # Refresh captures the old widgets once more; detach them before resetting the draft.
            self.fields={}
            self.draft.update(page='playlist',playlist_id=item['id'],notice='Playlist saved.',
                workspace=dict(title='',memory='',entries=[],playlist_id=None))
        self.phone.act(commit)

    def show_send(self):
        item=self.selected_playlist()
        if item is None: self.show_playlist(); return
        self.heading('Send a little feeling', item['title'])
        self.button(self.body,'‹ Back to playlist',lambda:self.go('playlist'))
        self.text(self.body,'Send this playlist and its dedication privately to a contact.',11,design.MUTED)
        self.people_map={f'{camera.name(w)} · {w}':w for w in phone_apps.contacts(self.s)}
        if not self.people_map:
            self.text(self.body,'No contacts yet. Meet someone and exchange contact details first.',12); return
        combo=ttk.Combobox(self.body,values=list(self.people_map),state='readonly')
        previous=self.draft.get('recipient',''); combo.set(previous if previous in self.people_map else next(iter(self.people_map)))
        combo.pack(fill='x',pady=10); self.fields['recipient']=combo
        self.send_button=self.button(self.body,'Send playlist',self.send)

    def send(self):
        self.capture(); item=self.selected_playlist(); who=self.people_map.get(self.draft.get('recipient'))
        def commit(state):
            apps.share_playlist(state,item['id'],who)
            self.draft.update(page='playlist',notice='Sent to '+camera.name(who)+'.')
        self.phone.act(commit)
