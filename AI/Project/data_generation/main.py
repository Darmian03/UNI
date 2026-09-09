from __future__ import annotations

import argparse
import csv
import multiprocessing as mp
import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from data_generation.evaluator import evaluate_sample, stockfish_config_metadata
from data_generation.sampler import sample_positions
import data_generation.utils as dg_utils


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--num_positions",
        required=True,
    )
    parser.add_argument(
        "--elo",
        required=True,
        choices=["low", "high"],
    )
    return parser.parse_args()


def _evaluate_one(job: tuple[int, dict, dict]) -> tuple[int, dict]:
    i, sample_dict, ctx = job

    sample = dg_utils.PositionSample(
        fen=sample_dict["fen"],
        game_phase=sample_dict["game_phase"],
        move_number=int(sample_dict["move_number"]),
    )

    row = evaluate_sample(
        sample=sample,
        stockfish_path=Path(ctx["stockfish_path"]),
        cfg=dg_utils.StockfishConfig(**ctx["stockfish_cfg"]),
    )
    return i, row


def main() -> None:
    args = _parse_args()

    num_positions = dg_utils.parse_num_positions_thousands(args.num_positions)
    elo = dg_utils.parse_elo_bucket(args.elo)

    pgn_path = dg_utils.default_pgn_path()

    stockfish_path = dg_utils.resolve_stockfish_path()

    sampling_cfg = dg_utils.SamplingConfig()

    cpu_workers = max(1, mp.cpu_count())
    stockfish_cfg = dg_utils.StockfishConfig(threads=1)

    samples, _sampling_meta = sample_positions(
        pgn_path=pgn_path,
        num_positions=num_positions,
        elo=elo,
        sampling=sampling_cfg,
    )


    out_dir = dg_utils.output_dir()
    out_dir.mkdir(parents=True, exist_ok=True)

    n_k = num_positions // 1000
    csv_path = out_dir / f"stockfish_eval_{n_k}k_{elo}_elo.csv"

    ctx = {
        "stockfish_path": str(stockfish_path),
        "stockfish_cfg": stockfish_config_metadata(stockfish_cfg),
    }

    sample_payload = [
        {
            "fen": s.fen,
            "game_phase": s.game_phase,
            "move_number": s.move_number,
        }
        for s in samples
    ]

    rows: list[dict] = [{} for _ in range(len(sample_payload))]

    with mp.Pool(processes=cpu_workers) as pool:
        jobs = [(i, sp, ctx) for i, sp in enumerate(sample_payload)]
        for i, row in pool.imap_unordered(_evaluate_one, jobs, chunksize=8):
            rows[i] = row

    fieldnames = [
        "fen",
        "game_phase",
        "move_number",
        "best_move",
        "best_eval",
    ]

    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote: {csv_path}")


if __name__ == "__main__":
    main()
