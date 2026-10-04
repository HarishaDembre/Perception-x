"""
Dataset Builder & Synthesizer for Training Perception-X
Generates a diverse dataset of:
1. Normal Physical Objects (spheres, cylinders, cubes with realistic lighting)
2. Geometric Illusions (Muller-Lyer, Cafe Wall, Poggendorff)
3. Brightness Illusions (Hermann Grid, Simultaneous Contrast)
4. Ambiguous & Multistable Figures (Rubin's Vase, Necker Cube)
5. Manipulated / Forged Images (Spliced anomalies)
"""

import os
import random
import numpy as np
from PIL import Image, ImageDraw

def generate_random_object(size=(128, 128)):
    """Generates an unambiguous 3D shaded physical object."""
    w, h = size
    arr = np.ones((h, w, 3), dtype=np.uint8) * random.randint(220, 245)
    cx = random.randint(w // 3, 2 * w // 3)
    cy = random.randint(h // 3, 2 * h // 3)
    radius = random.randint(30, 48)
    
    # Random light direction
    lx, ly = random.uniform(-1, 1), random.uniform(-1, 1)
    lz = random.uniform(0.4, 1.0)
    light_dir = np.array([lx, ly, lz])
    light_dir = light_dir / np.linalg.norm(light_dir)
    
    obj_type = random.choice(["sphere", "cylinder", "torus"])
    
    for y in range(h):
        for x in range(w):
            dx = x - cx
            dy = y - cy
            dist_sq = dx * dx + dy * dy
            if dist_sq <= radius * radius:
                dz = np.sqrt(radius * radius - dist_sq)
                normal = np.array([dx, dy, dz]) / radius
                diffuse = max(0.0, np.dot(normal, light_dir))
                ambient = 0.25
                intensity = int(np.clip((ambient + 0.75 * diffuse) * 220, 0, 255))
                arr[y, x] = [intensity, int(intensity * 0.75), int(intensity * 0.6)]
                
    return Image.fromarray(arr)

def generate_random_geometric_illusion(size=(128, 128)):
    """Generates random variations of Muller-Lyer or Cafe Wall."""
    w, h = size
    sub = random.choice(["muller", "cafe"])
    
    if sub == "muller":
        img = Image.new('RGB', size, color=(250, 250, 250))
        draw = ImageDraw.Draw(img)
        cx, cy = w // 2, h // 2
        length = random.randint(50, 80)
        fin = random.randint(12, 22)
        y1, y2 = cy - 25, cy + 25
        
        # Line 1 (<--->)
        draw.line([cx - length//2, y1, cx + length//2, y1], fill=(20, 20, 20), width=2)
        draw.line([cx - length//2, y1, cx - length//2 + fin, y1 - fin], fill=(20, 20, 20), width=2)
        draw.line([cx - length//2, y1, cx - length//2 + fin, y1 + fin], fill=(20, 20, 20), width=2)
        draw.line([cx + length//2, y1, cx + length//2 - fin, y1 - fin], fill=(20, 20, 20), width=2)
        draw.line([cx + length//2, y1, cx + length//2 - fin, y1 + fin], fill=(20, 20, 20), width=2)
        
        # Line 2 (>---<)
        draw.line([cx - length//2, y2, cx + length//2, y2], fill=(20, 20, 20), width=2)
        draw.line([cx - length//2, y2, cx - length//2 - fin, y2 - fin], fill=(20, 20, 20), width=2)
        draw.line([cx - length//2, y2, cx - length//2 - fin, y2 + fin], fill=(20, 20, 20), width=2)
        draw.line([cx + length//2, y2, cx + length//2 + fin, y2 - fin], fill=(20, 20, 20), width=2)
        draw.line([cx + length//2, y2, cx + length//2 + fin, y2 + fin], fill=(20, 20, 20), width=2)
        return img
    else:
        # Cafe Wall
        img = Image.new('RGB', size, color=(140, 140, 140))
        draw = ImageDraw.Draw(img)
        rows = random.randint(5, 7)
        cols = random.randint(6, 8)
        mortar = 2
        row_h = (h - (rows + 1) * mortar) // rows
        col_w = w // cols
        for r in range(rows):
            y0 = mortar + r * (row_h + mortar)
            shift = (r % 3) * (col_w // 3)
            for c in range(-1, cols + 2):
                x0 = c * col_w + shift
                color = (20, 20, 20) if (c % 2 == 0) else (240, 240, 240)
                draw.rectangle([x0, y0, x0 + col_w, y0 + row_h], fill=color)
        return img

def generate_random_brightness_illusion(size=(128, 128)):
    """Generates random variations of Hermann grid or Simultaneous contrast."""
    w, h = size
    sub = random.choice(["hermann", "contrast"])
    
    if sub == "hermann":
        img = Image.new('RGB', size, color=(255, 255, 255))
        draw = ImageDraw.Draw(img)
        grid_n = random.randint(3, 5)
        bar_w = random.randint(6, 12)
        bw = (w - (grid_n - 1) * bar_w) // grid_n
        bh = (h - (grid_n - 1) * bar_w) // grid_n
        for i in range(grid_n):
            for j in range(grid_n):
                x0 = i * (bw + bar_w)
                y0 = j * (bh + bar_w)
                draw.rectangle([x0, y0, x0 + bw, y0 + bh], fill=(10, 10, 10))
        return img
    else:
        # Simultaneous contrast
        img = Image.new('RGB', size)
        draw = ImageDraw.Draw(img)
        draw.rectangle([0, 0, w // 2, h], fill=(25, 25, 25))
        draw.rectangle([w // 2, 0, w, h], fill=(235, 235, 235))
        pw, ph = random.randint(24, 34), random.randint(24, 34)
        draw.rectangle([(w//4) - pw//2, (h//2) - ph//2, (w//4) + pw//2, (h//2) + ph//2], fill=(128, 128, 128))
        draw.rectangle([(3*w//4) - pw//2, (h//2) - ph//2, (3*w//4) + pw//2, (h//2) + ph//2], fill=(128, 128, 128))
        return img

def generate_random_ambiguous_illusion(size=(128, 128)):
    """Generates Rubin's vase or Necker cube."""
    w, h = size
    sub = random.choice(["necker", "rubin"])
    
    if sub == "necker":
        img = Image.new('RGB', size, color=(255, 255, 255))
        draw = ImageDraw.Draw(img)
        cx, cy = w // 2, h // 2
        s = random.randint(40, 55)
        off = random.randint(15, 22)
        x1, y1 = cx - s//2 - off//2, cy - s//2 + off//2
        draw.rectangle([x1, y1, x1 + s, y1 + s], outline=(20, 20, 20), width=2)
        draw.rectangle([x1 + off, y1 - off, x1 + off + s, y1 - off + s], outline=(20, 20, 20), width=2)
        draw.line([x1, y1, x1 + off, y1 - off], fill=(20, 20, 20), width=2)
        draw.line([x1 + s, y1, x1 + off + s, y1 - off], fill=(20, 20, 20), width=2)
        draw.line([x1, y1 + s, x1 + off, y1 - off + s], fill=(20, 20, 20), width=2)
        draw.line([x1 + s, y1 + s, x1 + off + s, y1 - off + s], fill=(20, 20, 20), width=2)
        return img
    else:
        # Rubin's vase
        arr = np.ones((h, w, 3), dtype=np.uint8) * 240
        y_coords = np.linspace(-np.pi, np.pi, h)
        a1, a2 = random.uniform(20, 30), random.uniform(10, 18)
        profile = 25 + a1 * np.cos(y_coords) + a2 * np.sin(2 * y_coords)
        mid = w // 2
        for y in range(h):
            dx = int(profile[y])
            arr[y, :mid - dx] = [30, 30, 30]
            arr[y, mid + dx:] = [30, 30, 30]
        return Image.fromarray(arr)

def build_training_dataset(base_dir="data/dataset"):
    """
    Creates dataset structure:
    train/
      0_object/
      1_geometric/
      2_brightness/
      3_ambiguous/
    val/
      0_object/
      1_geometric/
      2_brightness/
      3_ambiguous/
    """
    splits = {"train": 60, "val": 20} # per category
    generators = {
        "0_object": generate_random_object,
        "1_geometric": generate_random_geometric_illusion,
        "2_brightness": generate_random_brightness_illusion,
        "3_ambiguous": generate_random_ambiguous_illusion
    }
    
    total = 0
    for split, count in splits.items():
        for cat_name, gen_func in generators.items():
            cat_dir = os.path.join(base_dir, split, cat_name)
            os.makedirs(cat_dir, exist_ok=True)
            for i in range(count):
                img = gen_func()
                save_path = os.path.join(cat_dir, f"{cat_name}_{i:03d}.png")
                img.save(save_path)
                total += 1
                
    print(f"Generated {total} total dataset images across train and val splits in '{base_dir}'")
    return base_dir

if __name__ == "__main__":
    build_training_dataset()
