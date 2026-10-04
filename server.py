"""
Flask Backend Server for Perception-X React Frontend
Provides REST API endpoints for image analysis, preset loading, and report launching.
"""

import os
import sys
import io
import json
import base64
import webbrowser

from flask import Flask, jsonify, request, send_from_directory
from PIL import Image
import numpy as np

# Ensure local imports work
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from models.perception_x_pipeline import PerceptionXPipeline

app = Flask(__name__, static_folder="react-frontend")
pipeline = PerceptionXPipeline()

def pil_to_base64(pil_img):
    buf = io.BytesIO()
    pil_img.save(buf, format="PNG")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode("utf-8")

@app.route("/")
def index():
    return send_from_directory("react-frontend", "index.html")

@app.route("/api/presets", methods=["GET"])
def get_presets():
    samples_dir = os.path.join(os.path.dirname(__file__), "data", "samples")
    files = [f for f in os.listdir(samples_dir) if f.endswith(".png")]
    return jsonify({"presets": sorted(files)})

@app.route("/api/analyze/<filename>", methods=["GET"])
def analyze_preset(filename):
    sample_path = os.path.join(os.path.dirname(__file__), "data", "samples", filename)
    if not os.path.exists(sample_path):
        return jsonify({"error": "Preset not found"}), 404

    img = Image.open(sample_path)
    res = pipeline.process_image(img)

    # 2D Fourier representation
    fourier_data = pipeline.extractor.extract_fourier_spectrum(img)["magnitude_spectrum"]
    norm_f = (fourier_data - fourier_data.min()) / (fourier_data.max() - fourier_data.min() + 1e-6)
    fourier_pil = Image.fromarray((norm_f * 255).astype("uint8")).convert("RGB")

    artifacts = res.pop("_artifacts")
    res["images"] = {
        "original": pil_to_base64(img),
        "fourier": pil_to_base64(fourier_pil),
        "ela": pil_to_base64(artifacts["ela_pil"]),
        "overlay": pil_to_base64(artifacts["overlay_pil"])
    }
    return jsonify(res)

@app.route("/api/analyze", methods=["POST"])
def analyze_upload():
    data = request.get_json()
    if not data or "image_b64" not in data:
        return jsonify({"error": "No image data provided"}), 400

    b64_str = data["image_b64"].split(",")[-1]
    img_bytes = base64.b64decode(b64_str)
    img = Image.open(io.BytesIO(img_bytes)).convert("RGB")

    name = data.get("name", "uploaded_image")
    res = pipeline.process_image(img)

    fourier_data = pipeline.extractor.extract_fourier_spectrum(img)["magnitude_spectrum"]
    norm_f = (fourier_data - fourier_data.min()) / (fourier_data.max() - fourier_data.min() + 1e-6)
    fourier_pil = Image.fromarray((norm_f * 255).astype("uint8")).convert("RGB")

    artifacts = res.pop("_artifacts")
    res["images"] = {
        "original": pil_to_base64(img),
        "fourier": pil_to_base64(fourier_pil),
        "ela": pil_to_base64(artifacts["ela_pil"]),
        "overlay": pil_to_base64(artifacts["overlay_pil"])
    }
    return jsonify(res)

@app.route("/api/open-docx", methods=["GET"])
def open_docx():
    paths = [
        os.path.expanduser("~") + "/Downloads/Perception_X_Research_Analysis_Report.docx",
        os.path.expanduser("~") + "/Desktop/Perception_X_Research_Analysis_Report.docx",
        os.path.join(os.path.dirname(__file__), "Perception_X_Research_Analysis_Report.docx")
    ]
    for p in paths:
        if os.path.exists(p):
            try:
                os.startfile(p)
                return jsonify({"status": "opened", "path": p})
            except Exception as e:
                return jsonify({"status": "error", "message": str(e)}), 500
    return jsonify({"error": "Report not found"}), 404

def run_server():
    port = 5000
    url = f"http://localhost:{port}"
    print(f"\n=======================================================")
    print(f"  PERCEPTION-X REACT APPLICATION RUNNING")
    print(f"  Frontend URL: {url}")
    print(f"=======================================================\n")
    try:
        webbrowser.open(url)
    except Exception:
        pass
    app.run(host="0.0.0.0", port=port, debug=False)

if __name__ == "__main__":
    run_server()
