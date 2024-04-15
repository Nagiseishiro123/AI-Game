import tkinter as tk

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
     board = solution.matrix
     
     self.canvas.delete("all")
    
     cell_size = min(400 // board.shape[0], 400 // board.shape[1])
    
     # Define a list of colors
     colors = ["red", "blue", "green", "orange", "purple", "brown", "cyan", "magenta", "yellow", "gray"]
    
    # Create a dictionary to map numbers to colors
     num_to_color = {num: colors[i % len(colors)] for i, num in enumerate(set(board.flatten()))}
    
     for i in range(board.shape[0]):
        for j in range(board.shape[1]):
            num = board[i, j]
            if num != 0:
                color = num_to_color[num]
                self.canvas.create_rectangle(j*cell_size, i*cell_size, (j+1)*cell_size, (i+1)*cell_size, fill=color)
                self.canvas.create_text(j*cell_size + cell_size/2, i*cell_size + cell_size/2, text=str(num), font=("Helvetica", 12), fill="white")
    
     for i in range(board.shape[0]+1):
        self.canvas.create_line(0, i*cell_size, board.shape[1]*cell_size, i*cell_size)
        
     for j in range(board.shape[1]+1):
        self.canvas.create_line(j*cell_size, 0, j*cell_size, board.shape[0]*cell_size)
    
     # Schedule the next draw_solution call after 1000 milliseconds (1 second)
     if self.current_index < len(self.solutions) - 1:
        self.current_index += 1
        self.master.after(1, self.draw_solution)


