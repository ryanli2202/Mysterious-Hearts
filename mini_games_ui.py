"""Phone-sized arcade. Timers and key bindings belong to the mounted view."""
import tkinter as tk
from tkinter import ttk
from copy import deepcopy
from time import monotonic
from math import sin, pi
import mini_games as games
from arcade_extra_ui import ExtraArcade, EXTRA_ENGINES, EXTRA_HELP

ENGINES = {'Connect 4': games.Connect4, 'Tetris': games.Tetris,
           'Blackjack': games.Blackjack, 'Snake': games.Snake,
           'Pong': games.Pong, '2048': games.Tiles2048, **EXTRA_ENGINES}
REALTIME = ('Tetris', 'Snake', 'Pong', 'Breakout')
HELP = {
    'Connect 4': 'Connect four discs in a row. You are gold; the computer is coral.',
    'Tetris': 'Arrows: move / rotate / soft drop · Space: hard drop · P: pause',
    'Blackjack': 'Get closer to 21 than the dealer. Dealer stands on all 17s. No wagers.',
    'Snake': 'Arrow keys or WASD to steer. Eat coral fruit; avoid walls and yourself.',
    'Pong': 'Up / Down or W / S to move. You are on the left. First to 7 wins.',
    '2048': 'Arrow keys or WASD slide tiles. Merge matching numbers to reach 2048.',
    **EXTRA_HELP,
}
BG, INK, GOLD, CORAL = '#141c2e', '#c4d1e3', '#f0c875', '#f08a8a'
BLOCKS = ('#141c2e', '#6bd6df', '#f0c875', '#b494ef', '#8fd49a', '#f08a8a', '#739fe9', '#efaf76')


def tile_paths(board, direction):
    """Map every original tile to its destination, including both merge partners."""
    paths, merges = [], set()
    for line in range(4):
        cells = [(line, i) if direction in ('up', 'down') else (i, line) for i in range(4)]
        if direction in ('right', 'down'):
            cells.reverse()
        occupied = [(x, y, board[y][x]) for x, y in cells if board[y][x]]
        source = target = 0
        while source < len(occupied):
            x, y, value = occupied[source]
            destination = cells[target]
            paths.append(((x, y), destination, value))
            source += 1
            if source < len(occupied) and occupied[source][2] == value:
                x, y, _ = occupied[source]
                paths.append(((x, y), destination, value))
                merges.add(destination)
                source += 1
            target += 1
    return paths, merges


