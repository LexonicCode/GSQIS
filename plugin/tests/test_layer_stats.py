"""
Unit tests for the layer statistics computation module.

These tests create in-memory vector layers to verify that
compute_layer_info, compute_numeric_stats, compute_string_stats,
compute_all_field_stats, and format_stats_as_text work correctly.
"""

import pytest
from qgis.core import (
    QgsApplication,
    QgsVectorLayer,
    QgsFeature,
    QgsGeometry,
    QgsPointXY,
    QgsField,
)
from qgis.PyQt.QtCore import QVariant


@pytest.fixture(scope="session")
def qgis_app():
    """Start a headless QGIS application for testing."""
    qgs = QgsApplication([], False)
    qgs.initQgis()
    yield qgs
    qgs.exitQgis()


@pytest.fixture
def point_layer(qgis_app):
    """Create a simple in-memory point layer with mixed field types."""
    layer = QgsVectorLayer(
        "Point?crs=epsg:4326",
        "test_points",
        "memory",
    )
    provider = layer.dataProvider()

    provider.addAttributes([
        QgsField("name", QVariant.String),
        QgsField("population", QVariant.Int),
        QgsField("area_km2", QVariant.Double),
        QgsField("category", QVariant.String),
    ])
    layer.updateFields()

    features = []
    data = [
        ("City A", 100000, 50.5, "urban", 1.0, 2.0),
        ("City B", 250000, 120.3, "urban", 3.0, 4.0),
        ("Town C", 5000, 8.7, "rural", 5.0, 6.0),
        ("Town D", 12000, 15.2, "rural", 7.0, 8.0),
        ("Village E", 800, 2.1, "rural", 9.0, 10.0),
    ]
    for name, pop, area, cat, x, y in data:
        feat = QgsFeature(layer.fields())
        feat.setAttributes([name, pop, area, cat])
        feat.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(x, y)))
        features.append(feat)

    provider.addFeatures(features)
    layer.updateExtents()
    return layer


@pytest.fixture
def empty_layer(qgis_app):
    """Create an empty in-memory point layer."""
    layer = QgsVectorLayer(
        "Point?crs=epsg:4326",
        "empty_layer",
        "memory",
    )
    provider = layer.dataProvider()
    provider.addAttributes([
        QgsField("value", QVariant.Int),
    ])
    layer.updateFields()
    return layer


class TestComputeLayerInfo:
    """Tests for compute_layer_info()."""

    def test_basic_info(self, point_layer):
        from plugin.core.layer_stats import compute_layer_info

        info = compute_layer_info(point_layer)

        assert info["name"] == "test_points"
        assert info["crs"] == "EPSG:4326"
        assert info["geometry_type"] == "Point"
        assert info["feature_count"] == 5
        assert info["field_count"] == 4

    def test_extent_is_string(self, point_layer):
        from plugin.core.layer_stats import compute_layer_info

        info = compute_layer_info(point_layer)
        assert isinstance(info["extent"], str)
        assert "," in info["extent"]

    def test_empty_layer_info(self, empty_layer):
        from plugin.core.layer_stats import compute_layer_info

        info = compute_layer_info(empty_layer)
        assert info["feature_count"] == 0
        assert info["field_count"] == 1


class TestNumericStats:
    """Tests for compute_numeric_stats()."""

    def test_integer_field(self, point_layer):
        from plugin.core.layer_stats import compute_numeric_stats

        stats = compute_numeric_stats(point_layer, "population")

        assert stats["count"] == 5
        assert stats["min"] == 800
        assert stats["max"] == 250000
        assert stats["sum"] == pytest.approx(367800)
        assert stats["mean"] == pytest.approx(73560.0)
        assert stats["median"] is not None
        assert stats["std_dev"] is not None

    def test_double_field(self, point_layer):
        from plugin.core.layer_stats import compute_numeric_stats

        stats = compute_numeric_stats(point_layer, "area_km2")

        assert stats["count"] == 5
        assert stats["min"] == pytest.approx(2.1)
        assert stats["max"] == pytest.approx(120.3)

    def test_nonexistent_field(self, point_layer):
        from plugin.core.layer_stats import compute_numeric_stats

        result = compute_numeric_stats(point_layer, "no_such_field")
        assert result is None

    def test_empty_layer(self, empty_layer):
        from plugin.core.layer_stats import compute_numeric_stats

        stats = compute_numeric_stats(empty_layer, "value")
        assert stats["count"] == 0
        assert stats["min"] is None


class TestStringStats:
    """Tests for compute_string_stats()."""

    def test_categorical_field(self, point_layer):
        from plugin.core.layer_stats import compute_string_stats

        stats = compute_string_stats(point_layer, "category")

        assert stats["count"] == 5
        assert stats["unique_count"] == 2
        assert stats["empty_count"] == 0

        # Top values should include "rural" (3) and "urban" (2)
        top_dict = dict(stats["top_values"])
        assert top_dict["rural"] == 3
        assert top_dict["urban"] == 2

    def test_name_field(self, point_layer):
        from plugin.core.layer_stats import compute_string_stats

        stats = compute_string_stats(point_layer, "name")

        assert stats["count"] == 5
        assert stats["unique_count"] == 5

    def test_nonexistent_field(self, point_layer):
        from plugin.core.layer_stats import compute_string_stats

        result = compute_string_stats(point_layer, "no_such_field")
        assert result is None


class TestComputeAllFieldStats:
    """Tests for compute_all_field_stats()."""

    def test_all_fields_covered(self, point_layer):
        from plugin.core.layer_stats import compute_all_field_stats

        results = compute_all_field_stats(point_layer)

        assert len(results) == 4
        names = [r["name"] for r in results]
        assert "name" in names
        assert "population" in names
        assert "area_km2" in names
        assert "category" in names

    def test_numeric_flags(self, point_layer):
        from plugin.core.layer_stats import compute_all_field_stats

        results = compute_all_field_stats(point_layer)
        by_name = {r["name"]: r for r in results}

        assert by_name["population"]["is_numeric"] is True
        assert by_name["area_km2"]["is_numeric"] is True
        assert by_name["name"]["is_numeric"] is False
        assert by_name["category"]["is_numeric"] is False


class TestFormatStatsAsText:
    """Tests for format_stats_as_text()."""

    def test_report_contains_layer_info(self, point_layer):
        from plugin.core.layer_stats import (
            compute_layer_info,
            compute_all_field_stats,
            format_stats_as_text,
        )

        info = compute_layer_info(point_layer)
        stats = compute_all_field_stats(point_layer)
        report = format_stats_as_text(info, stats)

        assert "LAYER SUMMARY" in report
        assert "test_points" in report
        assert "EPSG:4326" in report
        assert "Point" in report

    def test_report_contains_field_stats(self, point_layer):
        from plugin.core.layer_stats import (
            compute_layer_info,
            compute_all_field_stats,
            format_stats_as_text,
        )

        info = compute_layer_info(point_layer)
        stats = compute_all_field_stats(point_layer)
        report = format_stats_as_text(info, stats)

        assert "FIELD STATISTICS" in report
        assert "population" in report
        assert "category" in report

    def test_empty_fields_report(self):
        from plugin.core.layer_stats import format_stats_as_text

        info = {
            "name": "test",
            "crs": "EPSG:4326",
            "geometry_type": "Point",
            "feature_count": 0,
            "field_count": 0,
            "extent": "0, 0 : 0, 0",
        }
        report = format_stats_as_text(info, [])
        assert "No fields to summarize." in report
