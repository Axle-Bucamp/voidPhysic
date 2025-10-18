#!/usr/bin/env python3
"""
Beautiful 3D Visualizations for Void Physics
============================================

This module creates stunning 3D visualizations to showcase the void physics hypothesis.
It includes interactive plots, animations, and publication-quality figures.

Features:
- 3D potential landscapes with trajectories
- Interactive field evolution
- Phase space visualizations
- Entropy landscapes
- Multiverse representations
- Animated transitions
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.animation as animation
from matplotlib.colors import LinearSegmentedColormap
import seaborn as sns
from scipy import interpolate
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
from pathlib import Path

# Import our void physics modules
from void_physic.core.potential import DoubleWellPotential, PotentialParameters
from void_physic.core.stochastic import LangevinDynamics, WhiteNoise
from void_physic.simulation.langevin_solver import LangevinSolver, SolverParameters
from void_physic.simulation.statistics import EntropyCalculator

# Set up beautiful plotting
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

class Beautiful3DVisualizer:
    """Create beautiful 3D visualizations for void physics."""
    
    def __init__(self):
        """Initialize the visualizer."""
        self.setup_parameters()
        self.setup_components()
        self.setup_colors()
        
    def setup_parameters(self):
        """Set up parameters for visualization."""
        # Physical parameters
        self.lambda_coupling = 1.0
        self.v_vev = 1.0
        self.gamma_friction = 1.0
        self.noise_strength = 0.5
        
        # Visualization parameters
        self.resolution = 100
        self.n_trajectories = 500
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
        self.entropy_calc = EntropyCalculator()
        
    def setup_colors(self):
        """Set up beautiful color schemes."""
        # Custom colormaps
        self.void_colors = LinearSegmentedColormap.from_list(
            'void', ['#1a1a2e', '#16213e', '#0f3460', '#533483', '#7209b7']
        )
        
        self.entropy_colors = LinearSegmentedColormap.from_list(
            'entropy', ['#2d1b69', '#11998e', '#38ef7d', '#f093fb', '#f5576c']
        )
        
        self.phase_colors = LinearSegmentedColormap.from_list(
            'phase', ['#667eea', '#764ba2', '#f093fb', '#f5576c', '#4facfe']
        )
        
        # Color palettes
        self.void_palette = ['#1a1a2e', '#16213e', '#0f3460', '#533483', '#7209b7', '#e94560']
        self.entropy_palette = ['#2d1b69', '#11998e', '#38ef7d', '#f093fb', '#f5576c']
        self.phase_palette = ['#667eea', '#764ba2', '#f093fb', '#f5576c', '#4facfe']
        
    def create_3d_potential_landscape(self, save_path=None):
        """Create a stunning 3D potential landscape."""
        print("🎨 Creating 3D potential landscape...")
        
        # Create high-resolution grid
        phi = np.linspace(-2.5, 2.5, self.resolution)
        V = self.potential(phi)
        
        # Create 3D surface
        fig = plt.figure(figsize=(16, 12))
        ax = fig.add_subplot(111, projection='3d')
        
        # Create meshgrid for 3D surface
        phi_grid, V_grid = np.meshgrid(phi, V)
        z_grid = np.zeros_like(phi_grid)
        
        # Plot potential surface with beautiful colors
        surf = ax.plot_surface(phi_grid, V_grid, z_grid, 
                              cmap=self.void_colors, alpha=0.8, 
                              linewidth=0, antialiased=True)
        
        # Add contour lines
        contour = ax.contour(phi_grid, V_grid, z_grid, 
                           levels=20, colors='white', alpha=0.3, linewidths=0.5)
        
        # Mark critical points
        critical_points = self.potential.critical_points()
        for name, phi_val in critical_points.items():
            V_val = self.potential(np.array([phi_val]))[0]
            color = '#e94560' if name == 'symmetric' else '#38ef7d'
            ax.scatter([phi_val], [V_val], [0], 
                      c=color, s=200, alpha=0.9, edgecolors='white', linewidth=2)
            
            # Add labels
            ax.text(phi_val, V_val, 0.1, f'{name}\nφ={phi_val:.1f}', 
                   fontsize=10, ha='center', va='bottom', 
                   bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))
        
        # Add trajectories
        ensemble_results = self.solver.ensemble_simulation(phi0=0.0)
        trajectories = ensemble_results['trajectories']
        t = ensemble_results['time']
        
        # Plot sample trajectories
        n_plot = min(20, trajectories.shape[0])
        for i in range(0, n_plot, 2):
            phi_traj = trajectories[i]
            V_traj = self.potential(phi_traj)
            ax.plot(phi_traj, V_traj, t, 
                   color=self.void_palette[i % len(self.void_palette)], 
                   alpha=0.7, linewidth=2)
        
        # Plot mean trajectory
        mean_phi = ensemble_results['mean_field']
        mean_V = self.potential(mean_phi)
        ax.plot(mean_phi, mean_V, t, 
               'white', linewidth=4, alpha=0.9, label='Mean Trajectory')
        
        # Customize appearance
        ax.set_xlabel('Scalar Field φ', fontsize=14, fontweight='bold')
        ax.set_ylabel('Potential V(φ)', fontsize=14, fontweight='bold')
        ax.set_zlabel('Time', fontsize=14, fontweight='bold')
        ax.set_title('3D Potential Landscape: Void to Structure', 
                    fontsize=16, fontweight='bold', pad=20)
        
        # Set viewing angle
        ax.view_init(elev=20, azim=45)
        
        # Add colorbar
        cbar = fig.colorbar(surf, ax=ax, shrink=0.5, aspect=20)
        cbar.set_label('Potential Energy', fontsize=12, fontweight='bold')
        
        # Add legend
        ax.legend(loc='upper left', bbox_to_anchor=(0, 1))
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight', 
                       facecolor='white', edgecolor='none')
            print(f"✅ Saved to: {save_path}")
        
        plt.show()
        
    def create_3d_phase_space(self, save_path=None):
        """Create a beautiful 3D phase space visualization."""
        print("🎨 Creating 3D phase space...")
        
        # Run simulation
        ensemble_results = self.solver.ensemble_simulation(phi0=0.0)
        trajectories = ensemble_results['trajectories']
        t = ensemble_results['time']
        
        # Create 3D plot
        fig = plt.figure(figsize=(16, 12))
        ax = fig.add_subplot(111, projection='3d')
        
        # Plot trajectories in phase space
        n_plot = min(50, trajectories.shape[0])
        colors = plt.cm.plasma(np.linspace(0, 1, n_plot))
        
        for i in range(0, n_plot, 2):
            phi = trajectories[i]
            dphi_dt = np.gradient(phi, t)
            d2phi_dt2 = np.gradient(dphi_dt, t)
            
            ax.plot(phi, dphi_dt, d2phi_dt2, 
                   color=colors[i//2], alpha=0.6, linewidth=1.5)
        
        # Plot mean trajectory
        mean_phi = ensemble_results['mean_field']
        mean_dphi_dt = np.gradient(mean_phi, t)
        mean_d2phi_dt2 = np.gradient(mean_dphi_dt, t)
        
        ax.plot(mean_phi, mean_dphi_dt, mean_d2phi_dt2, 
               'white', linewidth=4, alpha=0.9, label='Mean Trajectory')
        
        # Add attractors
        critical_points = self.potential.critical_points()
        for name, phi_val in critical_points.items():
            if name != 'symmetric':  # Only stable points
                ax.scatter([phi_val], [0], [0], 
                          c='#38ef7d', s=300, alpha=0.9, 
                          edgecolors='white', linewidth=2, label=f'{name} Attractor')
        
        # Customize appearance
        ax.set_xlabel('Field φ', fontsize=14, fontweight='bold')
        ax.set_ylabel('Velocity dφ/dt', fontsize=14, fontweight='bold')
        ax.set_zlabel('Acceleration d²φ/dt²', fontsize=14, fontweight='bold')
        ax.set_title('3D Phase Space: Dynamics in Void Physics', 
                    fontsize=16, fontweight='bold', pad=20)
        
        # Set viewing angle
        ax.view_init(elev=30, azim=60)
        
        # Add legend
        ax.legend(loc='upper left', bbox_to_anchor=(0, 1))
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight', 
                       facecolor='white', edgecolor='none')
            print(f"✅ Saved to: {save_path}")
        
        plt.show()
        
    def create_3d_entropy_landscape(self, save_path=None):
        """Create a stunning 3D entropy landscape."""
        print("🎨 Creating 3D entropy landscape...")
        
        # Run simulation
        ensemble_results = self.solver.ensemble_simulation(phi0=0.0)
        trajectories = ensemble_results['trajectories']
        t = ensemble_results['time']
        
        # Calculate entropy
        entropy_values = self.entropy_calc.field_entropy(trajectories, t)
        entropy_rate = self.entropy_calc.entropy_production_rate(entropy_values, t)
        
        # Create 3D plot
        fig = plt.figure(figsize=(16, 12))
        ax = fig.add_subplot(111, projection='3d')
        
        # Create entropy surface
        phi_range = np.linspace(-2, 2, 50)
        t_range = np.linspace(0, self.t_max, 50)
        
        # Calculate entropy for each point
        entropy_surface = np.zeros((len(t_range), len(phi_range)))
        
        for i, t_val in enumerate(t_range):
            for j, phi_val in enumerate(phi_range):
                # Approximate entropy based on field value and time
                entropy_surface[i, j] = 0.5 * np.log(1 + phi_val**2) + 0.2 * t_val
        
        # Create meshgrid
        phi_grid, t_grid = np.meshgrid(phi_range, t_range)
        
        # Plot entropy surface
        surf = ax.plot_surface(phi_grid, t_grid, entropy_surface, 
                              cmap=self.entropy_colors, alpha=0.7, 
                              linewidth=0, antialiased=True)
        
        # Add entropy trajectories
        for i in range(0, min(20, trajectories.shape[0]), 2):
            phi_traj = trajectories[i]
            entropy_traj = 0.5 * np.log(1 + phi_traj**2) + 0.2 * t
            ax.plot(phi_traj, t, entropy_traj, 
                   color=self.entropy_palette[i % len(self.entropy_palette)], 
                   alpha=0.8, linewidth=2)
        
        # Plot mean entropy trajectory
        mean_phi = ensemble_results['mean_field']
        mean_entropy = 0.5 * np.log(1 + mean_phi**2) + 0.2 * t
        ax.plot(mean_phi, t, mean_entropy, 
               'white', linewidth=4, alpha=0.9, label='Mean Entropy')
        
        # Add time arrow
        ax.quiver(0, self.t_max*0.8, 2, 0, 0, 0.5, 
                 color='red', arrow_length_ratio=0.1, linewidth=3, alpha=0.8)
        ax.text(0.2, self.t_max*0.8, 2.2, 'Time Arrow', 
               fontsize=12, color='red', fontweight='bold')
        
        # Customize appearance
        ax.set_xlabel('Field φ', fontsize=14, fontweight='bold')
        ax.set_ylabel('Time', fontsize=14, fontweight='bold')
        ax.set_zlabel('Entropy S', fontsize=14, fontweight='bold')
        ax.set_title('3D Entropy Landscape: Time Emerges from Disorder', 
                    fontsize=16, fontweight='bold', pad=20)
        
        # Set viewing angle
        ax.view_init(elev=25, azim=45)
        
        # Add colorbar
        cbar = fig.colorbar(surf, ax=ax, shrink=0.5, aspect=20)
        cbar.set_label('Entropy', fontsize=12, fontweight='bold')
        
        # Add legend
        ax.legend(loc='upper left', bbox_to_anchor=(0, 1))
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight', 
                       facecolor='white', edgecolor='none')
            print(f"✅ Saved to: {save_path}")
        
        plt.show()
        
    def create_3d_multiverse(self, save_path=None):
        """Create a beautiful 3D multiverse visualization."""
        print("🎨 Creating 3D multiverse...")
        
        # Create 3D plot
        fig = plt.figure(figsize=(16, 12))
        ax = fig.add_subplot(111, projection='3d')
        
        # Create multiple universe bubbles
        n_universes = 15
        colors = plt.cm.Set3(np.linspace(0, 1, n_universes))
        
        for i in range(n_universes):
            # Random position and size
            x = np.random.uniform(-8, 8)
            y = np.random.uniform(-8, 8)
            z = np.random.uniform(-8, 8)
            r = np.random.uniform(0.8, 2.0)
            
            # Create sphere
            u = np.linspace(0, 2 * np.pi, 30)
            v = np.linspace(0, np.pi, 30)
            x_sphere = x + r * np.outer(np.cos(u), np.sin(v))
            y_sphere = y + r * np.outer(np.sin(u), np.sin(v))
            z_sphere = z + r * np.outer(np.ones(np.size(u)), np.cos(v))
            
            # Plot universe bubble
            ax.plot_surface(x_sphere, y_sphere, z_sphere, 
                           alpha=0.4, color=colors[i], linewidth=0)
            
            # Add universe label
            ax.text(x, y, z + r + 0.5, f'Universe {i+1}', 
                   fontsize=8, ha='center', va='bottom',
                   bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.8))
        
        # Add void at center
        void_u = np.linspace(0, 2 * np.pi, 30)
        void_v = np.linspace(0, np.pi, 30)
        void_x = 0.5 * np.outer(np.cos(void_u), np.sin(void_v))
        void_y = 0.5 * np.outer(np.sin(void_u), np.sin(void_v))
        void_z = 0.5 * np.outer(np.ones(np.size(void_u)), np.cos(void_v))
        
        ax.plot_surface(void_x, void_y, void_z, 
                       alpha=0.8, color='purple', linewidth=0)
        ax.text(0, 0, 1, 'THE VOID', 
               fontsize=14, ha='center', va='bottom', fontweight='bold',
               bbox=dict(boxstyle='round,pad=0.3', facecolor='purple', alpha=0.8, edgecolor='white'))
        
        # Add connection lines from void to universes
        for i in range(n_universes):
            x = np.random.uniform(-8, 8)
            y = np.random.uniform(-8, 8)
            z = np.random.uniform(-8, 8)
            ax.plot([0, x], [0, y], [0, z], 
                   'k--', alpha=0.3, linewidth=1)
        
        # Customize appearance
        ax.set_xlabel('Dimension 1', fontsize=14, fontweight='bold')
        ax.set_ylabel('Dimension 2', fontsize=14, fontweight='bold')
        ax.set_zlabel('Dimension 3', fontsize=14, fontweight='bold')
        ax.set_title('3D Multiverse: All Possible Realities', 
                    fontsize=16, fontweight='bold', pad=20)
        
        # Set viewing angle
        ax.view_init(elev=20, azim=45)
        
        # Set equal aspect ratio
        ax.set_xlim(-10, 10)
        ax.set_ylim(-10, 10)
        ax.set_zlim(-10, 10)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight', 
                       facecolor='white', edgecolor='none')
            print(f"✅ Saved to: {save_path}")
        
        plt.show()
        
    def create_animated_transition(self, save_path=None):
        """Create an animated transition from void to structure."""
        print("🎨 Creating animated transition...")
        
        # Run simulation
        ensemble_results = self.solver.ensemble_simulation(phi0=0.0)
        trajectories = ensemble_results['trajectories']
        t = ensemble_results['time']
        
        # Create figure
        fig = plt.figure(figsize=(12, 8))
        ax = fig.add_subplot(111, projection='3d')
        
        # Initialize plot elements
        lines = []
        for i in range(min(10, trajectories.shape[0])):
            line, = ax.plot([], [], [], 
                           color=self.void_palette[i % len(self.void_palette)], 
                           alpha=0.7, linewidth=2)
            lines.append(line)
        
        # Mean trajectory line
        mean_line, = ax.plot([], [], [], 'white', linewidth=4, alpha=0.9)
        
        # Set up the plot
        ax.set_xlim(-2, 2)
        ax.set_ylim(-2, 2)
        ax.set_zlim(0, self.t_max)
        ax.set_xlabel('Field φ', fontsize=12, fontweight='bold')
        ax.set_ylabel('Potential V(φ)', fontsize=12, fontweight='bold')
        ax.set_zlabel('Time', fontsize=12, fontweight='bold')
        ax.set_title('Animated Transition: Void to Structure', 
                    fontsize=14, fontweight='bold')
        
        # Add potential surface
        phi = np.linspace(-2, 2, 50)
        V = self.potential(phi)
        phi_grid, V_grid = np.meshgrid(phi, V)
        z_grid = np.zeros_like(phi_grid)
        
        ax.plot_surface(phi_grid, V_grid, z_grid, 
                       cmap=self.void_colors, alpha=0.3, linewidth=0)
        
        def animate(frame):
            """Animation function."""
            # Update trajectories
            for i, line in enumerate(lines):
                phi_traj = trajectories[i, :frame+1]
                V_traj = self.potential(phi_traj)
                t_traj = t[:frame+1]
                line.set_data_3d(phi_traj, V_traj, t_traj)
            
            # Update mean trajectory
            mean_phi = np.mean(trajectories[:min(10, trajectories.shape[0]), :frame+1], axis=0)
            mean_V = self.potential(mean_phi)
            mean_line.set_data_3d(mean_phi, mean_V, t[:frame+1])
            
            return lines + [mean_line]
        
        # Create animation
        anim = animation.FuncAnimation(fig, animate, frames=len(t), 
                                     interval=50, blit=True, repeat=True)
        
        if save_path:
            anim.save(save_path, writer='pillow', fps=20)
            print(f"✅ Saved to: {save_path}")
        
        plt.show()
        
    def create_interactive_plotly(self, save_path=None):
        """Create interactive Plotly visualizations."""
        print("🎨 Creating interactive Plotly visualizations...")
        
        # Run simulation
        ensemble_results = self.solver.ensemble_simulation(phi0=0.0)
        trajectories = ensemble_results['trajectories']
        t = ensemble_results['time']
        
        # Create subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('3D Trajectories', 'Phase Space', 'Entropy Evolution', 'Field Distribution'),
            specs=[[{'type': 'scatter3d'}, {'type': 'scatter3d'}],
                   [{'type': 'scatter'}, {'type': 'histogram'}]]
        )
        
        # 3D Trajectories
        for i in range(0, min(20, trajectories.shape[0]), 2):
            phi = trajectories[i]
            V = self.potential(phi)
            fig.add_trace(
                go.Scatter3d(
                    x=phi, y=V, z=t,
                    mode='lines',
                    line=dict(color=px.colors.qualitative.Set3[i % len(px.colors.qualitative.Set3)]),
                    name=f'Trajectory {i+1}',
                    showlegend=False
                ),
                row=1, col=1
            )
        
        # Phase Space
        for i in range(0, min(20, trajectories.shape[0]), 2):
            phi = trajectories[i]
            dphi_dt = np.gradient(phi, t)
            d2phi_dt2 = np.gradient(dphi_dt, t)
            fig.add_trace(
                go.Scatter3d(
                    x=phi, y=dphi_dt, z=d2phi_dt2,
                    mode='lines',
                    line=dict(color=px.colors.qualitative.Set3[i % len(px.colors.qualitative.Set3)]),
                    name=f'Phase {i+1}',
                    showlegend=False
                ),
                row=1, col=2
            )
        
        # Entropy Evolution
        entropy_values = self.entropy_calc.field_entropy(trajectories, t)
        fig.add_trace(
            go.Scatter(
                x=t, y=entropy_values,
                mode='lines',
                line=dict(color='green', width=3),
                name='Entropy'
            ),
            row=2, col=1
        )
        
        # Field Distribution
        final_field_values = trajectories[:, -1]
        fig.add_trace(
            go.Histogram(
                x=final_field_values,
                nbinsx=30,
                name='Field Distribution',
                marker_color='blue'
            ),
            row=2, col=2
        )
        
        # Update layout
        fig.update_layout(
            title_text="Interactive Void Physics Visualization",
            title_x=0.5,
            height=800,
            showlegend=False
        )
        
        # Update axes labels
        fig.update_xaxes(title_text="Field φ", row=1, col=1)
        fig.update_yaxes(title_text="Potential V(φ)", row=1, col=1)
        fig.update_zaxes(title_text="Time", row=1, col=1)
        
        fig.update_xaxes(title_text="Field φ", row=1, col=2)
        fig.update_yaxes(title_text="Velocity dφ/dt", row=1, col=2)
        fig.update_zaxes(title_text="Acceleration d²φ/dt²", row=1, col=2)
        
        fig.update_xaxes(title_text="Time", row=2, col=1)
        fig.update_yaxes(title_text="Entropy", row=2, col=1)
        
        fig.update_xaxes(title_text="Field Value", row=2, col=2)
        fig.update_yaxes(title_text="Count", row=2, col=2)
        
        if save_path:
            fig.write_html(save_path)
            print(f"✅ Saved to: {save_path}")
        
        fig.show()
        
    def create_all_visualizations(self, output_dir='examples/3d_visualizations'):
        """Create all 3D visualizations."""
        print("🎨 Creating all 3D visualizations...")
        
        # Create output directory
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        # Create all visualizations
        self.create_3d_potential_landscape(output_path / '3d_potential_landscape.png')
        self.create_3d_phase_space(output_path / '3d_phase_space.png')
        self.create_3d_entropy_landscape(output_path / '3d_entropy_landscape.png')
        self.create_3d_multiverse(output_path / '3d_multiverse.png')
        self.create_animated_transition(output_path / 'animated_transition.gif')
        self.create_interactive_plotly(output_path / 'interactive_visualization.html')
        
        print(f"✅ All visualizations saved to: {output_path}")


def main():
    """Run the beautiful 3D visualizer."""
    visualizer = Beautiful3DVisualizer()
    visualizer.create_all_visualizations()


if __name__ == "__main__":
    main()
