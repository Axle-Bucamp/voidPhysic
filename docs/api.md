# 📚 API Reference

## Overview

This document provides a comprehensive API reference for the Void Physics Life Simulation and Quantum Mechanics Integration. The API is organized into core classes that handle different aspects of the simulation, including the new quantum mechanics modules.

## Quantum Mechanics Module

### SchrodingerSolver

Solves the time-dependent Schrödinger equation using the split-operator FFT method.

```python
class SchrodingerSolver:
    def __init__(self, params: SchrodingerParameters):
        """Initialize Schrödinger equation solver.
        
        Args:
            params: SchrödingerParameters object containing solver configuration
        """
```

#### Methods

```python
def evolve_step(self, psi: WaveFunction) -> WaveFunction:
    """Evolve wave function by one time step.
    
    Args:
        psi: Current wave function
        
    Returns:
        Evolved wave function
    """

def evolve_trajectory(self, psi_init: WaveFunction, n_steps: int) -> Tuple[np.ndarray, np.ndarray]:
    """Evolve wave function over multiple time steps.
    
    Args:
        psi_init: Initial wave function
        n_steps: Number of time steps
        
    Returns:
        Tuple of (wave_function_trajectory, time_array)
    """

def create_gaussian_packet(self, x0: float, p0: float, sigma: float) -> WaveFunction:
    """Create initial Gaussian wave packet.
    
    Args:
        x0: Initial position
        p0: Initial momentum
        sigma: Width parameter
        
    Returns:
        Gaussian wave packet
    """
```

### WaveFunction

Represents a quantum wave function with probability density and current calculations.

```python
class WaveFunction:
    def __init__(self, psi: np.ndarray, x_grid: np.ndarray, mass: float = 1.0, hbar: float = 1.0):
        """Initialize wave function.
        
        Args:
            psi: Complex wave function values
            x_grid: Spatial grid
            mass: Particle mass
            hbar: Reduced Planck constant
        """
```

#### Methods

```python
def probability_density(self) -> np.ndarray:
    """Calculate probability density |ψ|²."""

def probability_current(self) -> np.ndarray:
    """Calculate probability current j = (ℏ/2mi)(ψ*∇ψ - ψ∇ψ*)."""

def normalize(self) -> None:
    """Normalize wave function to unit probability."""
```

### KleinGordonSolver

Solves the Klein-Gordon equation for relativistic spin-0 particles.

```python
class KleinGordonSolver:
    def __init__(self, params: RelativisticParameters):
        """Initialize Klein-Gordon equation solver.
        
        Args:
            params: RelativisticParameters object
        """
```

#### Methods

```python
def evolve_step(self, phi: np.ndarray, dphi_dt: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """Evolve field by one time step.
    
    Args:
        phi: Current field values
        dphi_dt: Current field time derivative
        
    Returns:
        Tuple of (new_phi, new_dphi_dt)
    """
```

### DiracSolver

Solves the Dirac equation for relativistic spin-½ particles.

```python
class DiracSolver:
    def __init__(self, params: RelativisticParameters):
        """Initialize Dirac equation solver.
        
        Args:
            params: RelativisticParameters object
        """
```

#### Methods

```python
def evolve_step(self, psi_spinor: np.ndarray) -> np.ndarray:
    """Evolve Dirac spinor by one time step.
    
    Args:
        psi_spinor: 2-component spinor wave function
        
    Returns:
        Evolved spinor
    """
```

### QuantumField

Represents a quantum scalar field with creation and annihilation operators.

```python
class QuantumField:
    def __init__(self, params: FieldParameters):
        """Initialize quantum field.
        
        Args:
            params: FieldParameters object
        """
```

#### Methods

```python
def evolve_step(self) -> None:
    """Evolve field by one time step."""

def calculate_observables(self) -> Dict[str, float]:
    """Calculate field observables (energy, variance, etc.)."""

def get_particle_positions(self, threshold: float = 0.1) -> List[float]:
    """Get positions where field amplitude exceeds threshold."""
```

### ParticleCreation

Handles particle creation and annihilation events in quantum field.

```python
class ParticleCreation:
    def __init__(self, quantum_field: QuantumField):
        """Initialize particle creation handler.
        
        Args:
            quantum_field: Associated quantum field
        """
```

#### Methods

```python
def particle_creation_event(self, k: float, amplitude: float) -> None:
    """Create particle with given momentum and amplitude.
    
    Args:
        k: Momentum
        amplitude: Creation amplitude
    """

def particle_annihilation_event(self, position: float, amplitude: float) -> None:
    """Annihilate particle at given position.
    
    Args:
        position: Annihilation position
        amplitude: Annihilation amplitude
    """
```

