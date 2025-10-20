"""
Professional Quantum Mechanics Educational Animation

This module creates a comprehensive, step-by-step educational animation
explaining quantum mechanics concepts with accurate scientific content
and clear disclaimers about void physics hypotheses.
"""

import numpy as np
from manim import *
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class QuantumMechanicsEducation(ThreeDScene):
    """
    Comprehensive educational animation covering quantum mechanics concepts
    from basic principles to advanced theories, with clear scientific accuracy.
    """
    
    def construct(self):
        # Introduction
        self.introduction()
        
        # Part 1: Classical vs Quantum
        self.part_1_classical_vs_quantum()
        
        # Part 2: Wave-Particle Duality
        self.part_2_wave_particle_duality()
        
        # Part 3: Schrödinger Equation
        self.part_3_schrodinger_equation()
        
        # Part 4: Quantum States and Superposition
        self.part_4_quantum_states()
        
        # Part 5: Quantum Tunneling
        self.part_5_quantum_tunneling()
        
        # Part 6: Atomic Structure
        self.part_6_atomic_structure()
        
        # Part 7: Quantum Field Theory
        self.part_7_quantum_field_theory()
        
        # Part 8: Void Physics Hypothesis (with disclaimers)
        self.part_8_void_physics_hypothesis()
        
        # Conclusion
        self.conclusion()
    
    def introduction(self):
        """Introduction to quantum mechanics education."""
        # Title
        title = Text("Quantum Mechanics", font_size=48, color=WHITE)
        subtitle = Text("From Classical Physics to Quantum Reality", font_size=24, color=GRAY)
        subtitle.next_to(title, DOWN)
        
        # Disclaimer
        disclaimer = Text(
            "This presentation covers established quantum mechanics\n"
            "and explores speculative void physics hypotheses",
            font_size=16, color=YELLOW
        )
        disclaimer.next_to(subtitle, DOWN, buff=1)
        
        # Learning objectives
        objectives = VGroup(
            Text("Learning Objectives:", font_size=20, color=BLUE),
            Text("• Understand wave-particle duality", font_size=16, color=WHITE),
            Text("• Learn the Schrödinger equation", font_size=16, color=WHITE),
            Text("• Explore quantum tunneling", font_size=16, color=WHITE),
            Text("• Understand atomic structure", font_size=16, color=WHITE),
            Text("• Introduction to quantum field theory", font_size=16, color=WHITE)
        )
        objectives.arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        objectives.next_to(disclaimer, DOWN, buff=1)
        
        # Show introduction
        self.play(Write(title), run_time=2)
        self.play(Write(subtitle), run_time=1)
        self.play(Write(disclaimer), run_time=1.5)
        
        for obj in objectives:
            self.play(Write(obj), run_time=0.5)
        
        self.wait(2)
        self.play(FadeOut(VGroup(title, subtitle, disclaimer, objectives)), run_time=2)
    
    def part_1_classical_vs_quantum(self):
        """Part 1: Classical vs Quantum Physics."""
        # Title
        title = Text("Part 1: Classical vs Quantum Physics", font_size=36, color=BLUE)
        title.to_edge(UP)
        self.play(Write(title))
        
        # Create comparison table
        table = self.create_classical_quantum_table()
        self.play(Create(table), run_time=2)
        
        # Animate classical particle
        self.animate_classical_particle()
        
        # Animate quantum particle
        self.animate_quantum_particle()
        
        # Key insight
        insight = Text(
            "Key Insight: Quantum mechanics describes the behavior\n"
            "of matter and energy at the atomic and subatomic level",
            font_size=18, color=GREEN
        )
        insight.to_edge(DOWN)
        self.play(Write(insight), run_time=2)
        
        self.wait(2)
        self.play(FadeOut(VGroup(title, table, insight)), run_time=2)
    
    def part_2_wave_particle_duality(self):
        """Part 2: Wave-Particle Duality."""
        # Title
        title = Text("Part 2: Wave-Particle Duality", font_size=36, color=GREEN)
        title.to_edge(UP)
        self.play(Write(title))
        
        # Explanation
        explanation = Text(
            "Light and matter exhibit both wave and particle properties\n"
            "depending on the experimental setup",
            font_size=20, color=WHITE
        )
        explanation.next_to(title, DOWN, buff=1)
        self.play(Write(explanation))
        
        # Create wave and particle representations
        wave_rep = self.create_wave_representation()
        particle_rep = self.create_particle_representation()
        
        # Position them side by side
        wave_rep.to_edge(LEFT)
        particle_rep.to_edge(RIGHT)
        
        self.play(Create(wave_rep), run_time=1.5)
        self.play(Create(particle_rep), run_time=1.5)
        
        # Animate wave properties
        self.animate_wave_properties(wave_rep)
        
        # Animate particle properties
        self.animate_particle_properties(particle_rep)
        
        # De Broglie equation
        equation = MathTex(
            r"\lambda = \frac{h}{p}",
            font_size=24, color=YELLOW
        )
        equation.to_edge(DOWN)
        self.play(Write(equation), run_time=1)
        
        # Explanation of equation
        eq_explanation = Text(
            "De Broglie wavelength: λ = h/p\n"
            "where h is Planck's constant and p is momentum",
            font_size=16, color=GRAY
        )
        eq_explanation.next_to(equation, DOWN)
        self.play(Write(eq_explanation), run_time=1.5)
        
        self.wait(2)
        self.play(FadeOut(VGroup(title, explanation, wave_rep, particle_rep, 
                                equation, eq_explanation)), run_time=2)
    
    def part_3_schrodinger_equation(self):
        """Part 3: The Schrödinger Equation."""
        # Title
        title = Text("Part 3: The Schrödinger Equation", font_size=36, color=YELLOW)
        title.to_edge(UP)
        self.play(Write(title))
        
        # Introduction
        intro = Text(
            "The fundamental equation of quantum mechanics\n"
            "describes how quantum states evolve over time",
            font_size=18, color=WHITE
        )
        intro.next_to(title, DOWN, buff=1)
        self.play(Write(intro))
        
        # Show the equation
        equation = MathTex(
            r"i\hbar \frac{\partial \Psi}{\partial t} = \hat{H} \Psi",
            font_size=32, color=YELLOW
        )
        equation.next_to(intro, DOWN, buff=1)
        self.play(Write(equation), run_time=2)
        
        # Explain each part
        self.explain_schrodinger_equation(equation)
        
        # Show Hamiltonian
        hamiltonian = MathTex(
            r"\hat{H} = \frac{\hat{p}^2}{2m} + V(\hat{x})",
            font_size=24, color=BLUE
        )
        hamiltonian.next_to(equation, DOWN, buff=1)
        self.play(Write(hamiltonian), run_time=1.5)
        
        # Show wave function properties
        self.show_wave_function_properties()
        
        self.wait(2)
        self.play(FadeOut(VGroup(title, intro, equation, hamiltonian)), run_time=2)
    
    def part_4_quantum_states(self):
        """Part 4: Quantum States and Superposition."""
        # Title
        title = Text("Part 4: Quantum States and Superposition", font_size=36, color=PURPLE)
        title.to_edge(UP)
        self.play(Write(title))
        
        # Explanation
        explanation = Text(
            "Quantum systems can exist in superposition of multiple states\n"
            "until measurement collapses the wave function",
            font_size=18, color=WHITE
        )
        explanation.next_to(title, DOWN, buff=1)
        self.play(Write(explanation))
        
        # Create quantum state visualization
        self.visualize_quantum_states()
        
        # Show measurement process
        self.show_measurement_process()
        
        # Uncertainty principle
        self.show_uncertainty_principle()
        
        self.wait(2)
        self.play(FadeOut(VGroup(title, explanation)), run_time=2)
    
    def part_5_quantum_tunneling(self):
        """Part 5: Quantum Tunneling."""
        # Title
        title = Text("Part 5: Quantum Tunneling", font_size=36, color=ORANGE)
        title.to_edge(UP)
        self.play(Write(title))
        
        # Explanation
        explanation = Text(
            "Particles can pass through energy barriers\n"
            "that would be impossible in classical physics",
            font_size=18, color=WHITE
        )
        explanation.next_to(title, DOWN, buff=1)
        self.play(Write(explanation))
        
        # Create tunneling visualization
        self.visualize_quantum_tunneling()
        
        # Applications
        applications = VGroup(
            Text("Applications:", font_size=20, color=BLUE),
            Text("• Scanning tunneling microscope", font_size=16, color=WHITE),
            Text("• Nuclear fusion in stars", font_size=16, color=WHITE),
            Text("• Quantum computing", font_size=16, color=WHITE)
        )
        applications.arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        applications.to_edge(DOWN)
        self.play(Write(applications), run_time=2)
        
        self.wait(2)
        self.play(FadeOut(VGroup(title, explanation, applications)), run_time=2)
    
    def part_6_atomic_structure(self):
        """Part 6: Atomic Structure."""
        # Title
        title = Text("Part 6: Atomic Structure", font_size=36, color=RED)
        title.to_edge(UP)
        self.play(Write(title))
        
        # Create 3D atom
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        
        # Create atom
        atom = self.create_3d_atom()
        self.play(Create(atom), run_time=2)
        
        # Show electron orbitals
        self.show_electron_orbitals(atom)
        
        # Show energy levels
        self.show_energy_levels()
        
        # Quantum numbers
        self.show_quantum_numbers()
        
        self.wait(2)
        self.play(FadeOut(atom), run_time=2)
    
    def part_7_quantum_field_theory(self):
        """Part 7: Quantum Field Theory."""
        # Title
        title = Text("Part 7: Quantum Field Theory", font_size=36, color=CYAN)
        title.to_edge(UP)
        self.play(Write(title))
        
        # Explanation
        explanation = Text(
            "Particles are excitations of quantum fields\n"
            "that permeate all of space",
            font_size=18, color=WHITE
        )
        explanation.next_to(title, DOWN, buff=1)
        self.play(Write(explanation))
        
        # Create field visualization
        self.visualize_quantum_fields()
        
        # Show particle creation/annihilation
        self.show_particle_creation_annihilation()
        
        # Standard Model
        self.show_standard_model()
        
        self.wait(2)
        self.play(FadeOut(VGroup(title, explanation)), run_time=2)
    
    def part_8_void_physics_hypothesis(self):
        """Part 8: Void Physics Hypothesis (with disclaimers)."""
        # Title with disclaimer
        title = Text("Part 8: Void Physics Hypothesis", font_size=36, color=GOLD)
        title.to_edge(UP)
        
        disclaimer = Text(
            "⚠️ SPECULATIVE HYPOTHESIS - NOT ESTABLISHED SCIENCE ⚠️",
            font_size=16, color=RED
        )
        disclaimer.next_to(title, DOWN)
        
        self.play(Write(title), run_time=1)
        self.play(Write(disclaimer), run_time=1)
        
        # Explanation
        explanation = Text(
            "This is a speculative framework exploring the idea that\n"
            "particles might emerge from a 'void' state through\n"
            "quantum fluctuations and field excitations",
            font_size=16, color=WHITE
        )
        explanation.next_to(disclaimer, DOWN, buff=1)
        self.play(Write(explanation), run_time=2)
        
        # What's scientific vs speculative
        scientific = VGroup(
            Text("Scientific Foundation:", font_size=18, color=GREEN),
            Text("• Quantum field theory", font_size=14, color=WHITE),
            Text("• Vacuum fluctuations", font_size=14, color=WHITE),
            Text("• Particle creation/annihilation", font_size=14, color=WHITE)
        )
        scientific.arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        scientific.to_edge(LEFT)
        
        speculative = VGroup(
            Text("Speculative Elements:", font_size=18, color=ORANGE),
            Text("• Void as fundamental state", font_size=14, color=WHITE),
            Text("• Emergence mechanisms", font_size=14, color=WHITE),
            Text("• Connection to cosmology", font_size=14, color=WHITE)
        )
        speculative.arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        speculative.to_edge(RIGHT)
        
        self.play(Write(scientific), run_time=1.5)
        self.play(Write(speculative), run_time=1.5)
        
        # Visualization of void physics
        self.visualize_void_physics_hypothesis()
        
        # Final disclaimer
        final_disclaimer = Text(
            "This framework is for educational and exploratory purposes only.\n"
            "It does not represent established physics.",
            font_size=14, color=RED
        )
        final_disclaimer.to_edge(DOWN)
        self.play(Write(final_disclaimer), run_time=2)
        
        self.wait(3)
        self.play(FadeOut(VGroup(title, disclaimer, explanation, scientific, 
                                speculative, final_disclaimer)), run_time=2)
    
    def conclusion(self):
        """Conclusion and summary."""
        # Title
        title = Text("Conclusion", font_size=48, color=WHITE)
        title.to_edge(UP)
        self.play(Write(title), run_time=2)
        
        # Summary
        summary = VGroup(
            Text("Key Takeaways:", font_size=24, color=BLUE),
            Text("• Quantum mechanics describes atomic-scale phenomena", font_size=18, color=WHITE),
            Text("• Wave-particle duality is fundamental", font_size=18, color=WHITE),
            Text("• Superposition and measurement are key concepts", font_size=18, color=WHITE),
            Text("• Quantum field theory extends to all particles", font_size=18, color=WHITE),
            Text("• Void physics remains speculative", font_size=18, color=ORANGE)
        )
        summary.arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        summary.next_to(title, DOWN, buff=1)
        
        for item in summary:
            self.play(Write(item), run_time=0.8)
        
        # Final message
        final_message = Text(
            "Continue exploring the quantum world!\n"
            "Science is an ongoing journey of discovery.",
            font_size=20, color=GREEN
        )
        final_message.to_edge(DOWN)
        self.play(Write(final_message), run_time=2)
        
        self.wait(3)
        self.play(FadeOut(VGroup(title, summary, final_message)), run_time=2)
    
    # Helper methods for creating visualizations
    
    def create_classical_quantum_table(self):
        """Create a comparison table between classical and quantum physics."""
        table = VGroup()
        
        # Headers
        classical_header = Text("Classical Physics", font_size=20, color=BLUE)
        quantum_header = Text("Quantum Physics", font_size=20, color=GREEN)
        
        # Properties
        classical_props = VGroup(
            Text("• Deterministic", font_size=16, color=WHITE),
            Text("• Continuous energy", font_size=16, color=WHITE),
            Text("• Particle or wave", font_size=16, color=WHITE),
            Text("• Classical mechanics", font_size=16, color=WHITE)
        )
        classical_props.arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        
        quantum_props = VGroup(
            Text("• Probabilistic", font_size=16, color=WHITE),
            Text("• Quantized energy", font_size=16, color=WHITE),
            Text("• Wave-particle duality", font_size=16, color=WHITE),
            Text("• Quantum mechanics", font_size=16, color=WHITE)
        )
        quantum_props.arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        
        # Position elements
        classical_header.to_edge(LEFT)
        quantum_header.to_edge(RIGHT)
        classical_props.next_to(classical_header, DOWN, buff=0.5)
        quantum_props.next_to(quantum_header, DOWN, buff=0.5)
        
        table.add(classical_header, quantum_header, classical_props, quantum_props)
        return table
    
    def animate_classical_particle(self):
        """Animate a classical particle."""
        particle = Dot(color=BLUE, radius=0.1)
        particle.to_edge(LEFT)
        
        # Classical trajectory
        trajectory = Line(particle.get_center(), particle.get_center() + RIGHT * 3, color=BLUE)
        
        self.play(Create(particle), run_time=0.5)
        self.play(Create(trajectory), run_time=0.5)
        self.play(particle.animate.move_to(particle.get_center() + RIGHT * 3), run_time=2)
        
        self.play(FadeOut(VGroup(particle, trajectory)), run_time=0.5)
    
    def animate_quantum_particle(self):
        """Animate a quantum particle."""
        # Wave packet
        wave_packet = self.create_wave_packet()
        wave_packet.to_edge(RIGHT)
        
        self.play(Create(wave_packet), run_time=1)
        
        # Show spreading
        for i in range(10):
            new_packet = self.create_wave_packet(spread=i*0.1)
            new_packet.to_edge(RIGHT)
            self.play(Transform(wave_packet, new_packet), run_time=0.2)
        
        self.play(FadeOut(wave_packet), run_time=0.5)
    
    def create_wave_packet(self, spread=0):
        """Create a wave packet visualization."""
        x_vals = np.linspace(-2, 2, 100)
        y_vals = np.exp(-x_vals**2 / (1 + spread)) * np.sin(5 * x_vals)
        
        wave = VGroup()
        for i in range(len(x_vals) - 1):
            line = Line(
                [x_vals[i], y_vals[i], 0],
                [x_vals[i+1], y_vals[i+1], 0],
                color=GREEN,
                stroke_width=2
            )
            wave.add(line)
        
        return wave
    
    def create_wave_representation(self):
        """Create wave representation."""
        wave = VGroup()
        for i in range(5):
            sine_wave = FunctionGraph(
                lambda x: 0.5 * np.sin(2 * PI * x + i * PI/2),
                x_range=[-2, 2],
                color=BLUE
            )
            sine_wave.shift(UP * i * 0.5)
            wave.add(sine_wave)
        
        return wave
    
    def create_particle_representation(self):
        """Create particle representation."""
        particles = VGroup()
        for i in range(5):
            particle = Dot(color=RED, radius=0.1)
            particle.move_to([0, i * 0.5, 0])
            particles.add(particle)
        
        return particles
    
    def animate_wave_properties(self, wave_rep):
        """Animate wave properties."""
        for i in range(20):
            new_wave = VGroup()
            for j, sine_wave in enumerate(wave_rep):
                new_sine = FunctionGraph(
                    lambda x: 0.5 * np.sin(2 * PI * x + i * 0.1 + j * PI/2),
                    x_range=[-2, 2],
                    color=BLUE
                )
                new_sine.shift(UP * j * 0.5)
                new_wave.add(new_sine)
            
            self.play(Transform(wave_rep, new_wave), run_time=0.1)
    
    def animate_particle_properties(self, particle_rep):
        """Animate particle properties."""
        for i in range(20):
            new_particles = VGroup()
            for j, particle in enumerate(particle_rep):
                new_particle = Dot(color=RED, radius=0.1)
                new_particle.move_to([np.sin(i * 0.1 + j) * 0.5, j * 0.5, 0])
                new_particles.add(new_particle)
            
            self.play(Transform(particle_rep, new_particles), run_time=0.1)
    
    def explain_schrodinger_equation(self, equation):
        """Explain parts of the Schrödinger equation."""
        # Highlight iℏ
        i_hbar = equation[0:2]
        self.play(Indicate(i_hbar, color=YELLOW), run_time=1)
        
        # Highlight ∂Ψ/∂t
        partial_psi = equation[2:6]
        self.play(Indicate(partial_psi, color=GREEN), run_time=1)
        
        # Highlight Ĥ
        hamiltonian = equation[7:8]
        self.play(Indicate(hamiltonian, color=BLUE), run_time=1)
        
        # Highlight Ψ
        psi = equation[9:10]
        self.play(Indicate(psi, color=RED), run_time=1)
    
    def show_wave_function_properties(self):
        """Show properties of the wave function."""
        properties = VGroup(
            Text("Wave Function Properties:", font_size=20, color=BLUE),
            Text("• Complex-valued: Ψ(x,t) = A(x,t) + iB(x,t)", font_size=16, color=WHITE),
            Text("• Probability density: |Ψ|²", font_size=16, color=WHITE),
            Text("• Normalization: ∫|Ψ|²dx = 1", font_size=16, color=WHITE),
            Text("• Superposition principle", font_size=16, color=WHITE)
        )
        properties.arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        properties.to_edge(DOWN)
        
        for prop in properties:
            self.play(Write(prop), run_time=0.8)
    
    def visualize_quantum_states(self):
        """Visualize quantum states and superposition."""
        # Create superposition visualization
        state1 = Text("|0⟩", font_size=24, color=BLUE)
        state2 = Text("|1⟩", font_size=24, color=RED)
        plus = Text("+", font_size=24, color=WHITE)
        
        superposition = VGroup(state1, plus, state2)
        superposition.arrange(RIGHT, buff=0.5)
        superposition.move_to(ORIGIN)
        
        self.play(Write(superposition), run_time=1.5)
        
        # Show measurement
        measurement = Text("Measurement → Collapse to |0⟩ or |1⟩", 
                          font_size=18, color=YELLOW)
        measurement.next_to(superposition, DOWN, buff=1)
        self.play(Write(measurement), run_time=1.5)
    
    def show_measurement_process(self):
        """Show the measurement process."""
        # Before measurement
        before = Text("Before measurement: Superposition", font_size=16, color=GREEN)
        before.to_edge(LEFT)
        
        # After measurement
        after = Text("After measurement: Definite state", font_size=16, color=RED)
        after.to_edge(RIGHT)
        
        self.play(Write(before), run_time=1)
        self.play(Write(after), run_time=1)
    
    def show_uncertainty_principle(self):
        """Show the uncertainty principle."""
        uncertainty = MathTex(
            r"\Delta x \Delta p \geq \frac{\hbar}{2}",
            font_size=24, color=ORANGE
        )
        uncertainty.to_edge(DOWN)
        
        explanation = Text(
            "The more precisely we know position, the less precisely\n"
            "we can know momentum, and vice versa",
            font_size=16, color=WHITE
        )
        explanation.next_to(uncertainty, DOWN)
        
        self.play(Write(uncertainty), run_time=1)
        self.play(Write(explanation), run_time=1.5)
    
    def visualize_quantum_tunneling(self):
        """Visualize quantum tunneling."""
        # Create barrier
        barrier = Rectangle(width=0.5, height=2, color=RED, fill_opacity=0.7)
        barrier.move_to(ORIGIN)
        
        # Create wave packet
        wave_packet = self.create_wave_packet()
        wave_packet.to_edge(LEFT)
        
        self.play(Create(barrier), run_time=1)
        self.play(Create(wave_packet), run_time=1)
        
        # Show tunneling
        for i in range(20):
            new_packet = self.create_wave_packet()
            new_packet.shift(RIGHT * i * 0.2)
            self.play(Transform(wave_packet, new_packet), run_time=0.1)
    
    def create_3d_atom(self):
        """Create a 3D atom visualization."""
        atom = VGroup()
        
        # Nucleus
        nucleus = Sphere(radius=0.3, color=RED)
        atom.add(nucleus)
        
        # Electron orbitals
        for n in range(1, 4):
            orbital = Circle(radius=n * 0.5, color=BLUE)
            orbital.set_stroke(width=2)
            atom.add(orbital)
        
        return atom
    
    def show_electron_orbitals(self, atom):
        """Show electron orbitals."""
        # Add electrons
        electrons = VGroup()
        for i in range(6):
            electron = Sphere(radius=0.1, color=YELLOW)
            electron.move_to([np.cos(i * PI/3), np.sin(i * PI/3), 0])
            electrons.add(electron)
        
        atom.add(electrons)
        self.play(Create(electrons), run_time=1)
        
        # Animate electron motion
        for i in range(30):
            new_electrons = VGroup()
            for j, electron in enumerate(electrons):
                angle = i * 0.1 + j * PI/3
                new_electron = Sphere(radius=0.1, color=YELLOW)
                new_electron.move_to([np.cos(angle), np.sin(angle), 0])
                new_electrons.add(new_electron)
            
            self.play(Transform(electrons, new_electrons), run_time=0.1)
    
    def show_energy_levels(self):
        """Show energy levels."""
        energy_levels = VGroup()
        for n in range(1, 5):
            level = Text(f"n = {n}", font_size=16, color=WHITE)
            level.move_to([3, n * 0.5, 0])
            energy_levels.add(level)
        
        self.play(Write(energy_levels), run_time=1.5)
    
    def show_quantum_numbers(self):
        """Show quantum numbers."""
        quantum_numbers = VGroup(
            Text("Quantum Numbers:", font_size=18, color=BLUE),
            Text("n: Principal quantum number", font_size=14, color=WHITE),
            Text("l: Orbital angular momentum", font_size=14, color=WHITE),
            Text("m: Magnetic quantum number", font_size=14, color=WHITE),
            Text("s: Spin quantum number", font_size=14, color=WHITE)
        )
        quantum_numbers.arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        quantum_numbers.to_edge(DOWN)
        
        for qn in quantum_numbers:
            self.play(Write(qn), run_time=0.5)
    
    def visualize_quantum_fields(self):
        """Visualize quantum fields."""
        # Create field visualization
        field = VGroup()
        for i in range(20):
            for j in range(20):
                x = (i - 10) * 0.2
                y = (j - 10) * 0.2
                z = 0.1 * np.sin(x) * np.cos(y)
                
                point = Dot3D([x, y, z], color=BLUE, radius=0.02)
                field.add(point)
        
        self.play(Create(field), run_time=2)
    
    def show_particle_creation_annihilation(self):
        """Show particle creation and annihilation."""
        # Create particle
        particle = Dot(color=GREEN, radius=0.1)
        particle.move_to(LEFT * 2)
        
        self.play(Create(particle), run_time=0.5)
        
        # Show annihilation
        self.play(FadeOut(particle), run_time=0.5)
        
        # Show creation
        self.play(Create(particle), run_time=0.5)
    
    def show_standard_model(self):
        """Show the Standard Model."""
        standard_model = VGroup(
            Text("Standard Model Particles:", font_size=18, color=BLUE),
            Text("• Quarks (up, down, charm, strange, top, bottom)", font_size=14, color=WHITE),
            Text("• Leptons (electron, muon, tau, neutrinos)", font_size=14, color=WHITE),
            Text("• Force carriers (photon, W, Z, gluons)", font_size=14, color=WHITE),
            Text("• Higgs boson", font_size=14, color=WHITE)
        )
        standard_model.arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        standard_model.to_edge(DOWN)
        
        for particle in standard_model:
            self.play(Write(particle), run_time=0.5)
    
    def visualize_void_physics_hypothesis(self):
        """Visualize the void physics hypothesis."""
        # Create void state
        void = Circle(radius=2, color=BLACK, fill_opacity=0.8)
        void.set_stroke(WHITE, width=2)
        
        # Add quantum fluctuations
        fluctuations = VGroup()
        for i in range(20):
            fluctuation = Dot(color=YELLOW, radius=0.05)
            fluctuation.move_to([np.random.uniform(-1.5, 1.5), 
                               np.random.uniform(-1.5, 1.5), 0])
            fluctuations.add(fluctuation)
        
        # Show emergence
        particles = VGroup()
        for i in range(5):
            particle = Dot(color=GREEN, radius=0.1)
            particle.move_to([np.random.uniform(-1.5, 1.5), 
                            np.random.uniform(-1.5, 1.5), 0])
            particles.add(particle)
        
        self.play(Create(void), run_time=1)
        self.play(Create(fluctuations), run_time=1)
        self.play(Create(particles), run_time=1)


def main():
    """Main function to run the educational animation."""
    import sys
    
    if len(sys.argv) > 1:
        scene_name = sys.argv[1]
        
        if scene_name == "full":
            scene = QuantumMechanicsEducation()
        else:
            print("Available scenes: full")
            return
        
        scene.render()
    else:
        print("Usage: python quantum_mechanics_education.py full")
        print("Available scenes: full")


if __name__ == "__main__":
    main()
