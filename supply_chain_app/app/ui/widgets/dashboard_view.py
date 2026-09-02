"""Dashboard screen: headline KPIs and trend/breakdown charts."""
from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGridLayout, QHBoxLayout, QScrollArea, QVBoxLayout, QWidget

from app.core import kpi as kpi_core
from app.database.db_manager import DatabaseManager
from app.ui.widgets.chart_canvas import MplCanvas, PALETTE_SERIES
from app.ui.widgets.common import KpiCard, PageHeader


class DashboardView(QWidget):
    def __init__(self, db: DatabaseManager):
        super().__init__()
        self.db = db

        outer = QVBoxLayout(self)
        outer.setContentsMargins(24, 20, 24, 20)
        outer.setSpacing(16)

        outer.addWidget(
            PageHeader(
                "Dashboard",
                "Portfolio-wide KPIs across sales, stock and revenue — refreshed from the local database.",
            )
        )

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.NoFrame)
        outer.addWidget(scroll, 1)

        content = QWidget()
        scroll.setWidget(content)
        self.content_layout = QVBoxLayout(content)
        self.content_layout.setSpacing(16)

        self.kpi_grid = QGridLayout()
        self.kpi_grid.setSpacing(12)
        self.content_layout.addLayout(self.kpi_grid)

        self.cards = {
            "total_revenue": KpiCard("Total Revenue"),
            "total_units_sold": KpiCard("Units Sold"),
            "total_stock_value": KpiCard("Stock Value"),
            "num_active_skus": KpiCard("Active SKUs"),
            "average_selling_price": KpiCard("Avg. Selling Price"),
            "total_units_in_stock": KpiCard("Units in Stock"),
        }
        for idx, card in enumerate(self.cards.values()):
            self.kpi_grid.addWidget(card, idx // 3, idx % 3)

        charts_row = QHBoxLayout()
        charts_row.setSpacing(16)
        self.trend_canvas = MplCanvas(width=6, height=3.4)
        self.category_canvas = MplCanvas(width=4, height=3.4)
        charts_row.addWidget(self.trend_canvas, 2)
        charts_row.addWidget(self.category_canvas, 1)
        self.content_layout.addLayout(charts_row)

        self.top_products_canvas = MplCanvas(width=10, height=3.6)
        self.content_layout.addWidget(self.top_products_canvas)
        self.content_layout.addStretch(1)

    def refresh(self) -> None:
        sales = self.db.get_sales()
        sales_monthly = self.db.get_sales_monthly()
        latest_stock = self.db.get_latest_stock()
        products = self.db.get_products()

        kpis = kpi_core.compute_headline_kpis(sales, latest_stock, products)
        self.cards["total_revenue"].set_value(f"{kpis['total_revenue']:,.0f}")
        self.cards["total_units_sold"].set_value(f"{kpis['total_units_sold']:,.0f}")
        self.cards["total_stock_value"].set_value(f"{kpis['total_stock_value']:,.0f}")
        self.cards["num_active_skus"].set_value(f"{kpis['num_active_skus']:,}")
        self.cards["average_selling_price"].set_value(f"{kpis['average_selling_price']:,.2f}")
        self.cards["total_units_in_stock"].set_value(f"{kpis['total_units_in_stock']:,.0f}")

        self._draw_trend(sales_monthly)
        self._draw_category(sales, products)
        self._draw_top_products(sales, products)

    def _draw_trend(self, sales_monthly) -> None:
        canvas = self.trend_canvas
        canvas.clear()
        trend = kpi_core.revenue_trend(sales_monthly)
        ax = canvas.axes
        if trend.empty:
            ax.text(0.5, 0.5, "No sales data imported yet", ha="center", va="center", color="#5C6B7A")
        else:
            ax.plot(trend["period"], trend["revenue"], marker="o", color=PALETTE_SERIES[0], linewidth=2)
            ax.set_title("Monthly Revenue Trend", fontsize=10, color="#1F3B57", loc="left")
            ax.tick_params(axis="x", rotation=45)
        canvas.redraw()

    def _draw_category(self, sales, products) -> None:
        canvas = self.category_canvas
        canvas.clear()
        by_cat = kpi_core.revenue_by_category(sales, products)
        ax = canvas.axes
        if by_cat.empty:
            ax.text(0.5, 0.5, "No data", ha="center", va="center", color="#5C6B7A")
        else:
            top = by_cat.head(6)
            ax.pie(
                top["revenue"], labels=top["category"], autopct="%1.0f%%",
                colors=PALETTE_SERIES * 2, textprops={"fontsize": 7.5},
            )
            ax.set_title("Revenue by Category", fontsize=10, color="#1F3B57")
        canvas.redraw()

    def _draw_top_products(self, sales, products) -> None:
        canvas = self.top_products_canvas
        canvas.clear()
        top = kpi_core.top_products_by_revenue(sales, products, top_n=10)
        ax = canvas.axes
        if top.empty:
            ax.text(0.5, 0.5, "No sales data imported yet", ha="center", va="center", color="#5C6B7A")
        else:
            top = top.sort_values("revenue")
            ax.barh(top["name"].astype(str).str.slice(0, 30), top["revenue"], color=PALETTE_SERIES[0])
            ax.set_title("Top 10 Products by Revenue", fontsize=10, color="#1F3B57", loc="left")
        canvas.redraw()
