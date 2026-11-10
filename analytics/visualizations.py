"""
GK GROCERY STORE – Plotly Visualizations Engine
Generates all 12 interactive commercial-grade charts specified in the requirements.
"""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from config import THEME_COLORS, CURRENCY

# Standard Layout Configuration for Plotly Figures
CHART_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="sans-serif", color=THEME_COLORS["text_dark"]),
    margin=dict(l=40, r=30, t=50, b=40),
    hoverlabel=dict(bgcolor="white", font_size=12, font_family="sans-serif"),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)


def chart_daily_sales_line(df: pd.DataFrame) -> go.Figure:
    """1. Daily Sales Line Chart"""
    fig = go.Figure()
    if df.empty:
        fig.add_annotation(text="No sales data for selected period", showarrow=False, font=dict(size=14))
        fig.update_layout(**CHART_LAYOUT, title="Daily Sales Trend")
        return fig

    fig.add_trace(go.Scatter(
        x=df["sale_date"],
        y=df["revenue"],
        mode="lines+markers",
        name="Revenue (₹)",
        line=dict(color=THEME_COLORS["primary"], width=3),
        marker=dict(size=6, color=THEME_COLORS["secondary"]),
        hovertemplate="<b>Date:</b> %{x|%d %b %Y}<br><b>Revenue:</b> ₹%{y:,.2f}<extra></extra>"
    ))

    fig.add_trace(go.Scatter(
        x=df["sale_date"],
        y=df["gross_profit"],
        mode="lines",
        name="Gross Profit (₹)",
        line=dict(color=THEME_COLORS["accent"], width=2, dash="dot"),
        hovertemplate="<b>Date:</b> %{x|%d %b %Y}<br><b>Profit:</b> ₹%{y:,.2f}<extra></extra>"
    ))

    fig.update_layout(
        **CHART_LAYOUT,
        title="<b>Daily Sales & Profit Trend</b>",
        xaxis=dict(showgrid=True, gridcolor="#E2E8F0", title="Date"),
        yaxis=dict(showgrid=True, gridcolor="#E2E8F0", title="Amount (₹)")
    )
    return fig


def chart_weekly_sales_bar(df: pd.DataFrame) -> go.Figure:
    """2. Weekly Sales Bar Chart"""
    fig = go.Figure()
    if df.empty:
        fig.add_annotation(text="No weekly sales data available", showarrow=False)
        fig.update_layout(**CHART_LAYOUT, title="Weekly Sales Trend")
        return fig

    fig.add_trace(go.Bar(
        x=df["week_label"],
        y=df["revenue"],
        name="Weekly Revenue",
        marker_color=THEME_COLORS["secondary"],
        hovertemplate="<b>Week:</b> %{x}<br><b>Revenue:</b> ₹%{y:,.2f}<extra></extra>"
    ))

    fig.update_layout(
        **CHART_LAYOUT,
        title="<b>Weekly Revenue Breakdown</b>",
        xaxis=dict(showgrid=False, title="Week"),
        yaxis=dict(showgrid=True, gridcolor="#E2E8F0", title="Revenue (₹)")
    )
    return fig


def chart_monthly_revenue_line(df: pd.DataFrame) -> go.Figure:
    """3. Monthly Revenue Line Chart"""
    fig = go.Figure()
    if df.empty:
        fig.add_annotation(text="No monthly revenue data available", showarrow=False)
        fig.update_layout(**CHART_LAYOUT, title="Monthly Revenue Trend")
        return fig

    fig.add_trace(go.Scatter(
        x=df["month_label"],
        y=df["revenue"],
        mode="lines+markers",
        name="Monthly Revenue",
        line=dict(color=THEME_COLORS["primary"], width=3),
        marker=dict(size=8, color=THEME_COLORS["accent"]),
        fill="tozeroy",
        fillcolor="rgba(34, 197, 94, 0.12)",
        hovertemplate="<b>Month:</b> %{x}<br><b>Revenue:</b> ₹%{y:,.2f}<extra></extra>"
    ))

    fig.update_layout(
        **CHART_LAYOUT,
        title="<b>Monthly Revenue Trajectory</b>",
        xaxis=dict(showgrid=True, gridcolor="#E2E8F0", title="Month"),
        yaxis=dict(showgrid=True, gridcolor="#E2E8F0", title="Revenue (₹)")
    )
    return fig


def chart_yearly_revenue_bar(df: pd.DataFrame) -> go.Figure:
    """4. Yearly Revenue Bar Chart"""
    fig = go.Figure()
    if df.empty:
        fig.add_annotation(text="No yearly data available", showarrow=False)
        fig.update_layout(**CHART_LAYOUT, title="Yearly Revenue Trend")
        return fig

    fig.add_trace(go.Bar(
        x=df["year_label"],
        y=df["revenue"],
        name="Annual Revenue",
        marker_color=THEME_COLORS["primary"],
        hovertemplate="<b>Year:</b> %{x}<br><b>Revenue:</b> ₹%{y:,.2f}<extra></extra>"
    ))

    fig.update_layout(
        **CHART_LAYOUT,
        title="<b>Annual Sales Performance</b>",
        xaxis=dict(title="Year"),
        yaxis=dict(showgrid=True, gridcolor="#E2E8F0", title="Revenue (₹)")
    )
    return fig


