# Void Physics Module

A mathematical modeling and visualization framework for "void physics" - the emergence of spacetime, matter, and time from a primordial topological void state.

## 🌌 Philosophy

The "void" represents a topological limit state without metric, time, or space. Through quantum fluctuations and symmetry breaking, this void can nucleate spacetime domains, giving rise to the observable universe. This module implements the mathematical formalism to model and visualize this profound concept.

### Key Concepts

- **Void State**: A topological limit with perfect symmetry, no metric, no time
- **Quantum Fluctuations**: Stochastic processes that break symmetry
- **Field Evolution**: Scalar field φ(t) rolling from void to ordered states
- **Time Emergence**: Time's arrow emerges from entropy gradient
- **Spacetime Formation**: Metric g_μν forms from field dynamics

## 📐 Mathematical Formalism

### Effective Action

The core mathematical framework is based on an effective action:

```
S[φ,g] = ∫d⁴x √(-g) [R/(2κ) - (1/2)g^μν ∂_μφ ∂_νφ - V(φ) + L_matter]
```

where:
- `R` is the Ricci scalar
- `κ = 8πG` is Einstein's gravitational constant
- `φ` is the scalar field (order parameter)
- `V(φ)` is the potential function
- `L_matter` describes matter/antimatter interactions

### Double-Well Potential

The potential function describes symmetry breaking:

```
V(φ) = (λ/4)(φ² - v²)² + V₀
```

- `φ = 0`: Symmetric "void" state (metastable)
- `φ = ±v`: Broken symmetry "vacuum" states (stable)
- `λ`: Self-coupling strength
- `v`: Vacuum expectation value

### Langevin Dynamics

Field evolution follows stochastic dynamics:

```
dφ/dt = -Γ dV/dφ + η(t)
```

where:
- `Γ` is the friction coefficient
- `η(t)` is white noise (quantum fluctuations)
- The noise represents "void strength"

### Time Emergence

Time emerges from entropy gradient:

```
t ∝ ∫ dS/R(S)
```

where `R(S)` is the entropy production rate.

## 🚀 Installation

### Prerequisites

- Python 3.11 or higher
- FFmpeg (for video rendering)
- LaTeX (optional, for equation rendering)

### Using uv (Recommended)

```bash
# Clone the repository
git clone https://github.com/void-physic/void-physic.git
cd void-physic

# Install with uv
uv sync

# Activate the environment
uv shell
```

### Using pip

```bash
# Install from source
pip install -e .

# Or install dependencies manually
pip install manimgl sympy numpy scipy matplotlib numba pytest
```

## 🎯 Quick Start

### 1. Run the Toy Model

```python
from void_physic.core.potential import DoubleWellPotential
from void_physic.core.stochastic import LangevinDynamics, WhiteNoise
from void_physic.simulation.langevin_solver import LangevinSolver

# Set up parameters
potential = DoubleWellPotential()
noise = WhiteNoise(strength=0.5)
dynamics = LangevinDynamics(potential, noise)
solver = LangevinSolver(dynamics)

# Run simulation
results = solver.ensemble_simulation(phi0=0.0, n_trajectories=1000)
print(f"Final mean field: {results['mean_field'][-1]:.3f}")
```

### 2. Generate Visualizations

```python
# Run the complete example
python examples/toy_model_0d.py
```

### 3. Create Manim Animations

```python
# Render the main void emergence scene
manimgl examples/void_emergence.py VoidEmergenceScene

# Render individual scenes
manimgl src/void_physic/visualization/potential_landscape.py PotentialLandscapeScene
manimgl src/void_physic/visualization/field_evolution.py FieldEvolutionScene
manimgl src/void_physic/visualization/entropy_time.py EntropyTimeScene
```

## 📊 Examples

### Toy Model (0D)

The `examples/toy_model_0d.py` demonstrates:

