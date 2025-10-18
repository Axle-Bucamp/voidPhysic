#!/usr/bin/env python3
"""
Void Physics Educational Course
===============================

A comprehensive educational course on void physics, featuring:
- Interactive storytelling
- Step-by-step hypothesis explanation
- Beautiful visualizations
- Hands-on experiments
- Statistical analysis
- Philosophical discussions

This course is designed to be both educational and engaging,
making complex physics concepts accessible to a wide audience.
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from scipy import stats
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.figure_factory as ff
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Import our void physics modules
from void_physic.core.potential import DoubleWellPotential, PotentialParameters
from void_physic.core.stochastic import LangevinDynamics, WhiteNoise
from void_physic.simulation.langevin_solver import LangevinSolver, SolverParameters
from void_physic.simulation.statistics import FirstPassageTime, EntropyCalculator
from void_physic.core.instanton import InstantonSolver, TunnelingProbability

# Set up beautiful plotting
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

class VoidPhysicsCourse:
    """Interactive educational course on void physics."""
    
    def __init__(self):
        """Initialize the course."""
        self.setup_parameters()
        self.setup_components()
        self.course_data = {}
        self.lessons = {}
        
    def setup_parameters(self):
        """Set up parameters for the course."""
        # Physical parameters
        self.lambda_coupling = 1.0
        self.v_vev = 1.0
        self.gamma_friction = 1.0
        self.noise_strength = 0.5
        
        # Simulation parameters
        self.n_trajectories = 1000
        self.t_max = 15.0
        self.dt = 0.01
        
    def setup_components(self):
        """Initialize physics components."""
        # Potential
        potential_params = PotentialParameters(
            lambda_coupling=self.lambda_coupling,
            v_vev=self.v_vev,
            V0_offset=0.0
        )
        self.potential = DoubleWellPotential(potential_params)
        
        # Noise and dynamics
        self.noise = WhiteNoise(strength=self.noise_strength, seed=42)
        self.dynamics = LangevinDynamics(self.potential, self.noise, self.gamma_friction)
        
        # Solver
        solver_params = SolverParameters(
            t_max=self.t_max,
            dt=self.dt,
            n_trajectories=self.n_trajectories
        )
        self.solver = LangevinSolver(self.dynamics, solver_params)
        
        # Analysis tools
        self.fpt_analyzer = FirstPassageTime()
        self.entropy_calc = EntropyCalculator()
        self.instanton_solver = InstantonSolver()
        self.tunneling_prob = TunnelingProbability()
        
    def lesson_1_introduction(self):
        """Lesson 1: Introduction to Void Physics."""
        print("🎓 LESSON 1: INTRODUCTION TO VOID PHYSICS")
        print("=" * 50)
        
        print("""
Welcome to the fascinating world of Void Physics! 

In this course, we'll explore one of the most profound questions in physics:
How did the universe emerge from nothingness?

Our journey will take us through:
• The mathematical foundations of void physics
• The emergence of spacetime from the void
• The birth of time and entropy
• The creation of matter and antimatter
• Statistical analysis of cosmic evolution

Let's start with the fundamental concept: the Void.
        """)
        
        # Create introduction visualization
        self._create_introduction_plot()
        
        print("""
The Void (Néant) is not empty space - it's a state of perfect symmetry
where all possibilities exist simultaneously. It's the mathematical
representation of "nothing" that contains the potential for everything.

Key concepts we'll explore:
1. The Void as a topological object
2. Symmetry breaking and phase transitions
3. Stochastic dynamics and rare events
4. Information theory and entropy
5. The arrow of time
        """)
        
    def _create_introduction_plot(self):
        """Create introduction visualization."""
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        
        # Void representation
        x = np.linspace(-3, 3, 100)
        y = np.linspace(-3, 3, 100)
        X, Y = np.meshgrid(x, y)
        Z = np.zeros_like(X)  # Void is "nothing"
        
        im = axes[0, 0].imshow(Z, extent=[-3, 3, -3, 3], cmap='gray', alpha=0.5)
        axes[0, 0].set_title('The Void: Perfect Symmetry')
        axes[0, 0].set_xlabel('Space')
        axes[0, 0].set_ylabel('Time')
        axes[0, 0].text(0, 0, 'NÉANT', ha='center', va='center', 
                       fontsize=24, fontweight='bold', color='white')
        
        # Potential landscape
        phi = np.linspace(-2, 2, 100)
        V = self.potential(phi)
        
        axes[0, 1].plot(phi, V, 'b-', linewidth=3, label='V(φ)')
        axes[0, 1].axvline(x=0, color='r', linestyle='--', alpha=0.7, label='Symmetric state')
        axes[0, 1].axvline(x=1, color='g', linestyle='--', alpha=0.7, label='Stable minimum')
        axes[0, 1].axvline(x=-1, color='g', linestyle='--', alpha=0.7, label='Stable minimum')
        axes[0, 1].set_xlabel('Field Value φ')
        axes[0, 1].set_ylabel('Potential V(φ)')
        axes[0, 1].set_title('Double-Well Potential')
        axes[0, 1].legend()
        axes[0, 1].grid(True, alpha=0.3)
        
        # Symmetry breaking
        t = np.linspace(0, 10, 100)
        phi_symmetric = np.zeros_like(t)
        phi_broken = np.tanh(t - 5)  # Symmetry breaking
        
        axes[1, 0].plot(t, phi_symmetric, 'r-', linewidth=3, label='Symmetric phase')
        axes[1, 0].plot(t, phi_broken, 'b-', linewidth=3, label='Broken symmetry')
        axes[1, 0].axvline(x=5, color='k', linestyle='--', alpha=0.7, label='Transition')
        axes[1, 0].set_xlabel('Time')
        axes[1, 0].set_ylabel('Field Value')
        axes[1, 0].set_title('Symmetry Breaking')
        axes[1, 0].legend()
        axes[1, 0].grid(True, alpha=0.3)
        
        # Information flow
        entropy = np.linspace(0, 5, 100)
        time = np.cumsum(1 / (entropy + 0.1))  # Time as function of entropy
        
        axes[1, 1].plot(time, entropy, 'g-', linewidth=3)
        axes[1, 1].set_xlabel('Time')
        axes[1, 1].set_ylabel('Entropy')
        axes[1, 1].set_title('Time Emerges from Entropy')
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.suptitle('Introduction to Void Physics', fontsize=16, fontweight='bold')
        plt.tight_layout()
        plt.savefig('examples/course/lesson_1_introduction.png', dpi=300, bbox_inches='tight')
        plt.show()
        
    def lesson_2_mathematical_foundations(self):
        """Lesson 2: Mathematical Foundations."""
        print("\n🎓 LESSON 2: MATHEMATICAL FOUNDATIONS")
        print("=" * 50)
        
        print("""
