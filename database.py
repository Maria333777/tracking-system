import sqlite3

DB_NAME = "company_tracking.db"

def connect_db():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def create_tables():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS suppliers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_name TEXT NOT NULL,
            phone TEXT,
            email TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS purchases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            supplier_id INTEGER NOT NULL,
            item_name TEXT NOT NULL,
            quantity REAL NOT NULL CHECK(quantity > 0),
            unit_cost REAL NOT NULL CHECK(unit_cost > 0),
            total_cost REAL NOT NULL CHECK(total_cost >= 0),
            purchase_date TEXT NOT NULL,
            status TEXT,
            FOREIGN KEY (supplier_id) REFERENCES suppliers(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            description TEXT NOT NULL,
            amount REAL NOT NULL CHECK(amount > 0),
            expense_date TEXT NOT NULL,
            payment_method TEXT,
            status TEXT
        )
    """)

    cursor.execute("""
        CREATE VIEW IF NOT EXISTS monthly_expense_summary AS
        SELECT substr(expense_date, 1, 7) AS month,
               SUM(amount) AS total_expenses
        FROM expenses
        GROUP BY substr(expense_date, 1, 7)
    """)

    conn.commit()
    conn.close()