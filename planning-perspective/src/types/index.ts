import type { Map as OLMap } from 'ol';
import type VectorLayer from 'ol/layer/Vector';
import type VectorSource from 'ol/source/Vector';

export interface SearchResult {
  label: string;
  lon: number;
  lat: number;
  bbox?: [number, number, number, number];
}

export interface LayerConfig {
  id: string;
  name: string;
  type: 'wms' | 'wfs' | 'rest';
  url: string;
  layerName?: string;
  visible: boolean;
  opacity: number;
  color: string;
  category: string;
  apiKey?: string;
  params?: Record<string, string>;
}

export interface DrawingTool {
  id: string;
  label: string;
  icon: string;
  type: 'Circle' | 'Box' | 'Polygon' | 'Freehand';
}

export interface MapContextType {
  map: OLMap | null;
  drawLayer: VectorLayer<VectorSource> | null;
  layers: LayerConfig[];
  setLayers: React.Dispatch<React.SetStateAction<LayerConfig[]>>;
  activeDrawTool: string | null;
  setActiveDrawTool: React.Dispatch<React.SetStateAction<string | null>>;
  searchResult: SearchResult | null;
  setSearchResult: React.Dispatch<React.SetStateAction<SearchResult | null>>;
}

export interface AppConfig {
  osApiKey: string;
  defaultCenter: [number, number]; // [lon, lat] in EPSG:4326
  defaultZoom: number;
}
