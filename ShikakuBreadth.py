import numpy as np
import math
import queue
import time
import matplotlib.pyplot as plt
import memory_profiler

# Shikaku Problem BRF :
# Author: Anibal Picazo Quintana
# Course: EARIN 18Z

class state:
    def __init__(self, value, ind, matrix, piece):
        self.ind = ind
        self.piece = piece
        self.value = value
        self.matrix = np.full((len(matrix), len(matrix)), 0)
        for i in range(len(matrix)):
            for j in range(len(matrix)):
                self.matrix[i, j] = matrix[i, j]
        self.applyPiece()

    def applyPiece(self):
        for i in range(len(self.piece)):
            self.matrix[self.piece[i]] = self.value

    def isSolution(self):
        t = True
        i = j = 0
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix)):
                if (self.matrix[i, j] == 0):
                    t = False
        return t

    def __str__(self):
        str = "State: \n {}"
        return str.format(self.matrix)


class Shikaku:

    def __init__(self, matrix):
        self.points = list()
        self.openList = queue.Queue()
        self.grid = matrix
        n = 0
        for i in range(len(matrix)):
            for j in range(len(matrix)):
                if matrix[i, j] != 0:
                    self.points.append([i, j, matrix[i, j], n])
                    n = n + 1

    def isPrime(self, numero):

        for i in range(2, numero):
            if (numero % i) == 0:
                return False
        return True

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
                    if ((x, y) == (vb + i, hb + j) and hb + j < len(matrix) and vb + i < len(matrix)):
                        hbaux.append((vb + i, hb + j))
                    if (hb + j < len(matrix) and vb + i < len(matrix) and matrix[vb + i, hb + j] == 0):
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

    def breadthFirst(self):

        initial = state(-1, -1, self.grid, [])
        self.openList.put(initial)
        nodes = 1
        goal = None

        while (not self.openList.empty() and goal == None):
            current = self.openList.get()
            # print(current.matrix)
            time.sleep(0)
            if (current.isSolution()):
                goal = current
            if (current.ind + 1 < len(self.points)):
                p = self.getPoint(current.ind + 1)

                neigh = self.getNeighbours(p[0], p[1], p[2], current.matrix, current.ind + 1)
                nodes = nodes + len(neigh)
                for i in range(len(neigh)):
                    self.openList.put(neigh[i])

        return goal, nodes


matrix2=np.array([[6,6,0,0,0,0,0,0,0,0,0,0],
                  [0, 0, 0, 0, 0, 0, 0, 10, 0, 0, 0, 0],
                  [0, 0, 0, 0, 16, 0, 0, 0, 0, 0, 0, 10],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 12, 0],
                  [0, 0, 0, 0, 0, 0, 16, 0, 0, 0, 14, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [4, 4, 0, 0, 0, 0, 12, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 12, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [2, 0, 0, 0, 0, 0, 9, 0, 3, 0, 0, 0]])

#matrix=np.array([ [0, 6, 0, 0, 0, 3, 0],
 #       [0, 0, 0, 0, 0, 2, 0],
  #      [0, 2, 0, 3, 0, 2, 0],
   #     [2, 0, 0, 0, 5, 0, 0],
    #    [0, 0, 6, 0, 0, 0, 4],
     #   [0, 0, 0, 0, 0, 0, 7],
      #  [0, 3, 0, 0, 4, 0, 0],])

#matrix2=np.array([[0,0,0,3,0],
#                  [0,4,0,2,0],
#                  [0,4,2,0,2],
#                  [0,0,0,0,0],
#                  [0,0,3,3,2]])
#matrix2=np.array([[0,0,0,0,5],
#                  [2,0,3,0,0],
#                  [0,0,3,0,0],
#                  [0,0,0,0,3],
#                  [3,2,2,2,0]])

#matrix2=np.array([[2,0,0,3,0],
#                  [0,0,2,0,2],
#                  [0,2,2,4,0],
#                  [4,0,0,0,0],
#                  [0,0,0,4,0]])
#matrix2 = np.array([[0, 0, 0, 0, 2], [2, 2, 2, 0, 2], [0, 0, 3, 0, 2], [3, 3, 0, 0, 0], [0, 4, 0, 0, 0]])


x=Shikaku(matrix2)
start_time = time.time()
mem_usage_before = memory_profiler.memory_usage()[0]
p,s=x.breadthFirst()
end_time = time.time()
mem_usage_after = memory_profiler.memory_usage()[0]
running_time = end_time - start_time
mem_usage = mem_usage_after - mem_usage_before
print(f"Running time: {running_time} seconds")
print(f"Memory usage: {mem_usage} MB")

print("Completed board: ",p)
print("Visited Nodes: ",s)

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

