"""Runs model-vs-model experiments and writes JSON results."""

from __future__ import annotations

import argparse
import json
import multiprocessing as mp
import os
import random
import statistics
import time
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

import chess
import chess.engine
from tqdm import tqdm

from custom_eval_engine import evaluator_white_pov
from minimax import minimax
from stockfish_engine import find_stockfish_exe


MAX_PLIES = 100
_TERMINATION_REASONS = {
    "ply_limit",
    "threefold_repetition",
    "fifty_move_rule",
    "insufficient_material",
}

PROJECT_ROOT = Path(__file__).resolve().parent
RESULTS_DIR = PROJECT_ROOT / "results"
TRAINED_MODELS_DIR = PROJECT_ROOT / "trained_models"


SUPPORTED_MODEL_TYPES = {"stockfish", "nn", "custom"}


@dataclass(frozen=True)
class Model:
    kind: str
    depth: int
    model_file: str | None = None

    def normalized_kind(self) -> str:
        return self.kind.strip().lower()

    def label(self) -> str:
        k = self.normalized_kind()
        if k == "nn" and self.model_file:
            return f"{k.upper()}({Path(self.model_file).stem})@d{self.depth}"
        return f"{k.upper()}@d{self.depth}"


@dataclass(frozen=True)
class Config:
    num_games: int
    seed: int
    model_a: Model
    model_b: Model
    num_workers: int | None = None
    max_plies: int = MAX_PLIES
    random_opening: bool = True
    random_opening_min_plies: int = 2
    random_opening_max_plies: int = 4
    device: str = "auto"


@dataclass
class Result:
    winner: str
    plies: int
    term_reason: str

    a_move_time_s: float
    b_move_time_s: float
    a_moves: int
    b_moves: int

    a_game_quality: float
    b_game_quality: float

    a_error_counts: dict[str, int]
    b_error_counts: dict[str, int]


class StockfishSession:
    """Stockfish UCI wrapper used in experiments."""

    def __init__(self, *, threads: int = 1):
        exe = find_stockfish_exe()
        self._engine = chess.engine.SimpleEngine.popen_uci(str(exe))
        self._engine.configure({"Threads": int(max(1, threads))})

    def close(self) -> None:
        self._engine.quit()

    def best_move_and_eval_white_cp(self, board: chess.Board, *, depth: int) -> tuple[chess.Move, float]:
        info = self._engine.analyse(board, chess.engine.Limit(depth=int(depth)))
        pv = info.get("pv") or []
        if pv:
            mv = pv[0]
        else:
            mv = self._engine.play(board, chess.engine.Limit(depth=int(depth))).move

        score = info.get("score")
        if score is None:
            cp_white = 0.0
        else:
            cp_white = float(score.pov(chess.WHITE).score(mate_score=100000) or 0)
        return mv, cp_white

    def eval_move_white_cp(self, board: chess.Board, move: chess.Move, *, depth: int) -> float:
        info = self._engine.analyse(board, chess.engine.Limit(depth=int(depth)), root_moves=[move])
        score = info.get("score")
        if score is None:
            return 0.0
        return float(score.pov(chess.WHITE).score(mate_score=100000) or 0)

def _phase_for(board: chess.Board) -> str:
    """Return a coarse game-phase label for optional NN conditioning."""
    material = 0
    material += 1 * int(board.pawns).bit_count()
    material += 3 * int(board.knights).bit_count()
    material += 3 * int(board.bishops).bit_count()
    material += 5 * int(board.rooks).bit_count()
    material += 9 * int(board.queens).bit_count()

    if board.fullmove_number < 10:
        return "early"
    if board.fullmove_number <= 30 and material > 20:
        return "mid"
    return "end"


class Player:
    def choose_move(self, _board: chess.Board) -> chess.Move:
        return chess.Move.null()


class StockfishPlayer(Player):
    def __init__(self, *, session: StockfishSession, depth: int):
        self._session = session
        self._depth = int(depth)

    def choose_move(self, board: chess.Board) -> chess.Move:
        mv, _ = self._session.best_move_and_eval_white_cp(board, depth=self._depth)
        return mv


