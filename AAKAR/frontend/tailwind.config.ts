import type { Config } from 'tailwindcss';

export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        'bg-primary': '#FFFFFF',
        'bg-secondary': '#F7F8FA',
        'bg-subtle': '#EFF1F5',
        'border-ui': '#E4E7EC',
        'text-primary': '#111827',
        'text-secondary': '#6B7280',
        'text-muted': '#9CA3AF',
        'accent': '#2563EB',
        'accent-hover': '#1D4ED8',
        'success': '#16A34A',
        'warning': '#D97706',
        'danger': '#DC2626',
        'info': '#0891B2',
        'map-parcel': '#2563EB',
        'map-building': '#7C3AED',
        'map-road': '#374151',
        'map-encroach': '#DC2626',
        'map-high-conf': '#16A34A',
        'map-mid-conf': '#D97706',
        'map-low-conf': '#DC2626'
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace']
      },
      borderRadius: {
        'card': '12px',
        'btn': '8px',
        'input': '8px'
      }
    }
  },
  plugins: []
} satisfies Config;
