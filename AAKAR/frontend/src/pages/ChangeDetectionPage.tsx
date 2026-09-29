import React, { useState } from 'react';
import { History, Play, Download, CheckCircle, ArrowRight } from 'lucide-react';
import { api } from '../api/client';

export const ChangeDetectionPage: React.FC = () => {
  const [epochBefore, setEpochBefore] = useState('2024-Q1');
  const [epochAfter, setEpochAfter] = useState('2026-Q1');
  const [isProcessing, setIsProcessing] = useState(false);

  const [summary, setSummary] = useState({
    NewParcel: 1,
    Deleted: 0,
    BoundaryChanged: 1,
    LandUseChanged: 1,
    BuildingAdded: 1,
    BuildingDemolished: 0,
    total_changes: 4,
  });

  const records = [
    {
      id: 'chg-001',
      type: 'BuildingAdded',
      parcel_id: 'p-wagholi-001',
      before: '2024-03-15',
      after: '2026-09-29',
      details: 'New 2-story structure (height: 6.8m, area: 180m²) detected',
      color: 'bg-emerald-50 text-success',
    },
    {
      id: 'chg-002',
      type: 'LandUseChanged',
      parcel_id: 'p-wagholi-002',
      before: '2024-03-15',
      after: '2026-09-29',
      details: 'Zone transitioned from Open Agricultural to Commercial Plot',
      color: 'bg-amber-50 text-warning',
    },
    {
      id: 'chg-003',
      type: 'BoundaryChanged',
      parcel_id: 'p-wagholi-003',
      before: '2024-03-15',
      after: '2026-09-29',
      details: 'Northern fence shifted northwards (+42.5 m² area expansion)',
      color: 'bg-blue-50 text-accent',
    },
    {
      id: 'chg-004',
      type: 'NewParcel',
      parcel_id: 'p-wagholi-006',
      before: '2024-03-15',
      after: '2026-09-29',
      details: 'Subdivided new cadastral lot carved from former commons',
      color: 'bg-purple-50 text-purple-600',
    },
  ];

  const handleRun = async () => {
    setIsProcessing(true);
    setTimeout(() => {
      setIsProcessing(false);
    }, 1200);
  };

  const handleDownload = () => {
    window.open('/api/v1/changedetection/report/job-pune-sec4-latest/download', '_blank');
  };

  return (
    <div className="p-8 space-y-6 max-w-[1440px] mx-auto">
      {/* Header */}
      <div className="pb-2 border-b border-border-ui">
        <span className="text-xs font-bold text-accent uppercase tracking-wider">
          Temporal GeoAI Analysis
        </span>
        <h2 className="text-2xl font-bold text-text-primary tracking-tight mt-0.5">
          Cadastral Change Detection Between Epochs
        </h2>
        <p className="text-sm text-text-secondary">
          Compare aerial survey baselines to track unauthorized constructions, subdivisions, and land use shifts
        </p>
      </div>

      {/* Epoch Selectors Bar */}
      <div className="aakar-card p-4 flex flex-wrap items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-2">
            <span className="text-xs text-text-secondary font-medium">Baseline Epoch:</span>
            <select
              value={epochBefore}
              onChange={(e) => setEpochBefore(e.target.value)}
              className="text-xs p-2 bg-bg-secondary border border-border-ui rounded-lg font-semibold"
            >
              <option value="2024-Q1">Epoch 2024-Q1 (SVAMITVA Baseline)</option>
              <option value="2025-Q1">Epoch 2025-Q1 (Drone Survey 1)</option>
            </select>
          </div>

          <ArrowRight className="w-4 h-4 text-text-muted" />

          <div className="flex items-center gap-2">
            <span className="text-xs text-text-secondary font-medium">Current Epoch:</span>
            <select
              value={epochAfter}
              onChange={(e) => setEpochAfter(e.target.value)}
              className="text-xs p-2 bg-bg-secondary border border-border-ui rounded-lg font-semibold"
            >
              <option value="2026-Q1">Epoch 2026-Q1 (AAKAR Re-Survey)</option>
            </select>
          </div>
        </div>

        <div className="flex gap-2">
          <button
            onClick={handleRun}
            disabled={isProcessing}
            className="aakar-btn-primary text-xs flex items-center gap-1.5"
          >
            <Play className="w-3.5 h-3.5 fill-white" />
            <span>{isProcessing ? 'Analyzing Epochs...' : 'Run Change Detection'}</span>
          </button>
          <button
            onClick={handleDownload}
            className="aakar-btn-secondary text-xs flex items-center gap-1.5"
          >
            <Download className="w-3.5 h-3.5 text-accent" />
            <span>Download Report</span>
          </button>
        </div>
      </div>

      {/* 6 Metric Mini Cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {[
          { label: 'New Parcels', count: summary.NewParcel, color: 'text-purple-600', bg: 'bg-purple-50' },
          { label: 'Boundary Shifts', count: summary.BoundaryChanged, color: 'text-accent', bg: 'bg-blue-50' },
          { label: 'Land Use Shifts', count: summary.LandUseChanged, color: 'text-warning', bg: 'bg-amber-50' },
          { label: 'Buildings Added', count: summary.BuildingAdded, color: 'text-success', bg: 'bg-emerald-50' },
          { label: 'Demolitions', count: summary.BuildingDemolished, color: 'text-text-muted', bg: 'bg-gray-100' },
          { label: 'Retired Parcels', count: summary.Deleted, color: 'text-danger', bg: 'bg-rose-50' },
        ].map((item, idx) => (
          <div key={idx} className={`aakar-card p-3.5 ${item.bg}`}>
            <span className="text-[11px] text-text-secondary font-medium block">{item.label}</span>
            <span className={`text-xl font-bold ${item.color} mt-0.5 block`}>{item.count}</span>
          </div>
        ))}
      </div>

      {/* Records Table */}
      <div className="aakar-card overflow-hidden">
        <div className="p-4 border-b border-border-ui bg-bg-secondary flex justify-between items-center">
          <h3 className="font-semibold text-xs text-text-primary uppercase tracking-wider">
            Detected Cadastral Change Log
          </h3>
          <span className="text-xs text-text-muted">{records.length} records</span>
        </div>

        <table className="w-full text-left border-collapse text-xs">
          <thead>
            <tr className="border-b border-border-ui bg-bg-subtle text-text-secondary font-semibold">
              <th className="py-3 px-4">Change Type</th>
              <th className="py-3 px-4">Parcel ID</th>
              <th className="py-3 px-4">Epoch Before</th>
              <th className="py-3 px-4">Epoch After</th>
              <th className="py-3 px-4">Analysis Findings</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-border-ui">
            {records.map((r) => (
              <tr key={r.id} className="hover:bg-bg-subtle/50 transition-colors">
                <td className="py-3 px-4">
                  <span className={`aakar-badge ${r.color}`}>{r.type}</span>
                </td>
                <td className="py-3 px-4 font-mono font-medium text-text-primary">{r.parcel_id}</td>
                <td className="py-3 px-4 font-mono text-text-muted">{r.before}</td>
                <td className="py-3 px-4 font-mono text-text-muted">{r.after}</td>
                <td className="py-3 px-4 font-medium text-text-primary">{r.details}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
