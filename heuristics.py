from collections import defaultdict
from typing import Tuple

from my_chess import PieceType, Color

WIN_SCORE = 1_000_000
DRAW_SCORE = 0

# --- Giá trị quân (centipawn) ---
PIECE_VALUES = {
    PieceType.PAWN: 100,
    PieceType.KNIGHT: 320,
    PieceType.BISHOP: 330,
    PieceType.ROOK: 500,
    PieceType.QUEEN: 900,
    PieceType.KING: 20000
}

# --- Piece-Square Tables (PST) cho trắng ---
PAWN_TABLE = [
     0,  0,  0,  0,  0,  0,  0,  0,
    50, 50, 50, 50, 50, 50, 50, 50,
    10, 10, 20, 30, 30, 20, 10, 10,
     5,  5, 10, 25, 25, 10,  5,  5,
     0,  0,  0, 20, 20,  0,  0,  0,
     5, -5,-10,  0,  0,-10, -5,  5,
     5, 10, 10,-20,-20, 10, 10,  5,
     0,  0,  0,  0,  0,  0,  0,  0
]

KNIGHT_TABLE = [
   -50,-40,-30,-30,-30,-30,-40,-50,
   -40,-20,  0,  0,  0,  0,-20,-40,
   -30,  0, 10, 15, 15, 10,  0,-30,
   -30,  5, 15, 20, 20, 15,  5,-30,
   -30,  0, 15, 20, 20, 15,  0,-30,
   -30,  5, 10, 15, 15, 10,  5,-30,
   -40,-20,  0,  5,  5,  0,-20,-40,
   -50,-40,-30,-30,-30,-30,-40,-50
]

BISHOP_TABLE = [
   -20,-10,-10,-10,-10,-10,-10,-20,
   -10,  0,  0,  0,  0,  0,  0,-10,
   -10,  0,  5, 10, 10,  5,  0,-10,
   -10,  5,  5, 10, 10,  5,  5,-10,
   -10,  0, 10, 10, 10, 10,  0,-10,
   -10, 10, 10, 10, 10, 10, 10,-10,
   -10,  5,  0,  0,  0,  0,  5,-10,
   -20,-10,-10,-10,-10,-10,-10,-20
]

ROOK_TABLE = [
     0,  0,  0,  0,  0,  0,  0,  0,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
     5, 10, 10, 10, 10, 10, 10,  5,
     0,  0,  0,  0,  0,  0,  0,  0
]

QUEEN_TABLE = [
   -20,-10,-10, -5, -5,-10,-10,-20,
   -10,  0,  0,  0,  0,  0,  0,-10,
   -10,  0,  5,  5,  5,  5,  0,-10,
    -5,  0,  5,  5,  5,  5,  0, -5,
     0,  0,  5,  5,  5,  5,  0, -5,
   -10,  5,  5,  5,  5,  5,  0,-10,
   -10,  0,  5,  0,  0,  0,  0,-10,
   -20,-10,-10, -5, -5,-10,-10,-20
]

KING_TABLE = [
   -30,-40,-40,-50,-50,-40,-40,-30,
   -30,-40,-40,-50,-50,-40,-40,-30,
   -30,-40,-40,-50,-50,-40,-40,-30,
   -30,-40,-40,-50,-50,-40,-40,-30,
   -20,-30,-30,-40,-40,-30,-30,-20,
   -10,-20,-20,-20,-20,-20,-20,-10,
    20, 20,  0,  0,  0,  0, 20, 20,
    20, 30, 10,  0,  0, 10, 30, 20
]

# --- Piece square table ---
PST = {
    PieceType.PAWN: PAWN_TABLE,
    PieceType.KNIGHT: KNIGHT_TABLE,
    PieceType.BISHOP: BISHOP_TABLE,
    PieceType.ROOK: ROOK_TABLE,
    PieceType.QUEEN: QUEEN_TABLE,
    PieceType.KING: KING_TABLE,
}

# --- Bonus kiểm soát trung tâm ---
CENTER_SQUARES = {(3,3), (3,4), (4,3), (4,4)}  # d4, e4, d5, e5


def pst_value(piece, file, rank) -> int:
    table = PST.get(piece.piece_type)
    idx = (rank * 8 + file) if piece.color == Color.WHITE else ((7 - rank) * 8 + file)
    return table[idx]



def king_safety_value(pos, color: Color, pawns) -> int: # pieces là ds (piece, (file, rank))
    if pos == None:
        return -100000

    kf, kr = pos
    score = 0

    # Thưởng nhập thành
    if color == Color.WHITE:
        if (kf, kr) in ((6, 0), (2, 0)):
            score += 30
    else:
        if (kf, kr) in ((6, 7), (2, 7)):
            score += 30

    # Pawn shield
    direction = 1 if color == Color.WHITE else -1
    for dx in (-1, 0, 1):
        nx, ny = kf + dx, kr + direction
        if 0 <= nx < 8 and 0 <= ny < 8:
            if (nx, ny) in pawns:
                score += 10
            else:
                score -= 5

    return score




def evaluate(board: 'Board') -> int:
    score = 0

    white_king = None
    black_king = None

    white_pawn_files = set()
    black_pawn_files = set()

    white_pawns = []
    black_pawns = []

    for file in range(8):
        for rank in range(8):
            p = board.piece_at(file, rank)
            if p is None:
                continue

            is_white = p.color == Color.WHITE

            material = PIECE_VALUES[p.piece_type]
            score += material if is_white else -material

            pst = pst_value(p, file, rank)
            score += pst if is_white else -pst

            if p.piece_type == PieceType.KING:
                if is_white:
                    white_king = (file, rank)
                else:
                    black_king = (file, rank)
                continue

            if p.piece_type != PieceType.PAWN:
                continue

            # Nếu tốt chồng thì bị trừ 10 điểm
            if is_white:
                white_pawns.append((file, rank))
                if file in white_pawn_files:
                    score -= 10
                else:
                    white_pawn_files.add(file)
            else:
                black_pawns.append((file, rank))
                if file in black_pawn_files:
                    score += 10
                else:
                    black_pawn_files.add(file)


    # Nếu bị cô lập thì trừ 15 điểm
    for file, _ in white_pawns:
        if (file - 1 not in white_pawn_files) and (file + 1 not in white_pawn_files):
            score -= 15

    for file, _ in black_pawns:
        if (file - 1 not in black_pawn_files) and (file + 1 not in black_pawn_files):
            score += 15

    score += king_safety_value(white_king, Color.WHITE, white_pawns) - \
            king_safety_value(black_king, Color.BLACK, black_pawns)

    return score


