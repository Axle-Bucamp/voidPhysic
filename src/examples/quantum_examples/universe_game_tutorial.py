#!/usr/bin/env python3
"""
Universe Game Tutorial

Interactive tutorial for the quantum void physics universe creation game.
Demonstrates how to create stable universes by tuning quantum parameters
and shows the scoring system.
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
from void_physic.core.potential import DoubleWellPotential, PotentialParameters


class UniverseGame:
    """
    Quantum Universe Creation Game
    
    Players tune quantum parameters to create stable universes with
    high complexity and entropy.
    """
    
    def __init__(self):
        self.level = 1
        self.score = 0
        self.particles_created = 0
        self.stability_time = 0
        self.entropy = 0
        self.is_running = False
        
        # Game parameters
        self.emergence_rate = 0.1
        self.quantum_coupling = 1.0
        self.void_strength = 1.0
        
        # Level requirements
        self.level_requirements = {
            1: {'min_particles': 5, 'min_stability': 50, 'min_entropy': 0.5},
            2: {'min_particles': 10, 'min_stability': 100, 'min_entropy': 1.0},
            3: {'min_particles': 20, 'min_stability': 200, 'min_entropy': 1.5},
            4: {'min_particles': 30, 'min_stability': 300, 'min_entropy': 2.0},
            5: {'min_particles': 50, 'min_stability': 500, 'min_entropy': 2.5}
        }
    
    def calculate_score(self, particles, stability_time, entropy, total_energy):
        """
        Calculate game score based on universe properties.
        
        Score = α·N_particles + β·t_stable + γ·S_entropy - δ·E_total
        """
        alpha = 10.0  # Particle bonus
        beta = 0.1    # Stability bonus
        gamma = 5.0   # Entropy bonus
        delta = 0.01  # Energy penalty
        
        score = (alpha * particles + 
                beta * stability_time + 
                gamma * entropy - 
                delta * total_energy)
        
        return max(0, score)  # Ensure non-negative score
    
    def run_simulation(self, n_steps=200):
        """Run universe simulation with current parameters."""
        print(f"🎮 Starting Universe Creation (Level {self.level})")
        print("=" * 50)
        
        # Set up field parameters
        field_params = FieldParameters(
            mass=1.0,
            hbar=1.0,
            c=1.0,
            coupling=self.quantum_coupling,
            x_min=-8.0,
            x_max=8.0,
            n_points=256,
            dt=0.02
        )
        
        # Initialize quantum field
        quantum_field = QuantumField(field_params)
        quantum_field.set_field(quantum_field.field_operator.vacuum_state())
        
        # Initialize particle creation
        particle_creation = ParticleCreation(quantum_field)
        
        # Simulation data
        particle_counts = []
        energy_values = []
        entropy_values = []
        field_evolution = []
        creation_events = []
        
        print(f"Parameters:")
        print(f"  Emergence rate: {self.emergence_rate:.3f}")
        print(f"  Quantum coupling: {self.quantum_coupling:.3f}")
        print(f"  Void strength: {self.void_strength:.3f}")
        print()
        
        # Run simulation
        for step in range(n_steps):
            # Particle emergence from void
            if np.random.random() < self.emergence_rate:
                k_random = np.random.uniform(-2.0, 2.0)
                amplitude = self.void_strength * np.random.uniform(0.5, 1.5)
                
                particle_creation.particle_creation_event(k_random, amplitude)
                creation_events.append(step)
            
            # Evolve field
            quantum_field.evolve_step()
            
            # Calculate observables
            observables = quantum_field.calculate_observables()
            particle_positions = quantum_field.get_particle_positions(threshold=0.1)
            
            # Store data
            particle_counts.append(len(particle_positions))
            energy_values.append(observables['total_energy'])
            entropy_values.append(observables['field_variance'])  # Simplified entropy
            field_evolution.append(quantum_field.field.copy())
            
            # Check for stability
            if step > 50:  # Allow initial settling
                recent_particles = particle_counts[-20:]
                if len(set(recent_particles)) <= 2:  # Stable particle count
                    self.stability_time += 1
                else:
                    self.stability_time = max(0, self.stability_time - 1)
        
        # Calculate final metrics
        self.particles_created = particle_counts[-1]
        self.entropy = entropy_values[-1]
        total_energy = energy_values[-1]
        
        # Calculate score
        self.score = self.calculate_score(
            self.particles_created, 
            self.stability_time, 
            self.entropy, 
            total_energy
        )
        
        # Store results
        self.simulation_results = {
            'particle_counts': particle_counts,
            'energy_values': energy_values,
            'entropy_values': entropy_values,
            'field_evolution': field_evolution,
            'creation_events': creation_events,
            'time_steps': list(range(n_steps))
        }
        
        return self.simulation_results
    
    def visualize_results(self):
        """Visualize simulation results."""
        if not hasattr(self, 'simulation_results'):
            print("No simulation results to visualize!")
            return
        
        results = self.simulation_results
        
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        fig.suptitle(f"Universe Creation Results - Level {self.level} (Score: {self.score:.1f})", 
                    fontsize=16)
        
        # Plot 1: Particle count evolution
        ax1 = axes[0, 0]
        ax1.plot(results['time_steps'], results['particle_counts'], 'b-', linewidth=2)
        ax1.axhline(y=self.level_requirements[self.level]['min_particles'], 
                   color='r', linestyle='--', alpha=0.7, label='Level Requirement')
        ax1.set_xlabel('Time Step')
        ax1.set_ylabel('Number of Particles')
        ax1.set_title('Particle Creation')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Energy evolution
        ax2 = axes[0, 1]
        ax2.plot(results['time_steps'], results['energy_values'], 'g-', linewidth=2)
        ax2.set_xlabel('Time Step')
        ax2.set_ylabel('Total Energy')
        ax2.set_title('Energy Evolution')
        ax2.grid(True, alpha=0.3)
        
        # Plot 3: Entropy evolution
        ax3 = axes[1, 0]
        ax3.plot(results['time_steps'], results['entropy_values'], 'purple', linewidth=2)
        ax3.axhline(y=self.level_requirements[self.level]['min_entropy'], 
                   color='r', linestyle='--', alpha=0.7, label='Level Requirement')
        ax3.set_xlabel('Time Step')
        ax3.set_ylabel('Entropy (Field Variance)')
        ax3.set_title('Entropy Evolution')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        # Plot 4: Field evolution
        ax4 = axes[1, 1]
        field_amplitude = np.abs(np.array(results['field_evolution']))
        im = ax4.imshow(field_amplitude, aspect='auto', origin='lower',
                       extent=[-8, 8, 0, len(results['time_steps'])],
                       cmap='viridis')
        ax4.set_xlabel('Position (x)')
        ax4.set_ylabel('Time Step')
        ax4.set_title('Field Evolution')
        plt.colorbar(im, ax=ax4, label='|φ|')
        
        plt.tight_layout()
        plt.show()
    
    def check_level_completion(self):
        """Check if current level is completed."""
        requirements = self.level_requirements[self.level]
        
        completed = (
            self.particles_created >= requirements['min_particles'] and
            self.stability_time >= requirements['min_stability'] and
            self.entropy >= requirements['min_entropy']
        )
        
        return completed, requirements
    
    def advance_level(self):
        """Advance to next level if requirements are met."""
        completed, requirements = self.check_level_completion()
        
        if completed:
            self.level += 1
            print(f"🎉 Level {self.level-1} completed!")
            print(f"🚀 Advancing to Level {self.level}")
            return True
        else:
            print(f"❌ Level {self.level} not completed yet.")
            print(f"Requirements:")
            print(f"  Particles: {self.particles_created}/{requirements['min_particles']}")
            print(f"  Stability: {self.stability_time}/{requirements['min_stability']}")
            print(f"  Entropy: {self.entropy:.2f}/{requirements['min_entropy']}")
            return False


def run_tutorial():
    """Run the universe game tutorial."""
    print("🎮 Quantum Void Physics Universe Game Tutorial")
    print("=" * 60)
    print()
    print("Welcome to the Universe Creation Game!")
    print("Your goal is to create stable universes by tuning quantum parameters.")
    print("Higher levels require more particles, stability, and entropy.")
    print()
    
    # Create game instance
    game = UniverseGame()
    
    # Tutorial level 1
    print("📚 TUTORIAL LEVEL 1: Basic Universe Creation")
    print("-" * 50)
    print("Goal: Create a universe with at least 5 particles")
    print("Parameters: Use default settings")
    print()
    
    # Run simulation
    game.run_simulation(n_steps=150)
    game.visualize_results()
    
    # Check completion
    completed, requirements = game.check_level_completion()
    if completed:
        print("✅ Tutorial Level 1 completed!")
        game.advance_level()
    else:
        print("❌ Try adjusting parameters and run again!")
    
    print()
    print("🎯 TUTORIAL LEVEL 2: Parameter Tuning")
    print("-" * 50)
    print("Goal: Create a more complex universe")
    print("Try increasing emergence rate and quantum coupling")
    print()
    
    # Adjust parameters for level 2
    game.emergence_rate = 0.15
    game.quantum_coupling = 1.5
    game.void_strength = 1.2
    
    # Run simulation
    game.run_simulation(n_steps=200)
    game.visualize_results()
    
    # Check completion
    completed, requirements = game.check_level_completion()
    if completed:
        print("✅ Tutorial Level 2 completed!")
        game.advance_level()
    else:
        print("❌ Try different parameter combinations!")
    
    print()
    print("🏆 FINAL CHALLENGE: High-Entropy Universe")
    print("-" * 50)
    print("Goal: Create a universe with maximum complexity")
    print("Experiment with extreme parameter values")
    print()
    
    # Extreme parameters for challenge
    game.emergence_rate = 0.25
    game.quantum_coupling = 2.0
    game.void_strength = 1.8
    
    # Run simulation
    game.run_simulation(n_steps=300)
    game.visualize_results()
    
    # Final results
    print("🏁 TUTORIAL COMPLETED!")
    print("=" * 50)
    print(f"Final Score: {game.score:.1f}")
    print(f"Particles Created: {game.particles_created}")
    print(f"Stability Time: {game.stability_time}")
    print(f"Entropy: {game.entropy:.3f}")
    print()
    print("💡 Tips for better scores:")
    print("  - Higher emergence rate = more particles")
    print("  - Higher quantum coupling = more complex interactions")
    print("  - Higher void strength = stronger field excitations")
    print("  - Balance parameters to maintain stability")
    print()
    print("🎮 Ready to play the full game?")
    print("Run the quantum dashboard and try the Game mode!")


def demonstrate_scoring_system():
    """Demonstrate the scoring system with different parameter sets."""
    print("\n📊 Scoring System Demonstration")
    print("=" * 50)
    
    # Test different parameter combinations
    test_configs = [
        {'name': 'Conservative', 'emergence_rate': 0.05, 'quantum_coupling': 0.8, 'void_strength': 0.8},
        {'name': 'Balanced', 'emergence_rate': 0.1, 'quantum_coupling': 1.0, 'void_strength': 1.0},
        {'name': 'Aggressive', 'emergence_rate': 0.2, 'quantum_coupling': 1.5, 'void_strength': 1.5},
        {'name': 'Extreme', 'emergence_rate': 0.3, 'quantum_coupling': 2.0, 'void_strength': 2.0}
    ]
    
    results = []
    
    for config in test_configs:
        print(f"\nTesting {config['name']} configuration...")
        
        game = UniverseGame()
        game.emergence_rate = config['emergence_rate']
        game.quantum_coupling = config['quantum_coupling']
        game.void_strength = config['void_strength']
        
        # Run simulation
        game.run_simulation(n_steps=150)
        
        results.append({
            'name': config['name'],
            'score': game.score,
            'particles': game.particles_created,
            'stability': game.stability_time,
            'entropy': game.entropy
        })
        
        print(f"  Score: {game.score:.1f}")
        print(f"  Particles: {game.particles_created}")
        print(f"  Stability: {game.stability_time}")
        print(f"  Entropy: {game.entropy:.3f}")
    
    # Create comparison plot
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle("Scoring System Comparison", fontsize=16)
    
    names = [r['name'] for r in results]
    scores = [r['score'] for r in results]
    particles = [r['particles'] for r in results]
    stability = [r['stability'] for r in results]
    entropy = [r['entropy'] for r in results]
    
    # Plot 1: Total scores
    ax1 = axes[0, 0]
    bars1 = ax1.bar(names, scores, color=['blue', 'green', 'orange', 'red'])
    ax1.set_ylabel('Total Score')
    ax1.set_title('Score Comparison')
    ax1.tick_params(axis='x', rotation=45)
    
    # Add score values on bars
    for bar, score in zip(bars1, scores):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                f'{score:.1f}', ha='center', va='bottom')
    
    # Plot 2: Particle counts
    ax2 = axes[0, 1]
    bars2 = ax2.bar(names, particles, color=['blue', 'green', 'orange', 'red'])
    ax2.set_ylabel('Particles Created')
    ax2.set_title('Particle Creation')
    ax2.tick_params(axis='x', rotation=45)
    
    # Plot 3: Stability times
    ax3 = axes[1, 0]
    bars3 = ax3.bar(names, stability, color=['blue', 'green', 'orange', 'red'])
    ax3.set_ylabel('Stability Time')
    ax3.set_title('Universe Stability')
    ax3.tick_params(axis='x', rotation=45)
    
    # Plot 4: Entropy values
    ax4 = axes[1, 1]
    bars4 = ax4.bar(names, entropy, color=['blue', 'green', 'orange', 'red'])
    ax4.set_ylabel('Entropy')
    ax4.set_title('Universe Complexity')
    ax4.tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.show()
    
    # Find best configuration
    best_config = max(results, key=lambda x: x['score'])
    print(f"\n🏆 Best configuration: {best_config['name']}")
    print(f"   Score: {best_config['score']:.1f}")


def main():
    """Main function."""
    print("🚀 Universe Game Tutorial")
    print("=" * 60)
    
    try:
        # Run tutorial
        run_tutorial()
        
        # Demonstrate scoring system
        demonstrate_scoring_system()
        
        print("\n✅ Tutorial completed successfully!")
        print("🎮 Ready to play the full quantum void physics game!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
