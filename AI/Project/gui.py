from __future__ import annotations

import os
import threading
import time
from dataclasses import dataclass
from pathlib import Path
from queue import Queue
from typing import Dict, List, Optional, Tuple

import chess
import pygame
from minimax import minimax
from stockfish_engine import evaluate_board as stockfish_evaluate_board
from stockfish_engine import find_stockfish_exe
from custom_eval_engine import evaluator_white_pov

EVT_MOUSEBUTTONDOWN = int(getattr(pygame, "MOUSEBUTTONDOWN", 1025))
EVT_MOUSEWHEEL = int(getattr(pygame, "MOUSEWHEEL", 1027))
EVT_QUIT = int(getattr(pygame, "QUIT", 256))
SRCALPHA = int(getattr(pygame, "SRCALPHA", 65536))
_pygame_init = getattr(pygame, "init", lambda: None)
_pygame_quit = getattr(pygame, "quit", lambda: None)

from NN_model.model import NeuralNetworkEvaluator

FPS = 60

LIGHT_SQ = (240, 217, 181)
DARK_SQ = (181, 136, 99)

HIGHLIGHT_SELECTED = (80, 160, 255)
HIGHLIGHT_LEGAL = (90, 220, 150)

CHECK_ORANGE = (255, 165, 0)
CHECKMATE_RED = (220, 20, 60)

PANEL_BG = (35, 35, 35)
TEXT = (235, 235, 235)
SUBTEXT = (190, 190, 190)
ACCENT = (70, 120, 200)

