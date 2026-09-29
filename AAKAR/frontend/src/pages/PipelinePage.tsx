import React, { useState } from 'react';
import { Cpu, Play, CheckCircle2, Terminal, Clock, RefreshCw, X } from 'lucide-react';
import { api } from '../api/client';

export const PipelinePage: React.FC = () => {
  const [isRunning, setIsRunning] = useState(false);
  const [progress, setProgress] = useState(100);
  const [stage, setStage] = useState('Pipeline idle / completed');
  const [showRunModal, setShowRunModal] = useState(false);
  const [autoScroll, setAutoScroll] = useState(true);

  // Form params
  const [projectName, setProjectName] = useState('Pune_Sector_4_Drone_Survey');
  const [tileSize, setTileSize] = useState(512);
  const [overlapPct, setOverlapPct] = useState(20);
  const [confidenceThreshold, setConfidenceThreshold] = useState(0.5);

  const [logs, setLogs] = useState<string[]>([
    '2026-09-29T10:00:01Z [INFO] Layer 1: Ingestion completed. GeoTIFF orthomosaic verified (EPSG:4326).',
    '2026-09-29T10:00:03Z [INFO] Layer 2: Preprocessing. 64 tiles extracted with 20% overlap. nDSM computed from DSM-DTM.',
    '2026-09-29T10:00:15Z [INFO] Layer 3: AI Inference batch complete. PyTorch U-Net & YOLOv8 extracted 4 structures, 9 boundaries.',
    '2026-09-29T10:00:22Z [INFO] Layer 4: GeoAI polygonization, Douglas-Peucker simplification, right-angle regularization applied.',
    '2026-09-29T10:00:28Z [INFO] Automated Topology Engine validated 9 parcels. 9 topology items classified.',
    '2026-09-29T10:00:32Z [INFO] Encroachment detection evaluated against existing GIS boundary layer.',
    '2026-09-29T10:00:35Z [INFO] Confidence & Dispute risk scores calculated. All layers published to Web-GIS.',
  ]);

  const handleStartPipeline = async () => {
    setShowRunModal(false);
    setIsRunning(true);
    setProgress(15);
    setStage('Layer 2: Preprocessing drone orthomosaic & computing nDSM...');
    setLogs((prev) => [
      ...prev,
      `--- Started new pipeline run for ${projectName} (Tile: ${tileSize}px, Overlap: ${overlapPct}%) ---`,
      `[INFO] Tiling raster into ${tileSize}x${tileSize} batches...`,
    ]);

    setTimeout(() => {
      setProgress(50);
      setStage('Layer 3: AI Inference (PyTorch U-Net + YOLOv8 footprint scan)...');
      setLogs((prev) => [...prev, '[INFO] Model forward pass complete. 9 boundary candidates identified.']);
    }, 1500);

    setTimeout(() => {
      setProgress(85);
      setStage('Layer 4: GeoAI polygonization, 9-error topology validation & encroachment checks...');
      setLogs((prev) => [...prev, '[INFO] Polygonizing contours and running 9 topology constraint checks...']);
    }, 3000);

    setTimeout(() => {
      setProgress(100);
      setIsRunning(false);
      setStage('Completed successfully. 9 preliminary parcels generated.');
      setLogs((prev) => [...prev, '[SUCCESS] Pipeline run finished. Layers ready in Web-GIS viewer.']);
    }, 4500);
  };

  return (
    <div className="p-8 space-y-6 max-w-[1440px] mx-auto">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-2 border-b border-border-ui">
        <div>
          <span className="text-xs font-bold text-accent uppercase tracking-wider">
            Layer 3 & 4 Orchestration
          </span>
          <h2 className="text-2xl font-bold text-text-primary tracking-tight mt-0.5">
            Cadastral AI Pipeline Control Center
          </h2>
          <p className="text-sm text-text-secondary">
            Execute batch semantic segmentation, footprint regularisation, and automated topology validation
          </p>
        </div>

        <button
          onClick={() => setShowRunModal(true)}
          disabled={isRunning}
          className={`aakar-btn-primary flex items-center gap-2 text-xs py-2.5 px-4 ${
            isRunning ? 'opacity-50 cursor-not-allowed' : ''
          }`}
        >
          <Play className="w-4 h-4 fill-white" />
          <span>{isRunning ? 'Pipeline Running...' : 'Run AI Pipeline'}</span>
        </button>
      </div>

      {/* Active Pipeline Status Card */}
      <div className="aakar-card p-6 space-y-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className={`w-3 h-3 rounded-full ${isRunning ? 'bg-accent animate-ping' : 'bg-success'}`} />
            <div>
              <h3 className="font-semibold text-sm text-text-primary">
                {isRunning ? 'Processing Active Job: job-pune-sec4' : 'Active Pipeline Status: Ready'}
              </h3>
              <p className="text-xs text-text-secondary mt-0.5">{stage}</p>
            </div>
          </div>
          <span className="font-mono text-sm font-bold text-accent">{progress}%</span>
        </div>

        <div className="w-full bg-bg-subtle h-2.5 rounded-full overflow-hidden">
          <div
            className="h-full bg-accent transition-all duration-300 rounded-full"
            style={{ width: `${progress}%` }}
          />
        </div>
      </div>

      {/* Grid: Past Runs & Log Viewer */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Past Runs Table */}
        <div className="aakar-card overflow-hidden h-fit">
          <div className="p-4 border-b border-border-ui bg-bg-secondary flex items-center justify-between">
            <h3 className="font-semibold text-xs text-text-primary uppercase tracking-wider">
              Execution History
            </h3>
            <span className="text-xs text-text-muted">Last 5 runs</span>
          </div>

          <table className="w-full text-left border-collapse text-xs">
            <thead>
              <tr className="border-b border-border-ui bg-bg-subtle text-text-secondary font-semibold">
                <th className="py-2.5 px-4">Run Date</th>
                <th className="py-2.5 px-4">Area Covered</th>
                <th className="py-2.5 px-4">Duration</th>
                <th className="py-2.5 px-4">Parcels Generated</th>
                <th className="py-2.5 px-4">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-border-ui">
              <tr className="hover:bg-bg-subtle/50">
                <td className="py-2.5 px-4 font-mono">2026-09-29 10:00</td>
                <td className="py-2.5 px-4">12.8 ha</td>
                <td className="py-2.5 px-4 font-mono">35s</td>
                <td className="py-2.5 px-4 font-bold text-text-primary">9</td>
                <td className="py-2.5 px-4">
                  <span className="aakar-badge bg-emerald-50 text-success">Completed</span>
                </td>
              </tr>
              <tr className="hover:bg-bg-subtle/50">
                <td className="py-2.5 px-4 font-mono">2026-09-28 16:30</td>
                <td className="py-2.5 px-4">8.2 ha</td>
                <td className="py-2.5 px-4 font-mono">24s</td>
                <td className="py-2.5 px-4 font-bold text-text-primary">6</td>
                <td className="py-2.5 px-4">
                  <span className="aakar-badge bg-emerald-50 text-success">Completed</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        {/* Live Monospace Log Viewer */}
        <div className="aakar-card p-4 space-y-3 flex flex-col h-[380px]">
          <div className="flex items-center justify-between pb-2 border-b border-border-ui">
            <div className="flex items-center gap-2 text-xs font-semibold text-text-primary">
              <Terminal className="w-4 h-4 text-accent" />
              <span>Pipeline Daemon Logs</span>
            </div>
            <label className="flex items-center gap-1.5 text-[11px] text-text-secondary cursor-pointer">
              <input
                type="checkbox"
                checked={autoScroll}
                onChange={(e) => setAutoScroll(e.target.checked)}
                className="rounded accent-accent"
              />
              <span>Auto-scroll</span>
            </label>
          </div>

          <div className="flex-1 bg-text-primary rounded-xl p-3 font-mono text-[11px] text-emerald-400 overflow-y-auto space-y-1">
            {logs.map((line, idx) => (
              <p key={idx} className="leading-relaxed">
                {line}
              </p>
            ))}
          </div>
        </div>
      </div>

      {/* Run AI Pipeline Modal */}
      {showRunModal && (
        <div className="fixed inset-0 bg-text-primary/60 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-bg-primary rounded-2xl max-w-md w-full p-6 shadow-2xl border border-border-ui space-y-4">
            <div className="flex items-center justify-between pb-3 border-b border-border-ui">
              <div className="flex items-center gap-2">
                <Cpu className="w-5 h-5 text-accent" />
                <h3 className="font-bold text-text-primary text-base">Configure AI Pipeline Run</h3>
              </div>
              <button onClick={() => setShowRunModal(false)} className="text-text-muted hover:text-text-primary">
                <X className="w-4 h-4" />
              </button>
            </div>

            <div className="space-y-3 text-xs">
              <div>
                <label className="text-text-secondary font-medium block mb-1">Project Name</label>
                <input
                  type="text"
                  value={projectName}
                  onChange={(e) => setProjectName(e.target.value)}
                  className="w-full p-2.5 border border-border-ui rounded-lg focus:outline-none focus:border-accent"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="text-text-secondary font-medium block mb-1">Tile Size (px)</label>
                  <select
                    value={tileSize}
                    onChange={(e) => setTileSize(Number(e.target.value))}
                    className="w-full p-2.5 border border-border-ui rounded-lg bg-bg-secondary"
                  >
                    <option value={256}>256 × 256</option>
                    <option value={512}>512 × 512 (Recommended)</option>
                    <option value={1024}>1024 × 1024</option>
                  </select>
                </div>

                <div>
                  <label className="text-text-secondary font-medium block mb-1">Tile Overlap (%)</label>
                  <select
                    value={overlapPct}
                    onChange={(e) => setOverlapPct(Number(e.target.value))}
                    className="w-full p-2.5 border border-border-ui rounded-lg bg-bg-secondary"
                  >
                    <option value={10}>10%</option>
                    <option value={20}>20% (Default)</option>
                    <option value={30}>30%</option>
                  </select>
                </div>
              </div>

              <div>
                <label className="text-text-secondary font-medium block mb-1">
                  Confidence Threshold Filter: {confidenceThreshold}
                </label>
                <input
                  type="range"
                  min="0.3"
                  max="0.8"
                  step="0.05"
                  value={confidenceThreshold}
                  onChange={(e) => setConfidenceThreshold(Number(e.target.value))}
                  className="w-full accent-accent"
                />
              </div>
            </div>

            <div className="flex justify-end gap-2 pt-3 border-t border-border-ui">
              <button onClick={() => setShowRunModal(false)} className="aakar-btn-secondary text-xs">
                Cancel
              </button>
              <button onClick={handleStartPipeline} className="aakar-btn-primary text-xs">
                Start Execution
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
