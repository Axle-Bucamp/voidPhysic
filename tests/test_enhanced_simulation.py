#!/usr/bin/env python3
"""Comprehensive test suite for the enhanced void physics simulation."""

import unittest
import numpy as np
import sys
import os

# Add examples directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'examples'))

try:
    from void_physics_life_game import (
        UniverseConfig, Universe, Particle, Atom, Bond, 
        PhysicsEngine, VoidEmergence, EntropyTracker, UniverseDashboard
    )
except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure you're running from the project root directory")
    sys.exit(1)


class TestParticle(unittest.TestCase):
    """Test Particle class functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.particle = Particle(position=np.array([0.0, 0.0, 0.0]), energy=1.0)
    
    def test_particle_initialization(self):
        """Test particle initialization."""
        self.assertEqual(self.particle.energy, 1.0)
        self.assertEqual(self.particle.mass, 1.0)
        self.assertEqual(self.particle.age, 0)
        np.testing.assert_array_equal(self.particle.position, [0.0, 0.0, 0.0])
    
    def test_distance_calculation(self):
        """Test distance calculation between particles."""
        other_particle = Particle(position=np.array([3.0, 4.0, 0.0]), energy=1.0)
        distance = self.particle.get_distance_to(other_particle)
        self.assertAlmostEqual(distance, 5.0, places=10)
    
    def test_velocity_update(self):
        """Test velocity update based on forces."""
        dt = 0.01
        self.particle.force = np.array([1.0, 0.0, 0.0])
        initial_velocity = self.particle.velocity.copy()
        self.particle.update_velocity(dt)
        expected_velocity = initial_velocity + (self.particle.force / self.particle.mass) * dt
        np.testing.assert_array_almost_equal(self.particle.velocity, expected_velocity)
    
    def test_position_update(self):
        """Test position update based on velocity."""
        dt = 0.01
        self.particle.velocity = np.array([1.0, 0.0, 0.0])
        initial_position = self.particle.position.copy()
        self.particle.update_position(dt)
        expected_position = initial_position + self.particle.velocity * dt
        np.testing.assert_array_almost_equal(self.particle.position, expected_position)


class TestAtom(unittest.TestCase):
    """Test Atom class functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.particles = [
            Particle(position=np.array([0.0, 0.0, 0.0]), energy=1.0),
            Particle(position=np.array([1.0, 0.0, 0.0]), energy=1.0)
        ]
        self.atom = Atom(self.particles)
    
    def test_atom_initialization(self):
        """Test atom initialization."""
        self.assertEqual(len(self.atom.particles), 2)
        self.assertEqual(self.atom.atomic_number, 2)
        self.assertEqual(len(self.atom.bonds), 0)
        self.assertEqual(self.atom.age, 0)
    
    def test_center_of_mass(self):
        """Test center of mass calculation."""
        expected_com = np.array([0.5, 0.0, 0.0])
        np.testing.assert_array_almost_equal(self.atom.position, expected_com)
    
    def test_total_energy(self):
        """Test total energy calculation."""
        expected_energy = 2.0 - 0.2  # 2 particles - binding energy
        self.assertAlmostEqual(self.atom.energy, expected_energy, places=10)
    
    def test_atomic_properties(self):
        """Test atomic property calculations."""
        self.assertGreater(self.atom.atomic_radius, 0)
        self.assertGreater(self.atom.electronegativity, 0)
        self.assertGreater(len(self.atom.electron_shells), 0)


