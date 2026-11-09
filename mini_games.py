"""Small, dependency-free game engines for the phone arcade."""
import random


class Connect4:
    def __init__(self):
        self.board = [[0] * 7 for _ in range(6)]
        self.result = ''

    def drop(self, col, player):
        if self.result or not 0 <= col < 7 or self.board[0][col]:
            return False
        row = next(r for r in range(5, -1, -1) if not self.board[r][col])
        self.board[row][col] = player
        for dx, dy in ((1, 0), (0, 1), (1, 1), (1, -1)):
            count = 1
            for sign in (-1, 1):
                x, y = col + dx * sign, row + dy * sign
                while 0 <= x < 7 and 0 <= y < 6 and self.board[y][x] == player:
                    count += 1
                    x, y = x + dx * sign, y + dy * sign
            if count >= 4:
                self.result = 'You win!' if player == 1 else 'Computer wins!'
        if not self.result and all(self.board[0]):
            self.result = 'Draw!'
        return True

    def computer(self):
        legal = [c for c in (3, 2, 4, 1, 5, 0, 6) if not self.board[0][c]]
        if self.result or not legal:
            return
        for player in (2, 1):
            for col in legal:
                trial = Connect4()
                trial.board = [row[:] for row in self.board]
                trial.drop(col, player)
                if trial.result and trial.result != 'Draw!':
                    self.drop(col, 2)
                    return
        self.drop(legal[0], 2)


def merge_line(line):
    values = [n for n in line if n]
    result, score = [], 0
    i = 0
    while i < len(values):
        n = values[i]
        if i + 1 < len(values) and n == values[i + 1]:
            n *= 2
            score += n
            i += 1
        result.append(n)
        i += 1
    return result + [0] * (len(line) - len(result)), score


class Tiles2048:
    def __init__(self):
        self.board = [[0] * 4 for _ in range(4)]
        self.score = 0
        self.over = False
        self.spawn()
        self.spawn()

    def spawn(self):
        empty = [(x, y) for y in range(4) for x in range(4) if not self.board[y][x]]
        if empty:
            x, y = random.choice(empty)
            self.board[y][x] = 4 if random.random() < .1 else 2

    def move(self, direction):
        if self.over:
            return False
        vertical = direction in ('up', 'down')
        reverse = direction in ('right', 'down')
        before = [r[:] for r in self.board]
        for i in range(4):
            line = [self.board[j][i] if vertical else self.board[i][j] for j in range(4)]
            merged, points = merge_line(line[::-1] if reverse else line)
            if reverse:
                merged.reverse()
            self.score += points
            for j, value in enumerate(merged):
                if vertical:
                    self.board[j][i] = value
                else:
                    self.board[i][j] = value
        changed = self.board != before
        if changed:
            self.spawn()
        self.over = not any(0 in row for row in self.board) and not any(
            self.board[y][x] == self.board[ny][nx]
            for y in range(4) for x in range(4)
            for nx, ny in ((x + 1, y), (x, y + 1)) if nx < 4 and ny < 4)
        return changed


class Snake:
    size = 20

    def __init__(self):
        self.body = [(9, 10), (8, 10), (7, 10)]
        self.direction = (1, 0)
        self.pending = self.direction
        self.score = 0
        self.over = False
        self.food = None
        self.feed()

    def feed(self):
        free = [(x, y) for y in range(self.size) for x in range(self.size) if (x, y) not in self.body]
        self.food = random.choice(free) if free else None
        if not free:
            self.over = True

    def turn(self, direction):
        if direction != (-self.direction[0], -self.direction[1]):
            self.pending = direction

    def step(self):
        if self.over:
            return
        self.direction = self.pending
        head = tuple(a + b for a, b in zip(self.body[0], self.direction))
        eating = head == self.food
        if not all(0 <= n < self.size for n in head) or head in (self.body if eating else self.body[:-1]):
            self.over = True
            return
        self.body.insert(0, head)
        if eating:
            self.score += 10
            self.feed()
        else:
            self.body.pop()


SHAPES = (
    ((0, 1), (1, 1), (2, 1), (3, 1)),
    ((1, 0), (2, 0), (1, 1), (2, 1)),
    ((1, 0), (0, 1), (1, 1), (2, 1)),
    ((1, 0), (2, 0), (0, 1), (1, 1)),
    ((0, 0), (1, 0), (1, 1), (2, 1)),
    ((0, 0), (0, 1), (1, 1), (2, 1)),
    ((2, 0), (0, 1), (1, 1), (2, 1)),
)