## Quantum Dashboard API

### QuantumDashboard

Interactive Plotly Dash application for quantum void physics exploration.

```python
class QuantumDashboard:
    def __init__(self):
        """Initialize quantum dashboard."""
```

#### Methods

```python
def run(self, debug: bool = True, port: int = 8050) -> None:
    """Run the dashboard server.
    
    Args:
        debug: Enable debug mode
        port: Server port
    """

def create_sandbox_layout(self) -> html.Div:
    """Create sandbox mode layout with parameter controls."""

def create_game_layout(self) -> html.Div:
    """Create game mode layout with universe simulation."""

def create_theory_layout(self) -> html.Div:
    """Create theory mode layout with equation explanations."""
```

#### Callbacks

The dashboard includes several Plotly Dash callbacks for real-time interaction:

- `update_sandbox_plots`: Updates quantum simulation plots based on parameter changes
- `update_game_plots`: Handles universe simulation in game mode
- `render_tab_content`: Switches between different dashboard modes

## Core Classes

### UniverseConfig

Configuration class for universe simulation parameters.

```python
class UniverseConfig:
    def __init__(self, seed: int = None, start_from_nothing: bool = True, 
                 emergence_rate: float = 0.1, initial_particle_energy: float = 1.0):
        """Initialize universe configuration.
        
        Args:
            seed: Random seed for reproducibility
            start_from_nothing: Whether to start from void (True) or seeded particles (False)
            emergence_rate: Probability of particle emergence per iteration
            initial_particle_energy: Initial energy of emerged particles
        """
```

#### Attributes

- `seed`: Random seed for reproducibility
- `start_from_nothing`: Whether to start from void or seeded particles
- `emergence_rate`: Particle emergence probability per iteration
- `initial_particle_energy`: Initial energy of new particles
- `force_constants`: Dictionary of Lennard-Jones force parameters
- `decay_constants`: Dictionary of bond decay parameters
- `time_limit`: Maximum simulation iterations
- `stability_threshold`: Threshold for universe stability

#### Methods

```python
def get_config_summary(self) -> Dict[str, Any]:
    """Get configuration summary for display."""
```

### Particle

Represents a fundamental particle in the void physics simulation.

```python
class Particle:
    def __init__(self, position: np.ndarray, energy: float = 1.0, 
                 mass: float = 1.0, charge: float = 0.0):
        """Initialize a particle.
        
        Args:
            position: 3D position vector
            energy: Particle energy
            mass: Particle mass
            charge: Particle charge
        """
```

#### Attributes

- `position`: 3D position vector (numpy array)
- `velocity`: 3D velocity vector (numpy array)
- `force`: 3D force vector (numpy array)
- `energy`: Particle energy
- `mass`: Particle mass
- `charge`: Particle charge
- `age`: Particle age in iterations
- `void_interference`: Void interference factor

#### Methods

```python
def get_distance_to(self, other: 'Particle') -> float:
    """Calculate distance to another particle."""

def update_velocity(self, dt: float) -> None:
    """Update velocity based on forces."""

def update_position(self, dt: float) -> None:
    """Update position based on velocity."""

def get_color(self) -> Tuple[float, float, float]:
    """Get visualization color based on energy."""
```

### Atom

Represents an atom composed of one or more particles with bonds to other atoms.

```python
class Atom:
    def __init__(self, particles: List[Particle]):
        """Initialize an atom from constituent particles.
        
        Args:
            particles: List of particles that form the atom
        """
```

#### Attributes

- `particles`: List of constituent particles
- `bonds`: List of bonds to other atoms
- `age`: Atom age in iterations
- `creation_time`: Iteration when atom was created
- `electron_shells`: Calculated electron shell radii
- `atomic_number`: Number of particles (simplified atomic number)
- `atomic_radius`: Calculated atomic radius
- `electronegativity`: Calculated electronegativity

#### Properties

```python
@property
def position(self) -> np.ndarray:
    """Center of mass position."""

@property
def energy(self) -> float:
    """Total energy including binding energy."""

@property
def mass(self) -> float:
    """Total mass of atom."""

@property
def volume(self) -> float:
    """Atomic volume based on electron shells."""

@property
def density(self) -> float:
    """Atomic density."""
```

#### Methods

