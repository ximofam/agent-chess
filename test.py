from agents import RandomAgent, MinimaxAgent, AlphaBetaAgent
from my_chess import Board, Color, Move

if __name__ == "__main__":
    board = Board()
    agent01 = RandomAgent("Ximofam", Color.WHITE)
    agent02 = AlphaBetaAgent("VIENTHUHAI", Color.BLACK)

    print(board)

    moves = [
        # Promotion sequence
        'e2e4', 'd7d5',
        'e4d5', 'c7c6',
        'd5c6', 'b7b5',
        'c6c7', 'b5b4',
        'c7b8R'
    ]

    while moves:
        move = Move.from_uci(moves.pop(0))

        if board.is_legal_move(move):
            board.push_move(move)


        print('================')
        print(board)


    print([move for move in board.get_legal_moves() if move.from_pos == (2, 6)])



