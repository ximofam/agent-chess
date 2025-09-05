"""
main_game.py
Pygame GUI: Human (White) vs Agent (Black)
- Expects your project's Board and agents to be importable:
    from chess.board import Board
    from agents import RandomAgent, MinimaxAgent
Adjust imports if your package layout differs.
"""
import os
import sys
import pygame
from typing import Optional, Tuple

from my_chess.piece import PIECE_TO_SYMBOL

# ---- Try to import user's modules (adjust paths if needed) ----
try:
    # Attempt imports matching the files you showed
    # Adjust these import paths if your project package name differs
    from my_chess import Board, Piece, Color, Move, PieceType
    from agents import RandomAgent, MinimaxAgent
except Exception as e:
    print("Không thể import module game từ project của bạn.")
    print("Lỗi import:", e)
    print("Hãy đảm bảo file `board.py`, `piece.py`, `move.py` nằm trong package `chess` và `agents.py` ở project root.")
    print("Bạn vẫn có thể sửa import paths ở đầu file main_game.py cho phù hợp.")
    sys.exit(1)

# ---- Configuration ----
WIDTH, HEIGHT = 640, 640
SQUARE_SIZE = WIDTH // 8
FPS = 30

WHITE_COLOR = (240, 217, 181)
BLACK_COLOR = (181, 136, 99)
HIGHLIGHT = (86, 180, 233)
SELECT = (246, 105, 65)
TEXT_COLOR = (20, 20, 20)


# ---- Utilities ----
def board_coords_from_mouse(pos: Tuple[int, int]) -> Tuple[int,int]:
    x, y = pos
    file = x // SQUARE_SIZE
    # Our Board.__repr__ prints rank 8 to 1 top to bottom; we assume board origin (0,0) is a1 at bottom-left visually.
    # We'll render rank 7 (top) -> index 7, so mouse y 0 should correspond to rank 7.
    rank = 7 - (y // SQUARE_SIZE)
    return file, rank

def screen_pos_from_square(file: int, rank: int) -> Tuple[int,int]:
    x = file * SQUARE_SIZE + SQUARE_SIZE // 2
    y = (7 - rank) * SQUARE_SIZE + SQUARE_SIZE // 2
    return x, y

# Try to get a printable symbol for a piece
def piece_text(piece) -> str:
    # If piece has symbol() use it. Else try name() and color to make letter.
    if piece is None:
        return ""
    try:
        s = piece.symbol()
        return s
    except Exception:
        try:
            name = piece.name()
            # Return uppercase single-char for white, lowercase for black
            ch = name[0].upper()
            return ch if piece.color.name == "WHITE" else ch.lower()
        except Exception:
            return "?"

# ---- Pygame setup ----
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT + 80))
pygame.display.set_caption("Chess - Human vs Agent")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 40)
small_font = pygame.font.SysFont(None, 22)

# ---- Game state ----
PIECE_IMAGES = {}

def load_images():
    for color in list(Color):
        for type in list(PieceType):
            symbol = PIECE_TO_SYMBOL[(type, color)]
            filename = f"Chess_{symbol.lower()}{'d' if color == Color.BLACK else 'l'}t60.png"
            path = os.path.join("images", filename)  # thư mục images/
            PIECE_IMAGES[symbol] = pygame.image.load(path)

load_images()

def new_game(agent_type: str = "minimax"):
    board = Board()
    # human plays WHITE
    human_color = Color.WHITE
    if agent_type == "random":
        agent = RandomAgent("Bot", Color.BLACK)
    else:
        agent = MinimaxAgent("Bot", Color.BLACK, depth=2)  # set depth shorter for speed
    return board, agent, human_color

# initial
agent_mode = "minimax"  # "random" or "minimax"
board, agent, HUMAN_COLOR = new_game(agent_mode)
selected: Optional[Tuple[int,int]] = None
legal_moves_cache = []  # list of Move for current selection

# Helper to get list from iterator safely
def list_moves_for_color(bd, color):
    return list(bd._get_legal_moves_of(color)) if hasattr(bd, "_get_legal_moves_of") else list(bd.get_legal_moves())

# Attempt to convert iterator to list for repeated scanning
def all_legal_moves(board):
    try:
        return list(board.get_legal_moves())
    except TypeError:
        # maybe is generator-like
        return list(board.get_legal_moves())

# Find a move object by from->to
def find_move_from_to(board, from_pos, to_pos):
    for m in all_legal_moves(board):
        if m.from_pos == from_pos and m.to_pos == to_pos:
            return m
    return None

