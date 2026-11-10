"""
GK GROCERY STORE – Sales Analysis Engine
Aggregates sales metrics, trends, order values, and category performance.
"""

import pandas as pd
import numpy as np
from datetime import datetime
from database.connection import fetch_dataframe, fetch_one


def get_sales_kpi_summary(start_date: datetime, end_date: datetime) -> dict:
    """
    Computes key performance indicators for sales within the date range.
    """
    start_str = start_date.strftime("%Y-%m-%d 00:00:00")
    end_str = end_date.strftime("%Y-%m-%d 23:59:59")

    sql = """
        SELECT 
            COUNT(DISTINCT s.id) as total_orders,
            COALESCE(SUM(s.total_amount), 0.0) as subtotal_revenue,
            COALESCE(SUM(s.discount_amount), 0.0) as total_discounts,
            COALESCE(SUM(s.grand_total), 0.0) as total_revenue,
            COALESCE(AVG(s.grand_total), 0.0) as avg_order_value
        FROM sales s
        WHERE s.sale_date BETWEEN ? AND ?
    """
    res = fetch_one(sql, (start_str, end_str))
    
    # Calculate total items sold
    items_sql = """
        SELECT COALESCE(SUM(si.quantity), 0.0) as total_items_sold
        FROM sales s
        JOIN sale_items si ON s.id = si.sale_id
        WHERE s.sale_date BETWEEN ? AND ?
    """
    items_res = fetch_one(items_sql, (start_str, end_str))
    
    total_orders = res["total_orders"] if res else 0
    total_revenue = float(res["total_revenue"]) if res else 0.0
    avg_order_value = float(res["avg_order_value"]) if res else 0.0
    total_discounts = float(res["total_discounts"]) if res else 0.0
    total_items = float(items_res["total_items_sold"]) if items_res else 0.0

    return {
        "total_orders": total_orders,
        "total_revenue": total_revenue,
        "avg_order_value": avg_order_value,
        "total_discounts": total_discounts,
        "total_items_sold": total_items
    }


def get_daily_sales_trend(start_date: datetime, end_date: datetime) -> pd.DataFrame:
    """Returns daily revenue, order counts, and gross profit."""
    start_str = start_date.strftime("%Y-%m-%d 00:00:00")
    end_str = end_date.strftime("%Y-%m-%d 23:59:59")

    sql = """
        SELECT 
            DATE(s.sale_date) as sale_date,
            COUNT(DISTINCT s.id) as order_count,
            ROUND(SUM(s.grand_total), 2) as revenue,
            ROUND(SUM(si.profit), 2) as gross_profit
        FROM sales s
        LEFT JOIN sale_items si ON s.id = si.sale_id
        WHERE s.sale_date BETWEEN ? AND ?
        GROUP BY DATE(s.sale_date)
        ORDER BY DATE(s.sale_date) ASC
    """
    df = fetch_dataframe(sql, (start_str, end_str))
    if not df.empty:
        df["sale_date"] = pd.to_datetime(df["sale_date"])
    return df


def get_weekly_sales_trend() -> pd.DataFrame:
    """Returns weekly revenue and orders for recent weeks."""
    sql = """
        SELECT 
            STRFTIME('%Y-W%W', s.sale_date) as week_label,
            COUNT(DISTINCT s.id) as order_count,
            ROUND(SUM(s.grand_total), 2) as revenue,
            ROUND(SUM(si.profit), 2) as gross_profit
        FROM sales s
        LEFT JOIN sale_items si ON s.id = si.sale_id
        GROUP BY STRFTIME('%Y-W%W', s.sale_date)
        ORDER BY week_label ASC
    """
    return fetch_dataframe(sql)


def get_monthly_sales_trend() -> pd.DataFrame:
    """Returns monthly revenue, orders, and profit trend."""
    sql = """
        SELECT 
            STRFTIME('%Y-%m', s.sale_date) as month_label,
            COUNT(DISTINCT s.id) as order_count,
            ROUND(SUM(s.grand_total), 2) as revenue,
            ROUND(SUM(si.cost_price * si.quantity), 2) as cogs,
            ROUND(SUM(si.profit), 2) as gross_profit
        FROM sales s
        LEFT JOIN sale_items si ON s.id = si.sale_id
        GROUP BY STRFTIME('%Y-%m', s.sale_date)
        ORDER BY month_label ASC
    """
    return fetch_dataframe(sql)


def get_yearly_sales_trend() -> pd.DataFrame:
    """Returns annual sales performance."""
    sql = """
        SELECT 
            STRFTIME('%Y', s.sale_date) as year_label,
            COUNT(DISTINCT s.id) as order_count,
            ROUND(SUM(s.grand_total), 2) as revenue,
            ROUND(SUM(si.profit), 2) as gross_profit
        FROM sales s
        LEFT JOIN sale_items si ON s.id = si.sale_id
        GROUP BY STRFTIME('%Y', s.sale_date)
        ORDER BY year_label ASC
    """
    return fetch_dataframe(sql)


def get_category_sales(start_date: datetime, end_date: datetime) -> pd.DataFrame:
    """Returns category-wise revenue, quantity, and profit."""
    start_str = start_date.strftime("%Y-%m-%d 00:00:00")
    end_str = end_date.strftime("%Y-%m-%d 23:59:59")

    sql = """
        SELECT 
            COALESCE(si.category, 'Other') as category,
            ROUND(SUM(si.quantity), 2) as quantity_sold,
            ROUND(SUM(si.subtotal), 2) as revenue,
            ROUND(SUM(si.profit), 2) as profit
        FROM sales s
        JOIN sale_items si ON s.id = si.sale_id
        WHERE s.sale_date BETWEEN ? AND ?
        GROUP BY si.category
        ORDER BY revenue DESC
    """
    return fetch_dataframe(sql, (start_str, end_str))


def get_payment_method_distribution(start_date: datetime, end_date: datetime) -> pd.DataFrame:
    """Returns sales breakdown by payment method."""
    start_str = start_date.strftime("%Y-%m-%d 00:00:00")
    end_str = end_date.strftime("%Y-%m-%d 23:59:59")

    sql = """
        SELECT 
            s.payment_method,
            COUNT(s.id) as transaction_count,
            ROUND(SUM(s.grand_total), 2) as total_amount
        FROM sales s
        WHERE s.sale_date BETWEEN ? AND ?
        GROUP BY s.payment_method
        ORDER BY total_amount DESC
    """
    return fetch_dataframe(sql, (start_str, end_str))

