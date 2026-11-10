"""
GK GROCERY STORE – Profit and Loss Statement Module
Delivers accurate financial accounting with historical COGS, gross margins,
operating overheads, and net profit calculations.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import date
from analytics.profit_analysis import get_pnl_summary, get_monthly_pnl_breakdown, get_expense_by_category
from analytics.visualizations import chart_monthly_pnl
from utils.helpers import format_currency, get_date_range
from utils.translations import t
from config import THEME_COLORS


def render_profit_loss():
    """Renders comprehensive Profit & Loss accounting report."""
    st.markdown(
        f"""
        <div class="brand-header-box">
            <div>
                <div class="brand-title">{t('nav_pnl')}</div>
                <div class="brand-subtitle">{t('app_subtitle')}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Date Filter
    c_f1, c_f2 = st.columns([2, 1])
    with c_f1:
        timeframe = st.selectbox(
            "Financial Reporting Period",
            ["Last 30 Days", "This Month", "Today", "Yesterday", "Last 7 Days", "This Year", "All Time"]
        )

    start_dt, end_dt = get_date_range(timeframe)
    pnl = get_pnl_summary(start_dt, end_dt)

    # P&L Top KPI Banner
    st.markdown(
        f"""
        <div class="kpi-grid">
            <div class="kpi-card kpi-primary">
                <div class="kpi-title">Gross Sales Revenue</div>
                <div class="kpi-value">{format_currency(pnl['revenue'])}</div>
                <div class="kpi-subtext">Total retail turnover</div>
            </div>
            <div class="kpi-card kpi-accent">
                <div class="kpi-title">Cost of Goods Sold (COGS)</div>
                <div class="kpi-value">{format_currency(pnl['cogs'])}</div>
                <div class="kpi-subtext">Historical wholesale inventory cost</div>
            </div>
            <div class="kpi-card kpi-secondary">
                <div class="kpi-title">Gross Profit</div>
                <div class="kpi-value">{format_currency(pnl['gross_profit'])}</div>
                <div class="kpi-subtext">Gross Margin: {pnl['gross_margin_pct']}%</div>
            </div>
            <div class="kpi-card kpi-danger">
                <div class="kpi-title">Operating Expenses</div>
                <div class="kpi-value">{format_currency(pnl['expenses'])}</div>
                <div class="kpi-subtext">Rent, power, salaries, logistics</div>
            </div>
            <div class="kpi-card {'kpi-secondary' if not pnl['is_loss'] else 'kpi-danger'}">
                <div class="kpi-title">Net Bottom-Line Profit</div>
                <div class="kpi-value">{format_currency(pnl['net_profit'])}</div>
                <div class="kpi-subtext {'sub-danger' if pnl['is_loss'] else ''}">
                    Net Margin: {pnl['net_margin_pct']}% {'(LOSS)' if pnl['is_loss'] else ''}
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Waterfall Chart: Revenue -> COGS -> Gross Profit -> Expenses -> Net Profit
    st.markdown("#### 🌊 Financial Waterfall Flow (Turnover to Net Profit)")
    
    fig_waterfall = go.Figure(go.Waterfall(
        name="P&L Flow",
        orientation="v",
        measure=["relative", "relative", "total", "relative", "total"],
        x=["Revenue", "COGS", "Gross Profit", "Operating Expenses", "Net Profit"],
        textposition="outside",
        text=[
            format_currency(pnl["revenue"]),
            f"-{format_currency(pnl['cogs'])}",
            format_currency(pnl["gross_profit"]),
            f"-{format_currency(pnl['expenses'])}",
            format_currency(pnl["net_profit"])
        ],
        y=[
            pnl["revenue"],
            -pnl["cogs"],
            0,
            -pnl["expenses"],
            0
        ],
        connector={"line": {"color": "#CBD5E1"}},
        decreasing={"marker": {"color": "#EF4444"}},
        increasing={"marker": {"color": "#22C55E"}},
        totals={"marker": {"color": "#14532D"}}
    ))

    fig_waterfall.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        yaxis=dict(showgrid=True, gridcolor="#E2E8F0", title="Amount (₹)"),
        margin=dict(l=40, r=40, t=20, b=40)
    )

    st.plotly_chart(fig_waterfall, use_container_width=True)

    # Monthly Multi-bar Trajectory
    st.markdown("#### 📅 Monthly Financial Performance Comparison")
    df_monthly = get_monthly_pnl_breakdown()
    fig_pnl_chart = chart_monthly_pnl(df_monthly)
    st.plotly_chart(fig_pnl_chart, use_container_width=True)

    # Structured Table
    st.markdown("##### 📑 Monthly Financial Statement Table")
    if not df_monthly.empty:
        display_m = df_monthly.rename(columns={
            "month_label": "Month",
            "revenue": "Revenue (₹)",
            "cogs": "COGS (₹)",
            "gross_profit": "Gross Profit (₹)",
            "expenses": "Expenses (₹)",
            "net_profit": "Net Profit (₹)"
        })
        st.dataframe(
            display_m,
            use_container_width=True,
            column_config={
                "Revenue (₹)": st.column_config.NumberColumn(format="₹%.2f"),
                "COGS (₹)": st.column_config.NumberColumn(format="₹%.2f"),
                "Gross Profit (₹)": st.column_config.NumberColumn(format="₹%.2f"),
                "Expenses (₹)": st.column_config.NumberColumn(format="₹%.2f"),
                "Net Profit (₹)": st.column_config.NumberColumn(format="₹%.2f"),
            },
            hide_index=True
        )

