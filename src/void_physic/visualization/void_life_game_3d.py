"""
3D Manim visualization for Void Physics Life Game.

This module creates stunning 3D animations showing the emergence of particles
from the void, their evolution, and the formation of complex structures.
"""

import numpy as np
from manim import *
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VoidLifeGame3D(ThreeDScene):
    """
    3D visualization of the Void Physics Life Game showing particle emergence,
    evolution, and complex structure formation.
    """
    
    def construct(self):
        # Title sequence
        self.title_sequence()
        
        # Act 1: The Void
        self.act_1_the_void()
        
        # Act 2: Quantum Fluctuations
        self.act_2_quantum_fluctuations()
        
        # Act 3: Particle Emergence
        self.act_3_particle_emergence()
        
        # Act 4: Structure Formation
        self.act_4_structure_formation()
        
        # Act 5: Universe Evolution
        self.act_5_universe_evolution()
        
        # Final credits
        self.final_credits()
    
    def title_sequence(self):
        """Animated title sequence."""
        # Main title
        title = Text("Void Physics Life Game", font_size=48, color=WHITE)
        subtitle = Text("From Nothing to Everything", font_size=24, color=GRAY)
        subtitle.next_to(title, DOWN)
        
        # Create title group
        title_group = VGroup(title, subtitle)
        title_group.move_to(ORIGIN)
        
        # Animate title
        self.play(Write(title), run_time=2)
        self.play(Write(subtitle), run_time=1)
        self.wait(1)
        
        # Transform to 3D
        self.play(
            title_group.animate.rotate(PI/4, axis=UP),
            run_time=2
        )
        self.wait(1)
        
        # Fade out
        self.play(FadeOut(title_group), run_time=1)
    
    def act_1_the_void(self):
        """Act 1: Show the primordial void state."""
        # Title
        act_title = Text("Act 1: The Void", font_size=36, color=CYAN)
        act_title.to_edge(UP)
        self.play(Write(act_title))
        
        # Create 3D void space
        void_space = Sphere(radius=3, color=BLACK, fill_opacity=0.8)
        void_space.set_stroke(WHITE, width=2)
        
        # Add void description
        void_text = Text("The primordial void\nwhere all possibilities exist", 
                        font_size=20, color=WHITE)
        void_text.to_edge(DOWN)
        
        # Show void
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        self.play(Create(void_space), run_time=2)
        self.play(Write(void_text), run_time=1)
        
        # Add subtle void field visualization
        void_field = self.create_void_field()
        self.play(Create(void_field), run_time=2)
        
        # Animate void field
        self.begin_ambient_camera_rotation(rate=0.1)
        for i in range(30):
            new_field = self.create_void_field(time=i*0.1)
            self.play(Transform(void_field, new_field), run_time=0.1)
        self.stop_ambient_camera_rotation()
        
        # Transition
        self.play(
            FadeOut(act_title),
            FadeOut(void_text),
            FadeOut(void_field),
            run_time=1
        )
    
    def act_2_quantum_fluctuations(self):
        """Act 2: Quantum fluctuations in the void."""
        # Title
        act_title = Text("Act 2: Quantum Fluctuations", font_size=36, color=YELLOW)
        act_title.to_edge(UP)
        self.play(Write(act_title))
        
        # Create quantum fluctuation field
        fluctuations = VGroup()
        for i in range(50):
            # Random quantum fluctuation
            pos = np.random.uniform(-2, 2, 3)
            fluctuation = Dot3D(pos, color=YELLOW, radius=0.05)
            fluctuation.set_opacity(np.random.uniform(0.3, 0.8))
            fluctuations.add(fluctuation)
        
        # Show fluctuations
        self.play(Create(fluctuations), run_time=2)
        
        # Animate fluctuations
        for i in range(20):
            new_fluctuations = VGroup()
            for j in range(50):
                pos = np.random.uniform(-2, 2, 3)
                fluctuation = Dot3D(pos, color=YELLOW, radius=0.05)
                fluctuation.set_opacity(np.random.uniform(0.3, 0.8))
                new_fluctuations.add(fluctuation)
            
            self.play(Transform(fluctuations, new_fluctuations), run_time=0.2)
        
        # Add quantum equation
        equation = Text("ΔE Δt ≥ ℏ/2", font_size=20, color=WHITE)
        equation.to_corner(UR)
        self.play(Write(equation))
        
        # Transition
        self.play(
            FadeOut(act_title),
            FadeOut(fluctuations),
            FadeOut(equation),
            run_time=1
        )
    
    def act_3_particle_emergence(self):
        """Act 3: Particles emerging from quantum fluctuations."""
        # Title
        act_title = Text("Act 3: Particle Emergence", font_size=36, color=GREEN)
        act_title.to_edge(UP)
        self.play(Write(act_title))
        
        # Create particles
        particles = VGroup()
        particle_trails = VGroup()
        
        # Emerge particles one by one
        for i in range(8):
            # Random emergence position
            pos = np.random.uniform(-2, 2, 3)
            
            # Create particle
            particle = Sphere(radius=0.1, color=GREEN)
            particle.move_to(pos)
            
            # Create trail
            trail = Line3D(pos, pos, color=GREEN, stroke_width=2)
            trail.set_opacity(0.5)
            
            # Show emergence
            self.play(
                Create(particle),
                Flash(particle, color=GREEN),
                run_time=0.5
            )
            
            particles.add(particle)
            particle_trails.add(trail)
        
        # Animate particle movement
        for i in range(50):
            new_particles = VGroup()
            new_trails = VGroup()
            
            for j, particle in enumerate(particles):
                # Random movement
                old_pos = particle.get_center()
                new_pos = old_pos + np.random.uniform(-0.1, 0.1, 3)
                new_pos = np.clip(new_pos, -2, 2)  # Keep in bounds
                
                # Update particle
                new_particle = Sphere(radius=0.1, color=GREEN)
                new_particle.move_to(new_pos)
                new_particles.add(new_particle)
                
                # Update trail
                new_trail = Line3D(old_pos, new_pos, color=GREEN, stroke_width=2)
                new_trail.set_opacity(0.5)
                new_trails.add(new_trail)
            
            self.play(
                Transform(particles, new_particles),
                Transform(particle_trails, new_trails),
                run_time=0.1
            )
        
        # Transition
        self.play(
            FadeOut(act_title),
            run_time=1
        )
    
    def act_4_structure_formation(self):
        """Act 4: Formation of complex structures."""
        # Title
        act_title = Text("Act 4: Structure Formation", font_size=36, color=BLUE)
        act_title.to_edge(UP)
        self.play(Write(act_title))
        
        # Create atomic structures
        atoms = VGroup()
        bonds = VGroup()
        
        # Form atoms
        for i in range(3):
            # Atom center
            center = np.random.uniform(-1.5, 1.5, 3)
            atom = Sphere(radius=0.2, color=BLUE)
            atom.move_to(center)
            atoms.add(atom)
            
            # Electrons orbiting
            for j in range(3):
                electron_pos = center + np.array([0.5, 0, 0])
                electron = Sphere(radius=0.05, color=YELLOW)
                electron.move_to(electron_pos)
                atoms.add(electron)
        
        # Show atom formation
        self.play(Create(atoms), run_time=2)
        
        # Animate electron orbits
        for i in range(30):
            new_atoms = VGroup()
            
            # Keep nuclei
            for j in range(3):
                nucleus = atoms[j]
                new_atoms.add(nucleus)
            
            # Update electron positions
            for j in range(3):
                nucleus_pos = atoms[j].get_center()
                for k in range(3):
                    angle = i * 0.2 + k * 2 * PI / 3
                    electron_pos = nucleus_pos + 0.5 * np.array([
                        np.cos(angle), np.sin(angle), 0
                    ])
                    electron = Sphere(radius=0.05, color=YELLOW)
                    electron.move_to(electron_pos)
                    new_atoms.add(electron)
            
            self.play(Transform(atoms, new_atoms), run_time=0.1)
        
        # Form molecular bonds
        if len(atoms) >= 6:  # If we have at least 2 atoms
            bond = Line3D(
                atoms[0].get_center(),
                atoms[3].get_center(),
                color=RED,
                stroke_width=3
            )
            bonds.add(bond)
            self.play(Create(bond), run_time=1)
        
        # Transition
        self.play(
            FadeOut(act_title),
            run_time=1
        )
    
    def act_5_universe_evolution(self):
        """Act 5: Universe evolution and complexity."""
        # Title
        act_title = Text("Act 5: Universe Evolution", font_size=36, color=PURPLE)
        act_title.to_edge(UP)
        self.play(Write(act_title))
        
        # Create universe structure
        universe = VGroup()
        
        # Add galaxies
        for i in range(5):
            galaxy_center = np.random.uniform(-3, 3, 3)
            galaxy = self.create_galaxy(galaxy_center)
            universe.add(galaxy)
        
        # Show universe
        self.play(Create(universe), run_time=3)
        
        # Animate universe expansion
        self.begin_ambient_camera_rotation(rate=0.05)
        for i in range(40):
            new_universe = VGroup()
            
            for galaxy in universe:
                # Expand galaxy
                new_galaxy = self.create_galaxy(
                    galaxy.get_center(),
                    scale=1 + i * 0.02
                )
                new_universe.add(new_galaxy)
            
            self.play(Transform(universe, new_universe), run_time=0.1)
        
        self.stop_ambient_camera_rotation()
        
        # Add final message
        final_text = Text("From void to complexity\nthrough quantum emergence", 
                         font_size=24, color=WHITE)
        final_text.to_edge(DOWN)
        self.play(Write(final_text), run_time=2)
        
        # Transition
        self.play(
            FadeOut(act_title),
            FadeOut(universe),
            FadeOut(final_text),
            run_time=2
        )
    
    def final_credits(self):
        """Final credits sequence."""
        credits = VGroup(
            Text("Void Physics Life Game", font_size=36, color=WHITE),
            Text("Quantum Mechanics Integration", font_size=24, color=GRAY),
            Text("From Nothing to Everything", font_size=20, color=BLUE),
            Text("Created with Manim", font_size=16, color=GREEN)
        )
        
        credits.arrange(DOWN, buff=0.5)
        credits.move_to(ORIGIN)
        
        # Animate credits
        for credit in credits:
            self.play(Write(credit), run_time=1)
            self.wait(0.5)
        
        self.wait(2)
        
        # Final fade
        self.play(FadeOut(credits), run_time=2)
    
    def create_void_field(self, time=0):
        """Create void field visualization."""
        field = VGroup()
        
        # Create field lines
        for i in range(20):
            start = np.random.uniform(-2, 2, 3)
            end = start + np.random.uniform(-0.5, 0.5, 3)
            
            line = Line3D(start, end, color=WHITE, stroke_width=1)
            line.set_opacity(0.3)
            field.add(line)
        
        return field
    
    def create_galaxy(self, center, scale=1.0):
        """Create a galaxy structure."""
        galaxy = VGroup()
        
        # Galaxy center
        nucleus = Sphere(radius=0.3 * scale, color=YELLOW)
        nucleus.move_to(center)
        galaxy.add(nucleus)
        
        # Spiral arms
        for arm in range(2):
            for i in range(20):
                angle = i * 0.3 + arm * PI
                radius = i * 0.1 * scale
                
                star_pos = center + radius * np.array([
                    np.cos(angle), np.sin(angle), 0
                ])
                
                star = Sphere(radius=0.05 * scale, color=WHITE)
                star.move_to(star_pos)
                galaxy.add(star)
        
        return galaxy


