"""
GK GROCERY STORE – Inventory Management Module
Tracks stock levels, handles inward purchase batches, calculates valuations,
and raises automated low-stock warnings.
"""

import streamlit as st
import pandas as pd
from datetime import date
from database.connection import fetch_dataframe, fetch_all, fetch_one, execute_query, execute_insert
from analytics.inventory_analysis import get_inventory_kpis, get_restock_recommendations
from utils.helpers import format_currency
from utils.translations import t, get_product_display_name, get_category_display_name


def render_inventory_management():
    """Renders comprehensive inventory management console."""
    st.markdown(
        f"""
        <div class="brand-header-box">
            <div>
                <div class="brand-title">{t('nav_inventory')}</div>
                <div class="brand-subtitle">{t('app_subtitle')}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    kpis = get_inventory_kpis()

    # KPI summary bar
    st.markdown(
        f"""
        <div class="kpi-grid">
            <div class="kpi-card kpi-primary">
                <div class="kpi-title">{t('kpi_total_products')}</div>
                <div class="kpi-value">{kpis['total_products']}</div>
                <div class="kpi-subtext">{kpis['total_units']:g} total stock units</div>
            </div>
            <div class="kpi-card kpi-secondary">
                <div class="kpi-title">{t('kpi_stock_valuation_cost')}</div>
                <div class="kpi-value">{format_currency(kpis['total_cost_valuation'])}</div>
                <div class="kpi-subtext">Capital tied in inventory</div>
            </div>
            <div class="kpi-card kpi-info">
                <div class="kpi-title">{t('kpi_stock_valuation_retail')}</div>
                <div class="kpi-value">{format_currency(kpis['total_retail_valuation'])}</div>
                <div class="kpi-subtext">Potential Profit: {format_currency(kpis['potential_profit'])}</div>
            </div>
            <div class="kpi-card kpi-accent">
                <div class="kpi-title">{t('kpi_low_stock')}</div>
                <div class="kpi-value">{kpis['low_stock_count']}</div>
                <div class="kpi-subtext">Requires replenishment</div>
            </div>
            <div class="kpi-card kpi-danger">
                <div class="kpi-title">{t('kpi_out_stock')}</div>
                <div class="kpi-value">{kpis['out_of_stock_count']}</div>
                <div class="kpi-subtext sub-danger">Zero inventory left</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    tab_all, tab_low, tab_out, tab_restock_rec, tab_inward = st.tabs([
        f"📋 {t('status_in_stock')}",
        f"⚠️ {t('status_low_stock')} ({kpis['low_stock_count']})",
        f"🚨 {t('status_out_of_stock')} ({kpis['out_of_stock_count']})",
        "💡 Restock Recommendations",
        "📥 Inward Stock / Restock"
    ])

    # Tab 1: All Available Products
    with tab_all:
        sql_all = """
            SELECT 
                p.id as "ID",
                p.name as "Product Name",
                p.category as "Category",
                p.stock_quantity as "Available Stock",
                p.min_stock_level as "Min Threshold",
                p.unit as "Unit",
                p.cost_price as "Cost Price (₹)",
                p.selling_price as "Selling Price (₹)",
                ROUND(p.stock_quantity * p.cost_price, 2) as "Cost Value (₹)",
                ROUND(p.stock_quantity * p.selling_price, 2) as "Retail Value (₹)",
                CASE 
                    WHEN p.stock_quantity <= 0 THEN 'OUT OF STOCK'
                    WHEN p.stock_quantity <= p.min_stock_level THEN 'LOW STOCK'
                    ELSE 'HEALTHY'
                END as "Status"
            FROM products p
            WHERE p.is_active = 1
            ORDER BY p.category, p.name
        """
        df_all = fetch_dataframe(sql_all)
        st.dataframe(
            df_all,
            use_container_width=True,
            column_config={
                "Cost Price (₹)": st.column_config.NumberColumn(format="₹%.2f"),
                "Selling Price (₹)": st.column_config.NumberColumn(format="₹%.2f"),
                "Cost Value (₹)": st.column_config.NumberColumn(format="₹%.2f"),
                "Retail Value (₹)": st.column_config.NumberColumn(format="₹%.2f"),
            },
            hide_index=True
        )

    # Tab 2: Low Stock Products
    with tab_low:
        sql_low = """
            SELECT 
                p.id as "ID",
                p.name as "Product Name",
                p.category as "Category",
                p.stock_quantity as "Available Stock",
                p.min_stock_level as "Min Threshold",
                p.unit as "Unit",
                p.cost_price as "Cost Price (₹)",
                p.selling_price as "Selling Price (₹)"
            FROM products p
            WHERE p.is_active = 1 AND p.stock_quantity > 0 AND p.stock_quantity <= p.min_stock_level
            ORDER BY p.stock_quantity ASC
        """
        df_low = fetch_dataframe(sql_low)
        if not df_low.empty:
            st.warning(f"⚠️ **{len(df_low)} products** are currently at or below their minimum safety stock threshold!")
            st.dataframe(df_low, use_container_width=True, hide_index=True)
        else:
            st.success("✅ Excellent! No products are currently in low-stock status.")

    # Tab 3: Out of Stock Products
    with tab_out:
        sql_out = """
            SELECT 
                p.id as "ID",
                p.name as "Product Name",
                p.category as "Category",
                p.stock_quantity as "Available Stock",
                p.unit as "Unit",
                p.cost_price as "Cost Price (₹)",
                p.selling_price as "Selling Price (₹)"
            FROM products p
            WHERE p.is_active = 1 AND p.stock_quantity <= 0
            ORDER BY p.name ASC
        """
        df_out = fetch_dataframe(sql_out)
        if not df_out.empty:
            st.error(f"🚨 **{len(df_out)} products** are completely out of stock!")
            st.dataframe(df_out, use_container_width=True, hide_index=True)
        else:
            st.success("✅ No products are out of stock.")

    # Tab 4: Restock Recommendations
    with tab_restock_rec:
        st.markdown("##### 💡 Intelligent Restock Suggestions")
        st.caption("Generated by analyzing current stock against minimum thresholds and 30-day sales velocity.")
        df_rec = get_restock_recommendations()
        if not df_rec.empty:
            st.dataframe(
                df_rec,
                use_container_width=True,
                column_config={
                    "cost_price": st.column_config.NumberColumn(label="Unit Cost (₹)", format="₹%.2f"),
                    "suggested_order_qty": st.column_config.NumberColumn(label="Suggested Order Qty", format="%.0f"),
                    "urgency_status": st.column_config.TextColumn(label="Urgency Level"),
                },
                hide_index=True
            )
        else:
            st.success("All inventory is currently at healthy operating levels!")

    # Tab 5: Inward Stock / Quick Restock Form
    with tab_inward:
        st.markdown("##### 📥 Inward Stock Batch / Quick Replenishment")
        all_active = fetch_all("SELECT id, name, category, stock_quantity, unit, cost_price FROM products WHERE is_active = 1 ORDER BY name ASC")
        p_choices = {f"#{p['id']} - {get_product_display_name(p['name'])} ({t('field_stock')}: {p['stock_quantity']:g} {p['unit']})": p['id'] for p in all_active}

        if p_choices:
            with st.form("inward_stock_form"):
                sel_p = st.selectbox("Select Product to Replenish *", list(p_choices.keys()))
                prod_id = p_choices[sel_p]
                prod_data = fetch_one("SELECT * FROM products WHERE id = ?", (prod_id,))

                col_in1, col_in2 = st.columns(2)
                with col_in1:
                    add_qty = st.number_input(f"Quantity to Add ({prod_data['unit']}) *", min_value=1.0, value=20.0, step=1.0)
                    new_cost = st.number_input("Purchase Cost Price ₹ (per unit)", min_value=0.01, value=float(prod_data["cost_price"]), step=1.0)

                with col_in2:
                    supplier = st.text_input("Supplier / Mandi Vendor Name", value="Wholesale Mandi Supplier")
                    invoice_ref = st.text_input("Supplier Invoice / Bill No.", placeholder="e.g. WH-8492")

                st.info(f"New Projected Stock: **{prod_data['stock_quantity'] + add_qty:g} {prod_data['unit']}** | Total Batch Cost: **{format_currency(add_qty * new_cost)}**")
                submit_inward = st.form_submit_button("Record Inward Stock & Update Inventory", use_container_width=True, type="primary")

                if submit_inward:
                    try:
                        # 1. Update product stock and optionally update cost price
                        execute_query(
                            """
                            UPDATE products 
                            SET stock_quantity = stock_quantity + ?, cost_price = ?, updated_at = CURRENT_TIMESTAMP
                            WHERE id = ?
                            """,
                            (add_qty, new_cost, prod_id)
                        )

                        # 2. Record stock purchase history
                        purch_id = execute_insert(
                            """
                            INSERT INTO stock_purchases (supplier_name, invoice_ref, total_amount, purchase_date, notes)
                            VALUES (?, ?, ?, ?, ?)
                            """,
                            (supplier, invoice_ref, round(add_qty * new_cost, 2), date.today().isoformat(), f"Restocked {prod_data['name']}")
                        )

                        execute_insert(
                            """
                            INSERT INTO stock_purchase_items (purchase_id, product_id, quantity, cost_price, subtotal)
                            VALUES (?, ?, ?, ?, ?)
                            """,
                            (purch_id, prod_id, add_qty, new_cost, round(add_qty * new_cost, 2))
                        )

                        st.success(f"Successfully added {add_qty:g} {prod_data['unit']} to '{prod_data['name']}'!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error updating stock: {str(e)}")