def draw_board(bd: Board, selected_sq=None, legal_moves=None):
    # draw squares
    for file in range(8):
        for rank in range(8):
            color = WHITE_COLOR if (file + rank) % 2 == 0 else BLACK_COLOR
            rect = pygame.Rect(file * SQUARE_SIZE, (7 - rank) * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            pygame.draw.rect(screen, color, rect)

            piece = bd.piece_at(file, rank)
            if piece:
                img = PIECE_IMAGES[piece.symbol()]
                img = pygame.transform.smoothscale(img, (SQUARE_SIZE, SQUARE_SIZE))
                screen.blit(img, rect)

    # highlight selected
    if selected_sq:
        fx, fy = selected_sq
        sx = fx * SQUARE_SIZE
        sy = (7 - fy) * SQUARE_SIZE
        pygame.draw.rect(screen, SELECT, (sx, sy, SQUARE_SIZE, SQUARE_SIZE), 4)

    # highlight legal moves
    if legal_moves:
        for mv in legal_moves:
            tx, ty = mv.to_pos
            cx, cy = screen_pos_from_square(tx, ty)
            pygame.draw.circle(screen, HIGHLIGHT, (cx, cy), 12)

    # # draw pieces
    # for file in range(8):
    #     for rank in range(8):
    #         piece = bd.piece_at(file, rank)
    #         if piece:
    #             text = piece_text(piece)
    #             if text is None: text = "?"
    #             cx, cy = screen_pos_from_square(file, rank)
    #             # choose color for piece text
    #             color = TEXT_COLOR if getattr(piece, 'color', None) == HUMAN_COLOR else (10,10,60)
    #             surf = font.render(text, True, color)
    #             rect = surf.get_rect(center=(cx, cy))
    #             screen.blit(surf, rect)

def draw_ui(bd: Board, agent_mode: str):
    # bottom bar background
    pygame.draw.rect(screen, (230,230,230), (0, HEIGHT, WIDTH, 80))
    # text: turn, result
    turn_text = f"Turn: {'WHITE' if bd.turn == Color.WHITE else 'BLACK'}"
    t_surf = small_font.render(turn_text, True, (0,0,0))
    screen.blit(t_surf, (10, HEIGHT + 10))
    # agent mode
    mode_text = f"Agent: {agent_mode} (press 1=random, 2=minimax)"
    m_surf = small_font.render(mode_text, True, (0,0,0))
    screen.blit(m_surf, (10, HEIGHT + 30))
    # controls
    ctrl_text = "Click to move. u=undo, r=restart"
    c_surf = small_font.render(ctrl_text, True, (0,0,0))
    screen.blit(c_surf, (10, HEIGHT + 50))

    # show result if game over
    res = bd.get_result()
    if res:
        res_surf = font.render(f"Result: {res}", True, (200,30,30))
        screen.blit(res_surf, (WIDTH//2 - res_surf.get_width()//2, HEIGHT + 20))


# ---- Main loop ----
running = True
ai_thinking = False

while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_u:
                board.pop_move()
                board.pop_move()
                # after undo, ensure turn corresponds and clear selection
                selected = None
                legal_moves_cache = []
            elif event.key == pygame.K_r:
                board, agent, HUMAN_COLOR = new_game(agent_mode)
                selected = None
                legal_moves_cache = []
            elif event.key == pygame.K_1:
                agent_mode = "random"
                board, agent, HUMAN_COLOR = new_game(agent_mode)
            elif event.key == pygame.K_2:
                agent_mode = "minimax"
                board, agent, HUMAN_COLOR = new_game(agent_mode)

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if board.get_result():  # game over: ignore clicks
                continue

            mx, my = event.pos
            if my > HEIGHT:
                continue  # clicked UI area
            file, rank = board_coords_from_mouse((mx, my))

            # only allow human moves if it's human's turn
            if board.turn != HUMAN_COLOR:
                continue

            piece = board.piece_at(file, rank)
            if selected is None:
                # pick a piece belonging to human
                if piece and piece.color == HUMAN_COLOR:
                    selected = (file, rank)
                    # compute legal moves from this piece (but filter self-check)
                    legal_moves_cache = []
                    for mv in all_legal_moves(board):
                        if mv.from_pos == selected:
                            # simulate to ensure not leaving king in check
                            board.push_move(mv)
                            ok = (not board.is_check(HUMAN_COLOR))
                            board.pop_move()
                            if ok:
                                legal_moves_cache.append(mv)
                else:
                    # clicked empty or enemy -> do nothing
                    pass
            else:
                # attempt move selected -> (file,rank)
                dest = (file, rank)
                mv = None
                for cand in legal_moves_cache:
                    if cand.to_pos == dest:
                        mv = cand
                        break
                if mv:
                    board.push_move(mv)
                    selected = None
                    legal_moves_cache = []
                else:
                    # if clicked a different own piece, change selection
                    if piece and piece.color == HUMAN_COLOR:
                        selected = (file, rank)
                        legal_moves_cache = []
                        for mv2 in all_legal_moves(board):
                            if mv2.from_pos == selected:
                                board.push_move(mv2)
                                ok = (not board.is_check(HUMAN_COLOR))
                                board.pop_move()
                                if ok:
                                    legal_moves_cache.append(mv2)
                    else:
                        # clicked invalid target => deselect
                        selected = None
                        legal_moves_cache = []

    # AI move if it's AI's turn and game not over
    if (not board.get_result()) and board.turn != HUMAN_COLOR:
        # ask agent for a move
        ai_move = agent.choose_move(board)
        if ai_move:
            board.push_move(ai_move)
        else:
            # no move -> pass (should be game over)
            pass

    # Draw everything
    screen.fill((0,0,0))
    draw_board(board, selected, legal_moves_cache)
    draw_ui(board, agent_mode)
    pygame.display.flip()

pygame.quit()
