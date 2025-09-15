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
            eval = minimax(board, self.depth - 1, not maximizing)
            board.pop_move()

            if maximizing and eval > best_val:
                best_val = eval
                best_move = move
            elif not maximizing and eval < best_val:
                best_val = eval
                best_move = move

        return best_move



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
            eval = alpha_beta(board, self.depth - 1, float("-inf"), float("inf"), not maximizing)
            board.pop_move()

            if maximizing and eval > best_val:
                best_val = eval
                best_move = move
            elif not maximizing and eval < best_val:
                best_val = eval
                best_move = move

        return best_move



def minimax(board, depth, maximizing) -> int:
    # Nếu đạt độ sâu giới hạn hoặc ván cờ đã kết thúc (chiếu hết, hòa, v.v.)
    # thì trả về giá trị đánh giá của bàn cờ hiện tại
    if depth == 0 or board.is_game_over():
        return evaluate(board)

    if maximizing:
        # Người chơi MAX cố gắng tối đa hóa giá trị
        max_eval = float("-inf")
        for move in board.get_legal_moves():  # Duyệt tất cả các nước đi hợp lệ
            board.push_move(move)            # Thực hiện nước đi
            eval = minimax(board, depth - 1, False)  # Đệ quy sang lượt MIN
            board.pop_move()                 # Hoàn tác nước đi để thử nước khác
            max_eval = max(max_eval, eval)   # Chọn giá trị lớn nhất trong các nước đi
        return max_eval
    else:
        # Người chơi MIN cố gắng tối thiểu hóa giá trị
        min_eval = float("inf")
        for move in board.get_legal_moves():  # Duyệt tất cả các nước đi hợp lệ
            board.push_move(move)             # Thực hiện nước đi
            eval = minimax(board, depth - 1, True)  # Đệ quy sang lượt MAX
            board.pop_move()                  # Hoàn tác nước đi
            min_eval = min(min_eval, eval)    # Chọn giá trị nhỏ nhất trong các nước đi
        return min_eval


def alpha_beta(board, depth, alpha, beta, maximizing) -> int:
    # Nếu đạt độ sâu giới hạn hoặc ván cờ đã kết thúc (chiếu hết, hòa, v.v.)
    # thì trả về giá trị đánh giá của bàn cờ hiện tại
    if depth == 0 or board.is_game_over():
        return evaluate(board)

    if maximizing:
        # Người chơi MAX muốn tối đa hóa giá trị
        max_eval = float("-inf")
        for move in board.get_legal_moves():  # Duyệt tất cả các nước đi hợp lệ
            board.push_move(move)  # Thực hiện nước đi
            eval = alpha_beta(board, depth - 1, alpha, beta, False)  # Đệ quy sang lượt MIN
            board.pop_move()  # Hoàn tác nước đi
            max_eval = max(max_eval, eval)  # Cập nhật giá trị lớn nhất
            alpha = max(alpha, eval)  # Cập nhật ngưỡng alpha (giá trị tốt nhất của MAX)
            if beta <= alpha: # Nếu alpha >= beta thì cắt tỉa (không cần xét thêm các nhánh khác)
                break
        return max_eval

    else:
        # Người chơi MIN muốn tối thiểu hóa giá trị
        min_eval = float("inf")
        for move in board.get_legal_moves():  # Duyệt tất cả các nước đi hợp lệ
            board.push_move(move)  # Thực hiện nước đi
            eval = alpha_beta(board, depth - 1, alpha, beta, True)  # Đệ quy sang lượt MAX
            board.pop_move()  # Hoàn tác nước đi
            min_eval = min(min_eval, eval)  # Cập nhật giá trị nhỏ nhất
            beta = min(beta, eval)  # Cập nhật ngưỡng beta (giá trị tốt nhất của MIN)
            if beta <= alpha:  # Nếu beta <= alpha thì cắt tỉa (không cần xét thêm các nhánh khác)
                break
        return min_eval