class TestBond(unittest.TestCase):
    """Test Bond class functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.config = UniverseConfig()
        self.particles1 = [Particle(position=np.array([0.0, 0.0, 0.0]), energy=1.0)]
        self.particles2 = [Particle(position=np.array([1.5, 0.0, 0.0]), energy=1.0)]
        self.atom1 = Atom(self.particles1)
        self.atom2 = Atom(self.particles2)
        self.bond = Bond(self.atom1, self.atom2, self.config)
    
    def test_bond_initialization(self):
        """Test bond initialization."""
        self.assertEqual(self.bond.atom1, self.atom1)
        self.assertEqual(self.bond.atom2, self.atom2)
        self.assertAlmostEqual(self.bond.distance, 1.5, places=10)
        self.assertGreater(self.bond.energy_capacity, 0)
    
    def test_bond_type_determination(self):
        """Test bond type determination."""
        self.assertIn(self.bond.bond_type, ["covalent", "polar_covalent", "ionic"])
    
    def test_energy_transmission(self):
        """Test energy transmission through bond."""
        initial_energy = 1.0
        transmitted = self.bond.transmit_energy(initial_energy, 0, 0.0)
        self.assertLess(transmitted, initial_energy)  # Should decay
        self.assertGreater(transmitted, 0)  # Should not be zero
    
    def test_bond_stability(self):
        """Test bond stability check."""
        is_stable = self.bond.is_stable()
        self.assertIsInstance(is_stable, bool)


class TestPhysicsEngine(unittest.TestCase):
    """Test PhysicsEngine functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.config = UniverseConfig()
        self.engine = PhysicsEngine(self.config)
    
    def test_lennard_jones_potential(self):
        """Test Lennard-Jones potential calculation."""
        # Test at sigma (should be zero)
        potential = self.engine.lennard_jones_potential(1.0)
        self.assertAlmostEqual(potential, 0.0, places=10)
        
        # Test at close distance (should be positive/repulsive)
        potential_close = self.engine.lennard_jones_potential(0.5)
        self.assertGreater(potential_close, 0)
        
        # Test at far distance (should be negative/attractive)
        potential_far = self.engine.lennard_jones_potential(2.0)
        self.assertLess(potential_far, 0)
    
    def test_lennard_jones_force(self):
        """Test Lennard-Jones force calculation."""
        # Test at sigma (should be zero)
        force = self.engine.lennard_jones_force(1.0)
        self.assertAlmostEqual(force, 0.0, places=10)
        
        # Test at close distance (should be positive/repulsive)
        force_close = self.engine.lennard_jones_force(0.5)
        self.assertGreater(force_close, 0)
        
        # Test at far distance (should be negative/attractive)
        force_far = self.engine.lennard_jones_force(2.0)
        self.assertLess(force_far, 0)
    
    def test_force_calculation(self):
        """Test force calculation between particles."""
        particles = [
            Particle(position=np.array([0.0, 0.0, 0.0]), energy=1.0),
            Particle(position=np.array([1.5, 0.0, 0.0]), energy=1.0)
        ]
        
        self.engine.calculate_forces(particles)
        
        # Forces should be equal and opposite (Newton's third law)
        force1 = particles[0].force
        force2 = particles[1].force
        np.testing.assert_array_almost_equal(force1, -force2)


class TestVoidEmergence(unittest.TestCase):
    """Test VoidEmergence functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.config = UniverseConfig()
        self.emergence = VoidEmergence(self.config)
    
    def test_emergence_probability(self):
        """Test particle emergence probability calculation."""
        # Empty universe should always allow first particle
        universe = Universe(self.config)
        should_emerge = self.emergence.should_emerge_particle(universe)
        self.assertTrue(should_emerge)
    
    def test_particle_creation(self):
        """Test particle creation."""
        universe = Universe(self.config)
        particle = self.emergence.create_particle(universe)
        
        self.assertIsInstance(particle, Particle)
        self.assertEqual(particle.energy, self.config.initial_particle_energy)


class TestEntropyTracker(unittest.TestCase):
    """Test EntropyTracker functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.config = UniverseConfig()
        self.tracker = EntropyTracker(self.config)
    
    def test_local_energy_calculation(self):
        """Test local energy calculation."""
        universe = Universe(self.config)
        universe.add_particle(Particle(position=np.array([0.0, 0.0, 0.0]), energy=1.0))
        
        local_energies = self.tracker.calculate_local_energy(universe)
        
        self.assertIn('kinetic', local_energies)
        self.assertIn('potential', local_energies)
        self.assertIn('bond', local_energies)
        self.assertIn('void_interference', local_energies)
        
        # All energies should be non-negative
        for energy_type, energy_value in local_energies.items():
            self.assertGreaterEqual(energy_value, 0)
    
    def test_total_energy_calculation(self):
        """Test total energy calculation."""
        universe = Universe(self.config)
        universe.add_particle(Particle(position=np.array([0.0, 0.0, 0.0]), energy=1.0))
        
        total_energy = self.tracker.calculate_total_energy(universe)
        self.assertGreaterEqual(total_energy, 0)
    
    def test_entropy_calculation(self):
        """Test entropy calculation."""
        universe = Universe(self.config)
        universe.add_particle(Particle(position=np.array([0.0, 0.0, 0.0]), energy=1.0))
        
        entropy = self.tracker.calculate_entropy(universe)
        self.assertGreaterEqual(entropy, 0)


