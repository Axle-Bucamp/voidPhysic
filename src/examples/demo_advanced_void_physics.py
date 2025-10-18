#!/usr/bin/env python3
"""
Demo: Advanced Void Physics Simulation
=====================================

A demonstration of the advanced void physics simulation featuring:
- Void particles that behave like liquid
- Wave function collapse
- Topological connectivity
- LYFE game mechanics
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from advanced_void_physics_simulation import AdvancedVoidPhysicsSimulation
import pandas as pd 

def create_demo_animation():
    """Create a demonstration animation of advanced void physics."""
    print("🌌 Creating Advanced Void Physics Demo...")
    
    # Create simulation
    sim = AdvancedVoidPhysicsSimulation(width=60, height=60)
    sim.initialize_topological_sources(n_sources=4)
    sim.create_initial_atoms(n_atoms=2)
    
    # Create figure
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Initialize plots
    universe_plot = axes[0, 0].imshow(sim.get_universe_image(), origin='lower')
    axes[0, 0].set_title('Advanced Void Physics Universe')
    axes[0, 0].set_xlabel('X')
    axes[0, 0].set_ylabel('Y')
    
    void_plot = axes[0, 1].imshow(sim.get_void_field_image(), origin='lower', cmap='RdBu_r')
    axes[0, 1].set_title('Topological Void Field')
    axes[0, 1].set_xlabel('X')
    axes[0, 1].set_ylabel('Y')
    
    # Add colorbar for void field
    plt.colorbar(void_plot, ax=axes[0, 1])
    
    # Statistics plots
    axes[1, 0].set_title('Particle Statistics')
    axes[1, 0].set_xlabel('Time')
    axes[1, 0].set_ylabel('Count')
    
    axes[1, 1].set_title('Wave Function States')
    axes[1, 1].set_xlabel('Time')
    axes[1, 1].set_ylabel('Count')
    
    def animate(frame):
        """Animation function."""
        # Update simulation
        sim.update(dt=0.1)
        
        # Update plots
        universe_plot.set_array(sim.get_universe_image())
        void_plot.set_array(sim.get_void_field_image())
        
        # Update titles with time
        axes[0, 0].set_title(f'Advanced Void Physics (t={sim.time:.1f})')
        axes[0, 1].set_title(f'Topological Void Field (t={sim.time:.1f})')
        
        # Update statistics
        if sim.history:
            history_df = pd.DataFrame(sim.history)
            axes[1, 0].clear()
            axes[1, 0].plot(history_df['time'], history_df['n_atoms'], 'b-', label='Atoms')
            axes[1, 0].plot(history_df['time'], history_df['n_void_particles'], 'r-', label='Void Particles')
            axes[1, 0].set_title('Particle Statistics')
            axes[1, 0].set_xlabel('Time')
            axes[1, 0].set_ylabel('Count')
            axes[1, 0].legend()
            axes[1, 0].grid(True, alpha=0.3)
            
            # Wave function states
            axes[1, 1].clear()
            matter_counts = [sim.stats['matter_atoms']] * len(history_df)
            antimatter_counts = [sim.stats['antimatter_atoms']] * len(history_df)
            superposition_counts = [sim.stats['superposition_atoms']] * len(history_df)
            
            axes[1, 1].plot(history_df['time'], matter_counts, 'r-', label='Matter')
            axes[1, 1].plot(history_df['time'], antimatter_counts, 'g-', label='Antimatter')
            axes[1, 1].plot(history_df['time'], superposition_counts, 'purple', label='Superposition')
            axes[1, 1].set_title('Wave Function States')
            axes[1, 1].set_xlabel('Time')
            axes[1, 1].set_ylabel('Count')
            axes[1, 1].legend()
            axes[1, 1].grid(True, alpha=0.3)
        
        return [universe_plot, void_plot]
    
    # Create animation
    anim = animation.FuncAnimation(fig, animate, frames=300, 
                                 interval=100, blit=False, repeat=True)
    
    plt.tight_layout()
    plt.show()
    
    return anim

def create_static_demo():
    """Create a static demonstration showing key moments."""
    print("🌌 Creating Static Demo...")
    
    # Create simulation
    sim = AdvancedVoidPhysicsSimulation(width=50, height=50)
    sim.initialize_topological_sources(n_sources=3)
    sim.create_initial_atoms(n_atoms=1)
    
    # Create figure with multiple time points
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    
    time_points = [0, 10, 20, 30, 40, 50]
    
    for i, t in enumerate(time_points):
        row = i // 3
        col = i % 3
        
        # Run simulation to time t
        while sim.time < t:
            sim.update(dt=0.1)
        
        # Plot universe
        universe_image = sim.get_universe_image()
        axes[row, col].imshow(universe_image, origin='lower')
        axes[row, col].set_title(f'Advanced Void Physics at t={t:.1f}')
        axes[row, col].set_xlabel('X')
        axes[row, col].set_ylabel('Y')
        
        # Add statistics
        n_atoms = len(sim.atoms)
        n_void_particles = len(sim.void_particles)
        n_superposition = sim.stats['superposition_atoms']
        axes[row, col].text(0.02, 0.98, 
                           f'Atoms: {n_atoms}\nVoid Particles: {n_void_particles}\nSuperposition: {n_superposition}', 
                           transform=axes[row, col].transAxes, 
                           verticalalignment='top',
                           bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    plt.suptitle('Advanced Void Physics: Evolution Over Time', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig('examples/advanced_void_physics_demo.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print("✅ Static demo saved as 'advanced_void_physics_demo.png'")

def print_simulation_info():
    """Print information about the advanced simulation."""
    print("\n🌌 Advanced Void Physics Simulation Info")
    print("=" * 60)
    print("""
This simulation implements refined void physics principles:

1. **Void Particles**: Smaller than atoms, behave like liquid
   - Much lower attraction strength (0.01 vs 1.0 for atoms)
   - Move toward nearest structures
   - Attach to atoms and make them age
   - Blob together to form new atoms

2. **Wave Function Collapse**: Atoms start in superposition
   - Matter/antimatter probabilities: 50/50
   - Collapse based on void field strength
   - Determines final atom type

3. **Topological Connectivity**: No time/space in void
   - Void field acts everywhere simultaneously
   - No distance dependence
   - Instantaneous effects across space

4. **LYFE Game Mechanics**: 
   - Void particles spawn continuously
   - Attraction to structures
   - Blob formation for atom creation
   - Aging and decay processes

5. **Physics Rules**:
   - Void particles have 100x lower attraction than atoms
   - Explains why we never see creation in normal conditions
   - Void tension drives evolution to T+1
   - No time/space constraints in void

Key Parameters:
- Void Particle Spawn Rate: Controls particle creation
- Blob Threshold: Particles needed to form atoms
- Attraction Strength: 0.01 for void particles, 1.0 for atoms
- Wave Function Collapse: Based on void field strength
    """)

def main():
    """Main demo function."""
    print("🌌 Advanced Void Physics Simulation Demo")
    print("=" * 70)
    
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
