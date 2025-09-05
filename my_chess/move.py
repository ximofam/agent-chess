from typing import Tuple, Optional


FILES = ["a", "b", "c", "d", "e", "f", "g", "h"]
RANKS = ["1", "2", "3", "4", "5", "6", "7", "8"]

def pos_to_square(x: int, y: int) -> str:
    return FILES[x] + RANKS[y]

def square_to_pos(square: str) -> Tuple[int, int]:
    return FILES.index(square[0]), RANKS.index(square[1])

class Move:
    def __init__(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int], piece: 'Piece' = None,
                 captured: 'Piece' = None, promotion: str=None, is_castling=False):
        self.from_pos = from_pos
        self.to_pos = to_pos
        self.promotion =  promotion
        self.piece = piece
        self.captured = captured
        self.is_castling = is_castling

    def to_uci(self) -> str:
        res = pos_to_square(*self.from_pos) + pos_to_square(*self.to_pos)
        if self.promotion:
            res += self.promotion
        return res

    def __repr__(self):
        return self.to_uci()

    @classmethod
    def from_uci(cls, uci: str) -> Optional['Move']:
        from_pos = square_to_pos(uci[:2])
        to_pos = square_to_pos(uci[2:4])

        move = cls(from_pos=from_pos, to_pos=to_pos)

        # Promotion
        if len(uci) == 5:
            move.promotion = uci[4]

        # # Nhận diện nhập thành
        # fx, fy = from_pos
        # tx, ty = to_pos
        # if (fy in (0, 7)  # rank vua
        #         and fx == 4  # cột e (x=4)
        #         and tx in (2, 6)  # cột c hoặc g
        #         and ty == fy):  # cùng hàng
        #     move.is_castling = True

        return move

    def __eq__(self, other):
        return (isinstance(other, Move)
                and (self.from_pos == other.from_pos and
                     self.to_pos == other.to_pos and
                     self.promotion == other.promotion and
                     self.is_castling == other.is_castling))
