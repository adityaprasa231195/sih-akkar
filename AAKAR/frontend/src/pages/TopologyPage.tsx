import React, { useState, useEffect } from 'react';
import { AlertTriangle, CheckCircle, Search, Filter, Wrench, X } from 'lucide-react';
import { TopologyError } from '../types';
import { fetchTopologyErrors } from '../api/client';

export const TopologyPage: React.FC = () => {
  const [errors, setErrors] = useState<TopologyError[]>([]);
  const [selectedError, setSelectedError] = useState<TopologyError | null>(null);
  const [severityFilter, setSeverityFilter] = useState('All');
  const [typeFilter, setTypeFilter] = useState('All');
  const [resolveModal, setResolveModal] = useState<TopologyError | null>(null);
  const [customNote, setCustomNote] = useState('');

  useEffect(() => {
    fetchTopologyErrors().then((data) => {
      setErrors(data);
      if (data.length > 0) setSelectedError(data[0]);
    });
  }, []);

  const filtered = errors.filter((err) => {
    if (severityFilter !== 'All' && err.severity !== severityFilter) return false;
    if (typeFilter !== 'All' && err.error_type !== typeFilter) return false;
    return true;
  });

  const handleResolve = (action: 'accept_suggested' | 'custom' | 'dismiss') => {
    if (!resolveModal) return;
    setErrors((prev) =>
      prev.map((e) =>
        e.error_id === resolveModal.error_id
          ? { ...e, status: action === 'dismiss' ? 'Dismissed' : 'AutoCorrected' }
          : e
      )
    );
    setResolveModal(null);
    setCustomNote('');
  };

  return (
    <div className="p-8 space-y-6 max-w-[1440px] mx-auto">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-2 border-b border-border-ui">
        <div>
          <span className="text-xs font-bold text-accent uppercase tracking-wider">
            Layer 4 GeoAI Spatial Validation
          </span>
          <h2 className="text-2xl font-bold text-text-primary tracking-tight mt-0.5">
            Automated 9-Error Topology Engine
          </h2>
          <p className="text-sm text-text-secondary">
            Continuous geometric validation enforcing OGC compliance and preventing illegal overlaps and voids
          </p>
        </div>

        <div className="flex items-center gap-2">
          <span className="aakar-badge bg-rose-50 text-danger font-semibold">
            {errors.filter((e) => e.severity === 'Critical' && e.status === 'Open').length} Critical Unresolved
          </span>
          <span className="aakar-badge bg-amber-50 text-warning font-semibold">
            {errors.filter((e) => e.severity === 'Warning' && e.status === 'Open').length} Warnings
          </span>
        </div>
      </div>

      {/* Filter Bar */}
      <div className="flex flex-wrap items-center justify-between gap-4 bg-bg-primary p-4 rounded-xl border border-border-ui">
        <div className="flex items-center gap-3">
          <Filter className="w-4 h-4 text-text-muted" />
          <select
            value={severityFilter}
            onChange={(e) => setSeverityFilter(e.target.value)}
            className="text-xs font-medium p-2 bg-bg-secondary border border-border-ui rounded-lg focus:outline-none"
          >
            <option value="All">All Severities</option>
            <option value="Critical">Critical (Approval Blocking)</option>
            <option value="Warning">Warning</option>
            <option value="Info">Info</option>
          </select>

          <select
            value={typeFilter}
            onChange={(e) => setTypeFilter(e.target.value)}
            className="text-xs font-medium p-2 bg-bg-secondary border border-border-ui rounded-lg focus:outline-none"
          >
            <option value="All">All 9 Error Types</option>
            <option value="Overlap">1. Polygon Overlap</option>
            <option value="Gap">2. Gap / Void</option>
            <option value="Sliver">3. Sliver Polygon</option>
            <option value="SelfIntersection">4. Self-Intersection</option>
            <option value="Duplicate">5. Duplicate Geometry</option>
            <option value="InvalidPolygon">6. Invalid Polygon (OGC)</option>
            <option value="UnclosedBoundary">7. Unclosed Boundary</option>
            <option value="Misalignment">8. Node Misalignment</option>
            <option value="InconsistentRelationship">9. Inconsistent Relationship</option>
          </select>
        </div>

        <span className="text-xs text-text-muted">
          Showing {filtered.length} of {errors.length} topology items
        </span>
      </div>

      {/* Grid: Table on Left + Mini Preview on Right */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Table */}
        <div className="lg:col-span-2 aakar-card overflow-hidden">
          <table className="w-full text-left border-collapse text-xs">
            <thead>
              <tr className="border-b border-border-ui bg-bg-subtle text-text-secondary font-semibold">
                <th className="py-3 px-4">Severity</th>
                <th className="py-3 px-4">Error Type</th>
                <th className="py-3 px-4">Feature ID</th>
                <th className="py-3 px-4">Description</th>
                <th className="py-3 px-4">Status</th>
                <th className="py-3 px-4 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-border-ui">
              {filtered.map((err) => {
                const isSelected = selectedError?.error_id === err.error_id;
                return (
                  <tr
                    key={err.error_id}
                    onClick={() => setSelectedError(err)}
                    className={`cursor-pointer transition-colors ${
                      isSelected ? 'bg-blue-50/60' : 'hover:bg-bg-subtle/50'
                    }`}
                  >
                    <td className="py-3 px-4">
                      <span
                        className={`aakar-badge ${
                          err.severity === 'Critical'
                            ? 'bg-rose-50 text-danger font-bold'
                            : err.severity === 'Warning'
                            ? 'bg-amber-50 text-warning font-semibold'
                            : 'bg-cyan-50 text-info font-medium'
                        }`}
                      >
                        {err.severity}
                      </span>
                    </td>
                    <td className="py-3 px-4 font-semibold text-text-primary">{err.error_type}</td>
                    <td className="py-3 px-4 font-mono text-text-secondary">{err.feature_id}</td>
                    <td className="py-3 px-4 max-w-xs truncate text-text-secondary">{err.description}</td>
                    <td className="py-3 px-4">
                      <span
                        className={`aakar-badge ${
                          err.status === 'Open'
                            ? 'bg-rose-50 text-danger'
                            : 'bg-emerald-50 text-success'
                        }`}
                      >
                        {err.status}
                      </span>
                    </td>
                    <td className="py-3 px-4 text-right">
                      {err.status === 'Open' && (
                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            setResolveModal(err);
                          }}
                          className="aakar-btn-secondary text-[11px] py-1 px-2.5 inline-flex items-center gap-1 text-accent border-blue-200 hover:bg-blue-50"
                        >
                          <Wrench className="w-3 h-3" /> Resolve
                        </button>
                      )}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>

        {/* Mini Preview Sidebar */}
        <div className="aakar-card p-5 space-y-4 h-fit">
          <div className="flex items-center justify-between pb-3 border-b border-border-ui">
            <h3 className="font-semibold text-sm text-text-primary">Topology Detail Inspection</h3>
            <span className="text-[11px] font-mono text-text-muted">{selectedError?.error_id}</span>
          </div>

          {selectedError ? (
            <div className="space-y-4 text-xs">
              <div className="h-44 bg-bg-secondary rounded-xl border border-border-ui relative flex items-center justify-center overflow-hidden">
                <svg className="w-full h-full p-4" viewBox="0 0 100 100">
                  <polygon points="15,20 65,20 65,80 15,80" fill="rgba(37, 99, 235, 0.15)" stroke="#2563EB" strokeWidth="2" />
                  {selectedError.error_type === 'Overlap' ? (
                    <polygon points="50,40 90,40 90,90 50,90" fill="rgba(220, 38, 38, 0.4)" stroke="#DC2626" strokeWidth="2" />
                  ) : (
                    <polygon points="15,20 65,80 15,80 65,20" fill="none" stroke="#DC2626" strokeWidth="2" strokeDasharray="3,3" />
                  )}
                </svg>
                <div className="absolute top-2 left-2 bg-white/90 px-2 py-0.5 rounded text-[10px] font-semibold text-danger">
                  {selectedError.error_type} Fault
                </div>
              </div>

              <div>
                <span className="text-text-muted block mb-1">Description</span>
                <p className="p-2.5 bg-bg-subtle rounded-lg text-text-primary leading-relaxed font-medium">
                  {selectedError.description}
                </p>
              </div>

              <div>
                <span className="text-text-muted block mb-1">Recommended Algorithmic Correction</span>
                <p className="p-2.5 bg-emerald-50 border border-emerald-200 rounded-lg text-success leading-relaxed font-medium">
                  {selectedError.suggested_correction || 'Review coordinates manually.'}
                </p>
              </div>

              {selectedError.status === 'Open' && (
                <button
                  onClick={() => setResolveModal(selectedError)}
                  className="w-full aakar-btn-primary py-2 text-xs flex items-center justify-center gap-1.5"
                >
                  <Wrench className="w-3.5 h-3.5" /> Resolve Error
                </button>
              )}
            </div>
          ) : (
            <p className="text-xs text-text-muted italic">Select a row to inspect.</p>
          )}
        </div>
      </div>

      {/* Resolve Modal */}
      {resolveModal && (
        <div className="fixed inset-0 bg-text-primary/60 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-bg-primary rounded-xl max-w-lg w-full p-6 shadow-2xl border border-border-ui">
            <div className="flex items-center justify-between pb-3 border-b border-border-ui mb-4">
              <h3 className="font-bold text-text-primary text-base">Resolve Topology Error</h3>
              <button onClick={() => setResolveModal(null)} className="text-text-muted hover:text-text-primary">
                <X className="w-4 h-4" />
              </button>
            </div>

            <p className="text-xs text-text-secondary mb-3">
              Apply algorithmic recommendation or document custom human surveyor adjustment:
            </p>

            <div className="p-3 bg-emerald-50 border border-emerald-200 rounded-lg text-xs text-success mb-4 font-medium">
              Suggested Fix: {resolveModal.suggested_correction}
            </div>

            <textarea
              value={customNote}
              onChange={(e) => setCustomNote(e.target.value)}
              placeholder="Optional notes or surveyor verification reference..."
              className="w-full h-20 p-2.5 border border-border-ui rounded-lg text-xs focus:outline-none focus:border-accent"
            />

            <div className="flex justify-between items-center mt-5 pt-3 border-t border-border-ui">
              <button
                onClick={() => handleResolve('dismiss')}
                className="text-xs text-text-muted hover:text-danger font-medium"
              >
                Dismiss Flag
              </button>
              <div className="flex gap-2">
                <button onClick={() => setResolveModal(null)} className="aakar-btn-secondary text-xs">
                  Cancel
                </button>
                <button
                  onClick={() => handleResolve('accept_suggested')}
                  className="aakar-btn-primary text-xs"
                >
                  Accept & Auto-Correct
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
