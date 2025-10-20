"""
Quantum field theory for void physics.

This module implements field operators, particle creation/annihilation,
and field evolution that connects to void particle emergence mechanisms.
"""

import numpy as np
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional, Tuple, Union
from abc import ABC, abstractmethod

from .operators import OperatorParameters


@dataclass
class FieldParameters:
    """Parameters for quantum field theory."""
    
    mass: float = 1.0  # Field mass
    hbar: float = 1.0  # Reduced Planck constant
    c: float = 1.0  # Speed of light
    coupling: float = 1.0  # Self-coupling strength
    x_min: float = -10.0  # Minimum spatial coordinate
    x_max: float = 10.0  # Maximum spatial coordinate
    n_points: int = 1024  # Number of spatial grid points
    dt: float = 0.01  # Time step


class FieldOperator:
    """
    Quantum field operator with creation and annihilation operators.
    
    In QFT, particles are excitations of quantum fields. This connects
    to void physics where particles emerge from field fluctuations.
    """
    
    def __init__(self, params: FieldParameters):
        self.params = params
        self.mass = params.mass
        self.hbar = params.hbar
        self.c = params.c
        self.coupling = params.coupling
        
        # Set up spatial grid
        self.x_grid = np.linspace(params.x_min, params.x_max, params.n_points)
        self.dx = self.x_grid[1] - self.x_grid[0]
        
        # Momentum grid for field modes
        self.k_grid = 2 * np.pi * np.fft.fftfreq(params.n_points, self.dx)
        
        # Field mode frequencies: ω_k = √(c²k² + (mc²/ℏ)²)
        self.omega_grid = np.sqrt(
            (self.c * self.k_grid)**2 + (self.mass * self.c**2 / self.hbar)**2
        )
        
        # Avoid division by zero
        self.omega_grid = np.maximum(self.omega_grid, 1e-10)
    
    def vacuum_state(self) -> np.ndarray:
        """
        Create vacuum state (no particles).
        
        Returns:
            Vacuum field configuration
        """
        return np.zeros(len(self.x_grid), dtype=complex)
    
    def create_particle(self, k: float, amplitude: float = 1.0) -> np.ndarray:
        """
        Create a particle with momentum k.
        
        Args:
            k: Momentum
            amplitude: Creation amplitude
            
        Returns:
            Field configuration with one particle
        """
        # Find closest k value in grid
        k_index = np.argmin(np.abs(self.k_grid - k))
        k_actual = self.k_grid[k_index]
        omega = self.omega_grid[k_index]
        
        # Single particle state: |1_k⟩
        # Field mode: φ_k(x) = (1/√(2ω_k)) * exp(ikx)
        field_mode = amplitude / np.sqrt(2 * omega) * np.exp(1j * k_actual * self.x_grid)
        
        return field_mode
    
    def create_multiple_particles(self, k_values: List[float], 
                                 amplitudes: Optional[List[float]] = None) -> np.ndarray:
        """
        Create multiple particles with different momenta.
        
        Args:
            k_values: List of momenta
            amplitudes: List of amplitudes (default: all 1.0)
            
        Returns:
            Field configuration with multiple particles
        """
        if amplitudes is None:
            amplitudes = [1.0] * len(k_values)
        
        field = self.vacuum_state()
        
        for k, amp in zip(k_values, amplitudes):
            particle_field = self.create_particle(k, amp)
            field += particle_field
        
        return field
    
    def particle_number(self, field: np.ndarray) -> float:
        """
        Calculate expected particle number in field.
        
        Args:
            field: Field configuration
            
        Returns:
            Expected particle number
        """
        # Convert to momentum space
        field_k = np.fft.fft(field)
        
        # Particle number: N = Σ_k |a_k|² where a_k are mode amplitudes
        # For each mode: |a_k|² = (2ω_k) * |φ_k|²
        mode_amplitudes = np.abs(field_k)**2
        particle_numbers = 2 * self.omega_grid * mode_amplitudes
        
        return np.sum(particle_numbers).real
    
    def energy_density(self, field: np.ndarray) -> np.ndarray:
        """
        Calculate energy density of field.
        
        Args:
            field: Field configuration
            
        Returns:
            Energy density
        """
        # Convert to momentum space
        field_k = np.fft.fft(field)
        
        # Energy density in momentum space: E_k = ω_k |a_k|²
        energy_k = self.omega_grid * np.abs(field_k)**2
        
        # Convert back to position space
        energy_density = np.fft.ifft(energy_k)
        
        return energy_density.real


