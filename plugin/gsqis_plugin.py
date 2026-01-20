"""
GSQIS Plugin - Main plugin implementation

This module contains the main plugin class.
"""

import os

from qgis.PyQt.QtCore import QCoreApplication, QSettings, QTranslator
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction
from qgis.core import QgsMessageLog, Qgis


class GSQISPlugin:
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
            f'gsqis_{locale}.qm'
        )

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr('&GSQIS Plugin')

        # Log plugin initialization
        QgsMessageLog.logMessage(
            'GSQIS Plugin initialized',
            'GSQIS',
            Qgis.Info
        )

    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        Args:
            message (str): String for translation.

        Returns:
            str: Translated string.
        """
        return QCoreApplication.translate('GSQISPlugin', message)

    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None
    ):
        """Add a toolbar icon to the toolbar.

        Args:
            icon_path (str): Path to the icon for this action
            text (str): Text that should be shown in menu items
            callback (function): Function to be called when action triggered
            enabled_flag (bool): A flag indicating if the action should be enabled
            add_to_menu (bool): Flag indicating whether to add action to menu
            add_to_toolbar (bool): Flag indicating whether to add action to toolbar
            status_tip (str): Optional text to show in a popup when mouse over
            whats_this (str): Optional text to show in whats this dialog
            parent (QWidget): Parent widget for the new action

        Returns:
            QAction: The action that was created
        """
        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.iface.addToolBarIcon(action)

        if add_to_menu:
            self.iface.addPluginToMenu(self.menu, action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""
        icon_path = os.path.join(self.plugin_dir, 'resources', 'icon.png')

        self.add_action(
            icon_path,
            text=self.tr('GSQIS Plugin'),
            callback=self.run,
            parent=self.iface.mainWindow(),
            status_tip=self.tr('Run GSQIS Plugin')
        )

        QgsMessageLog.logMessage(
            'GSQIS Plugin GUI initialized',
            'GSQIS',
            Qgis.Info
        )

    def unload(self):
        """Remove the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(self.menu, action)
            self.iface.removeToolBarIcon(action)

        QgsMessageLog.logMessage(
            'GSQIS Plugin unloaded',
            'GSQIS',
            Qgis.Info
        )

    def run(self):
        """Run method that performs all the real work."""
        try:
            # Log plugin execution
            QgsMessageLog.logMessage(
                'GSQIS Plugin executed',
                'GSQIS',
                Qgis.Info
            )

            # Show message to user
            self.iface.messageBar().pushMessage(
                "GSQIS",
                "Plugin executed successfully!",
                level=Qgis.Success,
                duration=3
            )

            # Your plugin logic goes here
            # Example: Get active layer
            active_layer = self.iface.activeLayer()
            if active_layer:
                QgsMessageLog.logMessage(
                    f'Active layer: {active_layer.name()}',
                    'GSQIS',
                    Qgis.Info
                )
            else:
                self.iface.messageBar().pushMessage(
                    "GSQIS",
                    "No active layer selected",
                    level=Qgis.Warning,
                    duration=3
                )

        except Exception as e:
            # Log error
            QgsMessageLog.logMessage(
                f'Error in GSQIS Plugin: {str(e)}',
                'GSQIS',
                Qgis.Critical
            )

            # Show error to user
            self.iface.messageBar().pushMessage(
                "Error",
                f"Plugin execution failed: {str(e)}",
                level=Qgis.Critical,
                duration=5
            )
