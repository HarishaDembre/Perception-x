# SYSTEM WORKFLOW & ARCHITECTURE FOR PERCEPTION-X

Perception-X is designed as a modular, 7-stage hierarchical perception and explainability pipeline. This architecture bridges the research gaps identified across the five reviewed papers by combining multi-category classification, receptive field explainability, bio-inspired ambiguity resolution, and forensic forgery discrimination.

---

## 1. High-Level Architectural Flowchart

```
                            ┌───────────────────────────────┐
                            │          Input Image          │
                            │      (Custom / Benchmark)     │
                            └───────────────┬───────────────┘
                                            │
                                            ▼
                    ┌───────────────────────────────────────────────┐
                    │  Stage 1: Multi-Domain Feature Extraction     │
                    │  - Cross-Sectional Luminance Profile          │
                    │  - 2D Fast Fourier Magnitude Spectrum         │
                    │  - Localized 8x8 ELA Compression Variance     │
                    │  - Bilateral Figure-Ground Symmetry Balance   │
                    └───────────────────────┬───────────────────────┘
                                            │
                                            ▼
                    ┌───────────────────────────────────────────────┐
                    │  Stage 2: Primary Problem Gating Decision     │
                    │  - Is Object / Non-Illusion Physical Image?   │
                    │  - Is Optical Illusion / Ambiguous Pattern?   │
                    │  - Is Digitally Manipulated / Spliced Image?  │
                    └───────┬───────────────┬───────────────┬───────┘
                            │               │               │
            ┌───────────────┘               │               └───────────────┐
            ▼                               ▼                               ▼
┌───────────────────────┐       ┌───────────────────────┐       ┌───────────────────────┐
│ Normal / Unambiguous  │       │ Optical Illusion /    │       │ Digital Splicing /    │
│ Physical Object       │       │ Ambiguous Stimulus    │       │ Image Tampering       │
└───────────────────────┘       └───────────┬───────────┘       └───────────────────────┘
                                            │
                                            ▼
                    ┌───────────────────────────────────────────────┐
                    │  Stage 3: Fine-Grained Multi-Category Class.  │
                    │  - Geometric & Distortion Illusions           │
                    │  - Brightness & Contrast Illusions            │
                    │  - Ambiguous & Multistable Figures            │
                    │  - Impossible Objects (Penrose, Escher)       │
                    │  - Motion & Peripheral Drift                  │
                    └───────────────┬───────────────────────────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    ▼                               ▼
    ┌───────────────────────────────┐ ┌───────────────────────────────┐
    │  Stage 4: Ambiguity Engine    │ │  Stage 5: Explainability &    │
    │  - Quantum Double-Well Tunnel │ │           Localization        │
    │  - Dual-State Probabilities   │ │ - Gradient Receptive Field Map│
    │  - Perceptual Entropy H       │ │ - JET Colormap Saliency Blend │
    │  (Maksymov 2024 Concept)      │ │ - Soft-Localization Bounding  │
    └───────────────┬───────────────┘ └───────────────┬───────────────┘
                    │                                 │
                    └───────────────┬─────────────────┘
                                    │
                                    ▼
                    ┌───────────────────────────────────────────────┐
                    │  Stage 6: Scientific Perceptual Reasoning     │
                    │  - Physical Reality vs Perceived Distortion   │
                    │  - Neurobiological Mechanisms (V1-V4 / LGN)   │
                    │  - Confidence Scoring & Multi-Modal Output    │
                    └───────────────────────────────────────────────┘
```

---

## 2. Stage-by-Stage Technical Specification

### Stage 1: Multi-Domain Feature Extraction
Extracts complementary mathematical representations:
1. **Luminance Cross-Section:** Computes horizontal and vertical 1D intensity profiles $I(x, y_0)$ to detect sudden contrast induction steps.
2. **2D Fast Fourier Transform (FFT):**
   $$F(u, v) = \sum_{x=0}^{M-1} \sum_{y=0}^{N-1} f(x, y) e^{-j 2\pi (\frac{ux}{M} + \frac{vy}{N})}$$
   Measures harmonic peak periodicity indicative of repetitive checkerboards or grid channels.
3. **Localized Error Level Analysis (ELA):**
   Subdivides the recompression error map into an $8 \times 8$ grid of blocks. Measures the ratio between the maximum block mean error and the median block error. A high local discrepancy ratio indicates an authentic photo spliced with alien pixels.
4. **Figure-Ground Symmetry & Balance:**
   Computes the bilateral horizontal symmetry and black-to-white pixel area balance ($1.0 - |P_{\text{white}} - P_{\text{black}}|$), a hallmark of bistable reversible figures.

---

### Stage 2: Primary Problem Gating
Categorizes the input image into one of three macro domains:
* `Normal / Unambiguous Physical Object`: Characterized by smooth Lambertian shading gradients, low Fourier periodicity, and low ELA discrepancy.
* `Optical Illusion / Ambiguous Pattern`: Characterized by high periodic harmonic energy, high Michelson contrast, or near-perfect figure-ground balance.
* `Digitally Manipulated / Forgery`: Characterized by high localized ELA block discrepancy ($>2.5\times$ background).

---

### Stage 3: Fine-Grained Multi-Category Classification
For images gated as illusions, categorizes into five core psychophysical families:
1. **Geometric & Distortion Illusions:** Müller-Lyer, Café Wall, Poggendorff, Hering illusions.
2. **Brightness & Contrast Illusions:** Hermann Grid, Simultaneous Contrast, White's illusion, Mach Bands.
3. **Ambiguous & Multistable Figures:** Rubin's Vase, Necker Cube, Duck-Rabbit.
4. **Impossible Objects:** Penrose Triangle, Escher Staircase, Devil's Tuning Fork.
5. **Motion Illusions:** Rotating Snakes, peripheral drift patterns.

---

### Stage 4: Quantum-Inspired Ambiguity & Multistability Engine
Standard networks force a winner-take-all classification, assigning $P \approx 1.0$ to one state. For ambiguous figures, Perception-X evaluates a double-well potential:
$$V(x) = (x^2 - 1)^2 + \delta \cdot x$$
where $x = -1$ corresponds to $\text{State}_A$ and $x = +1$ corresponds to $\text{State}_B$.
* Calculates **Perceptual Entropy**:
  $$H = - \sum_{i \in \{A, B\}} p_i \log_2(p_i)$$
* Maximum entropy ($H \approx 1.0$) triggers a non-rigid dual-state report (e.g., 47.5% Front-Facing vs. 52.5% Rear-Facing Cube) rather than an artificial single class.

---

### Stage 5: Explainability & Causal Localization Engine
* Computes spatial gradients $\nabla I = (\frac{\partial I}{\partial x}, \frac{\partial I}{\partial y})$ and Laplacian curvature.
* Produces a continuous activation map normalized to $[0.0, 1.0]$.
* Alpha-blends the activation map with the original RGB image using a JET colormap.
* Extracts the causal trigger bounding box $[ymin, xmin, ymax, xmax]$ matching the IllusionVQA evaluation protocol.

---

### Stage 6: Scientific Perceptual Reasoning Engine
Synthesizes a structured plain-language report:
* **Physical Reality:** Objective ground truth (e.g., *"Physical pixel luminance at intersections is mathematically identical to channels"*).
* **Perceptual Distortion:** Subjective human experience (e.g., *"Phantom gray blobs perceived at peripheral crossings"*).
* **Neurobiological Mechanism:** Exact scientific explanation (e.g., *"Lateral inhibition among On-Center / Off-Surround retinal ganglion cells"*).