class QuantumField:
    """
    Quantum field with time evolution and interactions.
    
    This represents a scalar field that can create/annihilate particles
    and connects to void physics emergence mechanisms.
    """
    
    def __init__(self, params: FieldParameters):
        self.params = params
        self.field_operator = FieldOperator(params)
        
        # Current field state
        self.field = self.field_operator.vacuum_state()
        self.time = 0.0
        
        # Interaction potential (for self-interactions)
        self.interaction_strength = params.coupling
    
    def set_field(self, field: np.ndarray) -> None:
        """Set current field configuration."""
        self.field = field.copy()
    
    def evolve_step(self) -> None:
        """
        Evolve field one time step using field equations.
        
        For a scalar field: ∂²φ/∂t² = ∇²φ - m²φ - λφ³
        """
        dt = self.params.dt
        dx = self.field_operator.dx
        
        # Current field and its time derivative (stored as imaginary part)
        if np.iscomplexobj(self.field):
            phi = self.field.real
            dphi_dt = self.field.imag
        else:
            phi = self.field
            dphi_dt = np.zeros_like(phi)
        
        # Field equation: ∂²φ/∂t² = ∇²φ - m²φ - λφ³
        d2phi_dx2 = np.gradient(np.gradient(phi, dx), dx)
        
        # Mass term
        mass_term = (self.params.mass * self.params.c / self.params.hbar)**2 * phi
        
        # Interaction term (self-coupling)
        interaction_term = self.params.coupling * phi**3
        
        # Second time derivative
        d2phi_dt2 = d2phi_dx2 - mass_term - interaction_term
        
        # Update field using leapfrog method
        phi_new = phi + dphi_dt * dt + 0.5 * d2phi_dt2 * dt**2
        dphi_dt_new = dphi_dt + d2phi_dt2 * dt
        
        # Store as complex field (real part = field, imaginary part = time derivative)
        self.field = phi_new + 1j * dphi_dt_new
        self.time += dt
    
    def evolve(self, n_steps: int) -> Tuple[np.ndarray, np.ndarray]:
        """
        Evolve field for multiple time steps.
        
        Args:
            n_steps: Number of time steps
            
        Returns:
            Field trajectory and time array
        """
        field_trajectory = np.zeros((n_steps, len(self.field)), dtype=complex)
        time_array = np.zeros(n_steps)
        
        for i in range(n_steps):
            field_trajectory[i] = self.field.copy()
            time_array[i] = self.time
            self.evolve_step()
        
        return field_trajectory, time_array
    
    def create_particle_emergence(self, k_emergence: float, 
                                 emergence_rate: float = 0.1) -> None:
        """
        Simulate particle emergence from void (field fluctuations).
        
        Args:
            k_emergence: Momentum of emerging particle
            emergence_rate: Probability of emergence per time step
        """
        if np.random.random() < emergence_rate:
            # Create new particle
            new_particle = self.field_operator.create_particle(k_emergence)
            
            # Add to existing field
            self.field += new_particle
    
    def get_particle_positions(self, threshold: float = 0.1) -> List[float]:
        """
        Extract particle positions from field configuration.
        
        Args:
            threshold: Minimum field amplitude to consider as particle
            
        Returns:
            List of particle positions
        """
        field_amplitude = np.abs(self.field)
        particle_positions = []
        
        # Find peaks in field amplitude
        for i in range(1, len(field_amplitude) - 1):
            if (field_amplitude[i] > threshold and 
                field_amplitude[i] > field_amplitude[i-1] and 
                field_amplitude[i] > field_amplitude[i+1]):
                particle_positions.append(self.field_operator.x_grid[i])
        
        return particle_positions
    
    def calculate_observables(self) -> Dict[str, float]:
        """
        Calculate field observables.
        
        Returns:
            Dictionary of observables
        """
        # Particle number
        particle_number = self.field_operator.particle_number(self.field)
        
        # Total energy
        energy_density = self.field_operator.energy_density(self.field)
        total_energy = np.sum(energy_density) * self.field_operator.dx
        
        # Field variance (measure of fluctuations)
        field_variance = np.var(np.abs(self.field))
        
        # Number of particles (from positions)
        particle_positions = self.get_particle_positions()
        num_particles = len(particle_positions)
        
        return {
            'particle_number': particle_number,
            'total_energy': total_energy,
            'field_variance': field_variance,
            'num_particles': num_particles,
            'time': self.time
        }


