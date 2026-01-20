"""
Unit tests for GSQIS Plugin
"""

import pytest
from qgis.core import QgsApplication


@pytest.fixture(scope='session')
def qgis_app():
    """Start QGIS application for testing.

    Yields:
        QgsApplication: QGIS application instance
    """
    qgs = QgsApplication([], False)
    qgs.initQgis()
    yield qgs
    qgs.exitQgis()


def test_plugin_imports():
    """Test that plugin module can be imported."""
    try:
        from plugin import gsqis_plugin
        assert gsqis_plugin is not None
    except ImportError as e:
        pytest.fail(f"Failed to import plugin module: {e}")


def test_plugin_metadata():
    """Test that metadata.txt exists and is valid."""
    import os
    import configparser

    metadata_path = os.path.join(
        os.path.dirname(__file__),
        '..',
        'metadata.txt'
    )

    assert os.path.exists(metadata_path), "metadata.txt not found"

    config = configparser.ConfigParser()
    config.read(metadata_path)

    # Check required fields
    assert config.has_section('general'), "Missing [general] section"
    assert config.has_option('general', 'name'), "Missing 'name' field"
    assert config.has_option('general', 'version'), "Missing 'version' field"
    assert config.has_option('general', 'qgisMinimumVersion'), "Missing 'qgisMinimumVersion' field"


# Add more tests as you develop your plugin
