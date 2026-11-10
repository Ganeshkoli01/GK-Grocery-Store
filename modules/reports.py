"""
GK GROCERY STORE – Business Analytics, Excel Exports & Power BI Integration
Provides multi-period business intelligence reports, multi-sheet Excel generation,
Power BI CSV dataset bundle exports, and sample data controls.
"""

import io
import zipfile
import streamlit as st
import pandas as pd
from datetime import date, datetime
from database.connection import fetch_dataframe, fetch_one
from database.db_setup import seed_sample_data, remove_sample_data
from analytics.sales_analysis import (
    get_daily_sales_trend,
    get_weekly_sales_trend,
    get_monthly_sales_trend,
    get_yearly_sales_trend
)
from analytics.visualizations import (
    chart_daily_sales_line,
    chart_weekly_sales_bar,
    chart_monthly_revenue_line,
    chart_yearly_revenue_bar
)
from utils.excel_export import generate_full_business_excel
from utils.helpers import format_currency
from utils.translations import t


def render_reports():
    """Renders comprehensive business analytics and export hub."""
    st.markdown(
        f"""
        <div class="brand-header-box">
            <div>
                <div class="brand-title">{t('nav_reports')}</div>
                <div class="brand-subtitle">{t('app_subtitle')}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    tab_analytics, tab_excel, tab_powerbi, tab_sample = st.tabs([
        "📊 Multi-Period Analytics",
        "📗 Comprehensive Excel Export",
        "⚡ Power BI Dataset Bundle",
        "⚙️ Sample Data Management"
    ])

    # TAB 1: Multi-Period Analytics (Daily, Weekly, Monthly, Yearly)
    with tab_analytics:
        p_choice = st.radio(
            "Select Reporting Horizon",
            ["Daily Analysis", "Weekly Analysis", "Monthly Analysis", "Yearly Analysis"],
            horizontal=True
        )

        if p_choice == "Daily Analysis":
            st.markdown("##### 📅 Daily Performance Breakdown")
            df_d = get_daily_sales_trend(datetime(2020, 1, 1), datetime.now())
            fig_d = chart_daily_sales_line(df_d)
            st.plotly_chart(fig_d, use_container_width=True)
            if not df_d.empty:
                st.dataframe(
                    df_d.rename(columns={"sale_date": "Date", "order_count": "Orders", "revenue": "Revenue (₹)", "gross_profit": "Gross Profit (₹)"}),
                    use_container_width=True,
                    column_config={"Revenue (₹)": st.column_config.NumberColumn(format="₹%.2f"), "Gross Profit (₹)": st.column_config.NumberColumn(format="₹%.2f")},
                    hide_index=True
                )

        elif p_choice == "Weekly Analysis":
            st.markdown("##### 📆 Weekly Performance Breakdown")
            df_w = get_weekly_sales_trend()
            fig_w = chart_weekly_sales_bar(df_w)
            st.plotly_chart(fig_w, use_container_width=True)
            if not df_w.empty:
                st.dataframe(
                    df_w.rename(columns={"week_label": "Week", "order_count": "Orders", "revenue": "Revenue (₹)", "gross_profit": "Gross Profit (₹)"}),
                    use_container_width=True,
                    column_config={"Revenue (₹)": st.column_config.NumberColumn(format="₹%.2f"), "Gross Profit (₹)": st.column_config.NumberColumn(format="₹%.2f")},
                    hide_index=True
                )

        elif p_choice == "Monthly Analysis":
            st.markdown("##### 🗓️ Monthly Performance Breakdown")
            df_m = get_monthly_sales_trend()
            fig_m = chart_monthly_revenue_line(df_m)
            st.plotly_chart(fig_m, use_container_width=True)
            if not df_m.empty:
                st.dataframe(
                    df_m.rename(columns={"month_label": "Month", "order_count": "Orders", "revenue": "Revenue (₹)", "cogs": "COGS (₹)", "gross_profit": "Gross Profit (₹)"}),
                    use_container_width=True,
                    column_config={"Revenue (₹)": st.column_config.NumberColumn(format="₹%.2f"), "COGS (₹)": st.column_config.NumberColumn(format="₹%.2f"), "Gross Profit (₹)": st.column_config.NumberColumn(format="₹%.2f")},
                    hide_index=True
                )

        elif p_choice == "Yearly Analysis":
            st.markdown("##### 📈 Annual Performance Breakdown")
            df_y = get_yearly_sales_trend()
            fig_y = chart_yearly_revenue_bar(df_y)
            st.plotly_chart(fig_y, use_container_width=True)
            if not df_y.empty:
                st.dataframe(
                    df_y.rename(columns={"year_label": "Year", "order_count": "Orders", "revenue": "Revenue (₹)", "gross_profit": "Gross Profit (₹)"}),
                    use_container_width=True,
                    column_config={"Revenue (₹)": st.column_config.NumberColumn(format="₹%.2f"), "Gross Profit (₹)": st.column_config.NumberColumn(format="₹%.2f")},
                    hide_index=True
                )

    # TAB 2: Multi-Sheet Excel Workbook Export
    with tab_excel:
        st.markdown("##### 📗 Export Complete Multi-Sheet Business Excel Workbook")
        st.markdown(
            """
            This generates a structured multi-tab `.xlsx` workbook containing:
            - **Sheet 1:** Detailed Sales Transactions
            - **Sheet 2:** Product Inventory & Stock Valuation
            - **Sheet 3:** Product Performance & Velocity
            - **Sheet 4:** Daily Profit and Loss Breakdown
            - **Sheet 5:** Operating Expenses Log
            - **Sheet 6:** Monthly Summary Financials
            """
        )

        if st.button("📊 Build & Prepare Excel Workbook", type="primary", use_container_width=True):
            with st.spinner("Compiling database tables and formatting spreadsheet..."):
                excel_buffer = generate_full_business_excel()
                st.success("✅ Workbook compiled successfully!")
                st.download_button(
                    label="📥 Download GK_Grocery_Store_Master_Report.xlsx",
                    data=excel_buffer,
                    file_name=f"GK_Grocery_Store_Master_Report_{date.today().isoformat()}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )

    # TAB 3: Power BI Dataset Export
    with tab_powerbi:
        st.markdown("##### ⚡ Power BI Star-Schema Dataset Bundle")
        st.markdown(
            """
            Export pre-structured Star-Schema CSV files ready for instant loading into Microsoft Power BI Desktop.
            Includes `fact_sales`, `fact_sale_items`, `fact_expenses`, `dim_products`, `dim_customers`, and `dim_calendar`.
            """
        )

        col_p1, col_p2 = st.columns([1.5, 1])
        with col_p1:
            if st.button("📦 Generate Power BI CSV Zip Bundle", type="primary", use_container_width=True):
                with st.spinner("Generating Star Schema CSVs..."):
                    zip_buffer = io.BytesIO()
                    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
                        # 1. Fact Sales
                        df_s = fetch_dataframe("SELECT * FROM sales")
                        zf.writestr("fact_sales.csv", df_s.to_csv(index=False))

                        # 2. Fact Sale Items
                        df_si = fetch_dataframe("SELECT * FROM sale_items")
                        zf.writestr("fact_sale_items.csv", df_si.to_csv(index=False))

                        # 3. Fact Expenses
                        df_e = fetch_dataframe("SELECT * FROM expenses")
                        zf.writestr("fact_expenses.csv", df_e.to_csv(index=False))

                        # 4. Dim Products
                        df_p = fetch_dataframe("SELECT * FROM products")
                        zf.writestr("dim_products.csv", df_p.to_csv(index=False))

                        # 5. Dim Customers
                        df_c = fetch_dataframe("SELECT * FROM customers")
                        zf.writestr("dim_customers.csv", df_c.to_csv(index=False))

                        # 6. Dim Calendar
                        calendar_dates = pd.date_range(start="2024-01-01", end="2026-12-31", freq="D")
                        df_cal = pd.DataFrame({
                            "Date": calendar_dates,
                            "Year": calendar_dates.year,
                            "Month": calendar_dates.month,
                            "MonthName": calendar_dates.strftime("%B"),
                            "Quarter": calendar_dates.quarter,
                            "DayOfWeek": calendar_dates.day_name()
                        })
                        zf.writestr("dim_calendar.csv", df_cal.to_csv(index=False))

                    zip_buffer.seek(0)
                    st.download_button(
                        label="📥 Download Power_BI_Datasets.zip",
                        data=zip_buffer,
                        file_name=f"GK_Grocery_PowerBI_Bundle_{date.today().isoformat()}.zip",
                        mime="application/zip",
                        use_container_width=True
                    )

        with col_p2:
            st.info("📖 View the complete step-by-step Power BI guide in the sidebar or under `powerbi/powerbi_guide.md`.")

    # TAB 4: Sample Data Management
    with tab_sample:
        st.markdown("##### ⚙️ Sample Data Configuration")
        st.markdown(
            """
            This application allows you to load realistic demonstration data (~40 Indian grocery items,
            60 days of sales transactions, and overhead expenses). All sample records are tagged with `is_sample = 1`.
            """
        )

        # Check current sample counts
        sample_sales_cnt = fetch_one("SELECT COUNT(*) as c FROM sales WHERE is_sample = 1")["c"]
        sample_exp_cnt = fetch_one("SELECT COUNT(*) as c FROM expenses WHERE is_sample = 1")["c"]
        actual_sales_cnt = fetch_one("SELECT COUNT(*) as c FROM sales WHERE is_sample = 0")["c"]

        st.write(f"- Sample Sales Transactions: **{sample_sales_cnt}**")
        st.write(f"- Sample Expense Records: **{sample_exp_cnt}**")
        st.write(f"- Genuine Store Customer Sales: **{actual_sales_cnt}**")

        c_s1, c_s2 = st.columns(2)
        with c_s1:
            if st.button("🗑️ Remove All Sample Data", use_container_width=True):
                remove_sample_data()
                st.success("All sample transactions and expenses have been safely removed! Genuine records remain intact.")
                st.rerun()

        with c_s2:
            if st.button("🔄 Re-Seed Sample Demonstration Data", use_container_width=True):
                seed_sample_data()
                st.success("Sample products, transactions, and expenses successfully loaded!")
                st.rerun()

