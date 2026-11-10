# Power BI Integration & Modeling Guide
## GK GROCERY STORE – SMART BUSINESS ANALYTICS

This guide walks data analysts and business owners through connecting Microsoft Power BI to GK Grocery Store datasets, creating a Star Schema data model, writing key DAX business measures, and building an executive-ready business intelligence dashboard.

---

## 1. Connecting Power BI to the Application Data

You have two simple and robust options for loading data into Power BI:

### Option A: Using Pre-Packaged Power BI CSV Exports (Recommended)
1. In the **GK Grocery Store Web App**, navigate to **Power BI Integration** from the Owner sidebar.
2. Click **"Generate & Download Power BI Data Bundle (.zip / CSVs)"**.
3. Open **Power BI Desktop**.
4. Click **Get Data** > **Text/CSV**.
5. Import the exported files:
   - `fact_sales.csv`
   - `fact_sale_items.csv`
   - `fact_expenses.csv`
   - `dim_products.csv`
   - `dim_customers.csv`
   - `dim_calendar.csv`

### Option B: Direct SQLite Database Connection (ODBC)
1. Install the free **SQLite ODBC Driver** (from `http://www.ch-werner.de/sqliteodbc/`).
2. Open Windows **ODBC Data Source Administrator (64-bit)**.
3. Under *System DSN*, click **Add** and select **SQLite3 ODBC Driver**.
4. Name the DSN `GK_Grocery_Store_DB` and browse to `database/gk_grocery_store.db`.
5. In Power BI Desktop: Click **Get Data** > **ODBC** > select `GK_Grocery_Store_DB`.

---

## 2. Star Schema Data Model Architecture

Arrange the tables in Power BI **Model View** using this recommended Star Schema:

```
                  ┌──────────────────────┐
                  │     dim_calendar     │
                  │   (Date Dimension)   │
                  └──────────┬───────────┘
                             │
            ┌────────────────┴────────────────┐
            │ 1:Many                          │ 1:Many
            ▼                                 ▼
┌─────────────────────────┐       ┌─────────────────────────┐
│       fact_sales        │       │      fact_expenses      │
│ (Transactions & Totals) │       │   (Operating Costs)     │
└───────────┬─────────────┘       └─────────────────────────┘
            │ 1:Many
            ▼
┌─────────────────────────┐
│     fact_sale_items     │
│ (Line Items, Cost, Rev) │
└───────────┬─────────────┘
            │ Many:1
            ▼
┌─────────────────────────┐
│      dim_products       │
│  (Catalog & Categories) │
└─────────────────────────┘
```

### Table Relationships:
1. `dim_calendar[Date]` ─── (1:*) ───> `fact_sales[sale_date]`
2. `dim_calendar[Date]` ─── (1:*) ───> `fact_expenses[expense_date]`
3. `fact_sales[id]` ─── (1:*) ───> `fact_sale_items[sale_id]`
4. `dim_products[id]` ─── (1:*) ───> `fact_sale_items[product_id]`
5. `dim_customers[id]` ─── (1:*) ───> `fact_sales[customer_id]`

---

## 3. Essential DAX Business Measures

Create a dedicated measures table called `_KeyMeasures` in Power BI and paste the following DAX calculations:

### 1. Total Revenue
```dax
Total Revenue = SUM(fact_sales[grand_total])
```

### 2. Cost of Goods Sold (COGS)
```dax
Total COGS = SUMX(
    fact_sale_items,
    fact_sale_items[cost_price] * fact_sale_items[quantity]
)
```

### 3. Gross Profit
```dax
Gross Profit = [Total Revenue] - [Total COGS]
```

### 4. Gross Profit Margin %
```dax
Gross Margin % = DIVIDE([Gross Profit], [Total Revenue], 0)
```

### 5. Operating Expenses
```dax
Total Operating Expenses = SUM(fact_expenses[amount])
```

### 6. Net Profit
```dax
Net Profit = [Gross Profit] - [Total Operating Expenses]
```

### 7. Net Profit Margin %
```dax
Net Margin % = DIVIDE([Net Profit], [Total Revenue], 0)
```

### 8. Total Orders
```dax
Total Orders = DISTINCTCOUNT(fact_sales[id])
```

### 9. Average Order Value (AOV)
```dax
Average Order Value = DIVIDE([Total Revenue], [Total Orders], 0)
```

### 10. Month-over-Month Revenue Growth %
```dax
MoM Revenue Growth % = 
VAR CurrentMonthRev = [Total Revenue]
VAR PreviousMonthRev = CALCULATE([Total Revenue], DATEADD(dim_calendar[Date], -1, MONTH))
RETURN
    DIVIDE(CurrentMonthRev - PreviousMonthRev, PreviousMonthRev, 0)
```

---

## 4. Recommended Power BI Dashboard Layout

Design a 2-page report with a clean grocery green visual palette (`#14532D`, `#22C55E`, `#F59E0B`, `#F8FAFC`):

### Page 1: Executive Sales & Profitability Overview
- **Top Row KPI Cards:** Total Revenue, Gross Profit, Total Expenses, Net Profit, Net Margin %, Total Orders.
- **Top Slicers:** Date Range (Calendar), Category, Payment Method.
- **Main Visual (Left):** Line & Clustered Column Chart (Columns: Revenue & COGS; Line: Net Profit).
- **Secondary Visual (Right):** Donut Chart of Revenue by Category.
- **Bottom Left:** Top 10 Best-Selling Products by Revenue (Bar Chart).
- **Bottom Right:** Expenses breakdown by Category (Tree Map or Horizontal Bar).

### Page 2: Inventory Health & Restocking Action Matrix
- **Top KPI Cards:** Total Inventory Valuation (At Cost), Total Retail Valuation, Low Stock Alerts Count, Out of Stock Count.
- **Table Visual:** Products Requiring Restock (Columns: Product Name, Category, Available Stock, Min Threshold, Sold Last 30 Days, Recommended Order Qty).
- **Scatter Plot:** Product Sales Velocity vs. Current Stock Level (to quickly spot dead stock vs out-of-stock risks).

---

## 5. Automated Refresh
To keep your Power BI report synchronized:
- If using SQLite/MySQL directly: Configure Power BI Scheduled Refresh via the **Power BI On-Premises Data Gateway (Personal Mode)**.
- If using CSV exports: Simply re-export fresh CSVs from the Streamlit app into your designated folder and click **Refresh** in Power BI Desktop.

