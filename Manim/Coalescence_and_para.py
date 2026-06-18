from manim import *

# The scene that renders a jet with droplets that have a coalescence event
class het(Scene):
    def construct(self):
        
        # Nozzle
        nozzle = Rectangle(
            color= GRAY,
            height= 3,
            width= 0.3,
            fill_color= GRAY,
            fill_opacity= 0.8
        )

        # Jet
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

        # Makes the jet round on the end
        WaterJetcirc.move_to(WaterJetsqr.get_edge_center(DOWN))
        WaterJet = VGroup(WaterJetsqr, WaterJetcirc)

        #Waterdrops
        def drop():
            return Circle(
                color=BLUE,
                radius=0.05,
                fill_color=BLUE,
                fill_opacity=0.8
            ).shift(UP * 2)

        Waterdrop1 = drop()
        Waterdrop2 = drop()
        Waterdrop3 = drop()
        Waterdrop4 = drop()
        Waterdrop5 = drop()

        nozzletext = Text(r"Our nozzle").shift(UP*2.4)

        # Scene start
        self.play(Create(nozzle))
        self.play(Write(nozzletext))
        self.wait(1.5)
        
        self.play(Unwrite(nozzletext))
        self.play(nozzle.animate.shift(UP * 3).scale(0.4))

        self.add(WaterJet)
        self.play(WaterJet.animate.shift(DOWN*0.84))
        
        self.add(Waterdrop1, Waterdrop2, Waterdrop3, Waterdrop4, Waterdrop5)
        
        # Moves the droplets after each other
        self.play(
           
            Waterdrop1.animate(run_time=3, rate_func=linear).shift(DOWN * 8),

            # Makes one droplet go faster than the others, and scales it up once it touches another droplet
            Succession(
                Wait(run_time=0.4),
                Waterdrop2.animate(run_time=2.0,rate_func=linear).shift(DOWN * 3),
                ScaleInPlace(Waterdrop2, scale_factor=1.5, run_time=0.01),
                Wait(run_time=0.05),
            ),
            
            Succession(
                Wait(run_time=2.45),
                Waterdrop2.animate(run_time=1.5,rate_func=linear).shift(DOWN*8)
            ),

            Succession(
                Wait(run_time=0.8),  
                Waterdrop3.animate(run_time=1.6,rate_func=linear).shift(DOWN * 3), # 1.6s voor de perfecte gelijke timing
                FadeOut(Waterdrop3, run_time=0.05)
            ),

            # Waterdrop 4
            Succession(
                Wait(run_time=1.2),
                Waterdrop4.animate(run_time=3,rate_func=linear).shift(DOWN * 8)
            ),
            
            # Waterdrop 5
            Succession(
                Wait(run_time=1.6),
                Waterdrop5.animate(run_time=3,rate_func=linear).shift(DOWN * 8)
            )     
        )
        self.wait(1)


# The scene that shows of the parameters that influence coalescence 
class para(Scene):
    def construct(self):

        # Makes nozzles
        def make_nozzle():
            return Rectangle(
                color=GRAY,
                height=3,
                width=0.3,
                fill_color=GRAY,
                fill_opacity=0.8,
            )
 
        nozzle1 = make_nozzle()
        nozzle2 = make_nozzle()
        nozzle3 = make_nozzle()
 
        # Diameter measuring bracket
        meetbar = Line(LEFT * 0.15 + DOWN * 2, RIGHT * 0.15 + DOWN * 2, color=WHITE)
        zijbarL = Line(LEFT * 0.15 + DOWN * 2.1, LEFT * 0.15 + DOWN * 1.9, color=WHITE)
        zijbarR = Line(RIGHT * 0.15 + DOWN * 2.1, RIGHT * 0.15 + DOWN * 1.9, color=WHITE)
        bar1 = VGroup(nozzle1, meetbar, zijbarL, zijbarR)
        bar1.to_edge(LEFT).shift(RIGHT * 1.5)
 
        # Position nozzle3 
        nozzle3.to_edge(RIGHT).shift(LEFT * 1.5)
 
        # Height bar: tracks the bottom of nozzle3
        ground_y = -2  # fixed "ground" level
        bar_x = nozzle3.get_center()[0] + 0.6 
 
        def make_height_bar():
            top_y = nozzle3.get_bottom()[1]
            return VGroup(
                Line([bar_x, ground_y, 0], [bar_x, top_y, 0], color=WHITE),
                Line([bar_x - 0.1, ground_y, 0], [bar_x + 0.1, ground_y, 0], color=WHITE),
                Line([bar_x - 0.1, top_y, 0], [bar_x + 0.1, top_y, 0], color=WHITE),
            )
 
        bar2 = always_redraw(make_height_bar)
 
        # Container walls
        Lbar = Line(LEFT * 3 + DOWN * 2.5, LEFT * 3 + UP * 2.5, color=BLUE)
        Rbar = Line(RIGHT * 3 + DOWN * 2.5, RIGHT * 3 + UP * 2.5, color=BLUE)
 
        # Velocity arrow & droplets 
        snelpijl = Arrow(start=RIGHT + UP, end=RIGHT + DOWN * 0.4)
 
        minidrops = VGroup(*[
            Circle(radius=0.05, color=BLUE, fill_opacity=0.8)
            for _ in range(50)
        ]).shift(UP * 1.5)
 
        # Labels
        textdia = Text("Diameter").scale(0.35)
        textsnel = Text("Velocity").scale(0.35)
        texthoog = Text("Height").scale(0.35)
 
        textdia.next_to(bar1, UP*6)
        textsnel.next_to(nozzle2, UP*6)
        texthoog.next_to(nozzle3, UP*6)
 
        # Scene start
        self.play(FadeIn(Lbar), FadeIn(Rbar))
        self.wait(0.3)
 
        # Parameter 1: Diameter 
        self.play(FadeIn(bar1), FadeIn(textdia))
        self.play(bar1.animate.stretch(2, dim=0), run_time=1.2)
        self.play(bar1.animate.stretch(0.25, dim=0), run_time=1.2) 
        self.play(bar1.animate.stretch(2, dim=0), run_time=1.2)
        self.wait(0.5)
 
        # Parameter 2: Velocity 
        self.play(FadeIn(nozzle2), FadeIn(textsnel))
        self.play(FadeIn(snelpijl), FadeIn(minidrops))
        self.play(nozzle2.animate.shift(UP*2).stretch(0.3, dim=1))
        sync_time = 5 
        
        self.play(        
            # The arrow stretches out and shrinks back
            snelpijl.animate(
                run_time=sync_time,
                rate_func=there_and_back
            ).stretch(1.7, dim=1),

            LaggedStart(
                *[
                    c.animate(rate_func=smooth).shift(DOWN * 6) 
                    for c in minidrops
                ],
                lag_ratio=0.04,
                run_time=sync_time,
                rate_func=smooth 
            ),
        )

        # Parameter 3: Height 
        self.play(FadeIn(nozzle3), FadeIn(texthoog), FadeIn(bar2))
        self.play(nozzle3.animate.shift(UP * 1), run_time=1.2)
        self.play(nozzle3.animate.shift(DOWN * 1), run_time=1.2)  
 
        self.wait()