import datetime
import flet as ft
from models import add_purchase, get_purchases, get_suppliers

def purchases_view(page: ft.Page):
    supplier_name = ft.TextField(label="Supplier Name", width=220)
    item_name = ft.TextField(label="Item Name", width=200)
    quantity = ft.TextField(label="Quantity", width=120)
    unit_cost = ft.TextField(label="Unit Cost", width=120)
    purchase_date = ft.TextField(label="Purchase Date", width=180, read_only=True)
    status = ft.TextField(label="Status", width=150)

    total_text = ft.Text("Total Cost: 0", size=16, weight=ft.FontWeight.BOLD)
    table_area = ft.Column()
    suppliers_map = {}

    today = datetime.datetime.now()

    def show_message(text):
        page.snack_bar = ft.SnackBar(ft.Text(text))
        page.snack_bar.open = True
        page.update()

    def set_purchase_date(e):
        if e.control.value:
            purchase_date.value = e.control.value.strftime("%Y-%m-%d")
            page.update()

    purchase_picker = ft.DatePicker(
        first_date=datetime.datetime(year=today.year - 1, month=1, day=1),
        last_date=datetime.datetime(year=today.year + 1, month=12, day=31),
        entry_mode=ft.DatePickerEntryMode.INPUT,
        field_hint_text="yyyy-mm-dd",
        field_label_text="Enter purchase date",
        help_text="Select purchase date",
        on_change=set_purchase_date,
    )

    def open_purchase_picker(e):
        page.show_dialog(purchase_picker)

    def load_suppliers():
        suppliers_map.clear()

        try:
            suppliers = get_suppliers()
            for supplier in suppliers:
                supplier_id = supplier[0]
                company = supplier[1]
                suppliers_map[company] = supplier_id
        except Exception as error:
            show_message(f"Error loading suppliers: {error}")

    def calculate_total(e=None):
        try:
            qty = int(quantity.value)
            cost = int(unit_cost.value)
            total_text.value = f"Total Cost: {qty * cost}"
        except:
            total_text.value = "Total Cost: 0"

        page.update()

    def load_purchases():
        table_area.controls.clear()

        try:
            purchases = get_purchases()

            if not purchases:
                table_area.controls.append(ft.Text("No purchases yet."))
            else:
                rows = []

                for purchase in purchases:
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
                        rows=rows,
                    )
                )

            page.update()

        except Exception as error:
            show_message(f"Error loading purchases: {error}")

    def save_purchase(e):
        supplier = supplier_name.value.strip()
        item = item_name.value.strip()
        date = purchase_date.value.strip()
        stat = status.value.strip()

        if supplier == "" or item == "" or date == "":
            show_message("Fill all required fields.")
            return

        if supplier not in suppliers_map:
            show_message("That supplier does not exist.")
            return

        try:
            qty = int(quantity.value)
            cost = int(unit_cost.value)
        except:
            show_message("Quantity and Unit Cost must be whole numbers.")
            return

        if qty <= 0 or cost <= 0:
            show_message("Quantity and Unit Cost must be positive.")
            return

        try:
            supplier_id = suppliers_map[supplier]

            add_purchase(
                supplier_id,
                item,
                qty,
                cost,
                date,
                stat
            )

            supplier_name.value = ""
            item_name.value = ""
            quantity.value = ""
            unit_cost.value = ""
            purchase_date.value = ""
            status.value = ""
            total_text.value = "Total Cost: 0"

            load_purchases()
            show_message("Purchase saved.")
            page.update()

        except Exception as error:
            show_message(f"Error saving purchase: {error}")

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
                    controls=[supplier_name, item_name],
                    wrap=True
                ),
                ft.Row(
                    controls=[
                        quantity,
                        unit_cost,
                        purchase_date,
                        ft.Button(
                            icon=ft.Icons.CALENDAR_MONTH,
                            content="Pick date",
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