# GSQIS ArcGIS Pro Toolbox — Developer Notes

This directory contains the **GSQIS ArcGIS Pro Python Toolbox** (`GSQIS_Toolbox.pyt`), providing geospatial analysis utilities for use inside ArcGIS Pro 3.0 and above.

## Structure

```
plugins/arcgis/
├── GSQIS_Toolbox.pyt    # ArcGIS Pro Python Toolbox (self-contained)
└── README.md            # This file
```

## Available Tools

| Tool | Category | Description |
|------|----------|-------------|
| Layer Statistics | Analysis | Computes numeric and categorical field statistics for a feature layer; exports a plain-text report. |

## Requirements

- ArcGIS Pro 3.0 or later
- No additional Python packages required (uses built-in `arcpy` only)

## Quick Start (Developer)

1. Open ArcGIS Pro.
2. In the **Catalog** pane, navigate to **Toolboxes → Add Toolbox**.
3. Browse to `plugins/arcgis/GSQIS_Toolbox.pyt` and click **OK**.
4. Expand **GSQIS Toolbox → Analysis** and double-click **Layer Statistics**.
5. Select a feature layer, choose an output `.txt` path, and run.

## Support

For end-user installation and usage instructions, refer to the distribution package in `dist/arcgis-plugin-release/`.

**Support contact:** geo-customersupport@idoxgroup.com
