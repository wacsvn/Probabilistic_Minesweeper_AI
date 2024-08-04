# ==============================CS-199==================================
# FILE:			MyAI.py
#
# AUTHOR: 		Justin Chung
#
# DESCRIPTION:	This file contains the MyAI class. You will implement your
# 				agent in this file. You will write the 'getAction' function,
# 				the constructor, and any additional helper functions.
#
# NOTES: 		- MyAI inherits from the abstract AI class in AI.py.
#
# 				- DO NOT MAKE CHANGES TO THIS FILE.
# ==============================CS-199==================================
from AI import AI
from Action import Action


class MyAI(AI):

    def __init__(self, rowDimension, colDimension, totalMines, startX, startY):
        # Initialize variables to store game information
        self.board = [
            [" " for _ in range(colDimension)] for _ in range(rowDimension)
        ]  # Stores revealed cells
        self.unrevealed = set(
            [(i, j) for i in range(rowDimension) for j in range(colDimension)]
        )  # Unrevealed cell coordinates
        self.flagged = set()  # Flagged cell coordinates
        self.total_mines = totalMines
        self.safe_neighbors = (
            {}
        )  # Stores the number of safe neighbors for each revealed cell

        # Mark the starting cell as safe (assuming no mine on the first move)
        self.board[startY][startX] = 0
        self.unrevealed.remove((startY, startX))

    def getAction(self, number: int) -> Action:
        """
        This function determines the next action based on the revealed information.

        Args:
            number: The number revealed in the last uncovered cell (ignored in this basic implementation).

        Returns:
            An Action object specifying the next move.
        """

        # Prioritize uncovering safe cells
        for cell in self.unrevealed:
            if self.is_safe(cell):
                self.unrevealed.remove(cell)
                self.board[cell[0]][cell[1]] = self.get_neighbor_mines(cell)
                return Action(AI.Action.UNCOVER, cell[0], cell[1])

        # If no safe cells, randomly choose an unrevealed cell (not ideal, can be improved)
        if len(self.unrevealed) > 0:
            cell = random.choice(list(self.unrevealed))
            self.unrevealed.remove(cell)
            return Action(AI.Action.UNCOVER, cell[0], cell[1])

        # No more moves possible (board filled or lost)
        return Action(AI.Action.LEAVE)

    def is_safe(self, cell):
        """
        Checks if a cell is safe based on the number of neighboring flags and revealed mines.

        Args:
            cell: A tuple representing the cell coordinates (row, col).

        Returns:
            True if the cell is safe, False otherwise.
        """
        neighbors = self.get_neighbors(cell)
        flagged_count = sum(1 for n in neighbors if n in self.flagged)
        revealed_mines = sum(
            self.board[n[0]][n[1]] == "X" for n in neighbors if n in self.board
        )
        return flagged_count == self.safe_neighbors.get(cell, 0) - revealed_mines

    def get_neighbors(self, cell):
        """
        Gets the coordinates of all neighboring cells within the board boundaries.

        Args:
            cell: A tuple representing the cell coordinates (row, col).

        Returns:
            A list of tuples representing neighboring cell coordinates.
        """
        row, col = cell
        neighbors = []
        for i in range(row - 1, row + 2):
            for j in range(col - 1, col + 2):
                if (
                    0 <= i < len(self.board)
                    and 0 <= j < len(self.board[0])
                    and (i, j) != cell
                ):
                    neighbors.append((i, j))
        return neighbors

    def get_neighbor_mines(self, cell):
        """
        Counts the number of mines around a revealed cell based on the surrounding flags.

        Args:
            cell: A tuple representing the cell coordinates (row, col).

        Returns:
            The number of mines around the cell (assuming flags are accurate).
        """
        neighbors = self.get_neighbors(cell)
        flagged_count = sum(1 for n in neighbors if n in self.flagged)
        return flagged_count
