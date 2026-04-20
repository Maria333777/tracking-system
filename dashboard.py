import flet as ft
from models import get_dashboard_summary

def dashboard_view(page: ft.Page):
    purchases_text = ft.Text("Total Purchases: 0.00", size=18, weight=ft.FontWeight.BOLD)
    expenses_text = ft.Text("Total Expenses: 0.00", size=18, weight=ft.FontWeight.BOLD)
    suppliers_text = ft.Text("Number of Suppliers: 0", size=18, weight=ft.FontWeight.BOLD)
    summary_text = ft.Text("General Summary", size=16)

    def load_dashboard():
        data = get_dashboard_summary()

        total_purchases = data["total_purchases"]
        total_expenses = data["total_expenses"]
        suppliers_count = data["suppliers_count"]

        purchases_text.value = f"Total Purchases: {total_purchases:.2f}"
        expenses_text.value = f"Total Expenses: {total_expenses:.2f}"
        suppliers_text.value = f"Number of Suppliers: {suppliers_count}"

        summary_text.value = (
            f"General Summary:\n"
            f"Purchases registered: {total_purchases:.2f}\n"
            f"Expenses registered: {total_expenses:.2f}\n"
            f"Active suppliers: {suppliers_count}\n"
            f"Total money tracked: {(total_purchases + total_expenses):.2f}"
        )

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
                ft.Divider(),
                summary_text,
                ft.ElevatedButton("Refresh Dashboard", on_click=lambda e: load_dashboard()),
            ],
            scroll=ft.ScrollMode.AUTO
        )
    )