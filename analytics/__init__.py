"""Analytics package for GK Grocery Store."""
from .sales_analysis import (
    get_sales_kpi_summary,
    get_daily_sales_trend,
    get_weekly_sales_trend,
    get_monthly_sales_trend,
    get_yearly_sales_trend,
    get_category_sales,
    get_payment_method_distribution
)
from .profit_analysis import (
    get_pnl_summary,
    get_monthly_pnl_breakdown,
    get_expense_by_category,
    get_product_profit_breakdown
)
from .inventory_analysis import (
    get_inventory_kpis,
    get_best_selling_products,
    get_slow_moving_products,
    get_restock_recommendations
)
from .visualizations import (
    chart_daily_sales_line,
    chart_weekly_sales_bar,
    chart_monthly_revenue_line,
    chart_yearly_revenue_bar,
    chart_revenue_vs_profit,
    chart_category_sales_pie,
    chart_top10_products_bar,
    chart_slow_moving_products,
    chart_product_wise_profit,
    chart_inventory_stock,
    chart_monthly_pnl,
    chart_cost_vs_selling_price
)

