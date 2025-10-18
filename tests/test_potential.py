"""
Tests for potential functions in void physics.
"""

import numpy as np
import pytest

from src.void_physic.core.potential import (
    DoubleWellPotential,
    MexicanHatPotential,
    PotentialParameters,
)


class TestDoubleWellPotential:
    """Test double-well potential functionality."""

    def test_potential_evaluation(self):
        """Test potential evaluation at various points."""
        potential = DoubleWellPotential()

        # Test at critical points
        phi_values = np.array([0.0, 1.0, -1.0])
        V_values = potential(phi_values)

        # Check that potential is positive
        assert np.all(V_values >= 0)

        # Check symmetry: V(φ) = V(-φ)
        assert abs(V_values[1] - V_values[2]) < 1e-10

    def test_gradient_calculation(self):
        """Test gradient calculation."""
        potential = DoubleWellPotential()

        # Test gradient at critical points
        phi_values = np.array([0.0, 1.0, -1.0])
        gradients = potential.gradient(phi_values)

        # At critical points, gradient should be zero
        assert abs(gradients[0]) < 1e-10  # φ = 0
        assert abs(gradients[1]) < 1e-10  # φ = v
        assert abs(gradients[2]) < 1e-10  # φ = -v

    def test_hessian_calculation(self):
        """Test Hessian (second derivative) calculation."""
        potential = DoubleWellPotential()

        # Test Hessian at critical points
        phi_values = np.array([0.0, 1.0, -1.0])
        hessians = potential.hessian(phi_values)

        # At φ = 0, should be negative (unstable)
        assert hessians[0] < 0

        # At φ = ±v, should be positive (stable)
        assert hessians[1] > 0
        assert hessians[2] > 0

    def test_critical_points(self):
        """Test critical point identification."""
        potential = DoubleWellPotential()
        critical_points = potential.critical_points()

        # Should have three critical points
        assert len(critical_points) == 3
        assert "symmetric" in critical_points
        assert "positive_vacuum" in critical_points
        assert "negative_vacuum" in critical_points

        # Check values
        assert critical_points["symmetric"] == 0.0
        assert critical_points["positive_vacuum"] == 1.0
        assert critical_points["negative_vacuum"] == -1.0

    def test_stability_analysis(self):
        """Test stability analysis."""
        potential = DoubleWellPotential()
        stability = potential.stability_analysis()

        # Check stability types
        assert stability["symmetric"]["type"] == "unstable"
        assert stability["positive_vacuum"]["type"] == "stable"
        assert stability["negative_vacuum"]["type"] == "stable"

    def test_barrier_height(self):
        """Test barrier height calculation."""
        potential = DoubleWellPotential()
        barrier_height = potential.barrier_height()

        # Barrier height should be positive
        assert barrier_height > 0

        # Should equal V(0) - V(±v)
        V_symmetric = potential(np.array([0.0]))[0]
        V_vacuum = potential(np.array([1.0]))[0]
        expected_height = V_symmetric - V_vacuum

        assert abs(barrier_height - expected_height) < 1e-10

    def test_effective_mass(self):
        """Test effective mass calculation."""
        potential = DoubleWellPotential()

        # At vacuum, effective mass should be positive
        mass_vacuum = potential.effective_mass(1.0)
        assert mass_vacuum > 0

        # At symmetric point, effective mass should be negative
        mass_symmetric = potential.effective_mass(0.0)
        assert mass_symmetric < 0

    def test_parameter_variation(self):
        """Test potential with different parameters."""
        params = PotentialParameters(lambda_coupling=2.0, v_vev=1.5, V0_offset=0.1)
        potential = DoubleWellPotential(params)

        # Test critical points with new parameters
        critical_points = potential.critical_points()
        assert critical_points["positive_vacuum"] == 1.5
        assert critical_points["negative_vacuum"] == -1.5

        # Test potential value at offset
        V_at_vacuum = potential(np.array([1.5]))[0]
        assert abs(V_at_vacuum - 0.1) < 1e-10


class TestMexicanHatPotential:
    """Test Mexican-hat potential functionality."""

    def test_potential_evaluation(self):
        """Test potential evaluation for complex field."""
        potential = MexicanHatPotential()

        # Test at symmetric point
        phi_real = np.array([0.0])
        phi_imag = np.array([0.0])
        V_symmetric = potential(phi_real, phi_imag)

        # Test at vacuum point
        phi_real = np.array([1.0])
        phi_imag = np.array([0.0])
        V_vacuum = potential(phi_real, phi_imag)

        # Vacuum should have lower potential
        assert V_vacuum[0] < V_symmetric[0]

    def test_gradient_calculation(self):
        """Test gradient calculation for complex field."""
        potential = MexicanHatPotential()

        # Test gradient at symmetric point
        phi_real = np.array([0.0])
        phi_imag = np.array([0.0])
        grad_real = potential.gradient_real(phi_real, phi_imag)
        grad_imag = potential.gradient_imag(phi_real, phi_imag)

        # At symmetric point, gradients should be zero
        assert abs(grad_real[0]) < 1e-10
        assert abs(grad_imag[0]) < 1e-10

    def test_vacuum_manifold(self):
        """Test vacuum manifold generation."""
        potential = MexicanHatPotential()
        phi_real, phi_imag = potential.vacuum_manifold(n_points=100)

        # Check that all points are on the circle |φ| = v
        phi_magnitude = np.sqrt(phi_real**2 + phi_imag**2)
        assert np.allclose(phi_magnitude, 1.0, atol=1e-10)

        # Check that we have the right number of points
        assert len(phi_real) == 100
        assert len(phi_imag) == 100


class TestPotentialParameters:
    """Test potential parameters functionality."""

    def test_default_parameters(self):
        """Test default parameter values."""
        params = PotentialParameters()

        assert params.lambda_coupling == 1.0
        assert params.v_vev == 1.0
        assert params.V0_offset == 0.0
        assert params.mass_squared == 0.0

    def test_custom_parameters(self):
        """Test custom parameter values."""
        params = PotentialParameters(
            lambda_coupling=2.0, v_vev=1.5, V0_offset=0.1, mass_squared=0.5
        )

        assert params.lambda_coupling == 2.0
        assert params.v_vev == 1.5
        assert params.V0_offset == 0.1
        assert params.mass_squared == 0.5


if __name__ == "__main__":
    pytest.main([__file__])