class MinimaxPlayer(Player):
    def __init__(
        self,
        *,
        depth: int,
        evaluator_white: Callable[[chess.Board], float],
    ):
        self._depth = int(depth)
        self._evaluator = evaluator_white

    def choose_move(self, board: chess.Board) -> chess.Move:
        mv, _ = minimax(board, depth=self._depth, evaluator=self._evaluator, use_multiprocessing=False)
        return mv

_ERROR_CATEGORIES = ("excellent", "good", "inaccuracy", "mistake", "blunder")


def _delta_to_quality_and_bucket(delta_cp: float) -> tuple[float, str]:
    """Map centipawn loss to a quality score and bucket."""

    d = float(abs(delta_cp))

    if d <= 20.0:
        return 1.0, "excellent"
    if d <= 50.0:
        return 0.9, "good"
    if d <= 100.0:
        return 0.75, "inaccuracy"
    if d <= 300.0:
        return 0.4, "mistake"
    return 0.1, "blunder"


def _harmonic_mean(values: list[float]) -> float:
    """Aggregate per-move quality into one per-game score."""

    if not values:
        return 0.0
    return float(statistics.harmonic_mean(values))

_WORKER: dict[str, Any] = {}


def _build_evaluator_for_spec(spec: Model, *, device: str = "auto") -> Callable[[chess.Board], float]:
    k = spec.normalized_kind()

    if k == "custom":
        return evaluator_white_pov

    if k == "nn":
        from NN_model.model import NeuralNetworkEvaluator

        model_path = TRAINED_MODELS_DIR / str(spec.model_file)

        nn_eval = NeuralNetworkEvaluator(model_path, device=device)

        def eval_white_nn(board: chess.Board) -> float:
            return float(nn_eval.evaluate(board, _phase_for(board)))

        return eval_white_nn

    return evaluator_white_pov


def _worker_init(cfg_dict: dict[str, Any]) -> None:
    """Initializer for each worker process."""

    import atexit

    cfg = Config(
        num_games=int(cfg_dict["num_games"]),
        seed=int(cfg_dict["seed"]),
        model_a=Model(**cfg_dict["model_a"]),
        model_b=Model(**cfg_dict["model_b"]),
        num_workers=(int(cfg_dict["num_workers"]) if cfg_dict.get("num_workers") is not None else None),
        max_plies=int(cfg_dict.get("max_plies", MAX_PLIES)),
        random_opening=bool(cfg_dict.get("random_opening", True)),
        random_opening_min_plies=int(cfg_dict.get("random_opening_min_plies", 2)),
        random_opening_max_plies=int(cfg_dict.get("random_opening_max_plies", 4)),
        device=str(cfg_dict.get("device", "auto")),
    )

    oracle = StockfishSession(threads=1)

    stockfish_session = None
    if cfg.model_a.normalized_kind() == "stockfish" or cfg.model_b.normalized_kind() == "stockfish":
        stockfish_session = StockfishSession(threads=1)

    def build_player(spec: Model) -> Player:
        kind = spec.normalized_kind()
        if kind == "stockfish":
            assert stockfish_session is not None
            return StockfishPlayer(session=stockfish_session, depth=spec.depth)
        if kind in ("nn", "custom"):
            evaluator = _build_evaluator_for_spec(spec, device=cfg.device)
            return MinimaxPlayer(depth=spec.depth, evaluator_white=evaluator)
        return MinimaxPlayer(depth=spec.depth, evaluator_white=evaluator_white_pov)

    _WORKER.clear()
    _WORKER["cfg"] = cfg
    _WORKER["oracle"] = oracle
    _WORKER["stockfish_session"] = stockfish_session
    _WORKER["player_a"] = build_player(cfg.model_a)
    _WORKER["player_b"] = build_player(cfg.model_b)

    atexit.register(_worker_close)


def _worker_close() -> None:
    oracle: StockfishSession | None = _WORKER.get("oracle")
    if oracle is not None:
        oracle.close()
    sf: StockfishSession | None = _WORKER.get("stockfish_session")
    if sf is not None:
        sf.close()


