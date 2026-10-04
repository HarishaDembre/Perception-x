# 1. LITERATURE REVIEW

## 1.1 Identification of Need
Human visual perception can be misled by certain visual patterns, resulting in optical illusions and ambiguous figures that are interpreted differently from their true physical content. While this phenomenon is well studied in psychology and vision science, there is no widely available automated system that can reliably detect whether an image contains an illusion, classify its type, explain why the illusion occurs, and distinguish a naturally occurring illusion from a digitally manipulated or deceptive image. 

Existing image-classification systems are trained on natural, unambiguous imagery and are not designed to recognize illusion-specific visual cues such as contrast induction, repeated geometric patterns, perspective tricks, or multistable figure-ground relationships. This creates a clear need for a dedicated AI-based system — such as **Perception-X** — that can detect, classify, localize, and explain ambiguous and illusory images with a measurable confidence score, drawing on recent advances in convolutional networks, explainable AI, vision-language models, and forgery detection.

---

## 1.2 Mind Map of the Literature Review
The mind map organizes the five reviewed papers around the core theme of the project, grouping them by their primary contribution area and the underlying algorithm family used in each study:

```
                                  ┌──────────────────────────────────────────────┐
                                  │                 PERCEPTION-X                 │
                                  │      AI-Based Ambiguous Image Detection      │
                                  │               & Classification               │
                                  └──────────────────────┬───────────────────────┘
                                                         │
         ┌───────────────────────┬───────────────────────┼───────────────────────┬───────────────────────┐
         │                       │                       │                       │                       │
┌────────▼────────┐     ┌────────▼────────┐     ┌────────▼────────┐     ┌────────▼────────┐     ┌────────▼────────┐
│  Comprehension  │     │   Multi-Modal   │     │Brightness Model │     │  Bio-Inspired / │     │     Digital     │
│ & Localization  │     │Illusion Recog.  │     │ & Localization  │     │ Quantum Tunnell.│     │  Manipulation   │
│   (VQA / VLM)   │     │   (CNN + GNN)   │     │ (U-Net / Auto)  │     │  (Bistability)  │     │   (CNN + LSTM)  │
├─────────────────┤     ├─────────────────┤     ├─────────────────┤     ├─────────────────┤     ├─────────────────┤
│ [P1] Shahgir    │     │ [P2] Leong      │     │ [P3] Mukherjee  │     │ [P4] Maksymov   │     │ [P5] DeepForgery│
│ et al., 2024    │     │ 2024            │     │ et al., 2024    │     │ 2024            │     │ Net Authors 2026│
│ COLM 2024       │     │ IEEE WTA 2024   │     │ Springer Appl.  │     │ AIP APL ML      │     │ Frontiers in AI │
├─────────────────┤     ├─────────────────┤     ├─────────────────┤     ├─────────────────┤     ├─────────────────┤
│ ViT / VLMs      │     │ CNN Extractor + │     │ CNN, Autoenc.,  │     │ Quantum-Tunnel  │     │ Hybrid CNN +    │
│ GPT-4V CoT      │     │ Graph Neural Net│     │ U-Net, U-Net++  │     │ Activation DNN  │     │ LSTM + Transfer │
└─────────────────┘     └─────────────────┘     └─────────────────┘     └─────────────────┘     └─────────────────┘
```

---

## 1.3 Detailed Review of Selected Research Papers

### [1]. IllusionVQA: A Challenging Optical Illusion Dataset for Vision Language Models
* **Authors:** H.S. Shahgir, K.S. Sayeed, A. Bhattacharjee, W.U. Ahmad, Y. Dong, R. Shahriyar (2024)
* **Venue:** COLM 2024 (Conference on Language Modeling) | arXiv:2403.15952
* **Summary:** This paper introduces *IllusionVQA*, a diverse dataset of challenging optical illusions and hard-to-interpret images used to test Vision-Language Models (VLMs) on two multiple-choice tasks:
  1. *Comprehension:* Identifying what the illusion depicts.
  2. *Soft Localization:* Pointing to the region causing the illusory effect with normalized bounding boxes.
  The best performing model, GPT-4V, achieved only about 63% accuracy on comprehension and under 50% on localization, far below human performance (~87–92%), revealing that current VLMs do not "see" illusions the way humans do.
