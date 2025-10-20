"""
Potential functions for void physics field theory.

This module implements various potential functions used in void physics,
including the double-well potential for symmetry breaking and the Mexican-hat
potential for more complex phase transitions.
"""

from dataclasses import dataclass
from typing import Any, Callable, Dict, Optional, Tuple

import numpy as np
import sympy as sp

from ..utils.constants import PhysicalConstants


@dataclass
class PotentialParameters:
    """Parameters for potential functions."""

    lambda_coupling: float = 1.0  # Self-coupling strength λ
    v_vev: float = 1.0  # Vacuum expectation value v
    V0_offset: float = 0.0  # Potential offset V₀
    mass_squared: float = 0.0  # Mass parameter m²


class DoubleWellPotential:
    """
    Double-well potential: V(φ) = (λ/4)(φ² - v²)² + V₀

    This potential describes symmetry breaking from a symmetric state (φ=0)
    to broken symmetry states (φ=±v). The symmetric state represents the
    "void" - a metastable configuration that can nucleate ordered domains.

    Physical interpretation:
    - φ=0: Symmetric "void" state (local maximum, unstable)
    - φ=±v: Broken symmetry "vacuum" states (global minima, stable)
    - λ: Controls the strength of self-interaction
    - v: Sets the scale of symmetry breaking
    """

    def __init__(self, params: Optional[PotentialParameters] = None):
        """
        Initialize double-well potential.

        Args:
            params: Potential parameters (uses default if None)
        """
        self.params = params or PotentialParameters()

    def __call__(self, phi: np.ndarray) -> np.ndarray:
        """
        Evaluate potential at given field values.

        Args:
            phi: Field values (can be scalar or array)

        Returns:
            Potential values
        """
        return (self.params.lambda_coupling / 4) * (
            phi**2 - self.params.v_vev**2
        ) ** 2 + self.params.V0_offset

    def gradient(self, phi: np.ndarray) -> np.ndarray:
        """
        Gradient of potential: dV/dφ

        Args:
            phi: Field values

        Returns:
            Gradient values
        """
        # Prevent overflow by clipping large values
        phi_safe = np.clip(phi, -1e6, 1e6)
        return (
            self.params.lambda_coupling
            * phi_safe
            * (phi_safe**2 - self.params.v_vev**2)
        )

    def hessian(self, phi: np.ndarray) -> np.ndarray:
        """
        Second derivative: d²V/dφ²

        Args:
            phi: Field values

        Returns:
            Hessian values
        """
        return self.params.lambda_coupling * (3 * phi**2 - self.params.v_vev**2)

    def critical_points(self) -> Dict[str, float]:
        """
        Find critical points where dV/dφ = 0.

        Returns:
            Dictionary mapping point names to φ values
        """
        # Solve: λφ(φ² - v²) = 0
        # Solutions: φ = 0, φ = ±v
        return {
            "symmetric": 0.0,
            "positive_vacuum": self.params.v_vev,
            "negative_vacuum": -self.params.v_vev,
        }
    
    def quantum_potential(self, psi: np.ndarray, x_grid: np.ndarray, 
                         mass: float = 1.0, hbar: float = 1.0) -> np.ndarray:
        """
        Add quantum potential: V_quantum = -(ℏ²/2m)(∇²√ρ)/√ρ
        
        This represents the "quantum force" that emerges from the wave function
        and can be related to void physics emergence mechanisms.
        
        Args:
            psi: Wave function
            x_grid: Spatial grid
            mass: Particle mass
            hbar: Reduced Planck constant
            
        Returns:
            Quantum potential values
        """
        # Probability density
        rho = np.abs(psi)**2
        
        # Avoid division by zero
        rho_safe = np.maximum(rho, 1e-10)
        sqrt_rho = np.sqrt(rho_safe)
        
        # Calculate second derivative of √ρ
        dx = x_grid[1] - x_grid[0]
        d2_sqrt_rho_dx2 = np.gradient(np.gradient(sqrt_rho, dx), dx)
        
        # Quantum potential
        V_quantum = -(hbar**2 / (2 * mass)) * d2_sqrt_rho_dx2 / sqrt_rho
        
        return V_quantum.real  # Should be real
    
    def tunneling_probability(self, psi: np.ndarray, x_grid: np.ndarray,
                             barrier_region: Tuple[float, float]) -> float:
        """
        Calculate quantum tunneling probability through potential barrier.
        
        Args:
            psi: Wave function
            x_grid: Spatial grid
            barrier_region: (x_min, x_max) defining barrier region
            
        Returns:
            Tunneling probability
        """
        x_min, x_max = barrier_region
        
        # Find indices corresponding to barrier region
        barrier_mask = (x_grid >= x_min) & (x_grid <= x_max)
        
        # Calculate probability inside barrier
        dx = x_grid[1] - x_grid[0]
        barrier_probability = np.sum(np.abs(psi)**2[barrier_mask]) * dx
        
        return barrier_probability
    
    def quantum_barrier_penetration(self, psi: np.ndarray, x_grid: np.ndarray,
                                   mass: float = 1.0, hbar: float = 1.0) -> Dict[str, float]:
        """
        Calculate quantum barrier penetration properties.
        
        Args:
            psi: Wave function
            x_grid: Spatial grid
            mass: Particle mass
            hbar: Reduced Planck constant
            
        Returns:
            Dictionary with penetration properties
        """
        # Find potential barrier (where V > 0 and dV/dx changes sign)
        phi_values = np.linspace(-2*self.params.v_vev, 2*self.params.v_vev, 1000)
        V_values = self(phi_values)
        
        # Find barrier height
        barrier_height = np.max(V_values)
        
        # Calculate quantum potential
        V_quantum = self.quantum_potential(psi, x_grid, mass, hbar)
        
        # Effective potential (classical + quantum)
        V_effective = V_values + V_quantum
        
        # Tunneling coefficient (WKB approximation)
        # T ≈ exp(-2∫√(2m(V-E)/ℏ²)dx)
        E_kinetic = hbar**2 / (2 * mass) * np.max(np.abs(np.gradient(psi, x_grid))**2)
        
        if barrier_height > E_kinetic:
            # Classical turning points
            turning_points = np.where(V_values > E_kinetic)[0]
            if len(turning_points) > 0:
                # Simple tunneling estimate
                barrier_width = len(turning_points) * (phi_values[1] - phi_values[0])
                tunneling_coefficient = np.exp(-2 * np.sqrt(2 * mass * (barrier_height - E_kinetic)) * barrier_width / hbar)
            else:
                tunneling_coefficient = 1.0
        else:
            tunneling_coefficient = 1.0
        
        return {
            'barrier_height': barrier_height,
            'quantum_potential_max': np.max(V_quantum),
            'effective_potential_max': np.max(V_effective),
            'tunneling_coefficient': tunneling_coefficient,
            'kinetic_energy': E_kinetic
        }

    def stability_analysis(self) -> Dict[str, Dict[str, Any]]:
        """
        Analyze stability of critical points.

        Returns:
            Dictionary with stability information for each critical point
        """
        critical_points = self.critical_points()
        stability = {}

        for name, phi_val in critical_points.items():
            d2V = self.hessian(np.array([phi_val]))[0]

            if d2V > 0:
                stability[name] = {
                    "type": "stable",
                    "mass_squared": d2V,
                    "description": "Local minimum",
                }
            elif d2V < 0:
                stability[name] = {
                    "type": "unstable",
                    "mass_squared": d2V,
                    "description": "Local maximum",
                }
            else:
                stability[name] = {
                    "type": "marginal",
                    "mass_squared": d2V,
                    "description": "Saddle point",
                }

        return stability

    def barrier_height(self) -> float:
        """
        Height of the potential barrier between vacua.

        Returns:
            Barrier height (V(0) - V(±v))
        """
        V_symmetric = self(np.array([0.0]))[0]
        V_vacuum = self(np.array([self.params.v_vev]))[0]
        return V_symmetric - V_vacuum

    def effective_mass(self, phi: float) -> float:
        """
        Effective mass at given field value: m_eff² = d²V/dφ²

        Args:
            phi: Field value

        Returns:
            Effective mass squared
        """
        return self.hessian(np.array([phi]))[0]

    def to_sympy(self) -> sp.Expr:
        """
        Convert to SymPy expression for symbolic manipulation.

        Returns:
            SymPy expression for the potential
        """
        phi = sp.Symbol("phi", real=True)
        return (self.params.lambda_coupling / 4) * (
            phi**2 - self.params.v_vev**2
        ) ** 2 + self.params.V0_offset


