import type { AppConfig, LayerConfig } from '../types';

export const APP_CONFIG: AppConfig = {
  osApiKey: import.meta.env.VITE_OS_API_KEY || '',
  defaultCenter: [-1.5, 53.0], // Centre of England
  defaultZoom: 7,
};

// Pre-configured planning data layers
// URLs and API keys to be provided by user - these are placeholder configurations
export const DEFAULT_LAYERS: LayerConfig[] = [
  {
    id: 'planning-applications',
    name: 'Planning Applications',
    type: 'wfs',
    url: '',
    layerName: 'planning_applications',
    visible: true,
    opacity: 0.8,
    color: '#e74c3c',
    category: 'Planning',
  },
  {
    id: 'listed-buildings',
    name: 'Listed Buildings',
    type: 'wms',
    url: '',
    layerName: 'listed_buildings',
    visible: true,
    opacity: 0.7,
    color: '#f39c12',
    category: 'Heritage',
  },
  {
    id: 'conservation-areas',
    name: 'Conservation Areas',
    type: 'wms',
    url: '',
    layerName: 'conservation_areas',
    visible: true,
    opacity: 0.5,
    color: '#27ae60',
    category: 'Heritage',
  },
  {
    id: 'flood-zones',
    name: 'Flood Zones',
    type: 'wms',
    url: '',
    layerName: 'flood_zones',
    visible: false,
    opacity: 0.5,
    color: '#3498db',
    category: 'Environment',
  },
  {
    id: 'green-belt',
    name: 'Green Belt',
    type: 'wms',
    url: '',
    layerName: 'green_belt',
    visible: false,
    opacity: 0.4,
    color: '#2ecc71',
    category: 'Environment',
  },
  {
    id: 'tree-preservation',
    name: 'Tree Preservation Orders',
    type: 'wfs',
    url: '',
    layerName: 'tree_preservation_orders',
    visible: false,
    opacity: 0.7,
    color: '#16a085',
    category: 'Environment',
  },
  {
    id: 'local-plan-allocations',
    name: 'Local Plan Allocations',
    type: 'wms',
    url: '',
    layerName: 'local_plan_allocations',
    visible: false,
    opacity: 0.6,
    color: '#9b59b6',
    category: 'Planning',
  },
  {
    id: 'article4-directions',
    name: 'Article 4 Directions',
    type: 'wms',
    url: '',
    layerName: 'article4_directions',
    visible: false,
    opacity: 0.6,
    color: '#e67e22',
    category: 'Planning',
  },
];

export const LAYER_CATEGORIES = ['Planning', 'Heritage', 'Environment'] as const;
