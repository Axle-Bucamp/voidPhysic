#!/usr/bin/env python3
"""
Advanced Void Physics Simulation
================================

This simulation implements the refined void physics model based on:
- Wave function collapse principles
- LYFE game mechanics
- Void particles that behave like a liquid
- Topological connectivity without time/space
- Attraction strength differences between void particles and atoms

Key concepts:
- Void particles spawn smaller than atoms, behave like liquid
- Void particles move to nearest structure and attach, making it age
- Too many void particles blob together to spawn new atoms
- Void particles have much lower attraction strength than atoms
- No time/space in void - acts everywhere simultaneously
- Wave function collapse determines atom properties
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Circle
import seaborn as sns
import pandas as pd
from scipy import ndimage
from scipy.spatial.distance import cdist
import warnings
warnings.filterwarnings('ignore')

# Set up beautiful plotting
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

class VoidParticle:
    """Represents a void particle - smaller than atoms, behaves like liquid."""
    
    def __init__(self, x, y, energy=0.1, age=0):
        self.x = x
        self.y = y
        self.energy = energy
        self.age = age
        self.attraction_strength = 0.01  # Much lower than atoms
        self.liquid_properties = True
        self.attached_to = None  # What it's attached to
        self.velocity = np.array([0.0, 0.0])
        self.blob_id = None  # For grouping with other void particles
        
    def update(self, universe_grid, void_field, dt=1.0):
        """Update void particle based on void physics rules."""
        self.age += dt
        
        # Void particles move toward nearest structure
        nearest_structure = self._find_nearest_structure(universe_grid)
        
        if nearest_structure is not None:
            # Move toward structure
            direction = np.array([nearest_structure.x - self.x, nearest_structure.y - self.y])
            distance = np.linalg.norm(direction)
            
            if distance > 0:
                direction = direction / distance
                # Void particles move slowly due to low attraction
                self.velocity = direction * self.attraction_strength
                self.x += self.velocity[0] * dt
                self.y += self.velocity[1] * dt
                
                # Check if close enough to attach
                if distance < 1.5:
                    self._attach_to_structure(nearest_structure)
        else:
            # No structure nearby - move randomly (liquid behavior)
            self.velocity += np.random.normal(0, 0.01, 2)
            self.velocity = np.clip(self.velocity, -0.1, 0.1)  # Limit speed
            self.x += self.velocity[0] * dt
            self.y += self.velocity[1] * dt
            
        # Check for blob formation with other void particles
        self._check_blob_formation(universe_grid)
        
    def _find_nearest_structure(self, universe_grid):
        """Find the nearest atom or structure."""
        min_distance = float('inf')
        nearest = None
        
        for y in range(universe_grid.shape[0]):
            for x in range(universe_grid.shape[1]):
                cell = universe_grid[y, x]
                if cell is not None and hasattr(cell, 'x'):
                    distance = np.sqrt((cell.x - self.x)**2 + (cell.y - self.y)**2)
                    if distance < min_distance:
                        min_distance = distance
                        nearest = cell
                        
        return nearest
        
    def _attach_to_structure(self, structure):
        """Attach to a structure and make it age."""
        if self.attached_to is None:
            self.attached_to = structure
            # Make structure age faster
            if hasattr(structure, 'aging_rate'):
                structure.aging_rate *= 1.1
            if hasattr(structure, 'energy'):
                structure.energy *= 0.99  # Slight energy drain
                
    def _check_blob_formation(self, universe_grid):
        """Check if void particles should blob together to form new atoms."""
        # This will be handled by the universe class
        pass
        
    def get_color(self):
        """Get color for visualization."""
        # Void particles are dark blue/purple
        intensity = min(1.0, self.energy * 10)
        return (intensity * 0.2, intensity * 0.1, intensity * 0.8)


class AdvancedAtom:
    """Represents an atom with wave function collapse properties."""
    
    def __init__(self, x, y, energy=1.0, age=0, atom_type='matter', wave_function=None):
        self.x = x
        self.y = y
        self.energy = energy
        self.age = age
        self.atom_type = atom_type  # 'matter' or 'antimatter'
        self.stability = 1.0
        self.attraction_strength = 1.0  # Much higher than void particles
        self.aging_rate = 0.01
        self.void_particles_attached = 0
        
        # Wave function properties
        if wave_function is None:
            # Initialize wave function as superposition
            self.wave_function = {
                'matter_probability': 0.5,
                'antimatter_probability': 0.5,
                'position_uncertainty': 0.1,
                'collapsed': False
            }
        else:
            self.wave_function = wave_function
            
    def update(self, universe_grid, void_field, dt=1.0):
        """Update atom based on void physics and wave function collapse."""
        self.age += dt
        
        # Count attached void particles
        self.void_particles_attached = self._count_attached_void_particles(universe_grid)
        
        # Wave function collapse based on void field
        self._wave_function_collapse(void_field)
        
        # Aging from void particles
        if self.void_particles_attached > 0:
            self.aging_rate *= (1 + self.void_particles_attached * 0.1)
            self.energy *= (1 - self.void_particles_attached * 0.01)
            
        # Normal aging
        self.stability -= self.aging_rate * dt
        
        # Check for decay
        if self.stability < 0.1 or self.energy < 0.01:
            self.energy = 0.0  # Atom decays
            
    def _count_attached_void_particles(self, universe_grid):
        """Count void particles attached to this atom."""
        count = 0
        for y in range(universe_grid.shape[0]):
            for x in range(universe_grid.shape[1]):
                cell = universe_grid[y, x]
                if (isinstance(cell, VoidParticle) and 
                    cell.attached_to == self):
                    count += 1
        return count
        
    def _wave_function_collapse(self, void_field):
        """Perform wave function collapse based on void field."""
        if not self.wave_function['collapsed']:
            # Get void field strength at this location
            if (0 <= int(self.y) < void_field.shape[0] and 
                0 <= int(self.x) < void_field.shape[1]):
                void_strength = void_field[int(self.y), int(self.x)]
                
                # Collapse probability based on void field
                collapse_probability = abs(void_strength) * 0.1
                
                if np.random.random() < collapse_probability:
                    # Wave function collapses
                    if void_strength > 0:
                        self.atom_type = 'matter'
                        self.wave_function['matter_probability'] = 1.0
                        self.wave_function['antimatter_probability'] = 0.0
                    else:
                        self.atom_type = 'antimatter'
                        self.wave_function['matter_probability'] = 0.0
                        self.wave_function['antimatter_probability'] = 1.0
                        
                    self.wave_function['collapsed'] = True
                    self.wave_function['position_uncertainty'] = 0.0
                    
    def get_color(self):
        """Get color based on atom type and wave function state."""
        if not self.wave_function['collapsed']:
            # Superposition state - purple
            intensity = min(1.0, self.energy)
            return (intensity * 0.8, intensity * 0.2, intensity * 0.8)
        elif self.atom_type == 'matter':
            # Matter - red
            intensity = min(1.0, self.energy)
            return (intensity, intensity * 0.3, intensity * 0.3)
        else:
            # Antimatter - green
            intensity = min(1.0, self.energy)
            return (intensity * 0.3, intensity, intensity * 0.3)


class VoidFieldGenerator:
    """Generates void field with topological connectivity."""
    
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.time = 0.0
        self.field = np.zeros((height, width))
        self.topological_sources = []
        
    def add_topological_source(self, x, y, strength, frequency):
        """Add a topological source that acts everywhere simultaneously."""
        self.topological_sources.append({
            'x': x, 'y': y, 'strength': strength, 'frequency': frequency
        })
        
    def update(self, dt=1.0):
        """Update void field - acts everywhere simultaneously (no time/space)."""
        self.time += dt
        self.field = np.zeros((self.height, self.width))
        
        # Topological sources act everywhere at once
        for source in self.topological_sources:
            x, y = source['x'], source['y']
            strength = source['strength']
            frequency = source['frequency']
            
            # Create interference pattern that affects entire field
            for i in range(self.height):
                for j in range(self.width):
                    # No distance dependence - topological connectivity
                    phase = 2 * np.pi * frequency * self.time
                    self.field[i, j] += strength * np.sin(phase)
                    
        # Add random void fluctuations
        self.field += np.random.normal(0, 0.05, (self.height, self.width))
        
        # Normalize
        self.field = np.tanh(self.field)


class AdvancedVoidPhysicsSimulation:
    """Advanced void physics simulation with void particles and wave function collapse."""
    
    def __init__(self, width=100, height=100):
        self.width = width
        self.height = height
        self.universe_grid = np.full((height, width), None, dtype=object)
        self.void_field = VoidFieldGenerator(width, height)
        self.time = 0.0
        self.void_particles = []
        self.atoms = []
        self.history = []
        
        # Simulation parameters
        self.void_particle_spawn_rate = 0.05
        self.void_particle_blob_threshold = 5  # Particles needed to form atom
        self.atom_spawn_probability = 0.1
        self.void_particle_lifetime = 100.0
        
        # Statistics
        self.stats = {
            'total_atoms': 0,
            'matter_atoms': 0,
            'antimatter_atoms': 0,
            'superposition_atoms': 0,
            'total_void_particles': 0,
            'total_energy': 0.0,
            'wave_collapse_events': 0,
            'atom_creation_events': 0,
            'void_particle_blobs': 0
        }
        
    def initialize_topological_sources(self, n_sources=6):
        """Initialize topological void sources."""
        for _ in range(n_sources):
            x = np.random.uniform(0, self.width)
            y = np.random.uniform(0, self.height)
            strength = np.random.uniform(0.5, 2.0)
            frequency = np.random.uniform(0.1, 0.8)
            self.void_field.add_topological_source(x, y, strength, frequency)
            
    def create_initial_atoms(self, n_atoms=3):
        """Create initial atoms in superposition states."""
        for _ in range(n_atoms):
            x = np.random.uniform(0, self.width)
            y = np.random.uniform(0, self.height)
            
            # Create atom in superposition state
            atom = AdvancedAtom(x, y, energy=1.0, age=0, atom_type='matter')
            atom.wave_function['collapsed'] = False  # Start in superposition
            
            # Add to universe
            self.universe_grid[int(y), int(x)] = atom
            self.atoms.append(atom)
            
    def update(self, dt=1.0):
        """Update the simulation."""
        self.time += dt
        
        # Update void field (acts everywhere simultaneously)
        self.void_field.update(dt)
        
        # Spawn void particles
        if np.random.random() < self.void_particle_spawn_rate:
            self._spawn_void_particle()
            
        # Update all atoms
        atoms_to_remove = []
        for atom in self.atoms:
            if atom.energy > 0:
                atom.update(self.universe_grid, self.void_field.field, dt)
                
                # Check for decay
                if atom.energy <= 0:
                    atoms_to_remove.append(atom)
                    self.universe_grid[int(atom.y), int(atom.x)] = None
                    
        # Remove decayed atoms
        for atom in atoms_to_remove:
            self.atoms.remove(atom)
            
        # Update void particles
        void_particles_to_remove = []
        for particle in self.void_particles:
            particle.update(self.universe_grid, self.void_field.field, dt)
            
            # Check lifetime
            if particle.age > self.void_particle_lifetime:
                void_particles_to_remove.append(particle)
                
        # Remove old void particles
        for particle in void_particles_to_remove:
            self.void_particles.remove(particle)
            
        # Check for void particle blob formation
        self._check_void_particle_blobs()
        
        # Update statistics
        self._update_statistics()
        
        # Store history
        self.history.append({
            'time': self.time,
            'n_atoms': len(self.atoms),
            'n_void_particles': len(self.void_particles),
            'total_energy': sum(atom.energy for atom in self.atoms),
            'void_activity': np.mean(np.abs(self.void_field.field))
        })
        
    def _spawn_void_particle(self):
        """Spawn a new void particle."""
        # Spawn in areas with high void field activity
        high_activity = self.void_field.field > 0.5
        
        if np.any(high_activity):
            y_coords, x_coords = np.where(high_activity)
            idx = np.random.randint(len(x_coords))
            x, y = x_coords[idx], y_coords[idx]
            
            # Check if location is empty
            if self.universe_grid[y, x] is None:
                particle = VoidParticle(x, y, energy=0.1, age=0)
                self.universe_grid[y, x] = particle
                self.void_particles.append(particle)
                
    def _check_void_particle_blobs(self):
        """Check if void particles should blob together to form atoms."""
        # Group nearby void particles
        if len(self.void_particles) >= self.void_particle_blob_threshold:
            # Simple blob detection - find clusters
            positions = np.array([[p.x, p.y] for p in self.void_particles])
            
            if len(positions) > 0:
                # Use simple clustering
                distances = cdist(positions, positions)
                clusters = []
                used = set()
                
                for i, particle in enumerate(self.void_particles):
                    if i in used:
                        continue
                        
                    cluster = [i]
                    used.add(i)
                    
                    # Find nearby particles
                    for j, other_particle in enumerate(self.void_particles):
                        if j in used:
                            continue
                            
                        if distances[i, j] < 3.0:  # Close enough to blob
                            cluster.append(j)
                            used.add(j)
                            
                    if len(cluster) >= self.void_particle_blob_threshold:
                        clusters.append(cluster)
                        
                # Create atoms from large clusters
                for cluster in clusters:
                    if len(cluster) >= self.void_particle_blob_threshold:
                        self._create_atom_from_blob(cluster)
                        
    def _create_atom_from_blob(self, cluster_indices):
        """Create a new atom from a blob of void particles."""
        # Calculate center position
        positions = [self.void_particles[i] for i in cluster_indices]
        center_x = np.mean([p.x for p in positions])
        center_y = np.mean([p.y for p in positions])
        
        # Create atom in superposition state
        atom = AdvancedAtom(center_x, center_y, energy=1.0, age=0, atom_type='matter')
        atom.wave_function['collapsed'] = False
        
        # Add to universe
        if (0 <= int(center_y) < self.height and 
            0 <= int(center_x) < self.width):
            self.universe_grid[int(center_y), int(center_x)] = atom
            self.atoms.append(atom)
            
        # Remove void particles that formed the atom
        for i in sorted(cluster_indices, reverse=True):
            particle = self.void_particles[i]
            self.universe_grid[int(particle.y), int(particle.x)] = None
            self.void_particles.pop(i)
            
        self.stats['atom_creation_events'] += 1
        self.stats['void_particle_blobs'] += 1
        
    def _update_statistics(self):
        """Update simulation statistics."""
        self.stats['total_atoms'] = len(self.atoms)
        self.stats['total_void_particles'] = len(self.void_particles)
        self.stats['total_energy'] = sum(atom.energy for atom in self.atoms)
        
        # Count atom types
        self.stats['matter_atoms'] = 0
        self.stats['antimatter_atoms'] = 0
        self.stats['superposition_atoms'] = 0
        
        for atom in self.atoms:
            if not atom.wave_function['collapsed']:
                self.stats['superposition_atoms'] += 1
            elif atom.atom_type == 'matter':
                self.stats['matter_atoms'] += 1
            else:
                self.stats['antimatter_atoms'] += 1
                
    def get_universe_image(self):
        """Get image representation of the universe."""
        image = np.zeros((self.height, self.width, 3))
        
        # Draw atoms
        for atom in self.atoms:
            if atom.energy > 0:
                color = np.array(atom.get_color())  # Convert to numpy array
                y, x = int(atom.y), int(atom.x)
                if 0 <= y < self.height and 0 <= x < self.width:
                    image[y, x] = color
                    
        # Draw void particles
        for particle in self.void_particles:
            color = np.array(particle.get_color())  # Convert to numpy array
            y, x = int(particle.y), int(particle.x)
            if 0 <= y < self.height and 0 <= x < self.width:
                # Blend with existing color
                existing = image[y, x]
                image[y, x] = np.clip(existing + color * 0.5, 0, 1)
                
        # Add void field overlay
        void_overlay = np.abs(self.void_field.field)
        void_overlay = np.stack([void_overlay, void_overlay, void_overlay], axis=2)
        image = image + void_overlay * 0.2
        
        return np.clip(image, 0, 1)
        
    def get_void_field_image(self):
        """Get image representation of the void field."""
        field = self.void_field.field
        # Normalize to [0, 1]
        field = (field + 1) / 2
        return field


class AdvancedVoidPhysicsVisualizer:
    """Visualizer for the advanced void physics simulation."""
    
    def __init__(self, simulation):
        self.simulation = simulation
        self.fig = None
        self.axes = None
        
    def create_visualization(self):
        """Create the main visualization."""
        self.fig, self.axes = plt.subplots(2, 2, figsize=(16, 12))
        
        # Universe view
        self.axes[0, 0].set_title('Advanced Void Physics Universe')
        self.axes[0, 0].set_xlabel('X')
        self.axes[0, 0].set_ylabel('Y')
        
        # Void field
        self.axes[0, 1].set_title('Topological Void Field')
        self.axes[0, 1].set_xlabel('X')
        self.axes[0, 1].set_ylabel('Y')
        
        # Statistics
        self.axes[1, 0].set_title('Atom Statistics')
        self.axes[1, 0].set_xlabel('Time')
        self.axes[1, 0].set_ylabel('Count')
        
        # Wave function states
        self.axes[1, 1].set_title('Wave Function States')
        self.axes[1, 1].set_xlabel('Time')
        self.axes[1, 1].set_ylabel('Count')
        
        plt.tight_layout()
        
    def update_visualization(self):
        """Update the visualization."""
        if self.fig is None:
            self.create_visualization()
            
        # Clear axes
        for ax in self.axes.flat:
            ax.clear()
            
        # Universe view
        universe_image = self.simulation.get_universe_image()
        self.axes[0, 0].imshow(universe_image, origin='lower', 
                              extent=[0, self.simulation.width, 0, self.simulation.height])
        self.axes[0, 0].set_title(f'Advanced Void Physics (t={self.simulation.time:.1f})')
        self.axes[0, 0].set_xlabel('X')
        self.axes[0, 0].set_ylabel('Y')
        
        # Void field
        void_image = self.simulation.get_void_field_image()
        im = self.axes[0, 1].imshow(void_image, origin='lower', 
                                   extent=[0, self.simulation.width, 0, self.simulation.height], 
                                   cmap='RdBu_r')
        self.axes[0, 1].set_title('Topological Void Field')
        self.axes[0, 1].set_xlabel('X')
        self.axes[0, 1].set_ylabel('Y')
        plt.colorbar(im, ax=self.axes[0, 1])
        
        # Statistics
        if self.simulation.history:
            history_df = pd.DataFrame(self.simulation.history)
            self.axes[1, 0].plot(history_df['time'], history_df['n_atoms'], 'b-', label='Atoms')
            self.axes[1, 0].plot(history_df['time'], history_df['n_void_particles'], 'r-', label='Void Particles')
            self.axes[1, 0].set_xlabel('Time')
            self.axes[1, 0].set_ylabel('Count')
            self.axes[1, 0].set_title('Particle Statistics')
            self.axes[1, 0].legend()
            self.axes[1, 0].grid(True, alpha=0.3)
            
        # Wave function states
        if self.simulation.history:
            # Calculate wave function states over time
            matter_counts = []
            antimatter_counts = []
            superposition_counts = []
            
            for entry in self.simulation.history:
                # This would need to be tracked in history
                matter_counts.append(self.simulation.stats['matter_atoms'])
                antimatter_counts.append(self.simulation.stats['antimatter_atoms'])
                superposition_counts.append(self.simulation.stats['superposition_atoms'])
                
            times = [entry['time'] for entry in self.simulation.history]
            self.axes[1, 1].plot(times, matter_counts, 'r-', label='Matter')
            self.axes[1, 1].plot(times, antimatter_counts, 'g-', label='Antimatter')
            self.axes[1, 1].plot(times, superposition_counts, 'purple', label='Superposition')
            self.axes[1, 1].set_xlabel('Time')
            self.axes[1, 1].set_ylabel('Count')
            self.axes[1, 1].set_title('Wave Function States')
            self.axes[1, 1].legend()
            self.axes[1, 1].grid(True, alpha=0.3)
            
        plt.tight_layout()
        plt.draw()
        
    def animate(self, n_frames=1000, interval=100):
        """Animate the simulation."""
        # Ensure figure is created
        if self.fig is None:
            self.create_visualization()
            
        def animate_frame(frame):
            self.simulation.update(dt=0.1)
            self.update_visualization()
            return []
            
        anim = animation.FuncAnimation(self.fig, animate_frame, frames=n_frames, 
                                     interval=interval, blit=False, repeat=True)
        return anim


def main():
    """Run the advanced void physics simulation."""
    print("🌌 Starting Advanced Void Physics Simulation...")
    print("Based on wave function collapse, LYFE game, and topological void physics")
    
    # Create simulation
    simulation = AdvancedVoidPhysicsSimulation(width=80, height=80)
    simulation.initialize_topological_sources(n_sources=4)
    simulation.create_initial_atoms(n_atoms=2)
    
    # Create visualizer
    visualizer = AdvancedVoidPhysicsVisualizer(simulation)
    
    # Run animation
    print("🎬 Starting animation...")
    anim = visualizer.animate(n_frames=500, interval=100)
    
    # Save animation
    print("💾 Saving animation...")
    anim.save('examples/advanced_void_physics_animation.gif', writer='pillow', fps=10)
    
    print("✅ Advanced void physics simulation completed!")
    print("Key features implemented:")
    print("- Void particles that behave like liquid")
    print("- Wave function collapse for atoms")
    print("- Topological connectivity (no time/space in void)")
    print("- Void particles blob together to form atoms")
    print("- Much lower attraction strength for void particles")
    print("- Atoms age when void particles attach")


if __name__ == "__main__":
    main()
