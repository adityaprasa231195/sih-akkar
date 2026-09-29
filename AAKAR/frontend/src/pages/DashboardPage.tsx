import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { KPICards } from '../components/KPICards';
import { ComparisonTable } from '../components/ComparisonTable';
import { RecentActivity } from '../components/RecentActivity';
import { fetchKPIs } from '../api/client';
import { DashboardKPIs } from '../types';
import { Map, AlertTriangle, ShieldAlert, Cpu, Download } from 'lucide-react';

export const DashboardPage: React.FC = () => {
  const navigate = useNavigate();
  const [kpis, setKpis] = useState<DashboardKPIs>({
    hectares_processed: 12.8,
    time_saved_pct: 96.9,
    gt_effort_reduced_pct: 77.8,
    topology_health_pct: 55.6,
    open_encroachments: 3,
    high_dispute_risk_count: 2,
    ulpin_ready_count: 4,
    changes_detected_count: 4,
  });

  useEffect(() => {
    fetchKPIs().then(setKpis).catch(console.error);
  }, []);

  return (
    <div className="p-8 space-y-8 max-w-[1440px] mx-auto">
      {/* Welcome Banner */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-2 border-b border-border-ui">
        <div>
          <span className="text-xs font-bold text-accent uppercase tracking-wider">
            National Land Records Modernization Programme (NLRMP)
          </span>
          <h2 className="text-2xl font-bold text-text-primary tracking-tight mt-0.5">
            Cadastral AI Operations Dashboard
          </h2>
          <p className="text-sm text-text-secondary">
            Autonomous parcel boundary extraction, 9-error topology validation, and ULPIN synchronization
          </p>
        </div>

        {/* Quick Launch Buttons */}
        <div className="flex items-center gap-2">
          <button
            onClick={() => navigate('/map')}
            className="aakar-btn-primary flex items-center gap-2 text-xs"
          >
            <Map className="w-4 h-4" /> Open Web-GIS
          </button>
          <button
            onClick={() => navigate('/pipeline')}
            className="aakar-btn-secondary flex items-center gap-2 text-xs"
          >
            <Cpu className="w-4 h-4 text-accent" /> Run AI Pipeline
          </button>
        </div>
      </div>

      {/* 8 Live KPI Cards */}
      <KPICards kpis={kpis} />

      {/* Main Grid: Comparison Table + Recent Activity */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-6">
          <ComparisonTable />
        </div>
        <div className="lg:col-span-1">
          <RecentActivity />
        </div>
      </div>
    </div>
  );
};
