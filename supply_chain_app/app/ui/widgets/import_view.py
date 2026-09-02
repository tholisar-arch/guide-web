"""Import screen: pick a file, map its columns, preview and commit to SQLite."""
from __future__ import annotations

from pathlib import Path

import pandas as pd
from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFileDialog,
    QFormLayout,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QVBoxLayout,
    QWidget,
)

from app.core.importer import FIELD_SPECS, apply_mapping, guess_mapping, read_tabular_file
from app.database.db_manager import DatabaseManager
from app.ui.widgets.common import PageHeader, dataframe_to_table

IMPORT_TYPE_LABELS = {
    "products": "Product Master Data",
    "sales": "Sales History",
    "stock": "Stock Levels",
}


class ColumnMappingDialog(QDialog):
    """Lets the user confirm/adjust which source column feeds each expected field."""

    def __init__(self, columns: list[str], import_type: str, parent=None):
        super().__init__(parent)
        self.import_type = import_type
        self.setWindowTitle(f"Map Columns — {IMPORT_TYPE_LABELS[import_type]}")
        self.resize(420, 320)

        layout = QVBoxLayout(self)
        info = QLabel(
            "We pre-filled a best guess. Review each field and pick the matching "
            "column from your file (or 'None' to skip optional fields)."
        )
        info.setWordWrap(True)
        layout.addWidget(info)

        form = QFormLayout()
        self.combos: dict[str, QComboBox] = {}
        guessed = guess_mapping(columns, import_type)
        specs = FIELD_SPECS[import_type]
        for field_name, (required, _hints) in specs.items():
            combo = QComboBox()
            combo.addItem("(None)")
            combo.addItems(columns)
            guess = guessed.get(field_name)
            if guess and guess in columns:
                combo.setCurrentText(guess)
            label = field_name.replace("_", " ").title() + (" *" if required else "")
            form.addRow(label, combo)
            self.combos[field_name] = combo
        layout.addLayout(form)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def mapping(self) -> dict[str, str | None]:
        result = {}
        for field_name, combo in self.combos.items():
            text = combo.currentText()
            result[field_name] = None if text == "(None)" else text
        return result


class ImportView(QWidget):
    data_imported = Signal()

    def __init__(self, db: DatabaseManager):
        super().__init__()
        self.db = db
        self._raw_df: pd.DataFrame | None = None
        self._file_path: Path | None = None
        self._mapping: dict[str, str | None] | None = None

        outer = QVBoxLayout(self)
        outer.setContentsMargins(24, 20, 24, 20)
        outer.setSpacing(14)

        outer.addWidget(
            PageHeader(
                "Import Data",
                "Import product master data, sales history and stock snapshots from Excel or CSV files. "
                "All processing happens locally — nothing leaves this computer.",
            )
        )

        controls = QFrame()
        controls.setObjectName("card")
        controls_layout = QHBoxLayout(controls)
        controls_layout.setContentsMargins(16, 14, 16, 14)

        controls_layout.addWidget(QLabel("Data type:"))
        self.type_combo = QComboBox()
        for key, label in IMPORT_TYPE_LABELS.items():
            self.type_combo.addItem(label, userData=key)
        controls_layout.addWidget(self.type_combo)

        self.browse_btn = QPushButton("Browse File…")
        self.browse_btn.clicked.connect(self._browse)
        controls_layout.addWidget(self.browse_btn)

        self.file_label = QLabel("No file selected.")
        self.file_label.setStyleSheet("color:#5C6B7A;")
        controls_layout.addWidget(self.file_label, 1)

        self.map_btn = QPushButton("Map Columns…")
        self.map_btn.setObjectName("secondaryButton")
        self.map_btn.setEnabled(False)
        self.map_btn.clicked.connect(self._open_mapping)
        controls_layout.addWidget(self.map_btn)

        self.import_btn = QPushButton("Import")
        self.import_btn.setEnabled(False)
        self.import_btn.clicked.connect(self._do_import)
        controls_layout.addWidget(self.import_btn)

        outer.addWidget(controls)

        self.status_label = QLabel("")
        self.status_label.setWordWrap(True)
        outer.addWidget(self.status_label)

        outer.addWidget(QLabel("Preview (first 50 rows of the source file):"))
        self.preview_table = QTableWidget()
        outer.addWidget(self.preview_table, 2)

        outer.addWidget(QLabel("Import history:"))
        self.log_table = QTableWidget()
        outer.addWidget(self.log_table, 1)

    # ------------------------------------------------------------------
    def _browse(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self, "Select a file to import", "", "Spreadsheet files (*.xlsx *.xlsm *.xls *.csv)"
        )
        if not path:
            return
        try:
            self._raw_df = read_tabular_file(path)
        except Exception as exc:  # noqa: BLE001 - surfaced to the user, not swallowed
            QMessageBox.critical(self, "Could not read file", str(exc))
            return

        self._file_path = Path(path)
        self._mapping = None
        self.file_label.setText(self._file_path.name)
        dataframe_to_table(self.preview_table, self._raw_df.head(50))
        self.map_btn.setEnabled(True)
        self.import_btn.setEnabled(False)
        self.status_label.setText(f"Loaded {len(self._raw_df)} row(s), {len(self._raw_df.columns)} column(s).")

    def _open_mapping(self) -> None:
        if self._raw_df is None:
            return
        import_type = self.type_combo.currentData()
        columns = [str(c) for c in self._raw_df.columns]
        dialog = ColumnMappingDialog(columns, import_type, self)
        if dialog.exec() == QDialog.Accepted:
            self._mapping = dialog.mapping()
            self.import_btn.setEnabled(True)
            self.status_label.setText("Column mapping confirmed. Click Import to commit to the database.")

    def _do_import(self) -> None:
        if self._raw_df is None or self._mapping is None or self._file_path is None:
            return
        import_type = self.type_combo.currentData()
        try:
            result = apply_mapping(self._raw_df, self._mapping, import_type)
        except ValueError as exc:
            QMessageBox.warning(self, "Mapping incomplete", str(exc))
            return

        if result.rows_imported == 0:
            QMessageBox.warning(self, "Nothing to import", "No valid rows were found after validation.")
            return

        if import_type == "products":
            self.db.upsert_products(result.dataframe)
        elif import_type == "sales":
            self.db.insert_sales(result.dataframe)
        elif import_type == "stock":
            self.db.insert_stock(result.dataframe)

        self.db.log_import(self._file_path.name, import_type, result.rows_imported, result.rows_rejected)

        message = f"Imported {result.rows_imported} row(s) into {IMPORT_TYPE_LABELS[import_type]}."
        if result.rows_rejected:
            message += f" {result.rows_rejected} row(s) rejected."
        if result.warnings:
            message += " " + " ".join(result.warnings)
        self.status_label.setText(message)
        QMessageBox.information(self, "Import complete", message)

        self.import_btn.setEnabled(False)
        self._raw_df = None
        self._mapping = None
        self.file_label.setText("No file selected.")
        self.preview_table.clear()
        self.preview_table.setRowCount(0)
        self.preview_table.setColumnCount(0)

        self._refresh_log()
        self.data_imported.emit()

    def _refresh_log(self) -> None:
        dataframe_to_table(self.log_table, self.db.get_import_log())

    def refresh(self) -> None:
        self._refresh_log()
