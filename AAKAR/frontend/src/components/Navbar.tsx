import React from 'react';
import { User, LogOut, CheckCircle, Shield } from 'lucide-react';
import { Role } from '../types';

interface NavbarProps {
  currentRole: Role;
  onRoleChange: (role: Role) => void;
  currentUser: string;
}

export const Navbar: React.FC<NavbarProps> = ({ currentRole, onRoleChange, currentUser }) => {
  const roles: Role[] = ['Administrator', 'Reviewer', 'Editor', 'Viewer'];

  return (
    <header className="h-16 bg-bg-primary border-b border-border-ui px-6 flex items-center justify-between sticky top-0 z-10 ml-[260px]">
      <div className="flex items-center gap-3">
        <span className="text-xs font-semibold text-text-muted uppercase tracking-wider">PROJECT:</span>
        <span className="text-sm font-semibold text-text-primary">Village Dive Gaothan Survey — Gram Panchayat Dive, Block Purandar</span>
        <span className="aakar-badge bg-emerald-50 text-success text-[11px] flex items-center gap-1">
          <CheckCircle className="w-3 h-3" /> SVAMITVA Cadastre Active
        </span>
      </div>

      <div className="flex items-center gap-4">
        {/* Role Switcher for prototype evaluation */}
        <div className="flex items-center gap-2 bg-bg-secondary px-3 py-1.5 rounded-lg border border-border-ui">
          <Shield className="w-3.5 h-3.5 text-accent" />
          <span className="text-xs text-text-secondary font-medium">Role:</span>
          <select
            value={currentRole}
            onChange={(e) => onRoleChange(e.target.value as Role)}
            className="text-xs font-semibold bg-transparent text-text-primary focus:outline-none cursor-pointer"
          >
            {roles.map((r) => (
              <option key={r} value={r}>
                {r}
              </option>
            ))}
          </select>
        </div>

        {/* User Badge */}
        <div className="flex items-center gap-2 pl-2 border-l border-border-ui">
          <div className="w-8 h-8 rounded-full bg-accent/10 text-accent flex items-center justify-center font-bold text-xs">
            {currentUser.charAt(0).toUpperCase()}
          </div>
          <div className="text-left">
            <p className="text-xs font-semibold text-text-primary">{currentUser}</p>
            <p className="text-[10px] text-text-muted">{currentRole}</p>
          </div>
        </div>

        <button
          title="Sign out"
          onClick={() => {
            localStorage.removeItem('aakar_token');
            window.location.reload();
          }}
          className="p-1.5 text-text-muted hover:text-danger rounded-lg hover:bg-bg-subtle transition-colors"
        >
          <LogOut className="w-4 h-4" />
        </button>
      </div>
    </header>
  );
};
