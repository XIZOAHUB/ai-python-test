# Sales Data Analyzer

A production-quality Python script for analyzing sales data from CSV files.

## Features

- **Robust error handling**: Gracefully handles missing values, invalid data, and file errors
- **Decimal precision**: Uses Python's `Decimal` type for accurate financial calculations
- **Clean architecture**: Well-structured functions following single responsibility principle
- **PEP8 compliant**: Follows Python style guidelines
- **Type hints**: Full type annotations for better code clarity
- **Comprehensive logging**: Warnings for skipped/invalid records

## Requirements

- Python 3.7+
- Standard library only (no external dependencies)

## Usage

### Basic Usage

```bash
python sales_analyzer.py
```

The script expects a file named `sales.csv` in the same directory.

### CSV Format

The CSV file must contain the following columns:

```csv
product_name,quantity,unit_price
Laptop,5,999.99
Wireless Mouse,15,29.99
```

**Column descriptions:**
- `product_name`: Name of the product (string)
- `quantity`: Number of units sold (numeric)
- `unit_price`: Price per unit (numeric, can include decimals)

## Calculations

The script performs three main analyses:

1. **Total Revenue**: Sum of all sales (quantity × unit_price)
2. **Average Order Value**: Mean revenue per transaction
3. **Top 5 Products**: Products ranked by total sales revenue

## Error Handling

The script handles various edge cases:

- Missing or malformed CSV files
- Missing column headers
- Empty/null values
- Invalid numeric values
- Negative quantities or prices
- Missing product names

Invalid records are skipped with warnings printed to stderr.

## Example Output

```
Reading sales data from sales.csv...
Successfully loaded 19 sales records.

Warning: Skipping row 14 - missing product name
Warning: Skipping row 15 - Invalid quantity value: 'invalid'. Must be a number.

============================================================
SALES ANALYSIS REPORT
============================================================

Total Revenue: $36,447.23
Average Order Value: $2,279.20

Top 5 Products by Revenue:

1. Laptop                                      $9,999.90
2. Monitor                                     $4,199.88
3. Headphones                                  $1,799.80
4. Keyboard                                    $1,519.81
5. Webcam                                        $779.94
============================================================
```

## Code Structure

```
sales_analyzer.py
├── read_sales_data()          # CSV file reading and validation
├── parse_decimal_value()      # Safe numeric parsing
├── calculate_total_revenue()  # Revenue calculation
├── calculate_average_order_value()  # Average order calculation
├── get_top_products()         # Top N products analysis
├── format_currency()          # Currency formatting
├── print_analysis_results()   # Results display
└── main()                     # Main execution flow
```

## Testing

To test with sample data, use the included `sales.csv` file or create your own following the format above.

## License

This code is provided as-is for educational and commercial use.
