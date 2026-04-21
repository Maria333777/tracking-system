import flet as ft
from models import get_suppliers, get_purchases, get_expenses

def dashboard_view(page: ft.Page):
    suppliers_text = ft.Text(size=20, weight=ft.FontWeight.BOLD)
    purchases_text = ft.Text(size=20, weight=ft.FontWeight.BOLD)
    expenses_text = ft.Text(size=20, weight=ft.FontWeight.BOLD)

    def load_dashboard():
        suppliers = get_suppliers()
        purchases = get_purchases()
        expenses = get_expenses()

        suppliers_text.value = f"Number of Suppliers: {len(suppliers)}"
        purchases_text.value = f"Total Purchases: {len(purchases)}"
        expenses_text.value = f"Total Expenses: {len(expenses)}"

        page.update()

    load_dashboard()

    return ft.Container(
        padding=20,
        content=ft.Column(
            controls=[
                ft.Text("Dashboard", size=24, weight=ft.FontWeight.BOLD),
                suppliers_text,
                purchases_text,
                expenses_text,
                ft.ElevatedButton("Refresh", on_click=lambda e: load_dashboard())
            ]
        )
    )