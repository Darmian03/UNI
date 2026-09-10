from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import chess
import torch
import torch.nn as nn

from NN_model.utils import DatasetConfig, encode_board


class NNEvalNet(nn.Module):
    """Lightweight CNN that outputs a scalar evaluation in pawns."""

    def __init__(self, in_channels: int):
        super().__init__()

        self.features = nn.Sequential(
            nn.Conv2d(in_channels, 32, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(64, 64, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
        )

        self.head = nn.Sequential(
            nn.Flatten(),
            nn.Linear(64 * 8 * 8, 256),
            nn.ReLU(inplace=True),
            nn.Linear(256, 1),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.features(x)
        x = self.head(x)
        return x.squeeze(-1)


@dataclass(frozen=True)
class SavedModelBundle:
    state_dict: dict[str, Any]
    dataset_config: dict[str, Any]
    model: dict[str, Any]


def input_channels(dataset_cfg: DatasetConfig) -> int:
    return 12 + 1 + 4 + 1 + (3 if dataset_cfg.include_game_phase else 0)


# For CPU inference of this small net (batch size 1), torch's default of using
# ALL cores is a big loss: spawning/synchronizing ~24 threads per forward pass
# costs far more than the math itself. Measured on a 24-core box:
#   all cores -> ~3.8 ms/evaluate,  8 threads -> ~0.10 ms/evaluate (~40x).
# Training (batched) is NOT affected — it keeps torch's default threading.
_CPU_INFERENCE_MAX_THREADS = 8


def _cap_cpu_inference_threads() -> None:
    """Limit intra-op threads for CPU inference of this small net."""
    current = torch.get_num_threads()
    cap = min(_CPU_INFERENCE_MAX_THREADS, max(1, os.cpu_count() or 1))
    if current > cap:
        torch.set_num_threads(cap)


def resolve_device(spec: str | None = "auto") -> torch.device:
    """Resolve a device spec to a ``torch.device``.

    Accepted specs (case-insensitive): ``"auto"``, ``"cpu"``, ``"cuda"``,
    ``"gpu"``, or an indexed GPU like ``"cuda:0"`` / ``"cuda:1"``.
    ``"auto"`` uses CUDA when available and falls back to CPU with a warning,
    so the project runs unchanged on machines without a GPU/CUDA.
    """
    s = (spec or "auto").strip().lower()

    if s == "cpu":
        return torch.device("cpu")

    if s in ("cuda", "gpu"):
        index: int | None = None
    elif s.startswith("cuda:") and len(s) > 5:
        try:
            index = int(s.split(":", 1)[1])
        except ValueError:
            raise ValueError(
                f"Unknown device spec: {spec!r} (expected 'auto', 'cpu', 'cuda' or 'cuda:<n>')."
            ) from None
    elif s == "auto":
        if torch.cuda.is_available():
            return torch.device("cuda")
        print("[device] CUDA not available — falling back to CPU.")
        return torch.device("cpu")
    else:
        raise ValueError(f"Unknown device spec: {spec!r} (expected 'auto', 'cpu', 'cuda' or 'cuda:<n>').")

    # Explicit CUDA request ("cuda", "gpu" or "cuda:<n>").
    if not torch.cuda.is_available():
        raise RuntimeError(
            f"Device '{spec}' was requested but CUDA is not available. "
            "Check your NVIDIA driver and the PyTorch build (a CUDA-enabled wheel)."
        )
    return torch.device(f"cuda:{index}" if index is not None else "cuda")


class NeuralNetworkEvaluator:
    """Inference-only wrapper exposing evaluate(board) -> float (centipawns)."""

    def __init__(self, model_path: Path, *, device: str | None = "auto"):
        bundle = torch.load(model_path, map_location="cpu", weights_only=True)
        self.dataset_cfg = DatasetConfig(**bundle["dataset_config"])
        in_ch = int(bundle["model"]["in_channels"])

        net = NNEvalNet(in_channels=in_ch)
        net.load_state_dict(bundle["state_dict"])
        net.eval()

        self.device = resolve_device(device)
        if self.device.type == "cpu":
            _cap_cpu_inference_threads()
        self.net = net.to(self.device)

    @torch.no_grad()
    def evaluate(self, board: chess.Board, game_phase: str | None = None) -> float:
        planes = encode_board(
            board,
            game_phase if game_phase in ("early", "mid", "end") else None,
            include_game_phase=self.dataset_cfg.include_game_phase,
        )
        x = torch.from_numpy(planes).unsqueeze(0).to(self.device)
        y_pawns = float(self.net(x).item())
        return y_pawns * float(self.dataset_cfg.target_scale)
