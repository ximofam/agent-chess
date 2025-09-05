from typing import List, Tuple, Optional, Iterator

from .move import Move
from .piece import Piece, Color, PieceType, opposite, PIECE_TO_SYMBOL


class Board:
    def __init__(self):
        self.state: List[List[Optional[Piece]]] = [[None] * 8 for _ in range(8)]
        self._stack_move = []
        self.turn = Color.WHITE

        # Khởi tạo init state
        board = [
            ['R', 'P', '.', '.', '.', '.', 'p', 'r'],
            ['N', 'P', '.', '.', '.', '.', 'p', 'n'],
            ['B', 'P', '.', '.', '.', '.', 'p', 'b'],
            ['Q', 'P', '.', '.', '.', '.', 'p', 'q'],
            ['K', 'P', '.', '.', '.', '.', 'p', 'k'],
            ['B', 'P', '.', '.', '.', '.', 'p', 'b'],
            ['N', 'P', '.', '.', '.', '.', 'p', 'n'],
            ['R', 'P', '.', '.', '.', '.', 'p', 'r']
        ]

        for rank in range(8):
            for file in range(8):
                if board[file][rank] != '.':
                    self.state[file][rank] = Piece.from_symbol(board[file][rank])


    def __repr__(self):
        rows = []
        for rank in range(7, -1, -1):  # In từ hàng 8 xuống 1
            row = []
            for file in range(8):
                piece = self.state[file][rank]
                row.append(piece.symbol() if piece else '.')  # '.' cho ô trống
            rows.append(str(rank + 1) + ' ' + ' '.join(row))
        # Thêm hàng file chữ cái
        rows.append('  ' + ' '.join('abcdefgh'))
        return '\n'.join(rows)


    def in_bounds(self, file: int, rank: int) -> bool:
        return 0 <= file < 8 and 0 <= rank < 8

    def set_piece_at(self, pos: Tuple[int, int], piece: Piece | None):
        file, rank = pos
        self.state[file][rank] = piece

    def piece_at(self, file: int, rank: int) -> Optional[Piece]:
        return None if not self.in_bounds(file, rank) else self.state[file][rank]

    def is_legal_move(self, move: Move) -> bool:
        return move in self.get_legal_moves()

    #def push_move(self, move: Move):
        # # Lấy 2 quân cờ tại điểm bắt đầu và điểm đến
        # piece = self.piece_at(*move.from_pos)
        # target = self.piece_at(*move.to_pos)
        #
        # # Di chuyển quân cờ
        # self.set_piece_at(move.to_pos, piece)
        # self.set_piece_at(move.from_pos, None)
        #
        # # Set quân cờ di chuyển và quân bị ăn và color vào move xong lưu lại vào stack
        # move.piece = piece
        # move.captured = target
        # self._stack_move.append(move)
        #
        # self.turn = opposite(self.turn)

    def push_move(self, move: Move):

        piece = self.piece_at(*move.from_pos)
        target = self.piece_at(*move.to_pos)

        # Nhập thành
        if move.is_castling:
            fx, fy = move.from_pos
            tx, ty = move.to_pos
            if tx == 6:  # king-side
                rook = self.piece_at(7, fy)
                self.set_piece_at((5, fy), rook)
                self.set_piece_at((7, fy), None)
                rook.has_moved = True
            elif tx == 2:  # queen-side
                rook = self.piece_at(0, fy)
                self.set_piece_at((3, fy), rook)
                self.set_piece_at((0, fy), None)
                rook.has_moved = True

        # Di chuyển
        self.set_piece_at(move.to_pos, piece)
        self.set_piece_at(move.from_pos, None)

        # Phong tốt
        if move.promotion:
            self.set_piece_at(move.to_pos, Piece.from_symbol(move.promotion))


        move.piece = piece
        move.captured = target
        self._stack_move.append(move)

        if piece:
            piece.has_moved = True

        self.turn = opposite(self.turn)

    def pop_move(self) -> Optional[Move]:
        if not self._stack_move:
            return None
        # Lấy move cuối cùng
        move = self._stack_move.pop()

        # Undo nhập thành
        if move.is_castling:
            fx, fy = move.from_pos
            tx, ty = move.to_pos
            if tx == 6:  # kingside
                rook = self.piece_at(5, fy)
                self.set_piece_at((7, fy), rook)
                self.set_piece_at((5, fy), None)
                if rook:
                    rook.has_moved = False
            elif tx == 2:  # queenside
                rook = self.piece_at(3, fy)
                self.set_piece_at((0, fy), rook)
                self.set_piece_at((3, fy), None)
                if rook:
                    rook.has_moved = False

        # Set các quân cờ lại vị trí cũ
        self.set_piece_at(move.to_pos, move.captured)
        self.set_piece_at(move.from_pos, move.piece)
        self.turn = opposite(self.turn)

        return move


    def find_king(self, color: Color) -> Tuple[int, int] | None:
        for file in range(8):
            for rank in range(8):
                piece = self.state[file][rank]
                if piece and piece.color == color and piece.name() == 'king':
                    return file, rank

        return None


    def is_check(self, color: Color) -> bool:
        king_pos = self.find_king(color)

        for move_of_opponent in self._get_legal_moves_of(opposite(color)):
            if move_of_opponent.to_pos == king_pos:
                return True

        return False


    def is_checkmate(self) -> bool:
        if not self.is_check(self.turn):
            return False

        color = self.turn

        for move in self._get_legal_moves_of(color):
            self.push_move(move)
            if not self.is_check(color):
                self.pop_move()
                return False

            self.pop_move()

        return True




    def is_stalemate(self) -> bool:
        if self.is_check(self.turn):
            return False

        return not any(self.get_legal_moves())

    def is_game_over(self) -> bool:
        return (not self.find_king(Color.WHITE) or
                not self.find_king(Color.BLACK) or
                self.is_checkmate() or
                self.is_stalemate())

    def get_result(self) -> str | None:
        if not self.find_king(Color.WHITE):
            return "BLACK_WIN"
        if not self.find_king(Color.BLACK):
            return 'WHITE_WIN'
        if self.is_checkmate():
            return "WHITE_WIN" if self.turn == Color.BLACK else "BLACK_WIN"
        if self.is_stalemate():
            return "DRAW"
        return None


    def get_legal_moves(self) -> Iterator[Move]:
        yield from self._get_legal_moves_of(self.turn)

    def _get_legal_moves_of(self, color: Color) -> Iterator[Move]:
        dispatch = {
            PieceType.PAWN: self._get_pawn_moves,
            PieceType.KNIGHT: self._get_knight_moves,
            PieceType.BISHOP: lambda pos, c: self._slide_moves(pos, c, [(1,1),(1,-1),(-1,1),(-1,-1)]),
            PieceType.ROOK:   lambda pos, c: self._slide_moves(pos, c, [(0,1),(0,-1),(-1,0),(1,0)]),
            PieceType.QUEEN:  lambda pos, c: self._slide_moves(pos, c, [(1,1),(1,-1),(-1,1),(-1,-1),(0,1),(0,-1),(-1,0),(1,0)]),
            PieceType.KING:   self._get_king_moves,
        }
        for file in range(8):
            for rank in range(8):
                piece = self.piece_at(file, rank)
                if piece and piece.color == color:
                    yield from dispatch[piece.piece_type]((file, rank), color)

    def _slide_moves(self, pos: Tuple[int,int], color: Color, directions: list[Tuple[int,int]]) -> Iterator[Move]:
        x, y = pos
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            while self.in_bounds(nx, ny):
                target = self.piece_at(nx, ny)
                if not target:
                    yield Move(pos, (nx, ny))
                else:
                    if target.color != color:
                        yield Move(pos, (nx, ny))
                    break
                nx, ny = nx + dx, ny + dy

    def _get_pawn_moves(self, pos: Tuple[int,int], color: Color) -> Iterator[Move]:
        x, y = pos
        direction = 1 if color == Color.WHITE else -1
        start_rank = 1 if color == Color.WHITE else 6
        promotion_rank = 7 if color == Color.WHITE else 0

        # Đi thẳng
        ny = y + direction
        if not self.piece_at(x, ny):
            #Phong quân
            if ny == promotion_rank:
                for promo in (PieceType.QUEEN, PieceType.ROOK, PieceType.BISHOP, PieceType.KNIGHT):
                    yield Move(pos, (x, ny), promotion=PIECE_TO_SYMBOL[(promo, self.turn)])
            else:
                yield Move(pos, (x, ny))
                # Đi 2 ô nếu ở vị trí bắt đầu
                if y == start_rank and not self.piece_at(x, y + 2 * direction):
                    yield Move(pos, (x, y + 2 * direction))

        # Ăn chéo
        for dx in (-1, 1):
            nx, ny = x + dx, y + direction
            target = self.piece_at(nx, ny)
            if self.in_bounds(nx, ny) and target and target.color != color:
                # Phong quân
                if ny == promotion_rank:
                    for promo in (PieceType.QUEEN, PieceType.ROOK, PieceType.BISHOP, PieceType.KNIGHT):
                        yield Move(pos, (nx, ny), promotion=PIECE_TO_SYMBOL[(promo, self.turn)])
                else:
                    yield Move(pos, (nx, ny))

    def _get_knight_moves(self, pos: Tuple[int,int], color: Color) -> Iterator[Move]:
        x, y = pos
        for dx, dy in [(1,2),(2,1),(2,-1),(1,-2),(-1,-2),(-2,-1),(-2,1),(-1,2)]:
            nx, ny = x + dx, y + dy
            target = self.piece_at(nx, ny)
            if self.in_bounds(nx, ny) and (not target or target.color != color):
                yield Move(pos, (nx, ny))

    def _get_king_moves(self, pos: Tuple[int,int], color: Color) -> Iterator[Move]:
        x, y = pos
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if dx == dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                target = self.piece_at(nx, ny)
                if self.in_bounds(nx, ny) and (not target or target.color != color):
                    yield Move(pos, (nx, ny))

        # ---- Nhập thành ----
        piece = self.piece_at(x, y)
        if not piece or piece.has_moved:
            return  # Vua đã di chuyển thì không nhập thành được

        # Vị trí xe phụ thuộc màu
        rank = 0 if color == Color.WHITE else 7

        # Nhập thành ngắn (king-side)
        rook = self.piece_at(7, rank)
        if rook and rook.piece_type == PieceType.ROOK and not rook.has_moved:
            if all(self.piece_at(f, rank) is None for f in (5, 6)):
                if not self.is_check(color):
                    # giả lập đi qua ô 5,6
                    self.push_move(Move((x, y), (5, rank)))
                    safe1 = not self.is_check(color)
                    self.pop_move()
                    self.push_move(Move((x, y), (6, rank)))
                    safe2 = not self.is_check(color)
                    self.pop_move()
                    if safe1 and safe2:
                        yield Move((x, y), (6, rank), is_castling=True)

        # Nhập thành dài (queen-side)
        rook = self.piece_at(0, rank)
        if rook and rook.piece_type == PieceType.ROOK and not rook.has_moved:
            if all(self.piece_at(f, rank) is None for f in (1, 2, 3)):
                if not self.is_check(color):
                    self.push_move(Move((x, y), (3, rank)))
                    safe1 = not self.is_check(color)
                    self.pop_move()
                    self.push_move(Move((x, y), (2, rank)))
                    safe2 = not self.is_check(color)
                    self.pop_move()
                    if safe1 and safe2:
                        yield Move((x, y), (2, rank), is_castling=True)