class VoidLifeGameIntro(Scene):
    """
    Introduction scene for the Void Life Game.
    """
    
    def construct(self):
        # Title
        title = Text("Void Physics Life Game", font_size=48, color=WHITE)
        subtitle = Text("Interactive Universe Creation", font_size=24, color=GRAY)
        subtitle.next_to(title, DOWN)
        
        # Description
        description = VGroup(
            Text("• Start from the primordial void", font_size=20, color=WHITE),
            Text("• Tune quantum parameters", font_size=20, color=WHITE),
            Text("• Watch particles emerge", font_size=20, color=WHITE),
            Text("• Build stable structures", font_size=20, color=WHITE),
            Text("• Create your own universe", font_size=20, color=WHITE)
        )
        description.arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        description.next_to(subtitle, DOWN, buff=1)
        
        # Show title
        self.play(Write(title), run_time=2)
        self.play(Write(subtitle), run_time=1)
        
        # Show description
        for item in description:
            self.play(Write(item), run_time=0.5)
        
        self.wait(2)
        
        # Fade out
        self.play(FadeOut(VGroup(title, subtitle, description)), run_time=2)


def main():
    """Main function to run the 3D visualization."""
    import sys
    
    if len(sys.argv) > 1:
        scene_name = sys.argv[1]
        
        if scene_name == "3d":
            scene = VoidLifeGame3D()
        elif scene_name == "intro":
            scene = VoidLifeGameIntro()
        else:
            print("Available scenes: 3d, intro")
            return
        
        scene.render()
    else:
        print("Usage: python void_life_game_3d.py <scene_name>")
        print("Available scenes: 3d, intro")


if __name__ == "__main__":
    main()
