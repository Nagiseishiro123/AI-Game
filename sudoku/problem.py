import copy

class Problem(object):

    def __init__(self, initial):
        self.initial = initial
        self.type = len(initial) 
        self.height = int(self.type/3) 

    def goal_test(self, state) -> bool:
        total = sum(range(1, self.type+1))

        # Check rows and columns and return false if total is invalid
        for row in range(self.type):
            if (len(state[row]) != self.type) or (sum(state[row]) != total):
                return False

            column_total = 0
            for column in range(self.type):
                column_total += state[column][row]

            if (column_total != total):
                return False

        # Check quadrants and return false if total is invalid
        for column in range(0,self.type,3):
            for row in range(0,self.type,self.height):

                block_total = 0
                for block_row in range(0,self.height):
                    for block_column in range(0,3):
                        block_total += state[row + block_row][column + block_column]

                if (block_total != total):
                    return False

        return True


    def filter_values(self, values, used) -> list:
        """Return a list of valid number that did not appear in used"""
        return [number for number in values if number not in used]

    
    def get_spot(self, state) -> int:
        """Return first empty cell (marked with 0)"""
        for row in range(self.type):
            for column in range(self.type):
                if state[row][column] == 0:
                    return row, column

    
    def filter_row(self, state, row) -> list:
        """Return a list of valid number that did not appear in row"""
        number_set = range(1, self.type+1) 
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
        row_start = int(row/self.height)*self.height
        column_start = int(column/3)*3
        
        for block_row in range(0, self.height):
            for block_column in range(0,3):
                in_block.append(state[row_start + block_row][column_start + block_column])
        options = self.filter_values(options, in_block)
        return options    

    def actions(self, state):
        row,column = self.get_spot(state)

        options = self.filter_row(state, row)
        options = self.filter_col(options, state, column)
        options = self.filter_quad(options, state, row, column)

        for number in options:
            new_state = copy.deepcopy(state)
            new_state[row][column] = number
            yield new_state

class Node:

    def __init__(self, state):
        self.state = state

    def expand(self, problem):
        # Return list of valid states
        return [Node(state) for state in problem.actions(self.state)]