"""
Layer statistics computation module.

Provides functions to compute summary statistics for QGIS vector layers,
including per-field numeric statistics and categorical value counts.
"""

import math

from qgis.core import (
    QgsVectorLayer,
    QgsField,
    QgsStatisticalSummary,
    QgsStringStatisticalSummary,
    QgsFeatureRequest,
    Qgis,
)


# Map QVariant type names to human-readable labels
_GEOMETRY_TYPE_NAMES = {
    Qgis.GeometryType.Point: "Point",
    Qgis.GeometryType.Line: "Line",
    Qgis.GeometryType.Polygon: "Polygon",
    Qgis.GeometryType.Null: "No Geometry",
    Qgis.GeometryType.Unknown: "Unknown",
}

# Numeric QVariant type names (from QMetaType)
_NUMERIC_TYPE_NAMES = {"Int", "Double", "LongLong", "Float", "Short", "UInt", "ULongLong", "UShort"}


def is_numeric_field(field):
    """Check if a QgsField holds numeric data.

    Args:
        field (QgsField): The field to check.

    Returns:
        bool: True if the field type is numeric.
    """
    return field.typeName() in _NUMERIC_TYPE_NAMES


def compute_layer_info(layer):
    """Compute basic information about a vector layer.

    Args:
        layer (QgsVectorLayer): The layer to summarize.

    Returns:
        dict: Layer information with keys:
            - name (str)
            - crs (str)
            - geometry_type (str)
            - feature_count (int)
            - field_count (int)
            - extent (str)
    """
    extent = layer.extent()
    return {
        "name": layer.name(),
        "crs": layer.crs().authid() or "Unknown",
        "geometry_type": _GEOMETRY_TYPE_NAMES.get(
            layer.geometryType(), "Unknown"
        ),
        "feature_count": layer.featureCount(),
        "field_count": len(layer.fields()),
        "extent": (
            f"{extent.xMinimum():.6f}, {extent.yMinimum():.6f} : "
            f"{extent.xMaximum():.6f}, {extent.yMaximum():.6f}"
        ),
    }


def compute_numeric_stats(layer, field_name):
    """Compute numeric statistics for a single field.

    Uses QgsStatisticalSummary for efficient computation.

    Args:
        layer (QgsVectorLayer): The source layer.
        field_name (str): Name of the numeric field.

    Returns:
        dict: Statistics with keys: count, min, max, mean, sum, std_dev, median.
            Values are None if computation fails.
    """
    stats = QgsStatisticalSummary(
        QgsStatisticalSummary.Statistic.Count
        | QgsStatisticalSummary.Statistic.Min
        | QgsStatisticalSummary.Statistic.Max
        | QgsStatisticalSummary.Statistic.Mean
        | QgsStatisticalSummary.Statistic.Sum
        | QgsStatisticalSummary.Statistic.StDev
        | QgsStatisticalSummary.Statistic.Median
    )

    field_index = layer.fields().indexFromName(field_name)
    if field_index < 0:
        return None

    request = QgsFeatureRequest().setFlags(QgsFeatureRequest.Flag.NoGeometry)
    request.setSubsetOfAttributes([field_index])

    values = []
    for feature in layer.getFeatures(request):
        val = feature.attributes()[field_index]
        if val is not None:
            try:
                values.append(float(val))
            except (ValueError, TypeError):
                continue

    if not values:
        return {
            "count": 0,
            "min": None,
            "max": None,
            "mean": None,
            "sum": None,
            "std_dev": None,
            "median": None,
        }

    stats.calculate(values)

    def _safe(val):
        if val is None or (isinstance(val, float) and math.isnan(val)):
            return None
        return val

    return {
        "count": stats.count(),
        "min": _safe(stats.min()),
        "max": _safe(stats.max()),
        "mean": _safe(stats.mean()),
        "sum": _safe(stats.sum()),
        "std_dev": _safe(stats.stDev()),
        "median": _safe(stats.median()),
    }


