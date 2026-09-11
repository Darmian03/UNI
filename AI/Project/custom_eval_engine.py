from __future__ import annotations

from dataclasses import dataclass
from collections.abc import Iterable

import chess

_PIECE_VALUES: dict[chess.PieceType, int] = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 0,
}

_PAWN_PST = [
    0, 0, 0, 0, 0, 0, 0, 0,
    50, 50, 50, 50, 50, 50, 50, 50,
    10, 10, 20, 30, 30, 20, 10, 10,
    5, 5, 10, 25, 25, 10, 5, 5,
    0, 0, 0, 20, 20, 0, 0, 0,
    5, -5, -10, 0, 0, -10, -5, 5,
    5, 10, 10, -20, -20, 10, 10, 5,
    0, 0, 0, 0, 0, 0, 0, 0,
]

_KNIGHT_PST = [
    -50, -40, -30, -30, -30, -30, -40, -50,
    -40, -20, 0, 0, 0, 0, -20, -40,
    -30, 0, 10, 15, 15, 10, 0, -30,
    -30, 5, 15, 20, 20, 15, 5, -30,
    -30, 0, 15, 20, 20, 15, 0, -30,
    -30, 5, 10, 15, 15, 10, 5, -30,
    -40, -20, 0, 5, 5, 0, -20, -40,
    -50, -40, -30, -30, -30, -30, -40, -50,
]

_BISHOP_PST = [
    -20, -10, -10, -10, -10, -10, -10, -20,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -10, 0, 5, 10, 10, 5, 0, -10,
    -10, 5, 5, 10, 10, 5, 5, -10,
    -10, 0, 10, 10, 10, 10, 0, -10,
    -10, 10, 10, 10, 10, 10, 10, -10,
    -10, 5, 0, 0, 0, 0, 5, -10,
    -20, -10, -10, -10, -10, -10, -10, -20,
]

_ROOK_PST = [
    0, 0, 0, 0, 0, 0, 0, 0,
    5, 10, 10, 10, 10, 10, 10, 5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    0, 0, 0, 5, 5, 0, 0, 0,
]

_QUEEN_PST = [
    -20, -10, -10, -5, -5, -10, -10, -20,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -10, 0, 5, 5, 5, 5, 0, -10,
    -5, 0, 5, 5, 5, 5, 0, -5,
    0, 0, 5, 5, 5, 5, 0, -5,
    -10, 5, 5, 5, 5, 5, 0, -10,
    -10, 0, 5, 0, 0, 0, 0, -10,
    -20, -10, -10, -5, -5, -10, -10, -20,
]

_KING_PST_MG = [
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -20, -30, -30, -40, -40, -30, -30, -20,
    -10, -20, -20, -20, -20, -20, -20, -10,
    20, 20, 0, 0, 0, 0, 20, 20,
    20, 30, 10, 0, 0, 10, 30, 20,
]

_KING_PST_EG = [
    -50, -40, -30, -20, -20, -30, -40, -50,
    -30, -20, -10, 0, 0, -10, -20, -30,
    -30, -10, 20, 30, 30, 20, -10, -30,
    -30, -10, 30, 40, 40, 30, -10, -30,
    -30, -10, 30, 40, 40, 30, -10, -30,
    -30, -10, 20, 30, 30, 20, -10, -30,
    -30, -30, 0, 0, 0, 0, -30, -30,
    -50, -30, -30, -30, -30, -30, -30, -50,
]


@dataclass(frozen=True)
class EvalWeights:
    """Centipawn weights for handcrafted evaluation."""

    material: float = 1.00
    pst: float = 1.00
    mobility: float = 3.00
    king_safety: float = 1.00
    pawn_structure: float = 1.00


def _piece_squares(piece_type: chess.PieceType, color: chess.Color, board: chess.Board) -> Iterable[int]:
    return board.pieces(piece_type, color)


