import React, { useState } from 'react';
import {
  X,
  Copy,
  Check,
  ShieldCheck,
  AlertTriangle,
  History,
  CheckCircle2,
  XCircle,
  Edit,
  ExternalLink
} from 'lucide-react';
import { Parcel, Role } from '../types';
import { RURAL_PARCEL_ALIASES } from '../data/cadastralData';

interface ParcelInspectorProps {
  parcel: Parcel | null;
  onClose: () => void;
  userRole: Role;
  onApprove: (parcelId: string, override: boolean, reason: string) => Promise<void>;
  onReject: (parcelId: string, reason: string) => Promise<void>;
  onViewHistory: (parcel: Parcel) => void;
}

export const ParcelInspector: React.FC<ParcelInspectorProps> = ({
  parcel,
  onClose,
  userRole,
  onApprove,
  onReject,
  onViewHistory,
}) => {
  const [copiedId, setCopiedId] = useState(false);
  const [copiedUlpin, setCopiedUlpin] = useState(false);
  const [showOverrideModal, setShowOverrideModal] = useState(false);
  const [overrideReason, setOverrideReason] = useState('');
  const [rejectModal, setRejectModal] = useState(false);
  const [rejectReason, setRejectReason] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  if (!parcel) return null;

  const canApprove = userRole === 'Reviewer' || userRole === 'Administrator';
  const isHighRisk = parcel.dispute_risk_score >= 60;
  const hasCriticalErrors = parcel.topology_status === 'HasErrors';

  const copyToClipboard = (text: string, isUlpin: boolean) => {
    navigator.clipboard.writeText(text);
    if (isUlpin) {
      setCopiedUlpin(true);
      setTimeout(() => setCopiedUlpin(false), 2000);
    } else {
      setCopiedId(true);
      setTimeout(() => setCopiedId(false), 2000);
    }
  };

  const handleApproveClick = async () => {
    setErrorMessage(null);
    if (hasCriticalErrors) {
      setErrorMessage('Approval blocked: unresolved Critical topology errors exist on this parcel.');
      return;
    }
    if (isHighRisk) {
      setShowOverrideModal(true);
      return;
    }

    try {
      setIsSubmitting(true);
      await onApprove(parcel.parcel_id, false, '');
    } catch (err: any) {
      setErrorMessage(err.response?.data?.detail || 'Approval failed');
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleOverrideSubmit = async () => {
    if (!overrideReason.trim()) return;
    try {
      setIsSubmitting(true);
      await onApprove(parcel.parcel_id, true, overrideReason);
      setShowOverrideModal(false);
    } catch (err: any) {
      setErrorMessage(err.response?.data?.detail || 'Override approval failed');
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleRejectSubmit = async () => {
    if (!rejectReason.trim()) return;
    try {
      setIsSubmitting(true);
      await onReject(parcel.parcel_id, rejectReason);
      setRejectModal(false);
    } catch (err: any) {
      setErrorMessage(err.response?.data?.detail || 'Rejection failed');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="w-[360px] bg-bg-primary border-l border-border-ui h-full flex flex-col shadow-xl absolute right-0 top-0 z-30">
      {/* Header */}
      <div className="p-4 border-b border-border-ui flex items-center justify-between bg-bg-secondary">
        <div>
          <span className="text-[10px] font-bold text-accent uppercase tracking-wider">Cadastral Inspector</span>
          <h3 className="font-semibold text-text-primary text-sm">Parcel Details</h3>
        </div>
        <button onClick={onClose} className="p-1 text-text-muted hover:text-text-primary rounded-lg">
          <X className="w-4 h-4" />
        </button>
      </div>

      {/* Content */}
      <div className="flex-1 overflow-y-auto p-5 space-y-5">
        {errorMessage && (
          <div className="p-3 bg-rose-50 border border-rose-200 rounded-lg text-xs text-danger font-medium">
            {errorMessage}
          </div>
        )}

        {/* Rural Survey Reference */}
        {RURAL_PARCEL_ALIASES[parcel.parcel_id] && (
          <div className="bg-accent/10 border border-accent/25 p-3 rounded-xl text-xs">
            <span className="text-[10px] uppercase tracking-wider block text-accent font-bold mb-0.5">
              Rural Land Record / Gat Reference
            </span>
            <span className="font-semibold text-text-primary text-sm">
              {RURAL_PARCEL_ALIASES[parcel.parcel_id]}
            </span>
          </div>
        )}

        {/* Intentional Encroachment Demo Warning Badge */}
        {parcel.parcel_id === 'p-saswad-006' && (
          <div className="p-3 bg-amber-50 border border-amber-300 dark:bg-amber-950/40 dark:border-amber-700/60 rounded-xl space-y-1.5 shadow-sm">
            <div className="flex items-center gap-1.5 text-amber-700 dark:text-amber-400 font-bold text-xs">
              <AlertTriangle className="w-4 h-4 text-amber-600 dark:text-amber-400 shrink-0" />
              <span>Boundary Encroachment Flag (Intentional Demo)</span>
            </div>
            <p className="text-[11px] text-amber-900 dark:text-amber-200 leading-snug">
              Farm pumphouse roof eave (<span className="font-mono font-semibold">b-saswad-105</span>) projects <span className="font-bold text-rose-600 dark:text-rose-400">1.2m</span> across the northern survey boundary into the Dive-Saswad road corridor setback.
            </p>
            <div className="pt-1 flex items-center gap-2">
              <span className="text-[10px] bg-amber-200/70 dark:bg-amber-900/60 text-amber-900 dark:text-amber-300 px-2 py-0.5 rounded font-mono font-semibold">
                Overlap: 12.8 m²
              </span>
              <span className="text-[10px] bg-rose-100 text-rose-700 dark:bg-rose-950/50 dark:text-rose-300 px-2 py-0.5 rounded font-mono font-semibold">
                Requires RTK Field Survey
              </span>
            </div>
          </div>
        )}

        {/* Monospace IDs */}
        <div className="space-y-2">
          <div>
            <span className="text-[11px] font-medium text-text-muted">Parcel ID</span>
            <div className="flex items-center justify-between bg-bg-subtle p-2 rounded-lg font-mono text-xs">
              <span className="truncate">{parcel.parcel_id}</span>
              <button onClick={() => copyToClipboard(parcel.parcel_id, false)} className="text-text-muted hover:text-text-primary">
                {copiedId ? <Check className="w-3.5 h-3.5 text-success" /> : <Copy className="w-3.5 h-3.5" />}
              </button>
            </div>
          </div>

          <div>
            <span className="text-[11px] font-medium text-text-muted">ULPIN (Bhu-Aadhaar 14-char)</span>
            <div className="flex items-center justify-between bg-bg-subtle p-2 rounded-lg font-mono text-xs">
              <span className={parcel.ulpin ? 'font-bold text-accent' : 'text-text-muted italic'}>
                {parcel.ulpin || 'Pending Reviewer Approval'}
              </span>
              {parcel.ulpin && (
                <button onClick={() => copyToClipboard(parcel.ulpin!, true)} className="text-text-muted hover:text-accent">
                  {copiedUlpin ? <Check className="w-3.5 h-3.5 text-success" /> : <Copy className="w-3.5 h-3.5" />}
                </button>
              )}
            </div>
          </div>
        </div>

        {/* Confidence & Risk */}
        <div className="p-4 bg-bg-secondary rounded-xl border border-border-ui space-y-3">
          <div>
            <div className="flex justify-between items-center text-xs mb-1">
              <span className="font-medium text-text-secondary">AI Confidence Score</span>
              <span className="font-bold text-sm text-text-primary">{(parcel.confidence_score * 100).toFixed(0)}%</span>
            </div>
            <div className="w-full bg-border-ui h-2 rounded-full overflow-hidden">
              <div
                className={`h-full rounded-full ${
                  parcel.confidence_score >= 0.85
                    ? 'bg-success'
                    : parcel.confidence_score >= 0.50
                    ? 'bg-warning'
                    : 'bg-danger'
                }`}
                style={{ width: `${parcel.confidence_score * 100}%` }}
              />
            </div>
          </div>

          <div className="flex justify-between items-center pt-2 border-t border-border-ui text-xs">
            <span className="font-medium text-text-secondary">Dispute Risk Score</span>
            <span
              className={`aakar-badge ${
                parcel.dispute_risk_score >= 60
                  ? 'bg-rose-50 text-danger font-bold'
                  : parcel.dispute_risk_score >= 30
                  ? 'bg-amber-50 text-warning font-semibold'
                  : 'bg-emerald-50 text-success'
              }`}
            >
              {parcel.dispute_risk_score} / 100 ({parcel.dispute_risk_score >= 60 ? 'High' : parcel.dispute_risk_score >= 30 ? 'Medium' : 'Low'})
            </span>
          </div>
        </div>

        {/* Attributes Grid */}
        <div className="grid grid-cols-2 gap-3 text-xs">
          <div className="p-3 bg-bg-subtle/70 rounded-lg">
            <span className="text-text-muted">Land Use Class</span>
            <p className="font-semibold text-text-primary mt-0.5">{parcel.land_use_class}</p>
          </div>
          <div className="p-3 bg-bg-subtle/70 rounded-lg">
            <span className="text-text-muted">Coverage Type</span>
            <p className="font-semibold text-text-primary mt-0.5">{parcel.coverage_type}</p>
          </div>
          <div className="p-3 bg-bg-subtle/70 rounded-lg">
            <span className="text-text-muted">Area</span>
            <p className="font-semibold text-text-primary mt-0.5">{parcel.area_sqm.toLocaleString()} m²</p>
          </div>
          <div className="p-3 bg-bg-subtle/70 rounded-lg">
            <span className="text-text-muted">Perimeter</span>
            <p className="font-semibold text-text-primary mt-0.5">{parcel.perimeter_m.toFixed(1)} m</p>
          </div>
        </div>

        {/* Status Pills */}
        <div className="space-y-2 text-xs">
          <div className="flex justify-between items-center p-2 rounded-lg bg-bg-secondary">
            <span className="text-text-secondary">Validation Status</span>
            <span
              className={`aakar-badge ${
                parcel.validation_status === 'Approved'
                  ? 'bg-emerald-50 text-success'
                  : parcel.validation_status === 'Rejected'
                  ? 'bg-rose-50 text-danger'
                  : 'bg-amber-50 text-warning'
              }`}
            >
              {parcel.validation_status}
            </span>
          </div>

          <div className="flex justify-between items-center p-2 rounded-lg bg-bg-secondary">
            <span className="text-text-secondary">Topology Status</span>
            <span
              className={`aakar-badge ${
                parcel.topology_status === 'Valid'
                  ? 'bg-emerald-50 text-success'
                  : 'bg-rose-50 text-danger'
              }`}
            >
              {parcel.topology_status}
            </span>
          </div>

          <div className="flex justify-between items-center p-2 rounded-lg bg-bg-secondary">
            <span className="text-text-secondary">Ground Truthing</span>
            <span className="aakar-badge bg-blue-50 text-accent">{parcel.gt_status}</span>
          </div>
        </div>
      </div>

      {/* Footer Action Buttons */}
      <div className="p-4 border-t border-border-ui bg-bg-secondary space-y-2">
        <div className="grid grid-cols-2 gap-2">
          <button
            onClick={handleApproveClick}
            disabled={!canApprove || isSubmitting || parcel.validation_status === 'Approved'}
            title={!canApprove ? 'Reviewer role required to approve' : ''}
            className={`aakar-btn-primary text-xs flex items-center justify-center gap-1.5 ${
              !canApprove || parcel.validation_status === 'Approved' ? 'opacity-50 cursor-not-allowed' : ''
            }`}
          >
            <CheckCircle2 className="w-3.5 h-3.5" /> Approve & ULPIN
          </button>

          <button
            onClick={() => setRejectModal(true)}
            disabled={!canApprove || isSubmitting}
            className={`aakar-btn-secondary text-xs flex items-center justify-center gap-1.5 text-danger border-rose-200 hover:bg-rose-50 ${
              !canApprove ? 'opacity-50 cursor-not-allowed' : ''
            }`}
          >
            <XCircle className="w-3.5 h-3.5" /> Reject
          </button>
        </div>

        <button
          onClick={() => onViewHistory(parcel)}
          className="w-full aakar-btn-secondary text-xs flex items-center justify-center gap-1.5"
        >
          <History className="w-3.5 h-3.5" /> View Version Timeline
        </button>
      </div>

      {/* Override High Risk Modal */}
      {showOverrideModal && (
        <div className="fixed inset-0 bg-text-primary/60 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-bg-primary rounded-xl max-w-md w-full p-6 shadow-2xl border border-border-ui">
            <div className="flex items-center gap-2 text-warning mb-3">
              <AlertTriangle className="w-5 h-5" />
              <h4 className="font-bold text-text-primary">Dispute Risk Approval Override</h4>
            </div>
            <p className="text-xs text-text-secondary mb-4 leading-relaxed">
              This parcel has a dispute risk score of <span className="font-bold text-danger">{parcel.dispute_risk_score}/100</span>.
              Reviewer-role approval requires mandatory documentation of justification.
            </p>
            <textarea
              value={overrideReason}
              onChange={(e) => setOverrideReason(e.target.value)}
              placeholder="Enter legal / field survey justification for override..."
              className="w-full h-24 p-3 border border-border-ui rounded-lg text-xs focus:outline-none focus:border-accent"
            />
            <div className="flex justify-end gap-2 mt-4">
              <button onClick={() => setShowOverrideModal(false)} className="aakar-btn-secondary text-xs">
                Cancel
              </button>
              <button
                onClick={handleOverrideSubmit}
                disabled={!overrideReason.trim()}
                className="aakar-btn-primary text-xs bg-warning hover:bg-amber-600"
              >
                Confirm Approval Override
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Reject Modal */}
      {rejectModal && (
        <div className="fixed inset-0 bg-text-primary/60 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-bg-primary rounded-xl max-w-md w-full p-6 shadow-2xl border border-border-ui">
            <h4 className="font-bold text-text-primary text-sm mb-2">Reject Preliminary Parcel</h4>
            <p className="text-xs text-text-secondary mb-4">State the specific reason for rejecting this feature:</p>
            <textarea
              value={rejectReason}
              onChange={(e) => setRejectReason(e.target.value)}
              placeholder="e.g. Obvious roof overhang bias, boundary deviates from physical hedgerow..."
              className="w-full h-24 p-3 border border-border-ui rounded-lg text-xs focus:outline-none focus:border-danger"
            />
            <div className="flex justify-end gap-2 mt-4">
              <button onClick={() => setRejectModal(false)} className="aakar-btn-secondary text-xs">
                Cancel
              </button>
              <button
                onClick={handleRejectSubmit}
                disabled={!rejectReason.trim()}
                className="aakar-btn-danger text-xs"
              >
                Confirm Rejection
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
