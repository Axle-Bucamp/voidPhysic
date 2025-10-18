"""
Tests for simulation modules in void physics.
"""

import numpy as np
import pytest

from src.void_physic.core.potential import DoubleWellPotential
from src.void_physic.core.stochastic import LangevinDynamics, WhiteNoise
from src.void_physic.simulation.langevin_solver import LangevinSolver, SolverParameters
from src.void_physic.simulation.statistics import EntropyCalculator, FirstPassageTime
from src.void_physic.utils.constants import PhysicalConstants


class TestLangevinSolver:
    """Test Langevin solver functionality."""

    def setup_method(self):
        """Set up test fixtures."""
        self.potential = DoubleWellPotential()
        self.noise = WhiteNoise(strength=1.0, seed=42)
        self.dynamics = LangevinDynamics(self.potential, self.noise)
        self.solver = LangevinSolver(self.dynamics)
        self.params = SolverParameters(
            dt=0.01, t_max=10.0, n_trajectories=100, save_trajectories=True
        )

    def test_euler_maruyama(self):
        """Test Euler-Maruyama integration."""
        t, phi = self.solver.euler_maruyama(phi0=0.0, params=self.params)

        # Check that we have the right number of time points (allow for floating point precision)
        expected_points = int(self.params.t_max / self.params.dt) + 1
        assert abs(len(t) - expected_points) <= 1
        assert abs(len(phi) - expected_points) <= 1

        # Check that time array is correct
        assert t[0] == 0.0
        assert abs(t[-1] - self.params.t_max) < self.params.dt

        # Check that field starts at initial value
        assert abs(phi[0] - 0.0) < 1e-10

    def test_milstein(self):
        """Test Milstein integration."""
        t, phi = self.solver.milstein(phi0=0.0, params=self.params)

        # Check basic properties
        assert len(t) == len(phi)
        assert t[0] == 0.0
        assert abs(phi[0] - 0.0) < 1e-10

    def test_runge_kutta_stochastic(self):
        """Test stochastic Runge-Kutta integration."""
        t, phi = self.solver.runge_kutta_stochastic(phi0=0.0, params=self.params)

        # Check basic properties
        assert len(t) == len(phi)
        assert t[0] == 0.0
        assert abs(phi[0] - 0.0) < 1e-10

    def test_ensemble_simulation(self):
        """Test ensemble simulation."""
        results = self.solver.ensemble_simulation(phi0=0.0, params=self.params)

        # Check that we have all required keys
        required_keys = [
            "time",
            "mean_field",
            "std_field",
            "var_field",
            "mean_energy",
            "std_energy",
        ]
        for key in required_keys:
            assert key in results

        # Check that trajectories are saved if requested
        if self.params.save_trajectories:
            assert "trajectories" in results
            assert results["trajectories"].shape == (
                self.params.n_trajectories,
                len(results["time"]),
            )

        # Check that mean field starts at initial value
        assert abs(results["mean_field"][0] - 0.0) < 1e-10

        # Check that variance is non-negative
        assert np.all(results["var_field"] >= 0)

    def test_first_passage_analysis(self):
        """Test first passage time analysis."""
        results = self.solver.first_passage_analysis(
            phi0=0.0, threshold=0.5, params=self.params
        )

        # Check that we have all required keys
        required_keys = [
            "first_passage_times",
            "mean_fpt",
            "std_fpt",
            "median_fpt",
            "survival_probability",
        ]
        for key in required_keys:
            assert key in results

        # Check that we have the right number of FPTs
        assert len(results["first_passage_times"]) == self.params.n_trajectories

        # Check that survival probability is between 0 and 1
        assert 0 <= results["survival_probability"] <= 1

    def test_energy_evolution(self):
        """Test energy evolution calculation."""
        results = self.solver.energy_evolution(phi0=0.0, params=self.params)

        # Check that we have all required keys
        required_keys = [
            "time",
            "field",
            "kinetic_energy",
            "potential_energy",
            "total_energy",
            "entropy_proxy",
        ]
        for key in required_keys:
            assert key in results

        # Check that energy components are non-negative
        assert np.all(results["kinetic_energy"] >= 0)
        assert np.all(results["potential_energy"] >= 0)
        assert np.all(results["total_energy"] >= 0)

        # Check that total energy equals kinetic + potential
        total_energy_calc = results["kinetic_energy"] + results["potential_energy"]
        assert np.allclose(results["total_energy"], total_energy_calc)


