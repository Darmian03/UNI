from __future__ import annotations

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


class NeuralNetworkEvaluator:
    """Inference-only wrapper exposing evaluate(board) -> float (centipawns)."""

    def __init__(self, model_path: Path):
        bundle = torch.load(model_path, map_location="cpu")
        self.dataset_cfg = DatasetConfig(**bundle["dataset_config"])
        in_ch = int(bundle["model"]["in_channels"])

        net = NNEvalNet(in_channels=in_ch)
        net.load_state_dict(bundle["state_dict"])
        net.eval()

        self.device = torch.device("cpu")
        self.net = net

    @torch.no_grad()
    def evaluate(self, board: chess.Board, game_phase: str | None = None) -> float:
        planes = encode_board(
            board,
            game_phase if game_phase in ("early", "mid", "end") else None,
            include_game_phase=self.dataset_cfg.include_game_phase,
        )
        x = torch.from_numpy(planes).unsqueeze(0)
        y_pawns = float(self.net(x).item())
        return y_pawns * float(self.dataset_cfg.target_scale)
