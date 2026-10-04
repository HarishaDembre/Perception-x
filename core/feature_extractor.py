"""
Multi-Domain Feature Extractor for Perception-X
Extracts physical, frequency, psychophysical, and manipulation features:
1. Luminance Profiles (Mukherjee et al., 2024)
2. 2D Fourier Frequency Spectrum (Leong, 2024)
3. Localized Error Level Analysis (ELA) for Tampering Detection (DeepForgeryNet, 2026)
4. Gradient & Geometric Disparity (Leong, 2024)
5. Ambiguity / Multistable Perceptual Entropy (Maksymov, 2024)
"""

import io
import numpy as np
from PIL import Image, ImageChops, ImageEnhance

class IllusionFeatureExtractor:
    def __init__(self):
        pass

    def extract_luminance_profile(self, img_pil):
        """Calculates horizontal and vertical cross-sectional luminance profiles."""
        gray = np.array(img_pil.convert('L'), dtype=np.float32) / 255.0
        h, w = gray.shape
        h_profile = gray[h // 2, :]
        v_profile = gray[:, w // 2]
        
        min_lum = float(np.min(gray))
        max_lum = float(np.max(gray))
        michelson_contrast = float((max_lum - min_lum) / (max_lum + min_lum + 1e-6))
        rms_contrast = float(np.std(gray))
        
        return {
            "h_profile": h_profile,
            "v_profile": v_profile,
            "michelson_contrast": michelson_contrast,
            "rms_contrast": rms_contrast,
            "mean_luminance": float(np.mean(gray))
        }

    def extract_fourier_spectrum(self, img_pil):
        """Computes 2D Fast Fourier Transform (FFT) magnitude spectrum."""
        gray = np.array(img_pil.convert('L'), dtype=np.float32)
        f = np.fft.fft2(gray)
        fshift = np.fft.fftshift(f)
        magnitude_spectrum = np.log(np.abs(fshift) + 1.0)
        
        h, w = magnitude_spectrum.shape
        center_y, center_x = h // 2, w // 2
        radius = min(h, w) // 6
        
        y, x = np.ogrid[:h, :w]
        mask = ((x - center_x)**2 + (y - center_y)**2) > (radius**2)
        hf_energy = float(np.mean(magnitude_spectrum[mask]))
        peak_periodicity = float(np.max(magnitude_spectrum[mask]) / (np.mean(magnitude_spectrum[mask]) + 1e-6))
        
        return {
            "magnitude_spectrum": magnitude_spectrum,
            "high_freq_energy": hf_energy,
            "periodicity_ratio": peak_periodicity
        }

    def compute_error_level_analysis(self, img_pil, quality=90):
        """
        Localized Error Level Analysis (ELA) to detect digital manipulation / splicing artifacts.
        Distinguishes global compression ringing from localized tampering discrepancies.
        """
        rgb = img_pil.convert('RGB')
        buf = io.BytesIO()
        rgb.save(buf, format='JPEG', quality=quality)
        buf.seek(0)
        recompressed = Image.open(buf)
        
        diff = ImageChops.difference(rgb, recompressed)
        diff_arr = np.array(diff, dtype=np.float32)
        diff_gray = np.mean(diff_arr, axis=2) # 2D error map
        
        h, w = diff_gray.shape
        grid_rows, grid_cols = 8, 8
        block_h, block_w = h // grid_rows, w // grid_cols
        
        block_means = []
        for r in range(grid_rows):
            for c in range(grid_cols):
                patch = diff_gray[r*block_h:(r+1)*block_h, c*block_w:(c+1)*block_w]
                block_means.append(np.mean(patch))
                
        block_means = np.array(block_means)
        median_err = float(np.median(block_means))
        max_err = float(np.max(block_means))
        
        # Localized inconsistency ratio: Splicing causes one patch to spike far above the rest
        discrepancy_ratio = float(max_err / (median_err + 1.5))
        
        # Forgery score is high ONLY when localized discrepancy is anomalous
        forgery_score = float(np.clip((discrepancy_ratio - 2.2) / 3.0, 0.0, 1.0))
        
        ela_max = float(np.max(diff_arr))
        scale = 15.0 if ela_max == 0 else min(255.0 / (ela_max + 1e-6), 25.0)
        enhanced_diff = ImageEnhance.Brightness(diff).enhance(scale)
        
        return {
            "ela_mean": float(np.mean(diff_arr)),
            "ela_max": ela_max,
            "discrepancy_ratio": discrepancy_ratio,
            "forgery_score": forgery_score,
            "ela_image": enhanced_diff
        }

    def compute_ambiguity_metrics(self, img_pil):
        """Evaluates figure-ground symmetry and bistable energy balance."""
        gray = np.array(img_pil.convert('L'), dtype=np.float32) / 255.0
        h, w = gray.shape
        
        median_thresh = np.median(gray)
        binary = gray > median_thresh
        black_ratio = float(np.mean(~binary))
        white_ratio = float(np.mean(binary))
        
        balance_index = 1.0 - abs(white_ratio - black_ratio)
        
        left_half = gray[:, :w//2]
        right_half_flipped = np.fliplr(gray[:, w//2:])
        min_cols = min(left_half.shape[1], right_half_flipped.shape[1])
        sym_diff = np.mean(np.abs(left_half[:, :min_cols] - right_half_flipped[:, :min_cols]))
        symmetry_score = float(1.0 - np.clip(sym_diff * 2.0, 0.0, 1.0))
        
        ambiguity_potential = float(np.clip(0.55 * balance_index + 0.45 * symmetry_score, 0.0, 1.0))
        
        return {
            "figure_ground_balance": balance_index,
            "bilateral_symmetry": symmetry_score,
            "ambiguity_potential": ambiguity_potential
        }

    def extract_all(self, img_pil):
        lum = self.extract_luminance_profile(img_pil)
        fft = self.extract_fourier_spectrum(img_pil)
        ela = self.compute_error_level_analysis(img_pil)
        amb = self.compute_ambiguity_metrics(img_pil)
        
        return {
            "luminance": lum,
            "fourier": fft,
            "ela": ela,
            "ambiguity": amb
        }
