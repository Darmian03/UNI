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
    """Move-ordering key; higher values are searched first (promotion > capture > check)."""

    score = 0
    if move.promotion is not None:
        score += 300
    if board.is_capture(move):
        score += 200
    if board.gives_check(move):
        score += 50

    return (score, "")


def _ordered_moves(board: chess.Board) -> List[chess.Move]:
    """Legal moves, shuffled then sorted by the ordering key (the shuffle breaks ties)."""
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
    """Alpha-beta search; all scores are from White's perspective."""
    # Terminal positions (mate/draws) and depth cutoffs end the recursion early.
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
            if alpha >= beta:  # cutoff: no remaining move can improve this node
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
            if alpha >= beta:  # cutoff: no remaining move can improve this node
                break

    return value


def _evaluate_root_move(args: Tuple[str, str, int, Callable[[chess.Board], float]]) -> Tuple[str, float]:
    """Evaluate one root move on a fresh board; illegal moves count as an immediate mate loss."""

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
    """Pool initializer: stash the evaluator in worker-global state (spawn workers can't receive it per task)."""
    _MP_STATE["evaluator"] = evaluator


def _evaluate_root_move_mp(args: Tuple[str, str, int]) -> Tuple[str, float]:
    """Worker-side entry point; pulls the shared evaluator from _MP_STATE."""
    fen, move_uci, depth = args
    evaluator = _MP_STATE["evaluator"]
    return _evaluate_root_move((fen, move_uci, depth, evaluator))


def _is_spawnable_evaluator(evaluator: Callable[[chess.Board], float]) -> bool:
    """True if the evaluator can be pickled for a spawn pool (functions defined in __main__ cannot)."""
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
    """Alpha-beta minimax; returns (best_move, score from White's perspective).

    The root move is picked with alpha-beta pruning over ordered moves; with
    use_multiprocessing each root move is searched in a parallel worker instead.
    """

    moves = _ordered_moves(board)

    maximizing = board.turn == chess.WHITE

    if depth == 0:
        # No search left: score every root move directly with the evaluator.
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
        # Fall back to single-process when the evaluator can't be pickled for spawn.
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

    # Sequential root search; alpha/beta are carried across sibling moves.
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
