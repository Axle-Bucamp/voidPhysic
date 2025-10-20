#!/usr/bin/env python3
"""
Schrödinger Tunneling Example

Demonstrates quantum tunneling through potential barriers using the
Schrödinger equation solver. Shows how particles can pass through
classically forbidden regions.
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


def create_barrier_potential(barrier_height: float = 2.0, barrier_width: float = 1.0):
    """Create a rectangular potential barrier."""
    def potential(x):
        return barrier_height * (np.abs(x) < barrier_width).astype(float)
    return potential


def create_double_barrier_potential(barrier_height: float = 2.0, 
                                  barrier_width: float = 0.5,
                                  barrier_separation: float = 2.0):
    """Create a double potential barrier (resonant tunneling)."""
    def potential(x):
        barrier1 = barrier_height * (np.abs(x + barrier_separation/2) < barrier_width/2).astype(float)
        barrier2 = barrier_height * (np.abs(x - barrier_separation/2) < barrier_width/2).astype(float)
        return barrier1 + barrier2
    return potential


def run_tunneling_simulation():
    """Run quantum tunneling simulation."""
    print("🔬 Quantum Tunneling Simulation")
    print("=" * 50)
    
    # Set up parameters
    params = SchrodingerParameters(
        mass=1.0,
        hbar=1.0,
        dt=0.01,
        x_min=-10.0,
        x_max=10.0,
        n_points=512
    )
    
    # Create potential (single barrier)
    potential_func = create_barrier_potential(barrier_height=3.0, barrier_width=1.0)
    params.potential = potential_func
    
    # Initialize solver
    solver = SchrodingerSolver(params)
    
    # Create initial wave packet (moving toward barrier)
    psi_init = solver.create_gaussian_packet(x0=-3.0, p0=2.0, sigma=0.8)
    
    print(f"Initial wave packet:")
    print(f"  Position: {solver.x_grid[np.argmax(np.abs(psi_init.psi)**2)]:.2f}")
    print(f"  Momentum: {psi_init.expectation_value(lambda psi, x: -1j * solver.hbar * np.gradient(psi, solver.dx)).real:.2f}")
    
    # Evolve wave function
    n_steps = 500
    psi_trajectory, time_array = solver.evolve_trajectory(psi_init, n_steps)
    
    # Calculate tunneling probability
    barrier_region = (-1.0, 1.0)  # Barrier location
    tunneling_prob = solver.tunneling_probability(psi_init, barrier_region)
    print(f"Tunneling probability: {tunneling_prob:.4f}")
    
    # Calculate observables over time
    observables = []
    for i, psi in enumerate(psi_trajectory):
        psi_temp = psi_init.copy()
        psi_temp.psi = psi
        obs = solver.calculate_observables(psi_temp)
        observables.append(obs)
    
    # Create visualization
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle("Quantum Tunneling Through Potential Barrier", fontsize=16)
    
    # Plot 1: Potential and initial wave function
    ax1 = axes[0, 0]
    V_values = potential_func(solver.x_grid)
    ax1.plot(solver.x_grid, V_values, 'r-', linewidth=2, label='Potential V(x)')
    ax1.plot(solver.x_grid, np.abs(psi_init.psi)**2, 'b-', linewidth=2, label='|ψ|² (initial)')
    ax1.set_xlabel('Position (x)')
    ax1.set_ylabel('Energy / Probability')
    ax1.set_title('Initial State')
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
    ax2.set_title('Wave Function Evolution |ψ(x,t)|²')
    plt.colorbar(im, ax=ax2, label='Probability Density')
    
    # Plot 3: Probability current
    ax3 = axes[1, 0]
    current_data = []
    for psi in psi_trajectory:
        dx = solver.dx
        dpsi_dx = np.gradient(psi, dx)
        j = (solver.hbar / (2 * solver.mass * 1j)) * (
            np.conj(psi) * dpsi_dx - psi * np.conj(dpsi_dx)
        )
        current_data.append(j.real)
    
    current_data = np.array(current_data)
    im2 = ax3.imshow(current_data, aspect='auto', origin='lower',
                    extent=[solver.x_grid[0], solver.x_grid[-1], 0, time_array[-1]],
                    cmap='RdBu')
    ax3.set_xlabel('Position (x)')
    ax3.set_ylabel('Time (t)')
    ax3.set_title('Probability Current j(x,t)')
    plt.colorbar(im2, ax=ax3, label='Current Density')
    
    # Plot 4: Observables over time
    ax4 = axes[1, 1]
    time_points = time_array[::10]  # Sample every 10th point
    position_vals = [obs['position'] for obs in observables[::10]]
    momentum_vals = [obs['momentum'] for obs in observables[::10]]
    energy_vals = [obs['energy'] for obs in observables[::10]]
    
    ax4.plot(time_points, position_vals, 'b-', label='Position ⟨x⟩')
    ax4.plot(time_points, momentum_vals, 'r-', label='Momentum ⟨p⟩')
    ax4.plot(time_points, energy_vals, 'g-', label='Energy ⟨E⟩')
    ax4.set_xlabel('Time (t)')
    ax4.set_ylabel('Expectation Value')
    ax4.set_title('Quantum Observables')
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()
    
    # Print final results
    final_obs = observables[-1]
    print(f"\nFinal observables:")
    print(f"  Position: {final_obs['position']:.2f}")
    print(f"  Momentum: {final_obs['momentum']:.2f}")
    print(f"  Energy: {final_obs['energy']:.2f}")
    print(f"  Position uncertainty: {final_obs['position_uncertainty']:.2f}")


def run_resonant_tunneling():
    """Run resonant tunneling simulation (double barrier)."""
    print("\n🎯 Resonant Tunneling (Double Barrier)")
    print("=" * 50)
    
    # Set up parameters
    params = SchrodingerParameters(
        mass=1.0,
        hbar=1.0,
        dt=0.01,
        x_min=-10.0,
        x_max=10.0,
        n_points=512
    )
    
    # Create double barrier potential
    potential_func = create_double_barrier_potential(
        barrier_height=3.0, 
        barrier_width=0.5,
        barrier_separation=2.0
    )
    params.potential = potential_func
    
    # Initialize solver
    solver = SchrodingerSolver(params)
    
    # Create initial wave packet
    psi_init = solver.create_gaussian_packet(x0=-4.0, p0=1.5, sigma=0.8)
    
    # Evolve wave function
    n_steps = 800
    psi_trajectory, time_array = solver.evolve_trajectory(psi_init, n_steps)
    
    # Create visualization
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle("Resonant Tunneling Through Double Barrier", fontsize=16)
    
    # Plot 1: Potential and wave function at different times
    ax1 = axes[0]
    V_values = potential_func(solver.x_grid)
    ax1.plot(solver.x_grid, V_values, 'r-', linewidth=2, label='Double Barrier')
    
    # Show wave function at different times
    time_indices = [0, n_steps//4, n_steps//2, 3*n_steps//4, n_steps-1]
    colors = ['blue', 'green', 'orange', 'purple', 'red']
    
    for i, (idx, color) in enumerate(zip(time_indices, colors)):
        psi_density = np.abs(psi_trajectory[idx])**2
        ax1.plot(solver.x_grid, psi_density, color=color, linewidth=2, 
                label=f't = {time_array[idx]:.2f}')
    
    ax1.set_xlabel('Position (x)')
    ax1.set_ylabel('Probability Density')
    ax1.set_title('Wave Function Evolution')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Transmission coefficient vs energy
    ax2 = axes[1]
    
    # Calculate transmission for different energies
    energies = np.linspace(0.5, 4.0, 50)
    transmission_coeffs = []
    
    for E in energies:
        # Create wave packet with energy E
        p0 = np.sqrt(2 * solver.mass * E)
        psi_test = solver.create_gaussian_packet(x0=-4.0, p0=p0, sigma=0.8)
        
        # Calculate transmission probability
        trans_prob = solver.tunneling_probability(psi_test, (-3.0, 3.0))
        transmission_coeffs.append(trans_prob)
    
    ax2.plot(energies, transmission_coeffs, 'b-', linewidth=2)
    ax2.axhline(y=1.0, color='r', linestyle='--', alpha=0.7, label='Perfect Transmission')
    ax2.set_xlabel('Energy (E)')
    ax2.set_ylabel('Transmission Coefficient')
    ax2.set_title('Transmission vs Energy')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()
    
    print(f"Resonant tunneling simulation completed!")
    print(f"Peak transmission at energy: {energies[np.argmax(transmission_coeffs)]:.2f}")


def main():
    """Main function."""
    print("🚀 Quantum Tunneling Examples")
    print("=" * 60)
    
    try:
        # Run single barrier tunneling
        run_tunneling_simulation()
        
        # Run resonant tunneling
        run_resonant_tunneling()
        
        print("\n✅ All simulations completed successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
