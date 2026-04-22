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
    page.window_width = 1200
    page.window_height = 760
    page.padding = 20
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#0b1220"
    page.scroll = "auto"

    title = ft.Text(
        "Company Purchase and Expense Tracking System",
        size=28,
        weight=ft.FontWeight.BOLD,
        color="white"
    )

    subtitle = ft.Text(
        "Manage suppliers, purchases, expenses and reports in one place.",
        size=14,
        color="#9ca3af"
    )

    header = ft.Container(
        padding=20,
        border_radius=20,
        bgcolor="#111827",
        border=ft.border.all(1, "#1f2937"),
        content=ft.Column(
            controls=[title, subtitle],
            spacing=6
        )
    )

    tabs = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        label_color="#93c5fd",
        unselected_label_color="#d1d5db",
        indicator_color="#60a5fa",
        divider_color="#334155",
        expand=1,
        tabs=[
            ft.Tab(
                text="Dashboard",
                content=dashboard_view(page)
            ),
            ft.Tab(
                text="Suppliers",
                content=suppliers_view(page)
            ),
            ft.Tab(
                text="Purchases",
                content=purchases_view(page)
            ),
            ft.Tab(
                text="Expenses",
                content=expenses_view(page)
            ),
            ft.Tab(
                text="Reports",
                content=reports_view(page)
            ),
        ],
    )

    page.add(
        ft.Column(
            controls=[
                header,
                tabs
            ],
            spacing=20,
            expand=True
        )
    )

if __name__ == "__main__":
    ft.app(target=main)