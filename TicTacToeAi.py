import copy
import random
from collections import deque

from heuristic import INF, WIN_PTS, evaluate

# Độ sâu lớn nhất của cây tìm kiếm (nhìn trước bao nhiêu nước đi)
MAX_DEPTH = 4


class TicTacToeAi:
    def __init__(self, board: list[list[str]], k: int, role: str) -> None:
        self.board = board
        self.m = len(board)
        self.n = len(board[0])
        self.k = k
        self.role = role

        self.prune = 0
        self.cnt = 0

        if role == "x":
            self.op_role = "o"
        else:
            self.op_role = "x"
        # self.state = 1 << (self.m * self.n * 2)
        # self.available_moves = deque(maxlen=m*n)

    def get_move(self) -> tuple[str, str] | None:
        self.cnt += 1
        # Check thắng thua, có thể cải thiện cách tính
        stop = evaluate(self.board, self.k, self.role, self.op_role)
        if abs(stop) == WIN_PTS:
            return stop

        move = None
        val = -INF
        alpha = -INF
        beta = INF

        self.prune = 0

        for i in range(self.m):
            for j in range(self.n):
                if self.board[i][j] == ' ':
                    # Duyệt backtrack cây con
                    self.board[i][j] = self.role
                    tmp = self.search_min(alpha, beta, 1)
                    self.board[i][j] = ' '

                    if tmp > val:
                        val = tmp
                        if val > alpha:
                            alpha = val
                        # if val >= beta:
                        #     return val
                        # Cập nhật nước đi tốt nhất
                        move = (i, j)
        return (move, val)

    def search_max(self, alpha, beta, depth):
        self.cnt += 1
        # Check thắng thua, có thể cải thiện cách tính
        stop = evaluate(self.board, self.k, self.role, self.op_role)
        if abs(stop) == WIN_PTS:
            return stop

        val = -INF
        is_leaf = True

        if depth < MAX_DEPTH:
            for i in range(self.m):
                for j in range(self.n):
                    if self.board[i][j] == ' ':
                        is_leaf = False

                        # Duyệt backtrack cây con
                        self.board[i][j] = self.role
                        tmp = self.search_min(alpha, beta, depth + 1)
                        self.board[i][j] = ' '

                        if tmp > val:
                            val = tmp
                            if val > alpha:
                                alpha = val
                            if val >= beta:
                                self.prune += (self. m * self.n -
                                               depth) ** (MAX_DEPTH - depth - 1)
                                return val

        # Nếu là lá (không còn nc đi hoặc chạm đáy) thì đánh giá heuristic
        if is_leaf:
            return stop

        return val

    def search_min(self, alpha, beta, depth):
        self.cnt += 1
        # Check thắng thua, có thể cải thiện cách tính
        stop = evaluate(self.board, self.k, self.role, self.op_role)
        if abs(stop) == WIN_PTS:
            return stop

        val = INF
        is_leaf = True

        if depth < MAX_DEPTH:
            for i in range(self.m):
                for j in range(self.n):
                    if self.board[i][j] == ' ':
                        is_leaf = False

                        # Duyệt backtrack cây con
                        self.board[i][j] = self.op_role
                        tmp = self.search_max(alpha, beta, depth + 1)
                        self.board[i][j] = ' '

                        if tmp < val:
                            val = tmp
                            if val < beta:
                                beta = val
                            if val <= alpha:
                                self.prune += (self. m * self.n -
                                               depth) ** (MAX_DEPTH - depth - 1)
                                return val

        # Nếu là lá (không còn nc đi hoặc chạm đáy) thì đánh giá heuristic
        if is_leaf:
            return stop

        return val

    def get_prune_rate(self):
        '''Tính tỉ lệ cắt tỉa, chỉ chính xác ở những bước đầu, càng về sau càng lệch tuyến tính do width (số nc có thể đi) giảm.\n
        Có thể chỉnh cách tính pruning cho chính xác hơn.'''
        return float(self.prune) / (self.cnt + self.prune)