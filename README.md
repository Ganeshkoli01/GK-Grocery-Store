# GK GROCERY STORE – SMART BUSINESS ANALYTICS
> **"Smart Shopping. Smarter Business Decisions."**

A complete, modern, commercial-grade Grocery Store Management and Business Analytics Web Application built using **Python, Streamlit, SQLite, Pandas, NumPy, Plotly, ReportLab, and OpenPyXL**.

Developed as an intermediate-level Data Analytics & Business Intelligence portfolio project demonstrating end-to-end full-stack capabilities: database modeling, atomic POS transactions, financial accounting (COGS & Net Profit), inventory health tracking, interactive data visualizations, multi-tab Excel reporting, and Microsoft Power BI Star-Schema integration.

---

## 🌟 Key Features Overview

### 1. Dual-Role Architecture & Security
- **Owner (Admin) Mode:** Full managerial control over product catalog, wholesale cost prices, selling rates, stock replenishment, operating overhead expenses, profit & loss accounting, and business intelligence dashboards.
- **Customer Shopping Mode:** Clean, isolated shopping interface allowing customers to search, filter by category, view selling prices, manage shopping carts, place orders, and download official PDF tax invoices.
- **Strict Role Isolation:** Product cost prices, supplier details, gross margins, and profit metrics are cryptographically gated in the backend and never exposed to customer interfaces.
- **Security:** Passwords salted and hashed with PBKDF2-HMAC-SHA256. Session-state authentication.

### 2. POS Counter Billing & Customer Checkout
- **Atomic Database Transactions:** Built using database-level `BEGIN`, `COMMIT`, and `ROLLBACK` blocks. If stock validation fails or network disconnects, stock is never deducted and database integrity is preserved.
- **Real-Time Stock Checks:** Prevents negative inventory and automatically warns customers if quantities exceed available stock.
- **Historical Accuracy:** Every completed order preserves the **exact historical cost price** and selling price in `sale_items`. Subsequent cost price changes never distort past profit reports!
- **Instant Tax Invoices (PDF):** Generates official invoices with store branding, GSTIN, invoice ID (`GK-YYYYMMDD-XXXX`), line-item breakdown, discount calculations, and thank-you notes.

### 3. Financial Profit & Loss Statement (P&L)
Follows standard retail commercial accounting principles:
- **Gross Revenue** = $\sum (\text{Selling Price} \times \text{Quantity Sold})$
- **Cost of Goods Sold (COGS)** = $\sum (\text{Historical Cost Price} \times \text{Quantity Sold})$
- **Gross Profit** = $\text{Revenue} - \text{COGS}$
- **Gross Profit Margin (%)** = $(\frac{\text{Gross Profit}}{\text{Revenue}}) \times 100$
- **Operating Expenses** = Shop Rent + Electricity + Staff Salaries + Logistics + Packaging
- **Net Profit** = $\text{Gross Profit} - \text{Operating Expenses}$
- **Net Margin (%)** = $(\frac{\text{Net Profit}}{\text{Revenue}}) \times 100$
- Interactive Financial Waterfall chart visualizing cash flow from turnover down to net bottom-line profit.

### 4. Inventory Health & Restocking Matrix
- Real-time stock status badges: **Healthy**, **Low Stock**, and **Out of Stock**.
- Capital Valuation: Live calculation of inventory tied up at wholesale purchase cost vs. projected retail valuation.
- Restocking Recommendations: Automated restocking matrix combining minimum safety stock thresholds and 30-day sales run-rates with suggested reorder quantities.
- Batch Inward stock recorder: Fast replenishment with supplier invoice references.

### 5. Interactive Business Analytics & Visualizations
Powered by Plotly with a cohesive commercial grocery green theme:
1. Daily Sales Trend Line Chart (Revenue & Gross Profit)
2. Weekly Sales Revenue Bar Chart
3. Monthly Revenue Trajectory Line Chart
4. Annual Sales Performance Bar Chart
5. Revenue vs. Gross Profit Grouped Bar Comparison
6. Category-wise Sales Donut Chart
7. Top 10 Best-Selling Products Horizontal Bar Chart
8. Slow-Moving / Dead Stock Products Velocity Bar Chart
9. Product-wise Gross Profit Contribution Chart
10. Inventory Stock Level vs. Minimum Threshold Comparison
11. Monthly Profit & Loss Multi-Metric Grouped Chart
12. Pricing Spread (Cost Price vs. Selling Price) Comparison

### 6. Excel & Power BI Integration
- **Multi-Sheet Excel Master Workbook:** Generates a 6-tab formatted `.xlsx` workbook using OpenPyXL (`Sales Report`, `Product Inventory`, `Product Performance`, `Daily PnL`, `Expenses`, `Monthly Summary`) with currency formatting, headers, and column autosizing.
- **Power BI Star-Schema Zip Bundle:** 1-click generation of normalized CSV files (`fact_sales.csv`, `fact_sale_items.csv`, `fact_expenses.csv`, `dim_products.csv`, `dim_customers.csv`, `dim_calendar.csv`).
- Comprehensive Power BI guide with DAX formulas (`powerbi/powerbi_guide.md`).

---

## 🛠️ Technology Stack

| Layer | Technologies |
|---|---|
| **Frontend & UI/UX** | Python 3.12, Streamlit, Custom Responsive CSS3, SVG/PNG Graphic Assets |
| **Data Analytics** | Pandas 2.0+, NumPy |
| **Database** | SQLite3 (with WAL mode & foreign keys), convertible to MySQL |
| **Data Visualizations** | Plotly Express & Plotly Graph Objects |
| **Invoice Engine** | ReportLab (A4 vector PDF generation) |
| **Spreadsheet Engine** | OpenPyXL |
| **Business Intelligence**| Microsoft Power BI (Star Schema + DAX) |

