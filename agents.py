from abc import ABC, abstractmethod
from random import randrange
from typing import Optional

from heuristics import WIN_SCORE, DRAW_SCORE, evaluate
from my_chess import Color


class Agent(ABC):
    def __init__(self, name: str,  color: 'Color'):
        self.name = name
        self.color = color

    @abstractmethod
    def choose_move(self, board: 'Board') -> Optional['Move']:
        pass

# Agent này sẽ chọn ngẫu nhiên 1 nước đi từ các nước đi hợp lệ
class RandomAgent(Agent):
    def choose_move(self, board: 'Board') -> Optional['Move']:
        choice: Optional['Move'] = None
        for i, mv in enumerate(board.get_legal_moves(), start=1):
            # Xác suất 1/i chọn mv hiện tại => đảm bảo đều nhau
            if randrange(i) == 0:
                choice = mv
        return choice


# Dùng giải thuật minimax với hàm đánh giá là đếm số lượng quân cờ rồi tính tổng điểm
class MinimaxAgent(Agent):
    def __init__(self, name: str, color: 'Color', depth: int = 3):
        super().__init__(name, color)
        self.depth = depth

    def choose_move(self, board: 'Board') -> Optional['Move']:
        best_move = None
        best_val = float("-inf") if self.color == Color.WHITE else float("inf")
        maximizing = self.color == Color.WHITE

        for move in board.get_legal_moves():
            board.push_move(move)
            eval = self._minimax(board, self.depth - 1, not maximizing)
            board.pop_move()

            if maximizing and eval > best_val:
                best_val = eval
                best_move = move
            elif not maximizing and eval < best_val:
                best_val = eval
                best_move = move

        return best_move

    def _minimax(self, board: 'Board', depth: int, maximizing: bool) -> int:
        result = board.get_result()
        if result is not None:
            return WIN_SCORE if result == "WHITE_WIN" else -WIN_SCORE if result == "BLACK_WIN" else DRAW_SCORE

        if depth == 0:
            return evaluate(board)

        if maximizing:
            max_eval = float("-inf")
            for move in board.get_legal_moves():
                board.push_move(move)
                eval = self._minimax(board, depth - 1, False)
                board.pop_move()
                max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = float("inf")
            for move in board.get_legal_moves():
                board.push_move(move)
                eval = self._minimax(board, depth - 1, True)
                board.pop_move()
                min_eval = min(min_eval, eval)
            return min_eval



class AlphaBetaAgent(Agent):
    def __init__(self, name: str, color: 'Color', depth: int = 3):
        super().__init__(name, color)
        self.depth = depth

    def choose_move(self, board: 'Board') -> Optional['Move']:
        best_move = None
        best_val = float("-inf") if self.color == Color.WHITE else float("inf")
        maximizing = self.color == Color.WHITE

        for move in board.get_legal_moves():
            board.push_move(move)
            eval = self._minimax(board, self.depth - 1, float("-inf"), float("inf"), not maximizing)
            board.pop_move()

            if maximizing and eval > best_val:
                best_val = eval
                best_move = move
            elif not maximizing and eval < best_val:
                best_val = eval
                best_move = move

        return best_move

    def _minimax(self, board: 'Board', depth: int, alpha: float, beta: float, maximizing: bool) -> int:
        result = board.get_result()
        if result is not None:
            return WIN_SCORE if result == "WHITE_WIN" else -WIN_SCORE if result == "BLACK_WIN" else DRAW_SCORE

        if depth == 0:
            return evaluate(board)

        if maximizing:
            max_eval = float("-inf")
            for move in board.get_legal_moves():
                board.push_move(move)
                eval = self._minimax(board, depth - 1, alpha, beta, False)
                board.pop_move()
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float("inf")
            for move in board.get_legal_moves():
                board.push_move(move)
                eval = self._minimax(board, depth - 1, alpha, beta, True)
                board.pop_move()
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval
