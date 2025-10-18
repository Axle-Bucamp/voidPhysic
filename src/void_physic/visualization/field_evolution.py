"""
Manim scene for visualizing field evolution in void physics.

This scene shows the stochastic evolution of the scalar field φ(t)
with multiple trajectories, phase portraits, and statistical analysis.
"""

import logging

import numpy as np
from manim import *

from void_physic.core.potential import DoubleWellPotential, PotentialParameters
from void_physic.core.stochastic import LangevinDynamics, WhiteNoise
from void_physic.simulation.langevin_solver import LangevinSolver, SolverParameters
from void_physic.utils.constants import PhysicalConstants

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FieldEvolutionScene(Scene):
    """
    Scene visualizing field evolution and stochastic dynamics.

    Shows:
    1. Multiple stochastic trajectories φ(t)
    2. Ensemble statistics (mean, variance)
    3. Phase portrait (φ, dφ/dt)
    4. Probability density evolution
    5. First passage time analysis
    """

    def construct(self):
        # Set up parameters
        self.setup_parameters()

        # Create coordinate system
        self.setup_coordinate_system()

        # Run simulation
        self.run_simulation()

        # Show individual trajectories
        self.show_individual_trajectories()

        # Show ensemble statistics
        self.show_ensemble_statistics()

        # Show phase portrait
        self.show_phase_portrait()

        # Show probability density
        self.show_probability_density()

        # Show first passage analysis
        self.show_first_passage_analysis()

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
            dt=0.01,
            t_max=20.0,
            n_trajectories=50,  # Reduced for visualization
            save_trajectories=True,
        )

    def setup_coordinate_system(self):
        """Set up coordinate system for field evolution."""
        # Create axes for field vs time
        self.field_axes = Axes(
            x_range=[0, 20, 5],
            y_range=[-2, 2, 0.5],
            x_length=10,
            y_length=6,
            axis_config={"color": GRAY},
            tips=False,
        )

        # Add axis labels
        x_label = self.field_axes.get_x_axis_label(
            "t", edge=DOWN, direction=DOWN, buff=0.4
        )
        y_label = self.field_axes.get_y_axis_label(
            "\\phi(t)", edge=LEFT, direction=LEFT, buff=0.4
        )

        self.add(self.field_axes, x_label, y_label)

        # Title
        title = Text("Field Evolution in Void Physics", font_size=36, color=WHITE)
        title.to_edge(UP)
        self.add(title)

    def run_simulation(self):
        """Run the stochastic simulation."""
        # Initialize components
        potential = DoubleWellPotential(self.potential_params)
        noise_model = WhiteNoise(self.constants.noise_strength, seed=42)
        langevin_dynamics = LangevinDynamics(potential, noise_model, self.constants)
        solver = LangevinSolver(langevin_dynamics, self.constants)

        # Run ensemble simulation
        self.ensemble_results = solver.ensemble_simulation(0.0, self.solver_params)

        # Store trajectories for visualization
        self.trajectories = self.ensemble_results["trajectories"]
        self.time = self.ensemble_results["time"]
        self.mean_field = self.ensemble_results["mean_field"]
        self.std_field = self.ensemble_results["std_field"]

    def show_individual_trajectories(self):
        """Show individual stochastic trajectories."""
        # Create trajectory curves
        trajectory_curves = []

        # Show first few trajectories
        n_show = min(10, len(self.trajectories))

        for i in range(n_show):
            phi_traj = self.trajectories[i]

            # Create curve
            curve = self.field_axes.plot(
                lambda t, phi=phi_traj: self.interpolate_field(t, phi),
                x_range=[0, 20],
                color=BLUE,
                stroke_width=1,
                stroke_opacity=0.7,
            )

            trajectory_curves.append(curve)

        # Animate trajectories appearing
        self.play(*[Create(curve) for curve in trajectory_curves], run_time=2)

        # Add explanation
        explanation = Text(
            "Individual stochastic trajectories show quantum fluctuations",
            font_size=20,
            color=BLUE,
        )
        explanation.to_edge(DOWN)

        self.play(Write(explanation), run_time=1)
        self.wait(1)
        self.play(FadeOut(explanation), run_time=0.5)

    def show_ensemble_statistics(self):
        """Show ensemble statistics (mean and variance)."""
        # Create mean curve
        mean_curve = self.field_axes.plot(
            lambda t: self.interpolate_field(t, self.mean_field),
            x_range=[0, 20],
            color=RED,
            stroke_width=3,
        )

        # Create variance band
        upper_bound = self.mean_field + self.std_field
        lower_bound = self.mean_field - self.std_field

        variance_band = self.field_axes.plot(
            lambda t: self.interpolate_field(t, upper_bound),
            x_range=[0, 20],
            color=RED,
            stroke_width=1,
            stroke_opacity=0.3,
        )

        # Add mean label
        mean_label = Text("⟨φ⟩", color=RED, font_size=20)
        mean_label.next_to(mean_curve, UP)

        self.play(Create(mean_curve), Write(mean_label), run_time=1)

        # Add explanation
        explanation = Text(
            "Ensemble mean shows average evolution, variance shows fluctuations",
            font_size=20,
            color=RED,
        )
        explanation.to_edge(DOWN)

        self.play(Write(explanation), run_time=1)
        self.wait(1)
        self.play(FadeOut(explanation), run_time=0.5)

    def show_phase_portrait(self):
        """Show phase portrait (φ, dφ/dt)."""
        # Clear current scene
        self.play(
            *[FadeOut(mob) for mob in self.mobjects if mob != self.field_axes],
            run_time=0.5,
        )

        # Create new axes for phase portrait
        phase_axes = Axes(
            x_range=[-2, 2, 0.5],
            y_range=[-3, 3, 0.5],
            x_length=8,
            y_length=6,
            axis_config={"color": GRAY},
            tips=False,
        )

        x_label = phase_axes.get_x_axis_label(
            "\\phi", edge=DOWN, direction=DOWN, buff=0.4
        )
        y_label = phase_axes.get_y_axis_label(
            "\\dot{\\phi}", edge=LEFT, direction=LEFT, buff=0.4
        )

        self.add(phase_axes, x_label, y_label)

        # Create phase portrait for one trajectory
        phi_traj = self.trajectories[0]
        dphi_dt = np.gradient(phi_traj, self.time)

        # Create phase curve
        phase_curve = phase_axes.plot(
            lambda t: self.interpolate_field(t, phi_traj),
            x_range=[0, 20],
            color=GREEN,
            stroke_width=2,
        )

        # Add phase portrait label
        phase_label = Text("Phase Portrait (φ, φ̇)", font_size=24, color=WHITE)
        phase_label.to_edge(UP)

        self.play(Create(phase_curve), Write(phase_label), run_time=2)

        # Add explanation
        explanation = Text(
            "Phase portrait shows field velocity vs position", font_size=20, color=GREEN
        )
        explanation.to_edge(DOWN)

        self.play(Write(explanation), run_time=1)
        self.wait(1)
        self.play(FadeOut(explanation), run_time=0.5)

    def show_probability_density(self):
        """Show probability density evolution."""
        # This would show how the probability distribution P(φ,t) evolves
        # For now, show a simplified version

        explanation = Text(
            "Probability density P(φ,t) evolves from delta function to broad distribution",
            font_size=20,
            color=PURPLE,
        )
        explanation.to_edge(DOWN)

        self.play(Write(explanation), run_time=2)
        self.wait(1)
        self.play(FadeOut(explanation), run_time=0.5)

    def show_first_passage_analysis(self):
        """Show first passage time analysis."""
        # Calculate first passage times
        threshold = 0.5
        first_passage_times = []

        for phi_traj in self.trajectories:
            crossing_indices = np.where(phi_traj >= threshold)[0]
            if len(crossing_indices) > 0:
                first_passage_times.append(self.time[crossing_indices[0]])
            else:
                first_passage_times.append(np.inf)

        # Show histogram
        finite_times = [t for t in first_passage_times if t != np.inf]

        if len(finite_times) > 0:
            # Create simple histogram visualization
            histogram_text = Text(
                f"First Passage Times to φ = {threshold}:\n"
                f"Mean: {np.mean(finite_times):.2f}\n"
                f"Std: {np.std(finite_times):.2f}\n"
                f"Success rate: {len(finite_times)/len(first_passage_times):.2f}",
                font_size=18,
                color=ORANGE,
            )
            histogram_text.to_edge(DOWN)

            self.play(Write(histogram_text), run_time=2)
            self.wait(1)
            self.play(FadeOut(histogram_text), run_time=0.5)

    def show_summary(self):
        """Show summary of field evolution."""
        summary_text = Text(
            "Field Evolution Summary:\n"
            "• Stochastic trajectories show quantum fluctuations\n"
            "• Ensemble mean reveals average behavior\n"
            "• Phase portrait shows dynamical structure\n"
            "• First passage times quantify nucleation rate",
            font_size=16,
            color=WHITE,
        )
        summary_text.to_edge(RIGHT)

        self.play(Write(summary_text), run_time=3)
        self.wait(2)
        self.play(FadeOut(summary_text), run_time=1)

    def interpolate_field(self, t, field_values):
        """Interpolate field values at given time."""
        if t <= 0:
            return field_values[0]
        elif t >= self.time[-1]:
            return field_values[-1]
        else:
            # Linear interpolation
            idx = int(t / self.time[1])  # Assuming uniform time step
            if idx >= len(field_values) - 1:
                return field_values[-1]

            t1, t2 = self.time[idx], self.time[idx + 1]
            phi1, phi2 = field_values[idx], field_values[idx + 1]

            return phi1 + (phi2 - phi1) * (t - t1) / (t2 - t1)


class FieldEvolution3D(ThreeDScene):
    """
    3D visualization of field evolution.

    Shows field evolution in 3D space with time as the third dimension.
    """

    def construct(self):
        # Set up 3D scene
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)

        # Create 3D field evolution
        field_surface = self.create_3d_field_surface()

        # Show surface
        self.play(Create(field_surface), run_time=2)

        # Rotate camera
        self.begin_ambient_camera_rotation(rate=0.1)
        self.wait(5)
        self.stop_ambient_camera_rotation()

    def create_3d_field_surface(self):
        """Create 3D surface showing field evolution."""

        def field_function(x, y):
            # x is time, y is trajectory index
            # This is a simplified version
            return np.sin(x) * np.cos(y)

        surface = Surface(
            field_function,
            u_range=[0, 20],
            v_range=[0, 10],
            resolution=(50, 50),
            fill_opacity=0.7,
            stroke_width=1,
            fill_color=BLUE,
            stroke_color=WHITE,
        )

        return surface
