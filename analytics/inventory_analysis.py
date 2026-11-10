"""
GK GROCERY STORE – Inventory Analysis & Product Performance Engine
Analyzes stock levels, inventory valuation, best-selling vs slow-moving items,
and generates restocking recommendations.
"""

import pandas as pd
from datetime import datetime
from database.connection import fetch_dataframe, fetch_one, fetch_all


def get_inventory_kpis() -> dict:
    """Computes overall stock counts and capital valuation."""
    sql = """
        SELECT 
            COUNT(id) as total_products,
            COALESCE(SUM(cost_price * stock_quantity), 0.0) as total_cost_valuation,
            COALESCE(SUM(selling_price * stock_quantity), 0.0) as total_retail_valuation,
            COALESCE(SUM(stock_quantity), 0.0) as total_units_in_stock
        FROM products
        WHERE is_active = 1
    """
    res = fetch_one(sql)

    low_stock_sql = """
        SELECT COUNT(id) as low_count 
        FROM products 
        WHERE is_active = 1 AND stock_quantity > 0 AND stock_quantity <= min_stock_level
    """
    low_res = fetch_one(low_stock_sql)

    out_stock_sql = """
        SELECT COUNT(id) as out_count 
        FROM products 
        WHERE is_active = 1 AND stock_quantity <= 0
    """
    out_res = fetch_one(out_stock_sql)

    cost_val = float(res["total_cost_valuation"]) if res else 0.0
    retail_val = float(res["total_retail_valuation"]) if res else 0.0
    potential_profit = retail_val - cost_val

    return {
        "total_products": res["total_products"] if res else 0,
        "total_units": float(res["total_units_in_stock"]) if res else 0.0,
        "total_cost_valuation": round(cost_val, 2),
        "total_retail_valuation": round(retail_val, 2),
        "potential_profit": round(potential_profit, 2),
        "low_stock_count": low_res["low_count"] if low_res else 0,
        "out_of_stock_count": out_res["out_count"] if out_res else 0
    }


def get_best_selling_products(start_date: datetime, end_date: datetime, limit: int = 10) -> pd.DataFrame:
    """
    Returns top best-selling products ranked by revenue / quantity.
    Includes: Rank, Product Name, Category, Total Qty Sold, Revenue, Profit.
    """
    start_str = start_date.strftime("%Y-%m-%d 00:00:00")
    end_str = end_date.strftime("%Y-%m-%d 23:59:59")

    sql = """
        SELECT 
            si.product_name,
            si.category,
            si.unit,
            ROUND(SUM(si.quantity), 2) as total_quantity_sold,
            ROUND(SUM(si.subtotal), 2) as total_revenue,
            ROUND(SUM(si.profit), 2) as total_profit
        FROM sales s
        JOIN sale_items si ON s.id = si.sale_id
        WHERE s.sale_date BETWEEN ? AND ?
        GROUP BY si.product_id, si.product_name, si.category, si.unit
        ORDER BY total_revenue DESC
        LIMIT ?
    """
    df = fetch_dataframe(sql, (start_str, end_str, limit))
    if not df.empty:
        df.insert(0, "sales_rank", range(1, len(df) + 1))
    return df


def get_slow_moving_products(start_date: datetime, end_date: datetime, limit: int = 15) -> pd.DataFrame:
    """
    Identifies products with low or zero sales during the selected period.
    """
    start_str = start_date.strftime("%Y-%m-%d 00:00:00")
    end_str = end_date.strftime("%Y-%m-%d 23:59:59")

    sql = """
        SELECT 
            p.id as product_id,
            p.name as product_name,
            p.category,
            p.unit,
            p.stock_quantity as current_stock,
            p.min_stock_level,
            COALESCE(sales_data.qty_sold, 0.0) as total_quantity_sold,
            COALESCE(sales_data.rev, 0.0) as total_revenue,
            sales_data.last_sold_date
        FROM products p
        LEFT JOIN (
            SELECT 
                si.product_id,
                ROUND(SUM(si.quantity), 2) as qty_sold,
                ROUND(SUM(si.subtotal), 2) as rev,
                MAX(s.sale_date) as last_sold_date
            FROM sales s
            JOIN sale_items si ON s.id = si.sale_id
            WHERE s.sale_date BETWEEN ? AND ?
            GROUP BY si.product_id
        ) sales_data ON p.id = sales_data.product_id
        WHERE p.is_active = 1
        ORDER BY total_quantity_sold ASC, p.stock_quantity DESC
        LIMIT ?
    """
    return fetch_dataframe(sql, (start_str, end_str, limit))


def get_restock_recommendations() -> pd.DataFrame:
    """
    Generates intelligent restocking recommendations based on:
    - Current stock <= min_stock_level OR stock == 0
    - Recent sales velocity
    """
    sql = """
        SELECT 
            p.id as product_id,
            p.name as product_name,
            p.category,
            p.unit,
            p.stock_quantity as current_stock,
            p.min_stock_level,
            p.cost_price,
            COALESCE(recent_sales.sold_last_30_days, 0) as sold_last_30_days,
            CASE 
                WHEN p.stock_quantity <= 0 THEN 'CRITICAL: Out of Stock'
                WHEN p.stock_quantity <= (p.min_stock_level * 0.5) THEN 'HIGH: Immediate Reorder'
                WHEN p.stock_quantity <= p.min_stock_level THEN 'MEDIUM: Restock Soon'
                ELSE 'HEALTHY: Sufficient Stock'
            END as urgency_status,
            CASE 
                WHEN p.stock_quantity <= p.min_stock_level THEN 
                    ROUND(MAX(p.min_stock_level * 2 - p.stock_quantity, 10), 0)
                ELSE 0
            END as suggested_order_qty
        FROM products p
        LEFT JOIN (
            SELECT 
                si.product_id,
                ROUND(SUM(si.quantity), 1) as sold_last_30_days
            FROM sales s
            JOIN sale_items si ON s.id = si.sale_id
            WHERE s.sale_date >= DATE('now', '-30 days')
            GROUP BY si.product_id
        ) recent_sales ON p.id = recent_sales.product_id
        WHERE p.is_active = 1 AND p.stock_quantity <= p.min_stock_level
        ORDER BY p.stock_quantity ASC, sold_last_30_days DESC
    """
    return fetch_dataframe(sql)

