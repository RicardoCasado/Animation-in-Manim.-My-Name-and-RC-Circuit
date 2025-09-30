from manim import *



class MyNameandRC_Circuit(Scene):
    def construct(self):
        
        #Define the points used on the plane
        points02=[
            np.array([-3,0,0]),   #0  
            np.array([3,0,0]),    #1  
            np.array([3,-3,0]),   #2
            np.array([-3,-3,0]),  #3
            np.array([0, 2, 0]),  #4
            np.array([3, 2, 0]),  #5
              
        ]

        #offset value
        valor01=-0.8
        valor02=1
        #parallel plate capacitor
        source_tension=[ np.array([valor01,0,0]) + points02[0], 
                         np.array([valor01,0,0]) + points02[3] 
                ]
        capacitor_tension=[ np.array([valor02,0,0]) + points02[1],
                            np.array([valor02,0,0]) + points02[2] 
                ]


        #Zigzag parameter
        n = 5           #Total segments (3 ascents and 3 descents) 
        dx = 0.3        #Horizontal separation between points 
        dy = 0.3        #Zigzag height 

        
        #1) Resistor Points
        points_diff=points02[4]-points02[5]         #Centered at the midpoint of the line joining points02[4] and points02[5] 
        length=points_diff[0]
        start_x=length*dx
        zigzag_points = [
            RIGHT * (start_x + i * dx) + (UP if i % 2 == 0 else DOWN) * dy
            for i in range(n + 1)
        ]

        #Beginning and end of the resistor
        resistor_start = zigzag_points[0]
        resistor_end = zigzag_points[-1]
        
        
        #left and right_point are the beggining and the end connected to the resistor  de la resistencia
        left_point = resistor_start + (LEFT + DOWN) * 0.3           #Beginning of the Line 
        right_point = resistor_end + (RIGHT + UP )* 0.3             # End of the Line  

        # 1.1) Assembled Resistor              
        # Here we join the left and right ends of the zigzag (resistor) to the np.array() points at the far left and right
        Allpoints=[ 
           points02[0], left_point, resistor_start, *zigzag_points, resistor_end, right_point, points02[1], points02[2]
        ]
        
        path01=VMobject().set_points_as_corners(Allpoints)              # Convert list to VMobject 
        path_zig = VMobject().set_points_as_corners(zigzag_points)




        #2) Words of my name.
        text01=Text("Ricardo").move_to(path01, UP)
        text02=Text("Casado").move_to(path01, UP)   
        nombres=VGroup(text01,text02).arrange(RIGHT, buff=0.3)  
        text01.align_to(text02, UP)                              # aligning heights         
        nombres.next_to(path_zig, UP, buff=0.3)
        
        # Slicing letters 
        letras_R, letras_icardo = text01[0], text01[1:]     # "R"  "icardo"                             
        letras_C, letras_asado  = text02[0], text02[1:]     # "C"  "asado"                              

        #Fixed margin 
        margin = 1.3
        #get_top() returns the 3D point [x,y,z] of the Mobject with the highest y-value.
        #path_zig.get_top() + margin * UP =  [0, margin, 0]
        target_anchor = path_zig.get_top() + margin * UP 
        


        # 2.1) Joining R and C at the center
        # We create copies to calculate the target position without moving the originals yet
        objetivo = (
            VGroup(letras_R.copy(), letras_C.copy())
            .arrange(RIGHT, buff=0.1)
            .move_to(target_anchor)     # target position
        )
        
        #Target position below of zigzag path
        molde = VGroup(letras_R.copy(), letras_C.copy()).arrange(RIGHT, buff=0.12)
        molde.move_to(path_zig.get_bottom())  # centra en X respecto al zigzag

        margin_R = 0.85
        margin_C = 1.55  
        r_target = molde[0].get_center() + margin_R*DOWN
        c_target = molde[1].get_center() + margin_C*DOWN

        


        #3)THIRD PART: capacitor of the electric circuit    
        # Initial position of capacitor (center between points02[1] and points02[2])
        mean_point = Line(points02[1], points02[2]).get_center()    # mean_point = (points02[1] + points02[2]) / 2 
        height = 0.2     
        width = 1.5     

        #3.1) Creating plates and capacitor
        top = mean_point + height * UP
        bottom = mean_point + height * DOWN
        plate1 = Line(top - width * RIGHT / 2, top + width * RIGHT / 2, color=WHITE, stroke_width=8 )
        plate2 = Line(bottom - width * RIGHT / 2, bottom + width * RIGHT / 2, color=WHITE, stroke_width=8 )

        #3.2) Creating Mask
        #Plates length
        rect_width=plate1.get_length()                 #weight
        rect_height=np.abs( top[1] - bottom[1] )       #heigth
        mask=Rectangle(
            width=rect_width,        
            height=rect_height,
            fill_color=BLACK,
            fill_opacity=1,
            stroke_width=0 
        ).move_to(mean_point)

        
        # 3.3) Creating the Power Source
        #Vertical line and its middle point
        source_path=Line(points02[3], points02[0], color=WHITE)
        midpoint_sourcepath=source_path.get_center()
        #The mask. Circle with full opacity
        circle02=Circle(radius=0.5, color=BLACK, fill_opacity=1.0, fill_color=BLACK)
        circle02=circle02.move_to(midpoint_sourcepath)        
        
        #Circle with its interior symbols
        circle01=Circle(radius=0.5, color=WHITE, fill_opacity=1.0, fill_color=BLACK)
        circle01=circle01.move_to(midpoint_sourcepath)
        top_circle01=circle01.get_top()  #Here uses Allpoints02
        
        #3.4) Symbols
        radius=0.2
        addition_circle = MathTex("+").scale(1).move_to(circle01.get_center() + UP*radius)
        subtraction_circle = MathTex("-").scale(1).move_to(circle01.get_center() + DOWN*radius)
        
        #3.5) Creating below line 
        below_line=Line(points02[2], points02[3])




        # 4) Path for the electrons / points
        # Points defining the electron path from the power supply to plate1 of the capacitor
        Allpoints02=[ 
           top_circle01, points02[0], left_point, resistor_start, *zigzag_points, resistor_end, right_point, points02[1], top
        ]           # It ends at 'top', not at points02[2]
        # Convert the list of points into a VMobject
        path_toplate1=VMobject().set_points_as_corners(Allpoints02) 



        #4.1) Tensions of Source and Capacitor

        
        #Label Tensions
        src_ref = Line(source_tension[0], source_tension[1])                    
        cap_ref = Line(capacitor_tension[0], capacitor_tension[1])              

        label_source = MathTex("V_s").next_to(src_ref, LEFT, buff=0.15)             
        label_capacitor = MathTex("V_c").next_to(cap_ref, RIGHT, buff=0.15)         

        #Tension Equation
        eq01=MathTex("V_s + V_c=0").move_to([0,-1.5,0])



        #5) Animations

        #5.1) Parameters
        m=8                   #numbers of electrons: m
        run_time = 4          # Each one takes 4sec to tour the line 
        launch_every = 0.8    # Launch  new point each  0.8s 
        plus_time = 0.3       #  duration of the FadeIn of the '+'  
        

        #5.2) Objects
        #electrons:: points   path_toplate1:: the path defines before
        electrons=[Dot(color=YELLOW).move_to(path_toplate1.get_start())
                   .set_opacity(0) 
                   .set_z_index(50)   # <- above of mask/circle 
                   for _ in range(m) 
        ] #Crea los puntos al inicio de la linea
        num_pairs=m//2 #numbers of symbols

        #addition and subtraction symbols
        additions=VGroup(*[Text("+").scale(0.6) for i in range(num_pairs)])
        subtraction=VGroup(*[Text("-").scale(1) for i in range(num_pairs)])
        
        #percentage
        perc = [0.1, 0.33, 0.67, 0.9]   
        
        # Vertical separation above plate1 and below plate2 respectively
        buff_plus  = 0.2                    # vertical separation above plate1
        buff_minus = 0.25                   # vertical separation below plate2

        # Place each symbol at the desired fraction of the plate
        for symbol, t in zip(additions, perc):
            symbol.move_to(plate1.point_from_proportion(t) + UP * buff_plus)

        for symbol, t in zip(subtraction, perc):
            symbol.move_to(plate2.point_from_proportion(t) + DOWN * buff_minus)




        #5.3) Animations List
        pair_seqs = []
        for k in range(num_pairs):
            d1 = electrons[2*k]             #it will use in seq1 
            d2 = electrons[2*k + 1]         #it will use in seq2

                        # Each electron: move and disappear
            seq1 = Succession(
                ApplyMethod(d1.set_opacity, 1, run_time=1e-6),      # Turn on
                MoveAlongPath(d1, path_toplate1, rate_func=linear, run_time=run_time),
                FadeOut(d1, run_time=0),
            )
            seq2 = Succession(
                ApplyMethod(d2.set_opacity, 1, run_time=1e-6),       # Turn on
                MoveAlongPath(d2, path_toplate1, rate_func=linear, run_time=run_time),
                FadeOut(d2, run_time=0),
            )
            # In the pair: the second one launches launch_every after the first
            # pair_motion stores the arrival of the even electron + the arrival of the odd electron
            pair_motion = LaggedStart(seq1, seq2, lag_ratio=launch_every / run_time )
    
            # When the pair finishes (the 2nd arrives), show the '+'
            # After both electrons (even + odd) arrive, use FadeIn()
            pair_seq = Succession(
                pair_motion,  #--> seq1 and seq2 using LaggedStart
                AnimationGroup(
                    FadeIn(additions[k], run_time=plus_time),
                    FadeIn(subtraction[k], run_time=plus_time),
                    lag_ratio=0.0  #simultanousley
                )
                            )
            pair_seqs.append(pair_seq)

        # Stagger PAIRS with a gap of 2*launch_every between starts
        # Duration of one pair: run_time + launch_every (for the 2nd) + plus_time
        pair_duration = run_time + launch_every + plus_time
        pair_lag_ratio = (2 * launch_every) / pair_duration




        #6) Scene
        self.wait(2)
        self.play(AnimationGroup(
                Write(text01),
                Write(text02),
                lag_ratio=0
                 ), run_time=3.5
            )  
        self.wait(1)
        #2) Unwrite  "icardo" y "asado"
        self.play(
                Unwrite(letras_icardo), 
                Unwrite(letras_asado), 
                run_time=3.5
            )
        self.wait(1)
        #3) Joining the letters R y C
        self.play(
            letras_R.animate.move_to(objetivo[0].get_center()), 
            letras_C.animate.move_to(objetivo[1].get_center()),
            run_time=2.5
        )
        self.wait(1)

        #4) Resistor Path
        self.play(Create(path01), run_time=3.5 )  # resistor
        self.wait(1)


        #5) Capacitor
        self.play(Create(plate1), Create(plate2), Create(mask), run_time=2)         #Capacitor
        self.play(Create(source_path,run_time=2))                                   #source line
        self.wait(1)
        
        #6) Symbols
        self.play( FadeIn(circle01), run_time=2)    
        self.play(FadeIn(addition_circle), FadeIn(subtraction_circle), run_time=2)
        self.wait(0.5)
        self.play(Create(below_line))
        self.wait(1)
        
        #7) Electrons
        self.play(LaggedStart(*pair_seqs, lag_ratio=pair_lag_ratio))
        self.wait(1)
        
        self.play(
                LaggedStart(
                   FadeIn(label_source,run_time=2),       #V_s y V_c
                   FadeIn(label_capacitor,run_time=2),
                   lag_ratio=0
                )
        )

        self.wait(1)
        self.play(FadeIn(eq01),run_time=2)
        self.wait(1.5)
        self.play(
                  Succession(
                  FadeOut(eq01, run_time=2), 
                  LaggedStart( 
                    FadeOut(label_source, run_time=2),
                    FadeOut(label_capacitor, run_time=2),
                    lag_ratio=0      
                    )
                  )
                )
        self.wait(2)
        
        self.play(
            letras_R.animate.move_to(r_target),
            letras_C.animate.move_to(c_target),
            run_time=2.5
        )
        self.wait(0.5)
        #Increase the separation of R and C
        sep_extra_R= 0.8
        sep_extra_C= -0.8
        self.play(
            letras_R.animate.shift(LEFT*sep_extra_R),
            letras_C.animate.shift(RIGHT*sep_extra_C),
            run_time=2
        )
        self.wait(0.5)
        # Same font of the original name
        base_style = dict(font=text01.font, weight=text01.weight, slant=text01.slant)

        tail_R = Text("icardo", **base_style).scale(1)
        tail_C = Text("asado",  **base_style).scale(1)
        
        # Place them next to R and C, aligned to the baseline
        tail_R.next_to(letras_R, RIGHT, buff=0.04).align_to(letras_R, DOWN)
        tail_C.next_to(letras_C, RIGHT, buff=0.04).align_to(letras_C, DOWN)

        # In front of the circuit lines (optional)
        tail_R.set_z_index(20)
        tail_C.set_z_index(20)
        
        self.wait(1)
        self.play(Write(tail_R), Write(tail_C), run_time=3.5)        
        
        self.wait(2)
        # In this final part, keep only the name, surname, resistor and capacitor

        #Vanish the additions and substraction symbols simultanously
        charges = VGroup(additions, subtraction)  # agrupa todos los símbolos
        self.play(FadeOut(charges), run_time=2)  # 
        self.wait(1)
        self.play(FadeOut(addition_circle), FadeOut(subtraction_circle) , run_time=2)  # 
        self.wait(1)
        self.play(FadeOut(below_line), run_time=2)  # 
        self.wait(1)
        self.play(
                LaggedStart(
                  FadeOut(circle01, run_time=2),
                  FadeOut(source_path, run_time=2),
                  lag_ratio=0

                )
        )

        self.wait(1)
        self.wait(6)