```python
def distance_to(self, other: 'Atom') -> float:
    """Distance to another atom."""

def can_bond_with(self, other: 'Atom', config: UniverseConfig) -> bool:
    """Check if atom can form bond with another atom."""

def form_bond(self, other: 'Atom', config: UniverseConfig) -> 'Bond':
    """Form a bond with another atom."""

def get_color(self) -> Tuple[float, float, float]:
    """Get color based on atomic properties."""

def get_size(self) -> float:
    """Get visual size for rendering."""
```

### Bond

Represents a bond between two atoms that transmits energy.

```python
class Bond:
    def __init__(self, atom1: Atom, atom2: Atom, config: UniverseConfig):
        """Initialize a bond between two atoms.
        
        Args:
            atom1: First atom
            atom2: Second atom
            config: Universe configuration
        """
```

#### Attributes

- `atom1`: First atom
- `atom2`: Second atom
- `distance`: Distance between atoms
- `energy_capacity`: Energy capacity of the bond
- `age`: Bond age in iterations
- `creation_time`: Iteration when bond was created
- `bond_type`: Type of bond (covalent, polar_covalent, ionic)
- `bond_order`: Bond order (single, double, triple)
- `bond_angle`: Bond angle with other bonds
- `resonance_frequency`: Resonance frequency for energy transmission

#### Methods

```python
def transmit_energy(self, energy: float, num_hops: int, 
                   cumulative_distance: float) -> float:
    """Transmit energy through bond with quantum mechanical decay."""

def is_stable(self) -> bool:
    """Check if bond is stable using quantum mechanical criteria."""

def get_color(self) -> Tuple[float, float, float]:
    """Get color based on bond type and strength."""

def get_width(self) -> float:
    """Get line width for rendering based on bond order."""

def get_opacity(self) -> float:
    """Get opacity based on bond strength."""
```

### PhysicsEngine

Handles force calculations and particle dynamics.

```python
class PhysicsEngine:
    def __init__(self, config: UniverseConfig):
        """Initialize physics engine.
        
        Args:
            config: Universe configuration
        """
```

#### Methods

```python
def lennard_jones_potential(self, r: float) -> float:
    """Calculate Lennard-Jones potential energy."""

def lennard_jones_force(self, r: float) -> float:
    """Calculate Lennard-Jones force."""

def calculate_forces(self, particles: List[Particle]) -> None:
    """Calculate forces between all particles."""

def update_particles(self, particles: List[Particle], dt: float) -> None:
    """Update particle positions and velocities."""
```

### VoidEmergence

Handles particle emergence from the void.

```python
class VoidEmergence:
    def __init__(self, config: UniverseConfig):
        """Initialize void emergence handler.
        
        Args:
            config: Universe configuration
        """
```

#### Methods

```python
def should_emerge_particle(self, universe: 'Universe') -> bool:
    """Determine if a new particle should emerge."""

def create_particle(self, universe: 'Universe') -> Particle:
    """Create a new particle."""

def _find_emergence_location(self, universe: 'Universe') -> np.ndarray:
    """Find location for new particle emergence."""
```

### EntropyTracker

Tracks entropy evolution and universe expansion.

```python
class EntropyTracker:
    def __init__(self, config: UniverseConfig):
        """Initialize entropy tracker.
        
        Args:
            config: Universe configuration
        """
```

#### Methods

```python
def calculate_local_energy(self, universe: 'Universe') -> Dict[str, float]:
    """Calculate local energy distributions for entropy computation."""

def calculate_total_energy(self, universe: 'Universe') -> float:
    """Calculate total energy including all forms."""

def calculate_entropy(self, universe: 'Universe') -> float:
    """Calculate entropy using local energy distributions and statistical mechanics."""

def update_expansion_rate(self, entropy_rate: float) -> None:
    """Update universe expansion rate based on entropy change."""
```

### Universe

Main simulation class that orchestrates all components.

```python
class Universe:
    def __init__(self, config: UniverseConfig):
        """Initialize universe simulation.
        
        Args:
            config: Universe configuration
        """
```

#### Attributes

- `particles`: List of all particles
- `atoms`: List of all atoms
- `bonds`: List of all bonds
- `iteration`: Current simulation iteration
- `total_energy`: Total energy of the universe
- `total_mass`: Total mass of the universe
- `history`: Simulation history data

#### Methods

```python
def update(self) -> None:
    """Update universe for one iteration."""

def add_particle(self, particle: Particle) -> None:
    """Add a particle to the universe."""

def create_atom(self, particles: List[Particle]) -> Atom:
    """Create an atom from particles."""

def check_bond_formation(self) -> None:
    """Check for new bond formation between atoms."""

def check_bond_breaking(self) -> None:
    """Check for bond breaking due to instability."""

def transmit_energy_through_bonds(self) -> None:
    """Transmit energy through bond network."""

def get_state_summary(self) -> Dict[str, Any]:
    """Get current universe state summary."""

def is_stable(self) -> bool:
    """Check if universe has reached stability."""
```

