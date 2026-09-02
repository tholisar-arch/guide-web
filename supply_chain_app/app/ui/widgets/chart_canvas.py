"""Matplotlib-in-Qt embedding helper.

Charts are rendered natively via ``matplotlib``'s Qt Agg backend into a
``QWidget`` — no browser/web view is used anywhere in the application.
"""
from __future__ import annotations

import matplotlib

matplotlib.use("QtAgg")

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas  # noqa: E402
from matplotlib.figure import Figure  # noqa: E402

ACCENT = "#2E86AB"
NAVY = "#1F3B57"
PALETTE_SERIES = ["#2E86AB", "#1F3B57", "#E8A33D", "#1B9E77", "#D64545", "#7C5CBF"]


class MplCanvas(FigureCanvas):
    """A blank matplotlib canvas ready to be embedded in a Qt layout."""

    def __init__(self, width: float = 5, height: float = 3.2, dpi: int = 100):
        self.fig = Figure(figsize=(width, height), dpi=dpi, tight_layout=True)
        self.fig.patch.set_facecolor("#FFFFFF")
        self.axes = self.fig.add_subplot(111)
        super().__init__(self.fig)
        self._style_axes(self.axes)

    @staticmethod
    def _style_axes(ax) -> None:
        ax.set_facecolor("#FFFFFF")
        for spine in ("top", "right"):
            ax.spines[spine].set_visible(False)
        ax.grid(axis="y", color="#E1E5EB", linewidth=0.8)
        ax.set_axisbelow(True)
        ax.tick_params(colors="#5C6B7A", labelsize=8)

    def clear(self) -> None:
        self.axes.clear()
        self._style_axes(self.axes)

    def redraw(self) -> None:
        self.fig.tight_layout()
        self.draw()
