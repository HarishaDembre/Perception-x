# HANDS-ON GUIDE & EXPERIMENTATION PLAYGROUND

This guide walks you through generating optical illusions, testing the multi-stage pipeline, and running custom experiments.

---

## 1. Quick Start Execution

To run the complete hands-on evaluation on all 8 benchmark stimuli:
```bash
python hands_on_demo.py
```

This script will:
1. Load or synthesize the 8 test stimuli:
   - `cafe_wall.png` (Geometric illusion)
   - `hermann_grid.png` (Brightness illusion)
   - `muller_lyer.png` (Geometric arrowhead distortion)
   - `necker_cube.png` (Ambiguous 3D wireframe)
   - `rubin_vase.png` (Ambiguous figure-ground silhouette)
   - `simultaneous_contrast.png` (Brightness center-surround induction)
   - `natural_object.png` (Normal 3D shaded sphere - non-illusion control)
   - `manipulated_splicing.png` (Digital tampering / forensic forgery)
2. Pass each stimulus through the 5-stage Perception-X pipeline.
3. Generate 4-panel visual diagnostic cards saved into `outputs/`.
4. Output terminal diagnostics for every processing step.

---

## 2. Testing Custom Images

You can test any image (from your local drive or web) with the Python API:

```python
from models.perception_x_pipeline import PerceptionXPipeline
from PIL import Image

# Initialize pipeline
pipeline = PerceptionXPipeline()

# Process an image file
result = pipeline.process_image("path/to/your/image.png")

# Inspect Stage 1 Gating Decision
gating = result["stage_1_problem_gating"]
print(f"Decision: {gating['decision']}")
print(f"Is Object?   {gating['is_object']}")
print(f"Is Illusion? {gating['is_illusion']}")
print(f"Is Forgery?  {gating['is_forgery']}")

# Inspect Stage 2 Classification & Ambiguity
category = result["stage_2_multi_category_classification"]
print(f"Category: {category['category']} (Confidence: {category['confidence']:.2%})")

# Multistability & Dual States
ambiguity = result["stage_3_ambiguity_analysis"]
if ambiguity["is_multistable"]:
    print(f"Perceptual Entropy: {ambiguity['perceptual_entropy']}")
    print(f"Dual States: {ambiguity['state_distribution']}")

# Causal Bounding Box
print(f"Trigger Bounding Box: {result['stage_4_localization']['trigger_bounding_box_normalized']}")

# Scientific Explanation
expl = result["stage_5_explanation"]
print(f"Physical Reality: {expl['physical_reality']}")
print(f"Mechanism:        {expl['scientific_mechanism']}")

# Save Visual Overlay
result["_artifacts"]["overlay_pil"].save("outputs/custom_result_overlay.png")
```

---

## 3. Interpreting the 4-Panel Diagnostic Cards

Each diagnostic card generated in `outputs/` contains four subplots:
1. **Panel 1 (Input Image):** The raw stimulus tested.
2. **Panel 2 (2D Fourier Spectrum):** Shows spatial frequency distribution. High harmonic peaks indicate regular periodic tiling (e.g., Hermann Grid and Café Wall).
3. **Panel 3 (Error Level Analysis - ELA):** Displays compression difference maps. Uniform low ELA indicates authentic rendering; localized bright clusters indicate image tampering / splicing.
4. **Panel 4 (Causal Trigger Overlay):** Displays a JET colormap heatmap showing where receptive field conflict occurs, bordered by a green dashed bounding box pinpointing the causal trigger.

---

## 4. Synthesizing New Parametric Stimuli

You can generate custom variations of illusions using `data/synthetic_generators.py`:

```python
from data.synthetic_generators import (
    generate_hermann_grid,
    generate_muller_lyer,
    generate_cafe_wall,
    generate_rubin_vase,
    generate_necker_cube
)

# Generate a dense 6x6 Hermann grid with 15px bars
grid = generate_hermann_grid(size=(512, 512), grid_n=6, bar_width=15)
grid.save("my_custom_hermann_grid.png")

# Generate Muller-Lyer with long fins
muller = generate_muller_lyer(size=(500, 500), line_length=250, fin_length=50)
muller.save("my_custom_muller_lyer.png")
```
