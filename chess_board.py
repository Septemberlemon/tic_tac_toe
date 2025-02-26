import random
import torch
from q_table import QTable


class ChessBoard:
    def __init__(self, path=None):
        self.chess_list = [0 for _ in range(9)]
        self.q_table = QTable(path)

    def clear(self):
        self.chess_list = [0 for _ in range(9)]

    def show(self):
        print("chess board:")
        print(self.chess_list[:3])
        print(self.chess_list[3:6])
        print(self.chess_list[6:])
        print("---------------")

    def showQValues(self):
        self.q_table.showQValues(self.numState)

    def placeAChessPiece(self, spot, chess_piece):
        if self.chess_list[spot] == 0:
            self.chess_list[spot] = chess_piece
            return 0
        return 1

    def randomPlaceAChessPiece(self, chess_piece):
        spot = random.choice(self.empty_spots)
        self.chess_list[spot] = chess_piece
        return spot

    def placeABestChessPiece(self, chess_piece, rand=False, explore_rate=0):
        if random.random() < explore_rate:
            return self.randomPlaceAChessPiece(chess_piece)
        max_value = max(self.q_table.table[self.numState][spot] for spot in self.empty_spots)
        best_spots = [spot for spot in self.empty_spots if self.q_table.table[self.numState][spot] == max_value]
        spot = random.choice(best_spots) if rand else best_spots[0]
        self.placeAChessPiece(spot, chess_piece)
        return spot

    def update_q_table(self, last_num_state, last_action, current_num_state):
        self.q_table.update(last_num_state, last_action, current_num_state, self.empty_spots)

    def checkLine(self, indices):
        line = [self.chess_list[index] for index in indices]
        return line[0] if len(set(line)) == 1 else 0

    @property
    def currentState(self):
        # -1 非法状态
        # 0 可以继续下
        # 1 a胜
        # 2 b胜
        # 3 平局
        a_win = False
        b_win = False

        all_indices = [(0, 1, 2), (3, 4, 5), (6, 7, 8),  # 行
                       (0, 3, 6), (1, 4, 7), (2, 5, 8),  # 列
                       (0, 4, 8), (2, 4, 6)]  # 对角线

        for indices in all_indices:
            temp = self.checkLine(indices)
            if temp == 1:
                a_win = True
            elif temp == 2:
                b_win = True

        if a_win and b_win:
            return -1
        if a_win:
            return 1
        if b_win:
            return 2
        if 0 not in self.chess_list:
            return 3
        return 0

    @property
    def numState(self):
        num = 0
        for i, element in enumerate(self.chess_list):
            num += element * 3 ** i
        return num

    @property
    def empty_spots(self):
        return [place for place in range(9) if self.chess_list[place] == 0]

    def save_q_table(self, path):
        torch.save(self.q_table.table, path)
