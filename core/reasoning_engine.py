"""
Cognitive-Science & Psychophysical Perceptual Reasoning Engine
Synthesizes scientific explanations for human perception vs. physical reality.
"""

class PerceptualReasoningEngine:
    def __init__(self):
        self.explanations_kb = {
            "Brightness & Contrast Illusions": {
                "phenomenon": "Brightness / Contrast Induction & Lateral Inhibition",
                "physical_reality": "The physical pixel luminance at intersections or test patches is mathematically uniform.",
                "perceptual_distortion": "The human visual cortex perceives phantom gray spots or perceives identical gray patches as having unequal brightness.",
                "neurobiological_mechanism": (
                    "Arises from On-Center / Off-Surround retinal ganglion cells undergoing lateral inhibition. "
                    "At grid intersections, a ganglion cell receives inhibitory signals from four surrounding bright channels, "
                    "suppressing its firing rate compared to cells positioned along straight channels (inhibited from only two sides). "
                    "This drop in neural response is decoded by V1 as darker illusory patches."
                )
            },
            "Geometric & Distortion Illusions": {
                "phenomenon": "Geometric Misalignment & Size-Constancy Distortion",
                "physical_reality": "The target line segments are strictly parallel, straight, or equal in Euclidean length.",
                "perceptual_distortion": "Lines appear bent, tilted, or of markedly unequal length.",
                "neurobiological_mechanism": (
                    "Triggered by size-constancy scaling mechanisms in the ventral visual pathway. "
                    "Inward-pointing fins mimic the near edge of a 3D convex structure (closer object), "
                    "whereas outward-pointing fins mimic the far corner of a room (distant object). "
                    "The brain automatically scales up the perceived length of the 'distant' segment. "
                    "In Cafe Wall illusions, border-locking between high-contrast tiles tilts orientation-selective simple cells in V1."
                )
            },
            "Ambiguous & Multistable Figures": {
                "phenomenon": "Perceptual Bistability & Figure-Ground Rivalry",
                "physical_reality": "A single stationary 2D pattern with symmetrical high-contrast contours.",
                "perceptual_distortion": "The observer perceives spontaneous, alternating switching between two distinct semantic entities.",
                "neurobiological_mechanism": (
                    "Explained by neural competition between mutually inhibitory neuronal populations in the temporal cortex. "
                    "Because both interpretations (e.g., face profiles vs. central chalice, or front vs. rear cube cube face) "
                    "have equal Bayesian priors and identical sensory support, neural adaptation (synaptic fatigue) causes "
                    "the dominant neural assembly to weaken, allowing the competing assembly to cross the perceptual threshold."
                )
            },
            "Digitally Manipulated / Forgery": {
                "phenomenon": "Digital Synthesis / Image Tampering",
                "physical_reality": "High-frequency compression residuals and boundary artifacts inconsistent with natural imaging physics.",
                "perceptual_distortion": "Appears as a convincing composite to the naked human eye but contains forensic anomalies.",
                "neurobiological_mechanism": (
                    "Human perception lacks low-level sensor sensitivity to detect re-compression block artifacts or subtle "
                    "JPEG quantization mismatch. Forensic Error Level Analysis (ELA) reveals artificial splicing boundaries."
                )
            },
            "Normal / Unambiguous Object": {
                "phenomenon": "Unambiguous Natural Perception",
                "physical_reality": "Continuous Lambertian reflectance and consistent directional lighting gradients.",
                "perceptual_distortion": "None. Perceived geometry and luminance faithfully align with physical reality.",
                "neurobiological_mechanism": (
                    "Visual processing follows coherent forward inference in V1-V4 and IT cortex without contradictory "
                    "receptive field inhibition or ambiguous figure-ground cues."
                )
            }
        }

    def generate_explanation(self, category_name, confidence, bistability_info=None):
        info = self.explanations_kb.get(category_name, self.explanations_kb["Normal / Unambiguous Object"])
        
        explanation = {
            "category": category_name,
            "confidence_score": round(confidence, 4),
            "phenomenon": info["phenomenon"],
            "physical_reality": info["physical_reality"],
            "perceptual_distortion": info["perceptual_distortion"],
            "scientific_mechanism": info["neurobiological_mechanism"]
        }
        
        if bistability_info and bistability_info.get("is_multistable"):
            explanation["multistable_resolution"] = {
                "entropy": bistability_info["perceptual_entropy"],
                "switching_probability": bistability_info["switching_probability"],
                "dual_states": bistability_info["state_distribution"],
                "recommendation": "Do NOT force single label; report dual perceptual states."
            }
            
        return explanation
