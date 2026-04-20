import flet as ft
from models import (
    get_report_by_category,
    get_report_by_supplier,
    get_report_by_month
)

def reports_view(page: ft.Page):
    category_table = ft.Column()
    supplier_table = ft.Column()
    month_table = ft.Column()

    def show_message(text):
        page.snack_bar = ft.SnackBar(ft.Text(text))
        page.snack_bar.open = True
        page.update()

    def make_table(title, columns, rows_data):
        if not rows_data:
            return ft.Column(
                controls=[
                    ft.Text(title, size=18, weight=ft.FontWeight.BOLD),
                    ft.Text("No data yet.")
                ]
            )

        rows = []
        for row in rows_data:
            rows.append(
                ft.DataRow(
                    cells=[ft.DataCell(ft.Text(str(value))) for value in row]
                )
            )

        return ft.Column(
            controls=[
                ft.Text(title, size=18, weight=ft.FontWeight.BOLD),
                ft.DataTable(
                    columns=[ft.DataColumn(ft.Text(col)) for col in columns],
                    rows=rows
                )
            ]
        )

    def load_reports():
        category_table.controls.clear()
        supplier_table.controls.clear()
        month_table.controls.clear()

        try:
            category_data = get_report_by_category()
            supplier_data = get_report_by_supplier()
            month_data = get_report_by_month()

            category_table.controls.append(
                make_table(
                    "Expenses by Category",
                    ["Category", "Total"],
                    category_data
                )
            )

            supplier_table.controls.append(
                make_table(
                    "Purchases by Supplier",
                    ["Supplier", "Total"],
                    supplier_data
                )
            )

            month_table.controls.append(
                make_table(
                    "Expenses by Month",
                    ["Month", "Total"],
                    month_data
                )
            )

            page.update()

        except Exception as e:
            show_message(f"Could not load reports: {e}")

    load_reports()

    return ft.Container(
        padding=20,
        content=ft.Column(
            controls=[
                ft.Text("Reports", size=22, weight=ft.FontWeight.BOLD),
                ft.Row(
                    controls=[
                        ft.ElevatedButton("Refresh Reports", on_click=lambda e: load_reports())
                    ]
                ),
                ft.Divider(),
                category_table,
                ft.Divider(),
                supplier_table,
                ft.Divider(),
                month_table,
            ],
            scroll=ft.ScrollMode.AUTO
        )
    )