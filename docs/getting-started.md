# 🚀 Getting Started

Welcome to the Void Physics Life Simulation with Quantum Mechanics Integration! This guide will help you get up and running quickly with both classical void physics and quantum mechanics features.

## Quick Start

### 1. Installation

```bash
# Clone the repository
git clone <repository-url>
cd void-physic

# Install dependencies using UV (recommended)
uv sync

# Or using pip
pip install -r requirements.txt
```

### 2. Run Your First Simulation

#### Classical Void Physics
```bash
# Navigate to examples directory
cd examples

# Run the classical simulation
uv run python void_physics_life_game.py

# Or with regular Python
python void_physics_life_game.py
```

#### Quantum Mechanics Dashboard
```bash
# Run the quantum dashboard
uv run python -m void_physic.visualization.quantum_dashboard

# Or with regular Python
python -m void_physic.visualization.quantum_dashboard
```

#### Quantum Examples
```bash
# Run quantum examples
cd examples/quantum_examples

# Schrödinger equation tunneling
python schrodinger_tunneling.py

# Wave packet evolution
python wave_packet_evolution.py

# Quantum void emergence
python quantum_void_emergence.py

# Universe game tutorial
python universe_game_tutorial.py
```

### 3. Choose Your Experience

#### Quantum Dashboard Modes

When you run the quantum dashboard, you'll have access to three modes:

1. **Sandbox Mode** (Recommended for learning)
   - Interactive parameter sliders (mass, ℏ, potential depth, etc.)
   - Real-time quantum equation visualization
   - Compare Schrödinger, Klein-Gordon, and Dirac equations
   - Perfect for understanding quantum mechanics concepts

2. **Game Mode** (Fun and educational)
   - Create universes by tuning quantum parameters
   - Score points for stability and complexity
   - Save successful universe configurations
   - Challenge levels with increasing difficulty

3. **Theory Mode**
   - Deep dive into quantum equations and derivations
   - Mathematical explanations and visualizations
   - Connection between quantum mechanics and void physics

#### Classical Void Physics Modes

When prompted, select your preferred visualization mode:

1. **Interactive Dashboard** (Recommended)
   - Real-time 3D visualization
   - Interactive parameter controls
   - Live statistics and analysis
   - Best for exploration and experimentation

2. **Matplotlib Animation**
   - 3D particle animation
   - Shows particle emergence and bonding
   - Good for understanding the physics

3. **Headless Simulation**
   - Run without visualization
   - Save results to files
   - Best for long simulations and analysis

## Quantum Mechanics Tutorials

### Tutorial 1: Your First Quantum Simulation

Let's start with a simple Schrödinger equation simulation:

```python
from void_physic.quantum.schrodinger import SchrodingerSolver, SchrodingerParameters

# Set up parameters
params = SchrodingerParameters(
    mass=1.0,
    hbar=1.0,
    dt=0.01,
    x_min=-5.0,
    x_max=5.0,
    n_points=256
)

# Create a simple harmonic potential
params.potential = lambda x: 0.5 * x**2

# Initialize solver
solver = SchrodingerSolver(params)

# Create initial wave packet
psi_init = solver.create_gaussian_packet(x0=0.0, p0=1.0, sigma=1.0)

# Evolve and visualize
psi_trajectory, time_array = solver.evolve_trajectory(psi_init, 100)
```

### Tutorial 2: Playing the Quantum Universe Game

1. **Start the Dashboard**: Run `python -m void_physic.visualization.quantum_dashboard`
2. **Switch to Game Mode**: Click the "Game" tab
3. **Adjust Parameters**:
   - Emergence Rate: Controls how often particles appear
   - Quantum Coupling: Affects field interactions
   - Void Strength: Determines particle creation amplitude
4. **Click "Start Universe"**: Watch your universe evolve!
5. **Score Points**: Higher scores for more particles, stability, and entropy
6. **Save Success**: Click "Save Universe" to preserve good configurations

### Tutorial 3: Quantum Tunneling

Explore quantum tunneling through potential barriers:

```python
# Create a potential barrier
def barrier_potential(x):
    return np.where(np.abs(x) < 1.0, 2.0, 0.0)

params.potential = barrier_potential

# Create wave packet with energy below barrier
psi_init = solver.create_gaussian_packet(x0=-2.0, p0=0.5, sigma=0.5)

# Watch it tunnel through!
```

### Tutorial 4: Quantum Field Theory

See particles emerge from quantum fields:

