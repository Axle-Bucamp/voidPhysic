"""
Stochastic dynamics for void physics field theory.

This module implements Langevin dynamics and noise models for describing
the stochastic evolution of fields in void physics, including the transition
from void to ordered states through quantum fluctuations.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Callable, Dict, Optional, Tuple

import numpy as np

from ..utils.constants import PhysicalConstants
from .potential import DoubleWellPotential


@dataclass
class NoiseParameters:
    """Parameters for noise models."""

    strength: float = 1.0  # Noise amplitude
    correlation_time: float = 0.0  # Correlation time (0 = white noise)
    spectral_index: float = 0.0  # Power spectrum index (0 = white noise)


class NoiseModel(ABC):
    """
    Abstract base class for noise models.

    Noise represents the quantum fluctuations of the "void" that can
    trigger the nucleation of ordered spacetime domains.
    """

    @abstractmethod
    def generate(self, t: np.ndarray, dt: float) -> np.ndarray:
        """
        Generate noise time series.

        Args:
            t: Time array
            dt: Time step

        Returns:
            Noise values
        """
        pass

    @abstractmethod
    def power_spectrum(self, frequencies: np.ndarray) -> np.ndarray:
        """
        Calculate power spectrum of the noise.

        Args:
            frequencies: Frequency array

        Returns:
            Power spectrum values
        """
        pass


class WhiteNoise(NoiseModel):
    """
    White noise: η(t) with ⟨η(t)η(t')⟩ = 2D δ(t-t')

    This represents uncorrelated quantum fluctuations that can trigger
    symmetry breaking in the void state.
    """

    def __init__(self, strength: float = 1.0, seed: Optional[int] = None):
        """
        Initialize white noise generator.

        Args:
            strength: Noise strength (diffusion coefficient D)
            seed: Random seed for reproducibility
        """
        self.strength = strength
        self.rng = np.random.RandomState(seed)

    def generate(self, t: np.ndarray, dt: float) -> np.ndarray:
        """
        Generate white noise time series.

        Args:
            t: Time array or scalar
            dt: Time step

        Returns:
            White noise values
        """
        # Handle both scalar and array inputs
        if np.isscalar(t):
            n_points = 1
        else:
            n_points = len(t)

        # White noise: Gaussian with variance 2D/dt
        variance = 2 * self.strength / dt
        return self.rng.normal(0, np.sqrt(variance), n_points)

    def power_spectrum(self, frequencies: np.ndarray) -> np.ndarray:
        """
        Power spectrum of white noise (flat).

        Args:
            frequencies: Frequency array

        Returns:
            Constant power spectrum
        """
        return np.full_like(frequencies, 2 * self.strength)

    def correlation_function(self, tau: np.ndarray) -> np.ndarray:
        """
        Correlation function: ⟨η(t)η(t+τ)⟩ = 2D δ(τ)

        Args:
            tau: Time lag array

        Returns:
            Correlation function values
        """
        # Dirac delta function approximation
        correlation = np.zeros_like(tau)
        # Use a reasonable threshold for numerical stability
        # For typical tau arrays, use threshold of 0.02
        threshold = 0.02
        correlation[np.abs(tau) < threshold] = 2 * self.strength
        return correlation


class ColoredNoise(NoiseModel):
    """
    Colored noise with power spectrum P(f) ∝ f^(-α).

    This can represent correlated quantum fluctuations with memory effects.
    """

    def __init__(
        self,
        strength: float = 1.0,
        spectral_index: float = 1.0,
        correlation_time: float = 1.0,
        seed: Optional[int] = None,
    ):
        """
        Initialize colored noise generator.

        Args:
            strength: Noise strength
            spectral_index: Power spectrum index α
            correlation_time: Characteristic correlation time
            seed: Random seed
        """
        self.strength = strength
        self.spectral_index = spectral_index
        self.correlation_time = correlation_time
        self.rng = np.random.RandomState(seed)

    def generate(self, t: np.ndarray, dt: float) -> np.ndarray:
        """
        Generate colored noise using Ornstein-Uhlenbeck process.

        Args:
            t: Time array
            dt: Time step

        Returns:
            Colored noise values
        """
        n_points = len(t)
        noise = np.zeros(n_points)

        # Ornstein-Uhlenbeck process: dη/dt = -η/τ + ξ(t)
        # where ξ(t) is white noise
        gamma = 1.0 / self.correlation_time
        white_noise = self.rng.normal(0, np.sqrt(2 * self.strength / dt), n_points)

        for i in range(1, n_points):
            noise[i] = noise[i - 1] * (1 - gamma * dt) + white_noise[i] * dt

        return noise

    def power_spectrum(self, frequencies: np.ndarray) -> np.ndarray:
        """
        Power spectrum: P(f) = 2D / (1 + (2πfτ)²)

        Args:
            frequencies: Frequency array

        Returns:
            Power spectrum values
        """
        omega = 2 * np.pi * frequencies
        return 2 * self.strength / (1 + (omega * self.correlation_time) ** 2)

    def correlation_function(self, tau: np.ndarray) -> np.ndarray:
        """
        Correlation function: ⟨η(t)η(t+τ)⟩ = D/τ exp(-|τ|/τ)

        Args:
            tau: Time lag array

        Returns:
            Correlation function values
        """
        return (self.strength / self.correlation_time) * np.exp(
            -np.abs(tau) / self.correlation_time
        )


class LangevinDynamics:
    """
    Langevin dynamics for scalar field evolution.

    Implements the stochastic differential equation:
    dφ/dt = -Γ dV/dφ + η(t)

    where:
    - Γ is the friction coefficient
    - V(φ) is the potential
    - η(t) is the noise (quantum fluctuations)

    This describes the stochastic evolution of the field from the void state
    to ordered configurations through thermal/quantum fluctuations.
    """

    def __init__(
        self,
        potential: Optional[DoubleWellPotential] = None,
        noise_model: Optional[NoiseModel] = None,
        constants: Optional[PhysicalConstants] = None,
    ):
        """
        Initialize Langevin dynamics.

        Args:
            potential: Scalar field potential
            noise_model: Noise model (uses white noise if None)
            constants: Physical constants
        """
        self.potential = potential or DoubleWellPotential()
        self.noise_model = noise_model or WhiteNoise()
        self.constants = constants or PhysicalConstants()

    def drift_term(self, phi: np.ndarray) -> np.ndarray:
        """
        Drift term: -Γ dV/dφ

        Args:
            phi: Field values

        Returns:
            Drift values
        """
        dV_dphi = self.potential.gradient(phi)
        return -self.constants.gamma_friction * dV_dphi

    def diffusion_term(self, t: np.ndarray, dt: float) -> np.ndarray:
        """
        Diffusion term: η(t)

        Args:
            t: Time array
            dt: Time step

        Returns:
            Noise values
        """
        return self.noise_model.generate(t, dt)

    def langevin_equation(
        self, phi: np.ndarray, t: np.ndarray, dt: float
    ) -> np.ndarray:
        """
        Complete Langevin equation: dφ/dt = -Γ dV/dφ + η(t)

        Args:
            phi: Current field values
            t: Time array
            dt: Time step

        Returns:
            Field time derivatives
        """
        drift = self.drift_term(phi)
        diffusion = self.diffusion_term(t, dt)
        return drift + diffusion

    def fokker_planck_equation(
        self, phi: np.ndarray, probability_density: np.ndarray
    ) -> np.ndarray:
        """
        Fokker-Planck equation for probability density evolution.

        ∂P/∂t = -∂/∂φ[A(φ)P] + (1/2)∂²/∂φ²[B(φ)P]

        where A(φ) = -Γ dV/dφ and B(φ) = 2D (for white noise)

        Args:
            phi: Field values
            probability_density: Current probability density P(φ,t)

        Returns:
            Time derivative of probability density
        """
        # Drift coefficient: A(φ) = -Γ dV/dφ
        A = self.drift_term(phi)

        # Diffusion coefficient: B(φ) = 2D (constant for white noise)
        B = 2 * self.noise_model.strength

        # Fokker-Planck equation (simplified for 1D)
        # ∂P/∂t = -∂/∂φ[A(φ)P] + (1/2)∂²/∂φ²[B(φ)P]

        # For numerical implementation, we would need finite differences
        # This is a placeholder for the full implementation
        dP_dt = np.zeros_like(probability_density)

        return dP_dt

    def stationary_distribution(self, phi: np.ndarray) -> np.ndarray:
        """
        Stationary probability distribution: P_st(φ) ∝ exp(-V(φ)/D)

        This gives the equilibrium distribution in the presence of noise.

        Args:
            phi: Field values

        Returns:
            Stationary probability density
        """
        V = self.potential(phi)
        D = self.noise_model.strength

        # Boltzmann distribution: P ∝ exp(-V/D)
        log_prob = -V / D
        log_prob = log_prob - np.max(log_prob)  # Normalize for numerical stability
        prob = np.exp(log_prob)

        # Normalize
        prob = prob / np.trapezoid(prob, phi)

        return prob

    def escape_rate(self, phi_initial: float, phi_final: float) -> float:
        """
        Calculate escape rate from initial to final state.

        This uses Kramers' formula for the escape rate over a potential barrier.

        Args:
            phi_initial: Initial field value
            phi_final: Final field value

        Returns:
            Escape rate (probability per unit time)
        """
        # Find the barrier height
        phi_barrier = 0.0  # For double-well, barrier is at φ=0
        V_initial = self.potential(np.array([phi_initial]))[0]
        V_barrier = self.potential(np.array([phi_barrier]))[0]
        V_final = self.potential(np.array([phi_final]))[0]

        barrier_height = V_barrier - V_initial

        # Kramers' escape rate: Γ = (ω₀ω_b/2π) exp(-ΔV/D)
        # where ω₀ and ω_b are frequencies at initial and barrier points
        hessian_initial = self.potential.hessian(np.array([phi_initial]))[0]
        hessian_barrier = self.potential.hessian(np.array([phi_barrier]))[0]

        # Check for valid frequencies
        if hessian_initial <= 0 or hessian_barrier >= 0:
            return 0.0  # No escape possible

        omega_initial = np.sqrt(abs(hessian_initial))
        omega_barrier = np.sqrt(abs(hessian_barrier))

        D = self.noise_model.strength
        if D <= 0:
            return 0.0

        escape_rate = (omega_initial * omega_barrier / (2 * np.pi)) * np.exp(
            -barrier_height / D
        )

        return escape_rate

    def first_passage_time_distribution(
        self,
        phi_initial: float,
        phi_threshold: float,
        n_trajectories: int = 1000,
        t_max: float = 100.0,
        dt: float = 0.01,
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Calculate first passage time distribution.

        This simulates multiple trajectories to find the distribution of
        times when the field first crosses a threshold (e.g., from void to ordered state).

        Args:
            phi_initial: Initial field value
            phi_threshold: Threshold to cross
            n_trajectories: Number of trajectories to simulate
            t_max: Maximum simulation time
            dt: Time step

        Returns:
            Tuple of (time_array, first_passage_times)
        """
        t = np.arange(0, t_max, dt)
        first_passage_times = []

        for _ in range(n_trajectories):
            phi = np.zeros_like(t)
            phi[0] = phi_initial

            for i in range(1, len(t)):
                # Euler-Maruyama integration
                dphi_dt = self.langevin_equation(phi[i - 1], t[i - 1], dt)
                phi[i] = phi[i - 1] + float(dphi_dt) * dt

                # Check for first passage
                if phi[i] >= phi_threshold:
                    first_passage_times.append(t[i])
                    break
            else:
                # No passage within time limit
                first_passage_times.append(np.inf)

        return t, np.array(first_passage_times)
