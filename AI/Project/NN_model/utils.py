from __future__ import annotations

import csv
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Literal, cast

import chess
import numpy as np

GamePhase = Literal["early", "mid", "end"]


@dataclass(frozen=True)
class DatasetConfig:
    target_scale: float = 100.0
    target_clip_cp: int = 10_000
    include_game_phase: bool = True


@dataclass(frozen=True)
class TrainConfig:
    dataset_csv: str
    epochs: int = 5
    batch_size: int = 512
    lr: float = 1e-3
    weight_decay: float = 1e-5
    val_split: float = 0.05
    seed: int = 42


def project_root() -> Path:
    """Project root directory (parent of NN_model/)."""
    return Path(__file__).resolve().parents[1]


def data_dir() -> Path:
    """Directory holding the CSV datasets."""
    return project_root() / "data"


def trained_models_dir() -> Path:
    """Directory where trained .pt models are saved."""
    return project_root() / "trained_models"


def set_seed(seed: int) -> None:
    """Seed Python, NumPy and torch RNGs for reproducibility."""
    import random

    import torch

    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)


_PIECE_TO_PLANE = {
    (chess.PAWN, chess.WHITE): 0,
    (chess.KNIGHT, chess.WHITE): 1,
    (chess.BISHOP, chess.WHITE): 2,
    (chess.ROOK, chess.WHITE): 3,
    (chess.QUEEN, chess.WHITE): 4,
    (chess.KING, chess.WHITE): 5,
    (chess.PAWN, chess.BLACK): 6,
    (chess.KNIGHT, chess.BLACK): 7,
    (chess.BISHOP, chess.BLACK): 8,
    (chess.ROOK, chess.BLACK): 9,
    (chess.QUEEN, chess.BLACK): 10,
    (chess.KING, chess.BLACK): 11,
}


def encode_board(board: chess.Board, game_phase: GamePhase | None, *, include_game_phase: bool) -> np.ndarray:
    """Encode a position into (C, 8, 8) float32 planes."""

    planes = np.zeros((12 + 1 + 4 + 1 + (3 if include_game_phase else 0), 8, 8), dtype=np.float32)

    for square, piece in board.piece_map().items():
        plane = _PIECE_TO_PLANE[(piece.piece_type, piece.color)]
        rank = chess.square_rank(square)
        file = chess.square_file(square)
        planes[plane, rank, file] = 1.0

    planes[12, :, :] = 1.0 if board.turn == chess.WHITE else 0.0

    planes[13, :, :] = 1.0 if board.has_kingside_castling_rights(chess.WHITE) else 0.0
    planes[14, :, :] = 1.0 if board.has_queenside_castling_rights(chess.WHITE) else 0.0
    planes[15, :, :] = 1.0 if board.has_kingside_castling_rights(chess.BLACK) else 0.0
    planes[16, :, :] = 1.0 if board.has_queenside_castling_rights(chess.BLACK) else 0.0

    ep = board.ep_square
    if ep is not None:
        ep_file = chess.square_file(ep)
        planes[17, :, ep_file] = 1.0

    if include_game_phase:
        phase_offset = 18
        if game_phase in ("early", "mid", "end"):
            idx = {"early": 0, "mid": 1, "end": 2}[game_phase]
            planes[phase_offset + idx, :, :] = 1.0

    return planes


def clamp_cp(cp: float, clip: int) -> float:
    """Clamp a centipawn value to [-clip, +clip] (keeps mate scores from dominating the loss)."""
    if cp > clip:
        return float(clip)
    if cp < -clip:
        return float(-clip)
    return float(cp)


def load_dataset_rows(csv_path: Path, *, dataset_cfg: DatasetConfig) -> tuple[list[str], list[GamePhase], list[float]]:
    """Load (fen, phase, target) rows from a CSV dataset."""

    fens: list[str] = []
    phases: list[GamePhase] = []
    targets: list[float] = []

    with csv_path.open("r", encoding="utf-8", newline="", errors="replace") as f:
        reader = csv.DictReader(f)
        for row in reader:
            fen = (row.get("fen") or "").strip()
            phase = (row.get("game_phase") or "").strip().lower()
            best_eval = (row.get("best_eval") or "").strip()
            if not fen or phase not in ("early", "mid", "end") or not best_eval:
                continue

            phase_t = cast(GamePhase, phase)

            cp = float(best_eval)

            cp = clamp_cp(cp, dataset_cfg.target_clip_cp)
            y = cp / float(dataset_cfg.target_scale)

            fens.append(fen)
            phases.append(phase_t)
            targets.append(y)

    return fens, phases, targets


def cpu_worker_count() -> int:
    """Number of DataLoader worker processes (all CPU cores)."""
    return max(0, os.cpu_count() or 0)
