"""Sales forecasting screen: per-SKU forecast with method choice and explanation."""
from __future__ import annotations

import numpy as np
from PySide6.QtWidgets import QComboBox, QFrame, QHBoxLayout, QLabel, QSpinBox, QVBoxLayout, QWidget

from app.config import FORECAST_HORIZON_MONTHS
from app.core import forecasting
from app.database.db_manager import DatabaseManager
from app.ui.widgets.chart_canvas import MplCanvas, PALETTE_SERIES
from app.ui.widgets.common import ExplanationBox, KpiCard, PageHeader

METHOD_CHOICES = ["Auto (best fit)"] + list(forecasting.METHODS.keys())


class ForecastView(QWidget):
    def __init__(self, db: DatabaseManager):
        super().__init__()
        self.db = db
        self._sales_monthly = None

        outer = QVBoxLayout(self)
        outer.setContentsMargins(24, 20, 24, 20)
        outer.setSpacing(14)

        outer.addWidget(
            PageHeader(
                "Sales Forecast",
                "Per-SKU demand forecast using classical, explainable statistical methods.",
            )
        )

        controls = QFrame()
        controls.setObjectName("card")
        controls_layout = QHBoxLayout(controls)
        controls_layout.setContentsMargins(16, 14, 16, 14)

        controls_layout.addWidget(QLabel("SKU:"))
        self.sku_combo = QComboBox()
        self.sku_combo.setMinimumWidth(260)
        self.sku_combo.currentIndexChanged.connect(self._recompute)
        controls_layout.addWidget(self.sku_combo)

        controls_layout.addWidget(QLabel("Method:"))
        self.method_combo = QComboBox()
        self.method_combo.addItems(METHOD_CHOICES)
        self.method_combo.currentIndexChanged.connect(self._recompute)
        controls_layout.addWidget(self.method_combo)

        controls_layout.addWidget(QLabel("Horizon (months):"))
        self.horizon_spin = QSpinBox()
        self.horizon_spin.setRange(1, 24)
        self.horizon_spin.setValue(FORECAST_HORIZON_MONTHS)
        self.horizon_spin.valueChanged.connect(self._recompute)
        controls_layout.addWidget(self.horizon_spin)
        controls_layout.addStretch(1)

        outer.addWidget(controls)

        kpi_row = QHBoxLayout()
        self.mae_card = KpiCard("MAE (units)")
        self.rmse_card = KpiCard("RMSE (units)")
        self.mape_card = KpiCard("MAPE")
        self.next_month_card = KpiCard("Next Month Forecast")
        for c in (self.mae_card, self.rmse_card, self.mape_card, self.next_month_card):
            kpi_row.addWidget(c)
        outer.addLayout(kpi_row)

        self.chart = MplCanvas(width=10, height=4)
        outer.addWidget(self.chart, 1)

        self.explanation = ExplanationBox("Select a SKU to see its forecast.")
        outer.addWidget(self.explanation)

    def refresh(self) -> None:
        self._sales_monthly = self.db.get_sales_monthly()
        products = self.db.get_products()

        current = self.sku_combo.currentData()
        self.sku_combo.blockSignals(True)
        self.sku_combo.clear()
        if not self._sales_monthly.empty:
            skus_with_sales = sorted(self._sales_monthly["sku"].unique())
            name_by_sku = dict(zip(products["sku"], products["name"])) if not products.empty else {}
            for sku in skus_with_sales:
                label = f"{sku} — {name_by_sku.get(sku, sku)}"
                self.sku_combo.addItem(label, userData=sku)
        self.sku_combo.blockSignals(False)

        if current:
            idx = self.sku_combo.findData(current)
            if idx >= 0:
                self.sku_combo.setCurrentIndex(idx)
        self._recompute()

    def _recompute(self) -> None:
        self.chart.clear()
        sku = self.sku_combo.currentData()
        if not sku or self._sales_monthly is None or self._sales_monthly.empty:
            self.chart.axes.text(0.5, 0.5, "Import sales history to see a forecast",
                                  ha="center", va="center", color="#5C6B7A")
            self.chart.redraw()
            self.explanation.set_text("No sales data imported yet.")
            for c in (self.mae_card, self.rmse_card, self.mape_card, self.next_month_card):
                c.set_value("-")
            return

        series = forecasting.build_series(self._sales_monthly, sku)
        horizon = self.horizon_spin.value()
        method_label = self.method_combo.currentText()

        if method_label == "Auto (best fit)":
            result = forecasting.auto_forecast(series, horizon)
        else:
            result = forecasting.METHODS[method_label](series, horizon)

        ax = self.chart.axes
        ax.plot(result.history.index, result.history.values, marker="o", label="Actual",
                color=PALETTE_SERIES[1], linewidth=2)
        if not result.fitted.dropna().empty:
            ax.plot(result.fitted.index, result.fitted.values, linestyle="--", label="Fitted",
                    color=PALETTE_SERIES[0], linewidth=1.5)
        if not result.forecast.empty:
            ax.plot(result.forecast.index, result.forecast.values, marker="s", linestyle="-.",
                    label="Forecast", color=PALETTE_SERIES[2], linewidth=2)
        ax.set_title(f"{sku} — {result.method}", fontsize=10, color="#1F3B57", loc="left")
        ax.tick_params(axis="x", rotation=45)
        ax.legend(fontsize=8, frameon=False)
        self.chart.redraw()

        mape = result.accuracy.get("mape", float("nan"))
        self.mae_card.set_value(f"{result.accuracy['mae']:.1f}" if not np.isnan(result.accuracy["mae"]) else "n/a")
        self.rmse_card.set_value(f"{result.accuracy['rmse']:.1f}" if not np.isnan(result.accuracy["rmse"]) else "n/a")
        self.mape_card.set_value(f"{mape:.1f}%" if not np.isnan(mape) else "n/a")
        next_val = result.forecast.iloc[0] if not result.forecast.empty else float("nan")
        self.next_month_card.set_value(f"{next_val:,.0f} units" if not np.isnan(next_val) else "n/a")

        self.explanation.set_text(result.explanation)
