# PERCEPTION-X API REFERENCE

## 1. models.perception_x_pipeline.PerceptionXPipeline

The unified top-level controller for image comprehension, gating, classification, multistability analysis, and explainability.

### Methods
* process_image(image_input: str | PIL.Image) -> dict
  * **Parameters:** image_input - Filepath string or PIL Image object.
  * **Returns:** Dictionary containing:
    * stage_1_problem_gating: Decision (Normal Object, Optical Illusion, or Digital Forgery), booleans (is_object, is_illusion, is_forgery), confidence score.
    * stage_2_multi_category_classification: Fine-grained category label and confidence score.
    * stage_3_ambiguity_analysis: Multistable status, perceptual entropy, switching probability, dual-state distribution.
    * stage_4_localization: Normalized bounding box [ymin, xmin, ymax, xmax], maximum heatmap intensity.
    * stage_5_explanation: Physical reality, perceptual distortion, and scientific neurobiological mechanism.
    * 
aw_measurements: Contrast, Fourier periodicity ratio, ELA score, symmetry balance.
    * _artifacts: Visual heatmap array, overlay PIL Image, and ELA PIL Image.

---

## 2. core.feature_extractor.IllusionFeatureExtractor

Extracts multi-domain physical, frequency, psychophysical, and forensic features.

### Methods
* extract_luminance_profile(img_pil: PIL.Image) -> dict: Cross-sectional 1D luminance profiles, Michelson contrast, RMS contrast.
* extract_fourier_spectrum(img_pil: PIL.Image) -> dict: 2D Fast Fourier Transform magnitude spectrum, peak periodicity ratio.
* compute_error_level_analysis(img_pil: PIL.Image, quality: int = 90) -> dict: Localized 8x8 block-variance ELA to detect image tampering.
* compute_ambiguity_metrics(img_pil: PIL.Image) -> dict: Figure-ground area balance, bilateral symmetry, ambiguity potential.
* extract_all(img_pil: PIL.Image) -> dict: Aggregates all extracted feature sets.

---

## 3. core.ambiguity_engine.QuantumTunnellingAmbiguityEngine

Simulates quantum-tunnelling double-well potential dynamics for bistable figures.

### Methods
* evaluate_bistable_states(ambiguity_potential: float, category_name: str) -> dict:
  * Evaluates double-well potential (x) = (x^2 - 1)^2 + \delta x$.
  * Computes Perceptual Entropy  = -\sum p_i \log_2(p_i)$.
  * Returns dual-state probabilities.

---

## 4. core.explainability.IllusionExplainabilityEngine

Generates pixel-level causal saliency heatmaps and soft-localization bounding boxes.

### Methods
* generate_causal_heatmap(img_pil: PIL.Image, category: str, features: dict) -> tuple[np.ndarray, list[int]]:
  * Computes receptive field gradients and returns normalized 2D activation heatmap and bounding box.
* create_overlay_image(img_pil: PIL.Image, heatmap: np.ndarray, alpha: float = 0.45) -> PIL.Image:
  * Blends a JET colormap heatmap with the input image.

---

## 5. core.reasoning_engine.PerceptualReasoningEngine

Provides neurobiologically grounded plain-language explanations.

### Methods
* generate_explanation(category_name: str, confidence: float, bistability_info: dict = None) -> dict:
  * Returns structured scientific explanation covering physical ground truth vs. perceptual experience.
