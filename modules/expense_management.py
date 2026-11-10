"""
GK GROCERY STORE – Operating Expense Management Module
Tracks operational store overheads like rent, utilities, salaries, and transport.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date
from database.connection import fetch_dataframe, fetch_all, fetch_one, execute_query, execute_insert
from config import EXPENSE_CATEGORIES, PAYMENT_METHODS
from utils.helpers import format_currency, get_date_range
from utils.translations import t


def render_expense_management():
    """Renders expense logging and overhead tracking console."""
    st.markdown(
        f"""
        <div class="brand-header-box">
            <div>
                <div class="brand-title">{t('nav_expenses')}</div>
                <div class="brand-subtitle">{t('app_subtitle')}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    tab_list, tab_add, tab_breakdown = st.tabs(["📋 Expense History", "➕ Log New Expense", "📊 Category Breakdown"])

    # TAB 1: Expense List & Filters
    with tab_list:
        c1, c2 = st.columns([2, 1.5])
        with c1:
            time_filter = st.selectbox("Filter Period", ["This Month", "Last 30 Days", "Today", "Last 7 Days", "This Year", "All Time"])
        with c2:
            cat_filter = st.selectbox("Expense Category", ["All Categories"] + EXPENSE_CATEGORIES)

        st_dt, end_dt = get_date_range(time_filter)
        where = ["expense_date BETWEEN ? AND ?"]
        params = [st_dt.strftime("%Y-%m-%d"), end_dt.strftime("%Y-%m-%d")]

        if cat_filter != "All Categories":
            where.append("category = ?")
            params.append(cat_filter)

        where_sql = "WHERE " + " AND ".join(where)

        sql = f"""
            SELECT 
                id,
                expense_date as "Date",
                category as "Category",
                title as "Description",
                amount as "Amount (₹)",
                payment_method as "Payment Mode",
                description as "Remarks"
            FROM expenses
            {where_sql}
            ORDER BY expense_date DESC
        """
        df_exp = fetch_dataframe(sql, tuple(params))

        total_exp = df_exp["Amount (₹)"].sum() if not df_exp.empty else 0.0

        st.metric("Total Filtered Operating Overhead", format_currency(total_exp))

        if not df_exp.empty:
            st.dataframe(
                df_exp.drop(columns=["id"]),
                use_container_width=True,
                column_config={
                    "Amount (₹)": st.column_config.NumberColumn(format="₹%.2f")
                },
                hide_index=True
            )
        else:
            st.info("No expenses found for the selected timeframe.")

    # TAB 2: Log New Expense
    with tab_add:
        st.markdown("##### ➕ Record Store Expense")
        with st.form("add_expense_form", clear_on_submit=True):
            col_e1, col_e2 = st.columns(2)
            with col_e1:
                e_cat = st.selectbox("Expense Category *", EXPENSE_CATEGORIES)
                e_title = st.text_input("Expense Title / Purpose *", placeholder="e.g. October Commercial Electricity Bill")
                e_amount = st.number_input("Amount (₹) *", min_value=1.0, value=2500.0, step=100.0)

            with col_e2:
                e_date = st.date_input("Expense Date *", value=date.today())
                e_mode = st.selectbox("Payment Method", PAYMENT_METHODS, index=1)
                e_desc = st.text_area("Remarks / Vendor Notes", placeholder="e.g. Paid online to MSEDCL via UPI")

            submit_exp = st.form_submit_button("Record Expense", use_container_width=True, type="primary")

            if submit_exp:
                if not e_title.strip():
                    st.error("Please provide an expense title.")
                else:
                    try:
                        execute_insert(
                            """
                            INSERT INTO expenses (category, title, amount, expense_date, description, payment_method, is_sample)
                            VALUES (?, ?, ?, ?, ?, ?, 0)
                            """,
                            (e_cat, e_title.strip(), round(e_amount, 2), e_date.isoformat(), e_desc.strip(), e_mode)
                        )
                        st.success(f"Expense '{e_title}' of {format_currency(e_amount)} recorded successfully!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error saving expense: {str(e)}")

    # TAB 3: Category Breakdown
    with tab_breakdown:
        st.markdown("##### 📊 Operating Expenses by Category")
        df_all_exp = fetch_dataframe(
            """
            SELECT category, ROUND(SUM(amount), 2) as total_amount, COUNT(id) as count
            FROM expenses
            GROUP BY category
            ORDER BY total_amount DESC
            """
        )

        if not df_all_exp.empty:
            c_b1, c_b2 = st.columns([1.2, 0.8])
            with c_b1:
                fig_exp = px.pie(
                    df_all_exp,
                    names="category",
                    values="total_amount",
                    hole=0.4,
                    title="<b>Overhead Distribution by Category</b>",
                    color_discrete_sequence=px.colors.sequential.Tealgrn_r
                )
                fig_exp.update_traces(textposition="inside", textinfo="percent+label")
                fig_exp.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
                st.plotly_chart(fig_exp, use_container_width=True)

            with c_b2:
                st.dataframe(
                    df_all_exp.rename(columns={"category": "Category", "total_amount": "Total Amount (₹)", "count": "Tx Count"}),
                    use_container_width=True,
                    column_config={"Total Amount (₹)": st.column_config.NumberColumn(format="₹%.2f")},
                    hide_index=True
                )
        else:
            st.info("No expense data available to display.")

