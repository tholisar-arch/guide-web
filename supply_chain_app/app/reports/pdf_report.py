"""PDF report export (reportlab), 100% local rendering — no browser/web engine."""
from __future__ import annotations

from datetime import datetime
from pathlib import Path

import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

NAVY = colors.HexColor("#1F3B57")
ACCENT = colors.HexColor("#2E86AB")
LIGHT_GREY = colors.HexColor("#F2F4F7")


def _styles():
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="ReportTitle", fontSize=22, textColor=NAVY, spaceAfter=6, leading=26))
    styles.add(ParagraphStyle(name="SectionTitle", fontSize=14, textColor=NAVY, spaceBefore=14, spaceAfter=8))
    styles.add(ParagraphStyle(name="Body", fontSize=9.5, leading=13))
    return styles


def _df_to_table(df: pd.DataFrame, max_rows: int = 30) -> Table:
    if df.empty:
        data = [["No data available."]]
    else:
        show = df.head(max_rows).copy()
        for col in show.columns:
            if show[col].dtype.kind == "f":
                show[col] = show[col].round(2)
        header = [str(c).replace("_", " ").title() for c in show.columns]
        data = [header] + show.astype(str).values.tolist()

    table = Table(data, repeatRows=1, hAlign="LEFT")
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), NAVY),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTSIZE", (0, 0), (-1, -1), 7.5),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT_GREY]),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#D0D5DD")),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ]
        )
    )
    return table


def build_pdf_report(
    output_path: str | Path,
    kpis: dict,
    top_products: pd.DataFrame,
    abc_xyz_matrix: pd.DataFrame,
    coverage: pd.DataFrame,
    recommendations: pd.DataFrame,
) -> Path:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    styles = _styles()

    doc = SimpleDocTemplate(
        str(output_path), pagesize=A4,
        leftMargin=1.6 * cm, rightMargin=1.6 * cm, topMargin=1.6 * cm, bottomMargin=1.6 * cm,
    )
    story = []

    story.append(Paragraph("Supply Chain &amp; Sales Decision Assistant", styles["ReportTitle"]))
    story.append(Paragraph("EMEA Distribution — Executive Report", styles["Body"]))
    story.append(Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}", styles["Body"]))
    story.append(Spacer(1, 0.6 * cm))

    story.append(Paragraph("Key Performance Indicators", styles["SectionTitle"]))
    kpi_rows = [[k.replace("_", " ").title(), f"{v:,.2f}" if isinstance(v, float) else str(v)]
                for k, v in kpis.items()]
    kpi_table = Table(kpi_rows, colWidths=[8 * cm, 6 * cm], hAlign="LEFT")
    kpi_table.setStyle(
        TableStyle(
            [
                ("FONTSIZE", (0, 0), (-1, -1), 9.5),
                ("ROWBACKGROUNDS", (0, 0), (-1, -1), [colors.white, LIGHT_GREY]),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#D0D5DD")),
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ]
        )
    )
    story.append(kpi_table)

    story.append(Paragraph("Top Products by Revenue", styles["SectionTitle"]))
    story.append(_df_to_table(top_products))

    story.append(PageBreak())
    story.append(Paragraph("ABC / XYZ Matrix (SKU count per class)", styles["SectionTitle"]))
    story.append(_df_to_table(abc_xyz_matrix.reset_index() if not abc_xyz_matrix.empty else abc_xyz_matrix))

    story.append(Paragraph("Stock Coverage — Highest Risk Items", styles["SectionTitle"]))
    risk_cols = ["sku", "name", "quantity_on_hand", "days_of_coverage", "reorder_point", "coverage_status"]
    risk_df = coverage[risk_cols] if not coverage.empty else coverage
    story.append(_df_to_table(risk_df))

    story.append(PageBreak())
    story.append(Paragraph("Automatic Recommendations", styles["SectionTitle"]))
    rec_cols = ["sku", "name", "priority", "category", "recommendation"]
    rec_df = recommendations[rec_cols] if not recommendations.empty else recommendations
    story.append(_df_to_table(rec_df, max_rows=40))

    doc.build(story)
    return output_path
