"""Canvas interactions and animated rendering for the expanded arcade."""
from copy import deepcopy
from math import sin, pi
from tkinter import ttk
import arcade_games as games

EXTRA_ENGINES = {'Memory Match': games.MemoryMatch, 'Minesweeper': games.Minesweeper,
                 'Breakout': games.Breakout, 'Match-3': games.Match3,
                 'Word Search': games.WordSearch, 'Simon Says': games.Simon,
                 'Solitaire': games.Solitaire}
EXTRA_HELP = {
    'Memory Match': 'Tap two cards to find a pair. Match all eight pairs to win.',
    'Minesweeper': 'Click to reveal. Right-click or use Flag mode to mark mines. First reveal is safe.',
    'Breakout': 'Move mouse or use ← / →. Play, then Space to launch. Catch + for a wider paddle.',
    'Match-3': 'Tap two adjacent gems to swap. Make rows of 3+ and chain cascades. 30 moves.',
    'Word Search': 'Drag across a word, or tap its first and last letters. Words can run in any direction.',
    'Simon Says': 'Watch the lights, then repeat with the pads or keys 1–4. Replay restarts this round.',
    'Solitaire': 'Draw-one Klondike. Click stock to deal. Select a card then a destination, or drag it. Aces go above; only Kings fill empty columns.',
}
COLORS = ('#f08a8a', '#f0c875', '#80c6a5', '#739fe9', '#b494ef')
INK, BG, GOLD = '#c4d1e3', '#141c2e', '#f0c875'