```python
from void_physic.quantum.field_theory import QuantumField, FieldParameters

# Set up quantum field
field_params = FieldParameters(
    mass=1.0, hbar=1.0, c=1.0, coupling=0.5,
    x_min=-5.0, x_max=5.0, n_points=128, dt=0.02
)

quantum_field = QuantumField(field_params)

# Start from vacuum
quantum_field.set_field(quantum_field.field_operator.vacuum_state())

# Add particle creation events
for i in range(50):
    if np.random.random() < 0.1:  # 10% chance
        k = np.random.uniform(-2.0, 2.0)
        amplitude = np.random.uniform(0.5, 1.0)
        quantum_field.field_operator.create_particle(k, amplitude)
    
    quantum_field.evolve_step()
```

## Understanding the Simulation

### What You'll See

- **Blue Dots**: Individual particles emerging from the void
- **Colored Spheres**: Atoms formed when particles cluster
- **Colored Lines**: Bonds between atoms
  - Gray: Covalent bonds
  - Light Blue: Polar covalent bonds
  - Orange: Ionic bonds

### Key Concepts

1. **Void Emergence**: Particles appear from nothing through void interference
2. **Distance Creation**: Distance only exists between emerged particles
3. **Atomic Bonding**: Particles form atoms which can bond together
4. **Energy Flow**: Energy flows through bonds like "lightning"
5. **Entropy Evolution**: The universe expands and evolves

## Interactive Dashboard

If you chose the Interactive Dashboard, you'll see:

### Controls Panel
- **Emergence Rate**: How often new particles appear
- **Force Constants**: Strength of atomic forces
- **Decay Constants**: How energy decays through bonds

### Visualization
- **3D Universe**: Real-time 3D view of particles, atoms, and bonds
- **Statistics**: Live physics data and analysis
- **Energy Analysis**: Energy density and distribution

### Physics Plots
- **Structure Evolution**: How particles, atoms, and bonds change over time
- **Energy Analysis**: Energy flow and conservation
- **Entropy Growth**: Universe evolution and thermodynamics

## First Experiments

### Experiment 1: Watch Emergence
1. Start with default settings
2. Watch the first particle appear at the origin
3. Observe how subsequent particles emerge nearby
4. Notice how distance is created between particles

### Experiment 2: Bond Formation
1. Let the simulation run until atoms form
2. Watch bonds appear between atoms
3. Notice how bond colors indicate different types
4. Observe energy flow through the bond network

### Experiment 3: Parameter Tuning
1. Adjust the emergence rate slider
2. See how it affects particle creation
3. Modify force constants
4. Observe changes in bonding behavior

## Understanding the Physics

### Energy Conservation
- Total energy is conserved throughout the simulation
- Energy transforms between kinetic, potential, bond, and void interference forms
- The simulation maintains energy conservation within numerical precision

### Entropy and Evolution
- Entropy generally increases over time (second law of thermodynamics)
- The universe expands as new particles emerge
- Stable structures form and persist

### Bond Physics
- Bonds form based on energy minima and quantum mechanical criteria
- Energy transmission follows exponential decay
- Different bond types have different properties

## Troubleshooting

### Common Issues

**"Plotly not available"**
- The simulation will use matplotlib instead
- Install plotly for enhanced visualization: `pip install plotly dash`

**"Module not found"**
- Make sure you're in the correct directory
- Check that dependencies are installed
- Try using UV: `uv run python void_physics_life_game.py`

**Slow Performance**
- Reduce the number of particles
- Increase the time step
- Turn off visualization for headless runs

### Getting Help

- Check the [Physics Documentation](physics.md) for detailed explanations
- See the [API Reference](api.md) for technical details
- Report issues on GitHub
- Join community discussions

## Next Steps

### Explore Further
- Read the [Physics Documentation](physics.md) for deep dives
- Check out the [API Reference](api.md) for programming
- Try different parameter combinations
- Experiment with different seeds

### Contribute
- See [Contributing Guidelines](contributing.md) for how to help
- Report bugs and suggest features
- Share your interesting simulations
- Help improve the documentation

### Advanced Usage
- Create custom configurations
- Run headless simulations for analysis
- Save and replay interesting universes
- Analyze the physics data programmatically

## Examples

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
        print(f"Iteration {i}: {stats['particle_count']} particles")
```

### Custom Parameters
```python
config = UniverseConfig(seed=456)
config.emergence_rate = 0.2  # Faster emergence
config.force_constants['epsilon'] = 1.5  # Stronger forces
config.time_limit = 5000  # Longer simulation

universe = Universe(config)
# Run simulation...
```

---

**Happy Simulating!** 🌌✨

Explore the emergence of complexity from nothing and discover the fascinating physics of void emergence!
