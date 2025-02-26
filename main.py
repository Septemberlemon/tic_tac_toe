from chess_board import ChessBoard


epochs = 10000
board = ChessBoard()


for epoch in range(epochs):
    board.clear()
    chess = 2
    last_num_state = None
    last_action = None
    while board.currentState == 0:
        chess = 3 - chess
        num_state = board.numState
        # board.showQValues()
        action = board.placeABestChessPiece(chess, rand=True, explore_rate=1)
        # board.show()
        current_state = board.currentState
        if current_state == chess:
            board.update_q_table(last_num_state, last_action, "lose")
            board.update_q_table(num_state, action, "won")
        elif current_state == 3:
            board.update_q_table(last_num_state, last_action, "draw")
            board.update_q_table(num_state, action, "draw")
        else:
            board.update_q_table(last_num_state, last_action, board.numState)
        last_num_state = num_state
        last_action = action

    print(f"epoch {epoch} ===================")
board.save_q_table("checkpoints/1.pt")

while True:
    board.clear()
    player_chess = int(input("输入所执棋（1或2）（输入3结束游戏）："))
    assert player_chess in [1, 2, 3]

    if player_chess == 3:
        print("Game Over!")
        break

    chess = 2
    while board.currentState == 0:
        chess = 3 - chess
        board.showQValues()
        if chess == player_chess:
            place = int(input("输入落子位置:"))
            while place - 1 not in board.empty_spots:
                place = int(input("非法位置！请重新输入:"))
            board.placeAChessPiece(place - 1, chess)
        else:
            board.placeABestChessPiece(chess, rand=True)
        board.show()

    if board.currentState == player_chess:
        print("You Won!")
    elif board.currentState == 3:
        print("It's A Draw.")
    else:
        print("You Lose!")
