"""
GK GROCERY STORE – Profit & Loss Analysis Engine
Computes Revenue, Historical COGS, Gross Profit, Operating Expenses, and Net Profit.
"""

import pandas as pd
from datetime import datetime
from database.connection import fetch_dataframe, fetch_one


def get_pnl_summary(start_date: datetime, end_date: datetime) -> dict:
    """
    Computes complete Profit & Loss metrics for the specified date window:
    Revenue, COGS, Gross Profit, Gross Margin %, Expenses, Net Profit, Net Margin %.
    """
    start_str = start_date.strftime("%Y-%m-%d 00:00:00")
    end_str = end_date.strftime("%Y-%m-%d 23:59:59")
    start_date_only = start_date.strftime("%Y-%m-%d")
    end_date_only = end_date.strftime("%Y-%m-%d")

    # 1. Revenue & COGS from sale_items (Historical Cost!)
    sales_sql = """
        SELECT 
            COALESCE(SUM(si.subtotal), 0.0) as revenue,
            COALESCE(SUM(si.cost_price * si.quantity), 0.0) as cogs,
            COALESCE(SUM(si.profit), 0.0) as gross_profit
        FROM sales s
        JOIN sale_items si ON s.id = si.sale_id
        WHERE s.sale_date BETWEEN ? AND ?
    """
    sales_res = fetch_one(sales_sql, (start_str, end_str))

    revenue = float(sales_res["revenue"]) if sales_res else 0.0
    cogs = float(sales_res["cogs"]) if sales_res else 0.0
    gross_profit = float(sales_res["gross_profit"]) if sales_res else (revenue - cogs)

    # 2. Operating Expenses within same date range
    exp_sql = """
        SELECT COALESCE(SUM(amount), 0.0) as total_expenses
        FROM expenses
        WHERE expense_date BETWEEN ? AND ?
    """
    exp_res = fetch_one(exp_sql, (start_date_only, end_date_only))
    expenses = float(exp_res["total_expenses"]) if exp_res else 0.0

    # 3. Net Profit calculations
    net_profit = gross_profit - expenses
    gross_margin_pct = (gross_profit / revenue * 100.0) if revenue > 0 else 0.0
    net_margin_pct = (net_profit / revenue * 100.0) if revenue > 0 else 0.0

    return {
        "revenue": round(revenue, 2),
        "cogs": round(cogs, 2),
        "gross_profit": round(gross_profit, 2),
        "gross_margin_pct": round(gross_margin_pct, 1),
        "expenses": round(expenses, 2),
        "net_profit": round(net_profit, 2),
        "net_margin_pct": round(net_margin_pct, 1),
        "is_loss": net_profit < 0
    }


def get_monthly_pnl_breakdown() -> pd.DataFrame:
    """Returns monthly Revenue, COGS, Gross Profit, Operating Expenses, and Net Profit."""
    # Monthly sales & COGS
    sales_sql = """
        SELECT 
            STRFTIME('%Y-%m', s.sale_date) as month_label,
            ROUND(SUM(si.subtotal), 2) as revenue,
            ROUND(SUM(si.cost_price * si.quantity), 2) as cogs,
            ROUND(SUM(si.profit), 2) as gross_profit
        FROM sales s
        JOIN sale_items si ON s.id = si.sale_id
        GROUP BY STRFTIME('%Y-%m', s.sale_date)
    """
    df_sales = fetch_dataframe(sales_sql)

    # Monthly expenses
    exp_sql = """
        SELECT 
            STRFTIME('%Y-%m', expense_date) as month_label,
            ROUND(SUM(amount), 2) as expenses
        FROM expenses
        GROUP BY STRFTIME('%Y-%m', expense_date)
    """
    df_exp = fetch_dataframe(exp_sql)

    if df_sales.empty:
        return pd.DataFrame(columns=["month_label", "revenue", "cogs", "gross_profit", "expenses", "net_profit"])

    # Merge sales and expenses
    df = pd.merge(df_sales, df_exp, on="month_label", how="left")
    df["expenses"] = df["expenses"].fillna(0.0)
    df["net_profit"] = df["gross_profit"] - df["expenses"]
    df = df.sort_values(by="month_label", ascending=True)
    return df


def get_expense_by_category(start_date: datetime, end_date: datetime) -> pd.DataFrame:
    """Returns expense totals grouped by category."""
    start_str = start_date.strftime("%Y-%m-%d")
    end_str = end_date.strftime("%Y-%m-%d")

    sql = """
        SELECT 
            category,
            ROUND(SUM(amount), 2) as total_amount,
            COUNT(id) as expense_count
        FROM expenses
        WHERE expense_date BETWEEN ? AND ?
        GROUP BY category
        ORDER BY total_amount DESC
    """
    return fetch_dataframe(sql, (start_str, end_str))


def get_product_profit_breakdown(start_date: datetime, end_date: datetime, limit: int = 15) -> pd.DataFrame:
    """Returns top profit-contributing products."""
    start_str = start_date.strftime("%Y-%m-%d 00:00:00")
    end_str = end_date.strftime("%Y-%m-%d 23:59:59")

    sql = """
        SELECT 
            si.product_name,
            si.category,
            ROUND(SUM(si.quantity), 2) as total_qty,
            ROUND(SUM(si.subtotal), 2) as revenue,
            ROUND(SUM(si.profit), 2) as total_profit,
            ROUND((SUM(si.profit) / NULLIF(SUM(si.subtotal), 0)) * 100, 1) as margin_pct
        FROM sales s
        JOIN sale_items si ON s.id = si.sale_id
        WHERE s.sale_date BETWEEN ? AND ?
        GROUP BY si.product_id, si.product_name, si.category
        ORDER BY total_profit DESC
        LIMIT ?
    """
    return fetch_dataframe(sql, (start_str, end_str, limit))

