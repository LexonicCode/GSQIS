import type { SearchResult } from '../types';

const POSTCODES_IO_URL = 'https://api.postcodes.io';
const NOMINATIM_URL = 'https://nominatim.openstreetmap.org';

// Regex patterns
const POSTCODE_REGEX = /^[A-Z]{1,2}\d[A-Z\d]?\s*\d[A-Z]{2}$/i;
const LATLON_REGEX = /^\s*(-?\d+\.?\d*)\s*[,\s]\s*(-?\d+\.?\d*)\s*$/;

function detectSearchType(query: string): 'postcode' | 'latlon' | 'address' {
  if (POSTCODE_REGEX.test(query.trim())) return 'postcode';
  if (LATLON_REGEX.test(query.trim())) return 'latlon';
  return 'address';
}

async function searchPostcode(postcode: string): Promise<SearchResult[]> {
  const cleaned = postcode.replace(/\s/g, '');

  // Try exact match first
  try {
    const response = await fetch(`${POSTCODES_IO_URL}/postcodes/${encodeURIComponent(cleaned)}`);
    if (response.ok) {
      const data = await response.json();
      if (data.result) {
        return [{
          label: data.result.postcode,
          lon: data.result.longitude,
          lat: data.result.latitude,
        }];
      }
    }
  } catch {
    // Fall through to autocomplete
  }

  // Try autocomplete
  try {
    const response = await fetch(`${POSTCODES_IO_URL}/postcodes/${encodeURIComponent(cleaned)}/autocomplete`);
    if (response.ok) {
      const data = await response.json();
      if (data.result) {
        const results = await Promise.all(
          data.result.slice(0, 5).map(async (pc: string) => {
            const res = await fetch(`${POSTCODES_IO_URL}/postcodes/${encodeURIComponent(pc)}`);
            const d = await res.json();
            return d.result ? {
              label: d.result.postcode,
              lon: d.result.longitude,
              lat: d.result.latitude,
            } : null;
          })
        );
        return results.filter((r: SearchResult | null): r is SearchResult => r !== null);
      }
    }
  } catch {
    // Return empty
  }

  return [];
}

function parseLatLon(query: string): SearchResult[] {
  const match = query.trim().match(LATLON_REGEX);
  if (!match) return [];

  const val1 = parseFloat(match[1]);
  const val2 = parseFloat(match[2]);

  // Determine which is lat and which is lon
  // UK latitude range: ~49-61, longitude range: ~-8 to 2
  let lat: number, lon: number;
  if (val1 >= 49 && val1 <= 61) {
    lat = val1;
    lon = val2;
  } else if (val2 >= 49 && val2 <= 61) {
    lat = val2;
    lon = val1;
  } else {
    // Default: assume lat, lon order
    lat = val1;
    lon = val2;
  }

  return [{
    label: `${lat.toFixed(5)}, ${lon.toFixed(5)}`,
    lon,
    lat,
  }];
}

async function searchAddress(query: string): Promise<SearchResult[]> {
  try {
    const params = new URLSearchParams({
      q: query,
      format: 'json',
      countrycodes: 'gb',
      limit: '5',
      addressdetails: '1',
    });

    const response = await fetch(`${NOMINATIM_URL}/search?${params}`, {
      headers: {
        'Accept': 'application/json',
      },
    });

    if (!response.ok) return [];

    const data = await response.json();
    return data.map((item: { display_name: string; lon: string; lat: string; boundingbox: string[] }) => ({
      label: item.display_name,
      lon: parseFloat(item.lon),
      lat: parseFloat(item.lat),
      bbox: item.boundingbox
        ? [
            parseFloat(item.boundingbox[2]), // west lon
            parseFloat(item.boundingbox[0]), // south lat
            parseFloat(item.boundingbox[3]), // east lon
            parseFloat(item.boundingbox[1]), // north lat
          ] as [number, number, number, number]
        : undefined,
    }));
  } catch {
    return [];
  }
}

export async function search(query: string): Promise<SearchResult[]> {
  const type = detectSearchType(query);

  switch (type) {
    case 'postcode':
      return searchPostcode(query);
    case 'latlon':
      return parseLatLon(query);
    case 'address':
      return searchAddress(query);
  }
}
