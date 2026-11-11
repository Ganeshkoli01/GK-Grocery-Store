"""
====================================================================
GK GROCERY STORE – SMART MANAGEMENT & BUSINESS ANALYTICS SYSTEM
Main Application Entrypoint
====================================================================
"""

import sys
from pathlib import Path

# Add project root directory to Python path
ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import streamlit as st

# 1. Page Configuration (Must be first Streamlit command)
st.set_page_config(
    page_title="GK GROCERY STORE – SMART BUSINESS ANALYTICS",
    page_icon="assets/logo.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import App Components
from config import APP_NAME, APP_SUBTITLE, APP_TAGLINE, APP_VERSION
from assets.styles import get_custom_css
from database.db_setup import init_database, seed_sample_data
from database.connection import fetch_one
from utils.helpers import get_logo_base64
from modules.authentication import (
    init_session_state,
    render_auth_page,
    logout_user,
    safe_get_query_param,
    safe_set_query_param
)
from modules.owner_dashboard import render_owner_dashboard
from modules.customer_dashboard import render_customer_purchase_history
from modules.product_management import render_product_management
from modules.inventory_management import render_inventory_management
from modules.billing import render_pos_billing
from modules.sales_management import render_sales_management
from modules.profit_loss import render_profit_loss
from modules.expense_management import render_expense_management
from modules.product_performance import render_product_performance
from modules.reports import render_reports
from modules.powerbi_view import render_powerbi_guide
from utils.translations import LANGUAGES, t, get_current_language, get_product_display_name


def ensure_db_ready():
    """Checks and initializes database schema and sample data on startup."""
    try:
        init_database()
        # If no products, seed automatically
        prod_check = fetch_one("SELECT COUNT(*) as cnt FROM products")
        if not prod_check or prod_check["cnt"] == 0:
            seed_sample_data()
    except Exception as e:
        st.error(f"Database initialization warning: {e}")


# Streamlit App Execution
def main():
    # Inject Custom Styling
    st.markdown(get_custom_css(), unsafe_allow_html=True)

    # Initialize State & Database
    init_session_state()
    ensure_db_ready()

    # Authentication Gate
    if not st.session_state.authenticated:
        render_auth_page()
        return

    # User Profile & Role from Session State
    user_role = st.session_state.get("user_role", "customer")
    full_name = st.session_state.get("full_name", "User")
    username = st.session_state.get("username", "")

    # Sidebar Navigation & Branding
    with st.sidebar:
        # Language Selector (English / मराठी / हिंदी)
        st.markdown("<div style='font-size: 11px; font-weight: 700; color: #475569; margin-bottom: 4px;'>🌐 LANGUAGE / भाषा / भाषा</div>", unsafe_allow_html=True)
        lang_keys = list(LANGUAGES.keys())
        current_idx = lang_keys.index(get_current_language())
        chosen_lang = st.selectbox(
            "Language",
            lang_keys,
            format_func=lambda k: LANGUAGES[k],
            index=current_idx,
            label_visibility="collapsed",
            key="app_language_selector"
        )
        if chosen_lang != st.session_state.get("language"):
            st.session_state.language = chosen_lang
            st.rerun()

        st.markdown("<div style='margin-bottom: 12px;'></div>", unsafe_allow_html=True)

        logo_uri = get_logo_base64()
        logo_html = f'<img src="{logo_uri}" style="width: 76px; height: 76px; border-radius: 50%; box-shadow: 0 4px 12px rgba(0,0,0,0.25); margin: 0 auto 8px auto; display: block; border: 2px solid rgba(255,255,255,0.7);" alt="GK Logo"/>' if logo_uri else '<div style="font-size: 24px; margin-bottom: 2px;">🛒</div>'

        st.markdown(
            f"""
            <div class="sidebar-brand-box">
                {logo_html}
                <div style="font-size: 16px; font-weight: 800; letter-spacing: -0.3px;">{t('app_title')}</div>
                <div style="font-size: 11px; opacity: 0.9; margin-top: 2px;">{t('app_subtitle')}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        role_badge = f"👑 {t('role_owner')}" if user_role == "owner" else f"👤 {t('role_customer')}"
        st.markdown(
            f"""
            <div class="sidebar-user-pill">
                <span>{full_name}</span>
                <span class="badge badge-success">{role_badge}</span>
            </div>
            """,
            unsafe_allow_html=True
        )

        # OWNER ROLE NAVIGATION
        if user_role == "owner":
            owner_nav_dict = {
                "dashboard": t("nav_dashboard"),
                "pos": t("nav_pos"),
                "products": t("nav_products"),
                "inventory": t("nav_inventory"),
                "sales": t("nav_sales"),
                "pnl": t("nav_pnl"),
                "expenses": t("nav_expenses"),
                "performance": t("nav_performance"),
                "reports": t("nav_reports"),
                "powerbi": t("nav_powerbi")
            }

            default_page = safe_get_query_param("page", "dashboard")
            page_keys = list(owner_nav_dict.keys())
            idx = page_keys.index(default_page) if default_page in page_keys else 0

            nav_key = st.radio(
                t("nav_menu_title"),
                page_keys,
                format_func=lambda k: owner_nav_dict[k],
                index=idx
            )
            if nav_key != default_page:
                safe_set_query_param("page", nav_key)

        # CUSTOMER ROLE NAVIGATION (Only My Purchase History)
        else:
            cust_nav_dict = {
                "customer_history": t("nav_customer_history")
            }

            nav_key = st.radio(
                t("customer_menu_title"),
                list(cust_nav_dict.keys()),
                format_func=lambda k: cust_nav_dict[k],
                index=0
            )

        st.markdown("<hr style='margin: 20px 0; border: none; border-top: 1px solid #E2E8F0;'>", unsafe_allow_html=True)

        if st.button(t("sign_out"), use_container_width=True):
            logout_user()

        st.markdown(
            f"""
            <div style="text-align: center; color: #94A3B8; font-size: 11px; margin-top: 15px;">
                v{APP_VERSION} • {t('app_title')}<br>
                Pune, Maharashtra
            </div>
            """,
            unsafe_allow_html=True
        )

    # PAGE ROUTER
    if user_role == "owner":
        if nav_key == "dashboard":
            render_owner_dashboard()
        elif nav_key == "pos":
            render_pos_billing()
        elif nav_key == "products":
            render_product_management()
        elif nav_key == "inventory":
            render_inventory_management()
        elif nav_key == "sales":
            render_sales_management()
        elif nav_key == "pnl":
            render_profit_loss()
        elif nav_key == "expenses":
            render_expense_management()
        elif nav_key == "performance":
            render_product_performance()
        elif nav_key == "reports":
            render_reports()
        elif nav_key == "powerbi":
            render_powerbi_guide()

    elif user_role == "customer":
        render_customer_purchase_history()


if __name__ == "__main__":
    main()

