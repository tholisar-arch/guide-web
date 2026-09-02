#!/usr/bin/env python3
"""Entry point for the Supply Chain & Sales Decision Assistant desktop app.

Run with:  python main.py
Package with PyInstaller using build.spec (see README.md).
"""
from __future__ import annotations

import sys
from pathlib import Path

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

from app.config import APP_ICON, APP_NAME, APP_ORG
from app.ui.main_window import MainWindow


def main() -> int:
    QApplication.setApplicationName(APP_NAME)
    QApplication.setOrganizationName(APP_ORG)
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    if Path(APP_ICON).exists():
        app.setWindowIcon(QIcon(APP_ICON))

    window = MainWindow()
    window.show()

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
