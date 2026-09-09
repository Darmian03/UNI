from __future__ import annotations

from dataclasses import asdict
from pathlib import Path
from typing import Any

import chess
import chess.engine

from data_generation.utils import PositionSample, StockfishConfig


def _open_engine(stockfish_path: Path, cfg: StockfishConfig) -> chess.engine.SimpleEngine:
    eng = chess.engine.SimpleEngine.popen_uci(str(stockfish_path))
    eng.configure({"Threads": int(cfg.threads)})
    return eng


def _close_engine(eng: chess.engine.SimpleEngine) -> None:
    eng.quit()


def probe_engine_id(stockfish_path: Path, cfg: StockfishConfig) -> dict[str, Any]:
    """Връща UCI идентификатора на Stockfish."""

    engine = _open_engine(stockfish_path, cfg)
    out = dict(engine.id)
    _close_engine(engine)
    return out


def stockfish_config_metadata(cfg: StockfishConfig) -> dict[str, Any]:
    return asdict(cfg)


def evaluate_sample(
    *,
    sample: PositionSample,
    stockfish_path: Path,
    cfg: StockfishConfig,
) -> dict[str, Any]:
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
