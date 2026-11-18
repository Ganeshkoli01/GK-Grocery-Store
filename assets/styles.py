"""
GK GROCERY STORE – Modern Commercial UI/UX Styling
Custom CSS designed for an elevated, clean, minimalist, enterprise-grade look.
Inspired by modern SaaS designs (Stripe, Linear, Shopify POS).
Guarantees high-contrast readability in both light and dark system modes.
"""

_CACHED_CUSTOM_CSS = None

def get_custom_css() -> str:
    global _CACHED_CUSTOM_CSS
    if _CACHED_CUSTOM_CSS is not None:
        return _CACHED_CUSTOM_CSS

    _CACHED_CUSTOM_CSS = """
    <style>
    /* ==================================================== */
    /* 1. MODERN HIGH-PERFORMANCE TYPOGRAPHY & SMOOTH BASE  */
    /* ==================================================== */
    html, body, [class*="css"], [data-testid="stAppViewContainer"] {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Inter", "Helvetica Neue", Arial, sans-serif;
        color: #0F172A !important;
        background-color: #F8FAFC !important;
    }

    /* Main Content Container */
    .block-container {
        padding-top: 1.25rem !important;
        padding-bottom: 2.5rem !important;
        max-width: 95% !important;
    }

    /* ==================================================== */
    /* 2. SLEEK MODERN SIDEBAR NAVIGATION                   */
    /* ==================================================== */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #E2E8F0 !important;
        box-shadow: 1px 0 6px rgba(0, 0, 0, 0.02) !important;
    }

    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] div[data-testid="stMarkdownContainer"] {
        color: #1E293B !important;
    }

    /* Sidebar Brand Card */
    .sidebar-brand-box {
        padding: 18px 14px;
        background: linear-gradient(135deg, #14532D 0%, #166534 100%) !important;
        color: #FFFFFF !important;
        border-radius: 14px;
        margin-bottom: 16px;
        text-align: center;
        box-shadow: 0 4px 14px rgba(20, 83, 45, 0.22);
    }

    .sidebar-brand-box * {
        color: #FFFFFF !important;
    }

    /* User Profile Pill */
    .sidebar-user-pill {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: #F0FDF4 !important;
        border: 1px solid #BBF7D0 !important;
        padding: 10px 14px;
        border-radius: 12px;
        font-size: 13px;
        font-weight: 700;
        margin-bottom: 16px;
    }

    .sidebar-user-pill span {
        color: #166534 !important;
    }

    /* Radio Navigation Menu Container */
    [data-testid="stSidebar"] [data-testid="stRadio"] > label {
        font-size: 11px !important;
        font-weight: 700 !important;
        color: #64748B !important;
        text-transform: uppercase !important;
        letter-spacing: 0.8px !important;
        margin-bottom: 8px !important;
        display: block !important;
    }

    /* Navigation Radio Items (Pill-Style Hover & Selection) */
    [data-testid="stSidebar"] [data-testid="stRadio"] [role="radiogroup"] label,
    [data-testid="stSidebar"] [data-baseweb="radio"] {
        background-color: transparent !important;
        padding: 8px 12px !important;
        border-radius: 10px !important;
        margin-bottom: 4px !important;
        transition: all 0.15s ease !important;
        cursor: pointer !important;
        display: flex !important;
        align-items: center !important;
    }

    [data-testid="stSidebar"] [data-testid="stRadio"] [role="radiogroup"] label:hover,
    [data-testid="stSidebar"] [data-baseweb="radio"]:hover {
        background-color: #F1F5F9 !important;
    }

    [data-testid="stSidebar"] [data-testid="stRadio"] [role="radiogroup"] label span,
    [data-testid="stSidebar"] [data-testid="stRadio"] [role="radiogroup"] label p,
    [data-testid="stSidebar"] [data-testid="stRadio"] [data-testid="stMarkdownContainer"] p,
    [data-testid="stSidebar"] [data-testid="stRadio"] [data-testid="stMarkdownContainer"] span,
    [data-testid="stSidebar"] [data-baseweb="radio"] div,
    [data-testid="stSidebar"] [data-baseweb="radio"] p,
    [data-testid="stSidebar"] [data-baseweb="radio"] span {
        color: #1E293B !important;
        font-weight: 600 !important;
        font-size: 13.5px !important;
        line-height: 1.4 !important;
        text-shadow: none !important;
    }

    /* ==================================================== */
    /* 3. TOP BRAND HEADER BANNER                           */
    /* ==================================================== */
    .brand-header-box {
        background: linear-gradient(135deg, #14532D 0%, #166534 60%, #15803D 100%);
        border-radius: 16px;
        padding: 22px 28px;
        color: #FFFFFF !important;
        margin-bottom: 24px;
        box-shadow: 0 8px 24px -6px rgba(20, 83, 45, 0.28);
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    .brand-header-box * {
        color: #FFFFFF !important;
    }

    .brand-title {
        font-size: 24px;
        font-weight: 800;
        letter-spacing: -0.4px;
        margin: 0;
        color: #FFFFFF !important;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .brand-subtitle {
        font-size: 13px;
        font-weight: 500;
        color: #DCFCE7 !important;
        margin-top: 4px;
        opacity: 0.95;
    }

    /* ==================================================== */
    /* 4. MINIMALIST & ATTRACTIVE KPI SUMMARY CARDS         */
    /* ==================================================== */
    .kpi-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(185px, 1fr));
        gap: 16px;
        margin-bottom: 24px;
    }

    .kpi-card {
        background: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 14px;
        padding: 18px 20px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05), 0 1px 2px rgba(0, 0, 0, 0.03);
        transition: transform 0.15s ease, box-shadow 0.15s ease, border-color 0.15s ease;
        position: relative;
        overflow: hidden;
    }

    .kpi-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.06);
        border-color: #CBD5E1 !important;
    }

    .kpi-card::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        background: #22C55E;
    }

    .kpi-card.kpi-primary::before { background: #14532D; }
    .kpi-card.kpi-secondary::before { background: #22C55E; }
    .kpi-card.kpi-accent::before { background: #F59E0B; }
    .kpi-card.kpi-danger::before { background: #EF4444; }
    .kpi-card.kpi-info::before { background: #0284C7; }

    .kpi-title {
        font-size: 11.5px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.6px;
        color: #64748B !important;
        margin-bottom: 6px;
    }

    .kpi-value {
        font-size: 26px;
        font-weight: 800;
        color: #0F172A !important;
        line-height: 1.2;
        letter-spacing: -0.5px;
    }

    .kpi-subtext {
        font-size: 12px;
        font-weight: 600;
        color: #166534 !important;
        margin-top: 4px;
    }

    .kpi-subtext.sub-danger {
        color: #DC2626 !important;
    }

    /* ==================================================== */
    /* 5. MODERN BADGES & PILLS                             */
    /* ==================================================== */
    .badge {
        display: inline-flex;
        align-items: center;
        padding: 4px 10px;
        border-radius: 9999px;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 0.3px;
    }

    .badge-success {
        background-color: #DCFCE7 !important;
        color: #15803D !important;
        border: 1px solid #86EFAC !important;
    }

    .badge-warning {
        background-color: #FEF3C7 !important;
        color: #B45309 !important;
        border: 1px solid #FDE68A !important;
    }

    .badge-danger {
        background-color: #FEE2E2 !important;
        color: #B91C1C !important;
        border: 1px solid #FCA5A5 !important;
    }

    .badge-info {
        background-color: #E0F2FE !important;
        color: #0369A1 !important;
        border: 1px solid #BAE6FD !important;
    }

    /* ==================================================== */
    /* 6. PRODUCT CARDS (CUSTOMER SHOPPING / POS GRID)      */
    /* ==================================================== */
    .product-card {
        background: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 14px;
        padding: 16px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        height: 100%;
        transition: all 0.2s ease;
    }

    .product-card:hover {
        border-color: #86EFAC !important;
        box-shadow: 0 10px 22px rgba(34, 197, 94, 0.12);
        transform: translateY(-2px);
    }

    .product-card-category {
        font-size: 11px;
        font-weight: 700;
        color: #15803D !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 4px;
    }

    .product-card-title {
        font-size: 15px;
        font-weight: 700;
        color: #0F172A !important;
        margin-bottom: 6px;
        line-height: 1.35;
        min-height: 40px;
    }

    .product-card-price {
        font-size: 20px;
        font-weight: 800;
        color: #14532D !important;
        letter-spacing: -0.3px;
    }

    .product-card-unit {
        font-size: 12px;
        font-weight: 600;
        color: #64748B !important;
    }

    /* ==================================================== */
    /* 7. MODERN BUTTONS & FORM INPUTS                      */
    /* ==================================================== */
    .stButton > button {
        border-radius: 10px !important;
        font-weight: 700 !important;
        font-size: 14px !important;
        padding: 8px 16px !important;
        transition: all 0.15s ease !important;
        border: 1px solid #CBD5E1 !important;
    }

    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #166534 0%, #15803D 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        box-shadow: 0 2px 8px rgba(22, 101, 52, 0.25) !important;
    }

    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, #14532D 0%, #166534 100%) !important;
        box-shadow: 0 4px 14px rgba(20, 83, 45, 0.35) !important;
        transform: translateY(-1px);
    }

    .stButton > button[kind="secondary"]:hover {
        background: #F1F5F9 !important;
        border-color: #94A3B8 !important;
    }

    /* Input Controls (Text, Select, Date, Number) */
    div[data-baseweb="input"],
    div[data-baseweb="select"] > div {
        border-radius: 10px !important;
        border: 1px solid #CBD5E1 !important;
        transition: border-color 0.15s ease, box-shadow 0.15s ease !important;
    }

    div[data-baseweb="input"]:focus-within,
    div[data-baseweb="select"] > div:focus-within {
        border-color: #22C55E !important;
        box-shadow: 0 0 0 3px rgba(34, 197, 94, 0.18) !important;
    }

    /* Input Labels */
    label[data-testid="stWidgetLabel"] p,
    label[data-testid="stWidgetLabel"] span {
        color: #1E293B !important;
        font-weight: 600 !important;
        font-size: 13.5px !important;
    }

    /* ==================================================== */
    /* 8. MODERN TABS STYLING                               */
    /* ==================================================== */
    div[data-testid="stTabs"] [data-baseweb="tab-list"] {
        gap: 8px !important;
        background-color: #F1F5F9 !important;
        padding: 5px !important;
        border-radius: 12px !important;
        border: 1px solid #E2E8F0 !important;
    }

    div[data-testid="stTabs"] [data-baseweb="tab"] {
        border-radius: 9px !important;
        font-weight: 600 !important;
        font-size: 13.5px !important;
        color: #64748B !important;
        padding: 8px 16px !important;
        border: none !important;
        background-color: transparent !important;
        transition: all 0.15s ease !important;
    }

    div[data-testid="stTabs"] [aria-selected="true"] {
        background-color: #FFFFFF !important;
        color: #14532D !important;
        font-weight: 700 !important;
        box-shadow: 0 1px 4px rgba(0, 0, 0, 0.08) !important;
    }

    /* Dataframes and Tables */
    [data-testid="stDataFrame"] {
        border: 1px solid #E2E8F0 !important;
        border-radius: 12px !important;
        overflow: hidden !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04) !important;
    }

    /* Clean Callouts */
    .info-callout {
        background: #F0FDF4 !important;
        border-left: 4px solid #22C55E !important;
        padding: 14px 18px;
        border-radius: 8px;
        font-size: 13.5px;
        color: #14532D !important;
        margin: 14px 0;
    }

    .warning-callout {
        background: #FFFBEB !important;
        border-left: 4px solid #F59E0B !important;
        padding: 14px 18px;
        border-radius: 8px;
        font-size: 13.5px;
        color: #92400E !important;
        margin: 14px 0;
    }

    /* Clean Header/Footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """
    return _CACHED_CUSTOM_CSS
