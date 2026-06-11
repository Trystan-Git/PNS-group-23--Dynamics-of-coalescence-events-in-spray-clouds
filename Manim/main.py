
        
from manim import *
from manim_physics import *

class het(Scene):
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

        Waterdrop1 = Circle(
            color= BLUE,
            radius= 0.05,
            fill_color=BLUE,
            fill_opacity=0.8
        ).shift(UP * 2)

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
        ).shift(UP * 2)

        Waterdrop4 = Circle(
            color= BLUE,
            radius= 0.05,
            fill_color=BLUE,
            fill_opacity=0.8
        ).shift(UP * 2)

        Waterdrop5 = Circle(
            color= BLUE,
            radius= 0.05,
            fill_color=BLUE,
            fill_opacity=0.8
        ).shift(UP * 2)

        # #De grote samengesmolten druppel
        # Waterdroop = Circle(
        #    color=BLUE,
        #    radius=0.08,
        #    fill_color=BLUE,
        #    fill_opacity=0.8
        # ).shift(DOWN)

        nozzletext = Text(r"Our nozzle").shift(UP*2.4)

        self.play(Create(nozzle))
        self.play(Write(nozzletext))
        self.wait(1.5)
        
        self.play(Unwrite(nozzletext))
        self.play(nozzle.animate.shift(UP * 3).scale(0.4))

        self.add(WaterJet)
        self.play(WaterJet.animate.shift(DOWN*0.84))
        
        self.add(Waterdrop1, Waterdrop2, Waterdrop3, Waterdrop4, Waterdrop5)


        self.play(
            # Waterdrop 1 vertrekt meteen
            Waterdrop1.animate(run_time=3).shift(DOWN * 8),
    
            # Waterdrop 2: Valt naar DOWN*3 en verandert daar in Waterdroop
            Succession(
                Wait(run_time=0.4),
                Waterdrop2.animate(run_time=2.0).shift(DOWN * 3),
                ScaleInPlace(Waterdrop2, scale_factor=1.5, run_time=0.01),
                Wait(run_time=0.05),
            ),
            
            Succession(
                Wait(run_time=2.45),
                Waterdrop2.animate(run_time=1.5).shift(DOWN*8)
            ),

            Succession(
                Wait(run_time=0.8),  
                Waterdrop3.animate(run_time=1.6).shift(DOWN * 3), # 1.6s voor de perfecte gelijke timing
                FadeOut(Waterdrop3, run_time=0.05)
            ),

            # Waterdrop 4
            Succession(
                Wait(run_time=1.2),
                Waterdrop4.animate(run_time=3).shift(DOWN * 8)
            ),
            
            # Waterdrop 5
            Succession(
                Wait(run_time=1.6),
                Waterdrop5.animate(run_time=3).shift(DOWN * 8)
            )     
        )
        self.wait(1)