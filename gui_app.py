"""
Perception-X Desktop Graphical User Interface (GUI)
A native Windows desktop application for interactive optical illusion analysis,
problem gating, fine-grained classification, multistability resolution, and explainable AI.
"""

import os
import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk

# Ensure local imports work
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from models.perception_x_pipeline import PerceptionXPipeline
from data.synthetic_generators import (
    generate_hermann_grid,
    generate_muller_lyer,
    generate_rubin_vase,
    generate_necker_cube,
    generate_simultaneous_contrast,
    generate_cafe_wall,
    generate_natural_object,
    generate_manipulated_splicing
)

class PerceptionXGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Perception-X: AI Optical Illusion & Image Comprehension Workbench")
        self.root.geometry("1260x860")
        self.root.minsize(1050, 750)
        
        # Set Windows application icon styling if available
        self.pipeline = PerceptionXPipeline()
        self.current_image_path = None
        self.current_image_pil = None
        self.analysis_result = None

        self._apply_theme()
        self._build_ui()
        
        # Load default sample on launch
        default_sample = os.path.join(os.path.dirname(__file__), "data", "samples", "hermann_grid.png")
        if os.path.exists(default_sample):
            self.load_image(default_sample)

    def _apply_theme(self):
        style = ttk.Style()
        style.theme_use("clam")
        
        # Palette: Professional Deep Navy & Crisp White
        self.bg_color = "#F4F6F9"
        self.card_bg = "#FFFFFF"
        self.primary = "#0A2540"
        self.accent = "#0066CC"
        self.text_dark = "#1A202C"
        self.border = "#CBD5E0"
        
        self.root.configure(bg=self.bg_color)
        
        style.configure("TFrame", background=self.bg_color)
        style.configure("Card.TFrame", background=self.card_bg, relief="groove")
        style.configure("Header.TLabel", font=("Times New Roman", 16, "bold"), foreground=self.primary, background=self.bg_color)
        style.configure("SubHeader.TLabel", font=("Times New Roman", 10, "italic"), foreground="#4A5568", background=self.bg_color)
        style.configure("CardTitle.TLabel", font=("Times New Roman", 12, "bold"), foreground=self.primary, background=self.card_bg)
        style.configure("TLabel", font=("Times New Roman", 10), background=self.card_bg, foreground=self.text_dark)
        style.configure("Bold.TLabel", font=("Times New Roman", 10, "bold"), background=self.card_bg, foreground=self.text_dark)
        
        style.configure("Primary.TButton", font=("Times New Roman", 10, "bold"), background=self.primary, foreground="#FFFFFF")
        style.map("Primary.TButton", background=[("active", self.accent)])
        
        style.configure("Action.TButton", font=("Times New Roman", 10), background="#E2E8F0")

    def _build_ui(self):
        # 1. Top Header Banner
        header_frame = tk.Frame(self.root, bg="#0A2540", height=65)
        header_frame.pack(fill="x", side="top")
        
        title_label = tk.Label(
            header_frame,
            text="PERCEPTION-X : OPTICAL ILLUSION & AMBIGUOUS IMAGE WORKBENCH",
            font=("Times New Roman", 15, "bold"),
            fg="#FFFFFF",
            bg="#0A2540"
        )
        title_label.pack(side="left", padx=20, pady=8)
        
        sub_label = tk.Label(
            header_frame,
            text="Multi-Category Classification • Bio-Inspired Multistability • Explainable Attribution",
            font=("Times New Roman", 9, "italic"),
            fg="#CBD5E0",
            bg="#0A2540"
        )
        sub_label.pack(side="left", padx=5, pady=8)

        # 2. Main Horizontal Container (Sidebar + Content)
        main_container = tk.Frame(self.root, bg=self.bg_color)
        main_container.pack(fill="both", expand=True, padx=12, pady=10)

        # Left Control Sidebar
        sidebar = tk.Frame(main_container, bg=self.card_bg, width=310, relief="solid", bd=1)
        sidebar.pack(side="left", fill="y", padx=(0, 10))
        sidebar.pack_propagate(False)
        self._build_sidebar(sidebar)

        # Right Main Workspace (Visual Panels & Analysis Cards)
        workspace = tk.Frame(main_container, bg=self.bg_color)
        workspace.pack(side="right", fill="both", expand=True)
        self._build_workspace(workspace)

    def _build_sidebar(self, parent):
        pad_x, pad_y = 12, 8
        
        # Section A: Input Selection
        lbl_sec1 = tk.Label(parent, text="IMAGE INPUT", font=("Times New Roman", 11, "bold"), fg=self.primary, bg=self.card_bg)
        lbl_sec1.pack(anchor="w", padx=pad_x, pady=(pad_y+4, 4))
        
        btn_browse = tk.Button(
            parent, text="📂 Browse Image File...", font=("Times New Roman", 10),
            bg="#EDF2F7", relief="groove", command=self.browse_file
        )
        btn_browse.pack(fill="x", padx=pad_x, pady=4)

        # Preset Sample Selector
        lbl_sample = tk.Label(parent, text="Select Preset Benchmark Stimulus:", font=("Times New Roman", 10), bg=self.card_bg)
        lbl_sample.pack(anchor="w", padx=pad_x, pady=(6, 2))
        
        self.sample_var = tk.StringVar(value="hermann_grid.png")
        self.samples_dict = {
            "Hermann Grid (Brightness Induction)": "hermann_grid.png",
            "Müller-Lyer (Geometric Size-Constancy)": "muller_lyer.png",
            "Café Wall (Border-Locking Tilt)": "cafe_wall.png",
            "Rubin's Vase (Figure-Ground Bistable)": "rubin_vase.png",
            "Necker Cube (3D Multistable Wireframe)": "necker_cube.png",
            "Simultaneous Contrast (Surround Induction)": "simultaneous_contrast.png",
            "Natural Shaded Object (Non-Illusion)": "natural_object.png",
            "Digitally Spliced Forgery (Tampered)": "manipulated_splicing.png"
        }
        
        self.combo_sample = ttk.Combobox(parent, values=list(self.samples_dict.keys()), state="readonly", font=("Times New Roman", 10))
        self.combo_sample.current(0)
        self.combo_sample.pack(fill="x", padx=pad_x, pady=3)
        self.combo_sample.bind("<<ComboboxSelected>>", self.on_sample_selected)

        ttk.Separator(parent, orient="horizontal").pack(fill="x", padx=pad_x, pady=12)

        # Section B: Generate Procedural Stimuli
        lbl_sec2 = tk.Label(parent, text="PROCEDURAL GENERATOR", font=("Times New Roman", 11, "bold"), fg=self.primary, bg=self.card_bg)
        lbl_sec2.pack(anchor="w", padx=pad_x, pady=(4, 4))

        gen_frame = tk.Frame(parent, bg=self.card_bg)
        gen_frame.pack(fill="x", padx=pad_x, pady=2)
        
        b1 = tk.Button(gen_frame, text="Generate Hermann", font=("Times New Roman", 9), bg="#F7FAFC", relief="groove",
                       command=lambda: self.set_procedural_image(generate_hermann_grid(), "hermann_grid.png"))
        b1.grid(row=0, column=0, sticky="ew", padx=2, pady=2)
        
        b2 = tk.Button(gen_frame, text="Generate Müller-Lyer", font=("Times New Roman", 9), bg="#F7FAFC", relief="groove",
                       command=lambda: self.set_procedural_image(generate_muller_lyer(), "muller_lyer.png"))
        b2.grid(row=0, column=1, sticky="ew", padx=2, pady=2)
        
        b3 = tk.Button(gen_frame, text="Generate Rubin Vase", font=("Times New Roman", 9), bg="#F7FAFC", relief="groove",
                       command=lambda: self.set_procedural_image(generate_rubin_vase(), "rubin_vase.png"))
        b3.grid(row=1, column=0, sticky="ew", padx=2, pady=2)
        
        b4 = tk.Button(gen_frame, text="Generate Necker Cube", font=("Times New Roman", 9), bg="#F7FAFC", relief="groove",
                       command=lambda: self.set_procedural_image(generate_necker_cube(), "necker_cube.png"))
        b4.grid(row=1, column=1, sticky="ew", padx=2, pady=2)
        
        b5 = tk.Button(gen_frame, text="Generate Café Wall", font=("Times New Roman", 9), bg="#F7FAFC", relief="groove",
                       command=lambda: self.set_procedural_image(generate_cafe_wall(), "cafe_wall.png"))
        b5.grid(row=2, column=0, sticky="ew", padx=2, pady=2)
        
        b6 = tk.Button(gen_frame, text="Generate Normal Object", font=("Times New Roman", 9), bg="#F7FAFC", relief="groove",
                       command=lambda: self.set_procedural_image(generate_natural_object(), "natural_object.png"))
        b6.grid(row=2, column=1, sticky="ew", padx=2, pady=2)

        gen_frame.grid_columnconfigure(0, weight=1)
        gen_frame.grid_columnconfigure(1, weight=1)

        ttk.Separator(parent, orient="horizontal").pack(fill="x", padx=pad_x, pady=12)

        # Section C: Main Action
        self.btn_run = tk.Button(
            parent, text="⚡ RUN PERCEPTION-X PIPELINE", font=("Times New Roman", 11, "bold"),
            bg="#0A2540", fg="#FFFFFF", activebackground="#0066CC", activeforeground="#FFFFFF",
            relief="raised", height=2, command=self.run_pipeline
        )
        self.btn_run.pack(fill="x", padx=pad_x, pady=10)

        # Section D: Quick Word Document Launcher
        btn_word = tk.Button(
            parent, text="📄 Open Word Report (.docx)", font=("Times New Roman", 10),
            bg="#EDF2F7", relief="groove", command=self.open_word_report
        )
        btn_word.pack(fill="x", padx=pad_x, pady=4)

        # Current File Label
        self.lbl_file_info = tk.Label(parent, text="No file loaded", font=("Times New Roman", 9, "italic"), fg="#718096", bg=self.card_bg, wraplength=270)
        self.lbl_file_info.pack(side="bottom", padx=pad_x, pady=8)

    def _build_workspace(self, parent):
        # Upper Region: 4 Image Panels (Original, Fourier, ELA, Causal Overlay)
        top_panels = tk.Frame(parent, bg=self.card_bg, relief="solid", bd=1, height=270)
        top_panels.pack(fill="x", pady=(0, 10))
        top_panels.pack_propagate(False)

        panel_w = 210
        self.lbl_orig = self._create_image_slot(top_panels, "1. Input Stimulus", 0)
        self.lbl_fourier = self._create_image_slot(top_panels, "2. 2D Fourier Spectrum", 1)
        self.lbl_ela = self._create_image_slot(top_panels, "3. Error Level Analysis (ELA)", 2)
        self.lbl_overlay = self._create_image_slot(top_panels, "4. Causal Trigger Overlay", 3)

        top_panels.grid_columnconfigure(0, weight=1)
        top_panels.grid_columnconfigure(1, weight=1)
        top_panels.grid_columnconfigure(2, weight=1)
        top_panels.grid_columnconfigure(3, weight=1)

        # Lower Region: Detailed Multi-Stage Diagnostic Cards (Scrollable)
        bottom_frame = tk.Frame(parent, bg=self.card_bg, relief="solid", bd=1)
        bottom_frame.pack(fill="both", expand=True)

        canvas = tk.Canvas(bottom_frame, bg=self.card_bg, highlightthickness=0)
        scrollbar = ttk.Scrollbar(bottom_frame, orient="vertical", command=canvas.yview)
        self.scroll_content = tk.Frame(canvas, bg=self.card_bg)

        self.scroll_content.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=self.scroll_content, anchor="nw", width=900)
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True, padx=8, pady=8)
        scrollbar.pack(side="right", fill="y", pady=8)

        self._build_diagnostic_cards(self.scroll_content)

    def _create_image_slot(self, parent, title, col):
        frame = tk.Frame(parent, bg=self.card_bg, padx=6, pady=6)
        frame.grid(row=0, column=col, sticky="nsew")
        
        lbl_title = tk.Label(frame, text=title, font=("Times New Roman", 10, "bold"), fg=self.primary, bg=self.card_bg)
        lbl_title.pack(anchor="n", pady=(0, 4))
        
        lbl_img = tk.Label(frame, bg="#E2E8F0", text="Awaiting image...", font=("Times New Roman", 9, "italic"), relief="sunken", bd=1)
        lbl_img.pack(fill="both", expand=True)
        return lbl_img

    def _build_diagnostic_cards(self, parent):
        pad_x = 12
        
        # --- Stage 1 & 2 Badges ---
        badge_frame = tk.Frame(parent, bg=self.card_bg)
        badge_frame.pack(fill="x", padx=pad_x, pady=(6, 4))

        self.badge_gate = tk.Label(
            badge_frame, text="STAGE 1 : AWAITING INGESTION",
            font=("Times New Roman", 10, "bold"), bg="#EDF2F7", fg="#2D3748",
            padx=10, pady=4, relief="ridge"
        )
        self.badge_gate.pack(side="left", padx=(0, 8))

        self.badge_category = tk.Label(
            badge_frame, text="STAGE 2 : CATEGORY UNASSIGNED",
            font=("Times New Roman", 10, "bold"), bg="#EDF2F7", fg="#2D3748",
            padx=10, pady=4, relief="ridge"
        )
        self.badge_category.pack(side="left", padx=4)

        # --- Stage 3: Multistability Box ---
        self.frame_bistable = tk.LabelFrame(
            parent, text="Stage 3: Quantum Multistability & Ambiguity Resolution (Maksymov 2024)",
            font=("Times New Roman", 11, "bold"), fg=self.primary, bg=self.card_bg, padx=10, pady=6
        )
        self.frame_bistable.pack(fill="x", padx=pad_x, pady=6)
        
        self.lbl_bistable_info = tk.Label(
            self.frame_bistable,
            text="Status: Monostable | Perceptual Entropy: 0.1500",
            font=("Times New Roman", 10), bg=self.card_bg, justify="left", anchor="w"
        )
        self.lbl_bistable_info.pack(fill="x")

        # --- Stage 4 & 5: Scientific Reasoning & Physical Reality ---
        self.frame_reasoning = tk.LabelFrame(
            parent, text="Stage 5: Scientific Perceptual Reasoning & Neurobiological Mechanism",
            font=("Times New Roman", 11, "bold"), fg=self.primary, bg=self.card_bg, padx=10, pady=6
        )
        self.frame_reasoning.pack(fill="x", padx=pad_x, pady=6)

        self.lbl_physical = tk.Label(
            self.frame_reasoning, text="Physical Reality: [Pending]",
            font=("Times New Roman", 10), fg="#2B6CB0", bg=self.card_bg, justify="left", anchor="w", wraplength=860
        )
        self.lbl_physical.pack(fill="x", pady=2)

        self.lbl_distortion = tk.Label(
            self.frame_reasoning, text="Perceptual Distortion: [Pending]",
            font=("Times New Roman", 10), fg="#C53030", bg=self.card_bg, justify="left", anchor="w", wraplength=860
        )
        self.lbl_distortion.pack(fill="x", pady=2)

        self.lbl_mechanism = tk.Label(
            self.frame_reasoning, text="Neurobiology: [Pending]",
            font=("Times New Roman", 10), fg="#2D3748", bg=self.card_bg, justify="left", anchor="w", wraplength=860
        )
        self.lbl_mechanism.pack(fill="x", pady=2)

        # --- Stage 6: Computed Multi-Domain Features ---
        self.frame_features = tk.LabelFrame(
            parent, text="Computed Multi-Domain Mathematical Features",
            font=("Times New Roman", 11, "bold"), fg=self.primary, bg=self.card_bg, padx=10, pady=6
        )
        self.frame_features.pack(fill="x", padx=pad_x, pady=(6, 12))

        self.lbl_metrics = tk.Label(
            self.frame_features,
            text="Michelson Contrast: - | Fourier Periodicity: - | Localized ELA Tamper: - | Symmetry: -",
            font=("Times New Roman", 10), bg=self.card_bg, justify="left", anchor="w"
        )
        self.lbl_metrics.pack(fill="x")

    def browse_file(self):
        file_path = filedialog.askopenfilename(
            title="Select an Image to Analyze",
            filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.tiff")]
        )
        if file_path:
            self.load_image(file_path)

    def on_sample_selected(self, event):
        selected_name = self.combo_sample.get()
        filename = self.samples_dict.get(selected_name)
        if filename:
            path = os.path.join(os.path.dirname(__file__), "data", "samples", filename)
            if os.path.exists(path):
                self.load_image(path)

    def set_procedural_image(self, img_pil, name):
        self.current_image_pil = img_pil
        self.current_image_path = name
        self.lbl_file_info.config(text=f"Loaded Procedural: {name}")
        self._display_slot_image(self.lbl_orig, img_pil)
        self.run_pipeline()

    def load_image(self, path):
        try:
            self.current_image_path = path
            self.current_image_pil = Image.open(path)
            self.lbl_file_info.config(text=f"File: {os.path.basename(path)}")
            self._display_slot_image(self.lbl_orig, self.current_image_pil)
            self.run_pipeline()
        except Exception as e:
            messagebox.showerror("Error Loading Image", str(e))

    def _display_slot_image(self, label, pil_img, max_size=(190, 190)):
        if pil_img is None:
            return
        img_copy = pil_img.copy()
        img_copy.thumbnail(max_size, Image.Resampling.LANCZOS)
        tk_img = ImageTk.PhotoImage(img_copy)
        label.configure(image=tk_img, text="")
        label.image = tk_img # keep reference

    def run_pipeline(self):
        if self.current_image_pil is None:
            messagebox.showwarning("No Image", "Please load an image or pick a preset first.")
            return

        # Execute Perception-X pipeline
        res = self.pipeline.process_image(self.current_image_pil)
        self.analysis_result = res
        
        gating = res["stage_1_problem_gating"]
        category = res["stage_2_multi_category_classification"]
        ambiguity = res["stage_3_ambiguity_analysis"]
        loc = res["stage_4_localization"]
        expl = res["stage_5_explanation"]
        raw = res["raw_measurements"]
        artifacts = res["_artifacts"]

        # 1. Update visual slots
        # Panel 2: Fourier spectrum (as PIL image from magma colormap)
        fourier_data = self.pipeline.extractor.extract_fourier_spectrum(self.current_image_pil)["magnitude_spectrum"]
        norm_fourier = (fourier_data - fourier_data.min()) / (fourier_data.max() - fourier_data.min() + 1e-6)
        fourier_pil = Image.fromarray((norm_fourier * 255).astype("uint8")).convert("RGB")
        self._display_slot_image(self.lbl_fourier, fourier_pil)

        # Panel 3: ELA image
        self._display_slot_image(self.lbl_ela, artifacts["ela_pil"])

        # Panel 4: Causal heatmap overlay
        self._display_slot_image(self.lbl_overlay, artifacts["overlay_pil"])

        # 2. Update Stage 1 Gating Badge
        if gating["is_illusion"]:
            bg_g, fg_g = "#C6F6D5", "#22543D" # Soft green
            icon = "👁️"
        elif gating["is_forgery"]:
            bg_g, fg_g = "#FED7D7", "#742A2A" # Soft red
            icon = "🚨"
        else:
            bg_g, fg_g = "#EBF8FF", "#2B6CB0" # Soft blue
            icon = "📦"
        self.badge_gate.config(
            text=f"{icon} STAGE 1 : {gating['decision'].upper()} (Confidence: {gating['confidence']:.1%})",
            bg=bg_g, fg=fg_g
        )

        # 3. Update Stage 2 Category Badge
        self.badge_category.config(
            text=f"STAGE 2 : {category['category']} (Confidence: {category['confidence']:.1%})",
            bg="#EDF2F7", fg="#2D3748"
        )

        # 4. Update Stage 3 Multistability
        if ambiguity["is_multistable"]:
            states_text = " | ".join([f"{k}: {v:.1%}" for k, v in ambiguity["state_distribution"].items()])
            bistable_str = (
                f"Status: Active Multistable Bistability (Active Perceptual Switching)\n"
                f"Perceptual Entropy (H): {ambiguity['perceptual_entropy']:.4f} (Max theoretical ambiguity ~ 1.0)\n"
                f"Dual-State Probabilities: {states_text}"
            )
            self.lbl_bistable_info.config(text=bistable_str, fg="#744210")
            self.frame_bistable.config(fg="#B7791F")
        else:
            self.lbl_bistable_info.config(
                text=f"Status: Monostable (Fixed Rigid Interpretation) | Perceptual Entropy: {ambiguity['perceptual_entropy']:.4f}",
                fg="#4A5568"
            )
            self.frame_bistable.config(fg=self.primary)

        # 5. Update Stage 5 Reasoning
        self.lbl_physical.config(text=f"Physical Ground Truth: {expl['physical_reality']}")
        self.lbl_distortion.config(text=f"Perceived Distortion:   {expl['perceptual_distortion']}")
        self.lbl_mechanism.config(text=f"Neurobiological Mechanism:\n{expl['scientific_mechanism']}")

        # 6. Update Computed Features
        metrics_str = (
            f"• Michelson Contrast: {raw['michelson_contrast']:.3f}   |   "
            f"• 2D Fourier Periodicity Ratio: {raw['fourier_periodicity_ratio']:.2f}   |   "
            f"• Localized ELA Tamper: {raw['ela_forgery_score']:.2f}   |   "
            f"• Bilateral Symmetry: {raw['bilateral_symmetry']:.2f}   |   "
            f"• Trigger BBox: {loc['trigger_bounding_box_normalized']}"
        )
        self.lbl_metrics.config(text=metrics_str)

    def open_word_report(self):
        paths_to_check = [
            os.path.expanduser("~") + "/Downloads/Perception_X_Research_Analysis_Report.docx",
            os.path.expanduser("~") + "/Desktop/Perception_X_Research_Analysis_Report.docx",
            os.path.join(os.path.dirname(__file__), "Perception_X_Research_Analysis_Report.docx")
        ]
        for p in paths_to_check:
            if os.path.exists(p):
                try:
                    os.startfile(p)
                    return
                except Exception as e:
                    messagebox.showinfo("Report Path", f"Report is located at:\n{p}")
                    return
        messagebox.showwarning("File Not Found", "Word report has not been generated yet.")

def main():
    root = tk.Tk()
    app = PerceptionXGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