class Tetris:
    def __init__(self):
        self.board = [[0] * 10 for _ in range(20)]
        self.score = self.lines = 0
        self.over = False
        self.bag = []
        self.next = self.take()
        self.spawn()

    def take(self):
        if not self.bag:
            self.bag = list(range(7))
            random.shuffle(self.bag)
        return self.bag.pop()

    def spawn(self):
        self.kind, self.next = self.next, self.take()
        self.piece = list(SHAPES[self.kind])
        self.x, self.y = 3, 0
        self.over = not self.fits(self.piece, self.x, self.y)

    def fits(self, piece, x, y):
        return all(0 <= x + px < 10 and 0 <= y + py < 20 and not self.board[y + py][x + px]
                   for px, py in piece)

    def move(self, dx, dy):
        if self.over or not self.fits(self.piece, self.x + dx, self.y + dy):
            return False
        self.x += dx
        self.y += dy
        return True

    def rotate(self):
        if self.over or self.kind == 1:
            return
        size = 4 if self.kind == 0 else 3
        rotated = [(size - 1 - y, x) for x, y in self.piece]
        for offset in (0, -1, 1, -2, 2):
            if self.fits(rotated, self.x + offset, self.y):
                self.piece = rotated
                self.x += offset
                return

    def step(self):
        if self.over or self.move(0, 1):
            return
        for x, y in self.piece:
            self.board[self.y + y][self.x + x] = self.kind + 1
        remaining = [row for row in self.board if not all(row)]
        cleared = 20 - len(remaining)
        self.lines += cleared
        self.score += (0, 100, 300, 500, 800)[cleared]
        self.board = [[0] * 10 for _ in range(cleared)] + remaining
        self.spawn()

    def drop(self):
        if self.over:
            return
        while self.move(0, 1):
            self.score += 2
        self.step()


def hand_value(cards):
    total = sum(min(rank, 10) if rank != 1 else 11 for rank, suit in cards)
    aces = sum(rank == 1 for rank, suit in cards)
    while total > 21 and aces:
        total -= 10
        aces -= 1
    return total


class Blackjack:
    def __init__(self):
        self.deck = [(r, s) for s in ('♠', '♥', '♦', '♣') for r in range(1, 14)]
        random.shuffle(self.deck)
        self.player = [self.deck.pop(), self.deck.pop()]
        self.dealer = [self.deck.pop(), self.deck.pop()]
        self.result = ''
        p, d = hand_value(self.player), hand_value(self.dealer)
        if p == 21 or d == 21:
            self.result = 'Push — both have Blackjack.' if p == d else ('Blackjack! You win.' if p == 21 else 'Dealer Blackjack.')

    def hit(self):
        if self.result:
            return
        self.player.append(self.deck.pop())
        if hand_value(self.player) > 21:
            self.result = 'Bust! Dealer wins.'
        elif hand_value(self.player) == 21:
            self.stand()

    def stand(self):
        if self.result:
            return
        while hand_value(self.dealer) < 17:
            self.dealer.append(self.deck.pop())
        p, d = hand_value(self.player), hand_value(self.dealer)
        self.result = 'You win!' if d > 21 or p > d else ('Push — a tie.' if p == d else 'Dealer wins.')


class Pong:
    def __init__(self):
        self.player = self.computer = 200
        self.scores = [0, 0]
        self.over = False
        self.serve()

    def serve(self):
        self.x = self.y = 200.
        self.vx = random.choice((-4., 4.))
        self.vy = random.choice((-2., 2.))

    def move(self, delta):
        self.player = max(36, min(364, self.player + delta))

    def step(self):
        if self.over:
            return
        self.computer = max(36, min(364, self.computer + max(-2.7, min(2.7, self.y - self.computer))))
        old_x = self.x
        self.x += self.vx
        self.y += self.vy
        if self.y <= 7 or self.y >= 393:
            self.y = max(7, min(393, self.y))
            self.vy *= -1
        for edge, paddle, left in ((29, self.player, True), (371, self.computer, False)):
            crossed = self.vx < 0 and self.x <= edge <= old_x if left else self.vx > 0 and old_x <= edge <= self.x
            if crossed and abs(self.y - paddle) <= 43:
                self.x = edge
                self.vx = min(8, abs(self.vx) + .25) * (1 if left else -1)
                self.vy = (self.y - paddle) / 9
        if self.x < 0 or self.x > 400:
            self.scores[0 if self.x > 400 else 1] += 1
            self.over = max(self.scores) >= 7
            if not self.over:
                self.serve()
