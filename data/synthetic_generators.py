import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import os

def generate_hermann_grid(size=(400, 400), grid_n=4, bar_width=20):
    """Generates a Hermann Grid illusion (Brightness/Contrast Category)."""
    img = Image.new('RGB', size, color=(0, 0, 0))
    w, h = size
    block_w = (w - (grid_n - 1) * bar_width) // grid_n
    block_h = (h - (grid_n - 1) * bar_width) // grid_n
    
    img_white = Image.new('RGB', size, color=(255, 255, 255))
    draw_w = ImageDraw.Draw(img_white)
    
    for i in range(grid_n):
        for j in range(grid_n):
            x0 = i * (block_w + bar_width)
            y0 = j * (block_h + bar_width)
            x1 = x0 + block_w
            y1 = y0 + block_h
            draw_w.rectangle([x0, y0, x1, y1], fill=(0, 0, 0))
            
    return img_white

def generate_muller_lyer(size=(400, 400), line_length=200, fin_length=35):
    """Generates Muller-Lyer illusion (Geometric Category)."""
    img = Image.new('RGB', size, color=(250, 250, 250))
    draw = ImageDraw.Draw(img)
    cx, cy = size[0] // 2, size[1] // 2
    
    # Top line: inward fins (<--->)
    y_top = cy - 70
    x0_top = cx - line_length // 2
    x1_top = cx + line_length // 2
    draw.line([x0_top, y_top, x1_top, y_top], fill=(20, 20, 20), width=4)
    draw.line([x0_top, y_top, x0_top + fin_length, y_top - fin_length], fill=(20, 20, 20), width=4)
    draw.line([x0_top, y_top, x0_top + fin_length, y_top + fin_length], fill=(20, 20, 20), width=4)
    draw.line([x1_top, y_top, x1_top - fin_length, y_top - fin_length], fill=(20, 20, 20), width=4)
    draw.line([x1_top, y_top, x1_top - fin_length, y_top + fin_length], fill=(20, 20, 20), width=4)
    
    # Bottom line: outward fins (>---<)
    y_bot = cy + 70
    x0_bot = cx - line_length // 2
    x1_bot = cx + line_length // 2
    draw.line([x0_bot, y_bot, x1_bot, y_bot], fill=(20, 20, 20), width=4)
    draw.line([x0_bot, y_bot, x0_bot - fin_length, y_bot - fin_length], fill=(20, 20, 20), width=4)
    draw.line([x0_bot, y_bot, x0_bot - fin_length, y_bot + fin_length], fill=(20, 20, 20), width=4)
    draw.line([x1_bot, y_bot, x1_bot + fin_length, y_bot - fin_length], fill=(20, 20, 20), width=4)
    draw.line([x1_bot, y_bot, x1_bot + fin_length, y_bot + fin_length], fill=(20, 20, 20), width=4)
    
    return img

def generate_rubin_vase(size=(400, 400)):
    """Generates Rubin's Vase bistable figure-ground illusion (Ambiguous Category)."""
    w, h = size
    arr = np.ones((h, w, 3), dtype=np.uint8) * 240
    
    y_coords = np.linspace(-np.pi, np.pi, h)
    profile = 70 + 35 * np.cos(y_coords) + 25 * np.sin(2 * y_coords) - 15 * np.cos(3 * y_coords)
    
    mid = w // 2
    for y in range(h):
        dx = int(profile[y])
        arr[y, :mid - dx] = [30, 30, 30]
        arr[y, mid + dx:] = [30, 30, 30]
        
    return Image.fromarray(arr)

