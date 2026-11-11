"""
GK GROCERY STORE – SMART BUSINESS ANALYTICS
Configuration Module
"""

import os
from pathlib import Path

# Base Paths
BASE_DIR = Path(__file__).resolve().parent
DATABASE_DIR = BASE_DIR / "database"
ASSETS_DIR = BASE_DIR / "assets"
EXPORTS_DIR = BASE_DIR / "exports"
POWERBI_DIR = BASE_DIR / "powerbi"

# Ensure runtime directories exist
EXPORTS_DIR.mkdir(parents=True, exist_ok=True)
DATABASE_DIR.mkdir(parents=True, exist_ok=True)
ASSETS_DIR.mkdir(parents=True, exist_ok=True)

# Application Branding
APP_NAME = "GK GROCERY STORE"
APP_SUBTITLE = "Smart Grocery Management & Business Analytics"
APP_TAGLINE = "Smart Shopping. Smarter Business Decisions."
APP_VERSION = "2.1.0"
CURRENCY = "₹"

# Color Palette (Modern Commercial Grocery Theme)
THEME_COLORS = {
    "primary": "#14532D",       # Dark Green
    "secondary": "#22C55E",     # Fresh Green
    "background": "#F8FAFC",    # Soft Slate Light
    "card_bg": "#FFFFFF",       # Crisp White
    "accent": "#F59E0B",        # Amber / Orange
    "danger": "#EF4444",        # Crimson Red
    "info": "#0284C7",          # Ocean Blue
    "text_dark": "#1E293B",     # Deep Slate
    "text_muted": "#64748B",    # Muted Gray
    "border": "#E2E8F0"         # Light Border
}

# Database Configuration
# Default to SQLite for easy local setup, structured for easy MySQL adapter plug-in
DB_TYPE = os.getenv("GK_DB_TYPE", "sqlite")
SQLITE_DB_PATH = DATABASE_DIR / "gk_grocery_store.db"

# MySQL Settings (for future enterprise switch without rewriting app logic)
MYSQL_CONFIG = {
    "host": os.getenv("MYSQL_HOST", "localhost"),
    "port": int(os.getenv("MYSQL_PORT", 3306)),
    "user": os.getenv("MYSQL_USER", "root"),
    "password": os.getenv("MYSQL_PASSWORD", ""),
    "database": os.getenv("MYSQL_DB", "gk_grocery_store")
}

# Product Categories
PRODUCT_CATEGORIES = [
    "Rice and Grains",
    "Pulses",
    "Dairy Products",
    "Cooking Oil",
    "Snacks",
    "Beverages",
    "Spices",
    "Household Items",
    "Personal Care",
    "Vegetables",
    "Bakery & Bread",
    "Dry Fruits & Nuts"
]

# Units of Measure
PRODUCT_UNITS = [
    "kg",
    "gram",
    "litre",
    "ml",
    "packet",
    "piece",
    "box",
    "bundle",
    "can"
]

# Payment Methods
PAYMENT_METHODS = ["Cash", "UPI", "Card", "Other"]

# Expense Categories
EXPENSE_CATEGORIES = [
    "Shop Rent",
    "Electricity Bills",
    "Transportation",
    "Employee Salaries",
    "Packaging & Bags",
    "Store Maintenance",
    "Marketing & Signage",
    "Licensing & Taxes",
    "Water & Sanitation",
    "Miscellaneous"
]

# Default Admin Setup
DEFAULT_ADMIN = {
    "username": "ganesh_01",
    "password": "Ganeshk@825",
    "full_name": "Ganesh Koli (Store Owner)",
    "email": "owner@gkgrocery.com",
    "phone": "+91 8010434421",
    "role": "owner"
}

# Demo Customer
DEFAULT_CUSTOMER = {
    "username": "customer",
    "password": "customer123",
    "full_name": "Rahul Sharma",
    "email": "rahul.sharma@example.com",
    "phone": "+91 98111 22233",
    "role": "customer"
}

