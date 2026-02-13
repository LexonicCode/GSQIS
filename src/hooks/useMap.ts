import { useEffect, useRef, useState, useCallback } from 'react';
import OLMap from 'ol/Map';
import View from 'ol/View';
import TileLayer from 'ol/layer/Tile';
import XYZ from 'ol/source/XYZ';
import VectorLayer from 'ol/layer/Vector';
import VectorSource from 'ol/source/Vector';
import { fromLonLat, transformExtent } from 'ol/proj';
import { defaults as defaultControls, ScaleLine, Attribution } from 'ol/control';
import { Style, Fill, Stroke, Circle as CircleStyle } from 'ol/style';
import { APP_CONFIG, DEFAULT_LAYERS } from '../utils/config';
import type { LayerConfig, SearchResult } from '../types';
import type BaseLayer from 'ol/layer/Base';

export function useMap(mapRef: React.RefObject<HTMLDivElement | null>) {
  const [map, setMap] = useState<OLMap | null>(null);
  const [drawLayer, setDrawLayer] = useState<VectorLayer<VectorSource> | null>(null);
  const [layers, setLayers] = useState<LayerConfig[]>(DEFAULT_LAYERS);
  const [activeDrawTool, setActiveDrawTool] = useState<string | null>(null);
  const [searchResult, setSearchResult] = useState<SearchResult | null>(null);
  const olLayersRef = useRef(new globalThis.Map<string, TileLayer | VectorLayer<VectorSource>>());

  // Initialize map
  useEffect(() => {
    if (!mapRef.current || map) return;

    // OS Zoomstack raster tiles - fallback to OSM if no API key
    const basemapSource = APP_CONFIG.osApiKey
      ? new XYZ({
          url: `https://api.os.uk/maps/raster/v1/zxy/Light_3857/{z}/{x}/{y}.png?key=${APP_CONFIG.osApiKey}`,
          maxZoom: 20,
          attributions: '&copy; <a href="https://www.ordnancesurvey.co.uk/">Ordnance Survey</a>',
          crossOrigin: 'anonymous',
        })
      : new XYZ({
          url: 'https://tile.openstreetmap.org/{z}/{x}/{y}.png',
          maxZoom: 19,
          attributions: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
          crossOrigin: 'anonymous',
        });

    const basemap = new TileLayer({ source: basemapSource });

    // Drawing layer
    const drawSource = new VectorSource();
    const drawing = new VectorLayer({
      source: drawSource,
      style: new Style({
        fill: new Fill({ color: 'rgba(59, 130, 246, 0.15)' }),
        stroke: new Stroke({ color: '#3b82f6', width: 2, lineDash: [6, 4] }),
        image: new CircleStyle({
          radius: 5,
          fill: new Fill({ color: '#3b82f6' }),
          stroke: new Stroke({ color: '#fff', width: 1.5 }),
        }),
      }),
      zIndex: 999,
    });

    const olMap = new OLMap({
      target: mapRef.current,
      layers: [basemap, drawing],
      view: new View({
        center: fromLonLat(APP_CONFIG.defaultCenter),
        zoom: APP_CONFIG.defaultZoom,
        maxZoom: 20,
        minZoom: 5,
      }),
      controls: defaultControls({ attribution: false }).extend([
        new ScaleLine({ units: 'metric' }),
        new Attribution({ collapsible: true }),
      ]),
    });

    setMap(olMap);
    setDrawLayer(drawing);

    return () => {
      olMap.setTarget(undefined);
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [mapRef]);

  // Sync layer visibility/opacity
  useEffect(() => {
    if (!map) return;

    const mapLayers = map.getLayers();
    mapLayers.forEach((layer: BaseLayer) => {
      const layerId = layer.get('layerId');
      if (layerId) {
        const config = layers.find((l) => l.id === layerId);
        if (config) {
          layer.setVisible(config.visible);
          layer.setOpacity(config.opacity);
        }
      }
    });
  }, [map, layers]);

  // Navigate to search result
  const navigateToResult = useCallback(
    (result: SearchResult) => {
      if (!map) return;
      setSearchResult(result);
      const view = map.getView();
      const center = fromLonLat([result.lon, result.lat]);

      if (result.bbox) {
        const extent = transformExtent(result.bbox, 'EPSG:4326', 'EPSG:3857');
        view.fit(extent, { duration: 800, padding: [50, 50, 50, 50] });
      } else {
        view.animate({ center, zoom: 16, duration: 800 });
      }
    },
    [map]
  );

  return {
    map,
    drawLayer,
    layers,
    setLayers,
    activeDrawTool,
    setActiveDrawTool,
    searchResult,
    setSearchResult,
    navigateToResult,
    olLayersRef,
  };
}
