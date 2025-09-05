from agents import MinimaxAgent, RandomAgent
from my_chess import Board, Color

if __name__ == "__main__":
    board = Board()
    agent01 = RandomAgent("Ximofam", Color.WHITE)
    agent02 = MinimaxAgent("VIENTHUHAI", Color.BLACK)

    print(board)

    while True:
        curr_player = agent01 if agent01.color == board.turn else agent02

        if board.get_result():
            print(board.get_result())
            break

        move = curr_player.choose_move(board)

        board.push_move(move)


        print('================')
        print(board)
        print(f'{curr_player.name} move: {move.to_uci()}')




