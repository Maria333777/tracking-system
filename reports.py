import flet as ft
from models import get_report_by_category, get_report_by_supplier, get_report_by_month

def reports_view(page: ft.Page):
    category_area = ft.Column()
    supplier_area = ft.Column()
    month_area = ft.Column()

    def make_table(title, headers, data):
        if not data:
            return ft.Column([ft.Text(title, size=18, weight=ft.FontWeight.BOLD), ft.Text("No data yet.")])

        rows = []
        for row in data:
            rows.append(
                ft.DataRow(
                    cells=[ft.DataCell(ft.Text(str(value))) for value in row]
                )
            )

        return ft.Column(
            [
                ft.Text(title, size=18, weight=ft.FontWeight.BOLD),
                ft.DataTable(
                    columns=[ft.DataColumn(ft.Text(h)) for h in headers],
                    rows=rows
                )
            ]
        )

    def load_reports(e=None):
        category_area.controls.clear()
        supplier_area.controls.clear()
        month_area.controls.clear()

        category_area.controls.append(
            make_table("Expenses by Category", ["Category", "Total"], get_report_by_category())
        )

        supplier_area.controls.append(
            make_table("Purchases by Supplier", ["Supplier", "Total"], get_report_by_supplier())
        )

        month_area.controls.append(
            make_table("Expenses by Month", ["Month", "Total"], get_report_by_month())
        )

        page.update()

    load_reports()

    return ft.Container(
        padding=20,
        content=ft.Column(
            controls=[
                ft.Text("Reports", size=22, weight=ft.FontWeight.BOLD),
                ft.ElevatedButton("Refresh", on_click=load_reports),
                ft.Divider(),
                category_area,
                ft.Divider(),
                supplier_area,
                ft.Divider(),
                month_area,
            ],
            scroll=ft.ScrollMode.AUTO
        )
    )