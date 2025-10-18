"""
Langevin equation solver for void physics simulations.

This module implements numerical methods for solving stochastic differential
equations in void physics, including Euler-Maruyama integration and adaptive
timestepping for efficient simulation of field evolution.
"""

from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional, Tuple

import numpy as np
import scipy.integrate

from ..core.potential import DoubleWellPotential
from ..core.stochastic import LangevinDynamics, WhiteNoise
from ..utils.constants import PhysicalConstants


@dataclass
class SolverParameters:
    """Parameters for Langevin solver."""

    dt: float = 0.01  # Time step
    t_max: float = 100.0  # Maximum simulation time
    n_trajectories: int = 1000  # Number of stochastic trajectories
    adaptive: bool = True  # Use adaptive timestepping
    tolerance: float = 1e-6  # Tolerance for adaptive stepping
    save_trajectories: bool = True  # Save individual trajectories


class LangevinSolver:
    """
    Numerical solver for Langevin equations in void physics.

    Implements various integration schemes for the stochastic differential equation:
    dφ/dt = -Γ dV/dφ + η(t)

    where η(t) is noise representing quantum fluctuations of the void.
    """

    def __init__(
        self,
        langevin_dynamics: Optional[LangevinDynamics] = None,
        constants: Optional[PhysicalConstants] = None,
    ):
        """
        Initialize Langevin solver.

        Args:
            langevin_dynamics: Langevin dynamics object
            constants: Physical constants
        """
        self.dynamics = langevin_dynamics or LangevinDynamics()
        self.constants = constants or PhysicalConstants()

    def euler_maruyama(
        self, phi0: float, params: Optional[SolverParameters] = None
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Euler-Maruyama integration of Langevin equation.

        This is the simplest stochastic integration scheme:
        φ(t+dt) = φ(t) + [-Γ dV/dφ + η(t)] dt

        Args:
            phi0: Initial field value
            params: Solver parameters

        Returns:
            Tuple of (time_array, field_values)
        """
        if params is None:
            params = SolverParameters()

        # Create time array
        t = np.arange(0, params.t_max, params.dt)
        n_points = len(t)

        # Initialize field array
        phi = np.zeros(n_points)
        phi[0] = phi0

        # Generate noise
        noise = self.dynamics.noise_model.generate(t, params.dt)

        # Euler-Maruyama integration
        for i in range(1, n_points):
            # Drift term: -Γ dV/dφ
            drift = self.dynamics.drift_term(phi[i - 1])

            # Diffusion term: η(t)
            diffusion = noise[i]

            # Update field
            phi[i] = phi[i - 1] + (drift + diffusion) * params.dt

        return t, phi

    def milstein(
        self, phi0: float, params: Optional[SolverParameters] = None
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Milstein integration scheme (higher order than Euler-Maruyama).

        Includes correction term for better accuracy:
        φ(t+dt) = φ(t) + [-Γ dV/dφ + η(t)] dt + (1/2) η(t)² dt

        Args:
            phi0: Initial field value
            params: Solver parameters

        Returns:
            Tuple of (time_array, field_values)
        """
        if params is None:
            params = SolverParameters()

        t = np.arange(0, params.t_max, params.dt)
        n_points = len(t)

        phi = np.zeros(n_points)
        phi[0] = phi0

        noise = self.dynamics.noise_model.generate(t, params.dt)

        for i in range(1, n_points):
            drift = self.dynamics.drift_term(phi[i - 1])
            diffusion = noise[i]

            # Milstein correction term
            correction = 0.5 * diffusion**2 * params.dt

            phi[i] = phi[i - 1] + (drift + diffusion) * params.dt + correction

        return t, phi

    def runge_kutta_stochastic(
        self, phi0: float, params: Optional[SolverParameters] = None
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Stochastic Runge-Kutta integration scheme.

        Uses a 4th-order Runge-Kutta method for the deterministic part
        and appropriate stochastic terms.

        Args:
            phi0: Initial field value
            params: Solver parameters

        Returns:
            Tuple of (time_array, field_values)
        """
        if params is None:
            params = SolverParameters()

        t = np.arange(0, params.t_max, params.dt)
        n_points = len(t)

        phi = np.zeros(n_points)
        phi[0] = phi0

        noise = self.dynamics.noise_model.generate(t, params.dt)

        for i in range(1, n_points):
            # Runge-Kutta stages for deterministic part
            k1 = self.dynamics.drift_term(phi[i - 1])
            k2 = self.dynamics.drift_term(phi[i - 1] + 0.5 * k1 * params.dt)
            k3 = self.dynamics.drift_term(phi[i - 1] + 0.5 * k2 * params.dt)
            k4 = self.dynamics.drift_term(phi[i - 1] + k3 * params.dt)

            # Deterministic update
            drift_update = (k1 + 2 * k2 + 2 * k3 + k4) * params.dt / 6

            # Stochastic update
            diffusion = noise[i]
            stochastic_update = diffusion * params.dt

            phi[i] = phi[i - 1] + drift_update + stochastic_update

        return t, phi

    def ensemble_simulation(
        self, phi0: float, params: Optional[SolverParameters] = None
    ) -> Dict[str, np.ndarray]:
        """
        Run ensemble of stochastic trajectories.

        Args:
            phi0: Initial field value
            params: Solver parameters

        Returns:
            Dictionary with ensemble statistics
        """
        if params is None:
            params = SolverParameters()

        # Run multiple trajectories
        trajectories_list = []
        for _ in range(params.n_trajectories):
            t, phi = self.euler_maruyama(phi0, params)
            trajectories_list.append(phi)

        trajectories = np.array(trajectories_list)

        # Calculate ensemble statistics
        mean_phi = np.mean(trajectories, axis=0)
        std_phi = np.std(trajectories, axis=0)
        var_phi = np.var(trajectories, axis=0)

        # Calculate energy statistics
        energies_list = []
        for phi_traj in trajectories:
            # Energy: E = (1/2)(dφ/dt)² + V(φ)
            dphi_dt = np.gradient(phi_traj, t)
            kinetic = 0.5 * dphi_dt**2
            potential = self.dynamics.potential(phi_traj)
            energy = kinetic + potential
            energies_list.append(energy)

        energies = np.array(energies_list)
        mean_energy = np.mean(energies, axis=0)
        std_energy = np.std(energies, axis=0)

        return {
            "time": t,
            "trajectories": trajectories if params.save_trajectories else None,
            "mean_field": mean_phi,
            "std_field": std_phi,
            "var_field": var_phi,
            "mean_energy": mean_energy,
            "std_energy": std_energy,
        }

    def adaptive_timestep(
        self, phi0: float, params: Optional[SolverParameters] = None
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Adaptive timestep integration for better accuracy.

        Adjusts timestep based on local error estimates.

        Args:
            phi0: Initial field value
            params: Solver parameters

        Returns:
            Tuple of (time_array, field_values)
        """
        if params is None:
            params = SolverParameters()

        # Initialize
        t_current = 0.0
        phi_current = phi0
        dt = params.dt

        time_points = [t_current]
        field_points = [phi_current]

        while t_current < params.t_max:
            # Take two half steps
            phi_half1 = phi_current + 0.5 * self.dynamics.langevin_equation(
                np.array([phi_current]), np.array([t_current]), dt / 2
            )[0] * (dt / 2)
            phi_half2 = phi_half1 + 0.5 * self.dynamics.langevin_equation(
                np.array([phi_half1]), np.array([t_current + dt / 2]), dt / 2
            )[0] * (dt / 2)

            # Take one full step
            phi_full = (
                phi_current
                + self.dynamics.langevin_equation(
                    np.array([phi_current]), np.array([t_current]), dt
                )[0]
                * dt
            )

            # Estimate error
            error = np.abs(phi_full - phi_half2)

            # Adjust timestep
            if error < params.tolerance:
                # Accept step
                t_current += dt
                phi_current = phi_half2
                time_points.append(t_current)
                field_points.append(phi_current)

                # Increase timestep
                dt = min(dt * 1.1, params.dt * 2)
            else:
                # Reject step, decrease timestep
                dt = max(dt * 0.5, params.dt * 0.1)

        return np.array(time_points), np.array(field_points)

    def first_passage_analysis(
        self, phi0: float, threshold: float, params: Optional[SolverParameters] = None
    ) -> Dict[str, Any]:
        """
        Analyze first passage times to a threshold.

        Args:
            phi0: Initial field value
            threshold: Threshold to cross
            params: Solver parameters

        Returns:
            Dictionary with first passage statistics
        """
        if params is None:
            params = SolverParameters()

        first_passage_times = []

        for _ in range(params.n_trajectories):
            t, phi = self.euler_maruyama(phi0, params)

            # Find first passage
            crossing_indices = np.where(phi >= threshold)[0]
            if len(crossing_indices) > 0:
                first_passage_times.append(t[crossing_indices[0]])
            else:
                first_passage_times.append(np.inf)

        first_passage_times_array = np.array(first_passage_times)

        # Remove infinite times for statistics
        finite_times = first_passage_times_array[first_passage_times_array != np.inf]

        if len(finite_times) > 0:
            mean_fpt = np.mean(finite_times)
            std_fpt = np.std(finite_times)
            median_fpt = np.median(finite_times)
            survival_probability = len(finite_times) / len(first_passage_times_array)
        else:
            mean_fpt = std_fpt = median_fpt = np.inf
            survival_probability = 0.0

        return {
            "first_passage_times": first_passage_times_array,
            "mean_fpt": mean_fpt,
            "std_fpt": std_fpt,
            "median_fpt": median_fpt,
            "survival_probability": survival_probability,
            "finite_times": finite_times,
        }

    def energy_evolution(
        self, phi0: float, params: Optional[SolverParameters] = None
    ) -> Dict[str, np.ndarray]:
        """
        Track energy evolution during field dynamics.

        Args:
            phi0: Initial field value
            params: Solver parameters

        Returns:
            Dictionary with energy statistics
        """
        t, phi = self.euler_maruyama(phi0, params)

        # Calculate energy components
        dphi_dt = np.gradient(phi, t)
        kinetic_energy = 0.5 * dphi_dt**2
        potential_energy = self.dynamics.potential(phi)
        total_energy = kinetic_energy + potential_energy

        # Calculate entropy (simplified)
        # S = -∫ P(φ) log P(φ) dφ
        # For now, use field variance as proxy
        field_variance = np.var(phi)
        entropy_proxy = (
            0.5 * np.log(2 * np.pi * np.e * field_variance) if field_variance > 0 else 0
        )

        return {
            "time": t,
            "field": phi,
            "kinetic_energy": kinetic_energy,
            "potential_energy": potential_energy,
            "total_energy": total_energy,
            "entropy_proxy": entropy_proxy,
        }
