"""
GSQIS Plugin - A QGIS plugin for geospatial analysis

This script initializes the plugin, making it known to QGIS.
"""


def classFactory(iface):
    """Load GSQISPlugin class from file gsqis_plugin.

    Args:
        iface (QgsInterface): A QGIS interface instance.

    Returns:
        GSQISPlugin: The plugin instance.
    """
    from .gsqis_plugin import GSQISPlugin
    return GSQISPlugin(iface)
