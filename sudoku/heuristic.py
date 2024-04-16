import math
import random
import time


class Heuristic(object):
    def __init__(self, initial_state: list):
        # number of rows = number of columns = N
        random.seed(time.time())
        self.board = initial_state
        self.N = len(initial_state)
        if len(initial_state[0]) != self.N:
            raise Exception('Wrong size of board')
        self.fixed_board = [[0 if self.board[i][j] == 0 else 1 for j in range(self.N)] for i in range(self.N)]
        self.N = int(math.sqrt(self.N))
        if self.N * self.N != len(self.board):
            raise Exception('Wrong size of board')

    def fill_block(self, row_idx, col_idx):
        # fill all empty in a block at (row_idx, col_idx)
        not_exist = list(range(1, len(self.board) + 1))
        exist = []
        for i in range(self.N):
            for j in range(self.N):
                if self.board[row_idx * self.N + i][col_idx * self.N + j] != 0:
                    exist += [self.board[row_idx * self.N + i][col_idx * self.N + j]]

        for item in exist:
            not_exist.remove(item)
        pos_of_non_exist = self.arg_non_fixed_cell()[row_idx * self.N + col_idx]
        for pos in pos_of_non_exist:
            self.board[pos[0]][pos[1]] = not_exist[0]
            del not_exist[0]

    def fill_board(self):
        # fill all empty cell in board
        for i in range(self.N):
            for j in range(self.N):
                self.fill_block(i, j)

    def calc_cost(self):
        # calculate the cost function of board
        cost = 0
        for i in range(self.N * self.N):
            cost += self.row_cost(i) + self.col_cost(i)
        return cost

    def row_cost(self, idx) -> int:
        # find number of missing value in a row
        existing_value = set(self.board[idx])
        return self.N * self.N - len(existing_value)

    def col_cost(self, idx) -> int:
        # find number of missing value in a column
        existing_value = set([self.board[row_idx][idx] for row_idx in range(self.N * self.N)])
        return self.N * self.N - len(existing_value)

    def arg_non_fixed_cell(self):
        # Find all position of non-fixed cell and group by block
        pos = []
        for row_block in range(self.N):
            for col_block in range(self.N):
                block_non_fixed = []
                for row_cell in range(self.N):
                    for col_cell in range(self.N):
                        if self.fixed_board[row_block * self.N + row_cell][col_block * self.N + col_cell] == 0:
                            block_non_fixed += [(row_block * self.N + row_cell, col_block * self.N + col_cell)]
                pos += [block_non_fixed]

        return pos

    def solve(self):
        # Hill Climbing
        self.fill_board()
        non_fixed_blocks = self.arg_non_fixed_cell()
        cost = self.calc_cost()
        while cost > 0:
            closer_goal = False
            for block in non_fixed_blocks:
                num_of_non_fixed_cells = len(block)
                for i in range(num_of_non_fixed_cells):
                    for j in range(i + 1, num_of_non_fixed_cells):
                        pos1 = block[i]     # position of non-fixed cell
                        pos2 = block[j]     # position of another non-fixed cell
                        cost_before = self.row_cost(pos1[0]) + self.col_cost(pos1[1]) + self.row_cost(pos2[0]) + self.col_cost(pos2[1])
                        self.board[pos1[0]][pos1[1]], self.board[pos2[0]][pos2[1]] = self.board[pos2[0]][pos2[1]], self.board[pos1[0]][pos1[1]]
                        cost_after = self.row_cost(pos1[0]) + self.col_cost(pos1[1]) + self.row_cost(pos2[0]) + self.col_cost(pos2[1])
                        if cost_after < cost_before:
                            cost = cost - cost_before + cost_after
                            closer_goal = True
                        else:
                            self.board[pos1[0]][pos1[1]], self.board[pos2[0]][pos2[1]] = self.board[pos2[0]][pos2[1]], self.board[pos1[0]][pos1[1]]
            if not closer_goal:
                # can not find a possible move
                # make a random move
                temp = non_fixed_blocks.copy()
                random.shuffle(temp)
                random.shuffle(temp[0])
                pos1 = temp[0][0]
                pos2 = temp[0][1]
                cost_before = self.row_cost(pos1[0]) + self.col_cost(pos1[1]) + self.row_cost(pos2[0]) + self.col_cost(pos2[1])
                self.board[pos1[0]][pos1[1]], self.board[pos2[0]][pos2[1]] = self.board[pos2[0]][pos2[1]], self.board[pos1[0]][pos1[1]]
                cost_after = self.row_cost(pos1[0]) + self.col_cost(pos1[1]) + self.row_cost(pos2[0]) + self.col_cost(pos2[1])
                cost = cost - cost_before + cost_after

        return self.board
