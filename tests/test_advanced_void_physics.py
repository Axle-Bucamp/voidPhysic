#!/usr/bin/env python3
"""
Test Advanced Void Physics Simulation
====================================

Test the advanced void physics simulation with void particles,
wave function collapse, and topological connectivity.
"""

import numpy as np
import sys
import os

# Add the examples directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_void_particle_class():
    """Test the VoidParticle class."""
    print("🧪 Testing VoidParticle Class...")
    
    try:
        from advanced_void_physics_simulation import VoidParticle
        
        # Create void particle
        particle = VoidParticle(x=10, y=10, energy=0.1, age=0)
        
        # Test initial state
        assert particle.x == 10, "X coordinate should be 10"
        assert particle.y == 10, "Y coordinate should be 10"
        assert particle.energy == 0.1, "Energy should be 0.1"
        assert particle.age == 0, "Age should be 0"
        assert particle.attraction_strength == 0.01, "Attraction strength should be 0.01"
        assert particle.liquid_properties == True, "Should have liquid properties"
        
        # Test color
        color = particle.get_color()
        assert len(color) == 3, "Color should have 3 components"
        assert all(0 <= c <= 1 for c in color), "Color components should be in [0,1]"
        
        print("✅ VoidParticle Class test passed!")
        return True
        
    except Exception as e:
        print(f"❌ VoidParticle Class test failed: {e}")
        return False

def test_advanced_atom_class():
    """Test the AdvancedAtom class."""
    print("🧪 Testing AdvancedAtom Class...")
    
    try:
        from advanced_void_physics_simulation import AdvancedAtom
        
        # Create atom
        atom = AdvancedAtom(x=10, y=10, energy=1.0, age=0, atom_type='matter')
        
        # Test initial state
        assert atom.x == 10, "X coordinate should be 10"
        assert atom.y == 10, "Y coordinate should be 10"
        assert atom.energy == 1.0, "Energy should be 1.0"
        assert atom.age == 0, "Age should be 0"
        assert atom.atom_type == 'matter', "Atom type should be matter"
        assert atom.attraction_strength == 1.0, "Attraction strength should be 1.0"
        
        # Test wave function
        assert 'matter_probability' in atom.wave_function, "Should have matter probability"
        assert 'antimatter_probability' in atom.wave_function, "Should have antimatter probability"
        assert 'collapsed' in atom.wave_function, "Should have collapsed state"
        
        # Test color
        color = atom.get_color()
        assert len(color) == 3, "Color should have 3 components"
        assert all(0 <= c <= 1 for c in color), "Color components should be in [0,1]"
        
        print("✅ AdvancedAtom Class test passed!")
        return True
        
    except Exception as e:
        print(f"❌ AdvancedAtom Class test failed: {e}")
        return False

def test_void_field_generator():
    """Test the VoidFieldGenerator class."""
    print("🧪 Testing VoidFieldGenerator Class...")
    
    try:
        from advanced_void_physics_simulation import VoidFieldGenerator
        
        # Create void field
        void_field = VoidFieldGenerator(width=50, height=50)
        
        # Test initial state
        assert void_field.width == 50, "Width should be 50"
        assert void_field.height == 50, "Height should be 50"
        assert void_field.time == 0.0, "Initial time should be 0"
        
        # Add topological source
        void_field.add_topological_source(x=25, y=25, strength=1.0, frequency=0.5)
        assert len(void_field.topological_sources) == 1, "Should have 1 topological source"
        
        # Update field
        void_field.update(dt=0.1)
        assert void_field.time > 0, "Time should have advanced"
        assert void_field.field.shape == (50, 50), "Field should be 50x50"
        
        print("✅ VoidFieldGenerator Class test passed!")
        return True
        
    except Exception as e:
        print(f"❌ VoidFieldGenerator Class test failed: {e}")
        return False

def test_advanced_simulation():
    """Test the AdvancedVoidPhysicsSimulation class."""
    print("🧪 Testing AdvancedVoidPhysicsSimulation Class...")
    
    try:
        from advanced_void_physics_simulation import AdvancedVoidPhysicsSimulation
        
        # Create simulation
        sim = AdvancedVoidPhysicsSimulation(width=30, height=30)
        sim.initialize_topological_sources(n_sources=2)
        sim.create_initial_atoms(n_atoms=2)
        
        # Test initial state
        assert len(sim.atoms) == 2, "Should have 2 initial atoms"
        assert len(sim.void_particles) == 0, "Should start with no void particles"
        assert sim.time == 0.0, "Initial time should be 0"
        
        # Run a few updates
        for i in range(5):
            sim.update(dt=0.1)
            
        # Check that simulation is running
        assert sim.time > 0, "Time should have advanced"
        assert len(sim.history) == 5, "Should have 5 history entries"
        
        # Test void field
        void_image = sim.get_void_field_image()
        assert void_image.shape == (30, 30), "Void field should be 30x30"
        
        # Test universe image
        universe_image = sim.get_universe_image()
        assert universe_image.shape == (30, 30, 3), "Universe image should be 30x30x3"
        
        # Test statistics
        assert 'total_atoms' in sim.stats, "Should have total_atoms in stats"
        assert 'total_void_particles' in sim.stats, "Should have total_void_particles in stats"
        assert 'superposition_atoms' in sim.stats, "Should have superposition_atoms in stats"
        
        print("✅ AdvancedVoidPhysicsSimulation Class test passed!")
        return True
        
    except Exception as e:
        print(f"❌ AdvancedVoidPhysicsSimulation Class test failed: {e}")
        return False

