#!/usr/bin/env python3
"""
Simple Test for Void Physics Core Components
============================================

This script tests the core void physics components without
the dashboard dependencies.
"""

import numpy as np
import sys
import os

# Add the examples directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_atom_class():
    """Test the Atom class."""
    print("🧪 Testing Atom Class...")
    
    try:
        # Import only the Atom class
        from universe_creation_simulation import Atom
        
        # Create atom
        atom = Atom(x=10, y=10, energy=1.0, age=0, atom_type='matter')
        
        # Test initial state
        assert atom.x == 10, "X coordinate should be 10"
        assert atom.y == 10, "Y coordinate should be 10"
        assert atom.energy == 1.0, "Energy should be 1.0"
        assert atom.age == 0, "Age should be 0"
        assert atom.atom_type == 'matter', "Atom type should be matter"
        
        # Test color
        color = atom.get_color()
        assert len(color) == 3, "Color should have 3 components"
        assert all(0 <= c <= 1 for c in color), "Color components should be in [0,1]"
        
        print("✅ Atom Class test passed!")
        return True
        
    except Exception as e:
        print(f"❌ Atom Class test failed: {e}")
        return False

def test_void_field():
    """Test the VoidField class."""
    print("🧪 Testing VoidField Class...")
    
    try:
        # Import only the VoidField class
        from universe_creation_simulation import VoidField
        
        # Create void field
        void_field = VoidField(width=50, height=50)
        
        # Test initial state
        assert void_field.width == 50, "Width should be 50"
        assert void_field.height == 50, "Height should be 50"
        assert void_field.time == 0.0, "Initial time should be 0"
        
        # Add interference source
        void_field.add_interference_source(x=25, y=25, frequency=0.5, amplitude=1.0)
        assert len(void_field.interference_sources) == 1, "Should have 1 interference source"
        
        # Update field
        void_field.update(dt=0.1)
        assert void_field.time > 0, "Time should have advanced"
        assert void_field.field.shape == (50, 50), "Field should be 50x50"
        
        print("✅ VoidField Class test passed!")
        return True
        
    except Exception as e:
        print(f"❌ VoidField Class test failed: {e}")
        return False

def test_void_physics_cell():
    """Test the VoidPhysicsCell class."""
    print("🧪 Testing VoidPhysicsCell Class...")
    
    try:
        # Import only the VoidPhysicsCell class
        from void_physics_life_game import VoidPhysicsCell
        
        # Create cell
        cell = VoidPhysicsCell(x=10, y=10, state='atom', energy=1.0, age=0, cell_type='matter')
        
        # Test initial state
        assert cell.x == 10, "X coordinate should be 10"
        assert cell.y == 10, "Y coordinate should be 10"
        assert cell.state == 'atom', "State should be atom"
        assert cell.energy == 1.0, "Energy should be 1.0"
        assert cell.age == 0, "Age should be 0"
        assert cell.cell_type == 'matter', "Cell type should be matter"
        
        # Test color
        color = cell.get_color()
        assert len(color) == 3, "Color should have 3 components"
        assert all(0 <= c <= 1 for c in color), "Color components should be in [0,1]"
        
        print("✅ VoidPhysicsCell Class test passed!")
        return True
        
    except Exception as e:
        print(f"❌ VoidPhysicsCell Class test failed: {e}")
        return False

def test_void_field_generator():
    """Test the VoidFieldGenerator class."""
    print("🧪 Testing VoidFieldGenerator Class...")
    
    try:
        # Import only the VoidFieldGenerator class
        from void_physics_life_game import VoidFieldGenerator
        
        # Create void field
        void_field = VoidFieldGenerator(width=50, height=50)
        
        # Test initial state
        assert void_field.width == 50, "Width should be 50"
        assert void_field.height == 50, "Height should be 50"
        assert void_field.time == 0.0, "Initial time should be 0"
        
        # Add interference source
        void_field.add_interference_source(x=25, y=25, frequency=0.5, amplitude=1.0, phase=0.0)
        assert len(void_field.interference_sources) == 1, "Should have 1 interference source"
        
        # Update field
        void_field.update(dt=0.1)
        assert void_field.time > 0, "Time should have advanced"
        assert void_field.field.shape == (50, 50), "Field should be 50x50"
        
        # Test field value
        field_value = void_field.get_field_at(25, 25)
        assert isinstance(field_value, (int, float)), "Field value should be numeric"
        
        print("✅ VoidFieldGenerator Class test passed!")
        return True
        
    except Exception as e:
        print(f"❌ VoidFieldGenerator Class test failed: {e}")
        return False

def test_universe_creation_simulation():
    """Test the universe creation simulation."""
    print("🧪 Testing Universe Creation Simulation...")
    
    try:
        # Import only the simulation class
        from universe_creation_simulation import UniverseCreationSimulation
        
        # Create simulation
        sim = UniverseCreationSimulation(width=30, height=30)
        sim.initialize_void_sources()
        sim.create_initial_atoms(n_atoms=3)
        
        # Test initial state
        assert len(sim.atoms) == 3, "Should have 3 initial atoms"
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
        
        print("✅ Universe Creation Simulation test passed!")
        return True
        
    except Exception as e:
        print(f"❌ Universe Creation Simulation test failed: {e}")
        return False

def test_void_physics_life_game():
    """Test the void physics life game."""
    print("🧪 Testing Void Physics Life Game...")
    
    try:
        # Import only the game class
        from void_physics_life_game import VoidPhysicsLifeGame
        
        # Create game
        game = VoidPhysicsLifeGame(width=30, height=30)
        game.initialize_void_sources(n_sources=2)
        game.create_initial_pattern('random', n_cells=3)
        
        # Test initial state
        assert game.time == 0.0, "Initial time should be 0"
        assert len(game.history) == 0, "Initial history should be empty"
        
        # Run a few updates
        for i in range(5):
            game.update(dt=0.1)
            
        # Check that game is running
        assert game.time > 0, "Time should have advanced"
        assert len(game.history) == 5, "Should have 5 history entries"
        
        # Test void field
        void_image = game.get_void_field_image()
        assert void_image.shape == (30, 30), "Void field should be 30x30"
        
        # Test universe image
        universe_image = game.get_universe_image()
        assert universe_image.shape == (30, 30, 3), "Universe image should be 30x30x3"
        
        # Test statistics
        assert 'total_cells' in game.stats, "Should have total_cells in stats"
        assert 'total_energy' in game.stats, "Should have total_energy in stats"
        
        print("✅ Void Physics Life Game test passed!")
        return True
        
    except Exception as e:
        print(f"❌ Void Physics Life Game test failed: {e}")
        return False

def run_all_tests():
    """Run all tests."""
    print("🧪 Running Simple Void Physics Tests")
    print("=" * 50)
    
    tests = [
        test_atom_class,
        test_void_field,
        test_void_physics_cell,
        test_void_field_generator,
        test_universe_creation_simulation,
        test_void_physics_life_game
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
        print("🎉 All tests passed! The void physics simulations are working correctly.")
        return True
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        return False

def main():
    """Main test function."""
    print("🌌 Simple Void Physics Test Suite")
    print("=" * 60)
    
    # Run tests
    all_tests_passed = run_all_tests()
    
    if all_tests_passed:
        print("\n🚀 Core components are working! The simulations should run correctly.")
        print("\nTo run the simulations:")
        print("  python examples/universe_creation_simulation.py")
        print("  python examples/void_physics_life_game.py")
        print("  python examples/void_physics_master_dashboard.py")
    else:
        print("\n⚠️  Please fix the failing tests before running the simulations.")

if __name__ == "__main__":
    main()
