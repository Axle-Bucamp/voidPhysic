"""
Relativistic quantum equations for void physics.

This module implements Klein-Gordon and Dirac equations as lightweight
extensions to the non-relativistic Schrodinger framework.
"""

import numpy as np
from dataclasses import dataclass
from typing import Any, Callable, Dict, Optional, Tuple, Union

from .operators import OperatorParameters


@dataclass
class RelativisticParameters:
    """Parameters for relativistic quantum equations."""
    
    mass: float = 1.0  # Rest mass
    c: float = 1.0  # Speed of light (natural units)
    hbar: float = 1.0  # Reduced Planck constant
    dt: float = 0.01  # Time step
    x_min: float = -10.0  # Minimum spatial coordinate
    x_max: float = 10.0  # Maximum spatial coordinate
    n_points: int = 1024  # Number of spatial grid points
    potential: Optional[Callable] = None  # Potential function V(x)


class KleinGordonSolver:
    """
    Klein-Gordon equation solver: (1/c² ∂²/∂t² - ∇² + (mc/ℏ)²)φ = 0
    
    This describes spin-0 relativistic particles and can be related to
    scalar field evolution in void physics.
    """
    
    def __init__(self, params: RelativisticParameters):
        self.params = params
        self.mass = params.mass
        self.c = params.c
        self.hbar = params.hbar
        self.dt = params.dt
        
        # Set up spatial grid
        self.x_grid = np.linspace(params.x_min, params.x_max, params.n_points)
        self.dx = self.x_grid[1] - self.x_grid[0]
        
        # Klein-Gordon dispersion relation: ω² = c²k² + (mc²/ℏ)²
        self.k_grid = 2 * np.pi * np.fft.fftfreq(params.n_points, self.dx)
        self.omega_grid = np.sqrt(
            (self.c * self.k_grid)**2 + (self.mass * self.c**2 / self.hbar)**2
        )
    
    def create_gaussian_field(self, x0: float = 0.0, k0: float = 0.0, 
                             sigma: float = 1.0) -> Tuple[np.ndarray, np.ndarray]:
        """
        Create Gaussian field initial condition.
        
        Args:
            x0: Center position
            k0: Initial wavenumber
            sigma: Width parameter
            
        Returns:
            Initial field and its time derivative
        """
        # Gaussian envelope
        gaussian = np.exp(-(self.x_grid - x0)**2 / (4 * sigma**2))
        
        # Wavenumber phase
        k_phase = np.exp(1j * k0 * self.x_grid)
        
        # Initial field
        phi = gaussian * k_phase
        
        # Initial time derivative (for second-order equation)
        omega0 = np.sqrt((self.c * k0)**2 + (self.mass * self.c**2 / self.hbar)**2)
        dphi_dt = -1j * omega0 * phi
        
        return phi, dphi_dt
    
    def evolve_step(self, phi: np.ndarray, dphi_dt: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Evolve Klein-Gordon field one time step.
        
        Args:
            phi: Current field
            dphi_dt: Current time derivative
            
        Returns:
            Evolved field and time derivative
        """
        # Convert to momentum space
        phi_k = np.fft.fft(phi)
        dphi_dt_k = np.fft.fft(dphi_dt)
        
        # Time evolution in momentum space
        cos_term = np.cos(self.omega_grid * self.dt)
        sin_term = np.sin(self.omega_grid * self.dt)
        
        # New field
        phi_new_k = phi_k * cos_term + dphi_dt_k * sin_term / self.omega_grid
        phi_new = np.fft.ifft(phi_new_k)
        
        # New time derivative
        dphi_dt_new_k = -phi_k * self.omega_grid * sin_term + dphi_dt_k * cos_term
        dphi_dt_new = np.fft.ifft(dphi_dt_new_k)
        
        return phi_new, dphi_dt_new
    
    def energy_density(self, phi: np.ndarray, dphi_dt: np.ndarray) -> np.ndarray:
        """
        Calculate energy density of Klein-Gordon field.
        
        Args:
            phi: Field values
            dphi_dt: Time derivative
            
        Returns:
            Energy density
        """
        # Spatial derivative
        dphi_dx = np.gradient(phi, self.dx)
        
        # Energy density: (1/2)[(1/c²)(∂φ/∂t)² + (∇φ)² + (mc/ℏ)²φ²]
        energy_density = 0.5 * (
            np.abs(dphi_dt)**2 / self.c**2 +
            np.abs(dphi_dx)**2 +
            (self.mass * self.c / self.hbar)**2 * np.abs(phi)**2
        )
        
        return energy_density.real


class DiracSolver:
    """
    Dirac equation solver: (iℏγ^μ∂_μ - mc)ψ = 0
    
    This describes spin-1/2 relativistic particles. For simplicity,
    we implement a 1D version with 2-component spinors.
    """
    
    def __init__(self, params: RelativisticParameters):
        self.params = params
        self.mass = params.mass
        self.c = params.c
        self.hbar = params.hbar
        self.dt = params.dt
        
        # Set up spatial grid
        self.x_grid = np.linspace(params.x_min, params.x_max, params.n_points)
        self.dx = self.x_grid[1] - self.x_grid[0]
        
        # Pauli matrices for 2-component spinor
        self.sigma_x = np.array([[0, 1], [1, 0]], dtype=complex)
        self.sigma_y = np.array([[0, -1j], [1j, 0]], dtype=complex)
        self.sigma_z = np.array([[1, 0], [0, -1]], dtype=complex)
        
        # Dirac matrices (1D version)
        self.gamma_0 = np.array([[1, 0], [0, -1]], dtype=complex)
        self.gamma_1 = np.array([[0, 1], [-1, 0]], dtype=complex)
    
    def create_gaussian_spinor(self, x0: float = 0.0, p0: float = 0.0, 
                              sigma: float = 1.0, spin_up: bool = True) -> np.ndarray:
        """
        Create Gaussian spinor initial condition.
        
        Args:
            x0: Center position
            p0: Initial momentum
            sigma: Width parameter
            spin_up: Spin orientation
            
        Returns:
            Initial spinor (2-component)
        """
        # Gaussian envelope
        gaussian = np.exp(-(self.x_grid - x0)**2 / (4 * sigma**2))
        
        # Momentum phase
        momentum_phase = np.exp(1j * p0 * self.x_grid / self.hbar)
        
        # Spinor components
        psi = np.zeros((2, len(self.x_grid)), dtype=complex)
        
        if spin_up:
            psi[0] = gaussian * momentum_phase  # Upper component
            psi[1] = 0.1 * gaussian * momentum_phase  # Small lower component
        else:
            psi[0] = 0.1 * gaussian * momentum_phase  # Small upper component
            psi[1] = gaussian * momentum_phase  # Lower component
        
        return psi
    
    def evolve_step(self, psi: np.ndarray) -> np.ndarray:
        """
        Evolve Dirac spinor one time step.
        
        Args:
            psi: Current spinor (2 x n_points)
            
        Returns:
            Evolved spinor
        """
        # Convert to momentum space
        psi_k = np.fft.fft(psi, axis=1)
        
        # Momentum grid
        k_grid = 2 * np.pi * np.fft.fftfreq(len(self.x_grid), self.dx)
        
        # Dirac Hamiltonian in momentum space: H = cα·p + βmc²
        # where α = γ⁰γ and β = γ⁰
        alpha = self.gamma_0 @ self.gamma_1
        beta = self.gamma_0
        
        # Time evolution operator: U = exp(-iHdt/ℏ)
        for i, k in enumerate(k_grid):
            H = self.c * alpha * k + beta * self.mass * self.c**2
            U = np.linalg.matrix_power(
                np.eye(2) - 1j * H * self.dt / self.hbar, 1
            )
            psi_k[:, i] = U @ psi_k[:, i]
        
        # Convert back to position space
        psi_new = np.fft.ifft(psi_k, axis=1)
        
        return psi_new
    
    def probability_density(self, psi: np.ndarray) -> np.ndarray:
        """
        Calculate probability density of Dirac spinor.
        
        Args:
            psi: Spinor (2 x n_points)
            
        Returns:
            Probability density
        """
        # Probability density: ψ†ψ = |ψ₁|² + |ψ₂|²
        return np.sum(np.abs(psi)**2, axis=0)
    
    def current_density(self, psi: np.ndarray) -> np.ndarray:
        """
        Calculate current density of Dirac spinor.
        
        Args:
            psi: Spinor (2 x n_points)
            
        Returns:
            Current density
        """
        # Current density: j = cψ†αψ
        alpha = self.gamma_0 @ self.gamma_1
        j = np.zeros(len(self.x_grid), dtype=complex)
        
        for i in range(len(self.x_grid)):
            psi_i = psi[:, i]
            j[i] = self.c * np.conj(psi_i) @ alpha @ psi_i
        
        return j.real
    
    def spin_expectation(self, psi: np.ndarray) -> np.ndarray:
        """
        Calculate spin expectation value.
        
        Args:
            psi: Spinor (2 x n_points)
            
        Returns:
            Spin expectation value
        """
        # Spin expectation: ⟨σ⟩ = ψ†σψ / (ψ†ψ)
        spin_expectation = np.zeros(len(self.x_grid))
        
        for i in range(len(self.x_grid)):
            psi_i = psi[:, i]
            norm = np.conj(psi_i) @ psi_i
            if norm > 1e-10:
                spin_expectation[i] = (np.conj(psi_i) @ self.sigma_z @ psi_i / norm).real
        
        return spin_expectation


class RelativisticComparison:
    """
    Compare Schrodinger, Klein-Gordon, and Dirac equations.
    """
    
    def __init__(self, params: RelativisticParameters):
        self.params = params
        
        # Initialize solvers
        from .schrodinger import SchrodingerSolver, SchrodingerParameters
        
        schrodinger_params = SchrodingerParameters(
            mass=params.mass,
            hbar=params.hbar,
            dt=params.dt,
            x_min=params.x_min,
            x_max=params.x_max,
            n_points=params.n_points,
            potential=params.potential
        )
        
        self.schrodinger_solver = SchrodingerSolver(schrodinger_params)
        self.klein_gordon_solver = KleinGordonSolver(params)
        self.dirac_solver = DiracSolver(params)
    
    def compare_dispersion(self, k_range: Tuple[float, float] = (-5.0, 5.0), 
                          n_points: int = 100) -> Dict[str, np.ndarray]:
        """
        Compare dispersion relations of different equations.
        
        Args:
            k_range: Range of wavenumbers
            n_points: Number of points
            
        Returns:
            Dictionary with dispersion relations
        """
        k_values = np.linspace(k_range[0], k_range[1], n_points)
        
        # Schrodinger: E = ℏ²k²/(2m)
        E_schrodinger = self.params.hbar**2 * k_values**2 / (2 * self.params.mass)
        
        # Klein-Gordon: E = √(c²k² + (mc²/ℏ)²)
        E_klein_gordon = np.sqrt(
            (self.params.c * k_values)**2 + 
            (self.params.mass * self.params.c**2 / self.params.hbar)**2
        )
        
        # Dirac: E = ±√(c²k² + (mc²/ℏ)²) (positive and negative energy)
        E_dirac_positive = E_klein_gordon
        E_dirac_negative = -E_klein_gordon
        
        return {
            'k_values': k_values,
            'schrodinger': E_schrodinger,
            'klein_gordon': E_klein_gordon,
            'dirac_positive': E_dirac_positive,
            'dirac_negative': E_dirac_negative
        }
    
    def compare_evolution(self, initial_conditions: Dict[str, Any], 
                         n_steps: int = 100) -> Dict[str, np.ndarray]:
        """
        Compare time evolution of different equations.
        
        Args:
            initial_conditions: Initial conditions for each solver
            n_steps: Number of time steps
            
        Returns:
            Dictionary with evolution results
        """
        results = {}
        
        # Schrodinger evolution
        if 'schrodinger' in initial_conditions:
            psi_init = self.schrodinger_solver.create_gaussian_packet(**initial_conditions['schrodinger'])
            psi_final, _ = self.schrodinger_solver.evolve(psi_init, n_steps)
            results['schrodinger'] = psi_final.probability_density
        
        # Klein-Gordon evolution
        if 'klein_gordon' in initial_conditions:
            phi_init, dphi_dt_init = self.klein_gordon_solver.create_gaussian_field(
                **initial_conditions['klein_gordon']
            )
            phi_current = phi_init.copy()
            dphi_dt_current = dphi_dt_init.copy()
            
            for _ in range(n_steps):
                phi_current, dphi_dt_current = self.klein_gordon_solver.evolve_step(
                    phi_current, dphi_dt_current
                )
            
            results['klein_gordon'] = np.abs(phi_current)**2
        
        # Dirac evolution
        if 'dirac' in initial_conditions:
            psi_init = self.dirac_solver.create_gaussian_spinor(**initial_conditions['dirac'])
            psi_current = psi_init.copy()
            
            for _ in range(n_steps):
                psi_current = self.dirac_solver.evolve_step(psi_current)
            
            results['dirac'] = self.dirac_solver.probability_density(psi_current)
        
        return results
