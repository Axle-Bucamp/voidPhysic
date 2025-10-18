"""
Lagrangian formalism for void physics field theory.

This module implements the effective action and field equations for void physics,
including the scalar field dynamics and simplified gravitational coupling.
"""

from dataclasses import dataclass
from typing import Any, Callable, Dict, Optional, Tuple

import numpy as np
import sympy as sp

from ..utils.constants import PhysicalConstants
from .potential import DoubleWellPotential, PotentialParameters


@dataclass
class MetricComponents:
    """Components of the spacetime metric g_μν."""

    g00: float = -1.0  # Time-time component (Minkowski: -1)
    g11: float = 1.0  # Space-space components (Minkowski: +1)
    g22: float = 1.0
    g33: float = 1.0
    g01: float = 0.0  # Off-diagonal components (Minkowski: 0)
    g02: float = 0.0
    g03: float = 0.0
    g12: float = 0.0
    g13: float = 0.0
    g23: float = 0.0


class EffectiveAction:
    """
    Effective action for void physics: S[φ,g] = ∫d⁴x √(-g) L

    where L = R/(2κ) - (1/2)g^μν ∂_μφ ∂_νφ - V(φ) + L_matter

    This action describes the dynamics of a scalar field φ coupled to gravity
    in the context of void physics. The scalar field represents the order
    parameter for the void → spacetime transition.
    """

    def __init__(
        self,
        potential: Optional[DoubleWellPotential] = None,
        constants: Optional[PhysicalConstants] = None,
    ):
        """
        Initialize effective action.

        Args:
            potential: Scalar field potential (uses default double-well if None)
            constants: Physical constants (uses default if None)
        """
        self.potential = potential or DoubleWellPotential()
        self.constants = constants or PhysicalConstants()

    def lagrangian_density(
        self,
        phi: np.ndarray,
        dphi_dt: np.ndarray,
        dphi_dx: np.ndarray,
        metric: Optional[MetricComponents] = None,
    ) -> np.ndarray:
        """
        Calculate Lagrangian density L.

        Args:
            phi: Scalar field values
            dphi_dt: Time derivatives ∂φ/∂t
            dphi_dx: Spatial derivatives ∂φ/∂x (assumed isotropic)
            metric: Spacetime metric (uses Minkowski if None)

        Returns:
            Lagrangian density values
        """
        if metric is None:
            metric = MetricComponents()

        # Kinetic term: (1/2)g^μν ∂_μφ ∂_νφ
        # For Minkowski metric: (1/2)[-(∂φ/∂t)² + (∇φ)²]
        kinetic = 0.5 * (-metric.g00 * dphi_dt**2 + metric.g11 * dphi_dx**2)

        # Potential term
        potential_term = self.potential(phi)

        # Total Lagrangian density (excluding gravity for now)
        return kinetic - potential_term

    def action_density(
        self,
        phi: np.ndarray,
        dphi_dt: np.ndarray,
        dphi_dx: np.ndarray,
        metric: Optional[MetricComponents] = None,
    ) -> np.ndarray:
        """
        Calculate action density (Lagrangian density times √(-g)).

        Args:
            phi: Scalar field values
            dphi_dt: Time derivatives
            dphi_dx: Spatial derivatives
            metric: Spacetime metric

        Returns:
            Action density values
        """
        if metric is None:
            metric = MetricComponents()

        # Determinant of metric: g = det(g_μν)
        # For Minkowski: g = -1, so √(-g) = 1
        sqrt_g = 1.0  # Simplified for Minkowski spacetime

        lagrangian = self.lagrangian_density(phi, dphi_dt, dphi_dx, metric)
        return sqrt_g * lagrangian

    def hamiltonian_density(
        self,
        phi: np.ndarray,
        pi: np.ndarray,
        dphi_dx: np.ndarray,
        metric: Optional[MetricComponents] = None,
    ) -> np.ndarray:
        """
        Calculate Hamiltonian density H = π φ̇ - L.

        Args:
            phi: Scalar field values
            pi: Canonical momentum π = ∂L/∂φ̇
            dphi_dx: Spatial derivatives
            metric: Spacetime metric

        Returns:
            Hamiltonian density values
        """
        if metric is None:
            metric = MetricComponents()

        # From Lagrangian: π = ∂L/∂φ̇ = -g^00 φ̇ = φ̇ (for Minkowski)
        dphi_dt = pi  # Canonical momentum relation

        # Hamiltonian density
        kinetic = 0.5 * (pi**2 + metric.g11 * dphi_dx**2)
        potential_term = self.potential(phi)

        return kinetic + potential_term

    def energy_density(
        self, phi: np.ndarray, dphi_dt: np.ndarray, dphi_dx: np.ndarray
    ) -> np.ndarray:
        """
        Calculate energy density T₀₀.

        Args:
            phi: Scalar field values
            dphi_dt: Time derivatives
            dphi_dx: Spatial derivatives

        Returns:
            Energy density values
        """
        kinetic = 0.5 * (dphi_dt**2 + dphi_dx**2)
        potential_term = self.potential(phi)
        return kinetic + potential_term

    def pressure_density(
        self, phi: np.ndarray, dphi_dt: np.ndarray, dphi_dx: np.ndarray
    ) -> np.ndarray:
        """
        Calculate pressure density Tᵢᵢ (isotropic).

        Args:
            phi: Scalar field values
            dphi_dt: Time derivatives
            dphi_dx: Spatial derivatives

        Returns:
            Pressure density values
        """
        kinetic = 0.5 * (dphi_dt**2 - dphi_dx**2)
        potential_term = self.potential(phi)
        return kinetic - potential_term


