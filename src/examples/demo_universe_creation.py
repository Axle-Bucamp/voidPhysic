#!/usr/bin/env python3
"""
Demo: Universe Creation Simulation
==================================

A simple demonstration of the universe creation simulation
showing how atoms emerge from the void through interference patterns.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from universe_creation_simulation import UniverseCreationSimulation

def create_demo_animation():
    """Create a demonstration animation of universe creation."""
    print("🌌 Creating Universe Creation Demo...")
    
    # Create simulation
    sim = UniverseCreationSimulation(width=60, height=60)
    sim.initialize_void_sources()
    sim.create_initial_atoms(n_atoms=3)
    
    # Create figure
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    # Initialize plots
    universe_plot = axes[0].imshow(sim.get_universe_image(), origin='lower')
    axes[0].set_title('Universe Creation')
    axes[0].set_xlabel('X')
    axes[0].set_ylabel('Y')
    
    void_plot = axes[1].imshow(sim.get_void_field_image(), origin='lower', cmap='RdBu_r')
    axes[1].set_title('Void Interference Field')
    axes[1].set_xlabel('X')
    axes[1].set_ylabel('Y')
    
    # Add colorbar for void field
    plt.colorbar(void_plot, ax=axes[1])
    
    def animate(frame):
        """Animation function."""
        # Update simulation
        sim.update(dt=0.1)
        
        # Update plots
        universe_plot.set_array(sim.get_universe_image())
        void_plot.set_array(sim.get_void_field_image())
        
        # Update titles with time
        axes[0].set_title(f'Universe Creation (t={sim.time:.1f})')
        axes[1].set_title(f'Void Field (t={sim.time:.1f})')
        
        return [universe_plot, void_plot]
    
    # Create animation
    anim = animation.FuncAnimation(fig, animate, frames=200, 
                                 interval=100, blit=False, repeat=True)
    
    plt.tight_layout()
    plt.show()
    
    return anim

def create_static_demo():
    """Create a static demonstration showing key moments."""
    print("🌌 Creating Static Demo...")
    
    # Create simulation
    sim = UniverseCreationSimulation(width=50, height=50)
    sim.initialize_void_sources()
    sim.create_initial_atoms(n_atoms=2)
    
    # Create figure with multiple time points
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    
    time_points = [0, 5, 10, 15, 20, 25]
    
    for i, t in enumerate(time_points):
        row = i // 3
        col = i % 3
        
        # Run simulation to time t
        while sim.time < t:
            sim.update(dt=0.1)
        
        # Plot universe
        universe_image = sim.get_universe_image()
        axes[row, col].imshow(universe_image, origin='lower')
        axes[row, col].set_title(f'Universe at t={t:.1f}')
        axes[row, col].set_xlabel('X')
        axes[row, col].set_ylabel('Y')
        
        # Add statistics
        n_atoms = len(sim.atoms)
        total_energy = sum(atom.energy for atom in sim.atoms)
        axes[row, col].text(0.02, 0.98, f'Atoms: {n_atoms}\nEnergy: {total_energy:.2f}', 
                           transform=axes[row, col].transAxes, 
                           verticalalignment='top',
                           bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    plt.suptitle('Universe Creation: Evolution Over Time', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig('examples/universe_creation_demo.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print("✅ Static demo saved as 'universe_creation_demo.png'")

def print_simulation_info():
    """Print information about the simulation."""
    print("\n🌌 Universe Creation Simulation Info")
    print("=" * 50)
    print("""
This simulation demonstrates void physics principles:

1. **The Void (Néant)**: A state of perfect symmetry where all possibilities exist
2. **Void Interference**: Patterns that test atoms and cause expansion or aging
3. **Atom Emergence**: Atoms appear where void interference is strong
4. **Expansion**: Atoms expand to neighboring locations when conditions allow
5. **Aging**: Atoms decay when void interference is weak
6. **Topological Connectivity**: Atoms can connect without distance constraints

Key Parameters:
- Void Interference Strength: Controls how strongly the void affects atoms
- Atom Creation Rate: How often new atoms are created
- Expansion Probability: Chance of atom expansion
- Decay Rate: How quickly atoms age and decay

The simulation shows how structure emerges from the void through
stochastic dynamics, creating the foundation for spacetime.
    """)

def main():
    """Main demo function."""
    print("🌌 Universe Creation Simulation Demo")
    print("=" * 60)
    
    # Print information
    print_simulation_info()
    
    # Ask user what they want to see
    print("\nWhat would you like to see?")
    print("1. Animated demo (interactive)")
    print("2. Static demo (multiple time points)")
    print("3. Both")
    
    try:
        choice = input("\nEnter your choice (1, 2, or 3): ").strip()
        
        if choice == '1':
            create_demo_animation()
        elif choice == '2':
            create_static_demo()
        elif choice == '3':
            create_static_demo()
            print("\nNow showing animated demo...")
            create_demo_animation()
        else:
            print("Invalid choice. Showing static demo...")
            create_static_demo()
            
    except KeyboardInterrupt:
        print("\nDemo interrupted by user.")
    except Exception as e:
        print(f"Error during demo: {e}")
        print("Showing static demo instead...")
        create_static_demo()

if __name__ == "__main__":
    main()
