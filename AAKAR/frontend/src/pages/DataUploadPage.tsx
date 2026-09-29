import React, { useState } from 'react';
import {
  UploadCloud,
  FileCheck,
  CheckCircle2,
  Camera,
  Layers,
  MapPin,
  Compass,
  ArrowRight,
  ArrowLeft
} from 'lucide-react';

export const DataUploadPage: React.FC = () => {
  const [currentStep, setCurrentStep] = useState<number>(1);
  const [selectedType, setSelectedType] = useState<string>('Drone Imagery');
  const [file, setFile] = useState<{ name: string; size: string; crs: string } | null>({
    name: 'Wagholi_Sector4_Drone_Orthomosaic.tif',
    size: '142.6 MB',
    crs: 'EPSG:4326 (WGS 84)',
  });
  const [isIngesting, setIsIngesting] = useState(false);
  const [ingestComplete, setIngestComplete] = useState(false);

  const dataTypes = [
    { title: 'Drone Imagery', desc: 'Raw high-res aerial imagery (GeoTIFF, JPEG2000)', icon: Camera },
    { title: 'ORI (Orthorectified)', desc: 'Orthorectified photogrammetric raster', icon: Layers },
    { title: 'DSM Raster', desc: 'Digital Surface Model containing object heights', icon: Layers },
    { title: 'DTM Raster', desc: 'Digital Terrain Model for nDSM computation', icon: Layers },
    { title: 'GIS Parcel Layer', desc: 'Existing cadastral boundary vectors (Shapefile/GeoJSON)', icon: MapPin },
    { title: 'Ground Truth Data', desc: 'Field verified survey checkpoints and vectors', icon: Compass },
    { title: 'GNSS / CORS Points', desc: 'High-precision RTK rover survey points', icon: MapPin },
  ];

  const handleStartIngest = () => {
    setIsIngesting(true);
    setTimeout(() => {
      setIsIngesting(false);
      setIngestComplete(true);
    }, 2000);
  };

  return (
    <div className="p-8 space-y-8 max-w-[1000px] mx-auto">
      {/* Header */}
      <div className="pb-2 border-b border-border-ui">
        <span className="text-xs font-bold text-accent uppercase tracking-wider">
          Layer 1 Ingestion Pipeline
        </span>
        <h2 className="text-2xl font-bold text-text-primary tracking-tight mt-0.5">
          Cadastral Data Ingestion & CRS Normalization
        </h2>
        <p className="text-sm text-text-secondary">
          Upload multi-source drone rasters, LiDAR elevation models, and existing vector cadastre
        </p>
      </div>

      {/* 3-Step Stepper Header */}
      <div className="flex items-center justify-between relative">
        <div className="absolute top-1/2 left-0 right-0 h-0.5 bg-border-ui -translate-y-1/2 z-0" />

        {[
          { num: 1, label: 'Select Data Type' },
          { num: 2, label: 'Upload & Validate' },
          { num: 3, label: 'Confirm & Ingest' },
        ].map((s) => {
          const isDone = currentStep > s.num;
          const isCurrent = currentStep === s.num;
          return (
            <div key={s.num} className="relative z-10 flex flex-col items-center bg-bg-secondary px-3">
              <div
                className={`w-9 h-9 rounded-full flex items-center justify-center font-bold text-xs transition-colors ${
                  isDone
                    ? 'bg-success text-white'
                    : isCurrent
                    ? 'bg-accent text-white shadow-md'
                    : 'bg-white border-2 border-border-ui text-text-muted'
                }`}
              >
                {isDone ? <CheckCircle2 className="w-5 h-5" /> : s.num}
              </div>
              <span className={`text-xs mt-2 font-medium ${isCurrent ? 'text-accent font-semibold' : 'text-text-secondary'}`}>
                {s.label}
              </span>
            </div>
          );
        })}
      </div>

      {/* Step 1: Select Data Type */}
      {currentStep === 1 && (
        <div className="space-y-4">
          <h3 className="text-sm font-semibold text-text-primary">Step 1: Choose Dataset Category</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {dataTypes.map((dt) => {
              const Icon = dt.icon;
              const isSelected = selectedType === dt.title;
              return (
                <div
                  key={dt.title}
                  onClick={() => setSelectedType(dt.title)}
                  className={`aakar-card p-4 cursor-pointer transition-all ${
                    isSelected
                      ? 'border-accent bg-blue-50/40 ring-1 ring-accent'
                      : 'hover:bg-bg-subtle'
                  }`}
                >
                  <div className="flex items-start gap-3">
                    <div className={`p-2 rounded-lg ${isSelected ? 'bg-accent text-white' : 'bg-bg-subtle text-text-muted'}`}>
                      <Icon className="w-5 h-5" />
                    </div>
                    <div>
                      <h4 className="font-semibold text-xs text-text-primary">{dt.title}</h4>
                      <p className="text-[11px] text-text-secondary mt-0.5">{dt.desc}</p>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>

          <div className="flex justify-end pt-4">
            <button
              onClick={() => setCurrentStep(2)}
              className="aakar-btn-primary text-xs flex items-center gap-2"
            >
              Next Step <ArrowRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      )}

      {/* Step 2: Upload File & Validate */}
      {currentStep === 2 && (
        <div className="space-y-5">
          <h3 className="text-sm font-semibold text-text-primary">
            Step 2: Upload {selectedType} File
          </h3>

          <div className="border-2 border-dashed border-border-ui hover:border-accent rounded-2xl p-10 text-center bg-bg-primary transition-colors cursor-pointer">
            <UploadCloud className="w-10 h-10 text-accent mx-auto mb-3" />
            <h4 className="text-sm font-semibold text-text-primary">
              Drag & Drop GeoTIFF / Shapefile here
            </h4>
            <p className="text-xs text-text-muted mt-1">Maximum file size: 500 MB per batch</p>
          </div>

          {file && (
            <div className="p-4 bg-bg-primary rounded-xl border border-border-ui space-y-2">
              <div className="flex items-center justify-between text-xs">
                <span className="font-semibold text-text-primary">{file.name}</span>
                <span className="text-text-muted">{file.size}</span>
              </div>
              <div className="flex items-center gap-2 text-xs text-success">
                <FileCheck className="w-4 h-4" />
                <span>Client validation passed: CRS valid ({file.crs})</span>
              </div>
            </div>
          )}

          <div className="flex justify-between pt-4">
            <button
              onClick={() => setCurrentStep(1)}
              className="aakar-btn-secondary text-xs flex items-center gap-2"
            >
              <ArrowLeft className="w-4 h-4" /> Back
            </button>
            <button
              onClick={() => setCurrentStep(3)}
              className="aakar-btn-primary text-xs flex items-center gap-2"
            >
              Next: Review & Ingest <ArrowRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      )}

      {/* Step 3: Confirm & Ingest */}
      {currentStep === 3 && (
        <div className="space-y-5">
          <h3 className="text-sm font-semibold text-text-primary">
            Step 3: Verification & Ingestion Summary
          </h3>

          <div className="aakar-card p-5 overflow-hidden">
            <table className="w-full text-xs text-left">
              <tbody className="divide-y divide-border-ui">
                <tr>
                  <td className="py-2.5 text-text-muted font-medium w-40">Dataset Category:</td>
                  <td className="py-2.5 font-bold text-text-primary">{selectedType}</td>
                </tr>
                <tr>
                  <td className="py-2.5 text-text-muted font-medium">Source File:</td>
                  <td className="py-2.5 font-mono text-text-primary">{file?.name}</td>
                </tr>
                <tr>
                  <td className="py-2.5 text-text-muted font-medium">File Size:</td>
                  <td className="py-2.5 text-text-secondary">{file?.size}</td>
                </tr>
                <tr>
                  <td className="py-2.5 text-text-muted font-medium">Detected CRS:</td>
                  <td className="py-2.5 font-mono text-accent">{file?.crs}</td>
                </tr>
                <tr>
                  <td className="py-2.5 text-text-muted font-medium">Target Storage:</td>
                  <td className="py-2.5 text-text-secondary">PostGIS Spatial Database (EPSG:4326)</td>
                </tr>
              </tbody>
            </table>
          </div>

          {ingestComplete && (
            <div className="p-4 bg-emerald-50 border border-emerald-200 rounded-xl text-xs text-success flex items-center gap-2 font-medium">
              <CheckCircle2 className="w-5 h-5 shrink-0" />
              <span>Ingestion complete. Tiling and nDSM computation scheduled for AI inference.</span>
            </div>
          )}

          <div className="flex justify-between pt-4">
            <button
              onClick={() => setCurrentStep(2)}
              disabled={isIngesting}
              className="aakar-btn-secondary text-xs flex items-center gap-2"
            >
              <ArrowLeft className="w-4 h-4" /> Back
            </button>
            <button
              onClick={handleStartIngest}
              disabled={isIngesting || ingestComplete}
              className={`aakar-btn-primary text-xs ${
                isIngesting || ingestComplete ? 'opacity-50 cursor-not-allowed' : ''
              }`}
            >
              {isIngesting ? 'Ingesting Dataset...' : ingestComplete ? 'Dataset Ingested' : 'Start Ingestion'}
            </button>
          </div>
        </div>
      )}
    </div>
  );
};
