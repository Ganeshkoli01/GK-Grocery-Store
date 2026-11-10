"""
GK GROCERY STORE – Customer Purchase History & Invoices Module
Allows customers to view their in-store purchases and download official PDF tax invoices.
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from database.connection import fetch_all, fetch_one
from utils.helpers import format_currency
from utils.invoice_generator import generate_invoice_pdf
from utils.translations import t, get_product_display_name, get_category_display_name


def render_customer_purchase_history():
    """Renders customer purchase history, itemized breakdowns, and tax invoice downloads."""
    st.markdown(
        f"""
        <div class="brand-header-box">
            <div>
                <div class="brand-title">{t('nav_customer_history')}</div>
                <div class="brand-subtitle">{t('app_subtitle')}</div>
            </div>
            <div style="text-align: right;">
                <span class="badge badge-success">{t('role_customer')}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    user_id = st.session_state.get("user_id")
    customer_name = st.session_state.get("full_name") or ""

    # Fetch customer's orders
    sales_history = fetch_all(
        """
        SELECT s.id, s.invoice_no, s.sale_date, s.grand_total, s.payment_method, s.customer_name, s.customer_phone, s.total_amount, s.discount_amount
        FROM sales s
        LEFT JOIN customers c ON s.customer_id = c.id
        WHERE (c.user_id = ? OR s.customer_name = ?)
        ORDER BY s.sale_date DESC
        """,
        (user_id, customer_name)
    )

    if not sales_history:
        st.info("ℹ️ No past purchases found for your account.")
        return

    # Customer KPI Stats
    total_orders = len(sales_history)
    total_spent = sum(float(s["grand_total"]) for s in sales_history)
    last_date = sales_history[0]["sale_date"]

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(
            f"""
            <div class="kpi-card kpi-primary">
                <div class="kpi-title">Total Orders Placed</div>
                <div class="kpi-value">{total_orders}</div>
                <div class="kpi-subtext">Verified Store Visits</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with c2:
        st.markdown(
            f"""
            <div class="kpi-card kpi-secondary">
                <div class="kpi-title">Total Amount Spent</div>
                <div class="kpi-value">{format_currency(total_spent)}</div>
                <div class="kpi-subtext">Cumulative Store Purchases</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with c3:
        st.markdown(
            f"""
            <div class="kpi-card kpi-info">
                <div class="kpi-title">Most Recent Purchase</div>
                <div class="kpi-value" style="font-size: 16px; font-weight: 700; margin-top: 5px;">{last_date}</div>
                <div class="kpi-subtext">Invoice: {sales_history[0]['invoice_no']}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<hr style='margin: 20px 0;'>", unsafe_allow_html=True)
    st.markdown("##### 🧾 All Invoices & Order Receipts")

    # Search / Filter Invoices
    search_inv = st.text_input("🔍 Search Invoices", placeholder="Search by Invoice No or Date...")

    filtered_history = sales_history
    if search_inv.strip():
        q = search_inv.strip().lower()
        filtered_history = [
            s for s in sales_history 
            if q in str(s["invoice_no"]).lower() or q in str(s["sale_date"]).lower()
        ]

    for s_record in filtered_history:
        with st.expander(f"🧾 {s_record['invoice_no']}  |  📅 {s_record['sale_date']}  |  💰 {format_currency(s_record['grand_total'])}  |  💳 {s_record['payment_method']}"):
            items_bought = fetch_all(
                """
                SELECT product_name, category, unit, quantity, selling_price, subtotal
                FROM sale_items
                WHERE sale_id = ?
                """,
                (s_record["id"],)
            )

            col_items, col_act = st.columns([2.2, 1])

            with col_items:
                df_items = pd.DataFrame(items_bought)
                if not df_items.empty:
                    df_items["product_name"] = df_items["product_name"].apply(lambda n: get_product_display_name(n))
                    df_items["category"] = df_items["category"].apply(lambda c: get_category_display_name(c))
                    st.table(df_items.rename(columns={
                        "product_name": t("field_product_name"),
                        "category": t("field_category"),
                        "unit": t("field_unit"),
                        "quantity": "Qty",
                        "selling_price": t("field_selling_price"),
                        "subtotal": t("field_subtotal")
                    }))

            with col_act:
                st.markdown(
                    f"""
                    <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 12px; margin-bottom: 12px;">
                        <div style="display:flex; justify-content:space-between; font-size: 13px;">
                            <span>Subtotal:</span><b>{format_currency(s_record['total_amount'])}</b>
                        </div>
                        <div style="display:flex; justify-content:space-between; font-size: 13px; color: #16A34A;">
                            <span>Discount:</span><b>-{format_currency(s_record['discount_amount'])}</b>
                        </div>
                        <hr style="margin: 6px 0;">
                        <div style="display:flex; justify-content:space-between; font-size: 15px; font-weight:800; color: #14532D;">
                            <span>Grand Total:</span><span>{format_currency(s_record['grand_total'])}</span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                sale_dict = {
                    "invoice_no": s_record["invoice_no"],
                    "customer_name": s_record["customer_name"],
                    "customer_phone": s_record["customer_phone"],
                    "sale_date": s_record["sale_date"],
                    "total_amount": s_record["total_amount"],
                    "discount_amount": s_record["discount_amount"],
                    "grand_total": s_record["grand_total"],
                    "payment_method": s_record["payment_method"]
                }
                pdf_hist = generate_invoice_pdf(sale_dict, items_bought)
                st.download_button(
                    label=f"📥 Download Tax Invoice PDF",
                    data=pdf_hist,
                    file_name=f"{s_record['invoice_no']}.pdf",
                    mime="application/pdf",
                    key=f"hist_pdf_{s_record['id']}",
                    type="primary",
                    use_container_width=True
                )