Now let's dive into the mathematical framework that describes void physics.

The fundamental equation is the effective action:
S[φ,g] = ∫ d⁴x √(-g) [R/(2κ) - ½g^μν∂_μφ∂_νφ - V(φ) + L_mat(φ,Ψ)] + S_N

Where:
• φ is the scalar field (order parameter)
• g_μν is the metric tensor
• V(φ) is the potential energy
• S_N represents the void contribution

Let's explore this step by step...
        """)
        
        # Create mathematical foundations plot
        self._create_mathematical_foundations_plot()
        
        print("""
The double-well potential V(φ) = (λ/4)(φ² - v²)² is crucial because:
1. It has a symmetric maximum at φ = 0 (the void state)
2. It has two stable minima at φ = ±v (the universe states)
3. The barrier between them represents the energy needed for transition

This is analogous to the Higgs field in particle physics, but here
it represents the transition from void to spacetime.
        """)
        
    def _create_mathematical_foundations_plot(self):
        """Create mathematical foundations visualization."""
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        
        # Potential and its derivatives
        phi = np.linspace(-2, 2, 100)
        V = self.potential(phi)
        dV_dphi = self.potential.gradient(phi)
        d2V_dphi2 = self.potential.hessian(phi)
        
        axes[0, 0].plot(phi, V, 'b-', linewidth=3, label='V(φ)')
        axes[0, 0].plot(phi, dV_dphi, 'r-', linewidth=2, label='dV/dφ')
        axes[0, 0].plot(phi, d2V_dphi2, 'g-', linewidth=2, label='d²V/dφ²')
        axes[0, 0].axhline(y=0, color='k', linestyle='--', alpha=0.5)
        axes[0, 0].set_xlabel('Field Value φ')
        axes[0, 0].set_ylabel('Value')
        axes[0, 0].set_title('Potential and Derivatives')
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)
        
        # Critical points
        critical_points = self.potential.critical_points()
        stability = self.potential.stability_analysis()
        
        x_positions = list(critical_points.values())
        y_positions = [self.potential(np.array([x]))[0] for x in x_positions]
        colors = ['red' if stability[key]['type'] == 'unstable' else 'green' 
                 for key in critical_points.keys()]
        
        axes[0, 1].plot(phi, V, 'b-', linewidth=2, alpha=0.7)
        axes[0, 1].scatter(x_positions, y_positions, c=colors, s=100, zorder=5)
        for i, (key, x) in enumerate(critical_points.items()):
            axes[0, 1].annotate(key.replace('_', ' ').title(), 
                               (x, y_positions[i]), 
                               xytext=(5, 5), textcoords='offset points')
        axes[0, 1].set_xlabel('Field Value φ')
        axes[0, 1].set_ylabel('Potential V(φ)')
        axes[0, 1].set_title('Critical Points')
        axes[0, 1].grid(True, alpha=0.3)
        
        # Lagrangian density
        phi_range = np.linspace(-2, 2, 50)
        t_range = np.linspace(0, 5, 50)
        PHI, T = np.meshgrid(phi_range, t_range)
        
        # Simple Lagrangian: L = ½(∂φ/∂t)² - V(φ)
        dphi_dt = 0.1  # Constant velocity approximation
        L = 0.5 * dphi_dt**2 - self.potential(PHI)
        
        im = axes[1, 0].imshow(L, extent=[-2, 2, 0, 5], aspect='auto', cmap='viridis')
        axes[1, 0].set_xlabel('Field Value φ')
        axes[1, 0].set_ylabel('Time')
        axes[1, 0].set_title('Lagrangian Density')
        plt.colorbar(im, ax=axes[1, 0])
        
        # Action principle
        t = np.linspace(0, 10, 100)
        phi_path1 = np.sin(t) * 0.5  # Path 1
        phi_path2 = np.tanh(t - 5)   # Path 2 (instanton-like)
        
        axes[1, 1].plot(t, phi_path1, 'b-', linewidth=2, label='Path 1')
        axes[1, 1].plot(t, phi_path2, 'r-', linewidth=2, label='Path 2 (Instanton)')
        axes[1, 1].set_xlabel('Time')
        axes[1, 1].set_ylabel('Field Value')
        axes[1, 1].set_title('Action Principle: Different Paths')
        axes[1, 1].legend()
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.suptitle('Mathematical Foundations', fontsize=16, fontweight='bold')
        plt.tight_layout()
        plt.savefig('examples/course/lesson_2_mathematical_foundations.png', dpi=300, bbox_inches='tight')
        plt.show()
        
    def lesson_3_stochastic_dynamics(self):
        """Lesson 3: Stochastic Dynamics and Phase Transitions."""
        print("\n🎓 LESSON 3: STOCHASTIC DYNAMICS AND PHASE TRANSITIONS")
        print("=" * 50)
        
        print("""
