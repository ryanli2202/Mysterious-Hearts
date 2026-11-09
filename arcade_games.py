"""Rules for the phone arcade's puzzle, memory, brick and card games."""
import random
import string


class MemoryMatch:
    def __init__(self):
        self.cards = list(range(8)) * 2
        random.shuffle(self.cards)
        self.face_up = []
        self.matched = set()
        self.moves = 0
        self.over = False

    def flip(self, index):
        if self.over or not 0 <= index < 16 or index in self.matched or index in self.face_up or len(self.face_up) == 2:
            return False
        self.face_up.append(index)
        if len(self.face_up) == 2:
            self.moves += 1
            if self.cards[self.face_up[0]] == self.cards[index]:
                self.matched.update(self.face_up)
                self.face_up.clear()
                self.over = len(self.matched) == 16
        return True

    def hide(self):
        if len(self.face_up) == 2:
            self.face_up.clear()


class Minesweeper:
    def __init__(self, difficulty='Easy'):
        self.difficulty = difficulty
        self.size, self.mine_count = {'Easy': (8, 10), 'Medium': (9, 15), 'Hard': (10, 22)}[difficulty]
        self.mines = set()
        self.revealed = set()
        self.flags = set()
        self.started = self.over = self.won = False

    def neighbors(self, cell):
        x, y = cell
        return {(nx, ny) for nx in range(max(0, x - 1), min(self.size, x + 2))
                for ny in range(max(0, y - 1), min(self.size, y + 2)) if (nx, ny) != cell}

    def count(self, cell):
        return len(self.neighbors(cell) & self.mines)

    def flag(self, cell):
        if self.over or cell in self.revealed:
            return
        if cell in self.flags: self.flags.remove(cell)
        elif len(self.flags) < self.mine_count: self.flags.add(cell)

    def reveal(self, cell):
        if self.over or cell in self.flags or cell in self.revealed:
            return
        if not self.started:
            safe = self.neighbors(cell) | {cell}
            available = [(x, y) for x in range(self.size) for y in range(self.size) if (x, y) not in safe]
            self.mines = set(random.sample(available, self.mine_count))
            self.started = True
        if cell in self.mines:
            self.revealed.add(cell)
            self.over = True
            return
        pending = [cell]
        while pending:
            current = pending.pop()
            if current in self.revealed or current in self.flags:
                continue
            self.revealed.add(current)
            if self.count(current) == 0:
                pending.extend(self.neighbors(current) - self.revealed - self.flags)
        self.won = len(self.revealed) == self.size ** 2 - self.mine_count
        self.over = self.won


class Breakout:
    def __init__(self):
        self.bricks = {(x, y) for y in range(5) for x in range(8)}
        self.paddle = 200.
        self.score = 0
        self.lives = 3
        self.over = self.won = False
        self.event = ''
        self.particles = []
        self.powerups = []
        self.wide = 0
        self.serve()

    @property
    def half_width(self):
        return 58 if self.wide else 38

    def serve(self):
        self.x, self.y = self.paddle, 325.
        self.vx, self.vy = random.choice((-2.6, 2.6)), -4.
        self.ready = True

    def move(self, delta):
        self.paddle = max(self.half_width, min(400 - self.half_width, self.paddle + delta))
        if self.ready: self.x = self.paddle

    def launch(self):
        self.ready = False

    def step(self):
        self.event = ''
        if self.over or self.ready:
            return
        self.wide = max(0, self.wide - 1)
        self.particles = [(x + vx, y + vy, vx, vy + .12, life - 1) for x, y, vx, vy, life in self.particles if life > 1]
        falling = []
        for px, py in self.powerups:
            py += 2
            if 342 <= py <= 360 and abs(px - self.paddle) <= self.half_width:
                self.wide = 500
                self.event = 'score'
            elif py < 400: falling.append((px, py))
        self.powerups = falling
        old_x, old_y = self.x, self.y
        self.x += self.vx
        self.y += self.vy
        if self.x < 6 or self.x > 394:
            self.x = max(6, min(394, self.x))
            self.vx *= -1
            self.event = 'bounce'
        if self.y < 6:
            self.y = 6
            self.vy = abs(self.vy)
            self.event = 'bounce'
        if self.vy > 0 and old_y <= 344 <= self.y and abs(self.x - self.paddle) <= self.half_width + 6:
            self.y = 344
            self.vy = -4.5
            self.vx = 4 * (self.x - self.paddle) / self.half_width
            self.event = 'bounce'
        for bx, by in sorted(self.bricks):
            left, top = 9 + bx * 48, 38 + by * 24
            if left - 6 <= self.x <= left + 50 and top - 6 <= self.y <= top + 26:
                self.bricks.remove((bx, by))
                self.score += 10
                if old_y < top - 6 or old_y > top + 26: self.vy *= -1
                else: self.vx *= -1
                self.particles.extend((left + 22, top + 10, random.uniform(-3, 3), random.uniform(-3, 1), 22) for _ in range(8))
                if random.random() < .16: self.powerups.append((left + 22, top))
                self.event = 'brick'
                break
        if not self.bricks:
            self.over = self.won = True
        elif self.y > 410:
            self.lives -= 1
            self.event = 'lose'
            self.over = self.lives == 0
            if not self.over: self.serve()


