"""
Quantum Void Physics Interactive Dashboard

A Plotly Dash application providing interactive exploration of quantum mechanics
concepts integrated with void physics. Features sandbox mode for parametric
exploration and game mode for universe creation challenges.
"""

import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import dash
from dash import dcc, html, Input, Output, State, callback_context
import dash_bootstrap_components as dbc
from typing import Dict, List, Tuple, Any, Optional
import json
import time
from pathlib import Path

# Import quantum modules
try:
    from ..quantum.schrodinger import SchrodingerSolver, SchrodingerParameters, WaveFunction
    from ..quantum.relativistic import KleinGordonSolver, DiracSolver, RelativisticParameters
    from ..quantum.field_theory import QuantumField, FieldParameters, ParticleCreation
    from ..core.potential import DoubleWellPotential, PotentialParameters
except ImportError:
    # Handle direct execution
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
    from void_physic.quantum.schrodinger import SchrodingerSolver, SchrodingerParameters, WaveFunction
    from void_physic.quantum.relativistic import KleinGordonSolver, DiracSolver, RelativisticParameters
    from void_physic.quantum.field_theory import QuantumField, FieldParameters, ParticleCreation
    from void_physic.core.potential import DoubleWellPotential, PotentialParameters


class QuantumDashboard:
    """
    Main dashboard class for quantum void physics visualization.
    """
    
    def __init__(self):
        self.app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], 
                           suppress_callback_exceptions=True)
        self.setup_layout()
        self.setup_callbacks()
        
        # Default parameters
        self.default_params = {
            'mass': 1.0,
            'hbar': 1.0,
            'potential_depth': 1.0,
            'barrier_width': 1.0,
            'coupling': 1.0,
            'equation_type': 'Schrodinger',
            'potential_type': 'double_well'
        }
        
        # Game state
        self.game_state = {
            'level': 1,
            'score': 0,
            'particles_created': 0,
            'stability_time': 0,
            'entropy': 0,
            'is_running': False
        }
    
    def setup_layout(self):
        """Set up the dashboard layout with tabs."""
        self.app.layout = dbc.Container([
            dbc.Row([
                dbc.Col([
                    html.H1("Quantum Void Physics Interactive", 
                           className="text-center mb-4"),
                    html.P("Explore quantum mechanics and void physics through "
                          "interactive visualizations and universe creation games.",
                          className="text-center text-muted mb-4")
                ])
            ]),
            
            dbc.Row([
                dbc.Col([
                    dcc.Tabs(id="main-tabs", value="sandbox", children=[
                        dcc.Tab(label="🔬 Sandbox", value="sandbox", 
                               className="custom-tab"),
                        dcc.Tab(label="🎮 Game", value="game", 
                               className="custom-tab"),
                        dcc.Tab(label="📚 Theory", value="theory", 
                               className="custom-tab")
                    ])
                ])
            ]),
            
            html.Div(id="tab-content")
        ], fluid=True)
    
    def create_sandbox_layout(self):
        """Create sandbox mode layout."""
        return dbc.Container([
            dbc.Row([
                # Control Panel
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader("Quantum Parameters"),
                        dbc.CardBody([
                            html.Label("Mass (m):"),
                            dcc.Slider(
                                id="mass-slider",
                                min=0.1, max=5.0, step=0.1, value=1.0,
                                marks={i: str(i) for i in [0.1, 1.0, 2.0, 3.0, 4.0, 5.0]}
                            ),
                            
                            html.Label("Planck Constant (ℏ):", className="mt-3"),
                            dcc.Slider(
                                id="hbar-slider",
                                min=0.1, max=2.0, step=0.1, value=1.0,
                                marks={i: str(i) for i in [0.1, 0.5, 1.0, 1.5, 2.0]}
                            ),
                            
                            html.Label("Potential Depth (V₀):", className="mt-3"),
                            dcc.Slider(
                                id="potential-depth-slider",
                                min=0.1, max=5.0, step=0.1, value=1.0,
                                marks={i: str(i) for i in [0.1, 1.0, 2.0, 3.0, 4.0, 5.0]}
                            ),
                            
                            html.Label("Barrier Width:", className="mt-3"),
                            dcc.Slider(
                                id="barrier-width-slider",
                                min=0.1, max=3.0, step=0.1, value=1.0,
                                marks={i: str(i) for i in [0.1, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0]}
                            ),
                            
                            html.Label("Coupling (λ):", className="mt-3"),
                            dcc.Slider(
                                id="coupling-slider",
                                min=0.1, max=3.0, step=0.1, value=1.0,
                                marks={i: str(i) for i in [0.1, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0]}
                            ),
                            
                            html.Label("Equation Type:", className="mt-3"),
                            dcc.Dropdown(
                                id="equation-type-dropdown",
                                options=[
                                    {'label': 'Schrödinger', 'value': 'Schrodinger'},
                                    {'label': 'Klein-Gordon', 'value': 'KleinGordon'},
                                    {'label': 'Dirac', 'value': 'Dirac'},
                                    {'label': 'QFT Field', 'value': 'QFT'}
                                ],
                                value='Schrodinger'
                            ),
                            
                            html.Label("Potential Type:", className="mt-3"),
                            dcc.Dropdown(
                                id="potential-type-dropdown",
                                options=[
                                    {'label': 'Double Well', 'value': 'double_well'},
                                    {'label': 'Harmonic', 'value': 'harmonic'},
                                    {'label': 'Step Barrier', 'value': 'step_barrier'},
                                    {'label': 'Mexican Hat', 'value': 'mexican_hat'}
                                ],
                                value='double_well'
                            ),
                            
                            dbc.Button("Run Simulation", id="run-simulation-btn", 
                                     color="primary", className="mt-3 w-100")
                        ])
                    ])
                ], width=3),
                
                # Visualization Panel
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader("Quantum Evolution"),
                        dbc.CardBody([
                            dcc.Graph(id="wave-function-plot"),
                            dcc.Graph(id="probability-current-plot"),
                            dcc.Graph(id="energy-eigenvalues-plot")
                        ])
                    ])
                ], width=9)
            ])
        ], fluid=True)
    
    def create_game_layout(self):
        """Create game mode layout."""
        return dbc.Container([
            dbc.Row([
                # Game Controls
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader("Universe Creation Game"),
                        dbc.CardBody([
                            html.H4(f"Level {self.game_state['level']}", id="level-display"),
                            html.P(f"Score: {self.game_state['score']}", id="score-display"),
                            html.P(f"Particles: {self.game_state['particles_created']}", 
                                  id="particles-display"),
                            html.P(f"Stability: {self.game_state['stability_time']}s", 
                                  id="stability-display"),
                            
                            html.Hr(),
                            
                            html.Label("Emergence Rate:"),
                            dcc.Slider(
                                id="emergence-rate-slider",
                                min=0.01, max=0.5, step=0.01, value=0.1,
                                marks={i: f"{i:.2f}" for i in [0.01, 0.1, 0.2, 0.3, 0.4, 0.5]}
                            ),
                            
                            html.Label("Quantum Coupling:", className="mt-3"),
                            dcc.Slider(
                                id="quantum-coupling-slider",
                                min=0.1, max=2.0, step=0.1, value=1.0,
                                marks={i: str(i) for i in [0.1, 0.5, 1.0, 1.5, 2.0]}
                            ),
                            
                            html.Label("Void Field Strength:", className="mt-3"),
                            dcc.Slider(
                                id="void-strength-slider",
                                min=0.1, max=2.0, step=0.1, value=1.0,
                                marks={i: str(i) for i in [0.1, 0.5, 1.0, 1.5, 2.0]}
                            ),
                            
                            dbc.Button("Start Universe", id="start-universe-btn", 
                                     color="success", className="mt-3 w-100"),
                            dbc.Button("Stop Universe", id="stop-universe-btn", 
                                     color="danger", className="mt-2 w-100", disabled=True),
                            dbc.Button("Save Universe", id="save-universe-btn", 
                                     color="info", className="mt-2 w-100", disabled=True)
                        ])
                    ])
                ], width=3),
                
                # Game Visualization
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader("Universe Evolution"),
                        dbc.CardBody([
                            dcc.Graph(id="universe-evolution-plot"),
                            dcc.Graph(id="particle-distribution-plot"),
                            dcc.Graph(id="entropy-evolution-plot")
                        ])
                    ])
                ], width=9)
            ])
        ], fluid=True)
    
    def create_theory_layout(self):
        """Create theory mode layout."""
        return dbc.Container([
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader("Quantum Mechanics Theory"),
                        dbc.CardBody([
                            html.H4("Schrödinger Equation"),
                            html.P("iℏ ∂ψ/∂t = Ĥψ = [p̂²/(2m) + V(x)]ψ"),
                            
                            html.H4("Probability Current"),
                            html.P("j = (ℏ/2mi)(ψ*∇ψ - ψ∇ψ*)"),
                            
                            html.H4("Quantum Potential"),
                            html.P("V_quantum = -(ℏ²/2m)(∇²√ρ)/√ρ"),
                            
                            html.H4("Void-Quantum Connection"),
                            html.P("Quantum vacuum fluctuations drive particle emergence "
                                  "from the void state through field excitations."),
                            
                            html.Hr(),
                            
                            html.H4("Equation Comparison"),
                            dcc.Graph(id="equation-comparison-plot")
                        ])
                    ])
                ])
            ])
        ], fluid=True)
    
    def setup_callbacks(self):
        """Set up dashboard callbacks."""
        
        @self.app.callback(
            Output("tab-content", "children"),
            Input("main-tabs", "value")
        )
        def render_tab_content(active_tab):
            if active_tab == "sandbox":
                return self.create_sandbox_layout()
            elif active_tab == "game":
                return self.create_game_layout()
            elif active_tab == "theory":
                return self.create_theory_layout()
        
        @self.app.callback(
            [Output("wave-function-plot", "figure"),
             Output("probability-current-plot", "figure"),
             Output("energy-eigenvalues-plot", "figure")],
            [Input("run-simulation-btn", "n_clicks"),
             Input("mass-slider", "value"),
             Input("hbar-slider", "value"),
             Input("potential-depth-slider", "value"),
             Input("barrier-width-slider", "value"),
             Input("coupling-slider", "value"),
             Input("equation-type-dropdown", "value"),
             Input("potential-type-dropdown", "value")]
        )
        def update_sandbox_plots(n_clicks, mass, hbar, potential_depth, 
                                barrier_width, coupling, equation_type, potential_type):
            if n_clicks is None:
                return self.create_empty_plots()
            
            try:
                # Create potential function
                potential_func = self.create_potential_function(
                    potential_type, potential_depth, barrier_width, coupling
                )
                
                # Set up solver based on equation type
                if equation_type == 'Schrodinger':
                    params = SchrodingerParameters(
                        mass=mass, hbar=hbar, potential=potential_func
                    )
                    solver = SchrodingerSolver(params)
                    
                    # Create initial wave function
                    psi_init = solver.create_gaussian_packet(x0=0.0, p0=0.0, sigma=1.0)
                    
                    # Evolve wave function
                    psi_trajectory, time_array = solver.evolve_trajectory(psi_init, 100)
                    
                    # Create plots
                    wave_plot = self.create_wave_function_plot(psi_trajectory, solver.x_grid, time_array)
                    current_plot = self.create_probability_current_plot(psi_trajectory, solver.x_grid, time_array)
                    energy_plot = self.create_energy_eigenvalues_plot(solver)
                    
                elif equation_type == 'KleinGordon':
                    params = RelativisticParameters(
                        mass=mass, c=1.0, hbar=hbar
                    )
                    solver = KleinGordonSolver(params)
                    
                    # Create initial field
                    phi_init, dphi_dt_init = solver.create_gaussian_field(x0=0.0, k0=0.0, sigma=1.0)
                    
                    # Evolve field
                    phi_current = phi_init.copy()
                    dphi_dt_current = dphi_dt_init.copy()
                    phi_trajectory = np.zeros((100, len(phi_init)), dtype=complex)
                    
                    for i in range(100):
                        phi_trajectory[i] = phi_current
                        phi_current, dphi_dt_current = solver.evolve_step(phi_current, dphi_dt_current)
                    
                    # Create plots
                    wave_plot = self.create_field_evolution_plot(phi_trajectory, solver.x_grid)
                    current_plot = self.create_empty_plot("Energy Density")
                    energy_plot = self.create_empty_plot("Dispersion Relation")
                    
                else:
                    # Default empty plots for other equation types
                    wave_plot = self.create_empty_plot("Wave Function")
                    current_plot = self.create_empty_plot("Probability Current")
                    energy_plot = self.create_empty_plot("Energy Eigenvalues")
                
                return wave_plot, current_plot, energy_plot
                
            except Exception as e:
                print(f"Error in sandbox simulation: {e}")
                return self.create_empty_plots()
        
        # Game mode callbacks
        @self.app.callback(
            [Output("universe-evolution-plot", "figure"),
             Output("particle-distribution-plot", "figure"),
             Output("entropy-evolution-plot", "figure"),
             Output("start-universe-btn", "disabled"),
             Output("stop-universe-btn", "disabled"),
             Output("save-universe-btn", "disabled")],
            [Input("start-universe-btn", "n_clicks"),
             Input("stop-universe-btn", "n_clicks"),
             Input("save-universe-btn", "n_clicks")],
            [State("emergence-rate-slider", "value"),
             State("quantum-coupling-slider", "value"),
             State("void-strength-slider", "value")]
        )
        def update_game_plots(start_clicks, stop_clicks, save_clicks, 
                             emergence_rate, quantum_coupling, void_strength):
            ctx = callback_context
            if not ctx.triggered:
                return self.create_empty_plots() + (False, True, True)
            
            button_id = ctx.triggered[0]["prop_id"].split(".")[0]
            
            if button_id == "start-universe-btn":
                # Start universe simulation
                self.game_state['is_running'] = True
                self.game_state['emergence_rate'] = emergence_rate
                self.game_state['quantum_coupling'] = quantum_coupling
                self.game_state['void_strength'] = void_strength
                
                # Run simulation
                results = self._run_universe_simulation()
                
                # Create plots
                evolution_plot = self.create_universe_evolution_plot(results)
                distribution_plot = self.create_particle_distribution_plot(results)
                entropy_plot = self.create_entropy_evolution_plot(results)
                
                return evolution_plot, distribution_plot, entropy_plot, True, False, False
                
            elif button_id == "stop-universe-btn":
                # Stop simulation
                self.game_state['is_running'] = False
                return self.create_empty_plots() + (False, True, True)
                
            elif button_id == "save-universe-btn":
                # Save universe
                self._save_universe()
                return self.create_empty_plots() + (False, True, True)
            
            return self.create_empty_plots() + (False, True, True)
    
    def create_potential_function(self, potential_type: str, depth: float, 
                                 width: float, coupling: float):
        """Create potential function based on type."""
        if potential_type == 'double_well':
            def potential(x):
                return (coupling / 4) * (x**2 - depth**2)**2
        elif potential_type == 'harmonic':
            def potential(x):
                return 0.5 * depth * x**2
        elif potential_type == 'step_barrier':
            def potential(x):
                return depth * (np.abs(x) < width).astype(float)
        else:  # mexican_hat
            def potential(x):
                return depth * (x**2 - width**2)**2 / (2 * width**4)
        
        return potential
    
    def create_wave_function_plot(self, psi_trajectory: np.ndarray, 
                                 x_grid: np.ndarray, time_array: np.ndarray):
        """Create wave function evolution plot."""
        fig = go.Figure()
        
        # Plot probability density |ψ|²
        psi_density = np.abs(psi_trajectory)**2
        
        fig.add_trace(go.Heatmap(
            z=psi_density,
            x=x_grid,
            y=time_array,
            colorscale='Viridis',
            name='|ψ|²'
        ))
        
        fig.update_layout(
            title="Wave Function Evolution |ψ(x,t)|²",
            xaxis_title="Position (x)",
            yaxis_title="Time (t)",
            height=400
        )
        
        return fig
    
    def create_probability_current_plot(self, psi_trajectory: np.ndarray,
                                      x_grid: np.ndarray, time_array: np.ndarray):
        """Create probability current plot."""
        fig = go.Figure()
        
        # Calculate probability current for each time step
        current_data = []
        for i, psi in enumerate(psi_trajectory):
            dx = x_grid[1] - x_grid[0]
            dpsi_dx = np.gradient(psi, dx)
            j = (1 / (2 * 1j)) * (np.conj(psi) * dpsi_dx - psi * np.conj(dpsi_dx))
            current_data.append(j.real)
        
        current_data = np.array(current_data)
        
        fig.add_trace(go.Heatmap(
            z=current_data,
            x=x_grid,
            y=time_array,
            colorscale='RdBu',
            name='Probability Current'
        ))
        
        fig.update_layout(
            title="Probability Current j(x,t)",
            xaxis_title="Position (x)",
            yaxis_title="Time (t)",
            height=400
        )
        
        return fig
    
    def create_energy_eigenvalues_plot(self, solver):
        """Create energy eigenvalues plot."""
        from ..quantum.operators import EnergyOperator, OperatorParameters
        
        op_params = OperatorParameters(
            mass=solver.mass,
            hbar=solver.hbar,
            potential=solver.params.potential,
            grid_spacing=solver.dx
        )
        energy_op = EnergyOperator(op_params)
        
        eigenvalues, eigenfunctions = energy_op.solve_eigenvalues(solver.x_grid, n_states=10)
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=list(range(len(eigenvalues))),
            y=eigenvalues,
            name='Energy Eigenvalues'
        ))
        
        fig.update_layout(
            title="Energy Eigenvalues",
            xaxis_title="Eigenstate (n)",
            yaxis_title="Energy (E)",
            height=400
        )
        
        return fig
    
    def create_field_evolution_plot(self, field_trajectory: np.ndarray, x_grid: np.ndarray):
        """Create field evolution plot for Klein-Gordon."""
        fig = go.Figure()
        
        field_amplitude = np.abs(field_trajectory)
        
        fig.add_trace(go.Heatmap(
            z=field_amplitude,
            x=x_grid,
            y=list(range(len(field_trajectory))),
            colorscale='Viridis',
            name='Field Amplitude'
        ))
        
        fig.update_layout(
            title="Klein-Gordon Field Evolution",
            xaxis_title="Position (x)",
            yaxis_title="Time Step",
            height=400
        )
        
        return fig
    
    def create_empty_plots(self):
        """Create empty plots for initial state."""
        empty_plot = go.Figure()
        empty_plot.update_layout(
            title="Click 'Run Simulation' to start",
            height=400
        )
        return empty_plot, empty_plot, empty_plot
    
    def create_empty_plot(self, title: str):
        """Create single empty plot."""
        fig = go.Figure()
        fig.update_layout(
            title=title,
            height=400
        )
        return fig
    
    def _run_universe_simulation(self):
        """Run universe simulation for game mode."""
        try:
            # Set up field parameters
            field_params = FieldParameters(
                mass=1.0,
                hbar=1.0,
                c=1.0,
                coupling=self.game_state['quantum_coupling'],
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
            
            # Run simulation
            n_steps = 150
            for step in range(n_steps):
                # Particle emergence from void
                if np.random.random() < self.game_state['emergence_rate']:
                    k_random = np.random.uniform(-2.0, 2.0)
                    amplitude = self.game_state['void_strength'] * np.random.uniform(0.5, 1.5)
                    
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
                entropy_values.append(observables['field_variance'])
                field_evolution.append(quantum_field.field.copy())
            
            # Calculate final metrics
            self.game_state['particles_created'] = particle_counts[-1]
            self.game_state['entropy'] = entropy_values[-1]
            self.game_state['score'] = self._calculate_score(
                self.game_state['particles_created'], 
                len(creation_events), 
                self.game_state['entropy'], 
                energy_values[-1]
            )
            
            return {
                'particle_counts': particle_counts,
                'energy_values': energy_values,
                'entropy_values': entropy_values,
                'field_evolution': field_evolution,
                'creation_events': creation_events,
                'time_steps': list(range(n_steps))
            }
            
        except Exception as e:
            print(f"Error in universe simulation: {e}")
            return {
                'particle_counts': [0],
                'energy_values': [0],
                'entropy_values': [0],
                'field_evolution': [np.zeros(256)],
                'creation_events': [],
                'time_steps': [0]
            }
    
    def _calculate_score(self, particles, events, entropy, energy):
        """Calculate game score."""
        alpha = 10.0  # Particle bonus
        beta = 5.0    # Event bonus
        gamma = 2.0   # Entropy bonus
        delta = 0.01  # Energy penalty
        
        score = (alpha * particles + 
                beta * events + 
                gamma * entropy - 
                delta * energy)
        
        return max(0, score)
    
    def _save_universe(self):
        """Save universe configuration."""
        try:
            universe_data = {
                'score': self.game_state['score'],
                'particles_created': self.game_state['particles_created'],
                'entropy': self.game_state['entropy'],
                'parameters': {
                    'emergence_rate': self.game_state['emergence_rate'],
                    'quantum_coupling': self.game_state['quantum_coupling'],
                    'void_strength': self.game_state['void_strength']
                },
                'timestamp': time.time()
            }
            
            # Save to universes directory
            universes_dir = Path("universes")
            universes_dir.mkdir(exist_ok=True)
            
            filename = f"quantum_universe_{self.game_state['score']:.1f}.json"
            filepath = universes_dir / filename
            
            with open(filepath, 'w') as f:
                json.dump(universe_data, f, indent=2)
            
            print(f"Universe saved to {filepath}")
            
        except Exception as e:
            print(f"Error saving universe: {e}")
    
    def create_universe_evolution_plot(self, results):
        """Create universe evolution plot."""
        fig = go.Figure()
        
        # Plot particle count evolution
        fig.add_trace(go.Scatter(
            x=results['time_steps'],
            y=results['particle_counts'],
            mode='lines',
            name='Particles',
            line=dict(color='blue', width=2)
        ))
        
        fig.update_layout(
            title="Universe Evolution",
            xaxis_title="Time Step",
            yaxis_title="Number of Particles",
            height=400
        )
        
        return fig
    
    def create_particle_distribution_plot(self, results):
        """Create particle distribution plot."""
        fig = go.Figure()
        
        # Plot energy evolution
        fig.add_trace(go.Scatter(
            x=results['time_steps'],
            y=results['energy_values'],
            mode='lines',
            name='Total Energy',
            line=dict(color='red', width=2)
        ))
        
        fig.update_layout(
            title="Energy Evolution",
            xaxis_title="Time Step",
            yaxis_title="Total Energy",
            height=400
        )
        
        return fig
    
    def create_entropy_evolution_plot(self, results):
        """Create entropy evolution plot."""
        fig = go.Figure()
        
        # Plot entropy evolution
        fig.add_trace(go.Scatter(
            x=results['time_steps'],
            y=results['entropy_values'],
            mode='lines',
            name='Entropy',
            line=dict(color='green', width=2)
        ))
        
        fig.update_layout(
            title="Entropy Evolution",
            xaxis_title="Time Step",
            yaxis_title="Entropy (Field Variance)",
            height=400
        )
        
        return fig
    
    def run(self, debug=True, port=8050):
        """Run the dashboard."""
        self.app.run(debug=debug, port=port)


def main():
    """Main function to run the dashboard."""
    dashboard = QuantumDashboard()
    dashboard.run()


if __name__ == "__main__":
    main()