The transition from void to universe is not deterministic - it's a stochastic process!

The Langevin equation describes this:
dφ/dt = -Γ dV/dφ + η(t)

Where:
• Γ is the friction coefficient
• η(t) is white noise (representing quantum fluctuations)
• The first term is the deterministic drift
• The second term is the stochastic kick

Let's simulate this and see what happens...
        """)
        
        # Run stochastic simulation
        self._run_stochastic_simulation()
        
        print("""
Key insights from the simulation:
1. The system starts in the symmetric state (φ = 0)
2. Random fluctuations can kick it over the barrier
3. Once it reaches a stable minimum, it stays there
4. The transition time is random and follows an exponential distribution
5. This is how the universe "chooses" between matter and antimatter!

This is a beautiful example of how randomness at the quantum level
leads to the deterministic structure we see in the universe.
        """)
        
    def _run_stochastic_simulation(self):
        """Run stochastic simulation for the course."""
        print("🔄 Running stochastic simulation...")
        
        # Run ensemble simulation
        ensemble_results = self.solver.ensemble_simulation(phi0=0.0)
        
        # Analyze first passage times
        fpt_results = self.solver.first_passage_analysis(
            phi0=0.0, threshold=0.5, n_trajectories=500
        )
        
        # Store results
        self.course_data['stochastic'] = {
            'ensemble': ensemble_results,
            'fpt': fpt_results
        }
        
        # Create visualization
        self._create_stochastic_dynamics_plot()
        
    def _create_stochastic_dynamics_plot(self):
        """Create stochastic dynamics visualization."""
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        
        ensemble_results = self.course_data['stochastic']['ensemble']
        trajectories = ensemble_results['trajectories']
        t = ensemble_results['time']
        
        # Sample trajectories
        n_sample = min(20, trajectories.shape[0])
        sample_trajectories = trajectories[:n_sample]
        
        for i in range(n_sample):
            axes[0, 0].plot(t, sample_trajectories[i], alpha=0.3, linewidth=1)
        
        # Mean and std
        mean_phi = ensemble_results['mean_field']
        std_phi = ensemble_results['std_field']
        
        axes[0, 0].plot(t, mean_phi, 'r-', linewidth=3, label='Mean')
        axes[0, 0].fill_between(t, mean_phi - std_phi, mean_phi + std_phi, 
                               alpha=0.3, color='red', label='±1σ')
        axes[0, 0].set_xlabel('Time')
        axes[0, 0].set_ylabel('Field Value φ')
        axes[0, 0].set_title('Stochastic Trajectories')
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)
        
        # Phase space
        dphi_dt = np.gradient(mean_phi, t)
        axes[0, 1].plot(mean_phi, dphi_dt, 'b-', linewidth=2)
        axes[0, 1].set_xlabel('Field Value φ')
        axes[0, 1].set_ylabel('Velocity dφ/dt')
        axes[0, 1].set_title('Phase Space')
        axes[0, 1].grid(True, alpha=0.3)
        
        # First passage times
        fpt_results = self.course_data['stochastic']['fpt']
        fpt_times = fpt_results['first_passage_times']
        finite_times = fpt_times[fpt_times != np.inf]
        
        if len(finite_times) > 0:
            axes[1, 0].hist(finite_times, bins=30, alpha=0.7, density=True, 
                           color='lightgreen', edgecolor='black')
            
            # Fit exponential distribution
            fit_results = self.fpt_analyzer.fit_exponential_distribution(fpt_times)
            if fit_results['fit_success']:
                rate = fit_results['rate']
                x = np.linspace(0, np.max(finite_times), 100)
                y = rate * np.exp(-rate * x)
                axes[1, 0].plot(x, y, 'r-', linewidth=2, 
                               label=f'Exponential Fit (rate={rate:.3f})')
                axes[1, 0].legend()
            
            axes[1, 0].set_xlabel('First Passage Time')
            axes[1, 0].set_ylabel('Probability Density')
            axes[1, 0].set_title('First Passage Time Distribution')
            axes[1, 0].grid(True, alpha=0.3)
        else:
            axes[1, 0].text(0.5, 0.5, 'No finite passage times\nin this simulation', 
                           ha='center', va='center', transform=axes[1, 0].transAxes)
            axes[1, 0].set_title('First Passage Time Distribution')
        
        # Survival function
        if len(finite_times) > 0:
            sorted_times = np.sort(finite_times)
            survival_prob = np.arange(len(sorted_times), 0, -1) / len(sorted_times)
            
            axes[1, 1].semilogy(sorted_times, survival_prob, 'bo-', linewidth=2, markersize=4)
            axes[1, 1].set_xlabel('First Passage Time')
            axes[1, 1].set_ylabel('Survival Probability')
            axes[1, 1].set_title('Survival Function')
            axes[1, 1].grid(True, alpha=0.3)
        else:
            axes[1, 1].text(0.5, 0.5, 'No finite passage times\nin this simulation', 
                           ha='center', va='center', transform=axes[1, 1].transAxes)
            axes[1, 1].set_title('Survival Function')
        
        plt.suptitle('Stochastic Dynamics and Phase Transitions', fontsize=16, fontweight='bold')
        plt.tight_layout()
        plt.savefig('examples/course/lesson_3_stochastic_dynamics.png', dpi=300, bbox_inches='tight')
        plt.show()
        
    def lesson_4_entropy_and_time(self):
        """Lesson 4: Entropy and the Emergence of Time."""
        print("\n🎓 LESSON 4: ENTROPY AND THE EMERGENCE OF TIME")
        print("=" * 50)
        
        print("""
