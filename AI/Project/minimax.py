from __future__ import annotations

import os
import multiprocessing as mp
import random
from typing import Callable, Dict, List, Optional, Tuple

import chess


MATE_VALUE = float("inf")

_MP_STATE: Dict[str, Optional[Callable[[chess.Board], float]]] = {"evaluator": None}


def _terminal_eval(board: chess.Board) -> Optional[float]:
    """Terminal score from White's perspective, or None."""

    if board.is_checkmate():
        return -MATE_VALUE if board.turn == chess.WHITE else MATE_VALUE

    if board.is_stalemate() or board.is_insufficient_material():
        return 0.0

    if board.halfmove_clock >= 100 and board.can_claim_fifty_moves():
        return 0.0

    if len(board.move_stack) >= 4 and board.can_claim_threefold_repetition():
        return 0.0

    return None


def _move_ordering_key(board: chess.Board, move: chess.Move) -> Tuple[int, str]:
    """Higher is better."""

    score = 0
    if move.promotion is not None:
        score += 300
    if board.is_capture(move):
        score += 200
    if board.gives_check(move):
        score += 50

    return (score, "")


def _ordered_moves(board: chess.Board) -> List[chess.Move]:
    moves = list(board.legal_moves)
    random.shuffle(moves)
    moves.sort(key=lambda m: _move_ordering_key(board, m), reverse=True)
    return moves


def _alphabeta(
    board: chess.Board,
    depth: int,
    alpha: float,
    beta: float,
    evaluator: Callable[[chess.Board], float],
) -> float:
    term = _terminal_eval(board)
    if term is not None:
        return term

    if depth <= 0:
        return float(evaluator(board))

    maximizing = board.turn == chess.WHITE

    if maximizing:
        value = -MATE_VALUE
        for move in _ordered_moves(board):
            board.push(move)
            score = _alphabeta(board, depth - 1, alpha, beta, evaluator)
            board.pop()

            if score > value:
                value = score
            if value > alpha:
                alpha = value
            if alpha >= beta:
                break
    else:
        value = MATE_VALUE
        for move in _ordered_moves(board):
            board.push(move)
            score = _alphabeta(board, depth - 1, alpha, beta, evaluator)
            board.pop()

            if score < value:
                value = score
            if value < beta:
                beta = value
            if alpha >= beta:
                break

    return value


def _evaluate_root_move(args: Tuple[str, str, int, Callable[[chess.Board], float]]) -> Tuple[str, float]:
    """Evaluate a root move in a fresh board."""

    fen, move_uci, depth, evaluator = args
    board = chess.Board(fen)
    move = chess.Move.from_uci(move_uci)
    if move not in board.legal_moves:
        return (move_uci, -MATE_VALUE if board.turn == chess.WHITE else MATE_VALUE)

    board.push(move)
    score = _alphabeta(board, depth, -MATE_VALUE, MATE_VALUE, evaluator)
    board.pop()
    return (move_uci, score)


def _mp_init(evaluator: Callable[[chess.Board], float]) -> None:
    _MP_STATE["evaluator"] = evaluator


def _evaluate_root_move_mp(args: Tuple[str, str, int]) -> Tuple[str, float]:
    fen, move_uci, depth = args
    evaluator = _MP_STATE["evaluator"]
    return _evaluate_root_move((fen, move_uci, depth, evaluator))


def _is_spawnable_evaluator(evaluator: Callable[[chess.Board], float]) -> bool:
    mod = getattr(evaluator, "__module__", None)
    if mod == "__main__":
        return False
    return True


def minimax(
    board: chess.Board,
    depth: int,
    evaluator: Callable[[chess.Board], float],
    use_multiprocessing: bool = False,
    num_processes: Optional[int] = None,
) -> Tuple[chess.Move, float]:
    """Алфа-бета minimax: връща най-добрия ход и оценка."""

    moves = _ordered_moves(board)

    maximizing = board.turn == chess.WHITE

    if depth == 0:
        best_move = moves[0]
        best_eval = -MATE_VALUE if maximizing else MATE_VALUE
        for move in moves:
            board.push(move)
            score = float(evaluator(board))
            board.pop()
            if maximizing:
                if score > best_eval:
                    best_eval = score
                    best_move = move
            else:
                if score < best_eval:
                    best_eval = score
                    best_move = move
        return best_move, float(best_eval)

    if use_multiprocessing:
        if not _is_spawnable_evaluator(evaluator):
            use_multiprocessing = False
        else:
            ctx = mp.get_context("spawn")
            processes = num_processes if num_processes is not None else max(1, os.cpu_count() or 1)

            fen = board.fen()
            tasks = [(fen, m.uci(), depth - 1) for m in moves]

            results: dict[str, float] = {}
            with ctx.Pool(processes=processes, initializer=_mp_init, initargs=(evaluator,)) as pool:
                for move_uci, score in pool.imap_unordered(_evaluate_root_move_mp, tasks, chunksize=1):
                    results[move_uci] = score

            best_move = moves[0]
            best_eval = -MATE_VALUE if maximizing else MATE_VALUE
            for m in moves:
                score = results.get(m.uci())
                if score is None:
                    continue
                if maximizing:
                    if score > best_eval:
                        best_eval = score
                        best_move = m
                else:
                    if score < best_eval:
                        best_eval = score
                        best_move = m

            return best_move, best_eval

    best_move = moves[0]
    best_eval = -MATE_VALUE if maximizing else MATE_VALUE

    alpha = -MATE_VALUE
    beta = MATE_VALUE

    for move in moves:
        board.push(move)
        score = _alphabeta(board, depth - 1, alpha, beta, evaluator)
        board.pop()

        if maximizing:
            if score > best_eval:
                best_eval = score
                best_move = move
            if best_eval > alpha:
                alpha = best_eval
        else:
            if score < best_eval:
                best_eval = score
                best_move = move
            if best_eval < beta:
                beta = best_eval

        if alpha >= beta:
            break

    return best_move, best_eval
