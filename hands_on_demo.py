"""
Hands-On Interactive Demonstration for Perception-X
Analyzes optical illusions, objects, and manipulated images across multiple domains:
- Physical Luminance & Spatial Frequency
- Ambiguity & Bistable States
- Saliency Localization Overlay
- Plain-Language Cognitive Perceptual Explanation
"""

import os
import glob
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

from models.perception_x_pipeline import PerceptionXPipeline

def run_hands_on_demo(samples_dir="data/samples", output_dir="outputs"):
    os.makedirs(output_dir, exist_ok=True)
    pipeline = PerceptionXPipeline()
    
    sample_files = sorted(glob.glob(os.path.join(samples_dir, "*.png")))
    if not sample_files:
        print("No sample images found. Running synthetic generators first...")
        from data.synthetic_generators import generate_all_samples
        generate_all_samples(samples_dir)
        sample_files = sorted(glob.glob(os.path.join(samples_dir, "*.png")))

    print("=" * 80)
    print("  PERCEPTION-X: OPTICAL ILLUSION & IMAGE COMPREHENSION WORKBENCH")
    print("  Synthesizing Shahgir (2024), Leong (2024), Mukherjee (2024), Maksymov (2024)")
    print("=" * 80)

    results_summary = []

    for img_path in sample_files:
        name = os.path.splitext(os.path.basename(img_path))[0]
        print(f"\n>>> PROCESSING: {name.upper()}")
        print("-" * 60)
        
        result = pipeline.process_image(img_path)
        gating = result["stage_1_problem_gating"]
        category = result["stage_2_multi_category_classification"]
        ambiguity = result["stage_3_ambiguity_analysis"]
        loc = result["stage_4_localization"]
        expl = result["stage_5_explanation"]
        
        print(f"  [Stage 1 Gating]       : {gating['decision']} (Conf: {gating['confidence']:.2%})")
        print(f"    - Is Object?        : {gating['is_object']}")
        print(f"    - Is Illusion?      : {gating['is_illusion']}")
        print(f"    - Is Forgery?       : {gating['is_forgery']}")
        print(f"  [Stage 2 Category]     : {category['category']} (Conf: {category['confidence']:.2%})")
        print(f"  [Stage 3 Multistability]: {ambiguity['status']}")
        if ambiguity["is_multistable"]:
            print(f"    - Perceptual Entropy: {ambiguity['perceptual_entropy']}")
            print(f"    - Dual States       : {ambiguity['state_distribution']}")
        print(f"  [Stage 4 Localization] : Bounding Box {loc['trigger_bounding_box_normalized']}")
        print(f"  [Stage 5 Explanation]  :")
        print(f"    - Physical Reality  : {expl['physical_reality']}")
        print(f"    - Perceived Effect  : {expl['perceptual_distortion']}")
        print(f"    - Mechanism         : {expl['scientific_mechanism'][:110]}...")

        # Create 4-panel diagnostic card
        fig, axes = plt.subplots(1, 4, figsize=(18, 4.5))
        fig.suptitle(f"Perception-X Diagnostic: {name.replace('_', ' ').title()} | Gate: {gating['decision']}", fontsize=14, fontweight='bold')

        # 1. Original Image
        orig_img = Image.open(img_path)
        axes[0].imshow(orig_img)
        axes[0].set_title("Input Image", fontsize=11, fontweight='semibold')
        axes[0].axis('off')

        # 2. Fourier Spectrum or Luminance Profile
        fourier_map = pipeline.extractor.extract_fourier_spectrum(orig_img)["magnitude_spectrum"]
        axes[1].imshow(fourier_map, cmap='magma')
        axes[1].set_title(f"2D Fourier Spectrum\n(Periodicity: {result['raw_measurements']['fourier_periodicity_ratio']:.2f})", fontsize=10)
        axes[1].axis('off')

        # 3. ELA or Feature Map
        ela_img = result["_artifacts"]["ela_pil"]
        axes[2].imshow(ela_img)
        axes[2].set_title(f"Error Level Analysis (ELA)\n(Tamper Score: {result['raw_measurements']['ela_forgery_score']:.2f})", fontsize=10)
        axes[2].axis('off')

        # 4. Localization Heatmap Overlay
        overlay_img = result["_artifacts"]["overlay_pil"]
        axes[3].imshow(overlay_img)
        # Draw bounding box
        ymin, xmin, ymax, xmax = loc["trigger_bounding_box_normalized"]
        rect = plt.Rectangle((xmin, ymin), xmax - xmin, ymax - ymin,
                             linewidth=2.5, edgecolor='lime', facecolor='none', linestyle='--')
        axes[3].add_patch(rect)
        axes[3].set_title(f"Causal Trigger Overlay\n{category['category']}", fontsize=10, fontweight='semibold', color='darkgreen')
        axes[3].axis('off')

        plt.tight_layout()
        card_path = os.path.join(output_dir, f"diagnostic_{name}.png")
        plt.savefig(card_path, dpi=180, bbox_inches='tight')
        plt.close()

        print(f"  [Saved Visual Card]   : {card_path}")

        results_summary.append({
            "name": name,
            "gate": gating["decision"],
            "category": category["category"],
            "confidence": category["confidence"],
            "multistable": ambiguity["is_multistable"],
            "card_path": card_path
        })

    print("\n" + "=" * 80)
    print("  HANDS-ON PLAYGROUND EXECUTION COMPLETE")
    print(f"  Generated {len(results_summary)} visual diagnostic cards in '{output_dir}/'")
    print("=" * 80)

    return results_summary

if __name__ == "__main__":
    run_hands_on_demo()