---

## 📁 Project Architecture

```
d:\GK GROCERY STORE – SMART MANAGEMENT & BUSINESS ANALYTICS SYSTEM\
│
├── app.py                      # Main application entry point & page router
├── config.py                   # Global constants, paths, categories, theme palette
├── requirements.txt            # Python dependencies
├── README.md                   # Complete documentation
│
├── database/                   # Database subsystem
│   ├── connection.py           # Abstraction layer with connection pooling & transactions
│   ├── schema.sql              # ANSI SQL schema & performance indexes
│   └── db_setup.py             # Schema builder & 60-day sample data generator
│
├── modules/                    # Application feature modules
│   ├── authentication.py       # Authentication, PBKDF2 hashing & session states
│   ├── owner_dashboard.py      # Executive KPI summary & date-filtered charts
│   ├── customer_dashboard.py   # Customer shopping storefront, cart & history
│   ├── product_management.py   # Product CRUD & live unit margin calculator
│   ├── inventory_management.py # Stock health, capital valuation & inward batches
│   ├── billing.py              # Store counter POS checkout terminal
│   ├── sales_management.py     # Transaction audit ledger & PDF reprint
│   ├── profit_loss.py          # Financial P&L statement & waterfall flow
│   ├── expense_management.py   # Overhead logs (rent, electricity, salaries)
│   ├── product_performance.py  # Best-sellers, slow-moving items & reorder matrix
│   ├── reports.py              # Multi-period analytics, Excel & Power BI exports
│   └── powerbi_view.py         # In-app Power BI architecture viewer
│
├── analytics/                  # Core analytical calculation engines
│   ├── sales_analysis.py       # Daily/weekly/monthly/yearly aggregations
│   ├── profit_analysis.py      # Historical COGS, gross & net margins
│   ├── inventory_analysis.py   # Stock valuation & velocity calculations
│   └── visualizations.py       # Plotly chart factories for all 12 charts
│
├── utils/                      # Helper utilities
│   ├── helpers.py              # PBKDF2 hashing, Indian currency formatting, dates
│   ├── invoice_generator.py    # ReportLab PDF invoice generator
│   └── excel_export.py         # Multi-sheet OpenPyXL formatted exporter
│
├── assets/                     # Graphics and styling
│   ├── logo.png                # Brand logo
│   └── styles.py               # Custom commercial CSS theme
│
├── powerbi/                    # Business intelligence documentation
│   └── powerbi_guide.md        # Star schema, table relationships & DAX measures
│
└── exports/                    # Runtime report output directory
```

---

## 🚀 Quick Start & Installation

### 1. Clone or Open Workspace
Open a terminal in the project directory:
```bash
cd "d:\GK GROCERY STORE – SMART MANAGEMENT & BUSINESS ANALYTICS SYSTEM"
```

### 2. Install Required Dependencies
```bash
pip install -r requirements.txt
```

### 3. Initialize Database & Seed Demonstration Data
```bash
python database/db_setup.py
```
*(The app also auto-initializes and seeds data on first launch if empty!)*

### 4. Run the Streamlit Application
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

---

## 🔑 Default Login Credentials

| Role | Username | Password | Purpose |
|---|---|---|---|
| **Store Owner (Admin)** | `ganesh_01` | `Ganeshk@825` | Full store management, P&L, inventory, analytics, pricing |
| **Customer** | `customer` | `customer123` | Product browsing, shopping cart, checkout, invoice downloads |

> **Note:** For quick testing and evaluation during interviews, the login page also includes a **"⚡ One-Click Demo Access"** tab that lets you log in with either role in a single click!

---

## 🧪 Testing Verification Checklist

The application includes end-to-end tests for all critical workflows:

1. **Owner Authentication:** Verify owner logs in and can access management pages.
2. **Customer Security Isolation:** Customer account cannot view owner analytics, wholesale cost prices, or profit margins.
3. **Product Addition:** Add a new product and verify real-time unit margin and margin % calculations.
4. **Inventory Valuation:** Check that adding inward stock automatically adjusts total capital valuation.
5. **Customer Shopping & Cart:** Add items, modify quantities, and observe dynamic subtotal updates.
6. **Atomic Transaction Checkout:** Confirm order, verify stock decreases in `products`, record appears in `sales`, line items appear in `sale_items`, and PDF receipt downloads.
7. **Negative Stock Protection:** Verify orders exceeding available inventory are rejected and roll back safely.
8. **Financial P&L Audit:** Add an expense (e.g. ₹5,000 electricity) and verify Net Profit updates immediately.
9. **Plotly Charts:** Filter across different timeframes (Today, Last 7 Days, Last 30 Days, This Year) and verify all charts update dynamically.
10. **Excel Workbook:** Click "Build & Prepare Excel Workbook" and verify all 6 formatted sheets are generated.
11. **Power BI Export:** Generate Power BI Zip bundle and verify all 6 CSV files are included.
12. **Sample Data Toggle:** Safely remove sample data or re-seed without affecting genuine store sales.

---

## 📄 License & Credits
Developed with ❤️ by **Ganesh Koli** for GK Grocery Store Smart Management & Business Analytics.
Designed for commercial operations and professional Data Analyst portfolio demonstrations.

