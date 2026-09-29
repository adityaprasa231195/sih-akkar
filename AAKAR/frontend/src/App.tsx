import React, { useState } from 'react';
import { BrowserRouter, Routes, Route, Navigate, useLocation } from 'react-router-dom';
import { Sidebar } from './components/Sidebar';
import { Navbar } from './components/Navbar';
import { DashboardPage } from './pages/DashboardPage';
import { MapViewPage } from './pages/MapViewPage';
import { TopologyPage } from './pages/TopologyPage';
import { EncroachmentsPage } from './pages/EncroachmentsPage';
import { GroundTruthPage } from './pages/GroundTruthPage';
import { PipelinePage } from './pages/PipelinePage';
import { DataUploadPage } from './pages/DataUploadPage';
import { ChangeDetectionPage } from './pages/ChangeDetectionPage';
import { ExportPage } from './pages/ExportPage';
import { AdminPage } from './pages/AdminPage';
import { LoginPage } from './pages/LoginPage';
import { PublicLookupPage } from './pages/PublicLookupPage';
import { Role } from './types';

const Layout: React.FC<{
  currentRole: Role;
  onRoleChange: (r: Role) => void;
  currentUser: string;
  children: React.ReactNode;
}> = ({ currentRole, onRoleChange, currentUser, children }) => {
  const location = useLocation();
  const isPublic = location.pathname === '/lookup' || location.pathname === '/login';

  if (isPublic) {
    return <>{children}</>;
  }

  return (
    <div className="min-h-screen bg-bg-secondary flex">
      <Sidebar />
      <div className="flex-1 flex flex-col min-w-0">
        <Navbar
          currentRole={currentRole}
          onRoleChange={onRoleChange}
          currentUser={currentUser}
        />
        <main className="flex-1 ml-[260px]">{children}</main>
      </div>
    </div>
  );
};

export const App: React.FC = () => {
  const [currentRole, setCurrentRole] = useState<Role>('Reviewer');
  const [currentUser, setCurrentUser] = useState<string>('reviewer');

  const handleLogin = (role: Role, uname: string) => {
    setCurrentRole(role);
    setCurrentUser(uname);
    localStorage.setItem('aakar_token', `mock_token_${uname}`);
  };

  return (
    <BrowserRouter>
      <Layout
        currentRole={currentRole}
        onRoleChange={setCurrentRole}
        currentUser={currentUser}
      >
        <Routes>
          <Route path="/" element={<DashboardPage />} />
          <Route path="/map" element={<MapViewPage userRole={currentRole} />} />
          <Route path="/topology" element={<TopologyPage />} />
          <Route path="/encroachments" element={<EncroachmentsPage />} />
          <Route path="/groundtruth" element={<GroundTruthPage />} />
          <Route path="/pipeline" element={<PipelinePage />} />
          <Route path="/upload" element={<DataUploadPage />} />
          <Route path="/changedetection" element={<ChangeDetectionPage />} />
          <Route path="/export" element={<ExportPage />} />
          <Route path="/admin" element={<AdminPage />} />
          <Route path="/login" element={<LoginPage onLogin={handleLogin} />} />
          <Route path="/lookup" element={<PublicLookupPage />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </Layout>
    </BrowserRouter>
  );
};

export default App;
