"""
GK GROCERY STORE – Authentication & Role Management Module
Manages secure authentication, password hashing, session states, and role separation.
"""

import streamlit as st
from database.connection import fetch_one, execute_insert
from utils.helpers import hash_password, verify_password
from utils.translations import LANGUAGES, t, get_current_language
from config import APP_NAME, APP_TAGLINE, DEFAULT_ADMIN, DEFAULT_CUSTOMER


def init_session_state():
    """Initializes user session state variables if not already present."""
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "user_role" not in st.session_state:
        st.session_state.user_role = None
    if "user_id" not in st.session_state:
        st.session_state.user_id = None
    if "username" not in st.session_state:
        st.session_state.username = None
    if "full_name" not in st.session_state:
        st.session_state.full_name = None
    if "cart" not in st.session_state:
        st.session_state.cart = {}  # {product_id: {"name": ..., "price": ..., "unit": ..., "qty": ...}}


def login_user(username_attempt: str, password_attempt: str) -> bool:
    """Verifies credentials and populates session state."""
    user = fetch_one(
        "SELECT id, username, password_hash, salt, full_name, role FROM users WHERE username = ?",
        (username_attempt.strip(),)
    )
    if not user:
        return False

    if verify_password(password_attempt, user["password_hash"], user["salt"]):
        st.session_state.authenticated = True
        st.session_state.user_role = user["role"]
        st.session_state.user_id = user["id"]
        st.session_state.username = user["username"]
        st.session_state.full_name = user["full_name"]
        return True
    return False


def logout_user():
    """Clears authentication session state."""
    st.session_state.authenticated = False
    st.session_state.user_role = None
    st.session_state.user_id = None
    st.session_state.username = None
    st.session_state.full_name = None
    st.session_state.cart = {}
    st.rerun()


def register_customer(username: str, password: str, full_name: str, phone: str, email: str, address: str) -> tuple[bool, str]:
    """Registers a new customer account securely."""
    # Check if username exists
    existing = fetch_one("SELECT id FROM users WHERE username = ?", (username.strip(),))
    if existing:
        return False, "Username already taken. Please choose another."

    pwd_hash, salt = hash_password(password)
    try:
        user_id = execute_insert(
            """
            INSERT INTO users (username, password_hash, salt, full_name, email, phone, role)
            VALUES (?, ?, ?, ?, ?, ?, 'customer')
            """,
            (username.strip(), pwd_hash, salt, full_name.strip(), email.strip(), phone.strip())
        )

        execute_insert(
            """
            INSERT INTO customers (user_id, full_name, email, phone, address)
            VALUES (?, ?, ?, ?, ?)
            """,
            (user_id, full_name.strip(), email.strip(), phone.strip(), address.strip())
        )
        return True, "Account created successfully! You can now sign in."
    except Exception as e:
        return False, f"Registration error: {str(e)}"


def render_auth_page():
    """Displays modern dual-role authentication interface."""
    init_session_state()

    c_top1, c_top2 = st.columns([3, 1])
    with c_top2:
        lang_keys = list(LANGUAGES.keys())
        c_idx = lang_keys.index(get_current_language())
        auth_lang = st.selectbox(
            "Language",
            lang_keys,
            format_func=lambda k: LANGUAGES[k],
            index=c_idx,
            key="auth_lang_select"
        )
        if auth_lang != st.session_state.get("language"):
            st.session_state.language = auth_lang
            st.rerun()

    st.markdown(
        f"""
        <div style="text-align: center; margin-top: 10px; margin-bottom: 25px;">
            <div style="font-size: 38px;">🛒</div>
            <h1 style="color: #14532D; margin: 0; font-size: 32px; font-weight: 800;">{t('app_title')}</h1>
            <p style="color: #64748B; font-size: 15px; margin-top: 4px;">{t('app_tagline')}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        tab_login, tab_register, tab_demo = st.tabs(["🔐 Sign In", "📝 Customer Registration", "⚡ One-Click Demo Access"])

        with tab_login:
            st.markdown("##### Log in to your account")
            with st.form("login_form"):
                username_input = st.text_input("Username", placeholder="e.g. admin or customer")
                password_input = st.text_input("Password", type="password", placeholder="Enter your password")
                submitted = st.form_submit_button("Sign In", use_container_width=True, type="primary")

                if submitted:
                    if not username_input or not password_input:
                        st.error("Please enter both username and password.")
                    else:
                        success = login_user(username_input, password_input)
                        if success:
                            st.success(f"Welcome back, {st.session_state.full_name}!")
                            st.rerun()
                        else:
                            st.error("Invalid username or password. Please try again.")

        with tab_register:
            st.markdown("##### New Customer Account")
            with st.form("register_form"):
                reg_name = st.text_input("Full Name *", placeholder="e.g. Vikram Sharma")
                reg_phone = st.text_input("Mobile Number *", placeholder="e.g. +91 98765 43210")
                reg_email = st.text_input("Email Address", placeholder="e.g. vikram@example.com")
                reg_user = st.text_input("Choose Username *", placeholder="e.g. vikram24")
                reg_pass = st.text_input("Choose Password *", type="password", placeholder="Minimum 6 characters")
                reg_address = st.text_area("Delivery / Billing Address", placeholder="Apartment, Street, City")

                reg_submitted = st.form_submit_button("Create Customer Account", use_container_width=True, type="primary")

                if reg_submitted:
                    if not reg_name or not reg_phone or not reg_user or not reg_pass:
                        st.error("Please fill in all mandatory fields (*).")
                    elif len(reg_pass) < 4:
                        st.error("Password must be at least 4 characters.")
                    else:
                        ok, msg = register_customer(reg_user, reg_pass, reg_name, reg_phone, reg_email, reg_address)
                        if ok:
                            st.success(msg)
                        else:
                            st.error(msg)

        with tab_demo:
            st.markdown("##### Instant Testing Credentials")
            st.info("For evaluation and portfolio presentation, switch between roles instantly:")

            c_demo1, c_demo2 = st.columns(2)
            with c_demo1:
                if st.button("🔑 Login as Owner (Admin)", use_container_width=True, type="primary"):
                    login_user(DEFAULT_ADMIN["username"], DEFAULT_ADMIN["password"])
                    st.rerun()
                st.caption(f"Username: `{DEFAULT_ADMIN['username']}` | Pass: `{DEFAULT_ADMIN['password']}`")

            with c_demo2:
                if st.button("📜 Login as Customer (View Receipts)", use_container_width=True):
                    login_user(DEFAULT_CUSTOMER["username"], DEFAULT_CUSTOMER["password"])
                    st.rerun()
                st.caption(f"Username: `{DEFAULT_CUSTOMER['username']}` | Pass: `{DEFAULT_CUSTOMER['password']}`")

