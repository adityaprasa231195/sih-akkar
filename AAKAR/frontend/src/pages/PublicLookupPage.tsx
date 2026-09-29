import React, { useState } from 'react';
import { Search, Download, CheckCircle2, MapPin, Building, Calendar, ShieldCheck } from 'lucide-react';
import { api } from '../api/client';

export const PublicLookupPage: React.FC = () => {
  const [query, setQuery] = useState('MH070300120001');
  const [result, setResult] = useState<any | null>({
    ulpin: 'MH070300120001',
    area_sqm: 684.5,
    land_use_class: 'Residential',
    validation_status: 'Approved',
    last_approved_date: '2026-09-29',
    state: 'Maharashtra',
    district: 'Pune',
    taluka: 'Haveli',
    village: 'Wagholi',
  });
  const [isSearching, setIsSearching] = useState(false);
  const [notFound, setNotFound] = useState(false);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;
    setIsSearching(true);
    setNotFound(false);

    try {
      const res = await api.get(`/public/parcel/${query.trim()}`);
      setResult(res.data);
    } catch (err) {
      // Try search query endpoint
      try {
        const searchRes = await api.get(`/public/parcel/search?q=${query.trim()}`);
        if (searchRes.data && searchRes.data.length > 0) {
          setResult(searchRes.data[0]);
        } else {
          setResult(null);
          setNotFound(true);
        }
      } catch (e) {
        setResult(null);
        setNotFound(true);
      }
    } finally {
      setIsSearching(false);
    }
  };

  const handleDownloadPDF = () => {
    const content = `
AAKAR CITIZEN CADASTRAL SUMMARY
Department of Land Resources, Ministry of Rural Development, Govt of India
========================================================================
ULPIN: ${result.ulpin}
Village: ${result.village}, Taluka: ${result.taluka}, District: ${result.district}, State: ${result.state}
Area: ${result.area_sqm} m²
Land Use Classification: ${result.land_use_class}
Cadastral Validation Status: ${result.validation_status}
Approved Date: ${result.last_approved_date}
Geo-Anchor Coordinate: WGS84 EPSG:4326
========================================================================
Verified via AAKAR Automated Cadastral Platform
`;
    const blob = new Blob([content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `AAKAR_Parcel_${result.ulpin}.txt`;
    a.click();
  };

  return (
    <div className="min-h-screen bg-bg-secondary flex flex-col justify-between">
      {/* Public Top Banner */}
      <header className="bg-bg-primary border-b border-border-ui py-4 px-6">
        <div className="max-w-5xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-lg bg-accent text-white flex items-center justify-center font-bold text-lg">
              आ
            </div>
            <div>
              <h1 className="text-base font-bold text-text-primary tracking-tight">AAKAR Citizen Portal</h1>
              <p className="text-[11px] text-text-muted">
                Ministry of Rural Development · Dept of Land Resources (DoLR)
              </p>
            </div>
          </div>
          <span className="text-xs bg-emerald-50 text-success border border-emerald-200 px-2.5 py-1 rounded-full font-medium flex items-center gap-1">
            <ShieldCheck className="w-3.5 h-3.5" /> Official Land Record Verification
          </span>
        </div>
      </header>

      {/* Main Search Body */}
      <main className="flex-1 max-w-4xl w-full mx-auto p-6 space-y-8 my-auto">
        <div className="text-center space-y-2">
          <h2 className="text-3xl font-extrabold text-text-primary tracking-tight">
            Mapping Every Corner of India
          </h2>
          <p className="text-sm text-text-secondary max-w-lg mx-auto">
            Search verified land parcels by 14-character Bhu-Aadhaar (ULPIN) ID or registered village location
          </p>
        </div>

        {/* Large Rounded Search Bar */}
        <form onSubmit={handleSearch} className="relative max-w-2xl mx-auto">
          <div className="relative flex items-center">
            <Search className="w-5 h-5 text-accent absolute left-4" />
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Enter ULPIN (e.g. MH070300120001) or Village Name..."
              className="w-full pl-12 pr-32 py-3.5 bg-bg-primary border-2 border-border-ui focus:border-accent rounded-full text-sm font-medium focus:outline-none shadow-sm"
            />
            <button
              type="submit"
              disabled={isSearching}
              className="absolute right-2 aakar-btn-primary rounded-full py-2 px-6 text-xs font-semibold"
            >
              {isSearching ? 'Searching...' : 'Lookup'}
            </button>
          </div>
          <p className="text-[11px] text-text-muted text-center mt-2">
            Try demo ULPIN: <span className="font-mono text-accent cursor-pointer" onClick={() => setQuery('MH070300120001')}>MH070300120001</span> or <span className="font-mono text-accent cursor-pointer" onClick={() => setQuery('MH070300120002')}>MH070300120002</span>
          </p>
        </form>

        {/* Search Results Card */}
        {result && (
          <div className="aakar-card p-6 bg-bg-primary border border-border-ui shadow-lg space-y-6 max-w-2xl mx-auto">
            <div className="flex items-center justify-between pb-3 border-b border-border-ui">
              <div>
                <span className="text-[11px] font-bold text-text-muted uppercase tracking-wider">
                  Verified ULPIN Record
                </span>
                <h3 className="text-xl font-bold font-mono text-accent mt-0.5">{result.ulpin}</h3>
              </div>
              <span className="aakar-badge bg-emerald-50 text-success text-xs font-semibold flex items-center gap-1">
                <CheckCircle2 className="w-3.5 h-3.5" /> Approved Cadastre
              </span>
            </div>

            {/* Read-Only Geometry Map Representation */}
            <div className="h-44 bg-bg-secondary rounded-xl border border-border-ui relative flex items-center justify-center overflow-hidden">
              <svg className="w-full h-full p-4" viewBox="0 0 100 100">
                <polygon points="20,20 80,20 80,80 20,80" fill="rgba(37, 99, 235, 0.15)" stroke="#2563EB" strokeWidth="2.5" />
                <circle cx="50" cy="50" r="3" fill="#2563EB" />
              </svg>
              <div className="absolute bottom-2 right-2 bg-white/95 px-2 py-0.5 rounded text-[10px] font-mono text-text-muted">
                EPSG:4326 · Centroid (18.5804, 73.9804)
              </div>
            </div>

            {/* Public Attributes Grid (Privacy protected) */}
            <div className="grid grid-cols-2 sm:grid-cols-3 gap-3 text-xs">
              <div className="p-3 bg-bg-subtle rounded-lg">
                <span className="text-text-muted flex items-center gap-1">
                  <MapPin className="w-3 h-3" /> Location
                </span>
                <p className="font-semibold text-text-primary mt-1">
                  {result.village}, {result.taluka}
                </p>
                <p className="text-[10px] text-text-muted">{result.district}, {result.state}</p>
              </div>

              <div className="p-3 bg-bg-subtle rounded-lg">
                <span className="text-text-muted flex items-center gap-1">
                  <Building className="w-3 h-3" /> Land Use
                </span>
                <p className="font-semibold text-text-primary mt-1">{result.land_use_class}</p>
                <p className="text-[10px] text-text-muted">Cadastral zoning</p>
              </div>

              <div className="p-3 bg-bg-subtle rounded-lg">
                <span className="text-text-muted flex items-center gap-1">
                  <Calendar className="w-3 h-3" /> Approved Date
                </span>
                <p className="font-semibold text-text-primary mt-1">{result.last_approved_date}</p>
                <p className="text-[10px] text-text-muted">Surveyor sign-off</p>
              </div>
            </div>

            <div className="pt-2 flex justify-between items-center text-xs">
              <span className="text-text-muted">Area: <strong className="text-text-primary">{result.area_sqm} m²</strong></span>
              <button
                onClick={handleDownloadPDF}
                className="aakar-btn-secondary text-xs flex items-center gap-1.5"
              >
                <Download className="w-3.5 h-3.5 text-accent" />
                <span>Download Cadastral Certificate</span>
              </button>
            </div>
          </div>
        )}

        {notFound && (
          <div className="text-center p-8 bg-bg-primary rounded-xl border border-border-ui max-w-md mx-auto space-y-2">
            <p className="font-bold text-text-primary text-sm">No registered parcel found</p>
            <p className="text-xs text-text-muted">
              Check the 14-character ULPIN ID or contact the local Taluka land records officer.
            </p>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="bg-bg-primary border-t border-border-ui py-4 text-center text-xs text-text-muted">
        <p>DoLR Government of India · Digital India Land Records Modernization Programme</p>
      </footer>
    </div>
  );
};
