#!/usr/bin/env python3
"""
Sales Data Analysis Script

This module provides functionality to analyze sales data from a CSV file,
calculating key metrics including total revenue, average order value,
and top-performing products.

Expected CSV format:
    product_name, quantity, unit_price
"""

import csv
import sys
from pathlib import Path
from typing import Dict, List, Tuple
from decimal import Decimal, InvalidOperation


def read_sales_data(filepath: str) -> List[Dict[str, str]]:
    """
    Read sales data from a CSV file.
    
    Args:
        filepath: Path to the CSV file
        
    Returns:
        List of dictionaries containing sales records
        
    Raises:
        FileNotFoundError: If the CSV file doesn't exist
        csv.Error: If the CSV file is malformed
    """
    file_path = Path(filepath)
    
    if not file_path.exists():
        raise FileNotFoundError(f"CSV file not found: {filepath}")
    
    sales_records = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            
            # Validate that required columns exist
            required_columns = {'product_name', 'quantity', 'unit_price'}
            if not required_columns.issubset(set(reader.fieldnames or [])):
                raise ValueError(
                    f"CSV must contain columns: {', '.join(required_columns)}"
                )
            
            for row in reader:
                sales_records.append(row)
                
    except csv.Error as e:
        raise csv.Error(f"Error parsing CSV file: {e}")
    
    return sales_records


def parse_decimal_value(value: str, field_name: str) -> Decimal:
    """
    Safely parse a string value to Decimal.
    
    Args:
        value: String value to parse
        field_name: Name of the field (for error messages)
        
    Returns:
        Decimal value
        
    Raises:
        ValueError: If value cannot be parsed as a decimal
    """
    try:
        # Strip whitespace and handle empty strings
        cleaned_value = value.strip() if value else "0"
        return Decimal(cleaned_value)
    except (InvalidOperation, ValueError):
        raise ValueError(
            f"Invalid {field_name} value: '{value}'. Must be a number."
        )


def calculate_total_revenue(sales_records: List[Dict[str, str]]) -> Decimal:
    """
    Calculate total revenue from all sales records.
    
    Args:
        sales_records: List of sales record dictionaries
        
    Returns:
        Total revenue as Decimal
    """
    total = Decimal('0')
    
    for idx, record in enumerate(sales_records, start=1):
        try:
            quantity = parse_decimal_value(record.get('quantity', '0'), 'quantity')
            unit_price = parse_decimal_value(record.get('unit_price', '0'), 'unit_price')
            
            # Skip records with negative or zero values
            if quantity <= 0 or unit_price < 0:
                print(
                    f"Warning: Skipping row {idx} - invalid quantity or price",
                    file=sys.stderr
                )
                continue
                
            total += quantity * unit_price
            
        except ValueError as e:
            print(f"Warning: Skipping row {idx} - {e}", file=sys.stderr)
            continue
    
    return total


def calculate_average_order_value(sales_records: List[Dict[str, str]]) -> Decimal:
    """
    Calculate average order value (revenue per transaction).
    
    Args:
        sales_records: List of sales record dictionaries
        
    Returns:
        Average order value as Decimal
    """
    total_revenue = Decimal('0')
    valid_orders = 0
    
    for idx, record in enumerate(sales_records, start=1):
        try:
            quantity = parse_decimal_value(record.get('quantity', '0'), 'quantity')
            unit_price = parse_decimal_value(record.get('unit_price', '0'), 'unit_price')
            
            if quantity <= 0 or unit_price < 0:
                continue
                
            total_revenue += quantity * unit_price
            valid_orders += 1
            
        except ValueError:
            continue
    
    # Avoid division by zero
    if valid_orders == 0:
        return Decimal('0')
    
    return total_revenue / valid_orders


def get_top_products(
    sales_records: List[Dict[str, str]], 
    top_n: int = 5
) -> List[Tuple[str, Decimal]]:
    """
    Calculate top N products by total sales revenue.
    
    Args:
        sales_records: List of sales record dictionaries
        top_n: Number of top products to return (default: 5)
        
    Returns:
        List of tuples (product_name, total_sales) sorted by revenue descending
    """
    # Dictionary to accumulate sales by product
    product_sales: Dict[str, Decimal] = {}
    
    for idx, record in enumerate(sales_records, start=1):
        try:
            product_name = record.get('product_name', '').strip()
            
            # Skip records with missing product names
            if not product_name:
                print(
                    f"Warning: Skipping row {idx} - missing product name",
                    file=sys.stderr
                )
                continue
            
            quantity = parse_decimal_value(record.get('quantity', '0'), 'quantity')
            unit_price = parse_decimal_value(record.get('unit_price', '0'), 'unit_price')
            
            if quantity <= 0 or unit_price < 0:
                continue
            
            revenue = quantity * unit_price
            
            # Accumulate sales for each product
            if product_name in product_sales:
                product_sales[product_name] += revenue
            else:
                product_sales[product_name] = revenue
                
        except ValueError:
            continue
    
    # Sort products by revenue (descending) and return top N
    sorted_products = sorted(
        product_sales.items(),
        key=lambda x: x[1],
        reverse=True
    )
    
    return sorted_products[:top_n]


def format_currency(amount: Decimal) -> str:
    """
    Format a Decimal amount as currency string.
    
    Args:
        amount: Decimal amount to format
        
    Returns:
        Formatted currency string
    """
    return f"${amount:,.2f}"


def print_analysis_results(
    total_revenue: Decimal,
    average_order: Decimal,
    top_products: List[Tuple[str, Decimal]]
) -> None:
    """
    Print formatted analysis results to stdout.
    
    Args:
        total_revenue: Total revenue calculated
        average_order: Average order value calculated
        top_products: List of top products with their sales
    """
    print("\n" + "=" * 60)
    print("SALES ANALYSIS REPORT")
    print("=" * 60)
    
    print(f"\nTotal Revenue: {format_currency(total_revenue)}")
    print(f"Average Order Value: {format_currency(average_order)}")
    
    print(f"\nTop {len(top_products)} Products by Revenue:")
    print("-" * 60)
    
    if not top_products:
        print("No valid product data found.")
    else:
        for rank, (product, sales) in enumerate(top_products, start=1):
            print(f"{rank}. {product:<40} {format_currency(sales):>15}")
    
    print("=" * 60 + "\n")


def main() -> None:
    """
    Main execution function.
    
    Reads sales data, performs analysis, and displays results.
    Handles errors gracefully with appropriate error messages.
    """
    csv_filepath = "sales.csv"
    
    try:
        # Read sales data
        print(f"Reading sales data from {csv_filepath}...")
        sales_records = read_sales_data(csv_filepath)
        
        if not sales_records:
            print("Warning: No sales records found in CSV file.", file=sys.stderr)
            return
        
        print(f"Successfully loaded {len(sales_records)} sales records.\n")
        
        # Perform calculations
        total_revenue = calculate_total_revenue(sales_records)
        average_order = calculate_average_order_value(sales_records)
        top_products = get_top_products(sales_records, top_n=5)
        
        # Display results
        print_analysis_results(total_revenue, average_order, top_products)
        
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
        
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
        
    except csv.Error as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
        
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
