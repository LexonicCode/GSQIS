# GSQIS - QGIS Plugin Development Project

This repository contains a QGIS plugin project for geospatial analysis, developed for QGIS 3.40+.

## Repository Structure

```
GSQIS/
├── plugin/                          # Main plugin directory
│   ├── metadata.txt                # Plugin metadata
│   ├── __init__.py                # Plugin entry point
│   ├── gsqis_plugin.py            # Main plugin implementation
│   ├── resources/                  # Icons and resources
│   ├── tests/                      # Unit tests
│   ├── i18n/                       # Internationalization files
│   ├── LICENSE
│   └── README.md
├── QGIS_PLUGIN_DEV_GUIDE.md       # Comprehensive development reference
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```

## Quick Start

### Prerequisites

- **QGIS 3.40+** installed
- **Python 3.9+**
- Basic knowledge of Python and QGIS

### Installation for Development

1. **Clone the repository:**
   ```bash
   git clone https://github.com/LexonicCode/GSQIS.git
   cd GSQIS
   ```

2. **Install development dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Link plugin to QGIS:**

   Create a symbolic link from the plugin directory to your QGIS plugins folder:

   **Linux:**
   ```bash
   ln -s $(pwd)/plugin ~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/gsqis_plugin
   ```

   **Windows (Command Prompt as Administrator):**
   ```cmd
   mklink /D "%APPDATA%\QGIS\QGIS3\profiles\default\python\plugins\gsqis_plugin" "C:\path\to\GSQIS\plugin"
   ```

   **macOS:**
   ```bash
   ln -s $(pwd)/plugin ~/Library/Application\ Support/QGIS/QGIS3/profiles/default/python/plugins/gsqis_plugin
   ```

4. **Enable the plugin in QGIS:**
   - Open QGIS
   - Go to **Plugins > Manage and Install Plugins**
   - Find "GSQIS Plugin" and enable it

### Running Tests

```bash
cd plugin
pytest tests/
```

With coverage:
```bash
pytest --cov=. --cov-report=term-missing tests/
```

## Documentation

### QGIS Plugin Development Guide

The repository includes a comprehensive development guide based on the QGIS 3.40 PyQGIS Developer Cookbook:

📖 **[QGIS_PLUGIN_DEV_GUIDE.md](QGIS_PLUGIN_DEV_GUIDE.md)**

This guide covers:
- Plugin structure and required files
- PyQGIS API reference
- Best practices for plugin development
- Logging and error handling
- Testing strategies
- Common code patterns and examples

### Official QGIS Resources

- **PyQGIS Developer Cookbook**: https://docs.qgis.org/3.40/en/docs/pyqgis_developer_cookbook/
- **PyQGIS API Documentation**: https://qgis.org/pyqgis/3.40/
- **QGIS Plugin Repository**: https://plugins.qgis.org/

## Development Workflow

1. **Create a new branch for your feature:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** to the plugin code

3. **Test your changes:**
   ```bash
   pytest tests/
   ```

4. **Reload the plugin in QGIS:**
   - Use the **Plugin Reloader** plugin for quick development cycles
   - Or restart QGIS

5. **Commit and push:**
   ```bash
   git add .
   git commit -m "Description of changes"
   git push origin feature/your-feature-name
   ```

## Plugin Features (Planned)

- [ ] Custom geospatial analysis tools
- [ ] Processing algorithms
- [ ] Data visualization components
- [ ] Export/import functionality
- [ ] Integration with external services

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes with tests
4. Submit a pull request

## Development Tips

### Plugin Reloader

For faster development, install the **Plugin Reloader** plugin:
1. Open QGIS
2. Go to **Plugins > Manage and Install Plugins**
3. Search for "Plugin Reloader"
4. Install and use it to reload your plugin without restarting QGIS

### Debugging

Enable Python debugging in QGIS:
1. Go to **Settings > Options > System**
2. Check "Environment" section
3. Set `QGIS_DEBUG=1` for verbose logging

View debug messages in:
- **View > Panels > Log Messages**

### Code Quality

Format code with Black:
```bash
black plugin/
```

Check code style with flake8:
```bash
flake8 plugin/
```

## License

This project is licensed under the MIT License - see the [LICENSE](plugin/LICENSE) file for details.

## Support

For questions or issues:
- **GitHub Issues**: https://github.com/LexonicCode/GSQIS/issues
- **QGIS Documentation**: https://docs.qgis.org/3.40/

## Acknowledgments

This project is built using:
- **QGIS** - The world's leading open source GIS
- **PyQGIS** - Python bindings for QGIS
- **Qt/PyQt** - Cross-platform GUI framework

---

**Happy Plugin Development! 🗺️**