def _pst_value(piece_type: chess.PieceType, square: int, *, endgame_t: float) -> int:
    """PST value for a piece on a square; the king blends midgame/endgame tables by phase."""
    if piece_type == chess.PAWN:
        return _PAWN_PST[square]
    if piece_type == chess.KNIGHT:
        return _KNIGHT_PST[square]
    if piece_type == chess.BISHOP:
        return _BISHOP_PST[square]
    if piece_type == chess.ROOK:
        return _ROOK_PST[square]
    if piece_type == chess.QUEEN:
        return _QUEEN_PST[square]
    if piece_type == chess.KING:
        mg = _KING_PST_MG[square]
        eg = _KING_PST_EG[square]
        return int(round((1.0 - endgame_t) * mg + endgame_t * eg))
    return 0


def _game_phase_endgame_t(board: chess.Board) -> float:
    """Endgame-ness in [0, 1] from remaining material (queens weigh most); 1.0 = full endgame."""
    phase = 0
    phase += 1 * (len(board.pieces(chess.KNIGHT, chess.WHITE)) + len(board.pieces(chess.KNIGHT, chess.BLACK)))
    phase += 1 * (len(board.pieces(chess.BISHOP, chess.WHITE)) + len(board.pieces(chess.BISHOP, chess.BLACK)))
    phase += 2 * (len(board.pieces(chess.ROOK, chess.WHITE)) + len(board.pieces(chess.ROOK, chess.BLACK)))
    phase += 4 * (len(board.pieces(chess.QUEEN, chess.WHITE)) + len(board.pieces(chess.QUEEN, chess.BLACK)))

    max_phase = 24
    phase = max(0, min(max_phase, phase))
    return 1.0 - (phase / float(max_phase))


def _material_eval_white(board: chess.Board) -> int:
    """Material balance in centipawns (White minus Black), plus a two-bishop bonus."""
    score = 0
    for pt, val in _PIECE_VALUES.items():
        score += val * len(board.pieces(pt, chess.WHITE))
        score -= val * len(board.pieces(pt, chess.BLACK))

    if len(board.pieces(chess.BISHOP, chess.WHITE)) >= 2:
        score += 25
    if len(board.pieces(chess.BISHOP, chess.BLACK)) >= 2:
        score -= 25

    return score


def _pst_eval_white(board: chess.Board, *, endgame_t: float) -> int:
    """PST sum for both sides; Black's squares are mirrored so one table serves both colors."""
    score = 0
    for pt in (chess.PAWN, chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN, chess.KING):
        for sq in _piece_squares(pt, chess.WHITE, board):
            score += _pst_value(pt, sq, endgame_t=endgame_t)
        for sq in _piece_squares(pt, chess.BLACK, board):
            score -= _pst_value(pt, chess.square_mirror(sq), endgame_t=endgame_t)
    return score


def _mobility(board: chess.Board, color: chess.Color) -> int:
    """Number of legal moves for a color (board copy so the real turn is untouched)."""
    b = board.copy(stack=False)
    b.turn = color
    return sum(1 for _ in b.legal_moves)


def _mobility_eval_white(board: chess.Board, *, endgame_t: float) -> int:
    """Mobility difference; scaled down in the endgame when few pieces remain."""
    w = _mobility(board, chess.WHITE)
    b = _mobility(board, chess.BLACK)
    scale = 1.0 - 0.35 * endgame_t
    return int(round((w - b) * scale))


def _pawn_structure_eval_white(board: chess.Board, *, endgame_t: float) -> int:
    score = 0

    def pawns(color: chess.Color) -> list[int]:
        return list(board.pieces(chess.PAWN, color))

    w_pawns = pawns(chess.WHITE)
    b_pawns = pawns(chess.BLACK)

    def file_counts(pawn_sqs: list[int]) -> list[int]:
        counts = [0] * 8
        for sq in pawn_sqs:
            counts[chess.square_file(sq)] += 1
        return counts

    w_files = file_counts(w_pawns)
    b_files = file_counts(b_pawns)

    def is_isolated(sq: int, counts: list[int]) -> bool:
        f = chess.square_file(sq)
        left = counts[f - 1] if f - 1 >= 0 else 0
        right = counts[f + 1] if f + 1 < 8 else 0
        # A pawn is passed when no enemy pawn can stop it on its file or adjacent files.
        return left == 0 and right == 0

    def is_passed(color: chess.Color, sq: int, enemy_pawns: list[int]) -> bool:
        f = chess.square_file(sq)
        r = chess.square_rank(sq)

        for ep in enemy_pawns:
            ef = chess.square_file(ep)
            er = chess.square_rank(ep)
            if abs(ef - f) > 1:
                continue
            if color == chess.WHITE:
                if er > r:
                    return False
            else:
                if er < r:
                    return False
        return True

    doubled_pen = 12
    isolated_pen = 10
    passed_bonus_mg = 18
    passed_bonus_eg = 35

    for sq in w_pawns:
        f = chess.square_file(sq)
        if w_files[f] >= 2:
            score -= doubled_pen
        if is_isolated(sq, w_files):
            score -= isolated_pen
        if is_passed(chess.WHITE, sq, b_pawns):
            score += int(round((1.0 - endgame_t) * passed_bonus_mg + endgame_t * passed_bonus_eg))

    for sq in b_pawns:
        f = chess.square_file(sq)
        if b_files[f] >= 2:
            score += doubled_pen
        if is_isolated(sq, b_files):
            score += isolated_pen
        if is_passed(chess.BLACK, sq, w_pawns):
            score -= int(round((1.0 - endgame_t) * passed_bonus_mg + endgame_t * passed_bonus_eg))

    """King-safety score (White minus Black): rewards own pawn shield and punishes enemy
    attackers around the king; both effects fade in the endgame, plus a check penalty."""

    return score


