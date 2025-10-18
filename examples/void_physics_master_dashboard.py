#!/usr/bin/env python3
"""
Void Physics Master Dashboard
=============================

A comprehensive dashboard that combines:
- Universe Creation Simulation
- Void Physics Life Game
- Real-time parameter control
- Statistical analysis
- Pattern recognition
- Educational content

This dashboard implements the complete void physics framework with
interference patterns, topological connectivity, and emergent behavior.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import seaborn as sns
import pandas as pd
from scipy import ndimage
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

# Import our simulation classes
from universe_creation_simulation import UniverseCreationSimulation, Atom, VoidField
from void_physics_life_game import VoidPhysicsLifeGame, VoidPhysicsCell, VoidFieldGenerator

# Set up beautiful plotting
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

class VoidPhysicsMasterDashboard:
    """Master dashboard combining all void physics simulations."""
    
    def __init__(self):
        self.setup_simulations()
        self.setup_app()
        self.setup_layout()
        self.setup_callbacks()
        
    def setup_simulations(self):
        """Initialize both simulations."""
        # Universe creation simulation
        self.universe_sim = UniverseCreationSimulation(width=60, height=60)
        self.universe_sim.initialize_void_sources()
        self.universe_sim.create_initial_atoms(n_atoms=5)
        
        # Life game simulation
        self.life_game = VoidPhysicsLifeGame(width=60, height=60)
        self.life_game.initialize_void_sources(n_sources=4)
        self.life_game.create_initial_pattern('random', n_cells=20)
        
        # Simulation state
        self.simulation_running = True
        self.current_simulation = 'universe'  # 'universe' or 'life_game'
        
    def setup_app(self):
        """Setup the Dash app."""
        self.app = dash.Dash(__name__)
        
    def setup_layout(self):
        """Setup the dashboard layout."""
        self.app.layout = html.Div([
            # Header
            html.Div([
                html.H1("🌌 Void Physics Master Dashboard", 
                       style={'textAlign': 'center', 'color': 'white', 
                             'backgroundColor': '#1a1a2e', 'padding': '20px',
                             'fontSize': '2.5em', 'fontWeight': 'bold'}),
                html.P("Exploring the emergence of spacetime from the void through stochastic dynamics", 
                      style={'textAlign': 'center', 'color': '#cccccc', 'fontSize': '1.2em'})
            ]),
            
            # Main control panel
            html.Div([
                html.Div([
                    html.H3("🎮 Simulation Control", style={'color': 'white', 'textAlign': 'center'}),
                    
                    # Simulation selection
                    html.Label("Select Simulation:", style={'color': 'white', 'fontWeight': 'bold'}),
                    dcc.RadioItems(
                        id='simulation-selector',
                        options=[
                            {'label': '🌌 Universe Creation', 'value': 'universe'},
                            {'label': '🎮 Life Game', 'value': 'life_game'}
                        ],
                        value='universe',
                        style={'color': 'white'}
                    ),
                    
                    html.Hr(style={'borderColor': '#444'}),
                    
                    # Global controls
                    html.Label("Global Parameters:", style={'color': 'white', 'fontWeight': 'bold'}),
                    
                    html.Label("Void Interference Strength:"),
                    dcc.Slider(
                        id='global-void-strength',
                        min=0.1, max=3.0, step=0.1, value=1.0,
                        marks={i/10: str(i/10) for i in range(1, 31, 3)},
                        tooltip={"placement": "bottom", "always_visible": True}
                    ),
                    
                    html.Label("Time Speed:"),
                    dcc.Slider(
                        id='time-speed',
                        min=0.1, max=5.0, step=0.1, value=1.0,
                        marks={i/10: str(i/10) for i in range(1, 51, 5)},
                        tooltip={"placement": "bottom", "always_visible": True}
                    ),
                    
                    html.Hr(style={'borderColor': '#444'}),
                    
                    # Control buttons
                    html.Div([
                        html.Button('▶️ Start', id='start-button', n_clicks=0,
                                  style={'margin': '5px', 'padding': '10px', 'backgroundColor': '#4CAF50', 'color': 'white'}),
                        html.Button('⏸️ Pause', id='pause-button', n_clicks=0,
                                  style={'margin': '5px', 'padding': '10px', 'backgroundColor': '#FF9800', 'color': 'white'}),
                        html.Button('🔄 Reset', id='reset-button', n_clicks=0,
                                  style={'margin': '5px', 'padding': '10px', 'backgroundColor': '#F44336', 'color': 'white'}),
                    ], style={'textAlign': 'center'}),
                    
                ], style={'width': '25%', 'display': 'inline-block', 'verticalAlign': 'top',
                         'backgroundColor': '#16213e', 'padding': '20px', 'margin': '10px',
                         'borderRadius': '15px', 'border': '2px solid #444'}),
                
                # Main visualization area
                html.Div([
                    dcc.Graph(id='main-simulation-plot', style={'height': '500px'}),
                    dcc.Interval(
                        id='main-interval',
                        interval=200,  # Update every 200ms
                        n_intervals=0
                    )
                ], style={'width': '70%', 'display': 'inline-block', 'verticalAlign': 'top'})
                
            ], style={'display': 'flex', 'margin': '20px'}),
            
            # Parameter control panels
            html.Div([
                # Universe creation parameters
                html.Div([
                    html.H3("🌌 Universe Creation Parameters", style={'color': 'white', 'textAlign': 'center'}),
                    
                    html.Label("Atom Creation Rate:"),
                    dcc.Slider(id='universe-creation-rate', min=0.001, max=0.1, step=0.001, value=0.01),
                    
                    html.Label("Expansion Probability:"),
                    dcc.Slider(id='universe-expansion-prob', min=0.01, max=0.5, step=0.01, value=0.1),
                    
                    html.Label("Decay Rate:"),
                    dcc.Slider(id='universe-decay-rate', min=0.0001, max=0.01, step=0.0001, value=0.001),
                    
                    html.Label("Energy Conservation:"),
                    dcc.Slider(id='universe-energy-conservation', min=0.5, max=1.0, step=0.01, value=0.8),
                    
                ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top',
                         'backgroundColor': '#0f3460', 'padding': '20px', 'margin': '10px',
                         'borderRadius': '15px', 'border': '2px solid #444'}),
                
                # Life game parameters
                html.Div([
                    html.H3("🎮 Life Game Parameters", style={'color': 'white', 'textAlign': 'center'}),
                    
                    html.Label("Void to Atom Threshold:"),
                    dcc.Slider(id='life-void-threshold', min=0.1, max=1.0, step=0.1, value=0.7),
                    
                    html.Label("Expansion Threshold:"),
                    dcc.Slider(id='life-expansion-threshold', min=0.1, max=1.0, step=0.1, value=0.6),
                    
                    html.Label("Aging Rate:"),
                    dcc.Slider(id='life-aging-rate', min=0.01, max=0.2, step=0.01, value=0.05),
                    
                    html.Label("Energy Decay Rate:"),
                    dcc.Slider(id='life-energy-decay', min=0.9, max=1.0, step=0.001, value=0.99),
                    
                ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top',
                         'backgroundColor': '#533483', 'padding': '20px', 'margin': '10px',
                         'borderRadius': '15px', 'border': '2px solid #444'})
                
            ], style={'display': 'flex', 'margin': '20px'}),
            
            # Analysis panels
            html.Div([
                # Void field analysis
                html.Div([
                    html.H3("🌀 Void Field Analysis", style={'color': 'white', 'textAlign': 'center'}),
                    dcc.Graph(id='void-field-plot', style={'height': '300px'})
                ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top',
                         'backgroundColor': '#7209b7', 'padding': '20px', 'margin': '10px',
                         'borderRadius': '15px', 'border': '2px solid #444'}),
                
                # Statistics panel
                html.Div([
                    html.H3("📊 Real-time Statistics", style={'color': 'white', 'textAlign': 'center'}),
                    html.Div(id='statistics-display', style={'color': 'white', 'fontSize': '14px'})
                ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top',
                         'backgroundColor': '#e94560', 'padding': '20px', 'margin': '10px',
                         'borderRadius': '15px', 'border': '2px solid #444'})
                
            ], style={'display': 'flex', 'margin': '20px'}),
            
            # Evolution history
            html.Div([
                html.H3("📈 Evolution History", style={'color': 'white', 'textAlign': 'center'}),
                dcc.Graph(id='evolution-history-plot', style={'height': '400px'})
            ], style={'width': '100%', 'backgroundColor': '#2d1b69', 'padding': '20px', 'margin': '20px',
                     'borderRadius': '15px', 'border': '2px solid #444'}),
            
            # Educational content
            html.Div([
                html.H3("🎓 Void Physics Concepts", style={'color': 'white', 'textAlign': 'center'}),
                html.Div([
                    html.Div([
                        html.H4("🌌 The Void (Néant)", style={'color': '#4CAF50'}),
                        html.P("The void is not empty space - it's a state of perfect symmetry where all possibilities exist simultaneously. It's the mathematical representation of 'nothing' that contains the potential for everything."),
                    ], style={'width': '30%', 'display': 'inline-block', 'verticalAlign': 'top', 'margin': '10px'}),
                    
                    html.Div([
                        html.H4("⚡ Void Interference", style={'color': '#FF9800'}),
                        html.P("Void interference patterns test atoms and cause them to expand randomly where constraints allow, or age if not. This creates the real space t+1 from the timeless void."),
                    ], style={'width': '30%', 'display': 'inline-block', 'verticalAlign': 'top', 'margin': '10px'}),
                    
                    html.Div([
                        html.H4("🔗 Topological Connectivity", style={'color': '#F44336'}),
                        html.P("The void is connected to all spaces without distance or space constraints. This topological connectivity allows for non-local interactions and emergent behavior."),
                    ], style={'width': '30%', 'display': 'inline-block', 'verticalAlign': 'top', 'margin': '10px'}),
                ])
            ], style={'width': '100%', 'backgroundColor': '#11998e', 'padding': '20px', 'margin': '20px',
                     'borderRadius': '15px', 'border': '2px solid #444'})
            
        ], style={'backgroundColor': '#1a1a2e', 'color': 'white', 'fontFamily': 'Arial, sans-serif'})
        
    def setup_callbacks(self):
        """Setup all dashboard callbacks."""
        
        @self.app.callback(
            [Output('main-simulation-plot', 'figure'),
             Output('void-field-plot', 'figure'),
             Output('evolution-history-plot', 'figure'),
             Output('statistics-display', 'children')],
            [Input('main-interval', 'n_intervals'),
             Input('simulation-selector', 'value'),
             Input('global-void-strength', 'value'),
             Input('time-speed', 'value'),
             Input('universe-creation-rate', 'value'),
             Input('universe-expansion-prob', 'value'),
             Input('universe-decay-rate', 'value'),
             Input('universe-energy-conservation', 'value'),
             Input('life-void-threshold', 'value'),
             Input('life-expansion-threshold', 'value'),
             Input('life-aging-rate', 'value'),
             Input('life-energy-decay', 'value'),
             Input('start-button', 'n_clicks'),
             Input('pause-button', 'n_clicks'),
             Input('reset-button', 'n_clicks')]
        )
        def update_dashboard(n_intervals, simulation_type, void_strength, time_speed,
                           universe_creation_rate, universe_expansion_prob, universe_decay_rate, universe_energy_conservation,
                           life_void_threshold, life_expansion_threshold, life_aging_rate, life_energy_decay,
                           start_clicks, pause_clicks, reset_clicks):
            
            # Update current simulation
            self.current_simulation = simulation_type
            
            # Update simulation parameters
            if simulation_type == 'universe':
                self.universe_sim.void_interference_strength = void_strength
                self.universe_sim.atom_creation_rate = universe_creation_rate
                self.universe_sim.expansion_probability = universe_expansion_prob
                self.universe_sim.decay_rate = universe_decay_rate
                
                # Update simulation
                if self.simulation_running:
                    self.universe_sim.update(dt=0.1 * time_speed)
                    
                # Get simulation data
                universe_image = self.universe_sim.get_universe_image()
                void_image = self.universe_sim.get_void_field_image()
                stats = self.universe_sim.stats
                history = self.universe_sim.history
                
            else:  # life_game
                self.life_game.rules['void_to_atom_threshold'] = life_void_threshold
                self.life_game.rules['expansion_threshold'] = life_expansion_threshold
                self.life_game.rules['aging_rate'] = life_aging_rate
                self.life_game.rules['energy_decay_rate'] = life_energy_decay
                
                # Update simulation
                if self.simulation_running:
                    self.life_game.update(dt=0.1 * time_speed)
                    
                # Get simulation data
                universe_image = self.life_game.get_universe_image()
                void_image = self.life_game.get_void_field_image()
                stats = self.life_game.stats
                history = self.life_game.history
            
            # Create main simulation plot
            main_fig = go.Figure()
            main_fig.add_trace(go.Image(z=universe_image, colorscale='Viridis', showscale=False))
            
            main_fig.update_layout(
                title=f"{'🌌 Universe Creation' if simulation_type == 'universe' else '🎮 Life Game'} (t={self.universe_sim.time if simulation_type == 'universe' else self.life_game.time:.1f})",
                xaxis_title="X",
                yaxis_title="Y",
                width=800,
                height=500,
                plot_bgcolor='black',
                paper_bgcolor='black',
                font=dict(color='white')
            )
            
            # Create void field plot
            void_fig = go.Figure()
            void_fig.add_trace(go.Heatmap(z=void_image, colorscale='RdBu_r', showscale=True))
            
            void_fig.update_layout(
                title="🌀 Void Interference Field",
                xaxis_title="X",
                yaxis_title="Y",
                width=500,
                height=300,
                plot_bgcolor='black',
                paper_bgcolor='black',
                font=dict(color='white')
            )
            
            # Create evolution history plot
            history_fig = go.Figure()
            
            if history:
                history_df = pd.DataFrame(history)
                
                if simulation_type == 'universe':
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
                    
                else:  # life_game
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
                    title="📈 Evolution History",
                    xaxis_title="Time",
                    yaxis_title="Count",
                    yaxis2=dict(title="Energy", overlaying="y", side="right") if simulation_type == 'universe' else None,
                    width=1000,
                    height=400,
                    plot_bgcolor='black',
                    paper_bgcolor='black',
                    font=dict(color='white')
                )
            
            # Create statistics display
            if simulation_type == 'universe':
                stats_text = f"""
                **🌌 Universe Creation Statistics:**
                - Total Atoms: {stats['total_atoms']}
                - Matter Atoms: {stats['matter_atoms']}
                - Antimatter Atoms: {stats['antimatter_atoms']}
                - Total Energy: {stats['total_energy']:.2f}
                - Average Age: {stats['average_age']:.2f}
                - Expansion Events: {stats['expansion_events']}
                - Decay Events: {stats['decay_events']}
                """
            else:
                stats_text = f"""
                **🎮 Life Game Statistics:**
                - Total Cells: {stats['total_cells']}
                - Void Cells: {stats['void_cells']}
                - Atom Cells: {stats['atom_cells']}
                - Matter Cells: {stats['matter_cells']}
                - Antimatter Cells: {stats['antimatter_cells']}
                - Decayed Cells: {stats['decayed_cells']}
                - Total Energy: {stats['total_energy']:.2f}
                - Average Age: {stats['average_age']:.2f}
                """
            
            return main_fig, void_fig, history_fig, stats_text
        
        # Control button callbacks
        @self.app.callback(
            Output('start-button', 'n_clicks'),
            [Input('start-button', 'n_clicks')]
        )
        def start_simulation(n_clicks):
            if n_clicks > 0:
                self.simulation_running = True
            return 0
            
        @self.app.callback(
            Output('pause-button', 'n_clicks'),
            [Input('pause-button', 'n_clicks')]
        )
        def pause_simulation(n_clicks):
            if n_clicks > 0:
                self.simulation_running = not self.simulation_running
            return 0
            
        @self.app.callback(
            Output('reset-button', 'n_clicks'),
            [Input('reset-button', 'n_clicks')]
        )
        def reset_simulation(n_clicks):
            if n_clicks > 0:
                if self.current_simulation == 'universe':
                    self.universe_sim = UniverseCreationSimulation(60, 60)
                    self.universe_sim.initialize_void_sources()
                    self.universe_sim.create_initial_atoms(n_atoms=5)
                else:
                    self.life_game.reset()
            return 0
            
    def run(self, debug=False, port=8052):
        """Run the master dashboard."""
        print("🚀 Starting Void Physics Master Dashboard...")
        print(f"📊 Dashboard will be available at: http://localhost:{port}")
        print("🌌 Explore the emergence of spacetime from the void!")
        
        self.app.run_server(debug=debug, port=port)


def main():
    """Run the master dashboard."""
    dashboard = VoidPhysicsMasterDashboard()
    dashboard.run(debug=False, port=8052)


if __name__ == "__main__":
    main()
