"""
Manim scene for visualizing the potential landscape in void physics.

This scene shows the double-well potential with a ball rolling animation
to demonstrate the transition from void to ordered states.
"""

import logging

import numpy as np
from manim import *

from void_physic.core.potential import DoubleWellPotential, PotentialParameters
from void_physic.core.stochastic import LangevinDynamics, WhiteNoise
from void_physic.utils.constants import PhysicalConstants

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PotentialLandscapeScene(Scene):
    """
    Scene visualizing the potential landscape and field dynamics.

    Shows:
    1. Double-well potential V(φ) = (λ/4)(φ² - v²)²
    2. Ball rolling animation representing field evolution
    3. Quantum tunneling visualization
    4. Instanton trajectory overlay
    """

    def construct(self):
        # Set up parameters
        potential_params = PotentialParameters(
            lambda_coupling=1.0, v_vev=1.0, V0_offset=0.0
        )

        potential = DoubleWellPotential(potential_params)

        # Create coordinate system
        self.setup_coordinate_system()

        # Draw potential landscape
        potential_curve = self.create_potential_curve(potential)

        # Add labels and annotations
        labels = self.create_labels()

        # Create ball for rolling animation
        ball = self.create_ball()

        # Show potential landscape
        self.play(Create(potential_curve), run_time=2)
        self.play(Create(labels), run_time=1)

        # Ball rolling animation
        self.animate_ball_rolling(ball, potential_curve)

        # Show quantum tunneling
        self.show_quantum_tunneling(potential_curve)

        # Show instanton trajectory
        self.show_instanton_trajectory(potential_curve)

        # Final summary
        self.show_summary()

    def setup_coordinate_system(self):
        """Set up the coordinate system and axes."""
        # Create axes
        axes = Axes(
            x_range=[-2.5, 2.5, 0.5],
            y_range=[-0.5, 1.5, 0.5],
            x_length=10,
            y_length=6,
            axis_config={"color": GRAY},
            tips=False,
        )

        # Add axis labels
        x_label = axes.get_x_axis_label("\\phi", edge=DOWN, direction=DOWN, buff=0.4)
        y_label = axes.get_y_axis_label("V(\\phi)", edge=LEFT, direction=LEFT, buff=0.4)

        self.add(axes, x_label, y_label)
        self.axes = axes

    def create_potential_curve(self, potential):
        """Create the potential curve."""
        # Generate potential data
        phi_range = np.linspace(-2.5, 2.5, 1000)
        V_values = potential(phi_range)

        # Create curve
        potential_curve = self.axes.plot(
            lambda x: potential(np.array([x]))[0],
            x_range=[-2.5, 2.5],
            color=BLUE,
            stroke_width=4,
        )

        # Add critical points
        critical_points = potential.critical_points()

        # Symmetric point (void state)
        void_point = self.axes.coords_to_point(0, potential(np.array([0]))[0])
        void_dot = Dot(void_point, color=RED, radius=0.1)
        void_label = MathTex("\\text{Void}", color=RED).next_to(void_dot, UP)

        # Vacuum points
        vacuum_points = []
        for name, phi_val in critical_points.items():
            if name != "symmetric":
                point = self.axes.coords_to_point(
                    phi_val, potential(np.array([phi_val]))[0]
                )
                dot = Dot(point, color=GREEN, radius=0.1)
                label = MathTex(f"\\text{{Vacuum}}", color=GREEN).next_to(dot, UP)
                vacuum_points.extend([dot, label])

        # Combine all elements
        potential_elements = [potential_curve, void_dot, void_label] + vacuum_points

        return potential_elements

    def create_labels(self):
        """Create labels and annotations."""
        # Title
        title = Text("Double-Well Potential", font_size=36, color=WHITE)
        title.to_edge(UP)

        # Equation
        equation = MathTex(
            "V(\\phi) = \\frac{\\lambda}{4}(\\phi^2 - v^2)^2", font_size=24
        )
        equation.next_to(title, DOWN)

        # Physical interpretation
        interpretation = Text(
            "Void state (φ=0) is metastable and can nucleate ordered domains",
            font_size=20,
            color=YELLOW,
        )
        interpretation.to_edge(DOWN)

        return [title, equation, interpretation]

    def create_ball(self):
        """Create a ball for the rolling animation."""
        ball = Circle(radius=0.15, color=YELLOW, fill_opacity=1)
        ball.set_fill(YELLOW)
        return ball

    def animate_ball_rolling(self, ball, potential_elements):
        """Animate ball rolling down the potential."""
        # Start ball at void state
        void_point = self.axes.coords_to_point(0, potential(np.array([0]))[0] + 0.3)
        ball.move_to(void_point)

        self.play(FadeIn(ball), run_time=0.5)

        # Create rolling animation
        def get_ball_position(phi):
            potential_val = DoubleWellPotential()(np.array([phi]))[0]
            return self.axes.coords_to_point(phi, potential_val + 0.3)

        # Animate ball rolling to positive vacuum
        positive_vacuum_trajectory = ParametricFunction(
            lambda t: get_ball_position(t), t_range=[0, 1.0], color=YELLOW
        )

        self.play(
            MoveAlongPath(ball, positive_vacuum_trajectory),
            run_time=3,
            rate_func=smooth,
        )

        # Add explanation
        explanation = Text(
            "Field rolls from void to ordered state", font_size=20, color=YELLOW
        )
        explanation.to_edge(DOWN)

        self.play(Write(explanation), run_time=1)
        self.wait(1)
        self.play(FadeOut(explanation), run_time=0.5)

    def show_quantum_tunneling(self, potential_elements):
        """Show quantum tunneling through the barrier."""
        # Create tunneling path
        tunneling_path = self.axes.plot(
            lambda x: 0.5 * np.exp(-(x**2) / 0.5),  # Gaussian barrier penetration
            x_range=[-1, 1],
            color=PURPLE,
            stroke_width=3,
        )

        # Add tunneling label
        tunneling_label = Text("Quantum Tunneling", color=PURPLE, font_size=20)
        tunneling_label.next_to(tunneling_path, UP)

        self.play(Create(tunneling_path), Write(tunneling_label), run_time=2)
        self.wait(1)
        self.play(FadeOut(tunneling_path), FadeOut(tunneling_label), run_time=0.5)

    def show_instanton_trajectory(self, potential_elements):
        """Show instanton trajectory."""

        # Create instanton path (kink solution)
        def instanton_profile(phi):
            v = 1.0
            return v * np.tanh(phi)

        instanton_curve = self.axes.plot(
            instanton_profile, x_range=[-2, 2], color=ORANGE, stroke_width=4
        )

        # Add instanton label
        instanton_label = Text("Instanton Solution", color=ORANGE, font_size=20)
        instanton_label.next_to(instanton_curve, DOWN)

        self.play(Create(instanton_curve), Write(instanton_label), run_time=2)
        self.wait(1)
        self.play(FadeOut(instanton_curve), FadeOut(instanton_label), run_time=0.5)

    def show_summary(self):
        """Show summary of key concepts."""
        summary_text = Text(
            "Key Concepts:\n"
            "• Void state is metastable\n"
            "• Quantum fluctuations trigger nucleation\n"
            "• Instanton solutions describe tunneling\n"
            "• Entropy drives time's arrow",
            font_size=18,
            color=WHITE,
        )
        summary_text.to_edge(RIGHT)

        self.play(Write(summary_text), run_time=3)
        self.wait(2)
        self.play(FadeOut(summary_text), run_time=1)


