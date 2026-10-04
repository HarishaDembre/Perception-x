"""
Perception-X Local Web Application Server
A zero-dependency browser-based GUI built on Python's standard http.server.
Allows interactive drag-and-drop image analysis, preset illusion testing,
multistability inspection, and visual feature examination.
"""

import os
import sys
import io
import json
import base64
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from PIL import Image
import numpy as np

# Local imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from models.perception_x_pipeline import PerceptionXPipeline

PORT = 8500
PIPELINE = PerceptionXPipeline()

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Perception-X : AI Optical Illusion & Ambiguous Image Workbench</title>
    <link href="https://fonts.googleapis.com/css2?family=Times+New+Roman&family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary: #0A2540;
            --accent: #0066CC;
            --bg: #F7FAFC;
            --card-bg: #FFFFFF;
            --text-main: #1A202C;
            --text-muted: #4A5568;
            --border: #E2E8F0;
            --success-bg: #C6F6D5;
            --success-text: #22543D;
            --danger-bg: #FED7D7;
            --danger-text: #742A2A;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: 'Times New Roman', serif;
            background-color: var(--bg);
            color: var(--text-main);
            line-height: 1.5;
        }
        header {
            background-color: var(--primary);
            color: #FFFFFF;
            padding: 16px 32px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
        header h1 {
            font-size: 1.4rem;
            letter-spacing: 0.5px;
        }
        header p {
            font-size: 0.85rem;
            color: #CBD5E0;
            font-style: italic;
        }
        .container {
            max-width: 1350px;
            margin: 20px auto;
            padding: 0 20px;
            display: grid;
            grid-template-columns: 320px 1fr;
            gap: 20px;
        }
        .sidebar {
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.04);
            height: fit-content;
        }
        .sidebar h2 {
            font-size: 1.1rem;
            color: var(--primary);
            margin-bottom: 12px;
            border-bottom: 2px solid var(--border);
            padding-bottom: 6px;
        }
        .upload-zone {
            border: 2px dashed #CBD5E0;
            border-radius: 6px;
            padding: 20px;
            text-align: center;
            cursor: pointer;
            background: #F8FAFC;
            transition: all 0.2s ease;
            margin-bottom: 16px;
        }
        .upload-zone:hover {
            border-color: var(--accent);
            background: #EDF2F7;
        }
        .upload-zone input { display: none; }
        .preset-btn {
            display: block;
            width: 100%;
            padding: 8px 12px;
            margin-bottom: 6px;
            background: #EDF2F7;
            border: 1px solid #CBD5E0;
            border-radius: 4px;
            font-family: 'Times New Roman', serif;
            font-size: 0.9rem;
            text-align: left;
            cursor: pointer;
            transition: all 0.15s ease;
        }
        .preset-btn:hover {
            background: var(--accent);
            color: #FFFFFF;
            border-color: var(--accent);
        }
        .main-panel {
            display: flex;
            flex-direction: column;
            gap: 20px;
        }
        .visual-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 12px;
        }
        .visual-card {
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 6px;
            padding: 10px;
            text-align: center;
            box-shadow: 0 2px 4px rgba(0,0,0,0.03);
        }
        .visual-card h3 {
            font-size: 0.95rem;
            color: var(--primary);
            margin-bottom: 8px;
        }
        .visual-card img {
            width: 100%;
            height: 180px;
            object-fit: contain;
            background: #EDF2F7;
            border-radius: 4px;
            border: 1px solid #E2E8F0;
        }
        .card {
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.04);
        }
        .card h2 {
            font-size: 1.15rem;
            color: var(--primary);
            margin-bottom: 12px;
        }
        .badges-row {
            display: flex;
            gap: 12px;
            margin-bottom: 16px;
            flex-wrap: wrap;
        }
        .badge {
            padding: 6px 14px;
            border-radius: 4px;
            font-weight: bold;
            font-size: 0.95rem;
            border: 1px solid transparent;
        }
        .badge-illusion { background: var(--success-bg); color: var(--success-text); border-color: #9AE6B4; }
        .badge-forgery { background: var(--danger-bg); color: var(--danger-text); border-color: #FEB2B2; }
        .badge-object { background: #EBF8FF; color: #2B6CB0; border-color: #BEE3F8; }
        .badge-category { background: #EDF2F7; color: #2D3748; border-color: #CBD5E0; }
        .reasoning-box p {
            margin-bottom: 8px;
            font-size: 1rem;
        }
        .reasoning-box strong { color: var(--primary); }
        .prob-bar-container {
            margin: 10px 0;
        }
        .prob-label {
            display: flex;
            justify-content: space-between;
            font-size: 0.9rem;
            margin-bottom: 3px;
        }
        .prob-bar {
            background: #E2E8F0;
            border-radius: 4px;
            height: 14px;
            overflow: hidden;
        }
        .prob-fill {
            background: var(--accent);
            height: 100%;
            transition: width 0.3s ease;
        }
        .metrics-table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 10px;
            font-size: 0.95rem;
        }
        .metrics-table th, .metrics-table td {
            border: 1px solid var(--border);
            padding: 8px 12px;
            text-align: left;
        }
        .metrics-table th { background: #EDF2F7; color: var(--primary); }
    </style>
</head>
<body>
    <header>
        <div>
            <h1>PERCEPTION-X WORKBENCH</h1>
            <p>AI Optical Illusion Detection • Multistability Resolution • Explainable Attribution</p>
        </div>
        <div style="font-size: 0.85rem; color: #E2E8F0;">Times New Roman Layout • Python 3.14 Engine</div>
    </header>

    <div class="container">
        <!-- Sidebar Controls -->
        <div class="sidebar">
            <h2>Select Input Image</h2>
            <div class="upload-zone" onclick="document.getElementById('fileInput').click()">
                <p><strong>📁 Click to Upload Custom Image</strong></p>
                <p style="font-size: 0.8rem; color: #718096; margin-top: 4px;">Supports PNG, JPG, JPEG, TIFF</p>
                <input type="file" id="fileInput" accept="image/*" onchange="uploadImage(event)">
            </div>

            <h2>Preset Benchmarks</h2>
            <button class="preset-btn" onclick="loadPreset('cafe_wall.png')">1. Café Wall (Geometric Tilt)</button>
            <button class="preset-btn" onclick="loadPreset('hermann_grid.png')">2. Hermann Grid (Brightness)</button>
            <button class="preset-btn" onclick="loadPreset('muller_lyer.png')">3. Müller-Lyer (Size Distortion)</button>
            <button class="preset-btn" onclick="loadPreset('necker_cube.png')">4. Necker Cube (3D Wireframe)</button>
            <button class="preset-btn" onclick="loadPreset('rubin_vase.png')">5. Rubin's Vase (Figure-Ground)</button>
            <button class="preset-btn" onclick="loadPreset('simultaneous_contrast.png')">6. Simultaneous Contrast</button>
            <button class="preset-btn" onclick="loadPreset('natural_object.png')">7. Natural Shaded Sphere (Object)</button>
            <button class="preset-btn" onclick="loadPreset('manipulated_splicing.png')">8. Digitally Spliced (Forgery)</button>
        </div>

        <!-- Main Results Area -->
        <div class="main-panel">
            <!-- 4 Visual Panels -->
            <div class="visual-grid">
                <div class="visual-card">
                    <h3>1. Input Stimulus</h3>
                    <img id="imgOrig" src="" alt="Input Image">
                </div>
                <div class="visual-card">
                    <h3>2. 2D Fourier Spectrum</h3>
                    <img id="imgFourier" src="" alt="Fourier Spectrum">
                </div>
                <div class="visual-card">
                    <h3>3. Error Level Analysis (ELA)</h3>
                    <img id="imgEla" src="" alt="ELA Residual">
                </div>
                <div class="visual-card">
                    <h3>4. Causal Trigger Overlay</h3>
                    <img id="imgOverlay" src="" alt="Causal Overlay">
                </div>
            </div>

            <!-- Stage 1 & 2 Diagnostic Card -->
            <div class="card">
                <h2>Hierarchical Perceptual Decisions</h2>
                <div class="badges-row">
                    <span id="badgeGate" class="badge badge-illusion">STAGE 1: Awaiting Analysis</span>
                    <span id="badgeCategory" class="badge badge-category">STAGE 2: Category Unassigned</span>
                </div>

                <!-- Stage 3 Multistability -->
                <div id="multistableSection" style="margin-top: 15px; border-top: 1px solid #E2E8F0; padding-top: 12px;">
                    <h3 style="font-size: 1rem; color: #0A2540; margin-bottom: 6px;">Stage 3: Quantum Multistability & Perceptual Entropy (Maksymov 2024)</h3>
                    <p id="entropyText" style="font-size: 0.95rem; color: #4A5568;">Status: Monostable</p>
                    <div id="probBarsContainer"></div>
                </div>
            </div>

            <!-- Stage 5 Scientific Reasoning -->
            <div class="card reasoning-box">
                <h2>Stage 5: Scientific Perceptual Reasoning</h2>
                <p><strong>Physical Ground Truth:</strong> <span id="txtPhysical">-</span></p>
                <p><strong>Perceptual Distortion:</strong> <span id="txtDistortion" style="color: #C53030;">-</span></p>
                <p><strong>Neurobiological Mechanism:</strong></p>
                <p id="txtMechanism" style="color: #2D3748; background: #F7FAFC; padding: 10px; border-radius: 4px; border-left: 3px solid #0066CC;">-</p>
            </div>

            <!-- Stage 6 Mathematical Metrics -->
            <div class="card">
                <h2>Computed Multi-Domain Mathematical Features</h2>
                <table class="metrics-table">
                    <tr><th>Metric Name</th><th>Measured Value</th><th>Physical Significance</th></tr>
                    <tr><td>Michelson Contrast</td><td id="mContrast">-</td><td>Ratio of luminance amplitude over DC baseline</td></tr>
                    <tr><td>2D Fourier Periodicity</td><td id="mPeriodicity">-</td><td>High-frequency harmonic spike ratio (Periodic grid detection)</td></tr>
                    <tr><td>Localized ELA Tamper</td><td id="mEla">-</td><td>Block-variance recompression anomaly (Forgery discrimination)</td></tr>
                    <tr><td>Bilateral Symmetry</td><td id="mSymmetry">-</td><td>Figure-ground symmetry balance across horizontal axis</td></tr>
                    <tr><td>Causal Bounding Box</td><td id="mBbox">-</td><td>Normalized [ymin, xmin, ymax, xmax] trigger coordinates</td></tr>
                </table>
            </div>
        </div>
    </div>

    <script>
        function renderAnalysis(data) {
            const g = data.stage_1_problem_gating;
            const c = data.stage_2_multi_category_classification;
            const a = data.stage_3_ambiguity_analysis;
            const l = data.stage_4_localization;
            const e = data.stage_5_explanation;
            const m = data.raw_measurements;

            // Images
            document.getElementById('imgOrig').src = data.images.original;
            document.getElementById('imgFourier').src = data.images.fourier;
            document.getElementById('imgEla').src = data.images.ela;
            document.getElementById('imgOverlay').src = data.images.overlay;

            // Badges
            const bGate = document.getElementById('badgeGate');
            bGate.className = 'badge ' + (g.is_illusion ? 'badge-illusion' : (g.is_forgery ? 'badge-forgery' : 'badge-object'));
            bGate.innerText = 'STAGE 1: ' + g.decision.toUpperCase() + ' (' + (g.confidence * 100).toFixed(1) + '%)';

            const bCat = document.getElementById('badgeCategory');
            bCat.innerText = 'STAGE 2: ' + c.category + ' (' + (c.confidence * 100).toFixed(1) + '%)';

            // Multistability
            const entText = document.getElementById('entropyText');
            const bars = document.getElementById('probBarsContainer');
            bars.innerHTML = '';
            if (a.is_multistable) {
                entText.innerHTML = '<strong>Status: Active Multistable Bistability</strong> | Perceptual Entropy: <strong>' + a.perceptual_entropy.toFixed(4) + '</strong> (Max ~ 1.0)';
                for (const [stName, prob] of Object.entries(a.state_distribution)) {
                    const pct = (prob * 100).toFixed(1);
                    bars.innerHTML += `
                        <div class="prob-bar-container">
                            <div class="prob-label"><span>${stName}</span><span>${pct}%</span></div>
                            <div class="prob-bar"><div class="prob-fill" style="width: ${pct}%;"></div></div>
                        </div>
                    `;
                }
            } else {
                entText.innerText = 'Status: Monostable (Fixed Rigid Interpretation) | Perceptual Entropy: ' + a.perceptual_entropy.toFixed(4);
            }

            // Reasoning
            document.getElementById('txtPhysical').innerText = e.physical_reality;
            document.getElementById('txtDistortion').innerText = e.perceptual_distortion;
            document.getElementById('txtMechanism').innerText = e.scientific_mechanism;

            // Metrics
            document.getElementById('mContrast').innerText = m.michelson_contrast.toFixed(4);
            document.getElementById('mPeriodicity').innerText = m.fourier_periodicity_ratio.toFixed(2);
            document.getElementById('mEla').innerText = m.ela_forgery_score.toFixed(2);
            document.getElementById('mSymmetry').innerText = m.bilateral_symmetry.toFixed(2);
            document.getElementById('mBbox').innerText = JSON.stringify(l.trigger_bounding_box_normalized);
        }

        function loadPreset(filename) {
            fetch('/api/analyze_preset?name=' + filename)
                .then(r => r.json())
                .then(data => renderAnalysis(data));
        }

        function uploadImage(e) {
            const file = e.target.files[0];
            if (!file) return;
            const reader = new FileReader();
            reader.onload = function(evt) {
                fetch('/api/analyze_upload', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ image_b64: evt.target.result })
                })
                .then(r => r.json())
                .then(data => renderAnalysis(data));
            };
            reader.readAsDataURL(file);
        }

        // Load default on startup
        window.onload = function() {
            loadPreset('hermann_grid.png');
        };
    </script>
</body>
</html>
"""

def pil_to_b64(pil_img):
    buf = io.BytesIO()
    pil_img.save(buf, format="PNG")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode("utf-8")

class PerceptionXHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/" or self.path.startswith("/index"):
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(HTML_TEMPLATE.encode("utf-8"))
            
        elif self.path.startswith("/api/analyze_preset"):
            import urllib.parse
            query = urllib.parse.urlparse(self.path).query
            params = urllib.parse.parse_qs(query)
            filename = params.get("name", ["hermann_grid.png"])[0]
            
            sample_path = os.path.join(os.path.dirname(__file__), "data", "samples", filename)
            if not os.path.exists(sample_path):
                self.send_error(404, "Preset not found")
                return
                
            img = Image.open(sample_path)
            res = PIPELINE.process_image(img)
            
            # Prepare images as base64
            fourier = PIPELINE.extractor.extract_fourier_spectrum(img)["magnitude_spectrum"]
            norm_f = (fourier - fourier.min()) / (fourier.max() - fourier.min() + 1e-6)
            fourier_pil = Image.fromarray((norm_f * 255).astype("uint8")).convert("RGB")
            
            res["images"] = {
                "original": pil_to_b64(img),
                "fourier": pil_to_b64(fourier_pil),
                "ela": pil_to_b64(res["_artifacts"]["ela_pil"]),
                "overlay": pil_to_b64(res["_artifacts"]["overlay_pil"])
            }
            del res["_artifacts"]
            
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(res).encode("utf-8"))
            
        else:
            self.send_error(404, "Not Found")

    def do_POST(self):
        if self.path == "/api/analyze_upload":
            content_length = int(self.headers.get("Content-Length", 0))
            post_data = self.rfile.read(content_length)
            req = json.loads(post_data.decode("utf-8"))
            
            # Decode b64
            b64_str = req["image_b64"].split(",")[-1]
            img_bytes = base64.b64decode(b64_str)
            img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
            
            res = PIPELINE.process_image(img)
            
            fourier = PIPELINE.extractor.extract_fourier_spectrum(img)["magnitude_spectrum"]
            norm_f = (fourier - fourier.min()) / (fourier.max() - fourier.min() + 1e-6)
            fourier_pil = Image.fromarray((norm_f * 255).astype("uint8")).convert("RGB")
            
            res["images"] = {
                "original": pil_to_b64(img),
                "fourier": pil_to_b64(fourier_pil),
                "ela": pil_to_b64(res["_artifacts"]["ela_pil"]),
                "overlay": pil_to_b64(res["_artifacts"]["overlay_pil"])
            }
            del res["_artifacts"]
            
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(res).encode("utf-8"))

def start_server():
    server = HTTPServer(("localhost", PORT), PerceptionXHandler)
    url = f"http://localhost:{PORT}"
    print(f"Perception-X Web App running at: {url}")
    try:
        webbrowser.open(url)
    except Exception:
        pass
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping Perception-X Web App.")
        server.server_close()

if __name__ == "__main__":
    start_server()
