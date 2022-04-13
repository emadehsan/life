import pprint
from typing import List, Tuple


class Life:
    def __init__(self, num_rows: int, num_cols: int):
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.board = [
            [0] * num_cols for _ in range(num_rows)
        ]

    def clear_board(self) -> None:
        for y in range(self.num_rows):
            for x in range(self.num_cols):
                self.board[y][x] = 0

    def set_board(self, board: List[List[int]]) -> None:
        # make a deep copy, to avoid bugs?
        # self.board = [
        #     row[:] for row in board
        # ]

        # or manually set the values in old array, to avoid memory leak of pointing to new array
        for y in range(len(board)):
            for x in range(len(board[0])):
                self.board[y][x] = board[y][x]

    def get_board(self) -> List[List[int]]:
        return self.board

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

            if 0 <= x1 < len(board_copy[0]) and 0 <= y1 < len(board_copy):
                num_neighbours += board_copy[y1][x1]

        return num_neighbours

    def _make_live(self, cells: List[Tuple[int]], x: int, y: int) -> None:
        # for the given cell coordinates relative to x,y sets the value of these cells to 1
        for cell in cells:
            x1 = x + cell[0]
            y1 = y + cell[1]
            self.board[y1][x1] = 1

    def put_glider_at(self, x, y) -> None:
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

        self._make_live(cells, x, y)

    def put_underpopulation_example(self, x: int, y: int) -> None:
        # note: clear the grid before this step
        # this method puts an L at given x,y
        # 1
        # 1
        # 1, 1
        live_cells = [
            # x, y
            (0, 0),
            (0, 1),
            (0, 2),
            (1, 2)
        ]

        self._make_live(live_cells, x, y)

    def put_survival_example(self, x: int, y: int) -> None:
        live_cells = [
            (0, 0),
            (0, 1),
            (1, 1)
        ]
        self._make_live(live_cells, x, y)

    def put_overpopulation_example(self, x: int, y: int) -> None:
        live_cells = [
            # x, y, according to computer axis?
            (2, 0),
            (0, 1),
            (1, 1),
            (2, 1),
            (0, 2)
        ]
        self._make_live(live_cells, x, y)

    def put_reproduction_example(self, x: int, y: int) -> None:
        # 1
        # 1, 1
        live_cells = [
            (0, 0),
            (0, 1),
            (1, 1)
        ]
        self._make_live(live_cells, x, y)


if __name__ == '__main__':

    board = [[0, 1, 0], [0, 0, 1], [1, 1, 1], [0, 0, 0]]
    # next = [[0,0,0],[1,0,1],[0,1,1],[0,1,0]]

    l = Life(num_rows=len(board), num_cols=len(board[0]))
    l.set_board(board)
    print("Original")
    pprint.pprint(l.get_board())

    l.compute_next_state()
    print("Next State")
    pprint.pprint(l.get_board())















