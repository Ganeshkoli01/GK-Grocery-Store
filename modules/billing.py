"""
GK GROCERY STORE – Direct Store POS Counter Billing Terminal (Owner Mode)
Enables fast point-of-sale checkout for in-store walk-in customers.
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from database.connection import fetch_all, fetch_one, get_db_transaction
from config import PAYMENT_METHODS
from utils.helpers import format_currency, generate_invoice_number
from utils.invoice_generator import generate_invoice_pdf
from utils.translations import t, get_product_display_name, get_category_display_name


def set_preset_value(session_key: str, new_val: float):
    """Safely updates widget state via on_click callback before widget instantiation."""
    st.session_state[session_key] = new_val


def render_pos_billing():
    """Renders high-speed POS billing counter for store owner."""
    st.markdown(
        f"""
        <div class="brand-header-box">
            <div>
                <div class="brand-title">{t('nav_pos')}</div>
                <div class="brand-subtitle">{t('app_subtitle')}</div>
            </div>
            <div style="text-align: right;">
                <span class="badge badge-success">POS ACTIVE</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    if "pos_cart" not in st.session_state:
        st.session_state.pos_cart = []

    c_left, c_right = st.columns([1.6, 1.4])

    with c_left:
        st.markdown(f"##### 🔍 {t('field_product_name')}")
        active_products = fetch_all(
            "SELECT id, name, category, selling_price, cost_price, stock_quantity, unit FROM products WHERE is_active = 1 AND stock_quantity > 0 ORDER BY name ASC"
        )
        p_dict = {
            f"{get_product_display_name(p['name'])} (₹{p['selling_price']:.2f}/{p['unit']}) [{t('field_stock')}: {p['stock_quantity']:g}]": p 
            for p in active_products
        }

        if p_dict:
            sel_item_label = st.selectbox(f"🔍 {t('field_product_name')}", list(p_dict.keys()), label_visibility="collapsed")
            selected_p = p_dict[sel_item_label]

            p_unit_raw = (selected_p["unit"] or "").lower().strip()
            is_weight = p_unit_raw in ["kg", "kilogram", "gram", "g"]
            is_volume = p_unit_raw in ["litre", "liter", "ml"]

            # ----------------------------------------------------
            # KILOGRAMS & GRAMS FLEXIBLE DUAL-MODE BILLING
            # ----------------------------------------------------
            if is_weight:
                c_mode, c_input = st.columns([1.1, 1.9])
                with c_mode:
                    unit_mode = st.radio(
                        t("billing_unit_type"),
                        ["kg", "g"],
                        format_func=lambda m: t("mode_kg") if m == "kg" else t("mode_gram"),
                        horizontal=True,
                        key=f"mode_sel_{selected_p['id']}"
                    )

                if unit_mode == "g":
                    max_g = float(selected_p["stock_quantity"] * 1000.0)
                    g_key = f"val_g_{selected_p['id']}"
                    if g_key not in st.session_state:
                        st.session_state[g_key] = min(500.0, max_g)
                    elif st.session_state[g_key] > max_g:
                        st.session_state[g_key] = max_g

                    with c_input:
                        bill_g = st.number_input(
                            f"{t('field_unit')} ({t('mode_gram')})",
                            min_value=10.0,
                            max_value=max_g,
                            step=50.0,
                            key=g_key
                        )
                    
                    # Quick preset buttons for grams
                    st.caption("Quick Grams Presets:")
                    g_cols = st.columns(5)
                    g_presets = [100.0, 250.0, 500.0, 750.0, 1000.0]
                    for g_idx, g_val in enumerate(g_presets):
                        if g_val <= max_g:
                            g_cols[g_idx].button(
                                f"{g_val:g} g",
                                key=f"chip_g_{selected_p['id']}_{g_val}",
                                on_click=set_preset_value,
                                args=(g_key, g_val),
                                use_container_width=True
                            )

                    bill_qty_base = bill_g / 1000.0
                    display_qty_str = f"{bill_g:g} g ({bill_qty_base:g} kg)"
                else:
                    max_k = float(selected_p["stock_quantity"])
                    k_key = f"val_kg_{selected_p['id']}"
                    if k_key not in st.session_state:
                        st.session_state[k_key] = min(1.0, max_k)
                    elif st.session_state[k_key] > max_k:
                        st.session_state[k_key] = max_k

                    with c_input:
                        bill_k = st.number_input(
                            f"{t('field_unit')} ({t('mode_kg')})",
                            min_value=0.01,
                            max_value=max_k,
                            step=0.25,
                            key=k_key
                        )
                    
                    # Quick preset buttons for kg
                    st.caption("Quick KG Presets:")
                    k_cols = st.columns(5)
                    k_presets = [0.25, 0.5, 1.0, 2.0, 5.0]
                    k_labels = ["250 g", "500 g", "1 kg", "2 kg", "5 kg"]
                    for k_idx, (k_val, k_lbl) in enumerate(zip(k_presets, k_labels)):
                        if k_val <= max_k:
                            k_cols[k_idx].button(
                                k_lbl,
                                key=f"chip_k_{selected_p['id']}_{k_val}",
                                on_click=set_preset_value,
                                args=(k_key, k_val),
                                use_container_width=True
                            )

                    bill_qty_base = bill_k
                    display_qty_str = f"{bill_k:g} kg ({bill_k * 1000:g} g)" if (bill_k * 1000) % 1000 != 0 else f"{bill_k:g} kg"

            # ----------------------------------------------------
            # LITRES & MILLILITRES DUAL-MODE BILLING
            # ----------------------------------------------------
            elif is_volume:
                c_mode, c_input = st.columns([1.1, 1.9])
                with c_mode:
                    vol_mode = st.radio(
                        t("billing_unit_type"),
                        ["L", "ml"],
                        format_func=lambda m: t("mode_litre") if m == "L" else t("mode_ml"),
                        horizontal=True,
                        key=f"mode_vol_{selected_p['id']}"
                    )

                if vol_mode == "ml":
                    max_ml = float(selected_p["stock_quantity"] * 1000.0)
                    with c_input:
                        bill_ml = st.number_input(
                            f"{t('field_unit')} ({t('mode_ml')})",
                            min_value=50.0,
                            max_value=max_ml,
                            value=min(500.0, max_ml),
                            step=50.0,
                            key=f"val_ml_{selected_p['id']}"
                        )
                    bill_qty_base = bill_ml / 1000.0
                    display_qty_str = f"{bill_ml:g} ml ({bill_qty_base:g} L)"
                else:
                    max_l = float(selected_p["stock_quantity"])
                    with c_input:
                        bill_l = st.number_input(
                            f"{t('field_unit')} ({t('mode_litre')})",
                            min_value=0.1,
                            max_value=max_l,
                            value=min(1.0, max_l),
                            step=0.5,
                            key=f"val_l_{selected_p['id']}"
                        )
                    bill_qty_base = bill_l
                    display_qty_str = f"{bill_l:g} L ({bill_l * 1000:g} ml)" if (bill_l * 1000) % 1000 != 0 else f"{bill_l:g} L"

            # ----------------------------------------------------
            # PACKET / PIECE / OTHER UNITS
            # ----------------------------------------------------
            else:
                max_oth = float(selected_p["stock_quantity"])
                bill_qty_base = st.number_input(
                    f"{t('field_unit')} ({selected_p['unit']})",
                    min_value=1.0,
                    max_value=max_oth,
                    value=min(1.0, max_oth),
                    step=1.0,
                    key=f"val_oth_{selected_p['id']}"
                )
                display_qty_str = f"{bill_qty_base:g} {selected_p['unit']}"

            # Real-time subtotal estimation banner
            est_subtotal = round(bill_qty_base * float(selected_p["selling_price"]), 2)
            st.markdown(
                f"""
                <div class="info-callout" style="padding: 8px 12px; margin: 8px 0;">
                    🛒 <b>{display_qty_str}</b> @ {format_currency(selected_p['selling_price'])}/{selected_p['unit']} = <b>{format_currency(est_subtotal)}</b>
                </div>
                """,
                unsafe_allow_html=True
            )

            if st.button(t("btn_add_item"), type="primary", use_container_width=True):
                # Check if already in pos_cart
                existing = next((item for item in st.session_state.pos_cart if item["product_id"] == selected_p["id"]), None)
                if existing:
                    new_q = existing["quantity"] + bill_qty_base
                    if new_q <= selected_p["stock_quantity"]:
                        existing["quantity"] = new_q
                        existing["subtotal"] = round(new_q * selected_p["selling_price"], 2)
                        if is_weight:
                            existing["display_qty"] = f"{new_q * 1000:g} g ({new_q:g} kg)" if new_q < 1.0 else (f"{new_q:g} kg ({new_q * 1000:g} g)" if (new_q * 1000) % 1000 != 0 else f"{new_q:g} kg")
                        elif is_volume:
                            existing["display_qty"] = f"{new_q * 1000:g} ml ({new_q:g} L)" if new_q < 1.0 else f"{new_q:g} L"
                        else:
                            existing["display_qty"] = f"{new_q:g} {selected_p['unit']}"
                    else:
                        st.error(f"Cannot exceed stock ({selected_p['stock_quantity']:g} {selected_p['unit']}).")
                else:
                    st.session_state.pos_cart.append({
                        "product_id": selected_p["id"],
                        "product_name": selected_p["name"],
                        "display_name": get_product_display_name(selected_p["name"]),
                        "category": selected_p["category"],
                        "unit": selected_p["unit"],
                        "cost_price": float(selected_p["cost_price"]),
                        "selling_price": float(selected_p["selling_price"]),
                        "quantity": bill_qty_base,
                        "display_qty": display_qty_str,
                        "subtotal": est_subtotal,
                        "max_stock": float(selected_p["stock_quantity"])
                    })
                st.rerun()

        st.markdown("<hr style='margin: 15px 0;'>", unsafe_allow_html=True)
        st.markdown(f"##### 🛒 {t('field_subtotal')}")
        if not st.session_state.pos_cart:
            st.caption("No items added to current bill yet.")
        else:
            for idx, item in enumerate(st.session_state.pos_cart):
                ci1, ci2, ci3, ci4 = st.columns([3.2, 1.4, 1.4, 0.7])
                with ci1:
                    disp = item.get("display_name", item["product_name"])
                    disp_q = item.get("display_qty", f"{item['quantity']:g} {item['unit']}")
                    st.write(f"**{disp}**<br><small style='color: #15803D; font-weight: 600;'>{disp_q}</small>", unsafe_allow_html=True)
                with ci2:
                    st.write(f"@{format_currency(item['selling_price'])}/{item['unit']}")
                with ci3:
                    st.write(f"**{format_currency(item['subtotal'])}**")
                with ci4:
                    if st.button("❌", key=f"pos_del_{idx}"):
                        st.session_state.pos_cart.pop(idx)
                        st.rerun()

    with c_right:
        st.markdown(f"##### 🧾 {t('field_grand_total')}")
        pos_subtotal = sum(it["subtotal"] for it in st.session_state.pos_cart)

        with st.form("pos_checkout_form"):
            walkin_name = st.text_input(t("field_customer_name"), value="Walk-in Customer")
            walkin_phone = st.text_input(t("field_customer_phone"), placeholder="+91 XXXXX XXXXX")
            payment_mode = st.selectbox(t("field_payment_method"), PAYMENT_METHODS, index=0)
            discount_val = st.number_input(t("field_discount"), min_value=0.0, max_value=float(pos_subtotal), value=0.0, step=5.0)

            final_total = max(pos_subtotal - discount_val, 0.0)

            st.markdown(
                f"""
                <div style="background: #F1F5F9; border-radius: 8px; padding: 14px; margin: 12px 0;">
                    <div style="display:flex; justify-content:space-between;"><span>{t('field_subtotal')}:</span><b>{format_currency(pos_subtotal)}</b></div>
                    <div style="display:flex; justify-content:space-between; color: #16A34A;"><span>{t('field_discount')}:</span><b>-{format_currency(discount_val)}</b></div>
                    <hr style="margin: 8px 0;">
                    <div style="display:flex; justify-content:space-between; font-size: 18px; font-weight:800; color: #14532D;">
                        <span>{t('field_grand_total')}:</span><span>{format_currency(final_total)}</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            submit_pos = st.form_submit_button(t("btn_complete_sale"), type="primary", use_container_width=True)

            if submit_pos:
                if not st.session_state.pos_cart:
                    st.error("Please add at least one item to bill.")
                else:
                    inv_no = generate_invoice_number()
                    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    try:
                        with get_db_transaction() as conn:
                            cursor = conn.cursor()
                            # 1. Insert sales header
                            cursor.execute(
                                """
                                INSERT INTO sales 
                                (invoice_no, customer_name, customer_phone, total_amount, discount_amount, grand_total, payment_method, payment_status, sale_date, is_sample)
                                VALUES (?, ?, ?, ?, ?, ?, ?, 'Paid', ?, 0)
                                """,
                                (
                                    inv_no,
                                    walkin_name.strip(),
                                    walkin_phone.strip(),
                                    round(pos_subtotal, 2),
                                    round(discount_val, 2),
                                    round(final_total, 2),
                                    payment_mode,
                                    now_str
                                )
                            )
                            sale_id = cursor.lastrowid

                            # 2. Insert items & deduct stock
                            for item in st.session_state.pos_cart:
                                prof = round((item["selling_price"] - item["cost_price"]) * item["quantity"], 2)
                                cursor.execute(
                                    """
                                    INSERT INTO sale_items 
                                    (sale_id, product_id, product_name, category, unit, quantity, cost_price, selling_price, subtotal, profit)
                                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                                    """,
                                    (
                                        sale_id,
                                        item["product_id"],
                                        item["product_name"],
                                        item["category"],
                                        item["unit"],
                                        item["quantity"],
                                        item["cost_price"],
                                        item["selling_price"],
                                        item["subtotal"],
                                        prof
                                    )
                                )

                                cursor.execute(
                                    """
                                    UPDATE products 
                                    SET stock_quantity = stock_quantity - ?, updated_at = CURRENT_TIMESTAMP
                                    WHERE id = ?
                                    """,
                                    (item["quantity"], item["product_id"])
                                )

                        st.session_state.pos_last_invoice = {
                            "sale_data": {
                                "invoice_no": inv_no,
                                "customer_name": walkin_name,
                                "customer_phone": walkin_phone,
                                "sale_date": now_str,
                                "total_amount": round(pos_subtotal, 2),
                                "discount_amount": round(discount_val, 2),
                                "grand_total": round(final_total, 2),
                                "payment_method": payment_mode
                            },
                            "items": st.session_state.pos_cart.copy()
                        }
                        st.session_state.pos_cart = []
                        st.success(f"Sale recorded! Invoice: {inv_no}")
                        st.rerun()

                    except Exception as e:
                        st.error(f"Billing failed: {str(e)}")

        if "pos_last_invoice" in st.session_state and st.session_state.pos_last_invoice:
            inv = st.session_state.pos_last_invoice
            pdf_b = generate_invoice_pdf(inv["sale_data"], inv["items"])
            st.download_button(
                f"{t('btn_download_pdf')} ({inv['sale_data']['invoice_no']})",
                data=pdf_b,
                file_name=f"{inv['sale_data']['invoice_no']}.pdf",
                mime="application/pdf",
                type="primary",
                use_container_width=True
            )

