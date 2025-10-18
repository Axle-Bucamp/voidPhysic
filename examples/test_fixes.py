#!/usr/bin/env python3
"""
Test Fixes for Void Physics Simulations
======================================

Quick test to verify that the fixes for the animation and color issues work.
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
import os

# Add the examples directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_advanced_simulation():
    """Test the advanced void physics simulation."""
    print("🧪 Testing Advanced Void Physics Simulation...")
    
    try:
        from advanced_void_physics_simulation import AdvancedVoidPhysicsSimulation
        
        # Create simulation
        sim = AdvancedVoidPhysicsSimulation(width=20, height=20)
        sim.initialize_topological_sources(n_sources=2)
        sim.create_initial_atoms(n_atoms=1)
        
        # Test image generation
        universe_image = sim.get_universe_image()
        void_image = sim.get_void_field_image()
        
        assert universe_image.shape == (20, 20, 3), "Universe image should be 20x20x3"
        assert void_image.shape == (20, 20), "Void image should be 20x20"
        assert np.all(universe_image >= 0) and np.all(universe_image <= 1), "Image values should be in [0,1]"
        
        # Run a few updates
        for i in range(5):
            sim.update(dt=0.1)
            
        # Test updated images
        universe_image = sim.get_universe_image()
        assert universe_image.shape == (20, 20, 3), "Updated universe image should be 20x20x3"
        
        print("✅ Advanced simulation test passed!")
        return True
        
    except Exception as e:
        print(f"❌ Advanced simulation test failed: {e}")
        return False

def test_universe_creation_simulation():
    """Test the universe creation simulation."""
    print("🧪 Testing Universe Creation Simulation...")
    
    try:
        from universe_creation_simulation import UniverseCreationSimulation
        
        # Create simulation
        sim = UniverseCreationSimulation(width=20, height=20)
        sim.initialize_void_sources()
        sim.create_initial_atoms(n_atoms=1)
        
        # Test image generation
        universe_image = sim.get_universe_image()
        void_image = sim.get_void_field_image()
        
        assert universe_image.shape == (20, 20, 3), "Universe image should be 20x20x3"
        assert void_image.shape == (20, 20), "Void image should be 20x20"
        assert np.all(universe_image >= 0) and np.all(universe_image <= 1), "Image values should be in [0,1]"
        
        # Run a few updates
        for i in range(5):
            sim.update(dt=0.1)
            
        # Test updated images
        universe_image = sim.get_universe_image()
        assert universe_image.shape == (20, 20, 3), "Updated universe image should be 20x20x3"
        
        print("✅ Universe creation simulation test passed!")
        return True
        
    except Exception as e:
        print(f"❌ Universe creation simulation test failed: {e}")
        return False

def test_life_game_simulation():
    """Test the life game simulation."""
    print("🧪 Testing Life Game Simulation...")
    
    try:
        from void_physics_life_game import VoidPhysicsLifeGame
        
        # Create game
        game = VoidPhysicsLifeGame(width=20, height=20)
        game.initialize_void_sources(n_sources=2)
        game.create_initial_pattern('random', n_cells=2)
        
        # Test image generation
        universe_image = game.get_universe_image()
        void_image = game.get_void_field_image()
        
        assert universe_image.shape == (20, 20, 3), "Universe image should be 20x20x3"
        assert void_image.shape == (20, 20), "Void image should be 20x20"
        assert np.all(universe_image >= 0) and np.all(universe_image <= 1), "Image values should be in [0,1]"
        
        # Run a few updates
        for i in range(5):
            game.update(dt=0.1)
            
        # Test updated images
        universe_image = game.get_universe_image()
        assert universe_image.shape == (20, 20, 3), "Updated universe image should be 20x20x3"
        
        print("✅ Life game simulation test passed!")
        return True
        
    except Exception as e:
        print(f"❌ Life game simulation test failed: {e}")
        return False

def test_visualization_creation():
    """Test that visualizations can be created without errors."""
    print("🧪 Testing Visualization Creation...")
    
    try:
        from advanced_void_physics_simulation import AdvancedVoidPhysicsSimulation, AdvancedVoidPhysicsVisualizer
        
        # Create simulation and visualizer
        sim = AdvancedVoidPhysicsSimulation(width=20, height=20)
        sim.initialize_topological_sources(n_sources=1)
        sim.create_initial_atoms(n_atoms=1)
        
        visualizer = AdvancedVoidPhysicsVisualizer(sim)
        
        # Test visualization creation
        visualizer.create_visualization()
        assert visualizer.fig is not None, "Figure should be created"
        assert visualizer.axes is not None, "Axes should be created"
        
        # Test update
        visualizer.update_visualization()
        
        print("✅ Visualization creation test passed!")
        return True
        
    except Exception as e:
        print(f"❌ Visualization creation test failed: {e}")
        return False

def run_all_tests():
    """Run all tests."""
    print("🧪 Running Fix Tests")
    print("=" * 40)
    
    tests = [
        test_advanced_simulation,
        test_universe_creation_simulation,
        test_life_game_simulation,
        test_visualization_creation
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
    print("\n" + "=" * 40)
    print("📊 Test Results Summary:")
    
    passed = sum(results)
    total = len(results)
    
    for i, (test, result) in enumerate(zip(tests, results)):
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"  {i+1}. {test.__name__}: {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All fixes are working correctly!")
        return True
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        return False

def main():
    """Main test function."""
    print("🔧 Void Physics Fixes Test Suite")
    print("=" * 50)
    
    # Run tests
    all_tests_passed = run_all_tests()
    
    if all_tests_passed:
        print("\n🚀 All simulations should now work correctly!")
        print("\nYou can now run:")
        print("  python examples/demo_advanced_void_physics.py")
        print("  python examples/universe_creation_simulation.py")
        print("  python examples/void_physics_life_game.py")
    else:
        print("\n⚠️  Please fix the remaining issues.")

if __name__ == "__main__":
    main()
