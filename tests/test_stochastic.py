"""
Tests for stochastic dynamics in void physics.
"""

import numpy as np
import pytest

from src.void_physic.core.potential import DoubleWellPotential
from src.void_physic.core.stochastic import ColoredNoise, LangevinDynamics, WhiteNoise


class TestWhiteNoise:
    """Test white noise functionality."""

    def test_noise_generation(self):
        """Test white noise generation."""
        noise = WhiteNoise(strength=1.0, seed=42)

        # Generate noise
        t = np.linspace(0, 10, 100)
        dt = t[1] - t[0]
        noise_values = noise.generate(t, dt)

        # Check that noise has correct length
        assert len(noise_values) == len(t)

        # Check that noise is approximately zero mean
        mean_noise = np.mean(noise_values)
        assert abs(mean_noise) < 0.5  # Should be small for large sample

    def test_noise_variance(self):
        """Test noise variance."""
        noise = WhiteNoise(strength=2.0, seed=42)

        # Generate noise
        t = np.linspace(0, 10, 1000)
        dt = t[1] - t[0]
        noise_values = noise.generate(t, dt)

        # Check variance (should be approximately 2D/dt)
        expected_variance = 2 * noise.strength / dt
        actual_variance = np.var(noise_values)

        # Allow for some statistical fluctuation
        assert abs(actual_variance - expected_variance) / expected_variance < 0.2

    def test_power_spectrum(self):
        """Test power spectrum calculation."""
        noise = WhiteNoise(strength=1.0)

        frequencies = np.linspace(0, 10, 100)
        power_spectrum = noise.power_spectrum(frequencies)

        # White noise should have flat power spectrum
        assert np.allclose(power_spectrum, 2 * noise.strength)

    def test_correlation_function(self):
        """Test correlation function calculation."""
        noise = WhiteNoise(strength=1.0)

        tau = np.linspace(-1, 1, 100)
        correlation = noise.correlation_function(tau)

        # At tau = 0, correlation should be maximum
        max_correlation = np.max(correlation)
        assert max_correlation > 0

        # At tau != 0, correlation should be zero (approximately)
        # Use a more reasonable tolerance for the Dirac delta approximation
        # Only check values that are clearly non-zero tau
        non_zero_tau = tau[np.abs(tau) > 0.05]  # Only check tau values > 0.05
        non_zero_correlation = correlation[np.abs(tau) > 0.05]
        assert np.allclose(non_zero_correlation, 0, atol=0.1)


class TestColoredNoise:
    """Test colored noise functionality."""

    def test_noise_generation(self):
        """Test colored noise generation."""
        noise = ColoredNoise(
            strength=1.0, spectral_index=1.0, correlation_time=1.0, seed=42
        )

        # Generate noise
        t = np.linspace(0, 10, 100)
        dt = t[1] - t[0]
        noise_values = noise.generate(t, dt)

        # Check that noise has correct length
        assert len(noise_values) == len(t)

        # Check that noise is approximately zero mean
        mean_noise = np.mean(noise_values)
        assert abs(mean_noise) < 0.5

    def test_power_spectrum(self):
        """Test power spectrum calculation."""
        noise = ColoredNoise(strength=1.0, spectral_index=1.0, correlation_time=1.0)

        frequencies = np.linspace(0, 10, 100)
        power_spectrum = noise.power_spectrum(frequencies)

        # Power spectrum should decrease with frequency
        assert power_spectrum[0] > power_spectrum[-1]

    def test_correlation_function(self):
        """Test correlation function calculation."""
        noise = ColoredNoise(strength=1.0, spectral_index=1.0, correlation_time=1.0)

        tau = np.linspace(0, 5, 100)
        correlation = noise.correlation_function(tau)

        # Correlation should decrease with tau
        assert correlation[0] > correlation[-1]

        # Correlation should be positive
        assert np.all(correlation >= 0)


class TestLangevinDynamics:
    """Test Langevin dynamics functionality."""

    def test_drift_term(self):
        """Test drift term calculation."""
        potential = DoubleWellPotential()
        dynamics = LangevinDynamics(potential)

        # Test drift at critical points
        phi_values = np.array([0.0, 1.0, -1.0])
        drift = dynamics.drift_term(phi_values)

        # At critical points, drift should be zero
        assert np.allclose(drift, 0, atol=1e-10)

    def test_diffusion_term(self):
        """Test diffusion term calculation."""
        potential = DoubleWellPotential()
        noise = WhiteNoise(strength=1.0, seed=42)
        dynamics = LangevinDynamics(potential, noise)

        # Generate diffusion term
        t = np.linspace(0, 10, 100)
        dt = t[1] - t[0]
        diffusion = dynamics.diffusion_term(t, dt)

        # Check that diffusion has correct length
        assert len(diffusion) == len(t)

    def test_langevin_equation(self):
        """Test complete Langevin equation."""
        potential = DoubleWellPotential()
        noise = WhiteNoise(strength=1.0, seed=42)
        dynamics = LangevinDynamics(potential, noise)

        # Test at critical point
        phi = np.array([0.0])
        t = np.array([0.0])
        dt = 0.01

        dphi_dt = dynamics.langevin_equation(phi, t, dt)

        # At critical point, drift should be zero, only diffusion remains
        assert len(dphi_dt) == 1

    def test_stationary_distribution(self):
        """Test stationary distribution calculation."""
        potential = DoubleWellPotential()
        noise = WhiteNoise(strength=1.0)
        dynamics = LangevinDynamics(potential, noise)

        # Calculate stationary distribution
        phi = np.linspace(-2, 2, 100)
        stationary = dynamics.stationary_distribution(phi)

        # Check that distribution is normalized
        integral = np.trapz(stationary, phi)
        assert abs(integral - 1.0) < 1e-6

        # Check that distribution is positive
        assert np.all(stationary >= 0)

    def test_escape_rate(self):
        """Test escape rate calculation."""
        potential = DoubleWellPotential()
        noise = WhiteNoise(strength=1.0)
        dynamics = LangevinDynamics(potential, noise)

        # Calculate escape rate (from stable minimum to another stable minimum)
        escape_rate = dynamics.escape_rate(phi_initial=-1.0, phi_final=1.0)

        # Escape rate should be positive
        assert escape_rate > 0

        # Should be finite
        assert np.isfinite(escape_rate)

    def test_first_passage_time_distribution(self):
        """Test first passage time distribution calculation."""
        potential = DoubleWellPotential()
        noise = WhiteNoise(strength=1.0, seed=42)
        dynamics = LangevinDynamics(potential, noise)

        # Calculate first passage time distribution
        t, fpt_times = dynamics.first_passage_time_distribution(
            phi_initial=0.0, phi_threshold=0.5, n_trajectories=100, t_max=10.0, dt=0.01
        )

        # Check that we have the right number of trajectories
        assert len(fpt_times) == 100

        # Check that some trajectories have finite FPT
        finite_fpt = fpt_times[fpt_times != np.inf]
        assert len(finite_fpt) > 0

        # Check that finite FPTs are positive
        assert np.all(finite_fpt > 0)


if __name__ == "__main__":
    pytest.main([__file__])