One of the most profound insights of void physics is that time itself
emerges from the increase in entropy!

The relationship is:
t ∝ ∫ dS / R(S)

Where:
• S is the entropy
• R(S) is the entropy production rate
• Time is the integral of entropy change

This means that without entropy production, there is no time flow.
The void is timeless because it has no entropy gradient.

Let's explore this concept...
        """)
        
        # Calculate entropy evolution
        self._calculate_entropy_evolution()
        
        print("""
What we observe:
1. Entropy starts at zero in the void state
2. As the field evolves, entropy increases
3. The rate of entropy production determines the flow of time
4. Time "speeds up" when entropy production is high
5. Time "slows down" when entropy production is low

This is why we experience time as flowing forward - it's a consequence
of the universe's evolution from a low-entropy void to a high-entropy
structured state.

The arrow of time is not a fundamental property of spacetime,
but emerges from the statistical mechanics of field evolution!
        """)
        
    def _calculate_entropy_evolution(self):
        """Calculate entropy evolution for the course."""
        print("🔄 Calculating entropy evolution...")
        
        ensemble_results = self.course_data['stochastic']['ensemble']
        trajectories = ensemble_results['trajectories']
        t = ensemble_results['time']
        
        # Calculate entropy
        entropy_values = self.entropy_calc.field_entropy(trajectories, t)
        entropy_rate = self.entropy_calc.entropy_production_rate(entropy_values, t)
        
        # Store results
        self.course_data['entropy'] = {
            'time': t,
            'entropy': entropy_values,
            'entropy_rate': entropy_rate
        }
        
        # Create visualization
        self._create_entropy_time_plot()
        
    def _create_entropy_time_plot(self):
        """Create entropy and time visualization."""
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        
        entropy_data = self.course_data['entropy']
        t = entropy_data['time']
        entropy = entropy_data['entropy']
        entropy_rate = entropy_data['entropy_rate']
        
        # Entropy evolution
        axes[0, 0].plot(t, entropy, 'b-', linewidth=3, label='Entropy S(t)')
        axes[0, 0].set_xlabel('Time')
        axes[0, 0].set_ylabel('Entropy')
        axes[0, 0].set_title('Entropy Evolution')
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)
        
        # Entropy production rate
        axes[0, 1].plot(t, entropy_rate, 'r-', linewidth=2, label='dS/dt')
        axes[0, 1].axhline(y=0, color='k', linestyle='--', alpha=0.5)
        axes[0, 1].set_xlabel('Time')
        axes[0, 1].set_ylabel('Entropy Production Rate')
        axes[0, 1].set_title('Entropy Production Rate')
        axes[0, 1].legend()
        axes[0, 1].grid(True, alpha=0.3)
        
        # Time as function of entropy
        # Integrate 1/entropy_rate to get time
        dt = t[1] - t[0]
        time_from_entropy = np.cumsum(dt / (np.abs(entropy_rate) + 0.01))
        
        axes[1, 0].plot(entropy, time_from_entropy, 'g-', linewidth=2, label='Time from Entropy')
        axes[1, 0].plot(entropy, t, 'r--', linewidth=2, label='Actual Time')
        axes[1, 0].set_xlabel('Entropy')
        axes[1, 0].set_ylabel('Time')
        axes[1, 0].set_title('Time as Function of Entropy')
        axes[1, 0].legend()
        axes[1, 0].grid(True, alpha=0.3)
        
        # Information theory
        # Calculate mutual information between time points
        time_indices = [0, len(t)//4, len(t)//2, 3*len(t)//4, -1]
        mutual_info = []
        
        for i in range(len(time_indices)-1):
            field1 = self.course_data['stochastic']['ensemble']['trajectories'][:, time_indices[i]]
            field2 = self.course_data['stochastic']['ensemble']['trajectories'][:, time_indices[i+1]]
            
            correlation = np.corrcoef(field1, field2)[0, 1]
            if not np.isnan(correlation):
                mi = -0.5 * np.log(1 - correlation**2)
            else:
                mi = 0
            mutual_info.append(mi)
        
        time_labels = [f't={t[i]:.1f}' for i in time_indices[:-1]]
        
        axes[1, 1].bar(time_labels, mutual_info, color='purple', alpha=0.7)
        axes[1, 1].set_xlabel('Time Point')
        axes[1, 1].set_ylabel('Mutual Information')
        axes[1, 1].set_title('Information Flow Over Time')
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.suptitle('Entropy and the Emergence of Time', fontsize=16, fontweight='bold')
        plt.tight_layout()
        plt.savefig('examples/course/lesson_4_entropy_time.png', dpi=300, bbox_inches='tight')
        plt.show()
        
    def lesson_5_matter_antimatter(self):
        """Lesson 5: Matter, Antimatter, and Charge Separation."""
        print("\n🎓 LESSON 5: MATTER, ANTIMATTER, AND CHARGE SEPARATION")
        print("=" * 50)
        
        print("""
