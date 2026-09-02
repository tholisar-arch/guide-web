"""Recommendations screen: prioritized, rule-based action list with explanations."""
from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QComboBox, QHBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget

from app.core.abc_xyz import compute_abc_xyz
from app.core.recommendations import generate_recommendations, summarize
from app.core.stock_coverage import compute_coverage
from app.database.db_manager import DatabaseManager
from app.ui.widgets.common import KpiCard, PageHeader

PRIORITY_COLORS = {
    "Critical": QColor("#D64545"),
    "High": QColor("#E8834D"),
    "Medium": QColor("#E8A33D"),
    "Low": QColor("#1B9E77"),
}


class RecommendationsView(QWidget):
    def __init__(self, db: DatabaseManager):
        super().__init__()
        self.db = db
        self._full_df = None

        outer = QVBoxLayout(self)
        outer.setContentsMargins(24, 20, 24, 20)
        outer.setSpacing(14)

        outer.addWidget(
            PageHeader(
                "Recommendations",
                "Automatic, explained recommendations combining ABC/XYZ classification and stock coverage.",
            )
        )

        kpi_row = QHBoxLayout()
        self.critical_card = KpiCard("Critical")
        self.high_card = KpiCard("High")
        self.medium_card = KpiCard("Medium")
        self.low_card = KpiCard("Low")
        for c in (self.critical_card, self.high_card, self.medium_card, self.low_card):
            kpi_row.addWidget(c)
        outer.addLayout(kpi_row)

        filter_row = QHBoxLayout()
        filter_row.addWidget(QLabel("Filter by priority:"))
        self.priority_filter = QComboBox()
        self.priority_filter.addItems(["All", "Critical", "High", "Medium", "Low"])
        self.priority_filter.currentIndexChanged.connect(self._apply_filter)
        filter_row.addWidget(self.priority_filter)
        filter_row.addWidget(QLabel("Category:"))
        self.category_filter = QComboBox()
        self.category_filter.addItem("All")
        self.category_filter.currentIndexChanged.connect(self._apply_filter)
        filter_row.addWidget(self.category_filter)
        filter_row.addStretch(1)
        outer.addLayout(filter_row)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["SKU", "Product", "Priority", "Category", "Recommendation"])
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setWordWrap(True)
        self.table.itemSelectionChanged.connect(self._show_explanation)
        outer.addWidget(self.table, 2)

        self.explanation_label = QLabel("Select a recommendation to see the detailed explanation.")
        self.explanation_label.setWordWrap(True)
        self.explanation_label.setStyleSheet(
            "background:#FFFFFF; border:1px solid #E1E5EB; border-radius:8px; padding:12px; color:#1B2430;"
        )
        outer.addWidget(self.explanation_label)

    def refresh(self) -> None:
        sales_monthly = self.db.get_sales_monthly()
        latest_stock = self.db.get_latest_stock()
        products = self.db.get_products()
        params = self.db.get_simulation_params()

        abc_xyz_df = compute_abc_xyz(sales_monthly, products)
        coverage_df = compute_coverage(
            sales_monthly, latest_stock, products,
            service_level=params["service_level"],
            default_lead_time_days=params["lead_time_days"],
            review_period_days=params["review_period_days"],
        )
        self._full_df = generate_recommendations(abc_xyz_df, coverage_df)

        summary = summarize(self._full_df)
        self.critical_card.set_value(str(summary["critical"]))
        self.high_card.set_value(str(summary["high"]))
        self.medium_card.set_value(str(summary["medium"]))
        self.low_card.set_value(str(summary["low"]))

        current_cat = self.category_filter.currentText()
        self.category_filter.blockSignals(True)
        self.category_filter.clear()
        self.category_filter.addItem("All")
        if self._full_df is not None and not self._full_df.empty:
            for cat in sorted(self._full_df["category"].unique()):
                self.category_filter.addItem(cat)
        idx = self.category_filter.findText(current_cat)
        self.category_filter.setCurrentIndex(idx if idx >= 0 else 0)
        self.category_filter.blockSignals(False)

        self._apply_filter()

    def _apply_filter(self) -> None:
        if self._full_df is None or self._full_df.empty:
            self.table.setRowCount(0)
            return
        df = self._full_df
        priority = self.priority_filter.currentText()
        if priority != "All":
            df = df[df["priority"] == priority]
        category = self.category_filter.currentText()
        if category != "All":
            df = df[df["category"] == category]

        self.table.setRowCount(len(df))
        for row_idx, (_, r) in enumerate(df.iterrows()):
            values = [r["sku"], r["name"], r["priority"], r["category"], r["recommendation"]]
            for col_idx, value in enumerate(values):
                item = QTableWidgetItem(str(value))
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                if col_idx == 2:
                    item.setForeground(PRIORITY_COLORS.get(r["priority"], QColor("#1B2430")))
                item.setData(Qt.UserRole, r["explanation"])
                self.table.setItem(row_idx, col_idx, item)
        self.table.resizeColumnsToContents()
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.resizeRowsToContents()

    def _show_explanation(self) -> None:
        items = self.table.selectedItems()
        if not items:
            return
        text = items[0].data(Qt.UserRole)
        if text:
            self.explanation_label.setText(text)