- Stochastic field evolution in double-well potential
- First passage time analysis
- Entropy evolution and time emergence
- Parameter dependence studies
- Statistical analysis of nucleation events

### Visualization Scenes

#### Potential Landscape
- 3D visualization of double-well potential
- Ball rolling animation
- Quantum tunneling visualization
- Instanton trajectory overlay

#### Field Evolution
- Multiple stochastic trajectories
- Ensemble statistics (mean, variance)
- Phase portrait (φ, dφ/dt)
- Probability density evolution

#### Entropy-Time Connection
- Entropy S(t) evolution
- Entropy production rate dS/dt
- Time's arrow emergence
- Thermodynamic quantities

#### Complete Narrative
- 4-act story: Void → Instability → Emergence → Time's Arrow
- Philosophical and mathematical aspects
- 3D visualizations

## 🔬 Scientific Background

This module is inspired by and connects to several areas of theoretical physics:

### Quantum Cosmology
- Hartle-Hawking no-boundary proposal
- Wheeler-DeWitt equation
- Quantum tunneling in cosmology

### Field Theory
- Spontaneous symmetry breaking
- Instanton solutions
- Effective field theory

### Statistical Mechanics
- Stochastic processes
- First passage time theory
- Entropy production

### Cosmology
- Inflationary models
- Phase transitions in early universe
- Baryon asymmetry

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/void_physic

# Run specific test categories
pytest tests/test_potential.py
pytest tests/test_stochastic.py
pytest tests/test_simulation.py
```

## 📚 API Reference

### Core Physics

- `DoubleWellPotential`: Double-well potential with symmetry breaking
- `LangevinDynamics`: Stochastic field evolution
- `WhiteNoise`: Quantum fluctuation model
- `InstantonSolver`: Tunneling probability calculations

### Simulation

- `LangevinSolver`: Numerical integration of stochastic equations
- `FirstPassageTime`: Statistical analysis of nucleation events
- `EntropyCalculator`: Entropy and thermodynamic quantities

### Visualization

- `VoidEmergenceScene`: Complete 4-act narrative animation
- `PotentialLandscapeScene`: Potential visualization
- `FieldEvolutionScene`: Field dynamics visualization
- `EntropyTimeScene`: Entropy and time emergence

## 🔮 Future Work

### Planned Extensions

1. **Lattice Field Theory**: Path integral Monte Carlo simulations
2. **Full General Relativity**: Complete Einstein field equations
3. **Quantum Field Theory**: Full QFT treatment with renormalization
4. **Cosmological Applications**: Connection to CMB and large-scale structure
5. **Machine Learning**: AI-assisted parameter optimization

### Research Directions

- Connection to string theory and M-theory
- Quantum gravity applications
- Multiverse scenarios
- Information theory and black holes

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Setup

```bash
# Clone and install in development mode
git clone https://github.com/void-physic/void-physic.git
cd void-physic
uv sync --dev

# Run tests
uv run pytest

# Format code
uv run black src/ tests/
uv run isort src/ tests/

# Type checking
uv run mypy src/
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- 3Blue1Brown for the Manim animation engine
- The theoretical physics community for foundational concepts
- Contributors and users of this project

## 📖 References

1. Hartle, J. B., & Hawking, S. W. (1983). Wave function of the Universe. Physical Review D, 28(12), 2960.
2. Coleman, S. (1977). The fate of the false vacuum: Semiclassical theory. Physical Review D, 15(10), 2929.
3. Guth, A. H. (1981). Inflationary universe: A possible solution to the horizon and flatness problems. Physical Review D, 23(2), 347.
4. Linde, A. (1982). A new inflationary universe scenario: A possible solution of the horizon, flatness, homogeneity, isotropy and primordial monopole problems. Physics Letters B, 108(6), 389-393.

## 🌟 Star the Repository

If you find this project interesting or useful, please consider starring it on GitHub!

---

*"The void contains all possibilities. From the void, everything emerges."*
