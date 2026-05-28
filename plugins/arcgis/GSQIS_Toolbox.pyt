"""
GSQIS ArcGIS Pro Toolbox

Idox Geospatial SDK — ArcGIS Pro Python Toolbox
Version: 1.0.0

Provides geospatial analysis tools for use within ArcGIS Pro 3.0+.
Current tools:
  - Layer Statistics: Compute summary statistics for a feature layer.

Support: geo-customersupport@idoxgroup.com
"""

import arcpy


class Toolbox:
    """ArcGIS Pro toolbox definition for GSQIS."""

    def __init__(self):
        self.label = "GSQIS Toolbox"
        self.alias = "gsqis"
        self.description = (
            "Idox Geospatial GSQIS Toolbox for ArcGIS Pro. "
            "Provides geospatial analysis utilities including layer statistics."
        )
        # List of tool classes contained in this toolbox
        self.tools = [LayerStatistics]


class LayerStatistics:
    """Compute summary statistics for all fields in a feature layer."""

    def __init__(self):
        self.label = "Layer Statistics"
        self.description = (
            "Computes summary statistics for all attribute fields in a "
            "feature layer. Numeric fields yield count, min, max, mean, "
            "median, sum, and standard deviation. Text fields yield count, "
            "unique value count, and top recurring values. "
            "Results are written to a report text file."
        )
        self.category = "Analysis"
        self.canRunInBackground = True

    def getParameterInfo(self):
        """Define tool parameter definitions."""

        param_layer = arcpy.Parameter(
            displayName="Input Feature Layer",
            name="in_layer",
            datatype="GPFeatureLayer",
            parameterType="Required",
            direction="Input",
        )

        param_output = arcpy.Parameter(
            displayName="Output Report File",
            name="out_report",
            datatype="DEFile",
            parameterType="Required",
            direction="Output",
        )
        param_output.filter.list = ["txt"]

        param_max_unique = arcpy.Parameter(
            displayName="Maximum Unique Values to Report (text fields)",
            name="max_unique",
            datatype="GPLong",
            parameterType="Optional",
            direction="Input",
        )
        param_max_unique.value = 20
        param_max_unique.filter.type = "Range"
        param_max_unique.filter.list = [1, 100]

        return [param_layer, param_output, param_max_unique]

    def isLicensed(self):
        """Allow the tool to execute (no special licence required)."""
        return True

    def updateParameters(self, parameters):
        """Modify parameters before internal validation."""
        return

    def updateMessages(self, parameters):
        """Modify messages after internal validation."""
        return

    def execute(self, parameters, messages):
        """Run the Layer Statistics tool."""
        in_layer = parameters[0].valueAsText
        out_report = parameters[1].valueAsText
        max_unique = int(parameters[2].value) if parameters[2].value else 20

        desc = arcpy.Describe(in_layer)
        layer_name = desc.name
        crs = desc.spatialReference.name if desc.spatialReference else "Unknown"
        geometry_type = desc.shapeType if hasattr(desc, "shapeType") else "Unknown"
        feature_count = int(arcpy.GetCount_management(in_layer)[0])
        fields = arcpy.ListFields(in_layer)

        messages.addMessage(f"Processing layer: {layer_name}")
        messages.addMessage(f"  CRS: {crs}")
        messages.addMessage(f"  Geometry type: {geometry_type}")
        messages.addMessage(f"  Feature count: {feature_count}")
        messages.addMessage(f"  Field count: {len(fields)}")

        report_lines = []
        report_lines.append("=" * 60)
        report_lines.append("LAYER SUMMARY")
        report_lines.append("=" * 60)
        report_lines.append(f"  Name:           {layer_name}")
        report_lines.append(f"  CRS:            {crs}")
        report_lines.append(f"  Geometry Type:  {geometry_type}")
        report_lines.append(f"  Feature Count:  {feature_count}")
        report_lines.append(f"  Field Count:    {len(fields)}")
        report_lines.append("")
        report_lines.append("=" * 60)
        report_lines.append("FIELD STATISTICS")
        report_lines.append("=" * 60)

        numeric_types = {
            "SmallInteger", "Integer", "BigInteger",
            "Single", "Double",
        }

        for field in fields:
            report_lines.append("")
            report_lines.append(f"--- {field.name} ({field.type}) ---")

            if field.type in numeric_types:
                stats = _compute_numeric_stats(in_layer, field.name)
                report_lines.append(f"  Count:      {stats['count']}")
                for key, label in [
                    ("min", "Min"),
                    ("max", "Max"),
                    ("mean", "Mean"),
                    ("median", "Median"),
                    ("sum", "Sum"),
                    ("std_dev", "Std Dev"),
                ]:
                    val = stats.get(key)
                    if val is not None:
                        report_lines.append(f"  {label + ':':<12}{val:.6g}")
                    else:
                        report_lines.append(f"  {label + ':':<12}N/A")
            else:
                stats = _compute_text_stats(in_layer, field.name, max_unique)
                report_lines.append(f"  Count:          {stats['count']}")
                report_lines.append(f"  Empty:          {stats['empty_count']}")
                report_lines.append(f"  Unique Values:  {stats['unique_count']}")
                if stats["top_values"]:
                    report_lines.append("  Top Values:")
                    for val, cnt in stats["top_values"]:
                        display = val if val else "(empty)"
                        report_lines.append(f"    {display}: {cnt}")

        report_lines.append("")
        report_text = "\n".join(report_lines)

        with open(out_report, "w", encoding="utf-8") as f:
            f.write(report_text)

        messages.addMessage(f"Report written to: {out_report}")
        return

    def postExecute(self, parameters):
        """Actions to perform after execution."""
        return


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def _compute_numeric_stats(layer, field_name):
    """Return basic numeric statistics for *field_name* in *layer*."""
    values = []
    with arcpy.da.SearchCursor(layer, [field_name]) as cursor:
        for row in cursor:
            v = row[0]
            if v is not None:
                try:
                    values.append(float(v))
                except (ValueError, TypeError):
                    continue

    if not values:
        return {
            "count": 0,
            "min": None, "max": None, "mean": None,
            "sum": None, "std_dev": None, "median": None,
        }

    count = len(values)
    total = sum(values)
    mean = total / count
    min_val = min(values)
    max_val = max(values)

    variance = sum((x - mean) ** 2 for x in values) / count
    std_dev = variance ** 0.5

    sorted_vals = sorted(values)
    mid = count // 2
    if count % 2 == 0:
        median = (sorted_vals[mid - 1] + sorted_vals[mid]) / 2.0
    else:
        median = sorted_vals[mid]

    return {
        "count": count,
        "min": min_val,
        "max": max_val,
        "mean": mean,
        "sum": total,
        "std_dev": std_dev,
        "median": median,
    }


def _compute_text_stats(layer, field_name, max_unique=20):
    """Return text/categorical statistics for *field_name* in *layer*."""
    value_counts = {}
    count = 0
    empty_count = 0

    with arcpy.da.SearchCursor(layer, [field_name]) as cursor:
        for row in cursor:
            v = row[0]
            if v is None:
                continue
            str_val = str(v)
            count += 1
            if str_val.strip() == "":
                empty_count += 1
            value_counts[str_val] = value_counts.get(str_val, 0) + 1

    sorted_values = sorted(
        value_counts.items(), key=lambda x: (-x[1], x[0])
    )

    return {
        "count": count,
        "empty_count": empty_count,
        "unique_count": len(value_counts),
        "top_values": sorted_values[:max_unique],
    }