def generate_necker_cube(size=(400, 400), s=130, offset=50):
    """Generates Necker Cube wireframe (Ambiguous / Multistable Depth Category)."""
    img = Image.new('RGB', size, color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    cx, cy = size[0] // 2, size[1] // 2
    
    x1, y1 = cx - s // 2 - offset // 2, cy - s // 2 + offset // 2
    x2, y2 = x1 + s, y1 + s
    
    x3, y3 = x1 + offset, y1 - offset
    x4, y4 = x3 + s, y3 + s
    
    draw.rectangle([x1, y1, x2, y2], outline=(20, 20, 20), width=4)
    draw.rectangle([x3, y3, x4, y4], outline=(20, 20, 20), width=4)
    
    draw.line([x1, y1, x3, y3], fill=(20, 20, 20), width=4)
    draw.line([x2, y1, x4, y3], fill=(20, 20, 20), width=4)
    draw.line([x1, y2, x3, y4], fill=(20, 20, 20), width=4)
    draw.line([x2, y2, x4, y4], fill=(20, 20, 20), width=4)
    
    return img

def generate_simultaneous_contrast(size=(400, 400), patch_size=(90, 90)):
    """Generates Simultaneous Brightness Contrast illusion (Brightness/Contrast Category)."""
    img = Image.new('RGB', size)
    w, h = size
    draw = ImageDraw.Draw(img)
    
    draw.rectangle([0, 0, w // 2, h], fill=(30, 30, 30))
    draw.rectangle([w // 2, 0, w, h], fill=(230, 230, 230))
    
    pw, ph = patch_size
    lx0 = (w // 4) - pw // 2
    ly0 = (h // 2) - ph // 2
    draw.rectangle([lx0, ly0, lx0 + pw, ly0 + ph], fill=(128, 128, 128))
    
    rx0 = (3 * w // 4) - pw // 2
    ry0 = (h // 2) - ph // 2
    draw.rectangle([rx0, ry0, rx0 + pw, ry0 + ph], fill=(128, 128, 128))
    
    return img

def generate_cafe_wall(size=(400, 400), rows=8, cols=10, mortar=3):
    """Generates Cafe Wall illusion (Geometric Category)."""
    img = Image.new('RGB', size, color=(140, 140, 140))
    draw = ImageDraw.Draw(img)
    w, h = size
    row_h = (h - (rows + 1) * mortar) // rows
    col_w = w // cols
    
    shifts = [0, col_w // 3, 2 * col_w // 3, col_w // 3, 0, col_w // 3, 2 * col_w // 3, col_w // 3]
    
    for r in range(rows):
        y0 = mortar + r * (row_h + mortar)
        y1 = y0 + row_h
        shift = shifts[r % len(shifts)]
        for c in range(-1, cols + 2):
            x0 = c * col_w + shift
            x1 = x0 + col_w
            color = (15, 15, 15) if (c % 2 == 0) else (245, 245, 245)
            draw.rectangle([x0, y0, x1, y1], fill=color)
            
    return img

def generate_natural_object(size=(400, 400)):
    """Generates a standard, unambiguous 3D shaded sphere/object (Normal / Non-Illusion)."""
    w, h = size
    arr = np.ones((h, w, 3), dtype=np.uint8) * 235
    cx, cy = w // 2, h // 2
    radius = 120
    
    light_dir = np.array([-0.577, -0.577, 0.577])
    
    for y in range(h):
        for x in range(w):
            dx = (x - cx)
            dy = (y - cy)
            dist_sq = dx * dx + dy * dy
            if dist_sq <= radius * radius:
                dz = np.sqrt(radius * radius - dist_sq)
                normal = np.array([dx, dy, dz]) / radius
                diffuse = max(0.0, np.dot(normal, -light_dir))
                ambient = 0.25
                intensity = int(np.clip((ambient + 0.75 * diffuse) * 220, 0, 255))
                arr[y, x] = [intensity, int(intensity * 0.7), int(intensity * 0.5)]
                
    return Image.fromarray(arr)

def generate_manipulated_splicing(size=(400, 400)):
    """Generates a digitally manipulated/spliced image with compression artifact inconsistency (Forgery)."""
    img = generate_natural_object(size)
    draw = ImageDraw.Draw(img)
    cx, cy = size[0] // 2 + 50, size[1] // 2 + 30
    draw.rectangle([cx - 40, cy - 40, cx + 40, cy + 40], fill=(40, 180, 220), outline=(255, 0, 0), width=2)
    arr = np.array(img)
    noise = np.random.randint(-45, 45, (80, 80, 3))
    patch = np.clip(arr[cy-40:cy+40, cx-40:cx+40].astype(int) + noise, 0, 255).astype(np.uint8)
    arr[cy-40:cy+40, cx-40:cx+40] = patch
    return Image.fromarray(arr)

def generate_all_samples(output_dir="data/samples"):
    os.makedirs(output_dir, exist_ok=True)
    stimuli = {
        "hermann_grid": (generate_hermann_grid(), "Brightness / Contrast Illusion (Lateral Inhibition)"),
        "muller_lyer": (generate_muller_lyer(), "Geometric Illusion (Arrowhead Length Distortion)"),
        "rubin_vase": (generate_rubin_vase(), "Ambiguous Figure (Bistable Face-Vase Perception)"),
        "necker_cube": (generate_necker_cube(), "Ambiguous 3D Wireframe (Multistable Depth Reversal)"),
        "simultaneous_contrast": (generate_simultaneous_contrast(), "Brightness / Contrast Illusion (Center-Surround Induction)"),
        "cafe_wall": (generate_cafe_wall(), "Geometric Illusion (Border Shifted Parallel Misalignment)"),
        "natural_object": (generate_natural_object(), "Unambiguous Natural Object (Shaded Sphere - Non-Illusion)"),
        "manipulated_splicing": (generate_manipulated_splicing(), "Digitally Manipulated / Spliced Forgery (High-Frequency Artifact)")
    }
    
    manifest = []
    for key, (img, desc) in stimuli.items():
        path = os.path.join(output_dir, f"{key}.png")
        img.save(path)
        manifest.append({"name": key, "path": path, "description": desc})
        print(f"Generated sample: {path} -> {desc}")
        
    return manifest

if __name__ == "__main__":
    generate_all_samples()
