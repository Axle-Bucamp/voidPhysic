"""
Physical constants and parameters for void physics calculations.

This module defines the fundamental constants used throughout the void physics
framework, including Planck units, coupling constants, and model parameters.
"""

from dataclasses import dataclass
from typing import Any, Dict

import numpy as np


@dataclass
class PhysicalConstants:
    """
    Physical constants for void physics calculations.

    All values are in natural units where ℏ = c = 1, unless otherwise specified.
    """

    # Fundamental constants
    hbar: float = 1.0  # Reduced Planck constant (natural units)
    c: float = 1.0  # Speed of light (natural units)
    G: float = 6.674e-11  # Newton's gravitational constant (SI units)
    kappa: float = 8 * np.pi * 6.674e-11  # Einstein's gravitational constant

    # Model parameters for double-well potential
    lambda_coupling: float = 1.0  # Self-coupling strength λ
    v_vev: float = 1.0  # Vacuum expectation value v
    V0_offset: float = 0.0  # Potential offset V₀

    # Stochastic dynamics parameters
    gamma_friction: float = 1.0  # Friction coefficient Γ
    noise_strength: float = 1.0  # Noise amplitude (related to "void strength")

    # Numerical parameters
    dt_default: float = 0.01  # Default timestep
    n_trajectories: int = 1000  # Default number of stochastic trajectories

    # Cosmological parameters (for connection to observations)
    H0: float = 2.2e-18  # Hubble constant (s⁻¹)
    rho_critical: float = 9.47e-27  # Critical density (kg/m³)

    def to_dict(self) -> Dict[str, Any]:
        """Convert constants to dictionary for easy serialization."""
        return {
            "hbar": self.hbar,
            "c": self.c,
            "G": self.G,
            "kappa": self.kappa,
            "lambda_coupling": self.lambda_coupling,
            "v_vev": self.v_vev,
            "V0_offset": self.V0_offset,
            "gamma_friction": self.gamma_friction,
            "noise_strength": self.noise_strength,
            "dt_default": self.dt_default,
            "n_trajectories": self.n_trajectories,
            "H0": self.H0,
            "rho_critical": self.rho_critical,
        }

    @classmethod
    def from_dict(cls, params: Dict[str, Any]) -> "PhysicalConstants":
        """Create constants from dictionary."""
        return cls(**params)

    def get_planck_units(self) -> Dict[str, float]:
        """
        Get Planck units for dimensional analysis.

        Returns:
            Dictionary with Planck length, time, mass, and energy
        """
        # Planck length: l_P = √(ℏG/c³)
        l_planck = np.sqrt(self.hbar * self.G / (self.c**3))

        # Planck time: t_P = √(ℏG/c⁵)
        t_planck = np.sqrt(self.hbar * self.G / (self.c**5))

        # Planck mass: m_P = √(ℏc/G)
        m_planck = np.sqrt(self.hbar * self.c / self.G)

        # Planck energy: E_P = √(ℏc⁵/G)
        e_planck = np.sqrt(self.hbar * (self.c**5) / self.G)

        return {
            "length": l_planck,
            "time": t_planck,
            "mass": m_planck,
            "energy": e_planck,
        }


# Default constants instance
DEFAULT_CONSTANTS = PhysicalConstants()


def get_constants(**kwargs) -> PhysicalConstants:
    """
    Get physical constants with optional overrides.

    Args:
        **kwargs: Parameter overrides

    Returns:
        PhysicalConstants instance with specified parameters
    """
    params = DEFAULT_CONSTANTS.to_dict()
    params.update(kwargs)
    return PhysicalConstants.from_dict(params)
