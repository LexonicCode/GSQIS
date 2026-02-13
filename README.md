# PlanningPerspective

A web-GIS application for visualising UK planning-related data on an interactive map.

## Features

- **Interactive basemap** - Ordnance Survey Zoomstack tiles (falls back to OpenStreetMap)
- **Search** - by address, postcode, or lat/lon coordinates
- **Drawing tools** - circle, rectangle, polygon, and freehand to define areas of interest
- **Planning data layers** - WMS, WFS and REST API integration for:
  - Planning Applications
  - Listed Buildings
  - Conservation Areas
  - Flood Zones
  - Green Belt
  - Tree Preservation Orders
  - Local Plan Allocations
  - Article 4 Directions
- **Legend panel** - filter by category, toggle visibility, adjust opacity
- **Live coordinates** - cursor position displayed in lat/lon

## Tech Stack

- React + TypeScript + Vite
- OpenLayers 10
- postcodes.io + Nominatim for geocoding

## Getting Started

```bash
npm install
npm run dev
```

### OS Zoomstack Tiles

To use Ordnance Survey basemap tiles, create a `.env` file:

```
VITE_OS_API_KEY=your_os_api_key_here
```

Sign up for a free key at [OS Data Hub](https://osdatahub.os.uk/).

Without an API key the map defaults to OpenStreetMap tiles.

### Configuring Data Layers

Layer service endpoints are defined in `src/utils/config.ts`. Update the `url` and optional `apiKey` fields for each layer to connect to your WMS/WFS/REST services.

## Build

```bash
npm run build    # outputs to dist/
npm run preview  # preview the production build locally
```

## Deployment

A `vercel.json` is included for one-click Vercel deployment. Set `VITE_OS_API_KEY` as an environment variable in your Vercel project settings.

## License

MIT
