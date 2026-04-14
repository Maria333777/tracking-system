from database import connect_db


# ---------------- SUPPLIERS ----------------
def add_supplier(company_name, phone, email):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO suppliers (company_name, phone, email)
        VALUES (?, ?, ?)
    """, (company_name, phone, email))
    conn.commit()
    conn.close()


def get_suppliers():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM suppliers ORDER BY company_name")
    data = cursor.fetchall()
    conn.close()
    return data


def update_supplier(supplier_id, company_name, phone, email):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE suppliers
        SET company_name = ?, phone = ?, email = ?
        WHERE id = ?
    """, (company_name, phone, email, supplier_id))
    conn.commit()
    conn.close()


# ---------------- PURCHASES ----------------
def add_purchase(supplier_id, item_name, quantity, unit_cost, purchase_date, status):
    total_cost = quantity * unit_cost

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO purchases
        (supplier_id, item_name, quantity, unit_cost, total_cost, purchase_date, status)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (supplier_id, item_name, quantity, unit_cost, total_cost, purchase_date, status))
    conn.commit()
    conn.close()


def get_purchases():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT purchases.id, suppliers.company_name, purchases.item_name,
               purchases.quantity, purchases.unit_cost, purchases.total_cost,
               purchases.purchase_date, purchases.status
        FROM purchases
        JOIN suppliers ON purchases.supplier_id = suppliers.id
        ORDER BY purchases.purchase_date DESC
    """)
    data = cursor.fetchall()
    conn.close()
    return data


def update_purchase(purchase_id, supplier_id, item_name, quantity, unit_cost, purchase_date, status):
    total_cost = quantity * unit_cost

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE purchases
        SET supplier_id = ?, item_name = ?, quantity = ?, unit_cost = ?,
            total_cost = ?, purchase_date = ?, status = ?
        WHERE id = ?
    """, (supplier_id, item_name, quantity, unit_cost, total_cost, purchase_date, status, purchase_id))
    conn.commit()
    conn.close()


# ---------------- EXPENSES ----------------
def add_expense(category, description, amount, expense_date, payment_method, status):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO expenses
        (category, description, amount, expense_date, payment_method, status)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (category, description, amount, expense_date, payment_method, status))
    conn.commit()
    conn.close()


def get_expenses():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM expenses
        ORDER BY expense_date DESC
    """)
    data = cursor.fetchall()
    conn.close()
    return data


def update_expense(expense_id, category, description, amount, expense_date, payment_method, status):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE expenses
        SET category = ?, description = ?, amount = ?, expense_date = ?,
            payment_method = ?, status = ?
        WHERE id = ?
    """, (category, description, amount, expense_date, payment_method, status, expense_id))
    conn.commit()
    conn.close()