class MexicanHatPotential:
    """
    Mexican-hat potential: V(φ) = (λ/4)(|φ|² - v²)² + V₀

    This is a complex field version of the double-well potential, where
    φ is a complex scalar field. The potential has a U(1) symmetry that
    can be spontaneously broken.

    Physical interpretation:
    - |φ|=0: Symmetric "void" state (local maximum, unstable)
    - |φ|=v: Broken symmetry "vacuum" manifold (global minimum, stable)
    - The vacuum manifold is a circle in the complex plane
    """

    def __init__(self, params: Optional[PotentialParameters] = None):
        """
        Initialize Mexican-hat potential.

        Args:
            params: Potential parameters (uses default if None)
        """
        self.params = params or PotentialParameters()

    def __call__(self, phi_real: np.ndarray, phi_imag: np.ndarray) -> np.ndarray:
        """
        Evaluate potential at given complex field values.

        Args:
            phi_real: Real part of field
            phi_imag: Imaginary part of field

        Returns:
            Potential values
        """
        phi_magnitude_squared = phi_real**2 + phi_imag**2
        return (self.params.lambda_coupling / 4) * (
            phi_magnitude_squared - self.params.v_vev**2
        ) ** 2 + self.params.V0_offset

    def gradient_real(self, phi_real: np.ndarray, phi_imag: np.ndarray) -> np.ndarray:
        """
        Gradient with respect to real part: ∂V/∂φ_real

        Args:
            phi_real: Real part of field
            phi_imag: Imaginary part of field

        Returns:
            Gradient values
        """
        phi_magnitude_squared = phi_real**2 + phi_imag**2
        return (
            self.params.lambda_coupling
            * phi_real
            * (phi_magnitude_squared - self.params.v_vev**2)
        )

    def gradient_imag(self, phi_real: np.ndarray, phi_imag: np.ndarray) -> np.ndarray:
        """
        Gradient with respect to imaginary part: ∂V/∂φ_imag

        Args:
            phi_real: Real part of field
            phi_imag: Imaginary part of field

        Returns:
            Gradient values
        """
        phi_magnitude_squared = phi_real**2 + phi_imag**2
        return (
            self.params.lambda_coupling
            * phi_imag
            * (phi_magnitude_squared - self.params.v_vev**2)
        )

    def critical_points(self) -> Dict[str, Tuple[float, float]]:
        """
        Find critical points where gradients vanish.

        Returns:
            Dictionary mapping point names to (φ_real, φ_imag) values
        """
        return {
            "symmetric": (0.0, 0.0),
            "vacuum_manifold": (self.params.v_vev, 0.0),  # Representative point
        }

    def vacuum_manifold(self, n_points: int = 100) -> Tuple[np.ndarray, np.ndarray]:
        """
        Generate points on the vacuum manifold (circle |φ| = v).

        Args:
            n_points: Number of points to generate

        Returns:
            Tuple of (phi_real, phi_imag) arrays
        """
        theta = np.linspace(0, 2 * np.pi, n_points)
        phi_real = self.params.v_vev * np.cos(theta)
        phi_imag = self.params.v_vev * np.sin(theta)
        return phi_real, phi_imag