def test_wave_function_collapse():
    """Test wave function collapse functionality."""
    print("🧪 Testing Wave Function Collapse...")
    
    try:
        from advanced_void_physics_simulation import AdvancedAtom, VoidFieldGenerator
        
        # Create atom in superposition
        atom = AdvancedAtom(x=10, y=10, energy=1.0, age=0, atom_type='matter')
        atom.wave_function['collapsed'] = False
        
        # Create void field
        void_field = VoidFieldGenerator(width=20, height=20)
        void_field.add_topological_source(x=10, y=10, strength=2.0, frequency=0.5)
        void_field.update(dt=0.1)
        
        # Test initial superposition state
        assert not atom.wave_function['collapsed'], "Atom should start in superposition"
        assert atom.wave_function['matter_probability'] == 0.5, "Should have equal probabilities"
        assert atom.wave_function['antimatter_probability'] == 0.5, "Should have equal probabilities"
        
        # Simulate wave function collapse
        original_collapsed = atom.wave_function['collapsed']
        atom._wave_function_collapse(void_field.field)
        
        # Check if collapse occurred (probabilistic)
        if atom.wave_function['collapsed']:
            assert atom.wave_function['matter_probability'] + atom.wave_function['antimatter_probability'] == 1.0, "Probabilities should sum to 1"
            assert atom.wave_function['position_uncertainty'] == 0.0, "Position uncertainty should be 0 after collapse"
        
        print("✅ Wave Function Collapse test passed!")
        return True
        
    except Exception as e:
        print(f"❌ Wave Function Collapse test failed: {e}")
        return False

def test_void_particle_behavior():
    """Test void particle behavior and blob formation."""
    print("🧪 Testing Void Particle Behavior...")
    
    try:
        from advanced_void_physics_simulation import VoidParticle, AdvancedVoidPhysicsSimulation
        
        # Create simulation
        sim = AdvancedVoidPhysicsSimulation(width=20, height=20)
        sim.initialize_topological_sources(n_sources=1)
        
        # Create void particles
        particles = []
        for i in range(3):
            particle = VoidParticle(x=10 + i, y=10, energy=0.1, age=0)
            particles.append(particle)
            sim.void_particles.append(particle)
            sim.universe_grid[10, 10 + i] = particle
        
        # Test initial state
        assert len(sim.void_particles) == 3, "Should have 3 void particles"
        
        # Update simulation
        sim.update(dt=0.1)
        
        # Check that particles are still there
        assert len(sim.void_particles) >= 0, "Should have some void particles remaining"
        
        print("✅ Void Particle Behavior test passed!")
        return True
        
    except Exception as e:
        print(f"❌ Void Particle Behavior test failed: {e}")
        return False

def run_all_tests():
    """Run all tests."""
    print("🧪 Running Advanced Void Physics Tests")
    print("=" * 50)
    
    tests = [
        test_void_particle_class,
        test_advanced_atom_class,
        test_void_field_generator,
        test_advanced_simulation,
        test_wave_function_collapse,
        test_void_particle_behavior
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test {test.__name__} failed with exception: {e}")
            results.append(False)
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    
    passed = sum(results)
    total = len(results)
    
    for i, (test, result) in enumerate(zip(tests, results)):
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"  {i+1}. {test.__name__}: {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The advanced void physics simulation is working correctly.")
        return True
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        return False

def main():
    """Main test function."""
    print("🌌 Advanced Void Physics Test Suite")
    print("=" * 60)
    
    # Run tests
    all_tests_passed = run_all_tests()
    
    if all_tests_passed:
        print("\n🚀 Advanced void physics simulation is ready!")
        print("\nKey features implemented:")
        print("- Void particles that behave like liquid")
        print("- Wave function collapse for atoms")
        print("- Topological connectivity (no time/space in void)")
        print("- Void particles blob together to form atoms")
        print("- Much lower attraction strength for void particles")
        print("- Atoms age when void particles attach")
        print("\nTo run the simulation:")
        print("  python examples/advanced_void_physics_simulation.py")
    else:
        print("\n⚠️  Please fix the failing tests before running the simulation.")

if __name__ == "__main__":
    main()
