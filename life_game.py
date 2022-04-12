
from typing import List


class Life:
    def __init__(self, num_rows: int, num_cols: int):
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.board = [
            [1] * num_cols for _ in range(num_rows)
        ]

    def clear_board(self):
        for y in range(self.num_rows):
            for x in range(self.num_cols):
                self.board[y][x] = 0

    def get_board(self) -> List[List[int]]:
        return self.board

    def put_glider_at(self, x, y):
        # will put a glider in the 3x3 box with x,y at its 0,0 position
        # assumes that board is empty. also direction is bottom-right
        cells = [
            # x, y
            (0, 1),
            (1, 2),
            (2, 0),
            (2, 1),
            (2, 2)
        ]

        for cell in cells:
            x1 = x + cell[0]
            y1 = y + cell[1]
            self.board[y1][x1] = 1

    def compute_next_state(self) -> None:
        # compute the next state based on the rules of game of life

        # TODO: won't this be memory intensive? Should we use the trick to use O(1) space?
        # make a copy of current state
        board_copy = [
            row[:] for row in self.board
        ]

        for y in range(self.num_rows):
            for x in range(self.num_cols):
                num_neighbours = self._count_neighbours(board_copy, x=x, y=y)

                if self.board[y][x] == 1 and num_neighbours not in [2,3]:
                    # an alive cell changes its state to dead if neighbours count is other than 2 or 3
                    self.board[y][x] = 0
                elif self.board[y][x] == 0 and num_neighbours == 3:
                    # a dead cell is brought to life with exactly 3 neighbours
                    self.board[y][x] = 1

    def _count_neighbours(self, board_copy: List[List[int]], x: int, y: int) -> int:
        neighbours = [
            # x, y as if they were coordinates of matrix with origin 0,0 as the first Top-Left element
            (-1, -1),
            (0, -1),
            (1, -1),
            (-1, 0),
            # (0, 0),  # itself
            (1, 0),
            (-1, 1),
            (0, 1),
            (1, 1)
        ]

        num_neighbours = 0

        for neigh in neighbours:
            x1 = x + neigh[0]
            y1 = y + neigh[1]

            if 0 <= x1 < self.num_cols and 0 <= y1 < self.num_rows:
                num_neighbours += board_copy[y][x]

        return num_neighbours
