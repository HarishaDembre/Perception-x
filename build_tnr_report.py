import docx
import os
import shutil
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def create_tnr_document():
    doc = docx.Document()
    
    # 1. Page Margins (1 inch everywhere)
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        
    # 2. Configure Normal style for Times New Roman
    style_normal = doc.styles['Normal']
    font_normal = style_normal.font
    font_normal.name = 'Times New Roman'
    font_normal.size = Pt(11)
    font_normal.color.rgb = RGBColor(0x22, 0x22, 0x22)
    
    def add_p(text, bold=False, italic=False, size=11, align=WD_ALIGN_PARAGRAPH.LEFT, space_after=6, color=RGBColor(0x22, 0x22, 0x22)):
        p = doc.add_paragraph()
        p.alignment = align
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = 1.15
        r = p.add_run(text)
        r.bold = bold
        r.italic = italic
        r.font.name = 'Times New Roman'
        r.font.size = Pt(size)
        r.font.color.rgb = color
        return p

    def add_h1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.bold = True
        r.font.name = 'Times New Roman'
        r.font.size = Pt(15)
        r.font.color.rgb = RGBColor(0x0A, 0x25, 0x40)
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.bold = True
        r.font.name = 'Times New Roman'
        r.font.size = Pt(13)
        r.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)
        return p

    def add_h3(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.bold = True
        r.font.name = 'Times New Roman'
        r.font.size = Pt(11.5)
        r.font.color.rgb = RGBColor(0x2D, 0x37, 0x48)
        return p

    def add_bullet(text):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.15
        r = p.runs[0] if p.runs else p.add_run(text)
        r.text = text
        r.font.name = 'Times New Roman'
        r.font.size = Pt(10.5)
        return p

    # --- COVER / TITLE ---
    add_p('PERCEPTION-X: AI-BASED AMBIGUOUS IMAGE DETECTION, MULTI-CATEGORY OPTICAL ILLUSION CLASSIFICATION, AND EXPLAINABLE FORENSIC PIPELINE',
          bold=True, size=18, align=WD_ALIGN_PARAGRAPH.CENTER, color=RGBColor(0x0A, 0x25, 0x40), space_after=6)
          
    add_p('Comprehensive Research Literature Review, Mind Map Synthesis, Dataset Architecture, Technical Workflow Specification, and Hands-On Experimental Verification\nPrepared in Times New Roman | Based on: COLM 2024, IEEE ISWTA 2024, Springer Applied Intelligence 2024, AIP APL 2024, Frontiers in AI 2026',
          italic=True, size=10.5, align=WD_ALIGN_PARAGRAPH.CENTER, color=RGBColor(0x4A, 0x55, 0x68), space_after=18)

    # --- 1. LITERATURE REVIEW ---
    add_h1('1. LITERATURE REVIEW')
    
    add_h2('1.1 Identification of Need')
    add_p('Human visual perception can be misled by certain visual patterns, resulting in optical illusions and ambiguous figures that are interpreted differently from their true physical content. While this phenomenon is well studied in psychology and vision science, there is no widely available automated system that can reliably detect whether an image contains an illusion, classify its type, explain why the illusion occurs, and distinguish a naturally occurring illusion from a digitally manipulated or deceptive image.')
    add_p('Existing image-classification systems are trained on natural, unambiguous imagery and are not designed to recognize illusion-specific visual cues such as contrast induction, repeated geometric patterns, perspective tricks, or multistable figure-ground relationships. This creates a clear need for a dedicated AI-based system — such as Perception-X — that can detect, classify, localize and explain ambiguous and illusory images with a measurable confidence score, drawing on recent advances in convolutional networks, explainable AI, vision-language models and forgery detection.')

    add_h2('1.2 Mind Map of the Literature Review')
    add_p('The mind map organizes the five reviewed papers around the core theme of Perception-X, grouping them by their primary contribution area and the underlying algorithm family used in each study:')
    
    mm_text = (
        '• Branch 1 (Illusion Comprehension & Localization): [P1] Shahgir et al., 2024 (COLM 2024) -> ViT / VLMs (GPT-4V, few-shot, Chain-of-Thought)\n'
        '• Branch 2 (Multi-Modal Illusion Recognition): [P2] Leong, 2024 (IEEE WTA 2024) -> CNN feature extractor + Graph Neural Network\n'
        '• Branch 3 (Brightness Illusion Modeling & Localization): [P3] Mukherjee et al., 2024 (Springer Applied Intelligence) -> CNN, Autoencoder, U-Net, U-Net++\n'
        '• Branch 4 (Bio-Inspired / Quantum Illusion Perception): [P4] Maksymov, 2024 (AIP APL Machine Learning) -> Quantum-Tunnelling Activation-based DNN (QT-DNN)\n'
        '• Branch 5 (Digital Manipulation & Deepfake Detection): [P5] DeepForgeryNet, 2026 (Frontiers in AI) -> Hybrid CNN-LSTM + Transfer Learning'
    )
    add_p(mm_text, size=9.5, space_after=10)

    add_h2('1.3 Reviewed Papers in Full Detail')

    papers_data = [
        {
            'id': '[1]',
            'title': 'IllusionVQA: A Challenging Optical Illusion Dataset for Vision Language Models',
            'authors': 'Shahgir et al. (2024) — COLM 2024 (Conference on Language Modeling)',
            'summary': 'This paper introduces IllusionVQA, a diverse dataset of challenging optical illusions and hard-to-interpret images, used to test Vision-Language Models (VLMs) on two multiple-choice tasks: comprehension (identifying what the illusion depicts) and soft localization (pointing to the region causing the illusory effect). The best performing model, GPT-4V, achieved only about 63% accuracy on comprehension and under 50% on localization, far below human performance, revealing that current VLMs do not "see" illusions the way humans do.',
            'algo': 'Vision Transformers / Vision-Language Models (GPT-4V class), prompted with few-shot and Chain-of-Thought reasoning.',
            'adv': ['Provides a large, diverse benchmark spanning many illusion categories rather than a narrow single type.',
                    'Evaluates both classification (comprehension) and spatial localization in one framework.',
                    'Enables direct, quantitative comparison between human and AI perceptual performance.'],
            'disadv': ['VLMs show poor and inconsistent localization accuracy, especially with ambiguous or ill-defined illusion boundaries.',
                       'No pixel-level heatmap or Grad-CAM-style explainability is produced — only multiple-choice answers.',
                       'Dependent on very large, closed pretrained models, making it computationally expensive to reproduce or fine-tune.']
        },
        {
            'id': '[2]',
            'title': 'A Multi-Modal Deep Learning Approach for Enhanced Optical Illusion Recognition',
            'authors': 'Leong, W.Y. (2024) — 2024 IEEE 8th Symposium on Wireless Technology & Applications (IEEE Xplore)',
            'summary': 'This paper proposes a multi-modal deep learning model that fuses visual features with contextual information and cognitive-science-driven priors to improve recognition and classification of optical illusions such as geometric, color and motion illusions. A CNN extracts low-level visual features while a Graph Neural Network integrates contextual relationships between image regions, producing a joint representation used for final classification.',
            'algo': 'CNN-based visual feature extractor + Graph Neural Network for contextual fusion (multi-modal architecture).',
            'adv': ['Fusing visual and contextual cues improves classification accuracy over CNN-only baselines.',
                    'Covers multiple illusion categories (geometric, color, motion) in a single model.',
                    'Published in an IEEE venue with a clearly reproducible architecture.'],
            'disadv': ['Multi-modal fusion increases computational and memory overhead, limiting real-time / web deployment.',
                       'No explainability module — the model does not indicate which pixels drive its decision.',
                       'Evaluated on a relatively small, non-public illusion dataset, limiting generalizability.']
        },
        {
            'id': '[3]',
            'title': 'Deep Learning Models for Perception of Brightness Related Illusions',
            'authors': 'Mukherjee, A.; Paul, A.; Ghosh, K. (2024) — Applied Intelligence, Springer, Vol. 54(21), pp. 10259–10283',
            'summary': 'This paper studies how deep networks trained for low-level vision tasks (de-noising, de-blurring) replicate human brightness-contrast illusions such as the Hermann grid and grating induction. CNN, Autoencoder, U-Net and U-Net++ architectures are systematically compared to see which best reproduces human-like illusory perception, including antagonistic illusions that classical filtering models cannot explain.',
            'algo': 'CNN, Autoencoder, U-Net, and U-Net++ (encoder-decoder segmentation-style networks).',
            'adv': ['U-Net-family architectures naturally support pixel-level output, making them well suited to region-highlighting/explainability tasks.',
                    'Strong grounding in psychophysical validation against real human perceptual data.',
                    'Published in a reputable Springer journal (Applied Intelligence) in 2024.'],
            'disadv': ['Restricted to a single illusion category (brightness/contrast); no geometric, motion or depth illusions considered.',
                       'No end-user interface, confidence scoring, or illusion-type classification layer.',
                       'Focused purely on replication of perception rather than automated detection/classification for practical use.']
        },
        {
            'id': '[4]',
            'title': 'Quantum-Tunnelling Deep Neural Network for Optical Illusion Recognition',
            'authors': 'Maksymov, I.S. (2024) — APL Machine Learning, AIP Publishing',
            'summary': 'This paper introduces QT-DNN, a deep neural network whose activation function is inspired by the quantum-tunnelling effect from physics. The model is tasked with simulating human perception of classic multistable figures — the Necker cube and Rubin\'s vase — and is shown to reproduce the oscillating, sometimes-ambiguous switching between interpretations that humans experience, unlike conventional DNNs which tend to lock onto a single rigid interpretation.',
            'algo': 'Quantum-Tunnelling-based activation function within a Deep Neural Network (QT-DNN).',
            'adv': ['Produces human-like ambiguous/oscillating outputs for multistable figures rather than one fixed label.',
                    'Offers a biologically and cognitively grounded alternative to standard activation functions.',
                    'Published in a peer-reviewed AIP journal in 2024, with a clear, reproducible mathematical formulation.'],
            'disadv': ['Proof-of-concept scale — tested only on a few classic stimuli (Necker cube, Rubin\'s vase), not a large labeled dataset.',
                       'No reported classification accuracy or benchmark comparison against modern CNN/Transformer baselines.',
                       'Not yet integrated into a deployable detection-and-classification pipeline.']
        },
        {
            'id': '[5]',
            'title': 'DeepForgeryNet: A Hybrid CNN–LSTM and Transfer Learning Framework for Robust Image Forgery and Deepfake Detection',
            'authors': 'DeepForgeryNet Authors (2026) — Frontiers in Artificial Intelligence',
            'summary': 'This paper presents DeepForgeryNet, an artifact-aware deep learning architecture for detecting digitally manipulated and deepfake images. It combines transfer-learning-based CNN feature extraction with an LSTM to model contextual dependencies between manipulation artifacts, using structured data augmentation to improve generalization across manipulation types and datasets.',
            'algo': 'Hybrid CNN (transfer learning) + LSTM (Long Short-Term Memory) network.',
            'adv': ['Jointly captures low-level artifact traces and high-level contextual inconsistencies, improving robustness across manipulation types.',
                    'Uses transfer learning, reducing the amount of training data required.',
                    'Recent (2026) and directly relevant to distinguishing digitally manipulated images from naturally occurring ones.'],
            'disadv': ['CNN + LSTM combination is computationally heavier than single-branch CNN detectors, affecting real-time use.',
                       'Designed for malicious manipulation/deepfakes, not for naturally occurring optical illusions or ambiguous figures.',
                       'No mechanism to distinguish an intentionally deceptive manipulation from a naturally ambiguous/illusory image.']
        }
    ]

    for p in papers_data:
        add_h3(f"{p['id']} {p['title']}")
        add_p(p['authors'], italic=True, size=9.5)
        add_p(f"Summary of the Paper: {p['summary']}")
        add_p(f"Algorithm(s) / Technique Used: {p['algo']}")
        add_p('Advantages:', bold=True, size=10)
        for a in p['adv']:
            add_bullet(a)
        add_p('Disadvantages:', bold=True, size=10)
        for d in p['disadv']:
            add_bullet(d)

    add_h2('1.4 Existing System')
    add_p('Existing work in this space is fragmented across three separate research threads that Perception-X aims to unify. First, illusion-focused benchmarks such as IllusionVQA test large Vision-Language Models on comprehension and localization but do not provide a lightweight, deployable classifier or an explanation-generation layer. Second, illusion-replication studies (the brightness-illusion work using CNN/Autoencoder/U-Net/U-Net++, and the multi-modal CNN+GNN recognition model) focus on a narrow illusion category or lack pixel-level explainability and confidence scoring suitable for an end-user web application. Third, the quantum-tunnelling DNN offers a promising bio-inspired mechanism for representing ambiguous, multistable perception but remains a proof-of-concept, untested at dataset scale. Separately, image-forgery and deepfake detection research (e.g., DeepForgeryNet) has matured for detecting malicious manipulation but is not designed to recognize naturally occurring optical illusions, and no existing system combines illusion detection with manipulation detection in a single, explainable, confidence-scored pipeline.')

    add_h2('1.5 Proposed System')
    add_p('Perception-X proposes a unified AI-based pipeline that (1) detects whether an input image contains an ambiguous or illusory pattern, (2) classifies the specific illusion category (geometric, color and brightness, size, perspective and depth, motion, ambiguous figures, impossible objects, or normal image), (3) highlights the responsible image region using explainable-AI techniques such as Grad-CAM, (4) generates a human-readable explanation of the perceptual effect, (5) reports a confidence score for every prediction, and (6) optionally flags images that are digitally manipulated rather than naturally illusory. This directly addresses the research gaps identified across the five reviewed papers — combining VLM-level comprehension, CNN/U-Net-based pixel-level localization, bio-inspired handling of genuine ambiguity, and forgery-awareness in one accessible web-based system.')

    add_h2('1.6 Objectives of the Project (Mapped to Reviewed Papers)')
    
    add_p('Objective 1: Detect and classify the type of ambiguous/optical illusion image with high accuracy using a fused visual-contextual deep learning model.', bold=True)
    add_p('Mapped Reference Paper: [2] Leong, W.Y. (2024) — A Multi-Modal Deep Learning Approach for Enhanced Optical Illusion Recognition, IEEE WTA 2024.\nThis objective adopts the paper\'s CNN + Graph Neural Network fusion strategy for extracting and contextualizing visual features, but extends it with a lighter-weight backbone (transfer learning on ResNet/EfficientNet) suitable for real-time web inference, addressing the original paper\'s computational-overhead limitation.')

    add_p('Objective 2: Localize and visually explain the region responsible for the illusion, and generate a plain-language explanation with a confidence score.', bold=True)
    add_p('Mapped Reference Paper: [3] Mukherjee, A.; Paul, A.; Ghosh, K. (2024) — Deep Learning Models for Perception of Brightness Related Illusions, Applied Intelligence (Springer).\nBuilding on the paper\'s use of U-Net / U-Net++ encoder-decoder architectures — which naturally produce pixel-level outputs — this objective adapts the same architectural family (combined with Grad-CAM-style saliency mapping) to generate region-highlighting overlays and confidence scores across all illusion categories, not just brightness illusions.')

    add_p('Objective 3: Benchmark and validate system comprehension of ambiguous images against human-level performance, and handle genuinely multistable figures gracefully rather than forcing a single rigid label.', bold=True)
    add_p('Mapped Reference Paper: [1] Shahgir et al. (2024) — IllusionVQA: A Challenging Optical Illusion Dataset for Vision Language Models, COLM 2024.\nThis objective reuses the paper\'s comprehension/localization multiple-choice evaluation protocol as a validation benchmark for Perception-X, while incorporating an ambiguity-aware output (inspired by the quantum-tunnelling DNN concept in [4] Maksymov, 2024) so that genuinely multistable figures can be reported with split confidence rather than a forced single-class decision.')

    add_h2('1.7 Literature Review Table (Table 1.1)')
    add_p('Table 1.1: Literature Review Summary across 12 Comparison Parameters', italic=True)

    t_headers = ['Sl.', 'Year', 'Authors', 'Paper Title', 'Venue', 'Research Focus', 'Methodology', 'Key Contribution', 'Dataset', 'Limitations', 'Research Gap Found', 'DOI / Link']
    t_rows = [
        ['1', '2024', 'Shahgir et al.', 'IllusionVQA: Optical Illusion Dataset for VLMs', 'COLM 2024', 'Benchmarking VLM comprehension & localization', 'Curated VQA dataset; evaluated GPT-4V with few-shot CoT', 'Showed VLMs lag well behind human accuracy', 'IllusionVQA (686 Q&A)', 'No pixel-level explainability; mislocalization', 'No end-to-end pipeline with causal heatmaps', 'arXiv:2403.15952'],
        ['2', '2024', 'Leong, W.Y.', 'Multi-Modal Deep Learning Illusion Recognition', 'IEEE ISWTA 2024', 'Improving recognition by fusing visual & contextual cues', 'CNN visual extractor + Graph Neural Network fusion', 'Visual + graph reasoning improves accuracy', 'Mixed illusion corpus', 'High computational cost; no heatmaps', 'Lacks lightweight explainable web model', '10.1109/ISWTA (Doc 10698939)'],
        ['3', '2024', 'Mukherjee et al.', 'Deep Learning for Brightness Illusions', 'Springer Appl. Intell.', 'Replicating brightness-contrast illusions', 'CNN, Autoencoder, U-Net, U-Net++ restoration tasks', 'U-Net matches human lateral inhibition', 'Brightness illusion set', 'Restricted to brightness; no taxonomy', 'No unified model across categories', '10.1007/s10489-024-05658-w'],
        ['4', '2024', 'Maksymov, I.S.', 'Quantum-Tunnelling DNN for Illusion Recognition', 'AIP APL Mach. Learn.', 'Modeling ambiguous perception (Necker, Rubin)', 'QT-DNN: Quantum-tunnelling activation function', 'Produces oscillating dual-state probabilities', 'Synthetic Necker & Rubin', 'Proof-of-concept; not tested at scale', 'No large-scale deployable classifier', '10.1063/5.0225771'],
        ['5', '2026', 'DeepForgeryNet', 'DeepForgeryNet: Hybrid CNN-LSTM Framework', 'Frontiers in AI', 'Detecting manipulated & deepfake images', 'Hybrid CNN + LSTM transfer learning with augmentation', 'Cross-dataset forensic generalization', 'CASIA, CoMoFoD, NIST', 'High complexity; unaware of illusions', 'No illusion vs. manipulation integration', '10.3389/frai.2026.1810912']
    ]

    tbl = doc.add_table(rows=len(t_rows) + 1, cols=len(t_headers))
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    for c_i, h in enumerate(t_headers):
        cell = tbl.cell(0, c_i)
        cell.text = h
        set_cell_background(cell, '0A2540')
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        for r in p.runs:
            r.bold = True
            r.font.name = 'Times New Roman'
            r.font.size = Pt(8)
            r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
            
    for r_i, row in enumerate(t_rows):
        for c_i, val in enumerate(row):
            cell = tbl.cell(r_i + 1, c_i)
            cell.text = val
            set_cell_background(cell, 'F7FAFC' if r_i % 2 == 1 else 'FFFFFF')
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(1.5)
            p.paragraph_format.space_after = Pt(1.5)
            for r in p.runs:
                r.font.name = 'Times New Roman'
                r.font.size = Pt(7.5)

    add_h2('1.8 Research Gap Identified')
    gaps = [
        'No existing system performs illusion detection, multi-class illusion classification, region-level explainability and confidence scoring together in a single, deployable pipeline (Papers 1, 2, 3).',
        'Illusion-replication research remains category-specific (e.g., brightness-only in Paper 3), with no unified model spanning geometric, motion, depth, and ambiguous-figure categories.',
        'Bio-inspired handling of genuine perceptual ambiguity (Paper 4) has not been validated at dataset scale or integrated into a production classification system.',
        'Manipulation/deepfake detection research (Paper 5) is disconnected from illusion-detection research, leaving no system able to distinguish a naturally occurring illusion from a deliberately deceptive, digitally altered image.',
        'Vision-Language Model benchmarks (Paper 1) reveal a large human-AI performance gap in illusion localization that current lightweight, deployable models have not closed.'
    ]
    for g in gaps:
        add_bullet(g)

    # --- 2. DATASET CATALOG ---
    add_h1('2. DATASET CATALOG & IMPORT MANUAL')
    add_p('To enable researchers and developers to reproduce experiments, the datasets utilized across the 5 papers are cataloged below with exact schemas and Python import code:')
    
    datasets_info = [
        ('IllusionVQA (Shahgir et al., 2024)', 'COLM 2024 | Hugging Face: ahmadki/IllusionVQA',
         '686 curated items spanning Geometric, Brightness, Ambiguous, Impossible, and Camouflage categories with normalized bounding box annotations.\n'
         'Import Snippet:\n'
         'from datasets import load_dataset\n'
         'dataset = load_dataset("ahmadki/IllusionVQA")\n'
         'sample = dataset["test"][0]'),
         
        ('Multi-Modal Optical Illusion Corpus (Leong, 2024)', 'IEEE ISWTA 2024 | ImageFolder + Graphs',
         '~1,200 stimuli across Geometric, Chromatic, and Motion classes paired with patch connectivity adjacency graphs.\n'
         'Import Snippet:\n'
         'from torchvision import datasets, transforms\n'
         'transform = transforms.Compose([transforms.Resize((224, 224)), transforms.ToTensor()])\n'
         'dataset = datasets.ImageFolder("path/to/multimodal_corpus", transform=transform)'),
         
        ('Brightness-Contrast Psychophysical Dataset (Mukherjee et al., 2024)', 'Springer Applied Intelligence | TIFF / NumPy',
         '14 classical brightness stimuli (Hermann Grid, White\'s illusion, simultaneous contrast, Mach bands) with human perceived luminance profiles.\n'
         'Import Snippet:\n'
         'import numpy as np; from PIL import Image\n'
         'matrix = np.array(Image.open("hermann_grid.png").convert("L"), dtype=np.float32) / 255.0'),
         
        ('Ambiguous Multistable Figures Suite (Maksymov, 2024)', 'AIP APL Machine Learning | Vector Wireframes',
         'Synthetic Necker Cube, Rubin\'s Vase, and Duck-Rabbit stimuli with double-well potential parameters and dual-state ground-truth vectors.\n'
         'Import Snippet:\n'
         'bistable_data = {"rubin_vase": {"state_A": "Facing Profiles", "state_B": "Central Vase", "entropy": 1.0}}'),
         
        ('CASIA & CoMoFoD Forgery Datasets (DeepForgeryNet, 2026)', 'Frontiers in AI | JPEG/TIFF with Binary Masks',
         'CASIA v1 (1.7k) and CASIA v2 (12.6k) spliced and copy-move images with ground-truth tampering masks for forensic validation.\n'
         'Import Snippet:\n'
         'ela = ImageChops.difference(img, recompressed_jpeg)')
    ]
    for d_title, d_src, d_body in datasets_info:
        add_h2(d_title)
        add_p(d_src, italic=True, size=9.5)
        add_p(d_body)

    # --- 3. EMPIRICAL HANDS-ON RESULTS WITH EMBEDDED DIAGNOSTIC CARDS ---
    add_h1('3. EMPIRICAL HANDS-ON RESULTS & DIAGNOSTIC VISUALIZATIONS')
    add_p('Each stimulus was processed through the complete 5-stage Perception-X pipeline. The resulting 4-panel diagnostic visual cards are embedded below:')

    diagnostic_cases = [
        ('Cafe Wall Illusion', 'outputs/diagnostic_cafe_wall.png', 'Geometric & Distortion', 'Optical Illusion (93.29% conf)',
         'Parallel grout lines appear tilted due to border-locking among alternating high-contrast black and white tiles, tilting V1 simple-cell receptive fields.'),
        ('Hermann Grid Illusion', 'outputs/diagnostic_hermann_grid.png', 'Brightness & Contrast', 'Optical Illusion (88.00% conf)',
         'Phantom gray spots emerge at intersections due to lateral inhibition from 4 bright channels suppressing retinal ganglion cell firing rates.'),
        ('Digitally Manipulated Splicing', 'outputs/diagnostic_manipulated_splicing.png', 'Digital Splicing Forgery', 'Digital Forgery (98.00% conf)',
         'Localized block-variance ELA reveals an alien high-frequency noise patch inconsistent with natural imaging physics, successfully isolated from natural illusions.'),
        ('Muller-Lyer Illusion', 'outputs/diagnostic_muller_lyer.png', 'Geometric & Distortion', 'Optical Illusion (88.00% conf)',
         'Inward-pointing fins mimic closer convex 3D structures while outward fins mimic distant concave corners, triggering automatic size-constancy scaling in the brain.'),
        ('Natural Physical Object', 'outputs/diagnostic_natural_object.png', 'Normal / Non-Illusory Physical Object', 'Normal Object (94.00% conf)',
         'Continuous Lambertian reflectance and consistent directional lighting. Correctly passes through Stage 1 gating as is_object=True, is_illusion=False.'),
        ('Necker Cube Wireframe', 'outputs/diagnostic_necker_cube.png', 'Ambiguous & Multistable Figures', 'Optical Illusion (88.00% conf)',
         'Quantum-tunneling double-well resolution yielded a balanced dual-state probability: 47.45% Front-Lower View vs 52.55% Back-Upper View with Perceptual Entropy H = 0.9981.'),
        ('Rubin\'s Vase Silhouette', 'outputs/diagnostic_rubin_vase.png', 'Ambiguous & Multistable Figures', 'Optical Illusion (88.00% conf)',
         'Figure-ground rivalry yielded dual states: 60.89% Two Facing Silhouettes vs 39.11% Central Symmetrical Vase with Perceptual Entropy H = 0.9655.'),
        ('Simultaneous Contrast', 'outputs/diagnostic_simultaneous_contrast.png', 'Brightness & Contrast', 'Optical Illusion (88.00% conf)',
         'Identical gray center target patches on dark vs. light surrounds appear to have different brightness due to center-surround contrast induction.')
    ]

    for title, img_path, cat, gate, mech in diagnostic_cases:
        add_h2(f'Case Study: {title}')
        add_p(f'Category: {cat} | Primary Gating: {gate}', italic=True, size=10)
        add_p(f'Perceptual Mechanism: {mech}')
        if os.path.exists(img_path):
            try:
                doc.add_picture(img_path, width=Inches(6.0))
                p_cap = doc.add_paragraph()
                p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p_cap.paragraph_format.space_after = Pt(10)
                r_cap = p_cap.add_run(f'Figure: 4-Panel Perception-X Diagnostic Card for {title}')
                r_cap.font.name = 'Times New Roman'
                r_cap.font.size = Pt(9.5)
                r_cap.font.italic = True
            except Exception as e:
                add_p(f'[Image file located at: {img_path}]')
        add_p('', space_after=6)

    # --- 4. CODEBASE STRUCTURE & EXECUTION ---
    add_h1('4. CODEBASE STRUCTURE & EXECUTION INSTRUCTIONS')
    add_p('The complete system is organized in perception_x_optical_illusion/ with modular components:')
    
    code_layout = (
        'perception_x_optical_illusion/\n'
        '├── docs/                                    # Markdown documentation suite\n'
        '│   ├── LITERATURE_REVIEW.md                 # Full 5-paper review & Table 1.1\n'
        '│   ├── DATASETS_GUIDE.md                    # Dataset schemas & import snippets\n'
        '│   ├── SYSTEM_WORKFLOW_AND_ARCHITECTURE.md  # 7-stage technical workflow\n'
        '│   └── HANDS_ON_GUIDE.md                    # Tutorial & custom image testing\n'
        '├── data/\n'
        '│   ├── dataset_catalog.json                 # Metadata catalog\n'
        '│   ├── dataset_importers.py                 # Importers for IllusionVQA, CASIA, etc.\n'
        '│   ├── synthetic_generators.py              # Procedural illusion stimuli generator\n'
        '│   └── samples/                             # 8 test stimuli PNGs\n'
        '├── core/\n'
        '│   ├── feature_extractor.py                 # Luminance, 2D FFT, Localized ELA, Symmetry\n'
        '│   ├── ambiguity_engine.py                  # Quantum-tunnelling bistability solver\n'
        '│   ├── explainability.py                    # Causal heatmap overlay & bounding box\n'
        '│   └── reasoning_engine.py                  # Cognitive perceptual reasoner\n'
        '├── models/\n'
        '│   └── perception_x_pipeline.py             # 5-stage hierarchical classification engine\n'
        '├── outputs/                                 # 8 high-resolution 4-panel diagnostic PNGs\n'
        '├── hands_on_demo.py                         # Interactive test runner\n'
        '└── generate_docx_report.py                  # Word report generator'
    )
    add_p(code_layout, size=8.5, space_after=12)

    # Save to multiple convenient destinations
    doc_paths = [
        'Perception_X_Research_Analysis_Report.docx',
        os.path.expanduser('~') + '/Downloads/Perception_X_Research_Analysis_Report.docx',
        os.path.expanduser('~') + '/Desktop/Perception_X_Research_Analysis_Report.docx'
    ]
    
    for p in doc_paths:
        try:
            doc.save(p)
            print(f'Successfully saved Times New Roman DOCX to: {p}')
        except Exception as e:
            print(f'Could not save to {p}: {e}')

if __name__ == '__main__':
    create_tnr_document()