class TestFirstPassageTime:
    """Test first passage time analysis functionality."""

    def setup_method(self):
        """Set up test fixtures."""
        self.fpt_analyzer = FirstPassageTime()

    def test_fit_exponential_distribution(self):
        """Test exponential distribution fitting."""
        # Generate synthetic FPT data
        np.random.seed(42)
        fpt_times = np.random.exponential(scale=2.0, size=1000)

        # Fit exponential distribution
        fit_results = self.fpt_analyzer.fit_exponential_distribution(fpt_times)

        # Check that fit was successful
        assert fit_results["fit_success"]
        assert fit_results["rate"] > 0
        assert fit_results["mean"] > 0
        assert fit_results["p_value"] > 0.05  # Good fit

    def test_fit_weibull_distribution(self):
        """Test Weibull distribution fitting."""
        # Generate synthetic FPT data
        np.random.seed(42)
        fpt_times = np.random.weibull(a=2.0, size=1000)

        # Fit Weibull distribution
        fit_results = self.fpt_analyzer.fit_weibull_distribution(fpt_times)

        # Check that fit was successful
        assert fit_results["fit_success"]
        assert fit_results["shape"] > 0
        assert fit_results["scale"] > 0
        assert fit_results["p_value"] > 0.05  # Good fit

    def test_survival_function(self):
        """Test survival function calculation."""
        # Generate synthetic FPT data
        np.random.seed(42)
        fpt_times = np.random.exponential(scale=2.0, size=1000)

        # Calculate survival function
        time_points = np.linspace(0, 10, 100)
        survival = self.fpt_analyzer.survival_function(fpt_times, time_points)

        # Check that survival function is decreasing
        assert np.all(np.diff(survival) <= 0)

        # Check that survival function is between 0 and 1
        assert np.all(survival >= 0)
        assert np.all(survival <= 1)

        # Check that survival function starts at 1
        assert abs(survival[0] - 1.0) < 1e-10

    def test_hazard_function(self):
        """Test hazard function calculation."""
        # Generate synthetic FPT data
        np.random.seed(42)
        fpt_times = np.random.exponential(scale=2.0, size=1000)

        # Calculate hazard function
        time_points = np.linspace(0, 10, 100)
        hazard = self.fpt_analyzer.hazard_function(fpt_times, time_points)

        # Check that hazard function is non-negative
        assert np.all(hazard >= 0)

        # For exponential distribution, hazard should be constant
        # (allowing for statistical fluctuations)
        hazard_std = np.std(hazard)
        assert hazard_std < 1.0  # Should be relatively constant

    def test_confidence_intervals(self):
        """Test confidence interval calculation."""
        # Generate synthetic FPT data
        np.random.seed(42)
        fpt_times = np.random.exponential(scale=2.0, size=1000)

        # Calculate confidence intervals
        ci_results = self.fpt_analyzer.confidence_intervals(fpt_times)

        # Check that we have all required keys
        required_keys = ["mean_lower", "mean_upper", "mean_estimate", "std_estimate"]
        for key in required_keys:
            assert key in ci_results

        # Check that confidence interval bounds are reasonable
        assert ci_results["mean_lower"] < ci_results["mean_estimate"]
        assert ci_results["mean_upper"] > ci_results["mean_estimate"]
        assert ci_results["std_estimate"] > 0


class TestEntropyCalculator:
    """Test entropy calculator functionality."""

    def setup_method(self):
        """Set up test fixtures."""
        self.entropy_calc = EntropyCalculator()

        # Generate synthetic trajectory data
        np.random.seed(42)
        self.n_trajectories = 100
        self.n_times = 50
        self.phi_trajectories = np.random.normal(
            0, 1, (self.n_trajectories, self.n_times)
        )
        self.time_points = np.linspace(0, 10, self.n_times)

    def test_field_entropy(self):
        """Test field entropy calculation."""
        entropy = self.entropy_calc.field_entropy(
            self.phi_trajectories, self.time_points
        )

        # Check that entropy has correct length
        assert len(entropy) == self.n_times

        # Check that entropy is non-negative
        assert np.all(entropy >= 0)

        # Check that entropy is finite
        assert np.all(np.isfinite(entropy))

    def test_mutual_information(self):
        """Test mutual information calculation."""
        # Create two field components
        phi1_trajectories = self.phi_trajectories
        phi2_trajectories = self.phi_trajectories + 0.5 * np.random.normal(
            0, 1, self.phi_trajectories.shape
        )

        mutual_info = self.entropy_calc.mutual_information(
            phi1_trajectories, phi2_trajectories, self.time_points
        )

        # Check that mutual information has correct length
        assert len(mutual_info) == self.n_times

        # Check that mutual information is non-negative
        assert np.all(mutual_info >= 0)

        # Check that mutual information is finite
        assert np.all(np.isfinite(mutual_info))

    def test_entropy_production_rate(self):
        """Test entropy production rate calculation."""
        # Create synthetic entropy data
        entropy = np.log(1 + self.time_points)

        entropy_rate = self.entropy_calc.entropy_production_rate(
            entropy, self.time_points
        )

        # Check that entropy rate has correct length
        assert len(entropy_rate) == len(entropy)

        # Check that entropy rate is finite
        assert np.all(np.isfinite(entropy_rate))

    def test_thermodynamic_quantities(self):
        """Test thermodynamic quantities calculation."""
        potential = DoubleWellPotential()

        thermo_quantities = self.entropy_calc.thermodynamic_quantities(
            self.phi_trajectories, self.time_points, potential
        )

        # Check that we have all required keys
        required_keys = [
            "time",
            "entropy",
            "entropy_rate",
            "mean_energy",
            "mean_potential",
            "temperature",
            "free_energy",
            "mean_field",
            "field_variance",
        ]
        for key in required_keys:
            assert key in thermo_quantities

        # Check that all quantities have correct length
        for key in required_keys:
            assert len(thermo_quantities[key]) == self.n_times

        # Check that entropy is non-negative
        assert np.all(thermo_quantities["entropy"] >= 0)

        # Check that temperature is non-negative
        assert np.all(thermo_quantities["temperature"] >= 0)

        # Check that field variance is non-negative
        assert np.all(thermo_quantities["field_variance"] >= 0)

    def test_phase_transition_indicators(self):
        """Test phase transition indicators calculation."""
        indicators = self.entropy_calc.phase_transition_indicators(
            self.phi_trajectories, self.time_points
        )

        # Check that we have all required keys
        required_keys = [
            "time",
            "order_parameter",
            "susceptibility",
            "binder_cumulant",
            "correlation_length",
        ]
        for key in required_keys:
            assert key in indicators

        # Check that all indicators have correct length
        for key in required_keys:
            assert len(indicators[key]) == self.n_times

        # Check that susceptibility is non-negative
        assert np.all(indicators["susceptibility"] >= 0)

        # Check that correlation length is non-negative
        assert np.all(indicators["correlation_length"] >= 0)


if __name__ == "__main__":
    pytest.main([__file__])
