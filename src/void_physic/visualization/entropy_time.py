"""
Manim scene for visualizing entropy evolution and time emergence in void physics.

This scene shows how entropy increases during the void → spacetime transition,
demonstrating the emergence of time's arrow from the reversible void state.
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


class EntropyTimeScene(Scene):
    """
    Scene visualizing entropy evolution and time emergence.

    Shows:
    1. Entropy S(t) increasing over time
    2. Entropy production rate dS/dt
    3. Time's arrow emerging from entropy gradient
    4. Reversible void → Irreversible cosmos transition
    5. Thermodynamic quantities evolution
    """

    def construct(self):
        # Set up parameters
        self.setup_parameters()

        # Create coordinate system
        self.setup_coordinate_system()

        # Run simulation
        self.run_simulation()

        # Show entropy evolution
        self.show_entropy_evolution()

        # Show entropy production rate
        self.show_entropy_production_rate()

        # Show time's arrow emergence
        self.show_times_arrow()

        # Show thermodynamic quantities
        self.show_thermodynamic_quantities()

        # Show phase transition
        self.show_phase_transition()

        # Final summary
        self.show_summary()

    def setup_parameters(self):
        """Set up simulation parameters."""
        self.potential_params = PotentialParameters(
            lambda_coupling=1.0, v_vev=1.0, V0_offset=0.0
        )

        self.constants = PhysicalConstants(
            gamma_friction=1.0, noise_strength=0.5, dt_default=0.01
        )

        self.solver_params = SolverParameters(
            dt=0.01, t_max=30.0, n_trajectories=100, save_trajectories=True
        )

    def setup_coordinate_system(self):
        """Set up coordinate system for entropy visualization."""
        # Create axes for entropy vs time
        self.entropy_axes = Axes(
            x_range=[0, 30, 5],
            y_range=[0, 3, 0.5],
            x_length=10,
            y_length=6,
            axis_config={"color": GRAY},
            tips=False,
        )

        # Add axis labels
        x_label = self.entropy_axes.get_x_axis_label(
            "t", edge=DOWN, direction=DOWN, buff=0.4
        )
        y_label = self.entropy_axes.get_y_axis_label(
            "S(t)", edge=LEFT, direction=LEFT, buff=0.4
        )

        self.add(self.entropy_axes, x_label, y_label)

        # Title
        title = Text("Entropy Evolution and Time's Arrow", font_size=36, color=WHITE)
        title.to_edge(UP)
        self.add(title)

    def run_simulation(self):
        """Run the stochastic simulation and calculate entropy."""
        # Initialize components
        potential = DoubleWellPotential(self.potential_params)
        noise_model = WhiteNoise(self.constants.noise_strength, seed=42)
        langevin_dynamics = LangevinDynamics(potential, noise_model, self.constants)
        solver = LangevinSolver(langevin_dynamics, self.constants)

        # Run ensemble simulation
        self.ensemble_results = solver.ensemble_simulation(0.0, self.solver_params)

        # Calculate entropy
        entropy_calc = EntropyCalculator()
        self.entropy = entropy_calc.field_entropy(
            self.ensemble_results["trajectories"], self.ensemble_results["time"]
        )

        # Calculate entropy production rate
        self.entropy_rate = entropy_calc.entropy_production_rate(
            self.entropy, self.ensemble_results["time"]
        )

        # Calculate thermodynamic quantities
        self.thermo_quantities = entropy_calc.thermodynamic_quantities(
            self.ensemble_results["trajectories"],
            self.ensemble_results["time"],
            potential,
        )

        self.time = self.ensemble_results["time"]

    def show_entropy_evolution(self):
        """Show entropy evolution over time."""
        # Create entropy curve
        entropy_curve = self.entropy_axes.plot(
            lambda t: self.interpolate_entropy(t),
            x_range=[0, 30],
            color=RED,
            stroke_width=4,
        )

        # Add entropy label
        entropy_label = MathTex("S(t)", color=RED, font_size=24)
        entropy_label.next_to(entropy_curve, UP)

        # Show curve
        self.play(Create(entropy_curve), Write(entropy_label), run_time=2)

        # Add explanation
        explanation = Text(
            "Entropy increases as field evolves from void to ordered state",
            font_size=20,
            color=RED,
        )
        explanation.to_edge(DOWN)

        self.play(Write(explanation), run_time=1)
        self.wait(1)
        self.play(FadeOut(explanation), run_time=0.5)

    def show_entropy_production_rate(self):
        """Show entropy production rate."""
        # Create entropy rate curve
        entropy_rate_curve = self.entropy_axes.plot(
            lambda t: self.interpolate_entropy_rate(t),
            x_range=[0, 30],
            color=ORANGE,
            stroke_width=3,
        )

        # Add rate label
        rate_label = MathTex("\\frac{dS}{dt}", color=ORANGE, font_size=24)
        rate_label.next_to(entropy_rate_curve, UP)

        self.play(Create(entropy_rate_curve), Write(rate_label), run_time=1)

        # Add explanation
        explanation = Text(
            "Entropy production rate shows how fast disorder increases",
            font_size=20,
            color=ORANGE,
        )
        explanation.to_edge(DOWN)

        self.play(Write(explanation), run_time=1)
        self.wait(1)
        self.play(FadeOut(explanation), run_time=0.5)

    def show_times_arrow(self):
        """Show time's arrow emerging from entropy gradient."""
        # Create time arrow
        time_arrow = Arrow(
            start=self.entropy_axes.coords_to_point(0, 0),
            end=self.entropy_axes.coords_to_point(30, 0),
            color=YELLOW,
            stroke_width=6,
        )

        # Add arrow label
        arrow_label = Text("Time's Arrow", color=YELLOW, font_size=20)
        arrow_label.next_to(time_arrow, DOWN)

        # Show arrow
        self.play(Create(time_arrow), Write(arrow_label), run_time=1)

        # Add explanation
        explanation = Text(
            "Time's arrow emerges from entropy gradient: t ∝ ∫ dS/R(S)",
            font_size=18,
            color=YELLOW,
        )
        explanation.to_edge(DOWN)

        self.play(Write(explanation), run_time=2)
        self.wait(1)
        self.play(FadeOut(explanation), run_time=0.5)

    def show_thermodynamic_quantities(self):
        """Show thermodynamic quantities evolution."""
        # Create temperature curve
        temperature_curve = self.entropy_axes.plot(
            lambda t: self.interpolate_temperature(t),
            x_range=[0, 30],
            color=BLUE,
            stroke_width=3,
        )

        # Add temperature label
        temp_label = MathTex("T(t)", color=BLUE, font_size=24)
        temp_label.next_to(temperature_curve, UP)

        self.play(Create(temperature_curve), Write(temp_label), run_time=1)

        # Add explanation
        explanation = Text(
            "Temperature increases as system gains energy from void fluctuations",
            font_size=18,
            color=BLUE,
        )
        explanation.to_edge(DOWN)

        self.play(Write(explanation), run_time=2)
        self.wait(1)
        self.play(FadeOut(explanation), run_time=0.5)

    def show_phase_transition(self):
        """Show the phase transition from void to cosmos."""
        # Create phase transition indicator
        transition_point = self.entropy_axes.coords_to_point(15, 1.5)
        transition_dot = Dot(transition_point, color=PURPLE, radius=0.2)

        # Add transition label
        transition_label = Text("Phase Transition", color=PURPLE, font_size=20)
        transition_label.next_to(transition_dot, UP)

        # Show transition
        self.play(Create(transition_dot), Write(transition_label), run_time=1)

        # Add explanation
        explanation = Text(
            "Phase transition: Reversible void → Irreversible cosmos",
            font_size=18,
            color=PURPLE,
        )
        explanation.to_edge(DOWN)

        self.play(Write(explanation), run_time=2)
        self.wait(1)
        self.play(FadeOut(explanation), run_time=0.5)

    def show_summary(self):
        """Show summary of entropy and time emergence."""
        summary_text = Text(
            "Entropy and Time's Arrow:\n"
            "• Entropy S(t) increases monotonically\n"
            "• Entropy production rate dS/dt > 0\n"
            "• Time's arrow emerges from entropy gradient\n"
            "• Phase transition: void → cosmos\n"
            "• Thermodynamic quantities evolve",
            font_size=16,
            color=WHITE,
        )
        summary_text.to_edge(RIGHT)

        self.play(Write(summary_text), run_time=3)
        self.wait(2)
        self.play(FadeOut(summary_text), run_time=1)

    def interpolate_entropy(self, t):
        """Interpolate entropy at given time."""
        if t <= 0:
            return self.entropy[0]
        elif t >= self.time[-1]:
            return self.entropy[-1]
        else:
            idx = int(t / self.time[1])
            if idx >= len(self.entropy) - 1:
                return self.entropy[-1]

            t1, t2 = self.time[idx], self.time[idx + 1]
            s1, s2 = self.entropy[idx], self.entropy[idx + 1]

            return s1 + (s2 - s1) * (t - t1) / (t2 - t1)

    def interpolate_entropy_rate(self, t):
        """Interpolate entropy rate at given time."""
        if t <= 0:
            return self.entropy_rate[0]
        elif t >= self.time[-1]:
            return self.entropy_rate[-1]
        else:
            idx = int(t / self.time[1])
            if idx >= len(self.entropy_rate) - 1:
                return self.entropy_rate[-1]

            t1, t2 = self.time[idx], self.time[idx + 1]
            r1, r2 = self.entropy_rate[idx], self.entropy_rate[idx + 1]

            return r1 + (r2 - r1) * (t - t1) / (t2 - t1)

    def interpolate_temperature(self, t):
        """Interpolate temperature at given time."""
        temp_values = self.thermo_quantities["temperature"]

        if t <= 0:
            return temp_values[0]
        elif t >= self.time[-1]:
            return temp_values[-1]
        else:
            idx = int(t / self.time[1])
            if idx >= len(temp_values) - 1:
                return temp_values[-1]

            t1, t2 = self.time[idx], self.time[idx + 1]
            temp1, temp2 = temp_values[idx], temp_values[idx + 1]

            return temp1 + (temp2 - temp1) * (t - t1) / (t2 - t1)