class ExtraArcade:
    def later(self, ms, callback):
        token = None
        def run():
            self.jobs.discard(token)
            callback()
        token = self.after(ms, run)
        self.jobs.add(token)
        return token

    def cancel_jobs(self):
        for token in self.jobs:
            self.after_cancel(token)
        self.jobs.clear()

    def setup_extra(self, controls):
        self.selection = None
        self.drag_start = None
        self.drag_point = None
        self.dragging = False
        self.flag_mode = False
        self.busy = False
        self.lit = None
        self.word_anchor = None
        self.canvas.bind('<Button-3>', self.right_click)
        self.canvas.bind('<B1-Motion>', self.drag)
        self.canvas.bind('<ButtonRelease-1>', self.release)
        self.canvas.bind('<Motion>', self.pointer_move)
        if self.name == 'Minesweeper':
            self.flag_button = ttk.Button(controls, text='Flag: Off', command=self.toggle_flag)
            self.flag_button.pack(side='left')
            difficulty = ttk.Combobox(controls, values=('Easy', 'Medium', 'Hard'), width=8, state='readonly')
            difficulty.set(self.model.difficulty)
            popup = difficulty.tk.call('ttk::combobox::PopdownWindow', str(difficulty))
            difficulty.tk.call(str(popup) + '.f.l', 'configure', '-background', '#293447',
                               '-foreground', INK, '-selectbackground', '#3b4a60',
                               '-selectforeground', GOLD, '-highlightbackground', '#293447')
            difficulty.pack(side='left', padx=6)
            def change(_):
                self.sessions[self.name] = games.Minesweeper(difficulty.get())
                self.open(self.name)
            difficulty.bind('<<ComboboxSelected>>', change)
        elif self.name == 'Simon Says':
            ttk.Button(controls, text='Replay sequence', command=self.simon_play).pack(side='left')
            if not self.model.over: self.later(450, self.simon_play)
            self.busy = not self.model.over
        elif self.name == 'Solitaire':
            ttk.Button(controls, text='To foundation', command=self.solitaire_auto).pack(side='left')
        elif self.name == 'Memory Match' and len(self.model.face_up) == 2:
            self.later(700, self.memory_hide)
        elif self.name == 'Match-3' and self.model.matches:
            self.busy = True
            self.later(350, self.match_settle)

    def toggle_flag(self):
        self.flag_mode = not self.flag_mode
        self.flag_button.config(text='Flag: On' if self.flag_mode else 'Flag: Off')

    def cell_at(self, x, y, size, top=0, side=400):
        if 0 <= x < side and top <= y < top + side:
            return int(x / (side / size)), int((y - top) / (side / size))
        return None

    def extra_click(self, x, y):
        m = self.model
        if self.name not in EXTRA_ENGINES: return False
        if self.busy or (self.animation and self.name != 'Breakout'): return True
        before = deepcopy(m.__dict__)
        if self.name == 'Memory Match':
            cell = self.cell_at(x, y, 4)
            if cell and m.flip(cell[1] * 4 + cell[0]):
                self.effect('win' if m.over else 'match' if len(m.matched) > len(before['matched']) else 'flip')
                self.animate(before, .25)
                if len(m.face_up) == 2: self.later(850, self.memory_hide)
        elif self.name == 'Minesweeper':
            cell = self.cell_at(x, y, m.size)
            if cell:
                if self.flag_mode: m.flag(cell)
                else: m.reveal(cell)
                if before != m.__dict__:
                    self.effect('win' if m.won else 'lose' if m.over else 'reveal')
                    self.animate(before, .32)
        elif self.name == 'Match-3':
            cell = self.cell_at(x, y, 7)
            if cell and not m.over:
                if self.selection is None:
                    self.selection = cell
                    self.effect('tap')
                else:
                    source = self.selection
                    self.selection = None
                    if m.swap(source, cell):
                        self.busy = True
                        self.effect('slide')
                        self.animate(before, .23, ('swap', source, cell))
                        self.later(280, self.match_flash)
                    else: self.effect('invalid')
                self.draw()
        elif self.name == 'Word Search':
            # Letters occupy the upper 320 pixels, leaving room for the word list.
            cell = (int(x / 40), int(y / 32)) if 0 <= x < 400 and 0 <= y < 320 else None
            if cell and not m.over:
                self.drag_start = cell
                if self.word_anchor is None:
                    self.word_anchor = cell
                    self.selection = [cell]
                else:
                    self.word_finish(cell)
                self.draw()
        elif self.name == 'Simon Says':
            if 25 <= x < 375 and 25 <= y < 375:
                self.simon_press((1 if x >= 200 else 0) + (2 if y >= 200 else 0))
        elif self.name == 'Solitaire':
            hit = self.solitaire_hit(x, y)
            if hit and hit[0] == 'stock':
                if m.draw():
                    self.selection = None
                    self.effect('card')
                    self.animate(before, .22)
            elif hit:
                if self.selection and m.move(self.selection, hit[:2]):
                    self.selection = None
                    self.effect('win' if m.over else 'card')
                    self.animate(before, .25)
                elif hit[2] is not None:
                    self.selection = hit
                    self.drag_start = (x, y)
                    self.effect('tap')
                else: self.selection = None
            self.draw()
        elif self.name == 'Breakout':
            if not self.paused: m.launch()
        return True

    def right_click(self, event):
        if self.name != 'Minesweeper' or self.animation: return
        cell = self.cell_at(*self.logical(event.x, event.y), self.model.size)
        if cell:
            before = deepcopy(self.model.__dict__)
            self.model.flag(cell)
            if before != self.model.__dict__: self.effect('tap')
            self.draw()

    def pointer_move(self, event):
        if self.name == 'Breakout' and not self.paused:
            x, _ = self.logical(event.x, event.y)
            self.model.move(x - self.model.paddle)
            self.draw()

    def drag(self, event):
        if self.busy or self.animation or self.drag_start is None: return
        x, y = self.logical(event.x, event.y)
        if self.name == 'Word Search' and self.word_anchor is not None:
            cell = (max(0, min(9, int(x / 40))), max(0, min(9, int(y / 32))))
            self.selection = games.WordSearch.line(self.word_anchor, cell)
            self.dragging = cell != self.drag_start
        elif self.name == 'Solitaire' and self.selection:
            self.dragging = abs(x - self.drag_start[0]) + abs(y - self.drag_start[1]) > 5
            self.drag_point = (x, y)
        self.draw()

    def release(self, event):
        x, y = self.logical(event.x, event.y)
        if self.name == 'Word Search' and self.dragging and self.word_anchor:
            if 0 <= x < 400 and 0 <= y < 320: self.word_finish((int(x / 40), int(y / 32)))
            else: self.word_anchor = self.selection = None
        elif self.name == 'Solitaire' and self.dragging and self.selection:
            before = deepcopy(self.model.__dict__)
            target = self.solitaire_hit(x, y)
            if target and self.model.move(self.selection, target[:2]):
                self.effect('win' if self.model.over else 'card')
                self.animate(before, .25)
            else: self.effect('invalid')
            self.selection = None
        self.dragging = False
        self.drag_start = self.drag_point = None
        self.draw()

    def word_finish(self, cell):
        before = deepcopy(self.model.__dict__)
        if self.model.select(self.word_anchor, cell):
            self.effect('win' if self.model.over else 'match')
            self.animate(before, .35)
        else: self.effect('invalid')
        self.word_anchor = self.selection = None

    def memory_hide(self):
        before = deepcopy(self.model.__dict__)
        self.model.hide()
        self.animate(before, .22)

    def match_flash(self):
        self.effect('match')
        self.animate(deepcopy(self.model.__dict__), .22, 'flash', force=True)
        self.later(240, self.match_settle)

    def match_settle(self):
        before = deepcopy(self.model.__dict__)
        self.model.settle()
        self.animate(before, .32, 'fall')
        self.later(350, self.match_continue)

    def match_continue(self):
        if self.model.matches: self.match_flash()
        else:
            self.busy = False
            if self.model.over: self.effect('win')
            self.draw()

    def simon_play(self):
        if self.model.over: return
        self.cancel_jobs()
        self.model.position = 0
        self.busy = True
        self.lit = None
        self.draw()
        def light(index):
            if index == len(self.model.sequence):
                self.lit = None
                self.busy = False
                self.draw()
                return
            self.lit = self.model.sequence[index]
            self.effect(f'note{self.lit}')
            self.draw()
            def dark():
                self.lit = None
                self.draw()
                self.later(180, lambda: light(index + 1))
            self.later(420, dark)
        self.later(300, lambda: light(0))

    def simon_press(self, color):
        if self.busy or self.model.over: return
        outcome = self.model.press(color)
        self.lit = color
        self.busy = True
        self.effect('lose' if outcome == 'lose' else f'note{color}')
        self.draw()
        def unlight():
            self.lit = None
            self.busy = False
            self.draw()
            if outcome == 'round':
                self.busy = True
                self.later(500, self.simon_play)
        self.later(220, unlight)

    def solitaire_positions(self, state):
        positions = {}
        for i, card in enumerate(state['stock']): positions[card] = (8, 10, False)
        for i, card in enumerate(state['waste']): positions[card] = (64, 10, True)
        for col, pile in enumerate(state['foundations']):
            for card in pile: positions[card] = (176 + col * 56, 10, True)
        for col, pile in enumerate(state['tableau']):
            gap = min(22, 225 / max(1, len(pile) - 1))
            for i, card in enumerate(pile): positions[card] = (8 + col * 56, 105 + i * gap, i >= state['hidden'][col])
        return positions

    def solitaire_hit(self, x, y):
        m = self.model
        if 10 <= y < 76:
            if 8 <= x < 56: return ('stock', 0, None)
            if 64 <= x < 112: return ('waste', 0, len(m.waste) - 1 if m.waste else None)
            for col in range(4):
                if 176 + col * 56 <= x < 224 + col * 56:
                    return ('foundation', col, len(m.foundations[col]) - 1 if m.foundations[col] else None)
        if 105 <= y < 396:
            col = int((x - 8) // 56)
            if 0 <= col < 7 and 8 + col * 56 <= x < 56 + col * 56:
                pile = m.tableau[col]
                if not pile: return ('tableau', col, None)
                gap = min(22, 225 / max(1, len(pile) - 1))
                if y > 105 + gap * (len(pile) - 1) + 66: return None
                index = min(len(pile) - 1, int((y - 105) / gap))
                return ('tableau', col, index) if index >= m.hidden[col] else None
        return None

    def solitaire_auto(self):
        if self.animation: return
        before = deepcopy(self.model.__dict__)
        if self.model.auto(self.selection):
            self.selection = None
            self.effect('win' if self.model.over else 'card')
            self.animate(before, .25)
        else: self.effect('invalid')

    def draw_card(self, x, y, card, face, selected=False):
        if selected: self.rect(x - 2, y - 2, 52, 70, GOLD)
        self.rect(x, y, 48, 66, '#293d53' if face else '#354969')
        rank, suit = card
        label = f'{ {1: "A", 11: "J", 12: "Q", 13: "K"}.get(rank, rank)}{("♥", "♦", "♠", "♣")[suit]}' if face else '◆'
        self.text(x + 24, y + (11 if face else 33), label, 12, '#f08a8a' if face and suit < 2 else INK if face else '#92add7')

    def draw_extra(self, before, progress, ease):
        m = self.model
        anim = self.animation
        status = ''
        if self.name == 'Memory Match':
            status = f'{len(m.matched) // 2}/8 pairs · {m.moves} turns' + (' · You win!' if m.over else '')
            old_visible = set(before['face_up']) | before['matched']
            visible = set(m.face_up) | m.matched
            for i, value in enumerate(m.cards):
                x, y = i % 4 * 100 + 7, i // 4 * 100 + 7
                face = i in visible
                width = 86
                if anim and (i in old_visible) != face:
                    width *= max(.05, abs(2 * progress - 1))
                    if progress < .5: face = i in old_visible
                self.rect(x + (86 - width) / 2, y, width, 86, '#36625a' if i in m.matched else '#46516b' if face else '#354969')
                if width > 35: self.text(x + 43, y + 43, ('★', '♥', '♣', '♦', '☀', '♫', '☂', '☾')[value] if face else '?', 34, GOLD if face else '#8da6ca')
        elif self.name == 'Minesweeper':
            status = f'{m.difficulty} · Flags {len(m.flags)}/{m.mine_count}' + (' · Cleared!' if m.won else ' · Mine! New game to retry.' if m.over else '')
            side = 400 / m.size
            newly = sorted(m.revealed - before['revealed'])
            visible = before['revealed'] | set(newly[:int(len(newly) * ease)]) if anim else m.revealed
            for y in range(m.size):
                for x in range(m.size):
                    cell = (x, y)
                    revealed = cell in visible
                    self.rect(x * side + 2, y * side + 2, side - 4, side - 4, '#233149' if revealed else '#496183')
                    label = '●' if m.over and cell in m.mines else '⚑' if cell in m.flags else str(m.count(cell)) if revealed and m.count(cell) else ''
                    self.text((x + .5) * side, (y + .5) * side, label, 18, COLORS[(m.count(cell) - 1) % 5] if revealed else GOLD)
        elif self.name == 'Breakout':
            status = f'Score {m.score} · Lives {m.lives}' + (' · You win!' if m.won else ' · Game over' if m.over else ' · Space / Launch to serve' if m.ready else '')
            for x, y in m.bricks: self.rect(9 + x * 48, 38 + y * 24, 44, 20, COLORS[y])
            for x, y, vx, vy, life in m.particles: self.rect(x, y, 2 + life / 8, 2 + life / 8, GOLD)
            for x, y in m.powerups:
                self.oval(x - 10, y - 10, 20, 20, '#80c6a5')
                self.text(x, y, '+', 14, BG)
            self.rect(m.paddle - m.half_width, 350, m.half_width * 2, 10, GOLD)
            self.oval(m.x - 6, m.y - 6, 12, 12, GOLD)
        elif self.name == 'Match-3':
            status = f'Score {m.score} · {m.moves} moves left' + (f' · Combo ×{m.combo}' if m.combo > 1 else '') + (' · Finished!' if m.over else '')
            phase = anim['direction'] if anim else None
            pieces = [(x, y, value) for y, row in enumerate(m.board) for x, value in enumerate(row)]
            if phase == 'fall' and m.falls:
                pieces = [(x, old_y + (y - old_y) * ease, value) for x, old_y, y, value in m.falls]
            elif isinstance(phase, tuple) and phase[0] == 'swap':
                a, b = phase[1:]
                pieces = [(x, y, value) for x, y, value in pieces if (x, y) not in (a, b)]
                for source, dest in ((a, b), (b, a)):
                    pieces.append((source[0] + (dest[0] - source[0]) * ease, source[1] + (dest[1] - source[1]) * ease, before['board'][source[1]][source[0]]))
            for x, y, value in pieces:
                side = 47
                if phase == 'flash' and (x, y) in m.matches: side *= 1 - .8 * progress
                cx, cy = (x + .5) * 400 / 7, (y + .5) * 400 / 7
                if cy < 0: continue
                if self.selection == (x, y): self.rect(cx - 27, cy - 27, 54, 54, GOLD)
                self.oval(cx - side / 2, cy - side / 2, side, side, COLORS[value])
                if side > 20: self.text(cx, cy, ('◆', '★', '●', '■', '♥')[value], 18, BG)
        elif self.name == 'Word Search':
            status = f'{m.theme} · {len(m.found)}/{len(m.words)} words' + (' · All found!' if m.over else '')
            found_cells = {cell for word in m.found for cell in m.paths[word]}
            new_cells = {cell for word in m.found - before['found'] for cell in m.paths[word]}
            for y, row in enumerate(m.board):
                for x, letter in enumerate(row):
                    color = '#36625a' if (x, y) in found_cells else '#283952'
                    if self.selection and (x, y) in self.selection: color = '#8c7547'
                    if anim and (x, y) in new_cells: color = '#68a185' if progress < .7 else color
                    self.rect(x * 40 + 1, y * 32 + 1, 38, 30, color)
                    self.text(x * 40 + 20, y * 32 + 16, letter, 16)
            for i, word in enumerate(m.words):
                self.text(68 + i % 3 * 132, 345 + i // 3 * 30, ('✓ ' if word in m.found else '') + word, 12, '#80c6a5' if word in m.found else INK)
        elif self.name == 'Simon Says':
            status = f'Round {len(m.sequence)} · {m.score} completed · ' + ('Game over' if m.over else 'Watch…' if self.busy else 'Your turn')
            for i in range(4):
                x, y = 25 + i % 2 * 180, 25 + i // 2 * 180
                lit = self.lit == i
                if lit: self.rect(x - 5, y - 5, 160, 160, '#80c6a5')
                self.rect(x, y, 150, 150, COLORS[i] if lit else ('#754047', '#776538', '#37624f', '#354d78')[i])
                self.text(x + 75, y + 75, str(i + 1), 40, BG if lit else INK)
        elif self.name == 'Solitaire':
            status = f'{sum(map(len, m.foundations))}/52 home · {m.moves} moves' + (' · You win!' if m.over else '')
            self.rect(8, 10, 48, 66, '#293c52')
            self.text(32, 43, '↻', 23)
            for col, suit in enumerate(('♥', '♦', '♠', '♣')):
                self.rect(176 + col * 56, 10, 48, 66, '#293c52')
                self.text(200 + col * 56, 43, suit, 20, '#69829d')
            for col in range(7): self.rect(8 + col * 56, 105, 48, 66, '#293c52')
            old_positions = self.solitaire_positions(before)
            positions = self.solitaire_positions(m.__dict__)
            drawn = []
            if m.stock: drawn.append(m.stock[-1])
            if m.waste: drawn.append(m.waste[-1])
            drawn += [pile[-1] for pile in m.foundations if pile]
            drawn += [card for pile in m.tableau for card in pile]
            # Moving cards render above the stationary piles.
            drawn.sort(key=lambda card: bool(anim and old_positions.get(card) != positions[card]))
            selected = []
            if self.selection:
                kind, col, index = self.selection
                selected = m.pile(kind, col)[index:]
            for card in drawn:
                x, y, face = positions[card]
                if anim and card in old_positions:
                    ox, oy, old_face = old_positions[card]
                    x, y = ox + (x - ox) * ease, oy + (y - oy) * ease
                if self.dragging and card in selected: continue
                self.draw_card(x, y, card, face, card in selected)
            if self.dragging and self.drag_point:
                for i, card in enumerate(selected): self.draw_card(self.drag_point[0] - 24, self.drag_point[1] - 12 + i * 22, card, True, True)
        return status
