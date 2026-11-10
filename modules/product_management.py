"""
GK GROCERY STORE – Product Management Module (Owner Only)
Enables adding, editing, searching, and managing products with live profit margin calculations.
"""

import streamlit as st
import pandas as pd
from datetime import date
from database.connection import fetch_all, fetch_one, execute_insert, execute_query, fetch_dataframe
from config import PRODUCT_CATEGORIES, PRODUCT_UNITS, CURRENCY
from utils.helpers import format_currency
from utils.translations import t, get_current_language, get_product_display_name, get_category_display_name


def render_product_management():
    """Renders product catalog management interface."""
    st.markdown(
        f"""
        <div class="brand-header-box">
            <div>
                <div class="brand-title">{t('nav_products')}</div>
                <div class="brand-subtitle">{t('app_subtitle')}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    tab_list, tab_add, tab_edit = st.tabs([f"📋 {t('field_product_name')}", f"➕ {t('btn_add_product')}", f"✏️ {t('btn_update_product')}"])

    # TAB 1: Product Catalog List & Search
    with tab_list:
        c_search, c_cat, c_status = st.columns([2, 1.5, 1])
        with c_search:
            search_query = st.text_input("🔍 Search by Product Name or ID", placeholder="e.g. Rice, Dal, Tea...")
        with c_cat:
            cat_filter = st.selectbox("Filter Category", ["All Categories"] + PRODUCT_CATEGORIES)
        with c_status:
            status_filter = st.selectbox("Status", ["All", "Active Only", "Inactive Only"])

        # Construct query
        where_clauses = []
        params = []

        if search_query.strip():
            where_clauses.append("(name LIKE ? OR id = ?)")
            params.extend([f"%{search_query.strip()}%", search_query.strip()])

        if cat_filter != "All Categories":
            where_clauses.append("category = ?")
            params.append(cat_filter)

        if status_filter == "Active Only":
            where_clauses.append("is_active = 1")
        elif status_filter == "Inactive Only":
            where_clauses.append("is_active = 0")

        where_sql = ("WHERE " + " AND ".join(where_clauses)) if where_clauses else ""
        sql = f"""
            SELECT 
                id as "ID",
                name as "Product Name",
                category as "Category",
                cost_price as "Cost Price (₹)",
                selling_price as "Selling Price (₹)",
                ROUND(selling_price - cost_price, 2) as "Unit Margin (₹)",
                ROUND(((selling_price - cost_price) / selling_price) * 100, 1) as "Margin (%)",
                stock_quantity as "Stock Qty",
                unit as "Unit",
                min_stock_level as "Min Threshold",
                is_active as "Active"
            FROM products
            {where_sql}
            ORDER BY id DESC
        """

        df = fetch_dataframe(sql, tuple(params))

        if not df.empty:
            df["Product Name"] = df["Product Name"].apply(lambda n: get_product_display_name(n))
            df["Category"] = df["Category"].apply(lambda c: get_category_display_name(c))
            st.dataframe(
                df,
                use_container_width=True,
                column_config={
                    "Cost Price (₹)": st.column_config.NumberColumn(format="₹%.2f"),
                    "Selling Price (₹)": st.column_config.NumberColumn(format="₹%.2f"),
                    "Unit Margin (₹)": st.column_config.NumberColumn(format="₹%.2f"),
                    "Margin (%)": st.column_config.NumberColumn(format="%.1f%%"),
                    "Active": st.column_config.CheckboxColumn()
                },
                hide_index=True
            )
            st.caption(f"Showing **{len(df)}** products matching criteria.")
        else:
            st.warning("No products found matching the search criteria.")

    # TAB 2: Add New Product
    with tab_add:
        st.markdown("##### ➕ Create New Grocery Product")
        with st.form("add_product_form", clear_on_submit=True):
            col_a1, col_a2 = st.columns(2)
            with col_a1:
                p_name = st.text_input("Product Name *", placeholder="e.g. Daawat Super Basmati Rice")
                p_category = st.selectbox("Category *", PRODUCT_CATEGORIES)
                p_unit = st.selectbox("Unit of Measure *", PRODUCT_UNITS, index=0)
                p_expiry = st.date_input("Expiry Date (Optional)", value=None)

            with col_a2:
                p_cost = st.number_input("Cost Price (Wholesale Purchase) ₹ *", min_value=0.01, value=50.0, step=1.0)
                p_selling = st.number_input("Selling Price (Retail Charge) ₹ *", min_value=0.01, value=65.0, step=1.0)
                p_initial_stock = st.number_input("Initial Available Stock *", min_value=0.0, value=20.0, step=1.0)
                p_min_stock = st.number_input("Minimum Stock Alert Level *", min_value=1.0, value=10.0, step=1.0)

            # Live Margin Calculation Info Box
            unit_margin = p_selling - p_cost
            margin_pct = (unit_margin / p_selling * 100.0) if p_selling > 0 else 0.0

            if unit_margin > 0:
                st.markdown(
                    f"""
                    <div class="info-callout">
                        <b>📈 Expected Unit Economics:</b> Profit per {p_unit}: <b>{format_currency(unit_margin)}</b> | Expected Margin: <b>{margin_pct:.1f}%</b>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f"""
                    <div class="warning-callout">
                        <b>⚠️ Alert:</b> Selling price is less than or equal to cost price! Unit margin: <b>{format_currency(unit_margin)}</b>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            submit_add = st.form_submit_button("Save New Product", use_container_width=True, type="primary")

            if submit_add:
                if not p_name.strip():
                    st.error("Product name cannot be empty.")
                else:
                    exp_date_str = p_expiry.isoformat() if p_expiry else None
                    try:
                        new_id = execute_insert(
                            """
                            INSERT INTO products 
                            (name, category, cost_price, selling_price, stock_quantity, min_stock_level, unit, expiry_date, is_active)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, 1)
                            """,
                            (p_name.strip(), p_category, p_cost, p_selling, p_initial_stock, p_min_stock, p_unit, exp_date_str)
                        )
                        st.success(f"Product '{p_name}' successfully added with ID #{new_id}!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error saving product: {str(e)}")

    # TAB 3: Edit / Deactivate Product
    with tab_edit:
        st.markdown("##### ✏️ Modify Existing Product Details")
        all_prods = fetch_all("SELECT id, name, category, cost_price, selling_price, stock_quantity, min_stock_level, unit, is_active FROM products ORDER BY name ASC")
        prod_options = {f"#{p['id']} - {get_product_display_name(p['name'])} ({get_category_display_name(p['category'])})": p['id'] for p in all_prods}

        if prod_options:
            selected_label = st.selectbox("Select Product to Edit", list(prod_options.keys()))
            selected_id = prod_options[selected_label]
            prod = fetch_one("SELECT * FROM products WHERE id = ?", (selected_id,))

            if prod:
                with st.form("edit_product_form"):
                    e_col1, e_col2 = st.columns(2)
                    with e_col1:
                        edit_name = st.text_input("Product Name", value=prod["name"])
                        cat_idx = PRODUCT_CATEGORIES.index(prod["category"]) if prod["category"] in PRODUCT_CATEGORIES else 0
                        edit_category = st.selectbox("Category", PRODUCT_CATEGORIES, index=cat_idx)
                        unit_idx = PRODUCT_UNITS.index(prod["unit"]) if prod["unit"] in PRODUCT_UNITS else 0
                        edit_unit = st.selectbox("Unit", PRODUCT_UNITS, index=unit_idx)
                        edit_active = st.checkbox("Product is Active / Sellable", value=bool(prod["is_active"]))

                    with e_col2:
                        edit_cost = st.number_input("Cost Price ₹", min_value=0.01, value=float(prod["cost_price"]), step=1.0)
                        edit_selling = st.number_input("Selling Price ₹", min_value=0.01, value=float(prod["selling_price"]), step=1.0)
                        edit_stock = st.number_input("Available Stock", min_value=0.0, value=float(prod["stock_quantity"]), step=1.0)
                        edit_min = st.number_input("Min Stock Level", min_value=1.0, value=float(prod["min_stock_level"]), step=1.0)

                    margin_val = edit_selling - edit_cost
                    margin_p = (margin_val / edit_selling * 100.0) if edit_selling > 0 else 0.0
                    st.caption(f"Calculated Margin: **{format_currency(margin_val)}** ({margin_p:.1f}%)")

                    submit_edit = st.form_submit_button("Update Product", use_container_width=True, type="primary")

                    if submit_edit:
                        execute_query(
                            """
                            UPDATE products 
                            SET name = ?, category = ?, cost_price = ?, selling_price = ?, 
                                stock_quantity = ?, min_stock_level = ?, unit = ?, is_active = ?, updated_at = CURRENT_TIMESTAMP
                            WHERE id = ?
                            """,
                            (edit_name.strip(), edit_category, edit_cost, edit_selling, edit_stock, edit_min, edit_unit, 1 if edit_active else 0, selected_id)
                        )
                        st.success(f"Product '{edit_name}' successfully updated!")
                        st.rerun()
        else:
            st.info("No products currently exist in database.")

