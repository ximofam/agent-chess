from enum import Enum, auto
from typing import Optional


# định nghĩa enum màu của quân cờ
class Color(Enum):
    WHITE = auto()
    BLACK = auto()

def opposite(color: Color) -> Color:
    return Color.WHITE if color == Color.BLACK else Color.BLACK


# Định nghĩa loại quân cờ
class PieceType(Enum):
    PAWN = auto()
    KNIGHT = auto()
    BISHOP = auto()
    ROOK = auto()
    QUEEN = auto()
    KING = auto()

PIECE_TO_SYMBOL = {
    (PieceType.PAWN, Color.WHITE): "P",
    (PieceType.KNIGHT, Color.WHITE): "N",
    (PieceType.BISHOP, Color.WHITE): "B",
    (PieceType.ROOK, Color.WHITE): "R",
    (PieceType.QUEEN, Color.WHITE): "Q",
    (PieceType.KING, Color.WHITE): "K",

    (PieceType.PAWN, Color.BLACK): "p",
    (PieceType.KNIGHT, Color.BLACK): "n",
    (PieceType.BISHOP, Color.BLACK): "b",
    (PieceType.ROOK, Color.BLACK): "r",
    (PieceType.QUEEN, Color.BLACK): "q",
    (PieceType.KING, Color.BLACK): "k",
}
SYMBOL_TO_PIECE = {v: k for k, v in PIECE_TO_SYMBOL.items()}
PIECE_NAMES = [None, "pawn", "knight", "bishop", "rook", "queen", "king"]

class Piece:
    def __init__(self, piece_type: PieceType, color: Color):
        self.piece_type = piece_type
        self.color = color
        self.has_moved = False

    def symbol(self) -> str:
        return PIECE_TO_SYMBOL[(self.piece_type, self.color)]

    def name(self) -> str:
        return PIECE_NAMES[self.piece_type.value]

    @classmethod
    def from_symbol(cls, symbol: str) -> Optional['Piece']:
        if symbol not in SYMBOL_TO_PIECE:
            return None
        piece_type, color = SYMBOL_TO_PIECE[symbol]
        return cls(piece_type, color)

    def __repr__(self) -> str:
        return f"Piece({self.piece_type.name}, {self.color.name})"