class Match3:
    size = 7

    def __init__(self):
        self.score = 0
        self.moves = 30
        self.over = False
        self.combo = 0
        self.matches = set()
        self.falls = []
        self.shuffle()

    def find_matches(self):
        found = set()
        for y in range(7):
            for x in range(7):
                for dx, dy in ((1, 0), (0, 1)):
                    if x + 2 * dx < 7 and y + 2 * dy < 7:
                        cells = [(x + i * dx, y + i * dy) for i in range(3)]
                        if len({self.board[cy][cx] for cx, cy in cells}) == 1:
                            found.update(cells)
        return found

    def swap_cells(self, a, b):
        ax, ay = a
        bx, by = b
        self.board[ay][ax], self.board[by][bx] = self.board[by][bx], self.board[ay][ax]

    def legal_moves(self):
        result = []
        for y in range(7):
            for x in range(7):
                for other in ((x + 1, y), (x, y + 1)):
                    if max(other) >= 7: continue
                    self.swap_cells((x, y), other)
                    if self.find_matches(): result.append(((x, y), other))
                    self.swap_cells((x, y), other)
        return result

    def shuffle(self):
        while True:
            self.board = [[-1] * 7 for _ in range(7)]
            for y in range(7):
                for x in range(7):
                    choices = set(range(5))
                    if x > 1 and self.board[y][x-1] == self.board[y][x-2]: choices.discard(self.board[y][x-1])
                    if y > 1 and self.board[y-1][x] == self.board[y-2][x]: choices.discard(self.board[y-1][x])
                    self.board[y][x] = random.choice(sorted(choices))
            if self.legal_moves(): return

    def swap(self, a, b):
        if self.over or self.matches or abs(a[0] - b[0]) + abs(a[1] - b[1]) != 1:
            return False
        self.swap_cells(a, b)
        self.matches = self.find_matches()
        if not self.matches:
            self.swap_cells(a, b)
            return False
        self.moves -= 1
        self.combo = 0
        self.falls = []
        return True

    def settle(self):
        if not self.matches: return
        self.combo += 1
        self.score += 10 * len(self.matches) * self.combo
        self.falls = []
        for x in range(7):
            survivors = [(y, self.board[y][x]) for y in range(7) if (x, y) not in self.matches]
            missing = 7 - len(survivors)
            entries = [(i - missing, random.randrange(5)) for i in range(missing)] + survivors
            for y, (old_y, value) in enumerate(entries):
                self.board[y][x] = value
                self.falls.append((x, old_y, y, value))
        self.matches = self.find_matches()
        if not self.matches:
            self.over = self.moves == 0
            if not self.over and not self.legal_moves():
                self.shuffle()
                self.falls = []


