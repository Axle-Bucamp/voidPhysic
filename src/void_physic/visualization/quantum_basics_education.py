"""
Quantum Mechanics Basics - Educational Animation

A focused educational animation covering the fundamental concepts
of quantum mechanics with clear scientific accuracy and pedagogical approach.
"""

import numpy as np
from manim import *
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class QuantumBasicsEducation(Scene):
    """
    Educational animation covering quantum mechanics basics:
    - Wave-particle duality
    - Schrödinger equation
    - Quantum states
    - Atomic structure
    """
    
    def construct(self):
        # Introduction
        self.introduction()
        
        # Wave-Particle Duality
        self.wave_particle_duality()
        
        # Schrödinger Equation
        self.schrodinger_equation()
        
        # Quantum States
        self.quantum_states()
        
        # Atomic Structure
        self.atomic_structure()
        
        # Conclusion
        self.conclusion()
    
    def introduction(self):
        """Introduction to quantum mechanics."""
        # Title
        title = Text("Quantum Mechanics Basics", font_size=48, color=WHITE)
        subtitle = Text("Understanding the Quantum World", font_size=24, color=GRAY)
        subtitle.next_to(title, DOWN)
        
        # What we'll learn
        objectives = VGroup(
            Text("What we'll learn:", font_size=20, color=BLUE),
            Text("• Wave-particle duality", font_size=16, color=WHITE),
            Text("• The Schrödinger equation", font_size=16, color=WHITE),
            Text("• Quantum states and superposition", font_size=16, color=WHITE),
            Text("• Atomic structure", font_size=16, color=WHITE)
        )
        objectives.arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        objectives.next_to(subtitle, DOWN, buff=1)
        
        # Show introduction
        self.play(Write(title), run_time=2)
        self.play(Write(subtitle), run_time=1)
        
        for obj in objectives:
            self.play(Write(obj), run_time=0.5)
        
        self.wait(2)
        self.play(FadeOut(VGroup(title, subtitle, objectives)), run_time=2)
    
    def wave_particle_duality(self):
        """Explain wave-particle duality."""
        # Title
        title = Text("Wave-Particle Duality", font_size=36, color=GREEN)
        title.to_edge(UP)
        self.play(Write(title))
        
        # Explanation
        explanation = Text(
            "Light and matter exhibit both wave and particle properties\n"
            "depending on how we observe them",
            font_size=18, color=WHITE
        )
        explanation.next_to(title, DOWN, buff=1)
        self.play(Write(explanation))
        
        # Create wave and particle representations
        wave_section = VGroup()
        wave_title = Text("Wave Properties", font_size=20, color=BLUE)
        wave_title.to_edge(LEFT)
        wave_section.add(wave_title)
        
        # Wave visualization
        wave = FunctionGraph(
            lambda x: 0.5 * np.sin(2 * PI * x),
            x_range=[-2, 2],
            color=BLUE
        )
        wave.next_to(wave_title, DOWN, buff=0.5)
        wave_section.add(wave)
        
        # Wave properties
        wave_props = VGroup(
            Text("• Interference", font_size=14, color=WHITE),
            Text("• Diffraction", font_size=14, color=WHITE),
            Text("• Wavelength", font_size=14, color=WHITE)
        )
        wave_props.arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        wave_props.next_to(wave, DOWN, buff=0.5)
        wave_section.add(wave_props)
        
        # Particle section
        particle_section = VGroup()
        particle_title = Text("Particle Properties", font_size=20, color=RED)
        particle_title.to_edge(RIGHT)
        particle_section.add(particle_title)
        
        # Particle visualization
        particle = Dot(color=RED, radius=0.2)
        particle.next_to(particle_title, DOWN, buff=0.5)
        particle_section.add(particle)
        
        # Particle properties
        particle_props = VGroup(
            Text("• Localized", font_size=14, color=WHITE),
            Text("• Momentum", font_size=14, color=WHITE),
            Text("• Energy", font_size=14, color=WHITE)
        )
        particle_props.arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        particle_props.next_to(particle, DOWN, buff=0.5)
        particle_section.add(particle_props)
        
        # Show both sections
        self.play(Create(wave_section), run_time=1.5)
        self.play(Create(particle_section), run_time=1.5)
        
        # Animate wave
        for i in range(20):
            new_wave = FunctionGraph(
                lambda x: 0.5 * np.sin(2 * PI * x + i * 0.1),
                x_range=[-2, 2],
                color=BLUE
            )
            new_wave.next_to(wave_title, DOWN, buff=0.5)
            self.play(Transform(wave, new_wave), run_time=0.1)
        
        # Animate particle
        for i in range(20):
            new_particle = Dot(color=RED, radius=0.2)
            new_particle.move_to([2 + np.sin(i * 0.1) * 0.5, -1, 0])
            self.play(Transform(particle, new_particle), run_time=0.1)
        
        # De Broglie equation
        equation = Text("λ = h/p", font_size=24, color=YELLOW)
        equation.to_edge(DOWN)
        self.play(Write(equation), run_time=1)
        
        # Explanation of equation
        eq_explanation = Text(
            "De Broglie wavelength: Every particle has a wavelength",
            font_size=16, color=GRAY
        )
        eq_explanation.next_to(equation, DOWN)
        self.play(Write(eq_explanation), run_time=1.5)
        
        self.wait(2)
        self.play(FadeOut(VGroup(title, explanation, wave_section, particle_section, 
                                equation, eq_explanation)), run_time=2)
    
    def schrodinger_equation(self):
        """Explain the Schrödinger equation."""
        # Title
        title = Text("The Schrödinger Equation", font_size=36, color=YELLOW)
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
        equation = Text("iℏ ∂Ψ/∂t = ĤΨ", font_size=32, color=YELLOW)
        equation.next_to(intro, DOWN, buff=1)
        self.play(Write(equation), run_time=2)
        
        # Explain each part
        self.explain_equation_parts(equation)
        
        # Show Hamiltonian
        hamiltonian = Text("Ĥ = p̂²/(2m) + V(x̂)", font_size=24, color=BLUE)
        hamiltonian.next_to(equation, DOWN, buff=1)
        self.play(Write(hamiltonian), run_time=1.5)
        
        # Explain Hamiltonian
        hamiltonian_explanation = VGroup(
            Text("Hamiltonian = Kinetic Energy + Potential Energy", font_size=16, color=WHITE),
            Text("Ĥ = p²/(2m) + V(x)", font_size=14, color=GRAY)
        )
        hamiltonian_explanation.arrange(DOWN, buff=0.2)
        hamiltonian_explanation.next_to(hamiltonian, DOWN, buff=0.5)
        self.play(Write(hamiltonian_explanation), run_time=1.5)
        
        # Show wave function properties
        properties = VGroup(
            Text("Wave Function Properties:", font_size=18, color=BLUE),
            Text("• Complex-valued: Ψ(x,t) = A(x,t) + iB(x,t)", font_size=14, color=WHITE),
            Text("• Probability density: |Ψ|²", font_size=14, color=WHITE),
            Text("• Normalization: ∫|Ψ|²dx = 1", font_size=14, color=WHITE)
        )
        properties.arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        properties.to_edge(DOWN)
        
        for prop in properties:
            self.play(Write(prop), run_time=0.8)
        
        self.wait(2)
        self.play(FadeOut(VGroup(title, intro, equation, hamiltonian, 
                                hamiltonian_explanation, properties)), run_time=2)
    
    def quantum_states(self):
        """Explain quantum states and superposition."""
        # Title
        title = Text("Quantum States and Superposition", font_size=36, color=PURPLE)
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
        
        # Create superposition visualization
        state1 = Text("|0⟩", font_size=32, color=BLUE)
        state2 = Text("|1⟩", font_size=32, color=RED)
        plus = Text("+", font_size=32, color=WHITE)
        
        superposition = VGroup(state1, plus, state2)
        superposition.arrange(RIGHT, buff=0.5)
        superposition.move_to(ORIGIN)
        
        self.play(Write(superposition), run_time=1.5)
        
        # Show measurement
        measurement = Text("Measurement → Collapse to |0⟩ or |1⟩", 
                          font_size=18, color=YELLOW)
        measurement.next_to(superposition, DOWN, buff=1)
        self.play(Write(measurement), run_time=1.5)
        
        # Show collapse animation
        self.animate_measurement_collapse(superposition)
        
        # Uncertainty principle
        uncertainty = Text("Δx Δp ≥ ℏ/2", font_size=24, color=ORANGE)
        uncertainty.to_edge(DOWN)
        
        uncertainty_explanation = Text(
            "Uncertainty Principle: The more precisely we know position,\n"
            "the less precisely we can know momentum",
            font_size=16, color=WHITE
        )
        uncertainty_explanation.next_to(uncertainty, DOWN)
        
        self.play(Write(uncertainty), run_time=1)
        self.play(Write(uncertainty_explanation), run_time=1.5)
        
        self.wait(2)
        self.play(FadeOut(VGroup(title, explanation, superposition, measurement, 
                                uncertainty, uncertainty_explanation)), run_time=2)
    
    def atomic_structure(self):
        """Explain atomic structure."""
        # Title
        title = Text("Atomic Structure", font_size=36, color=RED)
        title.to_edge(UP)
        self.play(Write(title))
        
        # Create atom
        atom = self.create_atom_visualization()
        self.play(Create(atom), run_time=2)
        
        # Show energy levels
        self.show_energy_levels()
        
        # Show quantum numbers
        self.show_quantum_numbers()
        
        # Show electron configuration
        self.show_electron_configuration()
        
        self.wait(2)
        self.play(FadeOut(atom), run_time=2)
    
    def conclusion(self):
        """Conclusion and summary."""
        # Title
        title = Text("Conclusion", font_size=48, color=WHITE)
        title.to_edge(UP)
        self.play(Write(title), run_time=2)
        
        # Summary
        summary = VGroup(
            Text("Key Concepts:", font_size=24, color=BLUE),
            Text("• Wave-particle duality is fundamental", font_size=18, color=WHITE),
            Text("• Schrödinger equation describes quantum evolution", font_size=18, color=WHITE),
            Text("• Superposition allows multiple states", font_size=18, color=WHITE),
            Text("• Measurement collapses the wave function", font_size=18, color=WHITE),
            Text("• Atoms have quantized energy levels", font_size=18, color=WHITE)
        )
        summary.arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        summary.next_to(title, DOWN, buff=1)
        
        for item in summary:
            self.play(Write(item), run_time=0.8)
        
        # Final message
        final_message = Text(
            "Quantum mechanics is the foundation of modern physics!\n"
            "Continue exploring the quantum world.",
            font_size=20, color=GREEN
        )
        final_message.to_edge(DOWN)
        self.play(Write(final_message), run_time=2)
        
        self.wait(3)
        self.play(FadeOut(VGroup(title, summary, final_message)), run_time=2)
    
    # Helper methods
    
    def explain_equation_parts(self, equation):
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
    
    def animate_measurement_collapse(self, superposition):
        """Animate measurement collapse."""
        # Show collapse to |0⟩
        collapse_to_0 = Text("|0⟩", font_size=32, color=BLUE)
        collapse_to_0.move_to(superposition.get_center())
        
        self.play(Transform(superposition, collapse_to_0), run_time=1)
        self.wait(0.5)
        
        # Show collapse to |1⟩
        collapse_to_1 = Text("|1⟩", font_size=32, color=RED)
        collapse_to_1.move_to(superposition.get_center())
        
        self.play(Transform(superposition, collapse_to_1), run_time=1)
        self.wait(0.5)
    
    def create_atom_visualization(self):
        """Create atom visualization."""
        atom = VGroup()
        
        # Nucleus
        nucleus = Circle(radius=0.3, color=RED, fill_opacity=0.8)
        atom.add(nucleus)
        
        # Electron orbitals
        for n in range(1, 4):
            orbital = Circle(radius=n * 0.5, color=BLUE)
            orbital.set_stroke(width=2)
            atom.add(orbital)
        
        # Electrons
        electrons = VGroup()
        for i in range(6):
            electron = Dot(color=YELLOW, radius=0.1)
            electron.move_to([np.cos(i * PI/3) * 0.8, np.sin(i * PI/3) * 0.8, 0])
            electrons.add(electron)
        
        atom.add(electrons)
        
        # Animate electron motion
        for i in range(30):
            new_electrons = VGroup()
            for j, electron in enumerate(electrons):
                angle = i * 0.1 + j * PI/3
                new_electron = Dot(color=YELLOW, radius=0.1)
                new_electron.move_to([np.cos(angle) * 0.8, np.sin(angle) * 0.8, 0])
                new_electrons.add(new_electron)
            
            self.play(Transform(electrons, new_electrons), run_time=0.1)
        
        return atom
    
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
    
    def show_electron_configuration(self):
        """Show electron configuration."""
        config = VGroup(
            Text("Electron Configuration:", font_size=18, color=GREEN),
            Text("1s² 2s² 2p⁶ 3s² 3p⁶ 4s² 3d¹⁰...", font_size=16, color=WHITE)
        )
        config.arrange(DOWN, buff=0.2)
        config.to_edge(DOWN)
        
        self.play(Write(config), run_time=1.5)


def main():
    """Main function to run the educational animation."""
    import sys
    
    if len(sys.argv) > 1:
        scene_name = sys.argv[1]
        
        if scene_name == "basics":
            scene = QuantumBasicsEducation()
        else:
            print("Available scenes: basics")
            return
        
        scene.render()
    else:
        print("Usage: python quantum_basics_education.py basics")
        print("Available scenes: basics")


if __name__ == "__main__":
    main()
