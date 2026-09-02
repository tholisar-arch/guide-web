"""Stock coverage screen: reorder points, safety stock, and risk classification."""
from __future__ import annotations

from PySide6.QtWidgets import QHBoxLayout, QTableWidget, QVBoxLayout, QWidget

from app.core.stock_coverage import compute_coverage
from app.database.db_manager import DatabaseManager
from app.ui.widgets.chart_canvas import MplCanvas
from app.ui.widgets.common import ExplanationBox, KpiCard, PageHeader, dataframe_to_table

STATUS_COLORS = {
    "Stockout Risk": "#D64545",
    "Low": "#E8A33D",
    "Adequate": "#1B9E77",
    "Excess": "#2E86AB",
    "Excess (No Demand)": "#7C5CBF",
    "No Demand Data": "#9AA5B1",
}

EXPLANATION = (
    "Days of coverage = current stock / average daily demand. Reorder point = "
    "(average daily demand x lead time) + safety stock, where safety stock is sized "
    "to the chosen target service level (see the Simulator screen to adjust these "
    "parameters and see the impact instantly)."
)


class StockCoverageView(QWidget):
    def __init__(self, db: DatabaseManager):
        super().__init__()
        self.db = db

        outer = QVBoxLayout(self)
        outer.setContentsMargins(24, 20, 24, 20)
        outer.setSpacing(14)

        outer.addWidget(
            PageHeader(
                "Stock Coverage",
                "Days of forward coverage, safety stock and reorder points for every SKU.",
            )
        )

        kpi_row = QHBoxLayout()
        self.stockout_card = KpiCard("Stockout Risk SKUs")
        self.low_card = KpiCard("Low Coverage SKUs")
        self.excess_card = KpiCard("Excess Stock SKUs")
        self.value_card = KpiCard("Total Stock Value")
        for c in (self.stockout_card, self.low_card, self.excess_card, self.value_card):
            kpi_row.addWidget(c)
        outer.addLayout(kpi_row)

        self.status_chart = MplCanvas(width=10, height=2.8)
        outer.addWidget(self.status_chart)

        outer.addWidget(ExplanationBox(EXPLANATION))

        self.table = QTableWidget()
        outer.addWidget(self.table, 1)

    def refresh(self) -> None:
        sales_monthly = self.db.get_sales_monthly()
        latest_stock = self.db.get_latest_stock()
        products = self.db.get_products()
        params = self.db.get_simulation_params()

        df = compute_coverage(
            sales_monthly, latest_stock, products,
            service_level=params["service_level"],
            default_lead_time_days=params["lead_time_days"],
            review_period_days=params["review_period_days"],
        )

        if df.empty:
            self.stockout_card.set_value("-")
            self.low_card.set_value("-")
            self.excess_card.set_value("-")
            self.value_card.set_value("-")
        else:
            counts = df["coverage_status"].value_counts()
            self.stockout_card.set_value(str(int(counts.get("Stockout Risk", 0))))
            self.low_card.set_value(str(int(counts.get("Low", 0))))
            self.excess_card.set_value(str(int(counts.get("Excess", 0))))
            self.value_card.set_value(f"{df['stock_value'].sum():,.0f}")

        self._draw_status_chart(df)
        dataframe_to_table(self.table, df.drop(columns=["service_level_used", "z_score"], errors="ignore"))

    def _draw_status_chart(self, df) -> None:
        canvas = self.status_chart
        canvas.clear()
        ax = canvas.axes
        if df.empty:
            ax.text(0.5, 0.5, "Import stock levels to see coverage analysis",
                    ha="center", va="center", color="#5C6B7A")
            canvas.redraw()
            return
        counts = df["coverage_status"].value_counts()
        order = [s for s in STATUS_COLORS if s in counts.index]
        values = [counts[s] for s in order]
        colors = [STATUS_COLORS[s] for s in order]
        ax.barh(order, values, color=colors)
        ax.set_title("SKU Count by Coverage Status", fontsize=10, color="#1F3B57", loc="left")
        canvas.redraw()
