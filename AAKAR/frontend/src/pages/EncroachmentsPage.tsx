import React, { useState, useEffect } from 'react';
import { ShieldAlert, AlertOctagon, CheckCircle2, XCircle, Search, Eye } from 'lucide-react';
import { EncroachmentFlag } from '../types';
import { fetchEncroachments } from '../api/client';

export const EncroachmentsPage: React.FC = () => {
  const [flags, setFlags] = useState<EncroachmentFlag[]>([]);
  const [selectedFlag, setSelectedFlag] = useState<EncroachmentFlag | null>(null);

  useEffect(() => {
    fetchEncroachments().then((data) => {
      setFlags(data);
      if (data.length > 0) setSelectedFlag(data[0]);
    });
  }, []);

  const totalOpen = flags.filter((f) => f.status === 'Open').length;
  const possibleCount = flags.filter((f) => f.flag_type === 'PossibleEncroachment' && f.status === 'Open').length;
  const unauthCount = flags.filter((f) => f.flag_type === 'UnauthorizedConstruction' && f.status === 'Open').length;
  const mismatchCount = flags.filter((f) => f.flag_type === 'BoundaryMismatch' && f.status === 'Open').length;

  const handleAction = (flagId: string, status: 'Resolved' | 'Dismissed') => {
    setFlags((prev) =>
      prev.map((f) => (f.encroachment_flag_id === flagId ? { ...f, status } : f))
    );
    if (selectedFlag?.encroachment_flag_id === flagId) {
      setSelectedFlag((prev) => (prev ? { ...prev, status } : null));
    }
  };

  return (
    <div className="p-8 space-y-6 max-w-[1440px] mx-auto">
      {/* Header */}
      <div className="pb-2 border-b border-border-ui">
        <span className="text-xs font-bold text-danger uppercase tracking-wider">
          Enforcement & Compliance
        </span>
        <h2 className="text-2xl font-bold text-text-primary tracking-tight mt-0.5">
          Cadastral Encroachment & Unauthorized Construction
        </h2>
        <p className="text-sm text-text-secondary">
          Automated overlay intersection comparing AI building footprints against registered cadastre
        </p>
      </div>

      {/* 4 Summary Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="aakar-card p-4 bg-bg-primary border-l-4 border-l-danger">
          <span className="text-xs text-text-muted font-medium">Total Open Violations</span>
          <h3 className="text-2xl font-bold text-danger mt-1">{totalOpen}</h3>
          <p className="text-[11px] text-text-muted mt-0.5">Pending legal resolution</p>
        </div>

        <div className="aakar-card p-4 bg-bg-primary">
          <span className="text-xs text-text-muted font-medium">Boundary Intrusion</span>
          <h3 className="text-2xl font-bold text-text-primary mt-1">{possibleCount}</h3>
          <p className="text-[11px] text-text-muted mt-0.5">Building extends past plot</p>
        </div>

        <div className="aakar-card p-4 bg-bg-primary">
          <span className="text-xs text-text-muted font-medium">Unauthorized Construction</span>
          <h3 className="text-2xl font-bold text-warning mt-1">{unauthCount}</h3>
          <p className="text-[11px] text-text-muted mt-0.5">Structure on Open/Gov land</p>
        </div>

        <div className="aakar-card p-4 bg-bg-primary">
          <span className="text-xs text-text-muted font-medium">Boundary Mismatch</span>
          <h3 className="text-2xl font-bold text-accent mt-1">{mismatchCount}</h3>
          <p className="text-[11px] text-text-muted mt-0.5">Drone vs historic GIS &gt; 2m</p>
        </div>
      </div>

      {/* Table & Mini Map Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 aakar-card overflow-hidden">
          <table className="w-full text-left border-collapse text-xs">
            <thead>
              <tr className="border-b border-border-ui bg-bg-subtle text-text-secondary font-semibold">
                <th className="py-3 px-4">Flag Type</th>
                <th className="py-3 px-4">Parcel ID</th>
                <th className="py-3 px-4">Building ID</th>
                <th className="py-3 px-4">Overlap Area</th>
                <th className="py-3 px-4">Confidence</th>
                <th className="py-3 px-4">Status</th>
                <th className="py-3 px-4 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-border-ui">
              {flags.map((flag) => {
                const isSelected = selectedFlag?.encroachment_flag_id === flag.encroachment_flag_id;
                return (
                  <tr
                    key={flag.encroachment_flag_id}
                    onClick={() => setSelectedFlag(flag)}
                    className={`cursor-pointer transition-colors ${
                      isSelected ? 'bg-rose-50/50' : 'hover:bg-bg-subtle/50'
                    }`}
                  >
                    <td className="py-3 px-4">
                      <span
                        className={`aakar-badge ${
                          flag.flag_type === 'UnauthorizedConstruction'
                            ? 'bg-rose-50 text-danger font-bold'
                            : flag.flag_type === 'PossibleEncroachment'
                            ? 'bg-amber-50 text-warning font-semibold'
                            : 'bg-blue-50 text-accent font-medium'
                        }`}
                      >
                        {flag.flag_type}
                      </span>
                    </td>
                    <td className="py-3 px-4 font-mono font-medium text-text-primary">{flag.parcel_id}</td>
                    <td className="py-3 px-4 font-mono text-text-muted">{flag.building_id || 'N/A'}</td>
                    <td className="py-3 px-4 font-bold text-text-primary">{flag.overlap_area_sqm} m²</td>
                    <td className="py-3 px-4 text-text-secondary">{(flag.confidence * 100).toFixed(0)}%</td>
                    <td className="py-3 px-4">
                      <span
                        className={`aakar-badge ${
                          flag.status === 'Open'
                            ? 'bg-rose-50 text-danger'
                            : 'bg-emerald-50 text-success'
                        }`}
                      >
                        {flag.status}
                      </span>
                    </td>
                    <td className="py-3 px-4 text-right">
                      {flag.status === 'Open' && (
                        <div className="flex items-center justify-end gap-1.5">
                          <button
                            onClick={(e) => {
                              e.stopPropagation();
                              handleAction(flag.encroachment_flag_id, 'Resolved');
                            }}
                            className="p-1 text-success hover:bg-emerald-50 rounded"
                            title="Mark Resolved"
                          >
                            <CheckCircle2 className="w-4 h-4" />
                          </button>
                          <button
                            onClick={(e) => {
                              e.stopPropagation();
                              handleAction(flag.encroachment_flag_id, 'Dismissed');
                            }}
                            className="p-1 text-text-muted hover:text-danger rounded"
                            title="Dismiss Flag"
                          >
                            <XCircle className="w-4 h-4" />
                          </button>
                        </div>
                      )}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>

        {/* Side Panel Mini Map Inspection */}
        <div className="aakar-card p-5 space-y-4 h-fit">
          <div className="flex items-center justify-between pb-3 border-b border-border-ui">
            <h3 className="font-semibold text-sm text-text-primary">Encroachment Spatial Overlay</h3>
            <span className="text-[11px] font-mono text-text-muted">{selectedFlag?.encroachment_flag_id}</span>
          </div>

          {selectedFlag ? (
            <div className="space-y-4 text-xs">
              {/* Mini Map SVG */}
              <div className="h-48 bg-bg-secondary rounded-xl border border-border-ui relative flex items-center justify-center overflow-hidden">
                <svg className="w-full h-full p-4" viewBox="0 0 100 100">
                  {/* Parcel boundary (Blue) */}
                  <polygon points="10,15 70,15 70,85 10,85" fill="rgba(37, 99, 235, 0.1)" stroke="#2563EB" strokeWidth="2" />
                  {/* Building footprint (Purple) extending out into Red encroachment zone */}
                  <polygon points="40,30 90,30 90,70 40,70" fill="rgba(124, 58, 237, 0.25)" stroke="#7C3AED" strokeWidth="2" />
                  {/* Overlap Intrusion slice (Red hatched) */}
                  <polygon points="70,30 90,30 90,70 70,70" fill="rgba(220, 38, 38, 0.5)" stroke="#DC2626" strokeWidth="2" strokeDasharray="2,2" />
                </svg>
                <div className="absolute bottom-2 left-2 bg-white/95 px-2 py-1 rounded text-[10px] shadow-sm flex items-center gap-3">
                  <span className="flex items-center gap-1 text-accent font-medium">
                    <span className="w-2 h-2 bg-accent inline-block rounded-sm" /> Parcel
                  </span>
                  <span className="flex items-center gap-1 text-purple-600 font-medium">
                    <span className="w-2 h-2 bg-purple-600 inline-block rounded-sm" /> Footprint
                  </span>
                  <span className="flex items-center gap-1 text-danger font-bold">
                    <span className="w-2 h-2 bg-danger inline-block rounded-sm" /> Intrusion
                  </span>
                </div>
              </div>

              <div>
                <span className="text-text-muted block mb-1">Survey Notes & Field Details</span>
                <p className="p-3 bg-bg-subtle rounded-lg text-text-primary leading-relaxed font-medium">
                  {selectedFlag.notes || 'No surveyor remarks filed.'}
                </p>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div className="p-3 bg-bg-subtle rounded-lg">
                  <span className="text-text-muted">Intrusion Area</span>
                  <p className="font-bold text-danger text-sm mt-0.5">{selectedFlag.overlap_area_sqm} m²</p>
                </div>
                <div className="p-3 bg-bg-subtle rounded-lg">
                  <span className="text-text-muted">AI Model Confidence</span>
                  <p className="font-bold text-text-primary text-sm mt-0.5">{(selectedFlag.confidence * 100).toFixed(0)}%</p>
                </div>
              </div>

              {selectedFlag.status === 'Open' && (
                <div className="flex gap-2 pt-2">
                  <button
                    onClick={() => handleAction(selectedFlag.encroachment_flag_id, 'Resolved')}
                    className="flex-1 aakar-btn-primary py-2 text-xs flex items-center justify-center gap-1.5"
                  >
                    <CheckCircle2 className="w-3.5 h-3.5" /> Mark Resolved
                  </button>
                  <button
                    onClick={() => handleAction(selectedFlag.encroachment_flag_id, 'Dismissed')}
                    className="aakar-btn-secondary py-2 text-xs text-text-muted hover:text-danger"
                  >
                    Dismiss
                  </button>
                </div>
              )}
            </div>
          ) : (
            <p className="text-xs text-text-muted italic">Select an encroachment to inspect.</p>
          )}
        </div>
      </div>
    </div>
  );
};
