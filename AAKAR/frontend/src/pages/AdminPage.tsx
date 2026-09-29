import React, { useState } from 'react';
import { Users, UserPlus, Settings, ShieldCheck, History, Sliders, X } from 'lucide-react';
import { Role } from '../types';

export const AdminPage: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'users' | 'settings' | 'logs'>('users');
  const [showInviteModal, setShowInviteModal] = useState(false);
  const [inviteEmail, setInviteEmail] = useState('');
  const [inviteRole, setInviteRole] = useState<Role>('Viewer');

  const [users, setUsers] = useState([
    { id: '1', username: 'admin', email: 'admin@aakar.gov.in', role: 'Administrator', created: '2026-09-01' },
    { id: '2', username: 'reviewer', email: 'reviewer@aakar.gov.in', role: 'Reviewer', created: '2026-09-05' },
    { id: '3', username: 'editor', email: 'editor@aakar.gov.in', role: 'Editor', created: '2026-09-10' },
    { id: '4', username: 'viewer', email: 'viewer@aakar.gov.in', role: 'Viewer', created: '2026-09-12' },
  ]);

  const [manualBaseline, setManualBaseline] = useState(48.0);
  const [highConfThreshold, setHighConfThreshold] = useState(0.85);

  const handleRoleChange = (userId: string, newRole: Role) => {
    setUsers((prev) =>
      prev.map((u) => (u.id === userId ? { ...u, role: newRole } : u))
    );
  };

  const handleInviteSubmit = () => {
    if (!inviteEmail.trim()) return;
    setUsers((prev) => [
      ...prev,
      {
        id: String(prev.length + 1),
        username: inviteEmail.split('@')[0],
        email: inviteEmail,
        role: inviteRole,
        created: '2026-09-29',
      },
    ]);
    setShowInviteModal(false);
    setInviteEmail('');
  };

  return (
    <div className="p-8 space-y-6 max-w-[1440px] mx-auto">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-2 border-b border-border-ui">
        <div>
          <span className="text-xs font-bold text-accent uppercase tracking-wider">
            System Governance & Control
          </span>
          <h2 className="text-2xl font-bold text-text-primary tracking-tight mt-0.5">
            Platform Administration & Audit Records
          </h2>
          <p className="text-sm text-text-secondary">
            Manage authorized state surveyors, tune algorithmic baseline parameters, and review system audit logs
          </p>
        </div>

        <button
          onClick={() => setShowInviteModal(true)}
          className="aakar-btn-primary text-xs flex items-center gap-1.5"
        >
          <UserPlus className="w-4 h-4" /> Invite User
        </button>
      </div>

      {/* Tabs */}
      <div className="flex gap-2 border-b border-border-ui pb-2 text-xs font-medium">
        <button
          onClick={() => setActiveTab('users')}
          className={`px-3 py-1.5 rounded-lg transition-colors flex items-center gap-1.5 ${
            activeTab === 'users' ? 'bg-accent text-white font-semibold' : 'text-text-secondary hover:bg-bg-subtle'
          }`}
        >
          <Users className="w-4 h-4" /> User Management
        </button>
        <button
          onClick={() => setActiveTab('settings')}
          className={`px-3 py-1.5 rounded-lg transition-colors flex items-center gap-1.5 ${
            activeTab === 'settings' ? 'bg-accent text-white font-semibold' : 'text-text-secondary hover:bg-bg-subtle'
          }`}
        >
          <Sliders className="w-4 h-4" /> System Calibration
        </button>
        <button
          onClick={() => setActiveTab('logs')}
          className={`px-3 py-1.5 rounded-lg transition-colors flex items-center gap-1.5 ${
            activeTab === 'logs' ? 'bg-accent text-white font-semibold' : 'text-text-secondary hover:bg-bg-subtle'
          }`}
        >
          <History className="w-4 h-4" /> Complete Audit Log
        </button>
      </div>

      {/* Tab 1: Users */}
      {activeTab === 'users' && (
        <div className="aakar-card overflow-hidden">
          <table className="w-full text-left border-collapse text-xs">
            <thead>
              <tr className="border-b border-border-ui bg-bg-subtle text-text-secondary font-semibold">
                <th className="py-3 px-4">User</th>
                <th className="py-3 px-4">Official Email</th>
                <th className="py-3 px-4">Cadastral Role</th>
                <th className="py-3 px-4">Created Date</th>
                <th className="py-3 px-4 text-right">Role Assignment</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-border-ui">
              {users.map((u) => (
                <tr key={u.id} className="hover:bg-bg-subtle/50 transition-colors">
                  <td className="py-3 px-4 font-semibold text-text-primary">{u.username}</td>
                  <td className="py-3 px-4 font-mono text-text-secondary">{u.email}</td>
                  <td className="py-3 px-4">
                    <span
                      className={`aakar-badge ${
                        u.role === 'Administrator'
                          ? 'bg-purple-50 text-purple-600 font-bold'
                          : u.role === 'Reviewer'
                          ? 'bg-blue-50 text-accent font-semibold'
                          : u.role === 'Editor'
                          ? 'bg-emerald-50 text-success'
                          : 'bg-gray-100 text-text-muted'
                      }`}
                    >
                      {u.role}
                    </span>
                  </td>
                  <td className="py-3 px-4 font-mono text-text-muted">{u.created}</td>
                  <td className="py-3 px-4 text-right">
                    <select
                      value={u.role}
                      onChange={(e) => handleRoleChange(u.id, e.target.value as Role)}
                      className="p-1.5 bg-bg-secondary border border-border-ui rounded text-xs font-medium cursor-pointer"
                    >
                      <option value="Viewer">Viewer</option>
                      <option value="Editor">Editor</option>
                      <option value="Reviewer">Reviewer</option>
                      <option value="Administrator">Administrator</option>
                    </select>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* Tab 2: System Settings */}
      {activeTab === 'settings' && (
        <div className="aakar-card p-6 max-w-2xl space-y-6">
          <div>
            <h3 className="text-sm font-semibold text-text-primary">Operational Parameters</h3>
            <p className="text-xs text-text-secondary mt-0.5">
              These baseline variables drive the automated KPI benchmark calculations across all dashboards.
            </p>
          </div>

          <div className="space-y-4 text-xs">
            <div>
              <label className="font-medium text-text-primary block mb-1">
                Manual Survey Baseline (Hours per Hectare)
              </label>
              <div className="flex items-center gap-3">
                <input
                  type="number"
                  value={manualBaseline}
                  onChange={(e) => setManualBaseline(Number(e.target.value))}
                  className="w-32 p-2 border border-border-ui rounded-lg font-mono"
                />
                <span className="text-text-muted">Standard DoLR conventional theodolite rate (default: 48h/ha)</span>
              </div>
            </div>

            <div>
              <label className="font-medium text-text-primary block mb-1">
                High Confidence Review Threshold: {(highConfThreshold * 100).toFixed(0)}%
              </label>
              <input
                type="range"
                min="0.7"
                max="0.95"
                step="0.05"
                value={highConfThreshold}
                onChange={(e) => setHighConfThreshold(Number(e.target.value))}
                className="w-full accent-accent"
              />
              <span className="text-[11px] text-text-muted">
                Parcels meeting this threshold bypass mandatory field ground-truthing.
              </span>
            </div>
          </div>
        </div>
      )}

      {/* Tab 3: Complete Audit Log */}
      {activeTab === 'logs' && (
        <div className="aakar-card overflow-hidden">
          <table className="w-full text-left border-collapse text-xs">
            <thead>
              <tr className="border-b border-border-ui bg-bg-subtle text-text-secondary font-semibold">
                <th className="py-2.5 px-4">Timestamp</th>
                <th className="py-2.5 px-4">User</th>
                <th className="py-2.5 px-4">Action</th>
                <th className="py-2.5 px-4">Feature Target</th>
                <th className="py-2.5 px-4">Details</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-border-ui font-mono text-[11px]">
              <tr className="hover:bg-bg-subtle/50">
                <td className="py-2.5 px-4 text-text-muted">2026-09-29 11:20:14</td>
                <td className="py-2.5 px-4 text-text-primary font-bold">reviewer</td>
                <td className="py-2.5 px-4 text-success">Approve</td>
                <td className="py-2.5 px-4 text-accent">p-wagholi-001</td>
                <td className="py-2.5 px-4 text-text-secondary font-sans">Assigned ULPIN MH070300120001 (Confidence: 94%)</td>
              </tr>
              <tr className="hover:bg-bg-subtle/50">
                <td className="py-2.5 px-4 text-text-muted">2026-09-29 10:45:00</td>
                <td className="py-2.5 px-4 text-text-primary font-bold">editor</td>
                <td className="py-2.5 px-4 text-accent">Edit</td>
                <td className="py-2.5 px-4 text-accent">p-wagholi-003</td>
                <td className="py-2.5 px-4 text-text-secondary font-sans">Boundary adjusted to match physical fence</td>
              </tr>
              <tr className="hover:bg-bg-subtle/50">
                <td className="py-2.5 px-4 text-text-muted">2026-09-29 10:00:35</td>
                <td className="py-2.5 px-4 text-text-primary font-bold">admin</td>
                <td className="py-2.5 px-4 text-purple-600">ModelRun</td>
                <td className="py-2.5 px-4 text-accent">job-pune-sec4</td>
                <td className="py-2.5 px-4 text-text-secondary font-sans">Batch processed 64 tiles in 35 seconds</td>
              </tr>
            </tbody>
          </table>
        </div>
      )}

      {/* Invite Modal */}
      {showInviteModal && (
        <div className="fixed inset-0 bg-text-primary/60 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-bg-primary rounded-xl max-w-md w-full p-6 shadow-2xl border border-border-ui space-y-4">
            <div className="flex items-center justify-between pb-3 border-b border-border-ui">
              <h3 className="font-bold text-text-primary text-base">Invite Cadastral Officer</h3>
              <button onClick={() => setShowInviteModal(false)} className="text-text-muted hover:text-text-primary">
                <X className="w-4 h-4" />
              </button>
            </div>

            <div className="space-y-3 text-xs">
              <div>
                <label className="text-text-secondary font-medium block mb-1">Email Address</label>
                <input
                  type="email"
                  value={inviteEmail}
                  onChange={(e) => setInviteEmail(e.target.value)}
                  placeholder="officer@nic.in or state portal"
                  className="w-full p-2.5 border border-border-ui rounded-lg focus:outline-none focus:border-accent"
                />
              </div>

              <div>
                <label className="text-text-secondary font-medium block mb-1">Assign Initial Role</label>
                <select
                  value={inviteRole}
                  onChange={(e) => setInviteRole(e.target.value as Role)}
                  className="w-full p-2.5 border border-border-ui rounded-lg bg-bg-secondary"
                >
                  <option value="Viewer">Viewer (Read-only)</option>
                  <option value="Editor">Editor (Geometry & attribute updates)</option>
                  <option value="Reviewer">Reviewer (Approval gate authority)</option>
                  <option value="Administrator">Administrator (Full authority)</option>
                </select>
              </div>
            </div>

            <div className="flex justify-end gap-2 pt-3 border-t border-border-ui">
              <button onClick={() => setShowInviteModal(false)} className="aakar-btn-secondary text-xs">
                Cancel
              </button>
              <button onClick={handleInviteSubmit} className="aakar-btn-primary text-xs">
                Send Invitation
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
