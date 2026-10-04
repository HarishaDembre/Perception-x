import os
import json
from models.perception_x_pipeline import PerceptionXPipeline

def run_deep_analysis():
    pipeline = PerceptionXPipeline()
    samples_dir = "data/samples"
    
    print("=" * 90)
    print("           PERCEPTION-X: IN-DEPTH OPTICAL ILLUSION & IMAGE ANALYSIS WORKBENCH")
    print("       Multi-Category Perception, Problem Gating, Feature Attribution & Cognitive Reasoning")
    print("=" * 90)
    
    stimuli = [
        ("cafe_wall.png", "Café Wall Illusion", "Geometric / Tilt Distortion"),
        ("hermann_grid.png", "Hermann Grid Illusion", "Brightness / Lateral Inhibition"),
        ("muller_lyer.png", "Müller-Lyer Illusion", "Geometric / Arrowhead Length Distortion"),
        ("rubin_vase.png", "Rubin's Vase Silhouette", "Ambiguous / Figure-Ground Bistability"),
        ("necker_cube.png", "Necker Cube Wireframe", "Ambiguous / 3D Multistable Depth"),
        ("simultaneous_contrast.png", "Simultaneous Contrast", "Brightness / Center-Surround Induction"),
        ("natural_object.png", "Shaded Sphere Object", "Normal / Non-Illusory Physical Object"),
        ("manipulated_splicing.png", "Digitally Spliced Image", "Forensic Forgery / Digital Tampering")
    ]
    
    for filename, title, family in stimuli:
        path = os.path.join(samples_dir, filename)
        if not os.path.exists(path):
            continue
            
        res = pipeline.process_image(path)
        gating = res["stage_1_problem_gating"]
        category = res["stage_2_multi_category_classification"]
        ambiguity = res["stage_3_ambiguity_analysis"]
        loc = res["stage_4_localization"]
        expl = res["stage_5_explanation"]
        raw = res["raw_measurements"]
        
        print("\n" + "#" * 90)
        print(f"  ANALYSIS FOR: {title.upper()} ({family})")
        print("#" * 90)
        
        print("\n  [1. STAGE 1: PROBLEM GATING DECISION]")
        print(f"      • Final Decision   : {gating['decision']}")
        print(f"      • Confidence Score : {gating['confidence']:.2%}")
        print(f"      • Is Real Object?  : {gating['is_object']}")
        print(f"      • Is Illusion?     : {gating['is_illusion']}")
        print(f"      • Is Forgery?      : {gating['is_forgery']}")
        
        print("\n  [2. STAGE 2: MULTI-CATEGORY ILLUSION CLASSIFICATION]")
        print(f"      • Assigned Category: {category['category']}")
        print(f"      • Category Conf.   : {category['confidence']:.2%}")
        
        print("\n  [3. STAGE 3: MULTISTABILITY & BISTABLE RESOLUTION (Maksymov 2024)]")
        print(f"      • Ambiguity Status : {ambiguity['status']}")
        if ambiguity["is_multistable"]:
            print(f"      • Perceptual Entropy (H): {ambiguity['perceptual_entropy']} (Max ambiguity ~ 1.0)")
            print(f"      • Quantum Tunneling Rate: {ambiguity['switching_probability']}")
            print(f"      • Dual-State Probabilities:")
            for state_name, prob in ambiguity["state_distribution"].items():
                print(f"          - {state_name:<30}: {prob:.2%}")
        else:
            print(f"      • Interpretation   : Monostable (Fixed rigid perceptual interpretation)")
            
        print("\n  [4. STAGE 4: EXPLAINABLE ATTRIBUTION & TRIGGER LOCALIZATION]")
        print(f"      • Causal Trigger Box [ymin, xmin, ymax, xmax]: {loc['trigger_bounding_box_normalized']}")
        print(f"      • Peak Heatmap Activation Intensity          : {loc['heatmap_max_intensity']:.2f}")
        print(f"      • Output Visual Card                         : outputs/diagnostic_{filename}")
        
        print("\n  [5. STAGE 5: SCIENTIFIC PERCEPTUAL REASONING]")
        print(f"      • Physical Reality        : {expl['physical_reality']}")
        print(f"      • Perceived Distortion    : {expl['perceptual_distortion']}")
        print(f"      • Neurobiological Cause   : {expl['scientific_mechanism']}")
        
        print("\n  [6. COMPUTED MULTI-DOMAIN FEATURES]")
        print(f"      • Michelson Contrast      : {raw['michelson_contrast']:.4f}")
        print(f"      • 2D Fourier Periodicity  : {raw['fourier_periodicity_ratio']:.4f}")
        print(f"      • Localized ELA Tamper    : {raw['ela_forgery_score']:.4f}")
        print(f"      • Figure-Ground Balance   : {raw['figure_ground_balance']:.4f}")
        print(f"      • Bilateral Symmetry      : {raw['bilateral_symmetry']:.4f}")

    print("\n" + "=" * 90)
    print("                     ALL 8 ILLUSION CASE ANALYSES COMPLETED")
    print("=" * 90)

if __name__ == "__main__":
    run_deep_analysis()
