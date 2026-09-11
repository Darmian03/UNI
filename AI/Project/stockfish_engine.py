from __future__ import annotations

import os
import shutil
from pathlib import Path

import chess
import chess.engine


def find_stockfish_exe() -> Path:
    """Locate the Stockfish executable (cross-platform).

    Resolution order: STOCKFISH_PATH env var > PATH > well-known install
    locations > glob scan of common dirs. Raises FileNotFoundError with an
    install hint if nothing is found, so callers fail fast on a bogus path.
    """
    env = os.environ.get("STOCKFISH_PATH")
    if env:
        p = Path(env).expanduser()
        if p.is_file():
            return p
        raise FileNotFoundError(
            f"STOCKFISH_PATH is set to {p!s}, but that file does not exist."
        )

    on_path = shutil.which("stockfish") or shutil.which("stockfish.exe")
    if on_path:
        return Path(on_path)

    home = Path.home()
    candidates = [
        # Linux (apt/brew/manual) and macOS
        Path("/usr/games/stockfish"),
        Path("/usr/local/bin/stockfish"),
        Path("/usr/bin/stockfish"),
        home / "bin" / "stockfish",
        Path("/opt/homebrew/bin/stockfish"),
        # Windows
        Path(r"C:\Program Files\stockfish\stockfish.exe"),
        Path(r"C:\Program Files\Stockfish\stockfish.exe"),
        Path(r"C:\stockfish\stockfish.exe"),
    ]

    for p in candidates:
        if p.is_file():
            return p

    # Last resort: scan a few common directories for any stockfish binary.
    search_dirs = [
        home / "bin",
        Path("/usr/local/bin"),
        Path(r"C:\Program Files\stockfish"),
        Path(r"C:\Program Files\Stockfish"),
    ]
    patterns = ["stockfish*.exe"] if os.name == "nt" else ["stockfish*"]
    for d in search_dirs:
        if not d.is_dir():
            continue
        for pattern in patterns:
            matches = sorted(
                m for m in d.glob(pattern) if m.is_file() and os.access(m, os.X_OK)
            )
            if matches:
                return matches[0]

    raise FileNotFoundError(
        "Could not find a Stockfish executable. Install it (e.g. 'sudo apt install stockfish', "
        "'brew install stockfish', or download from https://stockfishchess.org/download/) "
        "and either put it on PATH or set the STOCKFISH_PATH environment variable."
    )


def evaluate_board(
    board: chess.Board,
    *,
    depth: int = 12,
    threads: int = 1,
    stockfish_path: Path | None = None,
) -> tuple[chess.Move, float]:
    """Analyse a board with Stockfish; returns (best_move, centipawn score from White's POV)."""
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
