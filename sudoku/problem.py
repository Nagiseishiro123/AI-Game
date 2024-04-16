import copy
import tkinter as tk

class Problem(object):

    def __init__(self, initial):
        self.initial = initial
        self.type = len(initial)
        self.height = int(self.type / 3)

    def goal_test(self, state) -> bool:
        """Return true if the given state is in the goal state."""
        total = sum(range(1, self.type + 1))

        # Check rows and columns and return false if total is invalid
        for row in range(self.type):
            if (len(state[row]) != self.type) or (sum(state[row]) != total):
                return False

            column_total = 0
            for column in range(self.type):
                column_total += state[column][row]

            if column_total != total:
                return False

        # Check quadrants and return false if total is invalid
        for column in range(0, self.type, 3):
            for row in range(0, self.type, self.height):

                block_total = 0
                for block_row in range(0, self.height):
                    for block_column in range(0, 3):
                        block_total += state[row + block_row][column + block_column]

                if block_total != total:
                    return False

        return True

class SolutionVisualizer:
    def __init__(self, master, solutions):
        self.master = master
        self.solutions = solutions
        self.current_index = 0
        
        self.frame = tk.Frame(self.master)
        self.frame.pack()
        
        self.canvas = tk.Canvas(self.frame, width=400, height=400)
        self.canvas.pack()
        
        self.draw_solution()
        
    def draw_solution(self):
     solution = self.solutions[self.current_index]
     state = solution.state
    
     self.canvas.delete("all")
    
     cell_size = min(400 // len(state), 400 // len(state[0]))
    
    # Define a list of colors
     colors = ['#FF3333', '#FFCC33', '#CCFF33', '#33FF33', '#00BFFF', '#8A2BE2', '#8B008B', '#3333FF', '#CC33FF', '#FF33CC']
    
    # Create a dictionary to map numbers to colors
     num_to_color = {num: colors[i % len(colors)] for i, num in enumerate(set(sum(state, [])))}
    
     for i in range(len(state)):
        for j in range(len(state[i])):
            num = state[i][j]
            if num != 0:
                color = num_to_color[num]
                self.canvas.create_rectangle(j*cell_size, i*cell_size, (j+1)*cell_size, (i+1)*cell_size, fill=color)
                self.canvas.create_text(j*cell_size + cell_size/2, i*cell_size + cell_size/2, text=str(num), font=("Helvetica", 16, "bold"), fill="white")
     

     for i in range(0, len(state)+1, 3):
        self.canvas.create_line(0, i*cell_size, len(state[0])*cell_size, i*cell_size, width=5)
     for j in range(0, len(state[0])+1, 3):
        self.canvas.create_line(j*cell_size, 0, j*cell_size, len(state)*cell_size, width=5)

     for i in range(len(state)+1):
        self.canvas.create_line(0, i*cell_size, len(state[0])*cell_size, i*cell_size)
        
     for j in range(len(state[0])+1):
        self.canvas.create_line(j*cell_size, 0, j*cell_size, len(state)*cell_size)
    
     # Schedule the next draw_solution call after 1000 milliseconds (1 second)
     if self.current_index < len(self.solutions) - 1:
        self.current_index += 1
        self.master.after(1, self.draw_solution)

class SolutionVisualizerHillClimbing:
    def __init__(self, master, solutions):
        self.master = master
        self.solutions = solutions
        self.current_index = 0
        
        self.frame = tk.Frame(self.master)
        self.frame.pack()
        
        self.canvas = tk.Canvas(self.frame, width=400, height=400)
        self.canvas.pack()
        
        self.draw_solution()
        
    def draw_solution(self):
     solution = self.solutions[self.current_index]
     state = solution
    
     self.canvas.delete("all")
    
     cell_size = min(400 // len(state), 400 // len(state[0]))
    
    # Define a list of colors
     colors = ['#FF3333', '#FFCC33', '#CCFF33', '#33FF33', '#00BFFF', '#8A2BE2', '#8B008B', '#3333FF', '#CC33FF', '#FF33CC']
    
    # Create a dictionary to map numbers to colors
     num_to_color = {num: colors[i % len(colors)] for i, num in enumerate(set(sum(state, [])))}
    
     for i in range(len(state)):
        for j in range(len(state[i])):
            num = state[i][j]
            if num != 0:
                color = num_to_color[num]
                self.canvas.create_rectangle(j*cell_size, i*cell_size, (j+1)*cell_size, (i+1)*cell_size, fill=color)
                self.canvas.create_text(j*cell_size + cell_size/2, i*cell_size + cell_size/2, text=str(num), font=("Helvetica", 16, "bold"), fill="white")
     

     for i in range(0, len(state)+1, 3):
        self.canvas.create_line(0, i*cell_size, len(state[0])*cell_size, i*cell_size, width=5)
     for j in range(0, len(state[0])+1, 3):
        self.canvas.create_line(j*cell_size, 0, j*cell_size, len(state)*cell_size, width=5)

     for i in range(len(state)+1):
        self.canvas.create_line(0, i*cell_size, len(state[0])*cell_size, i*cell_size)
        
     for j in range(len(state[0])+1):
        self.canvas.create_line(j*cell_size, 0, j*cell_size, len(state)*cell_size)
    
     # Schedule the next draw_solution call after 1000 milliseconds (1 second)
     if self.current_index < len(self.solutions) - 1:
        self.current_index += 1
        self.master.after(1, self.draw_solution)