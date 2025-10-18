"""
Instanton calculations for void physics tunneling.

This module implements instanton solutions and tunneling probability calculations
for the transition from void to ordered states in void physics.
"""

from dataclasses import dataclass
from typing import Any, Callable, Dict, Optional, Tuple

import numpy as np
import scipy.integrate
import scipy.optimize

from ..utils.constants import PhysicalConstants
from .potential import DoubleWellPotential


@dataclass
class InstantonParameters:
    """Parameters for instanton calculations."""

    phi_initial: float = -1.0  # Initial field value (symmetric state)
    phi_final: float = 1.0  # Final field value (broken symmetry)
    euclidean_time_max: float = 10.0  # Maximum Euclidean time
    n_points: int = 1000  # Number of discretization points


class InstantonSolver:
    """
    Solver for instanton solutions in void physics.

    An instanton is a classical solution to the Euclidean field equations
    that describes tunneling between different vacuum states. In void physics,
    instantons represent the nucleation of spacetime domains from the void.

    The Euclidean action is:
    S_E = ∫dτ [(1/2)(dφ/dτ)² + V(φ)]

    where τ is Euclidean time and V(φ) is the potential.
    """

    def __init__(
        self,
        potential: Optional[DoubleWellPotential] = None,
        constants: Optional[PhysicalConstants] = None,
    ):
        """
        Initialize instanton solver.

        Args:
            potential: Scalar field potential
            constants: Physical constants
        """
        self.potential = potential or DoubleWellPotential()
        self.constants = constants or PhysicalConstants()

    def euclidean_action(self, phi: np.ndarray, tau: np.ndarray) -> float:
        """
        Calculate Euclidean action for a field configuration.

        Args:
            phi: Field values as function of Euclidean time
            tau: Euclidean time array

        Returns:
            Euclidean action value
        """
        if len(phi) != len(tau):
            raise ValueError("Field and time arrays must have same length")

        # Kinetic term: (1/2)(dφ/dτ)²
        dphi_dtau = np.gradient(phi, tau)
        kinetic = 0.5 * dphi_dtau**2

        # Potential term
        potential_term = self.potential(phi)

        # Total action
        integrand = kinetic + potential_term
        action = np.trapezoid(integrand, tau)

        return action

    def euclidean_equation_of_motion(
        self, phi: np.ndarray, tau: np.ndarray
    ) -> np.ndarray:
        """
        Euclidean equation of motion: d²φ/dτ² = dV/dφ

        Args:
            phi: Field values
            tau: Euclidean time

        Returns:
            Second derivative d²φ/dτ²
        """
        dV_dphi = self.potential.gradient(phi)
        return dV_dphi

    def bounce_solution(
        self, params: Optional[InstantonParameters] = None
    ) -> Tuple[np.ndarray, np.ndarray, float]:
        """
        Find the bounce solution (instanton) between two vacua.

        The bounce solution is a classical solution that starts and ends at
        the same vacuum state, passing through the other vacuum at τ=0.

        Args:
            params: Instanton parameters

        Returns:
            Tuple of (tau, phi_bounce, action)
        """
        if params is None:
            params = InstantonParameters()

        # Create Euclidean time array
        tau = np.linspace(
            -params.euclidean_time_max, params.euclidean_time_max, params.n_points
        )
        dtau = tau[1] - tau[0]

        # Initial guess: kink solution
        phi_guess = params.phi_final * np.tanh(tau)

        def action_functional(phi_array):
            """Action as function of field values."""
            return self.euclidean_action(phi_array, tau)

        def constraint_function(phi_array):
            """Constraint: field should start and end at initial vacuum."""
            return np.array(
                [phi_array[0] - params.phi_initial, phi_array[-1] - params.phi_initial]
            )

        # Minimize action with constraints
        constraints = {"type": "eq", "fun": constraint_function}

        result = scipy.optimize.minimize(
            action_functional,
            phi_guess,
            method="SLSQP",
            constraints=constraints,
            options={"maxiter": 1000},
        )

        if not result.success:
            raise RuntimeError(f"Instanton optimization failed: {result.message}")

        phi_bounce = result.x
        action = result.fun

        return tau, phi_bounce, action

    def kink_solution(
        self, params: Optional[InstantonParameters] = None
    ) -> Tuple[np.ndarray, np.ndarray, float]:
        """
        Find the kink solution (domain wall) between two vacua.

        The kink solution connects two different vacuum states and represents
        a domain wall in spacetime.

        Args:
            params: Instanton parameters

        Returns:
            Tuple of (tau, phi_kink, action)
        """
        if params is None:
            params = InstantonParameters()

        # Create Euclidean time array
        tau = np.linspace(
            -params.euclidean_time_max, params.euclidean_time_max, params.n_points
        )

        # Analytical kink solution for double-well potential
        # φ(τ) = v tanh(√(λ/2) v τ)
        v = self.potential.params.v_vev
        lambda_coupling = self.potential.params.lambda_coupling
        kink_width = np.sqrt(2 / lambda_coupling) / v

        phi_kink = v * np.tanh(tau / kink_width)

        # Calculate action
        action = self.euclidean_action(phi_kink, tau)

        return tau, phi_kink, action

    def instanton_profile(
        self, tau: np.ndarray, phi_center: float = 0.0, width: float = 1.0
    ) -> np.ndarray:
        """
        Generate instanton profile with given center and width.

        Args:
            tau: Euclidean time array
            phi_center: Center position of instanton
            width: Width of instanton

        Returns:
            Instanton field profile
        """
        v = self.potential.params.v_vev
        lambda_coupling = self.potential.params.lambda_coupling

        # Kink profile: φ(τ) = v tanh((τ - τ₀)/w)
        # where w = √(2/λ)/v is the width
        w = np.sqrt(2 / lambda_coupling) / v

        phi_profile = v * np.tanh((tau - phi_center) / (width * w))

        return phi_profile

    def multi_instanton_solution(
        self, n_instantons: int, params: Optional[InstantonParameters] = None
    ) -> Tuple[np.ndarray, np.ndarray, float]:
        """
        Find multi-instanton solution (instanton gas).

        This represents multiple nucleation events in the void.

        Args:
            n_instantons: Number of instantons
            params: Instanton parameters

        Returns:
            Tuple of (tau, phi_multi, action)
        """
        if params is None:
            params = InstantonParameters()

        tau = np.linspace(
            -params.euclidean_time_max, params.euclidean_time_max, params.n_points
        )

        # For simplicity, use superposition of single instantons
        # In practice, this would require more sophisticated methods
        phi_multi = np.zeros_like(tau)

        v = self.potential.params.v_vev
        lambda_coupling = self.potential.params.lambda_coupling
        w = np.sqrt(2 / lambda_coupling) / v

        # Place instantons at regular intervals
        for i in range(n_instantons):
            center = (
                -params.euclidean_time_max
                + (2 * i + 1) * params.euclidean_time_max / n_instantons
            )
            phi_multi += v * np.tanh((tau - center) / w)

        # Normalize to stay within potential wells
        phi_multi = np.clip(phi_multi, -v, v)

        action = self.euclidean_action(phi_multi, tau)

        return tau, phi_multi, action


