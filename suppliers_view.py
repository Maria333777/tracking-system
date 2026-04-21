import flet as ft
from models import add_supplier, get_suppliers, update_supplier, delete_supplier

def suppliers_view(page: ft.Page):
    company_name = ft.TextField(label="Company Name", width=230)
    phone = ft.TextField(label="Phone", width=180)
    email = ft.TextField(label="Email", width=230)

    editing_id = None
    editing_text = ft.Text("Editing: none")
    table_area = ft.Column()

    def show_message(text):
        page.snack_bar = ft.SnackBar(ft.Text(text))
        page.snack_bar.open = True
        page.update()

    def clear_form(e=None):
        nonlocal editing_id
        editing_id = None
        company_name.value = ""
        phone.value = ""
        email.value = ""
        editing_text.value = "Editing: none"
        page.update()

    def fill_form(supplier):
        nonlocal editing_id
        editing_id = supplier[0]
        company_name.value = supplier[1] or ""
        phone.value = supplier[2] or ""
        email.value = supplier[3] or ""
        editing_text.value = f"Editing supplier ID: {editing_id}"
        page.update()

    def save_supplier_data(e):
        name = company_name.value.strip()
        phone_value = phone.value.strip()
        email_value = email.value.strip()

        if name == "":
            show_message("Company name is required.")
            return

        try:
            add_supplier(name, phone_value, email_value)
            clear_form()
            load_suppliers()
            show_message("Supplier saved.")
        except Exception as error:
            show_message(f"Error: {error}")

    def update_supplier_data(e):
        if editing_id is None:
            show_message("Pick a supplier first.")
            return

        name = company_name.value.strip()
        phone_value = phone.value.strip()
        email_value = email.value.strip()

        if name == "":
            show_message("Company name is required.")
            return

        try:
            update_supplier(editing_id, name, phone_value, email_value)
            clear_form()
            load_suppliers()
            show_message("Supplier updated.")
        except Exception as error:
            show_message(f"Error: {error}")

    def remove_supplier(supplier_id):
        try:
            delete_supplier(supplier_id)
            clear_form()
            load_suppliers()
            show_message("Supplier deleted.")
        except Exception as error:
            show_message(f"Error: {error}")

    def refresh_table(e):
        load_suppliers()

    def make_edit_handler(supplier):
        def edit_handler(e):
            fill_form(supplier)
        return edit_handler

    def make_delete_handler(supplier_id):
        def delete_handler(e):
            remove_supplier(supplier_id)
        return delete_handler

    def load_suppliers():
        table_area.controls.clear()
        suppliers = get_suppliers()

        if not suppliers:
            table_area.controls.append(ft.Text("No suppliers yet."))
        else:
            rows = []

            for supplier in suppliers:
                rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(supplier[0]))),
                            ft.DataCell(ft.Text(str(supplier[1]))),
                            ft.DataCell(ft.Text(str(supplier[2]))),
                            ft.DataCell(ft.Text(str(supplier[3]))),
                            ft.DataCell(
                                ft.TextButton(
                                    "Edit",
                                    on_click=make_edit_handler(supplier)
                                )
                            ),
                            ft.DataCell(
                                ft.TextButton(
                                    "Delete",
                                    on_click=make_delete_handler(supplier[0])
                                )
                            ),
                        ]
                    )
                )

            table_area.controls.append(
                ft.DataTable(
                    columns=[
                        ft.DataColumn(ft.Text("ID")),
                        ft.DataColumn(ft.Text("Company")),
                        ft.DataColumn(ft.Text("Phone")),
                        ft.DataColumn(ft.Text("Email")),
                        ft.DataColumn(ft.Text("Edit")),
                        ft.DataColumn(ft.Text("Delete")),
                    ],
                    rows=rows
                )
            )

        page.update()

    load_suppliers()

    return ft.Container(
        padding=20,
        content=ft.Column(
            controls=[
                ft.Text("Suppliers", size=22, weight=ft.FontWeight.BOLD),
                editing_text,
                ft.Row([company_name, phone, email], wrap=True),
                ft.Row(
                    [
                        ft.ElevatedButton("Save", on_click=save_supplier_data),
                        ft.ElevatedButton("Update", on_click=update_supplier_data),
                        ft.OutlinedButton("Clear", on_click=clear_form),
                        ft.OutlinedButton("Refresh", on_click=refresh_table),
                    ],
                    wrap=True
                ),
                ft.Divider(),
                table_area,
            ],
            scroll=ft.ScrollMode.AUTO
        )
    )