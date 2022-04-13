
from manimlib import *

import sys
sys.path.insert(1, '.')

from life_game import Life

CUSTOM_WHITE = '#ecf0f1'

class AppLife(Scene):

    def construct(self) -> None:

        # size of each row
        N = 30

        # this grid will be our playground to display life animation
        grid = AppLife.create_grid(num_rows=N, num_cols=N, cell_height=10)
        self.add(grid)

        # create a life object
        life = Life(num_rows=N, num_cols=N)

        # 1. display laughing head
        self.show_glider(grid=grid, life=life, num_generations=3, wait_time=0.005)

        # 2. show intro
        self.show_intro()

        # 3. show rules
        self.clear()
        self.add(grid)
        self.show_rules(grid, life)


        # self.embed()

    @staticmethod
    def create_grid(num_rows, num_cols, cell_height=6):
        # create a grid of squares
        square = Square()
        square.set_fill(BLACK, opacity=0.6)
        square.set_stroke(BLACK, width=0)

        grid = square.get_grid(num_rows, num_cols, height=cell_height)
        grid.arrange_in_grid(h_buff=0, v_buff=0)

        return grid

    def show_glider(self, grid, life, num_generations, wait_time):
        # create an empty Life board, and then put a glider on it

        life.put_glider_at(5, 5)
        self.animate_grid(grid, life, num_generations, wait_time)

    def animate_grid(self, grid, life, num_generations, wait_time=0.1):

        generation = 1
        while generation <= num_generations:
            self.wait(wait_time)

            # put current state on display
            for y in range(life.num_rows):
                for x in range(life.num_cols):

                    # grid is a one dimensional (400,) list
                    grid_idx = life.num_cols * y + x

                    # this cell is alive
                    if life.board[y][x] == 1:
                        grid[grid_idx].set_fill(CUSTOM_WHITE)
                        # grid[grid_idx].set_fill(WHITE)
                    else:
                        grid[grid_idx].set_fill(BLACK, opacity=0.6)

            life.compute_next_state()

            generation += 1

    def show_intro(self):
        text = Text("Game of Life",
                    # font="Consolas",
                    font_size=40)

        body = Text(
            """
            Conway's Game of Life is a zero player game\n
            with 4 simple rules
            """,
            font="Arial",
            font_size=24,

            # t2c is a dict that you can choose color for different text
            # t2c={"Text": BLUE, "TexText": BLUE, "LaTeX": ORANGE}
        )
        VGroup(text, body).arrange(DOWN, buff=1)
        self.play(Write(text))
        self.play(Write(body))
        # self.play(FadeIn(difference, UP))
        # self.wait(3)

    def show_rules(self, grid, life):
        rules = [
            {
                "title": "1. Underpopulation",
                "body": "Any live cell with fewer than two live neighbours dies"
            },
            {
                "title": "2. Survival",
                "body": "Any live cell with two or three live neighbours lives on to the next generation"
            },
            {
                "title": "3. Overpopulation",
                "body": "Any live cell with more than three live neighbours dies, as if by overpopulation"
            },
            {
                "title": "4. Reproduction",
                "body": "Any dead cell with exactly three live neighbours becomes a live cell"
            }
        ]

        for rule in rules:
            # clear_grid and text

            self.clear()
            self.add(grid)
            # show this rule's animation
            self.display_underpopulation(grid, life)

            # display this rule's text
            title = Text(rule['title'], font_size=30, font_color='Red')
            body = Text(rule['body'], font_size=14)
            VGroup(title, body).arrange(DOWN, buff=1)
            self.play(Write(title))
            self.play(Write(body))

    def display_underpopulation(self, grid, life: Life) -> None:
        # clear the board
        life.clear_board()

        # put example in the center
        x = life.num_cols // 2 - 3
        y = life.num_rows // 2 - 3
        life.put_underpopulation_example(x, y)

        # display
        self.animate_grid(grid, life, num_generations=30)
        pass

