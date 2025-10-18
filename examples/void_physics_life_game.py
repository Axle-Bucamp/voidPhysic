#!/usr/bin/env python3
"""
Void Physics Life Game
======================

An advanced cellular automaton that implements void physics rules:
- Void interference patterns test and expand atoms
- Topological connectivity without distance constraints
- Aging and expansion based on void field strength
- Real-time parameter control and visualization
- Statistical analysis and pattern recognition

The game follows the principle that the void (néant) generates
interference patterns that test atoms and cause them to expand
randomly where constraints allow, or age if not, creating real space t+1.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Circle, Rectangle
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

class VoidPhysicsCell:
    """A cell in the void physics life game."""
    
    def __init__(self, x, y, state='void', energy=0.0, age=0, cell_type='neutral'):
        self.x = x
        self.y = y
        self.state = state  # 'void', 'atom', 'matter', 'antimatter', 'decayed'
        self.energy = energy
        self.age = age
        self.cell_type = cell_type  # 'neutral', 'matter', 'antimatter'
        self.stability = 1.0
        self.void_interference = 0.0
        self.expansion_potential = 0.0
        self.topological_connections = []  # Connections to other cells
        self.last_update_time = 0.0
        
    def update(self, void_field, universe_grid, time, rules):
        """Update cell state based on void physics rules."""
        self.last_update_time = time
        
        # Get void interference at this location
        if 0 <= self.y < void_field.shape[0] and 0 <= self.x < void_field.shape[1]:
            self.void_interference = void_field[int(self.y), int(self.x)]
        else:
            self.void_interference = 0.0
            
        # Age the cell
        self.age += 1
        
        # Apply void physics rules
        if self.state == 'void':
            self._update_void_state(universe_grid, rules)
        elif self.state == 'atom':
            self._update_atom_state(universe_grid, rules)
        elif self.state in ['matter', 'antimatter']:
            self._update_matter_state(universe_grid, rules)
        elif self.state == 'decayed':
            self._update_decayed_state(universe_grid, rules)
            
    def _update_void_state(self, universe_grid, rules):
        """Update void state - can become atom under strong interference."""
        if self.void_interference > rules['void_to_atom_threshold']:
            # Void becomes atom
            self.state = 'atom'
            self.energy = rules['initial_atom_energy']
            self.age = 0
            self.cell_type = 'neutral'
            
    def _update_atom_state(self, universe_grid, rules):
        """Update atom state - can expand or decay based on interference."""
        # Calculate expansion potential
        if self.void_interference > rules['expansion_threshold']:
            self.expansion_potential += rules['expansion_rate'] * self.void_interference
        else:
            # Weak interference - atom ages
            self.stability -= rules['aging_rate'] * (1 - self.void_interference)
            self.energy *= rules['energy_decay_rate']
            
        # Check for expansion
        if self.expansion_potential > rules['expansion_threshold']:
            self._attempt_expansion(universe_grid, rules)
            self.expansion_potential = 0.0
            
        # Check for decay
        if self.stability < rules['decay_threshold'] or self.energy < rules['min_energy']:
            self.state = 'decayed'
            self.energy = 0.0
            
    def _update_matter_state(self, universe_grid, rules):
        """Update matter/antimatter state - can interact with opposite type."""
        # Find neighboring cells of opposite type
        opposite_type = 'antimatter' if self.cell_type == 'matter' else 'matter'
        neighbors = self._get_neighbors(universe_grid)
        
        for neighbor in neighbors:
            if (neighbor.state == opposite_type and 
                neighbor.cell_type == opposite_type):
                # Annihilation
                self.state = 'void'
                neighbor.state = 'void'
                self.energy = 0.0
                neighbor.energy = 0.0
                return
                
        # Normal matter/antimatter evolution
        if self.void_interference > rules['matter_stability_threshold']:
            self.energy += rules['matter_energy_gain'] * self.void_interference
        else:
            self.energy *= rules['matter_energy_decay']
            
        # Check for decay
        if self.energy < rules['min_energy']:
            self.state = 'decayed'
            self.energy = 0.0
            
    def _update_decayed_state(self, universe_grid, rules):
        """Update decayed state - can return to void."""
        if self.void_interference > rules['decay_to_void_threshold']:
            self.state = 'void'
            self.energy = 0.0
            self.age = 0
            
    def _attempt_expansion(self, universe_grid, rules):
        """Attempt to expand to neighboring cells."""
        neighbors = self._get_empty_neighbors(universe_grid)
        
        if neighbors and np.random.random() < rules['expansion_probability']:
            # Choose random neighbor for expansion
            new_x, new_y = neighbors[np.random.randint(len(neighbors))]
            
            # Create new cell
            new_cell = VoidPhysicsCell(new_x, new_y, 
                                     state='atom',
                                     energy=self.energy * rules['energy_conservation_factor'],
                                     age=0,
                                     cell_type=self.cell_type)
            
            # Add to universe
            if (0 <= new_y < universe_grid.shape[0] and 
                0 <= new_x < universe_grid.shape[1]):
                universe_grid[new_y, new_x] = new_cell
                
                # Create topological connection
                self.topological_connections.append(new_cell)
                new_cell.topological_connections.append(self)
                
    def _get_neighbors(self, universe_grid):
        """Get all neighboring cells."""
        neighbors = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                    
                new_x = int(self.x + dx)
                new_y = int(self.y + dy)
                
                if (0 <= new_x < universe_grid.shape[1] and 
                    0 <= new_y < universe_grid.shape[0]):
                    
                    neighbor = universe_grid[new_y, new_x]
                    if neighbor is not None:
                        neighbors.append(neighbor)
                        
        return neighbors
        
    def _get_empty_neighbors(self, universe_grid):
        """Get empty neighboring cells."""
        neighbors = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                    
                new_x = int(self.x + dx)
                new_y = int(self.y + dy)
                
                if (0 <= new_x < universe_grid.shape[1] and 
                    0 <= new_y < universe_grid.shape[0]):
                    
                    if universe_grid[new_y, new_x] is None:
                        neighbors.append((new_x, new_y))
                        
        return neighbors
        
    def get_color(self):
        """Get color based on cell state and properties."""
        if self.state == 'void':
            return (0.1, 0.1, 0.1)  # Dark gray
        elif self.state == 'atom':
            intensity = min(1.0, self.energy)
            return (intensity, intensity, 1.0)  # Blue
        elif self.state == 'matter':
            intensity = min(1.0, self.energy)
            return (intensity, 0.5, 0.5)  # Red
        elif self.state == 'antimatter':
            intensity = min(1.0, self.energy)
            return (0.5, intensity, 0.5)  # Green
        elif self.state == 'decayed':
            return (0.5, 0.5, 0.5)  # Gray
        else:
            return (0.0, 0.0, 0.0)  # Black


class VoidFieldGenerator:
    """Generates void interference patterns."""
    
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.time = 0.0
        self.interference_sources = []
        self.field = np.zeros((height, width))
        
    def add_interference_source(self, x, y, frequency, amplitude, phase=0.0):
        """Add a source of void interference."""
        self.interference_sources.append({
            'x': x, 'y': y, 'frequency': frequency, 'amplitude': amplitude, 'phase': phase
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
            phase = source['phase']
            
            # Create wave pattern
            for i in range(self.height):
                for j in range(self.width):
                    distance = np.sqrt((i - y)**2 + (j - x)**2)
                    wave_phase = 2 * np.pi * freq * self.time - distance * 0.1 + phase
                    self.field[i, j] += amp * np.sin(wave_phase) / (1 + distance * 0.1)
                    
        # Add random void fluctuations
        self.field += np.random.normal(0, 0.05, (self.height, self.width))
        
        # Normalize to [-1, 1]
        self.field = np.tanh(self.field)
        
    def get_field_at(self, x, y):
        """Get field value at specific coordinates."""
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.field[int(y), int(x)]
        return 0.0


class VoidPhysicsLifeGame:
    """Main life game class implementing void physics rules."""
    
    def __init__(self, width=100, height=100):
        self.width = width
        self.height = height
        self.universe_grid = np.full((height, width), None, dtype=object)
        self.void_field = VoidFieldGenerator(width, height)
        self.time = 0.0
        self.history = []
        
        # Game rules
        self.rules = {
            'void_to_atom_threshold': 0.7,
            'initial_atom_energy': 1.0,
            'expansion_threshold': 0.6,
            'expansion_rate': 0.1,
            'aging_rate': 0.05,
            'energy_decay_rate': 0.99,
            'decay_threshold': 0.1,
            'min_energy': 0.01,
            'expansion_probability': 0.3,
            'energy_conservation_factor': 0.8,
            'matter_stability_threshold': 0.5,
            'matter_energy_gain': 0.02,
            'matter_energy_decay': 0.98,
            'decay_to_void_threshold': 0.8
        }
        
        # Statistics
        self.stats = {
            'total_cells': 0,
            'void_cells': 0,
            'atom_cells': 0,
            'matter_cells': 0,
            'antimatter_cells': 0,
            'decayed_cells': 0,
            'total_energy': 0.0,
            'average_age': 0.0,
            'expansion_events': 0,
            'decay_events': 0,
            'annihilation_events': 0
        }
        
    def initialize_void_sources(self, n_sources=8):
        """Initialize void interference sources."""
        for _ in range(n_sources):
            x = np.random.uniform(0, self.width)
            y = np.random.uniform(0, self.height)
            freq = np.random.uniform(0.1, 0.8)
            amp = np.random.uniform(0.5, 2.0)
            phase = np.random.uniform(0, 2 * np.pi)
            self.void_field.add_interference_source(x, y, freq, amp, phase)
            
    def create_initial_pattern(self, pattern_type='random', n_cells=50):
        """Create initial pattern of cells."""
        if pattern_type == 'random':
            for _ in range(n_cells):
                x = np.random.randint(0, self.width)
                y = np.random.randint(0, self.height)
                
                if self.universe_grid[y, x] is None:
                    cell_type = 'matter' if np.random.random() > 0.5 else 'antimatter'
                    cell = VoidPhysicsCell(x, y, state='atom', energy=1.0, 
                                         age=0, cell_type=cell_type)
                    self.universe_grid[y, x] = cell
                    
        elif pattern_type == 'glider':
            # Create a glider pattern
            center_x, center_y = self.width // 2, self.height // 2
            glider_pattern = [(0, 1), (1, 2), (2, 0), (2, 1), (2, 2)]
            
            for dx, dy in glider_pattern:
                x, y = center_x + dx, center_y + dy
                if 0 <= x < self.width and 0 <= y < self.height:
                    cell = VoidPhysicsCell(x, y, state='atom', energy=1.0, 
                                         age=0, cell_type='matter')
                    self.universe_grid[y, x] = cell
                    
        elif pattern_type == 'oscillator':
            # Create an oscillator pattern
            center_x, center_y = self.width // 2, self.height // 2
            oscillator_pattern = [(0, 0), (1, 0), (2, 0)]
            
            for dx, dy in oscillator_pattern:
                x, y = center_x + dx, center_y + dy
                if 0 <= x < self.width and 0 <= y < self.height:
                    cell = VoidPhysicsCell(x, y, state='atom', energy=1.0, 
                                         age=0, cell_type='matter')
                    self.universe_grid[y, x] = cell
                    
    def update(self, dt=1.0):
        """Update the game state."""
        self.time += dt
        
        # Update void field
        self.void_field.update(dt)
        
        # Update all cells
        cells_to_remove = []
        for y in range(self.height):
            for x in range(self.width):
                cell = self.universe_grid[y, x]
                if cell is not None:
                    cell.update(self.void_field.field, self.universe_grid, self.time, self.rules)
                    
                    # Check for removal
                    if cell.state == 'void' and cell.energy == 0:
                        cells_to_remove.append((x, y))
                        
        # Remove cells that became void
        for x, y in cells_to_remove:
            self.universe_grid[y, x] = None
            
        # Update statistics
        self._update_statistics()
        
        # Store history
        self.history.append({
            'time': self.time,
            'void_cells': self.stats['void_cells'],
            'atom_cells': self.stats['atom_cells'],
            'matter_cells': self.stats['matter_cells'],
            'antimatter_cells': self.stats['antimatter_cells'],
            'decayed_cells': self.stats['decayed_cells'],
            'total_energy': self.stats['total_energy'],
            'void_activity': np.mean(np.abs(self.void_field.field))
        })
        
    def _update_statistics(self):
        """Update game statistics."""
        self.stats['total_cells'] = 0
        self.stats['void_cells'] = 0
        self.stats['atom_cells'] = 0
        self.stats['matter_cells'] = 0
        self.stats['antimatter_cells'] = 0
        self.stats['decayed_cells'] = 0
        self.stats['total_energy'] = 0.0
        self.stats['average_age'] = 0.0
        
        ages = []
        for y in range(self.height):
            for x in range(self.width):
                cell = self.universe_grid[y, x]
                if cell is not None:
                    self.stats['total_cells'] += 1
                    self.stats['total_energy'] += cell.energy
                    ages.append(cell.age)
                    
                    if cell.state == 'void':
                        self.stats['void_cells'] += 1
                    elif cell.state == 'atom':
                        self.stats['atom_cells'] += 1
                    elif cell.state == 'matter':
                        self.stats['matter_cells'] += 1
                    elif cell.state == 'antimatter':
                        self.stats['antimatter_cells'] += 1
                    elif cell.state == 'decayed':
                        self.stats['decayed_cells'] += 1
                        
        if ages:
            self.stats['average_age'] = np.mean(ages)
            
    def get_universe_image(self):
        """Get image representation of the universe."""
        image = np.zeros((self.height, self.width, 3))
        
        # Draw cells
        for y in range(self.height):
            for x in range(self.width):
                cell = self.universe_grid[y, x]
                if cell is not None:
                    color = np.array(cell.get_color())  # Convert to numpy array
                    image[y, x] = color
                else:
                    # Show void field
                    void_value = (self.void_field.field[y, x] + 1) / 2
                    image[y, x] = [void_value * 0.1, void_value * 0.1, void_value * 0.1]
                    
        return np.clip(image, 0, 1)
        
    def get_void_field_image(self):
        """Get image representation of the void field."""
        field = self.void_field.field
        # Normalize to [0, 1]
        field = (field + 1) / 2
        return field
        
    def reset(self):
        """Reset the game."""
        self.universe_grid = np.full((self.height, self.width), None, dtype=object)
        self.time = 0.0
        self.history = []
        self.void_field = VoidFieldGenerator(self.width, self.height)
        self.initialize_void_sources()
        self.create_initial_pattern('random', 30)


class VoidPhysicsLifeGameVisualizer:
    """Visualizer for the void physics life game."""
    
    def __init__(self, game):
        self.game = game
        self.fig = None
        self.axes = None
        
    def create_visualization(self):
        """Create the main visualization."""
        self.fig, self.axes = plt.subplots(2, 2, figsize=(16, 12))
        
        # Universe view
        self.axes[0, 0].set_title('Void Physics Life Game')
        self.axes[0, 0].set_xlabel('X')
        self.axes[0, 0].set_ylabel('Y')
        
        # Void field
        self.axes[0, 1].set_title('Void Interference Field')
        self.axes[0, 1].set_xlabel('X')
        self.axes[0, 1].set_ylabel('Y')
        
        # Statistics
        self.axes[1, 0].set_title('Cell Statistics')
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
        universe_image = self.game.get_universe_image()
        self.axes[0, 0].imshow(universe_image, origin='lower', 
                              extent=[0, self.game.width, 0, self.game.height])
        self.axes[0, 0].set_title(f'Void Physics Life Game (t={self.game.time:.1f})')
        self.axes[0, 0].set_xlabel('X')
        self.axes[0, 0].set_ylabel('Y')
        
        # Void field
        void_image = self.game.get_void_field_image()
        im = self.axes[0, 1].imshow(void_image, origin='lower', 
                                   extent=[0, self.game.width, 0, self.game.height], 
                                   cmap='RdBu_r')
        self.axes[0, 1].set_title('Void Interference Field')
        self.axes[0, 1].set_xlabel('X')
        self.axes[0, 1].set_ylabel('Y')
        plt.colorbar(im, ax=self.axes[0, 1])
        
        # Statistics
        if self.game.history:
            history_df = pd.DataFrame(self.game.history)
            self.axes[1, 0].plot(history_df['time'], history_df['atom_cells'], 'b-', label='Atoms')
            self.axes[1, 0].plot(history_df['time'], history_df['matter_cells'], 'r-', label='Matter')
            self.axes[1, 0].plot(history_df['time'], history_df['antimatter_cells'], 'g-', label='Antimatter')
            self.axes[1, 0].set_xlabel('Time')
            self.axes[1, 0].set_ylabel('Count')
            self.axes[1, 0].set_title('Cell Statistics')
            self.axes[1, 0].legend()
            self.axes[1, 0].grid(True, alpha=0.3)
            
        # Energy evolution
        if self.game.history:
            self.axes[1, 1].plot(history_df['time'], history_df['total_energy'], 'purple', linewidth=2)
            self.axes[1, 1].set_xlabel('Time')
            self.axes[1, 1].set_ylabel('Total Energy')
            self.axes[1, 1].set_title('Energy Evolution')
            self.axes[1, 1].grid(True, alpha=0.3)
            
        plt.tight_layout()
        plt.draw()
        
    def animate(self, n_frames=1000, interval=100):
        """Animate the game."""
        # Ensure figure is created
        if self.fig is None:
            self.create_visualization()
            
        def animate_frame(frame):
            self.game.update(dt=0.1)
            self.update_visualization()
            return []
            
        anim = animation.FuncAnimation(self.fig, animate_frame, frames=n_frames, 
                                     interval=interval, blit=False, repeat=True)
        return anim


class VoidPhysicsLifeGameDashboard:
    """Interactive dashboard for the void physics life game."""
    
    def __init__(self, game):
        self.game = game
        self.app = dash.Dash(__name__)
        self.setup_layout()
        self.setup_callbacks()
        
    def setup_layout(self):
        """Setup the dashboard layout."""
        self.app.layout = html.Div([
            html.H1("Void Physics Life Game - Interactive Dashboard", 
                   style={'textAlign': 'center', 'color': 'white', 'backgroundColor': '#1a1a2e'}),
            
            html.Div([
                # Control panel
                html.Div([
                    html.H3("Game Controls", style={'color': 'white'}),
                    
                    html.Label("Void to Atom Threshold:"),
                    dcc.Slider(
                        id='void-threshold-slider',
                        min=0.1, max=1.0, step=0.1, value=0.7,
                        marks={i/10: str(i/10) for i in range(1, 11)}
                    ),
                    
                    html.Label("Expansion Threshold:"),
                    dcc.Slider(
                        id='expansion-threshold-slider',
                        min=0.1, max=1.0, step=0.1, value=0.6,
                        marks={i/10: str(i/10) for i in range(1, 11)}
                    ),
                    
                    html.Label("Expansion Rate:"),
                    dcc.Slider(
                        id='expansion-rate-slider',
                        min=0.01, max=0.5, step=0.01, value=0.1,
                        marks={i/100: str(i/100) for i in range(1, 51, 5)}
                    ),
                    
                    html.Label("Aging Rate:"),
                    dcc.Slider(
                        id='aging-rate-slider',
                        min=0.01, max=0.2, step=0.01, value=0.05,
                        marks={i/100: str(i/100) for i in range(1, 21, 2)}
                    ),
                    
                    html.Label("Energy Decay Rate:"),
                    dcc.Slider(
                        id='energy-decay-slider',
                        min=0.9, max=1.0, step=0.001, value=0.99,
                        marks={i/1000: str(i/1000) for i in range(900, 1001, 20)}
                    ),
                    
                    html.Label("Expansion Probability:"),
                    dcc.Slider(
                        id='expansion-prob-slider',
                        min=0.1, max=1.0, step=0.1, value=0.3,
                        marks={i/10: str(i/10) for i in range(1, 11)}
                    ),
                    
                    html.Button('Reset Game', id='reset-button', n_clicks=0),
                    html.Button('Pause/Resume', id='pause-button', n_clicks=0),
                    
                ], style={'width': '25%', 'display': 'inline-block', 'verticalAlign': 'top',
                         'backgroundColor': '#16213e', 'padding': '20px', 'margin': '10px',
                         'borderRadius': '10px'}),
                
                # Main visualization
                html.Div([
                    dcc.Graph(id='game-plot'),
                    dcc.Interval(
                        id='interval-component',
                        interval=200,  # Update every 200ms
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
            [Output('game-plot', 'figure'),
             Output('void-field-plot', 'figure'),
             Output('history-plot', 'figure'),
             Output('stats-display', 'children')],
            [Input('interval-component', 'n_intervals'),
             Input('void-threshold-slider', 'value'),
             Input('expansion-threshold-slider', 'value'),
             Input('expansion-rate-slider', 'value'),
             Input('aging-rate-slider', 'value'),
             Input('energy-decay-slider', 'value'),
             Input('expansion-prob-slider', 'value'),
             Input('reset-button', 'n_clicks')]
        )
        def update_dashboard(n_intervals, void_threshold, expansion_threshold, 
                           expansion_rate, aging_rate, energy_decay, expansion_prob, reset_clicks):
            
            # Update game rules
            self.game.rules['void_to_atom_threshold'] = void_threshold
            self.game.rules['expansion_threshold'] = expansion_threshold
            self.game.rules['expansion_rate'] = expansion_rate
            self.game.rules['aging_rate'] = aging_rate
            self.game.rules['energy_decay_rate'] = energy_decay
            self.game.rules['expansion_probability'] = expansion_prob
            
            # Reset if button clicked
            if reset_clicks > 0:
                self.game.reset()
            
            # Update game
            self.game.update(dt=0.1)
            
            # Create game plot
            game_fig = go.Figure()
            game_image = self.game.get_universe_image()
            
            game_fig.add_trace(go.Image(z=game_image, 
                                      colorscale='Viridis',
                                      showscale=False))
            
            game_fig.update_layout(
                title=f"Void Physics Life Game (t={self.game.time:.1f})",
                xaxis_title="X",
                yaxis_title="Y",
                width=600,
                height=400
            )
            
            # Create void field plot
            void_fig = go.Figure()
            void_image = self.game.get_void_field_image()
            
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
            
            if self.game.history:
                history_df = pd.DataFrame(self.game.history)
                
                history_fig.add_trace(go.Scatter(
                    x=history_df['time'],
                    y=history_df['atom_cells'],
                    mode='lines',
                    name='Atoms',
                    line=dict(color='blue', width=2)
                ))
                
                history_fig.add_trace(go.Scatter(
                    x=history_df['time'],
                    y=history_df['matter_cells'],
                    mode='lines',
                    name='Matter',
                    line=dict(color='red', width=2)
                ))
                
                history_fig.add_trace(go.Scatter(
                    x=history_df['time'],
                    y=history_df['antimatter_cells'],
                    mode='lines',
                    name='Antimatter',
                    line=dict(color='green', width=2)
                ))
                
                history_fig.update_layout(
                    title="Evolution History",
                    xaxis_title="Time",
                    yaxis_title="Number of Cells",
                    width=1000,
                    height=300
                )
            
            # Create statistics display
            stats_text = f"""
            **Current Statistics:**
            - Total Cells: {self.game.stats['total_cells']}
            - Void Cells: {self.game.stats['void_cells']}
            - Atom Cells: {self.game.stats['atom_cells']}
            - Matter Cells: {self.game.stats['matter_cells']}
            - Antimatter Cells: {self.game.stats['antimatter_cells']}
            - Decayed Cells: {self.game.stats['decayed_cells']}
            - Total Energy: {self.game.stats['total_energy']:.2f}
            - Average Age: {self.game.stats['average_age']:.2f}
            - Void Activity: {np.mean(np.abs(self.game.void_field.field)):.3f}
            """
            
            return game_fig, void_fig, history_fig, stats_text
            
    def run(self, debug=False, port=8051):
        """Run the dashboard."""
        self.app.run_server(debug=debug, port=port)


def main():
    """Run the void physics life game."""
    print("🎮 Starting Void Physics Life Game...")
    
    # Create game
    game = VoidPhysicsLifeGame(width=80, height=80)
    game.initialize_void_sources(n_sources=6)
    game.create_initial_pattern('random', n_cells=40)
    
    # Create visualizer
    visualizer = VoidPhysicsLifeGameVisualizer(game)
    
    # Run animation
    print("🎬 Starting animation...")
    anim = visualizer.animate(n_frames=1000, interval=100)
    
    # Save animation
    print("💾 Saving animation...")
    anim.save('examples/void_physics_life_game_animation.gif', writer='pillow', fps=10)
    
    # Create dashboard
    print("📊 Creating interactive dashboard...")
    dashboard = VoidPhysicsLifeGameDashboard(game)
    
    # Run dashboard
    print("🚀 Starting dashboard on http://localhost:8051")
    dashboard.run(debug=False, port=8051)


if __name__ == "__main__":
    main()