def compute_string_stats(layer, field_name, max_unique=20):
    """Compute statistics for a text/categorical field.

    Args:
        layer (QgsVectorLayer): The source layer.
        field_name (str): Name of the text field.
        max_unique (int): Maximum number of unique values to report.

    Returns:
        dict: Statistics with keys:
            - count (int): Number of non-null values
            - empty_count (int): Number of empty strings
            - unique_count (int): Number of distinct values
            - top_values (list[tuple]): Up to max_unique (value, count) pairs,
              sorted by count descending.
    """
    field_index = layer.fields().indexFromName(field_name)
    if field_index < 0:
        return None

    request = QgsFeatureRequest().setFlags(QgsFeatureRequest.Flag.NoGeometry)
    request.setSubsetOfAttributes([field_index])

    value_counts = {}
    count = 0
    empty_count = 0

    for feature in layer.getFeatures(request):
        val = feature.attributes()[field_index]
        if val is None:
            continue
        str_val = str(val)
        count += 1
        if str_val == "":
            empty_count += 1
        value_counts[str_val] = value_counts.get(str_val, 0) + 1

    # Sort by count descending, then alphabetically
    sorted_values = sorted(
        value_counts.items(), key=lambda x: (-x[1], x[0])
    )

    return {
        "count": count,
        "empty_count": empty_count,
        "unique_count": len(value_counts),
        "top_values": sorted_values[:max_unique],
    }


def compute_all_field_stats(layer):
    """Compute statistics for all fields in a layer.

    Args:
        layer (QgsVectorLayer): The source layer.

    Returns:
        list[dict]: One entry per field with keys:
            - name (str): Field name
            - type_name (str): Field type
            - is_numeric (bool): Whether the field is numeric
            - stats (dict): The computed statistics
    """
    results = []
    for field in layer.fields():
        entry = {
            "name": field.name(),
            "type_name": field.typeName(),
            "is_numeric": is_numeric_field(field),
        }
        if entry["is_numeric"]:
            entry["stats"] = compute_numeric_stats(layer, field.name())
        else:
            entry["stats"] = compute_string_stats(layer, field.name())
        results.append(entry)
    return results


def format_stats_as_text(layer_info, field_stats):
    """Format layer statistics as a plain-text report.

    Args:
        layer_info (dict): Output from compute_layer_info().
        field_stats (list[dict]): Output from compute_all_field_stats().

    Returns:
        str: Formatted text report.
    """
    lines = []
    lines.append("=" * 60)
    lines.append("LAYER SUMMARY")
    lines.append("=" * 60)
    lines.append(f"  Name:           {layer_info['name']}")
    lines.append(f"  CRS:            {layer_info['crs']}")
    lines.append(f"  Geometry Type:  {layer_info['geometry_type']}")
    lines.append(f"  Feature Count:  {layer_info['feature_count']}")
    lines.append(f"  Field Count:    {layer_info['field_count']}")
    lines.append(f"  Extent:         {layer_info['extent']}")
    lines.append("")

    if not field_stats:
        lines.append("No fields to summarize.")
        return "\n".join(lines)

    lines.append("=" * 60)
    lines.append("FIELD STATISTICS")
    lines.append("=" * 60)

    for entry in field_stats:
        lines.append("")
        lines.append(f"--- {entry['name']} ({entry['type_name']}) ---")
        stats = entry["stats"]
        if stats is None:
            lines.append("  Could not compute statistics.")
            continue

        if entry["is_numeric"]:
            lines.append(f"  Count:    {stats['count']}")
            for key in ("min", "max", "mean", "median", "sum", "std_dev"):
                val = stats[key]
                label = key.replace("_", " ").title()
                if val is not None:
                    lines.append(f"  {label + ':':<12}{val:.6g}")
                else:
                    lines.append(f"  {label + ':':<12}N/A")
        else:
            lines.append(f"  Count:          {stats['count']}")
            lines.append(f"  Empty:          {stats['empty_count']}")
            lines.append(f"  Unique Values:  {stats['unique_count']}")
            if stats["top_values"]:
                lines.append(f"  Top Values:")
                for val, cnt in stats["top_values"]:
                    display = val if val else "(empty)"
                    lines.append(f"    {display}: {cnt}")

    lines.append("")
    return "\n".join(lines)
