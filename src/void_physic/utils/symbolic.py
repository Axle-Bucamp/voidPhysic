"""
Symbolic mathematics utilities using SymPy.

This module provides symbolic computation capabilities for void physics,
including automatic differentiation, equation derivation, and LaTeX rendering.
"""

from typing import Any, Dict, Optional, Tuple

import numpy as np
import sympy as sp

from .constants import PhysicalConstants


class SymbolicMath:
    """
    Symbolic mathematics utilities for void physics calculations.

    Provides automatic differentiation, equation derivation, and LaTeX rendering
    for the mathematical formalism of void physics.
    """

    def __init__(self, constants: Optional[PhysicalConstants] = None):
        """
        Initialize symbolic math utilities.

        Args:
            constants: Physical constants (uses default if None)
        """
        self.constants = constants or PhysicalConstants()

        # Define symbolic variables
        self.phi = sp.Symbol("phi", real=True)  # Scalar field
        self.t = sp.Symbol("t", real=True)  # Time parameter
        self.x = sp.Symbol("x", real=True)  # Spatial coordinate
        self.lambda_sym = sp.Symbol("lambda", positive=True)  # Coupling
        self.v_sym = sp.Symbol("v", positive=True)  # VEV
        self.V0_sym = sp.Symbol("V_0", real=True)  # Offset

    def double_well_potential(self) -> sp.Expr:
        """
        Symbolic double-well potential: V(φ) = (λ/4)(φ² - v²)² + V₀

        Returns:
            SymPy expression for the potential
        """
        return (self.lambda_sym / 4) * (self.phi**2 - self.v_sym**2) ** 2 + self.V0_sym

    def potential_gradient(self) -> sp.Expr:
        """
        Gradient of double-well potential: dV/dφ

        Returns:
            SymPy expression for the gradient
        """
        V = self.double_well_potential()
        return sp.diff(V, self.phi)

    def potential_hessian(self) -> sp.Expr:
        """
        Second derivative of potential: d²V/dφ²

        Returns:
            SymPy expression for the Hessian
        """
        V = self.double_well_potential()
        return sp.diff(V, self.phi, 2)

    def langevin_equation(self) -> sp.Expr:
        """
        Symbolic Langevin equation: dφ/dt = -Γ dV/dφ + η(t)

        Returns:
            SymPy expression for the Langevin equation
        """
        gamma = sp.Symbol("Gamma", positive=True)
        eta = sp.Function("eta")(self.t)  # Noise function

        dV_dphi = self.potential_gradient()
        return -gamma * dV_dphi + eta

    def effective_action_density(self) -> sp.Expr:
        """
        Effective action density: L = (1/2)(∂_μφ)² - V(φ)

        Returns:
            SymPy expression for the Lagrangian density
        """
        # Define spacetime derivatives
        dphi_dt = sp.Function("phi_dot")(self.t)
        dphi_dx = sp.Function("phi_prime")(self.x)

        # Kinetic term: (1/2)[(∂φ/∂t)² - (∂φ/∂x)²] (Minkowski metric)
        kinetic = (1 / 2) * (dphi_dt**2 - dphi_dx**2)

        # Potential term
        potential = self.double_well_potential()

        return kinetic - potential

    def euler_lagrange_equation(self) -> sp.Expr:
        """
        Euler-Lagrange equation for the scalar field.

        Returns:
            SymPy expression for the equation of motion
        """
        L = self.effective_action_density()

        # For simplicity, assume φ depends only on time
        # Full derivation would use functional derivatives
        dL_dphi = sp.diff(L, self.phi)
        dL_dphi_dot = sp.diff(L, sp.Function("phi_dot")(self.t))

        # Euler-Lagrange: d/dt(∂L/∂φ̇) - ∂L/∂φ = 0
        return sp.diff(dL_dphi_dot, self.t) - dL_dphi

    def instanton_action(self) -> sp.Expr:
        """
        Euclidean action for instanton calculation.

        Returns:
            SymPy expression for the Euclidean action
        """
        # Euclidean time: t → iτ
        tau = sp.Symbol("tau", real=True)

        # Euclidean Lagrangian: L_E = (1/2)(dφ/dτ)² + V(φ)
        dphi_dtau = sp.Function("phi_dot_euclidean")(tau)
        kinetic_euclidean = (1 / 2) * dphi_dtau**2
        potential = self.double_well_potential()

        return kinetic_euclidean + potential

    def substitute_constants(self, expr: sp.Expr) -> sp.Expr:
        """
        Substitute numerical values for symbolic constants.

        Args:
            expr: SymPy expression

        Returns:
            Expression with constants substituted
        """
        substitutions = {
            self.lambda_sym: self.constants.lambda_coupling,
            self.v_sym: self.constants.v_vev,
            self.V0_sym: self.constants.V0_offset,
        }
        return expr.subs(substitutions)

    def to_latex(self, expr: sp.Expr) -> str:
        """
        Convert SymPy expression to LaTeX string.

        Args:
            expr: SymPy expression

        Returns:
            LaTeX string
        """
        return sp.latex(expr)

    def numerical_eval(self, expr: sp.Expr, phi_val: float) -> float:
        """
        Evaluate expression numerically at given field value.

        Args:
            expr: SymPy expression
            phi_val: Field value to evaluate at

        Returns:
            Numerical value
        """
        # Substitute constants and field value
        expr_num = self.substitute_constants(expr)
        expr_num = expr_num.subs(self.phi, phi_val)

        # Convert to float
        return float(expr_num.evalf())

    def find_critical_points(self) -> Dict[str, float]:
        """
        Find critical points of the potential (where dV/dφ = 0).

        Returns:
            Dictionary mapping critical point names to φ values
        """
        dV_dphi = self.potential_gradient()
        critical_points = sp.solve(dV_dphi, self.phi)

        # Substitute constants to get numerical values
        critical_points_num = []
        for cp in critical_points:
            cp_num = self.substitute_constants(cp)
            critical_points_num.append(float(cp_num.evalf()))

        # Label the points
        labels = {}
        for i, cp in enumerate(critical_points_num):
            if abs(cp) < 1e-6:
                labels["symmetric"] = cp
            elif cp > 0:
                labels["positive_vacuum"] = cp
            elif cp < 0:
                labels["negative_vacuum"] = cp
            else:
                labels[f"critical_point_{i}"] = cp

        return labels

    def stability_analysis(self) -> Dict[str, Any]:
        """
        Analyze stability of critical points.

        Returns:
            Dictionary with stability information
        """
        critical_points = self.find_critical_points()
        d2V_dphi2 = self.potential_hessian()

        stability = {}
        for name, phi_val in critical_points.items():
            # Evaluate second derivative at critical point
            d2V_val = self.numerical_eval(d2V_dphi2, phi_val)

            if d2V_val > 0:
                stability[name] = {"type": "stable", "mass_squared": d2V_val}
            elif d2V_val < 0:
                stability[name] = {"type": "unstable", "mass_squared": d2V_val}
            else:
                stability[name] = {"type": "marginal", "mass_squared": d2V_val}

        return stability
