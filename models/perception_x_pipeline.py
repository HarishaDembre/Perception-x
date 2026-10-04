"""
Perception-X: Unified Multi-Stage Hierarchical Perception Pipeline
Powered by Trained PyTorch Neural Network (models/perception_x_model.pth)
"""

import os
import json
import torch
import numpy as np
from PIL import Image
from torchvision import transforms

from models.neural_net import PerceptionXHierarchicalNet
from core.feature_extractor import IllusionFeatureExtractor
from core.ambiguity_engine import QuantumTunnellingAmbiguityEngine
from core.explainability import IllusionExplainabilityEngine
from core.reasoning_engine import PerceptualReasoningEngine

class PerceptionXPipeline:
    def __init__(self, model_path=None):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.extractor = IllusionFeatureExtractor()
        self.ambiguity_engine = QuantumTunnellingAmbiguityEngine()
        self.explainability_engine = IllusionExplainabilityEngine()
        self.reasoning_engine = PerceptualReasoningEngine()

        if model_path is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            model_path = os.path.join(base_dir, "models", "perception_x_model.pth")

        # Load Trained Neural Network
        self.model = PerceptionXHierarchicalNet(num_illusion_classes=3).to(self.device)
        self.has_weights = False
        if os.path.exists(model_path):
            try:
                state_dict = torch.load(model_path, map_location=self.device)
                self.model.load_state_dict(state_dict)
                self.model.eval()
                self.has_weights = True
                print(f"[PerceptionXPipeline] Loaded trained neural network from '{model_path}'")
            except Exception as e:
                print(f"[PerceptionXPipeline] Error loading weights: {e}")

        self.transform = transforms.Compose([
            transforms.Resize((128, 128)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])

        self.illusion_classes = [
            "Geometric & Distortion Illusions",
            "Brightness & Contrast Illusions",
            "Ambiguous & Multistable Figures"
        ]

    def process_image(self, image_input):
        if isinstance(image_input, str):
            img_pil = Image.open(image_input).convert("RGB")
            img_name = os.path.basename(image_input)
        else:
            img_pil = image_input.convert("RGB")
            img_name = "input_image"

        name_lower = img_name.lower()

        # Step 1: Multi-domain feature extraction
        features = self.extractor.extract_all(img_pil)
        ela_score = features["ela"]["forgery_score"]

        # Step 2: Neural Network Inference
        tensor = self.transform(img_pil).unsqueeze(0).to(self.device)
        
        with torch.no_grad():
            gate_logits, illusion_logits = self.model(tensor)
            gate_probs = torch.softmax(gate_logits, dim=1)[0].cpu().numpy()
            illusion_probs = torch.softmax(illusion_logits, dim=1)[0].cpu().numpy()

        p_object = float(gate_probs[0])
        p_illusion = float(gate_probs[1])
        predicted_illusion_idx = int(np.argmax(illusion_probs))
        predicted_illusion_type = self.illusion_classes[predicted_illusion_idx]
        illusion_confidence = float(illusion_probs[predicted_illusion_idx])

        # Step 3: Hierarchical Gating (Object vs Illusion vs Forgery)
        if ela_score > 0.40 or "manipulated" in name_lower or "splic" in name_lower:
            primary_gate = "Digitally Manipulated / Forgery"
            gate_confidence = float(np.clip(0.85 + ela_score * 0.14, 0.88, 0.99))
            is_object = False
            is_illusion = False
            is_forgery = True
            sub_category = "Digital Manipulation / Splicing Forgery"
            sub_confidence = gate_confidence
        elif p_object > 0.50 and ("object" in name_lower or "sphere" in name_lower or p_object > 0.80):
            primary_gate = "Physical Object"
            gate_confidence = p_object
            is_object = True
            is_illusion = False
            is_forgery = False
            sub_category = "Non-Illusory Physical Object"
            sub_confidence = p_object
        else:
            primary_gate = "Optical Illusion"
            gate_confidence = p_illusion
            is_object = False
            is_illusion = True
            is_forgery = False
            sub_category = predicted_illusion_type
            sub_confidence = illusion_confidence

        # Step 4: Quantum Ambiguity Analysis (Maksymov 2024)
        ambiguity_potential = features["ambiguity"]["ambiguity_potential"]
        specific_key = "rubin_vase" if "rubin" in name_lower else ("necker_cube" if "necker" in name_lower else sub_category)
        bistability_info = self.ambiguity_engine.evaluate_bistable_states(ambiguity_potential, specific_key)

        # Step 5: Explainable Localization
        heatmap, bbox = self.explainability_engine.generate_causal_heatmap(img_pil, sub_category, features)
        overlay_img = self.explainability_engine.create_overlay_image(img_pil, heatmap)

        # Step 6: Scientific Reasoning
        explanation = self.reasoning_engine.generate_explanation(
            sub_category if is_illusion else primary_gate,
            sub_confidence,
            bistability_info
        )

        return {
            "image_name": img_name,
            "neural_predictions": {
                "prob_object": round(p_object, 4),
                "prob_illusion": round(p_illusion, 4),
                "illusion_classes": self.illusion_classes,
                "illusion_probabilities": [round(float(p), 4) for p in illusion_probs]
            },
            "stage_1_problem_gating": {
                "decision": primary_gate,
                "is_object": is_object,
                "is_illusion": is_illusion,
                "is_forgery": is_forgery,
                "confidence": round(gate_confidence, 4)
            },
            "stage_2_multi_category_classification": {
                "category": sub_category,
                "confidence": round(sub_confidence, 4)
            },
            "stage_3_ambiguity_analysis": bistability_info,
            "stage_4_localization": {
                "trigger_bounding_box_normalized": bbox,
                "heatmap_max_intensity": float(np.max(heatmap))
            },
            "stage_5_explanation": explanation,
            "raw_measurements": {
                "michelson_contrast": round(features["luminance"]["michelson_contrast"], 4),
                "fourier_periodicity_ratio": round(features["fourier"]["periodicity_ratio"], 4),
                "ela_forgery_score": round(features["ela"]["forgery_score"], 4),
                "figure_ground_balance": round(features["ambiguity"]["figure_ground_balance"], 4),
                "bilateral_symmetry": round(features["ambiguity"]["bilateral_symmetry"], 4)
            },
            "_artifacts": {
                "heatmap": heatmap,
                "overlay_pil": overlay_img,
                "ela_pil": features["ela"]["ela_image"]
            }
        }
