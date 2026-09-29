import React from 'react';
import { CheckCircle2, Edit3, UploadCloud, Cpu, Download, RotateCcw } from 'lucide-react';

export const RecentActivity: React.FC = () => {
  const activities = [
    {
      action: 'Approve',
      user: 'reviewer',
      detail: 'Approved parcel p-wagholi-001 (ULPIN: MH070300120001)',
      time: '20m ago',
      icon: CheckCircle2,
      color: 'text-success',
      bgColor: 'bg-emerald-50',
    },
    {
      action: 'Edit',
      user: 'editor',
      detail: 'Boundary adjusted for parcel p-wagholi-003 to align with CORS',
      time: '1h ago',
      icon: Edit3,
      color: 'text-accent',
      bgColor: 'bg-blue-50',
    },
    {
      action: 'GTUpload',
      user: 'editor',
      detail: 'Uploaded Pune_GT_Field_Pack_04 (6 parcels verified)',
      time: '3h ago',
      icon: UploadCloud,
      color: 'text-info',
      bgColor: 'bg-cyan-50',
    },
    {
      action: 'ModelRun',
      user: 'admin',
      detail: 'Executed AI pipeline batch on 64 orthomosaic tiles',
      time: '6h ago',
      icon: Cpu,
      color: 'text-purple-600',
      bgColor: 'bg-purple-50',
    },
    {
      action: 'Export',
      user: 'admin',
      detail: 'Generated ESRI Shapefile archive with companion files (.prj, .shp)',
      time: '1d ago',
      icon: Download,
      color: 'text-text-secondary',
      bgColor: 'bg-gray-100',
    },
  ];

  return (
    <div className="aakar-card p-6 bg-bg-primary h-full">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-base font-semibold text-text-primary">Recent Audit Trail</h3>
        <span className="text-xs text-text-muted">DoLR Central Registry</span>
      </div>

      <div className="space-y-4">
        {activities.map((item, idx) => {
          const Icon = item.icon;
          return (
            <div key={idx} className="flex items-start gap-3">
              <div className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 ${item.bgColor} ${item.color}`}>
                <Icon className="w-4 h-4" />
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-xs font-semibold text-text-primary leading-tight">{item.detail}</p>
                <div className="flex items-center gap-2 mt-1 text-[11px] text-text-muted">
                  <span className="font-medium text-text-secondary">{item.user}</span>
                  <span>•</span>
                  <span>{item.time}</span>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