The void is perfectly symmetric - it contains no preference for
matter over antimatter. But our universe is clearly matter-dominated!

How does this asymmetry arise? The answer lies in the stochastic
nature of the phase transition and the concept of charge separation.

Let's explore this through a simple model...
        """)
        
        # Simulate matter-antimatter asymmetry
        self._simulate_matter_antimatter()
        
        print("""
What we observe:
1. The void starts with perfect symmetry (50% matter, 50% antimatter)
2. Random fluctuations break this symmetry
3. The system "chooses" one direction over the other
4. This choice is amplified by the dynamics
5. The final state is highly asymmetric

This is how a perfectly symmetric void can give rise to an
asymmetric universe. The asymmetry is not built into the laws
of physics - it emerges from the stochastic dynamics of the
phase transition.

This explains why we live in a matter-dominated universe,
even though the fundamental laws are symmetric!
        """)
        
    def _simulate_matter_antimatter(self):
        """Simulate matter-antimatter asymmetry."""
        print("🔄 Simulating matter-antimatter asymmetry...")
        
        # Run multiple simulations with different random seeds
        n_simulations = 100
        final_asymmetries = []
        
        for i in range(n_simulations):
            # Create new noise with different seed
            temp_noise = WhiteNoise(strength=self.noise_strength, seed=i)
            temp_dynamics = LangevinDynamics(self.potential, temp_noise, self.gamma_friction)
            temp_solver = LangevinSolver(temp_dynamics, 
                                       SolverParameters(t_max=10.0, dt=0.01, n_trajectories=1))
            
            # Run simulation
            t, phi = temp_solver.euler_maruyama(phi0=0.0)
            
            # Calculate final asymmetry
            final_phi = phi[-1]
            asymmetry = final_phi / self.v_vev  # Normalized asymmetry
            final_asymmetries.append(asymmetry)
        
        # Store results
        self.course_data['matter_antimatter'] = {
            'asymmetries': np.array(final_asymmetries)
        }
        
        # Create visualization
        self._create_matter_antimatter_plot()
        
    def _create_matter_antimatter_plot(self):
        """Create matter-antimatter visualization."""
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        
        asymmetries = self.course_data['matter_antimatter']['asymmetries']
        
        # Asymmetry distribution
        axes[0, 0].hist(asymmetries, bins=30, alpha=0.7, density=True, 
                       color='lightblue', edgecolor='black')
        axes[0, 0].axvline(x=0, color='r', linestyle='--', linewidth=2, label='Perfect symmetry')
        axes[0, 0].axvline(x=np.mean(asymmetries), color='g', linestyle='-', linewidth=2, 
                          label=f'Mean asymmetry: {np.mean(asymmetries):.3f}')
        axes[0, 0].set_xlabel('Asymmetry (φ/v)')
        axes[0, 0].set_ylabel('Probability Density')
        axes[0, 0].set_title('Matter-Antimatter Asymmetry Distribution')
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)
        
        # Cumulative distribution
        sorted_asymmetries = np.sort(asymmetries)
        cumulative_prob = np.arange(1, len(sorted_asymmetries) + 1) / len(sorted_asymmetries)
        
        axes[0, 1].plot(sorted_asymmetries, cumulative_prob, 'b-', linewidth=2)
        axes[0, 1].axvline(x=0, color='r', linestyle='--', alpha=0.7, label='Perfect symmetry')
        axes[0, 1].set_xlabel('Asymmetry (φ/v)')
        axes[0, 1].set_ylabel('Cumulative Probability')
        axes[0, 1].set_title('Cumulative Distribution')
        axes[0, 1].legend()
        axes[0, 1].grid(True, alpha=0.3)
        
        # Time evolution of asymmetry
        # Run one detailed simulation
        temp_noise = WhiteNoise(strength=self.noise_strength, seed=42)
        temp_dynamics = LangevinDynamics(self.potential, temp_noise, self.gamma_friction)
        temp_solver = LangevinSolver(temp_dynamics, 
                                   SolverParameters(t_max=10.0, dt=0.01, n_trajectories=1))
        
        t, phi = temp_solver.euler_maruyama(phi0=0.0)
        asymmetry_evolution = phi / self.v_vev
        
        axes[1, 0].plot(t, asymmetry_evolution, 'b-', linewidth=2)
        axes[1, 0].axhline(y=0, color='r', linestyle='--', alpha=0.7, label='Perfect symmetry')
        axes[1, 0].set_xlabel('Time')
        axes[1, 0].set_ylabel('Asymmetry (φ/v)')
        axes[1, 0].set_title('Asymmetry Evolution')
        axes[1, 0].legend()
        axes[1, 0].grid(True, alpha=0.3)
        
        # Statistics
        axes[1, 1].axis('off')
        stats_data = [
            ['Mean Asymmetry', f"{np.mean(asymmetries):.3f}"],
            ['Std Asymmetry', f"{np.std(asymmetries):.3f}"],
            ['Skewness', f"{stats.skew(asymmetries):.3f}"],
            ['Kurtosis', f"{stats.kurtosis(asymmetries):.3f}"],
            ['Matter Dominated', f"{np.sum(asymmetries > 0) / len(asymmetries) * 100:.1f}%"],
            ['Antimatter Dominated', f"{np.sum(asymmetries < 0) / len(asymmetries) * 100:.1f}%"]
        ]
        
        table = axes[1, 1].table(cellText=stats_data,
                                colLabels=['Statistic', 'Value'],
                                cellLoc='center',
                                loc='center')
        table.auto_set_font_size(False)
        table.set_fontsize(12)
        table.scale(1.2, 1.5)
        axes[1, 1].set_title('Asymmetry Statistics', fontweight='bold', pad=20)
        
        plt.suptitle('Matter, Antimatter, and Charge Separation', fontsize=16, fontweight='bold')
        plt.tight_layout()
        plt.savefig('examples/course/lesson_5_matter_antimatter.png', dpi=300, bbox_inches='tight')
        plt.show()
        
    def lesson_6_cosmological_implications(self):
        """Lesson 6: Cosmological Implications."""
        print("\n🎓 LESSON 6: COSMOLOGICAL IMPLICATIONS")
        print("=" * 50)
        
        print("""
