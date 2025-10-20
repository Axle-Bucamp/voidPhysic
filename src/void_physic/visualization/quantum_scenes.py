"""
Quantum mechanics animation scenes for void physics.

This module contains Manim scenes that visualize quantum mechanical
concepts and their connection to void physics emergence.
"""

import numpy as np
from manim import *
import logging

# Import quantum modules
try:
    from ..quantum.schrodinger import SchrodingerSolver, SchrodingerParameters, WaveFunction
    from ..quantum.relativistic import KleinGordonSolver, DiracSolver, RelativisticParameters
    from ..quantum.field_theory import QuantumField, FieldParameters, ParticleCreation
    from ..core.potential import DoubleWellPotential, PotentialParameters
except ImportError:
    # Handle direct execution
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
    from void_physic.quantum.schrodinger import SchrodingerSolver, SchrodingerParameters, WaveFunction
    from void_physic.quantum.relativistic import KleinGordonSolver, DiracSolver, RelativisticParameters
    from void_physic.quantum.field_theory import QuantumField, FieldParameters, ParticleCreation
    from void_physic.core.potential import DoubleWellPotential, PotentialParameters

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SchrodingerEvolutionScene(Scene):
    """
    Scene 1: Schrödinger equation evolution showing wave packet spreading
    and tunneling through potential barriers.
    """
    
    def construct(self):
        # Title
        title = Text("Schrödinger Equation Evolution", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))
        
        # Set up parameters
        params = SchrodingerParameters(
            mass=1.0,
            hbar=1.0,
            dt=0.01,
            x_min=-8.0,
            x_max=8.0,
            n_points=256
        )
        
        # Create potential function (double well)
        def potential_func(x):
            return 0.5 * (x**2 - 1)**2
        
        params.potential = potential_func
        
        # Initialize solver
        solver = SchrodingerSolver(params)
        
        # Create initial wave packet
        psi_init = solver.create_gaussian_packet(x0=-2.0, p0=1.0, sigma=0.8)
        
        # Set up axes
        axes = Axes(
            x_range=[-8, 8, 2],
            y_range=[0, 1, 0.2],
            x_length=10,
            y_length=4,
            axis_config={"color": BLUE}
        )
        axes.to_edge(DOWN)
        
        # Create potential curve
        potential_curve = axes.plot(
            lambda x: 0.1 * potential_func(x),
            color=RED,
            x_range=[-8, 8]
        )
        
        # Create wave function curve
        x_vals = solver.x_grid
        psi_vals = np.abs(psi_init.psi)**2
        
        wave_curve = axes.plot_line_graph(
            x_vals, psi_vals,
            add_vertex_dots=False,
            line_color=YELLOW
        )
        
        # Add labels
        x_label = Text("Position (x)", font_size=20).next_to(axes, DOWN)
        y_label = Text("|ψ|²", font_size=20).next_to(axes, LEFT)
        
        # Show initial setup
        self.play(Create(axes))
        self.play(Create(potential_curve))
        self.play(Create(wave_curve))
        self.play(Write(x_label), Write(y_label))
        
        # Animate evolution
        for i in range(50):
            # Evolve wave function
            psi_init = solver.evolve_step(psi_init)
            
            # Update wave curve
            new_psi_vals = np.abs(psi_init.psi)**2
            new_wave_curve = axes.plot_line_graph(
                x_vals, new_psi_vals,
                add_vertex_dots=False,
                line_color=YELLOW
            )
            
            self.play(Transform(wave_curve, new_wave_curve), run_time=0.1)
        
        # Add equation
        equation = Text("iℏ ∂Ψ/∂t = ĤΨ", font_size=20, color=WHITE)
        equation.to_corner(UR)
        self.play(Write(equation))
        
        self.wait(2)