class TunnelingProbability:
    """
    Calculate tunneling probabilities from instanton solutions.

    The tunneling probability is given by:
    P ~ exp(-S_E/ℏ)

    where S_E is the Euclidean action of the instanton.
    """

    def __init__(
        self,
        instanton_solver: Optional[InstantonSolver] = None,
        constants: Optional[PhysicalConstants] = None,
    ):
        """
        Initialize tunneling probability calculator.

        Args:
            instanton_solver: Instanton solver
            constants: Physical constants
        """
        self.instanton_solver = instanton_solver or InstantonSolver()
        self.constants = constants or PhysicalConstants()

    def bounce_probability(self, params: Optional[InstantonParameters] = None) -> float:
        """
        Calculate tunneling probability from bounce solution.

        Args:
            params: Instanton parameters

        Returns:
            Tunneling probability
        """
        tau, phi_bounce, action = self.instanton_solver.bounce_solution(params)

        # Tunneling probability: P ~ exp(-S_E/ℏ)
        probability = np.exp(-action / self.constants.hbar)

        return probability

    def kink_probability(self, params: Optional[InstantonParameters] = None) -> float:
        """
        Calculate tunneling probability from kink solution.

        Args:
            params: Instanton parameters

        Returns:
            Tunneling probability
        """
        tau, phi_kink, action = self.instanton_solver.kink_solution(params)

        probability = np.exp(-action / self.constants.hbar)

        return probability

    def nucleation_rate(
        self, volume: float = 1.0, params: Optional[InstantonParameters] = None
    ) -> float:
        """
        Calculate nucleation rate per unit volume.

        The nucleation rate is the probability per unit time per unit volume
        for a void domain to nucleate into spacetime.

        Args:
            volume: Volume of the system
            params: Instanton parameters

        Returns:
            Nucleation rate
        """
        # Get bounce solution
        tau, phi_bounce, action = self.instanton_solver.bounce_solution(params)

        # Calculate prefactor (determinant of fluctuations)
        # For simplicity, use dimensional analysis
        v = self.instanton_solver.potential.params.v_vev
        lambda_coupling = self.instanton_solver.potential.params.lambda_coupling

        # Prefactor: ~ (S_E/2πℏ)^(1/2) * (λv²)^(1/2)
        prefactor = np.sqrt(action / (2 * np.pi * self.constants.hbar)) * np.sqrt(
            lambda_coupling * v**2
        )

        # Nucleation rate: Γ = (prefactor/volume) * exp(-S_E/ℏ)
        rate = (prefactor / volume) * np.exp(-action / self.constants.hbar)

        return rate

    def critical_radius(
        self, surface_tension: float = 1.0, pressure_difference: float = 1.0
    ) -> float:
        """
        Calculate critical radius for bubble nucleation.

        This gives the minimum size for a nucleated domain to grow rather than collapse.

        Args:
            surface_tension: Surface tension of the domain wall
            pressure_difference: Pressure difference between phases

        Returns:
            Critical radius
        """
        # Critical radius: R_c = 2σ/ΔP
        # where σ is surface tension and ΔP is pressure difference
        return 2 * surface_tension / pressure_difference

    def bubble_growth_rate(
        self,
        radius: float,
        surface_tension: float = 1.0,
        pressure_difference: float = 1.0,
        viscosity: float = 1.0,
    ) -> float:
        """
        Calculate bubble growth rate for nucleated domains.

        Args:
            radius: Current bubble radius
            surface_tension: Surface tension
            pressure_difference: Pressure difference
            viscosity: Viscosity of the medium

        Returns:
            Growth rate dR/dt
        """
        # Growth rate: dR/dt = (ΔP * R - 2σ) / (4ηR)
        # where η is viscosity
        numerator = pressure_difference * radius - 2 * surface_tension
        denominator = 4 * viscosity * radius

        if denominator == 0:
            return 0.0

        return numerator / denominator

    def phase_transition_completion_time(
        self,
        initial_radius: float,
        final_radius: float,
        surface_tension: float = 1.0,
        pressure_difference: float = 1.0,
        viscosity: float = 1.0,
    ) -> float:
        """
        Calculate time for phase transition to complete.

        Args:
            initial_radius: Initial bubble radius
            final_radius: Final bubble radius
            surface_tension: Surface tension
            pressure_difference: Pressure difference
            viscosity: Viscosity

        Returns:
            Completion time
        """

        # Integrate growth rate equation
        def growth_rate(r):
            return self.bubble_growth_rate(
                r, surface_tension, pressure_difference, viscosity
            )

        # Time integral: t = ∫ dR / (dR/dt)
        def integrand(r):
            dr_dt = growth_rate(r)
            if dr_dt == 0:
                return np.inf
            return 1.0 / dr_dt

        time = scipy.integrate.quad(integrand, initial_radius, final_radius)[0]

        # Return 0 if no transition is possible (negative time)
        return max(0.0, time)
