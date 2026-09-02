"""Main application window: sidebar navigation + stacked pages."""
from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QButtonGroup,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from app.config import APP_NAME, APP_VERSION, DATABASE_PATH
from app.database.db_manager import DatabaseManager
from app.ui.theme import STYLESHEET
from app.ui.widgets.abc_xyz_view import AbcXyzView
from app.ui.widgets.dashboard_view import DashboardView
from app.ui.widgets.forecast_view import ForecastView
from app.ui.widgets.import_view import ImportView
from app.ui.widgets.recommendations_view import RecommendationsView
from app.ui.widgets.reports_view import ReportsView
from app.ui.widgets.simulator_view import SimulatorView
from app.ui.widgets.stock_view import StockCoverageView

NAV_ITEMS = [
    ("Dashboard", "\N{BAR CHART}"),
    ("Import Data", "\N{INBOX TRAY}"),
    ("Sales Forecast", "\N{CHART WITH UPWARDS TREND}"),
    ("ABC / XYZ Analysis", "\N{INPUT SYMBOL FOR LATIN LETTERS}"),
    ("Stock Coverage", "\N{PACKAGE}"),
    ("Recommendations", "\N{ELECTRIC LIGHT BULB}"),
    ("Simulator", "\N{LEVEL SLIDER}"),
    ("Reports", "\N{PRINTER}"),
]


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = DatabaseManager()

        self.setWindowTitle(APP_NAME)
        self.resize(1440, 900)
        self.setMinimumSize(1100, 700)
        self.setStyleSheet(STYLESHEET)

        central = QWidget()
        central.setObjectName("centralArea")
        root_layout = QHBoxLayout(central)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        sidebar = self._build_sidebar()
        root_layout.addWidget(sidebar)

        self.stack = QStackedWidget()
        root_layout.addWidget(self.stack, 1)
        self.setCentralWidget(central)

        self.dashboard_view = DashboardView(self.db)
        self.import_view = ImportView(self.db)
        self.forecast_view = ForecastView(self.db)
        self.abc_xyz_view = AbcXyzView(self.db)
        self.stock_view = StockCoverageView(self.db)
        self.recommendations_view = RecommendationsView(self.db)
        self.simulator_view = SimulatorView(self.db)
        self.reports_view = ReportsView(self.db)

        self.pages = [
            self.dashboard_view, self.import_view, self.forecast_view, self.abc_xyz_view,
            self.stock_view, self.recommendations_view, self.simulator_view, self.reports_view,
        ]
        for page in self.pages:
            self.stack.addWidget(page)

        self.import_view.data_imported.connect(self.refresh_all)

        self.statusBar().showMessage(
            f"{APP_NAME} v{APP_VERSION}  |  100% local — no data leaves this computer  |  Database: {DATABASE_PATH}"
        )

        self.nav_buttons[0].setChecked(True)
        self.refresh_all()

    def _build_sidebar(self) -> QWidget:
        sidebar = QWidget()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(240)
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        title = QLabel("Supply Chain\nAssistant")
        title.setObjectName("sidebarTitle")
        layout.addWidget(title)
        subtitle = QLabel("EMEA Distribution Analytics")
        subtitle.setObjectName("sidebarSubtitle")
        layout.addWidget(subtitle)

        self.nav_buttons: list[QPushButton] = []
        group = QButtonGroup(sidebar)
        group.setExclusive(True)
        for idx, (label, icon) in enumerate(NAV_ITEMS):
            btn = QPushButton(f"  {icon}   {label}")
            btn.setObjectName("navButton")
            btn.setCheckable(True)
            btn.setCursor(Qt.PointingHandCursor)
            btn.clicked.connect(lambda _checked=False, i=idx: self._navigate(i))
            layout.addWidget(btn)
            group.addButton(btn)
            self.nav_buttons.append(btn)

        layout.addStretch(1)
        version_label = QLabel(f"v{APP_VERSION}")
        version_label.setStyleSheet("color:#5C6B7A; padding:12px; font-size:8pt;")
        layout.addWidget(version_label)
        return sidebar

    def _navigate(self, index: int) -> None:
        self.stack.setCurrentIndex(index)
        page = self.pages[index]
        if hasattr(page, "refresh"):
            page.refresh()

    def refresh_all(self) -> None:
        for page in self.pages:
            if hasattr(page, "refresh"):
                page.refresh()

    def closeEvent(self, event) -> None:  # noqa: N802 - Qt override signature
        self.db.close()
        super().closeEvent(event)
