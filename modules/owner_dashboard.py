"""
GK GROCERY STORE – Executive Owner Dashboard
Delivers real-time executive KPIs, dynamic date filtering, and interactive Plotly visuals.
"""

import streamlit as st
from datetime import datetime, date
from utils.helpers import get_date_range, format_currency
from analytics.sales_analysis import (
    get_sales_kpi_summary,
    get_daily_sales_trend,
    get_monthly_sales_trend,
    get_category_sales
)
from analytics.profit_analysis import (
    get_pnl_summary,
    get_monthly_pnl_breakdown,
    get_product_profit_breakdown
)
from analytics.inventory_analysis import (
    get_inventory_kpis,
    get_best_selling_products
)
from analytics.visualizations import (
    chart_daily_sales_line,
    chart_monthly_revenue_line,
    chart_revenue_vs_profit,
    chart_top10_products_bar,
    chart_category_sales_pie,
    chart_product_wise_profit,
    chart_inventory_stock
)
from database.connection import fetch_dataframe
from utils.translations import t, get_product_display_name


def render_owner_dashboard():
    """Renders the executive owner dashboard."""
    # Top Header Banner
    st.markdown(
        f"""
        <div class="brand-header-box">
            <div>
                <div class="brand-title">{t('nav_dashboard')}</div>
                <div class="brand-subtitle">{t('app_subtitle')}</div>
            </div>
            <div style="text-align: right;">
                <span class="badge badge-success">STORE ACTIVE</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Date Filter Controls Bar
    c_filter1, c_filter2, c_filter3 = st.columns([2, 1.5, 1.5])

    time_labels = {
        "Last 30 Days": t("time_last_30_days"),
        "Today": t("time_today"),
        "Yesterday": t("time_yesterday"),
        "Last 7 Days": t("time_last_7_days"),
        "This Month": t("time_this_month"),
        "This Year": t("time_this_year"),
        "All Time": t("time_all_time"),
        "Custom Date Range": t("time_custom")
    }

    with c_filter1:
        date_option = st.selectbox(
            "📅 " + t("nav_dashboard"),
            list(time_labels.keys()),
            format_func=lambda k: time_labels[k],
            index=0
        )

    custom_start = None
    custom_end = None
    if date_option == "Custom Date Range":
        with c_filter2:
            custom_start = st.date_input("Start Date", value=date.today())
        with c_filter3:
            custom_end = st.date_input("End Date", value=date.today())

    start_dt, end_dt = get_date_range(date_option, custom_start, custom_end)

    st.caption(f"Showing performance from **{start_dt.strftime('%d %b %Y')}** to **{end_dt.strftime('%d %b %Y')}**")

    # Fetch Calculated KPI Data
    sales_kpis = get_sales_kpi_summary(start_dt, end_dt)
    pnl_kpis = get_pnl_summary(start_dt, end_dt)
    inv_kpis = get_inventory_kpis()

    # 6 Primary KPI Summary Cards
    st.markdown(
        f"""
        <div class="kpi-grid">
            <div class="kpi-card kpi-primary">
                <div class="kpi-title">{t('kpi_total_revenue')}</div>
                <div class="kpi-value">{format_currency(pnl_kpis['revenue'])}</div>
                <div class="kpi-subtext">Avg Order: {format_currency(sales_kpis['avg_order_value'])}</div>
            </div>
            <div class="kpi-card kpi-secondary">
                <div class="kpi-title">{t('kpi_gross_profit')}</div>
                <div class="kpi-value">{format_currency(pnl_kpis['gross_profit'])}</div>
                <div class="kpi-subtext">Gross Margin: {pnl_kpis['gross_margin_pct']}%</div>
            </div>
            <div class="kpi-card {'kpi-secondary' if not pnl_kpis['is_loss'] else 'kpi-danger'}">
                <div class="kpi-title">{t('kpi_net_profit')}</div>
                <div class="kpi-value">{format_currency(pnl_kpis['net_profit'])}</div>
                <div class="kpi-subtext {'sub-danger' if pnl_kpis['is_loss'] else ''}">
                    Expenses: {format_currency(pnl_kpis['expenses'])}
                </div>
            </div>
            <div class="kpi-card kpi-info">
                <div class="kpi-title">{t('kpi_total_orders')}</div>
                <div class="kpi-value">{sales_kpis['total_orders']:,}</div>
                <div class="kpi-subtext">{sales_kpis['total_items_sold']:g} units sold</div>
            </div>
            <div class="kpi-card kpi-accent">
                <div class="kpi-title">{t('kpi_total_products')}</div>
                <div class="kpi-value">{inv_kpis['total_products']}</div>
                <div class="kpi-subtext">Stock Val: {format_currency(inv_kpis['total_cost_valuation'])}</div>
            </div>
            <div class="kpi-card kpi-danger">
                <div class="kpi-title">{t('kpi_low_stock')}</div>
                <div class="kpi-value">{inv_kpis['low_stock_count'] + inv_kpis['out_of_stock_count']}</div>
                <div class="kpi-subtext sub-danger">{inv_kpis['out_of_stock_count']} out of stock</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<hr style='margin: 15px 0; border: none; border-top: 1px solid #E2E8F0;'>", unsafe_allow_html=True)

    # Charts Row 1: Daily Sales Trend & Monthly Revenue Trajectory
    r1_col1, r1_col2 = st.columns(2)

    with r1_col1:
        df_daily = get_daily_sales_trend(start_dt, end_dt)
        fig_daily = chart_daily_sales_line(df_daily)
        st.plotly_chart(fig_daily, use_container_width=True)

    with r1_col2:
        df_monthly = get_monthly_sales_trend()
        fig_monthly = chart_monthly_revenue_line(df_monthly)
        st.plotly_chart(fig_monthly, use_container_width=True)

    # Charts Row 2: Revenue vs Profit & Category-wise Distribution
    r2_col1, r2_col2 = st.columns([1.1, 0.9])

    with r2_col1:
        df_monthly_pnl = get_monthly_pnl_breakdown()
        fig_rev_vs_prof = chart_revenue_vs_profit(df_monthly_pnl)
        st.plotly_chart(fig_rev_vs_prof, use_container_width=True)

    with r2_col2:
        df_cat = get_category_sales(start_dt, end_dt)
        fig_cat = chart_category_sales_pie(df_cat)
        st.plotly_chart(fig_cat, use_container_width=True)

    # Charts Row 3: Top 10 Best Selling Products & Top Profitable Products
    r3_col1, r3_col2 = st.columns(2)

    with r3_col1:
        df_top10 = get_best_selling_products(start_dt, end_dt, limit=10)
        fig_top10 = chart_top10_products_bar(df_top10)
        st.plotly_chart(fig_top10, use_container_width=True)

    with r3_col2:
        df_profit_prods = get_product_profit_breakdown(start_dt, end_dt, limit=10)
        fig_profit_prods = chart_product_wise_profit(df_profit_prods)
        st.plotly_chart(fig_profit_prods, use_container_width=True)

    # Charts Row 4: Inventory Overview
    st.markdown("#### 📦 Inventory Stock Overview")
    df_inv = fetch_dataframe("SELECT name, stock_quantity, min_stock_level FROM products WHERE is_active = 1 ORDER BY stock_quantity ASC LIMIT 15")
    fig_inv = chart_inventory_stock(df_inv)
    st.plotly_chart(fig_inv, use_container_width=True)