* **Algorithm / Technique:** Vision Transformers (ViT) / Multimodal LLMs (GPT-4V class), prompted with few-shot and Chain-of-Thought (CoT) reasoning.
* **Advantages:**
  - Provides a large, diverse benchmark spanning many illusion categories rather than a narrow single type.
  - Evaluates both classification (comprehension) and spatial localization in one framework.
  - Enables direct, quantitative comparison between human and AI perceptual performance.
* **Disadvantages:**
  - VLMs show poor and inconsistent localization accuracy, especially with ambiguous or ill-defined illusion boundaries.
  - No pixel-level heatmap or Grad-CAM-style explainability is produced — only multiple-choice answers and coarse bounding boxes.
  - Dependent on very large, closed pretrained models, making it computationally expensive to reproduce or fine-tune.

### [2]. A Multi-Modal Deep Learning Approach for Enhanced Optical Illusion Recognition
* **Authors:** W.Y. Leong (2024)
* **Venue:** 2024 IEEE 8th Symposium on Wireless Technology & Applications (IEEE Xplore: 10.1109/ISWTA61853.2024.10698939)
* **Summary:** This paper proposes a multi-modal deep learning model that fuses visual features with contextual information and cognitive-science-driven priors to improve recognition and classification of optical illusions such as geometric, color, and motion illusions. A CNN extracts low-level visual features while a Graph Neural Network (GNN) integrates contextual relationships between image regions, producing a joint representation used for final classification.
* **Algorithm / Technique:** CNN-based visual feature extractor + Graph Neural Network for contextual fusion (multi-modal architecture).
* **Advantages:**
  - Fusing visual and contextual cues improves classification accuracy over CNN-only baselines.
  - Covers multiple illusion categories (geometric, color, motion) in a single model.
  - Published in an IEEE venue with a reproducible architecture.
* **Disadvantages:**
  - Multi-modal fusion increases computational and memory overhead, limiting real-time / web deployment.
  - No explainability module — the model does not indicate which pixels drive its decision.
  - Evaluated on a relatively small, non-public illusion dataset, limiting generalizability.

### [3]. Deep Learning Models for Perception of Brightness Related Illusions
* **Authors:** A. Mukherjee, A. Paul, K. Ghosh (2024)
* **Venue:** Applied Intelligence, Springer, Vol. 54(21), pp. 10259–10283 (DOI: 10.1007/s10489-024-05658-w)
* **Summary:** This paper studies how deep networks trained for low-level vision tasks (denoising, deblurring) replicate human brightness-contrast illusions such as the Hermann grid and grating induction. CNN, Autoencoder, U-Net, and U-Net++ architectures are systematically compared to see which best reproduces human-like illusory perception, including antagonistic illusions that classical filtering models cannot explain.
* **Algorithm / Technique:** CNN, Autoencoder, U-Net, and U-Net++ (encoder-decoder segmentation-style networks).
* **Advantages:**
  - U-Net-family architectures naturally support pixel-level output, making them well suited to region-highlighting/explainability tasks.
  - Strong grounding in psychophysical validation against real human perceptual data.
  - Published in a reputable Springer journal in 2024.
* **Disadvantages:**
  - Restricted to a single illusion category (brightness/contrast); no geometric, motion, or depth illusions considered.
  - No end-user interface, confidence scoring, or illusion-type classification layer.
  - Focused purely on replication of perception rather than automated detection/classification for practical use.

### [4]. Quantum-Tunnelling Deep Neural Network for Optical Illusion Recognition
* **Authors:** I.S. Maksymov (2024)
* **Venue:** APL Machine Learning, AIP Publishing (DOI: 10.1063/5.0225771)
* **Summary:** This paper introduces QT-DNN, a deep neural network whose activation function is inspired by the quantum-tunnelling effect from physics. The model is tasked with simulating human perception of classic multistable figures — the Necker cube and Rubin's vase — and is shown to reproduce the oscillating, sometimes-ambiguous switching between interpretations that humans experience, unlike conventional DNNs which tend to lock onto a single rigid interpretation.
* **Algorithm / Technique:** Quantum-Tunnelling-based activation function within a Deep Neural Network (QT-DNN).
* **Advantages:**
  - Produces human-like ambiguous/oscillating outputs for multistable figures rather than one fixed label.
  - Offers a biologically and cognitively grounded alternative to standard activation functions.
  - Published in a peer-reviewed AIP journal in 2024, with a clear mathematical formulation.
