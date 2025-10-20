#!/usr/bin/env python3
"""
Quantum Void Emergence Example

Demonstrates how particles emerge from quantum vacuum fluctuations
in the void physics framework, connecting quantum field theory
to void particle creation.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from void_physic.quantum.field_theory import QuantumField, FieldParameters, ParticleCreation
from void_physic.quantum.schrodinger import SchrodingerSolver, SchrodingerParameters
from void_physic.core.stochastic import WhiteNoise


def run_quantum_field_emergence():
    """Demonstrate particle emergence from quantum field."""
    print("🌌 Quantum Field Particle Emergence")
    print("=" * 50)
    
    # Set up field parameters
    field_params = FieldParameters(
        mass=1.0,
        hbar=1.0,
        c=1.0,
        coupling=0.5,
        x_min=-10.0,
        x_max=10.0,
        n_points=512,
        dt=0.01
    )
    
    # Initialize quantum field
    quantum_field = QuantumField(field_params)
    
    # Initialize particle creation system
    particle_creation = ParticleCreation(quantum_field)
    
    print("Starting from vacuum state...")
    print("Adding quantum vacuum fluctuations...")
    
    # Simulate emergence over time
    n_steps = 200
    emergence_rate = 0.05  # 5% chance per step
    
    results = particle_creation.simulate_void_emergence(n_steps, emergence_rate)
    
    # Create visualization
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle("Quantum Void Emergence", fontsize=16)
    
    # Plot 1: Field evolution
    ax1 = axes[0, 0]
    field_evolution = np.array(results['field_evolution'])
    field_amplitude = np.abs(field_evolution)
    
    im = ax1.imshow(field_amplitude, aspect='auto', origin='lower',
                   extent=[field_params.x_min, field_params.x_max, 0, results['time'][-1]],
                   cmap='viridis')
    ax1.set_xlabel('Position (x)')
    ax1.set_ylabel('Time (t)')
    ax1.set_title('Field Amplitude Evolution')
    plt.colorbar(im, ax=ax1, label='|φ|')
    
    # Plot 2: Particle count over time
    ax2 = axes[0, 1]
    ax2.plot(results['time'], results['particle_count'], 'b-', linewidth=2)
    ax2.set_xlabel('Time (t)')
    ax2.set_ylabel('Number of Particles')
    ax2.set_title('Particle Emergence')
    ax2.grid(True, alpha=0.3)
    
    # Plot 3: Total energy evolution
    ax3 = axes[1, 0]
    ax3.plot(results['time'], results['total_energy'], 'r-', linewidth=2)
    ax3.set_xlabel('Time (t)')
    ax3.set_ylabel('Total Energy')
    ax3.set_title('Energy Creation')
    ax3.grid(True, alpha=0.3)
    
    # Plot 4: Final field state
    ax4 = axes[1, 1]
    final_field = results['field_evolution'][-1]
    ax4.plot(quantum_field.field_operator.x_grid, np.abs(final_field), 'g-', linewidth=2, label='|φ|')
    ax4.plot(quantum_field.field_operator.x_grid, final_field.real, 'b--', alpha=0.7, label='Re(φ)')
    ax4.plot(quantum_field.field_operator.x_grid, final_field.imag, 'r--', alpha=0.7, label='Im(φ)')
    ax4.set_xlabel('Position (x)')
    ax4.set_ylabel('Field Amplitude')
    ax4.set_title('Final Field State')
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()
    
    print(f"Final particle count: {results['particle_count'][-1]}")
    print(f"Final total energy: {results['total_energy'][-1]:.3f}")
    print(f"Number of creation events: {len(particle_creation.creation_events)}")


def run_quantum_vacuum_fluctuations():
    """Demonstrate quantum vacuum fluctuations driving emergence."""
    print("\n⚡ Quantum Vacuum Fluctuations")
    print("=" * 50)
    
    # Set up parameters
    params = SchrodingerParameters(
        mass=1.0,
        hbar=1.0,
        dt=0.01,
        x_min=-8.0,
        x_max=8.0,
        n_points=256
    )
    
    # No potential (free space)
    params.potential = lambda x: np.zeros_like(x)
    
    # Initialize solver
    solver = SchrodingerSolver(params)
    
    # Initialize quantum noise
    quantum_noise = WhiteNoise(strength=1.0, quantum_mode=True, hbar=1.0)
    
    # Start with vacuum state (zero field)
    psi_vacuum = solver.create_gaussian_packet(x0=0.0, p0=0.0, sigma=0.1)
    psi_vacuum.psi *= 0.01  # Very small amplitude (near vacuum)
    
    # Simulate vacuum fluctuations
    n_steps = 100
    psi_trajectory = []
    fluctuation_trajectory = []
    
    psi_current = psi_vacuum.copy()
    
    for step in range(n_steps):
        # Generate quantum vacuum fluctuation
        vacuum_fluctuation = quantum_noise.quantum_vacuum_fluctuation(
            psi_current.psi, solver.x_grid, solver.mass
        )
        
        # Add fluctuation to wave function
        psi_current.psi += vacuum_fluctuation * 0.1
        
        # Normalize
        psi_current.normalize()
        
        # Store trajectory
        psi_trajectory.append(psi_current.psi.copy())
        fluctuation_trajectory.append(vacuum_fluctuation.copy())
        
        # Evolve one step
        psi_current = solver.evolve_step(psi_current)
    
    # Create visualization
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle("Quantum Vacuum Fluctuations", fontsize=16)
    
    # Plot 1: Wave function evolution
    ax1 = axes[0, 0]
    psi_density = np.abs(np.array(psi_trajectory))**2
    im = ax1.imshow(psi_density, aspect='auto', origin='lower',
                   extent=[solver.x_grid[0], solver.x_grid[-1], 0, n_steps],
                   cmap='viridis')
    ax1.set_xlabel('Position (x)')
    ax1.set_ylabel('Time Step')
    ax1.set_title('Wave Function Evolution')
    plt.colorbar(im, ax=ax1, label='|ψ|²')
    
    # Plot 2: Vacuum fluctuations
    ax2 = axes[0, 1]
    fluctuation_data = np.array(fluctuation_trajectory)
    im2 = ax2.imshow(fluctuation_data, aspect='auto', origin='lower',
                    extent=[solver.x_grid[0], solver.x_grid[-1], 0, n_steps],
                    cmap='RdBu')
    ax2.set_xlabel('Position (x)')
    ax2.set_ylabel('Time Step')
    ax2.set_title('Vacuum Fluctuations')
    plt.colorbar(im2, ax=ax2, label='Fluctuation')
    
    # Plot 3: Field variance over time
    ax3 = axes[1, 0]
    field_variance = [np.var(np.abs(psi)) for psi in psi_trajectory]
    ax3.plot(range(n_steps), field_variance, 'g-', linewidth=2)
    ax3.set_xlabel('Time Step')
    ax3.set_ylabel('Field Variance')
    ax3.set_title('Fluctuation Growth')
    ax3.grid(True, alpha=0.3)
    
    # Plot 4: Final state
    ax4 = axes[1, 1]
    final_psi = psi_trajectory[-1]
    ax4.plot(solver.x_grid, np.abs(final_psi)**2, 'b-', linewidth=2, label='|ψ|²')
    ax4.plot(solver.x_grid, final_psi.real, 'r--', alpha=0.7, label='Re(ψ)')
    ax4.plot(solver.x_grid, final_psi.imag, 'g--', alpha=0.7, label='Im(ψ)')
    ax4.set_xlabel('Position (x)')
    ax4.set_ylabel('Amplitude')
    ax4.set_title('Final State')
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()
    
    print(f"Initial field variance: {np.var(np.abs(psi_vacuum.psi)):.6f}")
    print(f"Final field variance: {np.var(np.abs(psi_trajectory[-1])):.6f}")
    print(f"Variance growth factor: {np.var(np.abs(psi_trajectory[-1]))/np.var(np.abs(psi_vacuum.psi)):.2f}")


def run_void_particle_creation():
    """Demonstrate void particle creation with quantum mechanics."""
    print("\n🎯 Void Particle Creation")
    print("=" * 50)
    
    # Set up field parameters
    field_params = FieldParameters(
        mass=1.0,
        hbar=1.0,
        c=1.0,
        coupling=0.3,
        x_min=-6.0,
        x_max=6.0,
        n_points=256,
        dt=0.02
    )
    
    # Initialize quantum field
    quantum_field = QuantumField(field_params)
    
    # Start from vacuum
    quantum_field.set_field(quantum_field.field_operator.vacuum_state())
    
    # Simulate particle creation events
    n_steps = 150
    particle_positions_history = []
    field_evolution = []
    
    for step in range(n_steps):
        # Random particle creation from void
        if np.random.random() < 0.08:  # 8% chance per step
            # Random momentum for emerging particle
            k_random = np.random.uniform(-2.0, 2.0)
            amplitude = np.random.uniform(0.5, 1.5)
            
            # Create particle
            new_particle = quantum_field.field_operator.create_particle(k_random, amplitude)
            quantum_field.field += new_particle
        
        # Evolve field
        quantum_field.evolve_step()
        
        # Get particle positions
        particle_positions = quantum_field.get_particle_positions(threshold=0.1)
        particle_positions_history.append(particle_positions.copy())
        field_evolution.append(quantum_field.field.copy())
    
    # Create visualization
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle("Void Particle Creation", fontsize=16)
    
    # Plot 1: Field evolution
    ax1 = axes[0, 0]
    field_amplitude = np.abs(np.array(field_evolution))
    im = ax1.imshow(field_amplitude, aspect='auto', origin='lower',
                   extent=[field_params.x_min, field_params.x_max, 0, n_steps],
                   cmap='viridis')
    ax1.set_xlabel('Position (x)')
    ax1.set_ylabel('Time Step')
    ax1.set_title('Field Evolution')
    plt.colorbar(im, ax=ax1, label='|φ|')
    
    # Plot 2: Particle positions over time
    ax2 = axes[0, 1]
    for step, positions in enumerate(particle_positions_history):
        if positions:
            ax2.scatter(positions, [step] * len(positions), c='red', s=20, alpha=0.7)
    ax2.set_xlabel('Position (x)')
    ax2.set_ylabel('Time Step')
    ax2.set_title('Particle Creation Events')
    ax2.grid(True, alpha=0.3)
    
    # Plot 3: Particle count over time
    ax3 = axes[1, 0]
    particle_counts = [len(positions) for positions in particle_positions_history]
    ax3.plot(range(n_steps), particle_counts, 'b-', linewidth=2)
    ax3.set_xlabel('Time Step')
    ax3.set_ylabel('Number of Particles')
    ax3.set_title('Particle Count Evolution')
    ax3.grid(True, alpha=0.3)
    
    # Plot 4: Final field state
    ax4 = axes[1, 1]
    final_field = field_evolution[-1]
    ax4.plot(quantum_field.field_operator.x_grid, np.abs(final_field), 'g-', linewidth=2, label='|φ|')
    ax4.plot(quantum_field.field_operator.x_grid, final_field.real, 'b--', alpha=0.7, label='Re(φ)')
    ax4.plot(quantum_field.field_operator.x_grid, final_field.imag, 'r--', alpha=0.7, label='Im(φ)')
    
    # Mark particle positions
    final_positions = particle_positions_history[-1]
    if final_positions:
        ax4.scatter(final_positions, [np.abs(final_field)[np.argmin(np.abs(quantum_field.field_operator.x_grid - pos))] for pos in final_positions], 
                   c='red', s=50, label='Particles', zorder=5)
    
    ax4.set_xlabel('Position (x)')
    ax4.set_ylabel('Field Amplitude')
    ax4.set_title('Final State with Particles')
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()
    
    total_particles_created = sum(len(positions) for positions in particle_positions_history)
    final_particle_count = len(particle_positions_history[-1])
    
    print(f"Total particles created: {total_particles_created}")
    print(f"Final particle count: {final_particle_count}")
    print(f"Particle creation rate: {total_particles_created/n_steps:.3f} particles/step")


def main():
    """Main function."""
    print("🚀 Quantum Void Emergence Examples")
    print("=" * 60)
    
    try:
        # Run quantum field emergence
        run_quantum_field_emergence()
        
        # Run quantum vacuum fluctuations
        run_quantum_vacuum_fluctuations()
        
        # Run void particle creation
        run_void_particle_creation()
        
        print("\n✅ All quantum void emergence simulations completed successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
