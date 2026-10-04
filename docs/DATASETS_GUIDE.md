# DATASETS GUIDE & IMPORT MANUAL FOR PERCEPTION-X

This guide documents the datasets used across the five literature review papers, their data schemas, physical properties, and complete Python import scripts.

---

## 1. IllusionVQA (Shahgir et al., 2024 - COLM 2024)

### Overview
IllusionVQA is the first large-scale benchmark designed specifically to test Vision-Language Models (VLMs) on optical illusions. It spans multiple optical illusion categories, requiring models to answer both perceptual comprehension questions and provide soft spatial localization of the illusion's trigger region.

* **Repository:** [ahmadki/IllusionVQA (Hugging Face)](https://huggingface.co/datasets/ahmadki/IllusionVQA)
* **Total Instances:** 686 curated multiple-choice items
* **Illusion Taxonomies:**
  1. Geometric Distortion (e.g., Müller-Lyer, Café Wall, Poggendorff)
  2. Brightness & Contrast (e.g., Hermann Grid, White's Illusion)
  3. Ambiguous Figures (e.g., Rubin's Vase, Duck-Rabbit)
  4. Impossible Objects (e.g., Penrose Triangle, Impossible Staircase)
  5. Camouflage & Hidden Figures
  6. Perspective & Size Constancy (e.g., Ponzo Illusion)

### Data Schema
| Field Name | Type | Description |
|---|---|---|
| `image_id` | `str` | Unique sample identifier hash |
| `image` | `PIL.Image` | High-resolution optical illusion RGB image |
| `question` | `str` | Perceptual question prompt |
| `options` | `list[str]` | 4 candidate options (`[A, B, C, D]`) |
| `answer` | `int` | Zero-indexed ground truth human perceptual choice |
| `category` | `str` | High-level illusion classification category |
| `soft_localization_bbox` | `list[float]` | Normalized bounding box `[ymin, xmin, ymax, xmax]` |
| `human_accuracy` | `float` | Human baseline performance (~87–92%) |
| `vlm_accuracy` | `dict` | Baseline scores (GPT-4V: 63.2%, Gemini: 58.4%, LLaVA: 46.1%) |

### Python Import Snippet
```python
from datasets import load_dataset
from PIL import Image

# Option 1: Load directly from Hugging Face Datasets
dataset = load_dataset("ahmadki/IllusionVQA")
sample = dataset["test"][0]

image = sample["image"]
question = sample["question"]
options = sample["options"]
bbox = sample["soft_localization_bbox"]

print(f"Question: {question}")
print(f"Options: {options}")
print(f"Causal Bounding Box: {bbox}")
```

---

## 2. Multi-Modal Illusion Corpus (Leong, 2024 - IEEE ISWTA)

### Overview
Constructed for evaluating multi-modal CNN-GNN architectures by representing images both as convolutional feature maps and region adjacency graphs.

* **Size:** ~1,200 curated illusion stimuli and normal control images
* **Categories:** Geometric, Color/Brightness, Motion

### Graph Data Representation
* **Nodes ($V$):** Patches extracted from a grid or superpixel segmentation ($D=512$ feature vectors from ResNet backbone).
* **Edges ($E$):** Spatial proximity and geometric alignment between adjacent patches.
* **Adjacency Matrix ($A$):** Weighted matrix encoding visual contrast and edge orientation discrepancies across patch borders.

### Python Import Snippet
```python
import torch
from torchvision import datasets, transforms

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# Load structured directory
# dataset = datasets.ImageFolder(root="path/to/multimodal_corpus", transform=transform)
# loader = torch.utils.data.DataLoader(dataset, batch_size=32, shuffle=True)
```

---

## 3. Brightness-Contrast Psychophysical Dataset (Mukherjee et al., 2024)

### Overview
A standardized battery of classical brightness illusions designed to measure receptive field lateral inhibition.

* **Publisher:** Springer *Applied Intelligence*
* **Stimuli Included:**
  - Hermann Grid (grid intersections vs. straight channels)
  - Simultaneous Brightness Contrast (identical center gray targets on black vs. white surrounds)
  - White's Illusion (equal gray bars on black vs. white grating stripes)
  - Grating Induction
  - Mach Bands (luminance ramps inducing phantom edge spikes)
  - Todorovic Illusion

### Physical vs. Perceived Luminance Schema
* `physical_matrix`: Floating point array $[0.0, 1.0]$ representing true calibrated luminance.
* `psychophysical_response`: Vector of human perceptual brightness ratings recorded under psychophysical lab conditions.

### Python Import Snippet
```python
import numpy as np
from PIL import Image

def load_brightness_benchmark(image_path):
    img = Image.open(image_path).convert('L')
    physical_matrix = np.array(img, dtype=np.float32) / 255.0
    center_row = physical_matrix[physical_matrix.shape[0] // 2, :]
    
    # Calculate Michelson and RMS contrast
    c_michelson = (np.max(center_row) - np.min(center_row)) / (np.max(center_row) + np.min(center_row) + 1e-6)
    return physical_matrix, center_row, c_michelson
```

---

## 4. Synthetic Ambiguous Figures & Multistable Suite (Maksymov, 2024)

### Overview
Procedural wireframe and silhouette stimuli designed to model perceptual bistability where the human visual cortex spontaneously alternates between two distinct interpretations.

* **Key Stimuli:** Necker Cube, Rubin's Vase, Duck-Rabbit, Schröder Staircase.
* **Attributes:**
  - `state_A`: Semantic label for interpretation 1 (e.g., Facing Faces).
  - `state_B`: Semantic label for interpretation 2 (e.g., Central Vase).
  - `barrier_potential` ($V_0$): Tunneling energy barrier height.
  - `perceptual_entropy` ($H$): Shannon entropy measuring ambiguity.

### Python Import Snippet
```python
from data.synthetic_generators import generate_rubin_vase, generate_necker_cube

rubin_img = generate_rubin_vase(size=(400, 400))
necker_img = generate_necker_cube(size=(400, 400))
```

---

## 5. CASIA & CoMoFoD Forgery Datasets (DeepForgeryNet, 2026)

### Overview
Standard public benchmarks used to evaluate forensic tampering detection (splicing and copy-move) vs. natural authentic images.

* **CASIA v1.0:** 1,721 color images (authentic and spliced).
* **CASIA v2.0:** 12,614 images with realistic post-processing and boundary blurs.
* **CoMoFoD:** 5,000 images focused specifically on copy-move duplication.

### Error Level Analysis (ELA) Preprocessing Pipeline
```python
import io
import numpy as np
from PIL import Image, ImageChops

def compute_ela(image_path, quality=90):
    im = Image.open(image_path).convert('RGB')
    buf = io.BytesIO()
    im.save(buf, format='JPEG', quality=quality)
    buf.seek(0)
    recompressed = Image.open(buf)
    diff = ImageChops.difference(im, recompressed)
    return np.array(diff, dtype=np.float32)
```
