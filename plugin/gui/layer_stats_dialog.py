"""
Layer Statistics Dialog.

A dialog that displays summary statistics for the active vector layer,
including basic layer info and per-field numeric/categorical statistics.
"""

from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QTabWidget,
    QTableWidget,
    QTableWidgetItem,
    QTextEdit,
    QPushButton,
    QFileDialog,
    QHeaderView,
    QGroupBox,
    QFormLayout,
    QComboBox,
    QWidget,
)
from qgis.core import QgsProject, QgsVectorLayer, QgsMessageLog, Qgis

from ..core.layer_stats import (
    compute_layer_info,
    compute_all_field_stats,
    format_stats_as_text,
)


class LayerStatsDialog(QDialog):
    """Dialog for displaying vector layer statistics."""

    def __init__(self, iface, parent=None):
        """Initialize the dialog.

        Args:
            iface: QGIS interface instance.
            parent: Optional parent widget.
        """
        super().__init__(parent)
        self.iface = iface
        self._layer_info = None
        self._field_stats = None
        self._setup_ui()
        self._populate_layer_combo()
        self._on_layer_changed()

    def _setup_ui(self):
        """Build the dialog UI programmatically."""
        self.setWindowTitle("Layer Statistics")
        self.setMinimumSize(600, 500)
        self.resize(700, 550)

        layout = QVBoxLayout(self)

        # Layer selector
        selector_layout = QHBoxLayout()
        selector_layout.addWidget(QLabel("Layer:"))
        self.layer_combo = QComboBox()
        self.layer_combo.currentIndexChanged.connect(self._on_layer_changed)
        selector_layout.addWidget(self.layer_combo, stretch=1)
        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.clicked.connect(self._on_refresh)
        selector_layout.addWidget(self.refresh_btn)
        layout.addLayout(selector_layout)

        # Tab widget
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs, stretch=1)

        # --- Overview tab ---
        self.overview_group = QGroupBox("Layer Information")
        overview_form = QFormLayout(self.overview_group)
        self.info_labels = {}
        for key, label in [
            ("name", "Name"),
            ("crs", "CRS"),
            ("geometry_type", "Geometry Type"),
            ("feature_count", "Feature Count"),
            ("field_count", "Field Count"),
            ("extent", "Extent"),
        ]:
            value_label = QLabel("—")
            value_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
            self.info_labels[key] = value_label
            overview_form.addRow(f"{label}:", value_label)
        self.tabs.addTab(self.overview_group, "Overview")

        # --- Field Statistics tab ---
        self.stats_table = QTableWidget()
        self.stats_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.stats_table.setAlternatingRowColors(True)
        self.stats_table.setSortingEnabled(True)
        self.tabs.addTab(self.stats_table, "Field Statistics")

        # --- Text Report tab ---
        self.report_text = QTextEdit()
        self.report_text.setReadOnly(True)
        self.report_text.setFontFamily("monospace")
        self.tabs.addTab(self.report_text, "Text Report")

        # Bottom buttons
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        self.export_btn = QPushButton("Export Report...")
        self.export_btn.clicked.connect(self._on_export)
        btn_layout.addWidget(self.export_btn)
        self.close_btn = QPushButton("Close")
        self.close_btn.clicked.connect(self.close)
        btn_layout.addWidget(self.close_btn)
        layout.addLayout(btn_layout)

    def _populate_layer_combo(self):
        """Fill the layer combo box with available vector layers."""
        self.layer_combo.blockSignals(True)
        self.layer_combo.clear()

        layers = QgsProject.instance().mapLayers().values()
        vector_layers = [
            l for l in layers if isinstance(l, QgsVectorLayer)
        ]

        if not vector_layers:
            self.layer_combo.addItem("(no vector layers)", None)
        else:
            # Put the active layer first if it's a vector layer
            active = self.iface.activeLayer()
            if isinstance(active, QgsVectorLayer) and active in vector_layers:
                vector_layers.remove(active)
                vector_layers.insert(0, active)
            for layer in vector_layers:
                self.layer_combo.addItem(layer.name(), layer.id())

        self.layer_combo.blockSignals(False)

    def _get_selected_layer(self):
        """Return the currently selected QgsVectorLayer or None."""
        layer_id = self.layer_combo.currentData()
        if layer_id is None:
            return None
        return QgsProject.instance().mapLayer(layer_id)

    def _on_layer_changed(self):
        """Recompute statistics when the selected layer changes."""
        layer = self._get_selected_layer()
        if layer is None:
            self._clear()
            return
        self._compute_and_display(layer)

    def _on_refresh(self):
        """Refresh the layer list and recompute."""
        self._populate_layer_combo()
        self._on_layer_changed()

    def _clear(self):
        """Clear all displayed statistics."""
        for label in self.info_labels.values():
            label.setText("—")
        self.stats_table.setRowCount(0)
        self.stats_table.setColumnCount(0)
        self.report_text.clear()
        self._layer_info = None
        self._field_stats = None

    def _compute_and_display(self, layer):
        """Compute stats and populate all tabs.

        Args:
            layer (QgsVectorLayer): The layer to analyze.
        """
        try:
            self._layer_info = compute_layer_info(layer)
            self._field_stats = compute_all_field_stats(layer)
        except Exception as e:
            QgsMessageLog.logMessage(
                f"Error computing statistics: {e}", "GSQIS", Qgis.Critical
            )
            self._clear()
            self.report_text.setPlainText(f"Error computing statistics:\n{e}")
            return

        # Overview tab
        for key, label in self.info_labels.items():
            label.setText(str(self._layer_info.get(key, "—")))

        # Field Statistics tab
        self._populate_stats_table()

        # Text Report tab
        report = format_stats_as_text(self._layer_info, self._field_stats)
        self.report_text.setPlainText(report)

    def _populate_stats_table(self):
        """Fill the statistics table with per-field data."""
        if not self._field_stats:
            self.stats_table.setRowCount(0)
            self.stats_table.setColumnCount(0)
            return

        columns = [
            "Field", "Type", "Count", "Min", "Max",
            "Mean", "Median", "Std Dev", "Unique",
        ]
        self.stats_table.setColumnCount(len(columns))
        self.stats_table.setHorizontalHeaderLabels(columns)
        self.stats_table.setRowCount(len(self._field_stats))

        for row, entry in enumerate(self._field_stats):
            stats = entry["stats"] or {}
            self.stats_table.setItem(row, 0, QTableWidgetItem(entry["name"]))
            self.stats_table.setItem(row, 1, QTableWidgetItem(entry["type_name"]))

            if entry["is_numeric"]:
                self._set_cell(row, 2, stats.get("count"))
                self._set_cell(row, 3, stats.get("min"))
                self._set_cell(row, 4, stats.get("max"))
                self._set_cell(row, 5, stats.get("mean"))
                self._set_cell(row, 6, stats.get("median"))
                self._set_cell(row, 7, stats.get("std_dev"))
                self._set_cell(row, 8, "—")
            else:
                self._set_cell(row, 2, stats.get("count"))
                self._set_cell(row, 3, "—")
                self._set_cell(row, 4, "—")
                self._set_cell(row, 5, "—")
                self._set_cell(row, 6, "—")
                self._set_cell(row, 7, "—")
                self._set_cell(row, 8, stats.get("unique_count"))

        self.stats_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents
        )

    def _set_cell(self, row, col, value):
        """Set a table cell, formatting numbers nicely.

        Args:
            row (int): Row index.
            col (int): Column index.
            value: The value to display.
        """
        if value is None:
            text = "—"
        elif isinstance(value, float):
            text = f"{value:.6g}"
        else:
            text = str(value)
        item = QTableWidgetItem(text)
        item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.stats_table.setItem(row, col, item)

    def _on_export(self):
        """Export the text report to a file."""
        if not self._layer_info:
            return
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Layer Statistics",
            f"{self._layer_info['name']}_stats.txt",
            "Text Files (*.txt);;All Files (*)",
        )
        if not path:
            return
        try:
            report = format_stats_as_text(self._layer_info, self._field_stats)
            with open(path, "w", encoding="utf-8") as f:
                f.write(report)
            QgsMessageLog.logMessage(
                f"Statistics exported to {path}", "GSQIS", Qgis.Info
            )
        except Exception as e:
            QgsMessageLog.logMessage(
                f"Failed to export statistics: {e}", "GSQIS", Qgis.Critical
            )
