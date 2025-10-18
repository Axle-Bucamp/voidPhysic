#!/usr/bin/env python3
"""
Void Physics: Particle Emergence & Evolution Simulation
=======================================================

A 3D particle physics simulation where particles emerge from the void,
form atoms with real physics interactions, create bonds through "lightning" 
energy transmission with exponential decay, and evolve into stable complex 
structures that persist across iterations.

Key principles:
- Void has no spatial representation (no distance, no time)
- Particles emerge from void with 3D coordinates
- Atoms form and interact via simplified real physics (forces, bonds)
- Energy transmits through bonds like "lightning" with exponential decay
- System evolves until stable structures emerge or time limit reached
- Successful stable universes save their seed/parameters for replay
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns
import pandas as pd
from scipy.spatial import cKDTree
from scipy.spatial.distance import pdist, squareform
import networkx as nx
import json
import random
import time
from pathlib import Path
from typing import List, Dict, Tuple, Optional, Any
import warnings
warnings.filterwarnings('ignore')

try:
    import plotly.graph_objects as go
    import plotly.express as px
    from plotly.subplots import make_subplots
    import plotly.dash as dash
    from plotly.dash import dcc, html, Input, Output, State
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False

# Set up beautiful plotting
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# Physical constants
kB = 1.380649e-23  # Boltzmann constant (J/K)
epsilon_0 = 8.854187817e-12  # Vacuum permittivity (F/m)
e = 1.602176634e-19  # Elementary charge (C)


class UniverseConfig:
    """Configuration for universe simulation parameters."""
    
    def __init__(self, seed=None):
        self.seed = seed or random.randint(0, 2**32)
        np.random.seed(self.seed)
        random.seed(self.seed)
        
        # Emergence parameters
        self.start_from_nothing = True
        self.emergence_rate = 0.1
        self.initial_particle_energy = 1.0
        
        # Force constants (Lennard-Jones potential)
        self.force_constants = {
            'epsilon': 1.0,  # Depth of potential well
            'sigma': 1.0,    # Distance at which potential is zero
            'cutoff': 5.0    # Increased cutoff distance for interactions
        }
        
        # Bond decay constants
        self.decay_constants = {
            'alpha': 0.1,    # Bond hop decay
            'beta': 0.01,    # Distance decay
            'min_bond_energy': 0.01
        }
        
        # Simulation parameters
        self.time_limit = 10000
        self.dt = 0.01
        self.stability_threshold = 0.95
        self.min_structure_lifetime = 100
        
        # Entropy parameters
        self.expansion_constant = 0.001
        self.entropy_cutoff = 0.001


class Particle:
    """A fundamental particle that emerges from the void."""
    
    def __init__(self, position: np.ndarray, energy: float = 1.0, 
                 mass: float = 1.0, charge: float = 0.0):
        self.position = np.array(position, dtype=float)  # 3D position
        self.velocity = np.zeros(3, dtype=float)
        self.energy = energy
        self.mass = mass
        self.charge = charge
        self.age = 0
        self.void_interference = 0.0
        self.force = np.zeros(3, dtype=float)
        
    def update_position(self, dt: float):
        """Update position using velocity."""
        self.position += self.velocity * dt
        
    def update_velocity(self, dt: float):
        """Update velocity using force."""
        self.velocity += (self.force / self.mass) * dt
        
    def get_distance_to(self, other: 'Particle') -> float:
        """Calculate distance to another particle."""
        return np.linalg.norm(self.position - other.position)
        
    def get_color(self) -> Tuple[float, float, float]:
        """Get color based on energy level."""
        intensity = min(1.0, self.energy)
        return (intensity, 0.5, 1.0)  # Blue for particles


class Atom:
    """An atom composed of one or more particles with bonds to other atoms."""
    
    def __init__(self, particles: List[Particle]):
        self.particles = particles
        self.bonds = []
        self.age = 0
        self.creation_time = 0
        self.electron_shells = self._calculate_electron_shells()
        self.atomic_number = len(particles)  # Simplified: atomic number = particle count
        self.atomic_radius = self._calculate_atomic_radius()
        self.electronegativity = self._calculate_electronegativity()
        
    def _calculate_electron_shells(self) -> List[float]:
        """Calculate electron shell radii based on quantum mechanics."""
        n_particles = len(self.particles)
        if n_particles == 0:
            return []
        
        shells = []
        # Simplified shell model: 2, 8, 8, 18 electrons per shell
        shell_capacities = [2, 8, 8, 18]
        shell_radii = [1.0, 2.0, 3.0, 4.0]  # Relative radii
        
        electrons_left = n_particles
        for i, capacity in enumerate(shell_capacities):
            if electrons_left <= 0:
                break
            electrons_in_shell = min(electrons_left, capacity)
            shells.append(electrons_in_shell * shell_radii[i])
            electrons_left -= electrons_in_shell
        
        return shells
    
    def _calculate_atomic_radius(self) -> float:
        """Calculate atomic radius based on electron shells and particle density."""
        if not self.electron_shells:
            return 0.5
        
        # Atomic radius is roughly the outermost electron shell
        max_shell = max(self.electron_shells) if self.electron_shells else 0.5
        return max_shell * 0.3  # Scale factor
    
    def _calculate_electronegativity(self) -> float:
        """Calculate electronegativity based on atomic structure."""
        # Simplified Pauling electronegativity scale
        # Higher atomic number and more electrons = higher electronegativity
        base_electronegativity = 0.5 + (self.atomic_number * 0.1)
        return min(4.0, base_electronegativity)
    
    @property
    def position(self) -> np.ndarray:
        """Center of mass position."""
        if not self.particles:
            return np.zeros(3)
        total_mass = sum(p.mass for p in self.particles)
        if total_mass == 0:
            return self.particles[0].position if self.particles else np.zeros(3)
        return sum(p.position * p.mass for p in self.particles) / total_mass
    
    @property
    def energy(self) -> float:
        """Total energy of atom including binding energy."""
        particle_energy = sum(p.energy for p in self.particles)
        # Add binding energy (negative, makes atom more stable)
        binding_energy = -0.1 * len(self.particles)  # More particles = more binding
        return particle_energy + binding_energy
    
    @property
    def mass(self) -> float:
        """Total mass of atom."""
        return sum(p.mass for p in self.particles)
    
    @property
    def volume(self) -> float:
        """Calculate atomic volume based on electron shells."""
        if not self.electron_shells:
            return (4/3) * np.pi * (0.5**3)
        
        # Volume of outermost shell
        outer_radius = max(self.electron_shells) * 0.3
        return (4/3) * np.pi * (outer_radius**3)
    
    @property
    def density(self) -> float:
        """Calculate atomic density."""
        if self.volume > 0:
            return self.mass / self.volume
        return 0.0
    
    def distance_to(self, other: 'Atom') -> float:
        """Distance to another atom."""
        return np.linalg.norm(self.position - other.position)
    
    def can_bond_with(self, other: 'Atom', config: UniverseConfig) -> bool:
        """Check if atom can form bond with another atom using quantum mechanics."""
        distance = self.distance_to(other)
        
        # Use Lennard-Jones potential to determine bonding
        epsilon = config.force_constants['epsilon']
        sigma = config.force_constants['sigma']
        
        # Quantum mechanical bonding criteria:
        # 1. Energy threshold based on electronegativity difference
        electronegativity_diff = abs(self.electronegativity - other.electronegativity)
        energy_threshold = epsilon * 0.1  # Reduced threshold for easier bonding
        
        # 2. Distance threshold based on atomic radii (more generous)
        bonding_distance = (self.atomic_radius + other.atomic_radius) * 3.0  # Increased from 2.0
        
        # 3. Valence electron availability (simplified)
        valence_electrons = min(len(self.particles), 8)  # Max 8 valence electrons
        
        # 4. Lennard-Jones potential check (bonding occurs near energy minimum)
        if distance > 0:
            # Use simplified LJ potential calculation
            term1 = (sigma / distance) ** 12
            term2 = (sigma / distance) ** 6
            lj_potential = 4 * epsilon * (term1 - term2)
            # Bonding is favorable when potential is negative (attractive)
            lj_favorable = lj_potential < 0.1  # Close to energy minimum
        else:
            lj_favorable = False
        
        return (self.energy > energy_threshold and 
                other.energy > energy_threshold and
                distance < bonding_distance and
                distance > (self.atomic_radius + other.atomic_radius) * 0.5 and  # Avoid overlap
                valence_electrons > 0 and
                lj_favorable)
    
    def form_bond(self, other: 'Atom', config: UniverseConfig) -> 'Bond':
        """Form a bond with another atom."""
        bond = Bond(self, other, config)
        self.bonds.append(bond)
        other.bonds.append(bond)
        
        # Update atomic properties due to bonding
        self._update_bonding_properties(bond)
        other._update_bonding_properties(bond)
        
        return bond
    
    def _update_bonding_properties(self, bond: 'Bond') -> None:
        """Update atomic properties due to bonding."""
        # Bonding can affect electron distribution
        # This is a simplified model
        if len(self.bonds) > 0:
            # More bonds = more stable = slightly higher binding energy
            bond_stabilization = 0.01 * len(self.bonds)
            # This could be implemented as a small energy adjustment
    
    def get_color(self) -> Tuple[float, float, float]:
        """Get color based on atomic properties."""
        # Color based on atomic number and energy state
        atomic_color = self._get_atomic_color()
        
        # Energy intensity affects brightness
        energy_intensity = min(1.0, max(0.2, self.energy / 10.0))
        
        # Bond count affects saturation
        bond_factor = min(1.0, len(self.bonds) / 4.0)
        
        # Combine factors
        r, g, b = atomic_color
        return (
            min(1.0, r * energy_intensity),
            min(1.0, g * energy_intensity * (0.5 + 0.5 * bond_factor)),
            min(1.0, b * energy_intensity)
        )
    
    def _get_atomic_color(self) -> Tuple[float, float, float]:
        """Get base color based on atomic number (periodic table inspired)."""
        # Simplified periodic table colors
        colors = {
            1: (1.0, 1.0, 1.0),    # Hydrogen - white
            2: (0.8, 0.8, 1.0),    # Helium - light blue
            3: (0.8, 0.5, 1.0),    # Lithium - light purple
            4: (0.5, 0.8, 0.5),    # Beryllium - light green
            5: (1.0, 0.8, 0.8),    # Boron - light pink
            6: (0.3, 0.3, 0.3),    # Carbon - dark gray
            7: (0.3, 0.3, 0.8),    # Nitrogen - blue
            8: (1.0, 0.3, 0.3),    # Oxygen - red
            9: (0.5, 0.8, 0.5),    # Fluorine - green
            10: (0.8, 0.8, 0.8),   # Neon - light gray
        }
        
        # Get color based on atomic number, with fallback
        base_color = colors.get(self.atomic_number, (0.5, 0.5, 0.5))
        
        # Adjust based on electronegativity (higher = more blue)
        electronegativity_factor = self.electronegativity / 4.0
        r, g, b = base_color
        b = min(1.0, b + electronegativity_factor * 0.3)
        r = max(0.2, r - electronegativity_factor * 0.2)
        
        return (r, g, b)
    
    def get_size(self) -> float:
        """Get visual size for rendering."""
        return max(0.5, min(3.0, self.atomic_radius * 2.0))


class Bond:
    """A bond between two atoms that transmits energy with quantum mechanical properties."""
    
    def __init__(self, atom1: Atom, atom2: Atom, config: UniverseConfig):
        self.atom1 = atom1
        self.atom2 = atom2
        self.distance = atom1.distance_to(atom2)
        self.energy_capacity = min(atom1.energy, atom2.energy) * 0.1
        self.age = 0
        self.creation_time = 0
        self.config = config
        
        # Quantum mechanical bond properties
        self.bond_type = self._determine_bond_type()
        self.bond_order = self._calculate_bond_order()
        self.bond_angle = 0.0  # Will be calculated based on other bonds
        self.resonance_frequency = self._calculate_resonance_frequency()
        
    def _determine_bond_type(self) -> str:
        """Determine bond type based on electronegativity difference."""
        electronegativity_diff = abs(self.atom1.electronegativity - self.atom2.electronegativity)
        
        if electronegativity_diff < 0.5:
            return "covalent"
        elif electronegativity_diff < 1.7:
            return "polar_covalent"
        else:
            return "ionic"
    
    def _calculate_bond_order(self) -> float:
        """Calculate bond order (single, double, triple bond)."""
        # Simplified: based on energy capacity and distance
        optimal_distance = (self.atom1.atomic_radius + self.atom2.atomic_radius) * 1.5
        
        # Bond order increases with energy and decreases with distance
        energy_factor = self.energy_capacity / 2.0
        distance_factor = max(0.1, optimal_distance / self.distance)
        
        bond_order = energy_factor * distance_factor
        return min(3.0, max(0.5, bond_order))  # Between single and triple bond
    
    def _calculate_resonance_frequency(self) -> float:
        """Calculate bond resonance frequency for energy transmission."""
        # Based on bond strength and atomic masses
        reduced_mass = (self.atom1.mass * self.atom2.mass) / (self.atom1.mass + self.atom2.mass)
        bond_strength = self.energy_capacity
        
        if reduced_mass > 0 and bond_strength > 0:
            # Simple harmonic oscillator: ω = sqrt(k/m)
            # k is bond strength, m is reduced mass
            frequency = np.sqrt(bond_strength / reduced_mass)
            return frequency
        return 1.0
    
    def transmit_energy(self, energy: float, num_hops: int, 
                       cumulative_distance: float) -> float:
        """Transmit energy through bond with quantum mechanical decay."""
        alpha = self.config.decay_constants['alpha']
        beta = self.config.decay_constants['beta']
        
        # Base exponential decay
        decay_factor = np.exp(-alpha * num_hops) * np.exp(-beta * cumulative_distance)
        
        # Quantum mechanical corrections:
        # 1. Bond type affects transmission efficiency
        bond_efficiency = {
            "covalent": 0.9,
            "polar_covalent": 0.7,
            "ionic": 0.5
        }
        efficiency = bond_efficiency.get(self.bond_type, 0.6)
        
        # 2. Bond order affects transmission (higher order = better transmission)
        order_factor = min(1.0, self.bond_order / 2.0)
        
        # 3. Resonance frequency affects transmission (resonant frequencies transmit better)
        frequency_factor = 1.0 / (1.0 + abs(self.resonance_frequency - 1.0))
        
        # Combine all factors
        total_decay = decay_factor * efficiency * order_factor * frequency_factor
        transmitted = energy * total_decay
        
        # Update bond energy capacity
        self.energy_capacity += transmitted * 0.05  # Some energy stored in bond
        
        return transmitted
    
    def is_stable(self) -> bool:
        """Check if bond is stable using quantum mechanical criteria."""
        min_energy = self.config.decay_constants['min_bond_energy']
        
        # Bond stability depends on multiple factors:
        # 1. Energy threshold
        energy_stable = self.energy_capacity > min_energy
        
        # 2. Distance stability (bonds too long or too short are unstable)
        optimal_distance = (self.atom1.atomic_radius + self.atom2.atomic_radius) * 1.5
        distance_ratio = self.distance / optimal_distance
        distance_stable = 0.8 < distance_ratio < 2.0
        
        # 3. Bond type stability (more lenient)
        bond_stability = {
            "covalent": 0.05,
            "polar_covalent": 0.03,
            "ionic": 0.02
        }
        type_stability = bond_stability.get(self.bond_type, 0.05)
        
        return energy_stable and distance_stable and (self.energy_capacity > type_stability)
    
    def get_color(self) -> Tuple[float, float, float]:
        """Get color based on bond type and strength."""
        base_colors = {
            "covalent": (0.8, 0.8, 0.8),      # Gray for covalent
            "polar_covalent": (0.6, 0.8, 1.0), # Light blue for polar covalent
            "ionic": (1.0, 0.8, 0.6)          # Light orange for ionic
        }
        
        base_color = base_colors.get(self.bond_type, (0.7, 0.7, 0.7))
        
        # Intensity based on bond strength and order
        strength_intensity = min(1.0, self.energy_capacity / 3.0)
        order_intensity = min(1.0, self.bond_order / 3.0)
        
        # Combine intensities
        intensity = (strength_intensity + order_intensity) / 2.0
        
        # Apply intensity to base color
        r, g, b = base_color
        return (
            min(1.0, r * intensity),
            min(1.0, g * intensity),
            min(1.0, b * intensity)
        )
    
    def get_width(self) -> float:
        """Get line width for rendering based on bond order."""
        return max(1.0, min(5.0, self.bond_order * 2.0))
    
    def get_opacity(self) -> float:
        """Get opacity based on bond strength."""
        return min(1.0, max(0.3, self.energy_capacity / 2.0))


class PhysicsEngine:
    """Handles force calculations and physics updates."""
    
    def __init__(self, config: UniverseConfig):
        self.config = config
        
    def lennard_jones_potential(self, r: float) -> float:
        """Calculate Lennard-Jones potential."""
        epsilon = self.config.force_constants['epsilon']
        sigma = self.config.force_constants['sigma']
        
        if r == 0:
            return float('inf')
        
        term1 = (sigma / r) ** 12
        term2 = (sigma / r) ** 6
        return 4 * epsilon * (term1 - term2)
    
    def lennard_jones_force(self, r: float) -> float:
        """Calculate Lennard-Jones force magnitude."""
        epsilon = self.config.force_constants['epsilon']
        sigma = self.config.force_constants['sigma']
        
        if r == 0:
            return 0.0
        
        # F(r) = -dV/dr = 24*epsilon * (2*(sigma/r)^13 - (sigma/r)^7) / r
        term1 = 2 * (sigma / r) ** 13
        term2 = (sigma / r) ** 7
        return 24 * epsilon * (term1 - term2) / r
    
    def calculate_forces(self, particles: List[Particle]) -> None:
        """Calculate forces between all particles."""
        n = len(particles)
        
        # Reset forces
        for particle in particles:
            particle.force.fill(0.0)
        
        # Calculate pairwise forces
        for i in range(n):
            for j in range(i + 1, n):
                p1, p2 = particles[i], particles[j]
                r_vec = p2.position - p1.position
                r = np.linalg.norm(r_vec)
                
                if r < self.config.force_constants['cutoff'] and r > 0:
                    force_mag = self.lennard_jones_force(r)
                    force_vec = force_mag * (r_vec / r)
                    
                    # Apply forces (Newton's third law)
                    p1.force += force_vec
                    p2.force -= force_vec
    
    def update_particles(self, particles: List[Particle], dt: float) -> None:
        """Update particle positions and velocities."""
        self.calculate_forces(particles)
        
        for particle in particles:
            particle.update_velocity(dt)
            particle.update_position(dt)
            particle.age += 1


class VoidEmergence:
    """Handles particle emergence from the void."""
    
    def __init__(self, config: UniverseConfig):
        self.config = config
        self.iteration = 0
        
    def should_emerge_particle(self, universe: 'Universe') -> bool:
        """Determine if a new particle should emerge."""
        self.iteration += 1
        
        # First particle always emerges
        if len(universe.particles) == 0:
            return True
        
        # Calculate emergence probability
        void_strength = self._calculate_void_strength(universe)
        matter_density = self._calculate_matter_density(universe)
        
        # Lower probability near stable structures
        emergence_prob = (self.config.emergence_rate * void_strength * 
                         (1 - matter_density))
        
        return np.random.random() < emergence_prob
    
    def create_particle(self, universe: 'Universe') -> Particle:
        """Create a new particle."""
        if len(universe.particles) == 0:
            # First particle at origin
            position = np.zeros(3)
        else:
            # Emerge near existing particles but avoid dense regions
            position = self._find_emergence_location(universe)
        
        energy = self.config.initial_particle_energy
        particle = Particle(position, energy)
        
        # Add some randomness to initial energy
        particle.energy *= np.random.uniform(0.8, 1.2)
        
        return particle
    
    def _calculate_void_strength(self, universe: 'Universe') -> float:
        """Calculate current void field strength."""
        # Simple model: void strength decreases as universe gets more complex
        complexity = len(universe.atoms) + len(universe.bonds)
        return max(0.1, 1.0 / (1.0 + complexity * 0.01))
    
    def _calculate_matter_density(self, universe: 'Universe') -> float:
        """Calculate local matter density around potential emergence points."""
        if len(universe.particles) == 0:
            return 0.0
        
        # Use spatial distribution to estimate density
        positions = np.array([p.position for p in universe.particles])
        
        if len(positions) < 2:
            return 0.0
        
        # Calculate average nearest neighbor distance
        tree = cKDTree(positions)
        distances, _ = tree.query(positions, k=min(4, len(positions)))
        avg_distance = np.mean(distances[:, 1:])  # Exclude self-distance
        
        # Convert to density (closer particles = higher density)
        density = 1.0 / (1.0 + avg_distance)
        return min(1.0, density)
    
    def _find_emergence_location(self, universe: 'Universe') -> np.ndarray:
        """Find location for new particle emergence."""
        if len(universe.particles) == 0:
            return np.zeros(3)
        
        # Try to emerge near existing particles but not too close
        existing_positions = np.array([p.position for p in universe.particles])
        
        # Find areas with moderate particle density
        tree = cKDTree(existing_positions)
        
        # Sample potential locations
        best_position = None
        best_score = float('inf')
        
        for _ in range(10):  # Try 10 random locations
            # Pick a random existing particle as reference
            ref_particle = np.random.choice(universe.particles)
            
            # Generate position near reference but not too close
            # Reduced offset to encourage bonding
            offset = np.random.normal(0, 1.0, 3)  # Reduced from 2.0 to 1.0
            candidate_pos = ref_particle.position + offset
            
            # Calculate distance to nearest existing particle
            distances, _ = tree.query(candidate_pos, k=1)
            
            # Score based on distance (not too close, not too far)
            # Target distance should be within bonding range
            target_distance = 1.5  # Within bonding range for atomic radius ~0.3
            score = abs(distances - target_distance)
            
            if score < best_score:
                best_score = score
                best_position = candidate_pos
        
        return best_position if best_position is not None else np.zeros(3)


class EntropyTracker:
    """Tracks entropy evolution and universe expansion with local vs total energy analysis."""
    
    def __init__(self, config: UniverseConfig):
        self.config = config
        self.entropy_history = []
        self.expansion_rate = 0.0
        self.local_energy_history = []
        self.total_energy_history = []
        
    def calculate_local_energy(self, universe: 'Universe') -> Dict[str, float]:
        """Calculate local energy distributions for entropy computation."""
        local_energies = {
            'kinetic': 0.0,
            'potential': 0.0,
            'bond': 0.0,
            'void_interference': 0.0
        }
        
        # Kinetic energy from particle velocities
        for particle in universe.particles:
            kinetic = 0.5 * particle.mass * np.linalg.norm(particle.velocity)**2
            local_energies['kinetic'] += kinetic
        
        # Potential energy from Lennard-Jones interactions
        n = len(universe.particles)
        for i in range(n):
            for j in range(i + 1, n):
                p1, p2 = universe.particles[i], universe.particles[j]
                r = p1.get_distance_to(p2)
                if r > 0 and r < universe.config.force_constants['cutoff']:
                    potential = universe.physics_engine.lennard_jones_potential(r)
                    local_energies['potential'] += potential
        
        # Bond energy (stored in bonds)
        for bond in universe.bonds:
            local_energies['bond'] += bond.energy_capacity
        
        # Void interference energy
        for particle in universe.particles:
            local_energies['void_interference'] += particle.void_interference * particle.energy
        
        return local_energies
    
    def calculate_total_energy(self, universe: 'Universe') -> float:
        """Calculate total energy including all forms."""
        local_energies = self.calculate_local_energy(universe)
        return sum(local_energies.values())
    
    def calculate_entropy(self, universe: 'Universe') -> float:
        """Calculate entropy using local energy distributions and statistical mechanics."""
        n_particles = len(universe.particles)
        n_atoms = len(universe.atoms)
        n_bonds = len(universe.bonds)
        
        if n_particles == 0:
            return 0.0

        # Get energy distributions
        local_energies = self.calculate_local_energy(universe)
        total_energy = self.calculate_total_energy(universe)
        
        # Store for history
        self.local_energy_history.append(local_energies.copy())
        self.total_energy_history.append(total_energy)
        
        # Calculate universe volume/area for energy density
        universe_volume = self._calculate_universe_volume(universe)
        universe_area = self._calculate_universe_area(universe)
        
        # Calculate local energy density (energy per unit area)
        local_energy_density = {}
        for energy_type, energy_value in local_energies.items():
            if universe_area > 0:
                local_energy_density[energy_type] = energy_value / universe_area
            else:
                local_energy_density[energy_type] = 0.0
        
        # Store energy density for analysis
        if not hasattr(self, 'energy_density_history'):
            self.energy_density_history = []
        self.energy_density_history.append(local_energy_density.copy())
        
        # Boltzmann entropy: S = k_B * ln(Ω)
        # Ω = number of microstates
        
        # 1. Positional entropy (spatial distribution)
        if n_particles > 1:
            positions = np.array([p.position for p in universe.particles])
            # Calculate volume occupied by particles
            if len(positions) > 1:
                # Use convex hull volume as a measure of spatial distribution
                try:
                    from scipy.spatial import ConvexHull
                    hull = ConvexHull(positions)
                    volume = hull.volume
                    if volume > 0:
                        # Entropy proportional to log of accessible volume
                        position_entropy = kB * np.log(volume + 1.0)
                    else:
                        position_entropy = kB * np.log(n_particles)
                except:
                    # Fallback: entropy based on particle spread
                    distances = pdist(positions)
                    avg_distance = np.mean(distances) if len(distances) > 0 else 1.0
                    position_entropy = kB * np.log(avg_distance * n_particles + 1.0)
            else:
                position_entropy = kB * np.log(2.0)  # Minimal entropy for single particle
        else:
            position_entropy = 0.0
        
        # 2. Energy entropy (distribution of energy among different forms)
        if total_energy > 0:
            # Calculate energy distribution entropy
            energy_fractions = []
            for energy_type, energy_value in local_energies.items():
                if energy_value > 0:
                    fraction = energy_value / total_energy
                    if fraction > 0:
                        energy_fractions.append(fraction)
            
            if energy_fractions:
                # Shannon entropy of energy distribution
                energy_entropy = -kB * sum(f * np.log(f) for f in energy_fractions if f > 0)
            else:
                energy_entropy = 0.0
        else:
            energy_entropy = 0.0
        
        # 3. Configurational entropy (atomic and bond arrangements)
        config_entropy = 0.0
        if n_atoms > 0:
            # Entropy from atomic configurations
            config_entropy += kB * np.log(n_atoms + 1)
        
        if n_bonds > 0:
            # Entropy from bond network topology
            # More bonds = more possible arrangements
            config_entropy += kB * np.log(n_bonds + 1)
        
        # 4. Temperature-based entropy (if we can estimate temperature)
        temperature = self._estimate_temperature(universe, local_energies['kinetic'])
        if temperature > 0:
            # S = C * ln(T) where C is a constant
            thermal_entropy = kB * np.log(temperature + 1.0)
        else:
            thermal_entropy = 0.0
        
        # 5. Energy density entropy (local vs total energy distribution)
        if universe_area > 0 and total_energy > 0:
            # Calculate how energy is distributed across space
            total_energy_density = total_energy / universe_area
            density_entropy = 0.0
            
            # Entropy from energy density variations
            for energy_type, density in local_energy_density.items():
                if density > 0 and total_energy_density > 0:
                    density_ratio = density / total_energy_density
                    if density_ratio > 0:
                        density_entropy += -kB * density_ratio * np.log(density_ratio)
        else:
            density_entropy = 0.0
        
        total_entropy = position_entropy + energy_entropy + config_entropy + thermal_entropy + density_entropy
        
        return total_entropy
    
    def _calculate_universe_volume(self, universe: 'Universe') -> float:
        """Calculate the volume occupied by the universe."""
        if len(universe.particles) < 2:
            return 0.0
        
        positions = np.array([p.position for p in universe.particles])
        try:
            from scipy.spatial import ConvexHull
            hull = ConvexHull(positions)
            return hull.volume
        except:
            # Fallback: bounding box volume
            min_pos = np.min(positions, axis=0)
            max_pos = np.max(positions, axis=0)
            return np.prod(max_pos - min_pos)
    
    def _calculate_universe_area(self, universe: 'Universe') -> float:
        """Calculate the surface area of the universe."""
        if len(universe.particles) < 3:
            return 0.0
        
        positions = np.array([p.position for p in universe.particles])
        try:
            from scipy.spatial import ConvexHull
            hull = ConvexHull(positions)
            return hull.area
        except:
            # Fallback: bounding box surface area
            min_pos = np.min(positions, axis=0)
            max_pos = np.max(positions, axis=0)
            dims = max_pos - min_pos
            return 2 * (dims[0]*dims[1] + dims[1]*dims[2] + dims[0]*dims[2])
    
    def _estimate_temperature(self, universe: 'Universe', kinetic_energy: float) -> float:
        """Estimate temperature from kinetic energy using equipartition theorem."""
        n_particles = len(universe.particles)
        if n_particles == 0:
            return 0.0
        
        # Equipartition: KE = (3/2) * n * k_B * T for 3D system
        # T = (2 * KE) / (3 * n * k_B)
        degrees_of_freedom = 3 * n_particles  # 3D system
        if degrees_of_freedom > 0:
            temperature = (2 * kinetic_energy) / (degrees_of_freedom * kB)
            return max(0.0, temperature)
        return 0.0
    
    def update_expansion_rate(self, entropy_rate: float) -> None:
        """Update universe expansion rate based on entropy change."""
        self.expansion_rate = self.config.expansion_constant * abs(entropy_rate)
    
    def expand_universe(self, universe: 'Universe') -> None:
        """Expand universe space based on entropy."""
        if self.expansion_rate < self.config.entropy_cutoff:
            return
        
        # Slightly expand distances between particles
        expansion_factor = 1.0 + self.expansion_rate * self.config.dt
        
        for particle in universe.particles:
            # Expand from center of mass
            center = universe.get_center_of_mass()
            direction = particle.position - center
            particle.position = center + direction * expansion_factor


class StabilityAnalyzer:
    """Analyzes universe stability and persistent structures."""
    
    def __init__(self, config: UniverseConfig):
        self.config = config
        self.stable_structures = []
        self.structure_history = {}
        
    def identify_stable_structures(self, universe: 'Universe') -> List[Atom]:
        """Identify stable atomic structures."""
        stable_structures = []
        
        for atom in universe.atoms:
            # Check if atom is stable (lived long enough)
            if atom.age > self.config.min_structure_lifetime:
                # Check if atom has energy equilibrium
                if self._is_energy_balanced(atom):
                    stable_structures.append(atom)
        
        # Update stable structures list
        self.stable_structures = stable_structures
        return stable_structures
    
    def _is_energy_balanced(self, atom: Atom) -> bool:
        """Check if atom has energy equilibrium."""
        # Simple energy balance: energy input ≈ energy output
        total_bond_energy = sum(bond.energy_capacity for bond in atom.bonds)
        energy_ratio = total_bond_energy / (atom.energy + 1e-10)
        
        # Balanced if energy ratio is within reasonable range
        return 0.1 < energy_ratio < 2.0
    
    def is_universe_stable(self, universe: 'Universe') -> bool:
        """Check if universe has reached stability."""
        stable_mass = sum(atom.mass for atom in self.stable_structures)
        total_mass = universe.total_mass
        
        if total_mass == 0:
            return False
        
        stability_ratio = stable_mass / total_mass
        return stability_ratio > self.config.stability_threshold


class UniverseArchive:
    """Handles saving and loading universe configurations."""
    
    def __init__(self, archive_dir: str = "universes"):
        self.archive_dir = Path(archive_dir)
        self.archive_dir.mkdir(exist_ok=True)
    
    def save_universe(self, universe: 'Universe', config: UniverseConfig) -> None:
        """Save universe state and configuration."""
        archive_data = {
            'seed': config.seed,
            'parameters': {
                'emergence_rate': config.emergence_rate,
                'force_constants': config.force_constants,
                'decay_constants': config.decay_constants,
                'time_limit': config.time_limit,
                'stability_threshold': config.stability_threshold
            },
            'final_state': {
                'iteration': universe.iteration,
                'total_energy': universe.total_energy,
                'total_mass': universe.total_mass,
                'particle_count': len(universe.particles),
                'atom_count': len(universe.atoms),
                'bond_count': len(universe.bonds),
                'entropy': universe.entropy_tracker.calculate_entropy(universe)
            },
            'stable_structures': [
                {
                    'position': atom.position.tolist(),
                    'energy': atom.energy,
                    'mass': atom.mass,
                    'age': atom.age,
                    'bond_count': len(atom.bonds)
                }
                for atom in universe.stability_analyzer.stable_structures
            ],
            'timestamp': time.time()
        }
        
        filename = self.archive_dir / f"universe_{config.seed}.json"
        with open(filename, 'w') as f:
            json.dump(archive_data, f, indent=2)
        
        print(f"Saved universe to {filename}")
    
    def load_universe(self, seed: int) -> Dict[str, Any]:
        """Load universe configuration."""
        filename = self.archive_dir / f"universe_{seed}.json"
        if filename.exists():
            with open(filename, 'r') as f:
                return json.load(f)
        else:
            raise FileNotFoundError(f"Universe {seed} not found")


class Universe:
    """Main universe simulation class."""
    
    def __init__(self, config: UniverseConfig):
        self.config = config
        self.iteration = 0
        
        # Physics components
        self.particles: List[Particle] = []
        self.atoms: List[Atom] = []
        self.bonds: List[Bond] = []
        
        # Physics engines
        self.physics_engine = PhysicsEngine(config)
        self.void_emergence = VoidEmergence(config)
        self.entropy_tracker = EntropyTracker(config)
        self.stability_analyzer = StabilityAnalyzer(config)
        self.archive = UniverseArchive()
        
        # History tracking
        self.history = []
        
    @property
    def total_energy(self) -> float:
        """Total energy in universe using enhanced entropy tracker."""
        return self.entropy_tracker.calculate_total_energy(self)
    
    @property
    def total_mass(self) -> float:
        """Total mass in universe."""
        return sum(p.mass for p in self.particles)
    
    def get_center_of_mass(self) -> np.ndarray:
        """Calculate center of mass."""
        if not self.particles:
            return np.zeros(3)
        
        total_mass = self.total_mass
        if total_mass == 0:
            return self.particles[0].position
        
        return sum(p.position * p.mass for p in self.particles) / total_mass
    
    def add_particle(self, particle: Particle) -> None:
        """Add particle to universe."""
        self.particles.append(particle)
    
    def create_atom(self, particles: List[Particle]) -> Atom:
        """Create atom from particles."""
        atom = Atom(particles)
        atom.creation_time = self.iteration
        self.atoms.append(atom)
        return atom
    
    def check_bond_formation(self) -> None:
        """Check for new bond formation between atoms."""
        bonds_formed = 0
        for i, atom1 in enumerate(self.atoms):
            for j, atom2 in enumerate(self.atoms[i+1:], i+1):
                if (atom1.can_bond_with(atom2, self.config) and 
                    not self._atoms_already_bonded(atom1, atom2)):
                    bond = atom1.form_bond(atom2, self.config)
                    bond.creation_time = self.iteration
                    self.bonds.append(bond)
                    bonds_formed += 1
        
        if bonds_formed > 0:
            pass  # Bonds formed successfully
    
    def check_bond_breaking(self) -> None:
        """Check for bond breaking due to instability."""
        bonds_to_remove = []
        
        for bond in self.bonds:
            if not bond.is_stable():
                bonds_to_remove.append(bond)
        
        # Remove unstable bonds
        bonds_broken = 0
        for bond in bonds_to_remove:
            self.bonds.remove(bond)
            if bond in bond.atom1.bonds:
                bond.atom1.bonds.remove(bond)
            if bond in bond.atom2.bonds:
                bond.atom2.bonds.remove(bond)
            bonds_broken += 1
        
        if bonds_broken > 0:
            pass  # Bonds broken due to instability
    
    def transmit_energy_through_bonds(self) -> None:
        """Transmit energy through bond network."""
        for bond in self.bonds:
            if bond.energy_capacity > self.config.decay_constants['min_bond_energy']:
                # Transmit energy between bonded atoms
                energy_to_transmit = bond.energy_capacity * 0.1
                
                # Calculate transmission parameters
                num_hops = 1  # Direct bond
                cumulative_distance = bond.distance
                
                transmitted = bond.transmit_energy(
                    energy_to_transmit, num_hops, cumulative_distance)
                
                # Distribute transmitted energy
                bond.atom1.particles[0].energy += transmitted * 0.5
                bond.atom2.particles[0].energy += transmitted * 0.5
    
    def update_entropy(self) -> None:
        """Update entropy and expansion."""
        current_entropy = self.entropy_tracker.calculate_entropy(self)
        self.entropy_tracker.entropy_history.append(current_entropy)
        
        # Calculate entropy rate
        if len(self.entropy_tracker.entropy_history) > 1:
            entropy_rate = (current_entropy - 
                          self.entropy_tracker.entropy_history[-2])
            self.entropy_tracker.update_expansion_rate(entropy_rate)
            self.entropy_tracker.expand_universe(self)
    
    def update(self, dt: float = None) -> None:
        """Update universe state."""
        if dt is None:
            dt = self.config.dt
        
        self.iteration += 1
        
        # 1. Void emergence
        if self.void_emergence.should_emerge_particle(self):
            particle = self.void_emergence.create_particle(self)
            self.add_particle(particle)
            
            # Create atom from new particle
            atom = self.create_atom([particle])
        
        # 2. Physics update
        if self.particles:
            self.physics_engine.update_particles(self.particles, dt)
        
        # 3. Bonding
        self.check_bond_formation()
        self.check_bond_breaking()
        
        # 4. Energy transmission
        self.transmit_energy_through_bonds()
        
        # 5. Entropy & expansion
        self.update_entropy()
        
        # 6. Stability analysis
        self.stability_analyzer.identify_stable_structures(self)
        
        # 7. Store history
        if self.iteration % 10 == 0:  # Store every 10 iterations
            self.history.append({
                'iteration': self.iteration,
                'particle_count': len(self.particles),
                'atom_count': len(self.atoms),
                'bond_count': len(self.bonds),
                'total_energy': self.total_energy,
                'entropy': self.entropy_tracker.calculate_entropy(self),
                'stable_structures': len(self.stability_analyzer.stable_structures)
            })
    
    def is_stable(self) -> bool:
        """Check if universe has reached stability."""
        return self.stability_analyzer.is_universe_stable(self)
    
    def _atoms_already_bonded(self, atom1: Atom, atom2: Atom) -> bool:
        """Check if atoms are already bonded."""
        return any(bond.atom2 == atom2 for bond in atom1.bonds)
    
    def get_state_summary(self) -> Dict[str, Any]:
        """Get current universe state summary."""
        return {
            'iteration': self.iteration,
            'particle_count': len(self.particles),
            'atom_count': len(self.atoms),
            'bond_count': len(self.bonds),
            'total_energy': self.total_energy,
            'total_mass': self.total_mass,
            'entropy': self.entropy_tracker.calculate_entropy(self),
            'stable_structures': len(self.stability_analyzer.stable_structures),
            'is_stable': self.is_stable()
        }


class UniverseSimulation:
    """Main simulation runner."""
    
    def __init__(self, config: UniverseConfig):
        self.config = config
        self.universe = Universe(config)
        
    def run(self, max_iterations: int = None, save_interval: int = 100) -> None:
        """Run the universe simulation."""
        if max_iterations is None:
            max_iterations = self.config.time_limit
        
        print(f"Starting universe simulation (seed: {self.config.seed})")
        print(f"Max iterations: {max_iterations}")
        
        for iteration in range(max_iterations):
            self.universe.update()
            
            # Check for stability
            if self.universe.is_stable():
                print(f"Universe reached stability at iteration {iteration}")
                self.universe.archive.save_universe(self.universe, self.config)
                break
            
            # Save checkpoint
            if iteration % save_interval == 0 and iteration > 0:
                print(f"Iteration {iteration}: {self.universe.get_state_summary()}")
        
        # Final save
        self.universe.archive.save_universe(self.universe, self.config)
        print("Simulation complete!")


class UniverseDashboard:
    """Interactive dashboard for universe simulation."""
    
    def __init__(self, universe: Universe):
        self.universe = universe
        if PLOTLY_AVAILABLE:
            self.app = dash.Dash(__name__)
            self.setup_layout()
            self.setup_callbacks()
        else:
            print("Plotly not available. Using matplotlib visualization only.")
    
    def setup_layout(self):
        """Setup the dashboard layout."""
        if not PLOTLY_AVAILABLE:
            return
            
        self.app.layout = html.Div([
            html.H1("🌌 Void Physics Universe Simulation", 
                   style={'textAlign': 'center', 'color': 'white', 
                         'backgroundColor': '#1a1a2e', 'padding': '20px'}),
            
            html.Div([
                # Control panel
                html.Div([
                    html.H3("🎛️ Universe Controls", style={'color': 'white'}),
                    
                    html.Label("Emergence Rate:"),
                    dcc.Slider(
                        id='emergence-rate-slider',
                        min=0.01, max=0.5, step=0.01, value=0.1,
                        marks={i/100: f'{i/100:.2f}' for i in range(1, 51, 5)}
                    ),
                    
                    html.Label("Force Strength (ε):"),
                    dcc.Slider(
                        id='force-epsilon-slider',
                        min=0.1, max=5.0, step=0.1, value=1.0,
                        marks={i/10: f'{i/10:.1f}' for i in range(1, 51, 5)}
                    ),
                    
                    html.Label("Bond Decay (α):"),
                    dcc.Slider(
                        id='bond-decay-slider',
                        min=0.01, max=0.5, step=0.01, value=0.1,
                        marks={i/100: f'{i/100:.2f}' for i in range(1, 51, 5)}
                    ),
                    
                    html.Label("Distance Decay (β):"),
                    dcc.Slider(
                        id='distance-decay-slider',
                        min=0.001, max=0.1, step=0.001, value=0.01,
                        marks={i/1000: f'{i/1000:.3f}' for i in range(1, 101, 10)}
                    ),
                    
                    html.Br(),
                    html.Button('🔄 Reset Universe', id='reset-button', n_clicks=0,
                              style={'backgroundColor': '#ff6b6b', 'color': 'white', 
                                   'padding': '10px', 'border': 'none', 'borderRadius': '5px'}),
                    html.Button('⏸️ Pause/Resume', id='pause-button', n_clicks=0,
                              style={'backgroundColor': '#4ecdc4', 'color': 'white', 
                                   'padding': '10px', 'border': 'none', 'borderRadius': '5px'}),
                    
                ], style={'width': '25%', 'display': 'inline-block', 'verticalAlign': 'top',
                         'backgroundColor': '#16213e', 'padding': '20px', 'margin': '10px',
                         'borderRadius': '10px'}),
                
                # Main 3D visualization
                html.Div([
                    dcc.Graph(id='universe-3d-plot'),
                    dcc.Interval(
                        id='interval-component',
                        interval=500,  # Update every 500ms
                        n_intervals=0
                    )
                ], style={'width': '70%', 'display': 'inline-block', 'verticalAlign': 'top'})
                
            ], style={'display': 'flex'}),
            
            # Statistics and analysis
            html.Div([
                html.Div([
                    html.H3("📊 Universe Statistics", style={'color': 'white'}),
                    html.Div(id='universe-stats')
                ], style={'width': '30%', 'display': 'inline-block', 'verticalAlign': 'top',
                         'backgroundColor': '#0f3460', 'padding': '20px', 'margin': '10px',
                         'borderRadius': '10px'}),
                
                html.Div([
                    html.H3("🔬 Physics Analysis", style={'color': 'white'}),
                    dcc.Graph(id='physics-plots')
                ], style={'width': '65%', 'display': 'inline-block', 'verticalAlign': 'top',
                         'backgroundColor': '#533483', 'padding': '20px', 'margin': '10px',
                         'borderRadius': '10px'})
                
            ], style={'display': 'flex'}),
            
        ], style={'backgroundColor': '#1a1a2e', 'color': 'white', 'fontFamily': 'Arial'})
    
    def setup_callbacks(self):
        """Setup dashboard callbacks."""
        if not PLOTLY_AVAILABLE:
            return
            
        @self.app.callback(
            [Output('universe-3d-plot', 'figure'),
             Output('universe-stats', 'children'),
             Output('physics-plots', 'figure')],
            [Input('interval-component', 'n_intervals'),
             Input('emergence-rate-slider', 'value'),
             Input('force-epsilon-slider', 'value'),
             Input('bond-decay-slider', 'value'),
             Input('distance-decay-slider', 'value'),
             Input('reset-button', 'n_clicks')]
        )
        def update_dashboard(n_intervals, emergence_rate, force_epsilon, 
                           bond_decay, distance_decay, reset_clicks):
            
            # Update universe parameters
            self.universe.config.emergence_rate = emergence_rate
            self.universe.config.force_constants['epsilon'] = force_epsilon
            self.universe.config.decay_constants['alpha'] = bond_decay
            self.universe.config.decay_constants['beta'] = distance_decay
            
            # Reset if button clicked
            if reset_clicks > 0:
                self.universe = Universe(self.universe.config)
            
            # Update universe
            self.universe.update()
            
            # Create 3D plot
            fig_3d = self._create_3d_plot()
            
            # Create statistics display
            stats_text = self._create_stats_display()
            
            # Create physics analysis plots
            fig_physics = self._create_physics_plots()
            
            return fig_3d, stats_text, fig_physics
    
    def _create_3d_plot(self):
        """Create 3D visualization of universe."""
        fig = go.Figure()
        
        if self.universe.particles:
            # Get particle data
            positions = np.array([p.position for p in self.universe.particles])
            energies = [p.energy for p in self.universe.particles]
            ages = [p.age for p in self.universe.particles]
            
            # Add atoms (enhanced visualization)
            atom_positions = np.array([atom.position for atom in self.universe.atoms])
            atom_energies = [atom.energy for atom in self.universe.atoms]
            atom_sizes = [atom.get_size() for atom in self.universe.atoms]
            atom_colors = [atom.get_color() for atom in self.universe.atoms]
            
            if len(atom_positions) > 0:
                fig.add_trace(go.Scatter3d(
                    x=atom_positions[:, 0],
                    y=atom_positions[:, 1], 
                    z=atom_positions[:, 2],
                    mode='markers',
                    marker=dict(
                        size=atom_sizes,
                        color=atom_colors,
                        opacity=0.8,
                        line=dict(width=2, color='black'),
                        colorbar=dict(title="Atomic Energy")
                    ),
                    text=[f'Atom #{i}<br>Energy: {e:.2f}<br>Atomic #: {atom.atomic_number}<br>Bonds: {len(atom.bonds)}' 
                          for i, (e, atom) in enumerate(zip(atom_energies, self.universe.atoms))],
                    hovertemplate='%{text}<extra></extra>',
                    name='Atoms'
                ))
            
            # Add particles (smaller, dimmer)
            if len(positions) > 0:
                fig.add_trace(go.Scatter3d(
                    x=positions[:, 0],
                    y=positions[:, 1], 
                    z=positions[:, 2],
                    mode='markers',
                    marker=dict(
                        size=4,
                        color=energies,
                        colorscale='Hot',
                        opacity=0.4,
                        showscale=False
                    ),
                    text=[f'Particle<br>Energy: {e:.2f}<br>Age: {a}' for e, a in zip(energies, ages)],
                    hovertemplate='%{text}<extra></extra>',
                    name='Particles'
                ))
            
            # Add bonds (enhanced visualization)
            if len(self.universe.bonds) > 0:
                for i, bond in enumerate(self.universe.bonds):
                    p1, p2 = bond.atom1.position, bond.atom2.position
                    bond_color = f'rgb({int(bond.get_color()[0]*255)}, {int(bond.get_color()[1]*255)}, {int(bond.get_color()[2]*255)})'
                    
                    fig.add_trace(go.Scatter3d(
                        x=[p1[0], p2[0]],
                        y=[p1[1], p2[1]],
                        z=[p1[2], p2[2]],
                        mode='lines',
                        line=dict(
                            color=bond_color, 
                            width=max(1, bond.get_width())
                        ),
                        opacity=max(0.1, bond.get_opacity()),
                        showlegend=False,
                        hoverinfo='skip',
                        name=f'{bond.bond_type} bond'
                    ))
        
        # Update layout
        fig.update_layout(
            title=f'Universe at Iteration {self.universe.iteration}',
            scene=dict(
                xaxis_title='X',
                yaxis_title='Y',
                zaxis_title='Z',
                bgcolor='rgba(0,0,0,0.1)'
            ),
            width=800,
            height=600,
            margin=dict(l=0, r=0, b=0, t=50)
        )
        
        return fig
    
    def _create_stats_display(self):
        """Create enhanced statistics display with energy breakdown."""
        stats = self.universe.get_state_summary()
        
        # Get detailed energy breakdown
        local_energies = self.universe.entropy_tracker.calculate_local_energy(self.universe)
        
        # Calculate energy density information
        universe_area = self.universe.entropy_tracker._calculate_universe_area(self.universe)
        universe_volume = self.universe.entropy_tracker._calculate_universe_volume(self.universe)
        total_energy = stats['total_energy']
        
        # Energy density calculations
        energy_density_area = total_energy / universe_area if universe_area > 0 else 0
        energy_density_volume = total_energy / universe_volume if universe_volume > 0 else 0
        
        # Local energy density
        local_energy_density = {}
        for energy_type, energy_value in local_energies.items():
            local_energy_density[energy_type] = energy_value / universe_area if universe_area > 0 else 0
        
        stats_html = f"""
        <div style="font-family: monospace;">
            <h4>📈 Universe State:</h4>
            <p><strong>Iteration:</strong> {stats['iteration']}</p>
            <p><strong>Particles:</strong> {stats['particle_count']}</p>
            <p><strong>Atoms:</strong> {stats['atom_count']}</p>
            <p><strong>Bonds:</strong> {stats['bond_count']}</p>
            
            <h4>⚡ Energy Analysis:</h4>
            <p><strong>Total Energy:</strong> {total_energy:.3f}</p>
            <p><strong>Kinetic:</strong> {local_energies['kinetic']:.3f}</p>
            <p><strong>Potential:</strong> {local_energies['potential']:.3f}</p>
            <p><strong>Bond Energy:</strong> {local_energies['bond']:.3f}</p>
            <p><strong>Void Interference:</strong> {local_energies['void_interference']:.3f}</p>
            
            <h4>📊 Energy Density (Local vs Total):</h4>
            <p><strong>Total Energy/Area:</strong> {energy_density_area:.3f} E/m²</p>
            <p><strong>Total Energy/Volume:</strong> {energy_density_volume:.3f} E/m³</p>
            <p><strong>Local Kinetic Density:</strong> {local_energy_density['kinetic']:.3f} E/m²</p>
            <p><strong>Local Potential Density:</strong> {local_energy_density['potential']:.3f} E/m²</p>
            <p><strong>Local Bond Density:</strong> {local_energy_density['bond']:.3f} E/m²</p>
            
            <h4>🌍 Universe Geometry:</h4>
            <p><strong>Universe Area:</strong> {universe_area:.2f} m²</p>
            <p><strong>Universe Volume:</strong> {universe_volume:.2f} m³</p>
            <p><strong>Particle Density:</strong> {stats['particle_count'] / universe_volume:.3f} particles/m³</p>
            
            <h4>🌡️ Thermodynamics:</h4>
            <p><strong>Total Mass:</strong> {stats['total_mass']:.2f}</p>
            <p><strong>Entropy:</strong> {stats['entropy']:.2e}</p>
            <p><strong>Temperature:</strong> {self.universe.entropy_tracker._estimate_temperature(self.universe, local_energies['kinetic']):.2f} K</p>
            
            <h4>🏗️ Structure Analysis:</h4>
            <p><strong>Stable Structures:</strong> {stats['stable_structures']}</p>
            <p><strong>Universe Stable:</strong> {'✅' if stats['is_stable'] else '❌'}</p>
            
            <h4>🔬 Bond Analysis:</h4>
        """
        
        # Add bond type statistics
        bond_types = {}
        for bond in self.universe.bonds:
            bond_type = bond.bond_type
            bond_types[bond_type] = bond_types.get(bond_type, 0) + 1
        
        for bond_type, count in bond_types.items():
            stats_html += f'<p><strong>{bond_type.title()} Bonds:</strong> {count}</p>'
        
        stats_html += """
        </div>
        """
        
        return html.Div([html.Div(stats_html, dangerously_allow_html=True)])
    
    def _create_physics_plots(self):
        """Create enhanced physics analysis plots with energy breakdown."""
        if not self.universe.history:
            return go.Figure()
        
        history_df = pd.DataFrame(self.universe.history)
        
        fig = make_subplots(
            rows=4, cols=2,
            subplot_titles=('Structure Evolution', 'Total Energy vs Local Energy', 
                          'Entropy Growth', 'Energy Distribution',
                          'Energy Density Evolution', 'Universe Geometry',
                          'Bond Type Evolution', 'Stability Progress'),
            specs=[[{"type": "scatter"}, {"type": "scatter"}],
                           [{"type": "scatter"}, {"type": "scatter"}],
                           [{"type": "scatter"}, {"type": "scatter"}],
                           [{"type": "scatter"}, {"type": "scatter"}]]
        )
        
        # Structure evolution
        fig.add_trace(
            go.Scatter(x=history_df['iteration'], y=history_df['particle_count'],
                      mode='lines', name='Particles', line=dict(color='blue')),
            row=1, col=1
        )
        fig.add_trace(
            go.Scatter(x=history_df['iteration'], y=history_df['atom_count'],
                      mode='lines', name='Atoms', line=dict(color='red')),
            row=1, col=1
        )
        fig.add_trace(
            go.Scatter(x=history_df['iteration'], y=history_df['bond_count'],
                      mode='lines', name='Bonds', line=dict(color='green')),
            row=1, col=1
        )
        
        # Total vs Local Energy comparison
        if len(self.universe.entropy_tracker.total_energy_history) > 0:
            # Create iteration array for energy history
            energy_iterations = list(range(len(self.universe.entropy_tracker.total_energy_history)))
            
            fig.add_trace(
                go.Scatter(x=energy_iterations, y=self.universe.entropy_tracker.total_energy_history,
                          mode='lines', name='Total Energy', line=dict(color='purple')),
                row=1, col=2
            )
            
            # Add local energy components if available
            if len(self.universe.entropy_tracker.local_energy_history) > 0:
                local_hist = self.universe.entropy_tracker.local_energy_history
                kinetic_energies = [e['kinetic'] for e in local_hist]
                potential_energies = [e['potential'] for e in local_hist]
                bond_energies = [e['bond'] for e in local_hist]
                
                fig.add_trace(
                    go.Scatter(x=energy_iterations, y=kinetic_energies,
                              mode='lines', name='Kinetic', line=dict(color='orange')),
                    row=1, col=2
                )
                fig.add_trace(
                    go.Scatter(x=energy_iterations, y=potential_energies,
                              mode='lines', name='Potential', line=dict(color='red')),
                    row=1, col=2
                )
                fig.add_trace(
                    go.Scatter(x=energy_iterations, y=bond_energies,
                              mode='lines', name='Bond Energy', line=dict(color='green')),
                    row=1, col=2
                )
        
        # Entropy growth
        fig.add_trace(
            go.Scatter(x=history_df['iteration'], y=history_df['entropy'],
                      mode='lines', name='Entropy', line=dict(color='orange')),
            row=2, col=1
        )
        
        # Current energy distribution (pie chart would be better, but scatter for now)
        current_local_energies = self.universe.entropy_tracker.calculate_local_energy(self.universe)
        energy_types = list(current_local_energies.keys())
        energy_values = list(current_local_energies.values())
        
        fig.add_trace(
            go.Scatter(x=energy_types, y=energy_values,
                      mode='markers+text', name='Energy Distribution',
                      marker=dict(size=20, color=['blue', 'red', 'green', 'purple'])),
            row=2, col=2
        )
        
        # Energy Density Evolution (if available)
        if hasattr(self.universe.entropy_tracker, 'energy_density_history') and len(self.universe.entropy_tracker.energy_density_history) > 0:
            energy_density_hist = self.universe.entropy_tracker.energy_density_history
            density_iterations = list(range(len(energy_density_hist)))
            
            kinetic_densities = [e['kinetic'] for e in energy_density_hist]
            potential_densities = [e['potential'] for e in energy_density_hist]
            bond_densities = [e['bond'] for e in energy_density_hist]
            
            fig.add_trace(
                go.Scatter(x=density_iterations, y=kinetic_densities,
                          mode='lines', name='Kinetic Density', line=dict(color='orange')),
                row=3, col=1
            )
            fig.add_trace(
                go.Scatter(x=density_iterations, y=potential_densities,
                          mode='lines', name='Potential Density', line=dict(color='red')),
                row=3, col=1
            )
            fig.add_trace(
                go.Scatter(x=density_iterations, y=bond_densities,
                          mode='lines', name='Bond Density', line=dict(color='green')),
                row=3, col=1
            )
        
        # Universe Geometry Evolution
        universe_areas = []
        universe_volumes = []
        for i in range(len(history_df)):
            # Simulate universe geometry evolution (would need to track this in history)
            universe_areas.append(history_df.iloc[i]['particle_count'] * 2.0)  # Rough estimate
            universe_volumes.append(history_df.iloc[i]['particle_count'] * 4.0)  # Rough estimate
        
        fig.add_trace(
            go.Scatter(x=history_df['iteration'], y=universe_areas,
                      mode='lines', name='Universe Area', line=dict(color='cyan')),
            row=3, col=2
        )
        fig.add_trace(
            go.Scatter(x=history_df['iteration'], y=universe_volumes,
                      mode='lines', name='Universe Volume', line=dict(color='magenta')),
            row=3, col=2
        )
        
        # Bond type evolution (simplified - would need more history tracking)
        current_bond_types = {}
        for bond in self.universe.bonds:
            bond_type = bond.bond_type
            current_bond_types[bond_type] = current_bond_types.get(bond_type, 0) + 1
        
        if current_bond_types:
            fig.add_trace(
                go.Scatter(x=list(current_bond_types.keys()), y=list(current_bond_types.values()),
                          mode='markers+text', name='Current Bond Types',
                          marker=dict(size=15, color=['gray', 'lightblue', 'orange'])),
                row=4, col=1
            )
        
        # Stability progress
        fig.add_trace(
            go.Scatter(x=history_df['iteration'], y=history_df['stable_structures'],
                      mode='lines', name='Stable Structures', line=dict(color='brown')),
            row=4, col=2
        )
        
        fig.update_layout(height=1200, showlegend=True, 
                         title_text="Enhanced Physics Analysis Dashboard with Energy Density")
        
        return fig
    
    def run(self, debug=False, port=8052):
        """Run the dashboard."""
        if PLOTLY_AVAILABLE:
            print(f"🚀 Starting dashboard on http://localhost:{port}")
            self.app.run_server(debug=debug, port=port)
        else:
            print("❌ Plotly not available. Cannot run dashboard.")


# Keep the existing visualization classes but adapt them for 3D
class Visualizer3D:
    """3D visualization for the universe simulation."""
    
    def __init__(self):
        self.fig = plt.figure(figsize=(15, 10))
        self.ax_universe = self.fig.add_subplot(221, projection='3d')
        self.ax_particles = self.fig.add_subplot(222, projection='3d')
        self.ax_stats = self.fig.add_subplot(223)
        self.ax_energy = self.fig.add_subplot(224)
        
    def update(self, universe: Universe) -> None:
        """Update visualization."""
        self.ax_universe.clear()
        self.ax_particles.clear()
        self.ax_stats.clear()
        self.ax_energy.clear()
        
        # Universe view (particles + bonds)
        if universe.particles:
            positions = np.array([p.position for p in universe.particles])
            energies = [p.energy for p in universe.particles]
            
            scatter = self.ax_universe.scatter(positions[:, 0], positions[:, 1], 
                                             positions[:, 2], c=energies, 
                                             cmap='hot', s=50, alpha=0.7)
            
            # Draw bonds
            for bond in universe.bonds:
                p1, p2 = bond.atom1.position, bond.atom2.position
                self.ax_universe.plot([p1[0], p2[0]], [p1[1], p2[1]], 
                                    [p1[2], p2[2]], 'b-', alpha=0.5, linewidth=2)
        
        self.ax_universe.set_title(f'Universe (t={universe.iteration})')
        self.ax_universe.set_xlabel('X')
        self.ax_universe.set_ylabel('Y')
        self.ax_universe.set_zlabel('Z')
        
        # Particle energy distribution
        if universe.particles:
            energies = [p.energy for p in universe.particles]
            ages = [p.age for p in universe.particles]
            
            self.ax_particles.scatter(ages, energies, c=energies, cmap='viridis')
            self.ax_particles.set_xlabel('Age')
            self.ax_particles.set_ylabel('Energy')
            self.ax_particles.set_title('Particle Energy vs Age')
        
        # Statistics
        if universe.history:
            history_df = pd.DataFrame(universe.history)
            
            self.ax_stats.plot(history_df['iteration'], history_df['particle_count'], 
                             'b-', label='Particles')
            self.ax_stats.plot(history_df['iteration'], history_df['atom_count'], 
                             'r-', label='Atoms')
            self.ax_stats.plot(history_df['iteration'], history_df['bond_count'], 
                             'g-', label='Bonds')
            self.ax_stats.set_xlabel('Iteration')
            self.ax_stats.set_ylabel('Count')
            self.ax_stats.set_title('Structure Evolution')
            self.ax_stats.legend()
            self.ax_stats.grid(True, alpha=0.3)
        
        # Energy evolution
        if universe.history:
            self.ax_energy.plot(history_df['iteration'], history_df['total_energy'], 
                              'purple', linewidth=2)
            self.ax_energy.set_xlabel('Iteration')
            self.ax_energy.set_ylabel('Total Energy')
            self.ax_energy.set_title('Energy Evolution')
            self.ax_energy.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.draw()
    
    def animate(self, universe: Universe, n_frames: int = 1000, 
                interval: int = 100) -> animation.FuncAnimation:
        """Create animation of universe evolution."""
        def animate_frame(frame):
            universe.update()
            self.update(universe)
            return []
        
        anim = animation.FuncAnimation(self.fig, animate_frame, frames=n_frames,
                                     interval=interval, blit=False, repeat=True)
        return anim


def main():
    """Run the void physics universe simulation."""
    print("🌌 Starting Void Physics Universe Simulation...")
    
    # Create configuration
    config = UniverseConfig(seed=42)
    
    # Create universe
    universe = Universe(config)
    
    # Ask user for visualization mode
    print("\n🎮 Choose visualization mode:")
    print("1. Interactive Dashboard (requires Plotly)")
    print("2. Matplotlib Animation")
    print("3. Run simulation without visualization")
    
    try:
        choice = input("Enter choice (1-3): ").strip()
    except:
        choice = "2"  # Default to matplotlib
    
    if choice == "1" and PLOTLY_AVAILABLE:
        # Interactive dashboard
        print("🚀 Starting interactive dashboard...")
        dashboard = UniverseDashboard(universe)
        dashboard.run(debug=False, port=8052)
        
    elif choice == "2":
        # Matplotlib animation
        print("🎬 Starting matplotlib animation...")
        visualizer = Visualizer3D()
        
        # Run simulation with visualization
        for i in range(1000):
            universe.update()
            if i % 10 == 0:
                visualizer.update(universe)
                plt.pause(0.01)
        
        plt.show()
        
    else:
        # Run simulation without visualization
        print("⚡ Running simulation without visualization...")
        simulation = UniverseSimulation(config)
        simulation.run(max_iterations=1000, save_interval=50)
    
    print("✅ Simulation complete!")
    print(f"Final state: {universe.get_state_summary()}")
    
    # Show saved universes
    archive_dir = Path("examples/universes")
    if archive_dir.exists():
        saved_universes = list(archive_dir.glob("universe_*.json"))
        if saved_universes:
            print(f"\n💾 Found {len(saved_universes)} saved universes:")
            for universe_file in saved_universes:
                print(f"  - {universe_file.name}")


if __name__ == "__main__":
    main()