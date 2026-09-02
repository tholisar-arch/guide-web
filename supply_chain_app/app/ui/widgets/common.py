"""Small reusable UI building blocks shared across screens."""
from __future__ import annotations

import pandas as pd
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)


class KpiCard(QFrame):
    """A single 'stat tile': big value, small caption label."""

    def __init__(self, label: str, value: str = "-", parent: QWidget | None = None):
        super().__init__(parent)
        self.setObjectName("card")
        self.setMinimumHeight(90)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 14, 16, 14)
        layout.setSpacing(4)

        self.value_label = QLabel(value)
        self.value_label.setObjectName("kpiValue")
        self.caption_label = QLabel(label.upper())
        self.caption_label.setObjectName("kpiLabel")
        self.caption_label.setWordWrap(True)

        layout.addWidget(self.value_label)
        layout.addWidget(self.caption_label)

    def set_value(self, value: str) -> None:
        self.value_label.setText(value)


class PageHeader(QWidget):
    """Title + subtitle banner used at the top of every screen."""

    def __init__(self, title: str, subtitle: str = "", parent: QWidget | None = None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)
        title_label = QLabel(title)
        title_label.setObjectName("pageTitle")
        layout.addWidget(title_label)
        if subtitle:
            subtitle_label = QLabel(subtitle)
            subtitle_label.setObjectName("pageSubtitle")
            subtitle_label.setWordWrap(True)
            layout.addWidget(subtitle_label)


class ExplanationBox(QFrame):
    """A quiet, always-visible panel explaining how the numbers above were derived."""

    def __init__(self, text: str = "", parent: QWidget | None = None):
        super().__init__(parent)
        self.setObjectName("card")
        layout = QHBoxLayout(self)
        layout.setContentsMargins(14, 10, 14, 10)
        icon = QLabel("ℹ")
        icon.setStyleSheet("font-size: 14pt; color: #2E86AB;")
        layout.addWidget(icon, 0, Qt.AlignTop)
        self.text_label = QLabel(text)
        self.text_label.setWordWrap(True)
        self.text_label.setStyleSheet("color: #5C6B7A; font-size: 9pt;")
        layout.addWidget(self.text_label, 1)

    def set_text(self, text: str) -> None:
        self.text_label.setText(text)


def dataframe_to_table(table: QTableWidget, df: pd.DataFrame, float_cols: tuple[str, ...] = ()) -> None:
    """Populate a QTableWidget from a pandas DataFrame."""
    table.clear()
    table.setRowCount(0)
    table.setColumnCount(0)
    if df is None or df.empty:
        return

    table.setColumnCount(len(df.columns))
    table.setHorizontalHeaderLabels([str(c).replace("_", " ").title() for c in df.columns])
    table.setRowCount(len(df))
    table.setAlternatingRowColors(True)
    table.setEditTriggers(QTableWidget.NoEditTriggers)
    table.setSelectionBehavior(QTableWidget.SelectRows)

    for row_idx, (_, row) in enumerate(df.iterrows()):
        for col_idx, col_name in enumerate(df.columns):
            value = row[col_name]
            if isinstance(value, float):
                text = f"{value:,.2f}" if col_name in float_cols or True else str(value)
            elif isinstance(value, bool):
                text = "Yes" if value else "No"
            else:
                text = str(value)
            item = QTableWidgetItem(text)
            item.setFlags(item.flags() & ~Qt.ItemIsEditable)
            table.setItem(row_idx, col_idx, item)

    table.resizeColumnsToContents()
    table.horizontalHeader().setStretchLastSection(True)
