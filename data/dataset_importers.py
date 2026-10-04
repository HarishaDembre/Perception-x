"""
Dataset Importers & Catalog for Perception-X Optical Illusion Analysis
Covers all 5 papers reviewed:
1. IllusionVQA (Shahgir et al., 2024 - COLM 2024)
2. Multi-Modal Optical Illusion Dataset (Leong, 2024 - IEEE ISWTA)
3. Brightness-Contrast Psychophysical Dataset (Mukherjee et al., 2024 - Springer)
4. Synthetic Ambiguous Figures & Multistable Dataset (Maksymov, 2024 - AIP)
5. CASIA / CoMoFoD Forgery & Deepfake Datasets (DeepForgeryNet, 2026 - Frontiers in AI)
"""

import os
import json
import numpy as np
from PIL import Image

DATASET_CATALOG = {
    "IllusionVQA": {
        "paper": "IllusionVQA: A Challenging Optical Illusion Dataset for Vision Language Models",
        "authors": "H.S. Shahgir, K.S. Sayeed, A. Bhattacharjee, W.U. Ahmad, Y. Dong, R. Shahriyar (2024)",
        "venue": "COLM 2024 (Conference on Language Modeling)",
        "identifier": "ahmadki/IllusionVQA",
        "type": "Multi-Modal Visual Question Answering (VQA) & Localization",
        "format": "Parquet / JSON + PNG images",
        "size": "686 high-resolution illusion questions & annotations",
        "categories": [
            "Geometric Distortion", "Brightness & Contrast", "Ambiguous Figures",
            "Impossible Objects", "Perspective & Size Distortion", "Camouflage / Hidden Art"
        ],
        "key_features": [
            "image_id: Unique identifier",
            "image: PIL.Image RGB raster",
            "question: Human perceptual prompt (e.g., 'Which horizontal line is longer?')",
            "options: List of 4 multiple-choice answers [A, B, C, D]",
            "answer: Ground-truth index of correct perception",
            "illusion_category: Semantic category label",
            "soft_localization_bbox: Normalized [ymin, xmin, ymax, xmax] of illusion trigger region",
            "human_accuracy: Baseline human accuracy (averaging ~87-92%)",
            "vlm_accuracy: Benchmark accuracy across GPT-4V (63%), Gemini, LLaVA (<50%)"
        ],
        "import_snippet": """
# Option A: Hugging Face Datasets Library
from datasets import load_dataset
dataset = load_dataset('ahmadki/IllusionVQA')
sample = dataset['test'][0]
image = sample['image']
question = sample['question']
options = sample['options']

# Option B: Direct Git Clone
# git clone https://github.com/ahmadki/IllusionVQA.git
"""
    },
    "MultiModal_Illusion_Corpus": {
        "paper": "A Multi-Modal Deep Learning Approach for Enhanced Optical Illusion Recognition",
        "authors": "W.Y. Leong (2024)",
        "venue": "IEEE 8th Symposium on Wireless Technology & Applications (ISWTA 2024)",
        "type": "Graph-Structured Image Corpus for CNN-GNN Fusion",
        "format": "RGB Images + Region Adjacency Graphs (PyTorch Geometric)",
        "size": "~1,200 curated illusion stimuli + control images",
        "categories": ["Geometric Illusions", "Color & Chromatic Induction", "Motion / Peripheral Drift"],
        "key_features": [
            "visual_tensor: [3, 224, 224] normalized image tensor",
            "region_nodes: Visual patch embedding vectors (D=512)",
            "adjacency_matrix: Graph edges representing spatial connectivity & alignment",
            "cognitive_prior: Categorical prior vector based on visual psychophysics",
            "label: 3-class or 8-class illusion category ID"
        ],
        "import_snippet": """
# Custom PyTorch Dataset Loader
import torch
from torchvision import datasets, transforms

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])
# dataset = datasets.ImageFolder('path/to/multimodal_illusion_corpus', transform=transform)
"""
    },
    "Brightness_Contrast_Dataset": {
        "paper": "Deep Learning Models for Perception of Brightness Related Illusions",
        "authors": "A. Mukherjee, A. Paul, K. Ghosh (2024)",
        "venue": "Applied Intelligence (Springer), Vol. 54(21)",
        "type": "Psychophysical Luminance & Perceptual Contrast Response Matrix",
        "format": "NumPy arrays / Grayscale TIFF / PNG",
        "size": "Standardized battery of 14 classical brightness illusion stimuli with cross-sectional profiles",
        "categories": [
            "Hermann Grid", "White's Illusion", "Grating Induction",
            "Simultaneous Brightness Contrast", "Mach Bands", "Todorovic Illusion"
        ],
        "key_features": [
            "physical_luminance_map: Exact physical pixel intensity matrix [0..255]",
            "human_perceived_brightness_profile: Measured psychophysical luminance response curve",
            "lateral_inhibition_mask: Region of receptive field antagonism",
            "target_patch_coordinates: Coordinates of test patches undergoing induction"
        ],
        "import_snippet": """
import numpy as np
from PIL import Image

def load_brightness_stimulus(image_path):
    img = Image.open(image_path).convert('L')
    physical_matrix = np.array(img, dtype=np.float32) / 255.0
    # Cross-sectional luminance profile across center row:
    center_row = physical_matrix[physical_matrix.shape[0] // 2, :]
    return physical_matrix, center_row
"""
    },
    "Ambiguous_Multistable_Stimuli": {
        "paper": "Quantum-Tunnelling Deep Neural Network for Optical Illusion Recognition",
        "authors": "I.S. Maksymov (2024)",
        "venue": "APL Machine Learning, AIP Publishing",
        "type": "Bistable & Multistable Perceptual Switching Stimuli",
        "format": "Vector wireframes / Binary masks / Temporal state series",
        "size": "Synthetically parameterized bistable stimuli suite",
        "categories": [
            "Necker Cube (3D Wireframe Reversal)", "Rubin's Vase (Figure-Ground Ambiguity)",
            "Duck-Rabbit (Semantic Bistability)", "Schroder Staircase (Perspective Reversal)"
        ],
        "key_features": [
            "stimulus_geometry: High-contrast 2D edge / silhouette representation",
            "interpretation_A: Semantic label for state 1 (e.g., 'Face / Front-Facing')",
            "interpretation_B: Semantic label for state 2 (e.g., 'Vase / Back-Facing')",
            "perceptual_entropy: Shannon entropy of bistable probability distribution",
            "tunnelling_barrier_potential: Non-linear energy parameter governing perceptual switching"
        ],
        "import_snippet": """
# Dual-state representation dictionary
bistable_entry = {
    'name': 'rubin_vase',
    'state_A': {'label': 'Two Facing Profiles', 'prior': 0.50},
    'state_B': {'label': 'Central Chalice/Vase', 'prior': 0.50},
    'entropy': 1.00 # Max ambiguity
}
"""
    },
    "CASIA_CoMoFoD_Forgery_Benchmarks": {
        "paper": "DeepForgeryNet: A Hybrid CNN-LSTM and Transfer Learning Framework",
        "authors": "DeepForgeryNet Authors (2026)",
        "venue": "Frontiers in Artificial Intelligence",
        "type": "Digital Manipulation & Forgery Benchmark Datasets",
        "format": "High-resolution JPEG/TIFF with ground-truth binary tampering masks",
        "size": "CASIA v1.0 (1,721 images), CASIA v2.0 (12,614 images), CoMoFoD (5,000 images)",
        "categories": ["Splicing (Cut-and-Paste)", "Copy-Move Forgery", "Deepfake Generation", "Color Manipulation"],
        "key_features": [
            "authentic_image: Untampered natural reference image",
            "tampered_image: Spliced or copy-moved test image",
            "ground_truth_mask: Binary mask indicating forged pixels (1=forged, 0=authentic)",
            "ela_residual: Error Level Analysis compression difference map",
            "dct_coefficients: Discrete Cosine Transform blocking artifact frequency map"
        ],
        "import_snippet": """
# ELA (Error Level Analysis) pipeline for detecting digital manipulation:
from PIL import Image, ImageChops, ImageEnhance
import io

def compute_ela(image_path, quality=90, scale=15):
    original = Image.open(image_path).convert('RGB')
    buffer = io.BytesIO()
    original.save(buffer, 'JPEG', quality=quality)
    buffer.seek(0)
    resaved = Image.open(buffer)
    ela = ImageChops.difference(original, resaved)
    extrema = ela.getextrema()
    max_diff = max([ex[1] for ex in extrema])
    scale_factor = scale if max_diff == 0 else 255.0 / max_diff
    return ImageEnhance.Brightness(ela).enhance(scale_factor)
"""
    }
}

def export_catalog_json(out_file="data/dataset_catalog.json"):
    os.makedirs(os.path.dirname(out_file), exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(DATASET_CATALOG, f, indent=2)
    print(f"Dataset catalog exported to {out_file}")

if __name__ == "__main__":
    export_catalog_json()
    print("Catalog summary:")
    for k, v in DATASET_CATALOG.items():
        print(f" - [{k}]: {v['paper']} ({v['type']})")