def _play_one_game(game_index: int) -> Result:
    cfg: Config = _WORKER["cfg"]
    oracle: StockfishSession = _WORKER["oracle"]
    player_a: Player = _WORKER["player_a"]
    player_b: Player = _WORKER["player_b"]

    per_game_seed = int(cfg.seed) + int(game_index)
    random.seed(per_game_seed)

    rng = random.Random(per_game_seed)

    board = chess.Board()

    max_plies = int(cfg.max_plies)
    if bool(cfg.random_opening):
        lo = int(cfg.random_opening_min_plies)
        hi = int(cfg.random_opening_max_plies)
        lo = max(0, lo)
        hi = max(lo, hi)
        n_plies = rng.randint(lo, hi)
        for _ in range(n_plies):
            if board.is_game_over(claim_draw=True):
                break
            moves = list(board.legal_moves)
            if not moves:
                break
            board.push(rng.choice(moves))

    a_is_white = (int(game_index) % 2 == 0)

    a_time = 0.0
    b_time = 0.0
    a_moves = 0
    b_moves = 0

    a_move_qualities: list[float] = []
    b_move_qualities: list[float] = []
    a_error_counts: dict[str, int] = {k: 0 for k in _ERROR_CATEGORIES}
    b_error_counts: dict[str, int] = {k: 0 for k in _ERROR_CATEGORIES}

    def winner_for_color(winning_color: chess.Color) -> str:
        if winning_color == chess.WHITE:
            return "A" if a_is_white else "B"
        return "B" if a_is_white else "A"
    def strict_draw_reason(b: chess.Board) -> str | None:
        if b.is_insufficient_material():
            return "insufficient_material"
        if b.can_claim_threefold_repetition():
            return "threefold_repetition"
        if b.can_claim_fifty_moves():
            return "fifty_move_rule"
        return None

    while True:
        if len(board.move_stack) >= max_plies:
            return Result(
                winner="draw",
                plies=len(board.move_stack),
                term_reason="ply_limit",
                a_move_time_s=a_time,
                b_move_time_s=b_time,
                a_moves=a_moves,
                b_moves=b_moves,
                a_game_quality=_harmonic_mean(a_move_qualities),
                b_game_quality=_harmonic_mean(b_move_qualities),
                a_error_counts=a_error_counts,
                b_error_counts=b_error_counts,
            )

        dr = strict_draw_reason(board)
        if dr is not None:
            return Result(
                winner="draw",
                plies=len(board.move_stack),
                term_reason=dr,
                a_move_time_s=a_time,
                b_move_time_s=b_time,
                a_moves=a_moves,
                b_moves=b_moves,
                a_game_quality=_harmonic_mean(a_move_qualities),
                b_game_quality=_harmonic_mean(b_move_qualities),
                a_error_counts=a_error_counts,
                b_error_counts=b_error_counts,
            )

        if board.is_checkmate():
            winning_color = chess.BLACK if board.turn == chess.WHITE else chess.WHITE
            return Result(
                winner=winner_for_color(winning_color),
                plies=len(board.move_stack),
                term_reason="checkmate",
                a_move_time_s=a_time,
                b_move_time_s=b_time,
                a_moves=a_moves,
                b_moves=b_moves,
                a_game_quality=_harmonic_mean(a_move_qualities),
                b_game_quality=_harmonic_mean(b_move_qualities),
                a_error_counts=a_error_counts,
                b_error_counts=b_error_counts,
            )

        if board.is_stalemate():
            return Result(
                winner="draw",
                plies=len(board.move_stack),
                term_reason="stalemate",
                a_move_time_s=a_time,
                b_move_time_s=b_time,
                a_moves=a_moves,
                b_moves=b_moves,
                a_game_quality=_harmonic_mean(a_move_qualities),
                b_game_quality=_harmonic_mean(b_move_qualities),
                a_error_counts=a_error_counts,
                b_error_counts=b_error_counts,
            )

        if board.turn == chess.WHITE:
            current_is_a = a_is_white
        else:
            current_is_a = not a_is_white

        current_player = player_a if current_is_a else player_b

        t0 = time.perf_counter()
        move = current_player.choose_move(board)
        dt = time.perf_counter() - t0

        if current_is_a:
            a_time += dt
            a_moves += 1
        else:
            b_time += dt
            b_moves += 1

        _best_move, best_cp = oracle.best_move_and_eval_white_cp(board, depth=16)
        played_cp = oracle.eval_move_white_cp(board, move, depth=16)
        delta_cp = abs(float(best_cp) - float(played_cp))
        q, bucket = _delta_to_quality_and_bucket(delta_cp)

        if current_is_a:
            a_move_qualities.append(float(q))
            a_error_counts[bucket] = int(a_error_counts.get(bucket, 0)) + 1
        else:
            b_move_qualities.append(float(q))
            b_error_counts[bucket] = int(b_error_counts.get(bucket, 0)) + 1

        if move not in board.legal_moves:
            winner = "B" if current_is_a else "A"
            return Result(
                winner=winner,
                plies=len(board.move_stack),
                term_reason="illegal_move",
                a_move_time_s=a_time,
                b_move_time_s=b_time,
                a_moves=a_moves,
                b_moves=b_moves,
                a_game_quality=_harmonic_mean(a_move_qualities),
                b_game_quality=_harmonic_mean(b_move_qualities),
                a_error_counts=a_error_counts,
                b_error_counts=b_error_counts,
            )

        board.push(move)


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()

    p.add_argument("--num_games", type=int, required=True)
    p.add_argument("--seed", type=int, default=42)

    p.add_argument("--model_a", type=str, required=True)
    p.add_argument("--model_a_depth", type=int, required=True)
    p.add_argument("--model_a_model_file", type=str, default=None)

    p.add_argument("--model_b", type=str, required=True)
    p.add_argument("--model_b_depth", type=int, required=True)
    p.add_argument("--model_b_model_file", type=str, default=None)

    p.add_argument(
        "--num_workers",
        type=int,
        default=None,
    )

    p.add_argument(
        "--max_plies",
        type=int,
        default=MAX_PLIES,
    )

    p.add_argument(
        "--random_opening",
        action=argparse.BooleanOptionalAction,
        default=True,
    )

    p.add_argument(
        "--device",
        type=str,
        default="auto",
        help="Device for NN evaluation: 'auto', 'cpu', 'cuda' or 'cuda:<n>' (e.g. cuda:0). "
             "'auto' uses CUDA when available.",
    )

    return p.parse_args()


