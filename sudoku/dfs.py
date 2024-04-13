import time
from problem import *

def DFS(problem):
    start = Node(problem.initial)
    if problem.goal_test(start.state):
        return start.state

    stack = []
    stack.append(start) # Place initial node onto the stack

    while stack:
        node = stack.pop()
        if problem.goal_test(node.state):
            return node.state
        stack.extend(node.expand(problem)) # Add viable states onto the stack

    return None

def solve_dfs(board):
    print ("\nSolving with DFS...")
    start_time = time.time()
    problem = Problem(board)
    solution = DFS(problem)
    elapsed_time = time.time() - start_time

    if solution:
        print ("Found solution")
        for row in solution:
            print (row)
    else:
        print ("No possible solutions")

    print ("Elapsed time: " + str(elapsed_time))