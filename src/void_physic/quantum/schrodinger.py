"""
Schrodinger equation solver for void physics.

This module implements the time-dependent Schrodinger equation solver using
the split-operator FFT method, along with wave function evolution and
probability current calculations.
"""

import numpy as np
from dataclasses import dataclass
from typing import Any, Callable, Dict, Optional, Tuple, Union
from scipy.fft import fft, ifft, fftfreq

from .operators import Hamiltonian, OperatorParameters, QuantumPotential


@dataclass
class SchrodingerParameters:
    """Parameters for Schrodinger equation solver."""
    
    mass: float = 1.0  # Particle mass
    hbar: float = 1.0  # Reduced Planck constant
    dt: float = 0.01  # Time step
    x_min: float = -10.0  # Minimum spatial coordinate
    x_max: float = 10.0  # Maximum spatial coordinate
    n_points: int = 1024  # Number of spatial grid points
    potential: Optional[Callable] = None  # Potential function V(x)


class WaveFunction:
    """
    Wave function representation with normalization and evolution.
    """
    
    def __init__(self, psi: np.ndarray, x_grid: np.ndarray, 
                 mass: float = 1.0, hbar: float = 1.0):
        self.psi = psi.astype(complex)
        self.x_grid = x_grid
        self.mass = mass
        self.hbar = hbar
        self.normalize()
    
    def normalize(self) -> None:
        """Normalize wave function."""
        dx = self.x_grid[1] - self.x_grid[0]
        norm = np.sqrt(np.sum(np.abs(self.psi)**2) * dx)
        if norm > 0:
            self.psi /= norm
    
    @property
    def probability_density(self) -> np.ndarray:
        """Probability density |ψ|²."""
        return np.abs(self.psi)**2
    
    @property
    def phase(self) -> np.ndarray:
        """Phase of wave function."""
        return np.angle(self.psi)
    
    def expectation_value(self, operator: Callable) -> complex:
        """Calculate expectation value of operator."""
        dx = self.x_grid[1] - self.x_grid[0]
        return np.sum(np.conj(self.psi) * operator(self.psi, self.x_grid)) * dx
    
    def copy(self) -> 'WaveFunction':
        """Create a copy of the wave function."""
        return WaveFunction(self.psi.copy(), self.x_grid.copy(), 
                          self.mass, self.hbar)


class ProbabilityCurrent:
    """
    Probability current calculation: j = (ℏ/2mi)(ψ*∇ψ - ψ∇ψ*)
    """
    
    def __init__(self, mass: float = 1.0, hbar: float = 1.0):
        self.mass = mass
        self.hbar = hbar
    
    def calculate(self, psi: np.ndarray, x_grid: np.ndarray) -> np.ndarray:
        """
        Calculate probability current.
        
        Args:
            psi: Wave function
            x_grid: Spatial grid
            
        Returns:
            Probability current values
        """
        dx = x_grid[1] - x_grid[0]
        dpsi_dx = np.gradient(psi, dx)
        
        # Probability current: j = (ℏ/2mi)(ψ*∇ψ - ψ∇ψ*)
        j = (self.hbar / (2 * self.mass * 1j)) * (
            np.conj(psi) * dpsi_dx - psi * np.conj(dpsi_dx)
        )
        
        return j.real  # Should be real
    
    def divergence(self, psi: np.ndarray, x_grid: np.ndarray) -> np.ndarray:
        """
        Calculate divergence of probability current.
        
        Args:
            psi: Wave function
            x_grid: Spatial grid
            
        Returns:
            Divergence of probability current
        """
        j = self.calculate(psi, x_grid)
        dx = x_grid[1] - x_grid[0]
        return np.gradient(j, dx)


