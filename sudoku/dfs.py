import time
from typing import Tuple

from problem import *

DFS_state = []
class DFSAct(Problem):
    def __init__(self, initial):
        super().__init__(initial)

    def get_spot(self, state) -> tuple[int, int]:
        """Return first empty state (marked with 0)"""
        for row in range(self.type):
            for column in range(self.type):
                if state[row][column] == 0:
                    return row, column

    def filter_values(self, values, used) -> list:
        """Return a list of valid number that did not appear in used"""
        return [number for number in values if number not in used]

    def filter_row(self, state, row) -> list:
        """Return a list of valid number that did not appear in row"""
        number_set = range(1, self.type + 1)
        in_row = [number for number in state[row] if (number != 0)]
        options = self.filter_values(number_set, in_row)
        return options

    def filter_col(self, options, state, column) -> list:
        """Return a list of valid number that did not appear in col"""
        in_column = []
        for column_index in range(self.type):
            if state[column_index][column] != 0:
                in_column.append(state[column_index][column])
        options = self.filter_values(options, in_column)
        return options

    def filter_quad(self, options, state, row, column) -> list:
        """Return a list of valid number that did not appear in quadrant"""
        in_block = []
        row_start = int(row / self.height) * self.height
        column_start = int(column / 3) * 3

        for block_row in range(0, self.height):
            for block_column in range(0, 3):
                in_block.append(state[row_start + block_row][column_start + block_column])
        options = self.filter_values(options, in_block)
        return options

    def actions(self, state):
        row, column = self.get_spot(state)

        options = self.filter_row(state, row)
        options = self.filter_col(options, state, column)
        options = self.filter_quad(options, state, row, column)

        for number in options:
            new_state = copy.deepcopy(state)
            new_state[row][column] = number
            yield new_state


class Node(object):
    def __init__(self, state):
        self.state = state

    def expand(self, problem: DFSAct):
        return [Node(state) for state in problem.actions(self.state)]


def dfs(problem: DFSAct):
    start = Node(problem.initial)
    if problem.goal_test(start.state):
        return start.state

    stack = [start]

    while stack:
        node = stack.pop()
        DFS_state.append(node)
        if problem.goal_test(node.state):
            return node.state
        stack.extend(node.expand(problem))  # Add viable states onto the stack

    return None


def solve_dfs(board):
    print("\nSolving with DFS...")
    start_time = time.time()
    problem = DFSAct(board)
    solution = dfs(problem)
    elapsed_time = time.time() - start_time

    if solution:
        print("Found solution")
        for row in solution:
            print(row)
        root = tk.Tk()
        app = SolutionVisualizer(root, DFS_state)
        root.title("DFS Solver")
        root.mainloop()
    else:
        print("No possible solutions")

    print ("Elapsed time: " + str(elapsed_time))
    return solution

