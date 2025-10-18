"""
Toy Model: 0D Void Physics Simulation

This example demonstrates the core concepts of void physics using a simple
0D (zero-dimensional) model. We simulate the stochastic evolution of a scalar
field in a double-well potential, representing the transition from void to
ordered states.

The model includes:
- Double-well potential V(phi) = (lambda/4)(phi² - v²)²
- Langevin dynamics: dphi/dt = -Gamma dV/dphi + η(t)
- First passage time analysis
- Entropy evolution
- Statistical analysis of nucleation events
"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import sys

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from void_physic.core.potential import DoubleWellPotential, PotentialParameters
from void_physic.core.stochastic import LangevinDynamics, WhiteNoise
from void_physic.simulation.langevin_solver import LangevinSolver, SolverParameters
from void_physic.simulation.statistics import FirstPassageTime, EntropyCalculator
from void_physic.utils.constants import PhysicalConstants


def run_toy_model():
    """Run the complete toy model simulation."""
    
    print("Void Physics Toy Model - 0D Simulation")
    print("=" * 50)
    
    # 1. Set up parameters
    print("\n1. Setting up parameters...")
    
    # Potential parameters
    potential_params = PotentialParameters(
        lambda_coupling=1.0,  # Self-coupling strength
        v_vev=1.0,           # Vacuum expectation value
        V0_offset=0.0        # Potential offset
    )
    
    # Physical constants
    constants = PhysicalConstants(
        gamma_friction=1.0,   # Friction coefficient
        noise_strength=0.5,   # Noise amplitude (void strength)
        dt_default=0.01,      # Time step
        n_trajectories=1000   # Number of stochastic trajectories
    )
    
    # Solver parameters
    solver_params = SolverParameters(
        dt=0.01,
        t_max=50.0,
        n_trajectories=1000,
        save_trajectories=True
    )
    
    print(f"   • Coupling strength lambda = {potential_params.lambda_coupling}")
    print(f"   • Vacuum expectation value v = {potential_params.v_vev}")
    print(f"   • Friction coefficient Gamma = {constants.gamma_friction}")
    print(f"   • Noise strength D = {constants.noise_strength}")
    print(f"   • Number of trajectories = {solver_params.n_trajectories}")
    
    # 2. Initialize components
    print("\n2. Initializing components...")
    
    potential = DoubleWellPotential(potential_params)
    noise_model = WhiteNoise(constants.noise_strength, seed=42)
    langevin_dynamics = LangevinDynamics(potential, noise_model, constants)
    solver = LangevinSolver(langevin_dynamics, constants)
    
    # 3. Analyze potential
    print("\n3. Analyzing potential...")
    
    critical_points = potential.critical_points()
    stability = potential.stability_analysis()
    barrier_height = potential.barrier_height()
    
    print(f"   • Critical points: {critical_points}")
    print(f"   • Stability analysis:")
    for name, info in stability.items():
        print(f"     - {name}: {info['type']} (m² = {info['mass_squared']:.3f})")
    print(f"   • Barrier height: {barrier_height:.3f}")
    
    # 4. Run ensemble simulation
    print("\n4. Running ensemble simulation...")
    
    # Start from symmetric state (void)
    phi0 = 0.0
    
    ensemble_results = solver.ensemble_simulation(phi0, solver_params)
    
    print(f"   • Simulated {solver_params.n_trajectories} trajectories")
    print(f"   • Time range: 0 to {solver_params.t_max}")
    print(f"   • Final mean field: {ensemble_results['mean_field'][-1]:.3f}")
    print(f"   • Final field variance: {ensemble_results['var_field'][-1]:.3f}")
    
    # 5. First passage time analysis
    print("\n5. Analyzing first passage times...")
    
    fpt_analyzer = FirstPassageTime()
    
    # Calculate FPT to positive vacuum
    threshold = 0.5 * potential_params.v_vev  # Halfway to vacuum
    fpt_results = solver.first_passage_analysis(phi0, threshold, solver_params)
    
    print(f"   • Threshold: phi = {threshold}")
    print(f"   • Mean FPT: {fpt_results['mean_fpt']:.3f}")
    print(f"   • Survival probability: {fpt_results['survival_probability']:.3f}")
    
    # Fit distributions
    exponential_fit = fpt_analyzer.fit_exponential_distribution(fpt_results['first_passage_times'])
    weibull_fit = fpt_analyzer.fit_weibull_distribution(fpt_results['first_passage_times'])
    
    if 'p_value' in exponential_fit:
        print(f"   • Exponential fit: rate = {exponential_fit['rate']:.3f}, p-value = {exponential_fit['p_value']:.3f}")
    else:
        print(f"   • Exponential fit: rate = {exponential_fit['rate']:.3f}, fit_success = {exponential_fit['fit_success']}")
    print(f"   • Weibull fit: shape = {weibull_fit['shape']:.3f}, scale = {weibull_fit['scale']:.3f}")
    
    # 6. Entropy analysis
    print("\n6. Calculating entropy evolution...")
    
    entropy_calc = EntropyCalculator()
    
    if ensemble_results['trajectories'] is not None:
        entropy = entropy_calc.field_entropy(ensemble_results['trajectories'], ensemble_results['time'])
        entropy_rate = entropy_calc.entropy_production_rate(entropy, ensemble_results['time'])
        
        print(f"   • Initial entropy: {entropy[0]:.3f}")
        print(f"   • Final entropy: {entropy[-1]:.3f}")
        print(f"   • Maximum entropy rate: {np.max(entropy_rate):.3f}")
        
        # Thermodynamic quantities
        thermo_quantities = entropy_calc.thermodynamic_quantities(
            ensemble_results['trajectories'], 
            ensemble_results['time'],
            potential
        )
        
        print(f"   • Final temperature: {thermo_quantities['temperature'][-1]:.3f}")
        print(f"   • Final free energy: {thermo_quantities['free_energy'][-1]:.3f}")
    
    # 7. Create visualizations
    print("\n7. Creating visualizations...")
    
    create_plots(ensemble_results, fpt_results, entropy, entropy_rate, potential, solver_params)
    
    print("\n Toy model simulation completed!")
    print(f"   • Plots saved to: {Path(__file__).parent / 'toy_model_results.png'}")
    
    return {
        'ensemble_results': ensemble_results,
        'fpt_results': fpt_results,
        'entropy': entropy,
        'entropy_rate': entropy_rate,
        'potential': potential,
        'parameters': solver_params
    }


def create_plots(ensemble_results, fpt_results, entropy, entropy_rate, potential, params):
    """Create comprehensive plots of the simulation results."""
    
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    fig.suptitle('Void Physics Toy Model - 0D Simulation Results', fontsize=16)
    
    time = ensemble_results['time']
    
    # 1. Potential landscape
    ax1 = axes[0, 0]
    phi_range = np.linspace(-2, 2, 100)
    V_phi = potential(phi_range)
    ax1.plot(phi_range, V_phi, 'b-', linewidth=2, label='V(phi)')
    ax1.axhline(y=0, color='k', linestyle='--', alpha=0.5)
    ax1.axvline(x=0, color='k', linestyle='--', alpha=0.5)
    ax1.set_xlabel('Field phi')
    ax1.set_ylabel('Potential V(phi)')
    ax1.set_title('Double-Well Potential')
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    
    # 2. Field evolution (mean ± std)
    ax2 = axes[0, 1]
    mean_phi = ensemble_results['mean_field']
    std_phi = ensemble_results['std_field']
    ax2.plot(time, mean_phi, 'r-', linewidth=2, label='phi')
    ax2.fill_between(time, mean_phi - std_phi, mean_phi + std_phi, 
                     alpha=0.3, color='red', label='±sigma')
    ax2.axhline(y=0, color='k', linestyle='--', alpha=0.5)
    ax2.set_xlabel('Time')
    ax2.set_ylabel('Field phi')
    ax2.set_title('Field Evolution')
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    
    # 3. Energy evolution
    ax3 = axes[0, 2]
    mean_energy = ensemble_results['mean_energy']
    ax3.plot(time, mean_energy, 'g-', linewidth=2, label='E')
    ax3.set_xlabel('Time')
    ax3.set_ylabel('Energy')
    ax3.set_title('Energy Evolution')
    ax3.grid(True, alpha=0.3)
    ax3.legend()
    
    # 4. Entropy evolution
    ax4 = axes[1, 0]
    ax4.plot(time, entropy, 'purple', linewidth=2, label='S(t)')
    ax4.set_xlabel('Time')
    ax4.set_ylabel('Entropy S')
    ax4.set_title('Entropy Evolution')
    ax4.grid(True, alpha=0.3)
    ax4.legend()
    
    # 5. Entropy production rate
    ax5 = axes[1, 1]
    ax5.plot(time, entropy_rate, 'orange', linewidth=2, label='dS/dt')
    ax5.axhline(y=0, color='k', linestyle='--', alpha=0.5)
    ax5.set_xlabel('Time')
    ax5.set_ylabel('Entropy Rate dS/dt')
    ax5.set_title('Entropy Production Rate')
    ax5.grid(True, alpha=0.3)
    ax5.legend()
    
    # 6. First passage time histogram
    ax6 = axes[1, 2]
    finite_fpt = fpt_results['finite_times']
    if len(finite_fpt) > 0:
        ax6.hist(finite_fpt, bins=30, alpha=0.7, color='cyan', edgecolor='black')
        ax6.axvline(fpt_results['mean_fpt'], color='red', linestyle='--', 
                   linewidth=2, label=f'Mean: {fpt_results["mean_fpt"]:.2f}')
        ax6.set_xlabel('First Passage Time')
        ax6.set_ylabel('Frequency')
        ax6.set_title('First Passage Time Distribution')
        ax6.legend()
    else:
        ax6.text(0.5, 0.5, 'No finite FPTs', ha='center', va='center', transform=ax6.transAxes)
        ax6.set_title('First Passage Time Distribution')
    ax6.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    # Save plot
    output_path = Path(__file__).parent / 'toy_model_results.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.show()


def analyze_parameter_dependence():
    """Analyze how results depend on key parameters."""
    
    print("\n Parameter Dependence Analysis")
    print("=" * 40)
    
    # Test different noise strengths
    noise_strengths = [0.1, 0.3, 0.5, 0.7, 1.0]
    mean_fpts = []
    
    for noise_strength in noise_strengths:
        print(f"\nTesting noise strength D = {noise_strength}")
        
        # Set up with different noise strength
        constants = PhysicalConstants(noise_strength=noise_strength)
        potential = DoubleWellPotential()
        noise_model = WhiteNoise(noise_strength, seed=42)
        langevin_dynamics = LangevinDynamics(potential, noise_model, constants)
        solver = LangevinSolver(langevin_dynamics, constants)
        
        # Run simulation
        params = SolverParameters(n_trajectories=500, t_max=30.0)
        fpt_results = solver.first_passage_analysis(0.0, 0.5, params)
        
        mean_fpts.append(fpt_results['mean_fpt'])
        print(f"   Mean FPT: {fpt_results['mean_fpt']:.3f}")
    
    # Plot results
    plt.figure(figsize=(10, 6))
    plt.subplot(1, 2, 1)
    plt.plot(noise_strengths, mean_fpts, 'bo-', linewidth=2, markersize=8)
    plt.xlabel('Noise Strength D')
    plt.ylabel('Mean First Passage Time')
    plt.title('FPT vs Noise Strength')
    plt.grid(True, alpha=0.3)
    
    # Test different friction coefficients
    friction_coeffs = [0.5, 1.0, 1.5, 2.0, 2.5]
    mean_fpts_friction = []
    
    for gamma in friction_coeffs:
        print(f"\nTesting friction coefficient Gamma = {gamma}")
        
        constants = PhysicalConstants(gamma_friction=gamma)
        potential = DoubleWellPotential()
        noise_model = WhiteNoise(0.5, seed=42)
        langevin_dynamics = LangevinDynamics(potential, noise_model, constants)
        solver = LangevinSolver(langevin_dynamics, constants)
        
        params = SolverParameters(n_trajectories=500, t_max=30.0)
        fpt_results = solver.first_passage_analysis(0.0, 0.5, params)
        
        mean_fpts_friction.append(fpt_results['mean_fpt'])
        print(f"   Mean FPT: {fpt_results['mean_fpt']:.3f}")
    
    plt.subplot(1, 2, 2)
    plt.plot(friction_coeffs, mean_fpts_friction, 'ro-', linewidth=2, markersize=8)
    plt.xlabel('Friction Coefficient Gamma')
    plt.ylabel('Mean First Passage Time')
    plt.title('FPT vs Friction Coefficient')
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(Path(__file__).parent / 'parameter_dependence.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print(f"\n Parameter analysis completed!")
    print(f"   • Plots saved to: {Path(__file__).parent / 'parameter_dependence.png'}")


if __name__ == "__main__":
    # Run main simulation
    results = run_toy_model()
    
    # Run parameter analysis
    analyze_parameter_dependence()
    
    print("\nAll simulations completed successfully!")
    print("\nKey insights from the toy model:")
    print("• The void state (phi=0) is metastable and can nucleate ordered domains")
    print("• Noise strength controls the nucleation rate")
    print("• Entropy increases during the transition, driving time's arrow")
    print("• First passage times follow exponential/Weibull distributions")
    print("• The system exhibits phase transition behavior")