def chart_revenue_vs_profit(df: pd.DataFrame) -> go.Figure:
    """5. Revenue vs. Profit Chart"""
    fig = go.Figure()
    if df.empty:
        fig.add_annotation(text="No data for Revenue vs Profit", showarrow=False)
        fig.update_layout(**CHART_LAYOUT, title="Revenue vs. Profit")
        return fig

    fig.add_trace(go.Bar(
        x=df["month_label"] if "month_label" in df.columns else df["sale_date"],
        y=df["revenue"],
        name="Revenue",
        marker_color="#14532D",
        hovertemplate="<b>Revenue:</b> ₹%{y:,.2f}<extra></extra>"
    ))

    fig.add_trace(go.Bar(
        x=df["month_label"] if "month_label" in df.columns else df["sale_date"],
        y=df["gross_profit"],
        name="Gross Profit",
        marker_color="#22C55E",
        hovertemplate="<b>Gross Profit:</b> ₹%{y:,.2f}<extra></extra>"
    ))

    fig.update_layout(
        **CHART_LAYOUT,
        barmode="group",
        title="<b>Revenue vs. Gross Profit Comparison</b>",
        xaxis=dict(title="Timeline"),
        yaxis=dict(showgrid=True, gridcolor="#E2E8F0", title="Amount (₹)")
    )
    return fig


def chart_category_sales_pie(df: pd.DataFrame) -> go.Figure:
    """6. Category-wise Sales Pie / Donut Chart"""
    if df.empty:
        fig = go.Figure()
        fig.add_annotation(text="No category sales found", showarrow=False)
        fig.update_layout(**CHART_LAYOUT, title="Category Sales Distribution")
        return fig

    fig = px.pie(
        df,
        names="category",
        values="revenue",
        hole=0.45,
        title="<b>Sales Distribution by Category</b>",
        color_discrete_sequence=px.colors.sequential.Greens_r
    )
    fig.update_traces(
        textposition="inside",
        textinfo="percent+label",
        hovertemplate="<b>%{label}</b><br>Revenue: ₹%{value:,.2f}<br>Share: %{percent}<extra></extra>"
    )
    fig.update_layout(**CHART_LAYOUT)
    return fig


def chart_top10_products_bar(df: pd.DataFrame) -> go.Figure:
    """7. Top 10 Selling Products Horizontal Bar Chart"""
    if df.empty:
        fig = go.Figure()
        fig.add_annotation(text="No product sales recorded yet", showarrow=False)
        fig.update_layout(**CHART_LAYOUT, title="Top 10 Selling Products")
        return fig

    # Sort ascending for horizontal bar (top product appears at top)
    df_sorted = df.sort_values(by="total_revenue", ascending=True)

    fig = go.Figure(go.Bar(
        x=df_sorted["total_revenue"],
        y=df_sorted["product_name"],
        orientation="h",
        marker=dict(
            color=df_sorted["total_revenue"],
            colorscale=[[0, "#86EFAC"], [1, "#14532D"]]
        ),
        hovertemplate="<b>%{y}</b><br>Revenue: ₹%{x:,.2f}<extra></extra>"
    ))

    fig.update_layout(
        **CHART_LAYOUT,
        title="<b>Top 10 Revenue-Generating Products</b>",
        xaxis=dict(showgrid=True, gridcolor="#E2E8F0", title="Total Revenue (₹)"),
        yaxis=dict(title="")
    )
    return fig


def chart_slow_moving_products(df: pd.DataFrame) -> go.Figure:
    """8. Slow-Moving Products Chart"""
    if df.empty:
        fig = go.Figure()
        fig.add_annotation(text="No slow-moving products data", showarrow=False)
        fig.update_layout(**CHART_LAYOUT, title="Slow-Moving Items")
        return fig

    df_top_slow = df.head(10).sort_values(by="total_quantity_sold", ascending=True)

    fig = go.Figure(go.Bar(
        x=df_top_slow["product_name"],
        y=df_top_slow["total_quantity_sold"],
        marker_color=THEME_COLORS["accent"],
        hovertemplate="<b>%{x}</b><br>Units Sold: %{y}<extra></extra>"
    ))

    fig.update_layout(
        **CHART_LAYOUT,
        title="<b>Slow-Moving Products (Lowest Units Sold)</b>",
        xaxis=dict(tickangle=-35),
        yaxis=dict(showgrid=True, gridcolor="#E2E8F0", title="Units Sold")
    )
    return fig


