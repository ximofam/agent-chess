"""
Pygame GUI: Human (White) vs Agent (Black)
Structure: clean, modular, UI on the right, piece images with fallback to text.
"""

import os
import sys
import time
import pygame
from typing import Optional, Tuple, Dict

# Adjust imports to match your package layout
try:
    from my_chess import Board, Color, PieceType
    from my_chess.piece import PIECE_TO_SYMBOL
    from agents import RandomAgent, MinimaxAgent, AlphaBetaAgent
except Exception as e:
    print("Import error:", e)
    print("Hãy đảm bảo package my_chess và file agents.py có thể import được.")
    sys.exit(1)

# ---------------- Config ----------------
BOARD_SIZE = 640           # pixel size of board (square)
UI_WIDTH = 220             # width of UI panel on the right
WIDTH, HEIGHT = BOARD_SIZE + UI_WIDTH, BOARD_SIZE
SQUARE_SIZE = BOARD_SIZE // 8
FPS = 60

# Colors
LIGHT_SQ = (240, 217, 181)
DARK_SQ = (181, 136, 99)
HIGHLIGHT = (86, 180, 233)
SELECT = (246, 105, 65)
UI_BG = (240, 240, 240)
TEXT_COLOR = (30, 30, 30)
RESULT_COLOR = (200, 30, 30)

IMAGES_DIR = "images"      # folder with Chess_klt60.png etc.

# ---------------- Pygame init ----------------
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess - Human vs Agent")
clock = pygame.time.Clock()
FONT_LG = pygame.font.SysFont(None, 36)
FONT_MD = pygame.font.SysFont(None, 20)
FONT_SM = pygame.font.SysFont(None, 16)

# ---------------- Agents map ----------------
AGENTS = {
    "random": RandomAgent,
    "minimax": MinimaxAgent,
    "alpha-beta-pruning": AlphaBetaAgent
}

# ---------------- Globals (game state) ----------------
PIECE_IMAGES: Dict[str, pygame.Surface] = {}       # keyed by symbol like 'K' or 'k'
SCALED_CACHE: Dict[str, pygame.Surface] = {}       # cached scaled images to SQUARE_SIZE
board: Board
agent = None
HUMAN_COLOR = Color.WHITE
agent_mode = "minimax"
selected_sq = None
legal_moves_cache = []
last_ai_time = 0.0


