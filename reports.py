import flet as ft
from models import get_purchases, get_expenses

def reports_view(page: ft.Page):
    purchases_area = ft.Column()
    expenses_area = ft.Column()

    def load_reports():
        purchases_area.controls.clear()
        expenses_area.controls.clear()

        purchases = get_purchases()
        expenses = get_expenses()

        purchases_area.controls.append(
            ft.Text(f"Purchases registered: {len(purchases)}", size=18)
        )

        expenses_area.controls.append(
            ft.Text(f"Expenses registered: {len(expenses)}", size=18)
        )

        page.update()

    load_reports()

    return ft.Container(
        padding=20,
        content=ft.Column(
            controls=[
                ft.Text("Reports", size=24, weight=ft.FontWeight.BOLD),
                ft.Text("Simple Summary", size=18, weight=ft.FontWeight.BOLD),
                purchases_area,
                expenses_area,
                ft.ElevatedButton("Refresh", on_click=lambda e: load_reports())
            ]
        )
    )