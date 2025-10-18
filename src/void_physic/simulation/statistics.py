"""
Statistical analysis for void physics simulations.

This module provides statistical tools for analyzing void physics simulations,
including first passage time analysis, entropy calculations, and rare event statistics.
"""

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import scipy.optimize
import scipy.stats

from ..core.potential import DoubleWellPotential
from ..utils.constants import PhysicalConstants


@dataclass
class StatisticalParameters:
    """Parameters for statistical analysis."""

    confidence_level: float = 0.95  # Confidence level for intervals
    n_bootstrap: int = 1000  # Number of bootstrap samples
    bin_width: float = 0.1  # Histogram bin width
    kernel_bandwidth: float = 0.1  # Kernel density estimation bandwidth


class FirstPassageTime:
    """
    Analysis of first passage times in void physics.

    First passage times represent the time it takes for the field to transition
    from the void state to an ordered state, which is central to void physics.
    """

    def __init__(self, parameters: Optional[StatisticalParameters] = None):
        """
        Initialize first passage time analyzer.

        Args:
            parameters: Statistical parameters
        """
        self.params = parameters or StatisticalParameters()

    def fit_exponential_distribution(self, fpt_times: np.ndarray) -> Dict[str, Any]:
        """
        Fit exponential distribution to first passage times.

        For simple barrier crossing, FPT often follows exponential distribution:
        P(t) = λ exp(-λt)

        Args:
            fpt_times: First passage time data

        Returns:
            Dictionary with fit parameters and statistics
        """
        # Remove infinite times
        finite_times = fpt_times[fpt_times != np.inf]

        if len(finite_times) == 0:
            return {"rate": 0.0, "mean": np.inf, "fit_success": False}

        # Fit exponential distribution
        try:
            # When floc=0, expon.fit returns only (scale,) not (loc, scale)
            fit_params = scipy.stats.expon.fit(finite_times, floc=0)
            if len(fit_params) == 1:
                scale = fit_params[0]
                loc = 0.0
            else:
                loc, scale = fit_params
            rate = 1.0 / scale
            mean_fpt = scale

            # Goodness of fit test
            ks_stat, p_value = scipy.stats.kstest(
                finite_times, lambda x: scipy.stats.expon.cdf(x, loc, scale)
            )

            return {
                "rate": rate,
                "mean": mean_fpt,
                "scale": scale,
                "ks_statistic": ks_stat,
                "p_value": p_value,
                "fit_success": p_value > 0.05,
                "n_samples": len(finite_times),
            }
        except Exception as e:
            return {"rate": 0.0, "mean": np.inf, "fit_success": False, "error": str(e)}

    def fit_weibull_distribution(self, fpt_times: np.ndarray) -> Dict[str, Any]:
        """
        Fit Weibull distribution to first passage times.

        Weibull distribution is more general than exponential:
        P(t) = (k/λ)(t/λ)^(k-1) exp(-(t/λ)^k)

        Args:
            fpt_times: First passage time data

        Returns:
            Dictionary with fit parameters and statistics
        """
        finite_times = fpt_times[fpt_times != np.inf]

        if len(finite_times) == 0:
            return {"shape": 0.0, "scale": 0.0, "fit_success": False}

        try:
            shape, loc, scale = scipy.stats.weibull_min.fit(finite_times, floc=0)

            # Goodness of fit
            ks_stat, p_value = scipy.stats.kstest(
                finite_times,
                lambda x: scipy.stats.weibull_min.cdf(x, shape, loc, scale),
            )

            return {
                "shape": shape,
                "scale": scale,
                "ks_statistic": ks_stat,
                "p_value": p_value,
                "fit_success": p_value > 0.05,
                "n_samples": len(finite_times),
            }
        except Exception as e:
            return {"shape": 0.0, "scale": 0.0, "fit_success": False, "error": str(e)}

    def survival_function(
        self, fpt_times: np.ndarray, time_points: np.ndarray
    ) -> np.ndarray:
        """
        Calculate empirical survival function.

        S(t) = P(T > t) where T is the first passage time.

        Args:
            fpt_times: First passage time data
            time_points: Time points to evaluate survival function

        Returns:
            Survival function values
        """
        finite_times = fpt_times[fpt_times != np.inf]

        if len(finite_times) == 0:
            return np.zeros_like(time_points)

        survival = np.zeros_like(time_points)

        for i, t in enumerate(time_points):
            survival[i] = np.mean(finite_times > t)

        return survival

    def hazard_function(
        self, fpt_times: np.ndarray, time_points: np.ndarray
    ) -> np.ndarray:
        """
        Calculate empirical hazard function.

        h(t) = f(t)/S(t) where f(t) is the probability density and S(t) is survival function.

        Args:
            fpt_times: First passage time data
            time_points: Time points to evaluate hazard function

        Returns:
            Hazard function values
        """
        finite_times = fpt_times[fpt_times != np.inf]

        if len(finite_times) == 0:
            return np.zeros_like(time_points)

        # Use kernel density estimation for probability density
        if len(finite_times) > 1:
            kde = scipy.stats.gaussian_kde(
                finite_times, bw_method=self.params.kernel_bandwidth
            )
            pdf = kde(time_points)
        else:
            pdf = np.zeros_like(time_points)

        # Calculate survival function
        survival = self.survival_function(fpt_times, time_points)

        # Hazard function: h(t) = f(t)/S(t)
        hazard = np.divide(pdf, survival, out=np.zeros_like(pdf), where=survival > 0)

        return hazard

    def confidence_intervals(
        self, fpt_times: np.ndarray, alpha: Optional[float] = None
    ) -> Dict[str, float]:
        """
        Calculate confidence intervals for first passage time statistics.

        Args:
            fpt_times: First passage time data
            alpha: Significance level (uses default if None)

        Returns:
            Dictionary with confidence intervals
        """
        if alpha is None:
            alpha = 1 - self.params.confidence_level

        finite_times = fpt_times[fpt_times != np.inf]

        if len(finite_times) == 0:
            return {"mean_lower": np.inf, "mean_upper": np.inf}

        # Bootstrap confidence intervals
        bootstrap_means: List[float] = []
        for _ in range(self.params.n_bootstrap):
            bootstrap_sample = np.random.choice(
                finite_times, size=len(finite_times), replace=True
            )
            bootstrap_means.append(np.mean(bootstrap_sample))

        bootstrap_means_array = np.array(bootstrap_means)

        # Calculate percentiles
        lower_percentile = 100 * alpha / 2
        upper_percentile = 100 * (1 - alpha / 2)

        mean_lower = np.percentile(bootstrap_means_array, lower_percentile)
        mean_upper = np.percentile(bootstrap_means_array, upper_percentile)

        return {
            "mean_lower": mean_lower,
            "mean_upper": mean_upper,
            "mean_estimate": np.mean(finite_times),
            "std_estimate": np.std(finite_times),
        }


