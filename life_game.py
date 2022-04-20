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

    def put_still_life(self):
        # block
        block = [
            (0, 0),
            (0, 1),
            (1, 0),
            (1, 1)
        ]

        beeHive = [
            (0, 1),
            (0, 2),
            (1, 0),
            (1, 3),
            (2, 1),
            (2, 2)
        ]

        loaf = [
            (0, 1),
            (0, 2),
            (1, 0),
            (1, 3),
            (2, 1),
            (2, 3),
            (3, 2)
        ]

        boat = [
            (0, 0),
            (0, 1),
            (1, 0),
            (1, 2),
            (2, 1)
        ]

        tub = [
            (0, 1),
            (1, 0),
            (1, 2),
            (2, 1)
        ]
        shapes = [block, beeHive, loaf, boat, tub]

        # divide the board width into 6 parts
        # 6 parts contain 5 mid points. we'll place each shape at one of those points
        part_j = self.num_cols // (len(shapes) + 1)
        part_i = self.num_rows // 2  # center vertical

        for idx, shape in enumerate(shapes):
            self._make_live(shape, i=part_i, j=part_j*(idx+1))

    def put_oscillators(self):
        # period 2
        blinker = [
            (0, 0),
            (0, 1),
            (0, 2)
        ]

        # period 2
        toad = [
            (0, 1),
            (0, 2),
            (0, 3),
            (1, 0),
            (1, 1),
            (1, 2)
        ]

        # period 2
        beacon = [
            (0, 0),
            (0, 1),
            (1, 0),
            (1, 1),
            (2, 2),
            (2, 3),
            (3, 2),
            (3, 3)
        ]

        penta_decathlon = [
            (0, 1),
            (1, 1),
            (2, 0),
            (2, 2),
            (3, 1),
            (4, 1),
            (5, 1),
            (6, 1),
            (7, 0),
            (7, 2),
            (8, 1),
            (9, 1)
        ]

        shapes = [blinker, toad, beacon, penta_decathlon]

        i = self.num_rows // 2  # center vertical
        j = self.num_cols // (len(shapes) + 1)

        for idx, shape in enumerate(shapes):
            next_i = i - len(shape)//3  # adjust the height
            next_j = j * (idx + 1)
            self._make_live(shape, i=next_i, j=next_j)

    def put_copperhead(self, i, j):
        cells = [
            (0, 5),
            (0, 7),
            (0, 8),
            (1, 4),
            (1, 11),

            (2, 3),
            (2, 4),
            (2, 8),
            (2, 11),

            (3, 0),
            (3, 1),
            (3, 3),
            (3, 9),
            (3, 10),
            (4, 0),
            (4, 1),
            (4, 3),
            (4, 9),
            (4, 10),

            (5, 3),
            (5, 4),
            (5, 8),
            (5, 11),

            (6, 4),
            (6, 11),

            (7, 5),
            (7, 7),
            (7, 8)
        ]
        self._make_live(cells, i, j)

    def put_glider_gun(self, i, j):
        cells = [
            (4, 0),
            (5, 0),
            (4, 1),
            (5, 1),

            (4, 10),
            (5, 10),
            (6, 10),
            (3, 11),
            (7, 11),
            (2, 12),
            (8, 12),
            (2, 13),
            (8, 13),
            (5, 14),
            (3, 15),
            (7, 15),
            (4, 16),
            (5, 16),
            (6, 16),
            (5, 17),

            (2, 20),
            (3, 20),
            (4, 20),
            (2, 21),
            (3, 21),
            (4, 21),
            (1, 22),
            (5, 22),

            (0, 24),
            (1, 24),
            (5, 24),
            (6, 24),

            (2, 34),
            (3, 34),
            (2, 35),
            (3, 35)
        ]

        self._make_live(cells, i, j)

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















