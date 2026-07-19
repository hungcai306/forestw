import { useEffect, useRef } from 'react';
import Map from 'ol/Map';
import View from 'ol/View';
import TileLayer from 'ol/layer/Tile';
import XYZ from 'ol/source/XYZ';
import { fromLonLat } from 'ol/proj';
import 'ol/ol.css';

const GOOGLE_TILE_OPTIONS = {
  crossOrigin: 'anonymous' as const,
  maxZoom: 21,
  attributions: 'Map data © Google',
};

export default function MapPanel() {
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!ref.current) return;

    const satelliteLayer = new TileLayer({
      properties: { id: 'google-satellite', title: 'Google Satellite' },
      source: new XYZ({
        ...GOOGLE_TILE_OPTIONS,
        url: 'https://mt{0-3}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
      }),
    });

    const labelsLayer = new TileLayer({
      properties: { id: 'google-labels', title: 'Nhãn Google' },
      source: new XYZ({
        ...GOOGLE_TILE_OPTIONS,
        url: 'https://mt{0-3}.google.com/vt/lyrs=h&x={x}&y={y}&z={z}',
      }),
      opacity: 1,
    });

    const map = new Map({
      target: ref.current,
      layers: [satelliteLayer, labelsLayer],
      view: new View({
        center: fromLonLat([107.59, 16.46]),
        zoom: 10,
        maxZoom: 21,
      }),
    });

    return () => map.setTarget(undefined);
  }, []);

  return <div className="map" ref={ref} />;
}
