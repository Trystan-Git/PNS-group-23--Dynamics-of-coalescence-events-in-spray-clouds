from manim import *
from manim_physics import *

class Jet(Scene):
    def construct(self):
        
        nozzle = Rectangle(
            color= GRAY,
            height= 3,
            width= 0.3,
            fill_color= GRAY,
            fill_opacity= 0.8
        )

        WaterJetsqr = Rectangle(
            color= BLUE,
            height=0.4,
            width= 0.1,
            fill_color= BLUE,
            fill_opacity=0.8
        ).shift(UP * 3)

        WaterJetcirc = Circle(
            color= BLUE,
            radius = 0.05,
            fill_opacity = 0.8
        )

        WaterJetcirc.move_to(WaterJetsqr.get_edge_center(DOWN))

        WaterJet = VGroup(WaterJetsqr, WaterJetcirc)

        
        # Waterdrops = VGroup(*[
        #     Circle(
        #         radius=0.05, 
        #         color=BLUE, 
        #         fill_opacity=0.8
        #     ) 
        #     for _ in range(5)
        # ]).shift(UP * 2)

        Waterdrop1 = Circle(
            color= BLUE,
            radius= 0.05,
            fill_color=BLUE,
            fill_opacity=0.8
        )

        Waterdrop2 = Circle(
            color= BLUE,
            radius= 0.05,
            fill_color=BLUE,
            fill_opacity=0.8
        ).shift(UP * 2)

        Waterdrop3 = Circle(
            color= BLUE,
            radius= 0.05,
            fill_color=BLUE,
            fill_opacity=0.8
        )

        Waterdrop4 = Circle(
            color= BLUE,
            radius= 0.05,
            fill_color=BLUE,
            fill_opacity=0.8
        )

        Waterdrop5 = Circle(
            color= BLUE,
            radius= 0.05,
            fill_color=BLUE,
            fill_opacity=0.8
        )

        Waterdrops = VGroup(Waterdrop1, Waterdrop2, Waterdrop3, Waterdrop4, Waterdrop5)
        nozzletext = Text(r"Our nozzle").shift(UP*2.4)

        self.play(Create(nozzle))
        self.play(Write(nozzletext))
        self.wait(3)
        
        self.play(Unwrite(nozzletext))
        self.play(nozzle.animate.shift(UP * 3).scale(0.4))

        self.add(WaterJet)
        self.play(WaterJet.animate.shift(DOWN*0.84))

        self.add(Waterdrops)

        # self.play(LaggedStart([c.animate.shift(DOWN*3) for c in Waterdrops], lag_ratio=0.25))

        # self.play(Create(Waterdrop2))
        # self.play(Waterdrop2.animate.shift(DOWN * 2))
        # self.wait(2)









# class Clock(Scene):
#     def construct(self):

#         self.camera.background_color = WHITE

#         Uur12 = UP * 1.5

#         Clockoutside = Circle(
#             radius=1.8,
#             color=BLACK,
#             stroke_width = 7
#         )


#         Nob = Circle(
#             radius= 0.1,
#             color = BLACK,
#             fill_color = BLACK,
#             fill_opacity=1
#         )

#         secondewijzer= Line(
#             start=Nob.get_center(),
#             end = Uur12,
#             color=BLACK
#         )

#         self.play(Create(Clockoutside))

#         self.wait(2)

#         self.play(Create(Nob), Create(secondewijzer))

#         self.wait(5)

# # class PendulumBob(Scene):
# #     def construct(self):

# #         pivot = UP * 2

# #         bob = Circle(
# #             radius=0.4,
# #             color=WHITE,
# #             fill_color=BLUE,
# #             fill_opacity=0.8
# #         )

# #         bob.move_to(DOWN * 1.5)

# #         string = Line(
# #             start=pivot,
# #             end=bob.get_center()
# #         )

# #         pendulum = VGroup(string, bob)

# #         self.play(Create(string))
# #         self.play(GrowFromCenter(bob))
# #         self.wait()

# #         title = Text("Simple Pendulum Animation")
# #         title.to_edge(UP)
# #         self.play(Write(title))

# #         self.play(
# #             Rotate(pendulum, angle=70 * DEGREES, about_point=pivot),
# #             run_time=1,
# #             rate_func=smooth
# #         )

# #         self.play(
# #             Rotate(pendulum, angle=-140 * DEGREES, about_point=pivot),
# #             run_time=2,
# #             rate_func=smooth
# #         )

# #         self.play(
# #             Rotate(pendulum, angle=140 * DEGREES, about_point=pivot),
# #             run_time=2,
# #             rate_func=smooth
# #         )

# #         self.play(
# #             Rotate(pendulum, angle=-70 * DEGREES, about_point=pivot),
# #             run_time=1,
# #             rate_func=smooth
# #         )

# #         self.wait()





# # # use a SpaceScene to utilize all specific rigid-mechanics methods
# # class TwoObjectsFalling(SpaceScene):
# #     def construct(self):
# #         circle = Circle().shift(UP)
# #         circle.set_fill(color=BLUE)
# #         circle.shift(UP * 2)
# #         circle.scale(0.5)

# #         # cirlce2 = Circle().shift(UP)
# #         # circle2.set_fill(BLUE,1)


# #         ground = Line([-4, -3.5, 0], [4, -3.5, 0])
# #         wall1 = Line([-4, -3.5, 0], [-4, 3.5, 0])
# #         wall2 = Line([4, -3.5, 0], [4, 3.5, 0])
# #         walls = VGroup(ground, wall1, wall2)
# #         self.add(walls)

# #         self.play(
# #             DrawBorderThenFill(circle),
# #         )
# #         self.make_rigid_body(circle)  # Mobjects will move with gravity
# #         self.make_static_body(walls)  # Mobjects will stay in place
# #         self.wait(5)

 
    