def chart_product_wise_profit(df: pd.DataFrame) -> go.Figure:
    """9. Product-wise Profit Chart"""
    if df.empty:
        fig = go.Figure()
        fig.add_annotation(text="No profit data available", showarrow=False)
        fig.update_layout(**CHART_LAYOUT, title="Product-wise Profit")
        return fig

    df_top = df.head(10).sort_values(by="total_profit", ascending=True)

    fig = go.Figure(go.Bar(
        x=df_top["total_profit"],
        y=df_top["product_name"],
        orientation="h",
        marker=dict(color="#22C55E"),
        hovertemplate="<b>%{y}</b><br>Net Margin / Profit: ₹%{x:,.2f}<extra></extra>"
    ))

    fig.update_layout(
        **CHART_LAYOUT,
        title="<b>Top 10 Most Profitable Products</b>",
        xaxis=dict(showgrid=True, gridcolor="#E2E8F0", title="Gross Profit (₹)"),
        yaxis=dict(title="")
    )
    return fig


def chart_inventory_stock(df: pd.DataFrame) -> go.Figure:
    """10. Inventory Stock Chart (Stock Quantity vs Min Stock Level)"""
    fig = go.Figure()
    if df.empty:
        fig.add_annotation(text="No inventory records found", showarrow=False)
        fig.update_layout(**CHART_LAYOUT, title="Inventory Stock Overview")
        return fig

    sample_df = df.head(15)

    fig.add_trace(go.Bar(
        x=sample_df["name"],
        y=sample_df["stock_quantity"],
        name="Available Stock",
        marker_color=THEME_COLORS["primary"],
        hovertemplate="<b>%{x}</b><br>Stock: %{y}<extra></extra>"
    ))

    fig.add_trace(go.Scatter(
        x=sample_df["name"],
        y=sample_df["min_stock_level"],
        mode="lines+markers",
        name="Min Threshold Alert",
        line=dict(color=THEME_COLORS["danger"], width=2, dash="dash"),
        marker=dict(size=7, color=THEME_COLORS["danger"]),
        hovertemplate="<b>Min Threshold:</b> %{y}<extra></extra>"
    ))

    fig.update_layout(
        **CHART_LAYOUT,
        title="<b>Inventory Stock Level vs. Minimum Threshold</b>",
        xaxis=dict(tickangle=-35),
        yaxis=dict(showgrid=True, gridcolor="#E2E8F0", title="Quantity")
    )
    return fig


def chart_monthly_pnl(df: pd.DataFrame) -> go.Figure:
    """11. Monthly Profit and Loss Chart (Revenue, COGS, Expenses, Net Profit)"""
    fig = go.Figure()
    if df.empty:
        fig.add_annotation(text="No monthly P&L data available", showarrow=False)
        fig.update_layout(**CHART_LAYOUT, title="Monthly Profit & Loss")
        return fig

    fig.add_trace(go.Bar(
        x=df["month_label"],
        y=df["revenue"],
        name="Revenue",
        marker_color="#14532D"
    ))

    fig.add_trace(go.Bar(
        x=df["month_label"],
        y=df["cogs"],
        name="COGS",
        marker_color="#F59E0B"
    ))

    fig.add_trace(go.Bar(
        x=df["month_label"],
        y=df["expenses"],
        name="Operating Expenses",
        marker_color="#EF4444"
    ))

    fig.add_trace(go.Scatter(
        x=df["month_label"],
        y=df["net_profit"],
        name="Net Profit",
        mode="lines+markers",
        line=dict(color="#0284C7", width=3),
        marker=dict(size=8, color="#0284C7")
    ))

    fig.update_layout(
        **CHART_LAYOUT,
        barmode="group",
        title="<b>Monthly P&L: Revenue, COGS, Expenses & Net Profit</b>",
        xaxis=dict(title="Month"),
        yaxis=dict(showgrid=True, gridcolor="#E2E8F0", title="Amount (₹)")
    )
    return fig


def chart_cost_vs_selling_price(df: pd.DataFrame) -> go.Figure:
    """12. Cost Price vs. Selling Price Comparison Chart"""
    fig = go.Figure()
    if df.empty:
        fig.add_annotation(text="No products available", showarrow=False)
        fig.update_layout(**CHART_LAYOUT, title="Cost vs Selling Price")
        return fig

    sample = df.head(15)

    fig.add_trace(go.Bar(
        x=sample["name"],
        y=sample["cost_price"],
        name="Cost Price (Wholesale)",
        marker_color="#94A3B8",
        hovertemplate="<b>%{x}</b><br>Cost: ₹%{y:,.2f}<extra></extra>"
    ))

    fig.add_trace(go.Bar(
        x=sample["name"],
        y=sample["selling_price"],
        name="Selling Price (Retail)",
        marker_color="#22C55E",
        hovertemplate="<b>%{x}</b><br>Selling: ₹%{y:,.2f}<extra></extra>"
    ))

    fig.update_layout(
        **CHART_LAYOUT,
        barmode="group",
        title="<b>Product Pricing Spread: Cost Price vs. Selling Price</b>",
        xaxis=dict(tickangle=-35),
        yaxis=dict(showgrid=True, gridcolor="#E2E8F0", title="Price per Unit (₹)")
    )
    return fig

