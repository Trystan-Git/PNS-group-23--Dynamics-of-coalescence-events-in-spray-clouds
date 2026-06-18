from manim import *
import numpy as np

class NeusSpray(Scene):
    def construct(self):
        #De neusman introduceren
        neusman = ImageMobject("Echte neusman.jpg")
        neusman.scale(1.5)
        neusman.to_edge(RIGHT, buff=1.5)
        neusman.shift(LEFT * 2)

        self.play(FadeIn(neusman))
        self.wait()
        
        #De neusspray maken
        rechthoek = Rectangle(width=1.0,height=1.5,stroke_color=BLUE,fill_color=BLUE,fill_opacity=1)

        p1 = [-0.20, 0.75, 0]
        p2 = [ 0.20, 0.75, 0]
        p3 = [ 0.125, 1.75, 0]
        p4 = [-0.125, 1.75, 0]

        spray_tuit = Polygon(p1, p2, p3, p4,stroke_color=WHITE,fill_color=WHITE,fill_opacity=1)

        p5 = [-0.375, 1.375, 0]
        p6 = [ 0.375, 1.375, 0]
        
        lijn  = Line(p5,p6, color = BLUE, stroke_width=8)
        
        neusspray = VGroup(rechthoek, spray_tuit, lijn)
        neusspray.to_edge(LEFT, buff = 1.5)
        
        self.play(FadeIn(neusspray))
        self.wait()
        
        #neusspray naar neus bewegen
        self.play(neusspray.animate.move_to(LEFT * 1.8 + DOWN * 0.7),run_time=1)
        
        self.play(
            Rotate(neusspray, angle=-45 * DEGREES),
            run_time=2,
            rate_func=smooth)
        
        indruk_richting = rotate_vector(DOWN, -45 * DEGREES)

        self.play(
            lijn.animate.shift(indruk_richting * 0.4),
            run_time=0.6
        )
        self.wait()
        self.play(
            lijn.animate.shift(-indruk_richting * 0.4),
            run_time=0.5
        )
        
        #Een spray uit de neusspray laten komen
        spuit_richting = rotate_vector(RIGHT, -45 * DEGREES)
        startpunt = spray_tuit.get_top() + RIGHT * 0.38 + DOWN * 0.02

        #Hoofdpad van de spray:
        #eerst door de neusholte, daarna omlaag richting keel/luchtweg
        pad_punten = [
            startpunt,
            startpunt + RIGHT * 0.45 + UP * 0.5,
            startpunt + RIGHT * 1.10 + UP * 0.4,
            startpunt + RIGHT * 1.75 + UP * 0.25,
            startpunt + RIGHT * 2.0 + DOWN * 0.1,
            startpunt + RIGHT * 2.25 + DOWN * 0.30,
            startpunt + RIGHT * 2.55 + DOWN * 1.15,
            startpunt + RIGHT * 2.70 + DOWN * 1.75,
        ]

        spray_pad = VMobject()
        spray_pad.set_points_smoothly(pad_punten)

        #Handig om even te testen waar het pad ligt:
        #self.add(spray_pad.copy().set_stroke(GREEN, width=3, opacity=0.4))

        druppels = VGroup()
        animaties = []

        for i in range(110):
            druppel = Dot(
                point=startpunt,
                radius=np.random.uniform(0.025, 0.04),
                color=BLUE
            )

            if np.random.random() < 0.45:
                eind_alpha = np.random.uniform(0.10, 0.38)
            else:
                eind_alpha = np.random.uniform(0.45, 1.00)

            druppel_pad_punten = []

            for j, punt in enumerate(pad_punten):
                if j == 0:
                    druppel_pad_punten.append(punt)
                else:
                    spreiding = j / (len(pad_punten) - 1)

                    offset = (
                        UP * np.random.uniform(-0.18, 0.18) * spreiding
                        + RIGHT * np.random.uniform(-0.18, 0.18) * spreiding
                    )

                    druppel_pad_punten.append(punt + offset)

            druppel_pad = VMobject()
            druppel_pad.set_points_smoothly(druppel_pad_punten)

            deelpad = druppel_pad.copy()
            deelpad.pointwise_become_partial(druppel_pad, 0, eind_alpha)

            druppels.add(druppel)
            animaties.append(
                MoveAlongPath(druppel, deelpad, rate_func=smooth)
            )

        self.add(druppels)

        self.play(
            LaggedStart(
                *animaties,
                lag_ratio=0.05
            ),
            run_time=2.8,
            rate_func=linear
        )

        self.wait(4)
        
        #De plekken waar de spray komt highlighten
        neus_rechthoek = Rectangle(width=0.8,height=0.8,stroke_color=WHITE,fill_opacity=0)
        neus_rechthoek.move_to(UP *0.7 + LEFT *0.4)
        
        neuspijl = Line(start = (-2.2, 1.6, 0), end = (-0.9, 0.85, 0))
        neuspijl.add_tip(tip_shape = StealthTip)
        
        neustext = Text("Nose", font_size=40)
        neustext.move_to(UP * 1.9 + LEFT * 2.3)
        
        neus = VGroup(neus_rechthoek, neuspijl, neustext)
        self.play(Create(neus), runtime = 1)
        self.play(FadeOut(neus))
        
        mond_rechthoek = Rectangle(width=1.2,height=1.1,stroke_color=WHITE,fill_opacity=0)
        mond_rechthoek.move_to(UP *0.2 + RIGHT * 1.3)
        
        mondpijl = Line(start = (2.0, 1.6, 0), end = (1.3, 0.85, 0))
        mondpijl.add_tip(tip_shape = StealthTip)
        
        mondtext = Text("Nose canal", font_size=40)
        mondtext.move_to(UP * 1.9 + RIGHT * 1.8)
        
        mond = VGroup(mond_rechthoek, mondpijl, mondtext)
        self.play(Create(mond), runtime = 1)
        self.play(FadeOut(mond))
        
        keel_rechthoek = Rectangle(width=0.7,height=2.0,stroke_color=WHITE,fill_opacity=0)
        keel_rechthoek.move_to(DOWN *1 + RIGHT * 1.5)
        
        keelpijl = Line(start = (3.2, -1.0, 0), end = (2.1, -0.7, 0))
        keelpijl.add_tip(tip_shape = StealthTip)
        
        keeltext = Text("Airway", font_size=40)
        keeltext.move_to(DOWN * 1 + RIGHT * 4.2)
        
        keel = VGroup(keel_rechthoek, keelpijl, keeltext)
        self.play(Create(keel), runtime = 1)
        self.play(FadeOut(keel))
        self.wait()
        
        self.clear()
        self.wait()
        
        #individuele droplet size aanpassing
        scale = ValueTracker(0)

        drup = always_redraw(
            lambda: Circle(
                radius=0.5 * scale.get_value(),
                color=BLUE,
                fill_opacity=1
            )
        )

        staaf = always_redraw(
            lambda: VGroup(
                # verticale lijn
                Line(
                    DOWN * scale.get_value()/2,
                    UP * scale.get_value()/2
                ),
                # bovenste streepje
                Line(
                    UP * scale.get_value()/2 + LEFT*0.15,
                    UP * scale.get_value()/2 + RIGHT*0.15
                ),
                # onderste streepje
                Line(
                    DOWN * scale.get_value()/2 + LEFT*0.15,
                    DOWN * scale.get_value()/2 + RIGHT*0.15
                )
            ).next_to(drup, RIGHT, buff=0.5)
        )
        
        #en tekst erbij
        dropsize_text = Text("Size of the droplet", font_size=65)
        dropsize_text.to_edge(UP, buff=1)
        
        self.play(Write(dropsize_text), run_time=2)
        self.add(drup, staaf)
        self.play(scale.animate.set_value(2))
        self.play(scale.animate.set_value(0.4))
        self.play(scale.animate.set_value(1))
        self.wait()