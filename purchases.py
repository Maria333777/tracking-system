import datetime
import flet as ft
from models import add_purchase, get_purchases, get_suppliers

def purchases_view(page: ft.Page):
    supplier_input = ft.TextField(label="Supplier Name", width=220)
    item_name = ft.TextField(label="Item Name", width=200)
    quantity = ft.TextField(label="Quantity", width=150)
    unit_cost = ft.TextField(label="Unit Cost", width=150)
    purchase_date = ft.TextField(label="Purchase Date", width=180, read_only=True)
    status = ft.TextField(label="Status", width=180)

    total_text = ft.Text("Total Cost: 0.00", size=16, weight=ft.FontWeight.BOLD)
    table_area = ft.Column()
    suppliers_map = {}

    today = datetime.datetime.now()

    def show_message(text):
        page.snack_bar = ft.SnackBar(ft.Text(text))
        page.snack_bar.open = True
        page.update()

    def handle_purchase_date_change(e):
        purchase_date.value = e.control.value.strftime("%Y-%m-%d")
        page.update()

    def handle_purchase_date_dismissal(e):
        page.update()

    purchase_picker = ft.DatePicker(
        first_date=datetime.datetime(year=today.year - 1, month=1, day=1),
        last_date=datetime.datetime(year=today.year + 1, month=today.month, day=20),
        on_change=handle_purchase_date_change,
        on_dismiss=handle_purchase_date_dismissal,
    )

    def open_purchase_picker(e):
        page.show_dialog(purchase_picker)

    def load_suppliers():
        suppliers_map.clear()

        try:
            suppliers = get_suppliers()

            for supplier in suppliers:
                supplier_id = supplier[0]
                company_name = supplier[1]
                suppliers_map[company_name] = supplier_id

        except Exception as e:
            show_message(f"Could not load suppliers: {e}")

    def calculate_total(e=None):
        try:
            qty = float(quantity.value)
            cost = float(unit_cost.value)
            total = qty * cost
            total_text.value = f"Total Cost: {total:.2f}"
        except:
            total_text.value = "Total Cost: 0.00"

        page.update()

    def load_purchases():
        table_area.controls.clear()

        try:
            purchases_list = get_purchases()

            if not purchases_list:
                table_area.controls.append(ft.Text("No purchases saved yet."))
            else:
                rows = []

                for purchase in purchases_list:
                    rows.append(
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text(str(purchase[0]))),
                                ft.DataCell(ft.Text(str(purchase[1]))),
                                ft.DataCell(ft.Text(str(purchase[2]))),
                                ft.DataCell(ft.Text(str(purchase[3]))),
                                ft.DataCell(ft.Text(str(purchase[4]))),
                                ft.DataCell(ft.Text(str(purchase[5]))),
                                ft.DataCell(ft.Text(str(purchase[6]))),
                                ft.DataCell(ft.Text(str(purchase[7]))),
                            ]
                        )
                    )

                table_area.controls.append(
                    ft.DataTable(
                        columns=[
                            ft.DataColumn(ft.Text("ID")),
                            ft.DataColumn(ft.Text("Supplier")),
                            ft.DataColumn(ft.Text("Item")),
                            ft.DataColumn(ft.Text("Qty")),
                            ft.DataColumn(ft.Text("Unit Cost")),
                            ft.DataColumn(ft.Text("Total")),
                            ft.DataColumn(ft.Text("Date")),
                            ft.DataColumn(ft.Text("Status")),
                        ],
                        rows=rows
                    )
                )

            page.update()

        except Exception as e:
            show_message(f"Could not load purchases: {e}")

    def save_purchase(e):
        supplier_name = supplier_input.value.strip()
        item = item_name.value.strip()
        date = purchase_date.value.strip()
        purchase_status = status.value.strip()

        if not supplier_name or not item or not date:
            show_message("Fill all required fields.")
            return

        if supplier_name not in suppliers_map:
            show_message("That supplier does not exist.")
            return

        try:
            qty = float(quantity.value)
            cost = float(unit_cost.value)

            if qty <= 0 or cost <= 0:
                show_message("Quantity and Unit Cost must be positive.")
                return

            supplier_id = suppliers_map[supplier_name]

            add_purchase(
                supplier_id,
                item,
                qty,
                cost,
                date,
                purchase_status
            )

            supplier_input.value = ""
            item_name.value = ""
            quantity.value = ""
            unit_cost.value = ""
            purchase_date.value = ""
            status.value = ""
            total_text.value = "Total Cost: 0.00"

            load_purchases()
            show_message("Purchase saved successfully.")
            page.update()

        except Exception as e:
            show_message(f"Could not save purchase: {e}")

    def refresh_table(e):
        load_purchases()

    quantity.on_change = calculate_total
    unit_cost.on_change = calculate_total

    load_suppliers()
    load_purchases()

    return ft.Container(
        padding=20,
        content=ft.Column(
            controls=[
                ft.Text("Purchases", size=22, weight=ft.FontWeight.BOLD),
                ft.Row(
                    controls=[supplier_input, item_name],
                    wrap=True
                ),
                ft.Row(
                    controls=[
                        quantity,
                        unit_cost,
                        purchase_date,
                        ft.ElevatedButton(
                            "Pick date",
                            icon=ft.Icons.CALENDAR_MONTH,
                            on_click=open_purchase_picker,
                        ),
                        status,
                    ],
                    wrap=True
                ),
                total_text,
                ft.Row(
                    controls=[
                        ft.ElevatedButton("Save Purchase", on_click=save_purchase),
                        ft.OutlinedButton("Refresh Table", on_click=refresh_table),
                    ]
                ),
                ft.Divider(),
                ft.Text("Purchases List", size=18, weight=ft.FontWeight.BOLD),
                table_area,
            ],
            scroll=ft.ScrollMode.AUTO
        )
    )