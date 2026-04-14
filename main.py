import flet as ft
from database import create_tables
from suppliers_view import suppliers_view

def main(page: ft.Page):
    create_tables()

    page.title = "Company Purchase and Expense Tracking System"
    page.window_width = 1000
    page.window_height = 650
    page.padding = 20
    page.scroll = "auto"

    title = ft.Text(
        "Company Purchase and Expense Tracking System",
        size=24,
        weight=ft.FontWeight.BOLD
    )

    tabs = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        expand=1,
        tabs=[
            ft.Tab(
                text="Dashboard",
                content=ft.Container(
                    content=ft.Text("Dashboard view coming soon..."),
                    padding=20
                )
            ),
            ft.Tab(
                text="Suppliers",
                content=suppliers_view(page)
            ),
            ft.Tab(
                text="Purchases",
                content=ft.Container(
                    content=ft.Text("Purchases view coming soon..."),
                    padding=20
                )
            ),
            ft.Tab(
                text="Expenses",
                content=ft.Container(
                    content=ft.Text("Expenses view coming soon..."),
                    padding=20
                )
            ),
            ft.Tab(
                text="Reports",
                content=ft.Container(
                    content=ft.Text("Reports view coming soon..."),
                    padding=20
                )
            ),
        ],
    )

    page.add(
        ft.Column(
            controls=[title, tabs],
            expand=True
        )
    )

if __name__ == "__main__":
    ft.app(target=main)