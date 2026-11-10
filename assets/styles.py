"""
GK GROCERY STORE – Modern Commercial UI/UX Styling
Custom CSS designed for an elevated, clean, enterprise-ready look.
Guarantees high-contrast readability in both light and dark system modes.
"""

def get_custom_css() -> str:
    return """
    <style>
    /* Google Fonts & Base Typography */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        color: #0F172A !important;
    }

    /* Main Container */
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2.5rem;
        max-width: 96%;
    }

    /* ---------------------------------------------------- */
    /* SIDEBAR NAVIGATION & TEXT CONTRAST (CRITICAL FIX)    */
    /* ---------------------------------------------------- */
    [data-testid="stSidebar"] {
        background-color: #F8FAFC !important;
        border-right: 1px solid #E2E8F0 !important;
    }

    /* General Sidebar Typography */
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] div[data-testid="stMarkdownContainer"] {
        color: #0F172A !important;
    }

    /* Radio Group Title ("Navigation Menu") */
    [data-testid="stSidebar"] [data-testid="stRadio"] > label,
    [data-testid="stSidebar"] [data-testid="stRadio"] label p,
    [data-testid="stSidebar"] [data-testid="stRadio"] .st-emotion-cache-1qg05tj {
        font-size: 13px !important;
        font-weight: 700 !important;
        color: #0F172A !important;
        text-transform: uppercase !important;
        letter-spacing: 0.6px !important;
        margin-bottom: 8px !important;
        display: block !important;
    }

    /* Individual Radio Navigation Options */
    [data-testid="stSidebar"] [data-testid="stRadio"] [role="radiogroup"] label,
    [data-testid="stSidebar"] [data-baseweb="radio"] {
        background-color: transparent !important;
        padding: 6px 10px !important;
        border-radius: 8px !important;
        margin-bottom: 4px !important;
        transition: all 0.15s ease !important;
        cursor: pointer !important;
        display: flex !important;
        align-items: center !important;
    }

    [data-testid="stSidebar"] [data-testid="stRadio"] [role="radiogroup"] label:hover,
    [data-testid="stSidebar"] [data-baseweb="radio"]:hover {
        background-color: #E2E8F0 !important;
    }

    /* Radio Button Text Labels (MUST BE CRISP DARK SLATE) */
    [data-testid="stSidebar"] [data-testid="stRadio"] [role="radiogroup"] label span,
    [data-testid="stSidebar"] [data-testid="stRadio"] [role="radiogroup"] label p,
    [data-testid="stSidebar"] [data-testid="stRadio"] [data-testid="stMarkdownContainer"] p,
    [data-testid="stSidebar"] [data-testid="stRadio"] [data-testid="stMarkdownContainer"] span,
    [data-testid="stSidebar"] [data-baseweb="radio"] div,
    [data-testid="stSidebar"] [data-baseweb="radio"] p,
    [data-testid="stSidebar"] [data-baseweb="radio"] span {
        color: #0F172A !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        line-height: 1.4 !important;
        text-shadow: none !important;
        opacity: 1 !important;
    }

    /* Sidebar Brand Header (Must stay crisp white on dark green) */
    .sidebar-brand-box {
        padding: 18px 14px;
        background: linear-gradient(135deg, #14532D 0%, #166534 100%) !important;
        color: #FFFFFF !important;
        border-radius: 12px;
        margin-bottom: 18px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(20, 83, 45, 0.2);
    }

    .sidebar-brand-box * {
        color: #FFFFFF !important;
    }

    /* User Role Badge in Sidebar */
    .sidebar-user-pill {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: #ECFDF5 !important;
        border: 1px solid #A7F3D0 !important;
        padding: 10px 14px;
        border-radius: 10px;
        font-size: 12px;
        font-weight: 700;
        margin-bottom: 16px;
    }

    .sidebar-user-pill span {
        color: #065F46 !important;
    }

    /* ---------------------------------------------------- */
    /* TOP BRAND HEADER                                     */
    /* ---------------------------------------------------- */
    .brand-header-box {
        background: linear-gradient(135deg, #14532D 0%, #166534 50%, #15803D 100%);
        border-radius: 14px;
        padding: 20px 28px;
        color: white;
        margin-bottom: 22px;
        box-shadow: 0 8px 20px -4px rgba(20, 83, 45, 0.25);
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
        letter-spacing: -0.5px;
        margin: 0;
        color: #FFFFFF !important;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .brand-subtitle {
        font-size: 13px;
        font-weight: 400;
        color: #BBF7D0 !important;
        margin-top: 4px;
    }

    /* ---------------------------------------------------- */
    /* KPI SUMMARY CARDS                                    */
    /* ---------------------------------------------------- */
    .kpi-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
        gap: 16px;
        margin-bottom: 22px;
    }

    .kpi-card {
        background: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 12px;
        padding: 18px 20px;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.04);
        transition: transform 0.15s ease, box-shadow 0.15s ease;
        position: relative;
        overflow: hidden;
    }

    .kpi-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.07);
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
        font-size: 12px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.6px;
        color: #475569 !important;
        margin-bottom: 6px;
    }

    .kpi-value {
        font-size: 24px;
        font-weight: 800;
        color: #0F172A !important;
        line-height: 1.2;
    }

    .kpi-subtext {
        font-size: 12px;
        font-weight: 600;
        color: #15803D !important;
        margin-top: 4px;
    }

    .kpi-subtext.sub-danger {
        color: #DC2626 !important;
    }

    /* ---------------------------------------------------- */
    /* BADGES                                               */
    /* ---------------------------------------------------- */
    .badge {
        display: inline-block;
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

    /* ---------------------------------------------------- */
    /* PRODUCT CARDS (CUSTOMER SHOPPING)                    */
    /* ---------------------------------------------------- */
    .product-card {
        background: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 12px;
        padding: 16px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.03);
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        height: 100%;
        transition: all 0.2s ease;
    }

    .product-card:hover {
        border-color: #86EFAC !important;
        box-shadow: 0 8px 18px rgba(34, 197, 94, 0.12);
        transform: translateY(-2px);
    }

    .product-card-category {
        font-size: 11px;
        font-weight: 700;
        color: #15803D !important;
        text-transform: uppercase;
        margin-bottom: 4px;
    }

    .product-card-title {
        font-size: 15px;
        font-weight: 700;
        color: #0F172A !important;
        margin-bottom: 6px;
        line-height: 1.3;
        min-height: 40px;
    }

    .product-card-price {
        font-size: 19px;
        font-weight: 800;
        color: #14532D !important;
    }

    .product-card-unit {
        font-size: 12px;
        font-weight: 600;
        color: #64748B !important;
    }

    /* ---------------------------------------------------- */
    /* BUTTONS & FORM ELEMENTS                              */
    /* ---------------------------------------------------- */
    .stButton > button {
        border-radius: 8px;
        font-weight: 700;
        transition: all 0.15s ease;
    }

    /* Input Labels & Help Text */
    label[data-testid="stWidgetLabel"] p,
    label[data-testid="stWidgetLabel"] span {
        color: #0F172A !important;
        font-weight: 600 !important;
    }

    /* Clean Streamlit Dataframes & Tables */
    [data-testid="stDataFrame"] {
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        overflow: hidden;
    }

    /* ---------------------------------------------------- */
    /* CALLOUT BOXES                                        */
    /* ---------------------------------------------------- */
    .info-callout {
        background: #F0FDF4 !important;
        border-left: 4px solid #22C55E !important;
        padding: 12px 16px;
        border-radius: 6px;
        font-size: 13px;
        color: #14532D !important;
        margin: 12px 0;
    }

    .info-callout * {
        color: #14532D !important;
    }

    .warning-callout {
        background: #FFFBEB !important;
        border-left: 4px solid #F59E0B !important;
        padding: 12px 16px;
        border-radius: 6px;
        font-size: 13px;
        color: #92400E !important;
        margin: 12px 0;
    }

    .warning-callout * {
        color: #92400E !important;
    }

    /* App-like clean presentation */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """
