import { useRef, useEffect } from 'react';
import { useMap } from '../hooks/useMap';
import { SearchBar } from './SearchBar';
import { DrawingToolbar } from './DrawingToolbar';
import { Legend } from './Legend';
import { Coordinates } from './Coordinates';
import 'ol/ol.css';

export function MapView() {
  const mapContainerRef = useRef<HTMLDivElement>(null);
  const {
    map,
    drawLayer,
    layers,
    setLayers,
    activeDrawTool,
    setActiveDrawTool,
    navigateToResult,
  } = useMap(mapContainerRef);

  // Apply cursor style when drawing
  useEffect(() => {
    const container = mapContainerRef.current;
    if (!container) return;
    container.style.cursor = activeDrawTool ? 'crosshair' : '';
  }, [activeDrawTool]);

  return (
    <div className="app-container">
      <header className="app-header">
        <div className="header-brand">
          <svg className="header-logo" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z" />
            <circle cx="12" cy="10" r="3" />
          </svg>
          <h1>PlanningPerspective</h1>
        </div>
        <SearchBar onSelect={navigateToResult} />
      </header>

      <div className="main-content">
        <Legend layers={layers} setLayers={setLayers} />

        <div className="map-area">
          <DrawingToolbar
            map={map}
            drawLayer={drawLayer}
            activeDrawTool={activeDrawTool}
            setActiveDrawTool={setActiveDrawTool}
          />
          <div ref={mapContainerRef} className="map-container" />
          <Coordinates map={map} />
        </div>
      </div>
    </div>
  );
}
