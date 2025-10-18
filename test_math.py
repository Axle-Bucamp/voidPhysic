#!/usr/bin/env python3
"""
Test script to verify the mathematical foundations of void physics.

This script tests the core mathematical components to ensure they work correctly.
"""

import sys
import logging
import numpy as np
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_imports():
    """Test that all modules can be imported correctly."""
    logger.info("Testing imports...")
    
    try:
        from void_physic.core.potential import DoubleWellPotential, PotentialParameters
        from void_physic.core.stochastic import LangevinDynamics, WhiteNoise
        from void_physic.simulation.langevin_solver import LangevinSolver, SolverParameters
        from void_physic.utils.constants import PhysicalConstants
        logger.info("All imports successful")
        return True
    except ImportError as e:
        logger.error(f"Import failed: {e}")
        return False

def test_potential_math():
    """Test the mathematical properties of the double-well potential."""
    logger.info("Testing potential mathematics...")
    
    try:
        from void_physic.core.potential import DoubleWellPotential, PotentialParameters
        
        # Create potential with default parameters
        potential = DoubleWellPotential()
        
        # Test potential evaluation
        phi_values = np.array([0.0, 1.0, -1.0, 0.5, -0.5])
        V_values = potential(phi_values)
        
        # Check that potential is non-negative
        assert np.all(V_values >= 0), "Potential should be non-negative"
        logger.info("Potential is non-negative")
        
        # Test gradient calculation
        gradients = potential.gradient(phi_values)
        logger.info(f" Gradients calculated: {gradients}")
        
        # Test Hessian calculation
        hessians = potential.hessian(phi_values)
        logger.info(f" Hessians calculated: {hessians}")
        
        # Test critical points
        critical_points = potential.critical_points()
        logger.info(f" Critical points: {critical_points}")
        
        # Test stability analysis
        stability = potential.stability_analysis()
        logger.info(f" Stability analysis: {stability}")
        
        # Test barrier height
        barrier_height = potential.barrier_height()
        logger.info(f" Barrier height: {barrier_height}")
        
        return True
        
    except Exception as e:
        logger.error(f" Potential math test failed: {e}")
        return False

def test_stochastic_math():
    """Test the stochastic dynamics mathematics."""
    logger.info("Testing stochastic mathematics...")
    
    try:
        from void_physic.core.potential import DoubleWellPotential
        from void_physic.core.stochastic import LangevinDynamics, WhiteNoise
        from void_physic.utils.constants import PhysicalConstants
        
        # Set up components
        potential = DoubleWellPotential()
        noise = WhiteNoise(strength=1.0, seed=42)
        constants = PhysicalConstants()
        dynamics = LangevinDynamics(potential, noise, constants)
        
        # Test noise generation
        t = np.linspace(0, 10, 100)
        dt = t[1] - t[0]
        noise_values = noise.generate(t, dt)
        
        # Check noise properties
        assert len(noise_values) == len(t), "Noise should have same length as time array"
        logger.info(f" Noise generated: mean={np.mean(noise_values):.3f}, std={np.std(noise_values):.3f}")
        
        # Test drift term
        phi_values = np.array([0.0, 1.0, -1.0])
        drift = dynamics.drift_term(phi_values)
        logger.info(f" Drift terms: {drift}")
        
        # Test Langevin equation
        dphi_dt = dynamics.langevin_equation(phi_values, t[:3], dt)
        logger.info(f" Langevin equation: {dphi_dt}")
        
        return True
        
    except Exception as e:
        logger.error(f" Stochastic math test failed: {e}")
        return False

def test_numerical_solver():
    """Test the numerical solver."""
    logger.info("Testing numerical solver...")
    
    try:
        from void_physic.core.potential import DoubleWellPotential
        from void_physic.core.stochastic import LangevinDynamics, WhiteNoise
        from void_physic.simulation.langevin_solver import LangevinSolver, SolverParameters
        from void_physic.utils.constants import PhysicalConstants
        
        # Set up components
        potential = DoubleWellPotential()
        noise = WhiteNoise(strength=0.5, seed=42)
        constants = PhysicalConstants()
        dynamics = LangevinDynamics(potential, noise, constants)
        solver = LangevinSolver(dynamics, constants)
        
        # Set up solver parameters
        params = SolverParameters(
            dt=0.01,
            t_max=5.0,
            n_trajectories=10,  # Small number for testing
            save_trajectories=True
        )
        
        # Test Euler-Maruyama integration
        t, phi = solver.euler_maruyama(phi0=0.0, params=params)
        
        # Check results
        assert len(t) == len(phi), "Time and field arrays should have same length"
        assert abs(phi[0] - 0.0) < 1e-10, "Field should start at initial value"
        logger.info(f" Euler-Maruyama integration: {len(t)} time points")
        
        # Test ensemble simulation
        results = solver.ensemble_simulation(phi0=0.0, params=params)
        
        # Check ensemble results
        assert 'mean_field' in results, "Should have mean field"
        assert 'std_field' in results, "Should have std field"
        assert 'trajectories' in results, "Should have trajectories"
        logger.info(f" Ensemble simulation: {results['trajectories'].shape[0]} trajectories")
        
        return True
        
    except Exception as e:
        logger.error(f" Numerical solver test failed: {e}")
        return False

def test_entropy_calculation():
    """Test entropy calculation."""
    logger.info("Testing entropy calculation...")
    
    try:
        from void_physic.simulation.statistics import EntropyCalculator
        
        # Create synthetic trajectory data
        np.random.seed(42)
        n_trajectories = 50
        n_times = 20
        phi_trajectories = np.random.normal(0, 1, (n_trajectories, n_times))
        time_points = np.linspace(0, 10, n_times)
        
        # Test entropy calculation
        entropy_calc = EntropyCalculator()
        entropy = entropy_calc.field_entropy(phi_trajectories, time_points)
        
        # Check entropy properties
        assert len(entropy) == n_times, "Entropy should have same length as time"
        assert np.all(entropy >= 0), "Entropy should be non-negative"
        assert np.all(np.isfinite(entropy)), "Entropy should be finite"
        logger.info(f" Entropy calculation: {entropy}")
        
        # Test entropy production rate
        entropy_rate = entropy_calc.entropy_production_rate(entropy, time_points)
        assert len(entropy_rate) == n_times, "Entropy rate should have same length as time"
        assert np.all(np.isfinite(entropy_rate)), "Entropy rate should be finite"
        logger.info(f" Entropy production rate: {entropy_rate}")
        
        return True
        
    except Exception as e:
        logger.error(f" Entropy calculation test failed: {e}")
        return False

def main():
    """Run all tests."""
    logger.info("Starting Void Physics Math Tests")
    logger.info("=" * 50)
    
    tests = [
        ("Import Test", test_imports),
        ("Potential Math", test_potential_math),
        ("Stochastic Math", test_stochastic_math),
        ("Numerical Solver", test_numerical_solver),
        ("Entropy Calculation", test_entropy_calculation),
    ]
    
    results = []
    for test_name, test_func in tests:
        logger.info(f"\nRunning {test_name}...")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            logger.error(f"{test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    logger.info("\n" + "=" * 50)
    logger.info("Test Results Summary:")
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "PASSED" if result else "FAILED"
        logger.info(f"  {test_name}: {status}")
        if result:
            passed += 1
    
    logger.info(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        logger.info("All tests passed! The math is working correctly.")
        return 0
    else:
        logger.error("Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
