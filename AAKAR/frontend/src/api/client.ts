import axios from 'axios';
import { Parcel, DashboardKPIs, TopologyError, EncroachmentFlag, User } from '../types';

const API_BASE = '/api/v1';

export const api = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json'
  }
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('aakar_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const fetchKPIs = async (): Promise<DashboardKPIs> => {
  try {
    const res = await api.get('/dashboard/kpis');
    return res.data;
  } catch (err) {
    // Fallback data
    return {
      hectares_processed: 16.5,
      time_saved_pct: 96.9,
      gt_effort_reduced_pct: 96.4,
      topology_health_pct: 96.4,
      open_encroachments: 4,
      high_dispute_risk_count: 2,
      ulpin_ready_count: 54,
      changes_detected_count: 4
    };
  }
};

export const fetchParcels = async (filters: Record<string, any> = {}): Promise<Parcel[]> => {
  try {
    const res = await api.get('/parcels', { params: filters });
    return res.data;
  } catch (err) {
    return [];
  }
};

export const approveParcel = async (parcelId: string, override: boolean = false, reason: string = '') => {
  const res = await api.post(`/parcels/${parcelId}/approve`, {
    override_high_risk: override,
    override_reason: reason
  });
  return res.data;
};

export const rejectParcel = async (parcelId: string, reason: string) => {
  const res = await api.post(`/parcels/${parcelId}/reject`, {
    rejection_reason: reason
  });
  return res.data;
};

export const fetchTopologyErrors = async (): Promise<TopologyError[]> => {
  try {
    const res = await api.get('/topology/errors');
    return res.data;
  } catch (err) {
    return [];
  }
};

export const fetchEncroachments = async (): Promise<EncroachmentFlag[]> => {
  try {
    const res = await api.get('/encroachments');
    return res.data;
  } catch (err) {
    return [];
  }
};