class EntropyCalculator:
    """
    Calculate entropy and related thermodynamic quantities for void physics.

    Entropy plays a crucial role in void physics as it drives the emergence
    of time and the transition from reversible void to irreversible cosmos.
    """

    def __init__(self, parameters: Optional[StatisticalParameters] = None):
        """
        Initialize entropy calculator.

        Args:
            parameters: Statistical parameters
        """
        self.params = parameters or StatisticalParameters()

    def field_entropy(
        self, phi_trajectories: np.ndarray, time_points: np.ndarray
    ) -> np.ndarray:
        """
        Calculate entropy of field distribution over time.

        S(t) = -∫ P(φ,t) log P(φ,t) dφ

        Args:
            phi_trajectories: Field trajectories (n_trajectories, n_times)
            time_points: Time points

        Returns:
            Entropy as function of time
        """
        n_trajectories, n_times = phi_trajectories.shape
        entropy = np.zeros(n_times)

        for i in range(n_times):
            phi_values = phi_trajectories[:, i]

            # Remove any NaN or infinite values
            phi_values = phi_values[np.isfinite(phi_values)]

            if len(phi_values) < 2:
                entropy[i] = 0.0
                continue

            # Use kernel density estimation to get probability density
            try:
                kde = scipy.stats.gaussian_kde(
                    phi_values, bw_method=self.params.kernel_bandwidth
                )

                # Evaluate on a grid
                phi_min, phi_max = np.min(phi_values), np.max(phi_values)
                phi_grid = np.linspace(phi_min, phi_max, 100)
                pdf = kde(phi_grid)

                # Calculate entropy: S = -∫ p(x) log p(x) dx
                # Avoid log(0) by adding small epsilon
                epsilon = 1e-10
                pdf = np.maximum(pdf, epsilon)
                log_pdf = np.log(pdf)

                # Integrate using trapezoidal rule
                entropy[i] = -np.trapezoid(pdf * log_pdf, phi_grid)

            except Exception:
                # Fallback: use variance as entropy proxy
                variance = np.var(phi_values)
                if variance > 0:
                    entropy[i] = 0.5 * np.log(2 * np.pi * np.e * variance)
                else:
                    entropy[i] = 0.0

        return entropy

    def mutual_information(
        self,
        phi1_trajectories: np.ndarray,
        phi2_trajectories: np.ndarray,
        time_points: np.ndarray,
    ) -> np.ndarray:
        """
        Calculate mutual information between two field components.

        I(φ₁, φ₂) = S(φ₁) + S(φ₂) - S(φ₁, φ₂)

        Args:
            phi1_trajectories: First field trajectories
            phi2_trajectories: Second field trajectories
            time_points: Time points

        Returns:
            Mutual information as function of time
        """
        n_trajectories, n_times = phi1_trajectories.shape

        # Individual entropies
        S1 = self.field_entropy(phi1_trajectories, time_points)
        S2 = self.field_entropy(phi2_trajectories, time_points)

        # Joint entropy
        joint_entropy = np.zeros(n_times)

        for i in range(n_times):
            phi1_values = phi1_trajectories[:, i]
            phi2_values = phi2_trajectories[:, i]

            # Remove invalid values
            valid_mask = np.isfinite(phi1_values) & np.isfinite(phi2_values)
            phi1_values = phi1_values[valid_mask]
            phi2_values = phi2_values[valid_mask]

            if len(phi1_values) < 2:
                joint_entropy[i] = 0.0
                continue

            try:
                # 2D kernel density estimation
                values = np.vstack([phi1_values, phi2_values])
                kde = scipy.stats.gaussian_kde(values)

                # Evaluate on a 2D grid
                phi1_min, phi1_max = np.min(phi1_values), np.max(phi1_values)
                phi2_min, phi2_max = np.min(phi2_values), np.max(phi2_values)

                phi1_grid = np.linspace(phi1_min, phi1_max, 50)
                phi2_grid = np.linspace(phi2_min, phi2_max, 50)
                phi1_mesh, phi2_mesh = np.meshgrid(phi1_grid, phi2_grid)

                points = np.vstack([phi1_mesh.ravel(), phi2_mesh.ravel()])
                pdf = kde(points).reshape(phi1_mesh.shape)

                # Calculate joint entropy
                epsilon = 1e-10
                pdf = np.maximum(pdf, epsilon)
                log_pdf = np.log(pdf)

                # 2D integration
                joint_entropy[i] = -np.trapezoid(
                    np.trapezoid(pdf * log_pdf, phi1_grid, axis=1), phi2_grid
                )

            except Exception:
                # Fallback: use covariance as proxy
                cov_matrix = np.cov(phi1_values, phi2_values)
                joint_entropy[i] = 0.5 * np.log(
                    (2 * np.pi * np.e) ** 2 * np.linalg.det(cov_matrix)
                )

        # Mutual information
        mutual_info = S1 + S2 - joint_entropy

        return mutual_info

    def entropy_production_rate(
        self, entropy: np.ndarray, time_points: np.ndarray
    ) -> np.ndarray:
        """
        Calculate entropy production rate: dS/dt

        Args:
            entropy: Entropy values
            time_points: Time points

        Returns:
            Entropy production rate
        """
        # Numerical derivative
        dS_dt = np.gradient(entropy, time_points)
        return dS_dt

    def thermodynamic_quantities(
        self,
        phi_trajectories: np.ndarray,
        time_points: np.ndarray,
        potential: Optional[DoubleWellPotential] = None,
    ) -> Dict[str, np.ndarray]:
        """
        Calculate various thermodynamic quantities.

        Args:
            phi_trajectories: Field trajectories
            time_points: Time points
            potential: Field potential (uses default if None)

        Returns:
            Dictionary with thermodynamic quantities
        """
        if potential is None:
            potential = DoubleWellPotential()

        n_trajectories, n_times = phi_trajectories.shape

        # Calculate ensemble averages
        mean_phi = np.mean(phi_trajectories, axis=0)
        var_phi = np.var(phi_trajectories, axis=0)

        # Calculate energy components
        mean_energy = np.zeros(n_times)
        mean_potential = np.zeros(n_times)

        for i in range(n_times):
            phi_values = phi_trajectories[:, i]
            potential_values = potential(phi_values)
            mean_potential[i] = np.mean(potential_values)

            # Kinetic energy (approximate from variance)
            # E_kin ≈ (1/2) * var(φ) * ω² where ω is characteristic frequency
            mean_energy[i] = mean_potential[i] + 0.5 * var_phi[i]

        # Calculate entropy
        entropy = self.field_entropy(phi_trajectories, time_points)
        entropy_rate = self.entropy_production_rate(entropy, time_points)

        # Calculate temperature (from equipartition theorem)
        # T ≈ 2⟨E_kin⟩/k_B (in natural units, k_B = 1)
        temperature = 2 * (mean_energy - mean_potential)

        # Calculate free energy: F = E - TS
        # Handle case where temperature might be zero or negative
        # Use element-wise operations for arrays
        free_energy = np.where(
            temperature > 0, mean_energy - temperature * entropy, mean_energy
        )

        return {
            "time": time_points,
            "entropy": entropy,
            "entropy_rate": entropy_rate,
            "mean_energy": mean_energy,
            "mean_potential": mean_potential,
            "temperature": temperature,
            "free_energy": free_energy,
            "mean_field": mean_phi,
            "field_variance": var_phi,
        }

    def phase_transition_indicators(
        self, phi_trajectories: np.ndarray, time_points: np.ndarray
    ) -> Dict[str, np.ndarray]:
        """
        Calculate indicators of phase transitions.

        Args:
            phi_trajectories: Field trajectories
            time_points: Time points

        Returns:
            Dictionary with phase transition indicators
        """
        n_trajectories, n_times = phi_trajectories.shape

        # Order parameter (mean field)
        order_parameter = np.mean(phi_trajectories, axis=0)

        # Susceptibility (field variance)
        susceptibility = np.var(phi_trajectories, axis=0)

        # Binder cumulant (fourth moment)
        binder_cumulant = np.zeros(n_times)
        for i in range(n_times):
            phi_values = phi_trajectories[:, i]
            if len(phi_values) > 0:
                mean_phi = np.mean(phi_values)
                fourth_moment = np.mean((phi_values - mean_phi) ** 4)
                second_moment = np.mean((phi_values - mean_phi) ** 2)

                if second_moment > 0:
                    binder_cumulant[i] = 1 - fourth_moment / (3 * second_moment**2)
                else:
                    binder_cumulant[i] = 0.0

        # Correlation length (simplified)
        correlation_length = np.sqrt(susceptibility)

        return {
            "time": time_points,
            "order_parameter": order_parameter,
            "susceptibility": susceptibility,
            "binder_cumulant": binder_cumulant,
            "correlation_length": correlation_length,
        }
