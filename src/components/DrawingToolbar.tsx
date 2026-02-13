import { useEffect, useRef, useCallback } from 'react';
import Draw, { createBox } from 'ol/interaction/Draw';
import type { Map as OLMap } from 'ol';
import type VectorLayer from 'ol/layer/Vector';
import type VectorSource from 'ol/source/Vector';
import type { Type as GeomType } from 'ol/geom/Geometry';

interface DrawingToolbarProps {
  map: OLMap | null;
  drawLayer: VectorLayer<VectorSource> | null;
  activeDrawTool: string | null;
  setActiveDrawTool: React.Dispatch<React.SetStateAction<string | null>>;
}

const TOOLS = [
  { id: 'Circle', label: 'Circle', icon: 'M12 22C6.5 22 2 17.5 2 12S6.5 2 12 2s10 4.5 10 10-4.5 10-10 10z' },
  { id: 'Box', label: 'Rectangle', icon: 'M3 3h18v18H3z' },
  { id: 'Polygon', label: 'Polygon', icon: 'M12 2l9 7-3.5 10h-11L3 9z' },
  { id: 'Freehand', label: 'Freehand', icon: 'M3 17c3-3 6 2 9-1s6-6 9-3' },
];

export function DrawingToolbar({ map, drawLayer, activeDrawTool, setActiveDrawTool }: DrawingToolbarProps) {
  const drawInteractionRef = useRef<Draw | null>(null);

  const removeInteraction = useCallback(() => {
    if (map && drawInteractionRef.current) {
      map.removeInteraction(drawInteractionRef.current);
      drawInteractionRef.current = null;
    }
  }, [map]);

  const clearDrawings = useCallback(() => {
    if (drawLayer) {
      drawLayer.getSource()?.clear();
    }
    removeInteraction();
    setActiveDrawTool(null);
  }, [drawLayer, removeInteraction, setActiveDrawTool]);

  // Manage draw interaction
  useEffect(() => {
    if (!map || !drawLayer) return;

    removeInteraction();

    if (!activeDrawTool) return;

    const source = drawLayer.getSource();
    if (!source) return;

    let geometryType: GeomType;
    let geometryFunction;
    let freehand = false;

    switch (activeDrawTool) {
      case 'Circle':
        geometryType = 'Circle';
        break;
      case 'Box':
        geometryType = 'Circle';
        geometryFunction = createBox();
        break;
      case 'Polygon':
        geometryType = 'Polygon';
        break;
      case 'Freehand':
        geometryType = 'Polygon';
        freehand = true;
        break;
      default:
        return;
    }

    const draw = new Draw({
      source,
      type: geometryType,
      geometryFunction,
      freehand,
    });

    draw.on('drawend', () => {
      // Keep the drawing visible, deactivate tool
      setTimeout(() => setActiveDrawTool(null), 100);
    });

    map.addInteraction(draw);
    drawInteractionRef.current = draw;

    return () => {
      map.removeInteraction(draw);
    };
  }, [map, drawLayer, activeDrawTool, removeInteraction, setActiveDrawTool]);

  const handleToolClick = (toolId: string) => {
    if (activeDrawTool === toolId) {
      setActiveDrawTool(null);
    } else {
      setActiveDrawTool(toolId);
    }
  };

  return (
    <div className="drawing-toolbar">
      {TOOLS.map((tool) => (
        <button
          key={tool.id}
          className={`draw-btn ${activeDrawTool === tool.id ? 'active' : ''}`}
          onClick={() => handleToolClick(tool.id)}
          title={tool.label}
        >
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
            <path d={tool.icon} />
          </svg>
          <span>{tool.label}</span>
        </button>
      ))}
      <button className="draw-btn clear-btn" onClick={clearDrawings} title="Clear drawings">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
          <path d="M3 6h18M8 6V4h8v2M19 6v14a2 2 0 01-2 2H7a2 2 0 01-2-2V6" />
        </svg>
        <span>Clear</span>
      </button>
    </div>
  );
}