class ParticleCreation:
    """
    Particle creation/annihilation events in quantum field.
    
    This connects quantum field theory to void physics by modeling
    how particles emerge from field fluctuations.
    """
    
    def __init__(self, field: QuantumField):
        self.field = field
        self.creation_events = []
        self.annihilation_events = []
    
    def vacuum_fluctuation(self, amplitude: float = 0.1) -> None:
        """
        Add vacuum fluctuation to field.
        
        Args:
            amplitude: Fluctuation amplitude
        """
        # Random fluctuation in momentum space
        k_random = np.random.choice(self.field.field_operator.k_grid)
        fluctuation = self.field.field_operator.create_particle(k_random, amplitude)
        
        # Add to field
        self.field.field += fluctuation
    
    def particle_creation_event(self, k: float, amplitude: float = 1.0) -> None:
        """
        Create a particle creation event.
        
        Args:
            k: Particle momentum
            amplitude: Creation amplitude
        """
        # Create particle
        new_particle = self.field.field_operator.create_particle(k, amplitude)
        self.field.field += new_particle
        
        # Record event
        self.creation_events.append({
            'time': self.field.time,
            'momentum': k,
            'amplitude': amplitude,
            'position': self._find_creation_position(new_particle)
        })
    
    def particle_annihilation_event(self, position: float, 
                                   annihilation_rate: float = 0.1) -> bool:
        """
        Attempt particle annihilation at given position.
        
        Args:
            position: Position for annihilation
            annihilation_rate: Probability of annihilation
            
        Returns:
            True if annihilation occurred
        """
        if np.random.random() < annihilation_rate:
            # Find closest grid point
            pos_index = np.argmin(np.abs(self.field.field_operator.x_grid - position))
            
            # Reduce field amplitude at that position
            reduction_factor = 0.5
            self.field.field[pos_index] *= reduction_factor
            
            # Record event
            self.annihilation_events.append({
                'time': self.field.time,
                'position': position,
                'reduction_factor': reduction_factor
            })
            
            return True
        
        return False
    
    def _find_creation_position(self, particle_field: np.ndarray) -> float:
        """Find position where particle was created."""
        max_index = np.argmax(np.abs(particle_field))
        return self.field.field_operator.x_grid[max_index]
    
    def get_creation_rate(self, time_window: float = 1.0) -> float:
        """
        Calculate particle creation rate.
        
        Args:
            time_window: Time window for rate calculation
            
        Returns:
            Creation rate (particles per unit time)
        """
        recent_events = [
            event for event in self.creation_events
            if self.field.time - event['time'] <= time_window
        ]
        
        return len(recent_events) / time_window
    
    def simulate_void_emergence(self, n_steps: int, 
                               emergence_rate: float = 0.01) -> Dict[str, Any]:
        """
        Simulate particle emergence from void over time.
        
        Args:
            n_steps: Number of time steps
            emergence_rate: Probability of emergence per step
            
        Returns:
            Simulation results
        """
        results = {
            'time': [],
            'particle_count': [],
            'total_energy': [],
            'creation_events': [],
            'field_evolution': []
        }
        
        for step in range(n_steps):
            # Random emergence from void
            if np.random.random() < emergence_rate:
                # Random momentum for emerging particle
                k_random = np.random.uniform(-2.0, 2.0)
                self.particle_creation_event(k_random)
            
            # Evolve field
            self.field.evolve_step()
            
            # Calculate observables
            observables = self.field.calculate_observables()
            
            # Store results
            results['time'].append(self.field.time)
            results['particle_count'].append(observables['num_particles'])
            results['total_energy'].append(observables['total_energy'])
            results['field_evolution'].append(self.field.field.copy())
        
        return results
