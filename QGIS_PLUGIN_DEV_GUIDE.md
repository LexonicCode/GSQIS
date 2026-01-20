# QGIS Plugin Development Guide - Reference Documentation

**Version:** QGIS 3.40
**Last Updated:** 2026-01-20
**Based on:** PyQGIS Developer Cookbook 3.40

---

## Table of Contents
1. [Overview](#overview)
2. [Plugin Development Workflow](#plugin-development-workflow)
3. [Required Files and Structure](#required-files-and-structure)
4. [metadata.txt Specification](#metadatatxt-specification)
5. [Plugin Entry Point (__init__.py)](#plugin-entry-point-initpy)
6. [Main Plugin Class](#main-plugin-class)
7. [QgsInterface (iface)](#qgsinterface-iface)
8. [Best Practices](#best-practices)
9. [Logging and Error Handling](#logging-and-error-handling)
10. [Testing](#testing)
11. [PyQGIS Core APIs](#pyqgis-core-apis)
12. [Resources](#resources)

---

## Overview

QGIS plugins allow extending the functionality of QGIS through Python code. Plugins can add new processing algorithms, custom GUI components, interact with vector/raster layers, and integrate with external services.

### Plugin Types
- **Standard Plugins**: Add functionality through menus, toolbars, and dialogs
- **Processing Plugins**: Add custom algorithms to the Processing framework
- **Server Plugins**: Extend QGIS Server functionality

---

## Plugin Development Workflow

The official QGIS plugin development workflow consists of these steps:

1. **Idea**: Define what your plugin will do
2. **Setup**: Create required plugin files and structure
3. **Develop**: Write the code in appropriate files
4. **Document**: Write plugin documentation
5. **Translate** (Optional): Add internationalization support
6. **Test**: Reload and test the plugin in QGIS
7. **Publish**: Publish to the QGIS Plugin Repository

---

## Required Files and Structure

### Minimal Plugin Structure

A minimal QGIS plugin requires only **2 mandatory files**:

```
my_plugin/
├── metadata.txt          # REQUIRED: Plugin metadata
├── __init__.py          # REQUIRED: Plugin entry point
├── main_plugin.py       # Main plugin code
├── icon.png            # Optional: Plugin icon
├── LICENSE             # Recommended: License file
└── README.md           # Recommended: Documentation
```

### Complete Plugin Structure

A fully-featured plugin typically includes:

```
my_plugin/
├── metadata.txt          # Plugin metadata
├── __init__.py          # Entry point with classFactory()
├── main_plugin.py       # Main plugin class
├── gui/
│   ├── dialog.py        # Custom dialogs
│   └── form.ui         # Qt Designer UI files
├── processing/
│   └── algorithms.py    # Processing algorithms
├── resources/
│   ├── icon.png        # Plugin icon
│   └── resources.qrc   # Qt resources
├── i18n/               # Translation files
│   └── plugin_lang.ts
├── tests/              # Unit tests
│   └── test_plugin.py
├── LICENSE
└── README.md
```

---

## metadata.txt Specification

The `metadata.txt` file contains plugin metadata and **must** be in UTF-8 encoding.

### Required Fields

```ini
[general]
name=MyPlugin
qgisMinimumVersion=3.40
description=Short description of the plugin
about=Longer description with details about the plugin functionality
version=1.0.0
author=Your Name
email=your.email@example.com
```

### Optional Fields

```ini
# Version constraints
qgisMaximumVersion=3.99

# Categorization
category=Vector
# Allowed values: Raster, Vector, Database, Web

tags=gis, processing, analysis

# Project links
homepage=https://github.com/yourname/plugin
repository=https://github.com/yourname/plugin
tracker=https://github.com/yourname/plugin/issues

# Status flags
experimental=False
deprecated=False

# Additional metadata
changelog=1.0.0 - Initial release
icon=resources/icon.png

# Dependencies
plugin_dependencies=other_plugin
```

### Complete Field Reference

| Field | Required | Type | Description |
|-------|----------|------|-------------|
| name | Yes | string | Short plugin name |
| qgisMinimumVersion | Yes | version | Minimum QGIS version (e.g., 3.40) |
| description | Yes | string | Brief description (no HTML) |
| about | Yes | string | Detailed description (no HTML) |
| version | Yes | version | Plugin version (dotted notation) |
| author | Yes | string | Author name |
| email | Yes | email | Author email |
| qgisMaximumVersion | No | version | Maximum QGIS version |
| category | No | enum | Plugin category |
| changelog | No | text | Version history |
| experimental | No | boolean | Mark as experimental |
| deprecated | No | boolean | Mark as deprecated |
| homepage | No | url | Plugin homepage |
| repository | No | url | Source code repository |
| tracker | No | url | Issue tracker |
| icon | No | path | Icon file path |
| tags | No | csv | Comma-separated tags |
| plugin_dependencies | No | csv | Required plugin names |

---

## Plugin Entry Point (__init__.py)

The `__init__.py` file is the plugin's entry point and **must** contain a `classFactory()` function.

### Minimal __init__.py

```python
def classFactory(iface):
    """Load MyPlugin class from file main_plugin.

    Args:
        iface (QgsInterface): A QGIS interface instance.

    Returns:
        MyPlugin: The plugin instance.
    """
    from .main_plugin import MyPlugin
    return MyPlugin(iface)
```

### Server Plugin Entry Point

For QGIS Server plugins, also include:

```python
def serverClassFactory(serverIface):
    """Load server plugin.

    Args:
        serverIface: QGIS Server interface instance.

    Returns:
        The server plugin instance.
    """
    from .server_plugin import MyServerPlugin
    return MyServerPlugin(serverIface)
```

---

## Main Plugin Class

The main plugin class contains the core logic and is initialized with the QGIS interface.

### Basic Plugin Template

```python
from qgis.PyQt.QtCore import QCoreApplication
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction
from qgis.core import QgsMessageLog, Qgis

class MyPlugin:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        Args:
            iface (QgsInterface): An interface instance that will be passed
                to this class which provides the hook by which you can
                manipulate the QGIS application at run time.
        """
        # Save reference to the QGIS interface
        self.iface = iface

        # Initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)

        # Initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            f'plugin_{locale}.qm'
        )

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr('&My Plugin')

    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        Args:
            message (str): String for translation.

        Returns:
            str: Translated string.
        """
        return QCoreApplication.translate('MyPlugin', message)

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""
        icon_path = os.path.join(self.plugin_dir, 'icon.png')

        action = QAction(
            QIcon(icon_path),
            self.tr('My Plugin'),
            self.iface.mainWindow()
        )
        action.triggered.connect(self.run)

        # Add toolbar button and menu item
        self.iface.addToolBarIcon(action)
        self.iface.addPluginToMenu(self.menu, action)

        self.actions.append(action)

    def unload(self):
        """Remove the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(self.menu, action)
            self.iface.removeToolBarIcon(action)

    def run(self):
        """Run method that performs all the real work."""
        # Your plugin logic here
        QgsMessageLog.logMessage(
            'Plugin executed!',
            'MyPlugin',
            Qgis.Info
        )
```

---

## QgsInterface (iface)

The `QgsInterface` class provides the main interface to interact with QGIS at runtime.

### Key Concepts

- **iface** is a global variable available in the QGIS Python console
- Plugins receive an `iface` instance in their constructor
- `iface` provides access to map canvas, menus, toolbars, and layers

### Common iface Methods

```python
# Access the map canvas
canvas = iface.mapCanvas()

# Access active layer
layer = iface.activeLayer()

# Add layer to map
iface.addVectorLayer('/path/to/file.shp', 'layer_name', 'ogr')

# Zoom to layer
iface.zoomToActiveLayer()

# Access main window
main_window = iface.mainWindow()

# Message bar (user notifications)
iface.messageBar().pushMessage(
    "Info",
    "This is a message",
    level=Qgis.Info
)

# Add menu items
iface.addPluginToMenu('Plugin Name', action)
iface.removePluginMenu('Plugin Name', action)

# Add toolbar buttons
iface.addToolBarIcon(action)
iface.removeToolBarIcon(action)

# Refresh map canvas
iface.mapCanvas().refresh()
```

### Map Canvas Interaction

```python
# Get map canvas
canvas = iface.mapCanvas()

# Get extent
extent = canvas.extent()

# Set extent
canvas.setExtent(new_extent)

# Get scale
scale = canvas.scale()

# Get center point
center = canvas.center()

# Get layer set
layers = canvas.layers()
```

---

## Best Practices

### Code Organization

1. **Separate concerns**: Keep GUI code separate from business logic
2. **Use proper imports**: Import only what you need
3. **Follow PEP 8**: Use Python style guidelines
4. **Modular design**: Break complex logic into smaller functions/classes

### Resource Management

1. **Clean up properly**: Always implement `unload()` to remove menu items and disconnect signals
2. **Use context managers**: For file operations and database connections
3. **Disconnect signals**: Remove signal connections in `unload()`

### Performance

1. **Avoid print()**: Never use `print()` in multithreaded code (expressions, renderers, processing algorithms)
2. **Lazy loading**: Load resources only when needed
3. **Progress feedback**: Use progress dialogs for long operations
4. **Cancel support**: Allow users to cancel long-running operations

### User Experience

1. **Provide feedback**: Use message bars for success/error messages
2. **Meaningful messages**: Write clear, actionable error messages
3. **Internationalization**: Use `self.tr()` for all user-facing strings
4. **Icons and UI**: Use consistent icons and follow QGIS UI patterns

---

## Logging and Error Handling

### QgsMessageLog

For communicating issues to users. Messages appear in the **Log Messages Panel**.

```python
from qgis.core import QgsMessageLog, Qgis

# Log levels: Info, Warning, Critical, Success
QgsMessageLog.logMessage(
    'This is an info message',
    'Plugin Name',
    Qgis.Info
)

QgsMessageLog.logMessage(
    'This is a warning',
    'Plugin Name',
    Qgis.Warning
)

QgsMessageLog.logMessage(
    'This is an error',
    'Plugin Name',
    Qgis.Critical
)
```

### QgsMessageBar

For temporary messages in the main window.

```python
from qgis.core import Qgis

# Simple message
iface.messageBar().pushMessage(
    "Info",
    "Operation completed successfully",
    level=Qgis.Success
)

# Message with duration (seconds)
iface.messageBar().pushMessage(
    "Warning",
    "Check your input data",
    level=Qgis.Warning,
    duration=5
)

# Message with widget
iface.messageBar().pushMessage(
    "Error",
    "Operation failed",
    level=Qgis.Critical,
    duration=0  # 0 = until dismissed
)
```

### Python Logging Module

For developer debugging (recommended for Python developers).

```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger('MyPlugin')

# Use logging
logger.debug('Debug message')
logger.info('Info message')
logger.warning('Warning message')
logger.error('Error message')
logger.exception('Exception occurred')  # Includes traceback
```

### Error Handling Patterns

```python
try:
    # Risky operation
    result = perform_operation()
except Exception as e:
    # Log error
    QgsMessageLog.logMessage(
        f'Error occurred: {str(e)}',
        'Plugin Name',
        Qgis.Critical
    )

    # Notify user
    iface.messageBar().pushMessage(
        "Error",
        f"Operation failed: {str(e)}",
        level=Qgis.Critical
    )

    # Re-raise if needed
    # raise
```

### Important Warnings

⚠️ **NEVER use `print()` in:**
- Expression functions
- Renderers
- Symbol layers
- Processing algorithms
- Any multithreaded code

Using `print()` in these contexts is **unsafe** and **severely impacts performance**.

---

## Testing

### Unit Testing with pytest

```python
# tests/test_plugin.py
import pytest
from qgis.core import QgsApplication

@pytest.fixture(scope='session')
def qgis_app():
    """Start QGIS application."""
    qgs = QgsApplication([], False)
    qgs.initQgis()
    yield qgs
    qgs.exitQgis()

def test_plugin_loads(qgis_app):
    """Test that plugin loads correctly."""
    from my_plugin import MyPlugin
    from qgis.utils import iface

    plugin = MyPlugin(iface)
    assert plugin is not None

def test_plugin_functionality(qgis_app):
    """Test plugin functionality."""
    # Your tests here
    pass
```

### Headless Testing

Use `pytest-qgis` for headless testing without launching the full QGIS GUI:

```bash
pytest --qgis-disable-gui
```

### Code Coverage

```bash
pytest --cov=my_plugin --cov-report=term-missing
```

The `term-missing` parameter shows which lines are not covered by tests.

### Testing Best Practices

1. **Test coverage**: Aim for high test coverage (>80%)
2. **Continuous integration**: Automate testing in CI/CD pipelines
3. **Test edge cases**: Include tests for error conditions
4. **Mock external dependencies**: Use mocks for file systems, databases, etc.

---

## PyQGIS Core APIs

### Vector Layer Operations

```python
from qgis.core import QgsVectorLayer, QgsProject

# Load vector layer
layer = QgsVectorLayer('/path/to/file.shp', 'layer_name', 'ogr')

# Check if layer is valid
if not layer.isValid():
    print("Layer failed to load!")

# Add layer to project
QgsProject.instance().addMapLayer(layer)

# Get features
for feature in layer.getFeatures():
    # Get attributes
    attrs = feature.attributes()

    # Get geometry
    geom = feature.geometry()

    # Get specific field
    value = feature['field_name']

# Memory layer
memory_layer = QgsVectorLayer(
    'Point?crs=epsg:4326&field=name:string&field=value:int',
    'memory_layer',
    'memory'
)
```

### Geometry Operations

```python
from qgis.core import QgsGeometry, QgsPointXY

# Create point
point = QgsPointXY(10.0, 20.0)
geom = QgsGeometry.fromPointXY(point)

# Create line
points = [QgsPointXY(0, 0), QgsPointXY(1, 1)]
geom = QgsGeometry.fromPolylineXY(points)

# Create polygon
points = [QgsPointXY(0, 0), QgsPointXY(1, 0),
          QgsPointXY(1, 1), QgsPointXY(0, 1)]
geom = QgsGeometry.fromPolygonXY([points])

# Geometry operations
buffer = geom.buffer(10, 5)
area = geom.area()
length = geom.length()
centroid = geom.centroid()
```

### Processing Framework

```python
from qgis import processing

# Run processing algorithm
result = processing.run("native:buffer", {
    'INPUT': layer,
    'DISTANCE': 100,
    'SEGMENTS': 5,
    'OUTPUT': 'memory:'
})

# Get output layer
output_layer = result['OUTPUT']
```

### Project Operations

```python
from qgis.core import QgsProject

# Get current project
project = QgsProject.instance()

# Get all layers
layers = project.mapLayers()

# Get layer by name
layer = project.mapLayersByName('layer_name')[0]

# Save project
project.write('/path/to/project.qgs')

# Read project
project.read('/path/to/project.qgs')
```

---

## Resources

### Official Documentation

- **PyQGIS Developer Cookbook**: https://docs.qgis.org/3.40/en/docs/pyqgis_developer_cookbook/
- **Structuring Python Plugins**: https://docs.qgis.org/3.40/en/docs/pyqgis_developer_cookbook/plugins/plugins.html
- **Plugin Development Guide**: https://docs.qgis.org/3.40/en/docs/pyqgis_developer_cookbook/plugins/index.html
- **Code Snippets**: https://docs.qgis.org/3.40/en/docs/pyqgis_developer_cookbook/plugins/snippets.html
- **PyQGIS API Documentation**: https://qgis.org/pyqgis/3.40/
- **Using Vector Layers**: https://docs.qgis.org/3.40/en/docs/pyqgis_developer_cookbook/vector.html

### Tutorials

- **Building a Python Plugin**: https://www.qgistutorials.com/en/docs/3/building_a_python_plugin.html
- **PyQGIS Masterclass**: https://courses.spatialthoughts.com/pyqgis-masterclass.html
- **QGIS Plugin Workshop**: https://courses.spatialthoughts.com/qgis-plugin-workshop.html

### Tools and Templates

- **Minimal Plugin Template**: https://github.com/wonder-sk/qgis-minimal-plugin
- **QGIS Plugin Template**: https://github.com/opengeos/qgis-plugin-template
- **Plugin Builder**: Built-in QGIS tool for generating plugin scaffolding
- **pb_tool**: Command-line tool for plugin development

### Additional Resources

- **QGIS API Reference**: https://api.qgis.org/api/classQgisInterface.html
- **Plugin Repository**: https://plugins.qgis.org/
- **QGIS Testing Documentation**: https://docs.qgis.org/testing/pdf/en/QGIS-testing-PyQGISDeveloperCookbook-en.pdf
- **GIS-OPS Plugin Testing Tutorial**: https://github.com/gis-ops/tutorials/blob/master/qgis/QGIS_PluginTesting.md

---

## Quick Reference: Common Tasks

### Add Menu Action

```python
action = QAction(QIcon('icon.png'), 'Action Text', self.iface.mainWindow())
action.triggered.connect(self.run_action)
self.iface.addPluginToMenu('Plugin Name', action)
```

### Show Dialog

```python
from qgis.PyQt.QtWidgets import QDialog
dialog = MyDialog()
result = dialog.exec_()
if result:
    # Dialog accepted
    pass
```

### Get Selected Features

```python
layer = iface.activeLayer()
selected_features = layer.selectedFeatures()
for feature in selected_features:
    print(feature.attributes())
```

### Add Features to Layer

```python
from qgis.core import QgsFeature, QgsGeometry, QgsPointXY

layer.startEditing()
feature = QgsFeature(layer.fields())
feature.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(10, 20)))
feature.setAttributes([value1, value2])
layer.addFeature(feature)
layer.commitChanges()
```

### Progress Dialog

```python
from qgis.PyQt.QtWidgets import QProgressDialog

progress = QProgressDialog("Processing...", "Cancel", 0, 100)
for i in range(100):
    if progress.wasCanceled():
        break
    # Do work
    progress.setValue(i)
```

---

**End of Reference Guide**
