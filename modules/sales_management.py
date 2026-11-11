"""
GK GROCERY STORE – Sales Management & Audit Module
Enables searching, filtering, inspecting transaction line items, and downloading reports.
"""

import streamlit as st
import pandas as pd
from datetime import date
from database.connection import fetch_dataframe, fetch_all, fetch_one
from utils.helpers import format_currency, get_date_range
from utils.invoice_generator import generate_invoice_pdf
from utils.translations import t, get_product_display_name


def render_sales_management():
    """Renders sales transaction records and audit tools."""
    st.markdown(
        f"""
        <div class="brand-header-box">
            <div>
                <div class="brand-title">{t('nav_sales')}</div>
                <div class="brand-subtitle">{t('app_subtitle')}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Filter Bar
    c_f1, c_f2, c_f3 = st.columns([2, 1.5, 1.5])
    with c_f1:
        search_txt = st.text_input("🔍 Search Invoice No or Customer", placeholder="e.g. GK-202611... or Sharma")
    with c_f2:
        date_filter = st.selectbox(
            "Filter Timeframe",
            ["Today", "Yesterday", "Last 7 Days", "Last 30 Days", "This Month", "This Year", "All Time", "Specific Day"]
        )
    with c_f3:
        pay_filter = st.selectbox("Payment Method", ["All Payment Methods", "Cash", "UPI", "Card", "Other"])

    specific_day = None
    if date_filter == "Specific Day":
        specific_day = st.date_input("Select Day", value=date.today())

    # Build WHERE conditions
    where = []
    params = []

    if search_txt.strip():
        where.append("(s.invoice_no LIKE ? OR s.customer_name LIKE ? OR s.customer_phone LIKE ?)")
        params.extend([f"%{search_txt.strip()}%", f"%{search_txt.strip()}%", f"%{search_txt.strip()}%"])

    if date_filter == "Specific Day" and specific_day:
        where.append("DATE(s.sale_date) = ?")
        params.append(specific_day.isoformat())
    else:
        st_dt, end_dt = get_date_range(date_filter)
        where.append("s.sale_date BETWEEN ? AND ?")
        params.extend([st_dt.strftime("%Y-%m-%d 00:00:00"), end_dt.strftime("%Y-%m-%d 23:59:59")])

    if pay_filter != "All Payment Methods":
        where.append("s.payment_method = ?")
        params.append(pay_filter)

    where_sql = ("WHERE " + " AND ".join(where)) if where else ""

    sql = f"""
        SELECT 
            s.id,
            s.invoice_no as "Invoice No",
            s.sale_date as "Date & Time",
            s.customer_name as "Customer",
            s.customer_phone as "Phone",
            s.payment_method as "Payment",
            s.total_amount as "Subtotal (₹)",
            s.discount_amount as "Discount (₹)",
            s.grand_total as "Grand Total (₹)"
        FROM sales s
        {where_sql}
        ORDER BY s.sale_date DESC
    """

    df_sales = fetch_dataframe(sql, tuple(params))

    # Metric Bar
    total_rev = df_sales["Grand Total (₹)"].sum() if not df_sales.empty else 0.0
    total_tx = len(df_sales)

    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("Total Transactions", f"{total_tx:,}")
    with m2:
        st.metric("Total Filtered Revenue", format_currency(total_rev))
    with m3:
        avg_t = total_rev / total_tx if total_tx > 0 else 0.0
        st.metric("Average Transaction Value", format_currency(avg_t))

    st.markdown("<hr style='margin: 12px 0;'>", unsafe_allow_html=True)

    if df_sales.empty:
        st.warning("No sales transactions found matching your filter criteria.")
    else:
        # Table of transactions
        display_df = df_sales.drop(columns=["id"])
        st.dataframe(
            display_df,
            use_container_width=True,
            column_config={
                "Subtotal (₹)": st.column_config.NumberColumn(format="₹%.2f"),
                "Discount (₹)": st.column_config.NumberColumn(format="₹%.2f"),
                "Grand Total (₹)": st.column_config.NumberColumn(format="₹%.2f"),
            },
            hide_index=True
        )

        # Quick CSV Download of Filtered Sales
        csv_bytes = display_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Export Filtered Sales to CSV",
            data=csv_bytes,
            file_name=f"sales_export_{date.today().isoformat()}.csv",
            mime="text/csv"
        )

        st.markdown("<hr style='margin: 15px 0;'>", unsafe_allow_html=True)
        st.markdown("##### 🔍 Inspect Invoice Details & Re-print Receipt")

        # Invoice selector
        inv_choices = {f"{row['Invoice No']} | {row['Customer']} | {format_currency(row['Grand Total (₹)'])}": row['id'] for _, row in df_sales.head(50).iterrows()}
        selected_inv_label = st.selectbox("Choose an Invoice to Inspect:", list(inv_choices.keys()))
        selected_sale_id = inv_choices[selected_inv_label]

        sale_record = fetch_one("SELECT * FROM sales WHERE id = ?", (selected_sale_id,))
        items_bought = fetch_all(
            """
            SELECT product_name, category, unit, quantity, cost_price, selling_price, subtotal, profit
            FROM sale_items
            WHERE sale_id = ?
            """,
            (selected_sale_id,)
        )

        if sale_record and items_bought:
            col_d1, col_d2 = st.columns([2, 1])
            with col_d1:
                df_detail = pd.DataFrame(items_bought)
                df_detail["product_name"] = df_detail["product_name"].apply(lambda n: get_product_display_name(n))
                st.markdown(f"**Items Breakdown for Invoice `{sale_record['invoice_no']}`:**")
                st.dataframe(
                    df_detail.rename(columns={
                        "product_name": "Product",
                        "category": "Category",
                        "unit": "Unit",
                        "quantity": "Qty",
                        "cost_price": "Cost (₹)",
                        "selling_price": "Selling (₹)",
                        "subtotal": "Subtotal (₹)",
                        "profit": "Profit (₹)"
                    }),
                    use_container_width=True,
                    hide_index=True
                )

            with col_d2:
                st.markdown("**Invoice Actions:**")
                pdf_inv = generate_invoice_pdf(sale_record, items_bought)
                st.download_button(
                    label=f"📥 Download PDF Invoice ({sale_record['invoice_no']})",
                    data=pdf_inv,
                    file_name=f"{sale_record['invoice_no']}.pdf",
                    mime="application/pdf",
                    type="primary",
                    use_container_width=True
                )

