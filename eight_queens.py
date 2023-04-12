# Isssues I wasn't able to solve:
# 1. Program will print a state with an h of 0
#    then it will change the same state (in the array I assume)
#    it will realize that the state solves the problem and will finally 
#    print the solved output.

import random

# A queen object that keeps track of its row
class Queen:
    def __init__(self, row):
        self.row = row

    def getRow(self):
        return self.row

# A board object that keeps track of the queens and the number of conflicts, restarts, and state changes.
class Board:
    def __init__(self, size):
        self.size = size
        self.queens = [None] * size
        self.conflicts = 0
        self.state_changes = 0
        self.restarts = 0

    def printBoard(self):
        # For every row
        for i in range(self.size):
            # For every column
            for j in range(self.size):
                # If a queen is in the column, print Q at the row the queen is in
                if self.queens[j] is not None and self.queens[j].getRow() == i:
                    print(" 1 ", end="")
                # Otherwise, print a dot
                else:
                    print(" 0 ", end="")
            print()

    def randomize(self):
        # Places the queens randomly on the board
        for i in range(self.size):
            row = random.randint(0, self.size - 1)
            self.place_queen(i, row)

    def place_queen(self, column, row):
        # Places a queen object in the column and row we give it
        self.queens[column] = Queen(row)

    def remove_queen(self, column):
        # Removes the queen from the column we give it
        self.queens[column] = None

    def count_conflicts(self):
        # Count the number of conflicts among queens on the board
        conflicts = 0
        for i in range(self.size - 1):
            for j in range(i + 1, self.size):
                # If queens are in the rame row or diaganol, add to the conflicts - no queen is in the same col ever (hopefully)
                if self.queens[i] is not None and self.queens[j] is not None:
                    if (self.queens[i].getRow() == self.queens[j].getRow() or 
                        abs(self.queens[i].getRow() - self.queens[j].getRow()) == abs(i - j)):
                        conflicts += 1
        return conflicts

    def find_better_neighbor(self):
        min_conflicts = 9999
        best_moves = []
        # If there are no conflicts, we don't need to find a better neighbor
        if self.conflicts < 1:
            return min_conflicts, best_moves
        for i in range(self.size):
            # Save the current row of the queen in column i
            current_row = self.queens[i].getRow()
            # Try each possible row for the queen in column i
            for j in range(self.size):
                if j != current_row:
                    # Move the queen to row j and count the conflicts
                    self.place_queen(i, j)
                    conflicts = self.count_conflicts()
                    # If the conflicts are less than the before, update the best moves list
                    if conflicts < min_conflicts:
                        min_conflicts = conflicts
                        best_moves = [(i, j)]
                    # If the conflicts are equal to the minimum, add to the best moves list
                    elif conflicts == min_conflicts:
                        best_moves.append((i, j))
                    # Move the queen back to its original row if it wasn't a better move
                    if j != current_row and conflicts > self.conflicts:
                            self.place_queen(i, current_row)
        return min_conflicts, best_moves

    # Runs a hill climbing algo until we find the solution, restarts if there is no better neightbor
    def hill_climbing(self):
        while True:
            # Randomize the board
            self.randomize()
            # count the conflicts
            self.conflicts = self.count_conflicts()
            print(f"Current h: {self.conflicts}")
            print(f"Initial board:")
            self.printBoard()
            print("\n")
            
            while True:
                # Find a better neighbor by moving one queen
                min_conflicts, best_moves = self.find_better_neighbor()
                # If we have a better or equivalent neighbor, try to move to it
                if min_conflicts < self.conflicts:
                    # Move to a better neighbor and update the state changes
                    column, row = random.choice(best_moves)
                    self.place_queen(column, row)
                    self.conflicts = min_conflicts
                    self.state_changes += 1
                    print(f"Current h: {self.conflicts}")
                    print(f"Current State:")
                    self.printBoard()
                    print(f"Neighbors found with lower h: {len(best_moves)}")
                    print("Setting new current state\n")
                else:
                    # We didn't find a better neighbor, check if a we're done or restart
                    if self.conflicts == 0:
                        # No conflicts, we found the solution
                        # Print stuff and exit
                        print(f"Final h: {self.conflicts}")
                        self.printBoard()
                        print(f"Solution found!")
                        print(f"State changes: {self.state_changes}")
                        print(f"Restarts: {self.restarts}")
                        exit() 
                    else:
                        # We have conflicts
                        # Add one to restart, print stuff
                        # and restart with the break to get a new random board
                        print(f"Current h: {self.conflicts}")
                        print(f"Current State:")
                        self.printBoard()
                        print(f"Neighbors found with lower h: {len(best_moves)}")
                        print(f"RESTART\n")
                        self.restarts += 1
                        break
                
def main():
    # Create the 8 x 8 board and solve using hill climbing
    board = Board(8)
    board.hill_climbing()

if __name__ == "__main__":
    main()