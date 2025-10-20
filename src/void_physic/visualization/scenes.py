"""
Main Manim scenes for void physics visualization.

This module contains the complete 4-act narrative animation showing
the emergence of spacetime from the void state.
"""

import logging

import numpy as np
from manim import *

from void_physic.core.potential import DoubleWellPotential, PotentialParameters
from void_physic.core.stochastic import LangevinDynamics, WhiteNoise
from void_physic.simulation.langevin_solver import LangevinSolver, SolverParameters
from void_physic.simulation.statistics import EntropyCalculator
from void_physic.utils.constants import PhysicalConstants

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VoidEmergenceScene(Scene):
    """
    Complete 4-act narrative animation of void physics.

    Act 1: The Void - Abstract topological space (no metric)
    Act 2: Instability - Fluctuation η(t) triggers nucleation
    Act 3: Emergence - φ rolls down potential, spacetime forms
    Act 4: Time's Arrow - Entropy S(t) increases, time flows
    """

    def construct(self):
        # Set up parameters
        self.setup_parameters()

        # Act 1: The Void
        self.act_1_the_void()

        # Act 2: Instability
        self.act_2_instability()

        # Act 2.5: Quantum Fluctuations
        self.act_2_5_quantum_fluctuations()

        # Act 3: Emergence
        self.act_3_emergence()

        # Act 4: Time's Arrow
        self.act_4_times_arrow()

        # Final summary
        self.final_summary()

    def setup_parameters(self):
        """Set up simulation parameters."""
        self.potential_params = PotentialParameters(
            lambda_coupling=1.0, v_vev=1.0, V0_offset=0.0
        )

        self.constants = PhysicalConstants(
            gamma_friction=1.0, noise_strength=0.5, dt_default=0.01
        )

        self.solver_params = SolverParameters(
            dt=0.01, t_max=20.0, n_trajectories=50, save_trajectories=True
        )

    def act_1_the_void(self):
        """Act 1: The Void - Abstract topological space."""
        # Clear screen
        self.clear()

        # Title
        title = Text("Act 1: The Void", font_size=48, color=BLUE)
        title.to_edge(UP)
        self.add(title)

        # Void description
        void_text = Text(
            "The void is a topological limit state:\n"
            "• No metric, no time, no space\n"
            "• Perfect symmetry\n"
            "• All states are equivalent\n"
            "• 0/0 indeterminacy",
            font_size=24,
            color=WHITE,
        )
        void_text.move_to(ORIGIN)

        self.play(Write(void_text), run_time=3)
        self.wait(2)

        # Show abstract void
        void_circle = Circle(radius=2, color=BLUE, stroke_width=4)
        void_circle.set_fill(BLUE, opacity=0.3)

        void_label = Text("Void", font_size=36, color=BLUE)
        void_label.move_to(void_circle.get_center())

        self.play(Create(void_circle), Write(void_label), run_time=2)
        self.wait(1)

        # Show symmetry
        symmetry_text = Text("Perfect Symmetry", font_size=20, color=YELLOW)
        symmetry_text.next_to(void_circle, DOWN)

        self.play(Write(symmetry_text), run_time=1)
        self.wait(1)

        # Transition to next act
        self.play(FadeOut(void_text), FadeOut(symmetry_text), run_time=1)

        # Update title
        self.play(
            Transform(title, Text("Act 2: Instability", font_size=48, color=YELLOW)),
            run_time=1,
        )

    def act_2_instability(self):
        """Act 2: Instability - Fluctuation triggers nucleation."""
        # Show potential landscape
        potential_axes = Axes(
            x_range=[-2, 2, 0.5],
            y_range=[-0.5, 1.5, 0.5],
            x_length=8,
            y_length=4,
            axis_config={"color": GRAY},
            tips=False,
        )

        # Create potential curve
        potential_curve = potential_axes.plot(
            lambda x: DoubleWellPotential()(np.array([x]))[0],
            x_range=[-2, 2],
            color=BLUE,
            stroke_width=4,
        )

        # Add critical points
        void_point = potential_axes.coords_to_point(
            0, DoubleWellPotential()(np.array([0]))[0]
        )
        void_dot = Dot(void_point, color=RED, radius=0.1)

        self.play(
            Create(potential_axes),
            Create(potential_curve),
            Create(void_dot),
            run_time=2,
        )

        # Show fluctuation
        fluctuation_text = Text(
            "Quantum fluctuation η(t) breaks symmetry", font_size=20, color=YELLOW
        )
        fluctuation_text.to_edge(DOWN)

        self.play(Write(fluctuation_text), run_time=1)

        # Show noise
        noise_curve = potential_axes.plot(
            lambda x: 0.3 * np.sin(10 * x) * np.exp(-(x**2)),
            x_range=[-2, 2],
            color=YELLOW,
            stroke_width=2,
        )

        self.play(Create(noise_curve), run_time=1)
        self.wait(1)

        # Show instability
        instability_text = Text(
            "Instability grows exponentially", font_size=20, color=ORANGE
        )
        instability_text.to_edge(DOWN)

        self.play(Transform(fluctuation_text, instability_text), run_time=1)

        # Show exponential growth
        growth_curve = potential_axes.plot(
            lambda x: 0.1 * np.exp(2 * x) if x > 0 else 0,
            x_range=[0, 2],
            color=ORANGE,
            stroke_width=3,
        )

        self.play(Create(growth_curve), run_time=1)
        self.wait(1)

        # Transition to next act
        self.play(
            FadeOut(fluctuation_text),
            FadeOut(noise_curve),
            FadeOut(growth_curve),
            run_time=1,
        )

    def act_2_5_quantum_fluctuations(self):
        """Act 2.5: Quantum Fluctuations - Ψ triggers void instability."""
        # Title
        quantum_title = Text("Quantum Fluctuations", font_size=24, color=CYAN)
        quantum_title.to_edge(UP)
        self.play(Write(quantum_title))
        
        # Set up quantum axes
        quantum_axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-1, 1, 0.5],
            x_length=8,
            y_length=4,
            axis_config={"color": CYAN},
            tips=False,
        )
        
        # Create wave function visualization
        def wave_function(x):
            return 0.5 * np.exp(-x**2 / 2) * np.sin(3 * x)
        
        psi_curve = quantum_axes.plot(
            wave_function,
            x_range=[-3, 3],
            color=YELLOW,
            stroke_width=3,
        )
        
        # Show wave function
        self.play(Create(quantum_axes))
        self.play(Create(psi_curve))
        
        # Add wave function label
        psi_label = MathTex(r"\Psi(x,t)", font_size=20, color=YELLOW)
        psi_label.next_to(psi_curve, UP)
        self.play(Write(psi_label))
        
        # Show probability density
        def probability_density(x):
            return wave_function(x)**2
        
        prob_curve = quantum_axes.plot(
            probability_density,
            x_range=[-3, 3],
            color=GREEN,
            stroke_width=2,
        )
        
        prob_label = MathTex(r"|\Psi|^2", font_size=20, color=GREEN)
        prob_label.next_to(prob_curve, DOWN)
        
        self.play(Create(prob_curve))
        self.play(Write(prob_label))
        
        # Show quantum uncertainty
        uncertainty_text = Text(
            "Quantum uncertainty: Δx Δp ≥ ℏ/2", 
            font_size=18, 
            color=ORANGE
        )
        uncertainty_text.to_edge(DOWN)
        self.play(Write(uncertainty_text))
        
        # Animate wave function evolution
        for i in range(20):
            # Simple wave packet spreading
            def evolved_wave(x, t=i*0.1):
                return 0.5 * np.exp(-x**2 / (2 + t)) * np.sin(3 * x + t)
            
            new_psi_curve = quantum_axes.plot(
                lambda x: evolved_wave(x),
                x_range=[-3, 3],
                color=YELLOW,
                stroke_width=3,
            )
            
            new_prob_curve = quantum_axes.plot(
                lambda x: evolved_wave(x)**2,
                x_range=[-3, 3],
                color=GREEN,
                stroke_width=2,
            )
            
            self.play(
                Transform(psi_curve, new_psi_curve),
                Transform(prob_curve, new_prob_curve),
                run_time=0.1
            )
        
        # Show connection to void instability
        connection_text = Text(
            "When |Ψ|² > threshold → particle emergence", 
            font_size=18, 
            color=RED
        )
        connection_text.to_edge(DOWN)
        
        self.play(Transform(uncertainty_text, connection_text))
        
        # Show threshold line
        threshold_line = quantum_axes.plot(
            lambda x: 0.3,  # Threshold value
            x_range=[-3, 3],
            color=RED,
            stroke_width=2,
            stroke_dasharray=[5, 5]
        )
        
        self.play(Create(threshold_line))
        
        # Highlight regions above threshold
        above_threshold = quantum_axes.plot(
            lambda x: max(0, probability_density(x) - 0.3),
            x_range=[-3, 3],
            color=RED,
            stroke_width=4,
        )
        
        self.play(Create(above_threshold))
        
        # Add equation
        equation = MathTex(
            r"i\hbar \frac{\partial \Psi}{\partial t} = \hat{H}\Psi",
            font_size=16,
            color=WHITE
        )
        equation.to_corner(UR)
        self.play(Write(equation))
        
        self.wait(2)
        
        # Transition to next act
        self.play(
            FadeOut(quantum_title),
            FadeOut(psi_label),
            FadeOut(prob_label),
            FadeOut(uncertainty_text),
            FadeOut(threshold_line),
            FadeOut(above_threshold),
            FadeOut(equation),
            run_time=1,
        )

        # Update title
        title = self.mobjects[0]  # Assuming title is first object
        self.play(
            Transform(title, Text("Act 3: Emergence", font_size=48, color=GREEN)),
            run_time=1,
        )

    def act_3_emergence(self):
        """Act 3: Emergence - Field rolls down potential, spacetime forms."""
        # Show field evolution
        field_axes = Axes(
            x_range=[0, 20, 5],
            y_range=[-2, 2, 0.5],
            x_length=10,
            y_length=4,
            axis_config={"color": GRAY},
            tips=False,
        )

        # Create field trajectory
        field_curve = field_axes.plot(
            lambda t: 1.0 * np.tanh(t - 10),  # Simplified field evolution
            x_range=[0, 20],
            color=GREEN,
            stroke_width=4,
        )

        self.play(Create(field_axes), Create(field_curve), run_time=2)

        # Show emergence text
        emergence_text = Text(
            "Field rolls from void to ordered state", font_size=20, color=GREEN
        )
        emergence_text.to_edge(DOWN)

        self.play(Write(emergence_text), run_time=1)

        # Show spacetime formation
        spacetime_text = Text(
            "Spacetime emerges from field configuration", font_size=20, color=BLUE
        )
        spacetime_text.to_edge(DOWN)

        self.play(Transform(emergence_text, spacetime_text), run_time=1)

        # Show metric formation
        metric_text = Text(
            "Metric g_μν forms from field dynamics", font_size=20, color=PURPLE
        )
        metric_text.to_edge(DOWN)

        self.play(Transform(emergence_text, metric_text), run_time=1)

        self.wait(1)

        # Transition to next act
        self.play(FadeOut(emergence_text), run_time=1)

        # Update title
        title = self.mobjects[0]
        self.play(
            Transform(title, Text("Act 4: Time's Arrow", font_size=48, color=RED)),
            run_time=1,
        )

    def act_4_times_arrow(self):
        """Act 4: Time's Arrow - Entropy increases, time flows."""
        # Show entropy evolution
        entropy_axes = Axes(
            x_range=[0, 20, 5],
            y_range=[0, 3, 0.5],
            x_length=10,
            y_length=4,
            axis_config={"color": GRAY},
            tips=False,
        )

        # Create entropy curve
        entropy_curve = entropy_axes.plot(
            lambda t: 0.5 * np.log(1 + t),  # Simplified entropy evolution
            x_range=[0, 20],
            color=RED,
            stroke_width=4,
        )

        self.play(Create(entropy_axes), Create(entropy_curve), run_time=2)

        # Show entropy text
        entropy_text = Text(
            "Entropy S(t) increases monotonically", font_size=20, color=RED
        )
        entropy_text.to_edge(DOWN)

        self.play(Write(entropy_text), run_time=1)

        # Show time's arrow
        time_arrow = Arrow(
            start=entropy_axes.coords_to_point(0, 0),
            end=entropy_axes.coords_to_point(20, 0),
            color=YELLOW,
            stroke_width=6,
        )

        arrow_text = Text("Time's Arrow", font_size=20, color=YELLOW)
        arrow_text.next_to(time_arrow, DOWN)

        self.play(Create(time_arrow), Write(arrow_text), run_time=1)

        # Show time emergence
        time_text = Text(
            "Time emerges from entropy gradient", font_size=20, color=ORANGE
        )
        time_text.to_edge(DOWN)

        self.play(Transform(entropy_text, time_text), run_time=1)

        # Show equation
        equation = MathTex(
            "t \\propto \\int \\frac{dS}{\\mathcal{R}(S)}", font_size=24, color=WHITE
        )
        equation.to_edge(DOWN)

        self.play(Write(equation), run_time=2)
        self.wait(1)

        # Transition to summary
        self.play(
            FadeOut(entropy_text), FadeOut(arrow_text), FadeOut(equation), run_time=1
        )

        # Update title
        title = self.mobjects[0]
        self.play(
            Transform(title, Text("Void Physics Summary", font_size=48, color=WHITE)),
            run_time=1,
        )

    def final_summary(self):
        """Final summary of void physics."""
        summary_text = Text(
            "Void Physics: From Nothing to Everything\n\n"
            "1. Void: Topological limit state with perfect symmetry\n"
            "2. Instability: Quantum fluctuations break symmetry\n"
            "3. Emergence: Field rolls to ordered state, spacetime forms\n"
            "4. Time's Arrow: Entropy increases, time flows forward\n\n"
            "The universe emerges from the void through\n"
            "quantum fluctuations and entropy production.",
            font_size=18,
            color=WHITE,
        )
        summary_text.move_to(ORIGIN)

        self.play(Write(summary_text), run_time=5)
        self.wait(3)
        self.play(FadeOut(summary_text), run_time=2)

        # Final message
        final_message = Text(
            "The void contains all possibilities.\n"
            "From the void, everything emerges.",
            font_size=24,
            color=BLUE,
        )
        final_message.move_to(ORIGIN)

        self.play(Write(final_message), run_time=3)
        self.wait(2)
        self.play(FadeOut(final_message), run_time=2)


