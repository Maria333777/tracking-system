import flet as ft
from database import create_tables
from suppliers_view import suppliers_view
from purchases import purchases_view
from expenses import expenses_view
from dashboard import dashboard_view
from reports import reports_view

def main(page: ft.Page):
    create_tables()

    page.title = "Company Purchase and Expense Tracking System"
    page.window_width = 1100
    page.window_height = 700
    page.padding = 20
    page.scroll = "auto"

    title = ft.Text(
        "Company Purchase and Expense Tracking System",
        size=24,
        weight=ft.FontWeight.BOLD
    )

    tabs = ft.Tabs(
        expand=1,
        tabs=[
            ft.Tab(text="Dashboard", content=dashboard_view(page)),
            ft.Tab(text="Suppliers", content=suppliers_view(page)),
            ft.Tab(text="Purchases", content=purchases_view(page)),
            ft.Tab(text="Expenses", content=expenses_view(page)),
            ft.Tab(text="Reports", content=reports_view(page)),
        ]
    )

    page.add(ft.Column([title, tabs], expand=True))

if __name__ == "__main__":
    ft.app(target=main)