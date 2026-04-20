import flet as ft
from models import add_supplier, get_suppliers, delete_supplier

def suppliers_view(page: ft.Page):
    company_name = ft.TextField(label="Company Name", width=250)
    phone = ft.TextField(label="Phone", width=200)
    email = ft.TextField(label="Email", width=250)

    table_area = ft.Column()
    selected_supplier_id = None

    def show_message(text):
        page.snack_bar = ft.SnackBar(ft.Text(text))
        page.snack_bar.open = True
        page.update()

    def select_supplier(supplier_id):
        nonlocal selected_supplier_id

        if selected_supplier_id == supplier_id:
            selected_supplier_id = None
        else:
            selected_supplier_id = supplier_id

        load_suppliers()

    def load_suppliers():
        table_area.controls.clear()

        try:
            suppliers = get_suppliers()

            if not suppliers:
                table_area.controls.append(ft.Text("No suppliers saved yet."))
            else:
                rows = []
                for supplier in suppliers:
                    rows.append(
                        ft.DataRow(
                            selected=(selected_supplier_id == supplier[0]),
                            on_select_changed=lambda e, supplier_id=supplier[0]: select_supplier(supplier_id),
                            cells=[
                                ft.DataCell(ft.Text(str(supplier[0]))),
                                ft.DataCell(ft.Text(str(supplier[1]))),
                                ft.DataCell(ft.Text(str(supplier[2]))),
                                ft.DataCell(ft.Text(str(supplier[3]))),
                            ]
                        )
                    )

                table_area.controls.append(
                    ft.DataTable(
                        show_checkbox_column=True,
                        columns=[
                            ft.DataColumn(ft.Text("ID")),
                            ft.DataColumn(ft.Text("Company")),
                            ft.DataColumn(ft.Text("Phone")),
                            ft.DataColumn(ft.Text("Email")),
                        ],
                        rows=rows
                    )
                )

            page.update()

        except Exception as e:
            show_message(f"Could not load suppliers: {e}")

    def save_supplier(e):
        name = company_name.value.strip()
        phone_value = phone.value.strip()
        email_value = email.value.strip()

        if name == "":
            show_message("Company name is required.")
            return

        try:
            add_supplier(name, phone_value, email_value)

            company_name.value = ""
            phone.value = ""
            email.value = ""

            load_suppliers()
            show_message("Supplier saved successfully.")

        except Exception as e:
            show_message(f"Could not save supplier: {e}")

    def delete_selected_supplier(e):
        nonlocal selected_supplier_id

        if selected_supplier_id is None:
            show_message("Select a supplier first.")
            return

        try:
            delete_supplier(selected_supplier_id)
            selected_supplier_id = None
            load_suppliers()
            show_message("Supplier deleted successfully.")
        except Exception as e:
            show_message(f"Could not delete supplier: {e}")

    load_suppliers()

    return ft.Container(
        padding=20,
        content=ft.Column(
            controls=[
                ft.Text("Suppliers", size=22, weight=ft.FontWeight.BOLD),
                ft.Row(
                    controls=[company_name, phone, email],
                    wrap=True
                ),
                ft.Row(
                    controls=[
                        ft.ElevatedButton("Save Supplier", on_click=save_supplier),
                        ft.OutlinedButton("Refresh Table", on_click=lambda e: load_suppliers()),
                        ft.FilledButton("Delete Selected", on_click=delete_selected_supplier),
                    ]
                ),
                ft.Divider(),
                ft.Text("Suppliers List", size=18, weight=ft.FontWeight.BOLD),
                table_area,
            ],
            scroll=ft.ScrollMode.AUTO
        )
    )