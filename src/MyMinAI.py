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
from collections import deque


class MyAI:

    def __init__(self, rowDimension, colDimension, totalMines, startX, startY):
        # set up 2d list for game board
        self.rowDimension = rowDimension
        self.colDimension = colDimension
        self.totalMines = totalMines
        self.board = [[" " for _ in range(colDimension)] for _ in range(rowDimension)]
        self.board[startX][startY] = 0

        # track visited and flagged tiles
        self.revealed = set()
        self.flagged = set()
        self.safe_queue = deque([(startX, startY)])

    # checks boundary cells
    def get_neighbors(self, row, col):
        neighbors = []
        # ensure cells are in bounds
        for r in range(row - 1, row + 2):
            for c in range(col - 1, col + 2):
                if 0 <= r < self.rowDimension and 0 <= c < self.colDimension:
                    if r != row or c != col:
                        neighbors.append((r, c))
        return neighbors

    def update_board(self, x, y, number):
        # updates board with new number at (x, y)
        self.board[x][y] = number
        self.revealed.add((x, y))
        # add neighbors to queue
        if number == 0:
            for neighbor in self.get_neighbors(x, y):
                if neighbor not in self.revealed and neighbor not in self.safe_queue:
                    self.safe_queue.append(neighbor)

    def is_safe(self, cell):
        x, y = cell
        neighbors = self.get_neighbors(x, y)
        flagged_count = sum((nx, ny) in self.flagged for nx, ny in neighbors)
        unrevealed_count = sum((nx, ny) not in self.revealed for nx, ny in neighbors)
        # check if number on cell is the same as number of both flagged and unrevealed neighbors
        if self.board[x][y] == flagged_count + unrevealed_count:
            return True
        return False

    def should_flag(self, cell):
        x, y = cell
        neighbors = self.get_neighbors(x, y)
        flagged_count = sum((nx, ny) in self.flagged for nx, ny in neighbors)
        if self.board[x][y] == flagged_count: # should flag if equal to flagged neighbors
            return True
        return False

    def getAction(self, number: int) -> "Action Object":
        if number is not None:
            x, y = self.safe_queue.popleft()
            self.update_board(x, y, number)
            #print(f"revealed tiles: {list((self.revealed))}")
            #print(f"number of revealed tiles: {len(list((self.revealed)))}")
            #print(f"current safe queue: {list((self.safe_queue))}")

        """while self.safe_queue:
            print(f"just checking 1")
            cell = self.safe_queue[0]
            x, y = cell
            if (x, y) not in self.revealed:
                return Action(AI.Action.UNCOVER, x, y)"""

        # if there are tiles in safe_queue, pops one and returns an uncover action for that tile
        if self.safe_queue:
            # print(f"just checking 1")
            cell = self.safe_queue[0]
            x, y = cell
            if (x, y) not in self.revealed:
                # print(f"uncovering ({x},{y})")
                return Action(AI.Action.UNCOVER, x, y)

        for cell in self.revealed:
            # print(f"just checking 2")
            if self.board[cell[0]][cell[1]] != " ":
                if self.is_safe(cell):
                    for neighbor in self.get_neighbors(cell[0], cell[1]):
                        if (
                            neighbor not in self.revealed
                            and neighbor not in self.flagged
                        ):
                            self.safe_queue.append(neighbor)
                            #print(f"added to safe queue")
                if self.should_flag(cell):
                    for neighbor in self.get_neighbors(cell[0], cell[1]):
                        if (
                            neighbor not in self.revealed
                            and neighbor not in self.flagged
                        ):
                            self.flagged.add(neighbor)
                            return Action(AI.Action.FLAG, neighbor[1], neighbor[0])

        # if len(list(self.safe_queue)) == 0:

        if self.safe_queue:

            # debugs
            # print(f"just checking 3")
            # print(f"revealed tiles: {list((self.revealed))}")
            # print(f"current safe queue: {list((self.safe_queue))}")

            cell = self.safe_queue.popleft()
            # print(f"{cell}")
            if cell not in self.revealed:
                return Action(AI.Action.UNCOVER, cell[0], cell[1])

        # if all options exhausted or board is complete,
        return Action(AI.Action.LEAVE) 
