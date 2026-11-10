"""
GK GROCERY STORE – Product Performance & Movement Analytics Module
Identifies top revenue drivers, dead stock/slow-moving items, and restock prioritization.
"""

import streamlit as st
import pandas as pd
from analytics.inventory_analysis import (
    get_best_selling_products,
    get_slow_moving_products,
    get_restock_recommendations
)
from analytics.visualizations import (
    chart_top10_products_bar,
    chart_slow_moving_products,
    chart_product_wise_profit
)
from utils.helpers import get_date_range, format_currency
from utils.translations import t, get_product_display_name, get_category_display_name


def render_product_performance():
    """Renders product movement and velocity analysis."""
    st.markdown(
        f"""
        <div class="brand-header-box">
            <div>
                <div class="brand-title">{t('nav_performance')}</div>
                <div class="brand-subtitle">{t('app_subtitle')}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    c_f1, c_f2 = st.columns([2, 1])
    with c_f1:
        time_option = st.selectbox("Evaluation Window", ["Last 30 Days", "This Month", "Last 7 Days", "This Year", "All Time"])

    start_dt, end_dt = get_date_range(time_option)

    tab_best, tab_slow, tab_restock = st.tabs([
        "🏆 Best-Selling Products",
        "🐢 Slow-Moving & Dead Stock",
        "🔔 Restock Recommendations"
    ])

    # TAB 1: Best-Selling Products
    with tab_best:
        st.markdown("##### 🥇 Top 10 Best-Selling Grocery Products")
        df_top = get_best_selling_products(start_dt, end_dt, limit=10)

        if not df_top.empty:
            c_chart, c_tbl = st.columns([1.1, 0.9])
            with c_chart:
                fig_top = chart_top10_products_bar(df_top)
                st.plotly_chart(fig_top, use_container_width=True)

            with c_tbl:
                df_top_display = df_top.copy()
                df_top_display["product_name"] = df_top_display["product_name"].apply(lambda n: get_product_display_name(n))
                display_top = df_top_display.rename(columns={
                    "sales_rank": "Rank",
                    "product_name": "Product Name",
                    "category": "Category",
                    "total_quantity_sold": "Units Sold",
                    "total_revenue": "Revenue (₹)",
                    "total_profit": "Gross Profit (₹)"
                })
                st.dataframe(
                    display_top[["Rank", "Product Name", "Units Sold", "Revenue (₹)", "Gross Profit (₹)"]],
                    use_container_width=True,
                    column_config={
                        "Revenue (₹)": st.column_config.NumberColumn(format="₹%.2f"),
                        "Gross Profit (₹)": st.column_config.NumberColumn(format="₹%.2f"),
                    },
                    hide_index=True
                )
        else:
            st.info("No sales recorded for this period.")

    # TAB 2: Slow-Moving & Dead Stock
    with tab_slow:
        st.markdown("##### 🐢 Slow-Moving Products (Lowest Velocity)")
        df_slow = get_slow_moving_products(start_dt, end_dt, limit=15)

        if not df_slow.empty:
            c_s1, c_s2 = st.columns([1.1, 0.9])
            with c_s1:
                fig_slow = chart_slow_moving_products(df_slow)
                st.plotly_chart(fig_slow, use_container_width=True)

            with c_s2:
                # Separate zero-sales items
                df_zero = df_slow[df_slow["total_quantity_sold"] == 0]
                if not df_zero.empty:
                    st.warning(f"⚠️ **{len(df_zero)} products** had ZERO sales during this period!")
                
                df_slow_display = df_slow.copy()
                df_slow_display["product_name"] = df_slow_display["product_name"].apply(lambda n: get_product_display_name(n))
                display_slow = df_slow_display.rename(columns={
                    "product_name": "Product Name",
                    "category": "Category",
                    "current_stock": "Current Stock",
                    "total_quantity_sold": "Units Sold",
                    "total_revenue": "Revenue (₹)",
                    "last_sold_date": "Last Sold Date"
                })
                st.dataframe(
                    display_slow[["Product Name", "Category", "Current Stock", "Units Sold", "Last Sold Date"]],
                    use_container_width=True,
                    hide_index=True
                )
        else:
            st.info("No slow-moving data available.")

    # TAB 3: Restock Recommendations
    with tab_restock:
        st.markdown("##### 🔔 Replenishment Action Matrix")
        st.caption("Auto-generated based on current stock, minimum safety levels, and 30-day run-rate.")
        df_rec = get_restock_recommendations()

        if not df_rec.empty:
            df_rec_display = df_rec.copy()
            df_rec_display["product_name"] = df_rec_display["product_name"].apply(lambda n: get_product_display_name(n))
            st.dataframe(
                df_rec_display.rename(columns={
                    "product_name": "Product Name",
                    "category": "Category",
                    "current_stock": "Current Stock",
                    "min_stock_level": "Min Alert Level",
                    "cost_price": "Unit Cost (₹)",
                    "sold_last_30_days": "30-Day Sales",
                    "urgency_status": "Urgency",
                    "suggested_order_qty": "Suggested Order Qty"
                }),
                use_container_width=True,
                column_config={
                    "Unit Cost (₹)": st.column_config.NumberColumn(format="₹%.2f"),
                },
                hide_index=True
            )
        else:
            st.success("✅ All product stocks are in a healthy, safe operating range.")

