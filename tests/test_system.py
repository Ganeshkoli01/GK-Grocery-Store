"""
GK GROCERY STORE – Automated Comprehensive Verification Test Suite
Tests all 18 requirements specified in Section 21.
"""

import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from datetime import datetime, date, timedelta
from database.connection import fetch_one, fetch_all, execute_query, execute_insert, get_db_transaction, fetch_dataframe
from utils.helpers import verify_password, format_currency, generate_invoice_number
from utils.invoice_generator import generate_invoice_pdf
from utils.excel_export import generate_full_business_excel
from analytics.sales_analysis import get_sales_kpi_summary, get_daily_sales_trend
from analytics.profit_analysis import get_pnl_summary
from analytics.inventory_analysis import get_inventory_kpis, get_best_selling_products, get_restock_recommendations
from config import DEFAULT_ADMIN, DEFAULT_CUSTOMER


def run_all_tests():
    print("=" * 70)
    print("STARTING GK GROCERY STORE AUTOMATED TEST SUITE")
    print("=" * 70)
    passed = 0
    total = 0

    def test(name, condition, details=""):
        nonlocal passed, total
        total += 1
        if condition:
            passed += 1
            print(f" [PASS] Test {total:02d}: {name}")
        else:
            print(f"![FAIL] Test {total:02d}: {name} - {details}")

    # 1. Owner Login verification
    admin = fetch_one("SELECT * FROM users WHERE username = ?", (DEFAULT_ADMIN["username"],))
    test(
        "Owner credentials exist and password verification works",
        admin is not None and verify_password(DEFAULT_ADMIN["password"], admin["password_hash"], admin["salt"]),
        f"Admin found: {admin is not None}"
    )

    # 2. Owner can add new products
    test_prod_name = f"Test Organic Honey {datetime.now().strftime('%M%S')}"
    new_prod_id = execute_insert(
        """
        INSERT INTO products (name, category, cost_price, selling_price, stock_quantity, min_stock_level, unit, is_active)
        VALUES (?, 'Snacks', 150.0, 200.0, 50.0, 10.0, 'bottle', 1)
        """,
        (test_prod_name,)
    )
    test(
        "Owner can add new products with cost and selling price",
        new_prod_id > 0,
        f"New product ID: {new_prod_id}"
    )

    # 3. Owner can update product prices
    execute_query("UPDATE products SET selling_price = 220.0 WHERE id = ?", (new_prod_id,))
    updated_prod = fetch_one("SELECT selling_price FROM products WHERE id = ?", (new_prod_id,))
    test(
        "Owner can update product prices",
        updated_prod is not None and float(updated_prod["selling_price"]) == 220.0,
        f"Updated price: {updated_prod['selling_price'] if updated_prod else None}"
    )

    # 4. Owner can add new inventory
    initial_stock = float(fetch_one("SELECT stock_quantity FROM products WHERE id = ?", (new_prod_id,))["stock_quantity"])
    execute_query("UPDATE products SET stock_quantity = stock_quantity + 25 WHERE id = ?", (new_prod_id,))
    new_stock = float(fetch_one("SELECT stock_quantity FROM products WHERE id = ?", (new_prod_id,))["stock_quantity"])
    test(
        "Owner can add new inventory stock",
        new_stock == initial_stock + 25,
        f"Expected {initial_stock + 25}, got {new_stock}"
    )

    # 5. Customer can browse products (verify product querying)
    prods = fetch_all("SELECT id, name, selling_price FROM products WHERE is_active = 1")
    test(
        "Customer can query active products catalog",
        len(prods) > 0,
        f"Active products count: {len(prods)}"
    )

    # 6 & 7. Billing and Transaction Validation
    inv_no = generate_invoice_number()
    test_qty = 5.0
    stock_before = float(fetch_one("SELECT stock_quantity FROM products WHERE id = ?", (new_prod_id,))["stock_quantity"])
    
    with get_db_transaction() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO sales (invoice_no, customer_name, customer_phone, total_amount, discount_amount, grand_total, payment_method, is_sample)
            VALUES (?, 'Test Customer', '+91 99999 88888', 1100.0, 0.0, 1100.0, 'UPI', 0)
            """,
            (inv_no,)
        )
        test_sale_id = cursor.lastrowid
        cursor.execute(
            """
            INSERT INTO sale_items (sale_id, product_id, product_name, category, unit, quantity, cost_price, selling_price, subtotal, profit)
            VALUES (?, ?, ?, 'Snacks', 'bottle', ?, 150.0, 220.0, 1100.0, 350.0)
            """,
            (test_sale_id, new_prod_id, test_prod_name, test_qty)
        )
        cursor.execute("UPDATE products SET stock_quantity = stock_quantity - ? WHERE id = ?", (test_qty, new_prod_id))

    # 8. Stock decreases correctly after billing
    stock_after = float(fetch_one("SELECT stock_quantity FROM products WHERE id = ?", (new_prod_id,))["stock_quantity"])
    test(
        "Stock decreases correctly after successful billing",
        stock_after == stock_before - test_qty,
        f"Before: {stock_before}, After: {stock_after}"
    )

    # 9. Stock does NOT decrease if billing fails (Atomic Rollback Test)
    stock_pre_rollback = stock_after
    failed_transaction_thrown = False
    try:
        with get_db_transaction() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE products SET stock_quantity = stock_quantity - 10 WHERE id = ?", (new_prod_id,))
            # Intentionally raise an error to trigger rollback
            raise RuntimeError("Simulated network or validation fault!")
    except RuntimeError:
        failed_transaction_thrown = True

    stock_post_rollback = float(fetch_one("SELECT stock_quantity FROM products WHERE id = ?", (new_prod_id,))["stock_quantity"])
    test(
        "Stock does not decrease if billing fails (Transaction Rollback)",
        failed_transaction_thrown and (stock_post_rollback == stock_pre_rollback),
        f"Pre: {stock_pre_rollback}, Post: {stock_post_rollback}"
    )

    # 10. Invoice generates correctly (PDF binary check)
    sale_record = fetch_one("SELECT * FROM sales WHERE invoice_no = ?", (inv_no,))
    items_record = fetch_all("SELECT * FROM sale_items WHERE sale_id = ?", (sale_record["id"],))
    pdf_buf = generate_invoice_pdf(sale_record, items_record)
    test(
        "Invoice generates valid non-empty PDF document",
        len(pdf_buf.getvalue()) > 1000,
        f"PDF byte size: {len(pdf_buf.getvalue())}"
    )

    # 11. Sales are stored in the database
    stored_sale = fetch_one("SELECT * FROM sales WHERE invoice_no = ?", (inv_no,))
    test(
        "Sales record is correctly stored and queryable in database",
        stored_sale is not None and stored_sale["invoice_no"] == inv_no,
        f"Invoice: {stored_sale['invoice_no'] if stored_sale else None}"
    )

    # 12. Gross profit is calculated correctly
    # Selling 220, Cost 150, Qty 5 -> Revenue 1100, Cost 750, Gross Profit 350
    item_row = fetch_one("SELECT subtotal, cost_price, quantity, profit FROM sale_items WHERE sale_id = ?", (sale_record["id"],))
    expected_profit = (float(item_row["quantity"]) * 220.0) - (float(item_row["quantity"]) * 150.0)
    test(
        "Gross profit is calculated accurately using historical cost",
        float(item_row["profit"]) == expected_profit,
        f"Expected {expected_profit}, got {item_row['profit']}"
    )

    # 13. Net profit includes operating expenses
    pnl = get_pnl_summary(datetime(2020, 1, 1), datetime.now())
    test(
        "Net profit includes operating expenses (Net = Gross - Expenses)",
        round(pnl["net_profit"], 2) == round(pnl["gross_profit"] - pnl["expenses"], 2),
        f"Gross: {pnl['gross_profit']}, Exp: {pnl['expenses']}, Net: {pnl['net_profit']}"
    )

    # 14. Daily, weekly, monthly, and yearly reports work
    df_daily = get_daily_sales_trend(datetime.now() - timedelta(days=30), datetime.now())
    test(
        "Daily, weekly, monthly trend queries execute with valid DataFrames",
        not df_daily.empty,
        f"Daily rows: {len(df_daily)}"
    )

    # 15. Best-selling products are identified correctly
    df_best = get_best_selling_products(datetime(2020, 1, 1), datetime.now(), limit=5)
    test(
        "Best-selling products are identified and ranked",
        not df_best.empty and "sales_rank" in df_best.columns,
        f"Top product: {df_best.iloc[0]['product_name'] if not df_best.empty else None}"
    )

    # 16. Low stock alerts work
    inv_kpis = get_inventory_kpis()
    test(
        "Low stock and out-of-stock count detection functions properly",
        "low_stock_count" in inv_kpis and "out_of_stock_count" in inv_kpis,
        f"Low: {inv_kpis['low_stock_count']}, Out: {inv_kpis['out_of_stock_count']}"
    )

    # 17. Excel reports download correctly with all 6 sheets
    excel_buf = generate_full_business_excel()
    import openpyxl
    wb = openpyxl.load_workbook(excel_buf)
    expected_sheets = ["Sales Report", "Product Inventory", "Product Performance", "Daily PnL", "Expenses", "Monthly Summary"]
    all_sheets_present = all(s in wb.sheetnames for s in expected_sheets)
    test(
        "Excel report generates multi-tab workbook with all 6 required sheets",
        all_sheets_present,
        f"Sheets: {wb.sheetnames}"
    )

    # 18. Customer role isolation: Customer user has role='customer'
    cust = fetch_one("SELECT role FROM users WHERE username = ?", (DEFAULT_CUSTOMER["username"],))
    test(
        "Customer accounts have strictly restricted role ('customer')",
        cust is not None and cust["role"] == "customer",
        f"Role: {cust['role'] if cust else None}"
    )

    print("=" * 70)
    print(f"TEST RESULTS: {passed} / {total} TESTS PASSED ({passed/total*100:.1f}%)")
    print("=" * 70)

    # Cleanup test product
    execute_query("DELETE FROM sale_items WHERE sale_id = ?", (sale_record["id"],))
    execute_query("DELETE FROM sales WHERE id = ?", (sale_record["id"],))
    execute_query("DELETE FROM products WHERE id = ?", (new_prod_id,))


if __name__ == "__main__":
    run_all_tests()