# ---------------- Utilities ----------------
def board_coords_from_mouse(pos: Tuple[int, int]) -> Tuple[int, int]:
    x, y = pos
    if x >= BOARD_SIZE or y >= BOARD_SIZE:
        return -1, -1
    file = x // SQUARE_SIZE
    rank = 7 - (y // SQUARE_SIZE)
    return file, rank


def screen_center_from_square(file: int, rank: int) -> Tuple[int, int]:
    cx = file * SQUARE_SIZE + SQUARE_SIZE // 2
    cy = (7 - rank) * SQUARE_SIZE + SQUARE_SIZE // 2
    return cx, cy


def all_legal_moves(bd: Board):
    # ensure generator -> list for multiple iterations
    return list(bd.get_legal_moves())


# ---------------- Image loading ----------------
def load_images():
    PIECE_IMAGES.clear()
    SCALED_CACHE.clear()
    for color in list(Color):
        for ptype in list(PieceType):
            symbol = PIECE_TO_SYMBOL[(ptype, color)]  # e.g. 'K' or 'k'
            file_sym = symbol.lower()
            color_suffix = "d" if color == Color.BLACK else "l"
            filename = f"Chess_{file_sym}{color_suffix}t60.png"
            path = os.path.join(IMAGES_DIR, filename)
            try:
                img = pygame.image.load(path).convert_alpha()
                PIECE_IMAGES[symbol] = img
            except Exception:
                # missing image -> don't crash; fallback will render letter
                print(f"Warning: missing image '{path}', using text fallback.")
                PIECE_IMAGES[symbol] = None


def get_scaled_image(symbol: str):
    # return cached scaled image or scale and cache
    if symbol in SCALED_CACHE:
        return SCALED_CACHE[symbol]
    img = PIECE_IMAGES.get(symbol)
    if img:
        scaled = pygame.transform.smoothscale(img, (SQUARE_SIZE, SQUARE_SIZE))
        SCALED_CACHE[symbol] = scaled
        return scaled
    return None


# ---------------- Game functions ----------------
def new_game(mode: str = "minimax"):
    global board, agent, HUMAN_COLOR, agent_mode, selected_sq, legal_moves_cache, last_ai_time
    board = Board()
    HUMAN_COLOR = Color.WHITE
    AgentClass = AGENTS.get(mode, MinimaxAgent)
    # create agent with different params if needed
    if AgentClass is MinimaxAgent:
        agent = AgentClass("Vien Pham", Color.BLACK, depth=3)
    elif AgentClass is AlphaBetaAgent:
        agent = AgentClass("Bot", Color.BLACK, depth=3)
    else:
        agent = AgentClass("Ximofam", Color.BLACK)
    agent_mode = mode
    selected_sq = None
    legal_moves_cache = []
    last_ai_time = 0.0


def try_undo_pair():
    # undo up to two moves if possible
    if board.pop_move() is not None:
        board.pop_move()


# ---------------- Drawing ----------------
def draw_board(bd: Board, selected=None, legal_moves=None):
    # squares + pieces
    for file in range(8):
        for rank in range(8):
            light = (file + rank) % 2 == 0
            rect = pygame.Rect(file * SQUARE_SIZE, (7 - rank) * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            pygame.draw.rect(screen, LIGHT_SQ if light else DARK_SQ, rect)

            piece = bd.piece_at(file, rank)
            if piece:
                symbol = piece.symbol()
                img = get_scaled_image(symbol)
                if img:
                    screen.blit(img, rect)
                else:
                    # fallback text
                    text = FONT_LG.render(symbol, True, TEXT_COLOR)
                    screen.blit(text, text.get_rect(center=rect.center))

    # highlights
    if selected:
        fx, fy = selected
        rect = pygame.Rect(fx * SQUARE_SIZE, (7 - fy) * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
        pygame.draw.rect(screen, SELECT, rect, 4)

    if legal_moves:
        for mv in legal_moves:
            tx, ty = mv.to_pos
            cx, cy = screen_center_from_square(tx, ty)
            pygame.draw.circle(screen, HIGHLIGHT, (cx, cy), max(6, SQUARE_SIZE // 10))

    # file labels top & bottom, rank labels left & right
    files = "abcdefgh"
    for i in range(8):
        # bottom
        s = FONT_SM.render(files[i], True, TEXT_COLOR)
        bx = i * SQUARE_SIZE + SQUARE_SIZE // 2
        by = BOARD_SIZE - 10
        screen.blit(s, s.get_rect(center=(bx, by)))
        # top
        tx = i * SQUARE_SIZE + SQUARE_SIZE // 2
        ty = 10
        screen.blit(s, s.get_rect(center=(tx, ty)))

    for i in range(8):
        rtext = FONT_SM.render(str(i + 1), True, TEXT_COLOR)
        lx = 10
        ly = (7 - i) * SQUARE_SIZE + SQUARE_SIZE // 2
        screen.blit(rtext, rtext.get_rect(center=(lx, ly)))
        # right side
        rx = BOARD_SIZE - 10
        ry = (7 - i) * SQUARE_SIZE + SQUARE_SIZE // 2
        screen.blit(rtext, rtext.get_rect(center=(rx, ry)))


def draw_ui(bd: Board, agent_obj, mode: str, last_ai_sec: float):
    # panel background
    ui_rect = pygame.Rect(BOARD_SIZE, 0, UI_WIDTH, HEIGHT)
    pygame.draw.rect(screen, UI_BG, ui_rect)

    x0 = BOARD_SIZE + 12
    y = 12

    # Title
    screen.blit(FONT_LG.render("Game Info", True, TEXT_COLOR), (x0, y))
    y += 40

    # Turn
    turn = "WHITE" if bd.turn == Color.WHITE else "BLACK"
    screen.blit(FONT_MD.render(f"Turn: {turn}", True, TEXT_COLOR), (x0, y))
    y += 26

    # Agent mode & name
    name = getattr(agent_obj, "name", agent_obj.__class__.__name__)
    screen.blit(FONT_MD.render(f"Agent: {mode}", True, TEXT_COLOR), (x0, y))
    y += 20
    screen.blit(FONT_MD.render(f"Name: {name}", True, TEXT_COLOR), (x0, y))
    y += 28

    # Last AI time
    if last_ai_sec > 0:
        screen.blit(FONT_MD.render(f"AI last move: {last_ai_sec:.2f}s", True, TEXT_COLOR), (x0, y))
        y += 24

    # Controls
    screen.blit(FONT_MD.render("Controls:", True, TEXT_COLOR), (x0, y))
    y += 20
    controls = [
        "Click piece -> click target",
        "U : undo (undo 2 ply)",
        "R : restart",
        "1 : random agent",
        "2 : minimax agent",
        "3 : alpha-beta pruning agent"
    ]
    for c in controls:
        screen.blit(FONT_SM.render(c, True, TEXT_COLOR), (x0, y))
        y += 18

    # Result if any
    result = bd.get_result()
    if result:
        y = HEIGHT - 60
        screen.blit(FONT_LG.render("Result:", True, RESULT_COLOR), (x0, y))
        screen.blit(FONT_MD.render(result, True, RESULT_COLOR), (x0 + 10, y + 34))


# ---------------- Event handling ----------------
def handle_key(event):
    global agent_mode
    if event.key == pygame.K_u:
        try_undo_pair()
    elif event.key == pygame.K_r:
        new_game(agent_mode)
    elif event.key == pygame.K_1:
        agent_mode = "random"
        new_game(agent_mode)
    elif event.key == pygame.K_2:
        agent_mode = "minimax"
        new_game(agent_mode)
    elif event.key == pygame.K_3:
        agent_mode = "alpha-beta-pruning"
        new_game(agent_mode)


def handle_mouse(pos, button):
    global selected_sq, legal_moves_cache
    if button != 1:
        return
    if board.is_game_over():
        return
    file, rank = board_coords_from_mouse(pos)
    if file < 0:
        return
    # only allow human turn
    if board.turn != HUMAN_COLOR:
        return

    piece = board.piece_at(file, rank)
    if selected_sq is None:
        if piece and piece.color == HUMAN_COLOR:
            selected_sq = (file, rank)
            # compute legal moves for this piece and filter self-check
            legal_moves_cache = []
            for mv in all_legal_moves(board):
                if mv.from_pos == selected_sq:
                    board.push_move(mv)
                    ok = not board.is_check(HUMAN_COLOR)
                    board.pop_move()
                    if ok:
                        legal_moves_cache.append(mv)
            print(legal_moves_cache)
    else:
        # attempt to move selected -> clicked square
        dest = (file, rank)
        mv = next((m for m in legal_moves_cache if m.to_pos == dest), None)
        if mv:
            board.push_move(mv)
            # clear selection
            selected_sq = None
            legal_moves_cache = []
        else:
            # change selection if clicked another own piece
            if piece and piece.color == HUMAN_COLOR:
                selected_sq = (file, rank)
                legal_moves_cache = []
                for mv2 in all_legal_moves(board):
                    if mv2.from_pos == selected_sq:
                        board.push_move(mv2)
                        ok = not board.is_check(HUMAN_COLOR)
                        board.pop_move()
                        if ok:
                            legal_moves_cache.append(mv2)
            else:
                selected_sq = None
                legal_moves_cache = []


# ---------------- AI turn ----------------
def ai_move_if_needed():
    global last_ai_time
    if board.is_game_over():
        return
    if board.turn == HUMAN_COLOR:
        return
    start = time.perf_counter()
    mv = agent.choose_move(board)
    elapsed = time.perf_counter() - start
    last_ai_time = elapsed
    if mv:
        board.push_move(mv)


# ---------------- Main loop ----------------
def main_loop():
    running = True
    while running:
        clock.tick(FPS)
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                running = False
            elif ev.type == pygame.KEYDOWN:
                handle_key(ev)
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                handle_mouse(ev.pos, ev.button)

        # AI move (synchronous simple)
        ai_move_if_needed()

        # draw
        screen.fill((0, 0, 0))
        draw_board(board, selected_sq, legal_moves_cache)
        draw_ui(board, agent, agent_mode, last_ai_time)
        pygame.display.flip()

    pygame.quit()


# ---------------- Entry ----------------
if __name__ == "__main__":
    load_images()
    new_game(agent_mode)
    main_loop()
