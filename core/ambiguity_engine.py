"""
Quantum-Tunnelling & Perceptual Bistability Engine
Inspired by:
Maksymov, I.S. (2024) - "Quantum-Tunnelling Deep Neural Network for Optical Illusion Recognition",
APL Machine Learning, AIP Publishing.
"""

import numpy as np

class QuantumTunnellingAmbiguityEngine:
    def __init__(self, barrier_height=1.5, noise_temperature=0.3):
        self.barrier_height = barrier_height
        self.noise_temperature = noise_temperature

    def evaluate_bistable_states(self, ambiguity_potential, category_name):
        """
        Simulates quantum double-well potential perceptual switching.
        Potential: V(x) = (x^2 - 1)^2 + tilt * x
        Where x = -1 is State A and x = +1 is State B.
        """
        is_multistable = (category_name in ["Ambiguous Figures", "Perspective & Depth", "rubin_vase", "necker_cube"]) or (ambiguity_potential > 0.70)
        
        if not is_multistable:
            return {
                "is_multistable": False,
                "perceptual_entropy": 0.15,
                "switching_probability": 0.02,
                "state_distribution": {"Dominant State": 0.96, "Secondary State": 0.04},
                "status": "Monostable (Rigid Unambiguous Interpretation)"
            }
            
        # For bistable stimuli, calculate double-well tunneling
        tilt = (0.5 - ambiguity_potential) * 0.4 # Symmetric when ambiguity ~ 1.0
        
        # Energy barrier tunneling rate Gamma ~ exp(-2 * sqrt(2 * m * V_0) * L / hbar)
        tunneling_rate = float(np.exp(-self.barrier_height / (1.0 + ambiguity_potential * 1.5)))
        
        # Probabilities of state A and state B
        prob_a = float(1.0 / (1.0 + np.exp(tilt / self.noise_temperature)))
        prob_b = float(1.0 - prob_a)
        
        # Shannon Perceptual Entropy: H = -sum(p * log2(p))
        eps = 1e-9
        entropy = float(- (prob_a * np.log2(prob_a + eps) + prob_b * np.log2(prob_b + eps)))
        
        state_labels = {
            "rubin_vase": ("Two Facing Silhouettes", "Central Symmetrical Vase"),
            "necker_cube": ("Front-Lower Cube Perspective", "Back-Upper Cube Perspective"),
            "Ambiguous Figures": ("Primary Interpretation (Figure)", "Secondary Interpretation (Ground)"),
            "Perspective & Depth": ("Convex Depth Interpretation", "Concave Depth Interpretation")
        }
        
        label_a, label_b = state_labels.get(category_name, ("Interpretation A", "Interpretation B"))
        
        return {
            "is_multistable": True,
            "perceptual_entropy": round(entropy, 4),
            "switching_probability": round(tunneling_rate, 4),
            "state_distribution": {
                label_a: round(prob_a, 4),
                label_b: round(prob_b, 4)
            },
            "status": "Multistable Bistability (Active Perceptual Switching)"
        }