class ProbabilityFlowScene(Scene):
    """
    Scene 2: Animated vector field of probability current j showing
    how probability "flows" through space.
    """
    
    def construct(self):
        # Title
        title = Text("Probability Current Flow", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))
        
        # Set up parameters
        params = SchrodingerParameters(
            mass=1.0,
            hbar=1.0,
            dt=0.01,
            x_min=-6.0,
            x_max=6.0,
            n_points=128
        )
        
        # No potential (free particle)
        params.potential = lambda x: np.zeros_like(x)
        
        # Initialize solver
        solver = SchrodingerSolver(params)
        
        # Create initial wave packet
        psi_init = solver.create_gaussian_packet(x0=0.0, p0=1.0, sigma=1.0)
        
        # Set up axes
        axes = Axes(
            x_range=[-6, 6, 2],
            y_range=[-0.5, 0.5, 0.1],
            x_length=10,
            y_length=4,
            axis_config={"color": BLUE}
        )
        axes.to_edge(DOWN)
        
        # Create initial wave function
        x_vals = solver.x_grid
        psi_vals = np.abs(psi_init.psi)**2
        
        wave_curve = axes.plot_line_graph(
            x_vals, psi_vals,
            add_vertex_dots=False,
            line_color=YELLOW
        )
        
        # Create probability current vectors
        def create_current_vectors(psi):
            dx = solver.dx
            dpsi_dx = np.gradient(psi, dx)
            j = (solver.hbar / (2 * solver.mass * 1j)) * (
                np.conj(psi) * dpsi_dx - psi * np.conj(dpsi_dx)
            )
            j_real = j.real
            
            vectors = VGroup()
            for i in range(0, len(x_vals), 8):  # Sample every 8th point
                if abs(j_real[i]) > 0.01:  # Only show significant current
                    start_point = axes.coords_to_point(x_vals[i], 0)
                    end_point = axes.coords_to_point(
                        x_vals[i], j_real[i] * 2  # Scale for visibility
                    )
                    arrow = Arrow(start_point, end_point, color=GREEN, buff=0)
                    vectors.add(arrow)
            
            return vectors
        
        current_vectors = create_current_vectors(psi_init.psi)
        
        # Show initial setup
        self.play(Create(axes))
        self.play(Create(wave_curve))
        self.play(Create(current_vectors))
        
        # Animate evolution
        for i in range(30):
            # Evolve wave function
            psi_init = solver.evolve_step(psi_init)
            
            # Update wave curve
            new_psi_vals = np.abs(psi_init.psi)**2
            new_wave_curve = axes.plot_line_graph(
                x_vals, new_psi_vals,
                add_vertex_dots=False,
                line_color=YELLOW
            )
            
            # Update current vectors
            new_current_vectors = create_current_vectors(psi_init.psi)
            
            self.play(
                Transform(wave_curve, new_wave_curve),
                Transform(current_vectors, new_current_vectors),
                run_time=0.2
            )
        
        # Add equation
        equation = Text("j = (ℏ/2mi)(Ψ*∇Ψ - Ψ∇Ψ*)", font_size=16, color=WHITE)
        equation.to_corner(UR)
        self.play(Write(equation))
        
        self.wait(2)


class EnergyLandscapeScene(ThreeDScene):
    """
    Scene 3: 3D potential surface with wave function overlay showing
    energy landscape and quantum tunneling.
    """
    
    def construct(self):
        # Title
        title = Text("Energy Landscape & Quantum Tunneling", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))
        
        # Set up 3D axes
        axes = ThreeDAxes(
            x_range=[-4, 4, 1],
            y_range=[-4, 4, 1],
            z_range=[0, 3, 0.5],
            x_length=8,
            y_length=8,
            z_length=6
        )
        
        # Create potential surface
        def potential_func(x, y):
            return 0.5 * (x**2 + y**2 - 1)**2 + 0.5
        
        potential_surface = Surface(
            lambda x, y: axes.c2p(x, y, potential_func(x, y)),
            u_range=[-4, 4],
            v_range=[-4, 4],
            resolution=(20, 20),
            fill_color=RED,
            fill_opacity=0.7,
            stroke_color=RED
        )
        
        # Create wave function as probability cloud
        def create_probability_cloud():
            # Simple 2D Gaussian for demonstration
            x_vals = np.linspace(-3, 3, 20)
            y_vals = np.linspace(-3, 3, 20)
            X, Y = np.meshgrid(x_vals, y_vals)
            Z = np.exp(-(X**2 + Y**2) / 2)
            
            cloud = VGroup()
            for i in range(0, len(x_vals), 2):
                for j in range(0, len(y_vals), 2):
                    if Z[j, i] > 0.1:
                        point = Dot3D(
                            axes.c2p(x_vals[i], y_vals[j], Z[j, i] + 0.1),
                            color=YELLOW,
                            radius=0.05 * Z[j, i]
                        )
                        cloud.add(point)
            
            return cloud
        
        probability_cloud = create_probability_cloud()
        
        # Set camera angle
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        
        # Show 3D scene
        self.play(Create(axes))
        self.play(Create(potential_surface))
        self.play(Create(probability_cloud))
        
        # Rotate camera
        self.begin_ambient_camera_rotation(rate=0.1)
        self.wait(3)
        self.stop_ambient_camera_rotation()
        
        # Add equation
        equation = Text("V_quantum = -(ℏ²/2m)(∇²√ρ)/√ρ", font_size=16, color=WHITE)
        equation.to_corner(UR)
        self.play(Write(equation))
        
        self.wait(2)


