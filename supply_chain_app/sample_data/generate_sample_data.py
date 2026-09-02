"""One-off script that generated the sample_products/sales/stock CSVs in this folder.

Not part of the application itself; kept for reproducibility / regenerating
the demo dataset. Run with: python generate_sample_data.py
"""
from __future__ import annotations

import csv
import random
from datetime import date

random.seed(42)

PRODUCTS = [
    # sku, name, category, supplier, unit_cost, unit_price, lead_time_days, base_monthly_demand, trend_per_month, noise, seasonal
    ("FUSE-001", "Fast-Acting Fuse 10A", "Circuit Protection", "Mersen SA", 1.20, 3.50, 10, 900, 4, 0.10, False),
    ("FUSE-002", "Semiconductor Fuse 32A", "Circuit Protection", "Mersen SA", 4.80, 12.90, 21, 260, 1, 0.20, False),
    ("BUSB-010", "Copper Busbar 100A", "Power Distribution", "CopperTech Ltd", 18.50, 42.00, 30, 60, -0.5, 0.35, False),
    ("SURG-005", "Surge Protective Device Type 2", "Surge Protection", "Mersen SA", 22.00, 58.00, 25, 140, 2.5, 0.25, False),
    ("SURG-006", "Surge Protective Device Type 1+2", "Surge Protection", "Mersen SA", 55.00, 129.00, 35, 45, 0.8, 0.30, False),
    ("HOLD-020", "Fuse Holder Panel Mount", "Accessories", "ElecParts GmbH", 2.10, 6.20, 14, 500, 0, 0.12, True),
    ("SWITCH-030", "Disconnect Switch 63A", "Switching", "SwitchCo", 15.00, 39.00, 18, 180, 1.2, 0.20, False),
    ("SWITCH-031", "Disconnect Switch 125A", "Switching", "SwitchCo", 28.00, 72.00, 18, 90, -1.0, 0.30, False),
    ("CABLE-040", "Cable Lug 25mm2", "Accessories", "ElecParts GmbH", 0.45, 1.35, 7, 2200, 5, 0.08, True),
    ("RELAY-050", "Monitoring Relay 3-Phase", "Protection Relays", "Mersen SA", 32.00, 84.00, 28, 55, 0.3, 0.45, False),
    ("FUSE-003", "Slow-Blow Fuse 6A", "Circuit Protection", "Mersen SA", 0.90, 2.60, 10, 700, -3, 0.15, False),
    ("OBSOLETE-099", "Legacy Terminal Block (EOL)", "Accessories", "ElecParts GmbH", 3.00, 7.50, 14, 0, 0, 0, False),
]

random.seed(7)


def month_range(start_year: int, start_month: int, n: int):
    y, m = start_year, start_month
    for _ in range(n):
        yield y, m
        m += 1
        if m > 12:
            m = 1
            y += 1


def main() -> None:
    n_months = 18
    months = list(month_range(2025, 3, n_months))

    with open("sample_products.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Item Code", "Description", "Category", "Supplier", "Unit Cost", "Unit Price", "Lead Time (days)"])
        for sku, name, category, supplier, cost, price, lead_time, *_ in PRODUCTS:
            writer.writerow([sku, name, category, supplier, cost, price, lead_time])

    sales_rows = []
    for sku, name, category, supplier, cost, price, lead_time, base_demand, trend, noise, seasonal in PRODUCTS:
        for i, (y, m) in enumerate(months):
            demand = base_demand + trend * i
            if seasonal:
                demand *= 1 + 0.25 * (1 if m in (11, 12, 1) else (-0.15 if m in (6, 7, 8) else 0))
            demand *= 1 + random.gauss(0, noise)
            demand = max(0, round(demand))
            if demand == 0:
                continue
            day = random.randint(1, 27)
            sale_date = date(y, m, day)
            revenue = round(demand * price * random.uniform(0.97, 1.03), 2)
            sales_rows.append([sku, sale_date.isoformat(), demand, revenue])

    with open("sample_sales.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["SKU", "Sale Date", "Quantity", "Revenue"])
        writer.writerows(sales_rows)

    snapshot_date = date(months[-1][0], months[-1][1], 28).isoformat()
    stock_rows = []
    for sku, name, category, supplier, cost, price, lead_time, base_demand, trend, noise, seasonal in PRODUCTS:
        if sku == "OBSOLETE-099":
            qty = 340  # obsolete stock with no recent demand -> triggers a recommendation
        elif sku == "FUSE-001":
            qty = round(base_demand * lead_time / 30.44 * 0.4)  # intentionally low -> stockout risk
        elif sku == "BUSB-010":
            qty = round(base_demand * 6)  # intentionally high -> excess stock
        else:
            qty = round(max(0, base_demand + trend * n_months) * random.uniform(0.8, 1.6))
        stock_rows.append([sku, snapshot_date, qty, "Main DC"])

    with open("sample_stock.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["SKU", "Snapshot Date", "Quantity On Hand", "Warehouse"])
        writer.writerows(stock_rows)

    print(f"Generated {len(PRODUCTS)} products, {len(sales_rows)} sales rows, {len(stock_rows)} stock rows.")


if __name__ == "__main__":
    main()