class PotentialLandscape3D(ThreeDScene):
    """
    3D version of the potential landscape visualization.

    Shows the potential as a 3D surface with better visual impact.
    """

    def construct(self):
        # Set up 3D scene
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)

        # Create 3D potential surface
        potential_surface = self.create_3d_potential_surface()

        # Add labels
        labels = self.create_3d_labels()

        # Show surface
        self.play(Create(potential_surface), run_time=2)
        self.play(Create(labels), run_time=1)

        # Rotate camera
        self.begin_ambient_camera_rotation(rate=0.1)
        self.wait(5)
        self.stop_ambient_camera_rotation()

        # Show ball rolling
        self.show_3d_ball_rolling(potential_surface)

    def create_3d_potential_surface(self):
        """Create 3D potential surface."""

        def potential_function(x, y):
            # For 3D, we can show a 2D field or use y as a parameter
            phi = x
            return DoubleWellPotential()(np.array([phi]))[0]

        surface = Surface(
            potential_function,
            u_range=[-2, 2],
            v_range=[-1, 1],
            resolution=(50, 50),
            fill_opacity=0.7,
            stroke_width=1,
            fill_color=BLUE,
            stroke_color=WHITE,
        )

        return surface

    def create_3d_labels(self):
        """Create 3D labels."""
        # This would be more complex in 3D
        # For now, return empty list
        return []

    def show_3d_ball_rolling(self, surface):
        """Show ball rolling on 3D surface."""
        # Create 3D ball
        ball = Sphere(radius=0.1, color=YELLOW)
        ball.move_to([0, 0, 1])

        self.play(FadeIn(ball), run_time=0.5)

        # Animate ball rolling
        self.play(ball.animate.move_to([1, 0, 0.5]), run_time=2, rate_func=smooth)

        self.wait(1)
