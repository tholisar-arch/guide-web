"""Modern, flat Qt stylesheet (QSS) shared by the whole application.

No web technology is involved: this is plain Qt Style Sheets, interpreted
natively by the Qt widget toolkit.
"""

PALETTE = {
    "bg": "#F4F6F9",
    "surface": "#FFFFFF",
    "sidebar": "#132339",
    "sidebar_hover": "#1F3B57",
    "sidebar_active": "#2E86AB",
    "text": "#1B2430",
    "text_muted": "#5C6B7A",
    "border": "#E1E5EB",
    "accent": "#2E86AB",
    "accent_dark": "#1F3B57",
    "success": "#1B9E77",
    "warning": "#E8A33D",
    "danger": "#D64545",
}

STYLESHEET = f"""
* {{
    font-family: "Segoe UI", "Inter", Arial, sans-serif;
    font-size: 10.5pt;
    color: {PALETTE['text']};
}}

QMainWindow, QWidget#centralArea {{
    background-color: {PALETTE['bg']};
}}

/* ---------------- Sidebar ---------------- */
QWidget#sidebar {{
    background-color: {PALETTE['sidebar']};
}}
QLabel#sidebarTitle {{
    color: #FFFFFF;
    font-size: 13pt;
    font-weight: 600;
    padding: 18px 16px 4px 16px;
}}
QLabel#sidebarSubtitle {{
    color: #9FB3C8;
    font-size: 8.5pt;
    padding: 0px 16px 16px 16px;
}}
QPushButton#navButton {{
    background-color: transparent;
    color: #D6E0EA;
    border: none;
    text-align: left;
    padding: 12px 18px;
    font-size: 10.5pt;
    border-left: 3px solid transparent;
    border-radius: 0px;
}}
QPushButton#navButton:hover {{
    background-color: {PALETTE['sidebar_hover']};
}}
QPushButton#navButton:checked {{
    background-color: {PALETTE['sidebar_hover']};
    color: #FFFFFF;
    font-weight: 600;
    border-left: 3px solid {PALETTE['sidebar_active']};
}}

/* ---------------- Cards / surfaces ---------------- */
QFrame#card {{
    background-color: {PALETTE['surface']};
    border: 1px solid {PALETTE['border']};
    border-radius: 10px;
}}
QLabel#kpiValue {{
    font-size: 20pt;
    font-weight: 700;
    color: {PALETTE['accent_dark']};
}}
QLabel#kpiLabel {{
    font-size: 9pt;
    color: {PALETTE['text_muted']};
}}
QLabel#pageTitle {{
    font-size: 16pt;
    font-weight: 700;
    color: {PALETTE['accent_dark']};
}}
QLabel#pageSubtitle {{
    color: {PALETTE['text_muted']};
    font-size: 9.5pt;
}}
QLabel#sectionTitle {{
    font-size: 11.5pt;
    font-weight: 600;
    color: {PALETTE['accent_dark']};
    padding-top: 6px;
}}

/* ---------------- Inputs ---------------- */
QPushButton {{
    background-color: {PALETTE['accent']};
    color: white;
    border: none;
    border-radius: 6px;
    padding: 8px 16px;
    font-weight: 600;
}}
QPushButton:hover {{
    background-color: {PALETTE['accent_dark']};
}}
QPushButton:disabled {{
    background-color: #A9B7C4;
}}
QPushButton#secondaryButton {{
    background-color: {PALETTE['surface']};
    color: {PALETTE['accent_dark']};
    border: 1px solid {PALETTE['border']};
}}
QPushButton#secondaryButton:hover {{
    background-color: {PALETTE['bg']};
}}

QComboBox, QDateEdit, QLineEdit, QSpinBox, QDoubleSpinBox {{
    background-color: {PALETTE['surface']};
    border: 1px solid {PALETTE['border']};
    border-radius: 6px;
    padding: 5px 8px;
    min-height: 22px;
}}

QTableWidget, QTableView {{
    background-color: {PALETTE['surface']};
    alternate-background-color: {PALETTE['bg']};
    gridline-color: {PALETTE['border']};
    border: 1px solid {PALETTE['border']};
    border-radius: 8px;
}}
QHeaderView::section {{
    background-color: {PALETTE['accent_dark']};
    color: white;
    padding: 6px;
    border: none;
    font-weight: 600;
}}

QTabWidget::pane {{
    border: 1px solid {PALETTE['border']};
    border-radius: 8px;
    background: {PALETTE['surface']};
}}
QTabBar::tab {{
    padding: 8px 16px;
    background: transparent;
    color: {PALETTE['text_muted']};
}}
QTabBar::tab:selected {{
    color: {PALETTE['accent_dark']};
    font-weight: 600;
    border-bottom: 2px solid {PALETTE['accent']};
}}

QSlider::groove:horizontal {{
    height: 6px;
    background: {PALETTE['border']};
    border-radius: 3px;
}}
QSlider::handle:horizontal {{
    background: {PALETTE['accent']};
    width: 16px;
    margin: -6px 0;
    border-radius: 8px;
}}
QSlider::sub-page:horizontal {{
    background: {PALETTE['accent']};
    border-radius: 3px;
}}

QProgressBar {{
    border: 1px solid {PALETTE['border']};
    border-radius: 6px;
    text-align: center;
    background: {PALETTE['bg']};
}}
QProgressBar::chunk {{
    background-color: {PALETTE['accent']};
    border-radius: 6px;
}}

QStatusBar {{
    background: {PALETTE['surface']};
    border-top: 1px solid {PALETTE['border']};
}}
"""