class VoidEmergence3D(ThreeDScene):
    """
    3D version of the void emergence narrative.

    Shows the complete story in 3D space for enhanced visual impact.
    """

    def construct(self):
        # Set up 3D scene
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)

        # Act 1: The Void (3D)
        self.act_1_void_3d()

        # Act 2: Instability (3D)
        self.act_2_instability_3d()

        # Act 3: Emergence (3D)
        self.act_3_emergence_3d()

        # Act 4: Time's Arrow (3D)
        self.act_4_times_arrow_3d()

        # Final summary
        self.final_summary_3d()

    def act_1_void_3d(self):
        """Act 1: The Void in 3D."""
        # Create 3D void sphere
        void_sphere = Sphere(radius=1, color=BLUE, fill_opacity=0.3)

        # Add title
        title = Text("Act 1: The Void", font_size=36, color=BLUE)
        title.to_edge(UP)

        self.add(title)
        self.play(Create(void_sphere), run_time=2)
        self.wait(1)

        # Rotate sphere
        self.play(Rotate(void_sphere, angle=PI, axis=UP), run_time=2)
        self.wait(1)

        # Transition
        self.play(FadeOut(void_sphere), run_time=1)
        self.play(
            Transform(title, Text("Act 2: Instability", font_size=36, color=YELLOW)),
            run_time=1,
        )

    def act_2_instability_3d(self):
        """Act 2: Instability in 3D."""

        # Create 3D potential surface
        def potential_function(x, y):
            return DoubleWellPotential()(np.array([x]))[0]

        potential_surface = Surface(
            potential_function,
            u_range=[-2, 2],
            v_range=[-1, 1],
            resolution=(50, 50),
            fill_opacity=0.7,
            stroke_width=1,
            fill_color=BLUE,
            stroke_color=WHITE,
        )

        self.play(Create(potential_surface), run_time=2)
        self.wait(1)

        # Show fluctuation
        fluctuation_sphere = Sphere(radius=0.1, color=YELLOW)
        fluctuation_sphere.move_to([0, 0, 1])

        self.play(Create(fluctuation_sphere), run_time=1)

        # Animate fluctuation
        self.play(fluctuation_sphere.animate.move_to([0.5, 0, 0.5]), run_time=2)

        self.wait(1)

        # Transition
        self.play(FadeOut(potential_surface), FadeOut(fluctuation_sphere), run_time=1)
        title = self.mobjects[0]
        self.play(
            Transform(title, Text("Act 3: Emergence", font_size=36, color=GREEN)),
            run_time=1,
        )

    def act_3_emergence_3d(self):
        """Act 3: Emergence in 3D."""

        # Create 3D field evolution
        def field_function(x, y):
            return 0.5 * np.tanh(x - 5)

        field_surface = Surface(
            field_function,
            u_range=[0, 10],
            v_range=[0, 5],
            resolution=(50, 50),
            fill_opacity=0.7,
            stroke_width=1,
            fill_color=GREEN,
            stroke_color=WHITE,
        )

        self.play(Create(field_surface), run_time=2)
        self.wait(1)

        # Show spacetime formation
        spacetime_cube = Cube(side_length=1, color=BLUE, fill_opacity=0.5)
        spacetime_cube.move_to([5, 0, 0])

        self.play(Create(spacetime_cube), run_time=1)
        self.wait(1)

        # Transition
        self.play(FadeOut(field_surface), FadeOut(spacetime_cube), run_time=1)
        title = self.mobjects[0]
        self.play(
            Transform(title, Text("Act 4: Time's Arrow", font_size=36, color=RED)),
            run_time=1,
        )

    def act_4_times_arrow_3d(self):
        """Act 4: Time's Arrow in 3D."""

        # Create 3D entropy evolution
        def entropy_function(x, y):
            return 0.5 * np.log(1 + x)

        entropy_surface = Surface(
            entropy_function,
            u_range=[0, 10],
            v_range=[0, 5],
            resolution=(50, 50),
            fill_opacity=0.7,
            stroke_width=1,
            fill_color=RED,
            stroke_color=WHITE,
        )

        self.play(Create(entropy_surface), run_time=2)
        self.wait(1)

        # Show time arrow
        time_arrow = Arrow3D(
            start=[0, 0, 0], end=[10, 0, 0], color=YELLOW, thickness=0.1
        )

        self.play(Create(time_arrow), run_time=1)
        self.wait(1)

        # Transition
        self.play(FadeOut(entropy_surface), FadeOut(time_arrow), run_time=1)
        title = self.mobjects[0]
        self.play(
            Transform(title, Text("Void Physics Summary", font_size=36, color=WHITE)),
            run_time=1,
        )

    def final_summary_3d(self):
        """Final summary in 3D."""
        # Create 3D summary
        summary_sphere = Sphere(radius=1.5, color=WHITE, fill_opacity=0.3)

        self.play(Create(summary_sphere), run_time=2)

        # Rotate camera
        self.begin_ambient_camera_rotation(rate=0.1)
        self.wait(5)
        self.stop_ambient_camera_rotation()

        self.play(FadeOut(summary_sphere), run_time=2)
