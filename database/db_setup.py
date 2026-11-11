"""
GK GROCERY STORE – Database Initialization & Sample Data Seeder
Creates schema, seeds default accounts, and generates 35+ realistic grocery products,
60 days of sales transactions, and realistic operating expenses.
"""

import os
import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import random
from datetime import datetime, date, timedelta
from database.connection import get_raw_connection, get_db_transaction, execute_query, execute_insert, fetch_one, fetch_all
from utils.helpers import hash_password, generate_invoice_number
from config import BASE_DIR, DEFAULT_ADMIN, DEFAULT_CUSTOMER, EXPENSE_CATEGORIES

SCHEMA_FILE = BASE_DIR / "database" / "schema.sql"

# Realistic Sample Products for Indian Grocery Store
SAMPLE_PRODUCTS = [
    # Rice and Grains
    {"name": "India Gate Basmati Rice", "category": "Rice and Grains", "cost_price": 95.0, "selling_price": 125.0, "stock": 80.0, "min_stock": 20.0, "unit": "kg"},
    {"name": "Kolam Rice Premium", "category": "Rice and Grains", "cost_price": 42.0, "selling_price": 55.0, "stock": 150.0, "min_stock": 30.0, "unit": "kg"},
    {"name": "Aashirvaad Sharbati Atta (Wheat Flour)", "category": "Rice and Grains", "cost_price": 38.0, "selling_price": 48.0, "stock": 120.0, "min_stock": 25.0, "unit": "kg"},
    {"name": "Organic Poha (Flattened Rice)", "category": "Rice and Grains", "cost_price": 40.0, "selling_price": 52.0, "stock": 45.0, "min_stock": 15.0, "unit": "kg"},
    {"name": "Roasted Sooji (Rava)", "category": "Rice and Grains", "cost_price": 34.0, "selling_price": 45.0, "stock": 35.0, "min_stock": 10.0, "unit": "kg"},

    # Pulses
    {"name": "Toor Dal (Arhar Dal)", "category": "Pulses", "cost_price": 135.0, "selling_price": 165.0, "stock": 60.0, "min_stock": 20.0, "unit": "kg"},
    {"name": "Moong Dal Washed", "category": "Pulses", "cost_price": 98.0, "selling_price": 120.0, "stock": 50.0, "min_stock": 15.0, "unit": "kg"},
    {"name": "Chana Dal Premium", "category": "Pulses", "cost_price": 72.0, "selling_price": 90.0, "stock": 65.0, "min_stock": 15.0, "unit": "kg"},
    {"name": "Urad Dal Black Split", "category": "Pulses", "cost_price": 110.0, "selling_price": 135.0, "stock": 40.0, "min_stock": 10.0, "unit": "kg"},
    {"name": "Kabuli Chana (Chickpeas)", "category": "Pulses", "cost_price": 115.0, "selling_price": 145.0, "stock": 35.0, "min_stock": 10.0, "unit": "kg"},

    # Cooking Oil
    {"name": "Fortune Sunflower Oil Pouch", "category": "Cooking Oil", "cost_price": 118.0, "selling_price": 140.0, "stock": 70.0, "min_stock": 20.0, "unit": "litre"},
    {"name": "Gemini Groundnut Oil", "category": "Cooking Oil", "cost_price": 155.0, "selling_price": 185.0, "stock": 45.0, "min_stock": 15.0, "unit": "litre"},
    {"name": "Amul Pure Cow Ghee Tin", "category": "Cooking Oil", "cost_price": 540.0, "selling_price": 620.0, "stock": 30.0, "min_stock": 8.0, "unit": "litre"},
    {"name": "Mustard Oil Kachi Ghani", "category": "Cooking Oil", "cost_price": 130.0, "selling_price": 155.0, "stock": 50.0, "min_stock": 15.0, "unit": "litre"},

    # Dairy Products
    {"name": "Amul Taaza Toned Milk", "category": "Dairy Products", "cost_price": 52.0, "selling_price": 56.0, "stock": 40.0, "min_stock": 15.0, "unit": "litre"},
    {"name": "Amul Salted Butter 500g", "category": "Dairy Products", "cost_price": 240.0, "selling_price": 275.0, "stock": 25.0, "min_stock": 8.0, "unit": "packet"},
    {"name": "Fresh Malai Paneer", "category": "Dairy Products", "cost_price": 310.0, "selling_price": 380.0, "stock": 18.0, "min_stock": 5.0, "unit": "kg"},
    {"name": "Amul Masti Dahi Cup", "category": "Dairy Products", "cost_price": 30.0, "selling_price": 35.0, "stock": 30.0, "min_stock": 10.0, "unit": "packet"},

    # Snacks
    {"name": "Haldiram's Bhujia Sev 400g", "category": "Snacks", "cost_price": 85.0, "selling_price": 110.0, "stock": 50.0, "min_stock": 15.0, "unit": "packet"},
    {"name": "Parle-G Gold Biscuits 1kg", "category": "Snacks", "cost_price": 95.0, "selling_price": 120.0, "stock": 60.0, "min_stock": 15.0, "unit": "packet"},
    {"name": "Lay's Classic Salted Chips", "category": "Snacks", "cost_price": 16.0, "selling_price": 20.0, "stock": 75.0, "min_stock": 20.0, "unit": "packet"},
    {"name": "Maggi 2-Minute Noodles 4-Pack", "category": "Snacks", "cost_price": 50.0, "selling_price": 60.0, "stock": 80.0, "min_stock": 25.0, "unit": "packet"},

    # Beverages
    {"name": "Tata Tea Gold 500g", "category": "Beverages", "cost_price": 240.0, "selling_price": 290.0, "stock": 35.0, "min_stock": 10.0, "unit": "packet"},
    {"name": "Bru Instant Coffee 200g", "category": "Beverages", "cost_price": 270.0, "selling_price": 330.0, "stock": 25.0, "min_stock": 8.0, "unit": "box"},
    {"name": "Bournvita Nutrition Drink 500g", "category": "Beverages", "cost_price": 210.0, "selling_price": 250.0, "stock": 22.0, "min_stock": 6.0, "unit": "box"},
    {"name": "Frooti Mango Drink 1.2L", "category": "Beverages", "cost_price": 55.0, "selling_price": 70.0, "stock": 30.0, "min_stock": 10.0, "unit": "piece"},

    # Spices
    {"name": "Everest Turmeric Powder 200g", "category": "Spices", "cost_price": 42.0, "selling_price": 55.0, "stock": 45.0, "min_stock": 12.0, "unit": "packet"},
    {"name": "Everest Red Chilli Powder 200g", "category": "Spices", "cost_price": 65.0, "selling_price": 85.0, "stock": 40.0, "min_stock": 12.0, "unit": "packet"},
    {"name": "Everest Garam Masala 100g", "category": "Spices", "cost_price": 60.0, "selling_price": 78.0, "stock": 35.0, "min_stock": 10.0, "unit": "packet"},
    {"name": "Catch Jeera (Cumin Seeds) 200g", "category": "Spices", "cost_price": 80.0, "selling_price": 105.0, "stock": 30.0, "min_stock": 8.0, "unit": "packet"},

    # Household Items
    {"name": "Surf Excel Matic Front Load 2kg", "category": "Household Items", "cost_price": 380.0, "selling_price": 450.0, "stock": 28.0, "min_stock": 8.0, "unit": "box"},
    {"name": "Vim Dishwash Gel 750ml", "category": "Household Items", "cost_price": 125.0, "selling_price": 155.0, "stock": 35.0, "min_stock": 10.0, "unit": "piece"},
    {"name": "Dettol Antiseptic Liquid 550ml", "category": "Household Items", "cost_price": 170.0, "selling_price": 205.0, "stock": 25.0, "min_stock": 6.0, "unit": "piece"},
    {"name": "Colin Glass Cleaner 500ml", "category": "Household Items", "cost_price": 85.0, "selling_price": 105.0, "stock": 20.0, "min_stock": 5.0, "unit": "piece"},

    # Personal Care
    {"name": "Dove Moisturizing Soap 3x100g", "category": "Personal Care", "cost_price": 140.0, "selling_price": 175.0, "stock": 30.0, "min_stock": 8.0, "unit": "packet"},
    {"name": "Colgate Strong Teeth Toothpaste 300g", "category": "Personal Care", "cost_price": 115.0, "selling_price": 140.0, "stock": 40.0, "min_stock": 10.0, "unit": "packet"},
    {"name": "Head & Shoulders Shampoo 340ml", "category": "Personal Care", "cost_price": 260.0, "selling_price": 315.0, "stock": 22.0, "min_stock": 6.0, "unit": "piece"},

    # Vegetables (Staples)
    {"name": "Fresh Red Onions", "category": "Vegetables", "cost_price": 24.0, "selling_price": 35.0, "stock": 90.0, "min_stock": 25.0, "unit": "kg"},
    {"name": "Jyoti Potatoes Fresh", "category": "Vegetables", "cost_price": 20.0, "selling_price": 28.0, "stock": 110.0, "min_stock": 30.0, "unit": "kg"},
    {"name": "Hybrid Juicy Tomatoes", "category": "Vegetables", "cost_price": 28.0, "selling_price": 40.0, "stock": 65.0, "min_stock": 20.0, "unit": "kg"},

    # Low Stock / Out of Stock intentional items for realistic dashboard alerts
    {"name": "Almonds California Premium 500g", "category": "Dry Fruits & Nuts", "cost_price": 420.0, "selling_price": 520.0, "stock": 4.0, "min_stock": 10.0, "unit": "packet"},
    {"name": "Cashews Whole W320 500g", "category": "Dry Fruits & Nuts", "cost_price": 390.0, "selling_price": 490.0, "stock": 0.0, "min_stock": 10.0, "unit": "packet"},
    {"name": "Saffola Gold Pro Healthy Oil 5L", "category": "Cooking Oil", "cost_price": 780.0, "selling_price": 920.0, "stock": 3.0, "min_stock": 8.0, "unit": "can"}
]


