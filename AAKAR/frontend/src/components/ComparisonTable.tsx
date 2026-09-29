import React from 'react';
import { Check, X, Minus } from 'lucide-react';

export const ComparisonTable: React.FC = () => {
  const rows = [
    { feature: 'Urban coverage', naksha: 'Yes', svamitva: 'No', bhu: 'Partial', aakar: 'Yes' },
    { feature: 'Rural coverage', naksha: 'No', svamitva: 'Yes', bhu: 'Partial', aakar: 'Yes' },
    { feature: 'AI auto-extraction (parcels & footprints)', naksha: 'No', svamitva: 'No', bhu: 'No', aakar: 'Yes' },
    { feature: 'Automated 9-error topology validation', naksha: 'No', svamitva: 'No', bhu: 'No', aakar: 'Yes' },
    { feature: 'Multi-factor confidence scoring', naksha: 'No', svamitva: 'No', bhu: 'No', aakar: 'Yes' },
    { feature: 'Automatic encroachment detection', naksha: 'No', svamitva: 'No', bhu: 'No', aakar: 'Yes' },
    { feature: 'Change detection between survey epochs', naksha: 'No', svamitva: 'No', bhu: 'No', aakar: 'Yes' },
    { feature: 'Dispute risk scoring & human review gate', naksha: 'No', svamitva: 'No', bhu: 'No', aakar: 'Yes' },
    { feature: 'Parcel version history & rollback', naksha: 'No', svamitva: 'No', bhu: 'No', aakar: 'Yes' },
    { feature: 'ULPIN-compatible 14-char ID generation', naksha: 'Partial', svamitva: 'No', bhu: 'Yes', aakar: 'Yes' },
    { feature: 'Citizen parcel lookup portal', naksha: 'No', svamitva: 'No', bhu: 'No', aakar: 'Yes' },
    { feature: 'Confidence-based GT field prioritization', naksha: 'No', svamitva: 'No', bhu: 'No', aakar: 'Yes' },
    { feature: 'Open-source stack (no proprietary GIS license)', naksha: 'Partial', svamitva: 'Partial', bhu: 'Partial', aakar: 'Yes' },
  ];

  const renderBadge = (val: string, isAakar: boolean = false) => {
    if (isAakar || val === 'Yes') {
      return (
        <span className="aakar-badge bg-emerald-50 text-success gap-1">
          <Check className="w-3 h-3 stroke-[2.5]" /> Yes
        </span>
      );
    }
    if (val === 'Partial') {
      return (
        <span className="aakar-badge bg-amber-50 text-warning gap-1">
          <Minus className="w-3 h-3 stroke-[2.5]" /> Partial
        </span>
      );
    }
    return (
      <span className="aakar-badge bg-gray-100 text-text-muted gap-1">
        <X className="w-3 h-3 stroke-[2.5]" /> No
      </span>
    );
  };

  return (
    <div className="aakar-card p-6 bg-bg-primary overflow-hidden">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h2 className="text-base font-semibold text-text-primary">System Comparison — AAKAR vs Legacy Systems</h2>
          <p className="text-xs text-text-secondary mt-0.5">
            Single unified platform replacing fragmented urban-only and rural-only systems
          </p>
        </div>
        <span className="text-xs font-semibold px-2.5 py-1 bg-accent/10 text-accent rounded-full">
          Competitive Advantage
        </span>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-left border-collapse text-sm">
          <thead>
            <tr className="border-b border-border-ui bg-bg-subtle text-xs font-semibold text-text-secondary">
              <th className="py-3 px-4">Feature</th>
              <th className="py-3 px-4 text-center">NAKSHA (Urban)</th>
              <th className="py-3 px-4 text-center">SVAMITVA (Rural)</th>
              <th className="py-3 px-4 text-center">Bhu-Aadhaar (ID)</th>
              <th className="py-3 px-4 text-center bg-blue-50/50 text-accent">AAKAR (Unified)</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-border-ui">
            {rows.map((r, idx) => (
              <tr key={idx} className={idx % 2 === 1 ? 'bg-bg-subtle/50' : 'bg-bg-primary'}>
                <td className="py-2.5 px-4 font-medium text-text-primary">{r.feature}</td>
                <td className="py-2.5 px-4 text-center">{renderBadge(r.naksha)}</td>
                <td className="py-2.5 px-4 text-center">{renderBadge(r.svamitva)}</td>
                <td className="py-2.5 px-4 text-center">{renderBadge(r.bhu)}</td>
                <td className="py-2.5 px-4 text-center bg-blue-50/30">{renderBadge(r.aakar, true)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