class WordSearch:
    size = 10
    themes = {'Winterfield': ('CAMPUS', 'RIVER', 'CAFE', 'GARDEN', 'ARCADE', 'MARKET'),
              'Friends': ('GARRETT', 'EMILY', 'SOPHIE', 'YURIKO', 'MINSU', 'APRIL'),
              'Hobbies': ('PAINT', 'MUSIC', 'DANCE', 'BAKING', 'GAMES', 'READING')}

    def __init__(self):
        self.theme = random.choice(list(self.themes))
        self.words = self.themes[self.theme]
        self.board = [[''] * 10 for _ in range(10)]
        self.paths = {}
        self.found = set()
        self.over = False
        for word in sorted(self.words, key=len, reverse=True):
            options = []
            for y in range(10):
                for x in range(10):
                    for dx, dy in ((1, 0), (0, 1), (1, 1), (-1, 1), (-1, 0), (0, -1), (-1, -1), (1, -1)):
                        cells = [(x + dx * i, y + dy * i) for i in range(len(word))]
                        if all(0 <= cx < 10 and 0 <= cy < 10 and self.board[cy][cx] in ('', letter)
                               for (cx, cy), letter in zip(cells, word)):
                            options.append(cells)
            cells = random.choice(options)
            self.paths[word] = cells
            for (x, y), letter in zip(cells, word): self.board[y][x] = letter
        for row in self.board:
            for i, letter in enumerate(row):
                if not letter: row[i] = random.choice(string.ascii_uppercase)

    @staticmethod
    def line(a, b):
        dx, dy = b[0] - a[0], b[1] - a[1]
        if dx and dy and abs(dx) != abs(dy): return []
        length = max(abs(dx), abs(dy))
        sx, sy = (dx > 0) - (dx < 0), (dy > 0) - (dy < 0)
        return [(a[0] + i * sx, a[1] + i * sy) for i in range(length + 1)]

    def select(self, a, b):
        cells = self.line(a, b)
        if not cells or self.over: return False
        text = ''.join(self.board[y][x] for x, y in cells)
        word = next((w for w in self.words if w not in self.found and w in (text, text[::-1])), None)
        if not word: return False
        self.found.add(word)
        self.paths[word] = cells
        self.over = len(self.found) == len(self.words)
        return True


class Simon:
    def __init__(self):
        self.sequence = [random.randrange(4)]
        self.position = 0
        self.score = 0
        self.over = False

    def press(self, color):
        if self.over: return 'over'
        if color != self.sequence[self.position]:
            self.over = True
            return 'lose'
        self.position += 1
        if self.position == len(self.sequence):
            self.score += 1
            self.position = 0
            self.sequence.append(random.randrange(4))
            return 'round'
        return 'correct'


class Solitaire:
    """Draw-one Klondike. Cards are (rank 1..13, suit 0..3); 0/1 are red."""
    def __init__(self):
        deck = [(rank, suit) for suit in range(4) for rank in range(1, 14)]
        random.shuffle(deck)
        self.tableau = [[deck.pop() for _ in range(i + 1)] for i in range(7)]
        self.hidden = list(range(7))
        self.stock = deck
        self.waste = []
        self.foundations = [[] for _ in range(4)]
        self.moves = 0
        self.over = False

    def draw(self):
        if self.over: return False
        if self.stock: self.waste.append(self.stock.pop())
        elif self.waste:
            self.stock = self.waste[::-1]
            self.waste = []
        else: return False
        self.moves += 1
        return True

    def pile(self, kind, col=0):
        return self.waste if kind == 'waste' else self.foundations[col] if kind == 'foundation' else self.tableau[col]

    def move(self, source, target):
        if self.over or source is None or target is None: return False
        kind, col, index = source
        dest_kind, dest_col = target
        if dest_kind not in ('tableau', 'foundation') or (kind, col) == target: return False
        pile = self.pile(kind, col)
        if not 0 <= index < len(pile): return False
        if kind == 'tableau' and index < self.hidden[col]: return False
        if kind != 'tableau' and index != len(pile) - 1: return False
        moving = pile[index:]
        rank, suit = moving[0]
        dest = self.pile(dest_kind, dest_col)
        if dest_kind == 'foundation':
            if len(moving) != 1 or suit != dest_col or rank != len(dest) + 1: return False
        else:
            if dest:
                top_rank, top_suit = dest[-1]
                if top_rank != rank + 1 or (top_suit < 2) == (suit < 2): return False
            elif rank != 13: return False
            if any(a[0] != b[0] + 1 or (a[1] < 2) == (b[1] < 2) for a, b in zip(moving, moving[1:])): return False
        dest.extend(moving)
        del pile[index:]
        if kind == 'tableau': self.hidden[col] = min(self.hidden[col], max(0, len(pile) - 1))
        self.moves += 1
        self.over = sum(map(len, self.foundations)) == 52
        return True

    def auto(self, source):
        if source is None: return False
        pile = self.pile(source[0], source[1])
        if not pile: return False
        return self.move(source, ('foundation', pile[-1][1]))