class QuantumVoidEmergenceScene(Scene):
    """
    Scene 4: Particles emerging as field excitations from quantum vacuum,
    showing the connection between quantum field theory and void physics.
    """
    
    def construct(self):
        # Title
        title = Text("Quantum Void Emergence", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))
        
        # Set up field parameters
        field_params = FieldParameters(
            mass=1.0,
            hbar=1.0,
            c=1.0,
            coupling=0.5,
            x_min=-6.0,
            x_max=6.0,
            n_points=128,
            dt=0.02
        )
        
        # Initialize quantum field
        quantum_field = QuantumField(field_params)
        quantum_field.set_field(quantum_field.field_operator.vacuum_state())
        
        # Set up axes
        axes = Axes(
            x_range=[-6, 6, 2],
            y_range=[-1, 1, 0.2],
            x_length=10,
            y_length=4,
            axis_config={"color": BLUE}
        )
        axes.to_edge(DOWN)
        
        # Create initial field (vacuum)
        x_vals = quantum_field.field_operator.x_grid
        field_vals = np.abs(quantum_field.field)
        
        field_curve = axes.plot_line_graph(
            x_vals, field_vals,
            add_vertex_dots=False,
            line_color=WHITE
        )
        
        # Show vacuum state
        self.play(Create(axes))
        self.play(Create(field_curve))
        
        # Add vacuum label
        vacuum_label = Text("Vacuum State", font_size=24, color=WHITE)
        vacuum_label.next_to(axes, UP)
        self.play(Write(vacuum_label))
        
        # Simulate particle emergence
        particles = VGroup()
        emergence_events = []
        
        for step in range(20):
            # Random particle emergence
            if np.random.random() < 0.3:  # 30% chance per step
                # Create particle
                k_random = np.random.uniform(-2.0, 2.0)
                amplitude = np.random.uniform(0.5, 1.0)
                
                new_particle = quantum_field.field_operator.create_particle(k_random, amplitude)
                quantum_field.field += new_particle
                
                # Find emergence position
                max_idx = np.argmax(np.abs(new_particle))
                emergence_x = x_vals[max_idx]
                
                # Create particle visualization
                particle_dot = Dot(
                    axes.coords_to_point(emergence_x, 0),
                    color=YELLOW,
                    radius=0.1
                )
                particles.add(particle_dot)
                emergence_events.append(particle_dot)
                
                # Show emergence
                self.play(
                    Create(particle_dot),
                    Flash(particle_dot, color=YELLOW),
                    run_time=0.5
                )
            
            # Evolve field
            quantum_field.evolve_step()
            
            # Update field curve
            new_field_vals = np.abs(quantum_field.field)
            new_field_curve = axes.plot_line_graph(
                x_vals, new_field_vals,
                add_vertex_dots=False,
                line_color=WHITE
            )
            
            self.play(Transform(field_curve, new_field_curve), run_time=0.2)
        
        # Add equation
        equation = Text("â†|0⟩ = |1⟩", font_size=20, color=WHITE)
        equation.to_corner(UR)
        self.play(Write(equation))
        
        self.wait(2)


