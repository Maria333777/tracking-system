import flet as ft
from models import get_dashboard_summary, get_report_by_category, get_report_by_month

def dashboard_view(page: ft.Page):
    suppliers_text = ft.Text(size=20, weight=ft.FontWeight.BOLD)
    purchases_text = ft.Text(size=20, weight=ft.FontWeight.BOLD)
    expenses_text = ft.Text(size=20, weight=ft.FontWeight.BOLD)
    total_text = ft.Text(size=20, weight=ft.FontWeight.BOLD)

    category_area = ft.Column()
    month_area = ft.Column()

    def load_dashboard(e=None):
        summary = get_dashboard_summary()
        category_data = get_report_by_category()
        month_data = get_report_by_month()

        suppliers_text.value = f"Number of Suppliers: {summary['suppliers_count']}"
        purchases_text.value = f"Total Purchases: {summary['total_purchases']:.2f}"
        expenses_text.value = f"Total Expenses: {summary['total_expenses']:.2f}"
        total_text.value = f"Total Money Tracked: {summary['total_purchases'] + summary['total_expenses']:.2f}"

        category_area.controls.clear()
        month_area.controls.clear()

        category_area.controls.append(ft.Text("Category Totals", size=18, weight=ft.FontWeight.BOLD))
        if category_data:
            for row in category_data[:5]:
                category_area.controls.append(ft.Text(f"{row[0]}: {row[1]}"))
        else:
            category_area.controls.append(ft.Text("No category data yet."))

        month_area.controls.append(ft.Text("Monthly Totals", size=18, weight=ft.FontWeight.BOLD))
        if month_data:
            for row in month_data[:5]:
                month_area.controls.append(ft.Text(f"{row[0]}: {row[1]}"))
        else:
            month_area.controls.append(ft.Text("No monthly data yet."))

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
                total_text,
                ft.Divider(),
                category_area,
                ft.Divider(),
                month_area,
                ft.ElevatedButton("Refresh", on_click=load_dashboard),
            ],
            scroll=ft.ScrollMode.AUTO
        )
    )