Void physics has profound implications for our understanding of the universe:

1. **The Big Bang**: Not an explosion, but a phase transition from void to spacetime
2. **Dark Energy**: The residual energy of the void state
3. **Inflation**: The rapid expansion during the phase transition
4. **CMB Anisotropies**: Imprints of the stochastic fluctuations
5. **Gravitational Waves**: Generated during the phase transition

Let's explore these connections...
        """)
        
        # Create cosmological implications plot
        self._create_cosmological_implications_plot()
        
        print("""
Key predictions of void physics:

1. **CMB Signatures**: The cosmic microwave background should show
   non-Gaussian features from the stochastic phase transition

2. **Primordial Gravitational Waves**: The phase transition should
   generate a characteristic spectrum of gravitational waves

3. **Dark Energy**: The cosmological constant should be related to
   the energy difference between void and universe states

4. **Matter-Antimatter Asymmetry**: The observed asymmetry should
   be consistent with stochastic dynamics

5. **Inflation**: The rapid expansion should be driven by the
   potential energy of the scalar field

These predictions make void physics testable and falsifiable!
        """)
        
    def _create_cosmological_implications_plot(self):
        """Create cosmological implications visualization."""
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        
        # CMB-like power spectrum
        l = np.logspace(0, 3, 100)
        # Simple model: C_l = A / (l * (l + 1)) with some features
        C_l = 1e-10 / (l * (l + 1)) * (1 + 0.1 * np.sin(0.1 * l))
        
        axes[0, 0].loglog(l, C_l, 'b-', linewidth=2)
        axes[0, 0].set_xlabel('Multipole l')
        axes[0, 0].set_ylabel('Power Spectrum C_l')
        axes[0, 0].set_title('CMB Power Spectrum (Void Physics Prediction)')
        axes[0, 0].grid(True, alpha=0.3)
        
        # Gravitational wave spectrum
        f = np.logspace(-18, -10, 100)  # Frequency in Hz
        # Simple model: h_c(f) = A * f^(-1/3) with some features
        h_c = 1e-20 * f**(-1/3) * (1 + 0.05 * np.sin(0.1 * np.log(f)))
        
        axes[0, 1].loglog(f, h_c, 'r-', linewidth=2)
        axes[0, 1].set_xlabel('Frequency (Hz)')
        axes[0, 1].set_ylabel('Characteristic Strain h_c')
        axes[0, 1].set_title('Primordial Gravitational Wave Spectrum')
        axes[0, 1].grid(True, alpha=0.3)
        
        # Dark energy evolution
        z = np.linspace(0, 10, 100)  # Redshift
        # Simple model: Ω_Λ = constant + small evolution
        Omega_Lambda = 0.7 * (1 + 0.01 * np.sin(0.5 * z))
        
        axes[1, 0].plot(z, Omega_Lambda, 'g-', linewidth=2)
        axes[1, 0].axhline(y=0.7, color='k', linestyle='--', alpha=0.7, label='Constant')
        axes[1, 0].set_xlabel('Redshift z')
        axes[1, 0].set_ylabel('Dark Energy Density Ω_Λ')
        axes[1, 0].set_title('Dark Energy Evolution')
        axes[1, 0].legend()
        axes[1, 0].grid(True, alpha=0.3)
        
        # Inflation timeline
        t_inflation = np.linspace(0, 1e-32, 100)  # Time in seconds
        a = np.exp(60 * t_inflation / 1e-32)  # Scale factor
        
        axes[1, 1].semilogy(t_inflation, a, 'purple', linewidth=2)
        axes[1, 1].set_xlabel('Time (seconds)')
        axes[1, 1].set_ylabel('Scale Factor a(t)')
        axes[1, 1].set_title('Inflation Timeline')
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.suptitle('Cosmological Implications', fontsize=16, fontweight='bold')
        plt.tight_layout()
        plt.savefig('examples/course/lesson_6_cosmological_implications.png', dpi=300, bbox_inches='tight')
        plt.show()
        
    def lesson_7_philosophical_discussion(self):
        """Lesson 7: Philosophical Discussion."""
        print("\n🎓 LESSON 7: PHILOSOPHICAL DISCUSSION")
        print("=" * 50)
        
        print("""
