import { useState, useEffect } from 'react';
import { toLonLat } from 'ol/proj';
import type OLMap from 'ol/Map';
import type MapBrowserEvent from 'ol/MapBrowserEvent';

interface CoordinatesProps {
  map: OLMap | null;
}

export function Coordinates({ map }: CoordinatesProps) {
  const [coords, setCoords] = useState<{ lat: number; lon: number } | null>(null);

  useEffect(() => {
    if (!map) return;

    const handlePointerMove = (evt: MapBrowserEvent) => {
      const [lon, lat] = toLonLat(evt.coordinate);
      setCoords({ lat, lon });
    };

    map.on('pointermove', handlePointerMove);
    return () => {
      map.un('pointermove', handlePointerMove);
    };
  }, [map]);

  if (!coords) return null;

  return (
    <div className="coordinates-display">
      <span>Lat: {coords.lat.toFixed(5)}</span>
      <span>Lon: {coords.lon.toFixed(5)}</span>
    </div>
  );
}
