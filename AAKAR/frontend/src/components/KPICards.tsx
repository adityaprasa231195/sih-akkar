import React from 'react';
import {
  Layers,
  Clock,
  Compass,
  CheckSquare,
  ShieldAlert,
  AlertTriangle,
  BadgeCheck,
  History
} from 'lucide-react';
import { DashboardKPIs } from '../types';

interface KPICardsProps {
  kpis: DashboardKPIs;
}

export const KPICards: React.FC<KPICardsProps> = ({ kpis }) => {
  const cards = [
    {
      title: 'Hectares Processed',
      value: `${kpis.hectares_processed} ha`,
      subtext: 'High-res drone survey coverage',
      icon: Layers,
      color: 'text-accent',
      bgColor: 'bg-accent/10',
    },
    {
      title: 'Time Saved vs Manual',
      value: `${kpis.time_saved_pct}%`,
      subtext: 'AI pipeline vs 48h/ha baseline',
      icon: Clock,
      color: 'text-success',
      bgColor: 'bg-emerald-50',
    },
    {
      title: 'GT Effort Reduced',
      value: `${kpis.gt_effort_reduced_pct}%`,
      subtext: 'Targeted confidence verification',
      icon: Compass,
      color: 'text-accent',
      bgColor: 'bg-blue-50',
    },
    {
      title: 'Topology Health',
      value: `${kpis.topology_health_pct}%`,
      subtext: 'Parcels topology-valid',
      icon: CheckSquare,
      color: 'text-info',
      bgColor: 'bg-cyan-50',
    },
    {
      title: 'Encroachment Flags',
      value: `${kpis.open_encroachments} Open`,
      subtext: 'Structures outside boundary',
      icon: ShieldAlert,
      color: kpis.open_encroachments > 0 ? 'text-danger' : 'text-success',
      bgColor: kpis.open_encroachments > 0 ? 'bg-rose-50' : 'bg-emerald-50',
    },
    {
      title: 'Dispute Risk Parcels',
      value: `${kpis.high_dispute_risk_count} High Risk`,
      subtext: 'Score ≥ 60 awaiting review',
      icon: AlertTriangle,
      color: kpis.high_dispute_risk_count > 0 ? 'text-warning' : 'text-success',
      bgColor: kpis.high_dispute_risk_count > 0 ? 'bg-amber-50' : 'bg-emerald-50',
    },
    {
      title: 'ULPIN-Ready Parcels',
      value: `${kpis.ulpin_ready_count}`,
      subtext: 'Approved with 14-char ID',
      icon: BadgeCheck,
      color: 'text-success',
      bgColor: 'bg-emerald-50',
    },
    {
      title: 'Changes Detected',
      value: `${kpis.changes_detected_count}`,
      subtext: 'Since Epoch 2024 survey',
      icon: History,
      color: 'text-text-secondary',
      bgColor: 'bg-gray-100',
    },
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      {cards.map((c, idx) => {
        const Icon = c.icon;
        return (
          <div key={idx} className="aakar-card p-5 bg-bg-primary flex flex-col justify-between">
            <div className="flex items-center justify-between">
              <span className="text-xs font-medium text-text-secondary">{c.title}</span>
              <div className={`w-8 h-8 rounded-lg flex items-center justify-center ${c.bgColor} ${c.color}`}>
                <Icon className="w-4 h-4" />
              </div>
            </div>
            <div className="mt-3">
              <h3 className={`text-2xl font-bold tracking-tight ${c.color}`}>{c.value}</h3>
              <p className="text-xs text-text-muted mt-1">{c.subtext}</p>
            </div>
          </div>
        );
      })}
    </div>
  );
};
