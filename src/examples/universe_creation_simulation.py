#!/usr/bin/env python3
"""
Universe Creation Simulation with Wave Collapse
===============================================

This simulation implements void physics rules for universe creation:
- 2D wave collapse with atom emergence
- Void interference patterns that test and expand atoms
- Topological connectivity without distance constraints
- Life game mechanics with aging and expansion
- Real-time dashboard with parameter control

The simulation follows the principle that the void (néant) generates
interference patterns that test atoms and cause them to expand
randomly where constraints allow, or age if not, creating real space t+1.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Circle
import seaborn as sns
import pandas as pd
from scipy import ndimage
from scipy.spatial.distance import cdist
try:
    import plotly.graph_objects as go
    import plotly.express as px
    from plotly.subplots import make_subplots
    import plotly.dash as dash
    from plotly.dash import dcc, html, Input, Output, State
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
import threading
import time
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Set up beautiful plotting
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

class Atom:
    """Represents an atom in the universe with void physics properties."""
    
    def __init__(self, x, y, energy=1.0, age=0, atom_type='matter'):
        self.x = x
        self.y = y
        self.energy = energy
        self.age = age
        self.atom_type = atom_type  # 'matter' or 'antimatter'
        self.stability = 1.0
        self.connections = []  # Topological connections to other atoms
        self.void_interference = 0.0  # Current void interference level
        self.expansion_potential = 0.0  # Potential for expansion
        
    def update(self, void_field, universe_grid, dt=1.0):
        """Update atom state based on void physics rules."""
        # Get void interference at this location
        self.void_interference = void_field[int(self.y), int(self.x)]
        
        # Age the atom
        self.age += dt
        
        # Calculate expansion potential based on void interference
        if self.void_interference > 0.5:  # Strong void interference
            self.expansion_potential += 0.1 * self.void_interference
        else:  # Weak void interference - atom ages
            self.stability -= 0.05 * (1 - self.void_interference)
            self.energy *= 0.99  # Energy decay
            
        # Check for expansion
        if self.expansion_potential > 1.0:
            self._attempt_expansion(universe_grid)
            self.expansion_potential = 0.0
            
        # Check for decay
        if self.stability < 0.1:
            self.energy = 0.0  # Atom decays
            
    def _attempt_expansion(self, universe_grid):
        """Attempt to expand the atom to adjacent locations."""
        # Find empty adjacent cells
        neighbors = self._get_empty_neighbors(universe_grid)
        
        if neighbors:
            # Choose random neighbor for expansion
            new_x, new_y = neighbors[np.random.randint(len(neighbors))]
            
            # Create new atom
            new_atom = Atom(new_x, new_y, 
                          energy=self.energy * 0.8,  # Energy conservation
                          age=0,
                          atom_type=self.atom_type)
            
            # Add to universe
            universe_grid[int(new_y), int(new_x)] = new_atom
            
            # Create topological connection
            self.connections.append(new_atom)
            new_atom.connections.append(self)
            
    def _get_empty_neighbors(self, universe_grid):
        """Get empty neighboring cells."""
        neighbors = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                    
                new_x = int(self.x + dx)
                new_y = int(self.y + dy)
                
                # Check bounds
                if (0 <= new_x < universe_grid.shape[1] and 
                    0 <= new_y < universe_grid.shape[0]):
                    
                    if universe_grid[new_y, new_x] is None:
                        neighbors.append((new_x, new_y))
                        
        return neighbors
        
    def get_color(self):
        """Get color based on atom properties."""
        if self.atom_type == 'matter':
            # Blue to red based on energy
            intensity = min(1.0, self.energy)
            return (intensity, 0.5, 1.0 - intensity)
        else:
            # Green to yellow based on energy
            intensity = min(1.0, self.energy)
            return (intensity, 1.0, 0.5)


class VoidField:
    """Represents the void field that generates interference patterns."""
    
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.field = np.zeros((height, width))
        self.time = 0.0
        self.interference_sources = []
        
    def add_interference_source(self, x, y, frequency, amplitude):
        """Add a source of void interference."""
        self.interference_sources.append({
            'x': x, 'y': y, 'frequency': frequency, 'amplitude': amplitude
        })
        
    def update(self, dt=1.0):
        """Update the void field with interference patterns."""
        self.time += dt
        self.field = np.zeros((self.height, self.width))
        
        # Generate interference patterns from sources
        for source in self.interference_sources:
            x, y = source['x'], source['y']
            freq = source['frequency']
            amp = source['amplitude']
            
            # Create wave pattern
            for i in range(self.height):
                for j in range(self.width):
                    distance = np.sqrt((i - y)**2 + (j - x)**2)
                    phase = 2 * np.pi * freq * self.time - distance * 0.1
                    self.field[i, j] += amp * np.sin(phase) / (1 + distance * 0.1)
                    
        # Add random void fluctuations
        self.field += np.random.normal(0, 0.1, (self.height, self.width))
        
        # Normalize
        self.field = np.tanh(self.field)  # Keep in [-1, 1]


class UniverseCreationSimulation:
    """Main simulation class for universe creation."""
    
    def __init__(self, width=100, height=100):
        self.width = width
        self.height = height
        self.universe_grid = np.full((height, width), None, dtype=object)
        self.void_field = VoidField(width, height)
        self.time = 0.0
        self.atoms = []
        self.history = []
        
        # Simulation parameters
        self.void_interference_strength = 1.0
        self.atom_creation_rate = 0.01
        self.expansion_probability = 0.1
        self.decay_rate = 0.001
        
        # Statistics
        self.stats = {
            'total_atoms': 0,
            'matter_atoms': 0,
            'antimatter_atoms': 0,
            'total_energy': 0.0,
            'average_age': 0.0,
            'expansion_events': 0,
            'decay_events': 0
        }
        
    def initialize_void_sources(self):
        """Initialize void interference sources."""
        # Add random void sources
        n_sources = 5
        for _ in range(n_sources):
            x = np.random.uniform(0, self.width)
            y = np.random.uniform(0, self.height)
            freq = np.random.uniform(0.1, 0.5)
            amp = np.random.uniform(0.5, 1.5)
            self.void_field.add_interference_source(x, y, freq, amp)
            
    def create_initial_atoms(self, n_atoms=10):
        """Create initial atoms in the universe."""
        for _ in range(n_atoms):
            # Random position
            x = np.random.uniform(0, self.width)
            y = np.random.uniform(0, self.height)
            
            # Random type (matter or antimatter)
            atom_type = 'matter' if np.random.random() > 0.5 else 'antimatter'
            
            # Create atom
            atom = Atom(x, y, energy=1.0, age=0, atom_type=atom_type)
            
            # Add to universe
            self.universe_grid[int(y), int(x)] = atom
            self.atoms.append(atom)
            
    def update(self, dt=1.0):
        """Update the simulation."""
        self.time += dt
        
        # Update void field
        self.void_field.update(dt)
        
        # Update all atoms
        atoms_to_remove = []
        for atom in self.atoms:
            if atom.energy > 0:
                atom.update(self.void_field.field, self.universe_grid, dt)
                
                # Check for decay
                if atom.energy <= 0:
                    atoms_to_remove.append(atom)
                    self.universe_grid[int(atom.y), int(atom.x)] = None
                    self.stats['decay_events'] += 1
                    
        # Remove decayed atoms
        for atom in atoms_to_remove:
            self.atoms.remove(atom)
            
        # Create new atoms based on void interference
        if np.random.random() < self.atom_creation_rate:
            self._create_new_atom()
            
        # Update statistics
        self._update_statistics()
        
        # Store history
        self.history.append({
            'time': self.time,
            'n_atoms': len(self.atoms),
            'total_energy': sum(atom.energy for atom in self.atoms),
            'void_activity': np.mean(np.abs(self.void_field.field))
        })
        
    def _create_new_atom(self):
        """Create a new atom based on void interference."""
        # Find location with high void interference
        high_interference = self.void_field.field > 0.7
        
        if np.any(high_interference):
            # Choose random high-interference location
            y_coords, x_coords = np.where(high_interference)
            idx = np.random.randint(len(x_coords))
            x, y = x_coords[idx], y_coords[idx]
            
            # Check if location is empty
            if self.universe_grid[y, x] is None:
                # Random type
                atom_type = 'matter' if np.random.random() > 0.5 else 'antimatter'
                
                # Create atom
                atom = Atom(x, y, energy=1.0, age=0, atom_type=atom_type)
                
                # Add to universe
                self.universe_grid[y, x] = atom
                self.atoms.append(atom)
                self.stats['total_atoms'] += 1
                
    def _update_statistics(self):
        """Update simulation statistics."""
        if self.atoms:
            self.stats['matter_atoms'] = sum(1 for atom in self.atoms if atom.atom_type == 'matter')
            self.stats['antimatter_atoms'] = sum(1 for atom in self.atoms if atom.atom_type == 'antimatter')
            self.stats['total_energy'] = sum(atom.energy for atom in self.atoms)
            self.stats['average_age'] = np.mean([atom.age for atom in self.atoms])
        else:
            self.stats['matter_atoms'] = 0
            self.stats['antimatter_atoms'] = 0
            self.stats['total_energy'] = 0.0
            self.stats['average_age'] = 0.0
            
    def get_universe_image(self):
        """Get image representation of the universe."""
        image = np.zeros((self.height, self.width, 3))
        
        # Draw atoms
        for atom in self.atoms:
            if atom.energy > 0:
                color = np.array(atom.get_color())  # Convert to numpy array
                y, x = int(atom.y), int(atom.x)
                if 0 <= y < self.height and 0 <= x < self.width:
                    image[y, x] = color
                    
        # Add void field overlay
        void_overlay = np.abs(self.void_field.field)
        void_overlay = np.stack([void_overlay, void_overlay, void_overlay], axis=2)
        image = image + void_overlay * 0.3
        
        return np.clip(image, 0, 1)
        
    def get_void_field_image(self):
        """Get image representation of the void field."""
        field = self.void_field.field
        # Normalize to [0, 1]
        field = (field + 1) / 2
        return field


class UniverseCreationVisualizer:
    """Visualizer for the universe creation simulation."""
    
    def __init__(self, simulation):
        self.simulation = simulation
        self.fig = None
        self.axes = None
        
    def create_visualization(self):
        """Create the main visualization."""
        self.fig, self.axes = plt.subplots(2, 2, figsize=(16, 12))
        
        # Universe view
        self.axes[0, 0].set_title('Universe Creation')
        self.axes[0, 0].set_xlabel('X')
        self.axes[0, 0].set_ylabel('Y')
        
        # Void field
        self.axes[0, 1].set_title('Void Interference Field')
        self.axes[0, 1].set_xlabel('X')
        self.axes[0, 1].set_ylabel('Y')
        
        # Statistics
        self.axes[1, 0].set_title('Atom Statistics')
        self.axes[1, 0].set_xlabel('Time')
        self.axes[1, 0].set_ylabel('Count')
        
        # Energy evolution
        self.axes[1, 1].set_title('Energy Evolution')
        self.axes[1, 1].set_xlabel('Time')
        self.axes[1, 1].set_ylabel('Total Energy')
        
        plt.tight_layout()
        
    def update_visualization(self):
        """Update the visualization."""
        if self.fig is None:
            self.create_visualization()
            
        # Clear axes
        for ax in self.axes.flat:
            ax.clear()
            
        # Universe view
        universe_image = self.simulation.get_universe_image()
        self.axes[0, 0].imshow(universe_image, origin='lower', extent=[0, self.simulation.width, 0, self.simulation.height])
        self.axes[0, 0].set_title(f'Universe Creation (t={self.simulation.time:.1f})')
        self.axes[0, 0].set_xlabel('X')
        self.axes[0, 0].set_ylabel('Y')
        
        # Void field
        void_image = self.simulation.get_void_field_image()
        im = self.axes[0, 1].imshow(void_image, origin='lower', extent=[0, self.simulation.width, 0, self.simulation.height], cmap='RdBu_r')
        self.axes[0, 1].set_title('Void Interference Field')
        self.axes[0, 1].set_xlabel('X')
        self.axes[0, 1].set_ylabel('Y')
        plt.colorbar(im, ax=self.axes[0, 1])
        
        # Statistics
        if self.simulation.history:
            history_df = pd.DataFrame(self.simulation.history)
            self.axes[1, 0].plot(history_df['time'], history_df['n_atoms'], 'b-', label='Total Atoms')
            self.axes[1, 0].set_xlabel('Time')
            self.axes[1, 0].set_ylabel('Count')
            self.axes[1, 0].set_title('Atom Statistics')
            self.axes[1, 0].legend()
            self.axes[1, 0].grid(True, alpha=0.3)
            
        # Energy evolution
        if self.simulation.history:
            self.axes[1, 1].plot(history_df['time'], history_df['total_energy'], 'r-', label='Total Energy')
            self.axes[1, 1].set_xlabel('Time')
            self.axes[1, 1].set_ylabel('Total Energy')
            self.axes[1, 1].set_title('Energy Evolution')
            self.axes[1, 1].legend()
            self.axes[1, 1].grid(True, alpha=0.3)
            
        plt.tight_layout()
        plt.draw()
        
    def animate(self, n_frames=1000, interval=100):
        """Animate the simulation."""
        # Ensure figure is created
        if self.fig is None:
            self.create_visualization()
            
        def animate_frame(frame):
            self.simulation.update(dt=0.1)
            self.update_visualization()
            return []
            
        anim = animation.FuncAnimation(self.fig, animate_frame, frames=n_frames, 
                                     interval=interval, blit=False, repeat=True)
        return anim


class UniverseCreationDashboard:
    """Interactive dashboard for the universe creation simulation."""
    
    def __init__(self, simulation):
        self.simulation = simulation
        self.app = dash.Dash(__name__)
        self.setup_layout()
        self.setup_callbacks()
        
    def setup_layout(self):
        """Setup the dashboard layout."""
        self.app.layout = html.Div([
            html.H1("Universe Creation Simulation - Void Physics Dashboard", 
                   style={'textAlign': 'center', 'color': 'white', 'backgroundColor': '#1a1a2e'}),
            
            html.Div([
                # Control panel
                html.Div([
                    html.H3("Simulation Controls", style={'color': 'white'}),
                    
                    html.Label("Void Interference Strength:"),
                    dcc.Slider(
                        id='void-strength-slider',
                        min=0.1, max=2.0, step=0.1, value=1.0,
                        marks={i/10: str(i/10) for i in range(1, 21, 2)}
                    ),
                    
                    html.Label("Atom Creation Rate:"),
                    dcc.Slider(
                        id='creation-rate-slider',
                        min=0.001, max=0.1, step=0.001, value=0.01,
                        marks={i/1000: str(i/1000) for i in range(1, 101, 10)}
                    ),
                    
                    html.Label("Expansion Probability:"),
                    dcc.Slider(
                        id='expansion-prob-slider',
                        min=0.01, max=0.5, step=0.01, value=0.1,
                        marks={i/100: str(i/100) for i in range(1, 51, 5)}
                    ),
                    
                    html.Label("Decay Rate:"),
                    dcc.Slider(
                        id='decay-rate-slider',
                        min=0.0001, max=0.01, step=0.0001, value=0.001,
                        marks={i/10000: str(i/10000) for i in range(1, 101, 10)}
                    ),
                    
                    html.Button('Reset Simulation', id='reset-button', n_clicks=0),
                    html.Button('Pause/Resume', id='pause-button', n_clicks=0),
                    
                ], style={'width': '25%', 'display': 'inline-block', 'verticalAlign': 'top',
                         'backgroundColor': '#16213e', 'padding': '20px', 'margin': '10px',
                         'borderRadius': '10px'}),
                
                # Main visualization
                html.Div([
                    dcc.Graph(id='universe-plot'),
                    dcc.Interval(
                        id='interval-component',
                        interval=100,  # Update every 100ms
                        n_intervals=0
                    )
                ], style={'width': '70%', 'display': 'inline-block', 'verticalAlign': 'top'})
                
            ], style={'display': 'flex'}),
            
            # Statistics panel
            html.Div([
                html.Div([
                    html.H3("Real-time Statistics", style={'color': 'white'}),
                    html.Div(id='stats-display')
                ], style={'width': '50%', 'display': 'inline-block', 'verticalAlign': 'top',
                         'backgroundColor': '#0f3460', 'padding': '20px', 'margin': '10px',
                         'borderRadius': '10px'}),
                
                html.Div([
                    html.H3("Void Field Analysis", style={'color': 'white'}),
                    dcc.Graph(id='void-field-plot')
                ], style={'width': '45%', 'display': 'inline-block', 'verticalAlign': 'top',
                         'backgroundColor': '#533483', 'padding': '20px', 'margin': '10px',
                         'borderRadius': '10px'})
                
            ], style={'display': 'flex'}),
            
            # History plots
            html.Div([
                html.Div([
                    html.H3("Evolution History", style={'color': 'white'}),
                    dcc.Graph(id='history-plot')
                ], style={'width': '100%', 'backgroundColor': '#7209b7', 'padding': '20px',
                         'margin': '10px', 'borderRadius': '10px'})
            ])
            
        ], style={'backgroundColor': '#1a1a2e', 'color': 'white', 'fontFamily': 'Arial'})
        
    def setup_callbacks(self):
        """Setup dashboard callbacks."""
        
        @self.app.callback(
            [Output('universe-plot', 'figure'),
             Output('void-field-plot', 'figure'),
             Output('history-plot', 'figure'),
             Output('stats-display', 'children')],
            [Input('interval-component', 'n_intervals'),
             Input('void-strength-slider', 'value'),
             Input('creation-rate-slider', 'value'),
             Input('expansion-prob-slider', 'value'),
             Input('decay-rate-slider', 'value'),
             Input('reset-button', 'n_clicks')]
        )
        def update_dashboard(n_intervals, void_strength, creation_rate, 
                           expansion_prob, decay_rate, reset_clicks):
            
            # Update simulation parameters
            self.simulation.void_interference_strength = void_strength
            self.simulation.atom_creation_rate = creation_rate
            self.simulation.expansion_probability = expansion_prob
            self.simulation.decay_rate = decay_rate
            
            # Reset if button clicked
            if reset_clicks > 0:
                self.simulation = UniverseCreationSimulation(self.simulation.width, self.simulation.height)
                self.simulation.initialize_void_sources()
                self.simulation.create_initial_atoms()
            
            # Update simulation
            self.simulation.update(dt=0.1)
            
            # Create universe plot
            universe_fig = go.Figure()
            universe_image = self.simulation.get_universe_image()
            
            universe_fig.add_trace(go.Image(z=universe_image, 
                                          colorscale='Viridis',
                                          showscale=False))
            
            universe_fig.update_layout(
                title=f"Universe Creation (t={self.simulation.time:.1f})",
                xaxis_title="X",
                yaxis_title="Y",
                width=600,
                height=400
            )
            
            # Create void field plot
            void_fig = go.Figure()
            void_image = self.simulation.get_void_field_image()
            
            void_fig.add_trace(go.Heatmap(z=void_image, 
                                        colorscale='RdBu_r',
                                        showscale=True))
            
            void_fig.update_layout(
                title="Void Interference Field",
                xaxis_title="X",
                yaxis_title="Y",
                width=500,
                height=400
            )
            
            # Create history plot
            history_fig = go.Figure()
            
            if self.simulation.history:
                history_df = pd.DataFrame(self.simulation.history)
                
                history_fig.add_trace(go.Scatter(
                    x=history_df['time'],
                    y=history_df['n_atoms'],
                    mode='lines',
                    name='Total Atoms',
                    line=dict(color='blue', width=2)
                ))
                
                history_fig.add_trace(go.Scatter(
                    x=history_df['time'],
                    y=history_df['total_energy'],
                    mode='lines',
                    name='Total Energy',
                    yaxis='y2',
                    line=dict(color='red', width=2)
                ))
                
                history_fig.update_layout(
                    title="Evolution History",
                    xaxis_title="Time",
                    yaxis_title="Number of Atoms",
                    yaxis2=dict(title="Total Energy", overlaying="y", side="right"),
                    width=1000,
                    height=300
                )
            
            # Create statistics display
            stats_text = f"""
            **Current Statistics:**
            - Total Atoms: {self.simulation.stats['total_atoms']}
            - Matter Atoms: {self.simulation.stats['matter_atoms']}
            - Antimatter Atoms: {self.simulation.stats['antimatter_atoms']}
            - Total Energy: {self.simulation.stats['total_energy']:.2f}
            - Average Age: {self.simulation.stats['average_age']:.2f}
            - Expansion Events: {self.simulation.stats['expansion_events']}
            - Decay Events: {self.simulation.stats['decay_events']}
            - Void Activity: {np.mean(np.abs(self.simulation.void_field.field)):.3f}
            """
            
            return universe_fig, void_fig, history_fig, stats_text
            
    def run(self, debug=False, port=8050):
        """Run the dashboard."""
        self.app.run_server(debug=debug, port=port)


def main():
    """Run the universe creation simulation."""
    print("🌌 Starting Universe Creation Simulation...")
    
    # Create simulation
    simulation = UniverseCreationSimulation(width=80, height=80)
    simulation.initialize_void_sources()
    simulation.create_initial_atoms(n_atoms=5)
    
    # Create visualizer
    visualizer = UniverseCreationVisualizer(simulation)
    
    # Run animation
    print("🎬 Starting animation...")
    anim = visualizer.animate(n_frames=1000, interval=100)
    
    # Save animation
    print("💾 Saving animation...")
    anim.save('examples/universe_creation_animation.gif', writer='pillow', fps=10)
    
    # Create dashboard
    print("📊 Creating interactive dashboard...")
    dashboard = UniverseCreationDashboard(simulation)
    
    # Run dashboard
    print("🚀 Starting dashboard on http://localhost:8050")
    dashboard.run(debug=False, port=8050)


if __name__ == "__main__":
    main()
