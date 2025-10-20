"""
Quantum operators for void physics.

This module implements fundamental quantum operators including Hamiltonian,
momentum, and energy operators with eigenvalue solvers.
"""

import numpy as np
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Callable, Dict, Optional, Tuple, Union

from ..utils.constants import PhysicalConstants


@dataclass
class OperatorParameters:
    """Parameters for quantum operators."""
    
    mass: float = 1.0  # Particle mass
    hbar: float = 1.0  # Reduced Planck constant
    potential: Optional[Callable] = None  # Potential function V(x)
    grid_spacing: float = 0.1  # Spatial grid spacing


class QuantumOperator(ABC):
    """Abstract base class for quantum operators."""
    
    def __init__(self, params: OperatorParameters):
        self.params = params
        self.mass = params.mass
        self.hbar = params.hbar
        self.potential = params.potential
        self.dx = params.grid_spacing
    
    @abstractmethod
    def matrix_representation(self, x_grid: np.ndarray) -> np.ndarray:
        """Get matrix representation of operator on spatial grid."""
        pass
    
    @abstractmethod
    def apply(self, psi: np.ndarray, x_grid: np.ndarray) -> np.ndarray:
        """Apply operator to wave function."""
        pass


class MomentumOperator(QuantumOperator):
    """
    Momentum operator: p̂ = -iℏ∇
    
    In position representation, this becomes a derivative operator.
    """
    
    def matrix_representation(self, x_grid: np.ndarray) -> np.ndarray:
        """Get momentum operator matrix using finite differences."""
        n = len(x_grid)
        dx = x_grid[1] - x_grid[0]
        
        # Create derivative matrix using central differences
        momentum_matrix = np.zeros((n, n), dtype=complex)
        
        for i in range(1, n-1):
            momentum_matrix[i, i-1] = -1j * self.hbar / (2 * dx)
            momentum_matrix[i, i+1] = 1j * self.hbar / (2 * dx)
        
        # Boundary conditions (forward/backward differences)
        if n > 1:
            momentum_matrix[0, 1] = 1j * self.hbar / dx
            momentum_matrix[-1, -2] = -1j * self.hbar / dx
            
        return momentum_matrix
    
    def apply(self, psi: np.ndarray, x_grid: np.ndarray) -> np.ndarray:
        """Apply momentum operator using finite differences."""
        dx = x_grid[1] - x_grid[0]
        dpsi_dx = np.gradient(psi, dx)
        return -1j * self.hbar * dpsi_dx


class Hamiltonian(QuantumOperator):
    """
    Hamiltonian operator: Ĥ = p̂²/(2m) + V(x)
    
    Combines kinetic and potential energy terms.
    """
    
    def __init__(self, params: OperatorParameters):
        super().__init__(params)
        self.momentum_op = MomentumOperator(params)
    
    def matrix_representation(self, x_grid: np.ndarray) -> np.ndarray:
        """Get Hamiltonian matrix representation."""
        n = len(x_grid)
        dx = x_grid[1] - x_grid[0]
        
        # Kinetic energy matrix (second derivative)
        kinetic_matrix = np.zeros((n, n), dtype=complex)
        
        for i in range(1, n-1):
            kinetic_matrix[i, i-1] = -self.hbar**2 / (2 * self.mass * dx**2)
            kinetic_matrix[i, i] = self.hbar**2 / (self.mass * dx**2)
            kinetic_matrix[i, i+1] = -self.hbar**2 / (2 * self.mass * dx**2)
        
        # Boundary conditions
        if n > 1:
            kinetic_matrix[0, 0] = self.hbar**2 / (self.mass * dx**2)
            kinetic_matrix[0, 1] = -self.hbar**2 / (2 * self.mass * dx**2)
            kinetic_matrix[-1, -1] = self.hbar**2 / (self.mass * dx**2)
            kinetic_matrix[-1, -2] = -self.hbar**2 / (2 * self.mass * dx**2)
        
        # Add potential energy
        if self.potential is not None:
            potential_values = self.potential(x_grid)
            kinetic_matrix += np.diag(potential_values)
        
        return kinetic_matrix
    
    def apply(self, psi: np.ndarray, x_grid: np.ndarray) -> np.ndarray:
        """Apply Hamiltonian operator."""
        dx = x_grid[1] - x_grid[0]
        
        # Kinetic energy: -ℏ²/(2m) ∇²ψ
        d2psi_dx2 = np.gradient(np.gradient(psi, dx), dx)
        kinetic_term = -self.hbar**2 / (2 * self.mass) * d2psi_dx2
        
        # Potential energy: V(x)ψ
        if self.potential is not None:
            potential_values = self.potential(x_grid)
            potential_term = potential_values * psi
        else:
            potential_term = 0
        
        return kinetic_term + potential_term


class EnergyOperator(QuantumOperator):
    """
    Energy operator for eigenvalue problems: Ĥψ = Eψ
    """
    
    def __init__(self, params: OperatorParameters):
        super().__init__(params)
        self.hamiltonian = Hamiltonian(params)
    
    def solve_eigenvalues(self, x_grid: np.ndarray, n_states: int = 10) -> Tuple[np.ndarray, np.ndarray]:
        """
        Solve eigenvalue problem: Ĥψ = Eψ
        
        Args:
            x_grid: Spatial grid
            n_states: Number of eigenstates to compute
            
        Returns:
            eigenvalues: Energy eigenvalues
            eigenfunctions: Corresponding eigenfunctions
        """
        H_matrix = self.hamiltonian.matrix_representation(x_grid)
        
        # Solve eigenvalue problem
        eigenvalues, eigenfunctions = np.linalg.eigh(H_matrix)
        
        # Return only the requested number of states
        return eigenvalues[:n_states], eigenfunctions[:, :n_states]
    
    def apply(self, psi: np.ndarray, x_grid: np.ndarray) -> np.ndarray:
        """Apply energy operator (same as Hamiltonian)."""
        return self.hamiltonian.apply(psi, x_grid)


class QuantumPotential:
    """
    Quantum potential: V_quantum = -(ℏ²/2m)(∇²√ρ)/√ρ
    
    This represents the "quantum force" that emerges from the wave function
    and can be related to void physics emergence mechanisms.
    """
    
    def __init__(self, mass: float = 1.0, hbar: float = 1.0):
        self.mass = mass
        self.hbar = hbar
    
    def calculate(self, psi: np.ndarray, x_grid: np.ndarray) -> np.ndarray:
        """
        Calculate quantum potential from wave function.
        
        Args:
            psi: Wave function
            x_grid: Spatial grid
            
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
        V_quantum = -(self.hbar**2 / (2 * self.mass)) * d2_sqrt_rho_dx2 / sqrt_rho
        
        return V_quantum.real  # Should be real
    
    def force(self, psi: np.ndarray, x_grid: np.ndarray) -> np.ndarray:
        """
        Calculate quantum force: F = -∇V_quantum
        
        Args:
            psi: Wave function
            x_grid: Spatial grid
            
        Returns:
            Quantum force values
        """
        V_quantum = self.calculate(psi, x_grid)
        dx = x_grid[1] - x_grid[0]
        force = -np.gradient(V_quantum, dx)
        
        return force
