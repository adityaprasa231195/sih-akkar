import React, { useState } from 'react';
import { X, RotateCcw, Calendar, User, FileText, CheckCircle } from 'lucide-react';
import { Parcel, Role } from '../types';

interface TimelineModalProps {
  parcel: Parcel | null;
  onClose: () => void;
  userRole: Role;
  onRollback: (parcelId: string, versionId: string) => Promise<void>;
}

export const TimelineModal: React.FC<TimelineModalProps> = ({
  parcel,
  onClose,
  userRole,
  onRollback,
}) => {
  const [selectedVersion, setSelectedVersion] = useState<number>(1);
  const [isRollingBack, setIsRollingBack] = useState(false);

  if (!parcel) return null;

  const canRollback = userRole === 'Reviewer' || userRole === 'Administrator';

  // Sample version history snapshots
  const versions = [
    {
      id: 'ver-001',
      version: 1,
      date: '2026-09-14 11:20 AM',
      author: 'AI Pipeline (U-Net + Mask R-CNN)',
      reason: 'Initial preliminary parcel polygonization',
      area_sqm: 650.0,
      land_use: 'Residential',
      confidence: 0.88,
    },
    {
      id: 'ver-002',
      version: 2,
      date: '2026-09-25 03:45 PM',
      author: 'editor',
      reason: 'Adjusted northern fence edge to match ground CORS points',
      area_sqm: parcel.area_sqm,
      land_use: parcel.land_use_class,
      confidence: parcel.confidence_score,
    },
  ];

  const currentVer = versions.find((v) => v.version === selectedVersion) || versions[0];
  const initialVer = versions[0];

  const handleRollbackClick = async () => {
    try {
      setIsRollingBack(true);
      await onRollback(parcel.parcel_id, currentVer.id);
      onClose();
    } catch (err) {
      alert('Rollback failed');
    } finally {
      setIsRollingBack(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-text-primary/60 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div className="bg-bg-primary rounded-2xl max-w-3xl w-full p-6 shadow-2xl border border-border-ui flex flex-col max-h-[85vh]">
        {/* Header */}
        <div className="flex items-center justify-between pb-4 border-b border-border-ui">
          <div>
            <span className="text-xs font-bold text-accent uppercase tracking-wider">Parcel Version History</span>
            <h3 className="text-lg font-bold text-text-primary">Cadastral Evolution Timeline</h3>
            <p className="text-xs text-text-muted font-mono mt-0.5">{parcel.parcel_id}</p>
          </div>
          <button onClick={onClose} className="p-1.5 text-text-muted hover:text-text-primary rounded-lg">
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Body */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 py-6 flex-1 overflow-y-auto">
          {/* Left: Vertical Timeline */}
          <div className="space-y-4 border-r border-border-ui pr-4">
            <h4 className="text-xs font-semibold text-text-secondary uppercase tracking-wider">Versions</h4>
            {versions.map((v) => (
              <div
                key={v.version}
                onClick={() => setSelectedVersion(v.version)}
                className={`p-3 rounded-xl cursor-pointer border transition-all ${
                  selectedVersion === v.version
                    ? 'border-accent bg-blue-50/50 shadow-sm'
                    : 'border-border-ui hover:bg-bg-subtle'
                }`}
              >
                <div className="flex items-center justify-between">
                  <span className="font-bold text-sm text-text-primary">Version {v.version}</span>
                  {selectedVersion === v.version && (
                    <span className="w-2 h-2 rounded-full bg-accent" />
                  )}
                </div>
                <div className="text-[11px] text-text-muted mt-1 space-y-0.5">
                  <div className="flex items-center gap-1">
                    <Calendar className="w-3 h-3" /> {v.date}
                  </div>
                  <div className="flex items-center gap-1">
                    <User className="w-3 h-3" /> {v.author}
                  </div>
                </div>
              </div>
            ))}
          </div>

          {/* Right: Attribute Diff & Geometry Preview */}
          <div className="md:col-span-2 space-y-5">
            <div>
              <h4 className="text-xs font-semibold text-text-secondary uppercase tracking-wider mb-2">
                Version {currentVer.version} Snapshot Details
              </h4>
              <p className="text-xs text-text-secondary bg-bg-subtle p-3 rounded-lg flex items-center gap-2">
                <FileText className="w-4 h-4 text-accent" /> {currentVer.reason}
              </p>
            </div>

            {/* Two-Column Diff Table */}
            <div>
              <h5 className="text-xs font-semibold text-text-secondary mb-2">Attribute Diff (Initial vs Selected)</h5>
              <table className="w-full text-xs border border-border-ui rounded-lg overflow-hidden">
                <thead className="bg-bg-subtle border-b border-border-ui">
                  <tr>
                    <th className="p-2 text-left text-text-secondary font-medium">Attribute</th>
                    <th className="p-2 text-left text-text-secondary font-medium">Version 1 (Initial)</th>
                    <th className="p-2 text-left text-text-secondary font-medium">Version {currentVer.version}</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-border-ui">
                  <tr>
                    <td className="p-2 font-medium text-text-primary">Area (sqm)</td>
                    <td className="p-2 text-text-muted">{initialVer.area_sqm} m²</td>
                    <td className={`p-2 font-semibold ${initialVer.area_sqm !== currentVer.area_sqm ? 'bg-amber-50 text-warning' : 'text-text-primary'}`}>
                      {currentVer.area_sqm} m²
                    </td>
                  </tr>
                  <tr>
                    <td className="p-2 font-medium text-text-primary">Land Use</td>
                    <td className="p-2 text-text-muted">{initialVer.land_use}</td>
                    <td className="p-2 text-text-primary">{currentVer.land_use}</td>
                  </tr>
                  <tr>
                    <td className="p-2 font-medium text-text-primary">AI Confidence</td>
                    <td className="p-2 text-text-muted">{(initialVer.confidence * 100).toFixed(0)}%</td>
                    <td className="p-2 text-text-primary">{(currentVer.confidence * 100).toFixed(0)}%</td>
                  </tr>
                </tbody>
              </table>
            </div>

            {/* Geometry Diff Mock */}
            <div className="p-4 bg-bg-secondary border border-border-ui rounded-xl">
              <span className="text-[11px] font-semibold text-text-muted uppercase tracking-wider block mb-2">
                Geometry Boundary Shift
              </span>
              <div className="h-32 bg-white rounded-lg border border-border-ui relative flex items-center justify-center overflow-hidden">
                {/* SVG boundary comparison */}
                <svg className="w-full h-full p-4" viewBox="0 0 100 100">
                  {/* Before outline in gray */}
                  <polygon points="20,20 80,20 80,75 20,75" fill="none" stroke="#9CA3AF" stroke-width="2" stroke-dasharray="3,3" />
                  {/* After outline in blue */}
                  <polygon points="20,20 80,20 80,82 20,82" fill="#2563EB" fill-opacity="0.1" stroke="#2563EB" stroke-width="2" />
                </svg>
                <div className="absolute bottom-2 right-2 flex items-center gap-3 text-[10px] bg-white/90 px-2 py-1 rounded shadow-sm">
                  <span className="flex items-center gap-1 text-text-muted">
                    <span className="w-2.5 h-0.5 bg-text-muted inline-block" /> Initial
                  </span>
                  <span className="flex items-center gap-1 text-accent font-semibold">
                    <span className="w-2.5 h-0.5 bg-accent inline-block" /> Selected
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="pt-4 border-t border-border-ui flex justify-between items-center bg-bg-primary">
          <span className="text-xs text-text-muted">
            {canRollback ? 'Rollback is logged in the permanent audit trail.' : 'Reviewer role required to roll back.'}
          </span>
          <div className="flex gap-2">
            <button onClick={onClose} className="aakar-btn-secondary text-xs">
              Close
            </button>
            <button
              onClick={handleRollbackClick}
              disabled={!canRollback || isRollingBack || selectedVersion === versions.length}
              className={`aakar-btn-primary text-xs flex items-center gap-1.5 ${
                !canRollback || selectedVersion === versions.length ? 'opacity-50 cursor-not-allowed' : ''
              }`}
            >
              <RotateCcw className="w-3.5 h-3.5" /> Rollback to Version {selectedVersion}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