class RelativisticComparisonScene(Scene):
    """
    Scene 5: Side-by-side comparison of Schrödinger vs Klein-Gordon vs Dirac
    equations showing relativistic effects.
    """
    
    def construct(self):
        # Title
        title = Text("Relativistic Quantum Equations", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))
        
        # Create three subplots
        plot1 = Axes(
            x_range=[-4, 4, 1],
            y_range=[0, 1, 0.2],
            x_length=4,
            y_length=3,
            axis_config={"color": BLUE}
        ).to_edge(LEFT)
        
        plot2 = Axes(
            x_range=[-4, 4, 1],
            y_range=[0, 1, 0.2],
            x_length=4,
            y_length=3,
            axis_config={"color": BLUE}
        ).to_edge(RIGHT)
        
        plot3 = Axes(
            x_range=[-4, 4, 1],
            y_range=[0, 1, 0.2],
            x_length=4,
            y_length=3,
            axis_config={"color": BLUE}
        ).to_edge(DOWN)
        
        # Schrödinger evolution
        schrodinger_params = SchrodingerParameters(
            mass=1.0, hbar=1.0, dt=0.01, x_min=-4.0, x_max=4.0, n_points=64
        )
        schrodinger_params.potential = lambda x: np.zeros_like(x)
        schrodinger_solver = SchrodingerSolver(schrodinger_params)
        psi_init = schrodinger_solver.create_gaussian_packet(x0=0.0, p0=1.0, sigma=0.8)
        
        # Klein-Gordon evolution
        kg_params = RelativisticParameters(
            mass=1.0, c=1.0, hbar=1.0, dt=0.01, x_min=-4.0, x_max=4.0, n_points=64
        )
        kg_solver = KleinGordonSolver(kg_params)
        phi_init, dphi_dt_init = kg_solver.create_gaussian_field(x0=0.0, k0=1.0, sigma=0.8)
        
        # Create initial curves
        x_vals = schrodinger_solver.x_grid
        
        schrodinger_curve = plot1.plot_line_graph(
            x_vals, np.abs(psi_init.psi)**2,
            add_vertex_dots=False,
            line_color=YELLOW
        )
        
        kg_curve = plot2.plot_line_graph(
            x_vals, np.abs(phi_init)**2,
            add_vertex_dots=False,
            line_color=GREEN
        )
        
        # Dirac (simplified - just show dispersion)
        dirac_curve = plot3.plot(
            lambda x: 0.5 * np.exp(-x**2 / 2),
            color=PURPLE
        )
        
        # Add labels
        schrodinger_label = Text("Schrödinger", font_size=20).next_to(plot1, UP)
        kg_label = Text("Klein-Gordon", font_size=20).next_to(plot2, UP)
        dirac_label = Text("Dirac", font_size=20).next_to(plot3, UP)
        
        # Show plots
        self.play(Create(plot1), Create(plot2), Create(plot3))
        self.play(Create(schrodinger_curve), Create(kg_curve), Create(dirac_curve))
        self.play(Write(schrodinger_label), Write(kg_label), Write(dirac_label))
        
        # Animate evolution
        for i in range(20):
            # Evolve Schrödinger
            psi_init = schrodinger_solver.evolve_step(psi_init)
            new_schrodinger_curve = plot1.plot_line_graph(
                x_vals, np.abs(psi_init.psi)**2,
                add_vertex_dots=False,
                line_color=YELLOW
            )
            
            # Evolve Klein-Gordon
            phi_init, dphi_dt_init = kg_solver.evolve_step(phi_init, dphi_dt_init)
            new_kg_curve = plot2.plot_line_graph(
                x_vals, np.abs(phi_init)**2,
                add_vertex_dots=False,
                line_color=GREEN
            )
            
            self.play(
                Transform(schrodinger_curve, new_schrodinger_curve),
                Transform(kg_curve, new_kg_curve),
                run_time=0.2
            )
        
        # Add equations
        equations = VGroup(
            Text("iℏ ∂Ψ/∂t = ĤΨ", font_size=14, color=WHITE),
            Text("(1/c²)∂²φ/∂t² - ∇²φ + (m²c²/ℏ²)φ = 0", font_size=12, color=WHITE),
            Text("(iℏ γ^μ ∂_μ - mc)ψ = 0", font_size=14, color=WHITE)
        )
        
        equations[0].next_to(plot1, DOWN)
        equations[1].next_to(plot2, DOWN)
        equations[2].next_to(plot3, DOWN)
        
        self.play(Write(equations))
        
        self.wait(2)


