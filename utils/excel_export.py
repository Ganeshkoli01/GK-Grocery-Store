"""
GK GROCERY STORE – Comprehensive Excel Report Exporter
Generates multi-sheet formatted business reports using OpenPyXL and Pandas.
"""

import io
import pandas as pd
from datetime import datetime
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

from database.connection import fetch_dataframe, fetch_all


def generate_full_business_excel(start_date=None, end_date=None) -> io.BytesIO:
    """
    Builds a beautifully styled multi-tab Excel workbook containing:
    1. Sales Report
    2. Product Inventory
    3. Product Performance
    4. Profit and Loss
    5. Expenses
    6. Monthly Summary
    """
    buffer = io.BytesIO()

    # Query Data
    sales_sql = """
        SELECT 
            s.invoice_no as "Invoice No",
            s.sale_date as "Sale Date",
            s.customer_name as "Customer Name",
            s.customer_phone as "Customer Phone",
            s.payment_method as "Payment Mode",
            s.total_amount as "Subtotal (Rs)",
            s.discount_amount as "Discount (Rs)",
            s.grand_total as "Grand Total (Rs)"
        FROM sales s
        ORDER BY s.sale_date DESC
    """
    df_sales = fetch_dataframe(sales_sql)

    inv_sql = """
        SELECT 
            p.id as "Product ID",
            p.name as "Product Name",
            p.category as "Category",
            p.unit as "Unit",
            p.cost_price as "Cost Price (Rs)",
            p.selling_price as "Selling Price (Rs)",
            ROUND(p.selling_price - p.cost_price, 2) as "Unit Margin (Rs)",
            ROUND(((p.selling_price - p.cost_price) / p.selling_price) * 100, 1) as "Margin (%)",
            p.stock_quantity as "Available Stock",
            p.min_stock_level as "Min Stock Alert",
            ROUND(p.cost_price * p.stock_quantity, 2) as "Total Inventory Cost (Rs)",
            ROUND(p.selling_price * p.stock_quantity, 2) as "Total Retail Value (Rs)",
            CASE 
                WHEN p.stock_quantity <= 0 THEN 'Out of Stock'
                WHEN p.stock_quantity <= p.min_stock_level THEN 'Low Stock'
                ELSE 'Healthy'
            END as "Stock Status"
        FROM products p
        WHERE p.is_active = 1
        ORDER BY p.category, p.name
    """
    df_inventory = fetch_dataframe(inv_sql)

    perf_sql = """
        SELECT 
            si.product_name as "Product Name",
            si.category as "Category",
            ROUND(SUM(si.quantity), 2) as "Total Quantity Sold",
            ROUND(SUM(si.subtotal), 2) as "Total Revenue (Rs)",
            ROUND(SUM(si.cost_price * si.quantity), 2) as "Total COGS (Rs)",
            ROUND(SUM(si.profit), 2) as "Total Profit (Rs)",
            ROUND((SUM(si.profit) / NULLIF(SUM(si.subtotal), 0)) * 100, 1) as "Profit Margin (%)"
        FROM sale_items si
        GROUP BY si.product_id, si.product_name, si.category
        ORDER BY "Total Revenue (Rs)" DESC
    """
    df_perf = fetch_dataframe(perf_sql)

    pnl_sql = """
        SELECT 
            DATE(s.sale_date) as "Date",
            COUNT(DISTINCT s.id) as "Orders",
            ROUND(SUM(si.subtotal), 2) as "Gross Revenue (Rs)",
            ROUND(SUM(si.cost_price * si.quantity), 2) as "COGS (Rs)",
            ROUND(SUM(si.profit), 2) as "Gross Profit (Rs)"
        FROM sales s
        JOIN sale_items si ON s.id = si.sale_id
        GROUP BY DATE(s.sale_date)
        ORDER BY DATE(s.sale_date) DESC
    """
    df_pnl = fetch_dataframe(pnl_sql)

    exp_sql = """
        SELECT 
            e.expense_date as "Date",
            e.category as "Category",
            e.title as "Expense Item",
            e.amount as "Amount (Rs)",
            e.payment_method as "Payment Method",
            e.description as "Remarks"
        FROM expenses e
        ORDER BY e.expense_date DESC
    """
    df_exp = fetch_dataframe(exp_sql)

    monthly_sql = """
        SELECT 
            STRFTIME('%Y-%m', s.sale_date) as "Month",
            COUNT(DISTINCT s.id) as "Total Orders",
            ROUND(SUM(s.grand_total), 2) as "Revenue (Rs)",
            ROUND(SUM(si.cost_price * si.quantity), 2) as "COGS (Rs)",
            ROUND(SUM(si.profit), 2) as "Gross Profit (Rs)"
        FROM sales s
        JOIN sale_items si ON s.id = si.sale_id
        GROUP BY STRFTIME('%Y-%m', s.sale_date)
        ORDER BY "Month" DESC
    """
    df_monthly = fetch_dataframe(monthly_sql)

    # Use OpenPyXL to write and style sheets
    wb = openpyxl.Workbook()
    # Remove default sheet
    wb.remove(wb.active)

    sheets_data = [
        ("Sales Report", df_sales),
        ("Product Inventory", df_inventory),
        ("Product Performance", df_perf),
        ("Daily PnL", df_pnl),
        ("Expenses", df_exp),
        ("Monthly Summary", df_monthly)
    ]

    header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    header_fill = PatternFill(start_color="14532D", end_color="14532D", fill_type="solid")
    alt_row_fill = PatternFill(start_color="F8FAFC", end_color="F8FAFC", fill_type="solid")
    thin_border_side = Side(border_style="thin", color="E2E8F0")
    cell_border = Border(left=thin_border_side, right=thin_border_side, top=thin_border_side, bottom=thin_border_side)

    title_font = Font(name="Calibri", size=14, bold=True, color="14532D")

    for sheet_name, df in sheets_data:
        ws = wb.create_sheet(title=sheet_name)
        ws.views.sheetView[0].showGridLines = True

        # Write Title Banner
        ws.cell(row=1, column=1, value=f"GK GROCERY STORE – {sheet_name.upper()}")
        ws.cell(row=1, column=1).font = title_font
        ws.cell(row=2, column=1, value=f"Exported on: {datetime.now().strftime('%d-%b-%Y %I:%M %p')}")
        ws.cell(row=2, column=1).font = Font(name="Calibri", size=9, italic=True, color="64748B")

        # Start Table on Row 4
        start_row = 4
        headers = list(df.columns)

        # Write Headers
        for col_idx, h in enumerate(headers, 1):
            cell = ws.cell(row=start_row, column=col_idx, value=h)
            cell.font = header_font
            cell.fill = header_fill
            cell.alignment = Alignment(horizontal="center", vertical="center")
            cell.border = cell_border

        # Write Rows
        for row_idx, row_data in enumerate(df.values, start_row + 1):
            fill = alt_row_fill if row_idx % 2 == 0 else None
            for col_idx, val in enumerate(row_data, 1):
                cell = ws.cell(row=row_idx, column=col_idx, value=val)
                if fill:
                    cell.fill = fill
                cell.border = cell_border
                cell.font = Font(name="Calibri", size=10)
                
                # Check for numerical / currency columns
                col_name = headers[col_idx - 1]
                if isinstance(val, (int, float)):
                    if "(Rs)" in col_name or "Price" in col_name or "Subtotal" in col_name or "Total" in col_name or "Revenue" in col_name or "Amount" in col_name or "Profit" in col_name or "COGS" in col_name:
                        cell.number_format = '₹#,##0.00'
                        cell.alignment = Alignment(horizontal="right")
                    elif "(%)" in col_name or "Margin" in col_name:
                        cell.number_format = '0.0"%"'
                        cell.alignment = Alignment(horizontal="right")
                    else:
                        cell.number_format = '#,##0.00'
                        cell.alignment = Alignment(horizontal="right")
                else:
                    cell.alignment = Alignment(horizontal="left")

        # Auto-fit Column Widths
        for col in ws.columns:
            max_len = 0
            col_letter = get_column_letter(col[0].column)
            for cell in col:
                # ignore top title row for width
                if cell.row in [1, 2]:
                    continue
                val_str = str(cell.value or "")
                if len(val_str) > max_len:
                    max_len = len(val_str)
            ws.column_dimensions[col_letter].width = max(max_len + 4, 12)

    wb.save(buffer)
    buffer.seek(0)
    return buffer

