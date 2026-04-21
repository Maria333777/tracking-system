import flet as ft
from models import add_purchase, get_purchases, get_suppliers, update_purchase, delete_purchase

def purchases_view(page: ft.Page):
    supplier_dropdown = ft.Dropdown(label="Supplier", width=220)
    item_name = ft.TextField(label="Item Name", width=220)
    quantity = ft.TextField(label="Quantity", width=120)
    unit_cost = ft.TextField(label="Unit Cost", width=120)
    purchase_date = ft.TextField(label="Purchase Date", hint_text="YYYY-MM-DD", width=180)

    status = ft.Dropdown(
        label="Status",
        width=180,
        options=[
            ft.dropdown.Option("Paid"),
            ft.dropdown.Option("Pending"),
            ft.dropdown.Option("Approved"),
        ]
    )

    total_text = ft.Text("Total Cost: 0.00")
    editing_id = None
    editing_text = ft.Text("Editing: none")
    table_area = ft.Column()
    suppliers_map = {}

    def show_message(text):
        page.snack_bar = ft.SnackBar(ft.Text(text))
        page.snack_bar.open = True
        page.update()

    def clear_form(e=None):
        nonlocal editing_id
        editing_id = None
        supplier_dropdown.value = None
        item_name.value = ""
        quantity.value = ""
        unit_cost.value = ""
        purchase_date.value = ""
        status.value = None
        total_text.value = "Total Cost: 0.00"
        editing_text.value = "Editing: none"
        page.update()

    def calculate_total(e=None):
        try:
            qty = float(quantity.value)
            cost = float(unit_cost.value)
            total_text.value = f"Total Cost: {qty * cost:.2f}"
        except:
            total_text.value = "Total Cost: 0.00"
        page.update()

    def load_suppliers():
        supplier_dropdown.options.clear()
        suppliers_map.clear()

        suppliers = get_suppliers()
        for supplier in suppliers:
            supplier_id = supplier[0]
            company_name = supplier[1]
            suppliers_map[company_name] = supplier_id
            supplier_dropdown.options.append(ft.dropdown.Option(company_name))

        page.update()

    def fill_form(purchase):
        nonlocal editing_id
        editing_id = purchase[0]
        supplier_dropdown.value = purchase[1]
        item_name.value = purchase[2]
        quantity.value = str(purchase[3])
        unit_cost.value = str(purchase[4])
        purchase_date.value = purchase[6]
        status.value = purchase[7]
        total_text.value = f"Total Cost: {float(purchase[5]):.2f}"
        editing_text.value = f"Editing purchase ID: {editing_id}"
        page.update()

    def save_purchase_data(e):
        supplier_name = supplier_dropdown.value
        item = item_name.value.strip()
        date = purchase_date.value.strip()
        purchase_status = status.value

        if not supplier_name or not item or not date:
            show_message("Fill all required fields.")
            return

        try:
            qty = float(quantity.value)
            cost = float(unit_cost.value)

            if qty <= 0 or cost <= 0:
                show_message("Quantity and unit cost must be positive.")
                return

            supplier_id = suppliers_map[supplier_name]
            add_purchase(supplier_id, item, qty, cost, date, purchase_status)

            clear_form()
            load_purchases()
            show_message("Purchase saved.")
        except Exception as error:
            show_message(f"Error: {error}")

    def update_purchase_data(e):
        if editing_id is None:
            show_message("Pick a purchase first.")
            return

        supplier_name = supplier_dropdown.value
        item = item_name.value.strip()
        date = purchase_date.value.strip()
        purchase_status = status.value

        if not supplier_name or not item or not date:
            show_message("Fill all required fields.")
            return

        try:
            qty = float(quantity.value)
            cost = float(unit_cost.value)

            if qty <= 0 or cost <= 0:
                show_message("Quantity and unit cost must be positive.")
                return

            supplier_id = suppliers_map[supplier_name]
            update_purchase(editing_id, supplier_id, item, qty, cost, date, purchase_status)

            clear_form()
            load_purchases()
            show_message("Purchase updated.")
        except Exception as error:
            show_message(f"Error: {error}")

    def remove_purchase(purchase_id):
        try:
            delete_purchase(purchase_id)
            clear_form()
            load_purchases()
            show_message("Purchase deleted.")
        except Exception as error:
            show_message(f"Error: {error}")

    def load_purchases():
        table_area.controls.clear()
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
                            ft.DataCell(
                                ft.TextButton(
                                    "Edit",
                                    on_click=lambda e, purchase=purchase: fill_form(purchase)
                                )
                            ),
                            ft.DataCell(
                                ft.TextButton(
                                    "Delete",
                                    on_click=lambda e, purchase_id=purchase[0]: remove_purchase(purchase_id)
                                )
                            ),
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
                        ft.DataColumn(ft.Text("Edit")),
                        ft.DataColumn(ft.Text("Delete")),
                    ],
                    rows=rows
                )
            )

        page.update()

    quantity.on_change = calculate_total
    unit_cost.on_change = calculate_total

    load_suppliers()
    load_purchases()

    return ft.Container(
        padding=20,
        content=ft.Column(
            controls=[
                ft.Text("Purchases", size=22, weight=ft.FontWeight.BOLD),
                editing_text,
                ft.Row([supplier_dropdown, item_name], wrap=True),
                ft.Row([quantity, unit_cost, purchase_date, status], wrap=True),
                total_text,
                ft.Row(
                    [
                        ft.ElevatedButton("Save", on_click=save_purchase_data),
                        ft.ElevatedButton("Update", on_click=update_purchase_data),
                        ft.OutlinedButton("Clear", on_click=clear_form),
                        ft.OutlinedButton("Refresh", on_click=lambda e: load_purchases()),
                    ],
                    wrap=True
                ),
                ft.Divider(),
                table_area,
            ],
            scroll=ft.ScrollMode.AUTO
        )
    )