import copy


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