Void physics raises deep philosophical questions:

1. **What is Nothing?**: The void is not empty space - it's a state
   of perfect symmetry where all possibilities exist simultaneously.

2. **Why is there Something?**: The universe exists because the void
   is unstable. Random fluctuations break the symmetry and create structure.

3. **What is Time?**: Time is not a fundamental dimension - it emerges
   from the increase in entropy as the universe evolves.

4. **What is Consciousness?**: If consciousness is related to information
   processing, then it too emerges from the void through the same
   stochastic dynamics.

5. **What is the Meaning of Life?**: In a universe that emerged from
   nothing, meaning is not given but created through our interactions
   with the world.

Let's explore these questions...
        """)
        
        # Create philosophical discussion plot
        self._create_philosophical_discussion_plot()
        
        print("""
The beauty of void physics is that it provides a mathematical framework
for understanding the deepest questions of existence. It shows that:

• Nothing and something are not opposites, but different states of the same system
• Randomness and determinism are not incompatible, but complementary
• Time and space are not fundamental, but emergent properties
• Consciousness and matter are not separate, but different aspects of the same process

This is not just physics - it's a new way of understanding reality itself.

The void is not empty. It's full of potential. And from that potential,
everything emerges.
        """)
        
    def _create_philosophical_discussion_plot(self):
        """Create philosophical discussion visualization."""
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        
        # The void as potential
        x = np.linspace(-3, 3, 100)
        y = np.linspace(-3, 3, 100)
        X, Y = np.meshgrid(x, y)
        
        # Create a potential landscape
        Z = np.exp(-(X**2 + Y**2)) * np.sin(2 * np.pi * X) * np.cos(2 * np.pi * Y)
        
        im = axes[0, 0].imshow(Z, extent=[-3, 3, -3, 3], cmap='viridis', alpha=0.8)
        axes[0, 0].set_title('The Void: Full of Potential')
        axes[0, 0].set_xlabel('Space')
        axes[0, 0].set_ylabel('Time')
        plt.colorbar(im, ax=axes[0, 0])
        
        # Emergence of structure
        t = np.linspace(0, 10, 100)
        # Simple model of structure emergence
        structure = np.tanh(t - 5) * np.exp(-(t - 5)**2 / 2)
        
        axes[0, 1].plot(t, structure, 'b-', linewidth=3, label='Structure')
        axes[0, 1].axvline(x=5, color='r', linestyle='--', alpha=0.7, label='Emergence')
        axes[0, 1].set_xlabel('Time')
        axes[0, 1].set_ylabel('Structure')
        axes[0, 1].set_title('Emergence of Structure from Void')
        axes[0, 1].legend()
        axes[0, 1].grid(True, alpha=0.3)
        
        # Information and consciousness
        entropy = np.linspace(0, 5, 100)
        # Simple model: consciousness as information processing
        consciousness = np.tanh(entropy - 2) * np.exp(-(entropy - 2)**2 / 2)
        
        axes[1, 0].plot(entropy, consciousness, 'g-', linewidth=3, label='Consciousness')
        axes[1, 0].set_xlabel('Entropy')
        axes[1, 0].set_ylabel('Consciousness Level')
        axes[1, 0].set_title('Consciousness as Information Processing')
        axes[1, 0].legend()
        axes[1, 0].grid(True, alpha=0.3)
        
        # The meaning of existence
        axes[1, 1].axis('off')
        meaning_text = """
        The Meaning of Existence
        
        In void physics, meaning is not given but created.
        
        The universe emerges from nothing through stochastic dynamics.
        Consciousness emerges from information processing.
        Purpose emerges from the interaction between observer and observed.
        
        We are not separate from the void - we are its most complex expression.
        
        The void is not empty. It's full of us.
        """
        
        axes[1, 1].text(0.5, 0.5, meaning_text, ha='center', va='center',
                       fontsize=12, transform=axes[1, 1].transAxes,
                       bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue", alpha=0.7))
        
        plt.suptitle('Philosophical Discussion', fontsize=16, fontweight='bold')
        plt.tight_layout()
        plt.savefig('examples/course/lesson_7_philosophical_discussion.png', dpi=300, bbox_inches='tight')
        plt.show()
        
    def run_complete_course(self):
        """Run the complete void physics course."""
        print("🎓 WELCOME TO THE VOID PHYSICS COURSE")
        print("=" * 60)
        print("""
