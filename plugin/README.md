# GSQIS Plugin

A QGIS plugin for geospatial analysis developed using QGIS 3.40+.

## Features

- Custom geospatial analysis tools
- Integration with QGIS Processing framework
- User-friendly interface

## Installation

### Development Installation

1. Clone this repository
2. Copy the `plugin` directory to your QGIS plugins folder:
   - **Linux**: `~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/`
   - **Windows**: `C:\Users\<username>\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\`
   - **macOS**: `~/Library/Application Support/QGIS/QGIS3/profiles/default/python/plugins/`
3. Rename the directory to `gsqis_plugin`
4. Restart QGIS
5. Enable the plugin in **Plugins > Manage and Install Plugins**

### Plugin Repository Installation

(Coming soon - once published to QGIS Plugin Repository)

## Development

### Prerequisites

- QGIS 3.40 or higher
- Python 3.9+
- pytest (for testing)

### Project Structure

```
plugin/
├── metadata.txt          # Plugin metadata
├── __init__.py          # Plugin entry point
├── gsqis_plugin.py      # Main plugin class
├── resources/           # Icons and resources
├── tests/              # Unit tests
├── i18n/               # Translation files
├── LICENSE
└── README.md
```

### Testing

Run tests using pytest:

```bash
cd plugin
pytest tests/
```

For coverage report:

```bash
pytest --cov=. --cov-report=term-missing tests/
```

### Documentation

See [QGIS_PLUGIN_DEV_GUIDE.md](../QGIS_PLUGIN_DEV_GUIDE.md) for comprehensive development documentation based on the QGIS 3.40 PyQGIS Developer Cookbook.

## Usage

1. Open QGIS
2. Load a vector or raster layer
3. Click the GSQIS Plugin icon in the toolbar
4. (More detailed instructions will be added as features are developed)

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Resources

- [QGIS Plugin Development Guide](../QGIS_PLUGIN_DEV_GUIDE.md)
- [PyQGIS Developer Cookbook](https://docs.qgis.org/3.40/en/docs/pyqgis_developer_cookbook/)
- [QGIS API Documentation](https://qgis.org/pyqgis/3.40/)

## Changelog

### Version 0.1.0 (Development)

- Initial plugin structure
- Basic plugin skeleton
- Development environment setup
