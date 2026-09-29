import React, { useState, useEffect } from 'react';
import { Compass, UploadCloud, CheckCircle2, Navigation, ArrowUpRight, Check } from 'lucide-react';
import { api } from '../api/client';

export const GroundTruthPage: React.FC = () => {
  const [data, setData] = useState<{
    efficiency_metrics: {
      gt_effort_reduced_pct: number;
      estimated_visits_saved: number;
      total_parcels: number;
      priority_field_queue_count: number;
    };
    parcels: any[];
  }>({
    efficiency_metrics: {
      gt_effort_reduced_pct: 77.8,
      estimated_visits_saved: 7,
      total_parcels: 9,
      priority_field_queue_count: 2,
    },
    parcels: [],
  });

  const [uploadStatus, setUploadStatus] = useState<string | null>(null);

  useEffect(() => {
    api
      .get('/groundtruth/priority-list')
      .then((res) => setData(res.data))
      .catch(console.error);
  }, []);

  const handleMarkInProgress = (parcelId: string) => {
    setData((prev) => ({
      ...prev,
      parcels: prev.parcels.map((p) =>
        p.parcel_id === parcelId ? { ...p, gt_status: 'InProgress' } : p
      ),
    }));
  };

  const handleSimulatedUpload = () => {
    setUploadStatus('Uploading & matching field GNSS vectors...');
    setTimeout(() => {
      setUploadStatus('Successfully matched 6 parcels. High-confidence validation applied.');
      setData((prev) => ({
        ...prev,
        parcels: prev.parcels.map((p) => ({
          ...p,
          gt_status: 'Completed',
          confidence_score: Math.min(0.98, p.confidence_score + 0.18),
        })),
      }));
    }, 1500);
  };

  return (
    <div className="p-8 space-y-6 max-w-[1440px] mx-auto">
      {/* Header */}
      <div className="pb-2 border-b border-border-ui">
        <span className="text-xs font-bold text-accent uppercase tracking-wider">
          Field Survey Optimization
        </span>
        <h2 className="text-2xl font-bold text-text-primary tracking-tight mt-0.5">
          Ground-Truthing Confidence Queue & Field Ingestion
        </h2>
        <p className="text-sm text-text-secondary">
          Prioritizes surveyor field visits specifically for ambiguous or low-confidence geometries
        </p>
      </div>

      {/* GT Efficiency Widget */}
      <div className="aakar-card p-6 bg-gradient-to-r from-blue-50/80 to-indigo-50/50 border border-blue-100 flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
        <div className="space-y-1">
          <div className="flex items-center gap-2 text-accent font-semibold text-xs">
            <Compass className="w-4 h-4" />
            <span>Targeted Survey Optimization</span>
          </div>
          <h3 className="text-2xl font-bold text-text-primary">
            {data.efficiency_metrics.gt_effort_reduced_pct}% Field Effort Reduced
          </h3>
          <p className="text-xs text-text-secondary max-w-xl">
            Instead of uniformly surveying 100% of parcels, AAKAR concentrates mobile teams only on parcels scoring &lt; 0.85 confidence. High-confidence parcels pass via desktop review.
          </p>
        </div>

        <div className="flex items-center gap-4 bg-white p-4 rounded-xl shadow-sm border border-border-ui shrink-0">
          <div>
            <span className="text-[11px] text-text-muted font-medium block">Visits Saved</span>
            <span className="text-xl font-bold text-success">{data.efficiency_metrics.estimated_visits_saved} Plots</span>
          </div>
          <div className="w-px h-8 bg-border-ui" />
          <div>
            <span className="text-[11px] text-text-muted font-medium block">Priority Field Queue</span>
            <span className="text-xl font-bold text-danger">{data.efficiency_metrics.priority_field_queue_count} Plots</span>
          </div>
        </div>
      </div>

      {/* Grid: Left Priority Queue + Right GT Upload */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left: Priority Queue (Lowest Confidence First) */}
        <div className="lg:col-span-2 aakar-card overflow-hidden">
          <div className="p-4 border-b border-border-ui bg-bg-secondary flex justify-between items-center">
            <h3 className="font-semibold text-sm text-text-primary">
              Prioritized Field Queue (Lowest Confidence First)
            </h3>
            <span className="text-xs text-text-muted">Sorted ascending</span>
          </div>

          <table className="w-full text-left border-collapse text-xs">
            <thead>
              <tr className="border-b border-border-ui bg-bg-subtle text-text-secondary font-semibold">
                <th className="py-3 px-4">Parcel ID</th>
                <th className="py-3 px-4">AI Confidence</th>
                <th className="py-3 px-4">GT Status</th>
                <th className="py-3 px-4">Land Use</th>
                <th className="py-3 px-4">Area</th>
                <th className="py-3 px-4">Centroid Lat/Lon (GNSS Nav)</th>
                <th className="py-3 px-4 text-right">Field Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-border-ui">
              {data.parcels.map((p) => (
                <tr key={p.parcel_id} className="hover:bg-bg-subtle/50 transition-colors">
                  <td className="py-3 px-4 font-mono font-medium text-text-primary">{p.parcel_id}</td>
                  <td className="py-3 px-4">
                    <span
                      className={`aakar-badge ${
                        p.confidence_score >= 0.85
                          ? 'bg-emerald-50 text-success'
                          : p.confidence_score >= 0.50
                          ? 'bg-amber-50 text-warning font-semibold'
                          : 'bg-rose-50 text-danger font-bold'
                      }`}
                    >
                      {(p.confidence_score * 100).toFixed(0)}%
                    </span>
                  </td>
                  <td className="py-3 px-4">
                    <span className="aakar-badge bg-blue-50 text-accent font-medium">{p.gt_status}</span>
                  </td>
                  <td className="py-3 px-4 text-text-secondary">{p.land_use_class}</td>
                  <td className="py-3 px-4 font-medium text-text-primary">{p.area_sqm} m²</td>
                  <td className="py-3 px-4 font-mono text-[11px] text-text-muted">
                    {p.centroid_lat?.toFixed(4)}, {p.centroid_lon?.toFixed(4)}
                  </td>
                  <td className="py-3 px-4 text-right">
                    {p.gt_status === 'Pending' ? (
                      <button
                        onClick={() => handleMarkInProgress(p.parcel_id)}
                        className="aakar-btn-secondary text-[11px] py-1 px-2.5 inline-flex items-center gap-1 text-accent border-blue-200 hover:bg-blue-50"
                      >
                        <Navigation className="w-3 h-3" /> Mark In Progress
                      </button>
                    ) : (
                      <span className="text-[11px] text-success font-medium inline-flex items-center gap-1">
                        <Check className="w-3 h-3" /> In Field
                      </span>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Right: GT Upload Zone */}
        <div className="aakar-card p-6 space-y-5 h-fit">
          <div>
            <h3 className="font-semibold text-sm text-text-primary">Ingest Field GT Data</h3>
            <p className="text-xs text-text-secondary mt-0.5">
              Upload mobile surveyor GeoJSON or CORS GNSS coordinates
            </p>
          </div>

          <div
            onClick={handleSimulatedUpload}
            className="border-2 border-dashed border-border-ui hover:border-accent rounded-xl p-8 text-center cursor-pointer transition-colors bg-bg-secondary hover:bg-blue-50/20"
          >
            <UploadCloud className="w-8 h-8 text-accent mx-auto mb-2" />
            <p className="text-xs font-semibold text-text-primary">Drop Field Survey File Here</p>
            <p className="text-[11px] text-text-muted mt-1">GeoJSON, Shapefile (.zip), or CSV points</p>
            <button className="mt-4 aakar-btn-secondary text-xs py-1.5 px-3">
              Browse Files
            </button>
          </div>

          {uploadStatus && (
            <div className="p-3 bg-emerald-50 border border-emerald-200 rounded-lg text-xs text-success flex items-start gap-2">
              <CheckCircle2 className="w-4 h-4 shrink-0 mt-0.5" />
              <span>{uploadStatus}</span>
            </div>
          )}

          <div className="p-4 bg-bg-subtle rounded-xl text-xs space-y-2">
            <span className="font-semibold text-text-primary block">Survey Pack Verification</span>
            <div className="flex justify-between text-text-secondary">
              <span>Target Coordinate System:</span>
              <span className="font-mono font-medium text-text-primary">EPSG:4326</span>
            </div>
            <div className="flex justify-between text-text-secondary">
              <span>Auto-Snap Tolerance:</span>
              <span className="font-mono font-medium text-text-primary">0.30 meters</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