class EntropyTime3D(ThreeDScene):
    """
    3D visualization of entropy evolution.

    Shows entropy evolution in 3D space with additional dimensions.
    """

    def construct(self):
        # Set up 3D scene
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)

        # Create 3D entropy surface
        entropy_surface = self.create_3d_entropy_surface()

        # Show surface
        self.play(Create(entropy_surface), run_time=2)

        # Rotate camera
        self.begin_ambient_camera_rotation(rate=0.1)
        self.wait(5)
        self.stop_ambient_camera_rotation()

    def create_3d_entropy_surface(self):
        """Create 3D surface showing entropy evolution."""

        def entropy_function(x, y):
            # x is time, y is a parameter
            # This is a simplified version
            return np.log(1 + x) * np.cos(y)

        surface = Surface(
            entropy_function,
            u_range=[0, 30],
            v_range=[0, 10],
            resolution=(50, 50),
            fill_opacity=0.7,
            stroke_width=1,
            fill_color=RED,
            stroke_color=WHITE,
        )

        return surface


class TimeEmergenceScene(Scene):
    """
    Scene specifically focused on time emergence from entropy.

    Shows the philosophical and physical aspects of time emergence.
    """

    def construct(self):
        # Title
        title = Text("Time Emergence from Entropy", font_size=36, color=WHITE)
        title.to_edge(UP)
        self.add(title)

        # Show void state (no time)
        self.show_void_state()

        # Show fluctuation
        self.show_fluctuation()

        # Show entropy increase
        self.show_entropy_increase()

        # Show time emergence
        self.show_time_emergence()

        # Show time's arrow
        self.show_times_arrow()

        # Final summary
        self.show_summary()

    def show_void_state(self):
        """Show the void state with no time."""
        void_text = Text("Void State: No Time, No Space", font_size=24, color=BLUE)
        void_text.move_to(ORIGIN)

        self.play(Write(void_text), run_time=2)
        self.wait(1)
        self.play(FadeOut(void_text), run_time=0.5)

    def show_fluctuation(self):
        """Show quantum fluctuation."""
        fluctuation_text = Text("Quantum Fluctuation", font_size=24, color=YELLOW)
        fluctuation_text.move_to(ORIGIN)

        self.play(Write(fluctuation_text), run_time=1)
        self.wait(1)
        self.play(FadeOut(fluctuation_text), run_time=0.5)

    def show_entropy_increase(self):
        """Show entropy increase."""
        entropy_text = Text("Entropy Increases", font_size=24, color=RED)
        entropy_text.move_to(ORIGIN)

        self.play(Write(entropy_text), run_time=1)
        self.wait(1)
        self.play(FadeOut(entropy_text), run_time=0.5)

    def show_time_emergence(self):
        """Show time emergence."""
        time_text = Text("Time Emerges", font_size=24, color=GREEN)
        time_text.move_to(ORIGIN)

        self.play(Write(time_text), run_time=1)
        self.wait(1)
        self.play(FadeOut(time_text), run_time=0.5)

    def show_times_arrow(self):
        """Show time's arrow."""
        arrow_text = Text("Time's Arrow Points Forward", font_size=24, color=PURPLE)
        arrow_text.move_to(ORIGIN)

        self.play(Write(arrow_text), run_time=1)
        self.wait(1)
        self.play(FadeOut(arrow_text), run_time=0.5)

    def show_summary(self):
        """Show summary."""
        summary_text = Text(
            "Time emerges from entropy gradient:\n"
            "t ∝ ∫ dS/R(S)\n"
            "where R(S) is the entropy production rate",
            font_size=20,
            color=WHITE,
        )
        summary_text.move_to(ORIGIN)

        self.play(Write(summary_text), run_time=3)
        self.wait(2)
        self.play(FadeOut(summary_text), run_time=1)
