"""
Explainability & Localization Engine for Perception-X
Inspired by:
- Mukherjee et al. (2024) - U-Net Receptive Field Saliency & Luminance Induction Maps
- Shahgir et al. (2024 - IllusionVQA) - Causal Trigger Region Soft-Localization
"""

import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

class IllusionExplainabilityEngine:
    def __init__(self):
        pass

    def generate_causal_heatmap(self, img_pil, category, features):
        """
        Generates a pixel-level activation heatmap pinpointing the visual trigger
        causing the perceptual illusion or manipulation.
        """
        gray = np.array(img_pil.convert('L'), dtype=np.float32) / 255.0
        h, w = gray.shape
        heatmap = np.zeros((h, w), dtype=np.float32)
        
        # 1. Edge & gradient detection
        gy, gx = np.gradient(gray)
        gradient_mag = np.sqrt(gx**2 + gy**2)
        
        if "Brightness" in category or "Hermann" in category or "hermann" in category:
            row_mean = np.mean(gray, axis=1, keepdims=True)
            col_mean = np.mean(gray, axis=0, keepdims=True)
            intersection_map = (gray > 0.8) & (row_mean > 0.15) & (col_mean > 0.15)
            heatmap = intersection_map.astype(np.float32) * 0.9 + gradient_mag * 0.2
            
        elif "Geometric" in category or "muller" in category or "cafe" in category:
            laplacian = np.abs(np.gradient(gx)[1] + np.gradient(gy)[0])
            heatmap = laplacian / (np.max(laplacian) + 1e-6)
            
        elif "Ambiguous" in category or "rubin" in category or "necker" in category:
            heatmap = gradient_mag / (np.max(gradient_mag) + 1e-6)
            
        elif "Manipulated" in category or "Forgery" in category:
            ela_img = features["ela"]["ela_image"]
            ela_gray = np.array(ela_img.convert('L'), dtype=np.float32)
            heatmap = ela_gray / (np.max(ela_gray) + 1e-6)
            
        else: # Normal natural object
            heatmap = gradient_mag * 0.3
            
        # Normalize heatmap to [0, 1]
        heatmap = (heatmap - np.min(heatmap)) / (np.max(heatmap) - np.min(heatmap) + 1e-6)
        
        # Calculate soft-localization bounding box (Shahgir et al., 2024 IllusionVQA protocol)
        thresh = np.percentile(heatmap, 85)
        hot_y, hot_x = np.where(heatmap >= thresh)
        if len(hot_y) > 0 and len(hot_x) > 0:
            ymin, ymax = int(np.min(hot_y)), int(np.max(hot_y))
            xmin, xmax = int(np.min(hot_x)), int(np.max(hot_x))
            bbox = [ymin, xmin, ymax, xmax]
        else:
            bbox = [h//4, w//4, 3*h//4, 3*w//4]
            
        return heatmap, bbox

    def create_overlay_image(self, img_pil, heatmap, alpha=0.45):
        """Creates an RGB visual overlay with a JET colormap blended over the input image."""
        img_rgb = np.array(img_pil.convert('RGB'), dtype=np.float32) / 255.0
        
        # Use modern matplotlib colormaps
        cmap = plt.colormaps['jet']
        heatmap_colored = cmap(heatmap)[:, :, :3]
        
        # Blend
        overlay = (1.0 - alpha) * img_rgb + alpha * heatmap_colored
        overlay = np.clip(overlay * 255.0, 0, 255).astype(np.uint8)
        
        return Image.fromarray(overlay)
