import flet as ft
from models import get_dashboard_summary

def dashboard_view(page: ft.Page):
    purchases_text = ft.Text("Total Purchases: 0.00", size=18)
    expenses_text = ft.Text("Total Expenses: 0.00", size=18)
    suppliers_text = ft.Text("Number of Suppliers: 0", size=18)
    total_text = ft.Text("Total Money Tracked: 0.00", size=18, weight=ft.FontWeight.BOLD)

    def load_dashboard(e=None):
        data = get_dashboard_summary()

        purchases = float(data["total_purchases"])
        expenses = float(data["total_expenses"])
        suppliers = int(data["suppliers_count"])

        purchases_text.value = f"Total Purchases: {purchases:.2f}"
        expenses_text.value = f"Total Expenses: {expenses:.2f}"
        suppliers_text.value = f"Number of Suppliers: {suppliers}"
        total_text.value = f"Total Money Tracked: {purchases + expenses:.2f}"

        page.update()

    load_dashboard()

    return ft.Container(
        padding=20,
        content=ft.Column(
            controls=[
                ft.Text("Dashboard", size=22, weight=ft.FontWeight.BOLD),
                purchases_text,
                expenses_text,
                suppliers_text,
                total_text,
                ft.ElevatedButton("Refresh", on_click=load_dashboard),
            ]
        )
    )