@dataclass
class Dropdown:
    rect: pygame.Rect
    label: str
    options: List[str]
    selected_index: int = 0
    open: bool = False

    def selected(self) -> str:
        if not self.options:
            return ""
        self.selected_index = max(0, min(self.selected_index, len(self.options) - 1))
        return self.options[self.selected_index]

    def handle_event(self, event: pygame.event.Event) -> Optional[str]:
        if event.type != EVT_MOUSEBUTTONDOWN or event.button != 1:
            return None

        mx, my = event.pos
        if self.rect.collidepoint(mx, my):
            self.open = not self.open
            return None

        if not self.open:
            return None

        menu_rect = pygame.Rect(self.rect.x, self.rect.bottom, self.rect.w, self.rect.h * len(self.options))
        if not menu_rect.collidepoint(mx, my):
            self.open = False
            return None

        idx = (my - self.rect.bottom) // self.rect.h
        if 0 <= idx < len(self.options):
            self.selected_index = int(idx)
            self.open = False
            return self.selected()

        return None

    def draw_base(self, screen: pygame.Surface, font: pygame.font.Font) -> None:
        pygame.draw.rect(screen, (55, 55, 55), self.rect, border_radius=4)
        pygame.draw.rect(screen, (90, 90, 90), self.rect, width=1, border_radius=4)

        label_surf = font.render(f"{self.label}: {self.selected()}", True, TEXT)
        screen.blit(label_surf, (self.rect.x + 8, self.rect.y + (self.rect.h - label_surf.get_height()) // 2))

        pygame.draw.polygon(
            screen,
            (200, 200, 200),
            [
                (self.rect.right - 18, self.rect.y + self.rect.h // 2 - 3),
                (self.rect.right - 8, self.rect.y + self.rect.h // 2 - 3),
                (self.rect.right - 13, self.rect.y + self.rect.h // 2 + 4),
            ],
        )

    def draw_menu(self, screen: pygame.Surface, font: pygame.font.Font) -> None:
        if not self.open:
            return
        for i, opt in enumerate(self.options):
            r = pygame.Rect(self.rect.x, self.rect.bottom + i * self.rect.h, self.rect.w, self.rect.h)
            bg = (65, 65, 65) if i != self.selected_index else (85, 85, 85)
            pygame.draw.rect(screen, bg, r)
            pygame.draw.rect(screen, (90, 90, 90), r, width=1)
            s = font.render(opt, True, TEXT)
            screen.blit(s, (r.x + 8, r.y + (r.h - s.get_height()) // 2))

    def draw(self, screen: pygame.Surface, font: pygame.font.Font) -> None:
        self.draw_base(screen, font)
        self.draw_menu(screen, font)


@dataclass
class Button:
    rect: pygame.Rect
    text: str
    enabled: bool = True

    def handle_event(self, event: pygame.event.Event) -> bool:
        if not self.enabled:
            return False
        if event.type == EVT_MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(*event.pos):
                return True
        return False

    def draw(self, screen: pygame.Surface, font: pygame.font.Font) -> None:
        bg = (70, 70, 70) if self.enabled else (50, 50, 50)
        pygame.draw.rect(screen, bg, self.rect, border_radius=4)
        pygame.draw.rect(screen, (100, 100, 100), self.rect, width=1, border_radius=4)
        s = font.render(self.text, True, TEXT if self.enabled else SUBTEXT)
        screen.blit(s, (self.rect.centerx - s.get_width() // 2, self.rect.centery - s.get_height() // 2))
class EngineAdapter:
    def get_best_move(self, _board: chess.Board) -> chess.Move:
        return chess.Move.null()


class StockfishAdapter(EngineAdapter):
    def __init__(self, *, depth: int, threads: Optional[int] = None):
        self.depth = int(depth)
        self.threads = threads

    def get_best_move(self, board: chess.Board) -> chess.Move:
        move, _score = stockfish_evaluate_board(board, depth=self.depth, threads=self.threads)
        return move


class CustomMinimaxAdapter(EngineAdapter):
    def __init__(self, *, depth: int, num_processes: Optional[int] = None):
        self.depth = int(depth)
        self.num_processes = num_processes

    def get_best_move(self, board: chess.Board) -> chess.Move:
        move, _score = minimax(
            board,
            depth=self.depth,
            evaluator=evaluator_white_pov,
            use_multiprocessing=True,
            num_processes=self.num_processes,
        )
        return move


def _phase_for(board: chess.Board) -> str:
    """Return a coarse game-phase label for optional NN conditioning."""
    values = {
        chess.PAWN: 1,
        chess.KNIGHT: 3,
        chess.BISHOP: 3,
        chess.ROOK: 5,
        chess.QUEEN: 9,
    }
    material = 0
    for pt, v in values.items():
        material += v * (len(board.pieces(pt, chess.WHITE)) + len(board.pieces(pt, chess.BLACK)))

    if board.fullmove_number < 10:
        return "early"
    if board.fullmove_number <= 30 and material > 20:
        return "mid"
    return "end"


class NNMinimaxAdapter(EngineAdapter):
    def __init__(self, *, model_path: Path, depth: int = 3, num_processes: Optional[int] = None):
        self.depth = int(depth)
        self.num_processes = num_processes
        self.nn = NeuralNetworkEvaluator(model_path)

    def _evaluator_white(self, board: chess.Board) -> float:
        return float(self.nn.evaluate(board, _phase_for(board)))

    def get_best_move(self, board: chess.Board) -> chess.Move:
        move, _score = minimax(
            board,
            depth=self.depth,
            evaluator=self._evaluator_white,
            use_multiprocessing=True,
            num_processes=self.num_processes,
        )
        return move

@dataclass(frozen=True)
class HumanMoveRecord:
    fen_before: str
    move_uci: str
    san: str


@dataclass(frozen=True)
class AnalysisRow:
    ply_index: int
    san: str
    played_eval_cp: float
    best_san: str
    best_eval_cp: float


def run_post_game_analysis(
    *,
    human_moves: List[HumanMoveRecord],
    depth: int,
    threads: int,
) -> List[AnalysisRow]:
    """Прави Stockfish анализ за всеки човешки ход."""

    from chess import engine as chess_engine

    exe = find_stockfish_exe()
    engine = chess_engine.SimpleEngine.popen_uci(str(exe))
    engine.configure({"Threads": int(threads)})

    rows: List[AnalysisRow] = []
    for i, rec in enumerate(human_moves):
        b = chess.Board(rec.fen_before)
        info_best = engine.analyse(b, chess_engine.Limit(depth=int(depth)))
        pv = info_best.get("pv") or []
        best_move = pv[0] if pv else None
        score_best = info_best.get("score")
        best_eval = float(score_best.pov(b.turn).score(mate_score=100000) or 0) if score_best else 0.0
        best_san = b.san(best_move) if best_move is not None else "(none)"

        played_move = chess.Move.from_uci(rec.move_uci)
        info_played = engine.analyse(b, chess_engine.Limit(depth=int(depth)), root_moves=[played_move])
        score_played = info_played.get("score")
        played_eval = float(score_played.pov(b.turn).score(mate_score=100000) or 0) if score_played else 0.0

        rows.append(
            AnalysisRow(
                ply_index=i,
                san=rec.san,
                played_eval_cp=played_eval,
                best_san=best_san,
                best_eval_cp=best_eval,
            )
        )

    engine.quit()
    return rows

def _project_root() -> Path:
    return Path(__file__).resolve().parent


def _figures_dir() -> Path:
    return _project_root() / "data" / "figures"


def _piece_code(piece: chess.Piece) -> str:
    c = "w" if piece.color == chess.WHITE else "b"
    t = {
        chess.PAWN: "P",
        chess.KNIGHT: "N",
        chess.BISHOP: "B",
        chess.ROOK: "R",
        chess.QUEEN: "Q",
        chess.KING: "K",
    }[piece.piece_type]
    return f"{c}{t}"


def _load_piece_images(square_size: int) -> Dict[str, pygame.Surface]:
    out: Dict[str, pygame.Surface] = {}
    for code in ("wP", "wN", "wB", "wR", "wQ", "wK", "bP", "bN", "bB", "bR", "bQ", "bK"):
        p = _figures_dir() / f"{code}.png"
        img = pygame.image.load(str(p)).convert_alpha()
        out[code] = pygame.transform.smoothscale(img, (square_size, square_size))
    return out


def _square_to_screen(
    square: chess.Square,
    *,
    origin: Tuple[int, int],
    square_size: int,
    human_color: chess.Color,
) -> Tuple[int, int]:
    file = chess.square_file(square)
    rank = chess.square_rank(square)

    if human_color == chess.WHITE:
        x = origin[0] + file * square_size
        y = origin[1] + (7 - rank) * square_size
    else:
        x = origin[0] + (7 - file) * square_size
        y = origin[1] + rank * square_size

    return x, y


def _screen_to_square(
    pos: Tuple[int, int],
    *,
    origin: Tuple[int, int],
    square_size: int,
    human_color: chess.Color,
) -> Optional[chess.Square]:
    x, y = pos
    ox, oy = origin
    if x < ox or y < oy:
        return None

    file = (x - ox) // square_size
    rank_from_top = (y - oy) // square_size

    if not (0 <= file < 8 and 0 <= rank_from_top < 8):
        return None

    if human_color == chess.WHITE:
        rank = 7 - rank_from_top
        return chess.square(int(file), int(rank))
    rank = rank_from_top
    file2 = 7 - file
    return chess.square(int(file2), int(rank))


def _draw_board(
    screen: pygame.Surface,
    *,
    board: chess.Board,
    origin: Tuple[int, int],
    square_size: int,
    human_color: chess.Color,
    images: Dict[str, pygame.Surface],
    selected_square: Optional[chess.Square],
    legal_dests: List[chess.Square],
) -> None:
    king_sq = None
    if board.is_checkmate():
        king_sq = board.king(board.turn)
    elif board.is_check():
        king_sq = board.king(board.turn)

    for rank in range(8):
        for file in range(8):
            sq = chess.square(file, rank)
            is_light = (file + rank) % 2 == 0
            base = LIGHT_SQ if is_light else DARK_SQ

            sx, sy = _square_to_screen(sq, origin=origin, square_size=square_size, human_color=human_color)
            r = pygame.Rect(sx, sy, square_size, square_size)
            pygame.draw.rect(screen, base, r)
    if king_sq is not None:
        sx, sy = _square_to_screen(king_sq, origin=origin, square_size=square_size, human_color=human_color)
        r = pygame.Rect(sx, sy, square_size, square_size)
        pygame.draw.rect(screen, CHECKMATE_RED if board.is_checkmate() else CHECK_ORANGE, r)

    if selected_square is not None:
        if king_sq != selected_square:
            sx, sy = _square_to_screen(selected_square, origin=origin, square_size=square_size, human_color=human_color)
            r = pygame.Rect(sx, sy, square_size, square_size)
            s = pygame.Surface((square_size, square_size), SRCALPHA)
            s.fill((*HIGHLIGHT_SELECTED, 120))
            screen.blit(s, r.topleft)

    for dsq in legal_dests:
        if king_sq == dsq:
            continue
        sx, sy = _square_to_screen(dsq, origin=origin, square_size=square_size, human_color=human_color)
        r = pygame.Rect(sx, sy, square_size, square_size)
        s = pygame.Surface((square_size, square_size), SRCALPHA)
        s.fill((*HIGHLIGHT_LEGAL, 110))
        screen.blit(s, r.topleft)
    for square, piece in board.piece_map().items():
        code = _piece_code(piece)
        img = images.get(code)
        if img is None:
            continue
        sx, sy = _square_to_screen(square, origin=origin, square_size=square_size, human_color=human_color)
        screen.blit(img, (sx, sy))

@dataclass
class CaptureEvent:
    captured_code: Optional[str]
    capturer: Optional[chess.Color]


def _capture_for_move(board: chess.Board, move: chess.Move) -> Optional[str]:
    if not board.is_capture(move):
        return None

    if board.is_en_passant(move):
        file = chess.square_file(move.to_square)
        rank = chess.square_rank(move.to_square)
        cap_rank = rank - 1 if board.turn == chess.WHITE else rank + 1
        cap_sq = chess.square(file, cap_rank)
        piece = board.piece_at(cap_sq)
    else:
        piece = board.piece_at(move.to_square)

    return _piece_code(piece) if piece is not None else None


def _coerce_promotion(board: chess.Board, move: chess.Move) -> chess.Move:
    piece = board.piece_at(move.from_square)
    if piece is None or piece.piece_type != chess.PAWN:
        return move

    to_rank = chess.square_rank(move.to_square)
    if (piece.color == chess.WHITE and to_rank == 7) or (piece.color == chess.BLACK and to_rank == 0):
        return chess.Move(move.from_square, move.to_square, promotion=chess.QUEEN)

    return move


def main() -> None:
    _pygame_init()
    pygame.display.set_caption("Chess AI GUI")

    square_size = 80
    board_px = square_size * 8
    panel_w = 360
    margin = 16

    width = margin * 3 + board_px + panel_w
    height = margin * 2 + board_px

    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()

    # Cross-platform: SysFont(None, ...) uses the system default font on any OS.
    font = pygame.font.SysFont(None, 20)
    small = pygame.font.SysFont(None, 17)

    images = _load_piece_images(square_size)
    mini_images = _load_piece_images(32)

    board_origin = (margin, margin)
    panel_origin = (margin * 2 + board_px, margin)
    opponent_dd = Dropdown(
        rect=pygame.Rect(panel_origin[0], panel_origin[1] + 28, panel_w, 36),
        label="Opponent",
        options=["Stockfish", "Neural Network", "Custom Evaluation"],
    )

    color_dd = Dropdown(
        rect=pygame.Rect(panel_origin[0], panel_origin[1] + 78, panel_w, 36),
        label="Play as",
        options=["White", "Black"],
    )

    option_dd = Dropdown(
        rect=pygame.Rect(panel_origin[0], panel_origin[1] + 128, panel_w, 36),
        label="Option",
        options=["Depth 8"],
    )

    start_btn = Button(
        rect=pygame.Rect(panel_origin[0], panel_origin[1] + 178, panel_w, 40),
        text="Start Game",
        enabled=True,
    )

    game_menu_dd = Dropdown(
        rect=pygame.Rect(panel_origin[0], panel_origin[1], panel_w, 36),
        label="Game",
        options=["New Game"],
    )
    undo_btn = Button(
        rect=pygame.Rect(panel_origin[0], panel_origin[1] + 50, panel_w, 40),
        text="Undo last move",
        enabled=True,
    )

    state = "setup"

    board = chess.Board()
    human_color = chess.WHITE
    engine: Optional[EngineAdapter] = None

    selected_sq: Optional[chess.Square] = None
    legal_dests: List[chess.Square] = []

    move_san: List[str] = []
    capture_log: List[CaptureEvent] = []
    captured_by_white: List[str] = []
    captured_by_black: List[str] = []

    human_moves: List[HumanMoveRecord] = []
    engine_queue: "Queue[Optional[chess.Move]]" = Queue()
    engine_thread: Optional[threading.Thread] = None
    engine_thinking = False

    analysis_rows: List[AnalysisRow] = []
    analysis_thread: Optional[threading.Thread] = None
    analysis_queue: "Queue[Optional[List[AnalysisRow]]]" = Queue()
    analysis_scroll = 0

    history_scroll = 0

    status_msg = ""
    pending_analysis_at: Optional[float] = None

    def _game_result_message() -> str:
        if board.is_checkmate():
            winner = "White" if board.turn == chess.BLACK else "Black"
            return f"Checkmate. {winner} wins."
        if board.is_stalemate():
            return "Draw by stalemate."
        if board.is_insufficient_material():
            return "Draw by insufficient material."
        if board.can_claim_threefold_repetition():
            return "Draw (threefold repetition claim)."
        if board.can_claim_fifty_moves():
            return "Draw (50-move rule claim)."
        return "Game over."

    def _analysis_new_game_button_rect() -> pygame.Rect:
        panel = pygame.Rect(margin, margin, width - 2 * margin, height - 2 * margin)
        return pygame.Rect(panel.right - 140 - 12, panel.y + 10, 140, 32)

    def reset_to_setup() -> None:
        nonlocal state, board, engine, selected_sq, legal_dests
        nonlocal move_san, capture_log, captured_by_white, captured_by_black
        nonlocal human_moves, engine_thread, engine_thinking, status_msg
        nonlocal analysis_rows, analysis_thread, analysis_scroll, history_scroll, pending_analysis_at

        state = "setup"
        board = chess.Board()
        engine = None
        selected_sq = None
        legal_dests = []
        move_san = []
        capture_log = []
        captured_by_white = []
        captured_by_black = []
        human_moves = []
        engine_thread = None
        engine_thinking = False
        status_msg = ""
        pending_analysis_at = None
        analysis_rows = []
        analysis_thread = None
        analysis_scroll = 0
        history_scroll = 0

    def build_engine() -> EngineAdapter:
        opp = opponent_dd.selected()
        threads = max(1, os.cpu_count() or 1)
        num_procs = threads

        if opp == "Stockfish":
            depth = int(option_dd.selected())
            return StockfishAdapter(depth=depth, threads=threads)

        if opp == "Custom Evaluation":
            depth = int(option_dd.selected())
            return CustomMinimaxAdapter(depth=depth, num_processes=num_procs)

        model_label = option_dd.selected()
        model_map = {
            "NN 50K low elo": "nn_eval_50k_low_elo.pt",
            "NN 50K high elo": "nn_eval_50k_high_elo.pt",
            "NN 100K low elo": "nn_eval_100k_low_elo.pt",
            "NN 100K high elo": "nn_eval_100k_high_elo.pt",
            "NN 250K low elo": "nn_eval_250k_low_elo.pt",
            "NN 250K high elo": "nn_eval_250k_high_elo.pt",
            "NN 500K low elo": "nn_eval_500k_low_elo.pt",
            "NN 500K high elo": "nn_eval_500k_high_elo.pt",
            "NN 1000K low elo": "nn_eval_1000k_low_elo.pt",
            "NN 1000K high elo": "nn_eval_1000k_high_elo.pt",
        }

        fname = model_map.get(model_label, "nn_eval_50k_low_elo.pt")
        model_path = _project_root() / "trained_models" / fname

        return NNMinimaxAdapter(model_path=model_path, depth=4, num_processes=num_procs)

    def update_option_dropdown() -> None:
        opp = opponent_dd.selected()
        if opp == "Stockfish":
            option_dd.label = "Search depth"
            option_dd.options = ["4", "8", "12", "16"]
            option_dd.selected_index = 1
        elif opp == "Custom Evaluation":
            option_dd.label = "Minimax depth"
            option_dd.options = ["1", "2", "3", "4"]
            option_dd.selected_index = 2
        else:
            option_dd.label = "NN Model"
            option_dd.options = [
                "NN 50K low elo",
                "NN 50K high elo",
                "NN 100K low elo",
                "NN 100K high elo",
                "NN 250K low elo",
                "NN 250K high elo",
                "NN 500K low elo",
                "NN 500K high elo",
                "NN 1000K low elo",
                "NN 1000K high elo",
            ]
            option_dd.selected_index = 0

    update_option_dropdown()

    def start_game() -> None:
        nonlocal state, engine, board, human_color
        nonlocal selected_sq, legal_dests, status_msg

        board = chess.Board()
        selected_sq = None
        legal_dests = []
        status_msg = ""

        human_color = chess.WHITE if color_dd.selected() == "White" else chess.BLACK
        engine = build_engine()
        state = "playing"

    def begin_engine_move_if_needed() -> None:
        nonlocal engine_thread, engine_thinking

        if engine is None:
            return
        if board.is_game_over(claim_draw=True):
            return

        is_human_turn = board.turn == human_color
        if is_human_turn:
            return

        if engine_thinking:
            return

        def worker(fen: str) -> None:
            b = chess.Board(fen)
            mv = engine.get_best_move(b)
            engine_queue.put(mv)

        engine_thinking = True
        engine_thread = threading.Thread(target=worker, args=(board.fen(),), daemon=True)
        engine_thread.start()

    def apply_move(move: chess.Move, *, is_human: bool) -> None:
        nonlocal selected_sq, legal_dests, status_msg

        move = _coerce_promotion(board, move)
        if move not in board.legal_moves:
            status_msg = "Illegal move"
            return

        fen_before = board.fen()
        cap_code = _capture_for_move(board, move)
        capturer = board.turn

        san = board.san(move)
        board.push(move)

        move_san.append(san)
        capture_log.append(CaptureEvent(captured_code=cap_code, capturer=capturer if cap_code else None))

        if cap_code:
            if capturer == chess.WHITE:
                captured_by_white.append(cap_code)
            else:
                captured_by_black.append(cap_code)

        if is_human:
            human_moves.append(HumanMoveRecord(fen_before=fen_before, move_uci=move.uci(), san=san))

        selected_sq = None
        legal_dests = []
        status_msg = ""

    def undo_one_ply() -> None:
        nonlocal selected_sq, legal_dests

        if not board.move_stack:
            return

        board.pop()
        if move_san:
            move_san.pop()

        if capture_log:
            cap = capture_log.pop()
            if cap.captured_code and cap.capturer is not None:
                if cap.capturer == chess.WHITE and captured_by_white:
                    captured_by_white.pop()
                elif cap.capturer == chess.BLACK and captured_by_black:
                    captured_by_black.pop()

        if human_moves:
            if not move_san or human_moves[-1].san != move_san[-1]:
                human_moves.pop()

        selected_sq = None
        legal_dests = []

    def maybe_finish_game() -> None:
        nonlocal state, analysis_thread, engine_thinking, status_msg, pending_analysis_at

        if not board.is_game_over(claim_draw=True):
            return

        if state != "playing":
            return
        if pending_analysis_at is None:
            pending_analysis_at = time.time() + 3.0
            status_msg = _game_result_message()
            engine_thinking = False
            return
        if time.time() < float(pending_analysis_at):
            return
        state = "analysis"
        status_msg = "Analyzing..."
        pending_analysis_at = None

        def analysis_worker(moves: List[HumanMoveRecord]) -> None:
            threads = max(1, os.cpu_count() or 1)
            rows = run_post_game_analysis(human_moves=moves, depth=16, threads=threads)
            analysis_queue.put(rows)

        analysis_thread = threading.Thread(target=analysis_worker, args=(list(human_moves),), daemon=True)
        analysis_thread.start()
        engine_thinking = False

    running = True
    while running:
        clock.tick(FPS)
        if engine_thinking:
            if engine_queue.qsize() > 0:
                mv = engine_queue.get()
                apply_move(mv, is_human=False)
                engine_thinking = False
        if state == "analysis":
            if analysis_queue.qsize() > 0:
                res = analysis_queue.get()
                analysis_rows = res
                status_msg = "Analysis ready"
        if state == "playing":
            begin_engine_move_if_needed()
            maybe_finish_game()

        for event in pygame.event.get():
            if event.type == EVT_QUIT:
                running = False
                break

            if state == "setup":
                any_open = opponent_dd.open or color_dd.open or option_dd.open
                if any_open:
                    active = opponent_dd if opponent_dd.open else (color_dd if color_dd.open else option_dd)
                    changed = active.handle_event(event)
                    if active is opponent_dd:
                        color_dd.open = False
                        option_dd.open = False
                    elif active is color_dd:
                        opponent_dd.open = False
                        option_dd.open = False
                    else:
                        opponent_dd.open = False
                        color_dd.open = False

                    if active is opponent_dd and changed is not None:
                        update_option_dropdown()
                    continue

                changed = opponent_dd.handle_event(event)
                if changed is not None:
                    update_option_dropdown()

                if opponent_dd.open:
                    color_dd.open = False
                    option_dd.open = False

                color_dd.handle_event(event)
                if color_dd.open:
                    opponent_dd.open = False
                    option_dd.open = False

                option_dd.handle_event(event)
                if option_dd.open:
                    opponent_dd.open = False
                    color_dd.open = False

                if start_btn.handle_event(event):
                    start_game()

            elif state in ("playing", "analysis"):
                if state == "analysis":
                    analysis_new_btn = Button(rect=_analysis_new_game_button_rect(), text="New Game", enabled=True)
                    if analysis_new_btn.handle_event(event):
                        reset_to_setup()
                        update_option_dropdown()
                        continue

                if game_menu_dd.open:
                    sel = game_menu_dd.handle_event(event)
                    if sel == "New Game":
                        reset_to_setup()
                        update_option_dropdown()
                        continue
                    continue

                if game_menu_dd.handle_event(event) == "New Game":
                    reset_to_setup()
                    update_option_dropdown()
                    continue

                if undo_btn.handle_event(event) and state == "playing":
                    undo_one_ply()

                if event.type == EVT_MOUSEWHEEL:
                    mx, my = pygame.mouse.get_pos()
                    hist_rect = pygame.Rect(panel_origin[0], panel_origin[1] + 110, panel_w, height - (panel_origin[1] + 110) - margin)
                    if state == "analysis":
                        analysis_scroll = max(0, analysis_scroll - event.y * 20)
                    elif hist_rect.collidepoint(mx, my):
                        history_scroll = max(0, history_scroll - event.y * 20)

                if state == "playing":
                    if board.turn == human_color and not engine_thinking:
                        if event.type == EVT_MOUSEBUTTONDOWN and event.button == 1:
                            sq = _screen_to_square(event.pos, origin=board_origin, square_size=square_size, human_color=human_color)
                            if sq is None:
                                selected_sq = None
                                legal_dests = []
                                continue

                            if selected_sq is None:
                                piece = board.piece_at(sq)
                                if piece is None or piece.color != human_color:
                                    continue
                                selected_sq = sq
                                legal_dests = [m.to_square for m in board.legal_moves if m.from_square == sq]
                            else:
                                move = chess.Move(selected_sq, sq)
                                move = _coerce_promotion(board, move)
                                if move in board.legal_moves:
                                    apply_move(move, is_human=True)
                                else:
                                    piece = board.piece_at(sq)
                                    if piece is not None and piece.color == human_color:
                                        selected_sq = sq
                                        legal_dests = [m.to_square for m in board.legal_moves if m.from_square == sq]
                                    else:
                                        selected_sq = None
                                        legal_dests = []

        screen.fill((20, 20, 20))

        if state == "setup":
            pygame.draw.rect(screen, PANEL_BG, pygame.Rect(panel_origin[0], panel_origin[1], panel_w, board_px))
            title = font.render("Game Setup", True, TEXT)
            screen.blit(title, (panel_origin[0], panel_origin[1] + 6))

            dds = [opponent_dd, color_dd, option_dd]
            for d in dds:
                d.draw_base(screen, font)

            start_btn.draw(screen, font)

            hint = small.render("Choose opponent + option + color, then Start.", True, SUBTEXT)
            hint_y = start_btn.rect.bottom + 8
            screen.blit(hint, (panel_origin[0], hint_y))

            if status_msg:
                msg = small.render(status_msg, True, (255, 210, 120))
                screen.blit(msg, (panel_origin[0], hint_y + hint.get_height() + 6))

            _draw_board(
                screen,
                board=chess.Board(),
                origin=board_origin,
                square_size=square_size,
                human_color=chess.WHITE,
                images=images,
                selected_square=None,
                legal_dests=[],
            )

            open_dd = next((d for d in dds if d.open), None)
            if open_dd is not None:
                open_dd.draw_menu(screen, font)

        else:
            _draw_board(
                screen,
                board=board,
                origin=board_origin,
                square_size=square_size,
                human_color=human_color,
                images=images,
                selected_square=selected_sq,
                legal_dests=legal_dests,
            )
            pygame.draw.rect(screen, PANEL_BG, pygame.Rect(panel_origin[0], panel_origin[1], panel_w, board_px))
            game_menu_dd.draw_base(screen, font)
            if state == "playing":
                undo_btn.enabled = True
            else:
                undo_btn.enabled = False
            undo_btn.draw(screen, font)
            cap_y = panel_origin[1] + 100
            cap_title = font.render("Captured", True, TEXT)
            screen.blit(cap_title, (panel_origin[0], cap_y))
            wlab = small.render("White captured:", True, SUBTEXT)
            screen.blit(wlab, (panel_origin[0], cap_y + 24))
            x0 = panel_origin[0]
            y0 = cap_y + 44
            for i, code in enumerate(captured_by_white[-16:]):
                img = mini_images.get(code)
                if img:
                    screen.blit(img, (x0 + (i % 8) * 34, y0 + (i // 8) * 34))
            blab = small.render("Black captured:", True, SUBTEXT)
            screen.blit(blab, (panel_origin[0], cap_y + 120))
            x1 = panel_origin[0]
            y1 = cap_y + 140
            for i, code in enumerate(captured_by_black[-16:]):
                img = mini_images.get(code)
                if img:
                    screen.blit(img, (x1 + (i % 8) * 34, y1 + (i // 8) * 34))
            hist_y = cap_y + 220
            hist_title = font.render("Move History", True, TEXT)
            screen.blit(hist_title, (panel_origin[0], hist_y))

            hist_rect = pygame.Rect(panel_origin[0], hist_y + 28, panel_w, board_px - (hist_y + 28 - panel_origin[1]) - 10)
            pygame.draw.rect(screen, (45, 45, 45), hist_rect)
            pygame.draw.rect(screen, (80, 80, 80), hist_rect, width=1)
            lines: List[str] = []
            for i in range(0, len(move_san), 2):
                w = move_san[i] if i < len(move_san) else ""
                b = move_san[i + 1] if i + 1 < len(move_san) else ""
                lines.append(f"{(i // 2) + 1}. {w}  {b}")

            clip = screen.get_clip()
            screen.set_clip(hist_rect)
            y = hist_rect.y + 6 - history_scroll
            for ln in lines:
                s = small.render(ln, True, TEXT)
                screen.blit(s, (hist_rect.x + 6, y))
                y += s.get_height() + 4
            screen.set_clip(clip)
            if status_msg:
                s = small.render(status_msg, True, (255, 210, 120))
                screen.blit(s, (panel_origin[0], panel_origin[1] + board_px - 20))
            if state == "playing" and engine_thinking:
                overlay = pygame.Surface((board_px, 40), SRCALPHA)
                overlay.fill((0, 0, 0, 160))
                screen.blit(overlay, (board_origin[0], board_origin[1] + board_px // 2 - 20))
                t = font.render("Engine thinking...", True, TEXT)
                screen.blit(t, (board_origin[0] + board_px // 2 - t.get_width() // 2, board_origin[1] + board_px // 2 - t.get_height() // 2))
            if state == "analysis":
                overlay = pygame.Surface((width, height), SRCALPHA)
                overlay.fill((0, 0, 0, 180))
                screen.blit(overlay, (0, 0))

                panel = pygame.Rect(margin, margin, width - 2 * margin, height - 2 * margin)
                pygame.draw.rect(screen, (30, 30, 30), panel, border_radius=6)
                pygame.draw.rect(screen, (90, 90, 90), panel, width=1, border_radius=6)

                title = font.render("Post-Game Analysis (Human moves)", True, TEXT)
                screen.blit(title, (panel.x + 12, panel.y + 10))
                hint = small.render("Mouse wheel to scroll.", True, SUBTEXT)
                screen.blit(hint, (panel.x + 12, panel.y + 34))

                analysis_new_btn = Button(rect=_analysis_new_game_button_rect(), text="New Game", enabled=True)
                analysis_new_btn.draw(screen, small)

                inner = pygame.Rect(panel.x + 12, panel.y + 60, panel.w - 24, panel.h - 72)
                pygame.draw.rect(screen, (40, 40, 40), inner)

                clip = screen.get_clip()
                screen.set_clip(inner)
                y = inner.y + 8 - analysis_scroll

                if analysis_rows:
                    for row in analysis_rows:
                        delta = row.best_eval_cp - row.played_eval_cp
                        ln = (
                            f"{row.ply_index + 1}. {row.san} | played: {row.played_eval_cp:+.0f}cp | "
                            f"best: {row.best_san} ({row.best_eval_cp:+.0f}cp) | Δ {delta:+.0f}cp"
                        )
                        s = small.render(ln, True, TEXT)
                        screen.blit(s, (inner.x + 8, y))
                        y += s.get_height() + 6
                else:
                    s = small.render(status_msg or "Analyzing...", True, TEXT)
                    screen.blit(s, (inner.x + 8, y))

                screen.set_clip(clip)
            if game_menu_dd.open:
                game_menu_dd.draw_menu(screen, font)

        pygame.display.flip()

    _pygame_quit()


if __name__ == "__main__":
    main()