### UniverseDashboard

Interactive dashboard for visualization and control.

```python
class UniverseDashboard:
    def __init__(self, universe: Universe):
        """Initialize dashboard.
        
        Actually expects Universe object, not config.
        """
```

#### Methods

```python
def _create_3d_plot(self):
    """Create 3D visualization of universe."""

def _create_stats_display(self):
    """Create enhanced statistics display with energy breakdown."""

def _create_physics_plots(self):
    """Create enhanced physics analysis plots with energy breakdown."""

def run(self, debug: bool = False, port: int = 8052):
    """Run the dashboard."""
```

## Utility Functions

### Visualization

```python
def create_3d_animation(universe: Universe, max_iterations: int = 1000) -> None:
    """Create 3D animation of universe evolution."""

def save_universe_state(universe: Universe, filename: str) -> None:
    """Save universe state to file."""

def load_universe_state(filename: str) -> Universe:
    """Load universe state from file."""
```

### Analysis

```python
def analyze_bond_network(universe: Universe) -> Dict[str, Any]:
    """Analyze the bond network structure."""

def calculate_energy_flow(universe: Universe) -> Dict[str, float]:
    """Calculate energy flow through the system."""

def find_stable_structures(universe: Universe) -> List[Atom]:
    """Find stable atomic structures."""
```

## Configuration Examples

### Basic Configuration

```python
config = UniverseConfig(
    seed=123,
    emergence_rate=0.1,
    initial_particle_energy=1.0
)
```

### Advanced Configuration

```python
config = UniverseConfig(seed=456)
config.force_constants = {
    'epsilon': 1.5,  # Stronger interactions
    'sigma': 0.8,    # Smaller interaction range
    'cutoff': 4.0    # Shorter cutoff
}
config.decay_constants = {
    'alpha': 0.05,   # Slower bond decay
    'beta': 0.005,   # Slower distance decay
    'min_bond_energy': 0.02
}
config.time_limit = 5000
```

## Usage Examples

### Basic Simulation

```python
from void_physics_life_game import UniverseConfig, Universe

# Create configuration
config = UniverseConfig(seed=123)

# Create universe
universe = Universe(config)

# Run simulation
for i in range(100):
    universe.update()
    if i % 10 == 0:
        stats = universe.get_state_summary()
        print(f"Iteration {i}: {stats['particle_count']} particles, "
              f"{stats['atom_count']} atoms, {stats['bond_count']} bonds")
```

### Interactive Dashboard

```python
from void_physics_life_game import UniverseConfig, Universe, UniverseDashboard

# Create universe
config = UniverseConfig(seed=123)
universe = Universe(config)

# Create dashboard
dashboard = UniverseDashboard(universe)

# Run dashboard
dashboard.run(port=8052)
```

### Custom Analysis

```python
# Run simulation
for i in range(500):
    universe.update()

# Analyze results
stats = universe.get_state_summary()
local_energies = universe.entropy_tracker.calculate_local_energy(universe)
entropy = universe.entropy_tracker.calculate_entropy(universe)

print(f"Final state: {stats}")
print(f"Energy breakdown: {local_energies}")
print(f"Entropy: {entropy}")
```

## Error Handling

### Common Exceptions

- `ValueError`: Invalid configuration parameters
- `RuntimeError`: Simulation errors (e.g., division by zero)
- `ImportError`: Missing optional dependencies (plotly, scipy)

### Best Practices

1. **Validate Configuration**: Check parameter ranges before simulation
2. **Handle Edge Cases**: Check for empty particle lists
3. **Monitor Energy**: Ensure energy conservation within numerical precision
4. **Save Progress**: Regularly save universe state for long simulations

## Performance Considerations

### Optimization Tips

1. **Particle Count**: Large particle counts (>1000) may require performance optimization
2. **Time Step**: Smaller time steps improve accuracy but reduce performance
3. **Force Cutoff**: Shorter cutoffs improve performance but may affect physics
4. **Visualization**: Turn off visualization for performance-critical simulations

### Memory Management

- Universe history is stored sparsely to manage memory
- Old particle/atom data is cleaned up automatically
- Large simulations may require periodic state saving

---

This API reference provides comprehensive documentation for all major components of the Void Physics Life Simulation. For more detailed examples and tutorials, see the main documentation.