* **Disadvantages:**
  - Proof-of-concept scale — tested only on a few classic stimuli (Necker cube, Rubin's vase), not a large labeled dataset.
  - No reported classification accuracy or benchmark comparison against modern CNN/Transformer baselines.
  - Not yet integrated into a deployable detection-and-classification pipeline.

### [5]. DeepForgeryNet: A Hybrid CNN–LSTM and Transfer Learning Framework for Robust Image Forgery and Deepfake Detection
* **Authors:** DeepForgeryNet Authors (2026)
* **Venue:** Frontiers in Artificial Intelligence (DOI: 10.3389/frai.2026.1810912)
* **Summary:** This paper presents DeepForgeryNet, an artifact-aware deep learning architecture for detecting digitally manipulated and deepfake images. It combines transfer-learning-based CNN feature extraction with an LSTM to model contextual dependencies between manipulation artifacts, using structured data augmentation to improve generalization across manipulation types and datasets.
* **Algorithm / Technique:** Hybrid CNN (transfer learning) + LSTM (Long Short-Term Memory) network.
* **Advantages:**
  - Jointly captures low-level artifact traces and high-level contextual inconsistencies, improving robustness across manipulation types.
  - Uses transfer learning, reducing the amount of training data required.
  - Recent (2026) and directly relevant to distinguishing digitally manipulated images from naturally occurring ones.
* **Disadvantages:**
  - CNN + LSTM combination is computationally heavier than single-branch CNN detectors, affecting real-time use.
  - Designed for malicious manipulation/deepfakes, not for naturally occurring optical illusions or ambiguous figures.
  - No mechanism to distinguish an intentionally deceptive manipulation from a naturally ambiguous/illusory image.

---

## 1.4 Existing System
Existing work in this space is fragmented across three separate research threads that Perception-X aims to unify:
1. **Illusion-Focused Benchmarks:** Such as IllusionVQA test large Vision-Language Models on comprehension and localization, but do not provide a lightweight, deployable classifier or an explanation-generation layer.
2. **Illusion-Replication Studies:** The brightness-illusion work using CNN/Autoencoder/U-Net/U-Net++, and the multi-modal CNN+GNN recognition model focus on a narrow illusion category or lack pixel-level explainability and confidence scoring suitable for an end-user web application.
3. **Bio-Inspired Ambiguity Models:** The quantum-tunnelling DNN offers a promising bio-inspired mechanism for representing ambiguous, multistable perception but remains a proof-of-concept, untested at dataset scale.
4. **Image-Forgery & Deepfake Detection:** (e.g., DeepForgeryNet) has matured for detecting malicious manipulation but is not designed to recognize naturally occurring optical illusions, and no existing system combines illusion detection with manipulation detection in a single, explainable, confidence-scored pipeline.

---

## 1.5 Proposed System: Perception-X
Perception-X proposes a unified AI-based pipeline that:
1. Detects whether an input image contains an ambiguous or illusory pattern, or is an unambiguous natural physical object, or is a digital forgery.
2. Classifies the specific illusion category (geometric, color and brightness, size, perspective and depth, motion, ambiguous figures, impossible objects, or normal image).
3. Highlights the responsible image region using explainable-AI techniques such as Grad-CAM and receptive field saliency overlays.
4. Generates a human-readable explanation of the perceptual effect and underlying neurobiology.
5. Reports a confidence score for every prediction.
6. Optionally flags images that are digitally manipulated rather than naturally illusory.

---

## 1.6 Objectives of the Project (Mapped to Reviewed Papers)
* **Objective 1 (Detect and Classify):** Detect and classify the type of ambiguous/optical illusion image with high accuracy using a fused visual-contextual deep learning model.
  * *Mapped Reference Paper:* [2] Leong, W.Y. (2024) — IEEE ISWTA 2024.
* **Objective 2 (Localize and Explain):** Localize and visually explain the region responsible for the illusion, and generate a plain-language explanation with a confidence score.
  * *Mapped Reference Paper:* [3] Mukherjee, A.; Paul, A.; Ghosh, K. (2024) — Springer Applied Intelligence.
* **Objective 3 (Benchmark, Comprehend, and Handle Ambiguity):** Benchmark and validate system comprehension of ambiguous images against human-level performance, and handle genuinely multistable figures gracefully rather than forcing a single rigid label.
  * *Mapped Reference Papers:* [1] Shahgir et al. (2024) — COLM 2024 & [4] Maksymov, I.S. (2024) — AIP Publishing.

---

## 1.7 Literature Review Summary Table (Table 1.1)

| Sl. | Year | Authors | Paper Title | Venue | Research Focus | Methodology | Key Contribution | Dataset | Limitations | Research Gap Found | DOI / Paper Link |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **1** | 2024 | Shahgir et al. | IllusionVQA | COLM 2024 | Benchmarking comprehension & spatial localization | Curated multi-choice VQA dataset; evaluated VLMs (GPT-4V) with few-shot CoT | Introduced diverse illusion benchmark; showed VLMs lag human accuracy | IllusionVQA (curated illusion images) | No pixel-level explainability; models mislocalize regions; VQA-only | No end-to-end pipeline that both classifies illusion type and highlights causal region | arXiv:2403.15952 |
| **2** | 2024 | Leong, W.Y. | Multi-Modal Deep Learning Illusion Recognition | IEEE ISWTA 2024 | Improving recognition by fusing visual & contextual cues | CNN feature extractor fused with GNN for contextual integration | Demonstrated visual + graph fusion improves classification | Mixed illusion corpus (geometric, color, motion) | Higher computational cost; no explainability heatmap; small set | Lacks a lightweight, explainable variant suitable for real-time web deployment | IEEE Xplore: 10.1109/ISWTA (Doc ID 10698939) |
| **3** | 2024 | Mukherjee, Paul, Ghosh | Deep Learning Models for Brightness Illusions | Springer Applied Intelligence | Replicating & explaining brightness-contrast illusions | CNN, Autoencoder, U-Net, U-Net++ trained on restoration | Showed U-Net closely matches human psychophysical data | Brightness-contrast set (Hermann, White, grating) | Restricted to brightness category only; no taxonomy; no UI | No unified model covering brightness alongside geometric, motion & depth | DOI: 10.1007/s10489-024-05658-w |
| **4** | 2024 | Maksymov, I.S. | Quantum-Tunnelling DNN for Illusion Recognition | AIP APL Machine Learning | Modeling ambiguous perception (Necker, Rubin) | QT-DNN: Quantum-tunnelling activation function | Produced human-like oscillating/ambiguous outputs | Synthetic ambiguous stimuli (Necker, Rubin) | Conceptual proof-of-concept; not tested on large real datasets | No large-scale, production-ready classifier built on bio-inspired activation | DOI: 10.1063/5.0225771 |
| **5** | 2026 | DeepForgeryNet Authors | DeepForgeryNet: Hybrid CNN-LSTM Framework | Frontiers in AI | Detecting manipulated & deepfake images | Hybrid CNN (transfer learning) + LSTM with structured data augmentation | Achieved robust cross-dataset forgery detection via joint modeling | Public forgery/deepfake benchmarks (CASIA, etc.) | High model complexity; not designed for optical illusions | No integration between illusion detection and manipulation detection pipelines | https://doi.org/10.3389/frai.2026.1810912 |

---

## 1.8 Research Gaps Identified
1. **Absence of Unified Deployable Pipeline:** No existing system performs illusion detection, multi-class illusion classification, region-level explainability, and confidence scoring together in a single, deployable pipeline (Papers 1, 2, 3).
2. **Category Isolation:** Illusion-replication research remains category-specific (e.g., brightness-only in Paper 3), with no unified model spanning geometric, motion, depth, and ambiguous-figure categories.
3. **Unscaled Bio-Inspired Models:** Bio-inspired handling of genuine perceptual ambiguity (Paper 4) has not been validated at dataset scale or integrated into a production classification system.
4. **Disconnection from Forgery Forensics:** Manipulation/deepfake detection research (Paper 5) is disconnected from illusion-detection research, leaving no system able to distinguish a naturally occurring illusion from a deliberately deceptive, digitally altered image.
5. **Human-AI Performance Gap in Localization:** Vision-Language Model benchmarks (Paper 1) reveal a large human-AI performance gap in illusion localization that current lightweight, deployable models have not closed.
