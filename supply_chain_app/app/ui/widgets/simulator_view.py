"""Simulator screen: sliders for what-if business parameters, recomputed live."""
from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QSlider,
    QTableWidget,
    QVBoxLayout,
    QWidget,
)

from app.core.simulator import run_simulation
from app.database.db_manager import DatabaseManager
from app.ui.widgets.common import ExplanationBox, KpiCard, PageHeader, dataframe_to_table


class SliderRow(QWidget):
    """A labeled slider with a live value readout, on a 0-1000 internal scale for float precision."""

    def __init__(self, label: str, minimum: float, maximum: float, initial: float, suffix: str = "", parent=None):
        super().__init__(parent)
        self._min, self._max = minimum, maximum
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 4, 0, 4)
        self.name_label = QLabel(label)
        self.name_label.setMinimumWidth(190)
        layout.addWidget(self.name_label)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 1000)
        self.slider.setValue(self._to_slider(initial))
        layout.addWidget(self.slider, 1)

        self.value_label = QLabel()
        self.value_label.setMinimumWidth(70)
        self.value_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(self.value_label)

        self.suffix = suffix
        self.slider.valueChanged.connect(self._update_label)
        self._update_label()

    def _to_slider(self, value: float) -> int:
        return int(round((value - self._min) / (self._max - self._min) * 1000))

    def value(self) -> float:
        return self._min + (self.slider.value() / 1000) * (self._max - self._min)

    def _update_label(self) -> None:
        self.value_label.setText(f"{self.value():.1f}{self.suffix}")


class SimulatorView(QWidget):
    def __init__(self, db: DatabaseManager):
        super().__init__()
        self.db = db

        outer = QVBoxLayout(self)
        outer.setContentsMargins(24, 20, 24, 20)
        outer.setSpacing(14)

        outer.addWidget(
            PageHeader(
                "Simulator",
                "Move the sliders to explore what-if scenarios; safety stock, reorder points and coverage "
                "recompute instantly using the same formulas as the Stock Coverage screen.",
            )
        )

        controls = QFrame()
        controls.setObjectName("card")
        controls_layout = QVBoxLayout(controls)
        controls_layout.setContentsMargins(16, 14, 16, 14)

        self.service_level_slider = SliderRow("Target Service Level", 50.0, 99.9, 95.0, "%")
        self.lead_time_slider = SliderRow("Supplier Lead Time", 1, 90, 14, " days")
        self.review_period_slider = SliderRow("Review Period", 1, 30, 7, " days")
        self.growth_slider = SliderRow("Demand Growth", -50.0, 100.0, 0.0, "%")
        for row in (self.service_level_slider, self.lead_time_slider,
                    self.review_period_slider, self.growth_slider):
            row.slider.valueChanged.connect(self._recompute)
            controls_layout.addWidget(row)

        button_row = QHBoxLayout()
        self.save_btn = QPushButton("Save as New Baseline")
        self.save_btn.clicked.connect(self._save_baseline)
        self.reset_btn = QPushButton("Reset to Saved Baseline")
        self.reset_btn.setObjectName("secondaryButton")
        self.reset_btn.clicked.connect(self.refresh)
        button_row.addWidget(self.save_btn)
        button_row.addWidget(self.reset_btn)
        button_row.addStretch(1)
        controls_layout.addLayout(button_row)

        outer.addWidget(controls)

        kpi_grid = QGridLayout()
        self.safety_stock_before = KpiCard("Safety Stock — Before")
        self.safety_stock_after = KpiCard("Safety Stock — After")
        self.stockout_before = KpiCard("Stockout-Risk SKUs — Before")
        self.stockout_after = KpiCard("Stockout-Risk SKUs — After")
        self.excess_before = KpiCard("Excess SKUs — Before")
        self.excess_after = KpiCard("Excess SKUs — After")
        cards = [self.safety_stock_before, self.safety_stock_after, self.stockout_before,
                 self.stockout_after, self.excess_before, self.excess_after]
        for idx, card in enumerate(cards):
            kpi_grid.addWidget(card, idx // 3, idx % 3)
        outer.addLayout(kpi_grid)

        self.explanation = ExplanationBox("")
        outer.addWidget(self.explanation)

        outer.addWidget(QLabel("Simulated stock coverage detail:"))
        self.table = QTableWidget()
        outer.addWidget(self.table, 1)

    def refresh(self) -> None:
        params = self.db.get_simulation_params()
        self.service_level_slider.slider.setValue(self.service_level_slider._to_slider(params["service_level"] * 100))
        self.lead_time_slider.slider.setValue(self.lead_time_slider._to_slider(params["lead_time_days"]))
        self.review_period_slider.slider.setValue(self.review_period_slider._to_slider(params["review_period_days"]))
        self.growth_slider.slider.setValue(self.growth_slider._to_slider(params["demand_growth_pct"]))
        self._recompute()

    def _current_params(self) -> dict:
        return {
            "service_level": self.service_level_slider.value() / 100.0,
            "lead_time_days": self.lead_time_slider.value(),
            "review_period_days": self.review_period_slider.value(),
            "demand_growth_pct": self.growth_slider.value(),
        }

    def _recompute(self) -> None:
        sales_monthly = self.db.get_sales_monthly()
        latest_stock = self.db.get_latest_stock()
        products = self.db.get_products()
        baseline_params = self.db.get_simulation_params()
        simulated_params = self._current_params()

        result = run_simulation(sales_monthly, latest_stock, products, baseline_params, simulated_params)
        delta = result["delta"]

        self.safety_stock_before.set_value(f"{delta['total_safety_stock_before']:,.0f}")
        self.safety_stock_after.set_value(f"{delta['total_safety_stock_after']:,.0f}")
        self.stockout_before.set_value(str(delta["stockout_risk_count_before"]))
        self.stockout_after.set_value(str(delta["stockout_risk_count_after"]))
        self.excess_before.set_value(str(delta["excess_count_before"]))
        self.excess_after.set_value(str(delta["excess_count_after"]))

        safety_delta = delta["total_safety_stock_after"] - delta["total_safety_stock_before"]
        stockout_delta = delta["stockout_risk_count_after"] - delta["stockout_risk_count_before"]
        self.explanation.set_text(
            f"With service level {simulated_params['service_level']*100:.1f}%, lead time "
            f"{simulated_params['lead_time_days']:.0f} days, review period "
            f"{simulated_params['review_period_days']:.0f} days and demand growth "
            f"{simulated_params['demand_growth_pct']:+.1f}%: total safety stock changes by "
            f"{safety_delta:+,.0f} units and the number of stockout-risk SKUs changes by {stockout_delta:+d} "
            "versus the currently saved baseline."
        )

        sim_df = result["simulated"]
        display_cols = ["sku", "name", "avg_daily_demand", "lead_time_days", "safety_stock",
                         "reorder_point", "quantity_on_hand", "days_of_coverage", "coverage_status"]
        dataframe_to_table(self.table, sim_df[display_cols] if not sim_df.empty else sim_df)

    def _save_baseline(self) -> None:
        params = self._current_params()
        self.db.save_simulation_params(**params)
        QMessageBox.information(self, "Baseline saved",
                                 "The current slider values are now the saved baseline used across the app.")
