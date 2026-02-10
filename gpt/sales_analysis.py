import csv
import logging
from collections import defaultdict
from typing import Dict, List, Tuple


CSV_FILE_PATH = "sales.csv"


def setup_logging() -> None:
    """
    Configure basic logging for the application.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s:%(name)s:%(message)s"
    )


def safe_float(value: str) -> float:
    """
    Safely convert a string to float.
    Returns 0.0 if conversion fails.
    """
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def safe_int(value: str) -> int:
    """
    Safely convert a string to int.
    Returns 0 if conversion fails.
    """
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def read_sales_data(file_path: str) -> List[Dict[str, str]]:
    """
    Read sales data from a CSV file.
    Returns a list of row dictionaries.
    """
    rows = []

    try:
        with open(file_path, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                if not row:
                    continue
                rows.append(row)

    except FileNotFoundError:
        logging.error("CSV file not found: %s", file_path)
    except Exception as exc:
        logging.exception("Unexpected error reading CSV: %s", exc)

    return rows


def calculate_metrics(
    rows: List[Dict[str, str]]
) -> Tuple[float, float, List[Tuple[str, float]]]:
    """
    Calculate total revenue, average order value,
    and top 5 products by total sales.
    """
    total_revenue = 0.0
    order_count = 0
    product_sales: Dict[str, float] = defaultdict(float)

    for row in rows:
        product = row.get("product", "").strip()
        quantity = safe_int(row.get("quantity"))
        price = safe_float(row.get("price"))

        if not product or quantity <= 0 or price <= 0:
            logging.warning("Skipping invalid row: %s", row)
            continue

        revenue = quantity * price
        total_revenue += revenue
        product_sales[product] += revenue
        order_count += 1

    average_order_value = (
        total_revenue / order_count if order_count > 0 else 0.0
    )

    top_products = sorted(
        product_sales.items(),
        key=lambda item: item[1],
        reverse=True
    )[:5]

    return total_revenue, average_order_value, top_products


def main() -> None:
    """
    Application entry point.
    """
    setup_logging()

    rows = read_sales_data(CSV_FILE_PATH)
    if not rows:
        logging.error("No valid sales data found.")
        return

    total_revenue, avg_order_value, top_products = calculate_metrics(rows)

    print(f"Total Revenue: ${total_revenue:,.2f}")
    print(f"Average Order Value: ${avg_order_value:,.2f}")
    print("\nTop 5 Products by Sales:")
    for product, sales in top_products:
        print(f"- {product}: ${sales:,.2f}")


if __name__ == "__main__":
    main()
