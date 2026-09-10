from __future__ import annotations

from collections.abc import Iterator
from dataclasses import asdict
from pathlib import Path
from typing import Any

import chess
import chess.pgn

from data_generation.utils import EloBucket, GamePhase, PositionSample, SamplingConfig, game_matches_elo


def _material_cp(board: chess.Board) -> int:
    """Total material in pawn-equivalent units (both sides)."""
    values = {
        chess.PAWN: 1,
        chess.KNIGHT: 3,
        chess.BISHOP: 3,
        chess.ROOK: 5,
        chess.QUEEN: 9,
    }
    total = 0
    for piece_type, value in values.items():
        total += value * len(board.pieces(piece_type, chess.WHITE))
        total += value * len(board.pieces(piece_type, chess.BLACK))
    return total


def _is_low_material(board: chess.Board) -> bool:
    """True when the position has little material left (endgame-ish)."""
    return _material_cp(board) <= 20


def _phase_for(board: chess.Board, ply: int) -> GamePhase | None:
    """Coarse game-phase label for a position, or None if it should be skipped."""
    if ply <= 8:
        return None

    if 9 <= ply <= 17:
        return "early"

    if 10 <= board.fullmove_number <= 30:
        return "mid"

    if board.fullmove_number > 30 or _is_low_material(board):
        return "end"

    return None


def _iter_games(pgn_path: Path) -> Iterator[chess.pgn.Game]:
    """Yield games from a PGN file."""
    with pgn_path.open("r", encoding="utf-8", errors="replace") as f:
        while True:
            game = chess.pgn.read_game(f)
            if game is None:
                break
            yield game


def _target_counts(num_positions: int, sampling: SamplingConfig) -> dict[GamePhase, int]:
    """Per-phase sample counts from the configured ratios."""
    early = int(round(num_positions * sampling.early_ratio))
    mid = int(round(num_positions * sampling.mid_ratio))
    end = num_positions - early - mid
    if end < 0:
        end = 0
        mid = max(0, num_positions - early)
    return {"early": early, "mid": mid, "end": end}


def sample_positions(
    *,
    pgn_path: Path,
    num_positions: int,
    elo: EloBucket,
    sampling: SamplingConfig,
) -> tuple[list[PositionSample], dict[str, Any]]:
    """Sample positions from PGN games."""

    targets = _target_counts(num_positions, sampling)
    counts: dict[GamePhase, int] = {"early": 0, "mid": 0, "end": 0}

    seen_fens: set[str] = set()
    samples: list[PositionSample] = []

    for game in _iter_games(pgn_path):
        if not game_matches_elo(game.headers, elo):
            continue

        board = game.board()
        moves = list(game.mainline_moves())
        if len(moves) <= 9:
            continue

        for ply_index, move in enumerate(moves[:-1], start=1):
            if move not in board.legal_moves:
                break
            board.push(move)

            phase = _phase_for(board, ply_index)
            if phase is None:
                continue

            if counts[phase] >= targets[phase]:
                continue

            fen = board.fen()
            if fen in seen_fens:
                continue

            seen_fens.add(fen)
            samples.append(
                PositionSample(
                    fen=fen,
                    game_phase=phase,
                    move_number=board.fullmove_number,
                )
            )
            counts[phase] += 1

            if len(samples) >= num_positions:
                break

        if len(samples) >= num_positions:
            break

    return samples, {
        "sampling": asdict(sampling),
        "targets": targets,
        "achieved": counts,
        "unique_fens": len(seen_fens),
    }