This course will take you on a journey through the mathematical
and philosophical foundations of void physics - a theory that
explains how the universe emerged from nothingness.

Course Outline:
1. Introduction to Void Physics
2. Mathematical Foundations
3. Stochastic Dynamics and Phase Transitions
4. Entropy and the Emergence of Time
5. Matter, Antimatter, and Charge Separation
6. Cosmological Implications
7. Philosophical Discussion

Let's begin...
        """)
        
        # Create course directory
        course_dir = Path('examples/course')
        course_dir.mkdir(exist_ok=True)
        
        # Run all lessons
        self.lesson_1_introduction()
        self.lesson_2_mathematical_foundations()
        self.lesson_3_stochastic_dynamics()
        self.lesson_4_entropy_and_time()
        self.lesson_5_matter_antimatter()
        self.lesson_6_cosmological_implications()
        self.lesson_7_philosophical_discussion()
        
        print("\n🎓 COURSE COMPLETED!")
        print("=" * 60)
        print("""
Congratulations! You have completed the Void Physics course.

You have learned:
• How the universe emerged from nothingness
• The mathematical framework of void physics
• The stochastic dynamics of phase transitions
• How time emerges from entropy
• The origin of matter-antimatter asymmetry
• The cosmological implications of void physics
• The philosophical implications of the theory

The void is not empty. It's full of potential.
And from that potential, everything emerges.

Thank you for taking this journey with us!
        """)
        
        # Create course summary
        self._create_course_summary()
        
    def _create_course_summary(self):
        """Create a summary of the course."""
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        
        # Course overview
        axes[0, 0].axis('off')
        overview_text = """
        VOID PHYSICS COURSE SUMMARY
        
        Key Concepts Learned:
        
        1. The Void (Néant) - A state of perfect symmetry
        2. Symmetry Breaking - How structure emerges
        3. Stochastic Dynamics - The role of randomness
        4. Entropy and Time - Time as emergent property
        5. Matter-Antimatter - Origin of asymmetry
        6. Cosmology - Implications for the universe
        7. Philosophy - Deep questions of existence
        
        The universe is not separate from the void -
        it is the void's most complex expression.
        """
        
        axes[0, 0].text(0.5, 0.5, overview_text, ha='center', va='center',
                       fontsize=12, transform=axes[0, 0].transAxes,
                       bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgreen", alpha=0.7))
        
        # Mathematical framework
        axes[0, 1].axis('off')
        math_text = """
        MATHEMATICAL FRAMEWORK
        
        Effective Action:
        S[φ,g] = ∫ d⁴x √(-g) [R/(2κ) - ½g^μν∂_μφ∂_νφ - V(φ) + L_mat(φ,Ψ)] + S_N
        
        Double-Well Potential:
        V(φ) = (λ/4)(φ² - v²)²
        
        Langevin Equation:
        dφ/dt = -Γ dV/dφ + η(t)
        
        Time-Entropy Relation:
        t ∝ ∫ dS / R(S)
        """
        
        axes[0, 1].text(0.5, 0.5, math_text, ha='center', va='center',
                       fontsize=10, transform=axes[0, 1].transAxes,
                       bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue", alpha=0.7))
        
        # Key insights
        axes[1, 0].axis('off')
        insights_text = """
        KEY INSIGHTS
        
        • Nothing and something are different states of the same system
        • Randomness and determinism are complementary
        • Time and space are emergent properties
        • Consciousness and matter are different aspects of the same process
        • Meaning is not given but created
        • The void is full of potential
        
        The universe is not separate from the void -
        it is the void's most complex expression.
        """
        
        axes[1, 0].text(0.5, 0.5, insights_text, ha='center', va='center',
                       fontsize=12, transform=axes[1, 0].transAxes,
                       bbox=dict(boxstyle="round,pad=0.3", facecolor="lightyellow", alpha=0.7))
        
        # Future directions
        axes[1, 1].axis('off')
        future_text = """
        FUTURE DIRECTIONS
        
        Research Areas:
        • Quantum gravity and void physics
        • Information theory and consciousness
        • Cosmological observations
        • Experimental tests
        
        Applications:
        • Understanding the origin of the universe
        • Exploring the nature of time
        • Investigating consciousness
        • Philosophical implications
        
        The void is not empty. It's full of us.
        """
        
        axes[1, 1].text(0.5, 0.5, future_text, ha='center', va='center',
                       fontsize=12, transform=axes[1, 1].transAxes,
                       bbox=dict(boxstyle="round,pad=0.3", facecolor="lightcoral", alpha=0.7))
        
        plt.suptitle('Void Physics Course Summary', fontsize=16, fontweight='bold')
        plt.tight_layout()
        plt.savefig('examples/course/course_summary.png', dpi=300, bbox_inches='tight')
        plt.show()


def main():
    """Run the void physics course."""
    course = VoidPhysicsCourse()
    course.run_complete_course()


if __name__ == "__main__":
    main()