"""An in-person, click-to-move chess table."""
import queue
import threading
from uuid import uuid4
import tkinter as tk
from tkinter import ttk

import chess
import chess_lounge as lounge
import winterfield_ui as ui


class ChessTable(ttk.Frame):
    location_key = 'chess'
    allows_group = True

    def __init__(self, parent, game, who, name):
        super().__init__(parent, padding=10)
        self.game = game
        self.board = chess.Board()
        self.name = name
        self.opponent = who
        self.match_id = uuid4().hex
        self.captures = {chess.WHITE: [], chess.BLACK: []}
        self.skill = lounge.level(who) if who else 3
        self.selected = None
        self.last_move = None
        self.pending = None
        self.timer = None
        self.answers = queue.Queue()
        self.finished = False

        header = ttk.Frame(self)
        header.pack(fill='x')
        ttk.Button(header, text='Leave table', command=game.leave_main_area).pack(side='right')
        ttk.Label(header, text=name, font=('Georgia', 18, 'bold')).pack(side='left')
        ttk.Label(self, text=f'Stockfish level {self.skill}   ·   You play White').pack(anchor='w')
        if who is not None:
            self.record = tk.StringVar(self)
            ttk.Label(self, textvariable=self.record).pack(anchor='w')
            self.update_record()
        self.score = tk.StringVar(self)
        ttk.Label(self, textvariable=self.score, justify='left').pack(anchor='w')
        self.update_score()
        self.status = tk.StringVar(self, 'Choose a white piece to see its legal moves.')
        ttk.Label(self, textvariable=self.status, wraplength=450).pack(anchor='w', pady=4)
        self.actions = ttk.Frame(self)
        self.actions.pack(fill='x')
        self.canvas = tk.Canvas(self, bg=ui.INK, highlightthickness=0, width=280, height=280)
        self.canvas.pack(fill='both', expand=True)
        self.canvas.bind('<Configure>', lambda event: self.draw())
        self.canvas.bind('<Button-1>', self.click)
        self.bind('<Destroy>', self.cleanup)

    def cleanup(self, event):
        if event.widget is self and self.timer is not None:
            self.after_cancel(self.timer)
            self.timer = None

    def geometry_values(self):
        width, height = self.canvas.winfo_width(), self.canvas.winfo_height()
        size = max(1, (min(width, height) - 38) // 8)
        return (width - 8 * size) // 2, (height - 8 * size) // 2, size

    def draw(self):
        c = self.canvas
        c.delete('all')
        left, top, size = self.geometry_values()
        targets = {m.to_square for m in self.board.legal_moves if m.from_square == self.selected}
        for sq in chess.SQUARES:
            file, rank = chess.square_file(sq), chess.square_rank(sq)
            x, y = left + size * file, top + size * (7 - rank)
            fill = '#a9bbaa' if (file + rank) % 2 else '#617c78'
            if self.last_move and sq in (self.last_move.from_square, self.last_move.to_square):
                fill = '#c2ae78'
            if sq == self.selected:
                fill = '#e6c67e'
            c.create_rectangle(x, y, x+size, y+size, fill=fill, outline='')
            cx, cy = x + size/2, y + size/2
            piece = self.board.piece_at(sq)
            if piece:
                glyph = piece.unicode_symbol(invert_color=piece.color == chess.WHITE)
                font = ('Segoe UI Symbol', -max(1, int(size*.78)))
                if piece.color:
                    for dx, dy in ((-1,0),(1,0),(0,-1),(0,1)):
                        c.create_text(cx+dx, cy+dy, text=glyph, fill=ui.INK, font=font)
                c.create_text(cx, cy, text=glyph, fill='#fff5db' if piece.color else '#172337', font=font)
            if sq in targets:
                radius = size * (.43 if piece else .09)
                c.create_oval(cx-radius, cy-radius, cx+radius, cy+radius, outline='#244c46',
                              width=2, fill='' if piece else '#244c46')
            if file == 0:
                c.create_text(left-9, cy, text=str(rank+1), fill=ui.MUTED)
            if rank == 0:
                c.create_text(cx, top+size*8+9, text=chess.FILE_NAMES[file], fill=ui.MUTED)

    def click(self, event):
        if self.finished or not self.board.turn or self.pending:
            return
        left, top, size = self.geometry_values()
        file, row = (event.x-left)//size, (event.y-top)//size
        if not (0 <= file < 8 and 0 <= row < 8):
            return
        sq = chess.square(file, 7-row)
        moves = [m for m in self.board.legal_moves if m.from_square == self.selected and m.to_square == sq]
        if len(moves) > 1:
            self.pending = moves
            self.status.set('Promote your pawn.')
            for move in moves:
                ttk.Button(self.actions, text=chess.piece_name(move.promotion).title(),
                           command=lambda m=move: self.play(m)).pack(side='left')
        elif moves:
            self.play(moves[0])
        else:
            self.selected = sq if self.board.color_at(sq) == chess.WHITE and self.selected != sq else None
            self.draw()

    def update_score(self):
        self.score.set(f'You captured · {lounge.capture_summary(self.captures[chess.WHITE])}\n'
                       f'{self.name} captured · {lounge.capture_summary(self.captures[chess.BLACK])}')

    def update_record(self):
        totals, _ = lounge.match_history(self.game.state_data, self.opponent)
        self.record.set('Your record   ·   Wins {wins}   ·   Losses {losses}   ·   Draws {draws}'.format(**totals))

    def rematch(self):
        if self.opponent is not None and self.opponent not in lounge.opponents(self.game.state_data):
            self.status.set(self.status.get().split('\n')[0] + f'\n{self.name} is no longer available for a rematch.')
            return
        self.game.enter_chess(self.opponent, self.name)

    def play(self, move):
        if self.finished:
            return
        for child in self.actions.winfo_children():
            child.destroy()
        self.pending = self.selected = None
        notation = self.board.san(move)
        piece = lounge.captured_piece(self.board, move)
        if piece is not None:
            self.captures[self.board.turn].append(piece)
            self.update_score()
        self.board.push(move)
        self.last_move = move
        self.draw()
        outcome = self.board.outcome(claim_draw=True)
        if outcome:
            self.finished = True
            reason = outcome.termination.name.lower().replace('_', ' ')
            result = 'Draw' if outcome.winner is None else 'You won' if outcome.winner else 'You lost'
            self.status.set(f'{result}   ·   {reason.capitalize()}   ·   {notation} ({outcome.result()})')
            if self.opponent is not None:
                lounge.remember_match(self.game.state_data, self.match_id, self.opponent,
                                      outcome, notation, self.captures)
                self.game.persist()
                self.update_record()
            ttk.Button(self.actions, text='Rematch', command=self.rematch).pack(side='left')
        elif self.board.turn:
            self.status.set(f'{self.name} played {notation}. ' + ('Check! ' if self.board.is_check() else '') + 'Your move.')
        else:
            self.think()

    def think(self):
        for child in self.actions.winfo_children():
            child.destroy()
        self.status.set(f'{self.name} is thinking…')
        position = self.board.copy()
        def worker():
            try:
                answer = lounge.reply(position, self.skill)
            except (OSError, RuntimeError, ValueError, TimeoutError) as error:
                answer = error
            self.answers.put(answer)
        threading.Thread(target=worker, daemon=True).start()
        self.timer = self.after(50, self.poll)

    def poll(self):
        self.timer = None
        try:
            result = self.answers.get_nowait()
        except queue.Empty:
            self.timer = self.after(50, self.poll)
            return
        if isinstance(result, Exception):
            self.status.set(f'Stockfish could not move. {result}')
            ttk.Button(self.actions, text='Retry move', command=self.think).pack(side='left')
        else:
            self.play(result)


class MatchHistory(ttk.Frame):
    location_key = 'chess'
    allows_group = True

    def __init__(self, parent, game):
        super().__init__(parent, padding=16)
        import game_core as core
        import hidden_cast
        state = game.state_data
        head = ttk.Frame(self)
        head.pack(fill='x')
        ttk.Label(head, text='Chess match history', font=('Georgia', 19, 'bold')).pack(side='left')
        ttk.Button(head, text='Back to lounge', command=game.leave_main_area).pack(side='right')
        self.by_opponent = {}
        for match in lounge.saved_games(state):
            self.by_opponent.setdefault(match['opponent'], []).append(match)
        if not self.by_opponent:
            ttk.Label(self, text='Your first completed match against a character will appear here.').pack(anchor='w', pady=16)
            return
        self.names = {who: core.contact_name(state, who) if hidden_cast.known(state, who) else 'Someone new'
                      for who in self.by_opponent}
        self.opponents = self.listing(('Opponent','Wins','Losses','Draws'), (240,65,65,65), 5)
        for who in sorted(self.by_opponent, key=self.names.get):
            totals = lounge.totals_for(self.by_opponent[who])
            self.opponents.insert('', 'end', iid=who, values=(self.names[who], totals['wins'],
                                                              totals['losses'], totals['draws']))
        self.heading = tk.StringVar(self)
        ttk.Label(self, textvariable=self.heading, font=('Georgia', 14, 'bold')).pack(anchor='w', pady=(12,0))
        self.games = self.listing(('Game','Played','Your result','Final move'), (60,190,100,95), 7)
        self.detail = tk.StringVar(self)
        ttk.Label(self, textvariable=self.detail, justify='left', wraplength=560).pack(anchor='w', pady=6)
        self.opponents.bind('<<TreeviewSelect>>', self.select_opponent)
        self.games.bind('<<TreeviewSelect>>', self.select_game)
        self.opponents.selection_set(self.opponents.get_children()[0])
        self.select_opponent()

    def listing(self, columns, widths, rows):
        box = ttk.Frame(self)
        box.pack(fill='both', expand=True, pady=(6,0))
        tree = ttk.Treeview(box, columns=columns, show='headings', height=rows, selectmode='browse')
        scroll = ttk.Scrollbar(box, command=tree.yview)
        tree.configure(yscrollcommand=scroll.set)
        scroll.pack(side='right', fill='y')
        tree.pack(side='left', fill='both', expand=True)
        for column, width in zip(columns, widths):
            tree.heading(column, text=column, anchor='w')
            tree.column(column, width=width, minwidth=45, anchor='w')
        return tree

    def select_opponent(self, event=None):
        import story_calendar
        selection = self.opponents.selection()
        if not selection:
            return
        self.who = selection[0]
        self.heading.set('Games against ' + self.names[self.who])
        self.games.delete(*self.games.get_children())
        matches = self.by_opponent[self.who]
        for index in reversed(range(len(matches))):
            match = matches[index]
            minute = match['minute']
            played = f'{story_calendar.story_date(minute):%d %b %Y}  {minute%1440//60:02}:{minute%60:02}'
            result = {'1-0':'Won', '0-1':'Lost', '1/2-1/2':'Draw'}.get(match['result'], 'Unknown')
            self.games.insert('', 'end', iid=str(index), values=(index+1, played, result, match['move']))
        self.games.selection_set(self.games.get_children()[0])
        self.select_game()

    def select_game(self, event=None):
        selection = self.games.selection()
        if selection:
            index = int(selection[0])
            match = self.by_opponent[self.who][index]
            self.detail.set(f'Game {index+1}   ·   {match["reason"].capitalize()}\n'
                            f'You captured · {match["white"]}\n'
                            f'{self.names[self.who]} captured · {match["black"]}')
