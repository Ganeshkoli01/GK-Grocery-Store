"""
GK GROCERY STORE – Database Connection & Execution Engine
Provides unified database abstraction for SQLite with transaction support,
dictionary row mapping, and easy adaptability to MySQL/PostgreSQL.
"""

import sqlite3
import pandas as pd
from contextlib import contextmanager
from config import SQLITE_DB_PATH, DB_TYPE, MYSQL_CONFIG


def get_raw_connection():
    """Returns a raw database connection configured for data integrity."""
    if DB_TYPE == "sqlite":
        conn = sqlite3.connect(
            SQLITE_DB_PATH,
            detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES,
            timeout=30.0,
            check_same_thread=False
        )
        conn.row_factory = sqlite3.Row
        # Enable Foreign Key support and WAL mode for better concurrency
        conn.execute("PRAGMA foreign_keys = ON;")
        conn.execute("PRAGMA journal_mode = WAL;")
        return conn
    elif DB_TYPE == "mysql":
        # Ready for future MySQL deployment without touching business logic
        try:
            import mysql.connector
            return mysql.connector.connect(
                host=MYSQL_CONFIG["host"],
                port=MYSQL_CONFIG["port"],
                user=MYSQL_CONFIG["user"],
                password=MYSQL_CONFIG["password"],
                database=MYSQL_CONFIG["database"]
            )
        except ImportError:
            raise RuntimeError("mysql-connector-python package is required for MySQL mode.")
    else:
        raise ValueError(f"Unsupported DB_TYPE: {DB_TYPE}")


@contextmanager
def get_db_connection():
    """Context manager for read queries and auto-closing connections."""
    conn = get_raw_connection()
    try:
        yield conn
    finally:
        conn.close()


@contextmanager
def get_db_transaction():
    """
    Context manager for atomic write operations.
    Automatically commits on normal completion or rolls back on exceptions.
    """
    conn = get_raw_connection()
    try:
        yield conn
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()


def execute_query(sql: str, params=()) -> int:
    """Execute INSERT/UPDATE/DELETE query and return affected row count."""
    with get_db_transaction() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, params)
        return cursor.rowcount


def execute_insert(sql: str, params=()) -> int:
    """Execute INSERT query and return last inserted row ID."""
    with get_db_transaction() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, params)
        return cursor.lastrowid


def fetch_all(sql: str, params=()) -> list:
    """Fetch all rows returned by query as list of dictionaries."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, params)
        rows = cursor.fetchall()
        return [dict(row) for row in rows]


def fetch_one(sql: str, params=()) -> dict | None:
    """Fetch a single row as dictionary or None."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, params)
        row = cursor.fetchone()
        return dict(row) if row else None


def fetch_dataframe(sql: str, params=()) -> pd.DataFrame:
    """Fetch query results directly as a Pandas DataFrame."""
    with get_db_connection() as conn:
        # Use pandas read_sql_query
        return pd.read_sql_query(sql, conn, params=params)

