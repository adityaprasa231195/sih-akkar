import React from 'react';
import { NavLink } from 'react-router-dom';
import {
  LayoutDashboard,
  Map,
  AlertTriangle,
  ShieldAlert,
  Compass,
  Cpu,
  UploadCloud,
  History,
  Download,
  Users,
  Search,
  ExternalLink
} from 'lucide-react';

export const Sidebar: React.FC = () => {
  const navItems = [
    { name: 'Dashboard', path: '/', icon: LayoutDashboard },
    { name: 'Web-GIS Map', path: '/map', icon: Map },
    { name: 'Topology Errors', path: '/topology', icon: AlertTriangle },
    { name: 'Encroachments', path: '/encroachments', icon: ShieldAlert },
    { name: 'Ground Truthing', path: '/groundtruth', icon: Compass },
    { name: 'Pipeline Control', path: '/pipeline', icon: Cpu },
    { name: 'Data Upload', path: '/upload', icon: UploadCloud },
    { name: 'Change Detection', path: '/changedetection', icon: History },
    { name: 'Export', path: '/export', icon: Download },
    { name: 'Admin', path: '/admin', icon: Users },
  ];

  return (
    <aside className="w-[260px] bg-bg-secondary border-r border-border-ui flex flex-col h-screen fixed left-0 top-0 z-20">
      {/* Brand Header */}
      <div className="p-5 border-b border-border-ui bg-bg-primary">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-lg bg-accent text-white flex items-center justify-center font-bold text-lg">
            आ
          </div>
          <div>
            <h1 className="font-bold text-lg text-text-primary tracking-tight leading-none">AAKAR</h1>
            <p className="text-[11px] text-text-secondary mt-1">Ministry of Rural Dev · DoLR</p>
          </div>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 px-3 py-4 space-y-1 overflow-y-auto">
        {navItems.map((item) => {
          const Icon = item.icon;
          return (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) =>
                `flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors ${
                  isActive
                    ? 'text-accent bg-bg-subtle font-semibold'
                    : 'text-text-secondary hover:text-text-primary hover:bg-bg-subtle'
                }`
              }
            >
              <Icon className="w-4 h-4" />
              <span>{item.name}</span>
            </NavLink>
          );
        })}

        <div className="pt-4 border-t border-border-ui mt-4">
          <NavLink
            to="/lookup"
            target="_blank"
            className="flex items-center justify-between px-3 py-2.5 rounded-lg text-sm font-medium text-text-secondary hover:text-accent hover:bg-bg-subtle transition-colors"
          >
            <div className="flex items-center gap-3">
              <Search className="w-4 h-4 text-accent" />
              <span>Citizen Lookup</span>
            </div>
            <ExternalLink className="w-3.5 h-3.5 text-text-muted" />
          </NavLink>
        </div>
      </nav>

      {/* Footer Info */}
      <div className="p-4 border-t border-border-ui bg-bg-primary/50 text-[11px] text-text-muted">
        <p className="font-semibold text-text-secondary">AAKAR Cadastral v1.0</p>
        <p className="mt-0.5">EPSG:4326 · WGS84</p>
      </div>
    </aside>
  );
};