class FieldEquations:
    """
    Field equations derived from the effective action.

    This class implements the Euler-Lagrange equations for the scalar field
    and simplified Einstein equations for the metric.
    """

    def __init__(
        self,
        potential: Optional[DoubleWellPotential] = None,
        constants: Optional[PhysicalConstants] = None,
    ):
        """
        Initialize field equations.

        Args:
            potential: Scalar field potential
            constants: Physical constants
        """
        self.potential = potential or DoubleWellPotential()
        self.constants = constants or PhysicalConstants()

    def klein_gordon_equation(
        self,
        phi: np.ndarray,
        dphi_dt: np.ndarray,
        d2phi_dt2: np.ndarray,
        d2phi_dx2: np.ndarray,
    ) -> np.ndarray:
        """
        Klein-Gordon equation: □φ + dV/dφ = 0

        where □ = g^μν ∂_μ ∂_ν is the d'Alembertian operator.

        Args:
            phi: Scalar field values
            dphi_dt: First time derivatives
            d2phi_dt2: Second time derivatives
            d2phi_dx2: Second spatial derivatives (Laplacian)

        Returns:
            Klein-Gordon equation residuals (should be zero)
        """
        # d'Alembertian: □φ = -∂²φ/∂t² + ∇²φ (Minkowski)
        d_alembertian = -d2phi_dt2 + d2phi_dx2

        # Potential gradient
        dV_dphi = self.potential.gradient(phi)

        # Klein-Gordon equation: □φ + dV/dφ = 0
        return d_alembertian + dV_dphi

    def euler_lagrange_equation(
        self,
        phi: np.ndarray,
        dphi_dt: np.ndarray,
        d2phi_dt2: np.ndarray,
        d2phi_dx2: np.ndarray,
    ) -> np.ndarray:
        """
        Euler-Lagrange equation for the scalar field.

        This is equivalent to the Klein-Gordon equation but derived directly
        from the Lagrangian formalism.

        Args:
            phi: Scalar field values
            dphi_dt: First time derivatives
            d2phi_dt2: Second time derivatives
            d2phi_dx2: Second spatial derivatives

        Returns:
            Euler-Lagrange equation residuals
        """
        return self.klein_gordon_equation(phi, dphi_dt, d2phi_dt2, d2phi_dx2)

    def stress_energy_tensor(
        self, phi: np.ndarray, dphi_dt: np.ndarray, dphi_dx: np.ndarray
    ) -> Dict[str, np.ndarray]:
        """
        Calculate stress-energy tensor T_μν for the scalar field.

        Args:
            phi: Scalar field values
            dphi_dt: Time derivatives
            dphi_dx: Spatial derivatives

        Returns:
            Dictionary with stress-energy tensor components
        """
        # Energy density T₀₀
        T00 = 0.5 * (dphi_dt**2 + dphi_dx**2) + self.potential(phi)

        # Momentum density T₀ᵢ (isotropic)
        T0i = dphi_dt * dphi_dx

        # Pressure Tᵢᵢ (isotropic)
        Tii = 0.5 * (dphi_dt**2 - dphi_dx**2) - self.potential(phi)

        # Off-diagonal components (assumed zero for isotropic field)
        Tij = np.zeros_like(phi)

        return {
            "T00": T00,
            "T0i": T0i,
            "Tii": Tii,
            "Tij": Tij,
        }

    def einstein_equations(
        self,
        phi: np.ndarray,
        dphi_dt: np.ndarray,
        dphi_dx: np.ndarray,
        metric: Optional[MetricComponents] = None,
    ) -> Dict[str, np.ndarray]:
        """
        Simplified Einstein equations: G_μν = κ T_μν

        For simplicity, we assume a flat background metric and calculate
        the stress-energy tensor as the source.

        Args:
            phi: Scalar field values
            dphi_dt: Time derivatives
            dphi_dx: Spatial derivatives
            metric: Background metric (uses Minkowski if None)

        Returns:
            Dictionary with Einstein equation components
        """
        if metric is None:
            metric = MetricComponents()

        # Calculate stress-energy tensor
        T_mu_nu = self.stress_energy_tensor(phi, dphi_dt, dphi_dx)

        # For flat background, Einstein tensor G_μν = 0
        # So the equations become: 0 = κ T_μν
        # This gives us constraints on the field configuration

        einstein_equations = {}
        for component, T_value in T_mu_nu.items():
            einstein_equations[component] = self.constants.kappa * T_value

        return einstein_equations

    def conservation_equation(
        self,
        phi: np.ndarray,
        dphi_dt: np.ndarray,
        dphi_dx: np.ndarray,
        d2phi_dt2: np.ndarray,
        d2phi_dx2: np.ndarray,
    ) -> np.ndarray:
        """
        Energy-momentum conservation: ∇_μ T^μν = 0

        This provides a consistency check for the field equations.

        Args:
            phi: Scalar field values
            dphi_dt: First time derivatives
            dphi_dx: First spatial derivatives
            d2phi_dt2: Second time derivatives
            d2phi_dx2: Second spatial derivatives

        Returns:
            Conservation equation residuals (should be zero)
        """
        # For a scalar field, conservation reduces to the Klein-Gordon equation
        return self.klein_gordon_equation(phi, dphi_dt, d2phi_dt2, d2phi_dx2)

    def to_sympy(self) -> Dict[str, sp.Expr]:
        """
        Convert field equations to SymPy expressions for symbolic manipulation.

        Returns:
            Dictionary with SymPy expressions for the equations
        """
        # Define symbolic variables
        phi = sp.Symbol("phi", real=True)
        t = sp.Symbol("t", real=True)
        x = sp.Symbol("x", real=True)

        # Define field as function of spacetime
        phi_func = sp.Function("phi")(t, x)

        # Klein-Gordon equation
        d2phi_dt2 = sp.diff(phi_func, t, 2)
        d2phi_dx2 = sp.diff(phi_func, x, 2)
        dV_dphi = self.potential.gradient(sp.array([phi]))[0]  # Convert to symbolic

        klein_gordon = -d2phi_dt2 + d2phi_dx2 + dV_dphi

        return {
            "klein_gordon": klein_gordon,
            "phi_function": phi_func,
        }
