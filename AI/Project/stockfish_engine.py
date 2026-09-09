from __future__ import annotations

import os
from pathlib import Path

import chess
import chess.engine


def find_stockfish_exe() -> Path:
    env = os.environ.get("STOCKFISH_PATH")
    if env:
        return Path(env).expanduser()

    candidates = [
        Path(r"C:\\Program Files\\stockfish\\stockfish.exe"),
        Path(r"C:\\Program Files\\Stockfish\\stockfish.exe"),
        Path(r"C:\\stockfish\\stockfish.exe"),
        Path(r"C:\\Program Files\\stockfish"),
    ]

    for p in candidates:
        if p.is_file():
            return p
        if p.is_dir():
            exes = sorted(p.glob("stockfish*.exe"))
            if exes:
                return exes[0]

    return candidates[0]


def evaluate_board(
    board: chess.Board,
    *,
    depth: int = 12,
    threads: int = 1,
    stockfish_path: Path | None = None,
) -> tuple[chess.Move, float]:
    exe = stockfish_path or find_stockfish_exe()
    eng = chess.engine.SimpleEngine.popen_uci(str(exe))
    eng.configure({"Threads": int(max(1, threads))})

    info = eng.analyse(board, chess.engine.Limit(depth=int(depth)))
    score = info.get("score")
    cp_white = 0.0
    if score is not None:
        cp_white = float(score.pov(chess.WHITE).score(mate_score=100000) or 0)

    pv = info.get("pv") or []
    best_move = pv[0] if pv else eng.play(board, chess.engine.Limit(depth=int(depth))).move

    eng.quit()
    return best_move, cp_white