class Arcade(ExtraArcade, ttk.Frame):
    def __init__(self, parent, sessions, sounds=None):
        # Native Windows ttk themes can ignore background colours. Standalone
        # arcade windows need the same dark theme as the full application.
        if ttk.Style(parent).theme_use() != 'clam':
            import winterfield_ui
            winterfield_ui.install(parent.winfo_toplevel())
        super().__init__(parent)
        self.install_styles()
        self.pack(fill='both', expand=True)
        self.sessions = sessions
        self.sounds = sounds
        self.muted = False
        self.jobs = set()
        self.name = None
        self.timer = None
        self.animation_timer = None
        self.animation = None
        self.paused = True
        self.bind('<Destroy>', self.cleanup, add='+')
        self.menu()

    def install_styles(self):
        style = ttk.Style(self)
        panel, surface, edge = '#1c2433', '#293447', '#3b4a60'
        for kind in ('TFrame', 'TLabel', 'TButton', 'TCombobox', 'Vertical.TScrollbar'):
            name = 'Arcade.' + kind
            style.configure(name, background=panel if kind in ('TFrame', 'TLabel') else surface,
                            foreground=INK, fieldbackground=surface, troughcolor=BG,
                            arrowcolor=INK, bordercolor=edge, lightcolor=surface, darkcolor=surface)
            style.map(name, background=[('disabled', panel), ('pressed', edge), ('active', '#35485c')],
                      foreground=[('disabled', '#8191a8'), ('!disabled', INK)],
                      fieldbackground=[('readonly', surface), ('disabled', panel)],
                      selectbackground=[('!disabled', edge)], selectforeground=[('!disabled', INK)])

    def style_widgets(self):
        def visit(widget):
            for kind in (ttk.Frame, ttk.Label, ttk.Button, ttk.Combobox, ttk.Scrollbar):
                if isinstance(widget, kind):
                    suffix = 'Vertical.TScrollbar' if kind is ttk.Scrollbar else widget.winfo_class()
                    widget.configure(style='Arcade.' + suffix)
                    break
            for child in widget.winfo_children(): visit(child)
        visit(self)

    def cancel_timer(self):
        if self.timer is not None:
            self.after_cancel(self.timer)
            self.timer = None

    def cleanup(self, event):
        if event.widget is self:
            self.cancel_timer()
            self.cancel_animation()
            self.cancel_jobs()
            self.stop_effects()

    def effect(self, effect):
        if self.sounds and not self.muted:
            self.sounds.play('arcade_' + effect)

    def stop_effects(self):
        if self.sounds:
            self.sounds.stop_arcade()

    def toggle_sound(self):
        self.muted = not self.muted
        if self.muted: self.stop_effects()
        self.sound_button.config(text='SFX: Off' if self.muted else 'SFX: On')

    def move_sound(self, before, action=None):
        """Play event cues, never a sound for every animation frame."""
        m = self.model
        if before == m.__dict__: return
        if self.name in ('Connect 4', 'Blackjack') and m.result and not before['result']:
            self.effect('win' if 'You win' in m.result else 'lose' if 'wins' in m.result or 'Blackjack' in m.result else 'score')
        elif getattr(m, 'over', False) and not before.get('over', False):
            won = getattr(m, 'won', False) or (self.name == 'Pong' and m.scores[0] == 7) or (self.name == 'Snake' and m.food is None)
            self.effect('win' if won else 'lose')
        elif self.name == 'Connect 4': self.effect('drop')
        elif self.name == 'Blackjack': self.effect('card')
        elif self.name == '2048': self.effect('merge' if m.score > before['score'] else 'slide')
        elif self.name == 'Snake' and m.score > before['score']: self.effect('eat')
        elif self.name == 'Tetris':
            if m.lines > before['lines']: self.effect('clear')
            elif m.board != before['board']: self.effect('drop')
            elif action == 'up' and m.piece != before['piece']: self.effect('rotate')
            elif action: self.effect('tap')
        elif self.name == 'Pong':
            if m.scores != before['scores']: self.effect('score')
            elif m.vx * before['vx'] < 0 or m.vy * before['vy'] < 0: self.effect('bounce')
        elif self.name == 'Breakout' and m.event: self.effect(m.event)

    def cancel_animation(self):
        if self.animation_timer is not None:
            self.after_cancel(self.animation_timer)
        self.animation_timer = None
        self.animation = None

    def animate(self, before, duration=0.14, direction=None, force=False):
        self.cancel_animation()
        import phone_personalization
        if (before == self.model.__dict__ and not force) or phone_personalization.preferences()['reduced_motion']:
            self.draw()
            return
        self.animation = dict(before=before, start=monotonic(), duration=duration,
                              direction=direction)
        self.animation_frame()

    def animation_frame(self):
        self.animation_timer = None
        if not self.animation:
            return
        if monotonic() - self.animation['start'] >= self.animation['duration']:
            self.animation = None
        self.draw()
        if self.animation:
            self.animation_timer = self.after(16, self.animation_frame)

    def clear(self):
        self.cancel_timer()
        self.cancel_animation()
        self.cancel_jobs()
        self.stop_effects()
        for child in self.winfo_children():
            child.destroy()

    def menu(self):
        self.clear()
        self.name = None
        import phone_app_design as design
        design.hero(self, 'Mini Games', 'WINTERFIELD ARCADE', 'Ready, player?', f'{len(ENGINES)} games · Pick up and play')
        ttk.Label(self, text='Games stay in memory. Leaving pauses play.', foreground='#9da9be').pack(side='bottom', pady=6)
        list_frame = ttk.Frame(self)
        list_frame.pack(fill='both', expand=True)
        listing = tk.Canvas(list_frame, bg=BG, highlightthickness=0)
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=listing.yview)
        listing.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
        listing.pack(side='left', fill='both', expand=True)
        rows = ttk.Frame(listing)
        window = listing.create_window(0, 0, window=rows, anchor='nw')
        rows.bind('<Configure>', lambda e: listing.configure(scrollregion=listing.bbox('all')))
        listing.bind('<Configure>', lambda e: listing.itemconfigure(window, width=e.width))
        def wheel(event):
            listing.yview_scroll(-int(event.delta / 120) or (-1 if event.delta > 0 else 1), 'units')
            return 'break'
        listing.bind('<MouseWheel>', wheel)
        rows.bind('<MouseWheel>', wheel)
        for index, name in enumerate(ENGINES):
            panel = design.card(rows, name, HELP[name], '#bb9afa', ['✦', '▦', '♠', '↗'][index % 4])
            button = ttk.Button(panel, text='Resume game' if name in self.sessions else 'Play game',
                                padding=10, command=lambda n=name: self.open(n))
            button.pack(fill='x', pady=3)
            for widget in (panel, button, *panel.winfo_children()):
                widget.bind('<MouseWheel>', wheel)
            button.bind('<FocusIn>', lambda e, panel=panel: listing.yview_moveto(panel.winfo_y() / max(1, rows.winfo_height())))
        self.style_widgets()

    def open(self, name, restart=False):
        self.clear()
        self.name = name
        if restart or name not in self.sessions:
            self.sessions[name] = ENGINES[name]()
        self.model = self.sessions[name]
        self.paused = True
        bar = ttk.Frame(self)
        bar.pack(fill='x')
        ttk.Button(bar, text='‹ Games', command=self.menu).pack(side='left')
        ttk.Button(bar, text='New game', command=lambda: self.open(name, True)).pack(side='right')
        self.sound_button = ttk.Button(bar, text='SFX: Off' if self.muted else 'SFX: On', command=self.toggle_sound)
        self.sound_button.pack(side='right', padx=4)
        ttk.Label(self, text=name, font=('Segoe UI', 21, 'bold')).pack(anchor='w', pady=(10, 2))
        ttk.Label(self, text=HELP[name], wraplength=430).pack(anchor='w')
        self.status = ttk.Label(self, font=('Segoe UI', 11, 'bold'), wraplength=440)
        self.status.pack(anchor='w', pady=8)
        self.canvas = tk.Canvas(self, width=400, height=400, bg=BG, highlightthickness=2,
                                highlightbackground='#33415c', highlightcolor=GOLD, takefocus=True)
        self.canvas.bind('<Configure>', lambda e: self.draw())
        self.canvas.bind('<Button-1>', self.click)
        self.canvas.bind('<KeyPress>', self.key)
        self.canvas.bind('<FocusOut>', self.focus_out)
        controls = ttk.Frame(self)
        controls.pack(side='bottom', fill='x', pady=(8, 0))
        self.canvas.pack(fill='both', expand=True)
        if name in REALTIME:
            self.pause_button = ttk.Button(controls, text='Play', command=self.toggle)
            self.pause_button.pack(side='left', padx=2)
        actions = {
            'Connect 4': [(str(i + 1), str(i + 1)) for i in range(7)],
            'Blackjack': [('Hit', 'hit'), ('Stand', 'stand')],
            'Tetris': [('←', 'left'), ('↻', 'up'), ('→', 'right'), ('↓', 'down'), ('Drop', 'space')],
            'Snake': [('←', 'left'), ('↑', 'up'), ('↓', 'down'), ('→', 'right')],
            'Pong': [('↑', 'up'), ('↓', 'down')],
            '2048': [('←', 'left'), ('↑', 'up'), ('↓', 'down'), ('→', 'right')],
            'Breakout': [('←', 'left'), ('→', 'right'), ('Launch', 'space')],
        }
        for label, action in actions.get(name, []):
            ttk.Button(controls, text=label, width=5 if name == 'Connect 4' else 6,
                       command=lambda a=action: self.action(a)).pack(side='left', padx=1)
        self.setup_extra(controls)
        self.style_widgets()
        self.draw()
        self.canvas.focus_set()

    def focus_out(self, event):
        # Moving to a game button is safe; switching away from the phone pauses play.
        self.later(0, self.check_focus)

    def check_focus(self):
        if self.winfo_exists() and self.name in REALTIME:
            focus = self.focus_get()
            if focus is None or not str(focus).startswith(str(self) + '.'):
                self.paused = True
                self.cancel_timer()
                self.cancel_animation()
                self.stop_effects()
                self.pause_button.config(text='Resume')
                self.draw()

    def toggle(self):
        if self.model.over:
            return
        self.paused = not self.paused
        self.pause_button.config(text='Resume' if self.paused else 'Pause')
        self.canvas.focus_set()
        self.cancel_timer()
        self.cancel_animation()
        if not self.paused:
            self.schedule()
        else:
            self.stop_effects()
        self.draw()

    def schedule(self):
        delay = {'Tetris': max(100, 600 - getattr(self.model, 'lines', 0) * 15),
                 'Snake': max(65, 155 - getattr(self.model, 'score', 0) // 5), 'Pong': 20, 'Breakout': 20}[self.name]
        self.timer = self.after(delay, self.tick)

    def tick(self):
        self.timer = None
        if self.paused:
            return
        before = deepcopy(self.model.__dict__)
        self.model.step()
        self.move_sound(before)
        self.animate(before, 0.06 if self.name == 'Snake' else 0.018 if self.name == 'Pong' else 0.12)
        if not self.model.over:
            self.schedule()

    def key(self, event):
        key = event.keysym.lower()
        key = {'w': 'up', 'a': 'left', 's': 'down', 'd': 'right'}.get(key, key)
        if key in ('up', 'down', 'left', 'right', 'space', 'p', '1', '2', '3', '4', '5', '6', '7'):
            self.action(key)
            return 'break'

    def click(self, event):
        self.canvas.focus_set()
        x, y = self.logical(event.x, event.y)
        if self.extra_click(x, y): return
        if self.name == 'Connect 4':
            x, y = self.logical(event.x, event.y)
            if 25 <= x < 375 and 50 <= y < 350:
                self.action(str(int((x - 25) // 50) + 1))

    def action(self, action):
        self.canvas.focus_set()
        if self.animation and self.name in ('2048', 'Connect 4', 'Blackjack'):
            return
        model = self.model
        before = deepcopy(model.__dict__)
        if self.name == 'Simon Says' and action in ('1', '2', '3', '4'):
            self.simon_press(int(action) - 1)
            return
        if action == 'p' and self.name in REALTIME:
            self.toggle()
            return
        if self.name in REALTIME and (self.paused or model.over):
            return
        directions = {'left': (-1, 0), 'right': (1, 0), 'up': (0, -1), 'down': (0, 1)}
        if self.name == 'Connect 4' and action in '1234567' and len(action) == 1:
            if model.drop(int(action) - 1, 1):
                model.computer()
        elif self.name == '2048' and action in directions:
            model.move(action)
        elif self.name == 'Snake' and action in directions:
            model.turn(directions[action])
            return  # Steering must not interrupt the current movement tween.
        elif self.name == 'Pong' and action in ('up', 'down'):
            model.move(-24 if action == 'up' else 24)
        elif self.name == 'Tetris':
            if action == 'up': model.rotate()
            elif action == 'space': model.drop()
            elif action == 'down': model.step()
            elif action in ('left', 'right'): model.move(-1 if action == 'left' else 1, 0)
        elif self.name == 'Blackjack':
            if action == 'hit': model.hit()
            elif action == 'stand': model.stand()
        elif self.name == 'Breakout':
            if action in ('left', 'right'): model.move(-25 if action == 'left' else 25)
            elif action == 'space': model.launch()
        self.move_sound(before, action)
        self.animate(before, {'2048': 0.26, 'Connect 4': 0.65, 'Blackjack': 0.38}.get(self.name, 0.10), action)

    def logical(self, x, y):
        return ((x - self.ox) / self.scale, (y - self.oy) / self.scale)

    def rect(self, x, y, w, h, color):
        self.canvas.create_rectangle(self.ox + x * self.scale, self.oy + y * self.scale,
                                     self.ox + (x + w) * self.scale, self.oy + (y + h) * self.scale,
                                     fill=color, outline='')

    def text(self, x, y, text, size=16, color=INK):
        self.canvas.create_text(self.ox + x * self.scale, self.oy + y * self.scale,
                                text=text, fill=color, font=('Segoe UI', max(8, int(size * self.scale)), 'bold'))

    def oval(self, x, y, w, h, color):
        self.canvas.create_oval(self.ox + x * self.scale, self.oy + y * self.scale,
                                self.ox + (x + w) * self.scale, self.oy + (y + h) * self.scale,
                                fill=color, outline='')

    def draw(self):
        c, m = self.canvas, self.model
        animation = self.animation
        before = animation['before'] if animation else m.__dict__
        progress = min(1, (monotonic() - animation['start']) / animation['duration']) if animation else 1
        ease = 1 - (1 - progress) ** 3
        c.delete('all')
        w, h = max(1, c.winfo_width()), max(1, c.winfo_height())
        self.scale = min(w, h) / 400
        self.ox, self.oy = (w - 400 * self.scale) / 2, (h - 400 * self.scale) / 2
        status = ''
        if self.name == 'Connect 4':
            status = m.result or 'Your turn · Click a column or press 1–7'
            drops = sorted(((x, y, m.board[y][x]) for y in range(6) for x in range(7)
                            if m.board[y][x] != before['board'][y][x]), key=lambda item: item[2])
            if animation: status = 'Discs dropping…'
            self.rect(20, 45, 360, 310, '#314d85')
            for x in range(7):
                self.text(50 + x * 50, 25, str(x + 1), 12)
                for y in range(6):
                    value = before['board'][y][x] if animation else m.board[y][x]
                    self.oval(29 + x * 50, 54 + y * 50, 42, 42, (BG, GOLD, CORAL)[value])
            for i, (x, y, value) in enumerate(drops):
                t = max(0, min(1, progress * len(drops) - i))
                if t > 0:
                    self.oval(29 + x * 50, -42 + (96 + y * 50) * t * t, 42, 42, (BG, GOLD, CORAL)[value])
        elif self.name == '2048':
            status = f'Score: {m.score}' + (' · No moves left' if m.over else ' · 2048 reached! Keep going.' if any(max(r) >= 2048 for r in m.board) else '')
            for y in range(4):
                for x in range(4): self.tile(x, y, 0)
            paths, merges = tile_paths(before['board'], animation['direction']) if animation else ([], set())
            if animation and progress < .65:
                t = 1 - (1 - progress / .65) ** 3
                for (x, y), (nx, ny), value in paths:
                    self.tile(x + (nx - x) * t, y + (ny - y) * t, value)
            else:
                destinations = {destination for _, destination, _ in paths}
                t = max(0, (progress - .65) / .35)
                for y, row in enumerate(m.board):
                    for x, value in enumerate(row):
                        if not value: continue
                        size = 1
                        if animation:
                            if (x, y) in merges: size += .12 * sin(pi * t)
                            elif (x, y) not in destinations: size = .25 + .75 * t
                        self.tile(x, y, value, size)
        elif self.name == 'Snake':
            status = f'Score: {m.score}' + (' · You filled the board!' if m.over and m.food is None else ' · Game over' if m.over else '')
            for i, (x, y) in enumerate(m.body):
                old_x, old_y = before['body'][min(i, len(before['body']) - 1)]
                x, y = old_x + (x - old_x) * ease, old_y + (y - old_y) * ease
                self.rect(x * 20 + 1, y * 20 + 1, 18, 18, GOLD if i == 0 else '#80c6a5')
            if m.food:
                self.oval(m.food[0] * 20 + 2, m.food[1] * 20 + 2, 16, 16, CORAL)
        elif self.name == 'Tetris':
            status = f'Score: {m.score} · Lines: {m.lines}' + (' · Game over' if m.over else '')
            self.rect(10, 0, 200, 400, '#26334c')
            for y, row in enumerate(m.board):
                for x, value in enumerate(row):
                    self.rect(11 + x * 20, y * 20 + 1, 18, 18, BLOCKS[value])
            for x, y in m.piece:
                px, py = m.x + x, m.y + y
                if before['board'] == m.board and before['piece'] == m.piece and before['kind'] == m.kind:
                    px = before['x'] + x + (m.x - before['x']) * ease
                    py = before['y'] + y + (m.y - before['y']) * ease
                self.rect(11 + px * 20, py * 20 + 1, 18, 18, BLOCKS[m.kind + 1])
            if animation and m.lines > before['lines']:
                self.text(300, 280 - 25 * ease, f"+{m.lines - before['lines']} lines!", 18, GOLD)
            self.text(300, 35, 'NEXT', 14)
            for x, y in games.SHAPES[m.next]:
                self.rect(250 + x * 23, 70 + y * 23, 21, 21, BLOCKS[m.next + 1])
            self.text(300, 180, 'Clear full rows', 12)
            self.text(300, 210, 'Space to drop', 12)
        elif self.name == 'Blackjack':
            status = m.result or 'Hit for another card, or stand.'
            self.text(200, 25, 'PRACTICE TABLE · NO MONEY', 12, '#80c6a5')
            for cards, y, title in ((m.dealer, 95, 'Dealer'), (m.player, 270, 'You')):
                hidden = title == 'Dealer' and not m.result
                total = '?' if hidden else str(games.hand_value(cards))
                self.text(200, y - 30, f'{title} · {total}', 17)
                spacing = min(55, 350 / len(cards))
                start = 200 - (len(cards) - 1) * spacing / 2 - 23
                for i, (rank, suit) in enumerate(cards):
                    x = start + i * spacing
                    card_y = y
                    old_cards = before['dealer' if title == 'Dealer' else 'player']
                    if animation and i >= len(old_cards):
                        x += (365 - x) * (1 - ease)
                        card_y -= 80 * (1 - ease)
                    width = 46
                    revealing = animation and title == 'Dealer' and i == 1 and not before['result'] and m.result
                    face_down = hidden and i == 1
                    if revealing:
                        width *= max(.06, abs(2 * progress - 1))
                        face_down = progress < .5
                    self.rect(x + (46 - width) / 2, card_y, width, 72, '#354969' if face_down else '#293d53')
                    label = '?' if hidden and i == 1 else f'{ {1: "A", 11: "J", 12: "Q", 13: "K"}.get(rank, rank)}\n{suit}'
                    if width > 25:
                        self.text(x + 23, card_y + 36, '?' if face_down else label, 15, CORAL if suit in ('♥', '♦') else INK)
        elif self.name == 'Pong':
            status = f'You {m.scores[0]}  :  {m.scores[1]} Computer · First to 7'
            if m.over: status = 'You win!' if m.scores[0] == 7 else 'Computer wins!'
            for y in range(0, 400, 24): self.rect(199, y, 2, 12, '#33415c')
            self.rect(14, before['player'] + (m.player - before['player']) * ease - 36, 8, 72, GOLD)
            self.rect(378, before['computer'] + (m.computer - before['computer']) * ease - 36, 8, 72, CORAL)
            x, y = m.x, m.y
            if before['scores'] == m.scores:
                x = before['x'] + (m.x - before['x']) * progress
                y = before['y'] + (m.y - before['y']) * progress
            self.oval(x - 7, y - 7, 14, 14, GOLD)
        elif self.name in EXTRA_ENGINES:
            status = self.draw_extra(before, progress, ease)
        if self.name in REALTIME and self.paused and not m.over:
            status += ' · Paused — press Play / Resume'
        self.status.config(text=status)

    def tile(self, x, y, value, size=1):
        palette = ('#2a3750', '#53627b', '#677e87', '#9c7957', '#b78650', '#b76b61', '#9c5d85', '#725eaa', '#4c7eaa', '#439c9b', '#a18439', '#aa8734')
        color = palette[min(value.bit_length() - 1, len(palette) - 1)] if value else palette[0]
        side = 90 * size
        self.rect(x * 100 + 50 - side / 2, y * 100 + 50 - side / 2, side, side, color)
        if value:
            self.text(x * 100 + 50, y * 100 + 50, str(value), (25 if value < 10000 else 18) * size)