def _king_safety_eval_white(board: chess.Board, *, endgame_t: float) -> int:
    def king_sq(color: chess.Color) -> int | None:
        k = board.king(color)
        return int(k) if k is not None else None

    def pawn_shield(color: chess.Color, ksq: int) -> int:
        f = chess.square_file(ksq)
        r = chess.square_rank(ksq)
        score = 0
        dr = 1 if color == chess.WHITE else -1
        shield_rank = r + dr
        if not (0 <= shield_rank <= 7):
            return 0

        for df in (-1, 0, 1):
            ff = f + df
            if not (0 <= ff <= 7):
                continue
            sq = chess.square(ff, shield_rank)
        # Total number of enemy pieces attacking the squares around the king.
            if board.piece_at(sq) == chess.Piece(chess.PAWN, color):
                score += 1
        return score

    def king_ring_attack(color: chess.Color, ksq: int) -> int:
        enemy = not color
        attacks = 0
        for sq in chess.SquareSet(chess.BB_KING_ATTACKS[ksq]):
            attacks += len(board.attackers(enemy, sq))
        return attacks

    wk = king_sq(chess.WHITE)
    bk = king_sq(chess.BLACK)
    if wk is None or bk is None:
        return 0
    safety_scale = 1.0 - 0.75 * endgame_t

    w_shield = pawn_shield(chess.WHITE, wk)
    b_shield = pawn_shield(chess.BLACK, bk)

    w_ring = king_ring_attack(chess.WHITE, wk)
    b_ring = king_ring_attack(chess.BLACK, bk)

    score = 0
    score += int(round(safety_scale * (12 * w_shield)))
    score -= int(round(safety_scale * (12 * b_shield)))

    score -= int(round(safety_scale * (6 * w_ring)))
    score += int(round(safety_scale * (6 * b_ring)))
    if board.is_check():
        score += -35 if board.turn == chess.WHITE else 35

    return score


def _eval_white(board: chess.Board, weights: EvalWeights) -> float:
    endgame_t = _game_phase_endgame_t(board)

    material = _material_eval_white(board)
    pst = _pst_eval_white(board, endgame_t=endgame_t)
    pawn_struct = _pawn_structure_eval_white(board, endgame_t=endgame_t)
    mobility = _mobility_eval_white(board, endgame_t=endgame_t)
    king_safety = _king_safety_eval_white(board, endgame_t=endgame_t)

    total = (
        weights.material * material
        + weights.pst * pst
        + weights.pawn_structure * pawn_struct
        + weights.mobility * mobility
        + weights.king_safety * king_safety
    )
    total += 8 if board.turn == chess.WHITE else -8

    return float(total)


def evaluate_position(board: chess.Board) -> float:
    """Return centipawn score from the side-to-move perspective."""
    white_score = _eval_white(board, EvalWeights())
    return float(white_score if board.turn == chess.WHITE else -white_score)


def evaluator_white_pov(board: chess.Board) -> float:
    """Return centipawn score from White's perspective."""
    return float(_eval_white(board, EvalWeights()))
