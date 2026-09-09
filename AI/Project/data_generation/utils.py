from __future__ import annotations

import datetime as _dt
import os
import platform
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal, cast

EloBucket = Literal["low", "high"]
GamePhase = Literal["early", "mid", "end"]

LOW_ELO_MAX = 1600
HIGH_ELO_MIN = 2000


@dataclass(frozen=True)
class StockfishConfig:
    depth: int = 12
    multipv: int = 1
    threads: int = max(1, (os.cpu_count() or 1))


@dataclass(frozen=True)
class SamplingConfig:
    early_ratio: float = 0.30
    mid_ratio: float = 0.50
    end_ratio: float = 0.20


@dataclass(frozen=True)
class PositionSample:
    fen: str
    game_phase: GamePhase
    move_number: int


def project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def default_pgn_path() -> Path:
    return project_root() / "data" / "games.pgn"


def output_dir() -> Path:
    return project_root() / "data"


def iso_utc_now() -> str:
    return _dt.datetime.now(tz=_dt.timezone.utc).replace(microsecond=0).isoformat()


def parse_elo_bucket(value: str) -> EloBucket:
    v = value.strip().lower()
    return cast(EloBucket, v)


def parse_num_positions_thousands(value: str) -> int:
    return int(value) * 1000


def safe_int(value: Any) -> int | None:
    if value is None:
        return None
    s = str(value).strip()
    if not s:
        return None
    return int(float(s))


def game_matches_elo(headers: dict[str, Any], bucket: EloBucket) -> bool:
    white_elo = safe_int(headers.get("WhiteElo"))
    black_elo = safe_int(headers.get("BlackElo"))
    if white_elo is None or black_elo is None:
        return False

    lo = min(white_elo, black_elo)
    hi = max(white_elo, black_elo)

    if bucket == "low":
        return hi <= LOW_ELO_MAX
    return lo >= HIGH_ELO_MIN


def resolve_stockfish_path() -> Path:
    """Resolve Stockfish executable path."""

    env = os.environ.get("STOCKFISH_PATH")
    if env:
        p = Path(env).expanduser()
        if p.exists():
            return p

    default = Path(r"C:\Program Files\stockfish")
    if default.is_file():
        return default

    if default.is_dir():
        matches = sorted(default.glob("stockfish*.exe"))
        if matches:
            return matches[0]
    return default


def environment_metadata() -> dict[str, Any]:
    return {
        "platform": platform.platform(),
        "python": platform.python_version(),
        "cpu_count": os.cpu_count(),
    }
