"""
Void Physics Module

A mathematical modeling and visualization framework for "void physics" -
the emergence of spacetime, matter, and time from a primordial topological void state.

This module implements:
- Lagrangian formalism for effective field theory
- Stochastic dynamics (Langevin equations) for void → spacetime transitions
- Instanton calculations for tunneling probabilities
- Numerical simulations and statistical analysis
- Manim-based visualizations of the emergence process

Philosophical Foundation:
The "void" represents a topological limit state without metric, time, or space.
Through quantum fluctuations and symmetry breaking, this void can nucleate
spacetime domains, giving rise to the observable universe.

Mathematical Framework:
- Effective action: S[φ,g] = ∫d⁴x √(-g) [R/(2κ) - (1/2)g^μν ∂_μφ ∂_νφ - V(φ)]
- Double-well potential: V(φ) = (λ/4)(φ² - v²)² + V₀
- Langevin dynamics: dφ/dt = -Γ dV/dφ + η(t)
- Tunneling probability: P ~ exp(-S_E/ℏ)

Author: Void Physics Research
License: MIT
"""

__version__ = "0.1.0"
__author__ = "Void Physics Research"
__email__ = "research@void-physic.org"

from void_physic.core.instanton import InstantonSolver, TunnelingProbability
from void_physic.core.lagrangian import EffectiveAction, FieldEquations

# Core physics modules
from void_physic.core.potential import DoubleWellPotential, MexicanHatPotential
from void_physic.core.stochastic import LangevinDynamics, WhiteNoise

# Numerical simulation modules
from void_physic.simulation.langevin_solver import LangevinSolver
from void_physic.simulation.statistics import EntropyCalculator, FirstPassageTime

# Utility modules
from void_physic.utils.constants import PhysicalConstants
from void_physic.utils.symbolic import SymbolicMath

__all__ = [
    # Core physics
    "DoubleWellPotential",
    "MexicanHatPotential",
    "EffectiveAction",
    "FieldEquations",
    "LangevinDynamics",
    "WhiteNoise",
    "InstantonSolver",
    "TunnelingProbability",
    # Simulation
    "LangevinSolver",
    "FirstPassageTime",
    "EntropyCalculator",
    # Utils
    "PhysicalConstants",
    "SymbolicMath",
]
