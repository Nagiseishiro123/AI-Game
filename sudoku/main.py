import dfs
from heuristic import Heuristic
import  time

board = [
      [0,0,0,8,4,0,6,5,0],
      [0,8,0,0,0,0,0,0,9],
      [0,0,0,0,0,5,2,0,1],
      [0,3,4,0,7,0,5,0,6],
      [0,6,0,2,5,1,0,3,0],
      [5,0,9,0,6,0,7,2,0],
      [1,0,8,5,0,0,0,0,0],
      [6,0,0,0,0,0,0,4,0],
      [0,5,2,0,8,6,0,0,0]]

print("dfs:")
dfs_board = dfs.solve_dfs(board)

print("heuristic:")
new_board = Heuristic(board)
start_time = time.time()
heuristic_board = new_board.solve()
end_time = time.time()
print('\n'.join([str(line) for line in heuristic_board]))
print("elapsed time:", end_time - start_time)

for i in range(9):
      for j in range(9):
            if dfs_board[i][j] != heuristic_board[i][j]:
                  print(f"Fail at position {i} and {j}")
                  break

print("Success")