def _validate_spec(_spec: Model, *, _which: str) -> None:
    return


def _result_filename(cfg: Config) -> str:
    def tag(spec: Model) -> str:
        k = spec.normalized_kind()
        base = f"{k}_d{int(spec.depth)}"
        if k == "nn" and spec.model_file:
            base += f"_{Path(spec.model_file).stem}"
        return base

    ts = time.strftime("%Y%m%d_%H%M%S")
    return f"exp_{tag(cfg.model_a)}__vs__{tag(cfg.model_b)}__n{cfg.num_games}__seed{cfg.seed}__{ts}.json"


def run_experiment(cfg: Config) -> dict[str, Any]:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    cfg_dict = {
        "num_games": int(cfg.num_games),
        "seed": int(cfg.seed),
        "model_a": asdict(cfg.model_a),
        "model_b": asdict(cfg.model_b),
        "num_workers": (int(cfg.num_workers) if cfg.num_workers is not None else None),
        "max_plies": int(cfg.max_plies),
        "random_opening": bool(cfg.random_opening),
        "random_opening_min_plies": int(cfg.random_opening_min_plies),
        "random_opening_max_plies": int(cfg.random_opening_max_plies),
        "device": str(cfg.device),
    }

    num_games = int(cfg.num_games)

    ctx = mp.get_context("spawn")
    if cfg.num_workers is None:
        num_workers = max(1, min(int(num_games), os.cpu_count() or 1))
    else:
        num_workers = max(1, min(int(num_games), int(cfg.num_workers)))

    wins_a = 0
    wins_b = 0
    draws = 0
    terminations = 0

    plies_total = 0

    a_time_total = 0.0
    b_time_total = 0.0
    a_moves_total = 0
    b_moves_total = 0

    a_quality_sum = 0.0
    b_quality_sum = 0.0

    a_err_totals: dict[str, int] = {k: 0 for k in _ERROR_CATEGORIES}
    b_err_totals: dict[str, int] = {k: 0 for k in _ERROR_CATEGORIES}

    term_counts: dict[str, int] = {}

    tasks = list(range(num_games))

    with ctx.Pool(processes=num_workers, initializer=_worker_init, initargs=(cfg_dict,)) as pool:
        it = pool.imap_unordered(_play_one_game, tasks, chunksize=1)

        for gr in tqdm(it, total=num_games, desc="Games", unit="game"):
            if gr.winner == "A":
                wins_a += 1
            elif gr.winner == "B":
                wins_b += 1
            else:
                if gr.term_reason in _TERMINATION_REASONS:
                    terminations += 1
                else:
                    draws += 1

            plies_total += int(gr.plies)

            a_time_total += float(gr.a_move_time_s)
            b_time_total += float(gr.b_move_time_s)
            a_moves_total += int(gr.a_moves)
            b_moves_total += int(gr.b_moves)

            a_quality_sum += float(gr.a_game_quality)
            b_quality_sum += float(gr.b_game_quality)

            for k in _ERROR_CATEGORIES:
                a_err_totals[k] = int(a_err_totals.get(k, 0)) + int(gr.a_error_counts.get(k, 0))
                b_err_totals[k] = int(b_err_totals.get(k, 0)) + int(gr.b_error_counts.get(k, 0))

            term_counts[gr.term_reason] = int(term_counts.get(gr.term_reason, 0)) + 1

    termination_reason: str | None = None
    if terminations > 0:
        most_common = None
        most_common_count = -1
        for reason, cnt in term_counts.items():
            if reason not in _TERMINATION_REASONS:
                continue
            if int(cnt) > most_common_count:
                most_common = str(reason)
                most_common_count = int(cnt)
        termination_reason = most_common

    avg_plies = float(plies_total) / float(num_games)

    avg_move_time_a = (a_time_total / float(a_moves_total)) if a_moves_total > 0 else 0.0
    avg_move_time_b = (b_time_total / float(b_moves_total)) if b_moves_total > 0 else 0.0

    quality_a_final = (a_quality_sum / float(num_games)) * 10.0
    quality_b_final = (b_quality_sum / float(num_games)) * 10.0
    quality_a_final = float(max(0.0, min(10.0, quality_a_final)))
    quality_b_final = float(max(0.0, min(10.0, quality_b_final)))

    def build_stats(totals: dict[str, int], total_moves: int) -> dict[str, dict[str, float]]:
        out: dict[str, dict[str, float]] = {}
        for k in _ERROR_CATEGORIES:
            total_k = int(totals.get(k, 0))
            avg_per_game = float(total_k) / float(num_games)
            pct = (float(total_k) / float(total_moves) * 100.0) if total_moves > 0 else 0.0
            out[k] = {
                "average_per_game": avg_per_game,
                "percentage": pct,
            }
        return out

    move_error_stats = {
        "model_a": build_stats(a_err_totals, a_moves_total),
        "model_b": build_stats(b_err_totals, b_moves_total),
    }

    result: dict[str, Any] = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "num_games": int(num_games),
        "seed": int(cfg.seed),
        "model_a": {"type": cfg.model_a.kind, "depth": int(cfg.model_a.depth), "model_file": cfg.model_a.model_file},
        "model_b": {"type": cfg.model_b.kind, "depth": int(cfg.model_b.depth), "model_file": cfg.model_b.model_file},
        "wins_model_a": int(wins_a),
        "wins_model_b": int(wins_b),
        "draws": int(draws),
        "terminations": int(terminations),
        "termination_reason": termination_reason,
        "avg_plies_per_game": avg_plies,
        "avg_move_time_seconds": {"model_a": avg_move_time_a, "model_b": avg_move_time_b},
        "final_score": {"model_a": quality_a_final, "model_b": quality_b_final},
        "move_error_stats": move_error_stats,
        "termination_reasons": term_counts,
    }

    out_path = RESULTS_DIR / _result_filename(cfg)
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    print("Saved results:", out_path)
    return result


def main() -> None:
    args = _parse_args()

    cfg = Config(
        num_games=int(args.num_games),
        seed=int(args.seed),
        model_a=Model(kind=str(args.model_a), depth=int(args.model_a_depth), model_file=args.model_a_model_file),
        model_b=Model(kind=str(args.model_b), depth=int(args.model_b_depth), model_file=args.model_b_model_file),
        num_workers=(int(args.num_workers) if args.num_workers is not None else None),
        max_plies=int(args.max_plies),
        random_opening=bool(getattr(args, "random_opening", True)),
        device=str(args.device),
    )

    run_experiment(cfg)


if __name__ == "__main__":
    main()
