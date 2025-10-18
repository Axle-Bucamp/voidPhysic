"""
Cosmic Microwave Background Signatures from Void Physics

This example generates mock CMB anisotropy patterns and gravitational wave
spectra that would result from void nucleation in the early universe.
"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import sys

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from void_physic.core.potential import DoubleWellPotential, PotentialParameters
from void_physic.core.instanton import InstantonSolver, TunnelingProbability
from void_physic.utils.constants import PhysicalConstants


def generate_cmb_anisotropies():
    """
    Generate mock CMB anisotropy patterns from void nucleation.
    
    Returns:
        Dictionary with CMB data
    """
    print("🌌 Generating CMB anisotropies from void nucleation...")
    
    # Set up parameters
    potential_params = PotentialParameters(
        lambda_coupling=1.0,
        v_vev=1.0,
        V0_offset=0.0
    )
    
    potential = DoubleWellPotential(potential_params)
    instanton_solver = InstantonSolver(potential)
    tunneling_prob = TunnelingProbability(instanton_solver)
    
    # Calculate nucleation rate
    nucleation_rate = tunneling_prob.nucleation_rate(volume=1.0)
    
    print(f"   • Nucleation rate: {nucleation_rate:.3e}")
    
    # Generate mock CMB map
    # This is a simplified model - in reality, this would require
    # solving the full Einstein-Boltzmann equations
    
    # Angular resolution
    n_theta = 180
    n_phi = 360
    theta = np.linspace(0, np.pi, n_theta)
    phi = np.linspace(0, 2*np.pi, n_phi)
    
    # Create mock anisotropy pattern
    # Void nucleation would create specific patterns in the CMB
    cmb_map = np.zeros((n_theta, n_phi))
    
    # Add dipole (from void asymmetry)
    dipole_amplitude = 0.001  # 1 mK
    for i, t in enumerate(theta):
        for j, p in enumerate(phi):
            cmb_map[i, j] += dipole_amplitude * np.cos(t)
    
    # Add quadrupole (from void geometry)
    quadrupole_amplitude = 0.0005  # 0.5 mK
    for i, t in enumerate(theta):
        for j, p in enumerate(phi):
            cmb_map[i, j] += quadrupole_amplitude * (3*np.cos(t)**2 - 1)
    
    # Add higher multipoles (from void texture)
    for l in range(3, 10):
        multipole_amplitude = 0.0001 / l  # Decreasing amplitude
        for i, t in enumerate(theta):
            for j, p in enumerate(phi):
                # Simplified spherical harmonic
                if l == 3:
                    cmb_map[i, j] += multipole_amplitude * np.sin(t)**3 * np.cos(3*p)
                elif l == 4:
                    cmb_map[i, j] += multipole_amplitude * np.sin(t)**4 * np.cos(4*p)
                # Add more multipoles as needed
    
    # Add noise (instrumental and cosmic variance)
    noise_level = 0.0001  # 0.1 mK
    cmb_map += np.random.normal(0, noise_level, cmb_map.shape)
    
    return {
        'cmb_map': cmb_map,
        'theta': theta,
        'phi': phi,
        'nucleation_rate': nucleation_rate,
        'dipole_amplitude': dipole_amplitude,
        'quadrupole_amplitude': quadrupole_amplitude,
        'noise_level': noise_level
    }


def generate_gravitational_wave_spectrum():
    """
    Generate gravitational wave spectrum from void nucleation.
    
    Returns:
        Dictionary with GW data
    """
    print("🌊 Generating gravitational wave spectrum...")
    
    # Set up parameters
    potential_params = PotentialParameters(
        lambda_coupling=1.0,
        v_vev=1.0,
        V0_offset=0.0
    )
    
    potential = DoubleWellPotential(potential_params)
    instanton_solver = InstantonSolver(potential)
    tunneling_prob = TunnelingProbability(instanton_solver)
    
    # Calculate bubble collision parameters
    # This is a simplified model based on first-order phase transitions
    
    # Frequency range (Hz)
    frequencies = np.logspace(-18, -10, 1000)  # From nHz to mHz
    
    # Characteristic frequency (Hz)
    f_star = 1e-15  # 1 nHz (characteristic of void nucleation)
    
    # Power spectrum
    # For first-order phase transitions, the spectrum has a peak
    power_spectrum = np.zeros_like(frequencies)
    
    for i, f in enumerate(frequencies):
        if f < f_star:
            # Low frequency: power law
            power_spectrum[i] = (f / f_star)**3
        else:
            # High frequency: exponential cutoff
            power_spectrum[i] = (f / f_star)**(-1) * np.exp(-f / f_star)
    
    # Normalize
    power_spectrum = power_spectrum / np.max(power_spectrum)
    
    # Add characteristic amplitude
    # This would be calculated from the energy scale of the transition
    characteristic_amplitude = 1e-15  # 1e-15 strain
    
    # Convert to strain
    strain_spectrum = characteristic_amplitude * np.sqrt(power_spectrum)
    
    # Add noise (detector noise)
    noise_level = 1e-18  # 1e-18 strain
    strain_spectrum += np.random.normal(0, noise_level, len(frequencies))
    
    return {
        'frequencies': frequencies,
        'power_spectrum': power_spectrum,
        'strain_spectrum': strain_spectrum,
        'f_star': f_star,
        'characteristic_amplitude': characteristic_amplitude,
        'noise_level': noise_level
    }


def calculate_baryon_asymmetry():
    """
    Calculate baryon asymmetry from void physics.
    
    Returns:
        Dictionary with asymmetry data
    """
    print("⚛️ Calculating baryon asymmetry...")
    
    # Set up parameters
    potential_params = PotentialParameters(
        lambda_coupling=1.0,
        v_vev=1.0,
        V0_offset=0.0
    )
    
    potential = DoubleWellPotential(potential_params)
    instanton_solver = InstantonSolver(potential)
    tunneling_prob = TunnelingProbability(instanton_solver)
    
    # Calculate asymmetry parameters
    # This is a simplified model based on CP violation during nucleation
    
    # CP violation parameter
    epsilon_cp = 0.1  # 10% CP violation
    
    # Efficiency parameter (how much asymmetry survives)
    efficiency = 0.1  # 10% efficiency
    
    # Baryon asymmetry
    eta_b = epsilon_cp * efficiency * tunneling_prob.nucleation_rate(volume=1.0)
    
    # Observed value (from Big Bang nucleosynthesis)
    eta_b_observed = 6e-10
    
    # Ratio
    ratio = eta_b / eta_b_observed
    
    print(f"   • CP violation parameter: {epsilon_cp:.3f}")
    print(f"   • Efficiency: {efficiency:.3f}")
    print(f"   • Calculated asymmetry: {eta_b:.3e}")
    print(f"   • Observed asymmetry: {eta_b_observed:.3e}")
    print(f"   • Ratio: {ratio:.3f}")
    
    return {
        'eta_b': eta_b,
        'eta_b_observed': eta_b_observed,
        'ratio': ratio,
        'epsilon_cp': epsilon_cp,
        'efficiency': efficiency
    }


def create_visualizations():
    """Create visualizations of cosmological predictions."""
    
    print("📊 Creating visualizations...")
    
    # Generate data
    cmb_data = generate_cmb_anisotropies()
    gw_data = generate_gravitational_wave_spectrum()
    asymmetry_data = calculate_baryon_asymmetry()
    
    # Create figure
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('Cosmological Predictions from Void Physics', fontsize=16)
    
    # 1. CMB anisotropies
    ax1 = axes[0, 0]
    theta_mesh, phi_mesh = np.meshgrid(cmb_data['theta'], cmb_data['phi'], indexing='ij')
    im1 = ax1.contourf(phi_mesh, theta_mesh, cmb_data['cmb_map'], levels=20, cmap='RdBu_r')
    ax1.set_xlabel('φ (radians)')
    ax1.set_ylabel('θ (radians)')
    ax1.set_title('CMB Anisotropies from Void Nucleation')
    plt.colorbar(im1, ax=ax1, label='Temperature (mK)')
    
    # 2. Gravitational wave spectrum
    ax2 = axes[0, 1]
    ax2.loglog(gw_data['frequencies'], gw_data['strain_spectrum'], 'b-', linewidth=2, label='Void Physics')
    ax2.axvline(gw_data['f_star'], color='r', linestyle='--', label=f'f* = {gw_data["f_star"]:.1e} Hz')
    ax2.set_xlabel('Frequency (Hz)')
    ax2.set_ylabel('Strain')
    ax2.set_title('Gravitational Wave Spectrum')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # 3. Power spectrum
    ax3 = axes[1, 0]
    ax3.loglog(gw_data['frequencies'], gw_data['power_spectrum'], 'g-', linewidth=2)
    ax3.axvline(gw_data['f_star'], color='r', linestyle='--', label=f'f* = {gw_data["f_star"]:.1e} Hz')
    ax3.set_xlabel('Frequency (Hz)')
    ax3.set_ylabel('Power Spectrum')
    ax3.set_title('GW Power Spectrum')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # 4. Baryon asymmetry
    ax4 = axes[1, 1]
    categories = ['Calculated', 'Observed']
    values = [asymmetry_data['eta_b'], asymmetry_data['eta_b_observed']]
    colors = ['blue', 'red']
    
    bars = ax4.bar(categories, values, color=colors, alpha=0.7)
    ax4.set_ylabel('Baryon Asymmetry η_b')
    ax4.set_title('Baryon Asymmetry Comparison')
    ax4.set_yscale('log')
    
    # Add value labels on bars
    for bar, value in zip(bars, values):
        height = bar.get_height()
        ax4.text(bar.get_x() + bar.get_width()/2., height,
                f'{value:.2e}', ha='center', va='bottom')
    
    plt.tight_layout()
    
    # Save plot
    output_path = Path(__file__).parent / 'cmb_signatures.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.show()
    
    print(f"   • Plot saved to: {output_path}")
    
    return {
        'cmb_data': cmb_data,
        'gw_data': gw_data,
        'asymmetry_data': asymmetry_data
    }


def main():
    """Main function."""
    
    print("🌌 Void Physics - Cosmological Predictions")
    print("=" * 50)
    
    print("\nThis example generates mock cosmological predictions from void physics:")
    print("• CMB anisotropy patterns")
    print("• Gravitational wave spectra")
    print("• Baryon asymmetry calculations")
    print()
    
    # Generate predictions
    results = create_visualizations()
    
    print("\n✅ Cosmological predictions generated!")
    print()
    print("Key results:")
    print(f"• Nucleation rate: {results['cmb_data']['nucleation_rate']:.3e}")
    print(f"• CMB dipole amplitude: {results['cmb_data']['dipole_amplitude']:.3f} mK")
    print(f"• GW characteristic frequency: {results['gw_data']['f_star']:.1e} Hz")
    print(f"• Baryon asymmetry ratio: {results['asymmetry_data']['ratio']:.3f}")
    print()
    
    print("🔬 Scientific interpretation:")
    print("• Void nucleation creates specific CMB patterns")
    print("• Gravitational waves have characteristic frequency spectrum")
    print("• Baryon asymmetry depends on CP violation during nucleation")
    print("• These predictions can be tested against observations")
    print()
    
    print("📚 References:")
    print("• Planck Collaboration (2020) - CMB observations")
    print("• LIGO/Virgo Collaboration - Gravitational wave limits")
    print("• Big Bang nucleosynthesis - Baryon asymmetry")
    print("• Coleman & De Luccia (1980) - Bubble nucleation")


if __name__ == "__main__":
    main()
