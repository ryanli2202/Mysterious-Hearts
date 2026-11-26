"""Local chess rules, opponent selection and Stockfish tuning for the café."""
from pathlib import Path
import os
import re
import shutil
import subprocess

import chess
import chess.engine
import interiors
import leisure
import personality_types
import town_residents
import memory_store

PLAYING_ROOM = 'chess__playing_room'
ENGINE = Path(__file__).resolve().parent / 'vendor/stockfish/stockfish-windows-x86-64.exe'

# The specialist tiers are authored. Other cast members draw from their
# everyday personality profiles and leisure schedules below.
LEVELS = {'april': 20, 'sylvanis': 20, 'crow': 20, 'camila': 18, 'rei': 13,
          'elias': 12, 'gordon': 12, 'charles': 12, 'takeo': 11, 'fox': 10,
          'thirteen': 10,  # Controlled and precise under pressure.
          'mavis': 9,      # Resourceful intelligence specialist.
          'neo': 9,        # Technical problem-solving and practiced tactical judgement.
          'paul': 8,       # Attentive and exact, sometimes slow to commit.
          'sowon': 7,      # Competitive preparation tempered by impatience.
          'kouji': 5,      # Will commit before considering the consequences.
          'somchai': 5,    # Tests opponents readily, with little patience.
          'garrett': 7}    # Has played across the board from April.


def level(who):
    if who in LEVELS:
        return LEVELS[who]
    profile = personality_types.PROFILES.get(who, {})
    traits = set(profile.get('personality_traits', ()))
    interests = set(profile.get('interests', ()))
    resident = town_residents.RESIDENTS.get(who, {})
    words = set(re.findall(r"[a-z]+", ' '.join(resident.get(key, '') for key in
                                               ('voice', 'life')).lower()))
    score = 4 + len((traits | words) & {'patient', 'observant', 'attentive', 'precise',
                                        'disciplined', 'competitive', 'thoughtful', 'perceptive'})
    score += 2 * len(traits & {'analytical', 'inventive', 'logical'})
    score += bool(interests & {'science', 'electronics', 'astronomy', 'video games'})
    if 'chess' in leisure.PREFERENCES.get(who, ()) or 'chess' in words or 'chess' in interests:
        score += 3
    return min(12, score)


def opponents(state):
    if interiors.room(state) != PLAYING_ROOM or not interiors.available(state, state['player']):
        return []
    cast = [who for who in interiors.occupants(state, PLAYING_ROOM)
            if who != state['player'] and interiors.available(state, who)]
    locals_here = [who for who in state['world'].get('npcs', ())
                   if who in town_residents.RESIDENTS or who in personality_types.PROFILES]
    return list(dict.fromkeys(cast + locals_here))


def reply(board, skill):
    command = str(ENGINE) if os.name == 'nt' else shutil.which('stockfish')
    if not command:
        raise FileNotFoundError('Install Stockfish on the system path.')
    options = {'creationflags': subprocess.CREATE_NO_WINDOW} if os.name == 'nt' else {}
    with chess.engine.SimpleEngine.popen_uci(command, timeout=5, **options) as engine:
        engine.configure({'Skill Level': skill})
        result = engine.play(board, chess.engine.Limit(time=0.12 + skill * 0.035))
        if result.move not in board.legal_moves:
            raise ValueError('Stockfish returned an invalid move.')
        return result.move


def captured_piece(board, move):
    """Inspect the position before moving, including the displaced en passant pawn."""
    if board.is_en_passant(move):
        return chess.PAWN
    return board.piece_type_at(move.to_square)


def capture_summary(pieces):
    return ', '.join(f'{pieces.count(kind)} {chess.piece_name(kind)}' +
                     ('s' if pieces.count(kind) > 1 else '')
                     for kind in (chess.QUEEN, chess.ROOK, chess.BISHOP, chess.KNIGHT, chess.PAWN)
                     if kind in pieces) or 'none'


def remember_match(state, match_id, opponent, outcome, notation, captures):
    player = state['player']
    reason = outcome.termination.name.lower().replace('_', ' ')
    winner = player if outcome.winner == chess.WHITE else opponent
    result = 'The match was drawn' if outcome.winner is None else f'{winner} won'
    text = (f'Chess match at the Chess café: {player} played White against {opponent} as Black. '
            f'{result} by {reason}. Final move: {notation}. '
            f'{player} captured: {capture_summary(captures[chess.WHITE])}. '
            f'{opponent} captured: {capture_summary(captures[chess.BLACK])}.')
    rid = memory_store.add(state, source=f'chess-match:{match_id}', text=text, owners=[player, opponent],
                     subjects=[player, opponent], kind='chess match', location='chess',
                     minute=state['world']['minute'], certainty='played firsthand', importance=3)
    record = state['memory_store']['records'][rid]
    record.setdefault('chess_result', outcome.result())
    record.setdefault('chess_details', dict(reason=reason, move=notation,
                      white=capture_summary(captures[chess.WHITE]),
                      black=capture_summary(captures[chess.BLACK])))


def saved_games(state, opponent=None):
    """Read the player's completed games in ledger order, including legacy rows."""
    ledger = state.get('memory_store', {})
    player = state['player']
    for rid in ledger.get('owners', {}).get(opponent or player, ()):
        record = ledger['records'][rid]
        if record['kind'] != 'chess match' or player not in record['owners']:
            continue
        who = next((w for w in record['owners'] if w != player), None)
        if who is None:
            continue
        result = record.get('chess_result')
        details = record.get('chess_details')
        if details is None:
            # These delimiters are from the two earlier versions of remember_match.
            text = record['text'].removeprefix(
                f'Chess match at the Chess café: {player} played White against {who} as Black. ')
            ending, _, rest = text.partition('. Final move: ')
            move, _, captures = rest.partition(f'. {player} captured: ')
            white, _, black = captures.partition(f'. {who} captured: ')
            reason = ending
            for prefix, code in ((f'{player} won by ', '1-0'), (f'{who} won by ', '0-1'),
                                 ('The match was drawn by ', '1/2-1/2')):
                if ending.startswith(prefix):
                    result = result or code
                    reason = ending[len(prefix):]
                    break
            details = dict(reason=reason, move=move, white=white, black=black.removesuffix('.'))
        yield dict(opponent=who, result=result, minute=record['minute'], text=record['text'], **details)


def totals_for(games):
    totals = {'wins': 0, 'losses': 0, 'draws': 0}
    for game in games:
        field = {'1-0': 'wins', '0-1': 'losses', '1/2-1/2': 'draws'}.get(game['result'])
        if field:
            totals[field] += 1
    return totals


def match_history(state, opponent):
    """Player-perspective totals and the three most recent shared matches."""
    games = list(saved_games(state, opponent))
    return totals_for(games), [game['text'] for game in games[-3:]]
