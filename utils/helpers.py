"""
GK GROCERY STORE – General Helper Utilities
Includes secure password hashing, currency formatting, date filters,
and invoice number generators.
"""

from __future__ import annotations
import hashlib
import secrets
import random
import base64
from datetime import datetime, date, timedelta
from config import CURRENCY, ASSETS_DIR


def hash_password(password: str, salt: str = None) -> tuple[str, str]:
    """
    Hashes a password using PBKDF2-HMAC-SHA256 with a unique cryptographic salt.
    Returns (hex_hash, hex_salt).
    """
    if not salt:
        salt = secrets.token_hex(16)
    
    key = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        bytes.fromhex(salt),
        100000
    )
    return key.hex(), salt


def verify_password(password: str, stored_hash: str, salt: str) -> bool:
    """Verifies a password attempt against stored PBKDF2 hash and salt."""
    key, _ = hash_password(password, salt)
    return secrets.compare_digest(key, stored_hash)


def format_currency(amount: float | int | None) -> str:
    """Formats numeric amounts into Indian Rupee standard format (e.g. ₹1,25,000.00)."""
    if amount is None:
        return f"{CURRENCY}0.00"
    try:
        val = float(amount)
        # Handle negative values
        prefix = "-" if val < 0 else ""
        abs_val = abs(val)
        
        # Format according to Indian grouping (last 3, then groups of 2)
        s, dec = f"{abs_val:.2f}".split(".")
        if len(s) > 3:
            last3 = s[-3:]
            remaining = s[:-3]
            groups = []
            while len(remaining) > 2:
                groups.insert(0, remaining[-2:])
                remaining = remaining[:-2]
            if remaining:
                groups.insert(0, remaining)
            formatted = ",".join(groups) + "," + last3
        else:
            formatted = s
            
        return f"{prefix}{CURRENCY}{formatted}.{dec}"
    except (ValueError, TypeError):
        return f"{CURRENCY}0.00"


def generate_invoice_number() -> str:
    """Generates a human-friendly unique invoice number like GK-20261110-8472."""
    now = datetime.now()
    date_part = now.strftime("%Y%m%d")
    random_part = random.randint(1000, 9999)
    return f"GK-{date_part}-{random_part}"


def get_date_range(filter_option: str, custom_start=None, custom_end=None) -> tuple[datetime, datetime]:
    """
    Translates high-level date filter strings into precise start and end datetimes.
    """
    now = datetime.now()
    today_start = datetime.combine(now.date(), datetime.min.time())
    today_end = datetime.combine(now.date(), datetime.max.time())
    
    if filter_option == "Today":
        return today_start, today_end
    elif filter_option == "Yesterday":
        yesterday = now.date() - timedelta(days=1)
        return datetime.combine(yesterday, datetime.min.time()), datetime.combine(yesterday, datetime.max.time())
    elif filter_option == "Last 7 Days":
        start = today_start - timedelta(days=6)
        return start, today_end
    elif filter_option == "Last 30 Days":
        start = today_start - timedelta(days=29)
        return start, today_end
    elif filter_option == "This Month":
        start = datetime(now.year, now.month, 1, 0, 0, 0)
        return start, today_end
    elif filter_option == "This Year":
        start = datetime(now.year, 1, 1, 0, 0, 0)
        return start, today_end
    elif filter_option == "All Time":
        start = datetime(2020, 1, 1, 0, 0, 0)
        return start, today_end
    elif filter_option == "Custom Date Range" and custom_start and custom_end:
        start = datetime.combine(custom_start, datetime.min.time())
        end = datetime.combine(custom_end, datetime.max.time())
        return start, end
    else:
        # Default to Last 30 Days
        start = today_start - timedelta(days=29)
        return start, today_end


def get_stock_badge(stock: float, min_stock: float) -> tuple[str, str]:
    """Returns status text and color class for product stock level."""
    if stock <= 0:
        return "Out of Stock", "badge-danger"
    elif stock <= min_stock:
        return f"Low Stock ({stock:g} left)", "badge-warning"
    else:
        return "In Stock", "badge-success"


_CACHED_LOGO_B64 = None


def get_logo_base64() -> str:
    """Returns cached base64 data URI of the store logo for instant HTML embedding."""
    global _CACHED_LOGO_B64
    if _CACHED_LOGO_B64 is not None:
        return _CACHED_LOGO_B64

    logo_path = ASSETS_DIR / "logo.png"
    if logo_path.exists():
        try:
            with open(logo_path, "rb") as f:
                encoded = base64.b64encode(f.read()).decode("utf-8")
            _CACHED_LOGO_B64 = f"data:image/png;base64,{encoded}"
            return _CACHED_LOGO_B64
        except Exception:
            return ""
    return ""


