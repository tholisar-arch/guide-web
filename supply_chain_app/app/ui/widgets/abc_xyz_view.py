"""ABC / XYZ analysis screen: Pareto chart, 3x3 matrix, and full detail table."""
from __future__ import annotations

from PySide6.QtWidgets import QHBoxLayout, QTableWidget, QVBoxLayout, QWidget

from app.core.abc_xyz import EXPLANATION, compute_abc_xyz, matrix_summary
from app.database.db_manager import DatabaseManager
from app.ui.widgets.chart_canvas import MplCanvas, PALETTE_SERIES
from app.ui.widgets.common import ExplanationBox, PageHeader, dataframe_to_table


class AbcXyzView(QWidget):
    def __init__(self, db: DatabaseManager):
        super().__init__()
        self.db = db

        outer = QVBoxLayout(self)
        outer.setContentsMargins(24, 20, 24, 20)
        outer.setSpacing(14)

        outer.addWidget(
            PageHeader(
                "ABC / XYZ Analysis",
                "Cross revenue contribution (ABC) with demand predictability (XYZ) to prioritize inventory policy.",
            )
        )

        top_row = QHBoxLayout()
        self.pareto_chart = MplCanvas(width=6.5, height=3.6)
        top_row.addWidget(self.pareto_chart, 2)

        self.matrix_table = QTableWidget(3, 3)
        self.matrix_table.setHorizontalHeaderLabels(["X (stable)", "Y (moderate)", "Z (erratic)"])
        self.matrix_table.setVerticalHeaderLabels(["A (top revenue)", "B (mid)", "C (long tail)"])
        self.matrix_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.matrix_table.setMaximumWidth(420)
        top_row.addWidget(self.matrix_table, 1)
        outer.addLayout(top_row)

        outer.addWidget(ExplanationBox(EXPLANATION))

        self.detail_table = QTableWidget()
        outer.addWidget(self.detail_table, 1)

    def refresh(self) -> None:
        sales_monthly = self.db.get_sales_monthly()
        products = self.db.get_products()
        df = compute_abc_xyz(sales_monthly, products)

        self._draw_pareto(df)
        self._fill_matrix(df)
        dataframe_to_table(self.detail_table, df)

    def _draw_pareto(self, df) -> None:
        canvas = self.pareto_chart
        canvas.clear()
        ax = canvas.axes
        if df.empty:
            ax.text(0.5, 0.5, "No sales data imported yet", ha="center", va="center", color="#5C6B7A")
            canvas.redraw()
            return

        x = range(1, len(df) + 1)
        ax2 = ax.twinx()
        ax.bar(x, df["total_revenue"], color=PALETTE_SERIES[0], alpha=0.85)
        ax2.plot(x, df["cum_revenue_share"] * 100, color=PALETTE_SERIES[2], linewidth=2, marker=".")
        ax2.axhline(80, color="#D64545", linestyle="--", linewidth=1)
        ax2.set_ylim(0, 105)
        ax.set_title("Pareto Curve — Revenue by SKU (ranked)", fontsize=10, color="#1F3B57", loc="left")
        ax.set_xticks([])
        ax2.tick_params(labelsize=8)
        canvas.redraw()

    def _fill_matrix(self, df) -> None:
        pivot = matrix_summary(df)
        revenue_pivot = (
            df.pivot_table(index="abc_class", columns="xyz_class", values="total_revenue",
                            aggfunc="sum", fill_value=0, observed=False)
            if not df.empty else None
        )
        for i, abc in enumerate(["A", "B", "C"]):
            for j, xyz in enumerate(["X", "Y", "Z"]):
                count = int(pivot.loc[abc, xyz]) if pivot is not None and not pivot.empty else 0
                revenue = (
                    float(revenue_pivot.loc[abc, xyz])
                    if revenue_pivot is not None and abc in revenue_pivot.index and xyz in revenue_pivot.columns
                    else 0.0
                )
                from PySide6.QtWidgets import QTableWidgetItem
                item = QTableWidgetItem(f"{count} SKU(s)\n{revenue:,.0f}")
                self.matrix_table.setItem(i, j, item)
        self.matrix_table.resizeRowsToContents()
        self.matrix_table.resizeColumnsToContents()