class QFTFieldScene(Scene):
    """
    Scene 6: Field oscillations with particle creation/annihilation events
    showing quantum field theory in action.
    """
    
    def construct(self):
        # Title
        title = Text("Quantum Field Theory", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))
        
        # Set up field parameters
        field_params = FieldParameters(
            mass=1.0,
            hbar=1.0,
            c=1.0,
            coupling=0.3,
            x_min=-5.0,
            x_max=5.0,
            n_points=100,
            dt=0.02
        )
        
        # Initialize quantum field
        quantum_field = QuantumField(field_params)
        quantum_field.set_field(quantum_field.field_operator.vacuum_state())
        
        # Set up axes
        axes = Axes(
            x_range=[-5, 5, 1],
            y_range=[-2, 2, 0.5],
            x_length=10,
            y_length=4,
            axis_config={"color": BLUE}
        )
        axes.to_edge(DOWN)
        
        # Create initial field
        x_vals = quantum_field.field_operator.x_grid
        field_vals = quantum_field.field.real
        
        field_curve = axes.plot_line_graph(
            x_vals, field_vals,
            add_vertex_dots=False,
            line_color=WHITE
        )
        
        # Show initial field
        self.play(Create(axes))
        self.play(Create(field_curve))
        
        # Add field label
        field_label = Text("Quantum Field φ(x,t)", font_size=24, color=WHITE)
        field_label.next_to(axes, UP)
        self.play(Write(field_label))
        
        # Simulate field evolution with creation/annihilation
        creation_events = VGroup()
        annihilation_events = VGroup()
        
        for step in range(30):
            # Random field fluctuations
            if np.random.random() < 0.2:
                # Add random fluctuation
                fluctuation = np.random.normal(0, 0.1, len(quantum_field.field))
                quantum_field.field += fluctuation
            
            # Evolve field
            quantum_field.evolve_step()
            
            # Check for particle creation/annihilation
            field_amplitude = np.abs(quantum_field.field)
            max_amplitude = np.max(field_amplitude)
            
            if max_amplitude > 0.8:  # High amplitude - particle creation
                max_idx = np.argmax(field_amplitude)
                creation_x = x_vals[max_idx]
                
                creation_dot = Dot(
                    axes.coords_to_point(creation_x, field_vals[max_idx]),
                    color=GREEN,
                    radius=0.1
                )
                creation_events.add(creation_dot)
                
                self.play(
                    Create(creation_dot),
                    Flash(creation_dot, color=GREEN),
                    run_time=0.3
                )
            
            elif max_amplitude < 0.2:  # Low amplitude - particle annihilation
                if len(creation_events) > 0:
                    # Remove a random creation event
                    event_to_remove = creation_events[-1]
                    annihilation_events.add(event_to_remove)
                    creation_events.remove(event_to_remove)
                    
                    self.play(
                        FadeOut(event_to_remove),
                        Flash(event_to_remove, color=RED),
                        run_time=0.3
                    )
            
            # Update field curve
            new_field_vals = quantum_field.field.real
            new_field_curve = axes.plot_line_graph(
                x_vals, new_field_vals,
                add_vertex_dots=False,
                line_color=WHITE
            )
            
            self.play(Transform(field_curve, new_field_curve), run_time=0.2)
        
        # Add equation
        equation = Text("iℏ ∂φ̂/∂t = [φ̂, Ĥ]", font_size=16, color=WHITE)
        equation.to_corner(UR)
        self.play(Write(equation))
        
        self.wait(2)


def main():
    """Main function to run individual scenes."""
    import sys
    
    if len(sys.argv) > 1:
        scene_name = sys.argv[1]
        
        if scene_name == "schrodinger":
            scene = SchrodingerEvolutionScene()
        elif scene_name == "probability":
            scene = ProbabilityFlowScene()
        elif scene_name == "energy":
            scene = EnergyLandscapeScene()
        elif scene_name == "void":
            scene = QuantumVoidEmergenceScene()
        elif scene_name == "relativistic":
            scene = RelativisticComparisonScene()
        elif scene_name == "qft":
            scene = QFTFieldScene()
        else:
            print("Available scenes: schrodinger, probability, energy, void, relativistic, qft")
            return
        
        scene.render()
    else:
        print("Usage: python quantum_scenes.py <scene_name>")
        print("Available scenes: schrodinger, probability, energy, void, relativistic, qft")


if __name__ == "__main__":
    main()