class PlateauPotential:
    """
    Plateau potential for slow-roll inflation scenarios.

    V(φ) = V₀ * (1 - exp(-√(2/3) * φ/M_Pl))²

    This potential has a flat plateau at large φ values, suitable for
    modeling the transition from void to inflating spacetime.
    """

    def __init__(self, V0: float = 1.0, M_Pl: float = 1.0):
        """
        Initialize plateau potential.

        Args:
            V0: Potential scale
            M_Pl: Planck mass
        """
        self.V0 = V0
        self.M_Pl = M_Pl
        self.alpha = np.sqrt(2 / 3)  # Starobinsky parameter

    def __call__(self, phi: np.ndarray) -> np.ndarray:
        """
        Evaluate plateau potential.

        Args:
            phi: Field values

        Returns:
            Potential values
        """
        exponent = -self.alpha * phi / self.M_Pl
        return self.V0 * (1 - np.exp(exponent)) ** 2

    def gradient(self, phi: np.ndarray) -> np.ndarray:
        """
        Gradient of plateau potential.

        Args:
            phi: Field values

        Returns:
            Gradient values
        """
        exponent = -self.alpha * phi / self.M_Pl
        return (
            2
            * self.V0
            * self.alpha
            / self.M_Pl
            * np.exp(exponent)
            * (1 - np.exp(exponent))
        )

    def slow_roll_parameters(self, phi: float) -> Tuple[float, float]:
        """
        Calculate slow-roll parameters ε and η.

        Args:
            phi: Field value

        Returns:
            Tuple of (epsilon, eta) slow-roll parameters
        """
        V = self(np.array([phi]))[0]
        dV = self.gradient(np.array([phi]))[0]
        d2V = self.hessian(np.array([phi]))[0]

        epsilon = 0.5 * (dV / V) ** 2
        eta = d2V / V

        return epsilon, eta

    def hessian(self, phi: np.ndarray) -> np.ndarray:
        """
        Second derivative of plateau potential.

        Args:
            phi: Field values

        Returns:
            Hessian values
        """
        exponent = -self.alpha * phi / self.M_Pl
        return (
            2
            * self.V0
            * (self.alpha / self.M_Pl) ** 2
            * np.exp(exponent)
            * (2 * np.exp(exponent) - 1)
        )
