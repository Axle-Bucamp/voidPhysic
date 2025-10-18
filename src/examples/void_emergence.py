"""
Void Emergence Example

This example demonstrates the complete void physics framework by running
the main visualization scenes and showing the emergence of spacetime
from the void state.
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from void_physic.visualization.scenes import VoidEmergenceScene, VoidEmergence3D
from void_physic.visualization.potential_landscape import PotentialLandscapeScene, PotentialLandscape3D
from void_physic.visualization.field_evolution import FieldEvolutionScene, FieldEvolution3D
from void_physic.visualization.entropy_time import EntropyTimeScene, TimeEmergenceScene


def main():
    """Main function to run void emergence examples."""
    
    print("🌌 Void Physics - Emergence from the Void")
    print("=" * 50)
    
    print("\nThis example demonstrates the complete void physics framework.")
    print("You can run individual scenes using manimgl:")
    print()
    print("1. Main narrative (4 acts):")
    print("   manimgl examples/void_emergence.py VoidEmergenceScene")
    print()
    print("2. 3D version:")
    print("   manimgl examples/void_emergence.py VoidEmergence3D")
    print()
    print("3. Individual scenes:")
    print("   manimgl src/void_physic/visualization/potential_landscape.py PotentialLandscapeScene")
    print("   manimgl src/void_physic/visualization/field_evolution.py FieldEvolutionScene")
    print("   manimgl src/void_physic/visualization/entropy_time.py EntropyTimeScene")
    print()
    print("4. Time emergence focus:")
    print("   manimgl src/void_physic/visualization/entropy_time.py TimeEmergenceScene")
    print()
    
    print("🎬 Scene Descriptions:")
    print()
    print("• VoidEmergenceScene: Complete 4-act narrative")
    print("  - Act 1: The Void (abstract topological space)")
    print("  - Act 2: Instability (quantum fluctuations)")
    print("  - Act 3: Emergence (field evolution, spacetime formation)")
    print("  - Act 4: Time's Arrow (entropy increase, time emergence)")
    print()
    print("• PotentialLandscapeScene: Double-well potential visualization")
    print("  - 3D potential surface")
    print("  - Ball rolling animation")
    print("  - Quantum tunneling")
    print("  - Instanton trajectories")
    print()
    print("• FieldEvolutionScene: Stochastic field dynamics")
    print("  - Multiple trajectories")
    print("  - Ensemble statistics")
    print("  - Phase portraits")
    print("  - First passage analysis")
    print()
    print("• EntropyTimeScene: Entropy and time emergence")
    print("  - Entropy evolution")
    print("  - Entropy production rate")
    print("  - Time's arrow")
    print("  - Thermodynamic quantities")
    print()
    
    print("🔬 Scientific Content:")
    print()
    print("The animations demonstrate:")
    print("• Mathematical formalism of void physics")
    print("• Stochastic dynamics and quantum fluctuations")
    print("• Symmetry breaking and phase transitions")
    print("• Entropy production and time emergence")
    print("• Connection to cosmology and quantum field theory")
    print()
    
    print("📚 Educational Value:")
    print()
    print("These visualizations are designed for:")
    print("• Physics students learning field theory")
    print("• Researchers in quantum cosmology")
    print("• Anyone interested in the foundations of physics")
    print("• Philosophical exploration of time and space")
    print()
    
    print("🚀 Getting Started:")
    print()
    print("1. Install dependencies: uv sync")
    print("2. Run toy model: python examples/toy_model_0d.py")
    print("3. Generate animations: manimgl examples/void_emergence.py VoidEmergenceScene")
    print("4. Explore individual scenes as listed above")
    print()
    
    print("✨ The void contains all possibilities.")
    print("   From the void, everything emerges.")


if __name__ == "__main__":
    main()
