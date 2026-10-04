import React, { useState, useEffect } from 'react';

const PRESETS = [
  { id: 'cafe_wall.png', name: 'Café Wall Illusion', category: 'Geometric & Distortion', icon: '📐' },
  { id: 'hermann_grid.png', name: 'Hermann Grid Illusion', category: 'Brightness & Contrast', icon: '▦' },
  { id: 'muller_lyer.png', name: 'Müller-Lyer Illusion', category: 'Geometric Distortion', icon: '⇄' },
  { id: 'necker_cube.png', name: 'Necker Cube Wireframe', category: 'Ambiguous & Multistable', icon: '🧊' },
  { id: 'rubin_vase.png', name: "Rubin's Vase Silhouette", category: 'Ambiguous & Multistable', icon: '👥' },
  { id: 'simultaneous_contrast.png', name: 'Simultaneous Contrast', category: 'Brightness Induction', icon: '🌓' },
  { id: 'natural_object.png', name: 'Shaded Sphere (Object)', category: 'Non-Illusory Physical', icon: '⚪' },
  { id: 'manipulated_splicing.png', name: 'Digitally Spliced Image', category: 'Digital Forgery', icon: '✂️' }
];

export default function App() {
  const [selectedPreset, setSelectedPreset] = useState('hermann_grid.png');
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);

  const fetchAnalysis = async (presetName) => {
    setLoading(true);
    try {
      const res = await fetch(`/api/analyze/${presetName}`);
      const data = await res.json();
      setAnalysis(data);
    } catch (err) {
      console.error('Failed to fetch analysis:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleFileUpload = (e) => {
    const file = e.target.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = async (evt) => {
      setLoading(true);
      try {
        const res = await fetch('/api/analyze', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ image_b64: evt.target.result, name: file.name })
        });
        const data = await res.json();
        setAnalysis(data);
        setSelectedPreset(null);
      } catch (err) {
        console.error('Upload failed:', err);
      } finally {
        setLoading(false);
      }
    };
    reader.readAsDataURL(file);
  };

  useEffect(() => {
    fetchAnalysis('hermann_grid.png');
  }, []);

  return (
    <div className="min-h-screen flex flex-col font-serif bg-slate-50 text-slate-800">
      <header className="bg-[#0A2540] text-white shadow-md px-6 py-4 flex flex-wrap items-center justify-between">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 rounded bg-blue-600 flex items-center justify-center font-bold text-xl text-white">Ψ</div>
          <div>
            <h1 className="text-xl font-bold tracking-wider">PERCEPTION-X : REACT WORKBENCH</h1>
            <p className="text-xs text-slate-300 italic">Multi-Category AI Optical Illusion Classifier & Explainability Engine</p>
          </div>
        </div>
      </header>

      <div className="flex-1 max-w-7xl w-full mx-auto p-4 sm:p-6 grid grid-cols-1 lg:grid-cols-12 gap-6">
        <aside className="lg:col-span-3 space-y-6">
          <div className="bg-white rounded-lg border border-slate-200 p-4 shadow-sm">
            <h2 className="text-sm font-bold text-[#0A2540] uppercase tracking-wider mb-3">Upload Custom Image</h2>
            <label className="flex flex-col items-center justify-center border-2 border-dashed border-slate-300 rounded-lg p-5 cursor-pointer hover:bg-slate-50 hover:border-blue-500 transition group text-center">
              <span className="text-2xl mb-1 group-hover:scale-110 transition">📁</span>
              <span className="text-sm font-semibold text-slate-700">Click or Drag Image Here</span>
              <span className="text-xs text-slate-400 mt-1 font-sans">PNG, JPG, JPEG, TIFF</span>
              <input type="file" className="hidden" accept="image/*" onChange={handleFileUpload} />
            </label>
          </div>

          <div className="bg-white rounded-lg border border-slate-200 p-4 shadow-sm">
            <h2 className="text-sm font-bold text-[#0A2540] uppercase tracking-wider mb-3">Preset Benchmarks</h2>
            <div className="space-y-1.5">
              {PRESETS.map((p) => (
                <button
                  key={p.id}
                  onClick={() => {
                    setSelectedPreset(p.id);
                    fetchAnalysis(p.id);
                  }}
                  className={`w-full text-left px-3 py-2 rounded text-sm transition flex items-center justify-between ${
                    selectedPreset === p.id 
                      ? 'bg-blue-50 border border-blue-300 text-blue-900 font-bold' 
                      : 'hover:bg-slate-100 text-slate-700 border border-transparent'
                  }`}
                >
                  <span className="flex items-center gap-2">
                    <span>{p.icon}</span>
                    <span>{p.name}</span>
                  </span>
                  <span className="text-[10px] font-sans text-slate-400">{p.category.split(' ')[0]}</span>
                </button>
              ))}
            </div>
          </div>
        </aside>

        <main className="lg:col-span-9 space-y-6">
          {loading ? (
            <div className="bg-white rounded-lg border border-slate-200 p-12 text-center shadow-sm">
              <div className="inline-block w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full animate-spin mb-3"></div>
              <p className="text-base font-semibold text-slate-600">Processing Perception-X Pipeline...</p>
            </div>
          ) : analysis ? (
            <>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                <div className="bg-white rounded border border-slate-200 p-2 text-center shadow-sm">
                  <div className="text-xs font-bold text-slate-600 mb-1.5">1. Input Stimulus</div>
                  <img src={analysis.images.original} className="w-full h-36 object-contain bg-slate-100 rounded border border-slate-200" alt="Original" />
                </div>
                <div className="bg-white rounded border border-slate-200 p-2 text-center shadow-sm">
                  <div className="text-xs font-bold text-slate-600 mb-1.5">2. 2D Fourier Spectrum</div>
                  <img src={analysis.images.fourier} className="w-full h-36 object-contain bg-slate-100 rounded border border-slate-200" alt="Fourier" />
                </div>
                <div className="bg-white rounded border border-slate-200 p-2 text-center shadow-sm">
                  <div className="text-xs font-bold text-slate-600 mb-1.5">3. Error Level Analysis (ELA)</div>
                  <img src={analysis.images.ela} className="w-full h-36 object-contain bg-slate-100 rounded border border-slate-200" alt="ELA" />
                </div>
                <div className="bg-white rounded border border-slate-200 p-2 text-center shadow-sm">
                  <div className="text-xs font-bold text-slate-600 mb-1.5">4. Causal Trigger Overlay</div>
                  <img src={analysis.images.overlay} className="w-full h-36 object-contain bg-slate-100 rounded border border-slate-200" alt="Overlay" />
                </div>
              </div>

              <div className="bg-white rounded-lg border border-slate-200 p-5 shadow-sm space-y-4">
                <div className="flex flex-wrap items-center gap-3">
                  <div className={`px-4 py-2 rounded font-bold text-sm border flex items-center gap-2 ${
                    analysis.stage_1_problem_gating.is_illusion 
                      ? 'bg-emerald-50 text-emerald-800 border-emerald-300'
                      : analysis.stage_1_problem_gating.is_forgery
                        ? 'bg-rose-50 text-rose-800 border-rose-300'
                        : 'bg-blue-50 text-blue-800 border-blue-300'
                  }`}>
                    <span>{analysis.stage_1_problem_gating.is_illusion ? '👁️' : (analysis.stage_1_problem_gating.is_forgery ? '🚨' : '📦')}</span>
                    <span>STAGE 1: {analysis.stage_1_problem_gating.decision.toUpperCase()} ({(analysis.stage_1_problem_gating.confidence * 100).toFixed(1)}%)</span>
                  </div>

                  <div className="px-4 py-2 rounded font-bold text-sm bg-slate-100 text-slate-800 border border-slate-300">
                    STAGE 2: {analysis.stage_2_multi_category_classification.category} ({(analysis.stage_2_multi_category_classification.confidence * 100).toFixed(1)}%)
                  </div>
                </div>
              </div>
            </>
          ) : null}
        </main>
      </div>
    </div>
  );
}
