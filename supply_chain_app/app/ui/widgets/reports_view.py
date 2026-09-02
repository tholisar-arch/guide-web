"""Reports screen: generate PDF and Excel exports of the current analysis."""
from __future__ import annotations

from datetime import datetime

from PySide6.QtCore import QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QMessageBox, QPushButton, QVBoxLayout, QWidget

from app.config import REPORTS_DIR
from app.core import kpi as kpi_core
from app.core.abc_xyz import compute_abc_xyz, matrix_summary
from app.core.recommendations import generate_recommendations
from app.core.stock_coverage import compute_coverage
from app.database.db_manager import DatabaseManager
from app.reports.excel_report import build_excel_report
from app.reports.pdf_report import build_pdf_report
from app.ui.widgets.common import PageHeader


class ReportsView(QWidget):
    def __init__(self, db: DatabaseManager):
        super().__init__()
        self.db = db

        outer = QVBoxLayout(self)
        outer.setContentsMargins(24, 20, 24, 20)
        outer.setSpacing(16)

        outer.addWidget(
            PageHeader(
                "Reports",
                "Generate a PDF executive report or a multi-sheet Excel workbook from the current "
                "dashboard, ABC/XYZ, stock coverage and recommendations data. Files are saved locally.",
            )
        )

        card = QFrame()
        card.setObjectName("card")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(20, 20, 20, 20)
        card_layout.setSpacing(12)

        card_layout.addWidget(QLabel(f"Output folder: {REPORTS_DIR}"))

        btn_row = QHBoxLayout()
        self.pdf_btn = QPushButton("Generate PDF Report")
        self.pdf_btn.clicked.connect(self._generate_pdf)
        self.excel_btn = QPushButton("Generate Excel Report")
        self.excel_btn.clicked.connect(self._generate_excel)
        self.open_folder_btn = QPushButton("Open Reports Folder")
        self.open_folder_btn.setObjectName("secondaryButton")
        self.open_folder_btn.clicked.connect(self._open_folder)
        btn_row.addWidget(self.pdf_btn)
        btn_row.addWidget(self.excel_btn)
        btn_row.addWidget(self.open_folder_btn)
        btn_row.addStretch(1)
        card_layout.addLayout(btn_row)

        self.status_label = QLabel("No report generated yet in this session.")
        self.status_label.setWordWrap(True)
        card_layout.addWidget(self.status_label)

        outer.addWidget(card)
        outer.addStretch(1)

    def refresh(self) -> None:
        pass

    def _gather_data(self) -> dict:
        sales = self.db.get_sales()
        sales_monthly = self.db.get_sales_monthly()
        latest_stock = self.db.get_latest_stock()
        products = self.db.get_products()
        params = self.db.get_simulation_params()

        kpis = kpi_core.compute_headline_kpis(sales, latest_stock, products)
        top_products = kpi_core.top_products_by_revenue(sales, products, top_n=15)
        abc_xyz = compute_abc_xyz(sales_monthly, products)
        coverage = compute_coverage(
            sales_monthly, latest_stock, products,
            service_level=params["service_level"],
            default_lead_time_days=params["lead_time_days"],
            review_period_days=params["review_period_days"],
        )
        recommendations = generate_recommendations(abc_xyz, coverage)
        return {
            "kpis": kpis, "top_products": top_products, "abc_xyz": abc_xyz,
            "coverage": coverage, "recommendations": recommendations,
        }

    def _generate_pdf(self) -> None:
        try:
            data = self._gather_data()
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = REPORTS_DIR / f"supply_chain_report_{timestamp}.pdf"
            build_pdf_report(
                output_path, data["kpis"], data["top_products"], matrix_summary(data["abc_xyz"]),
                data["coverage"], data["recommendations"],
            )
            self.status_label.setText(f"PDF report generated: {output_path}")
            QMessageBox.information(self, "Report generated", f"PDF report saved to:\n{output_path}")
        except Exception as exc:  # noqa: BLE001
            QMessageBox.critical(self, "Report generation failed", str(exc))

    def _generate_excel(self) -> None:
        try:
            data = self._gather_data()
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = REPORTS_DIR / f"supply_chain_report_{timestamp}.xlsx"
            build_excel_report(
                output_path, data["kpis"], data["top_products"], data["abc_xyz"],
                data["coverage"], data["recommendations"],
            )
            self.status_label.setText(f"Excel report generated: {output_path}")
            QMessageBox.information(self, "Report generated", f"Excel report saved to:\n{output_path}")
        except Exception as exc:  # noqa: BLE001
            QMessageBox.critical(self, "Report generation failed", str(exc))

    def _open_folder(self) -> None:
        QDesktopServices.openUrl(QUrl.fromLocalFile(str(REPORTS_DIR)))
