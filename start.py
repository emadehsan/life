
from manimlib import *


class SquareToCircle(Scene):
    def construct(self):
        circle = Circle()
        # circle.set_x(3)
        # circle.set_y(3)
        circle.set_fill(BLUE, opacity=0.4)
        # circle.set_stroke(BLUE_E, width=5)
        circle.set_stroke(BLUE, width=5)

        # self.add(circle)

        square = Square()
        square.set_fill(RED, opacity=0.6)
        self.play(ShowCreation(square))
        self.wait(0.3)
        self.play(ReplacementTransform(square, circle))
        self.wait(0.3)
        self.play(ShowCreation(circle))

        self.embed()

