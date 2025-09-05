from abc import ABC, abstractmethod
from random import randrange
from typing import Optional

from my_chess import PieceType, Color


class Agent(ABC):
    def __init__(self, name: str,  color: 'Color'):
        self.name = name
        self.color = color

    @abstractmethod
    def choose_move(self, board: 'Board') -> Optional['Move']:
        pass

class RandomAgent(Agent):

    def choose_move(self, board: 'Board') -> Optional['Move']:
        choice: Optional['Move'] = None
        for i, mv in enumerate(board.get_legal_moves(), start=1):
            # Xác suất 1/i chọn mv hiện tại => đảm bảo đều nhau
            if randrange(i) == 0:
                choice = mv
        return choice



class MinimaxAgent(Agent):

    _piece_values = {
        PieceType.PAWN: 1,
        PieceType.KNIGHT: 3,
        PieceType.BISHOP: 3,
        PieceType.ROOK: 5,
        PieceType.QUEEN: 9,
        PieceType.KING: 1000
    }

    def __init__(self, name: str, color: 'Color', depth: int = 3):
        super().__init__(name, color)
        self.depth = depth

    def choose_move(self, board: 'Board') -> Optional['Move']:
        best_move = None
        if self.color == Color.WHITE:
            best_val = float("-inf")
            for move in board.get_legal_moves():
                board.push_move(move)
                eval = self._minimax(board, self.depth - 1, False)
                board.pop_move()
                if eval > best_val:
                    best_val = eval
                    best_move = move
        else:  # Black (minimizing)
            best_val = float("inf")
            for move in board.get_legal_moves():
                board.push_move(move)
                eval = self._minimax(board, self.depth - 1, True)
                board.pop_move()
                if eval < best_val:
                    best_val = eval
                    best_move = move
        return best_move

    def evaluate(self, board: 'Board') -> int:
        score = 0
        for file in range(8):
            for rank in range(8):
                piece = board.piece_at(file, rank)
                if piece is not None:
                    val = self._piece_values[piece.piece_type]
                    score += val if piece.color == Color.WHITE else -val
        return score

    def _minimax(self, board: 'Board', depth: int, maximizing: bool) -> int:
        if depth == 0:
            return self.evaluate(board)

        legal_moves = board.get_legal_moves()
        if not legal_moves:
            return self.evaluate(board)

        if board.get_result():
            return self.evaluate(board)

        if maximizing:
            max_eval = float("-inf")
            for move in legal_moves:
                board.push_move(move)
                eval = self._minimax(board, depth - 1, False)
                board.pop_move()
                max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = float("inf")
            for move in legal_moves:
                board.push_move(move)
                eval = self._minimax(board, depth - 1, True)
                board.pop_move()
                min_eval = min(min_eval, eval)
            return min_eval