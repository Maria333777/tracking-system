from database import connect_db

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
    cursor.execute("""
        SELECT id, company_name, phone, email
        FROM suppliers
        ORDER BY id DESC
    """)
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

def delete_supplier(supplier_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM suppliers WHERE id = ?", (supplier_id,))
    conn.commit()
    conn.close()

def add_purchase(supplier_id, item_name, quantity, unit_cost, purchase_date, status):
    total_cost = quantity * unit_cost
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO purchases (
            supplier_id, item_name, quantity, unit_cost,
            total_cost, purchase_date, status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (supplier_id, item_name, quantity, unit_cost, total_cost, purchase_date, status))
    conn.commit()
    conn.close()

def get_purchases():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.id, s.company_name, p.item_name, p.quantity,
               p.unit_cost, p.total_cost, p.purchase_date, p.status
        FROM purchases p
        JOIN suppliers s ON p.supplier_id = s.id
        ORDER BY p.id DESC
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

def delete_purchase(purchase_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM purchases WHERE id = ?", (purchase_id,))
    conn.commit()
    conn.close()

def add_expense(category, description, amount, expense_date, payment_method, status):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO expenses (
            category, description, amount, expense_date,
            payment_method, status
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (category, description, amount, expense_date, payment_method, status))
    conn.commit()
    conn.close()

def get_expenses():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, category, description, amount,
               expense_date, payment_method, status
        FROM expenses
        ORDER BY id DESC
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

def delete_expense(expense_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    conn.commit()
    conn.close()

def get_dashboard_summary():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM suppliers")
    suppliers_count = cursor.fetchone()[0]

    cursor.execute("SELECT COALESCE(SUM(total_cost), 0) FROM purchases")
    total_purchases = float(cursor.fetchone()[0])

    cursor.execute("SELECT COALESCE(SUM(amount), 0) FROM expenses")
    total_expenses = float(cursor.fetchone()[0])

    conn.close()

    return {
        "suppliers_count": suppliers_count,
        "total_purchases": total_purchases,
        "total_expenses": total_expenses,
    }

def get_report_by_category():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT category, ROUND(SUM(amount), 2)
        FROM expenses
        GROUP BY category
        ORDER BY SUM(amount) DESC
    """)
    data = cursor.fetchall()
    conn.close()
    return data

def get_report_by_supplier():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT s.company_name, ROUND(COALESCE(SUM(p.total_cost), 0), 2)
        FROM suppliers s
        LEFT JOIN purchases p ON s.id = p.supplier_id
        GROUP BY s.id, s.company_name
        ORDER BY COALESCE(SUM(p.total_cost), 0) DESC
    """)
    data = cursor.fetchall()
    conn.close()
    return data

def get_report_by_month():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT month, ROUND(total_expenses, 2)
        FROM monthly_expense_summary
        ORDER BY month DESC
    """)
    data = cursor.fetchall()
    conn.close()
    return data