import pprint
from typing import List, Tuple

from assets.head_to_life_board import AsciiToBoard


class Life:
    def __init__(self, num_rows: int=0, num_cols: int=0):
        self.num_rows = num_rows
        self.num_cols = num_cols

        self.board = [
            [0] * num_cols for _ in range(num_rows)
        ]

    def clear_board(self) -> None:
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                self.board[i][j] = 0

    def set_board_state(self, board: List[List[int]]) -> None:
        # make a deep copy, to avoid bugs?
        # self.board = [
        #     row[:] for row in board
        # ]


        # if dimensions of both are same, then overwrite values
        if len(self.board) == len(board) and len(self.board[0]) == len(board[0]):
            # or manually set the values in old array, to avoid memory leak of pointing to new array
            for i in range(len(board)):
                for j in range(len(board[0])):
                    self.board[i][j] = board[i][j]

        else:
            # otherwise, delete old one and add new
            del self.board
            self.board = board
            self.num_rows = len(self.board)
            self.num_cols = len(self.board[0])

    def get_board(self) -> List[List[int]]:
        return self.board

    def compute_next_state(self) -> None:
        # compute the next state based on the rules of game of life

        # TODO: won't this be memory intensive? Should we use the trick to use O(1) space?
        # make a copy of current state
        board_copy = [
            row[:] for row in self.board
        ]

        for i in range(self.num_rows):
            for j in range(self.num_cols):
                num_neighbours = self._count_neighbours(board_copy, i, j)

                if self.board[i][j] == 1 and num_neighbours not in [2,3]:
                    # an alive cell changes its state to dead if neighbours count is other than 2 or 3
                    self.board[i][j] = 0
                elif self.board[i][j] == 0 and num_neighbours == 3:
                    # a dead cell is brought to life with exactly 3 neighbours
                    self.board[i][j] = 1

    def _count_neighbours(self, board_copy: List[List[int]], i: int, j: int) -> int:
        neighbours = [
            # indexes of matrix with (0,0) as the first Top-Left element
            (-1, -1),
            (-1, 0),
            (-1, 1),
            (0, -1),
            # (0, 0),  # itself
            (0, 1),
            (1, -1),
            (1, 0),
            (1, 1)
        ]

        num_neighbours = 0

        for neigh in neighbours:
            # i, j are indexes of the cell for which we're counting neighbours
            # ii, jj are indexes of current neighbour
            ii = i + neigh[0]
            jj = j + neigh[1]

            if 0 <= ii < len(board_copy) and 0 <= jj < len(board_copy[0]):
                num_neighbours += board_copy[ii][jj]

        return num_neighbours

    def _make_live(self, cells: List[Tuple[int, int]], i: int, j: int) -> None:
        # for the given cells' indexes relative to i,j... sets the value of these cells to 1
        for cell in cells:
            ii = i + cell[0]
            jj = j + cell[1]
            self.board[ii][jj] = 1

    def put_glider_at(self, i: int, j: int) -> None:
        # will put a glider in the 3x3 box whose 0,0 will be positioned at i,j
        # precaution: clear the board, this method just overwrites the new values.
        # this glider will face bottom-right
        cells = [
            (0, 1),
            (1, 2),
            (2, 0),
            (2, 1),
            (2, 2),
        ]
        self._make_live(cells, i, j)

    def put_underpopulation_example(self, i: int, j: int) -> None:
        # note: clear the grid before this step
        # this method puts an L-pentomino at given i,j
        cells = [
            (0, 4),
            (2, 0),
            (2, 1),
            (3, 0),
            (3, 1),
        ]

        self._make_live(cells, i, j)

    def put_survival_example(self, i: int, j: int) -> None:
        # use a Tub (as described on wikipedia under "still life")
        cells = [
            (0, 1),
            (1, 0),
            (1, 2),
            (2, 1)
        ]
        self._make_live(cells, i, j)

    def put_overpopulation_example(self, i: int, j: int) -> None:
        # it is a Z-pentomino
        cells = [
            (0, 0),
            (0, 1),
            (1, 1),
            (2, 1),
            (2, 2)
        ]
        self._make_live(cells, i, j)

    def put_reproduction_example(self, i: int, j: int) -> None:
        # a 3 cell group
        cells = [
            (0, 0),
            (1, 0),
            (1, 1)
        ]
        self._make_live(cells, i, j)

    def put_r_pentomino(self, i: int, j: int) -> None:
        cells = [
            (0, 1),
            (0, 2),
            (1, 0),
            (1, 1),
            (2, 1)
        ]
        self._make_live(cells, i, j)

    def meme_head(self):

        self.set_board_state(
            AsciiToBoard.read_board_state()
        )


if __name__ == '__main__':

    board = [[0, 1, 0], [0, 0, 1], [1, 1, 1], [0, 0, 0]]
    # next = [[0,0,0],[1,0,1],[0,1,1],[0,1,0]]

    l = Life(num_rows=len(board), num_cols=len(board[0]))
    l.set_board_state(board)
    print("Original")
    pprint.pprint(l.get_board())

    l.compute_next_state()
    print("Next State")
    pprint.pprint(l.get_board())















