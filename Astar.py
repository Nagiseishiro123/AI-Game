import numpy as np
import math
import queue
import time
import memory_profiler
import matplotlib.pyplot as plt
from data import STATE
import tkinter as tk
from game import SolutionVisualizer

Astar_state = []
class state:
    def __init__(self, value, ind, matrix, piece, neigh=0, dim=1):
        self.ind = ind
        self.piece = piece
        self.value = value
        self.matrix = np.full(matrix.shape, 0)
        self.h = neigh
        for i in range(matrix.shape[0]):
            for j in range(matrix.shape[1]):
                self.matrix[i, j] = matrix[i, j]
        self.g = self.ind
        self.f = self.h + self.g
        self.applyPiece()

    def setH(self, h):
        self.h = h
        self.f = self.g + self.h

    def setG(self, g):
        self.g = g
        self.f = self.g + self.h

    def inList(self, list_states):
        t = False
        for i in range(len(list_states)):
            if (t):
                break
            if (self.equalsTo(list_states[i])):
                t = True
        return t

    def equalsTo(self, state):
        return self.value == state.value and self.ind == state.ind and self.piece == state.piece and np.array_equal(
            self.matrix, state.matrix)

    def applyPiece(self):
        for i in range(len(self.piece)):
            self.matrix[self.piece[i]] = self.value

    def isSolution(self):
        t = True
        i = j = 0
        for i in range(self.matrix.shape[0]):
            for j in range(self.matrix.shape[1]):
                if (self.matrix[i, j] == 0):
                    t = False
        return t

    def __str__(self):
        str = "State: \n {}"
        return str.format(self.matrix)


class Shikaku:

    def __init__(self, matrix):
        self.points = list()
        self.grid = matrix
        n = 0
        for i in range(matrix.shape[0]):
            for j in range(matrix.shape[1]):
                if matrix[i, j] != 0:
                    self.points.append([i, j, matrix[i, j], n])
                    n = n + 1

    def checkPieces(self, x, y, ind, nvalue, matrix, dim, value):
        h = list()
        v = list()
        hb = y - value + 1
        vb = x - dim + 1

        if (hb < 0):
            hb = 0
        if (vb < 0):
            vb = 0

        while (hb <= y and vb <= x):
            hbaux = list()

            for i in range(dim):
                for j in range(value):
                    if ((x, y) == (vb + i, hb + j) and hb + j < matrix.shape[1] and vb + i < matrix.shape[0]):
                        hbaux.append((vb + i, hb + j))
                    if (hb + j < matrix.shape[1] and vb + i < matrix.shape[0] and matrix[vb + i, hb + j] == 0):
                        hbaux.append((vb + i, hb + j))
            if len(hbaux) == nvalue:
                p = state(nvalue, ind, matrix, hbaux)
                h.append(p)

            hb = hb + 1
            if (hb > y and vb <= x):
                hb = y - value + 1
                if (hb < 0):
                    hb = 0
                vb = vb + 1

        return v, h

    def getNeighbours(self, x, y, value, matrix, ind):

        wt = st = []
        for dim in range(1, value + 1):
            if (value % dim == 0):
                w, s = self.checkPieces(x, y, ind, value, matrix, dim, int(value / dim))
                st = st + s
                wt = wt + w

        f = wt + st
        return f

    def getPoint(self, i):
        return self.points[i]

    def Astar(self):
        closedList = []
        openList = []
        initial = state(-1, -1, self.grid, [], 0)
        openList.append((initial.f, initial))
        nodes = 1
        goal = None

        while (not len(openList) == 0 and goal == None):
            p = min(openList, key=lambda x: x[0])
            index = openList.index(p)
            current = p[1]
            openList.pop(index)
            closedList.append(current)
            print(current.matrix)
            Astar_state.append(current)
            if (current.isSolution()):
                goal = current

            if (current.ind + 1 < len(self.points)):
                p = self.getPoint(current.ind + 1)

                neigh = self.getNeighbours(p[0], p[1], p[2], current.matrix, current.ind + 1)
                nodes = nodes + len(neigh)
                for i in range(len(neigh)):
                    if (not neigh[i].inList(closedList)):
                        h = len(self.points) - neigh[i].ind
                        if (neigh[i].isSolution()):
                            h = -100000

                        for j in range(neigh[i].ind + 1, len(self.points)):
                            p = self.getPoint(j)
                            h += len(self.getNeighbours(p[0], p[1], p[2], neigh[i].matrix, 0))

                        neigh[i].setH(h)
                        openList.append((neigh[i].f, neigh[i]))

        return goal, nodes


x = Shikaku(STATE[0])
mem_usage_before = memory_profiler.memory_usage()[0]
start_time = time.time()
p, s = x.Astar()
end_time = time.time()
mem_usage_after = memory_profiler.memory_usage()[0]
running_time = end_time - start_time
mem_usage = mem_usage_after - mem_usage_before
print(f"Running time: {running_time} seconds")
print(f"Memory usage: {mem_usage} MB")


print("Solution:")
print(p)
print("Number of generated nodes:")
print(s)

root = tk.Tk()
app = SolutionVisualizer(root, Astar_state)
root.mainloop()
"""
def visualize_solution(solution):
    board = solution.matrix
    fig, ax = plt.subplots()
    ax.set_xticks(np.arange(-.5, board.shape[1], 1), minor=True)
    ax.set_yticks(np.arange(-.5, board.shape[0], 1), minor=True)
    ax.grid(which="minor", color="black", linestyle='-', linewidth=2)
    for i in range(board.shape[0]):
        for j in range(board.shape[1]):
            if board[i, j] != 0:
                ax.text(j, i, str(board[i, j]), fontsize=12, ha='center', va='center')
    ax.imshow(board, cmap='Pastel1', interpolation='nearest')
    plt.show()

visualize_solution(p)
"""