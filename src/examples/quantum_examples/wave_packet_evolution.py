#!/usr/bin/env python3
"""
Wave Packet Evolution Example

Demonstrates the evolution of quantum wave packets in different potentials,
showing spreading, interference, and quantum effects.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from void_physic.quantum.schrodinger import SchrodingerSolver, SchrodingerParameters
from void_physic.quantum.operators import QuantumPotential


def create_harmonic_potential(omega: float = 1.0):
    """Create harmonic oscillator potential."""
    def potential(x):
        return 0.5 * omega**2 * x**2
    return potential


def create_anharmonic_potential(omega: float = 1.0, anharmonicity: float = 0.1):
    """Create anharmonic oscillator potential."""
    def potential(x):
        return 0.5 * omega**2 * x**2 + anharmonicity * x**4
    return potential


def create_quartic_potential(alpha: float = 1.0):
    """Create quartic potential V(x) = αx⁴."""
    def potential(x):
        return alpha * x**4
    return potential


def run_wave_packet_spreading():
    """Demonstrate wave packet spreading in free space."""
    print("📡 Wave Packet Spreading in Free Space")
    print("=" * 50)
    
    # Set up parameters (no potential)
    params = SchrodingerParameters(
        mass=1.0,
        hbar=1.0,
        dt=0.01,
        x_min=-15.0,
        x_max=15.0,
        n_points=1024
    )
    
    # No potential (free particle)
    params.potential = lambda x: np.zeros_like(x)
    
    # Initialize solver
    solver = SchrodingerSolver(params)
    
    # Create initial wave packet
    psi_init = solver.create_gaussian_packet(x0=0.0, p0=0.0, sigma=1.0)
    
    print(f"Initial wave packet width: {psi_init.expectation_value(lambda psi, x: (x - solver.x_grid[np.argmax(np.abs(psi)**2)])**2).real**0.5:.3f}")
    
    # Evolve wave function
    n_steps = 300
    psi_trajectory, time_array = solver.evolve_trajectory(psi_init, n_steps)
    
    # Calculate spreading over time
    widths = []
    for psi in psi_trajectory:
        psi_temp = psi_init.copy()
        psi_temp.psi = psi
        obs = solver.calculate_observables(psi_temp)
        widths.append(obs['position_uncertainty'])
    
    # Create visualization
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle("Wave Packet Spreading in Free Space", fontsize=16)
    
    # Plot 1: Initial and final wave functions
    ax1 = axes[0, 0]
    ax1.plot(solver.x_grid, np.abs(psi_init.psi)**2, 'b-', linewidth=2, label='Initial |ψ|²')
    ax1.plot(solver.x_grid, np.abs(psi_trajectory[-1])**2, 'r-', linewidth=2, label='Final |ψ|²')
    ax1.set_xlabel('Position (x)')
    ax1.set_ylabel('Probability Density')
    ax1.set_title('Wave Packet Evolution')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Wave function evolution (heatmap)
    ax2 = axes[0, 1]
    psi_density = np.abs(psi_trajectory)**2
    im = ax2.imshow(psi_density, aspect='auto', origin='lower',
                   extent=[solver.x_grid[0], solver.x_grid[-1], 0, time_array[-1]],
                   cmap='viridis')
    ax2.set_xlabel('Position (x)')
    ax2.set_ylabel('Time (t)')
    ax2.set_title('Probability Density Evolution')
    plt.colorbar(im, ax=ax2, label='|ψ|²')
    
    # Plot 3: Width evolution
    ax3 = axes[1, 0]
    ax3.plot(time_array, widths, 'g-', linewidth=2)
    ax3.set_xlabel('Time (t)')
    ax3.set_ylabel('Wave Packet Width')
    ax3.set_title('Spreading Over Time')
    ax3.grid(True, alpha=0.3)
    
    # Plot 4: Phase evolution
    ax4 = axes[1, 1]
    phase_data = np.angle(psi_trajectory)
    im2 = ax4.imshow(phase_data, aspect='auto', origin='lower',
                    extent=[solver.x_grid[0], solver.x_grid[-1], 0, time_array[-1]],
                    cmap='hsv')
    ax4.set_xlabel('Position (x)')
    ax4.set_ylabel('Time (t)')
    ax4.set_title('Phase Evolution')
    plt.colorbar(im2, ax=ax4, label='Phase (rad)')
    
    plt.tight_layout()
    plt.show()
    
    print(f"Final wave packet width: {widths[-1]:.3f}")
    print(f"Spreading factor: {widths[-1]/widths[0]:.2f}")


def run_harmonic_oscillator():
    """Demonstrate wave packet in harmonic oscillator potential."""
    print("\n🎵 Harmonic Oscillator")
    print("=" * 50)
    
    # Set up parameters
    params = SchrodingerParameters(
        mass=1.0,
        hbar=1.0,
        dt=0.01,
        x_min=-8.0,
        x_max=8.0,
        n_points=512
    )
    
    # Create harmonic potential
    omega = 1.0
    params.potential = create_harmonic_potential(omega)
    
    # Initialize solver
    solver = SchrodingerSolver(params)
    
    # Create initial wave packet (displaced from equilibrium)
    psi_init = solver.create_gaussian_packet(x0=2.0, p0=0.0, sigma=0.8)
    
    # Evolve wave function
    n_steps = 400
    psi_trajectory, time_array = solver.evolve_trajectory(psi_init, n_steps)
    
    # Calculate observables over time
    observables = []
    for psi in psi_trajectory:
        psi_temp = psi_init.copy()
        psi_temp.psi = psi
        obs = solver.calculate_observables(psi_temp)
        observables.append(obs)
    
    # Create visualization
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle("Harmonic Oscillator Evolution", fontsize=16)
    
    # Plot 1: Potential and wave function at different times
    ax1 = axes[0, 0]
    V_values = params.potential(solver.x_grid)
    ax1.plot(solver.x_grid, V_values, 'r-', linewidth=2, label='V(x) = ½ω²x²')
    
    # Show wave function at different times
    time_indices = [0, n_steps//4, n_steps//2, 3*n_steps//4, n_steps-1]
    colors = ['blue', 'green', 'orange', 'purple', 'red']
    
    for i, (idx, color) in enumerate(zip(time_indices, colors)):
        psi_density = np.abs(psi_trajectory[idx])**2
        ax1.plot(solver.x_grid, psi_density, color=color, linewidth=2,
                label=f't = {time_array[idx]:.2f}')
    
    ax1.set_xlabel('Position (x)')
    ax1.set_ylabel('Energy / Probability')
    ax1.set_title('Oscillatory Motion')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Position expectation value over time
    ax2 = axes[0, 1]
    positions = [obs['position'] for obs in observables]
    ax2.plot(time_array, positions, 'b-', linewidth=2)
    ax2.set_xlabel('Time (t)')
    ax2.set_ylabel('Position ⟨x⟩')
    ax2.set_title('Classical Oscillation')
    ax2.grid(True, alpha=0.3)
    
    # Plot 3: Energy evolution
    ax3 = axes[1, 0]
    energies = [obs['energy'] for obs in observables]
    ax3.plot(time_array, energies, 'g-', linewidth=2)
    ax3.axhline(y=omega, color='r', linestyle='--', alpha=0.7, label='ℏω')
    ax3.set_xlabel('Time (t)')
    ax3.set_ylabel('Energy ⟨E⟩')
    ax3.set_title('Energy Conservation')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # Plot 4: Phase space trajectory
    ax4 = axes[1, 1]
    momenta = [obs['momentum'] for obs in observables]
    ax4.plot(positions, momenta, 'purple', linewidth=2)
    ax4.set_xlabel('Position ⟨x⟩')
    ax4.set_ylabel('Momentum ⟨p⟩')
    ax4.set_title('Phase Space Trajectory')
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()
    
    # Calculate oscillation period
    # Find peaks in position
    from scipy.signal import find_peaks
    peaks, _ = find_peaks(positions, height=0.5)
    if len(peaks) > 1:
        period = 2 * (time_array[peaks[1]] - time_array[peaks[0]])
        theoretical_period = 2 * np.pi / omega
        print(f"Measured period: {period:.3f}")
        print(f"Theoretical period: {theoretical_period:.3f}")
        print(f"Error: {abs(period - theoretical_period)/theoretical_period*100:.1f}%")


def run_quantum_interference():
    """Demonstrate quantum interference between two wave packets."""
    print("\n🌊 Quantum Interference")
    print("=" * 50)
    
    # Set up parameters
    params = SchrodingerParameters(
        mass=1.0,
        hbar=1.0,
        dt=0.01,
        x_min=-10.0,
        x_max=10.0,
        n_points=1024
    )
    
    # No potential (free space)
    params.potential = lambda x: np.zeros_like(x)
    
    # Initialize solver
    solver = SchrodingerSolver(params)
    
    # Create two wave packets
    psi1 = solver.create_gaussian_packet(x0=-2.0, p0=1.0, sigma=0.8)
    psi2 = solver.create_gaussian_packet(x0=2.0, p0=-1.0, sigma=0.8)
    
    # Combine them (superposition)
    psi_init = psi1.copy()
    psi_init.psi = (psi1.psi + psi2.psi) / np.sqrt(2)  # Normalize
    psi_init.normalize()
    
    # Evolve wave function
    n_steps = 300
    psi_trajectory, time_array = solver.evolve_trajectory(psi_init, n_steps)
    
    # Create visualization
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle("Quantum Interference", fontsize=16)
    
    # Plot 1: Initial superposition
    ax1 = axes[0, 0]
    ax1.plot(solver.x_grid, np.abs(psi1.psi)**2, 'b--', alpha=0.7, label='Packet 1')
    ax1.plot(solver.x_grid, np.abs(psi2.psi)**2, 'r--', alpha=0.7, label='Packet 2')
    ax1.plot(solver.x_grid, np.abs(psi_init.psi)**2, 'k-', linewidth=2, label='Superposition')
    ax1.set_xlabel('Position (x)')
    ax1.set_ylabel('Probability Density')
    ax1.set_title('Initial State')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Interference pattern evolution
    ax2 = axes[0, 1]
    psi_density = np.abs(psi_trajectory)**2
    im = ax2.imshow(psi_density, aspect='auto', origin='lower',
                   extent=[solver.x_grid[0], solver.x_grid[-1], 0, time_array[-1]],
                   cmap='viridis')
    ax2.set_xlabel('Position (x)')
    ax2.set_ylabel('Time (t)')
    ax2.set_title('Interference Pattern')
    plt.colorbar(im, ax=ax2, label='|ψ|²')
    
    # Plot 3: Real and imaginary parts
    ax3 = axes[1, 0]
    psi_final = psi_trajectory[-1]
    ax3.plot(solver.x_grid, psi_final.real, 'b-', linewidth=2, label='Re(ψ)')
    ax3.plot(solver.x_grid, psi_final.imag, 'r-', linewidth=2, label='Im(ψ)')
    ax3.plot(solver.x_grid, np.abs(psi_final)**2, 'k-', linewidth=2, label='|ψ|²')
    ax3.set_xlabel('Position (x)')
    ax3.set_ylabel('Amplitude')
    ax3.set_title('Final Wave Function')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # Plot 4: Probability current
    ax4 = axes[1, 1]
    current_data = []
    for psi in psi_trajectory:
        dx = solver.dx
        dpsi_dx = np.gradient(psi, dx)
        j = (solver.hbar / (2 * solver.mass * 1j)) * (
            np.conj(psi) * dpsi_dx - psi * np.conj(dpsi_dx)
        )
        current_data.append(j.real)
    
    current_data = np.array(current_data)
    im2 = ax4.imshow(current_data, aspect='auto', origin='lower',
                    extent=[solver.x_grid[0], solver.x_grid[-1], 0, time_array[-1]],
                    cmap='RdBu')
    ax4.set_xlabel('Position (x)')
    ax4.set_ylabel('Time (t)')
    ax4.set_title('Probability Current')
    plt.colorbar(im2, ax=ax4, label='Current Density')
    
    plt.tight_layout()
    plt.show()
    
    print("Interference pattern shows constructive and destructive interference!")


def main():
    """Main function."""
    print("🚀 Wave Packet Evolution Examples")
    print("=" * 60)
    
    try:
        # Run wave packet spreading
        run_wave_packet_spreading()
        
        # Run harmonic oscillator
        run_harmonic_oscillator()
        
        # Run quantum interference
        run_quantum_interference()
        
        print("\n✅ All wave packet simulations completed successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
