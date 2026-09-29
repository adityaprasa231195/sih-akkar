import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Role } from '../types';
import { Lock, Mail, ArrowRight } from 'lucide-react';

interface LoginPageProps {
  onLogin: (role: Role, username: string) => void;
}

export const LoginPage: React.FC<LoginPageProps> = ({ onLogin }) => {
  const navigate = useNavigate();
  const [username, setUsername] = useState('reviewer');
  const [password, setPassword] = useState('reviewer123');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    let assignedRole: Role = 'Reviewer';
    if (username.includes('admin')) assignedRole = 'Administrator';
    else if (username.includes('editor')) assignedRole = 'Editor';
    else if (username.includes('viewer')) assignedRole = 'Viewer';

    onLogin(assignedRole, username);
    navigate('/');
  };

  const handleQuickLogin = (role: Role, uname: string) => {
    onLogin(role, uname);
    navigate('/');
  };

  return (
    <div className="min-h-screen bg-bg-secondary flex flex-col justify-center items-center p-4">
      {/* Centered Login Card */}
      <div className="w-full max-w-[400px] aakar-card p-8 bg-bg-primary shadow-xl border border-border-ui space-y-6">
        {/* Brand Wordmark */}
        <div className="text-center space-y-1">
          <div className="w-12 h-12 rounded-xl bg-accent text-white flex items-center justify-center font-bold text-2xl mx-auto shadow-md">
            आ
          </div>
          <h1 className="text-2xl font-bold text-accent tracking-tight pt-2">AAKAR</h1>
          <p className="text-xs text-text-muted">
            Ministry of Rural Development · Dept of Land Resources (DoLR)
          </p>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="space-y-4 text-xs">
          <div>
            <label className="font-semibold text-text-primary block mb-1">Surveyor ID / Email</label>
            <div className="relative">
              <Mail className="w-4 h-4 text-text-muted absolute left-3 top-1/2 -translate-y-1/2" />
              <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
                className="w-full pl-9 pr-3 py-2.5 border border-border-ui rounded-lg focus:outline-none focus:border-accent text-xs"
              />
            </div>
          </div>

          <div>
            <label className="font-semibold text-text-primary block mb-1">Password</label>
            <div className="relative">
              <Lock className="w-4 h-4 text-text-muted absolute left-3 top-1/2 -translate-y-1/2" />
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                className="w-full pl-9 pr-3 py-2.5 border border-border-ui rounded-lg focus:outline-none focus:border-accent text-xs"
              />
            </div>
          </div>

          <button
            type="submit"
            className="w-full aakar-btn-primary py-2.5 text-xs font-semibold flex items-center justify-center gap-2 mt-2"
          >
            <span>Sign In to Cadastral Console</span>
            <ArrowRight className="w-4 h-4" />
          </button>
        </form>

        {/* Demo Fast-Switch Buttons */}
        <div className="pt-4 border-t border-border-ui text-center">
          <span className="text-[11px] text-text-muted font-medium block mb-2">
            Prototype Demo Access:
          </span>
          <div className="grid grid-cols-2 gap-1.5 text-[11px]">
            <button
              onClick={() => handleQuickLogin('Reviewer', 'reviewer')}
              className="py-1 px-2 rounded border border-border-ui hover:bg-bg-subtle font-medium text-accent"
            >
              Reviewer (Approve)
            </button>
            <button
              onClick={() => handleQuickLogin('Administrator', 'admin')}
              className="py-1 px-2 rounded border border-border-ui hover:bg-bg-subtle font-medium text-purple-600"
            >
              Administrator
            </button>
            <button
              onClick={() => handleQuickLogin('Editor', 'editor')}
              className="py-1 px-2 rounded border border-border-ui hover:bg-bg-subtle font-medium text-success"
            >
              Editor
            </button>
            <button
              onClick={() => handleQuickLogin('Viewer', 'viewer')}
              className="py-1 px-2 rounded border border-border-ui hover:bg-bg-subtle font-medium text-text-muted"
            >
              Viewer (Read-only)
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
