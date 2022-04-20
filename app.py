import manimlib
from manimlib import *

import sys
sys.path.insert(1, '.')

from life_game import Life

CUSTOM_WHITE = '#ecf0f1'
_BLACK_OPACITY = 0.6
TITLE_FONT_SIZE = 60
BODY_FONT_SIZE = 30
TITLE_BODY_BUFFER = 0.4
FONT_FAMILY = 'Poppins'
# FONT_FAMILY = 'Verdana'


class AppLife(Scene):

    def construct(self) -> None:

        num_rows = 40
        # num_cols = 60
        num_cols = 72

        # create an empty life board
        life = Life(num_rows, num_cols)

        # this grid will be our playground to display life animation
        grid = AppLife.create_grid(num_rows, num_cols, cell_height=14)
        self.add(grid)

        # ANIMATIONS:

        # 1. display moving glider
        self.glider(grid, life, num_generations=30, wait_time=0.1)

        # 2. show intro
        self.show_title_n_body(
            title="Game of Life",
            body="Conway's Game of Life is a zero player game with a few simple rules",
            wait_time=2.5,
        )

        # 3. show rules
        # self.clear_screen(grid, life)
        self.show_rules(grid, life)

        # 4. show post rules message
        self.clear_screen(grid, life)
        self.show_text("These rules turn simple starting patterns into complex ones.\n"
                       "Some completely vanish and some keep progressing forever", font_size=BODY_FONT_SIZE, wait_time=2.5)

        # 5. R. Pentomino
        self.clear_screen(grid, life)
        self.show_text("R Pentomino", font_size=TITLE_FONT_SIZE, wait_time=1)
        # to show R-pentomino starting position
        self.r_pentomino(grid, life, num_generations=1, wait_time=1)
        self.wait(0.5)
        # to actually animate r pentomino
        self.r_pentomino(grid, life, num_generations=70)

        # 6. show message about interesting patterns
        # self.clear_screen(grid, life)
        # self.show_text("Some interesting patterns:", font_size=BODY_FONT_SIZE)

        # 7. Still Life
        self.clear_screen(grid, life)
        self.show_title_n_body("Still Life",
                               "Patterns that do not change in subsequent generations")
        self.still_life(grid, life, num_generations=15)

        # 8. Oscillators
        self.clear_screen(grid, life)
        self.show_title_n_body("Oscillators", "Come back to initial state after a few generations")
        self.oscillators(grid, life, num_generations=25, wait_time=0.3)

        # 9. Glider
        self.clear_screen(grid, life)
        self.show_title_n_body("Gosper Glider Gun", "Emits a Glider at every 30th generation (discovered in 1970)")
        self.glider_gun(grid, life, num_generations=1, wait_time=1)
        self.wait(0.5)
        self.glider_gun(grid, life, num_generations=90, wait_time=0.05)

        # 10. Copperhead
        self.clear_screen(grid, life)
        self.show_title_n_body("Copperhead", "Spaceship (discovered in 2016)")
        self.copperhead(grid, life, num_generations=1, wait_time=1)
        self.wait(0.5)
        self.copperhead(grid, life, num_generations=100, wait_time=0.1)

        # # 11. Google it
        # self.clear_screen(grid, life)
        # self.show_text("If you Google 'Game of Life', it is a nice easter egg",
        #                font_size=TITLE_FONT_SIZE)

        # 11. Predictability
        self.clear_screen(grid, life)
        self.show_question()

        # self.embed()

    @staticmethod
    def create_grid(num_rows, num_cols, cell_height=6):
        # create a grid of squares
        square = Square()
        square.set_fill(BLACK, opacity=_BLACK_OPACITY)
        square.set_stroke(BLACK, width=0)

        grid = square.get_grid(num_rows, num_cols, height=cell_height)
        grid.arrange_in_grid(
            n_rows=num_rows,
            n_cols=num_cols,
            h_buff=0,
            v_buff=0
        )

        return grid

    def animate_grid(self, grid, life, num_generations, wait_time=0.1):
        # the first iteration of loop plots the initial state of board
        # second iteration displays the one next generation

        # self.put_counter(wait_time)

        generation = 1
        while generation <= num_generations:
            self.wait(wait_time)

            # put current state on display
            # for i in range(life.num_rows):
            for i in range(len(life.board)):
                # for j in range(life.num_cols):
                for j in range(len(life.board[0])):

                    # grid is a one dimensional (400,) list
                    grid_idx = life.num_cols * i + j

                    # this cell is alive
                    if life.board[i][j] == 1:
                        grid[grid_idx].set_fill(CUSTOM_WHITE)
                        grid[grid_idx].set_stroke(BLACK, width=.3)
                    else:
                        grid[grid_idx].set_fill(BLACK, opacity=_BLACK_OPACITY)

            life.compute_next_state()
            generation += 1

    def show_title_n_body(self, title, body, wait_time=2.5):
        title = Text(title, font_size=TITLE_FONT_SIZE, font=FONT_FAMILY)
        body = Text(body, font_size=BODY_FONT_SIZE, font=FONT_FAMILY)
        vgroup = VGroup(title, body).arrange(DOWN, buff=TITLE_BODY_BUFFER, center=False, aligned_edge=LEFT) #.set_y(0)
        vgroup.to_edge(UP)
        vgroup.to_edge(LEFT)
        self.play(FadeIn(vgroup))
        self.wait(wait_time)

    def show_text(self, text_str, font_size, wait_time=2.5):
        text = Text(text_str, font_size=font_size, font=FONT_FAMILY)
        text.to_edge(UP)
        text.to_edge(LEFT)
        self.play(FadeIn(text))
        self.wait(wait_time)

    def show_question(self, wait_time=3):
        text = Text(
            "Q: Given a state of the board, is it possible to tell whether\n"
            "a certain pattern will vanish or live forever?",
                    font_size=BODY_FONT_SIZE, font=FONT_FAMILY)
        text.to_edge(UP)
        text.to_edge(LEFT)

        credits_text = Text("code: github.com/emadehsan/life",
                            font_size=BODY_FONT_SIZE, font=FONT_FAMILY)
        credits_text.to_edge(BOTTOM)
        text.to_edge(LEFT)

        self.play(FadeIn(text))
        self.wait(wait_time)
        self.play(FadeIn(credits_text))
        self.wait(wait_time)

    def show_rules(self, grid, life, wait_time=1.5):
        rules = [
            {
                "title": "Underpopulation",
                "body": "A live cell with fewer than two neighbours dies",
            },
            {
                "title": "Survival",
                "body": "A cell with two or three neighbours lives on to the next generation"
            },
            {
                "title": "Overpopulation",
                "body": "A cell with more than three neighbours dies"
            },
            {
                "title": "Reproduction",
                "body": "A dead cell with exactly three neighbours becomes a live cell"
            }
        ]

        # the 4 functions from life_game.py that set the configuration of the board
        # to example that shows the rule applied
        board_state_functions = [
            life.put_underpopulation_example,
            life.put_survival_example,
            life.put_overpopulation_example,
            life.put_reproduction_example
        ]

        # index of the square in the grid. this is the square that will be
        # affected in the next generation when playing by the rule. to get focus, make a flash
        # these matches the life.put_*_example functions' examples
        flash_indexes = [
            (0, 4),  # this cell will die
            (-1, -1),  # no change
            (1, 1),  # this will die
            (0, 1),  # this will come to life
        ]

        for i, rule in enumerate(rules):
            # make the board and grid empty and clear texts etc
            self.clear_screen(grid, life)

            # display this rule's text
            title = Text(rule['title'], font_size=TITLE_FONT_SIZE, font=FONT_FAMILY)
            body = Text(rule['body'], font_size=BODY_FONT_SIZE, font=FONT_FAMILY)
            # body2 = Text(rule['body2'], font_size=BODY_FONT_SIZE, font=FONT_FAMILY)

            vgroup = VGroup(title, body).arrange(DOWN, buff=TITLE_BODY_BUFFER, center=False, aligned_edge=LEFT)
            vgroup.to_edge(UP)
            vgroup.to_edge(LEFT)
            self.play(FadeIn(vgroup))

            # show this rule's animation
            self.display_rule_example(grid, life, board_state_functions[i], flash_indexes[i])

            self.wait(wait_time)

    def clear_screen(self, grid, life):
        life.clear_board()  # this will clear the live cells

        # now animate the grid for one generation,
        # this will make all the squares of the gird displayed to be gray(i.e. empty)
        self.animate_grid(grid, life, num_generations=1)

        # clear text & animation
        self.clear()

        # adds the background grid again (which is all gray cells, now)
        self.add(grid)

    def glider(self, grid, life, num_generations, wait_time=0.1):
        life.clear_board()
        life.put_glider_at(life.num_rows//3, life.num_cols//3)

        self.animate_grid(grid, life, num_generations, wait_time)

    def glider_gun(self, grid, life, num_generations, wait_time=0.1):
        life.clear_board()
        life.put_glider_gun(life.num_rows//2 - 5, life.num_cols//5)

        self.animate_grid(grid, life, num_generations, wait_time)

    def display_rule_example(self, grid, life: Life, set_board_state_func, flash_index, wait_time=1) -> None:
        # put example in the center. the examples chosen to highlight each rule
        # need just one generation of animation
        i = life.num_rows // 2 - 1
        j = life.num_cols // 2 - 1

        set_board_state_func(i, j)

        # animate for 1 generation, this will display the board starting state for this rule
        self.animate_grid(grid, life, num_generations=1, wait_time=wait_time)

        self.wait(wait_time)

        # add flash effect
        a, b = flash_index
        if a >= 0 and b >= 0:
            self.play(
                Flash(grid[
                          life.num_cols * (i+a) + (j+b)
                      ], color=RED_A, flash_radius=0.4)
            )

        # animate for 1 generation again, this will advance the board state for 1 generation
        self.animate_grid(grid, life, num_generations=1, wait_time=wait_time)

        self.wait(wait_time)

    def r_pentomino(self, grid, life, num_generations, wait_time=0.1):
        # put R-pentomino and animate it
        life.clear_board()
        life.put_r_pentomino(life.num_rows//2, life.num_cols//2)

        self.animate_grid(grid, life, num_generations, wait_time)

    def put_counter(self, wait_time):
        # CountInFrom()

        # counts the generation
        counter = DecimalNumber(1)#, text_config={"font": "monospace"})  #.scale(2)
        # ChangingDecimal()

        def update_func(t):
            return t *10

        counter.to_edge(UP)
        counter.to_edge(RIGHT)
        # counter.
        # ChangingDecimal()
        # self.add(counter)
        self.play(ChangingDecimal(counter, update_func), run_time=wait_time)

    def still_life(self, grid, life, num_generations, wait_time=0.2):
        life.clear_board()
        life.put_still_life()

        self.animate_grid(grid, life, num_generations, wait_time)

    def oscillators(self, grid, life, num_generations, wait_time=0.2):
        life.clear_board()
        life.put_oscillators()

        self.animate_grid(grid, life, num_generations, wait_time)

    def copperhead(self, grid, life, num_generations, wait_time=0.2):
        life.clear_board()
        life.put_copperhead(life.num_rows//2 - 4, life.num_cols//2 - 6)

        self.animate_grid(grid, life, num_generations, wait_time)
