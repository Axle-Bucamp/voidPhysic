"""
Quantum Mechanics Module for Void Physics

This module implements quantum mechanical equations and solvers that extend
the void physics framework with quantum field theory concepts.

Key Components:
- Schrodinger equation solver with split-operator FFT method
- Relativistic quantum equations (Klein-Gordon, Dirac)
- Quantum field theory operators and field evolution
- Probability current and density calculations
- Integration with void physics emergence mechanisms

Mathematical Foundation:
- Schrodinger: iℏ ∂Ψ/∂t = ĤΨ
- Probability current: j = (ℏ/2mi)(Ψ*∇Ψ - Ψ∇Ψ*)
- Quantum potential: V_quantum = -(ℏ²/2m)(∇²√ρ)/√ρ
- Field operators: â†, â for particle creation/annihilation

Author: Void Physics Research
License: MIT
"""

from .operators import Hamiltonian, MomentumOperator, EnergyOperator
from .schrodinger import SchrodingerSolver, WaveFunction, ProbabilityCurrent
from .relativistic import KleinGordonSolver, DiracSolver
from .field_theory import QuantumField, FieldOperator, ParticleCreation

__all__ = [
    # Operators
    "Hamiltonian",
    "MomentumOperator", 
    "EnergyOperator",
    # Schrodinger
    "SchrodingerSolver",
    "WaveFunction",
    "ProbabilityCurrent",
    # Relativistic
    "KleinGordonSolver",
    "DiracSolver",
    # Field Theory
    "QuantumField",
    "FieldOperator",
    "ParticleCreation",
]
