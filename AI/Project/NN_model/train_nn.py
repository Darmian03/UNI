from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path

if __package__ in (None, ""):
    # Allow running directly as `python NN_model/train_nn.py` from the project root.
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import chess
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset
from tqdm import tqdm

from NN_model.model import NNEvalNet, input_channels, resolve_device
from NN_model.utils import (
    DatasetConfig,
    TrainConfig,
    cpu_worker_count,
    data_dir,
    load_dataset_rows,
    set_seed,
    trained_models_dir,
)


class ChessEvalDataset(Dataset):
    """Maps (fen, phase) rows to encoded board tensors and centipawn targets."""

    def __init__(self, fens: list[str], phases: list[str], targets: list[float], *, dataset_cfg: DatasetConfig):
        self.fens = fens
        self.phases = phases
        self.targets = targets
        self.dataset_cfg = dataset_cfg

    def __len__(self) -> int:
        return len(self.fens)

    def __getitem__(self, idx: int):
        from NN_model.utils import encode_board

        fen = self.fens[idx]
        phase = self.phases[idx]
        board = chess.Board(fen)
        x = encode_board(board, phase, include_game_phase=self.dataset_cfg.include_game_phase)
        y = float(self.targets[idx])
        return torch.from_numpy(x), torch.tensor(y, dtype=torch.float32)


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--dataset", required=True)
    p.add_argument(
        "--device",
        type=str,
        default="auto",
        help="Training device: 'auto', 'cpu', 'cuda' or 'cuda:<n>' (e.g. cuda:0). "
             "'auto' uses CUDA when available, else CPU.",
    )
    p.add_argument("--epochs", type=int, default=5)
    p.add_argument("--batch_size", type=int, default=512)
    p.add_argument("--lr", type=float, default=1e-3)
    p.add_argument("--weight_decay", type=float, default=1e-5)
    p.add_argument("--val_split", type=float, default=0.05)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument(
        "--num_workers",
        type=int,
        default=None,
    )
    return p.parse_args()


def main() -> None:
    """Train NNEvalNet on a Stockfish-evaluated CSV and save the model bundle to trained_models/."""
    args = _parse_args()

    device = resolve_device(args.device)
    if device.type == "cuda":
        print(f"Training on CUDA: {torch.cuda.get_device_name(device.index or 0)}")
    else:
        print("Training on CPU.")

    train_cfg = TrainConfig(
        dataset_csv=args.dataset,
        epochs=args.epochs,
        batch_size=args.batch_size,
        lr=args.lr,
        weight_decay=args.weight_decay,
        val_split=args.val_split,
        seed=args.seed,
    )
    dataset_cfg = DatasetConfig()

    set_seed(train_cfg.seed)

    csv_path = data_dir() / train_cfg.dataset_csv

    print("Loading dataset:", csv_path)
    fens, phases, targets = load_dataset_rows(csv_path, dataset_cfg=dataset_cfg)

    n = len(fens)
    val_n = int(math.floor(n * float(train_cfg.val_split)))
    train_n = n - val_n
    train_fens, val_fens = fens[:train_n], fens[train_n:]
    train_phases, val_phases = phases[:train_n], phases[train_n:]
    train_targets, val_targets = targets[:train_n], targets[train_n:]

    train_ds = ChessEvalDataset(train_fens, train_phases, train_targets, dataset_cfg=dataset_cfg)
    val_ds = ChessEvalDataset(val_fens, val_phases, val_targets, dataset_cfg=dataset_cfg)

    workers = cpu_worker_count() if args.num_workers is None else max(0, int(args.num_workers))

    train_loader = DataLoader(
        train_ds,
        batch_size=train_cfg.batch_size,
        shuffle=True,
        num_workers=workers,
    )
    val_loader = DataLoader(
        val_ds,
        batch_size=train_cfg.batch_size,
        shuffle=False,
        num_workers=workers,
    )

    net = NNEvalNet(in_channels=input_channels(dataset_cfg)).to(device)

    opt = torch.optim.Adam(net.parameters(), lr=train_cfg.lr, weight_decay=train_cfg.weight_decay)
    loss_fn = nn.MSELoss()

    for epoch in range(1, train_cfg.epochs + 1):
        net.train()
        train_loss = 0.0
        for xb, yb in tqdm(train_loader, desc=f"Epoch {epoch}/{train_cfg.epochs}", unit="batch", leave=False):
            xb = xb.to(device, non_blocking=True)
            yb = yb.to(device, non_blocking=True)
            pred = net(xb)
            loss = loss_fn(pred, yb)

            opt.zero_grad(set_to_none=True)
            loss.backward()
            opt.step()

            train_loss += float(loss.item())

        if val_n > 0:
            net.eval()
            val_loss = 0.0
            with torch.no_grad():
                for xb, yb in tqdm(val_loader, desc=f"Val   {epoch}/{train_cfg.epochs}", unit="batch", leave=False):
                    xb = xb.to(device, non_blocking=True)
                    yb = yb.to(device, non_blocking=True)
                    pred = net(xb)
                    loss = loss_fn(pred, yb)
                    val_loss += float(loss.item())

            print(
                f"Epoch {epoch}: train_mse={train_loss / max(1, len(train_loader)):.6f} "
                f"val_mse={val_loss / max(1, len(val_loader)):.6f}"
            )
        else:
            print(f"Epoch {epoch}: train_mse={train_loss / max(1, len(train_loader)):.6f}")

    dataset_name = Path(train_cfg.dataset_csv).name
    stem = dataset_name.replace("stockfish_eval_", "").replace(".csv", "")
    model_path = trained_models_dir() / f"nn_eval_{stem}.pt"
    state_dict = net.state_dict()
    bundle = {
        "state_dict": {k: v.detach().cpu() for k, v in state_dict.items()},
        "dataset_config": {
            "target_scale": dataset_cfg.target_scale,
            "target_clip_cp": dataset_cfg.target_clip_cp,
            "include_game_phase": dataset_cfg.include_game_phase,
        },
        "model": {
            "arch": "NNEvalNet",
            "in_channels": input_channels(dataset_cfg),
        },
    }

    model_path.parent.mkdir(parents=True, exist_ok=True)
    torch.save(bundle, model_path)

    print("Saved model:", model_path)


if __name__ == "__main__":
    main()