class SchrodingerSolver:
    """
    Schrodinger equation solver using split-operator FFT method.
    
    Solves: iℏ ∂ψ/∂t = Ĥψ = [p̂²/(2m) + V(x)]ψ
    """
    
    def __init__(self, params: SchrodingerParameters):
        self.params = params
        self.mass = params.mass
        self.hbar = params.hbar
        self.dt = params.dt
        
        # Set up spatial grid
        self.x_grid = np.linspace(params.x_min, params.x_max, params.n_points)
        self.dx = self.x_grid[1] - self.x_grid[0]
        
        # Set up momentum grid for FFT
        self.k_grid = 2 * np.pi * fftfreq(params.n_points, self.dx)
        
        # Initialize operators
        op_params = OperatorParameters(
            mass=params.mass,
            hbar=params.hbar,
            potential=params.potential,
            grid_spacing=self.dx
        )
        self.hamiltonian = Hamiltonian(op_params)
        
        # Initialize probability current calculator
        self.probability_current = ProbabilityCurrent(params.mass, params.hbar)
        
        # Initialize quantum potential calculator
        self.quantum_potential = QuantumPotential(params.mass, params.hbar)
    
    def create_gaussian_packet(self, x0: float = 0.0, p0: float = 0.0, 
                              sigma: float = 1.0) -> WaveFunction:
        """
        Create Gaussian wave packet initial condition.
        
        Args:
            x0: Center position
            p0: Initial momentum
            sigma: Width parameter
            
        Returns:
            Initial wave function
        """
        # Gaussian envelope
        gaussian = np.exp(-(self.x_grid - x0)**2 / (4 * sigma**2))
        
        # Momentum phase
        momentum_phase = np.exp(1j * p0 * self.x_grid / self.hbar)
        
        # Combine
        psi = gaussian * momentum_phase
        
        return WaveFunction(psi, self.x_grid, self.mass, self.hbar)
    
    def create_eigenstate(self, n: int = 0) -> WaveFunction:
        """
        Create nth eigenstate of the Hamiltonian.
        
        Args:
            n: Eigenstate index (0 = ground state)
            
        Returns:
            Eigenstate wave function
        """
        from .operators import EnergyOperator
        
        op_params = OperatorParameters(
            mass=self.mass,
            hbar=self.hbar,
            potential=self.params.potential,
            grid_spacing=self.dx
        )
        energy_op = EnergyOperator(op_params)
        
        eigenvalues, eigenfunctions = energy_op.solve_eigenvalues(
            self.x_grid, n_states=n+1
        )
        
        psi = eigenfunctions[:, n]
        return WaveFunction(psi, self.x_grid, self.mass, self.hbar)
    
    def evolve_step(self, psi: WaveFunction) -> WaveFunction:
        """
        Evolve wave function one time step using split-operator method.
        
        Args:
            psi: Current wave function
            
        Returns:
            Evolved wave function
        """
        # Split-operator method: exp(-iĤdt/ℏ) ≈ exp(-iVdt/(2ℏ)) exp(-iTdt/ℏ) exp(-iVdt/(2ℏ))
        
        # Step 1: Half step in position space (potential)
        if self.params.potential is not None:
            V_values = self.params.potential(self.x_grid)
            psi.psi *= np.exp(-1j * V_values * self.dt / (2 * self.hbar))
        
        # Step 2: Full step in momentum space (kinetic)
        psi_k = fft(psi.psi)
        kinetic_phase = np.exp(-1j * self.hbar * self.k_grid**2 * self.dt / (2 * self.mass))
        psi_k *= kinetic_phase
        psi.psi = ifft(psi_k)
        
        # Step 3: Half step in position space (potential)
        if self.params.potential is not None:
            V_values = self.params.potential(self.x_grid)
            psi.psi *= np.exp(-1j * V_values * self.dt / (2 * self.hbar))
        
        # Normalize
        psi.normalize()
        
        return psi
    
    def evolve(self, psi: WaveFunction, n_steps: int) -> Tuple[WaveFunction, np.ndarray]:
        """
        Evolve wave function for multiple time steps.
        
        Args:
            psi: Initial wave function
            n_steps: Number of time steps
            
        Returns:
            Final wave function and time array
        """
        psi_evolved = psi.copy()
        time_array = np.arange(n_steps) * self.dt
        
        for _ in range(n_steps):
            psi_evolved = self.evolve_step(psi_evolved)
        
        return psi_evolved, time_array
    
    def evolve_trajectory(self, psi: WaveFunction, n_steps: int) -> Tuple[np.ndarray, np.ndarray]:
        """
        Evolve wave function and return full trajectory.
        
        Args:
            psi: Initial wave function
            n_steps: Number of time steps
            
        Returns:
            Wave function trajectory and time array
        """
        psi_trajectory = np.zeros((n_steps, len(self.x_grid)), dtype=complex)
        time_array = np.arange(n_steps) * self.dt
        
        psi_current = psi.copy()
        for i in range(n_steps):
            psi_trajectory[i] = psi_current.psi
            psi_current = self.evolve_step(psi_current)
        
        return psi_trajectory, time_array
    
    def calculate_observables(self, psi: WaveFunction) -> Dict[str, float]:
        """
        Calculate quantum observables.
        
        Args:
            psi: Wave function
            
        Returns:
            Dictionary of observables
        """
        dx = self.dx
        
        # Position expectation value
        x_expectation = np.sum(psi.probability_density * self.x_grid) * dx
        
        # Momentum expectation value
        p_expectation = psi.expectation_value(
            lambda psi, x: -1j * self.hbar * np.gradient(psi, dx)
        ).real
        
        # Energy expectation value
        E_expectation = psi.expectation_value(
            lambda psi, x: self.hamiltonian.apply(psi, x)
        ).real
        
        # Position uncertainty (standard deviation)
        x2_expectation = np.sum(psi.probability_density * self.x_grid**2) * dx
        x_uncertainty = np.sqrt(x2_expectation - x_expectation**2)
        
        # Probability current
        j = self.probability_current.calculate(psi.psi, self.x_grid)
        j_max = np.max(np.abs(j))
        
        return {
            'position': x_expectation,
            'momentum': p_expectation,
            'energy': E_expectation,
            'position_uncertainty': x_uncertainty,
            'max_probability_current': j_max
        }
    
    def tunneling_probability(self, psi: WaveFunction, barrier_region: Tuple[float, float]) -> float:
        """
        Calculate tunneling probability through a barrier region.
        
        Args:
            psi: Wave function
            barrier_region: (x_min, x_max) defining barrier region
            
        Returns:
            Tunneling probability
        """
        x_min, x_max = barrier_region
        
        # Find indices corresponding to barrier region
        barrier_mask = (self.x_grid >= x_min) & (self.x_grid <= x_max)
        
        # Calculate probability inside barrier
        dx = self.dx
        barrier_probability = np.sum(psi.probability_density[barrier_mask]) * dx
        
        return barrier_probability