class TestUniverse(unittest.TestCase):
    """Test Universe class functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.config = UniverseConfig()
        self.universe = Universe(self.config)
    
    def test_universe_initialization(self):
        """Test universe initialization."""
        self.assertEqual(len(self.universe.particles), 0)
        self.assertEqual(len(self.universe.atoms), 0)
        self.assertEqual(len(self.universe.bonds), 0)
        self.assertEqual(self.universe.iteration, 0)
    
    def test_particle_addition(self):
        """Test adding particles to universe."""
        particle = Particle(position=np.array([0.0, 0.0, 0.0]), energy=1.0)
        self.universe.add_particle(particle)
        
        self.assertEqual(len(self.universe.particles), 1)
        self.assertEqual(self.universe.particles[0], particle)
    
    def test_atom_creation(self):
        """Test atom creation from particles."""
        particles = [
            Particle(position=np.array([0.0, 0.0, 0.0]), energy=1.0),
            Particle(position=np.array([1.0, 0.0, 0.0]), energy=1.0)
        ]
        
        atom = self.universe.create_atom(particles)
        
        self.assertEqual(len(self.universe.atoms), 1)
        self.assertEqual(self.universe.atoms[0], atom)
    
    def test_bond_formation(self):
        """Test bond formation between atoms."""
        # Create two atoms close enough to bond
        particles1 = [Particle(position=np.array([0.0, 0.0, 0.0]), energy=1.0)]
        particles2 = [Particle(position=np.array([1.5, 0.0, 0.0]), energy=1.0)]
        
        atom1 = self.universe.create_atom(particles1)
        atom2 = self.universe.create_atom(particles2)
        
        self.universe.check_bond_formation()
        
        # Should form at least one bond
        self.assertGreater(len(self.universe.bonds), 0)
    
    def test_universe_update(self):
        """Test universe update cycle."""
        initial_iteration = self.universe.iteration
        self.universe.update()
        
        self.assertEqual(self.universe.iteration, initial_iteration + 1)
    
    def test_state_summary(self):
        """Test state summary generation."""
        summary = self.universe.get_state_summary()
        
        required_keys = [
            'iteration', 'particle_count', 'atom_count', 'bond_count',
            'total_energy', 'total_mass', 'entropy', 'stable_structures', 'is_stable'
        ]
        
        for key in required_keys:
            self.assertIn(key, summary)


class TestIntegration(unittest.TestCase):
    """Integration tests for the complete simulation."""
    
    def test_full_simulation_run(self):
        """Test a complete simulation run."""
        config = UniverseConfig(seed=123)
        universe = Universe(config)
        
        # Run simulation for several iterations
        for i in range(50):
            universe.update()
        
        # Check that simulation progressed
        self.assertGreater(universe.iteration, 0)
        
        # Check that particles were created
        self.assertGreater(len(universe.particles), 0)
        
        # Check that atoms were formed
        self.assertGreater(len(universe.atoms), 0)
    
    def test_energy_conservation(self):
        """Test that energy is conserved during simulation."""
        config = UniverseConfig(seed=123)
        universe = Universe(config)
        
        initial_energy = universe.total_energy
        
        # Run simulation for several iterations
        for i in range(100):
            universe.update()
        
        final_energy = universe.total_energy
        
        # Energy should be conserved within numerical precision
        energy_change = abs(final_energy - initial_energy)
        self.assertLess(energy_change, 1e-6)
    
    def test_entropy_increase(self):
        """Test that entropy generally increases over time."""
        config = UniverseConfig(seed=123)
        universe = Universe(config)
        
        initial_entropy = universe.entropy_tracker.calculate_entropy(universe)
        
        # Run simulation for several iterations
        for i in range(100):
            universe.update()
        
        final_entropy = universe.entropy_tracker.calculate_entropy(universe)
        
        # Entropy should generally increase (second law of thermodynamics)
        self.assertGreaterEqual(final_entropy, initial_entropy)


class TestVisualization(unittest.TestCase):
    """Test visualization components."""
    
    def test_dashboard_creation(self):
        """Test dashboard creation."""
        config = UniverseConfig()
        universe = Universe(config)
        
        try:
            dashboard = UniverseDashboard(universe)
            self.assertIsNotNone(dashboard)
        except ImportError:
            # Skip if plotly not available
            self.skipTest("Plotly not available")
    
    def test_3d_plot_creation(self):
        """Test 3D plot creation."""
        config = UniverseConfig()
        universe = Universe(config)
        
        # Add some particles for visualization
        universe.add_particle(Particle(position=np.array([0.0, 0.0, 0.0]), energy=1.0))
        universe.add_particle(Particle(position=np.array([1.0, 0.0, 0.0]), energy=1.0))
        
        try:
            dashboard = UniverseDashboard(universe)
            fig = dashboard._create_3d_plot()
            self.assertIsNotNone(fig)
        except ImportError:
            # Skip if plotly not available
            self.skipTest("Plotly not available")


def run_tests():
    """Run all tests."""
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test classes
    test_classes = [
        TestParticle,
        TestAtom,
        TestBond,
        TestPhysicsEngine,
        TestVoidEmergence,
        TestEntropyTracker,
        TestUniverse,
        TestIntegration,
        TestVisualization
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    print("🧪 Running Void Physics Life Simulation Test Suite")
    print("=" * 60)
    
    success = run_tests()
    
    if success:
        print("\n✅ All tests passed!")
        exit(0)
    else:
        print("\n❌ Some tests failed!")
        exit(1)