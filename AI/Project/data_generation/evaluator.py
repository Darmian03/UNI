from __future__ import annotations

from dataclasses import asdict
from pathlib import Path
from typing import Any

import chess
import chess.engine

from data_generation.utils import PositionSample, StockfishConfig


def _open_engine(stockfish_path: Path, cfg: StockfishConfig) -> chess.engine.SimpleEngine:
    """Start a Stockfish UCI engine with the given thread count."""
    eng = chess.engine.SimpleEngine.popen_uci(str(stockfish_path))
    eng.configure({"Threads": int(cfg.threads)})
    return eng


def _close_engine(eng: chess.engine.SimpleEngine) -> None:
    """Quit a Stockfish UCI engine."""
    eng.quit()


def stockfish_config_metadata(cfg: StockfishConfig) -> dict[str, Any]:
    """Serialize the config for passing across process boundaries."""
    return asdict(cfg)


def evaluate_sample(
    *,
    sample: PositionSample,
    stockfish_path: Path,
    cfg: StockfishConfig,
) -> dict[str, Any]:
    """Analyse one position with Stockfish and return its CSV row (best move + eval)."""
    eng = _open_engine(stockfish_path, cfg)
    b = chess.Board(sample.fen)
    info = eng.analyse(b, chess.engine.Limit(depth=int(cfg.depth)), multipv=1)

    mv = ""
    pv = info.get("pv") or []
    if isinstance(pv, (list, tuple)) and pv and hasattr(pv[0], "uci"):
        mv = pv[0].uci()

    cp = ""
    sc = info.get("score")
    if sc is not None:
        cp_val = sc.pov(chess.WHITE).score(mate_score=100000)
        cp = "" if cp_val is None else str(int(cp_val))

    _close_engine(eng)

    return {
        "fen": sample.fen,
        "game_phase": sample.game_phase,
        "move_number": sample.move_number,
        "best_move": mv,
        "best_eval": cp,
    }
