from manim import *

class MergeCircles(Scene):
    def construct(self):
        c1 = Circle(radius=0.5,color=BLUE,fill_opacity=1).shift(LEFT * 3)
        c2 = Circle(radius=0.5,color=BLUE,fill_opacity=1).shift(LEFT * 1)

        c3 = Circle(radius=0.7,color=BLUE,fill_opacity=1)

        self.play(Create(c1), Create(c2))

        self.play(
            c1.animate.move_to(ORIGIN),
            c2.animate.move_to(ORIGIN),
            rate_func=linear, run_time=1)
        
        self.play(ReplacementTransform(VGroup(c1, c2), c3), run_time=0.1, rate_func=linear)

        self.play(c3.animate.move_to(RIGHT*8),rate_func=linear, run_time=8/3)

        self.wait()