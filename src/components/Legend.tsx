import { useState } from 'react';
import { LAYER_CATEGORIES } from '../utils/config';
import type { LayerConfig } from '../types';

interface LegendProps {
  layers: LayerConfig[];
  setLayers: React.Dispatch<React.SetStateAction<LayerConfig[]>>;
}

export function Legend({ layers, setLayers }: LegendProps) {
  const [collapsed, setCollapsed] = useState(false);
  const [activeCategory, setActiveCategory] = useState<string | null>(null);
  const [searchFilter, setSearchFilter] = useState('');

  const toggleLayerVisibility = (layerId: string) => {
    setLayers((prev) =>
      prev.map((l) => (l.id === layerId ? { ...l, visible: !l.visible } : l))
    );
  };

  const updateLayerOpacity = (layerId: string, opacity: number) => {
    setLayers((prev) =>
      prev.map((l) => (l.id === layerId ? { ...l, opacity } : l))
    );
  };

  const filteredLayers = layers.filter((l) => {
    const matchesCategory = !activeCategory || l.category === activeCategory;
    const matchesSearch =
      !searchFilter || l.name.toLowerCase().includes(searchFilter.toLowerCase());
    return matchesCategory && matchesSearch;
  });

  const layersByCategory = LAYER_CATEGORIES.reduce(
    (acc, cat) => {
      acc[cat] = filteredLayers.filter((l) => l.category === cat);
      return acc;
    },
    {} as Record<string, LayerConfig[]>
  );

  return (
    <aside className={`legend-panel ${collapsed ? 'collapsed' : ''}`}>
      <div className="legend-header">
        <h2>Layers</h2>
        <button
          className="legend-toggle"
          onClick={() => setCollapsed(!collapsed)}
          title={collapsed ? 'Expand' : 'Collapse'}
        >
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d={collapsed ? 'M9 18l6-6-6-6' : 'M15 18l-6-6 6-6'} />
          </svg>
        </button>
      </div>

      {!collapsed && (
        <div className="legend-content">
          <div className="legend-search">
            <input
              type="text"
              placeholder="Filter layers..."
              value={searchFilter}
              onChange={(e) => setSearchFilter(e.target.value)}
            />
          </div>

          <div className="category-tabs">
            <button
              className={`category-tab ${!activeCategory ? 'active' : ''}`}
              onClick={() => setActiveCategory(null)}
            >
              All
            </button>
            {LAYER_CATEGORIES.map((cat) => (
              <button
                key={cat}
                className={`category-tab ${activeCategory === cat ? 'active' : ''}`}
                onClick={() => setActiveCategory(activeCategory === cat ? null : cat)}
              >
                {cat}
              </button>
            ))}
          </div>

          <div className="layer-list">
            {LAYER_CATEGORIES.map((category) => {
              const catLayers = layersByCategory[category];
              if (!catLayers || catLayers.length === 0) return null;

              return (
                <div key={category} className="layer-group">
                  <h3 className="layer-group-title">{category}</h3>
                  {catLayers.map((layer) => (
                    <div key={layer.id} className="layer-item">
                      <div className="layer-item-header">
                        <label className="layer-checkbox">
                          <input
                            type="checkbox"
                            checked={layer.visible}
                            onChange={() => toggleLayerVisibility(layer.id)}
                          />
                          <span
                            className="layer-swatch"
                            style={{ backgroundColor: layer.color }}
                          />
                          <span className="layer-name">{layer.name}</span>
                        </label>
                        {!layer.url && (
                          <span className="layer-badge" title="No service URL configured">
                            No URL
                          </span>
                        )}
                      </div>
                      {layer.visible && (
                        <div className="layer-controls">
                          <label className="opacity-label">
                            <span>Opacity</span>
                            <input
                              type="range"
                              min="0"
                              max="1"
                              step="0.05"
                              value={layer.opacity}
                              onChange={(e) =>
                                updateLayerOpacity(layer.id, parseFloat(e.target.value))
                              }
                            />
                            <span className="opacity-value">
                              {Math.round(layer.opacity * 100)}%
                            </span>
                          </label>
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              );
            })}
          </div>
        </div>
      )}
    </aside>
  );
}