def init_database():
    """Initializes schema and default users if they do not exist."""
    with open(SCHEMA_FILE, "r", encoding="utf-8") as f:
        schema_sql = f.read()

    conn = get_raw_connection()
    try:
        # SQLite executescript allows multiple statements
        conn.executescript(schema_sql)
        conn.commit()
    finally:
        conn.close()

    # Ensure default admin
    admin = fetch_one("SELECT id FROM users WHERE username = ?", (DEFAULT_ADMIN["username"],))
    if not admin:
        pwd_hash, salt = hash_password(DEFAULT_ADMIN["password"])
        execute_query(
            """
            INSERT INTO users (username, password_hash, salt, full_name, email, phone, role)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                DEFAULT_ADMIN["username"],
                pwd_hash,
                salt,
                DEFAULT_ADMIN["full_name"],
                DEFAULT_ADMIN["email"],
                DEFAULT_ADMIN["phone"],
                DEFAULT_ADMIN["role"]
            )
        )

    # Ensure default demo customer
    cust_user = fetch_one("SELECT id FROM users WHERE username = ?", (DEFAULT_CUSTOMER["username"],))
    if not cust_user:
        pwd_hash, salt = hash_password(DEFAULT_CUSTOMER["password"])
        user_id = execute_insert(
            """
            INSERT INTO users (username, password_hash, salt, full_name, email, phone, role)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                DEFAULT_CUSTOMER["username"],
                pwd_hash,
                salt,
                DEFAULT_CUSTOMER["full_name"],
                DEFAULT_CUSTOMER["email"],
                DEFAULT_CUSTOMER["phone"],
                DEFAULT_CUSTOMER["role"]
            )
        )
        execute_query(
            """
            INSERT INTO customers (user_id, full_name, email, phone, address)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                user_id,
                DEFAULT_CUSTOMER["full_name"],
                DEFAULT_CUSTOMER["email"],
                DEFAULT_CUSTOMER["phone"],
                "Main Road, Bastawad - 416106, Kolhapur, Maharashtra"
            )
        )


def seed_sample_data():
    """
    Seeds ~40 grocery products, 60 days of realistic sales,
    and monthly operating expenses.
    """
    init_database()

    # Check if products already exist
    existing_products = fetch_all("SELECT id, name FROM products")
    product_map = {p["name"]: p["id"] for p in existing_products}

    # Insert products
    with get_db_transaction() as conn:
        cursor = conn.cursor()
        for prod in SAMPLE_PRODUCTS:
            if prod["name"] not in product_map:
                cursor.execute(
                    """
                    INSERT INTO products (name, category, cost_price, selling_price, stock_quantity, min_stock_level, unit, expiry_date, is_active)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, 1)
                    """,
                    (
                        prod["name"],
                        prod["category"],
                        prod["cost_price"],
                        prod["selling_price"],
                        prod["stock"],
                        prod["min_stock"],
                        prod["unit"],
                        (date.today() + timedelta(days=180)).isoformat()
                    )
                )
                product_map[prod["name"]] = cursor.lastrowid

    # Retrieve all products for sale generation
    all_products = fetch_all("SELECT * FROM products WHERE is_active = 1")
    if not all_products:
        return

    # Check if sample sales already exist
    sample_sale_count = fetch_one("SELECT COUNT(*) as cnt FROM sales WHERE is_sample = 1")["cnt"]
    if sample_sale_count > 0:
        return  # Sample sales already seeded

    # Generate customer names
    customer_pool = [
        ("Rahul Sharma", "+91 98230 11223"),
        ("Pooja Patil", "+91 97654 33445"),
        ("Amitabh Kulkarni", "+91 98901 55667"),
        ("Sneha Deshmukh", "+91 91580 77889"),
        ("Vikram Singh", "+91 94220 99001"),
        ("Anita Jadhav", "+91 98812 22334"),
        ("Sunil Joshi", "+91 98224 44556"),
        ("Deepika Pawar", "+91 97668 66778"),
        ("Rajesh Shinde", "+91 99231 88990"),
        ("Meena Chavan", "+91 98500 12345")
    ]

    payment_pool = ["UPI", "Cash", "UPI", "Card", "UPI", "Cash"]  # Realistic UPI weightage

    # Seed sales over the past 60 days
    random.seed(42)
    today = datetime.now()

    with get_db_transaction() as conn:
        cursor = conn.cursor()

        # Seed sales transactions
        for day_offset in range(60, -1, -1):
            sale_date = today - timedelta(days=day_offset)
            # More sales on weekends (Friday, Saturday, Sunday)
            is_weekend = sale_date.weekday() in [4, 5, 6]
            orders_today = random.randint(4, 9) if is_weekend else random.randint(2, 6)

            for _ in range(orders_today):
                hour = random.randint(9, 21)
                minute = random.randint(0, 59)
                second = random.randint(0, 59)
                transaction_time = sale_date.replace(hour=hour, minute=minute, second=second)

                cust_name, cust_phone = random.choice(customer_pool)
                payment_method = random.choice(payment_pool)
                invoice_no = f"GK-{transaction_time.strftime('%Y%m%d')}-{random.randint(1000, 9999)}"

                # Pick 2 to 5 random products for this basket
                basket_size = random.randint(2, 5)
                chosen_products = random.sample(all_products, min(basket_size, len(all_products)))

                subtotal_sale = 0.0
                sale_items_data = []

                for prod in chosen_products:
                    # Realistic quantities: kg/litre usually 1 to 3, packets 1 to 4
                    if prod["unit"] in ["kg", "litre"]:
                        qty = float(random.choice([1, 1.5, 2, 2.5, 3]))
                    else:
                        qty = float(random.choice([1, 2, 3, 4]))

                    item_subtotal = round(qty * prod["selling_price"], 2)
                    item_profit = round((prod["selling_price"] - prod["cost_price"]) * qty, 2)
                    subtotal_sale += item_subtotal

                    sale_items_data.append((
                        prod["id"],
                        prod["name"],
                        prod["category"],
                        prod["unit"],
                        qty,
                        prod["cost_price"],      # Historical cost price
                        prod["selling_price"],   # Historical selling price
                        item_subtotal,
                        item_profit
                    ))

                discount = round(subtotal_sale * 0.05, 2) if (subtotal_sale > 1000 and random.random() > 0.5) else 0.0
                grand_total = round(subtotal_sale - discount, 2)

                cursor.execute(
                    """
                    INSERT INTO sales (invoice_no, customer_name, customer_phone, total_amount, discount_amount, grand_total, payment_method, payment_status, sale_date, is_sample)
                    VALUES (?, ?, ?, ?, ?, ?, ?, 'Paid', ?, 1)
                    """,
                    (
                        invoice_no,
                        cust_name,
                        cust_phone,
                        round(subtotal_sale, 2),
                        discount,
                        grand_total,
                        payment_method,
                        transaction_time.strftime("%Y-%m-%d %H:%M:%S")
                    )
                )
                sale_id = cursor.lastrowid

                for item in sale_items_data:
                    cursor.execute(
                        """
                        INSERT INTO sale_items (sale_id, product_id, product_name, category, unit, quantity, cost_price, selling_price, subtotal, profit)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """,
                        (sale_id, item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7], item[8])
                    )

        # Seed operating expenses for the past 2 months
        sample_expenses = [
            # Last Month
            ("Shop Rent", "Monthly Store Rental - Main Market", 25000.0, (today - timedelta(days=45)).date(), "Shop Owner Mr. Verma", "Bank Transfer"),
            ("Electricity Bills", "MSEDCL Commercial Power Bill", 4800.0, (today - timedelta(days=40)).date(), "Online Electricity Payment", "UPI"),
            ("Employee Salaries", "Salary - Store Helper & Billing Staff", 18000.0, (today - timedelta(days=35)).date(), "Staff monthly compensation", "Bank Transfer"),
            ("Transportation", "Wholesale Mandi Goods Transport & Porter", 3200.0, (today - timedelta(days=32)).date(), "Vehicle tempo delivery fees", "Cash"),
            ("Packaging & Bags", "Biodegradable Carry Bags & Bill Paper Rolls", 1850.0, (today - timedelta(days=31)).date(), "Wholesale packaging bulk supply", "UPI"),
            ("Store Maintenance", "Pest Control & Deep Cleaning", 1200.0, (today - timedelta(days=30)).date(), "Monthly hygiene inspection", "Cash"),

            # Current Month
            ("Shop Rent", "Monthly Store Rental - Main Market", 25000.0, (today - timedelta(days=15)).date(), "Shop Owner Mr. Verma", "Bank Transfer"),
            ("Electricity Bills", "MSEDCL Commercial Power Bill", 5200.0, (today - timedelta(days=10)).date(), "Online Electricity Payment", "UPI"),
            ("Employee Salaries", "Salary - Store Helper & Billing Staff", 18000.0, (today - timedelta(days=5)).date(), "Staff monthly compensation", "Bank Transfer"),
            ("Transportation", "Wholesale Mandi Goods Transport & Porter", 3600.0, (today - timedelta(days=7)).date(), "Vehicle tempo delivery fees", "Cash"),
            ("Packaging & Bags", "Biodegradable Carry Bags & Barcode Labels", 2100.0, (today - timedelta(days=3)).date(), "Wholesale packaging bulk supply", "UPI"),
            ("Miscellaneous", "Store Refreshments & Drinking Water Jars", 950.0, (today - timedelta(days=2)).date(), "Monthly Bisleri water jars", "Cash")
        ]

        for exp in sample_expenses:
            cursor.execute(
                """
                INSERT INTO expenses (category, title, amount, expense_date, description, payment_method, is_sample)
                VALUES (?, ?, ?, ?, ?, ?, 1)
                """,
                (exp[0], exp[1], exp[2], exp[3].isoformat(), exp[4], exp[5])
            )


def remove_sample_data():
    """
    Cleans up all sample data (sales, sale_items, expenses) flagged with is_sample = 1.
    Genuine store transactions are completely untouched!
    """
    with get_db_transaction() as conn:
        cursor = conn.cursor()
        # Find all sample sale IDs
        cursor.execute("SELECT id FROM sales WHERE is_sample = 1")
        sample_sales = cursor.fetchall()
        sale_ids = [row["id"] for row in sample_sales]

        if sale_ids:
            # Delete sale items for these sales
            placeholders = ",".join(["?"] * len(sale_ids))
            cursor.execute(f"DELETE FROM sale_items WHERE sale_id IN ({placeholders})", sale_ids)
            cursor.execute("DELETE FROM sales WHERE is_sample = 1")

        # Delete sample expenses
        cursor.execute("DELETE FROM expenses WHERE is_sample = 1")

    return True


if __name__ == "__main__":
    print("Initializing Database...")
    init_database()
    print("Database Initialized successfully.")
    print("Seeding Sample Data...")
    seed_sample_data()
    print("Sample Data Seeded successfully.")
