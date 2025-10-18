# 🚀 Getting Started

Welcome to the Void Physics Life Simulation! This guide will help you get up and running quickly.

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

```bash
# Navigate to examples directory
cd examples

# Run the simulation
uv run python void_physics_life_game.py

# Or with regular Python
python void_physics_life_game.py
```

### 3. Choose Your Experience

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
