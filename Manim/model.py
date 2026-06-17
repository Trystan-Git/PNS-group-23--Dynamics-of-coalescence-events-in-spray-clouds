from manim import *
import numpy as np


class model(MovingCameraScene):
    def construct(self):
        nozzle = Rectangle(
            fill_color=BLACK,
            fill_opacity=0.5,
            height=2.5,
            width=5
        )

        no_wave_jet = Rectangle(
            color=BLUE,
            height=2,
            width=5,
            fill_color=BLUE,
            fill_opacity=1
        )

        wavelength = 1.5
        R1 = 0.30
        R2 = 0.40
        half_thickness = 0.4   
        total_width = 10
        n_points = 200
        omega = 1.5
        ramp_length = 1.5    
        
        halve_cirkel= Circle(
            color=BLUE, 
            radius = 0.7, 
            fill_color=BLUE, 
            fill_opacity=1
        )  
        
        droplet1= Circle(
            color=BLUE, 
            radius = 0.7, 
            fill_color=BLUE, 
            fill_opacity=1
        )  
        droplet2= Circle(
            color=BLUE, 
            radius = 0.7, 
            fill_color=BLUE, 
            fill_opacity=1
        )  
        droplet3= Circle(
            color=BLUE, 
            radius = 0.7, 
            fill_color=BLUE, 
            fill_opacity=1
        )  
        droplet4= Circle(
            color=BLUE, 
            radius = 0.7, 
            fill_color=BLUE, 
            fill_opacity=1
        )  
        
        droplet5= Circle(
            color=BLUE, 
            radius = 0.7, 
            fill_color=BLUE, 
            fill_opacity=1
        )  
        
        droplet6= Circle(
            color=BLUE, 
            radius = 0.7, 
            fill_color=BLUE, 
            fill_opacity=1
        )  
        
        droplet7= Circle(
            color=BLUE, 
            radius = 0.7, 
            fill_color=BLUE, 
            fill_opacity=1
        )  
        droplet8= Circle(
            color=BLUE, 
            radius = 0.7, 
            fill_color=BLUE, 
            fill_opacity=1
        )  
        droplet9= Circle(
            color=BLUE, 
            radius = 0.7, 
            fill_color=BLUE, 
            fill_opacity=1
        )  
        droplet10= Circle(
            color=BLUE, 
            radius = 0.7, 
            fill_color=BLUE, 
            fill_opacity=1
        )  
        droplet11= Circle(
            color=BLUE, 
            radius = 0.7, 
            fill_color=BLUE, 
            fill_opacity=1
        )  
        droplet12= Circle(
            color=BLUE, 
            radius = 0.7, 
            fill_color=BLUE, 
            fill_opacity=1
        )  
        droplet13= Circle(
            color=BLUE, 
            radius = 0.7, 
            fill_color=BLUE, 
            fill_opacity=1
        )  
        droplet14= Circle(
            color=BLUE, 
            radius = 0.7, 
            fill_color=BLUE, 
            fill_opacity=1
        )  
        droplet15= Circle(
            color=BLUE, 
            radius = 0.7, 
            fill_color=BLUE, 
            fill_opacity=1
        )  
        droplet16= Circle(
            color=BLUE, 
            radius = 0.7, 
            fill_color=BLUE, 
            fill_opacity=1
        )  
        droplet17= Circle(
            color=BLUE, 
            radius = 0.7, 
            fill_color=BLUE, 
            fill_opacity=1
        )  
        black_droplet = Circle(
            color = BLACK, 
            radius=0.1, 
            fill_color = BLACK, 
            fill_opacity = 1
        )

        self.camera.frame.save_state()

        nozzle.set_z_index(2)
        no_wave_jet.set_z_index(1)

        self.play(Create(nozzle), run_time=1.5)

        self.play(
            nozzle.animate.shift(LEFT * 5).scale(0.4),
            no_wave_jet.animate.shift(LEFT * 5).scale(0.4),
            run_time=1.5
        )

        self.play(
            nozzle.animate.shift(LEFT),
            no_wave_jet.animate
                .stretch(7, dim=0)
                .shift(RIGHT * 5),
            run_time=2
        )

        self.play(
            nozzle.animate.shift(LEFT * 3),
            run_time=0.5
        )
        join_x = no_wave_jet.get_right()[0]

        time = ValueTracker(0)

        def make_shape():
            t = time.get_value()
            envelope_t = np.sin(omega * t)                      
            xs = np.linspace(join_x, join_x + total_width, n_points)
            dist = xs - join_x
            ramp = np.clip(dist / ramp_length, 0, 1)

            top = [
                [x, half_thickness + R1 * envelope_t * ramp[i] *
                 np.sin( 2* PI * dist[i] / wavelength), 0]
                for i, x in enumerate(xs)
            ]
            
            bottom = [
                [x, -half_thickness - R2 * envelope_t * ramp[i] *
                 np.sin(2* PI * dist[i] / wavelength), 0]
                for i, x in reversed(list(enumerate(xs)))
            ]

            shape = VMobject()
            shape.set_points_as_corners(top + bottom + [top[0]])
            shape.set_fill(BLUE, opacity=1)
            shape.set_stroke(BLUE, width=4)   
            return shape

        wave = always_redraw(make_shape)
        
        self.play(
            Create(wave),
            run_time=0.1)
        
        self.add(halve_cirkel, droplet1, droplet2, droplet3, droplet4, droplet5, droplet6, droplet7, droplet8, droplet9, droplet10, droplet11, droplet12, droplet13, droplet14, droplet15, droplet16, droplet17)
        halve_cirkel.set_x(17.8)
        droplet1.set_x(19.8)
        droplet2.set_x(21.8)
        droplet3.set_x(23.8)
        droplet4.set_x(25.8)
        droplet5.set_x(27.8)
        droplet6.set_x(29.8)
        droplet7.set_x(31.8)
        droplet8.set_x(33.8)
        droplet9.set_x(35.8)
        droplet10.set_x(37.8)
        droplet11.set_x(39.8)
        droplet12.set_x(41.8)
        droplet13.set_x(43.8)
        droplet14.set_x(45.8)
        droplet15.set_x(47.8)
        droplet16.set_x(49.8)
        droplet17.set_x(51.8)
        
        
        label = Text("Mean velocity", font_size=32)

        moving_label = always_redraw(
            lambda: label.move_to(
                self.camera.frame.get_center() + UP*1.5  + LEFT * 2  
            )
        )

        tracking_arrow = always_redraw(
            lambda: Arrow(
                start=moving_label.get_right(),
                end=moving_label.get_right()+ RIGHT * 1.5, 
                buff=0.1,
                color=WHITE
            ))
        
        label2 = Text("Standard deviation in velocity", font_size=32)

        moving_label2 = always_redraw(
            lambda: label2.move_to(
                self.camera.frame.get_center() + DOWN*1.5  + LEFT * 3 
            )
        )

        tracking_arrow2 = always_redraw(
            lambda: Arrow(
                start=moving_label2.get_right(),
                end=moving_label2.get_right()+ RIGHT * 1.5, 
                buff=0.1,
                color=WHITE
            ))
        

        
        self.play(
            time.animate(rate_func=linear).set_value(0.95),
            self.camera.frame.animate.move_to(halve_cirkel.get_right()),
            run_time=5,
        )
        
        self.add(
            moving_label, tracking_arrow
        )
        
        self.play(
            self.camera.frame.animate.move_to(droplet4.get_right()),
            run_time=3,
        )
        
        self.add(
            moving_label2, tracking_arrow2
        )
        
        self.play(
            droplet3.animate.shift(RIGHT*1.1),
            droplet5.animate.shift(LEFT*1.5), 
            droplet6.animate.shift(LEFT*1.25), 
            droplet8.animate.shift(RIGHT*1.1), 
            droplet9.animate.shift(LEFT*1.5), 
            self.camera.frame.animate.move_to(droplet10.get_right()),
            run_time=3
        )
        
        label3 = Text("Distance between nozzles", font_size=32)

        moving_label3 = always_redraw(
            lambda: label3.move_to(
                self.camera.frame.get_center() + UP*1.5  + LEFT * 2  
            )
        )
        
        self.play(
            FadeOut(moving_label, tracking_arrow, moving_label2, tracking_arrow2),
            run_time=0.5
        )
 
 
        baseline_y = -2

        mid_y13 = (droplet13.get_center()[1] + baseline_y) / 2 
        mid_y14 = (droplet14.get_center()[1] + baseline_y) / 2 
        mid_y15 = (droplet15.get_center()[1] + baseline_y) / 2 
        mid_y16 = (droplet16.get_center()[1] + baseline_y) / 2 
        mid_y17 = (droplet17.get_center()[1] + baseline_y) / 2 

        self.add(
            moving_label3,
            Line(start=droplet13.get_center()+DOWN, end=np.array([droplet13.get_center()[0], baseline_y, 0]), color=WHITE, stroke_width=2,),
            Line(start=droplet14.get_center()+DOWN, end=np.array([droplet14.get_center()[0], baseline_y, 0]), color=WHITE, stroke_width=2,),
            Line(start=droplet15.get_center()+DOWN, end=np.array([droplet15.get_center()[0], baseline_y, 0]), color=WHITE, stroke_width=2,),
            Line(start=droplet16.get_center()+DOWN, end=np.array([droplet16.get_center()[0], baseline_y, 0]), color=WHITE, stroke_width=2,),
            Line(start=droplet17.get_center()+DOWN, end=np.array([droplet17.get_center()[0], baseline_y, 0]), color=WHITE, stroke_width=2,),
            Line(
                start=np.array([droplet13.get_center()[0], mid_y13, 0]),
                end=np.array([droplet14.get_center()[0], mid_y14, 0]),
                color=WHITE, stroke_width=2,
            ),
            Line(
                start=np.array([droplet14.get_center()[0], mid_y14, 0]),
                end=np.array([droplet15.get_center()[0], mid_y15, 0]),
                color=WHITE, stroke_width=2,
            ),
            Line(
                start=np.array([droplet15.get_center()[0], mid_y15, 0]),
                end=np.array([droplet16.get_center()[0], mid_y16, 0]),
                color=WHITE, stroke_width=2,
            ),
            Line(
                start=np.array([droplet16.get_center()[0], mid_y16, 0]),
                end=np.array([droplet17.get_center()[0], mid_y17, 0]),
                color=WHITE, stroke_width=2,
        ))

        self.play(
            self.camera.frame.animate.move_to(droplet17.get_center()),
            run_time=4
        )
        
        self.add(black_droplet)
        black_droplet.set_x(80)
        
        self.play(
            FadeOut(moving_label3)
            self.camera.frame.animate.move_to(black_droplet.get_center()),
            run_time=4
        )
        
        
        
       
        

                
                    
        