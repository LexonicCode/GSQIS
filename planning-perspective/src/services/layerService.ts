import TileLayer from 'ol/layer/Tile';
import TileWMS from 'ol/source/TileWMS';
import VectorLayer from 'ol/layer/Vector';
import VectorSource from 'ol/source/Vector';
import GeoJSON from 'ol/format/GeoJSON';
import { bbox as bboxStrategy } from 'ol/loadingstrategy';
import { Style, Fill, Stroke, Circle as CircleStyle } from 'ol/style';
import type { LayerConfig } from '../types';

export function createWMSLayer(config: LayerConfig): TileLayer<TileWMS> {
  const params: Record<string, string> = {
    LAYERS: config.layerName || '',
    TILED: 'true',
    FORMAT: 'image/png',
    TRANSPARENT: 'true',
    ...config.params,
  };

  if (config.apiKey) {
    params['key'] = config.apiKey;
  }

  return new TileLayer({
    source: new TileWMS({
      url: config.url,
      params,
      serverType: 'geoserver',
      crossOrigin: 'anonymous',
    }),
    visible: config.visible,
    opacity: config.opacity,
    properties: { layerId: config.id },
  });
}

export function createWFSLayer(config: LayerConfig): VectorLayer<VectorSource> {
  const vectorSource = new VectorSource({
    format: new GeoJSON(),
    url: (extent) => {
      const baseUrl = config.url;
      const params = new URLSearchParams({
        service: 'WFS',
        version: '2.0.0',
        request: 'GetFeature',
        typeName: config.layerName || '',
        outputFormat: 'application/json',
        srsname: 'EPSG:3857',
        bbox: extent.join(',') + ',EPSG:3857',
        ...config.params,
      });
      if (config.apiKey) {
        params.set('key', config.apiKey);
      }
      return `${baseUrl}?${params.toString()}`;
    },
    strategy: bboxStrategy,
  });

  const color = config.color;

  return new VectorLayer({
    source: vectorSource,
    visible: config.visible,
    opacity: config.opacity,
    style: new Style({
      fill: new Fill({ color: hexToRgba(color, 0.3) }),
      stroke: new Stroke({ color, width: 2 }),
      image: new CircleStyle({
        radius: 6,
        fill: new Fill({ color: hexToRgba(color, 0.6) }),
        stroke: new Stroke({ color, width: 1.5 }),
      }),
    }),
    properties: { layerId: config.id },
  });
}

export function createRESTLayer(config: LayerConfig): VectorLayer<VectorSource> {
  const vectorSource = new VectorSource({
    format: new GeoJSON(),
    url: config.url,
    strategy: bboxStrategy,
  });

  const color = config.color;

  return new VectorLayer({
    source: vectorSource,
    visible: config.visible,
    opacity: config.opacity,
    style: new Style({
      fill: new Fill({ color: hexToRgba(color, 0.3) }),
      stroke: new Stroke({ color, width: 2 }),
      image: new CircleStyle({
        radius: 6,
        fill: new Fill({ color: hexToRgba(color, 0.6) }),
        stroke: new Stroke({ color, width: 1.5 }),
      }),
    }),
    properties: { layerId: config.id },
  });
}

export function createLayer(config: LayerConfig) {
  if (!config.url) return null;

  switch (config.type) {
    case 'wms':
      return createWMSLayer(config);
    case 'wfs':
      return createWFSLayer(config);
    case 'rest':
      return createRESTLayer(config);
    default:
      return null;
  }
}

function hexToRgba(hex: string, alpha: number): string {
  const r = parseInt(hex.slice(1, 3), 16);
  const g = parseInt(hex.slice(3, 5), 16);
  const b = parseInt(hex.slice(5, 7), 16);
  return `rgba(${r}, ${g}, ${b}, ${alpha})`;
}
