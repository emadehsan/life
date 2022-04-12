
from manimlib import *

import sys
sys.path.insert(1, '.')

from life_game import Life

CUSTOM_WHITE = '#ecf0f1'

class AppLife(Scene):
    def construct(self) -> None:

        square = Square()
        square.set_fill(BLACK, opacity=0.6)
        square.set_stroke(BLACK, width=0)

        # size of each row
        N = 20



        grid = square.get_grid(N, N, height=6)
        self.add(grid)

        # create an empty Life board, and then put a glider on it
        life = Life(num_rows=N, num_cols=N)
        life.put_glider_at(5, 5)

        # for i in range(10):
        #     self.wait()
        #     grid[i].set_fill(CUSTOM_WHITE)

        # return

        generation = 1
        while generation < 100:
            self.wait()

            # put current state on display
            for y in range(life.num_rows):
                for x in range(life.num_cols):

                    # grid is a one dimensional (400,) list
                    grid_idx = life.num_cols * y + x

                    # this cell is alive
                    if life.board[y][x] == 1:
                        grid[grid_idx].set_fill(CUSTOM_WHITE)
                    else:
                        grid[grid_idx].set_fill(BLACK, opacity=0.6)

            life.compute_next_state()

            generation += 1

        # self.embed()
