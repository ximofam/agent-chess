from agents import RandomAgent, MinimaxAgent, AlphaBetaAgent
from my_chess import Board, Color, Move

if __name__ == "__main__":
    board = Board()
    agent01 = RandomAgent("Ximofam", Color.BLACK)
    agent02 = AlphaBetaAgent("VIENTHUHAI", Color.WHITE)


    print(board)
    print("====================")

    while True:
        move = None
        name = ""
        if board.turn == agent01.color:
            move = agent01.choose_move(board)
            name = agent01.name
        else:
            move = agent02.choose_move(board)
            name = agent02.name

        board.push_move(move)
        print(board)
        print(f"{name} move: {move}")
        print("====================")

        result = board.get_result()
        if result is not None:
            print(result)
            break





